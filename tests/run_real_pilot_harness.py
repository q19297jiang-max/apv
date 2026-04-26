#!/usr/bin/env python3
"""
APV Real Pilot Harness

Runs current project-level validators against the real BBC sample project under
the canonical apv-projects contract.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = REPO_ROOT / "tests" / "projects" / "bbc-bank--credit-card-issuing-2026-04-25"
DEFAULT_COMPARISON_PROJECT = REPO_ROOT.parents[1] / "apv-projects" / "bbc-bank--credit-card-issuing-2026-04-25"
SELECTED_OUTPUTS = [
    Path("outputs/02-compliance.md"),
    Path("outputs/05-pricing.md"),
    Path("outputs/06-response.md"),
]


def run_check(label: str, command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip() or result.stderr.strip()

    print(f"\n[{label}]")
    if output:
        print(output)
    else:
        print("(no output)")

    return result.returncode, output


def compare_selected_files(baseline_project: Path, comparison_project: Path) -> list[str]:
    differences: list[str] = []

    for relative_path in SELECTED_OUTPUTS:
        baseline_file = baseline_project / relative_path
        comparison_file = comparison_project / relative_path

        if not baseline_file.exists():
            differences.append(f"{relative_path.as_posix()}: missing in baseline project")
            continue
        if not comparison_file.exists():
            differences.append(f"{relative_path.as_posix()}: missing in comparison project")
            continue

        baseline_content = baseline_file.read_text(encoding="utf-8")
        comparison_content = comparison_file.read_text(encoding="utf-8")
        if baseline_content != comparison_content:
            differences.append(f"{relative_path.as_posix()}: content differs")

    return differences


def main() -> int:
    parser = argparse.ArgumentParser(description="Run APV real pilot checks")
    parser.add_argument(
        "--project",
        type=Path,
        default=DEFAULT_PROJECT,
        help="Path to the APV project to validate",
    )
    parser.add_argument(
        "--compare-to",
        type=Path,
        default=DEFAULT_COMPARISON_PROJECT,
        help="Optional project path to compare selected output artifacts against",
    )
    args = parser.parse_args()

    project_path = args.project.resolve()
    if not project_path.exists():
        print(f"Project path not found: {project_path}")
        return 1

    python_executable = sys.executable
    validate_script = REPO_ROOT / "tools" / "validate-source-urls.py"
    freshness_script = REPO_ROOT / "tools" / "check-pricing-freshness.py"

    print("=" * 60)
    print("APV REAL PILOT HARNESS")
    print("=" * 60)
    print(f"Project: {project_path}")
    print("Checks: source URL validation, pricing freshness")

    comparison_path = args.compare_to.resolve()
    comparison_enabled = comparison_path.exists()
    if comparison_enabled:
        print(f"Comparison target: {comparison_path}")

    validate_code, _ = run_check(
        "source-url-validation",
        [python_executable, str(validate_script), "--project", str(project_path)],
    )
    freshness_code, _ = run_check(
        "pricing-freshness",
        [python_executable, str(freshness_script), "--project", str(project_path)],
    )

    comparison_differences: list[str] = []
    if comparison_enabled:
        comparison_differences = compare_selected_files(project_path, comparison_path)
        print("\n[artifact-comparison]")
        if comparison_differences:
            for item in comparison_differences:
                print(item)
        else:
            print("Selected output artifacts match comparison project")

    print("\n" + "=" * 60)
    print("HARNESS SUMMARY")
    print("=" * 60)
    print(f"Source URL validation: {'PASS' if validate_code == 0 else 'FAIL'}")
    print(f"Pricing freshness: {'PASS' if freshness_code == 0 else 'FAIL'}")
    if comparison_enabled:
        print(f"Artifact comparison: {'PASS' if not comparison_differences else 'FAIL'}")
    else:
        print("Artifact comparison: SKIPPED")

    if validate_code == 0 and freshness_code == 0 and not comparison_differences:
        print("Overall result: PASS")
        return 0

    print("Overall result: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())