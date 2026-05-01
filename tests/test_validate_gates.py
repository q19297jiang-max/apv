"""Tests for validate_gates.py"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from validate_gates import STAGE_CONTRACTS, check_gate


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
