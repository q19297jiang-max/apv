#!/usr/bin/env python3
"""
Pricing Freshness Checker for APV Accuracy Assurance

Checks that pricing data is current and alerts when refresh is needed.

Pricing Freshness Rules:
- Pricing pages: max 30 days old
- Alert at 25 days
- Block from RFP use if expired

Usage:
    python3 check-pricing-freshness.py --file <markdown-file>
    python3 check-pricing-freshness.py --directory <pricing-directory>
    python3 check-pricing-freshness.py --project <project-path>
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class FreshnessResult:
    """Result of freshness check."""
    def __init__(self):
        self.current = []      # Within validity period
        self.warning = []      # Approaching expiration (25+ days)
        self.expired = []      # Past validity period (30+ days)
        self.missing = []      # No date found

    def total_issues(self) -> int:
        return len(self.warning) + len(self.expired) + len(self.missing)

    def can_use_in_rfp(self) -> bool:
        """Check if all pricing is current enough for RFP use."""
        return len(self.expired) == 0 and len(self.missing) == 0


def extract_dates_from_frontmatter(content: str) -> Dict[str, Optional[datetime]]:
    """Extract date fields from YAML frontmatter."""
    dates = {
        'captured_date': None,
        'verified_date': None,
        'price_valid_until': None,
        'updated': None,
        'created': None,
    }

    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        for field in dates.keys():
            # Try multiple date formats
            patterns = [
                f'{field}:\\s*([\\d-]+)',  # YYYY-MM-DD
                f'{field}:\\s*"([^"]+)"',
                f'{field}:\\s*\'([^\']+)\'',
            ]
            for pattern in patterns:
                match = re.search(pattern, frontmatter)
                if match:
                    date_str = match.group(1)
                    try:
                        dates[field] = datetime.fromisoformat(date_str)
                    except ValueError:
                        # Try other common formats
                        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                            try:
                                dates[field] = datetime.strptime(date_str, fmt)
                                break
                            except ValueError:
                                pass
                    break

    return dates


def check_freshness(file_path: Path, max_age_days: int = 30, warning_days: int = 25) -> Dict:
    """Check freshness of a single pricing file."""
    result = {
        'file': str(file_path),
        'status': 'unknown',
        'dates': {},
        'age_days': None,
        'valid_until': None,
        'issue': None
    }

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        result['status'] = 'error'
        result['issue'] = f'Cannot read file: {e}'
        return result

    dates = extract_dates_from_frontmatter(content)
    result['dates'] = {k: v.isoformat() if v else None for k, v in dates.items()}

    # Determine which date to use for freshness check
    # Priority: price_valid_until > verified_date > captured_date > updated > created
    reference_date = None
    reference_field = None

    for field in ['price_valid_until', 'verified_date', 'captured_date', 'updated', 'created']:
        if dates[field]:
            reference_date = dates[field]
            reference_field = field
            break

    if not reference_date:
        result['status'] = 'missing'
        result['issue'] = 'No date found in frontmatter'
        return result

    result['reference_field'] = reference_field
    result['reference_date'] = reference_date.isoformat()

    now = datetime.now()
    age_days = (now - reference_date).days

    if reference_field == 'price_valid_until':
        # This is an expiration date
        days_until = (reference_date - now).days
        result['days_until_expiry'] = days_until

        if days_until < 0:
            result['status'] = 'expired'
            result['age_days'] = abs(days_until)
            result['issue'] = f'Expired {abs(days_until)} days ago'
        elif days_until <= (max_age_days - warning_days):
            result['status'] = 'warning'
            result['age_days'] = days_until
            result['issue'] = f'Expires in {days_until} days'
        else:
            result['status'] = 'current'
            result['age_days'] = days_until
    else:
        # This is a capture/verification date - check age
        result['age_days'] = age_days

        if age_days > max_age_days:
            result['status'] = 'expired'
            result['issue'] = f'{age_days} days old (max {max_age_days})'
        elif age_days >= warning_days:
            result['status'] = 'warning'
            result['issue'] = f'{age_days} days old (refresh at {warning_days})'
        else:
            result['status'] = 'current'

    return result


def check_directory(directory: Path, max_age_days: int = 30, warning_days: int = 25) -> FreshnessResult:
    """Check freshness of all pricing files in a directory."""
    result = FreshnessResult()

    for md_file in directory.rglob("*.md"):
        check = check_freshness(md_file, max_age_days, warning_days)

        if check['status'] == 'current':
            result.current.append(check)
        elif check['status'] == 'warning':
            result.warning.append(check)
        elif check['status'] == 'expired':
            result.expired.append(check)
        elif check['status'] == 'missing':
            result.missing.append(check)

    return result


def check_project(project_path: Path, max_age_days: int = 30, warning_days: int = 25) -> FreshnessResult:
    """Check freshness of pricing in an APV project."""
    result = FreshnessResult()

    # Check pricing output
    pricing_file = project_path / "outputs" / "05-pricing.md"
    if pricing_file.exists():
        check = check_freshness(pricing_file, max_age_days, warning_days)

        if check['status'] == 'current':
            result.current.append(check)
        elif check['status'] == 'warning':
            result.warning.append(check)
        elif check['status'] == 'expired':
            result.expired.append(check)
        elif check['status'] == 'missing':
            result.missing.append(check)

    # Check BOM evidence files
    evidence_dir = project_path / "evidence" / "pricing"
    if evidence_dir.exists():
        for date_dir in evidence_dir.iterdir():
            if date_dir.is_dir():
                bom_file = date_dir / "bom.md"
                if bom_file.exists():
                    check = check_freshness(bom_file, max_age_days, warning_days)

                    if check['status'] == 'current':
                        result.current.append(check)
                    elif check['status'] == 'warning':
                        result.warning.append(check)
                    elif check['status'] == 'expired':
                        result.expired.append(check)
                    elif check['status'] == 'missing':
                        result.missing.append(check)

                verification_file = date_dir / "calculator-verification.md"
                if verification_file.exists():
                    check = check_freshness(verification_file, max_age_days, warning_days)

                    if check['status'] == 'current':
                        result.current.append(check)
                    elif check['status'] == 'warning':
                        result.warning.append(check)
                    elif check['status'] == 'expired':
                        result.expired.append(check)
                    elif check['status'] == 'missing':
                        result.missing.append(check)

    return result


def print_results(result: FreshnessResult, max_age_days: int = 30, verbose: bool = False):
    """Print freshness check results."""
    print("\n" + "=" * 60)
    print(f"PRICING FRESHNESS CHECK (Max age: {max_age_days} days)")
    print("=" * 60)

    print(f"\n✅ Current: {len(result.current)} files")
    print(f"⚠️  Warning (approaching refresh): {len(result.warning)} files")
    print(f"❌ Expired (needs refresh): {len(result.expired)} files")
    print(f"❓ Missing dates: {len(result.missing)} files")

    print(f"\nTotal Issues: {result.total_issues()}")

    if result.can_use_in_rfp():
        print("\n✅ FRESHNESS CHECK PASSED - All pricing is current")
        if result.warning:
            print(f"   Note: {len(result.warning)} files will need refresh soon")
        return 0
    else:
        print("\n❌ FRESHNESS CHECK FAILED - Pricing refresh required")

        if result.expired:
            print(f"\n❌ EXPIRED ({len(result.expired)} files):")
            print("   These files MUST be refreshed before use in RFPs:\n")
            for item in result.expired[:10]:
                print(f"   - {item['file']}")
                print(f"     {item['issue']}")

        if result.missing:
            print(f"\n❓ MISSING DATES ({len(result.missing)} files):")
            print("   These files need date information added:\n")
            for item in result.missing[:10]:
                print(f"   - {item['file']}")

        if result.warning:
            print(f"\n⚠️  WARNING ({len(result.warning)} files):")
            print("   These files will need refresh soon:\n")
            for item in result.warning[:10]:
                print(f"   - {item['file']}")
                print(f"     {item['issue']}")

        print(f"\nAction Required:")
        print(f"1. Refresh expired pricing from official calculators")
        print(f"2. Add dates to files with missing dates")
        print(f"3. Update verified_date in frontmatter")

        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Check pricing data freshness'
    )
    parser.add_argument('--file', type=Path, help='Check single markdown file')
    parser.add_argument('--directory', type=Path, help='Check directory of pricing files')
    parser.add_argument('--project', type=Path, help='Check APV project pricing')
    parser.add_argument('--max-age', type=int, default=30,
                        help='Maximum age in days (default: 30)')
    parser.add_argument('--warning-age', type=int, default=25,
                        help='Warning age in days (default: 25)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--output', '-o', type=Path, help='Output results to JSON file')

    args = parser.parse_args()

    result = FreshnessResult()

    if args.file:
        check = check_freshness(args.file, args.max_age, args.warning_age)
        if check['status'] == 'current':
            result.current.append(check)
        elif check['status'] == 'warning':
            result.warning.append(check)
        elif check['status'] == 'expired':
            result.expired.append(check)
        else:
            result.missing.append(check)
    elif args.directory:
        result = check_directory(args.directory, args.max_age, args.warning_age)
    elif args.project:
        result = check_project(args.project, args.max_age, args.warning_age)
    else:
        parser.print_help()
        return 1

    # Print results
    exit_code = print_results(result, args.max_age, args.verbose)

    # Save to JSON if requested
    if args.output:
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'max_age_days': args.max_age,
            'warning_age_days': args.warning_age,
            'current': result.current,
            'warning': result.warning,
            'expired': result.expired,
            'missing': result.missing,
            'total_issues': result.total_issues(),
            'can_use_in_rfp': result.can_use_in_rfp()
        }
        args.output.write_text(json.dumps(output_data, indent=2))

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
