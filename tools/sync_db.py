"""Knowledge Indexer — walks knowledge/ markdown files and indexes them into SQLite."""

import argparse
import hashlib
import re
from pathlib import Path

from lib.frontmatter import parse_file
from lib.db import create_schema, insert_knowledge_page


def _extract_title(body: str) -> str | None:
    m = re.search(r"^#\s+(.+)", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def _detect_domain(file_path: Path, knowledge_dir: Path, fm: dict) -> str:
    if fm.get("category"):
        return fm["category"]
    try:
        rel = file_path.relative_to(knowledge_dir)
        if len(rel.parts) > 1:
            return rel.parts[0]
    except ValueError:
        pass
    return "general"


def _should_index(md_file: Path, fm: dict) -> bool:
    name = md_file.name.lower()
    if md_file.name.startswith("."):
        return False
    if "template" in name:
        return False
    if fm.get("category") == "documentation":
        return False
    return True


def sync_knowledge(knowledge_dir: Path, db_path: Path) -> dict:
    knowledge_dir = Path(knowledge_dir)
    db_path = Path(db_path)
    conn = create_schema(db_path)
    conn.execute("DELETE FROM knowledge_pages")
    conn.commit()

    stats = {"total": 0, "indexed": 0, "warnings": 0, "errors": 0}

    for md_file in sorted(knowledge_dir.rglob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
            fm, body = {}, text
            try:
                fm, body = parse_file(md_file)
            except Exception:
                pass

            if not _should_index(md_file, fm):
                continue

            stats["total"] += 1

            if not fm:
                stats["warnings"] += 1

            rel_path = str(md_file.relative_to(knowledge_dir))
            title = _extract_title(body) or _extract_title(text) or md_file.stem
            domain = _detect_domain(md_file, knowledge_dir, fm)
            content_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

            page = {
                "path": rel_path,
                "domain": domain,
                "type": fm.get("type", "unknown"),
                "title": title,
                "source_url": fm.get("source_url"),
                "last_verified": fm.get("last_verified"),
                "freshness_days": fm.get("freshness_days", 90),
            }
            insert_knowledge_page(conn, page)
            stats["indexed"] += 1
        except Exception:
            stats["errors"] += 1

    conn.close()
    return stats


def main():
    parser = argparse.ArgumentParser(description="Index knowledge markdown files into SQLite")
    parser.add_argument("--knowledge-dir", type=Path, default=Path(__file__).parent.parent / "knowledge")
    parser.add_argument("--db-path", type=Path, default=Path(__file__).parent.parent / "apv-v2.sqlite")
    args = parser.parse_args()

    stats = sync_knowledge(args.knowledge_dir, args.db_path)
    print(f"Sync complete: {stats}")


if __name__ == "__main__":
    main()
