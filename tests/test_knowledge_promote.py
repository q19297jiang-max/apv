"""Tests for knowledge_promote.py — post-RFP gap promotion tool."""

import json
import textwrap
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from knowledge_promote import parse_gap_log, suggest_promotions, generate_promotion_report


GAP_LOG_CONTENT = textwrap.dedent("""\
    # Knowledge Gap Log

    | # | Domain | Description | Severity | Stage Found | Resolved |
    |---|--------|-------------|----------|-------------|----------|
    | 1 | pricing | AWS RDS pricing missing for db.r6g | HIGH | pricer | No |
    | 2 | compliance | Vietnam regulations not covered | LOW | brainstorm | No |
    | 3 | sizing | GPU instance sizing methodology | HIGH | calculator | Yes |
""")


def test_parse_gap_log(tmp_path):
    p = tmp_path / "gap-log.md"
    p.write_text(GAP_LOG_CONTENT)
    gaps = parse_gap_log(p)
    assert len(gaps) == 3
    assert gaps[0] == {
        "id": 1,
        "domain": "pricing",
        "description": "AWS RDS pricing missing for db.r6g",
        "severity": "HIGH",
        "stage_found": "pricer",
        "resolved": False,
    }
    assert gaps[2]["resolved"] is True


def test_parse_gap_log_empty(tmp_path):
    # Missing file
    assert parse_gap_log(tmp_path / "nope.md") == []
    # Empty file
    p = tmp_path / "empty.md"
    p.write_text("")
    assert parse_gap_log(p) == []


def test_suggest_promotions_filters_resolved():
    gaps = [
        {"id": 1, "domain": "pricing", "description": "x", "severity": "HIGH", "stage_found": "pricer", "resolved": False},
        {"id": 2, "domain": "sizing", "description": "y", "severity": "HIGH", "stage_found": "calculator", "resolved": True},
    ]
    suggestions = suggest_promotions(gaps)
    assert len(suggestions) == 1
    assert suggestions[0]["domain"] == "pricing"


def test_suggest_promotions_maps_paths():
    gaps = [
        {"id": 1, "domain": "pricing", "description": "AWS RDS pricing", "severity": "HIGH", "stage_found": "pricer", "resolved": False},
        {"id": 2, "domain": "compliance", "description": "Vietnam regs", "severity": "LOW", "stage_found": "brainstorm", "resolved": False},
    ]
    suggestions = suggest_promotions(gaps)
    assert suggestions[0]["suggested_path"].startswith("knowledge/pricing/")
    assert suggestions[1]["suggested_path"].startswith("knowledge/compliance/")


def test_generate_promotion_report(tmp_path):
    gap_log = tmp_path / "gap-log.md"
    gap_log.write_text(GAP_LOG_CONTENT)
    output = tmp_path / "report.md"

    stats = generate_promotion_report(gap_log, output)
    assert output.exists()
    assert stats["total_gaps"] == 3
    assert stats["unresolved"] == 2
    assert stats["promotions"] == 2
    content = output.read_text()
    assert "AWS RDS pricing" in content
