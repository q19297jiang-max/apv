"""Regression tests for APV preflight behavior."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from create_snapshot import create_project_snapshot


REPO_ROOT = Path(__file__).resolve().parent.parent


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_false_green_project(project_dir: Path, db_path: Path) -> None:
    _write(project_dir / "input" / "normalized" / "rfp.md", "# RFP\n")
    _write(project_dir / "input" / "normalized" / "requirements-summary.md", "# Requirements\n")
    _write(project_dir / "input" / "normalized" / "volume-summary.md", "# Volume\n")

    _write(project_dir / "outputs" / "01-brainstorm.md", "# Brainstorm\n")
    _write(project_dir / "outputs" / "02-compliance.md", "# Compliance\n")
    _write(project_dir / "outputs" / "03-architecture.md", "# Architecture\n")
    _write(project_dir / "outputs" / "04-sizing.md", "# Sizing\n")
    _write(project_dir / "outputs" / "05-pricing.md", "# Pricing\n")
    _write(project_dir / "outputs" / "06-response.md", "# Response\n")
    _write(project_dir / "approvals" / "unified-checklist.md", "# Checklist\n")
    _write(project_dir / "evidence" / "pricing" / "pricing-evidence.md", "evidence")

    _write(
        project_dir / "verification" / "source-url-validation.json",
        json.dumps(
            {
                "pass": False,
                "valid": 2,
                "invalid": 0,
                "manual_review_required": True,
                "issues": ["Manual source review required before release."],
            }
        ),
    )
    _write(
        project_dir / "verification" / "freshness-report.json",
        json.dumps({"pass": True, "fresh": 10, "stale": 0}),
    )

    create_project_snapshot(project_dir, db_path, knowledge_commit="test-sha")


def _write_run_context(project_dir: Path, *, mode: str, release_eligible: bool, sales_brief_approved: bool) -> None:
    _write(
        project_dir / "working" / "00-run-context.json",
        json.dumps(
            {
                "mode": mode,
                "promotion_state": "not-eligible",
                "sales_brief_present": sales_brief_approved,
                "sales_brief_approved": sales_brief_approved,
                "release_eligible": release_eligible,
                "current_blocker": "Draft mode is not release-eligible" if mode == "draft" else "",
                "intent_capture_mode": "none",
                "urgency": "standard",
                "promotion_path": None,
                "promotion_attestation": None,
            }
        ),
    )


def test_preflight_rejects_stage_7_manual_review_false_green(tmp_path):
    project_dir = tmp_path / "project"
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder", encoding="utf-8")
    _make_false_green_project(project_dir, db_path)

    completed = subprocess.run(
        [str(REPO_ROOT / "bin" / "apv-preflight"), "--project", str(project_dir), "--skip-tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    assert "Stage 7: FAIL" in completed.stdout


def test_preflight_json_mode_returns_parseable_failure_payload(tmp_path):
    project_dir = tmp_path / "project"
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder", encoding="utf-8")
    _make_false_green_project(project_dir, db_path)

    completed = subprocess.run(
        [str(REPO_ROOT / "bin" / "apv-preflight"), "--project", str(project_dir), "--skip-tests", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    payload = json.loads(completed.stdout)
    assert payload["pass"] is False
    assert payload["repo_tests"]["skipped"] is True
    assert payload["snapshot"]["pass"] is True
    assert any(stage["stage"] == 7 and stage["pass"] is False for stage in payload["stages"])


def test_preflight_json_reports_draft_mode_governance_blocker(tmp_path):
    project_dir = tmp_path / "project"
    db_path = tmp_path / "apv-v2.sqlite"
    db_path.write_text("sqlite placeholder", encoding="utf-8")
    _make_false_green_project(project_dir, db_path)
    _write(
        project_dir / "verification" / "source-url-validation.json",
        json.dumps({"pass": True, "invalid": 0, "manual_review_required": False}),
    )
    _write(
        project_dir / "outputs" / "07-approval.md",
        "---\nstage: 7\ndecision: APPROVED\n---\n# Approval\n",
    )
    _write(
        project_dir / "approvals" / "release-decision.md",
        "---\nstage: 7\ndecision: APPROVED\n---\n# Release\n",
    )
    _write(
        project_dir / "approvals" / "reviewer-notes.md",
        "---\nstage: 7\ntype: reviewer-notes\n---\n# Notes\n",
    )
    _write_run_context(project_dir, mode="draft", release_eligible=False, sales_brief_approved=False)

    completed = subprocess.run(
        [str(REPO_ROOT / "bin" / "apv-preflight"), "--project", str(project_dir), "--skip-tests", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    payload = json.loads(completed.stdout)
    stage7 = next(stage for stage in payload["stages"] if stage["stage"] == 7)
    assert any("draft mode" in issue.lower() for issue in stage7["issues"])
