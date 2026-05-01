"""Tests for knowledge_audit module."""

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from knowledge_audit import AuditResult, FileAudit, audit_file, audit_directory


def _write(tmp: Path, name: str, content: str) -> Path:
    p = tmp / name
    p.write_text(content, encoding="utf-8")
    return p


class TestAuditResultEnum:
    def test_audit_result_enum(self):
        assert AuditResult.PASS.value == "PASS"
        assert AuditResult.STALE.value == "STALE"
        assert AuditResult.FAIL.value == "FAIL"


class TestAuditFile:
    def test_audit_file_pass(self, tmp_path):
        p = _write(tmp_path, "good.md", (
            "---\n"
            "type: knowledge\n"
            "category: compute\n"
            "source_url: https://example.com\n"
            "last_verified: 2026-04-30\n"
            "freshness_days: 90\n"
            "captured_date: 2026-04-30\n"
            "---\n"
            "This is valid body content with enough characters.\n"
        ))
        result = audit_file(p)
        assert result.status == AuditResult.PASS
        assert result.issues == []

    def test_audit_file_stale(self, tmp_path):
        p = _write(tmp_path, "stale.md", (
            "---\n"
            "type: knowledge\n"
            "category: compute\n"
            "source_url: https://example.com\n"
            "last_verified: 2025-01-01\n"
            "freshness_days: 30\n"
            "captured_date: 2025-01-01\n"
            "---\n"
            "This is valid body content with enough characters.\n"
        ))
        result = audit_file(p)
        assert result.status == AuditResult.STALE

    def test_audit_file_fail_missing_fields(self, tmp_path):
        p = _write(tmp_path, "bad.md", (
            "---\n"
            "type: knowledge\n"
            "---\n"
            "This is valid body content with enough characters.\n"
        ))
        result = audit_file(p)
        assert result.status == AuditResult.FAIL
        assert len(result.issues) > 0
        # Should mention missing fields
        assert any("missing" in i.lower() or "required" in i.lower() for i in result.issues)

    def test_audit_file_fail_no_frontmatter(self, tmp_path):
        p = _write(tmp_path, "nofm.md", "Just some text without frontmatter.\n")
        result = audit_file(p)
        assert result.status == AuditResult.FAIL

    def test_audit_file_fail_short_body(self, tmp_path):
        p = _write(tmp_path, "short.md", (
            "---\n"
            "type: knowledge\n"
            "category: compute\n"
            "source_url: https://example.com\n"
            "last_verified: 2026-04-30\n"
            "freshness_days: 90\n"
            "captured_date: 2026-04-30\n"
            "---\n"
            "Short\n"
        ))
        result = audit_file(p)
        assert result.status == AuditResult.FAIL


class TestAuditDirectory:
    def test_audit_directory_summary(self, tmp_path):
        _write(tmp_path, "good.md", (
            "---\n"
            "type: knowledge\n"
            "category: compute\n"
            "source_url: https://example.com\n"
            "last_verified: 2026-04-30\n"
            "freshness_days: 90\n"
            "captured_date: 2026-04-30\n"
            "---\n"
            "This is valid body content with enough characters.\n"
        ))
        _write(tmp_path, "bad.md", "No frontmatter here.\n")
        summary = audit_directory(tmp_path)
        assert summary["total"] == 2
        assert summary["pass"] >= 1
        assert summary["fail"] >= 1
        assert len(summary["results"]) == 2
