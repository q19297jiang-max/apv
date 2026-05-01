#!/usr/bin/env python3
"""migrate_v1.py — Migrate V1 APV knowledge files to V2 schema.

Walks V1 knowledge files, enriches frontmatter to V2 schema, and writes
to the V2 directory structure.
"""
import argparse
from pathlib import Path

from lib.frontmatter import parse_file, parse_frontmatter

# Freshness days by category
_FRESHNESS = {
    "pricing": 30,
    "infrastructure": 90,
    "patterns": 0,
    "commercial": 0,
}
_DEFAULT_FRESHNESS = 365


def _serialize_frontmatter(fm: dict) -> str:
    """Serialize a frontmatter dict to YAML block string."""
    lines = ["---"]
    for key, val in fm.items():
        if isinstance(val, list):
            items = ", ".join(
                f'"{v}"' if isinstance(v, str) and (" " in v or ":" in v or "/" in v or "[" in v) else str(v)
                for v in val
            )
            lines.append(f"{key}: [{items}]")
        elif isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif isinstance(val, (int, float)):
            lines.append(f"{key}: {val}")
        elif val is None:
            lines.append(f"{key}: null")
        else:
            s = str(val)
            if any(c in s for c in (':', '"', '[', ']', '#')):
                lines.append(f'{key}: "{s}"')
            else:
                lines.append(f"{key}: {s}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def enrich_frontmatter(fm: dict) -> dict:
    """Enrich V1 frontmatter to V2 schema.

    - Normalizes type: apv-knowledge → source
    - Adds freshness_days based on category
    - Adds last_verified defaulting to captured_date
    """
    result = dict(fm)

    # Normalize type
    if result.get("type") == "apv-knowledge":
        result["type"] = "source"

    # Add freshness_days
    category = result.get("category", "")
    result["freshness_days"] = _FRESHNESS.get(category, _DEFAULT_FRESHNESS)

    # Add last_verified
    if "last_verified" not in result:
        result["last_verified"] = result.get("captured_date")

    return result


def map_v1_path_to_v2(v1_path: Path) -> Path | None:
    """Map a V1 path to V2 relative path. Returns None if file should be skipped."""
    name = v1_path.name

    # Skip templates and non-markdown
    if name.endswith(".template.md"):
        return None
    if v1_path.suffix != ".md":
        return None

    # Extract from knowledge/ onwards
    parts = v1_path.parts
    try:
        idx = parts.index("knowledge")
    except ValueError:
        return None

    return Path(*parts[idx:])


def migrate_file(v1_path: Path, v2_base: Path, dry_run: bool = False) -> dict:
    """Migrate a single V1 file to V2. Returns status dict."""
    v2_rel = map_v1_path_to_v2(v1_path)
    if v2_rel is None:
        return {"path": str(v1_path), "status": "skipped", "reason": "filtered"}

    fm, body = parse_file(v1_path)
    enriched = enrich_frontmatter(fm)
    v2_path = v2_base / v2_rel

    if dry_run:
        return {"path": str(v1_path), "v2_path": str(v2_path), "status": "dry_run"}

    v2_path.parent.mkdir(parents=True, exist_ok=True)
    content = _serialize_frontmatter(enriched) + body
    v2_path.write_text(content, encoding="utf-8")

    return {"path": str(v1_path), "v2_path": str(v2_path), "status": "migrated"}


def migrate_all(v1_knowledge_dir: Path, v2_base: Path, dry_run: bool = False) -> dict:
    """Migrate all V1 knowledge files to V2. Returns summary dict."""
    v1_knowledge_dir = Path(v1_knowledge_dir)
    v2_base = Path(v2_base)
    results = []

    for f in sorted(v1_knowledge_dir.rglob("*")):
        if not f.is_file():
            continue
        # Skip backups directory
        if "backups" in f.parts:
            continue
        results.append(migrate_file(f, v2_base, dry_run))

    migrated = sum(1 for r in results if r["status"] == "migrated")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    dry = sum(1 for r in results if r["status"] == "dry_run")

    return {
        "total": len(results),
        "migrated": migrated,
        "skipped": skipped,
        "dry_run": dry,
        "files": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Migrate V1 APV knowledge to V2")
    parser.add_argument("--v1-dir", required=True, help="V1 knowledge directory")
    parser.add_argument("--v2-dir", required=True, help="V2 output base directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    summary = migrate_all(Path(args.v1_dir), Path(args.v2_dir), args.dry_run)
    print(f"Total: {summary['total']}, Migrated: {summary['migrated']}, "
          f"Skipped: {summary['skipped']}, Dry-run: {summary['dry_run']}")
    for f in summary["files"]:
        print(f"  {f['status']:10s} {f['path']}")


if __name__ == "__main__":
    main()
