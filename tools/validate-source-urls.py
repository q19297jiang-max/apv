#!/usr/bin/env python3
"""
Source URL Validator for APV Accuracy Assurance

Validates that source URLs in wiki pages and RFP responses are:
1. Present and not empty
2. Properly formatted
3. From official/primary sources
4. Accessible (HTTP check)

Usage:
    python3 validate-source-urls.py --file <markdown-file>
    python3 validate-source-urls.py --directory <wiki-directory>
    python3 validate-source-urls.py --project <project-path>
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import urllib.request
import urllib.error
from urllib.parse import urlparse


# Official/Primary source domains
OFFICIAL_DOMAINS = {
    # Compliance Standards
    'pcisecuritystandards.org',
    'pcissc.com',
    # Financial Regulators (APAC)
    'mas.gov.sg',
    'bnm.gov.my',
    'bsp.gov.ph',
    'bi.go.id',
    'bot.or.th',
    'fsc.gov.tw',
    'hkma.gov.hk',
    'bb.org.bd',  # Bangladesh Bank
    # Standards Organizations
    'iso.org',
    'nist.gov',
    # Card Networks
    'visa.com',
    'visaeurope.com',
    'mastercard.com',
    'amex.com',
    'discover.com',
    # Cloud Providers
    'aws.amazon.com',
    'calculator.aws',
    'azure.microsoft.com',
    'cloud.google.com',
    'gcp.google.com',
    # Official documentation
    'docs.aws.amazon.com',
    'learn.microsoft.com',
    'cloud.google.com/docs',
}

# Internal pricing sources (valid for SaaS/internal pricing)
INTERNAL_PRICING_PATTERNS = [
    'Internal',
    'SaaS',
    'Rate Sheet',
    'pricing',
    'v2.3',
    'v3.0',
]

# Secondary/unauthorized sources (forbidden)
FORBIDDEN_DOMAINS = {
    'wikipedia.org',
    'blogspot.com',
    'medium.com',
    'dev.to',
    'github.io',
    'stackexchange.com',
    'stackoverflow.com',
}


class ValidationResult:
    """Result of URL validation."""
    def __init__(self):
        self.valid = []
        self.missing = []
        self.invalid_format = []
        self.forbidden = []
        self.unofficial = []
        self.inaccessible = []

    def total_issues(self) -> int:
        return (len(self.missing) + len(self.invalid_format) +
                len(self.forbidden) + len(self.unofficial) +
                len(self.inaccessible))

    def is_compliant(self) -> bool:
        """Check if all validations passed."""
        return self.total_issues() == 0


def extract_urls_from_frontmatter(content: str) -> List[str]:
    """Extract source_url from YAML frontmatter."""
    urls = []
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # Find source_url field
        url_match = re.search(r'source_url:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
        if url_match:
            urls.append(url_match.group(1).strip())
        # Find additional source URLs
        for field in ['calculator_url', 'pricing_url', 'api_url']:
            url_match = re.search(rf'{field}:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
            if url_match:
                urls.append(url_match.group(1).strip())
    return urls


def extract_urls_from_content(content: str) -> List[Tuple[str, int]]:
    """Extract URLs from markdown content with line numbers."""
    urls = []
    # Markdown links: [text](url)
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
        url = match.group(2)
        if url.startswith('#'):
            continue
        line_num = content[:match.start()].count('\n') + 1
        urls.append((url, line_num))
    # Plain URLs
    for match in re.finditer(r'https?://[^\s\)]+', content):
        url = match.group(0)
        line_num = content[:match.start()].count('\n') + 1
        urls.append((url, line_num))
    return urls


def is_official_domain(url: str) -> bool:
    """Check if URL is from an official domain."""
    # First check if it's an internal pricing source (valid)
    if is_internal_pricing_source(url):
        return True

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    # Remove www. prefix
    domain = domain.replace('www.', '')

    # Check against official list
    for official in OFFICIAL_DOMAINS:
        if domain == official or domain.endswith('.' + official):
            return True
    return False


def is_internal_pricing_source(url: str) -> bool:
    """Check if URL/Text is an internal pricing source (valid for SaaS/internal pricing)."""
    if not url.startswith('http'):
        # Check if it matches internal pricing patterns
        for pattern in INTERNAL_PRICING_PATTERNS:
            if pattern.lower() in url.lower():
                return True
    return False


def is_forbidden_domain(url: str) -> bool:
    """Check if URL is from a forbidden domain."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    domain = domain.replace('www.', '')

    for forbidden in FORBIDDEN_DOMAINS:
        if domain == forbidden or domain.endswith('.' + forbidden):
            return True
    return False


def is_valid_url_format(url: str) -> bool:
    """Check if URL has valid format."""
    # Internal pricing sources are valid (even without HTTP)
    if is_internal_pricing_source(url):
        return True

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def check_url_accessible(url: str, timeout: int = 10) -> bool:
    """Check if URL is accessible via HTTP."""
    def perform_request(method: str) -> bool:
        req = urllib.request.Request(url, method=method)
        req.add_header('User-Agent', 'APV-Source-Validator/1.0')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status < 400

    try:
        return perform_request('HEAD')
    except urllib.error.HTTPError as error:
        if error.code in {403, 405, 501}:
            try:
                return perform_request('GET')
            except (urllib.error.URLError, urllib.error.HTTPError, Exception):
                return False
        return False
    except (urllib.error.URLError, Exception):
        try:
            return perform_request('GET')
        except (urllib.error.URLError, urllib.error.HTTPError, Exception):
            return False


def validate_markdown_file(file_path: Path) -> ValidationResult:
    """Validate a single markdown file."""
    result = ValidationResult()

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return result

    # Check frontmatter for source_url
    frontmatter_urls = extract_urls_from_frontmatter(content)
    if not frontmatter_urls:
        result.missing.append((str(file_path), "frontmatter", "source_url missing"))
    else:
        for url in frontmatter_urls:
            # Check if it's an internal pricing source first (valid)
            if is_internal_pricing_source(url):
                result.valid.append((str(file_path), "frontmatter", url))
            elif not is_valid_url_format(url):
                result.invalid_format.append((str(file_path), "frontmatter", url))
            elif is_forbidden_domain(url):
                result.forbidden.append((str(file_path), "frontmatter", url))
            elif not is_official_domain(url):
                result.unofficial.append((str(file_path), "frontmatter", url))
            elif check_url_accessible(url):
                result.valid.append((str(file_path), "frontmatter", url))
            else:
                result.inaccessible.append((str(file_path), "frontmatter", url))

    # Check content for URLs
    content_urls = extract_urls_from_content(content)
    for url, line_num in content_urls:
        # Skip already checked frontmatter URLs
        if url in frontmatter_urls:
            continue

        # Check if it's an internal pricing source (valid)
        if is_internal_pricing_source(url):
            continue  # Internal pricing is valid, skip further checks

        if not is_valid_url_format(url):
            result.invalid_format.append((str(file_path), f"line {line_num}", url))
        elif is_forbidden_domain(url):
            result.forbidden.append((str(file_path), f"line {line_num}", url))
        elif not is_official_domain(url):
            result.unofficial.append((str(file_path), f"line {line_num}", url))

    return result


def validate_project(project_path: Path) -> ValidationResult:
    """Validate all markdown files in a project."""
    result = ValidationResult()

    # Check RFP response
    response_file = project_path / "outputs" / "06-response.md"
    if response_file.exists():
        file_result = validate_markdown_file(response_file)
        merge_results(result, file_result)

    # Check pricing output
    pricing_file = project_path / "outputs" / "05-pricing.md"
    if pricing_file.exists():
        file_result = validate_markdown_file(pricing_file)
        merge_results(result, file_result)

    # Check compliance output
    compliance_file = project_path / "outputs" / "02-compliance.md"
    if compliance_file.exists():
        file_result = validate_markdown_file(compliance_file)
        merge_results(result, file_result)

    return result


def validate_directory(directory: Path) -> ValidationResult:
    """Validate all markdown files in a directory."""
    result = ValidationResult()

    for md_file in directory.rglob("*.md"):
        file_result = validate_markdown_file(md_file)
        merge_results(result, file_result)

    return result


def merge_results(target: ValidationResult, source: ValidationResult):
    """Merge validation results."""
    target.valid.extend(source.valid)
    target.missing.extend(source.missing)
    target.invalid_format.extend(source.invalid_format)
    target.forbidden.extend(source.forbidden)
    target.unofficial.extend(source.unofficial)
    target.inaccessible.extend(source.inaccessible)


def print_results(result: ValidationResult, verbose: bool = False):
    """Print validation results."""
    print("\n" + "=" * 60)
    print("SOURCE URL VALIDATION RESULTS")
    print("=" * 60)

    # Summary
    total_urls = len(result.valid)
    total_issues = result.total_issues()

    print(f"\nValid URLs: {len(result.valid)}")
    print(f"Missing source_url: {len(result.missing)}")
    print(f"Invalid format: {len(result.invalid_format)}")
    print(f"Forbidden sources: {len(result.forbidden)}")
    print(f"Unofficial sources: {len(result.unofficial)}")
    print(f"Inaccessible URLs: {len(result.inaccessible)}")

    print(f"\nTotal Issues: {total_issues}")

    if result.is_compliant():
        print("\n✅ VALIDATION PASSED - All source URLs compliant")
        return 0
    else:
        print("\n❌ VALIDATION FAILED - Issues found")

        if verbose or True:  # Always show details
            if result.missing:
                print("\n📋 Missing source_url:")
                for file, location, detail in result.missing[:10]:
                    print(f"  - {file} ({location}): {detail}")

            if result.invalid_format:
                print("\n🔧 Invalid URL format:")
                for file, location, url in result.invalid_format[:10]:
                    print(f"  - {file} ({location}): {url}")

            if result.forbidden:
                print("\n🚫 Forbidden sources (blogs, wikipedia, etc):")
                for file, location, url in result.forbidden[:10]:
                    print(f"  - {file} ({location}): {url}")

            if result.unofficial:
                print("\n⚠️  Unofficial sources (not from primary domains):")
                for file, location, url in result.unofficial[:10]:
                    print(f"  - {file} ({location}): {url}")

            if result.inaccessible:
                print("\n❓ Inaccessible URLs:")
                for file, location, url in result.inaccessible[:10]:
                    print(f"  - {file} ({location}): {url}")

        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Validate source URLs in APV content'
    )
    parser.add_argument('--file', type=Path, help='Validate single markdown file')
    parser.add_argument('--directory', type=Path, help='Validate directory of markdown files')
    parser.add_argument('--project', type=Path, help='Validate APV project outputs')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--output', '-o', type=Path, help='Output results to JSON file')

    args = parser.parse_args()

    result = ValidationResult()

    if args.file:
        result = validate_markdown_file(args.file)
    elif args.directory:
        result = validate_directory(args.directory)
    elif args.project:
        result = validate_project(args.project)
    else:
        parser.print_help()
        return 1

    # Print results
    exit_code = print_results(result, args.verbose)

    # Save to JSON if requested
    if args.output:
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'valid': result.valid,
            'missing': result.missing,
            'invalid_format': result.invalid_format,
            'forbidden': result.forbidden,
            'unofficial': result.unofficial,
            'inaccessible': result.inaccessible,
            'total_issues': result.total_issues(),
            'compliant': result.is_compliant()
        }
        args.output.write_text(json.dumps(output_data, indent=2))

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
