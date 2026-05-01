"""Tests for migrate_v1.py — V1→V2 knowledge migration."""
from pathlib import Path

from migrate_v1 import enrich_frontmatter, map_v1_path_to_v2


def _base_fm(**overrides):
    fm = {
        "type": "apv-knowledge",
        "category": "card-systems",
        "title": "Card Issuing Platform",
        "source_url": "https://www.emvco.com/example",
        "captured_date": "2026-04-24",
        "verified_by": "Infrastructure Architect",
        "tags": ["card-systems", "issuing", "cards"],
    }
    fm.update(overrides)
    return fm


def test_enrich_adds_freshness_days():
    result = enrich_frontmatter(_base_fm(category="card-systems"))
    assert result["freshness_days"] == 365


def test_enrich_adds_last_verified():
    result = enrich_frontmatter(_base_fm(captured_date="2026-04-24"))
    assert result["last_verified"] == "2026-04-24"


def test_enrich_normalizes_type():
    result = enrich_frontmatter(_base_fm(type="apv-knowledge"))
    assert result["type"] == "source"


def test_enrich_pricing_gets_30_day_freshness():
    result = enrich_frontmatter(_base_fm(category="pricing"))
    assert result["freshness_days"] == 30


def test_enrich_compliance_gets_365_day_freshness():
    result = enrich_frontmatter(_base_fm(category="compliance"))
    assert result["freshness_days"] == 365


def test_map_v1_path_card_systems():
    p = Path("wiki/apv/knowledge/card-systems/issuing.md")
    assert map_v1_path_to_v2(p) == Path("knowledge/card-systems/issuing.md")


def test_map_v1_path_compliance_country():
    p = Path("wiki/apv/knowledge/compliance/singapore/mas-trmg.md")
    assert map_v1_path_to_v2(p) == Path("knowledge/compliance/singapore/mas-trmg.md")


def test_map_v1_path_pricing():
    p = Path("wiki/apv/knowledge/pricing/aws.md")
    assert map_v1_path_to_v2(p) == Path("knowledge/pricing/aws.md")


def test_map_v1_skips_templates():
    p = Path("wiki/apv/knowledge/card-systems/issuing.template.md")
    assert map_v1_path_to_v2(p) is None


def test_map_v1_skips_scripts():
    p = Path("wiki/apv/knowledge/pricing/pricing-fetcher.py")
    assert map_v1_path_to_v2(p) is None
