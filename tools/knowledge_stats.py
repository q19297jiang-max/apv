"""Knowledge base health dashboard — coverage, staleness, gaps."""

import argparse
import json
import sqlite3
from pathlib import Path

from lib.db import create_schema


def get_stats(db_path: Path) -> dict:
    """Query knowledge_pages for health stats."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    total = conn.execute("SELECT COUNT(*) FROM knowledge_pages").fetchone()[0]

    rows = conn.execute(
        "SELECT domain, COUNT(*) as cnt FROM knowledge_pages GROUP BY domain"
    ).fetchall()
    by_domain = {r["domain"]: r["cnt"] for r in rows}

    stale_count = conn.execute("SELECT COUNT(*) FROM stale_knowledge").fetchone()[0]

    freshest = conn.execute(
        "SELECT MAX(last_verified) FROM knowledge_pages"
    ).fetchone()[0]

    oldest = conn.execute(
        "SELECT MIN(last_verified) FROM knowledge_pages"
    ).fetchone()[0]

    domains = sorted(by_domain.keys())

    missing = conn.execute(
        "SELECT COUNT(*) FROM knowledge_pages WHERE source_url IS NULL"
    ).fetchone()[0]

    conn.close()

    return {
        "total_pages": total,
        "by_domain": by_domain,
        "stale_count": stale_count,
        "freshest_date": freshest,
        "oldest_date": oldest,
        "domains_covered": domains,
        "missing_source_urls": missing,
    }


def format_stats_report(stats: dict) -> str:
    """Format stats as a readable markdown report."""
    lines = [
        "# Knowledge Base Health Report",
        "",
        f"**Total pages:** {stats['total_pages']}",
        f"**Stale pages:** {stats['stale_count']}",
        f"**Freshest:** {stats['freshest_date'] or 'N/A'}",
        f"**Oldest:** {stats['oldest_date'] or 'N/A'}",
        f"**Missing source URLs:** {stats['missing_source_urls']}",
        "",
        "## Coverage by Domain",
        "",
        "| Domain | Pages |",
        "|--------|-------|",
    ]
    for domain, count in sorted(stats["by_domain"].items()):
        lines.append(f"| {domain} | {count} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Knowledge base health stats")
    parser.add_argument("--db", required=True, help="Path to SQLite DB")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    stats = get_stats(Path(args.db))

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(format_stats_report(stats))


if __name__ == "__main__":
    main()
