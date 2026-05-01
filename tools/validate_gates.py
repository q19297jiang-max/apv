#!/usr/bin/env python3
"""Gate validator for APV V2 pipeline stages.

Checks whether required upstream artifacts exist before a stage runs.

Usage:
    python3 validate_gates.py --project PATH --stage N [--json]
"""
import argparse
import json
import sys
from pathlib import Path

STAGE_CONTRACTS: dict[int, list[str]] = {
    0: [],
    1: ["input/normalized/rfp.md", "input/normalized/requirements-summary.md"],
    2: ["outputs/01-brainstorm.md", "input/normalized/requirements-summary.md"],
    3: ["outputs/01-brainstorm.md", "outputs/02-compliance.md"],
    4: ["outputs/03-architecture.md", "input/normalized/volume-summary.md"],
    5: ["outputs/03-architecture.md", "outputs/04-sizing.md"],
    6: [
        "outputs/01-brainstorm.md",
        "outputs/02-compliance.md",
        "outputs/03-architecture.md",
        "outputs/04-sizing.md",
        "outputs/05-pricing.md",
    ],
    7: ["outputs/06-response.md"],
}


def check_gate(project_dir: Path, stage: int) -> dict:
    """Check if required upstream artifacts exist for a given stage.

    Returns:
        {"pass": bool, "stage": int, "missing": [str], "present": [str]}
    """
    required = STAGE_CONTRACTS.get(stage, [])
    missing = []
    present = []
    for rel in required:
        if (project_dir / rel).exists():
            present.append(rel)
        else:
            missing.append(rel)
    return {"pass": len(missing) == 0, "stage": stage, "missing": missing, "present": present}


def main():
    parser = argparse.ArgumentParser(description="Validate pipeline stage gates")
    parser.add_argument("--project", type=Path, required=True, help="Project directory")
    parser.add_argument("--stage", type=int, required=True, help="Stage number (0-7)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.stage not in STAGE_CONTRACTS:
        print(f"Error: unknown stage {args.stage}. Valid: 0-7", file=sys.stderr)
        sys.exit(2)

    result = check_gate(args.project, args.stage)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS ✓" if result["pass"] else "FAIL ✗"
        print(f"Stage {result['stage']}: {status}")
        if result["missing"]:
            print("Missing:")
            for m in result["missing"]:
                print(f"  - {m}")
        if result["present"]:
            print("Present:")
            for p in result["present"]:
                print(f"  - {p}")

    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
