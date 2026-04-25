#!/usr/bin/env python3
"""
APV Pricing Verification - Interactive verification workflow

This script provides an interactive verification workflow for pricing updates:
1. Reads fetched pricing from temp directory
2. Reads pricing from aws-component-catalog.md (source of truth)
3. Compares values and flags discrepancies
4. Opens calculator URLs for manual verification
5. Prompts user to resolve differences
6. Generates verification report

Usage:
    python pricing-verify.py --provider aws
    python pricing-verify.py --all
"""

import sys
import json
import subprocess
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configuration
TEMP_DIR = Path('/tmp/apv-pricing-updates')
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')
EVIDENCE_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/evidence/pricing')
COMPONENT_CATALOG = PRICING_DIR / 'aws-component-catalog.md'

# Calculator URLs
CALCULATOR_URLS = {
    'aws': 'https://calculator.aws/',
    'azure': 'https://azure.microsoft.com/pricing/',
    'gcp': 'https://cloud.google.com/products/calculator'
}


class PricingVerifier:
    """Interactive pricing verification workflow"""

    # Multiplier for RDS Multi-AZ pricing (approximately 2-3x single-AZ)
    MULTI_AZ_MULTIPLIER = 2.0

    def __init__(self, provider: str):
        self.provider = provider
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.temp_file = TEMP_DIR / f'{provider}.md'
        self.evidence_file = EVIDENCE_DIR / self.today / f'{provider}-api-response.json'
        self.component_catalog = COMPONENT_CATALOG if provider == 'aws' else None
        self.verification_results = []
        self.discrepancies = []

    def read_component_catalog_pricing(self) -> Dict[str, Dict[str, Any]]:
        """Read pricing from aws-component-catalog.md (source of truth)"""
        if not self.component_catalog or not self.component_catalog.exists():
            return {}

        catalog_pricing = {}
        with open(self.component_catalog, 'r') as f:
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
                # This is a header row, find the price column index
                headers = [p.strip() for p in line.split('|')[1:-1]]
                price_col_index = headers.index('Price/Hour') if 'Price/Hour' in headers else -1

                if price_col_index == -1:
                    continue

                # Read data rows starting from next line
                for j in range(i + 2, len(lines)):
                    row = lines[j]
                    if not row.startswith('|'):
                        break
                    if '---' in row:
                        continue

                    parts = [p.strip() for p in row.split('|')[1:-1]]
                    if len(parts) > price_col_index and parts[0] not in ['Instance', 'Component', '', '***']:
                        name = parts[0].replace('**', '').replace('*', '').strip()
                        price_str = parts[price_col_index]

                        # Extract price value (handle $ signs and USD)
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
        # Remove $, commas, and extract number
        clean = price_str.replace('$', '').replace(',', '').strip()
        match = re.search(r'([\d,]+\.?\d*)', clean)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        return None

    def read_fetched_pricing(self) -> Dict[str, Any]:
        """Read fetched pricing from temp file"""
        if not self.temp_file.exists():
            print(f"❌ No fetched pricing found for {self.provider}")
            print(f"   Run: python pricing-fetcher.py --provider {self.provider}")
            return {}

        with open(self.temp_file, 'r') as f:
            content = f.read()

        # Parse pricing from markdown
        pricing_items = self._parse_pricing_table(content)
        return {'content': content, 'items': pricing_items}

    def _parse_pricing_table(self, markdown: str) -> List[Dict[str, Any]]:
        """Parse pricing items from markdown table"""
        items = []
        lines = markdown.split('\n')

        for i, line in enumerate(lines):
            if line.startswith('|') and 'Instance' in line and 'Price/Hour' in line:
                # Found pricing table header, read next lines
                for j in range(i + 2, len(lines)):
                    row = lines[j]
                    if not row.startswith('|'):
                        break
                    if '---' in row:
                        continue

                    parts = [p.strip() for p in row.split('|')[1:-1]]  # Remove empty first/last
                    if len(parts) >= 5 and parts[0] not in ['Instance', 'Component']:
                        items.append({
                            'name': parts[0],
                            'price': parts[3],
                            'calculator_url': parts[-1] if parts[-1].startswith('http') else CALCULATOR_URLS.get(self.provider, '')
                        })

        return items

    def read_api_evidence(self) -> Dict[str, Any]:
        """Read API response evidence"""
        if not self.evidence_file.exists():
            return {}

        with open(self.evidence_file, 'r') as f:
            return json.load(f)

    def detect_discrepancies(self, temp_items: List[Dict], catalog_pricing: Dict) -> List[Dict]:
        """Detect pricing discrepancies between temp file and component catalog"""
        discrepancies = []

        if not catalog_pricing:
            return discrepancies

        # Create a lookup from temp items
        temp_pricing = {}
        for item in temp_items:
            name = item['name']
            price = self.parse_price_from_string(item.get('price', ''))
            if price:
                temp_pricing[name] = price

        # Compare each catalog item with temp pricing
        for catalog_name, catalog_data in catalog_pricing.items():
            catalog_price = catalog_data['price_hour']

            if catalog_name in temp_pricing:
                temp_price = temp_pricing[catalog_name]

                # Check for significant difference (>5%)
                if abs(temp_price - catalog_price) > (catalog_price * 0.05):
                    discrepancies.append({
                        'instance': catalog_name,
                        'catalog_price': catalog_price,
                        'temp_price': temp_price,
                        'difference_pct': ((temp_price - catalog_price) / catalog_price) * 100,
                        'section': catalog_data['section'],
                        'type': 'price_mismatch'
                    })
            else:
                # Item in catalog but not in temp
                discrepancies.append({
                    'instance': catalog_name,
                    'catalog_price': catalog_price,
                    'temp_price': None,
                    'difference_pct': None,
                    'section': catalog_data['section'],
                    'type': 'missing_in_temp'
                })

        # Check for items in temp but not in catalog
        for temp_name in temp_pricing:
            if temp_name not in catalog_pricing:
                discrepancies.append({
                    'instance': temp_name,
                    'catalog_price': None,
                    'temp_price': temp_pricing[temp_name],
                    'difference_pct': None,
                    'section': 'unknown',
                    'type': 'missing_in_catalog'
                })

        return discrepancies

    def display_discrepancy_report(self, discrepancies: List[Dict]) -> bool:
        """Display discrepancy report and require resolution"""
        if not discrepancies:
            return True

        print("=" * 70)
        print("⚠️  PRICING DISCREPANCIES DETECTED")
        print("=" * 70)
        print()
        print("The following differences were found between:")
        print(f"  - Component Catalog: {self.component_catalog}")
        print(f"  - Temp File: {self.temp_file}")
        print()

        # Group by type
        price_mismatches = [d for d in discrepancies if d['type'] == 'price_mismatch']
        missing_in_temp = [d for d in discrepancies if d['type'] == 'missing_in_temp']
        missing_in_catalog = [d for d in discrepancies if d['type'] == 'missing_in_catalog']

        if price_mismatches:
            print("PRICE MISMATCHES:")
            print("-" * 70)
            for d in price_mismatches:
                print(f"  {d['instance']}:")
                print(f"    Catalog: ${d['catalog_price']:.3f}/hour")
                print(f"    Temp:    ${d['temp_price']:.3f}/hour")
                print(f"    Diff:    {d['difference_pct']:+.1f}%")
                print()

        if missing_in_temp:
            print("MISSING IN TEMP FILE (in catalog but not temp):")
            print("-" * 70)
            for d in missing_in_temp[:10]:  # Limit to 10
                print(f"  {d['instance']}: ${d['catalog_price']:.3f}/hour")
            if len(missing_in_temp) > 10:
                print(f"  ... and {len(missing_in_temp) - 10} more")
            print()

        if missing_in_catalog:
            print("MISSING IN CATALOG (in temp but not catalog):")
            print("-" * 70)
            for d in missing_in_catalog[:10]:  # Limit to 10
                print(f"  {d['instance']}: ${d['temp_price']:.3f}/hour")
            if len(missing_in_catalog) > 10:
                print(f"  ... and {len(missing_in_catalog) - 10} more")
            print()

        print("Possible Causes:")
        print("  1. Calculator pricing has changed (most common)")
        print("  2. Component catalog is outdated")
        print("  3. Multi-AZ vs Single-AZ confusion")
        print("  4. Regional pricing differences")
        print()

        print("Resolution Options:")
        print("  [U]se Calculator  - Trust calculator (temp file), update catalog")
        print("  [K]eep Catalog    - Trust catalog, reject temp file")
        print("  [I]nvestigate     - Open calculator and investigate manually")
        print("  [A]bort           - Cancel verification")
        print()

        while True:
            response = input("How do you want to resolve? [U/K/I/A]: ").strip().upper()
            if response == 'U':
                print("  → Will use calculator pricing (trust temp file)")
                print("  ⚠️  Note: Component catalog should be updated separately")
                return True
            elif response == 'K':
                print("  → Will use catalog pricing (reject temp file)")
                print("  ⚠️  Note: Temp file needs correction")
                return False
            elif response == 'I':
                self._open_calculator(CALCULATOR_URLS.get(self.provider, ''))
                print("  → Calculator opened. Please investigate and return.")
                continue
            elif response == 'A':
                print("  → Verification aborted")
                return False
            else:
                print("  Invalid option. Try again.")

    def display_verification_report(self):
        """Display interactive verification report"""
        print("=" * 70)
        print(f"PRICING VERIFICATION: {self.provider.upper()}")
        print("=" * 70)
        print()

        # Read fetched pricing
        pricing_data = self.read_fetched_pricing()
        if not pricing_data:
            return False

        items = pricing_data.get('items', [])
        api_data = self.read_api_evidence()

        # Read component catalog pricing
        catalog_pricing = self.read_component_catalog_pricing()
        print(f"📊 Component Catalog: {self.component_catalog or 'N/A'}")
        print(f"   Found {len(catalog_pricing)} items in catalog" if catalog_pricing else "   (No component catalog for this provider)")

        if not items:
            print(f"⚠️  No pricing items found to verify")
            print()
            print("Note: This provider requires manual verification.")
            print(f"Please visit: {CALCULATOR_URLS.get(self.provider, '')}")
            return self._prompt_manual_verification()

        print(f"📝 Temp File: {self.temp_file}")
        print(f"   Found {len(items)} items in temp file")
        print()

        # NEW: Detect discrepancies automatically
        if catalog_pricing:
            print("=" * 70)
            print("🔍 RUNNING AUTOMATED VALIDATION")
            print("=" * 70)
            print()

            discrepancies = self.detect_discrepancies(items, catalog_pricing)

            if discrepancies:
                print(f"⚠️  Found {len(discrepancies)} pricing discrepancies")
                print()

                # Require resolution before continuing
                if not self.display_discrepancy_report(discrepancies):
                    print()
                    print("❌ Verification aborted due to unresolved discrepancies")
                    return False
            else:
                print("✅ No discrepancies detected - pricing matches catalog")
                print()

        print("=" * 70)
        print("MANUAL VERIFICATION")
        print("=" * 70)
        print()
        print("Instructions:")
        print("  - Each item will be displayed with price and calculator link")
        print("  - [O]pen calculator to verify")
        print("  - [C]onfirm if correct")
        print("  - [S]kip to defer verification")
        print("  - [Q]uit to cancel")
        print()

        # Verify each item
        for i, item in enumerate(items, 1):
            print(f"[{i}/{len(items)}] {item['name']}")
            print(f"    Temp Price:   {item['price']}")

            # Show catalog price if available
            if item['name'] in catalog_pricing:
                catalog_price = catalog_pricing[item['name']]['price_hour']
                print(f"    Catalog Price: ${catalog_price:.3f}/hour")

            print(f"    Calculator:   {item['calculator_url']}")
            print()

            while True:
                response = input("Verify? [O]pen [C]orrect [S]kip [Q]uit: ").strip().upper()

                if response == 'O':
                    # Open calculator in browser
                    self._open_calculator(item['calculator_url'])
                    print("     → Calculator opened. Please verify and return.")
                    continue
                elif response == 'C':
                    self.verification_results.append({
                        'item': item['name'],
                        'status': 'verified',
                        'temp_price': item['price']
                    })
                    print(f"     ✅ {item['name']}: VERIFIED")
                    break
                elif response == 'S':
                    self.verification_results.append({
                        'item': item['name'],
                        'status': 'deferred',
                        'temp_price': item['price']
                    })
                    print(f"     ⏭️  {item['name']}: DEFERRED")
                    break
                elif response == 'Q':
                    print("     → Verification cancelled")
                    return False
                else:
                    print("     Invalid option. Try again.")

            print()

        return self._summarize_results()

    def _prompt_manual_verification(self) -> bool:
        """Prompt for manual verification (Azure/GCP)"""
        print()
        print("Manual Verification Required")
        print("-" * 40)
        print(f"1. Visit: {CALCULATOR_URLS.get(self.provider, '')}")
        print("2. Select region: Singapore")
        print("3. Verify pricing for common instance types:")
        print("   - Compute: m6i.xlarge, c6i.xlarge, r6i.xlarge")
        print("   - Database: db.m6i.xlarge, db.r6i.2xlarge")
        print("   - Cache: cache.m6g.xlarge")
        print()

        response = input("Have you verified the pricing? [Y]es [N]o: ").strip().upper()

        if response == 'Y':
            self.verification_results.append({
                'item': f'{self.provider}-manual',
                'status': 'verified',
                'note': 'Manually verified by Infrastructure Architect'
            })
            return True
        return False

    def _open_calculator(self, url: str):
        """Open calculator URL in default browser"""
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', url])
            elif sys.platform == 'win32':
                subprocess.run(['start', url], shell=True)
            else:  # Linux
                subprocess.run(['xdg-open', url])
        except Exception as e:
            print(f"     ⚠️  Could not open browser: {e}")
            print(f"     → Please manually open: {url}")

    def _summarize_results(self) -> bool:
        """Summarize verification results"""
        print()
        print("=" * 70)
        print("VERIFICATION SUMMARY")
        print("=" * 70)
        print()

        verified = sum(1 for r in self.verification_results if r['status'] == 'verified')
        deferred = sum(1 for r in self.verification_results if r['status'] == 'deferred')
        total = len(self.verification_results)

        print(f"Provider:        {self.provider.upper()}")
        print(f"Total Items:     {total}")
        print(f"Verified:        ✅ {verified}")
        print(f"Deferred:        ⏭️  {deferred}")
        print(f"Discrepancies:   ⚠️  {len(self.discrepancies)}" if self.discrepancies else f"Discrepancies:   ✅ 0")
        print()

        if deferred > 0:
            print("⚠️  Some items were deferred. You can:")
            print("   1. Complete verification now")
            print("   2. Proceed with commit (deferred items will be noted)")
            print()

            response = input("Proceed with commit? [Y]es [N]o: ").strip().upper()
            return response == 'Y'

        if verified > 0:
            print("✅ All items verified!")
            print()
            print("Next Step:")
            print(f"  Run: python pricing-commit.py --provider {self.provider}")
            print()

        return True

    def save_verification_report(self):
        """Save verification report as evidence"""
        report = {
            'provider': self.provider,
            'date': self.today,
            'verified_by': 'Infrastructure Architect',
            'results': self.verification_results
        }

        report_file = EVIDENCE_DIR / self.today / f'{self.provider}-verification-report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📁 Verification report saved: {report_file}")
        return report_file


def main():
    parser = argparse.ArgumentParser(
        description='Verify pricing updates before committing',
        epilog="""
Examples:
  python pricing-verify.py --provider aws
  python pricing-verify.py --all

Workflow:
  1. Reads fetched pricing from /tmp/apv-pricing-updates/
  2. Displays each item for verification
  3. Opens calculator URLs for manual check
  4. Records verification results
  5. Generates verification report

Next Step:
  python pricing-commit.py --provider <provider>
        """
    )
    parser.add_argument('--provider', choices=['aws', 'azure', 'gcp'],
                        help='Cloud provider')
    parser.add_argument('--all', action='store_true',
                        help='Verify all providers')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else ['aws', 'azure', 'gcp']

    all_passed = True
    for provider in providers:
        verifier = PricingVerifier(provider)
        if not verifier.display_verification_report():
            all_passed = False
            break
        verifier.save_verification_report()

    if all_passed:
        print("=" * 70)
        print("VERIFICATION COMPLETE")
        print("=" * 70)
        sys.exit(0)
    else:
        print("=" * 70)
        print("VERIFICATION INCOMPLETE")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()
