import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from lib.db import create_schema, insert_knowledge_page, get_stale_pages, insert_pricing


def test_create_schema(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert "knowledge_pages" in tables
    assert "pricing" in tables
    assert "compliance" in tables
    assert "infrastructure" in tables
    assert "knowledge_gaps" in tables
    conn.close()


def test_insert_knowledge_page(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    insert_knowledge_page(conn, {
        "path": "knowledge/pricing/aws.md",
        "domain": "pricing",
        "type": "source",
        "source_url": "https://aws.amazon.com/ec2/pricing/",
        "freshness_days": 30,
        "last_verified": "2026-04-01",
        "title": "AWS EC2 Pricing",
    })
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    assert len(rows) == 1
    conn.close()


def test_stale_knowledge_detection(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    insert_knowledge_page(conn, {
        "path": "knowledge/pricing/old.md",
        "domain": "pricing",
        "type": "source",
        "source_url": "https://example.com",
        "freshness_days": 30,
        "last_verified": "2026-01-01",
        "title": "Old Pricing",
    })
    stale = get_stale_pages(conn)
    assert len(stale) == 1
    assert stale[0]["path"] == "knowledge/pricing/old.md"
    conn.close()


def test_insert_pricing(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    insert_pricing(conn, {
        "provider": "aws",
        "region": "ap-southeast-1",
        "service": "EC2",
        "instance_type": "m6i.xlarge",
        "hourly_price": 0.192,
        "monthly_price": 140.16,
        "source_url": "https://aws.amazon.com/ec2/pricing/",
        "verified_date": "2026-04-01",
    })
    rows = conn.execute("SELECT * FROM pricing WHERE provider='aws'").fetchall()
    assert len(rows) == 1
    conn.close()
