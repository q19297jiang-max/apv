"""Audit knowledge markdown files for completeness, freshness, and validity."""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from frontmatter import parse_file


class AuditResult(Enum):
    PASS = "PASS"
    STALE = "STALE"
    FAIL = "FAIL"


REQUIRED_FIELDS = ["type", "category", "source_url", "last_verified", "freshness_days", "captured_date"]


@dataclass
class FileAudit:
    path: Path
    status: AuditResult
    issues: list[str] = field(default_factory=list)


def audit_file(file_path: Path) -> FileAudit:
    """Audit a single knowledge markdown file."""
    file_path = Path(file_path)
    issues: list[str] = []

    try:
        fm, body = parse_file(file_path)
    except Exception as e:
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=[f"Read error: {e}"])

    # No frontmatter
    if not fm:
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=["No frontmatter found"])

    # Missing required fields
    missing = [f for f in REQUIRED_FIELDS if f not in fm]
    if missing:
        issues.append(f"Missing required fields: {', '.join(missing)}")
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=issues)

    # Body too short
    if len(body.strip()) < 10:
        issues.append("Body content is less than 10 characters")
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=issues)

    # Staleness check
    try:
        last_verified = fm["last_verified"]
        if isinstance(last_verified, str):
            last_verified_date = datetime.strptime(last_verified, "%Y-%m-%d").date()
        elif isinstance(last_verified, date):
            last_verified_date = last_verified
        else:
            last_verified_date = datetime.strptime(str(last_verified), "%Y-%m-%d").date()

        freshness_days = int(fm["freshness_days"])
        days_since = (date.today() - last_verified_date).days
        if days_since > freshness_days:
            issues.append(f"Stale: {days_since} days since verification (limit: {freshness_days})")
            return FileAudit(path=file_path, status=AuditResult.STALE, issues=issues)
    except (ValueError, TypeError) as e:
        issues.append(f"Invalid date/freshness value: {e}")
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=issues)

    return FileAudit(path=file_path, status=AuditResult.PASS, issues=[])


def audit_directory(directory: Path) -> dict:
    """Audit all markdown files in a directory."""
    directory = Path(directory)
    results = [audit_file(f) for f in sorted(directory.rglob("*.md")) if not f.name.startswith(".")]
    return {
        "total": len(results),
        "pass": sum(1 for r in results if r.status == AuditResult.PASS),
        "stale": sum(1 for r in results if r.status == AuditResult.STALE),
        "fail": sum(1 for r in results if r.status == AuditResult.FAIL),
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit knowledge files for completeness and freshness.")
    parser.add_argument("--knowledge-dir", type=Path, required=True, help="Path to knowledge directory")
    args = parser.parse_args()

    summary = audit_directory(args.knowledge_dir)

    for r in summary["results"]:
        icon = {"PASS": "✓", "STALE": "⚠", "FAIL": "✗"}[r.status.value]
        print(f"  {icon} {r.status.value:5s}  {r.path.name}")
        for issue in r.issues:
            print(f"         → {issue}")

    print(f"\nTotal: {summary['total']}  Pass: {summary['pass']}  Stale: {summary['stale']}  Fail: {summary['fail']}")

    if summary["stale"] > 0 or summary["fail"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
