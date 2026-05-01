"""Tests for tools/freshness.py."""
import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pytest

from lib.db import create_schema, insert_knowledge_page
from freshness import check_freshness, check_domain_freshness, generate_freshness_report


def _make_page(path, domain="pricing", days_ago=10, freshness_days=90):
    """Helper to build a knowledge page dict."""
    verified = (date.today() - timedelta(days=days_ago)).isoformat()
    return {
        "path": path,
        "domain": domain,
        "type": "reference",
        "title": path,
        "source_url": f"https://example.com/{path}",
        "last_verified": verified,
        "freshness_days": freshness_days,
    }


@pytest.fixture
def db_path(tmp_path):
    p = tmp_path / "test.sqlite"
    conn = create_schema(p)
    conn.close()
    return p


def test_check_freshness_all_fresh(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    insert_knowledge_page(conn, _make_page("fresh.md", days_ago=5, freshness_days=90))
    conn.close()

    result = check_freshness(db_path)
    assert result["total_pages"] == 1
    assert result["fresh"] == 1
    assert result["stale"] == 0
    assert result["stale_pages"] == []


def test_check_freshness_detects_stale(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    insert_knowledge_page(conn, _make_page("stale.md", days_ago=100, freshness_days=30))
    conn.close()

    result = check_freshness(db_path)
    assert result["total_pages"] == 1
    assert result["stale"] == 1
    assert result["fresh"] == 0
    assert len(result["stale_pages"]) == 1
    sp = result["stale_pages"][0]
    assert sp["path"] == "stale.md"
    assert sp["domain"] == "pricing"
    assert sp["days_since"] >= 100
    assert sp["threshold"] == 30


def test_check_domain_freshness(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    insert_knowledge_page(conn, _make_page("p1.md", domain="pricing", days_ago=100, freshness_days=30))
    insert_knowledge_page(conn, _make_page("c1.md", domain="compliance", days_ago=100, freshness_days=30))
    conn.close()

    result = check_domain_freshness(db_path, "pricing")
    assert result["total_pages"] == 1
    assert result["stale"] == 1
    assert all(sp["domain"] == "pricing" for sp in result["stale_pages"])


def test_generate_freshness_report(db_path, tmp_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    insert_knowledge_page(conn, _make_page("ok.md", days_ago=5, freshness_days=90))
    insert_knowledge_page(conn, _make_page("old.md", days_ago=100, freshness_days=30))
    conn.close()

    out = tmp_path / "freshness-report.json"
    result = generate_freshness_report(db_path, out)
    assert result["total_pages"] == 2
    assert result["stale"] == 1

    data = json.loads(out.read_text())
    assert data["total_pages"] == 2
    assert len(data["stale_pages"]) == 1
