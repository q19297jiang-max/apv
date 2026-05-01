"""Query pricing from SQLite database. Used by rfp-pricer skill."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

# Allow imports when run as script or module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.db import create_schema


def _connect(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def lookup_price(
    db_path,
    provider: str,
    region: str,
    service: str,
    instance_type: str | None = None,
    pricing_model: str = "on-demand",
) -> list[dict]:
    """Query pricing table, return matching rows as dicts."""
    conn = _connect(db_path)
    sql = "SELECT * FROM pricing WHERE provider=? AND region=? AND service=? AND pricing_model=?"
    params: list = [provider, region, service, pricing_model]
    if instance_type:
        sql += " AND instance_type=?"
        params.append(instance_type)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def lookup_service_prices(
    db_path, provider: str, region: str, service: str
) -> list[dict]:
    """All prices for a service (all pricing models)."""
    conn = _connect(db_path)
    rows = conn.execute(
        "SELECT * FROM pricing WHERE provider=? AND region=? AND service=? ORDER BY instance_type, pricing_model",
        (provider, region, service),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def format_pricing_table(rows: list[dict]) -> str:
    """Format pricing rows as a markdown table."""
    if not rows:
        return "_No pricing data found._"
    headers = ["Instance Type", "Pricing Model", "Hourly ($)", "Monthly ($)"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('instance_type', '-')} | {r.get('pricing_model', '-')} "
            f"| {r.get('hourly_price', '-')} | {r.get('monthly_price', '-')} |"
        )
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Query APV pricing database")
    p.add_argument("--db", required=True, help="Path to SQLite database")
    p.add_argument("--provider", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--service", required=True)
    p.add_argument("--instance-type", default=None)
    p.add_argument("--pricing-model", default="on-demand")
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()

    if args.instance_type:
        rows = lookup_price(args.db, args.provider, args.region, args.service, args.instance_type, args.pricing_model)
    else:
        rows = lookup_service_prices(args.db, args.provider, args.region, args.service)

    if args.as_json:
        print(json.dumps(rows, indent=2))
    else:
        print(format_pricing_table(rows))


if __name__ == "__main__":
    main()
