#!/usr/bin/env python3
"""
APV Freshness Checker

Checks if source URLs in APV knowledge files are within freshness thresholds:
- Compliance pages: 12 months (365 days)
- Pricing pages: 30 days
- Architecture pages: 12 months (365 days)

Usage:
    python3 check-freshness.py [--path PATH] [--compliance-days DAYS] [--pricing-days DAYS]
"""

import os
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List

# Default freshness thresholds
COMPLIANCE_FRESHNESS_DAYS = 365
PRICING_FRESHNESS_DAYS = 30
ARCHITECTURE_FRESHNESS_DAYS = 365

class FreshnessChecker:
    def __init__(self, knowledge_path: str, compliance_days: int = COMPLIANCE_FRESHNESS_DAYS,
                 pricing_days: int = PRICING_FRESHNESS_DAYS):
        self.knowledge_path = Path(knowledge_path)
        self.compliance_days = compliance_days
        self.pricing_days = pricing_days
        self.architecture_days = compliance_days  # Same as compliance

        self.results = {
            "check_date": datetime.now(timezone.utc).isoformat(),
            "compliance_threshold_days": compliance_days,
            "pricing_threshold_days": pricing_days,
            "files_checked": 0,
            "fresh": 0,
            "stale": 0,
            "unknown": 0,
            "files": []
        }

    def extract_field(self, content: str, field: str) -> str:
        """Extract a field from YAML frontmatter."""
        match = re.search(rf'^{field}:\s*[\'"]?([^\'"]*)[\'"]?\s*$', content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def check_freshness(self, file_path: Path) -> Dict[str, Any]:
        """Check if a knowledge file is within freshness threshold."""
        result = {
            "file": str(file_path.relative_to(self.knowledge_path.parent.parent)),
            "category": self.determine_category(file_path),
            "threshold_days": None,
            "last_verified": None,
            "status": None,
            "days_since_verification": None
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Get category and threshold
            category = result["category"]
            if category == "compliance":
                result["threshold_days"] = self.compliance_days
            elif category == "pricing":
                result["threshold_days"] = self.pricing_days
            elif category == "architecture":
                result["threshold_days"] = self.architecture_days

            # Extract last_verified date
            last_verified_str = self.extract_field(content, "last_verified")
            if last_verified_str:
                try:
                    # Parse date (accepts multiple formats)
                    for fmt in ["%Y-%m-%d", "%Y-%m-%d", "%Y-%m-%d"]:
                        try:
                            last_verified = datetime.strptime(last_verified_str, fmt).replace(tzinfo=timezone.utc)
                            result["last_verified"] = last_verified.isoformat()
                            break
                        except ValueError:
                            continue

                    if result["last_verified"]:
                        # Calculate days since verification
                        days_old = (datetime.now(timezone.utc) - last_verified).days
                        result["days_since_verification"] = days_old

                        # Check if within threshold
                        if days_old <= result["threshold_days"]:
                            result["status"] = "fresh"
                            self.results["fresh"] += 1
                        else:
                            result["status"] = "stale"
                            self.results["stale"] += 1
                            self.results["issues"].append({
                                "file": result["file"],
                                "issue": "stale_source_url",
                                "threshold": result["threshold_days"],
                                "days_old": days_old
                            })
                except Exception as e:
                    result["status"] = "unknown"
                    result["error"] = str(e)
                    self.results["unknown"] += 1
            else:
                result["status"] = "unknown"
                result["error"] = "No last_verified date found"

            self.results["files_checked"] += 1

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.results["unknown"] += 1

        return result

    def determine_category(self, file_path: Path) -> str:
        """Determine the category of a knowledge file based on its path."""
        path_str = str(file_path)

        # Pricing files
        if "/pricing/" in path_str:
            return "pricing"

        # Compliance files
        if "/compliance/" in path_str:
            return "compliance"

        # Infrastructure files (architecture)
        if "/infrastructure/" in path_str:
            return "architecture"

        # Default to compliance (most files)
        return "compliance"

    def check_directory(self) -> None:
        """Check freshness of all files in knowledge directory."""
        markdown_files = list(self.knowledge_path.rglob("*.md"))

        print(f"Checking freshness of {len(markdown_files)} files...")
        print(f"Thresholds: Compliance={self.compliance_days} days, Pricing={self.pricing_days} days")

        for file_path in markdown_files:
            result = self.check_freshness(file_path)
            self.results["files"].append(result)

    def print_summary(self) -> None:
        """Print freshness summary."""
        print("\n" + "="*60)
        print("APV SOURCE URL FRESHNESS CHECK")
        print("="*60)
        print(f"Check Date: {self.results['check_date']}")
        print(f"Files Checked: {self.results['files_checked']}")
        print(f"\nFreshness Thresholds:")
        print(f"  Compliance/Architecture: {self.compliance_days} days")
        print(f"  Pricing: {self.pricing_days} days")
        print(f"\nResults:")
        print(f"  ✅ Fresh: {self.results['fresh']}")
        print(f"  ⚠️  Stale: {self.results['stale']}")
        print(f"  ❓ Unknown: {self.results['unknown']}")
        print("="*60)

        # Show stale files if any
        stale_files = [f for f in self.results["files"] if f["status"] == "stale"]
        if stale_files:
            print(f"\n⚠️  Stale Files ({len(stale_files)}):")
            for file in stale_files[:10]:  # Show first 10
                print(f"  - {file['file']} ({file['days_since_verification']} days old, threshold: {file['threshold_days']} days)")
            if len(stale_files) > 10:
                print(f"  ... and {len(stale_files) - 10} more")

        if self.results["stale"] > 0:
            print(f"\n🔄 Action Required: Re-verify {self.results['stale']} files")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Check freshness of source URLs in APV knowledge files")
    parser.add_argument("--path", default="wiki/apv/knowledge", help="Path to APV knowledge directory")
    parser.add_argument("--compliance-days", type=int, default=COMPLIANCE_FRESHNESS_DAYS,
                        help="Freshness threshold for compliance pages (default: 365)")
    parser.add_argument("--pricing-days", type=int, default=PRICING_FRESHNESS_DAYS,
                        help="Freshness threshold for pricing pages (default: 30)")

    args = parser.parse_args()

    checker = FreshnessChecker(args.path, args.compliance_days, args.pricing_days)
    checker.check_directory()
    checker.print_summary()


if __name__ == "__main__":
    main()
