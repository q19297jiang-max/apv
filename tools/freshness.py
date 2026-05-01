"""Check knowledge freshness against configured thresholds.

Used by rfp-pricer and apv-reviewer skills.
Can generate verification/freshness-report.json.
"""

import argparse
import json
import math
import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.db import create_schema  # noqa: E402


def _query_all(db_path: Path) -> tuple[list[dict], int]:
    """Return (stale_pages_with_detail, total_count)."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    total = conn.execute("SELECT COUNT(*) FROM knowledge_pages").fetchone()[0]

    rows = conn.execute("SELECT * FROM stale_knowledge").fetchall()
    today = date.today()
    stale_pages = []
    for r in rows:
        last = date.fromisoformat(r["last_verified"])
        stale_pages.append({
            "path": r["path"],
            "domain": r["domain"],
            "days_since": (today - last).days,
            "threshold": r["freshness_days"],
        })
    conn.close()
    return stale_pages, total


def check_freshness(db_path: Path) -> dict:
    """Query stale_knowledge view, return freshness stats."""
    stale_pages, total = _query_all(db_path)
    return {
        "total_pages": total,
        "fresh": total - len(stale_pages),
        "stale": len(stale_pages),
        "stale_pages": stale_pages,
    }


def check_domain_freshness(db_path: Path, domain: str) -> dict:
    """Check freshness filtered to one domain."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    total = conn.execute(
        "SELECT COUNT(*) FROM knowledge_pages WHERE domain = ?", (domain,)
    ).fetchone()[0]

    rows = conn.execute(
        "SELECT * FROM stale_knowledge WHERE domain = ?", (domain,)
    ).fetchall()

    today = date.today()
    stale_pages = [
        {
            "path": r["path"],
            "domain": r["domain"],
            "days_since": (today - date.fromisoformat(r["last_verified"])).days,
            "threshold": r["freshness_days"],
        }
        for r in rows
    ]
    conn.close()

    return {
        "total_pages": total,
        "fresh": total - len(stale_pages),
        "stale": len(stale_pages),
        "stale_pages": stale_pages,
    }


def generate_freshness_report(db_path: Path, output_path: Path) -> dict:
    """Write JSON freshness report and return stats."""
    result = check_freshness(db_path)
    result["generated"] = date.today().isoformat()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check knowledge freshness")
    parser.add_argument("--db", required=True, help="Path to SQLite DB")
    parser.add_argument("--domain", help="Filter to domain")
    parser.add_argument("--report-path", help="Write JSON report to file")
    parser.add_argument("--json", action="store_true", help="Output JSON to stdout")
    args = parser.parse_args()

    db_path = Path(args.db)

    if args.report_path:
        result = generate_freshness_report(db_path, Path(args.report_path))
    elif args.domain:
        result = check_domain_freshness(db_path, args.domain)
    else:
        result = check_freshness(db_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Total: {result['total_pages']}  Fresh: {result['fresh']}  Stale: {result['stale']}")
        for sp in result["stale_pages"]:
            print(f"  STALE: {sp['path']} ({sp['domain']}) — {sp['days_since']}d > {sp['threshold']}d")

    return 1 if result["stale"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
