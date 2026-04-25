#!/usr/bin/env python3
"""
Pricing Format Validator - Ensures table format compliance

This script validates that all pricing tables in component catalogs follow
the standard format defined in component-catalog-template.md.

Usage:
    python pricing-format-validator.py --provider aws
    python pricing-format-validator.py --all
"""

import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Configuration
PRICING_DIR = Path('/Users/stevenjiang/workspace/mykb/wiki/apv/knowledge/pricing')

# Required columns for different table types
REQUIRED_COLUMNS = {
    'instance_based': {
        'required': ['instance', 'price/hour', 'monthly (730h)', 'calculator url'],
        'patterns': ['instance', 'vcpu', 'memory', 'storage', 'network']
    },
    'flat_rate': {
        'required': ['component', 'price', 'calculator url'],
        'patterns': ['component', 'billing unit', 'price']
    },
    'storage': {
        'required': ['storage type', 'price/gb-month', 'calculator url'],
        'patterns': ['storage type', 'price/gb-month', 'calculator url']
    },
    'regional_matrix': {
        'required': ['region code', 'calculator url'],
        'patterns': ['region code', 'region name', 'multiplier']
    },
    'savings_plans': {
        'required': ['instance', 'on-demand/hour', 'savings 3yr/hour', 'calculator url'],
        'patterns': ['instance', 'on-demand', 'savings', 'savings %']
    }
}

# Forbidden column names (use standard names instead)
FORBIDDEN_COLUMNS = ['source', 'link', 'url', 'href', 'documentation']


class PricingFormatValidator:
    """Validate pricing table format compliance"""

    def __init__(self, catalog_file: Path):
        self.catalog_file = catalog_file
        self.errors = []
        self.warnings = []
        self.tables_validated = 0

    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"Validating: {self.catalog_file}")
        print()

        with open(self.catalog_file, 'r') as f:
            content = f.read()

        # Check for required elements
        self._check_required_elements(content)

        # Validate all tables
        self._validate_tables(content)

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _check_required_elements(self, content: str):
        """Check for required elements in catalog"""
        # Check for regional pricing matrix
        if 'regional pricing matrix' not in content.lower():
            self.errors.append("❌ Missing Regional Pricing Matrix section")

        # Check for calculator URL references
        if 'calculator.aws' not in content and 'calculator.azure' not in content:
            self.warnings.append("⚠️  No calculator URLs found in catalog")

    def _validate_tables(self, content: str):
        """Validate all tables in the catalog"""
        lines = content.split('\n')
        in_table = False
        table_start = 0
        table_headers = []

        for i, line in enumerate(lines):
            # Detect table start
            if line.startswith('|') and self._is_header_row(line):
                in_table = True
                table_start = i
                table_headers = [h.strip().lower() for h in line.split('|')[1:-1]]

            # Detect table end
            elif in_table and (not line.startswith('|') or line.strip() == ''):
                if i > table_start + 1:  # Table had at least one data row
                    self._validate_table(table_headers, lines[table_start:i])
                in_table = False

    def _is_header_row(self, line: str) -> bool:
        """Check if line is a table header"""
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) < 2:
            return False

        # Must have pricing-related keywords
        keywords = ['instance', 'component', 'vcpu', 'memory', 'price', 'cost',
                   'calculator', 'storage', 'region', 'unit']
        return any(kw in ' '.join(parts).lower() for kw in keywords)

    def _validate_table(self, headers: List[str], table_lines: List[str]):
        """Validate a single table"""
        self.tables_validated += 1

        # Check for forbidden columns
        for header in headers:
            header_lower = header.lower()
            if any(forbidden in header_lower for forbidden in FORBIDDEN_COLUMNS):
                # Allow "source" if it's a URL
                if header_lower == 'source':
                    continue
                # Allow "calculator url" as the standard column name
                if header_lower == 'calculator url':
                    continue
                self.errors.append(f"❌ Table uses forbidden column: '{header}' (use 'Calculator URL' instead)")

        # Check for required columns based on table type
        table_type = self._identify_table_type(headers)

        if table_type:
            required = REQUIRED_COLUMNS[table_type]['required']
            headers_lower = [h.lower() for h in headers]
            missing = [req for req in required if req.lower() not in headers_lower]

            if missing:
                self.errors.append(f"❌ Table missing required columns: {', '.join(missing)}")

    def _identify_table_type(self, headers: List[str]) -> str:
        """Identify the type of pricing table"""
        headers_lower = [h.lower() for h in headers]

        # Check for regional matrix first
        if 'region code' in headers_lower and 'multiplier' in headers_lower:
            return 'regional_matrix'

        # Check for savings plans
        if 'instance' in headers_lower and 'on-demand' in headers_lower and 'savings' in headers_lower:
            return 'savings_plans'

        # Check for instance-based pricing
        if 'instance' in headers_lower:
            return 'instance_based'

        # Check for flat-rate pricing
        elif 'component' in headers_lower and 'billing unit' in headers_lower:
            return 'flat_rate'

        # Check for storage pricing
        elif 'storage type' in headers_lower:
            return 'storage'

        return None

    def _print_results(self):
        """Print validation results"""
        print("=" * 70)
        print("FORMAT VALIDATION RESULTS")
        print("=" * 70)
        print()

        print(f"Tables Validated: {self.tables_validated}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  {error}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if not self.errors:
            print("✅ All tables follow the standard format!")
        else:
            print("❌ Format violations found. See component-catalog-template.md for correct format.")


def main():
    parser = argparse.ArgumentParser(
        description='Validate pricing table format compliance',
        epilog="""
This script validates that all pricing tables in component catalogs follow
the standard format defined in component-catalog-template.md.

Required columns:
  - Instance-based: Instance, vCPU, Memory, Price/Hour, Monthly (730h), Calculator URL
  - Flat-rate: Component, Price, Billing Unit, Calculator URL
  - Storage: Storage Type, Price, Calculator URL

Forbidden columns:
  - Source, Link, URL (use 'Calculator URL' instead)

Examples:
  python pricing-format-validator.py --provider aws
  python pricing-format-validator.py --all
        """
    )

    parser.add_argument('--provider', choices=['aws', 'azure', 'gcp'],
                        help='Cloud provider to validate')
    parser.add_argument('--all', action='store_true',
                        help='Validate all providers')

    args = parser.parse_args()

    if not args.provider and not args.all:
        parser.print_help()
        sys.exit(1)

    providers = [args.provider] if args.provider else ['aws', 'azure', 'gcp']

    all_passed = True
    for provider in providers:
        catalog_file = PRICING_DIR / f'{provider}-component-catalog.md'

        if not catalog_file.exists():
            print(f"⚠️  Catalog not found: {catalog_file}")
            continue

        validator = PricingFormatValidator(catalog_file)
        if not validator.validate():
            all_passed = False

    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
