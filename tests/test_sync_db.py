import sys
import sqlite3
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

FIXTURES = Path(__file__).parent / "fixtures" / "knowledge"


def test_sync_db_indexes_knowledge_files(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES, knowledge_dir)
    db_path = tmp_path / "apv-v2.sqlite"

    from sync_db import sync_knowledge
    stats = sync_knowledge(knowledge_dir, db_path)

    assert stats["total"] >= 3
    assert stats["errors"] == 0

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    assert len(rows) >= 3

    pricing_rows = conn.execute("SELECT * FROM knowledge_pages WHERE domain='pricing'").fetchall()
    assert len(pricing_rows) >= 1
    conn.close()


def test_sync_db_skips_non_markdown(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "readme.txt").write_text("not markdown")
    (knowledge_dir / "test.md").write_text("---\ntype: concept\ncategory: test\n---\n# Test")

    db_path = tmp_path / "test.sqlite"
    from sync_db import sync_knowledge
    stats = sync_knowledge(knowledge_dir, db_path)
    assert stats["total"] == 1


def test_sync_db_reports_missing_frontmatter(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "no-fm.md").write_text("# No Frontmatter\nJust content")

    db_path = tmp_path / "test.sqlite"
    from sync_db import sync_knowledge
    stats = sync_knowledge(knowledge_dir, db_path)
    assert stats["warnings"] >= 1


def test_sync_db_idempotent(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES, knowledge_dir)
    db_path = tmp_path / "test.sqlite"

    from sync_db import sync_knowledge
    sync_knowledge(knowledge_dir, db_path)
    stats = sync_knowledge(knowledge_dir, db_path)

    conn = sqlite3.connect(str(db_path))
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    paths = [r[0] for r in rows]
    assert len(paths) == len(set(paths))
    conn.close()
