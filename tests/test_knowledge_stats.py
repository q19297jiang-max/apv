"""Tests for knowledge_stats tool."""
import json
import tempfile
from pathlib import Path

from lib.db import create_schema, insert_knowledge_page
from knowledge_stats import get_stats, format_stats_report


def _tmp_db():
    f = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    f.close()
    conn = create_schema(Path(f.name))
    return Path(f.name), conn


def _page(path, domain, **kw):
    return {
        "path": path,
        "domain": domain,
        "type": kw.get("type", "reference"),
        "title": kw.get("title", path),
        "source_url": kw.get("source_url"),
        "last_verified": kw.get("last_verified", "2026-04-30"),
        "freshness_days": kw.get("freshness_days", 90),
    }


def test_get_stats_basic():
    db_path, conn = _tmp_db()
    insert_knowledge_page(conn, _page("a.md", "pricing", source_url="https://x"))
    insert_knowledge_page(conn, _page("b.md", "pricing", source_url="https://y"))
    insert_knowledge_page(conn, _page("c.md", "compliance", source_url="https://z"))
    conn.close()

    stats = get_stats(db_path)
    assert stats["total_pages"] == 3
    assert stats["by_domain"]["pricing"] == 2
    assert stats["by_domain"]["compliance"] == 1
    assert set(stats["domains_covered"]) == {"pricing", "compliance"}
    assert stats["missing_source_urls"] == 0


def test_get_stats_empty_db():
    db_path, conn = _tmp_db()
    conn.close()

    stats = get_stats(db_path)
    assert stats["total_pages"] == 0
    assert stats["by_domain"] == {}
    assert stats["stale_count"] == 0
    assert stats["freshest_date"] is None
    assert stats["oldest_date"] is None


def test_get_stats_tracks_stale():
    db_path, conn = _tmp_db()
    # last_verified 200 days ago, freshness_days=90 → stale
    insert_knowledge_page(conn, _page("old.md", "infra", last_verified="2025-10-01", freshness_days=90))
    insert_knowledge_page(conn, _page("new.md", "infra", last_verified="2026-04-30", freshness_days=90))
    conn.close()

    stats = get_stats(db_path)
    assert stats["stale_count"] == 1
    assert stats["missing_source_urls"] == 2


def test_format_stats_report():
    stats = {
        "total_pages": 5,
        "by_domain": {"pricing": 3, "compliance": 2},
        "stale_count": 1,
        "freshest_date": "2026-04-30",
        "oldest_date": "2025-10-01",
        "domains_covered": ["pricing", "compliance"],
        "missing_source_urls": 0,
    }
    report = format_stats_report(stats)
    assert isinstance(report, str)
    assert "pricing" in report
    assert "3" in report
    assert "compliance" in report
