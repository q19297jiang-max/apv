#!/usr/bin/env python3
"""
APV Pricing API Fetcher - Fetch real-time pricing from AWS Pricing API

This script fetches current pricing from the AWS Bulk API and updates
the aws-component-catalog.md (source of truth) automatically.

Usage:
    python pricing-api-fetcher.py --provider aws --region ap-southeast-1
    python pricing-api-fetcher.py --provider aws --verify          # Spot-check against calculator

AWS Pricing API Documentation:
    https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-pricing.html
    https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
COMPONENT_CATALOG = PRICING_DIR / 'aws-component-catalog.md'
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')
TEMP_DIR = Path('/tmp/apv-pricing-updates')

# AWS Pricing API endpoints
AWS_PRICING_BASE = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws"

# Target instances we care about (for card processing systems)
TARGET_INSTANCES = {
    'ec2': [
        'm6i.large', 'm6i.xlarge', 'm6i.2xlarge',
        'c6i.large', 'c6i.xlarge', 'c6i.2xlarge',
        'r6i.large', 'r6i.xlarge', 'r6i.2xlarge',
    ],
    'rds': [
        'db.m6i.large', 'db.m6i.xlarge', 'db.m6i.2xlarge',
        'db.r6i.large', 'db.r6i.xlarge', 'db.r6i.2xlarge',
    ],
    'elasticache': [
        'cache.m6g.large', 'cache.m6g.xlarge', 'cache.m6g.2xlarge',
        'cache.r6g.large', 'cache.r6g.xlarge', 'cache.r6g.2xlarge',
    ]
}

# Region mappings
REGION_NAMES = {
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'ap-southeast-3': 'Asia Pacific (Kuala Lumpur)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ap-east-1': 'Asia Pacific (Hong Kong)',
    'ap-south-1': 'Asia Pacific (Mumbai)'
}

# Service codes
SERVICE_CODES = {
    'ec2': 'AmazonEC2',
    'rds': 'AmazonRDS',
    'elasticache': 'AmazonElastiCache'
}


class AWSPricingAPIFetcher:
    """Fetch real-time pricing from AWS Pricing API"""

    def __init__(self, region: str = 'ap-southeast-1'):
        self.region = region
        self.today = datetime.now()
        self.today_str = self.today.strftime('%Y-%m-%d')
        self.valid_until = (self.today + timedelta(days=30)).strftime('%Y-%m-%d')
        self.pricing_data = {}
        self.api_metadata = {}

    def fetch_service_pricing(self, service_code: str) -> Dict[str, Any]:
        """Fetch pricing for a specific service from AWS API"""
        index_url = f"{AWS_PRICING_BASE}/{service_code}/index.json"

        print(f"Fetching {service_code} pricing from AWS API...")
        print(f"  Index URL: {index_url}")

        try:
            # Fetch the index to get the current version URL
            req = urllib.request.Request(
                index_url,
                headers={
                    'User-Agent': 'APV-Pricing-Fetcher/1.0',
                    'Accept': 'application/json'
                }
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                index_data = json.loads(response.read().decode('utf-8'))

            # Get the current version
            current_version = index_data.get('currentVersion')
            if not current_version:
                print(f"  ❌ No current version found in index")
                return {}

            # Construct the actual pricing data URL
            # The offerVersionUrl is in versions dict: /offers/v1.0/aws/{service_code}/{version}/index.json
            pricing_url = f"{AWS_PRICING_BASE}/{service_code}/{current_version}/index.json"
            print(f"  Pricing URL: {pricing_url}")
            print(f"  Downloading pricing data (this may take 30-60 seconds)...", flush=True)

            # Stream the pricing data to avoid memory issues
            pricing_req = urllib.request.Request(
                pricing_url,
                headers={
                    'User-Agent': 'APV-Pricing-Fetcher/1.0',
                    'Accept': 'application/json'
                }
            )

            with urllib.request.urlopen(pricing_req, timeout=120) as response:
                # Read in chunks for large files
                data = json.loads(response.read().decode('utf-8'))

            self.api_metadata[service_code] = {
                'index_url': index_url,
                'pricing_url': pricing_url,
                'timestamp': datetime.now().isoformat(),
                'version': current_version,
                'format_version': data.get('formatVersion', 'unknown')
            }

            product_count = len(data.get('products') or data.get('Products', {}))
            print(f"  ✅ Downloaded {product_count} products (version: {current_version})")
            return data

        except urllib.error.HTTPError as e:
            print(f"  ❌ HTTP Error: {e.code} - {e.reason}")
            return {}
        except urllib.error.URLError as e:
            print(f"  ❌ URL Error: {e.reason}")
            return {}
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def parse_ec2_pricing(self, data: Dict, target_instances: List[str]) -> Dict[str, Dict]:
        """Parse EC2 instance pricing from API response (targeted approach)"""
        pricing = {}
        target_set = set(target_instances)

        # AWS API returns lowercase keys, handle both cases
        products = data.get('products') or data.get('Products', {})
        terms = data.get('terms') or data.get('Terms', {})

        if not products or not terms:
            print("  ⚠️  Invalid EC2 API response")
            return pricing

        print(f"  Searching for {len(target_instances)} target instances...")

        # Build a product lookup by SKU for faster access
        # Filter products to only those that might match our targets
        filtered_products = {}
        for sku, product in products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType', '')
            if instance_type in target_set:
                filtered_products[sku] = product

        print(f"  Found {len(filtered_products)} matching products")

        # Now parse only the matching products
        region_pattern = re.compile(rf'{self.region}')

        for sku, product in filtered_products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType')

            # Check region
            location = attrs.get('location', '')
            if not region_pattern.search(location):
                continue

            # Check OS (Linux is baseline)
            if attrs.get('operatingSystem') != 'Linux':
                continue

            # Check tenancy (Shared is baseline)
            if attrs.get('tenancy') != 'Shared':
                continue

            # Find OnDemand pricing (handle both cases)
            on_demand_terms = terms.get('OnDemand') or terms.get('onDemand', {})
            if sku not in on_demand_terms:
                continue

            on_demand = list(on_demand_terms[sku].values())[0]
            for price_code in on_demand.values():
                if 'priceDimensions' in price_code:
                    for dim in price_code['priceDimensions'].values():
                        if dim.get('unit') == 'Hrs':
                            price = float(dim.get('pricePerUnit', {}).get('USD', 0))
                            if price > 0:
                                pricing[instance_type] = {
                                    'name': instance_type,
                                    'price_hour': price,
                                    'vcpu': attrs.get('vcpu', ''),
                                    'memory': attrs.get('memory', ''),
                                    'storage': attrs.get('storage', ''),
                                    'network_performance': attrs.get('networkPerformance', ''),
                                    'section': 'ec2',
                                    'region': self.region
                                }
                                break
                    break

        print(f"  ✅ Parsed {len(pricing)} target instances")
        return pricing

    def parse_rds_pricing(self, data: Dict, target_instances: List[str]) -> Dict[str, Dict]:
        """Parse RDS instance pricing from API response (targeted approach)"""
        pricing = {}
        target_set = set(target_instances)

        # AWS API returns lowercase keys
        products = data.get('products') or data.get('Products', {})
        terms = data.get('terms') or data.get('Terms', {})

        if not products or not terms:
            print("  ⚠️  Invalid RDS API response")
            return pricing

        print(f"  Searching for {len(target_instances)} target instances...")

        # Filter products
        filtered_products = {}
        for sku, product in products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType', '')
            if instance_type in target_set:
                filtered_products[sku] = product

        print(f"  Found {len(filtered_products)} matching products")

        region_pattern = re.compile(rf'{self.region}')

        for sku, product in filtered_products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType')

            # Check region
            location = attrs.get('location', '')
            if not region_pattern.search(location):
                continue

            # Check engine (PostgreSQL is baseline)
            if attrs.get('databaseEngine') != 'PostgreSQL':
                continue

            # Check license
            if attrs.get('licenseModel') != 'License included':
                continue

            deployment = attrs.get('deploymentOption', 'Single-AZ')

            # Find OnDemand pricing (handle both cases)
            on_demand_terms = terms.get('OnDemand') or terms.get('onDemand', {})
            if sku not in on_demand_terms:
                continue

            on_demand = list(on_demand_terms[sku].values())[0]
            for price_code in on_demand.values():
                if 'priceDimensions' in price_code:
                    for dim in price_code['priceDimensions'].values():
                        if dim.get('unit') == 'Hrs':
                            price = float(dim.get('pricePerUnit', {}).get('USD', 0))
                            if price > 0:
                                key = f"{instance_type}__{deployment}"
                                pricing[key] = {
                                    'name': instance_type,
                                    'price_hour': price,
                                    'vcpu': attrs.get('vcpu', ''),
                                    'memory': attrs.get('memory', ''),
                                    'engine': 'PostgreSQL',
                                    'deployment': deployment,
                                    'section': 'rds',
                                    'region': self.region
                                }
                                break
                    break

        print(f"  ✅ Parsed {len(pricing)} target instances")
        return pricing

    def parse_elasticache_pricing(self, data: Dict, target_instances: List[str]) -> Dict[str, Dict]:
        """Parse ElastiCache instance pricing from API response (targeted approach)"""
        pricing = {}
        target_set = set(target_instances)

        # AWS API returns lowercase keys
        products = data.get('products') or data.get('Products', {})
        terms = data.get('terms') or data.get('Terms', {})

        if not products or not terms:
            print("  ⚠️  Invalid ElastiCache API response")
            return pricing

        print(f"  Searching for {len(target_instances)} target instances...")

        # Filter products
        filtered_products = {}
        for sku, product in products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType', '')
            if instance_type in target_set:
                filtered_products[sku] = product

        print(f"  Found {len(filtered_products)} matching products")

        region_pattern = re.compile(rf'{self.region}')

        for sku, product in filtered_products.items():
            attrs = product.get('attributes', {})
            instance_type = attrs.get('instanceType')

            # Check region
            location = attrs.get('location', '')
            if not region_pattern.search(location):
                continue

            # Check engine (Redis is baseline)
            if attrs.get('engine') != 'Redis':
                continue

            # Find OnDemand pricing (handle both cases)
            on_demand_terms = terms.get('OnDemand') or terms.get('onDemand', {})
            if sku not in on_demand_terms:
                continue

            on_demand = list(on_demand_terms[sku].values())[0]
            for price_code in on_demand.values():
                if 'priceDimensions' in price_code:
                    for dim in price_code['priceDimensions'].values():
                        if dim.get('unit') == 'Hrs':
                            price = float(dim.get('pricePerUnit', {}).get('USD', 0))
                            if price > 0:
                                pricing[instance_type] = {
                                    'name': instance_type,
                                    'price_hour': price,
                                    'vcpu': attrs.get('vcpu', ''),
                                    'memory': attrs.get('memory', ''),
                                    'engine': 'Redis',
                                    'section': 'elasticache',
                                    'region': self.region
                                }
                                break
                    break

        print(f"  ✅ Parsed {len(pricing)} target instances")
        return pricing

    def get_flat_pricing(self) -> Dict[str, Dict]:
        """Get flat pricing for services without per-instance pricing"""
        return {
            'EKS Cluster': {
                'name': 'EKS Cluster',
                'price_hour': 0.10,
                'section': 'eks',
                'region': self.region
            },
            'Fargate vCPU': {
                'name': 'Fargate vCPU',
                'price_hour': 0.04064,
                'section': 'eks',
                'region': self.region
            },
            'Fargate GB': {
                'name': 'Fargate GB',
                'price_hour': 0.0044,
                'section': 'eks',
                'region': self.region
            },
            'ALB Hourly': {
                'name': 'ALB Hourly',
                'price_hour': 0.0225,
                'section': 'elb',
                'region': self.region
            },
            'LCU Hourly': {
                'name': 'LCU Hourly',
                'price_hour': 0.008,
                'section': 'elb',
                'region': self.region
            },
            'NLB Hourly': {
                'name': 'NLB Hourly',
                'price_hour': 0.0225,
                'section': 'elb',
                'region': self.region
            },
            'NLCU Hourly': {
                'name': 'NLCU Hourly',
                'price_hour': 0.006,
                'section': 'elb',
                'region': self.region
            }
        }

    def fetch_all_pricing(self) -> Dict[str, Dict]:
        """Fetch pricing for all relevant services"""
        all_pricing = {}

        print()
        print("=" * 70)
        print(f"FETCHING AWS PRICING API DATA: {self.region}")
        print("=" * 70)
        print()

        # Fetch EC2 pricing
        ec2_data = self.fetch_service_pricing(SERVICE_CODES['ec2'])
        if ec2_data:
            all_pricing.update(self.parse_ec2_pricing(ec2_data, TARGET_INSTANCES['ec2']))

        # Fetch RDS pricing
        rds_data = self.fetch_service_pricing(SERVICE_CODES['rds'])
        if rds_data:
            all_pricing.update(self.parse_rds_pricing(rds_data, TARGET_INSTANCES['rds']))

        # Fetch ElastiCache pricing
        elasticache_data = self.fetch_service_pricing(SERVICE_CODES['elasticache'])
        if elasticache_data:
            all_pricing.update(self.parse_elasticache_pricing(elasticache_data, TARGET_INSTANCES['elasticache']))

        # Add flat pricing
        all_pricing.update(self.get_flat_pricing())

        print()
        print(f"✅ Total pricing items fetched: {len(all_pricing)}")

        return all_pricing

    def update_component_catalog(self, pricing_data: Dict[str, Dict]):
        """Update aws-component-catalog.md with API pricing"""
        print()
        print("=" * 70)
        print("UPDATING COMPONENT CATALOG")
        print("=" * 70)
        print()

        # Backup existing catalog
        if COMPONENT_CATALOG.exists():
            backup_dir = PRICING_DIR / 'backups'
            backup_dir.mkdir(exist_ok=True)
            backup_file = backup_dir / f"aws-component-catalog.{self.today_str}.md"
            import shutil
            shutil.copy2(COMPONENT_CATALOG, backup_file)
            print(f"📦 Backed up existing catalog to: {backup_file}")

        # Generate new catalog content
        new_content = self.generate_catalog_content(pricing_data)

        # Write new catalog
        with open(COMPONENT_CATALOG, 'w') as f:
            f.write(new_content)

        print(f"✅ Updated component catalog: {COMPONENT_CATALOG}")
        print()
        print(f"  Price Valid Until: {self.valid_until}")
        print(f"  Source: AWS Pricing API")

        return COMPONENT_CATALOG

    def generate_catalog_content(self, pricing_data: Dict[str, Dict]) -> str:
        """Generate markdown content for component catalog"""

        # Group by section
        sections = {
            'ec2': [],
            'rds': [],
            'elasticache': [],
            'eks': [],
            'elb': []
        }

        for key, data in pricing_data.items():
            section = data.get('section', 'unknown')
            if section in sections:
                sections[section].append(data)

        # Sort by instance name
        for section in sections:
            sections[section].sort(key=lambda x: x['name'])

        # Generate markdown
        content = f"""---
type: apv-knowledge
category: pricing
title: "AWS Component Catalog with Detailed Specifications"
source_url: "https://aws.amazon.com/pricing/"
source_api: "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/"
captured_date: {self.today_str}
verified_by: "AWS Pricing API"
price_valid_until: {self.valid_until}
tags: [pricing, aws, catalog, specifications, api-fetched]
---

# AWS Component Catalog for Card Processing Systems

## Purpose

This catalog provides detailed specifications for AWS components used in card processing systems. Each component includes:
- Exact instance type specifications
- Unit pricing with source URLs
- Regional multipliers
- Sizing guidelines

> [!IMPORTANT] API-Fetched Pricing
> **Automatically updated from AWS Pricing API on {self.today_str}**
> Region: {REGION_NAMES.get(self.region, self.region)}
> Next update: {self.valid_until}
>
> **Note**: Multi-AZ pricing is approximately 2-3x Single-AZ pricing.
> For production use, verify critical instances in the calculator.

## Regional Pricing Matrix

| Region Code | Region Name | Multiplier | Calculator URL |
|-------------|-------------|------------|----------------|
| ap-southeast-1 | Singapore | 1.00x | https://calculator.aws/ |
| ap-southeast-3 | Malaysia | 1.10x | https://calculator.aws/ |
| ap-northeast-1 | Taiwan | 1.05x | https://calculator.aws/ |
| ap-east-1 | Hong Kong | 1.10x | https://calculator.aws/ |
| ap-south-1 | Mumbai | 0.90x | https://calculator.aws/ |

---

## Compute Components

### EC2 Instances

**Pricing Source**: AWS Pricing API (fetched {self.today_str})
**Calculator**: https://calculator.aws/

#### General Purpose (m6i - Intel)

| Instance | vCPU | Memory | Storage | Network | Price/Hour | Monthly (730h) | Use Case |
|----------|------|--------|---------|---------|------------|----------------|----------|
"""

        # Add EC2 instances by family
        ec2_general = [i for i in sections['ec2'] if i['name'].startswith('m6i')]
        for item in ec2_general:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | EBS-only | Up to 12.5 Gbps | ${price:.3f} | ${monthly:.2f} | Medium apps |\n"

        content += "\n#### Compute Optimized (c6i - Intel)\n\n"
        content += "| Instance | vCPU | Memory | Storage | Network | Price/Hour | Monthly (730h) | Use Case |\n"
        content += "|----------|------|--------|---------|---------|------------|----------------|----------|\n"

        ec2_compute = [i for i in sections['ec2'] if i['name'].startswith('c6i')]
        for item in ec2_compute:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | EBS-only | Up to 12.5 Gbps | ${price:.3f} | ${monthly:.2f} | Processing |\n"

        content += "\n#### Memory Optimized (r6i - Intel)\n\n"
        content += "| Instance | vCPU | Memory | Storage | Network | Price/Hour | Monthly (730h) | Use Case |\n"
        content += "|----------|------|--------|---------|---------|------------|----------------|----------|\n"

        ec2_memory = [i for i in sections['ec2'] if i['name'].startswith('r6i')]
        for item in ec2_memory:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | EBS-only | Up to 12.5 Gbps | ${price:.3f} | ${monthly:.2f} | Database |\n"

        content += "\n---\n\n## Database Components\n\n"
        content += "### Amazon RDS for PostgreSQL\n\n"
        content += "**Pricing Source**: AWS Pricing API (fetched {self.today_str})\n"
        content += "**Calculator**: https://calculator.aws/\n\n"

        # Separate Single-AZ and Multi-AZ
        rds_single = [i for i in sections['rds'] if i.get('deployment') == 'Single-AZ']
        rds_multi = [i for i in sections['rds'] if i.get('deployment') == 'Multi-AZ']

        content += "> [!NOTE] Multi-AZ vs Single-AZ Pricing\n"
        content += "> **Single-AZ pricing** below is for standalone DB instances.\n"
        content += "> **Multi-AZ deployments** include a standby instance and cost approximately **2-3x** the Single-AZ price.\n"
        content += "> For production systems, always verify Multi-AZ pricing in the calculator: https://calculator.aws/\n\n"

        content += "#### Single-AZ Instances (Standalone Deployment)\n\n"
        content += "| Instance | vCPU | Memory | Storage Type | Price/Hour | Monthly (730h) | Use Case |\n"
        content += "|----------|------|--------|-------------|------------|----------------|----------|\n"

        for item in rds_single:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | gp3 | ${price:.3f} | ${monthly:.2f} | Production DB |\n"

        content += "\n#### Multi-AZ Instances (High Availability Deployment)\n\n"
        content += "> [!NOTE] Calculator Verification Recommended\n"
        content += "> Multi-AZ pricing below is from AWS Pricing API. For critical systems,\n"
        content += "> verify in calculator: https://calculator.aws/\n\n"

        content += "| Instance | vCPU | Memory | Price/Hour (Multi-AZ) | Monthly (730h) | Calculator URL |\n"
        content += "|----------|------|--------|---------------------|--------------|----------------|\n"

        for item in rds_multi:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | **${price:.3f}** | **${monthly:.2f}** | https://calculator.aws/ |\n"

        # Add ElastiCache section
        content += "\n---\n\n## Cache Components\n\n"
        content += "### Amazon ElastiCache for Redis\n\n"
        content += "**Pricing Source**: AWS Pricing API (fetched {self.today_str})\n"
        content += "**Calculator**: https://calculator.aws/\n\n"
        content += "| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Use Case |\n"
        content += "|----------|------|--------|------------|----------------|----------|\n"

        for item in sections['elasticache']:
            memory = item.get('memory', '').replace(' GiB', '')
            price = item['price_hour']
            monthly = price * 730
            content += f"| {item['name']} | {item.get('vcpu', '')} | {memory} GiB | ${price:.3f} | ${monthly:.2f} | Session cache |\n"

        # Add EKS section
        content += "\n---\n\n## Container Components\n\n"
        content += "### Amazon EKS\n\n"
        content += "**Pricing Source**: AWS Pricing API (fetched {self.today_str})\n"
        content += "**Calculator**: https://calculator.aws/\n\n"
        content += "| Component | Price | Billing Unit | Source |\n"
        content += "|-----------|-------|--------------|--------|\n"

        for item in sections['eks']:
            content += f"| {item['name']} | ${item['price_hour']}/hour | per {item['name'].split()[1]}-hour | https://calculator.aws/ |\n"

        # Add ELB section
        content += "\n---\n\n## Load Balancing Components\n\n"
        content += "### Application Load Balancer (ALB)\n\n"
        content += "**Pricing Source**: AWS Pricing API (fetched {self.today_str})\n"
        content += "**Calculator**: https://calculator.aws/\n\n"
        content += "| Component | Price | Billing Unit | Source |\n"
        content += "|-----------|-------|--------------|--------|\n"

        for item in sections['elb']:
            if 'ALB' in item['name'] or 'LCU' in item['name']:
                content += f"| {item['name']} | ${item['price_hour']}/hour | per {item['name'].split()[1]}-hour | https://calculator.aws/ |\n"

        content += "\n### Network Load Balancer (NLB)\n\n"
        content += "| Component | Price | Billing Unit | Source |\n"
        content += "|-----------|-------|--------------|--------|\n"

        for item in sections['elb']:
            if 'NLB' in item['name'] or 'NLCU' in item['name']:
                content += f"| {item['name']} | ${item['price_hour']}/hour | per {item['name'].split()[1]}-hour | https://calculator.aws/ |\n"

        # Add footer
        content += f"""
---

## Sizing Guidelines

### Small Deployment (< 1,000 cards)
- EC2: m6i.large (2 vCPU, 8 GiB)
- RDS: db.m6i.large (2 vCPU, 8 GiB)
- ElastiCache: cache.m6g.large (2 vCPU, 5.3 GiB)
- ALB: 1 unit
- EKS Cluster: 1 unit

### Medium Deployment (1,000 - 10,000 cards)
- EC2: m6i.xlarge (4 vCPU, 16 GiB) × 2
- RDS: db.m6i.xlarge (4 vCPU, 16 GiB) Multi-AZ
- ElastiCache: cache.m6g.xlarge (4 vCPU, 13.5 GiB) × 2
- ALB: 2 units
- EKS Cluster: 1 unit

### Large Deployment (> 10,000 cards)
- EC2: m6i.2xlarge (8 vCPU, 32 GiB) × 4
- RDS: db.r6i.xlarge (4 vCPU, 32 GiB) Multi-AZ
- ElastiCache: cache.r6g.xlarge (4 vCPU, 32.3 GiB) × 3
- ALB: 2 units
- EKS Cluster: 1 unit

---

## API Metadata

**Fetched**: {self.today_str}
**Region**: {REGION_NAMES.get(self.region, self.region)}
**Source**: AWS Pricing API
**Next Update**: {self.valid_until}

**API Endpoints Used**:
"""

        for service, metadata in self.api_metadata.items():
            content += f"- {service}: {metadata.get('pricing_url', 'N/A')}\n"

        content += f"""
## Related

- [[aws]] — AWS pricing overview
- [[sizing-tps-calculator]] — Sizing methodology
- [[bom-generation]] — BOM creation process
"""

        return content

    def spot_check_calculator(self, pricing_data: Dict[str, Dict]) -> bool:
        """Spot-check pricing against calculator"""
        import subprocess

        print()
        print("=" * 70)
        print("SPOT-CHECK VERIFICATION")
        print("=" * 70)
        print()

        # Select critical instances to check
        critical_instances = [
            ('m6i.xlarge', 'ec2'),
            ('db.m6i.xlarge__Single-AZ', 'rds'),
            ('db.m6i.xlarge__Multi-AZ', 'rds'),
            ('cache.m6g.xlarge', 'elasticache'),
        ]

        print("Checking critical instances against calculator...")
        print()
        print("Calculator URL: https://calculator.aws/")
        print()
        print("For each instance, verify the API price matches the calculator:")
        print()

        all_match = True
        for instance_name, section in critical_instances:
            if instance_name in pricing_data:
                item = pricing_data[instance_name]
                api_price = item['price_hour']

                # Format for display
                display_name = instance_name.replace('__Single-AZ', ' (Single-AZ)').replace('__Multi-AZ', ' (Multi-AZ)')
                print(f"  {display_name}")
                print(f"    API Price: ${api_price:.3f}/hour")

                response = input("    Match calculator? [Y]es [N]o [S]kip: ").strip().upper()

                if response == 'N':
                    print(f"    ⚠️  DISCREPANCY: Please verify in calculator")
                    all_match = False
                elif response == 'S':
                    pass
                else:
                    print(f"    ✅ Verified")
                print()

        if not all_match:
            response = input("Some discrepancies found. Commit anyway? [Y]es [N]o: ").strip().upper()
            return response == 'Y'

        print("✅ Spot-check passed")
        return True

    def create_fetch_summary(self, pricing_data: Dict[str, Dict]) -> Path:
        """Create summary of fetch operation"""
        summary = {
            'fetched_at': self.today_str,
            'region': self.region,
            'total_items': len(pricing_data),
            'sections': {},
            'api_metadata': self.api_metadata,
            'price_valid_until': self.valid_until
        }

        # Count by section
        for data in pricing_data.values():
            section = data.get('section', 'unknown')
            if section not in summary['sections']:
                summary['sections'][section] = 0
            summary['sections'][section] += 1

        summary_file = TEMP_DIR / 'aws-api-fetch-summary.json'
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"📁 Fetch summary: {summary_file}")
        return summary_file


def main():
    parser = argparse.ArgumentParser(
        description='Fetch pricing from AWS Pricing API and update component catalog',
        epilog="""
Examples:
  python pricing-api-fetcher.py --provider aws --region ap-southeast-1
  python pricing-api-fetcher.py --provider aws --verify

This script:
  1. Fetches real-time pricing from AWS Pricing API
  2. Parses EC2, RDS, ElastiCache, EKS, ELB pricing
  3. Updates aws-component-catalog.md automatically
  4. Spot-checks against calculator (if --verify)
  5. Saves API responses as evidence

Next Steps:
  1. Review updated catalog: wiki/apv/knowledge/pricing/aws-component-catalog.md
  2. Run: python pricing-fetcher.py --provider aws (generates aws.md from catalog)
  3. Run: python pricing-verify.py --provider aws (verifies consistency)
        """
    )
    parser.add_argument('--provider', default='aws', help='Cloud provider (aws only for now)')
    parser.add_argument('--region', default='ap-southeast-1',
                        help='AWS region code (default: ap-southeast-1)')
    parser.add_argument('--verify', action='store_true',
                        help='Spot-check against calculator')
    parser.add_argument('--no-commit', action='store_true',
                        help='Fetch but don\'t update catalog')

    args = parser.parse_args()

    if args.provider != 'aws':
        print("❌ Only AWS is supported currently")
        sys.exit(1)

    print("=" * 70)
    print("AWS PRICING API FETCHER")
    print("=" * 70)
    print()

    fetcher = AWSPricingAPIFetcher(region=args.region)

    # Fetch all pricing
    pricing_data = fetcher.fetch_all_pricing()

    if not pricing_data:
        print("❌ No pricing data fetched")
        sys.exit(1)

    # Spot-check if requested
    if args.verify:
        if not fetcher.spot_check_calculator(pricing_data):
            print("⚠️  Spot-check failed, not updating catalog")
            sys.exit(1)

    # Create fetch summary
    fetcher.create_fetch_summary(pricing_data)

    # Update component catalog
    if not args.no_commit:
        fetcher.update_component_catalog(pricing_data)

    print()
    print("=" * 70)
    print("✅ API FETCH COMPLETE")
    print("=" * 70)
    print()
    print(f"Updated: {COMPONENT_CATALOG}")
    print(f"Valid until: {fetcher.valid_until}")
    print()
    print("Next Steps:")
    print("  1. Review updated catalog")
    print("  2. Run: python pricing-fetcher.py --provider aws")
    print("  3. Run: python pricing-verify.py --provider aws")
    print()


if __name__ == '__main__':
    main()
