from pathlib import Path
import shutil


TESTS_ROOT = Path(__file__).resolve().parent


def build_runtime_project_fixture(tmp_path: Path) -> Path:
    project_root = tmp_path / "apv-projects" / "bbc-bank--credit-card-issuing--2026-04-26"

    (project_root / "input").mkdir(parents=True)
    (project_root / "outputs").mkdir()
    (project_root / "evidence" / "pricing").mkdir(parents=True)
    (project_root / "evidence" / "compliance").mkdir(parents=True)
    (project_root / "evidence" / "verification").mkdir(parents=True)
    (project_root / "approvals").mkdir()

    (project_root / "README.md").write_text(
        "# BBC Bank Credit Card Issuing System\n",
        encoding="utf-8",
    )
    (project_root / "SUMMARY.md").write_text(
        "# Execution Summary\n\nFixture-backed APV runtime test project.\n",
        encoding="utf-8",
    )

    shutil.copy(
        TESTS_ROOT / "data" / "bbc-rfp-summary.md",
        project_root / "input" / "bbc-rfp-summary.md",
    )
    shutil.copy(
        TESTS_ROOT / "output" / "bbc-brainstorm-output.md",
        project_root / "outputs" / "01-brainstorm.md",
    )
    shutil.copy(
        TESTS_ROOT / "output" / "bbc-compliance-output.md",
        project_root / "outputs" / "02-compliance.md",
    )
    shutil.copy(
        TESTS_ROOT / "output" / "bbc-pricing-output.md",
        project_root / "outputs" / "05-pricing.md",
    )
    shutil.copy(
        TESTS_ROOT / "output" / "bbc-response-output.md",
        project_root / "outputs" / "06-response.md",
    )

    approval_files = {
        "stage-1-requirements.md": "# Stage 1 Requirements Approval\n",
        "stage-2-compliance.md": "# Stage 2 Compliance Approval\n",
        "stage-3-architecture.md": "# Stage 3 Architecture Approval\n",
        "stage-4-sizing.md": "# Stage 4 Sizing Approval\n",
        "stage-5-pricing.md": "# Stage 5 Pricing Approval\n",
    }
    for relative_path, content in approval_files.items():
        (project_root / "approvals" / relative_path).write_text(content, encoding="utf-8")

    return project_root


def test_runtime_project_fixture_matches_canonical_contract(tmp_path: Path) -> None:
    project_root = build_runtime_project_fixture(tmp_path)

    expected_paths = [
        project_root / "README.md",
        project_root / "SUMMARY.md",
        project_root / "input",
        project_root / "outputs",
        project_root / "evidence" / "pricing",
        project_root / "evidence" / "compliance",
        project_root / "evidence" / "verification",
        project_root / "approvals",
        project_root / "outputs" / "01-brainstorm.md",
        project_root / "outputs" / "02-compliance.md",
        project_root / "outputs" / "05-pricing.md",
        project_root / "outputs" / "06-response.md",
        project_root / "approvals" / "stage-1-requirements.md",
        project_root / "approvals" / "stage-2-compliance.md",
        project_root / "approvals" / "stage-3-architecture.md",
        project_root / "approvals" / "stage-4-sizing.md",
        project_root / "approvals" / "stage-5-pricing.md",
    ]

    missing_paths = [path for path in expected_paths if not path.exists()]

    assert not missing_paths, "Missing expected runtime fixture paths: " + ", ".join(
        str(path.relative_to(project_root)) for path in missing_paths
    )


def test_runtime_project_fixture_contains_key_stage_markers(tmp_path: Path) -> None:
    project_root = build_runtime_project_fixture(tmp_path)

    brainstorm_output = (project_root / "outputs" / "01-brainstorm.md").read_text(encoding="utf-8")
    compliance_output = (project_root / "outputs" / "02-compliance.md").read_text(encoding="utf-8")
    pricing_output = (project_root / "outputs" / "05-pricing.md").read_text(encoding="utf-8")
    response_output = (project_root / "outputs" / "06-response.md").read_text(encoding="utf-8")

    assert "Executive Summary" in brainstorm_output
    assert "Recommended Approach" in brainstorm_output
    assert "PCI-DSS" in compliance_output
    assert "Executive Summary" in compliance_output
    assert "Monthly Cost Breakdown" in pricing_output
    assert "Source URLs" in pricing_output
    assert "Executive Summary" in response_output
    assert "Commercial Summary" in response_output