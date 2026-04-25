#!/usr/bin/env python3
"""
APV Source URL Verification Script

Checks all APV knowledge files for source URL compliance:
- Verifies source URLs are present in frontmatter
- Checks if source URLs are accessible
- Validates URL format and SSL certificates
- Generates compliance report
- Flags files missing source URLs

Usage:
    python3 verify-source-urls.py [--path PATH] [--output FILE]
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
import ssl
import email.utils

# Configuration
DEFAULT_PATH = "wiki/apv/knowledge"
OUTPUT_DIR = "wiki/apv/knowledge/evidence/reports"

class SourceURLVerifier:
    def __init__(self, knowledge_path: str = DEFAULT_PATH):
        self.knowledge_path = Path(knowledge_path)
        self.results = {
            "scan_date": datetime.now(timezone.utc).isoformat(),
            "files_checked": 0,
            "urls_checked": 0,
            "valid_urls": 0,
            "invalid_urls": 0,
            "missing_urls": 0,
            "ssl_errors": 0,
            "files": [],
            "issues": []
        }

    def check_url(self, url: str) -> Dict[str, Any]:
        """Check if a URL is accessible and valid."""
        result = {
            "url": url,
            "accessible": False,
            "http_status": None,
            "ssl_valid": None,
            "error": None
        }

        try:
            # Create SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED

            # Make request with timeout
            req = urllib.request.Request(
                url,
                method='HEAD',
                headers={'User-Agent': 'APV-URL-Verifier/1.0'}
            )

            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                result["accessible"] = True
                result["http_status"] = response.status
                result["ssl_valid"] = True

        except urllib.error.HTTPError as e:
            result["http_status"] = e.code
            result["error"] = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            result["error"] = f"URL Error: {str(e)}"
        except ssl.SSLError as e:
            result["ssl_valid"] = False
            result["error"] = f"SSL Error: {str(e)}"
        except Exception as e:
            result["error"] = f"Error: {str(e)}"

        return result

    def extract_source_url_from_frontmatter(self, content: str) -> str:
        """Extract source_url from YAML frontmatter."""
        match = re.search(r'^source_url:\s*[\'"]?([^\'"]*)[\'"]?\s*$', content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def extract_all_frontmatter_fields(self, content: str) -> Dict[str, str]:
        """Extract all relevant frontmatter fields."""
        fields = {}

        # Extract common fields
        patterns = {
            'source_url': r'^source_url:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'source_document': r'^source_document:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'source_version': r'^source_version:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'captured_date': r'^captured_date:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'verified_by': r'^verified_by:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'last_verified': r'^last_verified:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
            'freshness_days': r'^freshness_days:\s*[\'"]?([^\'"]*)[\'"]?\s*$',
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                fields[field] = match.group(1).strip()

        return fields

    def verify_file(self, file_path: Path) -> Dict[str, Any]:
        """Verify a single knowledge file."""
        result = {
            "file": str(file_path.relative_to(self.knowledge_path.parent.parent)),
            "has_source_url": False,
            "url_check": None,
            "frontmatter": {}
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter fields
            result["frontmatter"] = self.extract_all_frontmatter_fields(content)

            # Check for source_url
            source_url = result["frontmatter"].get("source_url")
            if source_url:
                result["has_source_url"] = True
                result["url_check"] = self.check_url(source_url)
                self.results["urls_checked"] += 1

                if result["url_check"]["accessible"]:
                    self.results["valid_urls"] += 1
                else:
                    self.results["invalid_urls"] += 1
                    self.results["issues"].append({
                        "file": result["file"],
                        "issue": "invalid_url",
                        "url": source_url,
                        "error": result["url_check"]["error"]
                    })
            else:
                self.results["missing_urls"] += 1
                self.results["issues"].append({
                    "file": result["file"],
                    "issue": "missing_source_url"
                })

            self.results["files_checked"] += 1

        except Exception as e:
            self.results["issues"].append({
                "file": result["file"],
                "issue": "file_read_error",
                "error": str(e)
            })

        return result

    def scan_directory(self) -> None:
        """Scan all markdown files in the knowledge directory."""
        markdown_files = list(self.knowledge_path.rglob("*.md"))

        print(f"Scanning {len(markdown_files)} files...")

        for file_path in markdown_files:
            result = self.verify_file(file_path)
            self.results["files"].append(result)

        # Calculate compliance percentage
        if self.results["urls_checked"] > 0:
            compliance_rate = (self.results["valid_urls"] / self.results["urls_checked"]) * 100
            self.results["compliance_percentage"] = round(compliance_rate, 2)
        else:
            self.results["compliance_percentage"] = 0

    def generate_report(self) -> Dict[str, Any]:
        """Generate compliance report."""
        return {
            "report_date": self.results["scan_date"],
            "report_version": "1.0",
            "verified_by": "Source URL Verification Script",
            "summary": {
                "total_files_checked": self.results["files_checked"],
                "total_urls_checked": self.results["urls_checked"],
                "valid_urls": self.results["valid_urls"],
                "invalid_urls": self.results["invalid_urls"],
                "missing_urls": self.results["missing_urls"],
                "ssl_errors": self.results["ssl_errors"],
                "compliance_percentage": self.results["compliance_percentage"]
            },
            "files": self.results["files"],
            "issues": self.results["issues"],
            "recommendations": self.generate_recommendations()
        }

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on issues found."""
        recommendations = []

        if self.results["missing_urls"] > 0:
            recommendations.append(f"Add source URLs to {self.results['missing_urls']} files")

        if self.results["invalid_urls"] > 0:
            recommendations.append(f"Fix {self.results['invalid_urls']} broken source URLs")

        if self.results["compliance_percentage"] < 100:
            recommendations.append(f"Achieve 100% source URL compliance (currently {self.results['compliance_percentage']}%)")

        if not recommendations:
            recommendations.append("All files compliant with source URL requirements")

        return recommendations

    def print_summary(self) -> None:
        """Print verification summary."""
        print("\n" + "="*60)
        print("APV SOURCE URL VERIFICATION REPORT")
        print("="*60)
        print(f"Scan Date: {self.results['scan_date']}")
        print(f"Files Checked: {self.results['files_checked']}")
        print(f"URLs Checked: {self.results['urls_checked']}")
        print(f"\nResults:")
        print(f"  ✅ Valid URLs: {self.results['valid_urls']}")
        print(f"  ❌ Invalid URLs: {self.results['invalid_urls']}")
        print(f"  ⚠️  Missing URLs: {self.results['missing_urls']}")
        print(f"\nCompliance: {self.results['compliance_percentage']}%")
        print("="*60)

        if self.results["issues"]:
            print(f"\n⚠️  Issues Found: {len(self.results['issues'])}")
            print("\nRecommendations:")
            for i, rec in enumerate(self.generate_recommendations(), 1):
                print(f"  {i}. {rec}")
        else:
            print("\n✅ All files compliant!")

    def save_report(self, output_file: str = None) -> str:
        """Save compliance report to JSON file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = f"{OUTPUT_DIR}/url-compliance-{timestamp}.json"

        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        report = self.generate_report()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Report saved to: {output_file}")
        return output_file


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Verify source URLs in APV knowledge files")
    parser.add_argument("--path", default=DEFAULT_PATH, help="Path to APV knowledge directory")
    parser.add_argument("--output", help="Output JSON file for compliance report")

    args = parser.parse_args()

    verifier = SourceURLVerifier(args.path)
    verifier.scan_directory()
    verifier.print_summary()

    if args.output:
        verifier.save_report(args.output)
    else:
        # Auto-generate output filename
        verifier.save_report()


if __name__ == "__main__":
    main()
