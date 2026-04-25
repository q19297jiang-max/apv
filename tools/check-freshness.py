#!/usr/bin/env python3
"""
APV Source URL Freshness Checker

Validates that source URLs are within acceptable freshness windows:
- Pricing sources: < 30 days
- Compliance sources: < 365 days
- General sources: < 180 days

Usage:
    python check-freshness.py <wiki-file-or-directory>
    python check-freshness.py --all              # Scan all APV wiki files
    python check-freshness.py --check <url>      # Check single URL

Returns:
    0 if all URLs fresh, 1 if any stale URLs found
"""

import re
import sys
import urllib.request
from urllib.error import URLError, HTTPError
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
import json
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import time

# Freshness requirements in days
FRESHNESS_LIMITS = {
    'pricing': 30,       # Pricing sources: 30 days
    'compliance': 365,   # Compliance sources: 1 year
    'general': 180,      # General sources: 6 months
    'calculator': 30,    # Calculator pages: 30 days
}

# Keywords to detect URL type
URL_TYPE_KEYWORDS = {
    'pricing': ['price', 'pricing', 'calculator', 'cost', 'estimator'],
    'compliance': ['pci-dss', 'regulation', 'compliance', 'standard', 'guideline', 'mas', 'bnm', 'bsp', 'bi'],
    'calculator': ['calculator', 'estimator', 'pricing'],
}

# Special domains known to have dynamic content
DYNAMIC_CONTENT_DOMAINS = {
    'calculator.aws',
    'azure.microsoft.com/pricing',
    'cloud.google.com/products/calculator',
    'gcppricing.com',
}


class FreshnessChecker:
    """Checks freshness of source URLs in APV wiki content."""

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.results = {
            'fresh': [],
            'stale': [],
            'unknown': [],  # No date info available
            'warning': [],  # Fresh but approaching limit
        }
        self.checked_urls: Dict[str, dict] = {}
        self.warning_threshold = 0.8  # Warn at 80% of freshness limit

    def detect_url_type(self, url: str, context: str = '') -> str:
        """
        Detect the type of URL based on URL content and context.

        Returns: 'pricing', 'compliance', 'calculator', or 'general'
        """
        url_lower = url.lower()
        context_lower = context.lower()

        for url_type, keywords in URL_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in url_lower or keyword in context_lower:
                    return url_type

        # Check if it's a calculator domain
        for domain in DYNAMIC_CONTENT_DOMAINS:
            if domain in url_lower:
                return 'calculator'

        return 'general'

    def get_freshness_limit(self, url_type: str) -> int:
        """Get freshness limit in days for URL type."""
        return FRESHNESS_LIMITS.get(url_type, FRESHNESS_LIMITS['general'])

    def extract_urls_from_file(self, filepath: Path) -> List[Tuple[str, int, str]]:
        """Extract source URLs from a markdown file."""
        urls = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # Markdown link format
                md_links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', line)
                for text, url in md_links:
                    urls.append((url, i, f"link: {text}"))

                # Source list format
                source_lines = re.findall(r'(?:source|url):\s*["\']?(https?://[^\s"\']+)["\']?', line, re.IGNORECASE)
                for url in source_lines:
                    urls.append((url, i, "source reference"))

                # Standalone URLs
                standalone = re.findall(r'(?:^|\s)(https?://[^\s\)]+)', line)
                for url in standalone:
                    urls.append((url, i, "standalone URL"))

        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)

        return urls

    def get_last_modified(self, url: str, timeout: int = 10) -> Optional[datetime]:
        """
        Get last-modified date from URL HTTP headers.

        Returns: datetime object or None if not available
        """
        try:
            req = urllib.request.Request(
                url,
                method='HEAD',
                headers={
                    'User-Agent': 'Mozilla/5.0 (APV-FreshnessChecker/1.0)'
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                # Try Last-Modified header
                last_modified = response.headers.get('Last-Modified')
                if last_modified:
                    return parsedate_to_datetime(last_modified)

                # For pages without Last-Modified, we can't determine freshness
                return None

        except HTTPError as e:
            # Some servers return 405 for HEAD requests, try GET
            if e.code == 405:
                try:
                    req = urllib.request.Request(
                        url,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (APV-FreshnessChecker/1.0)'
                        }
                    )
                    with urllib.request.urlopen(req, timeout=timeout) as response:
                        last_modified = response.headers.get('Last-Modified')
                        if last_modified:
                            return parsedate_to_datetime(last_modified)
                except:
                    pass
            return None
        except (URLError, Exception):
            return None

    def check_url_freshness(self, url: str, filepath: Path, line: int, context: str) -> Dict:
        """Check freshness of a single URL."""
        url_type = self.detect_url_type(url, context)
        freshness_limit = self.get_freshness_limit(url_type)
        now = datetime.now()

        result = {
            'url': url,
            'file': str(filepath),
            'line': line,
            'context': context,
            'url_type': url_type,
            'freshness_limit_days': freshness_limit,
            'status': 'unknown',
            'days_old': None,
            'issues': [],
        }

        # Check cache first
        if url in self.checked_urls:
            cached = self.checked_urls[url]
            result.update(cached)
            return result

        # Get last-modified date
        time.sleep(0.3)  # Rate limiting
        last_modified = self.get_last_modified(url)

        if last_modified is None:
            result['status'] = 'unknown'
            result['issues'].append('No date information available')
            self.checked_urls[url] = result
            return result

        # Calculate age (ensure both datetimes are aware or naive)
        if last_modified.tzinfo is not None:
            # last_modified is timezone-aware, make now also aware
            now = datetime.now(timezone.utc)
        else:
            # Both are naive, use naive now
            now = datetime.now()
        age = now - last_modified
        days_old = age.total_seconds() / 86400
        result['days_old'] = round(days_old, 1)
        result['last_modified'] = last_modified.isoformat()

        # Check if within freshness limit
        if days_old > freshness_limit:
            result['status'] = 'stale'
            result['issues'].append(f'{days_old:.1f} days old (limit: {freshness_limit} days)')
        elif days_old > freshness_limit * self.warning_threshold:
            result['status'] = 'warning'
            result['issues'].append(f'{days_old:.1f} days old (approaching {freshness_limit} day limit)')
        else:
            result['status'] = 'fresh'

        self.checked_urls[url] = result
        return result

    def scan_file(self, filepath: Path) -> Dict:
        """Scan a single file for URLs and check freshness."""
        urls = self.extract_urls_from_file(filepath)

        if not urls:
            return {
                'file': str(filepath),
                'urls_found': 0,
                'results': []
            }

        results = []
        for url, line, context in urls:
            result = self.check_url_freshness(url, filepath, line, context)
            results.append(result)
            if result['status'] in self.results:
                self.results[result['status']].append(result)

        return {
            'file': str(filepath),
            'urls_found': len(urls),
            'results': results
        }

    def scan_directory(self, directory: Path, pattern: str = "*.md") -> Dict:
        """Scan all markdown files in directory."""
        files = list(directory.rglob(pattern))
        results = []

        for filepath in files:
            result = self.scan_file(filepath)
            results.append(result)

        return {
            'files_scanned': len(files),
            'total_urls': sum(r['urls_found'] for r in results),
            'file_results': results
        }

    def print_report(self):
        """Print freshness report."""
        total = sum(len(v) for v in self.results.values())
        stale = len(self.results['stale'])

        print("\n" + "="*60)
        print("APV SOURCE URL FRESHNESS REPORT")
        print("="*60)
        print(f"Total URLs checked: {total}")
        print()

        # Show stale URLs first
        if self.results['stale']:
            print("🚨 STALE URLs (require attention):")
            for item in self.results['stale']:
                print(f"  - {item['url']}")
                print(f"    Type: {item['url_type']} (limit: {item['freshness_limit_days']} days)")
                print(f"    Age: {item['days_old']} days")
                print(f"    File: {item['file']}:{item['line']}")
            print()

        # Show warnings
        if self.results['warning']:
            print("⚠️  WARNING (approaching freshness limit):")
            for item in self.results['warning']:
                print(f"  - {item['url']}")
                print(f"    Age: {item['days_old']} days (limit: {item['freshness_limit_days']} days)")
                print(f"    File: {item['file']}:{item['line']}")
            print()

        # Show fresh URLs (summary only)
        if self.results['fresh']:
            print(f"✅ FRESH URLs: {len(self.results['fresh'])}")
            print()

        # Show unknown (no date info)
        if self.results['unknown']:
            print(f"❓ UNKNOWN (no date info): {len(self.results['unknown'])}")
            print("   Consider manually verifying these URLs:")
            for item in self.results['unknown'][:5]:  # Show first 5
                print(f"     - {item['url']}")
            if len(self.results['unknown']) > 5:
                print(f"     ... and {len(self.results['unknown']) - 5} more")
            print()

        # Summary
        print("="*60)
        if stale == 0:
            print("✅ ALL CHECKED URLS ARE WITHIN FRESHNESS LIMITS")
            return 0
        else:
            print(f"❌ FOUND {stale} STALE URL(S)")
            return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: check-freshness.py <file|directory|--all|--check URL>")
        print("\nExamples:")
        print("  check-freshness.py wiki/apv/compliance/pci-dss-overview.md")
        print("  check-freshness.py wiki/apv/")
        print("  check-freshness.py --all")
        print("  check-freshness.py --check https://aws.amazon.com/pricing/")
        sys.exit(1)

    checker = FreshnessChecker(strict_mode=True)

    # Check single URL
    if sys.argv[1] == '--check' and len(sys.argv) >= 3:
        url = sys.argv[2]
        result = checker.check_url_freshness(url, Path('command-line'), 1, 'manual check')
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['status'] != 'stale' else 1)

    # Scan all APV wiki files
    if sys.argv[1] == '--all':
        base_dir = Path('/Users/stevenjiang/workspace/mykb/wiki/apv')
        checker.scan_directory(base_dir)
        checker.print_report()
        sys.exit(0)

    # Scan specific file or directory
    target = Path(sys.argv[1])

    if target.is_file():
        checker.scan_file(target)
    elif target.is_dir():
        checker.scan_directory(target)
    else:
        print(f"Error: {target} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    checker.print_report()


if __name__ == '__main__':
    main()
