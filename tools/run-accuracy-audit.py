#!/usr/bin/env python3
"""
APV Accuracy Audit Tool

Runs monthly accuracy audits on compliance and pricing content.
Checks for:
- Missing source URLs
- Broken source URLs
- Forbidden sources
- Stale pricing data (>30 days)
- Missing verification dates

Usage:
    python3 run-accuracy-audit.py --wiki <wiki-directory>
    python3 run-accuracy-audit.py --projects <projects-directory>
    python3 run-accuracy-audit.py --full
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class AuditResult:
    """Result of accuracy audit."""
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.compliance_pages = {'total': 0, 'issues': []}
        self.pricing_pages = {'total': 0, 'issues': []}
        self.projects = {'total': 0, 'issues': []}
        self.summary = {
            'total_items': 0,
            'total_issues': 0,
            'compliance_rate': 0.0,
            'needs_action': []
        }

    def add_compliance_issue(self, file_path: str, issue: str):
        self.compliance_pages['issues'].append((file_path, issue))

    def add_pricing_issue(self, file_path: str, issue: str):
        self.pricing_pages['issues'].append((file_path, issue))

    def add_project_issue(self, project_path: str, issue: str):
        self.projects['issues'].append((project_path, issue))

    def calculate_summary(self):
        self.summary['total_items'] = (
            self.compliance_pages['total'] +
            self.pricing_pages['total'] +
            self.projects['total']
        )
        self.summary['total_issues'] = (
            len(self.compliance_pages['issues']) +
            len(self.pricing_pages['issues']) +
            len(self.projects['issues'])
        )

        if self.summary['total_items'] > 0:
            self.summary['compliance_rate'] = (
                (self.summary['total_items'] - self.summary['total_issues']) /
                self.summary['total_items'] * 100
            )

        # Determine items needing action
        if self.compliance_pages['issues']:
            self.summary['needs_action'].append('Compliance pages need review')
        if self.pricing_pages['issues']:
            self.summary['needs_action'].append('Pricing pages need refresh')
        if self.projects['issues']:
            self.summary['needs_action'].append('Projects need validation')


def audit_compliance_page(file_path: Path) -> List[str]:
    """Audit a single compliance page for accuracy issues."""
    issues = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return [f'Cannot read file: {e}']

    # Check for source URL in frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        issues.append('Missing frontmatter')
        return issues

    frontmatter = frontmatter_match.group(1)

    # Check for source_url field
    if not re.search(r'source_url:', frontmatter):
        issues.append('Missing source_url in frontmatter')
    else:
        url_match = re.search(r'source_url:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
        if url_match:
            url = url_match.group(1).strip()
            if not url.startswith('http'):
                issues.append(f'Invalid source_url format: {url}')
            elif 'wikipedia.org' in url or 'blogspot.com' in url:
                issues.append(f'Forbidden source: {url}')

    # Check for verified_date
    if not re.search(r'verified_date:', frontmatter):
        issues.append('Missing verified_date')

    # Check for source version
    if not re.search(r'source_version|version:', frontmatter):
        issues.append('Missing source version')

    return issues


def audit_pricing_page(file_path: Path) -> List[str]:
    """Audit a single pricing page for accuracy issues."""
    issues = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return [f'Cannot read file: {e}']

    # Check frontmatter for pricing fields
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        issues.append('Missing frontmatter')
        return issues

    frontmatter = frontmatter_match.group(1)

    # Check for source_url or calculator_url
    has_source = (
        re.search(r'source_url:', frontmatter) or
        re.search(r'calculator_url:', frontmatter)
    )
    if not has_source:
        issues.append('Missing source_url or calculator_url')

    # Check for verified_date or captured_date
    has_date = (
        re.search(r'verified_date:', frontmatter) or
        re.search(r'captured_date:', frontmatter)
    )
    if not has_date:
        issues.append('Missing verified_date or captured_date')

    # Check for price_valid_until
    if not re.search(r'price_valid_until:', frontmatter):
        issues.append('Missing price_valid_until date')

    # Check if pricing is stale (>30 days)
    date_fields = ['verified_date', 'captured_date', 'price_valid_until']
    for field in date_fields:
        match = re.search(f'{field}:\\s*"?([\\d-]+)"?', frontmatter)
        if match:
            date_str = match.group(1)
            try:
                date = datetime.fromisoformat(date_str)
                age_days = (datetime.now() - date).days

                if field == 'price_valid_until':
                    # This is an expiration date
                    if age_days > 0:
                        issues.append(f'Pricing expired {age_days} days ago')
                else:
                    # This is a verification date
                    if age_days > 30:
                        issues.append(f'Pricing stale ({age_days} days old, max 30)')
                break
            except ValueError:
                pass

    return issues


def audit_project(project_path: Path) -> List[str]:
    """Audit a single APV project for accuracy issues."""
    issues = []

    # Check if source URL validation passes
    try:
        result = subprocess.run(
            ['python3', 'wiki/apv/tools/validate-source-urls.py', '--project', str(project_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            issues.append('Source URL validation failed')
    except Exception as e:
        issues.append(f'Cannot run source URL validation: {e}')

    # Check if freshness check passes
    try:
        result = subprocess.run(
            ['python3', 'wiki/apv/tools/check-pricing-freshness.py', '--project', str(project_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            issues.append('Pricing freshness check failed')
    except Exception as e:
        issues.append(f'Cannot run freshness check: {e}')

    # Check for evidence files
    pricing_output = project_path / "outputs" / "05-pricing.md"
    if pricing_output.exists():
        # Check if BOM evidence exists
        evidence_dir = project_path / "evidence" / "pricing"
        if not evidence_dir.exists():
            issues.append('Missing pricing evidence directory')
        else:
            has_bom = False
            has_verification = False
            for date_dir in evidence_dir.iterdir():
                if date_dir.is_dir():
                    if (date_dir / "bom.md").exists():
                        has_bom = True
                    if (date_dir / "calculator-verification.md").exists():
                        has_verification = True

            if not has_bom:
                issues.append('Missing BOM evidence file')
            if not has_verification:
                issues.append('Missing calculator verification file')

    return issues


def audit_wiki_directory(wiki_dir: Path, result: AuditResult):
    """Audit all compliance and pricing pages in wiki directory."""
    print(f"\nAuditing wiki directory: {wiki_dir}")

    # Audit compliance pages
    compliance_dir = wiki_dir / "apv" / "knowledge" / "compliance"
    if compliance_dir.exists():
        for md_file in compliance_dir.rglob("*.md"):
            result.compliance_pages['total'] += 1
            issues = audit_compliance_page(md_file)
            for issue in issues:
                result.add_compliance_issue(str(md_file.relative_to(wiki_dir)), issue)

    # Audit pricing pages
    pricing_dir = wiki_dir / "apv" / "knowledge" / "pricing"
    if pricing_dir.exists():
        for md_file in pricing_dir.rglob("*.md"):
            result.pricing_pages['total'] += 1
            issues = audit_pricing_page(md_file)
            for issue in issues:
                result.add_pricing_issue(str(md_file.relative_to(wiki_dir)), issue)


def audit_projects_directory(projects_dir: Path, result: AuditResult):
    """Audit all APV projects."""
    print(f"\nAuditing projects directory: {projects_dir}")

    for project_dir in projects_dir.glob("apv-projects-*"):
        if project_dir.is_dir():
            result.projects['total'] += 1
            issues = audit_project(project_dir)
            for issue in issues:
                result.add_project_issue(project_dir.name, issue)


def print_audit_report(result: AuditResult):
    """Print audit report."""
    print("\n" + "=" * 70)
    print("APV ACCURACY AUDIT REPORT")
    print("=" * 70)
    print(f"Audit Date: {result['timestamp']}")
    print("=" * 70)

    # Compliance Pages
    print(f"\n📋 Compliance Pages")
    print(f"   Total: {result['compliance_pages']['total']}")
    print(f"   Issues: {len(result['compliance_pages']['issues'])}")
    if result['compliance_pages']['issues']:
        print("\n   Issues Found:")
        for file, issue in result['compliance_pages']['issues'][:10]:
            print(f"   - {file}")
            print(f"     {issue}")

    # Pricing Pages
    print(f"\n💰 Pricing Pages")
    print(f"   Total: {result['pricing_pages']['total']}")
    print(f"   Issues: {len(result['pricing_pages']['issues'])}")
    if result['pricing_pages']['issues']:
        print("\n   Issues Found:")
        for file, issue in result['pricing_pages']['issues'][:10]:
            print(f"   - {file}")
            print(f"     {issue}")

    # Projects
    print(f"\n📁 Projects")
    print(f"   Total: {result['projects']['total']}")
    print(f"   Issues: {len(result['projects']['issues'])}")
    if result['projects']['issues']:
        print("\n   Issues Found:")
        for project, issue in result['projects']['issues'][:10]:
            print(f"   - {project}")
            print(f"     {issue}")

    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total Items Audited: {result['summary']['total_items']}")
    print(f"Total Issues Found: {result['summary']['total_issues']}")
    print(f"Compliance Rate: {result['summary']['compliance_rate']:.1f}%")

    if result['summary']['compliance_rate'] >= 95:
        print("\n✅ ACCURACY TARGET MET (>95%)")
    else:
        print(f"\n❌ ACCURACY TARGET NOT MET (<95%)")

    if result['summary']['needs_action']:
        print("\nAction Required:")
        for action in result['summary']['needs_action']:
            print(f"  - {action}")

    print(f"\n{'=' * 70}")


def main():
    parser = argparse.ArgumentParser(
        description='Run APV accuracy audit'
    )
    parser.add_argument('--wiki', type=Path, help='Audit wiki directory')
    parser.add_argument('--projects', type=Path, help='Audit projects directory')
    parser.add_argument('--full', action='store_true', help='Run full audit (wiki + projects)')
    parser.add_argument('--output', '-o', type=Path, help='Output results to JSON file')

    args = parser.parse_args()

    result = AuditResult()

    # Determine what to audit
    if args.full:
        # Audit both wiki and projects
        wiki_dir = Path.cwd()
        projects_dir = Path.cwd() / "apv-projects"

        audit_wiki_directory(wiki_dir, result)
        audit_projects_directory(projects_dir, result)

    elif args.wiki:
        audit_wiki_directory(args.wiki, result)

    elif args.projects:
        audit_projects_directory(args.projects, result)

    else:
        parser.print_help()
        return 1

    # Calculate summary
    result.calculate_summary()

    # Print report
    print_audit_report(result.__dict__)

    # Save to JSON if requested
    if args.output:
        args.output.write_text(json.dumps(result.__dict__, indent=2))

    # Exit code based on compliance rate
    if result.summary['compliance_rate'] >= 95:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
