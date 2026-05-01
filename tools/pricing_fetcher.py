#!/usr/bin/env python3
"""Pricing freshness checker for APV V2.

Reads pricing knowledge files, checks freshness, and generates refresh plans.
Does NOT fetch from APIs — manual calculator verification is required.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from lib.frontmatter import parse_file

CALCULATOR_URLS = {
    "aws": "https://calculator.aws/",
    "azure": "https://azure.microsoft.com/pricing/calculator/",
    "gcp": "https://cloud.google.com/products/calculator",
}


def check_pricing_freshness(knowledge_dir: Path) -> list[dict]:
    """Scan knowledge/pricing/*.md and return freshness status for each."""
    pricing_dir = Path(knowledge_dir) / "pricing"
    if not pricing_dir.exists():
        return []

    results = []
    for f in sorted(pricing_dir.glob("*.md")):
        fm, _ = parse_file(f)
        last_verified = fm.get("last_verified")
        freshness_days = fm.get("freshness_days")
        if last_verified is None or freshness_days is None:
            continue

        if isinstance(last_verified, str):
            verified_date = date.fromisoformat(last_verified)
        else:
            verified_date = last_verified

        days_since = (date.today() - verified_date).days
        fd = int(freshness_days)

        if days_since > fd * 2:
            status = "expired"
        elif days_since > fd:
            status = "stale"
        else:
            status = "fresh"

        provider = f.stem
        results.append({
            "path": str(f),
            "provider": provider,
            "last_verified": str(verified_date),
            "freshness_days": fd,
            "days_since": days_since,
            "status": status,
        })

    return results


def generate_refresh_plan(stale_files: list[dict]) -> str:
    """Generate markdown refresh instructions for stale/expired files."""
    if not stale_files:
        return "All pricing files are fresh. No action needed."

    lines = ["# Pricing Refresh Plan\n"]
    for entry in stale_files:
        provider = entry["provider"]
        status_label = entry["status"].upper()
        url = CALCULATOR_URLS.get(provider, "N/A")
        lines.append(f"## {provider}.md — {status_label}")
        lines.append(f"- **Last verified**: {entry['last_verified']}")
        lines.append(f"- **Days since**: {entry['days_since']} (threshold: {entry['freshness_days']})")
        lines.append(f"- **Calculator**: {url}")
        lines.append("")
        lines.append("**Steps**:")
        lines.append(f"1. Verify pricing in calculator: {url}")
        lines.append("2. Update component catalog (`aws-component-catalog.md` or equivalent)")
        lines.append("3. Run `python3 pricing-fetcher-generic.py --provider " + provider + "`")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check pricing freshness")
    parser.add_argument("--knowledge-dir", required=True, help="Path to knowledge/ directory")
    parser.add_argument("--json", action="store_true", dest="output_json", help="Output JSON")
    args = parser.parse_args()

    results = check_pricing_freshness(Path(args.knowledge_dir))
    needs_update = [r for r in results if r["status"] != "fresh"]

    if args.output_json:
        print(json.dumps(results, indent=2))
    else:
        if needs_update:
            print(generate_refresh_plan(needs_update))
        else:
            print("All pricing files are fresh.")

    sys.exit(1 if needs_update else 0)


if __name__ == "__main__":
    main()
