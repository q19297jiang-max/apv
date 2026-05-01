#!/usr/bin/env python3
"""Gate validator for APV V2 pipeline stages.

Checks whether required upstream artifacts exist before a stage runs.

Usage:
    python3 validate_gates.py --project PATH --stage N [--json]
"""
import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from frontmatter import parse_file

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


def _sha256_file(file_path: Path) -> str:
    return "sha256:" + hashlib.sha256(file_path.read_bytes()).hexdigest()


def validate_snapshot(project_dir: Path) -> dict:
    """Validate snapshot artifacts and checksum integrity for a project."""
    project_dir = Path(project_dir)
    snapshot_path = project_dir / "working" / "00-knowledge-snapshot.json"
    snapshot_db = project_dir / "working" / "apv-v2-snapshot.sqlite"

    missing = []
    issues = []
    if not snapshot_path.exists():
        missing.append("working/00-knowledge-snapshot.json")
    if not snapshot_db.exists():
        missing.append("working/apv-v2-snapshot.sqlite")
    if missing:
        return {"pass": False, "missing": missing, "issues": issues}

    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"pass": False, "missing": [], "issues": [f"Invalid snapshot JSON: {exc}"]}

    for field in ("knowledge_commit", "snapshot_date", "snapshot_boundary"):
        if field not in snapshot:
            issues.append(f"Missing snapshot field: {field}")

    for rel_path, expected in snapshot.get("evidence_checksums", {}).items():
        file_path = project_dir / rel_path
        if not file_path.exists():
            issues.append(f"Snapshot boundary file missing: {rel_path}")
            continue
        actual = _sha256_file(file_path)
        if actual != expected:
            issues.append(f"Checksum mismatch for {rel_path}")

    overrides_checksum = snapshot.get("commercial_overrides_checksum")
    if overrides_checksum is not None:
        overrides_path = project_dir / "working" / "05-commercial-overrides.md"
        if not overrides_path.exists():
            issues.append("Snapshot expects working/05-commercial-overrides.md but file is missing")
        else:
            actual = _sha256_file(overrides_path)
            if actual != overrides_checksum:
                issues.append("Checksum mismatch for working/05-commercial-overrides.md")

    return {"pass": len(issues) == 0, "missing": [], "issues": issues}


def validate_commercial_overrides(project_dir: Path) -> dict:
    """Validate commercial override metadata and evidence when overrides exist."""
    project_dir = Path(project_dir)
    overrides_path = project_dir / "working" / "05-commercial-overrides.md"
    if not overrides_path.exists():
        return {"pass": True, "issues": []}

    issues = []
    try:
        fm, _ = parse_file(overrides_path)
    except Exception as exc:
        return {"pass": False, "issues": [f"Unable to parse overrides file: {exc}"]}

    approved_by = fm.get("approved_by")
    valid_until = fm.get("valid_until")
    if not approved_by:
        issues.append("Commercial overrides missing approved_by")
    if not valid_until:
        issues.append("Commercial overrides missing valid_until")
    else:
        try:
            expiry = date.fromisoformat(str(valid_until))
            if expiry < date.today():
                issues.append("Commercial overrides are expired")
        except ValueError:
            issues.append("Commercial overrides valid_until must be YYYY-MM-DD")

    evidence_dir = project_dir / "evidence" / "pricing" / "commercial"
    evidence_files = [p for p in evidence_dir.iterdir()] if evidence_dir.exists() else []
    if not evidence_files:
        issues.append("Commercial overrides require evidence in evidence/pricing/commercial/")

    return {"pass": len(issues) == 0, "issues": issues}


def check_gate(
    project_dir: Path,
    stage: int,
    check_snapshot_boundary: bool = False,
    check_commercial_override_rules: bool = False,
) -> dict:
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

    issues = []
    if check_snapshot_boundary:
        snapshot_result = validate_snapshot(project_dir)
        missing.extend(snapshot_result.get("missing", []))
        issues.extend(snapshot_result.get("issues", []))

    if check_commercial_override_rules:
        override_result = validate_commercial_overrides(project_dir)
        issues.extend(override_result.get("issues", []))

    return {
        "pass": len(missing) == 0 and len(issues) == 0,
        "stage": stage,
        "missing": missing,
        "present": present,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate pipeline stage gates")
    parser.add_argument("--project", type=Path, required=True, help="Project directory")
    parser.add_argument("--stage", type=int, required=True, help="Stage number (0-7)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--check-snapshot", action="store_true", help="Validate snapshot artifacts and checksums")
    parser.add_argument(
        "--check-commercial-overrides",
        action="store_true",
        help="Validate commercial override metadata and evidence if overrides exist",
    )
    args = parser.parse_args()

    if args.stage not in STAGE_CONTRACTS:
        print(f"Error: unknown stage {args.stage}. Valid: 0-7", file=sys.stderr)
        sys.exit(2)

    result = check_gate(
        args.project,
        args.stage,
        check_snapshot_boundary=args.check_snapshot,
        check_commercial_override_rules=args.check_commercial_overrides,
    )

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
        if result.get("issues"):
            print("Issues:")
            for issue in result["issues"]:
                print(f"  - {issue}")

    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
