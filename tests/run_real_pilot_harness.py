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


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = WORKSPACE_ROOT / "apv-projects" / "bbc-bank--credit-card-issuing-2026-04-25"


def run_check(label: str, command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip() or result.stderr.strip()

    print(f"\n[{label}]")
    if output:
        print(output)
    else:
        print("(no output)")

    return result.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Run APV real pilot checks")
    parser.add_argument(
        "--project",
        type=Path,
        default=DEFAULT_PROJECT,
        help="Path to the APV project to validate",
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

    validate_code, _ = run_check(
        "source-url-validation",
        [python_executable, str(validate_script), "--project", str(project_path)],
    )
    freshness_code, _ = run_check(
        "pricing-freshness",
        [python_executable, str(freshness_script), "--project", str(project_path)],
    )

    print("\n" + "=" * 60)
    print("HARNESS SUMMARY")
    print("=" * 60)
    print(f"Source URL validation: {'PASS' if validate_code == 0 else 'FAIL'}")
    print(f"Pricing freshness: {'PASS' if freshness_code == 0 else 'FAIL'}")

    if validate_code == 0 and freshness_code == 0:
        print("Overall result: PASS")
        return 0

    print("Overall result: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())