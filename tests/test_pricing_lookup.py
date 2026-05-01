"""Tests for tools/pricing_lookup.py."""

import json
import sqlite3
import tempfile
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from lib.db import create_schema
from pricing_lookup import lookup_price, lookup_service_prices, format_pricing_table


def _make_db(tmp_path: Path) -> Path:
    """Create a temp DB with test pricing data.

    Note: The pricing table PK is (provider, region, service, instance_type),
    so we encode pricing_model into instance_type for savings-plans entries
    by dropping the default PK and recreating with pricing_model in the key.
    """
    db_path = tmp_path / "test.sqlite"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    # Create schema but drop and recreate pricing with pricing_model in PK
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS pricing (
            provider TEXT NOT NULL,
            region TEXT NOT NULL,
            service TEXT NOT NULL,
            instance_type TEXT,
            hourly_price REAL,
            monthly_price REAL,
            pricing_model TEXT,
            source_url TEXT,
            verified_date TEXT,
            PRIMARY KEY (provider, region, service, instance_type, pricing_model)
        );
    """)
    rows = [
        ("aws", "ap-southeast-1", "EC2", "m6i.xlarge", 0.192, 140.16, "on-demand", "https://aws.amazon.com/ec2/pricing/", "2026-01-01"),
        ("aws", "ap-southeast-1", "EC2", "m6i.2xlarge", 0.384, 280.32, "on-demand", "https://aws.amazon.com/ec2/pricing/", "2026-01-01"),
        ("aws", "ap-southeast-1", "EC2", "m6i.xlarge", 0.123, 89.79, "savings-plans", "https://aws.amazon.com/ec2/pricing/", "2026-01-01"),
        ("aws", "ap-southeast-1", "RDS", "db.m6i.xlarge", 0.45, 328.5, "on-demand", "https://aws.amazon.com/rds/pricing/", "2026-01-01"),
        ("aws", "us-east-1", "EC2", "m6i.xlarge", 0.096, 70.08, "on-demand", "https://aws.amazon.com/ec2/pricing/", "2026-01-01"),
    ]
    for r in rows:
        conn.execute(
            """INSERT OR REPLACE INTO pricing
               (provider, region, service, instance_type, hourly_price, monthly_price, pricing_model, source_url, verified_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            r,
        )
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def db_path(tmp_path):
    return _make_db(tmp_path)


def test_lookup_exact_match(db_path):
    results = lookup_price(db_path, "aws", "ap-southeast-1", "EC2", instance_type="m6i.xlarge")
    assert len(results) == 1
    assert results[0]["instance_type"] == "m6i.xlarge"
    assert results[0]["hourly_price"] == 0.192


def test_lookup_no_match(db_path):
    results = lookup_price(db_path, "aws", "ap-southeast-1", "EC2", instance_type="c7g.16xlarge")
    assert results == []


def test_lookup_service_prices(db_path):
    results = lookup_service_prices(db_path, "aws", "ap-southeast-1", "EC2")
    assert len(results) == 3  # m6i.xlarge on-demand, m6i.2xlarge on-demand, m6i.xlarge savings-plans


def test_format_pricing_table(db_path):
    rows = lookup_service_prices(db_path, "aws", "ap-southeast-1", "EC2")
    table = format_pricing_table(rows)
    assert "| Instance Type" in table
    assert "m6i.xlarge" in table
    assert "---" in table  # separator line


def test_lookup_with_pricing_model(db_path):
    od = lookup_price(db_path, "aws", "ap-southeast-1", "EC2", instance_type="m6i.xlarge", pricing_model="on-demand")
    sp = lookup_price(db_path, "aws", "ap-southeast-1", "EC2", instance_type="m6i.xlarge", pricing_model="savings-plans")
    assert len(od) == 1
    assert od[0]["pricing_model"] == "on-demand"
    assert len(sp) == 1
    assert sp[0]["pricing_model"] == "savings-plans"
    assert sp[0]["hourly_price"] < od[0]["hourly_price"]
