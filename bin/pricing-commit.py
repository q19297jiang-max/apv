#!/usr/bin/env python3
"""
APV Pricing Commit - Commit verified pricing to knowledge base

This script commits verified pricing updates to the APV knowledge base:
1. Reads verified pricing from temp directory
2. Checks that verification report exists
3. VALIDATES against component catalog (NEW)
4. Commits to wiki/apv/knowledge/pricing/
5. Creates final evidence summary
6. Runs freshness check to confirm

Usage:
    python pricing-commit.py --provider aws
    python pricing-commit.py --all

WARNING: Only run this script AFTER verification!
"""

import sys
import json
import shutil
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
TEMP_DIR = Path('/tmp/apv-pricing-updates')
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')
COMPONENT_CATALOG = PRICING_DIR / 'aws-component-catalog.md'

# Frontmatter template
FRONTMATTER_TEMPLATE = """---
type: apv-knowledge
category: pricing
title: "{title}"
source_url: "{source_url}"
source_api: "{source_api}"
captured_date: {captured_date}
verified_by: "{verified_by}"
price_valid_until: {price_valid_until}
tags: [pricing, {provider}, singapore, calculator]
---
"""


class PricingCommitter:
    """Commit verified pricing to knowledge base"""

    def __init__(self, provider: str):
        self.provider = provider
        self.today = datetime.now()
        self.today_str = self.today.strftime('%Y-%m-%d')
        self.valid_until = (self.today + timedelta(days=30)).strftime('%Y-%m-%d')
        self.temp_file = TEMP_DIR / f'{self.provider}.md'
        self.target_file = PRICING_DIR / f'{self.provider}.md'
        self.verification_report = EVIDENCE_DIR / self.today_str / f'{self.provider}-verification-report.json'

    def check_prerequisites(self) -> bool:
        """Check that all prerequisites are met"""
        print(f"Checking prerequisites for {self.provider}...")
        print()

        # Check temp file exists
        if not self.temp_file.exists():
            print(f"❌ No fetched pricing found")
            print(f"   Expected: {self.temp_file}")
            print(f"   Run: python pricing-fetcher.py --provider {self.provider}")
            return False
        print(f"✅ Fetched pricing found: {self.temp_file}")

        # Check verification report exists
        if not self.verification_report.exists():
            print(f"❌ No verification report found")
            print(f"   Expected: {self.verification_report}")
            print(f"   Run: python pricing-verify.py --provider {self.provider}")
            return False
        print(f"✅ Verification report found: {self.verification_report}")

        # Load verification report
        with open(self.verification_report, 'r') as f:
            self.verification_data = json.load(f)

        verified_count = sum(1 for r in self.verification_data.get('results', [])
                           if r.get('status') == 'verified')

        if verified_count == 0:
            print(f"⚠️  No items verified in report")
            response = input("Proceed anyway? [Y]es [N]o: ").strip().upper()
            if response != 'Y':
                return False

        print(f"✅ Verified items: {verified_count}")
        print()
        return True

    def read_component_catalog_pricing(self) -> Dict[str, Dict[str, any]]:
        """Read pricing from aws-component-catalog.md (source of truth)"""
        if not COMPONENT_CATALOG.exists():
            return {}

        catalog_pricing = {}
        with open(COMPONENT_CATALOG, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        current_section = None

        for i, line in enumerate(lines):
            # Detect section headers
            if line.startswith('### ') or line.startswith('## '):
                if 'EC2' in line or 'Compute' in line:
                    current_section = 'ec2'
                elif 'RDS' in line or 'PostgreSQL' in line or 'Database' in line:
                    current_section = 'rds'
                elif 'ElastiCache' in line or 'Redis' in line or 'Cache' in line:
                    current_section = 'elasticache'
                elif 'EKS' in line or 'Container' in line:
                    current_section = 'eks'
                elif 'Load Balancing' in line or 'ALB' in line or 'NLB' in line:
                    current_section = 'elb'

            # Parse pricing tables
            if line.startswith('|') and ('Price/Hour' in line or 'Price' in line):
                for j in range(i + 2, len(lines)):
                    row = lines[j]
                    if not row.startswith('|'):
                        break
                    if '---' in row:
                        continue

                    parts = [p.strip() for p in row.split('|')[1:-1]]
                    if len(parts) >= 6 and parts[0] not in ['Instance', 'Component', '']:
                        name = parts[0]
                        price_str = parts[4] if len(parts) > 4 else ''

                        # Extract price value
                        price_match = re.search(r'\$?([\d,]+\.?\d*)', price_str.replace(',', ''))
                        if price_match:
                            price_float = float(price_match.group(1))

                            catalog_pricing[name] = {
                                'name': name,
                                'price_hour': price_float,
                                'vcpu': parts[1] if len(parts) > 1 else '',
                                'memory': parts[2] if len(parts) > 2 else '',
                                'section': current_section,
                                'is_multi_az': 'Multi-AZ' in lines[max(0, i-5):i] or 'Multi-AZ' in line
                            }

        return catalog_pricing

    def parse_price_from_string(self, price_str: str) -> Optional[float]:
        """Extract numeric price from string like '$1.148' or '$837.90'"""
        if not price_str:
            return None
        clean = price_str.replace('$', '').replace(',', '').strip()
        match = re.search(r'([\d,]+\.?\d*)', clean)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return None

    def validate_against_catalog(self) -> bool:
        """Validate pricing against component catalog before committing"""
        if self.provider != 'aws':
            # Skip validation for non-AWS providers (no component catalog)
            return True

        if not COMPONENT_CATALOG.exists():
            print(f"⚠️  Component catalog not found: {COMPONENT_CATALOG}")
            print("   Skipping catalog validation")
            return True

        print("=" * 60)
        print("PRE-COMMIT VALIDATION")
        print("=" * 60)
        print()

        # Read temp file pricing
        with open(self.temp_file, 'r') as f:
            temp_content = f.read()

        temp_pricing = {}
        # Parse pricing from temp file (RDS Multi-AZ section)
        for line in temp_content.split('\n'):
            if '|' in line and 'db.' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5 and parts[0].startswith('db.'):
                    name = parts[0].replace('**', '').replace('*', '').strip()
                    price_str = parts[4] if len(parts) > 4 else ''
                    price = self.parse_price_from_string(price_str)
                    if price:
                        temp_pricing[name] = price

        # Read catalog pricing
        catalog_pricing = self.read_component_catalog_pricing()

        print(f"Component Catalog: {COMPONENT_CATALOG}")
        print(f"  Found {len(catalog_pricing)} items")
        print()
        print(f"Temp File: {self.temp_file}")
        print(f"  Found {len(temp_pricing)} items")
        print()

        # Check for critical RDS Multi-AZ pricing
        critical_instances = ['db.m6i.xlarge', 'db.r6i.xlarge', 'db.m6i.large', 'db.r6i.large']

        validation_passed = True
        for instance in critical_instances:
            if instance in temp_pricing:
                temp_price = temp_pricing[instance]
                catalog_price = catalog_pricing.get(instance, {}).get('price_hour')

                if catalog_price:
                    # Check if temp price is approximately 2x catalog (Multi-AZ)
                    expected_multi_az = catalog_price * 2
                    tolerance = expected_multi_az * 0.3  # 30% tolerance

                    if abs(temp_price - expected_multi_az) > tolerance:
                        print(f"⚠️  {instance}:")
                        print(f"    Catalog (Single-AZ): ${catalog_price:.3f}/hour")
                        print(f"    Expected Multi-AZ:    ~${expected_multi_az:.3f}/hour (2x)")
                        print(f"    Temp File:            ${temp_price:.3f}/hour")
                        print(f"    Difference:           {abs(temp_price - expected_multi_az):.3f} ({abs(temp_price - expected_multi_az)/expected_multi_az*100:.1f}%)")
                        print()
                        validation_passed = False
                    else:
                        print(f"✅ {instance}: ${temp_price:.3f}/hour (Multi-AZ validated)")

        if validation_passed:
            print()
            print("✅ Pre-commit validation passed")
            return True
        else:
            print()
            print("❌ Pre-commit validation FAILED")
            print()
            print("Possible issues:")
            print("  1. Temp file has incorrect Multi-AZ pricing")
            print("  2. Component catalog is outdated")
            print("  3. Calculator pricing has changed")
            print()
            print("Recommendations:")
            print("  1. Run: python pricing-fetcher.py --provider aws")
            print("  2. Verify in calculator: https://calculator.aws/")
            print("  3. Update component catalog if calculator is correct")
            print()

            response = input("Proceed anyway? [Y]es [N]o: ").strip().upper()
            return response == 'Y'

    def backup_existing_pricing(self):
        """Backup existing pricing file before overwriting"""
        if self.target_file.exists():
            backup_dir = PRICING_DIR / 'backups'
            backup_dir.mkdir(exist_ok=True)
            backup_file = backup_dir / f"{self.provider}.{self.today_str}.md"

            shutil.copy2(self.target_file, backup_file)
            print(f"📦 Backed up existing pricing to: {backup_file}")

    def commit_pricing(self) -> bool:
        """Commit pricing to knowledge base"""
        print(f"Committing {self.provider} pricing to knowledge base...")
        print()

        # NEW: Run pre-commit validation
        if not self.validate_against_catalog():
            print("⚠️  Commit cancelled due to validation failure")
            return False

        print()
        print("Writing to knowledge base...")

        # Read temp file
        with open(self.temp_file, 'r') as f:
            content = f.read()

        # Ensure frontmatter has correct dates
        lines = content.split('\n')
        new_lines = []
        in_frontmatter = False
        frontmatter_updated = False

        for line in lines:
            if line == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                new_lines.append(line)
                continue
            else:
                if in_frontmatter:
                    in_frontmatter = False
                    new_lines.append(line)
                    continue

            if in_frontmatter:
                # Update frontmatter fields
                if line.startswith('captured_date:'):
                    new_lines.append(f'captured_date: {self.today_str}')
                    frontmatter_updated = True
                elif line.startswith('price_valid_until:'):
                    new_lines.append(f'price_valid_until: {self.valid_until}')
                    frontmatter_updated = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        content = '\n'.join(new_lines)

        # Write to target file
        self.target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.target_file, 'w') as f:
            f.write(content)

        print(f"✅ Committed to: {self.target_file}")
        print()

        return True

    def create_evidence_summary(self):
        """Create final evidence summary"""
        summary = {
            'provider': self.provider,
            'commit_date': self.today_str,
            'committed_by': 'Infrastructure Architect',
            'verification_report': str(self.verification_report),
            'pricing_file': str(self.target_file),
            'price_valid_until': self.valid_until,
            'verification_results': self.verification_data.get('results', [])
        }

        summary_file = EVIDENCE_DIR / self.today_str / f'{self.provider}-commit-summary.json'

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"📁 Evidence summary: {summary_file}")
        return summary_file

    def display_commit_summary(self):
        """Display commit summary"""
        print("=" * 60)
        print("COMMIT SUMMARY")
        print("=" * 60)
        print()
        print(f"Provider:         {self.provider.upper()}")
        print(f"Commit Date:      {self.today_str}")
        print(f"Price Valid Until: {self.valid_until}")
        print(f"Pricing File:     {self.target_file}")
        print(f"Evidence:         {EVIDENCE_DIR / self.today_str}")
        print()
        print("Next Steps:")
        print(f"  1. Review committed pricing: {self.target_file}")
        print(f"  2. Run freshness check: python check-freshness.py {PRICING_DIR}")
        print(f"  3. Commit to git: git add {self.target_file}")
        print()

    def run_freshness_check(self):
        """Run freshness check to confirm pricing is fresh"""
        print("Running freshness check...")
        print()

        # This would call the existing check-freshness.py script
        # For now, just verify the file was updated correctly
        with open(self.target_file, 'r') as f:
            content = f.read()

        if f'captured_date: {self.today_str}' in content:
            print(f"✅ Pricing is fresh (captured: {self.today_str})")
            return True
        else:
            print(f"⚠️  Warning: Captured date may not be updated correctly")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Commit verified pricing to knowledge base',
        epilog="""
Examples:
  python pricing-commit.py --provider aws
  python pricing-commit.py --all

WARNING: Only run AFTER verification!
Workflow:
  1. python pricing-fetcher.py --provider aws
  2. python pricing-verify.py --provider aws
  3. python pricing-commit.py --provider aws  ← You are here
        """
    )
    parser.add_argument('--provider', choices=['aws', 'azure', 'gcp'],
                        help='Cloud provider')
    parser.add_argument('--all', action='store_true',
                        help='Commit all providers')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else ['aws', 'azure', 'gcp']

    print("=" * 60)
    print("APV PRICING COMMIT")
    print("=" * 60)
    print()

    all_passed = True
    for provider in providers:
        committer = PricingCommitter(provider)

        if not committer.check_prerequisites():
            all_passed = False
            continue

        committer.backup_existing_pricing()

        if committer.commit_pricing():
            committer.create_evidence_summary()
            committer.display_commit_summary()
            committer.run_freshness_check()

        print()

    if all_passed:
        print("=" * 60)
        print("✅ ALL COMMITS COMPLETE")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("⚠️  SOME COMMITS FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
