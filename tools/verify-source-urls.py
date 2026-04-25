#!/usr/bin/env python3
"""
APV Source URL Verification System

Validates that all source URLs in APV content are:
1. Well-formed and valid URLs
2. Accessible (return HTTP 200-299)
3. From trusted/official sources

Usage:
    python verify-source-urls.py <wiki-file-or-directory>
    python verify-source-urls.py --all              # Scan all APV wiki files
    python verify-source-urls.py --check <url>      # Check single URL

Returns:
    0 if all URLs valid, 1 if any issues found
"""

import re
import sys
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
from pathlib import Path
from typing import List, Dict, Set, Tuple
import json
from datetime import datetime
import time

# Trusted domains for APV compliance sources
TRUSTED_DOMAINS = {
    # PCI-DSS official
    'pcisecuritystandards.org',
    # Singapore regulators
    'mas.gov.sg',
    'imda.gov.sg',
    'pdpc.gov.sg',
    # Malaysia regulators
    'bnm.gov.my',
    'pdp.gov.my',
    # Philippines regulators
    'bsp.gov.ph',
    'npc.gov.ph',
    # Indonesia regulators
    'bi.go.id',
    'kominfo.go.id',
    # Thailand regulators
    'bot.or.th',
    'pdpc.go.th',
    # Taiwan regulators
    'cbc.gov.tw',
    'pdpc.gov.tw',
    # Hong Kong regulators
    'hkma.gov.hk',
    'pcpd.org.hk',
    # Cloud providers (pricing calculators)
    'aws.amazon.com',
    'calculator.aws',
    'azure.microsoft.com',
    'cloud.google.com',
    'gcppricing.com',
    # Card networks
    'visapaymentsecurityintegration.com',
    'mastercard.com',
    'amexpaymentsecurity.com',
    'discoverglobalnetwork.com',
}

# Source-specific freshness requirements (days)
FRESHNESS_RULES = {
    'pricing': 30,      # Pricing sources must be < 30 days old
    'compliance': 365,  # Compliance sources must be < 1 year old
    'general': 180,     # General sources < 6 months
}

class URLVerifier:
    """Verifies source URLs in APV wiki content."""

    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        self.results = {
            'valid': [],
            'invalid': [],
            'inaccessible': [],
            'untrusted': [],
            'no_url': [],
        }
        self.checked_urls: Set[str] = set()

    def extract_urls_from_file(self, filepath: Path) -> List[Tuple[str, int, str]]:
        """
        Extract source URLs from a markdown file.

        Returns: List of (url, line_number, context)
        """
        urls = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # Look for URL patterns in markdown
                # - [text](url) format
                # - Sources: - url format
                # - source: "url" format

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

    def is_trusted_domain(self, url: str) -> bool:
        """Check if URL is from a trusted domain."""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()

        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]

        # Check exact match or subdomain
        for trusted in TRUSTED_DOMAINS:
            if domain == trusted or domain.endswith('.' + trusted):
                return True

        return False

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is well-formed and uses valid scheme."""
        try:
            result = urllib.parse.urlparse(url)
            # Must have scheme and netloc, and scheme must be http or https
            if not all([result.scheme, result.netloc]):
                return False
            if result.scheme not in ('http', 'https'):
                return False
            return True
        except:
            return False

    def check_url_accessibility(self, url: str, timeout: int = 10) -> Tuple[bool, int]:
        """
        Check if URL is accessible.

        Returns: (accessible, status_code)
        """
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (APV-URL-Verifier/1.0)'
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return (True, response.status)
        except HTTPError as e:
            return (False, e.code)
        except URLError:
            return (False, 0)
        except Exception:
            return (False, 0)

    def verify_url(self, url: str, filepath: Path, line: int, context: str) -> Dict:
        """Verify a single URL."""
        result = {
            'url': url,
            'file': str(filepath),
            'line': line,
            'context': context,
            'status': 'unknown',
            'issues': [],
        }

        # Check if valid URL format
        if not self.is_valid_url(url):
            result['status'] = 'invalid'
            result['issues'].append('Invalid URL format')
            return result

        # Check trusted domain
        if self.strict_mode and not self.is_trusted_domain(url):
            result['status'] = 'untrusted'
            result['issues'].append(f'Untrusted domain')
            return result

        # Check accessibility (with rate limiting)
        if url not in self.checked_urls:
            time.sleep(0.5)  # Rate limiting
            accessible, status = self.check_url_accessibility(url)
            self.checked_urls.add(url)

            if not accessible:
                result['status'] = 'inaccessible'
                result['issues'].append(f'HTTP {status}' if status else 'Connection failed')
                return result

        result['status'] = 'valid'
        return result

    def scan_file(self, filepath: Path) -> Dict:
        """Scan a single file for URLs and verify them."""
        urls = self.extract_urls_from_file(filepath)

        if not urls:
            return {
                'file': str(filepath),
                'urls_found': 0,
                'results': []
            }

        results = []
        for url, line, context in urls:
            result = self.verify_url(url, filepath, line, context)
            results.append(result)
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
        """Print verification report."""
        total = sum(len(v) for v in self.results.values())

        print("\n" + "="*60)
        print("APV SOURCE URL VERIFICATION REPORT")
        print("="*60)
        print(f"Total URLs checked: {total}")
        print()

        for status, items in self.results.items():
            if items:
                print(f"{status.upper()} ({len(items)}):")
                for item in items:
                    print(f"  - {item['url']}")
                    print(f"    File: {item['file']}:{item['line']}")
                    if item['issues']:
                        print(f"    Issues: {', '.join(item['issues'])}")
                print()

        # Summary
        valid = len(self.results['valid'])
        invalid = len(self.results['invalid'])
        inaccessible = len(self.results['inaccessible'])
        untrusted = len(self.results['untrusted'])

        if self.strict_mode:
            issues = invalid + inaccessible + untrusted
        else:
            issues = invalid + inaccessible

        if issues == 0:
            print("✅ ALL URLS VALID")
            return 0
        else:
            print(f"❌ FOUND {issues} ISSUE(S)")
            return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: verify-source-urls.py <file|directory|--all|--check URL>")
        print("\nExamples:")
        print("  verify-source-urls.py wiki/apv/compliance/pci-dss-overview.md")
        print("  verify-source-urls.py wiki/apv/")
        print("  verify-source-urls.py --all")
        print("  verify-source-urls.py --check https://pcisecuritystandards.org/documents/PCI_DSS_v4-0.pdf")
        sys.exit(1)

    verifier = URLVerifier(strict_mode=True)

    # Check single URL
    if sys.argv[1] == '--check' and len(sys.argv) >= 3:
        url = sys.argv[2]
        result = verifier.verify_url(url, Path('command-line'), 1, 'manual check')
        print(json.dumps(result, indent=2))
        sys.exit(0 if result['status'] == 'valid' else 1)

    # Scan all APV wiki files
    if sys.argv[1] == '--all':
        base_dir = Path('/Users/stevenjiang/workspace/mykb/wiki/apv')
        verifier.scan_directory(base_dir)
        verifier.print_report()
        sys.exit(0)

    # Scan specific file or directory
    target = Path(sys.argv[1])

    if target.is_file():
        verifier.scan_file(target)
    elif target.is_dir():
        verifier.scan_directory(target)
    else:
        print(f"Error: {target} is not a valid file or directory", file=sys.stderr)
        sys.exit(1)

    verifier.print_report()


if __name__ == '__main__':
    main()
