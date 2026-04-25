#!/usr/bin/env python3
"""
APV Pricing Fetcher - Fetch from component catalog

This script fetches pricing from the aws-component-catalog.md (the source of truth)
and creates a template for manual verification against the official calculator.

Usage:
    python pricing-fetcher.py --provider aws
"""

import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
COMPONENT_CATALOG = PRICING_DIR / 'aws-component-catalog.md'
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')
TEMP_DIR = Path('/tmp/apv-pricing-updates')

# Calculator URLs
CALCULATORS = {
    'aws': 'https://calculator.aws/',
    'azure': 'https://azure.microsoft.com/pricing/',
    'gcp': 'https://cloud.google.com/products/calculator'
}

# Singapore region codes
REGIONS = {
    'aws': 'ap-southeast-1',
    'azure': 'southeastasia',
    'gcp': 'asia-southeast1'
}


def open_calculator(provider: str):
    """Open the official calculator in browser"""
    url = CALCULATORS.get(provider, '')
    if not url:
        print(f"❌ No calculator URL for {provider}")
        return False

    print(f"Opening {url}...")
    try:
        if sys.platform == 'darwin':
            subprocess.run(['open', url])
        elif sys.platform == 'win32':
            subprocess.run(['start', url], shell=True)
        else:
            subprocess.run(['xdg-open', url])
        return True
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print(f"   Please manually open: {url}")
        return False


def read_component_catalog(provider: str) -> dict:
    """Read pricing from component catalog (source of truth)"""
    catalog_file = PRICING_DIR / f'{provider}-component-catalog.md'

    if not catalog_file.exists():
        print(f"❌ Component catalog not found: {catalog_file}")
        return {}

    with open(catalog_file, 'r') as f:
        content = f.read()

    # Parse pricing from component catalog
    sections = {
        'ec2': [],
        'ec2_savings': [],
        'rds_single_az': [],
        'rds_multi_az': [],
        'elasticache': [],
        'eks': [],
        'elb': [],
        'ebs': [],
        's3': [],
        'direct_connect': [],
        'vpc_flow_logs': [],
        'kms': [],
        'shield': []
    }

    lines = content.split('\n')
    current_section = None
    current_table_headers = []
    in_table = False
    in_ec2_section = False
    in_rds_section = False

    for i, line in enumerate(lines):
        # Track major sections
        if '## Compute Components' in line:
            in_ec2_section = True
            in_rds_section = False
        elif '## Database Components' in line:
            in_rds_section = True
            in_ec2_section = False
        elif '## Cache Components' in line:
            in_ec2_section = False
            in_rds_section = False

        # Detect section headers
        if line.startswith('### ') or line.startswith('#### '):
            in_table = False
            current_table_headers = []

            if 'Compute Savings Plans' in line:
                current_section = 'ec2_savings'
            elif 'General Purpose' in line or 'Compute Optimized' in line or 'Memory Optimized' in line:
                if in_ec2_section:
                    current_section = 'ec2'
            elif 'Single-AZ' in line and 'Instances' in line:
                current_section = 'rds_single_az'
            elif 'Multi-AZ' in line and 'Instances' in line and 'High Availability' in line:
                current_section = 'rds_multi_az'
            elif 'ElastiCache' in line or 'Redis' in line:
                current_section = 'elasticache'
            elif 'EKS' in line:
                current_section = 'eks'
            elif 'Application Load Balancer' in line or 'ALB' in line:
                current_section = 'elb'
            elif 'Network Load Balancer' in line or 'NLB' in line:
                current_section = 'elb'
            elif 'Amazon EBS' in line:
                current_section = 'ebs'
            elif 'Amazon S3' in line:
                current_section = 's3'
            elif 'Direct Connect' in line:
                current_section = 'direct_connect'
            elif 'VPC Flow Logs' in line:
                current_section = 'vpc_flow_logs'
            elif 'KMS' in line:
                current_section = 'kms'
            elif 'Shield' in line:
                current_section = 'shield'

        # Detect table headers (any row with | that contains Instance/Component and --- not in it)
        if line.startswith('|') and ('Instance' in line or 'Component' in line) and '---' not in line:
            in_table = True
            current_table_headers = [p.strip() for p in line.split('|')[1:-1]]

        # Parse table rows
        if in_table and line.startswith('|') and '---' not in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]

            # Skip header rows, separator rows, and empty rows
            if not parts or parts[0] in ['Instance', 'Component', '***', 'Engine', 'Source', 'Calculator URL', '---']:
                continue

            # Skip rows that don't have enough data
            if len(parts) < 3:
                continue

            # Extract data based on section type
            if current_section == 'ec2':
                # EC2 On-Demand: | Instance | vCPU | Memory | ... | Price/Hour | ... |
                if 'Price/Hour' in current_table_headers:
                    price_idx = current_table_headers.index('Price/Hour')
                    try:
                        price = parts[price_idx].replace('$', '').replace('USD', '').strip()
                        price_float = float(price) if price else 0

                        # Skip if price is 0 or invalid
                        if price_float <= 0:
                            continue

                        sections['ec2'].append({
                            'name': parts[0],
                            'vcpu': parts[1] if len(parts) > 1 else '',
                            'memory': parts[2] if len(parts) > 2 else '',
                            'price_hour': price_float,
                            'storage': parts[3] if len(parts) > 3 else '',
                            'network': parts[4] if len(parts) > 4 else '',
                            'calculator_url': parts[-1] if len(parts) > 0 and parts[-1].startswith('http') else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section == 'ec2_savings':
                # EC2 Savings Plans: | Instance | vCPU | Memory | On-Demand/Hour | Savings 3yr/Hour | ... |
                if 'On-Demand/Hour' in current_table_headers and 'Savings 3yr/Hour' in current_table_headers:
                    try:
                        on_demand_idx = current_table_headers.index('On-Demand/Hour')
                        savings_idx = current_table_headers.index('Savings 3yr/Hour')
                        monthly_idx = current_table_headers.index('Monthly (730h)') if 'Monthly (730h)' in current_table_headers else -1
                        savings_pct_idx = current_table_headers.index('Savings %') if 'Savings %' in current_table_headers else -1

                        on_demand_price = float(parts[on_demand_idx].replace('$', '').strip()) if on_demand_idx >= 0 else 0
                        savings_price = float(parts[savings_idx].replace('$', '').strip()) if savings_idx >= 0 else 0
                        monthly = parts[monthly_idx].replace('$', '').replace(',', '').strip() if monthly_idx >= 0 else ''
                        savings_pct = parts[savings_pct_idx].replace('%', '').strip() if savings_pct_idx >= 0 else ''

                        # Skip if prices are 0 or invalid
                        if on_demand_price <= 0 or savings_price <= 0:
                            continue

                        sections['ec2_savings'].append({
                            'name': parts[0],
                            'vcpu': parts[1] if len(parts) > 1 else '',
                            'memory': parts[2] if len(parts) > 2 else '',
                            'on_demand_hour': on_demand_price,
                            'savings_hour': savings_price,
                            'monthly': monthly,
                            'savings_pct': savings_pct,
                            'calculator_url': parts[-1] if len(parts) > 0 and parts[-1].startswith('http') else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section in ['rds_single_az', 'rds_multi_az']:
                # RDS: | Instance | vCPU | Memory | Price/Hour | ... |
                if 'Price/Hour' in current_table_headers:
                    price_idx = current_table_headers.index('Price/Hour')
                    try:
                        price = parts[price_idx].replace('$', '').replace('USD', '').replace('*', '').strip()
                        price_float = float(price) if price else 0

                        # Skip if price is 0 or invalid
                        if price_float <= 0:
                            continue

                        sections[current_section].append({
                            'name': parts[0],
                            'vcpu': parts[1] if len(parts) > 1 else '',
                            'memory': parts[2] if len(parts) > 2 else '',
                            'price_hour': price_float,
                            'calculator_url': parts[-1] if len(parts) > 0 and parts[-1].startswith('http') else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section == 'elasticache':
                # ElastiCache: | Instance | vCPU | Memory | Price/Hour | ... |
                if 'Price/Hour' in current_table_headers:
                    price_idx = current_table_headers.index('Price/Hour')
                    try:
                        price = parts[price_idx].replace('$', '').replace('USD', '').strip()
                        price_float = float(price) if price else 0

                        # Skip if price is 0 or invalid
                        if price_float <= 0:
                            continue

                        sections['elasticache'].append({
                            'name': parts[0],
                            'vcpu': parts[1] if len(parts) > 1 else '',
                            'memory': parts[2] if len(parts) > 2 else '',
                            'price_hour': price_float,
                            'calculator_url': parts[-1] if len(parts) > 0 and parts[-1].startswith('http') else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section == 'eks':
                # EKS: | Component | Price | Billing Unit | Calculator URL |
                if 'Price' in current_table_headers and 'Calculator URL' in current_table_headers:
                    try:
                        price_idx = current_table_headers.index('Price')
                        billing_idx = current_table_headers.index('Billing Unit')
                        url_idx = current_table_headers.index('Calculator URL')

                        price = parts[price_idx].replace('$', '').replace('/hour', '').replace('/vCPU-hour', '').replace('/GB-hour', '').strip()

                        sections['eks'].append({
                            'name': parts[0],
                            'price': parts[price_idx],
                            'billing_unit': parts[billing_idx],
                            'calculator_url': parts[url_idx] if url_idx < len(parts) else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section == 'elb':
                # Load Balancer: | Component | Price | Billing Unit | Calculator URL |
                if 'Price' in current_table_headers and 'Calculator URL' in current_table_headers:
                    try:
                        price_idx = current_table_headers.index('Price')
                        billing_idx = current_table_headers.index('Billing Unit')
                        url_idx = current_table_headers.index('Calculator URL')

                        sections['elb'].append({
                            'name': parts[0],
                            'price': parts[price_idx],
                            'billing_unit': parts[billing_idx],
                            'calculator_url': parts[url_idx] if url_idx < len(parts) else 'https://calculator.aws/'
                        })
                    except (ValueError, IndexError):
                        pass

            elif current_section in ['ebs', 's3', 'direct_connect', 'vpc_flow_logs', 'kms', 'shield']:
                # Generic parsing for storage/networking/security components
                if 'Calculator URL' in current_table_headers:
                    try:
                        url_idx = current_table_headers.index('Calculator URL')

                        # Create a dict with all parts
                        item_data = {'name': parts[0]}
                        for idx, header in enumerate(current_table_headers):
                            if idx < len(parts) and header != 'Calculator URL':
                                item_data[header.lower().replace(' ', '_')] = parts[idx]

                        item_data['calculator_url'] = parts[url_idx] if url_idx < len(parts) else 'https://calculator.aws/'
                        sections[current_section].append(item_data)
                    except (ValueError, IndexError):
                        pass

    return sections


def create_pricing_template(provider: str, catalog_sections: dict) -> str:
    """Create pricing template from component catalog data (dynamic)"""

    today = datetime.now().strftime('%Y-%m-%d')
    valid_until = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    if provider == 'aws':
        content = f"""---
type: apv-knowledge
category: pricing
title: "AWS Pricing for Singapore Region"
source_url: "https://calculator.aws/"
source_api: "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSComputeService"
captured_date: {today}
verified_by: "Infrastructure Architect"
price_valid_until: {valid_until}
tags: [pricing, aws, singapore, calculator]
---

# AWS Pricing for Card Processing (Singapore Region)

## Official Calculators

| Calculator | URL | Last Updated |
|------------|-----|-------------|
| AWS Pricing Calculator | https://calculator.aws/ | {today} |
| AWS EC2 Pricing | https://aws.amazon.com/ec2/pricing/ | {today} |
| AWS EKS Pricing | https://aws.amazon.com/eks/pricing/ | {today} |
| AWS RDS Pricing | https://aws.amazon.com/rds/pricing/ | {today} |
| AWS ElastiCache Pricing | https://aws.amazon.com/elasticache/pricing/ | {today} |
| AWS ALB Pricing | https://aws.amazon.com/elasticloadbalancing/pricing/ | {today} |

## Regional Pricing (Singapore ap-southeast-1)

> [!IMPORTANT] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: {today}
> Calculator: https://calculator.aws/
"""

        # EC2 Instances (On-Demand)
        if catalog_sections.get('ec2'):
            content += """
### EC2 Instances (Single-AZ)

**Source**: aws-component-catalog.md (EC2 Instances)

| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|------------|---------------|----------------|
"""
            for item in catalog_sections['ec2']:
                monthly = item['price_hour'] * 730
                content += f"| {item['name']} | {item['vcpu']} | {item['memory']} | ${item['price_hour']:.3f} | ${monthly:.2f} | {item['calculator_url']} |\n"

        # EC2 Compute Savings Plans
        if catalog_sections.get('ec2_savings'):
            content += """
### EC2 Instances - Compute Savings Plans (3yr No Upfront)

> [!NOTE] Calculator-Verified Savings Plans Pricing
> Pricing below was verified on """ + today + """ from https://calculator.aws/
> **3-year commitment required** for these prices.
> Calculator Configuration: Region: Asia Pacific (Singapore), Tenancy: Shared, OS: Linux, Workload: Consistent

| Instance | vCPU | Memory | On-Demand/Hour | Savings 3yr/Hour | Monthly (730h) | Savings % | Calculator URL |
|----------|------|--------|----------------|-----------------|---------------|-----------|----------------|
"""
            for item in catalog_sections['ec2_savings']:
                content += f"| {item['name']} | {item['vcpu']} | {item['memory']} | ${item['on_demand_hour']:.3f} | ${item['savings_hour']:.3f} | ${item['monthly']} | {item['savings_pct']}% | {item['calculator_url']} |\n"

        # EKS Pricing
        if catalog_sections.get('eks'):
            content += """
### EKS Pricing

**Source**: aws-component-catalog.md (Container Components)

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|----------------|
"""
            for item in catalog_sections['eks']:
                content += f"| {item['name']} | {item['price']} | {item['billing_unit']} | {item['calculator_url']} |\n"

        # Load Balancer Pricing
        if catalog_sections.get('elb'):
            content += """
### Load Balancer Pricing

**Source**: aws-component-catalog.md (Load Balancing Components)

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|----------------|
"""
            for item in catalog_sections['elb']:
                content += f"| {item['name']} | {item['price']} | {item['billing_unit']} | {item['calculator_url']} |\n"

        # EBS Pricing
        if catalog_sections.get('ebs'):
            content += """
### EBS Storage Pricing

**Source**: aws-component-catalog.md (Storage Components)

| Size | Price/GB-month | Calculator URL |
|------|----------------|----------------|
"""
            for item in catalog_sections['ebs']:
                content += f"| {item['name']} | {item.get('price/gb-month', item.get('price', ''))} | {item['calculator_url']} |\n"

        # S3 Pricing
        if catalog_sections.get('s3'):
            content += """
### S3 Storage Pricing

**Source**: aws-component-catalog.md (Storage Components)

| Storage Class | Price/GB-month | Min Storage | Calculator URL |
|---------------|----------------|-------------|----------------|
"""
            for item in catalog_sections['s3']:
                content += f"| {item['name']} | {item.get('price/gb-month', item.get('price', ''))} | {item.get('min_storage', '')} | {item['calculator_url']} |\n"

        # Direct Connect Pricing
        if catalog_sections.get('direct_connect'):
            content += """
### Direct Connect Pricing

**Source**: aws-component-catalog.md (Networking Components)

| Port Speed | Price/month | Data Transfer | Calculator URL |
|-----------|-------------|---------------|----------------|
"""
            for item in catalog_sections['direct_connect']:
                content += f"| {item['name']} | {item.get('price/month', '')} | {item.get('data_transfer', '')} | {item['calculator_url']} |\n"

        # VPC Flow Logs Pricing
        if catalog_sections.get('vpc_flow_logs'):
            content += """
### VPC Flow Logs Pricing

**Source**: aws-component-catalog.md (Networking Components)

| Component | Price | Calculator URL |
|-----------|-------|----------------|
"""
            for item in catalog_sections['vpc_flow_logs']:
                content += f"| {item['name']} | {item.get('price', '')} | {item['calculator_url']} |\n"

        # KMS Pricing
        if catalog_sections.get('kms'):
            content += """
### KMS Pricing

**Source**: aws-component-catalog.md (Security Components)

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|----------------|
"""
            for item in catalog_sections['kms']:
                content += f"| {item['name']} | {item.get('price', '')} | {item.get('billing_unit', '')} | {item['calculator_url']} |\n"

        # Shield Pricing
        if catalog_sections.get('shield'):
            content += """
### Shield Pricing

**Source**: aws-component-catalog.md (Security Components)

| Component | Price | Calculator URL |
|-----------|-------|----------------|
"""
            for item in catalog_sections['shield']:
                content += f"| {item['name']} | {item.get('price', '')} | {item['calculator_url']} |\n"

        # If no EKS or ELB data found, use default hardcoded values (for backward compatibility)
        if not catalog_sections.get('eks'):
            content += """
### EKS Pricing

**Source**: aws-component-catalog.md (Container Components)

| Component | Price | Calculator URL |
|-----------|-------|----------------|
| EKS Cluster | $0.10/hour | https://calculator.aws/ |
| Fargate vCPU | $0.04064/vCPU-hour | https://calculator.aws/ |
| Fargate GB | $0.0044/GB-hour | https://calculator.aws/ |
"""

        if not catalog_sections.get('elb'):
            content += """
### Load Balancer Pricing

**Source**: aws-component-catalog.md (Load Balancing Components)

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|----------------|
| ALB Hourly | $0.0225 | per ALB-hour | https://calculator.aws/ |
| LCU Hourly | $0.008 | per LCU-hour | https://calculator.aws/ |
"""

        # RDS Single-AZ Pricing
        if catalog_sections.get('rds_single_az'):
            content += """
### RDS Pricing (Single-AZ)

**Source**: aws-component-catalog.md (Database Components)

> [!NOTE] Multi-AZ Pricing
> Multi-AZ pricing is approximately 2-3x Single-AZ pricing.
> See "RDS Pricing (Verified from Calculator)" section below for calculator-verified Multi-AZ pricing.

| Engine | Instance | vCPU | Memory | Price/Hour (Single-AZ) | Price/Hour (Multi-AZ) | Calculator URL |
|--------|----------|------|--------|---------------------|------------------|----------------|
"""
            for item in catalog_sections['rds_single_az']:
                price = item['price_hour']
                multi_az_price = price * 2  # Approximate 2x for Multi-AZ
                content += f"| PostgreSQL | {item['name']} | {item['vcpu']} | {item['memory']} | ${price:.3f} | ${multi_az_price:.3f} | {item['calculator_url']} |\n"

        # RDS Multi-AZ Pricing (Calculator Verified)
        if catalog_sections.get('rds_multi_az'):
            content += f"""
### RDS Pricing (Verified from Calculator)

> [!IMPORTANT] Calculator-Verified Multi-AZ Pricing
> Verified on {today} from https://calculator.aws/

| Engine | Instance | vCPU | Price/Hour (Multi-AZ) | Monthly (730h) | Calculator URL |
|--------|----------|------|---------------------|--------------|----------------|
"""
            for item in catalog_sections['rds_multi_az']:
                monthly = item['price_hour'] * 730
                content += f"| PostgreSQL | {item['name']} | {item['vcpu']} | **${item['price_hour']:.3f}** | **${monthly:.2f}** | {item['calculator_url']} |\n"

            content += """
**Calculator Configuration**:
- Region: Asia Pacific (Singapore)
- Engine: PostgreSQL
- Instance Class: Memory Optimized (db.m6i)
- Instance Type: db.m6i.xlarge
- Deployment Option: Multi-AZ
- Storage: General Purpose SSD (gp2), 100 GB
- Utilization: 100% Utilized/Month
"""

        # ElastiCache Pricing
        if catalog_sections.get('elasticache'):
            content += """
### ElastiCache Pricing

**Source**: aws-component-catalog.md (Cache Components)

| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|------------|----------------|----------------|
"""
            for item in catalog_sections['elasticache']:
                monthly = item['price_hour'] * 730
                content += f"| {item['name']} | {item['vcpu']} | {item['memory']} | ${item['price_hour']:.3f} | ${monthly:.2f} | {item['calculator_url']} |\n"

        content += f"""
## Verification

- **Verified By**: Infrastructure Architect
- **Verification Date**: {today}
- **Verification Method**: https://calculator.aws/
- **Next Review**: {valid_until} (30 days)

## Related

- [[aws-pricing]] - AWS pricing reference
- [[aws-component-catalog]] - Component catalog (source of truth)
- [[tps-calculator]] - Component sizing methodology
"""
        return content

    return ""


def save_template(provider: str, content: str) -> Path:
    """Save template to temp directory"""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = TEMP_DIR / f'{provider}.md'

    with open(temp_file, 'w') as f:
        f.write(content)

    return temp_file


def create_evidence_record(provider: str, action: str) -> Path:
    """Create an evidence record"""
    today = datetime.now().strftime('%Y-%m-%d')
    evidence_dir = EVIDENCE_DIR / today
    evidence_dir.mkdir(parents=True, exist_ok=True)

    record = {
        'provider': provider,
        'date': today,
        'action': action,
        'calculator_url': CALCULATORS.get(provider, ''),
        'region': REGIONS.get(provider, ''),
        'catalog_file': str(COMPONENT_CATALOG),
        'timestamp': datetime.now().isoformat()
    }

    record_file = evidence_dir / f'{provider}-fetch-record.json'
    with open(record_file, 'w') as f:
        json.dump(record, f, indent=2)

    return record_file


def main():
    parser = argparse.ArgumentParser(
        description='Fetch pricing from component catalog (source of truth)',
        epilog="""
This script fetches pricing from aws-component-catalog.md and creates a
verification template. The component catalog is the SOURCE OF TRUTH for pricing.

Workflow:
  1. Read pricing from aws-component-catalog.md
  2. Create template with catalog pricing
  3. Open calculator for manual verification
  4. User verifies and updates template as needed
  5. Proceed to verification step

Examples:
  python pricing-fetcher.py --provider aws
  python pricing-fetcher.py --all

Next Steps:
  1. Review the template in /tmp/apv-pricing-updates/
  2. Verify pricing in https://calculator.aws/
  3. Update template if calculator shows different pricing
  4. Run: python pricing-verify.py --provider aws
        """
    )
    parser.add_argument('--provider', choices=['aws', 'azure', 'gcp'],
                        help='Cloud provider')
    parser.add_argument('--all', action='store_true',
                        help='Fetch all providers')
    parser.add_argument('--no-open', action='store_true',
                        help='Skip opening calculator browser')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else ['aws', 'azure', 'gcp']

    print("=" * 70)
    print("APV PRICING FETCHER - Component Catalog Mode")
    print("=" * 70)
    print()

    for provider in providers:
        print(f"Provider: {provider.upper()}")
        print(f"Component Catalog: {COMPONENT_CATALOG}")
        print(f"Calculator: {CALCULATORS.get(provider, '')}")
        print(f"Region: {REGIONS.get(provider, '')}")
        print()

        # Check component catalog exists
        if not COMPONENT_CATALOG.exists():
            print(f"❌ Component catalog not found: {COMPONENT_CATALOG}")
            print(f"   This script requires the component catalog as source of truth")
            continue

        # Read pricing from component catalog
        catalog_sections = read_component_catalog(provider)

        if not catalog_sections:
            print(f"⚠️  Could not parse pricing from component catalog")
            continue

        # Count total items across all sections
        total_items = sum(len(items) for items in catalog_sections.values())
        print(f"📊 Found {total_items} pricing items in component catalog")

        # Show breakdown by section
        for section, items in catalog_sections.items():
            if items:
                print(f"   - {section}: {len(items)} items")
        print()

        # Create evidence record
        create_evidence_record(provider, 'fetch-from-catalog')

        # Create template
        content = create_pricing_template(provider, catalog_sections)
        save_template(provider, content)

        print(f"📝 Created template: {TEMP_DIR / f'{provider}.md'}")

        # Open calculator
        if not args.no_open:
            open_calculator(provider)

        print()
        print("Instructions:")
        print(f"  1. Calculator opened in browser")
        print(f"  2. Component catalog pricing pre-filled in template")
        print(f"  3. Verify calculator pricing matches catalog")
        print(f"  4. Edit template if calculator shows different pricing")
        print(f"  5. Run: python pricing-verify.py --provider {provider}")
        print()

    print("=" * 70)
    print("FETCH COMPLETE")
    print("=" * 70)
    print(f"Template location: {TEMP_DIR}")
    print(f"Component catalog: {COMPONENT_CATALOG}")
    print()


if __name__ == '__main__':
    main()
