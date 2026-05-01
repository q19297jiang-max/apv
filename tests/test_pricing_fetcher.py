"""Tests for tools/pricing_fetcher.py."""

import textwrap
from pathlib import Path
from datetime import date

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from pricing_fetcher import check_pricing_freshness, generate_refresh_plan


def _write_pricing_md(tmp_path, filename, last_verified, freshness_days=30):
    """Helper to create a pricing .md file with frontmatter."""
    pricing_dir = tmp_path / "knowledge" / "pricing"
    pricing_dir.mkdir(parents=True, exist_ok=True)
    f = pricing_dir / filename
    f.write_text(textwrap.dedent(f"""\
        ---
        type: source
        category: pricing
        freshness_days: {freshness_days}
        last_verified: {last_verified}
        tags: [pricing]
        ---
        # Pricing
    """))
    return f


class TestCheckPricingFreshness:
    def test_check_pricing_freshness_all_fresh(self, tmp_path):
        today = date.today().isoformat()
        _write_pricing_md(tmp_path, "aws.md", today, 30)
        results = check_pricing_freshness(tmp_path / "knowledge")
        assert len(results) == 1
        assert results[0]["status"] == "fresh"
        assert results[0]["provider"] == "aws"

    def test_check_pricing_freshness_stale(self, tmp_path):
        from datetime import timedelta
        old = (date.today() - timedelta(days=45)).isoformat()
        _write_pricing_md(tmp_path, "aws.md", old, 30)
        results = check_pricing_freshness(tmp_path / "knowledge")
        assert len(results) == 1
        assert results[0]["status"] == "stale"
        assert results[0]["days_since"] >= 45

    def test_check_pricing_freshness_expired(self, tmp_path):
        from datetime import timedelta
        old = (date.today() - timedelta(days=90)).isoformat()
        _write_pricing_md(tmp_path, "aws.md", old, 30)
        results = check_pricing_freshness(tmp_path / "knowledge")
        assert len(results) == 1
        assert results[0]["status"] == "expired"

    def test_skips_non_pricing_files(self, tmp_path):
        """Scripts (.py) and non-md files in pricing dir should be ignored."""
        pricing_dir = tmp_path / "knowledge" / "pricing"
        pricing_dir.mkdir(parents=True, exist_ok=True)
        (pricing_dir / "some_script.py").write_text("print('hi')")
        (pricing_dir / "README.txt").write_text("readme")
        _write_pricing_md(tmp_path, "aws.md", date.today().isoformat(), 30)
        results = check_pricing_freshness(tmp_path / "knowledge")
        assert len(results) == 1
        assert results[0]["provider"] == "aws"


class TestGenerateRefreshPlan:
    def test_generate_refresh_plan(self):
        stale_files = [
            {"path": "/k/pricing/aws.md", "provider": "aws", "status": "stale",
             "days_since": 45, "freshness_days": 30, "last_verified": "2026-03-15"},
            {"path": "/k/pricing/gcp.md", "provider": "gcp", "status": "expired",
             "days_since": 90, "freshness_days": 30, "last_verified": "2026-01-30"},
        ]
        plan = generate_refresh_plan(stale_files)
        assert "calculator.aws" in plan
        assert "cloud.google.com/products/calculator" in plan
        assert "aws.md" in plan
        assert "gcp.md" in plan
        assert "expired" in plan.lower() or "EXPIRED" in plan
