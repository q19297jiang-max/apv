#!/usr/bin/env python3
"""Extract and validate URLs from knowledge/stage markdown files."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from lib.frontmatter import parse_file

# Patterns for URLs in body text
_MD_LINK_RE = re.compile(r'\[(?:[^\]]*)\]\((https?://[^\s\)]+)\)')
_BARE_URL_RE = re.compile(r'(?<!\()(https?://[^\s\)\]>]+)')


def extract_urls_from_file(file_path: Path) -> list[dict]:
    """Parse frontmatter source_url and find URLs in body text."""
    file_path = Path(file_path)
    fm, body = parse_file(file_path)
    results = []

    if fm.get("source_url"):
        results.append({"url": str(fm["source_url"]), "source_file": str(file_path), "location": "frontmatter"})

    # Find all URLs in body (markdown links + bare URLs), deduplicated
    seen = set()
    for url in _MD_LINK_RE.findall(body):
        if url not in seen:
            seen.add(url)
            results.append({"url": url, "source_file": str(file_path), "location": "body"})
    for url in _BARE_URL_RE.findall(body):
        if url not in seen:
            seen.add(url)
            results.append({"url": url, "source_file": str(file_path), "location": "body"})

    return results


def validate_url_format(url: str) -> dict:
    """Check URL is well-formed (has scheme and host)."""
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return {"url": url, "valid": True, "issue": None}
    issues = []
    if parsed.scheme not in ("http", "https"):
        issues.append(f"bad scheme: {parsed.scheme!r}")
    if not parsed.netloc:
        issues.append("missing host")
    return {"url": url, "valid": False, "issue": "; ".join(issues)}


def validate_directory(directory: Path) -> dict:
    """Scan all .md files, extract URLs, validate format."""
    directory = Path(directory)
    all_urls = []
    files = sorted(directory.rglob("*.md"))
    for f in files:
        all_urls.extend(extract_urls_from_file(f))

    results = []
    valid = invalid = 0
    for entry in all_urls:
        v = validate_url_format(entry["url"])
        v["source_file"] = entry["source_file"]
        v["location"] = entry["location"]
        results.append(v)
        if v["valid"]:
            valid += 1
        else:
            invalid += 1

    return {
        "total_files": len(files),
        "total_urls": len(all_urls),
        "valid": valid,
        "invalid": invalid,
        "results": results,
    }


def generate_validation_report(directory: Path, output_path: Path) -> dict:
    """Write JSON report to output_path."""
    report = validate_directory(directory)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Validate URLs in markdown files")
    parser.add_argument("--dir", required=True, help="Directory to scan")
    parser.add_argument("--report-path", default="verification/source-url-validation.json")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()

    report = generate_validation_report(Path(args.dir), Path(args.report_path))

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Files: {report['total_files']}, URLs: {report['total_urls']}, Valid: {report['valid']}, Invalid: {report['invalid']}")
        for r in report["results"]:
            if not r["valid"]:
                print(f"  INVALID: {r['url']} ({r['issue']}) in {r['source_file']}")

    sys.exit(0 if report["invalid"] == 0 else 1)


if __name__ == "__main__":
    main()
