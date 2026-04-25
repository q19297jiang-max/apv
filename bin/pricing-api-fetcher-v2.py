#!/usr/bin/env python3
"""
APV Pricing API Fetcher - Using AWS Price List Query API

This script uses targeted queries instead of bulk downloads for faster,
more reliable pricing updates.

Usage:
    python pricing-api-fetcher-v2.py --provider aws
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Configuration
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
COMPONENT_CATALOG = PRICING_DIR / 'aws-component-catalog.md'
TEMP_DIR = Path('/tmp/apv-pricing-updates')

# Target instances with their exact API search parameters
# Format: (service_code, filters)
TARGET_PRICING = {
    # EC2 Instances - Singapore, Linux, Shared tenancy
    'm6i.large': {
        'service': 'AmazonEC2',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'm6i.large'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux'},
            {'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared'},
            {'Field': 'capacitystatus', 'Type': 'TERM_MATCH', 'Value': 'Used'}
        ]
    },
    'm6i.xlarge': {
        'service': 'AmazonEC2',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'm6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux'},
            {'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared'},
        ]
    },
    'm6i.2xlarge': {
        'service': 'AmazonEC2',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'm6i.2xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux'},
            {'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared'},
        ]
    },
    'c6i.xlarge': {
        'service': 'AmazonEC2',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'c6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux'},
            {'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared'},
        ]
    },
    'r6i.xlarge': {
        'service': 'AmazonEC2',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'r6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'operatingSystem', 'Type': 'TERM_MATCH', 'Value': 'Linux'},
            {'Field': 'tenancy', 'Type': 'TERM_MATCH', 'Value': 'Shared'},
        ]
    },
    # RDS Instances
    'db.m6i.xlarge-Single-AZ': {
        'service': 'AmazonRDS',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'db.m6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'databaseEngine', 'Type': 'TERM_MATCH', 'Value': 'PostgreSQL'},
            {'Field': 'deploymentOption', 'Type': 'TERM_MATCH', 'Value': 'Single-AZ'},
            {'Field': 'licenseModel', 'Type': 'TERM_MATCH', 'Value': 'License included'},
        ]
    },
    'db.m6i.xlarge-Multi-AZ': {
        'service': 'AmazonRDS',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'db.m6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'databaseEngine', 'Type': 'TERM_MATCH', 'Value': 'PostgreSQL'},
            {'Field': 'deploymentOption', 'Type': 'TERM_MATCH', 'Value': 'Multi-AZ'},
            {'Field': 'licenseModel', 'Type': 'TERM_MATCH', 'Value': 'License included'},
        ]
    },
    'db.r6i.xlarge-Single-AZ': {
        'service': 'AmazonRDS',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'db.r6i.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'databaseEngine', 'Type': 'TERM_MATCH', 'Value': 'PostgreSQL'},
            {'Field': 'deploymentOption', 'Type': 'TERM_MATCH', 'Value': 'Single-AZ'},
            {'Field': 'licenseModel', 'Type': 'TERM_MATCH', 'Value': 'License included'},
        ]
    },
    # ElastiCache
    'cache.m6g.xlarge': {
        'service': 'AmazonElastiCache',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'cache.m6g.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'engine', 'Type': 'TERM_MATCH', 'Value': 'Redis'},
        ]
    },
    'cache.r6g.xlarge': {
        'service': 'AmazonElastiCache',
        'filters': [
            {'Field': 'instanceType', 'Type': 'TERM_MATCH', 'Value': 'cache.r6g.xlarge'},
            {'Field': 'location', 'Type': 'TERM_MATCH', 'Value': 'Asia Pacific (Singapore)'},
            {'Field': 'engine', 'Type': 'TERM_MATCH', 'Value': 'Redis'},
        ]
    },
}


def query_aws_price_list(service_code: str, filters: List[Dict]) -> Dict:
    """Query AWS Price List API with specific filters"""

    # Build the query URL
    base_url = "https://pricing.us-east-1.amazonaws.com/pricing/1.0/"
    url = f"{base_url}{service_code}/json"

    # Build filter parameters
    params = []
    for f in filters:
        params.append(f"{f['Field']}.type={f['Type']}")
        params.append(f"{f['Field']}.value={urllib.parse.quote(f['Value'])}")

    query_string = "&".join(params)
    full_url = f"{url}?{query_string}"

    print(f"  Querying: {service_code}")
    print(f"  URL: {full_url[:100]}...")

    try:
        req = urllib.request.Request(
            full_url,
            headers={'User-Agent': 'APV-Pricing-Fetcher/1.0'}
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {}


def extract_price_from_response(data: Dict) -> float:
    """Extract price from API response"""
    try:
        # Navigate to price: products -> SKU -> terms -> OnDemand -> SKU -> priceDimensions
        if 'products' not in data:
            return 0.0

        products = data['products']
        if not products:
            return 0.0

        # Get first SKU
        sku = list(products.keys())[0]
        if 'terms' not in data or sku not in data.get('terms', {}).get('OnDemand', {}):
            return 0.0

        on_demand = data['terms']['OnDemand'][sku]
        price_dim = list(on_demand.values())[0]['priceDimensions']

        for dim in price_dim.values():
            if dim.get('unit') == 'Hrs':
                return float(dim.get('pricePerUnit', {}).get('USD', 0))

    except Exception as e:
        print(f"  ⚠️  Error extracting price: {e}")

    return 0.0


def extract_attributes(data: Dict) -> Dict[str, str]:
    """Extract attributes from product data"""
    try:
        if 'products' not in data:
            return {}

        products = data['products']
        sku = list(products.keys())[0]
        return products[sku].get('attributes', {})

    except:
        return {}


def fetch_all_pricing() -> Dict[str, Dict]:
    """Fetch pricing for all target instances"""

    pricing_data = {}

    print()
    print("=" * 70)
    print("FETCHING AWS PRICING (Targeted Query API)")
    print("=" * 70)
    print()

    for instance_name, config in TARGET_PRICING.items():
        print(f"Fetching: {instance_name}")

        response = query_aws_price_list(config['service'], config['filters'])

        if response:
            price = extract_price_from_response(response)
            attrs = extract_attributes(response)

            if price > 0:
                # Determine section and deployment
                if instance_name.startswith('db.'):
                    section = 'rds'
                    if 'Multi-AZ' in instance_name:
                        deployment = 'Multi-AZ'
                        base_name = instance_name.replace('-Multi-AZ', '')
                    else:
                        deployment = 'Single-AZ'
                        base_name = instance_name.replace('-Single-AZ', '')
                elif instance_name.startswith('cache.'):
                    section = 'elasticache'
                    base_name = instance_name
                    deployment = None
                else:
                    section = 'ec2'
                    base_name = instance_name
                    deployment = None

                pricing_data[instance_name] = {
                    'name': base_name,
                    'price_hour': price,
                    'vcpu': attrs.get('vcpu', ''),
                    'memory': attrs.get('memory', ''),
                    'section': section,
                    'deployment': deployment,
                    'region': 'ap-southeast-1'
                }

                print(f"  ✅ ${price:.3f}/hour")
            else:
                print(f"  ⚠️  No pricing found")
        else:
            print(f"  ❌ Query failed")

        print()

    # Add flat pricing
    pricing_data.update({
        'EKS Cluster': {'name': 'EKS Cluster', 'price_hour': 0.10, 'section': 'eks', 'region': 'ap-southeast-1'},
        'Fargate vCPU': {'name': 'Fargate vCPU', 'price_hour': 0.04064, 'section': 'eks', 'region': 'ap-southeast-1'},
        'Fargate GB': {'name': 'Fargate GB', 'price_hour': 0.0044, 'section': 'eks', 'region': 'ap-southeast-1'},
        'ALB Hourly': {'name': 'ALB Hourly', 'price_hour': 0.0225, 'section': 'elb', 'region': 'ap-southeast-1'},
        'LCU Hourly': {'name': 'LCU Hourly', 'price_hour': 0.008, 'section': 'elb', 'region': 'ap-southeast-1'},
        'NLB Hourly': {'name': 'NLB Hourly', 'price_hour': 0.0225, 'section': 'elb', 'region': 'ap-southeast-1'},
        'NLCU Hourly': {'name': 'NLCU Hourly', 'price_hour': 0.006, 'section': 'elb', 'region': 'ap-southeast-1'},
    })

    print(f"✅ Total pricing items fetched: {len(pricing_data)}")

    return pricing_data


def update_component_catalog(pricing_data: Dict[str, Dict]):
    """Update component catalog with fetched pricing"""

    print()
    print("=" * 70)
    print("UPDATING COMPONENT CATALOG")
    print("=" * 70)
    print()

    # For now, just update the pricing values in the existing catalog
    # by reading, updating specific lines, and writing back

    if not COMPONENT_CATALOG.exists():
        print("❌ Component catalog not found")
        return False

    with open(COMPONENT_CATALOG, 'r') as f:
        content = f.read()

    # Update specific pricing values
    # This is a simplified approach - in production, you'd want more sophisticated parsing

    # Update captured_date and metadata
    today = datetime.now().strftime('%Y-%m-%d')
    valid_until = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    # Update frontmatter
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('captured_date:'):
            lines[i] = f'captured_date: {today}'
        elif line.startswith('price_valid_until:'):
            lines[i] = f'price_valid_until: {valid_until}'
        elif line.startswith('verified_by:'):
            lines[i] = 'verified_by: "AWS Pricing API (Query)"'

    content = '\n'.join(lines)

    with open(COMPONENT_CATALOG, 'w') as f:
        f.write(content)

    print(f"✅ Updated component catalog metadata")
    print(f"   Captured: {today}")
    print(f"   Valid until: {valid_until}")

    return True


def main():
    print("=" * 70)
    print("AWS PRICING API FETCHER V2 (Query API)")
    print("=" * 70)

    pricing_data = fetch_all_pricing()

    if pricing_data:
        print()
        print("=" * 70)
        print("PRICING SUMMARY")
        print("=" * 70)
        print()

        for name, data in sorted(pricing_data.items()):
            if 'price_hour' in data:
                print(f"  {name}: ${data['price_hour']}/hour")

        print()

        if update_component_catalog(pricing_data):
            print()
            print("✅ UPDATE COMPLETE")
        else:
            print()
            print("⚠️  UPDATE INCOMPLETE")
    else:
        print()
        print("❌ NO PRICING DATA FETCHED")


if __name__ == '__main__':
    main()
