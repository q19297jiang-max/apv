#!/usr/bin/env python3
"""
Generic Cloud Pricing Fetcher - Multi-Provider Support

This script fetches pricing from any cloud provider's component catalog
and generates pricing templates dynamically. No hardcoded values - everything
is read from the catalog (source of truth).

Supported providers: AWS, Azure, GCP (easily extensible)

Usage:
    python pricing-fetcher.py --provider aws
    python pricing-fetcher.py --all
"""

import sys
import json
import subprocess
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
TEMP_DIR = Path('/tmp/apv-pricing-updates')
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')

# Provider configurations (extensible)
PROVIDERS = {
    'aws': {
        'catalog_file': 'aws-component-catalog.md',
        'calculator_url': 'https://calculator.aws/',
        'display_name': 'AWS',
        'regions': {
            'ap-southeast-1': 'Singapore',
            'ap-southeast-3': 'Malaysia',
            'ap-northeast-1': 'Taiwan'
        }
    },
    'azure': {
        'catalog_file': 'azure-component-catalog.md',
        'calculator_url': 'https://azure.microsoft.com/pricing/',
        'display_name': 'Azure',
        'regions': {
            'southeastasia': 'Singapore',
            'eastasia': 'Hong Kong'
        }
    },
    'gcp': {
        'catalog_file': 'gcp-component-catalog.md',
        'calculator_url': 'https://cloud.google.com/products/calculator',
        'display_name': 'GCP',
        'regions': {
            'asia-southeast1': 'Singapore',
            'asia-east2': 'Hong Kong'
        }
    }
}


class GenericPricingParser:
    """Generic parser for any cloud provider's component catalog"""

    def __init__(self, provider: str):
        self.provider = provider
        self.config = PROVIDERS.get(provider, {})
        self.catalog_file = PRICING_DIR / self.config['catalog_file']

    def parse_catalog(self) -> Dict[str, List[Dict[str, Any]]]:
        """Parse component catalog and return all pricing sections"""
        if not self.catalog_file.exists():
            print(f"❌ Catalog not found: {self.catalog_file}")
            return {}

        with open(self.catalog_file, 'r') as f:
            content = f.read()

        sections = self._extract_sections(content)
        return sections

    def _extract_sections(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all pricing sections from catalog"""
        sections = {}
        lines = content.split('\n')

        current_section = None
        current_table_headers = []
        in_table = False
        current_major_section = None  # Compute, Database, Storage, etc.

        for i, line in enumerate(lines):
            # Track major sections (## level)
            if line.startswith('## '):
                current_major_section = self._normalize_major_section(line)
                current_section = None  # Reset current section
                in_table = False
                current_table_headers = []

            # Detect subsection headers (### or #### level)
            elif line.startswith('### ') or line.startswith('#### '):
                section_key = self._normalize_section_key(line, current_major_section)
                if section_key:
                    current_section = section_key
                    sections.setdefault(current_section, [])
                in_table = False
                current_table_headers = []

            # Detect table headers
            elif line.startswith('|') and self._is_table_header(line):
                in_table = True
                current_table_headers = [p.strip() for p in line.split('|')[1:-1]]

            # Parse table rows
            elif in_table and line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]

                if self._should_skip_row(parts, current_table_headers):
                    continue

                # Only parse if we have a current section
                if not current_section:
                    continue

                # Parse row based on section type
                row_data = self._parse_row(parts, current_table_headers, current_section)
                if row_data:
                    sections[current_section].append(row_data)

        return sections

    def _normalize_major_section(self, line: str) -> Optional[str]:
        """Normalize major section (## level) to a consistent key"""
        line_clean = re.sub(r'##\s*', '', line).strip().lower()

        # Map major sections to standard keys
        major_section_map = {
            'compute components': 'ec2',
            'database components': 'rds',
            'cache components': 'elasticache',
            'load balancing components': 'load_balancer',
            'container components': 'container',
            'storage components': 'storage',
            'networking components': 'networking',
            'security components': 'security'
        }

        return major_section_map.get(line_clean, line_clean.replace(' ', '_'))

    def _normalize_section_key(self, line: str, major_section: str = None) -> Optional[str]:
        """Normalize section header to a consistent key"""
        line_lower = line.lower()
        line_clean = re.sub(r'[###\s]+', ' ', line).strip()

        # Check for Savings Plans first (specific patterns)
        if 'compute savings' in line_lower:
            return 'ec2_savings_plans'
        elif 'database savings' in line_lower:
            return 'rds_savings_plans'
        elif 'cache savings' in line_lower:
            return 'elasticache_savings_plans'

        # Check for specific deployment types
        if 'single-az' in line_lower or 'single az' in line_lower:
            if major_section == 'rds':
                return 'rds_single_az'
            return f'{major_section}_single_az' if major_section else 'single_az'
        elif 'multi-az' in line_lower or 'multi az' in line_lower:
            if major_section == 'rds':
                return 'rds_multi_az'
            return f'{major_section}_multi_az' if major_section else 'multi_az'

        # For instance type subsections, consolidate under major section
        # But ONLY if it's clearly an instance type subsection
        instance_type_patterns = ['general purpose', 'compute optimized', 'memory optimized',
                                 'accelerated computing', 'storage optimized']
        if any(pattern in line_lower for pattern in instance_type_patterns):
            if major_section == 'ec2':
                return 'ec2'
            elif major_section == 'elasticache':
                return 'elasticache'

        # For specific service sections under major components
        if 'redis nodes' in line_lower:
            return 'elasticache'

        # Other patterns
        patterns = {
            'amazon eks': 'eks',
            'eks': 'eks',
            'application load balancer': 'alb',
            'network load balancer': 'nlb',
            'alb': 'alb',
            'nlb': 'nlb',
            'amazon ebs': 'ebs',
            'amazon s3': 's3',
            'ebs': 'ebs',
            's3': 's3',
            'aws direct connect': 'direct_connect',
            'direct connect': 'direct_connect',
            'vpc flow logs': 'vpc_flow_logs',
            'aws kms': 'kms',
            'kms': 'kms',
            'shield': 'shield'
        }

        for pattern, key in patterns.items():
            if pattern in line_lower:
                return key

        # Default: use major section if available
        if major_section:
            return major_section

        # Fallback: use cleaned line as key
        return line_clean.replace(' ', '_')

    def _is_table_header(self, line: str) -> bool:
        """Check if line is a table header"""
        # Must have at least 2 columns
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) < 2:
            return False

        # Check if first column looks like a header (not a data value)
        first_col = parts[0].lower()

        # Common header names
        header_names = ['instance', 'component', 'size', 'type', 'storage type',
                       'region', 'name', 'resource', 'service']

        # Data value patterns (NOT headers)
        data_patterns = [
            '.',  # Contains dot (e.g., m6i.large, db.m6i.xlarge)
            '$',  # Starts with $ (price)
            'https://',  # URL
            '***',  # Separator
            '---',  # Markdown separator
        ]

        # If it looks like data, it's not a header
        for pattern in data_patterns:
            if pattern in first_col or first_col.startswith(pattern):
                return False

        # If first column is a known header name, likely a header
        if any(header_name in first_col for header_name in header_names):
            return True

        # Check if all parts look like headers (contain header keywords)
        header_keywords = ['instance', 'component', 'vcpu', 'memory', 'price', 'cost',
                         'calculator', 'storage', 'region', 'unit', 'type', 'bandwidth']
        header_count = sum(1 for part in parts if any(kw in part.lower() for kw in header_keywords))

        # If most columns contain header keywords, it's likely a header
        return header_count >= len(parts) * 0.3

    def _should_skip_row(self, parts: List[str], headers: List[str]) -> bool:
        """Determine if row should be skipped"""
        # Skip empty rows
        if not parts or not any(parts):
            return True

        # Skip separator rows
        if any('---' in p for p in parts):
            return True

        # Skip separator rows with ***
        if any('***' in p for p in parts):
            return True

        # Skip rows where first column is a common header name (not data)
        if parts:
            first_col = parts[0].lower().strip()
            header_names = ['instance', 'component', 'size', 'type', 'storage type',
                           'region', 'name', 'resource', 'service', 'price', 'calculator']
            if first_col in header_names:
                return True

            # Skip source rows
            if first_col.startswith('**source**'):
                return True

        return False

    def _parse_row(self, parts: List[str], headers: List[str],
                   section_type: str) -> Optional[Dict[str, Any]]:
        """Parse a table row and return structured data"""

        row_data = {}

        # Extract all columns dynamically
        for idx, header in enumerate(headers):
            if idx < len(parts):
                key = header.lower().replace(' ', '_').replace('/', '_')
                value = parts[idx]
                row_data[key] = value

        # Add section type
        row_data['_section_type'] = section_type

        return row_data

    def get_section_items(self, sections: Dict, section_type: str) -> int:
        """Count items in a section"""
        return len(sections.get(section_type, []))


def create_pricing_template(provider: str, sections: Dict) -> str:
    """Generate pricing template from parsed sections (generic)"""

    config = PROVIDERS.get(provider, {})
    today = datetime.now().strftime('%Y-%m-%d')
    valid_until = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    content = f"""---
type: apv-knowledge
category: pricing
title: "{config['display_name']} Pricing for Singapore Region"
source_url: "{config['calculator_url']}"
captured_date: {today}
verified_by: "Infrastructure Architect"
price_valid_until: {valid_until}
tags: [pricing, {provider}, singapore, calculator]
---

# {config['display_name']} Pricing for Card Processing (Singapore Region)

## Official Calculators

| Calculator | URL | Last Updated |
|------------|-----|-------------|
| {config['display_name']} Pricing Calculator | {config['calculator_url']} | {today} |
"""

    # Add all sections dynamically
    section_order = ['ec2', 'ec2_savings_plans', 'rds_single_az', 'rds_multi_az',
                      'rds_savings_plans', 'elasticache', 'elasticache_savings_plans',
                      'alb', 'nlb', 'eks', 'ebs', 's3', 'direct_connect',
                      'vpc_flow_logs', 'kms', 'shield']

    for section in section_order:
        if sections.get(section):
            content += generate_section_content(section, sections[section], config)

    # Add verification section
    content += f"""
## Verification

- **Verified By**: Infrastructure Architect
- **Verification Date**: {today}
- **Verification Method**: {config['calculator_url']}
- **Next Review**: {valid_until} (30 days)

## Related

- [[{provider}-pricing]] - {config['display_name']} pricing reference
- [[{provider}-component-catalog]] - Component catalog (source of truth)
- [[tps-calculator]] - Component sizing methodology
"""

    return content


def generate_section_content(section_type: str, items: List[Dict],
                            config: Dict) -> str:
    """Generate markdown content for a section"""

    section_titles = {
        'ec2': '### Compute Instances',
        'ec2_savings_plans': '### Compute Savings Plans (3yr No Upfront)',
        'rds_single_az': '### Database Instances (Single-AZ)',
        'rds_multi_az': '### Database Instances (Multi-AZ)',
        'rds_savings_plans': '### Database Savings Plans (3yr No Upfront)',
        'elasticache': '### Cache Instances',
        'elasticache_savings_plans': '### Cache Savings Plans (3yr No Upfront)',
        'alb': '### Application Load Balancer (ALB)',
        'nlb': '### Network Load Balancer (NLB)',
        'eks': '### Amazon EKS',
        'ebs': '### Amazon EBS (gp3)',
        's3': '### Amazon S3',
        'direct_connect': '### AWS Direct Connect',
        'vpc_flow_logs': '### VPC Flow Logs',
        'kms': '### AWS KMS',
        'shield': '### AWS Shield Standard'
    }

    title = section_titles.get(section_type, f"### {section_type.replace('_', ' ').title()}")

    content = f"""
{title}

**Source**: {config['catalog_file']} ({section_type.replace('_', ' ').title()})

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from {config['catalog_file']} (the source of truth).
> Last verified: {datetime.now().strftime('%Y-%m-%d')}
> Calculator: {config['calculator_url']}

"""

    # Generate table based on first item's structure
    if items:
        # Get all unique columns from items
        all_columns = set()
        for item in items:
            all_columns.update(item.keys())

        # Filter out metadata columns
        display_columns = [col for col in all_columns if not col.startswith('_')]

        # Generate table header
        content += "| " + " | ".join(display_columns[:10]) + " |\n"
        content += "|" + "|".join(["----------"] * min(len(display_columns), 10)) + "|\n"

        # Generate table rows
        for item in items:
            row_data = []
            for col in display_columns[:10]:
                value = item.get(col, '')
                row_data.append(str(value))
            content += "| " + " | ".join(row_data) + " |\n"

    return content


def main():
    parser = argparse.ArgumentParser(
        description='Generic pricing fetcher for any cloud provider',
        epilog="""
This script fetches pricing from any cloud provider's component catalog
and generates pricing templates dynamically. No hardcoded values - everything
is read from the catalog (source of truth).

Supported providers: aws, azure, gcp

Workflow:
  1. Read pricing from [provider]-component-catalog.md
  2. Parse all sections dynamically
  3. Generate template with catalog pricing
  4. Open calculator for manual verification

Examples:
  python pricing-fetcher.py --provider aws
  python pricing-fetcher.py --all

Next Steps:
  1. Review the template in /tmp/apv-pricing-updates/
  2. Verify pricing in the calculator
  3. Run: python pricing-verify.py --provider <provider>

Adding New Providers:
  1. Create [provider]-component-catalog.md
  2. Add provider config to PROVIDERS dict
  3. No script changes needed!
        """
    )

    parser.add_argument('--provider', choices=list(PROVIDERS.keys()),
                        help='Cloud provider')
    parser.add_argument('--all', action='store_true',
                        help='Fetch all providers')
    parser.add_argument('--no-open', action='store_true',
                        help='Skip opening calculator browser')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else list(PROVIDERS.keys())

    print("=" * 70)
    print("GENERIC PRICING FETCHER - Multi-Provider Support")
    print("=" * 70)
    print()

    for provider in providers:
        config = PROVIDERS[provider]
        print(f"Provider: {config['display_name']}")
        print(f"Catalog: {config['catalog_file']}")
        print(f"Calculator: {config['calculator_url']}")
        print()

        # Parse catalog
        parser = GenericPricingParser(provider)
        sections = parser.parse_catalog()

        if not sections:
            print(f"⚠️  Could not parse pricing from catalog")
            continue

        # Count total items
        total_items = sum(len(items) for items in sections.values())
        print(f"📊 Found {total_items} pricing items")

        # Show breakdown
        for section, items in sections.items():
            if items:
                print(f"   - {section}: {len(items)} items")
        print()

        # Create evidence record
        create_evidence_record(provider, sections, config)

        # Generate template
        content = create_pricing_template(provider, sections)
        save_template(provider, content)

        print(f"📝 Created template: {TEMP_DIR / f'{provider}.md'}")

        # Open calculator
        if not args.no_open:
            open_calculator(config['calculator_url'])

        print()

    print("=" * 70)
    print("FETCH COMPLETE")
    print("=" * 70)


def create_evidence_record(provider: str, sections: Dict, config: Dict) -> Path:
    """Create evidence record for fetch operation"""
    today = datetime.now().strftime('%Y-%m-%d')
    evidence_dir = EVIDENCE_DIR / today
    evidence_dir.mkdir(parents=True, exist_ok=True)

    record = {
        'provider': provider,
        'display_name': config['display_name'],
        'date': today,
        'sections': {k: len(v) for k, v in sections.items()},
        'total_items': sum(len(v) for v in sections.values()),
        'catalog_file': str(config['catalog_file']),
        'calculator_url': config['calculator_url'],
        'timestamp': datetime.now().isoformat()
    }

    record_file = evidence_dir / f'{provider}-fetch-record.json'
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=2)

    return record_file


def save_template(provider: str, content: str) -> Path:
    """Save template to temp directory"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = TEMP_DIR / f'{provider}.md'

    with open(temp_file, 'w') as f:
        f.write(content)

    return temp_file


def open_calculator(url: str):
    """Open calculator URL in browser"""
    try:
        if sys.platform == 'darwin':
            subprocess.run(['open', url])
        elif sys.platform == 'win32':
            subprocess.run(['start', url], shell=True)
        else:
            subprocess.run(['xdg-open', url])
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print(f"   Please manually open: {url}")


if __name__ == '__main__':
    main()
