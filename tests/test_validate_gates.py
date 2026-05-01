"""Tests for validate_gates.py"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from validate_gates import (
    STAGE_CONTRACTS,
    check_gate,
    validate_commercial_overrides,
    validate_snapshot,
)


def _sha256_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def test_stage_contracts_defined():
    """All 8 stages (0-7) exist in STAGE_CONTRACTS."""
    for i in range(8):
        assert i in STAGE_CONTRACTS, f"Stage {i} missing from STAGE_CONTRACTS"


def test_check_gate_pass(tmp_path):
    """Stage 1 passes when required files exist."""
    for rel in STAGE_CONTRACTS[1]:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("test")
    result = check_gate(tmp_path, 1)
    assert result["pass"] is True
    assert result["stage"] == 1
    assert result["missing"] == []
    assert sorted(result["present"]) == sorted(STAGE_CONTRACTS[1])


def test_check_gate_fail(tmp_path):
    """Stage 1 fails when dir is empty."""
    result = check_gate(tmp_path, 1)
    assert result["pass"] is False
    assert result["stage"] == 1
    assert len(result["missing"]) == len(STAGE_CONTRACTS[1])


def test_check_gate_stage_2_requires_stage_1_output(tmp_path):
    """Stage 2 needs outputs/01-brainstorm.md."""
    result = check_gate(tmp_path, 2)
    assert result["pass"] is False
    assert "outputs/01-brainstorm.md" in result["missing"]


def test_check_gate_stage_0_always_passes(tmp_path):
    """Stage 0 has no requirements, always passes."""
    result = check_gate(tmp_path, 0)
    assert result["pass"] is True
    assert result["missing"] == []
    assert result["present"] == []


def test_validate_snapshot_requires_snapshot_artifacts(tmp_path):
    result = validate_snapshot(tmp_path)
    assert result["pass"] is False
    assert "working/00-knowledge-snapshot.json" in result["missing"]
    assert "working/apv-v2-snapshot.sqlite" in result["missing"]


def test_validate_snapshot_passes_with_matching_checksums(tmp_path):
    working = tmp_path / "working"
    evidence = tmp_path / "evidence" / "pricing"
    working.mkdir(parents=True)
    evidence.mkdir(parents=True)

    evidence_file = evidence / "pricing-evidence.md"
    evidence_text = "pricing evidence"
    evidence_file.write_text(evidence_text)

    overrides_file = working / "05-commercial-overrides.md"
    overrides_text = "approved_by: Finance\nvalid_until: 2099-01-01\n"
    overrides_file.write_text(overrides_text)

    snapshot = {
        "knowledge_commit": "abc123",
        "snapshot_date": "2026-05-01T10:00:00Z",
        "snapshot_boundary": "knowledge/ + evidence/ + working/05-commercial-overrides.md",
        "evidence_checksums": {
            "evidence/pricing/pricing-evidence.md": _sha256_text(evidence_text),
        },
        "commercial_overrides_checksum": _sha256_text(overrides_text),
    }
    (working / "00-knowledge-snapshot.json").write_text(json.dumps(snapshot, indent=2))
    (working / "apv-v2-snapshot.sqlite").write_text("sqlite placeholder")

    result = validate_snapshot(tmp_path)
    assert result["pass"] is True
    assert result["issues"] == []


def test_validate_snapshot_detects_mutated_boundary_file(tmp_path):
    working = tmp_path / "working"
    evidence = tmp_path / "evidence" / "pricing"
    working.mkdir(parents=True)
    evidence.mkdir(parents=True)

    evidence_file = evidence / "pricing-evidence.md"
    evidence_file.write_text("new text")

    snapshot = {
        "knowledge_commit": "abc123",
        "snapshot_date": "2026-05-01T10:00:00Z",
        "snapshot_boundary": "knowledge/ + evidence/",
        "evidence_checksums": {
            "evidence/pricing/pricing-evidence.md": _sha256_text("old text"),
        },
    }
    (working / "00-knowledge-snapshot.json").write_text(json.dumps(snapshot, indent=2))
    (working / "apv-v2-snapshot.sqlite").write_text("sqlite placeholder")

    result = validate_snapshot(tmp_path)
    assert result["pass"] is False
    assert any("checksum mismatch" in issue.lower() for issue in result["issues"])


def test_validate_commercial_overrides_passes_when_absent(tmp_path):
    result = validate_commercial_overrides(tmp_path)
    assert result["pass"] is True
    assert result["issues"] == []


def test_validate_commercial_overrides_requires_approval_fields(tmp_path):
    working = tmp_path / "working"
    working.mkdir(parents=True)
    (working / "05-commercial-overrides.md").write_text("# Overrides\n\nNo frontmatter here\n")

    result = validate_commercial_overrides(tmp_path)
    assert result["pass"] is False
    assert any("approved_by" in issue for issue in result["issues"])
    assert any("valid_until" in issue for issue in result["issues"])


def test_validate_commercial_overrides_rejects_expired_override(tmp_path):
    working = tmp_path / "working"
    evidence = tmp_path / "evidence" / "pricing" / "commercial"
    working.mkdir(parents=True)
    evidence.mkdir(parents=True)
    (evidence / "quote.pdf").write_text("quote")
    (working / "05-commercial-overrides.md").write_text(
        "---\napproved_by: Finance\nvalid_until: 2020-01-01\n---\n# Overrides\n"
    )

    result = validate_commercial_overrides(tmp_path)
    assert result["pass"] is False
    assert any("expired" in issue.lower() for issue in result["issues"])


def test_validate_commercial_overrides_requires_evidence(tmp_path):
    working = tmp_path / "working"
    working.mkdir(parents=True)
    (working / "05-commercial-overrides.md").write_text(
        "---\napproved_by: Finance\nvalid_until: 2099-01-01\n---\n# Overrides\n"
    )

    result = validate_commercial_overrides(tmp_path)
    assert result["pass"] is False
    assert any("evidence" in issue.lower() for issue in result["issues"])


def test_validate_commercial_overrides_passes_with_metadata_and_evidence(tmp_path):
    working = tmp_path / "working"
    evidence = tmp_path / "evidence" / "pricing" / "commercial"
    working.mkdir(parents=True)
    evidence.mkdir(parents=True)
    (evidence / "quote.pdf").write_text("quote")
    (working / "05-commercial-overrides.md").write_text(
        "---\napproved_by: Finance\nvalid_until: 2099-01-01\n---\n# Overrides\n"
    )

    result = validate_commercial_overrides(tmp_path)
    assert result["pass"] is True
    assert result["issues"] == []
