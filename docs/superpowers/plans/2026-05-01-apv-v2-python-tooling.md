# APV V2 Python Tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the 4 foundational Python tools that the APV V2 pipeline depends on — `sync-db.py`, `validate-gates.py`, `normalize.py`, and `knowledge-audit.py` — plus the SQLite schema and test fixtures.

**Architecture:** Each tool is a standalone CLI script in `wiki/apv-v2/tools/`. Tools read markdown files with YAML frontmatter, emit structured output to stdout (human-readable) and write file artifacts (machine-readable). The SQLite database (`apv-v2.sqlite`) is a derived index — always regenerable from knowledge markdown files. Zero external dependencies beyond Python stdlib (`sqlite3`, `json`, `argparse`, `pathlib`, `re`).

**Tech Stack:** Python 3.10+ (stdlib only), SQLite3, YAML frontmatter parsing (hand-rolled — no PyYAML dependency per zero-dep policy)

**V1 Reuse Note:** V1 has `pricing-format-validator.py`, `pricing-fetcher-generic.py`, and `verify-source-urls.py` in `wiki/apv/`. Review these for patterns but do NOT import them — V2 tools are standalone with different contracts.

---

## File Structure

```
wiki/apv-v2/
├── tools/
│   ├── lib/
│   │   ├── __init__.py              # Package init
│   │   ├── frontmatter.py           # YAML frontmatter parser (zero-dep)
│   │   └── db.py                    # SQLite schema + connection helpers
│   ├── sync-db.py                   # Parse knowledge/*.md → SQLite
│   ├── validate-gates.py            # Check required artifacts exist per stage
│   ├── normalize.py                 # Convert raw inputs to markdown
│   └── knowledge-audit.py           # Audit knowledge files (PASS/STALE/FAIL)
├── tests/
│   ├── conftest.py                  # Shared fixtures
│   ├── test_frontmatter.py          # Frontmatter parser tests
│   ├── test_sync_db.py              # sync-db tests
│   ├── test_validate_gates.py       # validate-gates tests
│   ├── test_normalize.py            # normalize tests
│   └── test_knowledge_audit.py      # knowledge-audit tests
│   └── fixtures/
│       ├── knowledge/               # Sample knowledge .md files
│       └── raw/                     # Sample raw input files
└── apv-v2.sqlite                    # (gitignored) derived index
```

---

### Task 1: Shared Library — Frontmatter Parser

**Files:**
- Create: `wiki/apv-v2/tools/lib/__init__.py`
- Create: `wiki/apv-v2/tools/lib/frontmatter.py`
- Create: `wiki/apv-v2/tests/test_frontmatter.py`
- Create: `wiki/apv-v2/tests/fixtures/knowledge/sample-entity.md`

- [ ] **Step 1: Create test fixture — sample knowledge file**

```markdown
---
type: entity
category: infrastructure
source_url: "https://aws.amazon.com/ec2/"
captured_date: 2026-03-15
last_verified: 2026-04-01
freshness_days: 90
tags: [aws, compute, ec2]
---

# Amazon EC2

Elastic Compute Cloud provides resizable compute capacity.

## Key Facts
- On-demand, reserved, and spot pricing models
- Multiple instance families (general, compute, memory optimized)
```

Write this to `wiki/apv-v2/tests/fixtures/knowledge/sample-entity.md`.

- [ ] **Step 2: Write failing tests for frontmatter parser**

```python
# wiki/apv-v2/tests/test_frontmatter.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from lib.frontmatter import parse_frontmatter, parse_file


def test_parse_frontmatter_basic():
    text = "---\ntype: entity\ntags: [a, b]\n---\n# Title\nBody"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "entity"
    assert fm["tags"] == ["a", "b"]
    assert body.strip() == "# Title\nBody"


def test_parse_frontmatter_no_frontmatter():
    text = "# Just a title\nNo frontmatter here"
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body == text


def test_parse_frontmatter_empty_values():
    text = "---\ntype: concept\nsource_url:\ntags: []\n---\nBody"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "concept"
    assert fm["source_url"] is None
    assert fm["tags"] == []


def test_parse_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("---\ntype: source\ncreated: 2026-01-01\n---\n# Test")
    fm, body = parse_file(f)
    assert fm["type"] == "source"
    assert fm["created"] == "2026-01-01"


def test_parse_frontmatter_quoted_strings():
    text = '---\nsource_url: "https://example.com"\ntitle: "A \\"quoted\\" title"\n---\nBody'
    fm, body = parse_frontmatter(text)
    assert fm["source_url"] == "https://example.com"


def test_parse_frontmatter_multiline_ignored():
    """Frontmatter parser handles simple key: value only — no multiline YAML blocks."""
    text = "---\ntype: entity\ncategory: pricing\n---\n# Content"
    fm, body = parse_frontmatter(text)
    assert fm["type"] == "entity"
    assert fm["category"] == "pricing"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_frontmatter.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'lib.frontmatter'`

- [ ] **Step 4: Implement frontmatter parser**

```python
# wiki/apv-v2/tools/lib/__init__.py
"""APV V2 shared tool library."""

# wiki/apv-v2/tools/lib/frontmatter.py
"""Zero-dependency YAML frontmatter parser.

Handles simple key: value pairs, arrays in [bracket] syntax,
quoted strings, dates, numbers, and booleans.
Does NOT handle nested YAML, multiline values, or anchors.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _parse_value(raw: str) -> Any:
    """Parse a single YAML value string into a Python type."""
    raw = raw.strip()
    if not raw or raw == "~" or raw == "null":
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False

    # Quoted string
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1].replace('\\"', '"').replace("\\'", "'")

    # Bracket array: [a, b, c]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_parse_value(item) for item in _split_array(inner)]

    # Integer
    try:
        return int(raw)
    except ValueError:
        pass

    # Float
    try:
        return float(raw)
    except ValueError:
        pass

    # Date-like strings (YYYY-MM-DD) — keep as string
    return raw


def _split_array(s: str) -> list[str]:
    """Split comma-separated array items, respecting quotes."""
    items = []
    current = []
    in_quote = None
    for ch in s:
        if ch in ('"', "'") and in_quote is None:
            in_quote = ch
            current.append(ch)
        elif ch == in_quote:
            in_quote = None
            current.append(ch)
        elif ch == "," and in_quote is None:
            items.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        items.append("".join(current).strip())
    return items


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown text.

    Returns (frontmatter_dict, body_text).
    If no frontmatter found, returns ({}, original_text).
    """
    if not text.startswith("---"):
        return {}, text

    # Find closing ---
    end_match = re.search(r"\n---\s*\n", text[3:])
    if end_match is None:
        # Try end of string
        end_match = re.search(r"\n---\s*$", text[3:])
        if end_match is None:
            return {}, text

    fm_text = text[4 : 3 + end_match.start()]
    body = text[3 + end_match.end() :]

    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        colon_pos = line.find(":")
        if colon_pos == -1:
            continue
        key = line[:colon_pos].strip()
        value = line[colon_pos + 1 :].strip()
        result[key] = _parse_value(value) if value else None

    return result, body


def parse_file(path: Path | str) -> tuple[dict[str, Any], str]:
    """Read a file and parse its frontmatter."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return parse_frontmatter(text)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_frontmatter.py -v`
Expected: All 6 tests PASS

- [ ] **Step 6: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/lib/__init__.py tools/lib/frontmatter.py tests/test_frontmatter.py tests/fixtures/knowledge/sample-entity.md
git commit -m "feat(apv-v2): add zero-dep YAML frontmatter parser with tests"
```

---

### Task 2: Shared Library — SQLite Schema & DB Helpers

**Files:**
- Create: `wiki/apv-v2/tools/lib/db.py`
- Create: `wiki/apv-v2/tests/test_db.py`

- [ ] **Step 1: Write failing tests for DB module**

```python
# wiki/apv-v2/tests/test_db.py
import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from lib.db import create_schema, insert_knowledge_page, get_stale_pages, insert_pricing


def test_create_schema(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert "knowledge_pages" in tables
    assert "pricing" in tables
    assert "compliance" in tables
    assert "infrastructure" in tables
    assert "knowledge_gaps" in tables
    conn.close()


def test_insert_knowledge_page(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    insert_knowledge_page(conn, {
        "path": "knowledge/pricing/aws.md",
        "domain": "pricing",
        "type": "source",
        "source_url": "https://aws.amazon.com/ec2/pricing/",
        "freshness_days": 30,
        "last_verified": "2026-04-01",
        "title": "AWS EC2 Pricing",
    })
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    assert len(rows) == 1
    conn.close()


def test_stale_knowledge_detection(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    # Insert a page verified 100 days ago with 30-day freshness
    insert_knowledge_page(conn, {
        "path": "knowledge/pricing/old.md",
        "domain": "pricing",
        "type": "source",
        "source_url": "https://example.com",
        "freshness_days": 30,
        "last_verified": "2026-01-01",
        "title": "Old Pricing",
    })
    stale = get_stale_pages(conn)
    assert len(stale) == 1
    assert stale[0]["path"] == "knowledge/pricing/old.md"
    conn.close()


def test_insert_pricing(tmp_path):
    db_path = tmp_path / "test.sqlite"
    conn = create_schema(db_path)
    insert_pricing(conn, {
        "provider": "aws",
        "region": "ap-southeast-1",
        "service": "EC2",
        "instance_type": "m6i.xlarge",
        "hourly_price": 0.192,
        "monthly_price": 140.16,
        "source_url": "https://aws.amazon.com/ec2/pricing/",
        "verified_date": "2026-04-01",
    })
    rows = conn.execute("SELECT * FROM pricing WHERE provider='aws'").fetchall()
    assert len(rows) == 1
    conn.close()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_db.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'lib.db'`

- [ ] **Step 3: Implement DB module**

```python
# wiki/apv-v2/tools/lib/db.py
"""SQLite schema and helpers for APV V2 knowledge index.

The database is a derived artifact — always regenerable from knowledge/*.md.
5 tables + 1 view per the system design spec.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS knowledge_pages (
    path TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT,
    source_url TEXT,
    captured_date TEXT,
    last_verified TEXT,
    freshness_days INTEGER DEFAULT 365,
    tags TEXT,  -- JSON array as string
    content_hash TEXT
);

CREATE VIEW IF NOT EXISTS stale_knowledge AS
SELECT *, julianday('now') - julianday(last_verified) AS days_since_verified
FROM knowledge_pages
WHERE last_verified IS NOT NULL
  AND julianday('now') - julianday(last_verified) > freshness_days;

CREATE TABLE IF NOT EXISTS pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    region TEXT NOT NULL,
    service TEXT NOT NULL,
    instance_type TEXT,
    hourly_price REAL,
    monthly_price REAL,
    pricing_model TEXT DEFAULT 'on-demand',
    source_url TEXT,
    verified_date TEXT,
    UNIQUE(provider, region, service, instance_type, pricing_model)
);

CREATE TABLE IF NOT EXISTS compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    framework TEXT NOT NULL,
    country TEXT,
    requirement_id TEXT,
    title TEXT NOT NULL,
    summary TEXT,
    source_url TEXT,
    UNIQUE(framework, country, requirement_id)
);

CREATE TABLE IF NOT EXISTS infrastructure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    service TEXT NOT NULL,
    category TEXT,
    features TEXT,  -- JSON array as string
    regions TEXT,   -- JSON array as string
    source_url TEXT,
    UNIQUE(provider, service)
);

CREATE TABLE IF NOT EXISTS knowledge_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT,
    domain TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT DEFAULT 'LOW',
    resolved INTEGER DEFAULT 0,
    created_date TEXT,
    resolved_date TEXT
);
"""


def create_schema(db_path: Path | str) -> sqlite3.Connection:
    """Create database with full schema. Returns open connection."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    return conn


def insert_knowledge_page(conn: sqlite3.Connection, page: dict[str, Any]) -> None:
    """Insert or replace a knowledge page record."""
    import json
    tags = json.dumps(page.get("tags", [])) if isinstance(page.get("tags"), list) else page.get("tags")
    conn.execute(
        """INSERT OR REPLACE INTO knowledge_pages
           (path, domain, type, title, source_url, captured_date,
            last_verified, freshness_days, tags, content_hash)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            page["path"],
            page["domain"],
            page["type"],
            page.get("title"),
            page.get("source_url"),
            page.get("captured_date"),
            page.get("last_verified"),
            page.get("freshness_days", 365),
            tags,
            page.get("content_hash"),
        ),
    )
    conn.commit()


def get_stale_pages(conn: sqlite3.Connection) -> list[dict]:
    """Return all knowledge pages past their freshness threshold."""
    rows = conn.execute("SELECT * FROM stale_knowledge").fetchall()
    return [dict(row) for row in rows]


def insert_pricing(conn: sqlite3.Connection, entry: dict[str, Any]) -> None:
    """Insert or replace a pricing record."""
    conn.execute(
        """INSERT OR REPLACE INTO pricing
           (provider, region, service, instance_type, hourly_price,
            monthly_price, pricing_model, source_url, verified_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            entry["provider"],
            entry["region"],
            entry["service"],
            entry.get("instance_type"),
            entry.get("hourly_price"),
            entry.get("monthly_price"),
            entry.get("pricing_model", "on-demand"),
            entry.get("source_url"),
            entry.get("verified_date"),
        ),
    )
    conn.commit()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_db.py -v`
Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/lib/db.py tests/test_db.py
git commit -m "feat(apv-v2): add SQLite schema and DB helpers with tests"
```

---

### Task 3: sync-db.py — Knowledge Indexer

**Files:**
- Create: `wiki/apv-v2/tools/sync-db.py`
- Create: `wiki/apv-v2/tests/test_sync_db.py`
- Create: `wiki/apv-v2/tests/fixtures/knowledge/pricing/aws-ec2.md`
- Create: `wiki/apv-v2/tests/fixtures/knowledge/compliance/pci-dss-req1.md`

- [ ] **Step 1: Create test fixtures**

```markdown
# wiki/apv-v2/tests/fixtures/knowledge/pricing/aws-ec2.md
---
type: source
category: pricing
source_url: "https://aws.amazon.com/ec2/pricing/"
captured_date: 2026-03-15
last_verified: 2026-04-01
freshness_days: 30
tags: [aws, ec2, pricing]
---

# AWS EC2 Pricing — Singapore (ap-southeast-1)

## On-Demand Pricing

| Instance | vCPU | RAM | Hourly | Monthly |
|----------|------|-----|--------|---------|
| m6i.large | 2 | 8 GiB | $0.096 | $70.08 |
| m6i.xlarge | 4 | 16 GiB | $0.192 | $140.16 |
```

```markdown
# wiki/apv-v2/tests/fixtures/knowledge/compliance/pci-dss-req1.md
---
type: source
category: compliance
source_url: "https://www.pcisecuritystandards.org/document_library/"
captured_date: 2026-01-10
last_verified: 2026-01-10
freshness_days: 365
tags: [pci-dss, compliance, network-security]
---

# PCI-DSS v4.0 — Requirement 1

Install and Maintain Network Security Controls.

## Key Controls
- 1.1: Processes and mechanisms for network security controls
- 1.2: Network security controls configured and maintained
```

- [ ] **Step 2: Write failing tests**

```python
# wiki/apv-v2/tests/test_sync_db.py
import sys
import sqlite3
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

FIXTURES = Path(__file__).parent / "fixtures" / "knowledge"


def test_sync_db_indexes_knowledge_files(tmp_path):
    """sync-db should parse all .md files in knowledge/ and insert into SQLite."""
    # Copy fixtures to tmp
    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES, knowledge_dir)

    db_path = tmp_path / "apv-v2.sqlite"

    from sync_db import sync_knowledge

    stats = sync_knowledge(knowledge_dir, db_path)

    assert stats["total"] >= 3  # sample-entity + aws-ec2 + pci-dss-req1
    assert stats["errors"] == 0

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    assert len(rows) >= 3

    # Check domain detection from path
    pricing_rows = conn.execute(
        "SELECT * FROM knowledge_pages WHERE domain='pricing'"
    ).fetchall()
    assert len(pricing_rows) >= 1

    conn.close()


def test_sync_db_skips_non_markdown(tmp_path):
    """sync-db should ignore non-.md files."""
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "readme.txt").write_text("not markdown")
    (knowledge_dir / "test.md").write_text(
        "---\ntype: concept\ncategory: test\n---\n# Test"
    )

    db_path = tmp_path / "test.sqlite"

    from sync_db import sync_knowledge

    stats = sync_knowledge(knowledge_dir, db_path)
    assert stats["total"] == 1


def test_sync_db_reports_missing_frontmatter(tmp_path):
    """sync-db should count files without frontmatter as warnings."""
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "no-fm.md").write_text("# No Frontmatter\nJust content")

    db_path = tmp_path / "test.sqlite"

    from sync_db import sync_knowledge

    stats = sync_knowledge(knowledge_dir, db_path)
    assert stats["warnings"] >= 1


def test_sync_db_idempotent(tmp_path):
    """Running sync-db twice should produce the same result."""
    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES, knowledge_dir)
    db_path = tmp_path / "test.sqlite"

    from sync_db import sync_knowledge

    sync_knowledge(knowledge_dir, db_path)
    stats = sync_knowledge(knowledge_dir, db_path)

    conn = sqlite3.connect(str(db_path))
    rows = conn.execute("SELECT * FROM knowledge_pages").fetchall()
    # Should not have duplicates
    paths = [r[0] for r in rows]
    assert len(paths) == len(set(paths))
    conn.close()
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_sync_db.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'sync_db'`

- [ ] **Step 4: Implement sync-db.py**

```python
#!/usr/bin/env python3
# wiki/apv-v2/tools/sync-db.py
"""Parse knowledge/*.md files and index into SQLite.

Usage:
    python3 sync-db.py [--knowledge-dir PATH] [--db-path PATH]

Defaults:
    --knowledge-dir: ../knowledge/
    --db-path: ../apv-v2.sqlite
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

# Allow running as script or import
sys.path.insert(0, str(Path(__file__).parent))

from lib.frontmatter import parse_file
from lib.db import create_schema, insert_knowledge_page


def _detect_domain(path: Path, knowledge_root: Path) -> str:
    """Detect knowledge domain from file path relative to knowledge root."""
    try:
        rel = path.relative_to(knowledge_root)
        parts = rel.parts
        if len(parts) > 1:
            return parts[0]  # First subdirectory = domain
        return "general"
    except ValueError:
        return "general"


def _extract_title(body: str) -> str | None:
    """Extract first H1 heading from markdown body."""
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else None


def _content_hash(text: str) -> str:
    """SHA-256 hash of file content for change detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def sync_knowledge(
    knowledge_dir: Path, db_path: Path
) -> dict[str, int]:
    """Index all .md files under knowledge_dir into SQLite.

    Returns stats dict with keys: total, indexed, warnings, errors.
    """
    conn = create_schema(db_path)
    stats = {"total": 0, "indexed": 0, "warnings": 0, "errors": 0}

    md_files = sorted(knowledge_dir.rglob("*.md"))

    for md_file in md_files:
        stats["total"] += 1
        try:
            text = md_file.read_text(encoding="utf-8")
            fm, body = parse_file(md_file)

            if not fm:
                stats["warnings"] += 1
                print(f"  WARN: No frontmatter in {md_file.name}", file=sys.stderr)
                # Still index it with minimal info
                rel_path = str(md_file.relative_to(knowledge_dir))
                insert_knowledge_page(conn, {
                    "path": rel_path,
                    "domain": _detect_domain(md_file, knowledge_dir),
                    "type": "unknown",
                    "title": _extract_title(body),
                    "content_hash": _content_hash(text),
                })
                stats["indexed"] += 1
                continue

            rel_path = str(md_file.relative_to(knowledge_dir))
            domain = fm.get("category", _detect_domain(md_file, knowledge_dir))

            insert_knowledge_page(conn, {
                "path": rel_path,
                "domain": domain,
                "type": fm.get("type", "unknown"),
                "title": _extract_title(body) or fm.get("title"),
                "source_url": fm.get("source_url"),
                "captured_date": str(fm["captured_date"]) if fm.get("captured_date") else None,
                "last_verified": str(fm["last_verified"]) if fm.get("last_verified") else None,
                "freshness_days": fm.get("freshness_days", 365),
                "tags": str(fm.get("tags", [])),
                "content_hash": _content_hash(text),
            })
            stats["indexed"] += 1

        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR: {md_file.name}: {e}", file=sys.stderr)

    conn.close()
    return stats


def main():
    parser = argparse.ArgumentParser(description="Sync knowledge markdown to SQLite index")
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path(__file__).parent.parent / "knowledge",
        help="Root directory of knowledge markdown files",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path(__file__).parent.parent / "apv-v2.sqlite",
        help="Output SQLite database path",
    )
    args = parser.parse_args()

    print(f"Syncing {args.knowledge_dir} → {args.db_path}")
    stats = sync_knowledge(args.knowledge_dir, args.db_path)
    print(f"Done: {stats['indexed']}/{stats['total']} indexed, "
          f"{stats['warnings']} warnings, {stats['errors']} errors")

    sys.exit(1 if stats["errors"] > 0 else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_sync_db.py -v`
Expected: All 4 tests PASS

- [ ] **Step 6: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/sync-db.py tests/test_sync_db.py tests/fixtures/knowledge/pricing/aws-ec2.md tests/fixtures/knowledge/compliance/pci-dss-req1.md
git commit -m "feat(apv-v2): add sync-db.py knowledge indexer with tests"
```

---

### Task 4: validate-gates.py — Stage Gate Checker

**Files:**
- Create: `wiki/apv-v2/tools/validate-gates.py`
- Create: `wiki/apv-v2/tests/test_validate_gates.py`

- [ ] **Step 1: Write failing tests**

```python
# wiki/apv-v2/tests/test_validate_gates.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from validate_gates import STAGE_CONTRACTS, check_gate


def test_stage_contracts_defined():
    """All 8 stages must have contracts defined."""
    assert len(STAGE_CONTRACTS) == 8
    for stage_num in range(8):
        assert stage_num in STAGE_CONTRACTS, f"Stage {stage_num} missing"


def test_check_gate_pass(tmp_path):
    """Gate check passes when all required files exist."""
    # Stage 1 requires: input/normalized/rfp.md, input/normalized/requirements-summary.md
    project = tmp_path / "project"
    (project / "input" / "normalized").mkdir(parents=True)
    (project / "input" / "normalized" / "rfp.md").write_text("# RFP")
    (project / "input" / "normalized" / "requirements-summary.md").write_text("# Reqs")

    result = check_gate(project, 1)
    assert result["pass"] is True
    assert result["missing"] == []


def test_check_gate_fail(tmp_path):
    """Gate check fails when required files are missing."""
    project = tmp_path / "project"
    project.mkdir()

    result = check_gate(project, 1)
    assert result["pass"] is False
    assert len(result["missing"]) > 0


def test_check_gate_stage_2_requires_stage_1_output(tmp_path):
    """Stage 2 requires outputs/01-brainstorm.md from Stage 1."""
    project = tmp_path / "project"
    (project / "input" / "normalized").mkdir(parents=True)
    (project / "outputs").mkdir()
    # Missing outputs/01-brainstorm.md
    (project / "input" / "normalized" / "requirements-summary.md").write_text("# Reqs")

    result = check_gate(project, 2)
    assert result["pass"] is False
    assert "outputs/01-brainstorm.md" in result["missing"]


def test_check_gate_stage_0_always_passes(tmp_path):
    """Stage 0 (ingestion) has no upstream requirements."""
    project = tmp_path / "project"
    project.mkdir()

    result = check_gate(project, 0)
    assert result["pass"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_validate_gates.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement validate-gates.py**

```python
#!/usr/bin/env python3
# wiki/apv-v2/tools/validate-gates.py
"""Validate that required upstream artifacts exist before a stage runs.

Usage:
    python3 validate-gates.py --project PATH --stage N

Exit codes: 0 = pass, 1 = fail (missing artifacts listed on stderr)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Stage contracts: stage_number → list of required input paths (relative to project root)
STAGE_CONTRACTS: dict[int, list[str]] = {
    0: [],  # Ingestion: needs raw/* but we don't enforce specific filenames
    1: [
        "input/normalized/rfp.md",
        "input/normalized/requirements-summary.md",
    ],
    2: [
        "outputs/01-brainstorm.md",
        "input/normalized/requirements-summary.md",
    ],
    3: [
        "outputs/01-brainstorm.md",
        "outputs/02-compliance.md",
    ],
    4: [
        "outputs/03-architecture.md",
        "input/normalized/volume-summary.md",
    ],
    5: [
        "outputs/03-architecture.md",
        "outputs/04-sizing.md",
    ],
    6: [
        "outputs/01-brainstorm.md",
        "outputs/02-compliance.md",
        "outputs/03-architecture.md",
        "outputs/04-sizing.md",
        "outputs/05-pricing.md",
    ],
    7: [
        "outputs/06-response.md",
    ],
}


def check_gate(project_dir: Path, stage: int) -> dict:
    """Check if all required artifacts exist for a given stage.

    Returns:
        {"pass": bool, "stage": int, "missing": [str], "present": [str]}
    """
    required = STAGE_CONTRACTS.get(stage, [])
    missing = []
    present = []

    for artifact in required:
        artifact_path = project_dir / artifact
        if artifact_path.exists() and artifact_path.stat().st_size > 0:
            present.append(artifact)
        else:
            missing.append(artifact)

    return {
        "pass": len(missing) == 0,
        "stage": stage,
        "missing": missing,
        "present": present,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate stage gate requirements")
    parser.add_argument("--project", type=Path, required=True, help="Project directory path")
    parser.add_argument("--stage", type=int, required=True, help="Stage number (0-7)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.stage not in STAGE_CONTRACTS:
        print(f"ERROR: Unknown stage {args.stage}. Valid: 0-7", file=sys.stderr)
        sys.exit(2)

    result = check_gate(args.project, args.stage)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["pass"]:
            print(f"✓ Stage {args.stage} gate PASSED — all {len(result['present'])} artifacts present")
        else:
            print(f"✗ Stage {args.stage} gate FAILED — {len(result['missing'])} artifacts missing:")
            for m in result["missing"]:
                print(f"  - {m}")

    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_validate_gates.py -v`
Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/validate-gates.py tests/test_validate_gates.py
git commit -m "feat(apv-v2): add validate-gates.py stage gate checker with tests"
```

---

### Task 5: normalize.py — Raw Input Converter

**Files:**
- Create: `wiki/apv-v2/tools/normalize.py`
- Create: `wiki/apv-v2/tests/test_normalize.py`
- Create: `wiki/apv-v2/tests/fixtures/raw/sample-rfp.txt`

- [ ] **Step 1: Create test fixture — sample raw input**

```text
# wiki/apv-v2/tests/fixtures/raw/sample-rfp.txt
REQUEST FOR PROPOSAL
Payment Gateway Infrastructure
Client: ACME Payments Pte Ltd
Date: 2026-04-15

1. BACKGROUND
ACME Payments requires a cloud-based payment gateway supporting
Visa, Mastercard, and local payment methods in Singapore.

2. REQUIREMENTS
- 500 TPS peak processing capacity
- PCI-DSS v4.0 Level 1 compliance
- 99.99% availability SLA
- Multi-AZ deployment in AWS Singapore

3. VOLUME DATA
- Monthly transactions: 50,000,000
- Average transaction value: SGD 85
- Peak multiplier: 3x during festive periods
```

- [ ] **Step 2: Write failing tests**

```python
# wiki/apv-v2/tests/test_normalize.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from normalize import normalize_raw_inputs, detect_input_type

FIXTURES = Path(__file__).parent / "fixtures" / "raw"


def test_detect_input_type_text():
    assert detect_input_type(FIXTURES / "sample-rfp.txt") == "text"


def test_detect_input_type_markdown():
    """A .md file should be detected as markdown."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write("# RFP\nSome content")
        f.flush()
        assert detect_input_type(Path(f.name)) == "markdown"


def test_normalize_creates_required_outputs(tmp_path):
    """normalize should create the 5 required normalized files."""
    raw_dir = tmp_path / "input" / "raw"
    raw_dir.mkdir(parents=True)
    # Copy fixture
    import shutil
    shutil.copy(FIXTURES / "sample-rfp.txt", raw_dir / "rfp.txt")

    output_dir = tmp_path / "input" / "normalized"

    normalize_raw_inputs(raw_dir, output_dir)

    # At minimum, rfp.md must be created
    assert (output_dir / "rfp.md").exists()
    content = (output_dir / "rfp.md").read_text()
    assert "Payment Gateway" in content


def test_normalize_text_to_markdown(tmp_path):
    """Plain text files should be converted to valid markdown."""
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "input.txt").write_text(
        "TITLE: Test RFP\n\n1. First Section\nContent here\n\n2. Second Section\nMore content"
    )

    output_dir = tmp_path / "normalized"

    normalize_raw_inputs(raw_dir, output_dir)

    rfp = (output_dir / "rfp.md").read_text()
    assert len(rfp) > 0


def test_normalize_preserves_markdown(tmp_path):
    """Markdown files should be copied with minimal transformation."""
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    original = "# RFP Document\n\n## Requirements\n- Item 1\n- Item 2\n"
    (raw_dir / "rfp.md").write_text(original)

    output_dir = tmp_path / "normalized"

    normalize_raw_inputs(raw_dir, output_dir)

    result = (output_dir / "rfp.md").read_text()
    assert "# RFP Document" in result
    assert "Item 1" in result
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_normalize.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 4: Implement normalize.py**

```python
#!/usr/bin/env python3
# wiki/apv-v2/tools/normalize.py
"""Convert raw RFP inputs to normalized markdown files.

Usage:
    python3 normalize.py --raw-dir PATH --output-dir PATH

Reads all files in raw-dir, converts to markdown, and writes
the 5 standard normalized files:
  - rfp.md              (main RFP document)
  - questionnaire.md    (if questionnaire found)
  - card-volume.md      (if volume data found)
  - requirements-summary.md (extracted requirements)
  - volume-summary.md   (extracted volume/sizing data)

Supports: .txt, .md, .csv (basic)
Future: .docx, .xlsx, .pdf (Phase 2 — requires external tools)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def detect_input_type(file_path: Path) -> str:
    """Detect input file type from extension."""
    ext = file_path.suffix.lower()
    type_map = {
        ".md": "markdown",
        ".markdown": "markdown",
        ".txt": "text",
        ".csv": "csv",
        ".tsv": "csv",
    }
    return type_map.get(ext, "text")


def _text_to_markdown(text: str) -> str:
    """Convert plain text to markdown with basic structure detection."""
    lines = text.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()

        # Detect numbered section headers: "1. SECTION" or "1. Section Name"
        section_match = re.match(r"^(\d+)\.\s+([A-Z][A-Z\s]+)$", stripped)
        if section_match:
            result.append(f"\n## {section_match.group(2).title()}\n")
            continue

        # Detect ALL-CAPS title lines
        if stripped and stripped == stripped.upper() and len(stripped) > 3 and not stripped.startswith("-"):
            result.append(f"\n# {stripped.title()}\n")
            continue

        # Detect key: value lines
        kv_match = re.match(r"^([A-Za-z\s]+):\s+(.+)$", stripped)
        if kv_match and len(kv_match.group(1)) < 30:
            result.append(f"- **{kv_match.group(1).strip()}**: {kv_match.group(2)}")
            continue

        result.append(line)

    return "\n".join(result)


def _extract_requirements(content: str) -> str:
    """Extract requirements section from normalized content."""
    lines = content.split("\n")
    requirements = []
    in_req_section = False

    for line in lines:
        if re.match(r"^##?\s+.*[Rr]equirement", line):
            in_req_section = True
            requirements.append(line)
            continue
        if in_req_section:
            if re.match(r"^##?\s+", line) and "requirement" not in line.lower():
                in_req_section = False
                continue
            requirements.append(line)

    if requirements:
        return "\n".join(requirements)

    # Fallback: extract bullet points with requirement-like keywords
    req_lines = [l for l in lines if re.search(r"(compliance|SLA|availability|capacity|TPS|PCI)", l)]
    if req_lines:
        return "# Requirements Summary\n\n" + "\n".join(f"- {l.strip('- ')}" for l in req_lines)

    return "# Requirements Summary\n\nNo structured requirements detected. Review rfp.md manually.\n"


def _extract_volumes(content: str) -> str:
    """Extract volume/sizing data from normalized content."""
    lines = content.split("\n")
    volume_lines = []

    for line in lines:
        if re.search(r"(TPS|transaction|volume|peak|monthly|daily|capacity)", line, re.IGNORECASE):
            volume_lines.append(line.strip())

    if volume_lines:
        return "# Volume Summary\n\n" + "\n".join(f"- {l.strip('- ')}" for l in volume_lines)

    return "# Volume Summary\n\nNo volume data detected. Review rfp.md manually.\n"


def normalize_raw_inputs(raw_dir: Path, output_dir: Path) -> dict[str, str]:
    """Process all files in raw_dir and write normalized outputs.

    Returns dict mapping output filename → status.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}

    # Collect all raw content
    all_content = []
    raw_files = sorted(raw_dir.iterdir())

    for raw_file in raw_files:
        if raw_file.is_dir() or raw_file.name.startswith("."):
            continue

        input_type = detect_input_type(raw_file)
        text = raw_file.read_text(encoding="utf-8", errors="replace")

        if input_type == "markdown":
            all_content.append(text)
        elif input_type == "text":
            all_content.append(_text_to_markdown(text))
        elif input_type == "csv":
            # Basic CSV → markdown table
            lines = text.strip().split("\n")
            if lines:
                header = lines[0]
                md = f"| {header.replace(',', ' | ')} |\n"
                md += f"| {' | '.join(['---'] * len(header.split(',')))} |\n"
                for line in lines[1:]:
                    md += f"| {line.replace(',', ' | ')} |\n"
                all_content.append(md)

    combined = "\n\n---\n\n".join(all_content)

    # Write rfp.md (always)
    (output_dir / "rfp.md").write_text(combined)
    results["rfp.md"] = "created"

    # Write requirements-summary.md
    req_summary = _extract_requirements(combined)
    (output_dir / "requirements-summary.md").write_text(req_summary)
    results["requirements-summary.md"] = "created"

    # Write volume-summary.md
    vol_summary = _extract_volumes(combined)
    (output_dir / "volume-summary.md").write_text(vol_summary)
    results["volume-summary.md"] = "created"

    return results


def main():
    parser = argparse.ArgumentParser(description="Normalize raw RFP inputs to markdown")
    parser.add_argument("--raw-dir", type=Path, required=True, help="Directory with raw input files")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output directory for normalized files")
    args = parser.parse_args()

    if not args.raw_dir.exists():
        print(f"ERROR: Raw directory not found: {args.raw_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Normalizing {args.raw_dir} → {args.output_dir}")
    results = normalize_raw_inputs(args.raw_dir, args.output_dir)
    for name, status in results.items():
        print(f"  {status}: {name}")
    print("Done.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_normalize.py -v`
Expected: All 4 tests PASS

- [ ] **Step 6: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/normalize.py tests/test_normalize.py tests/fixtures/raw/sample-rfp.txt
git commit -m "feat(apv-v2): add normalize.py raw input converter with tests"
```

---

### Task 6: knowledge-audit.py — Knowledge File Auditor

**Files:**
- Create: `wiki/apv-v2/tools/knowledge-audit.py`
- Create: `wiki/apv-v2/tests/test_knowledge_audit.py`

- [ ] **Step 1: Write failing tests**

```python
# wiki/apv-v2/tests/test_knowledge_audit.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from knowledge_audit import audit_file, audit_directory, AuditResult


def test_audit_result_enum():
    assert AuditResult.PASS.value == "PASS"
    assert AuditResult.STALE.value == "STALE"
    assert AuditResult.FAIL.value == "FAIL"


def test_audit_file_pass(tmp_path):
    """A well-formed, fresh knowledge file should PASS."""
    f = tmp_path / "test.md"
    f.write_text(
        '---\ntype: entity\ncategory: infrastructure\n'
        'source_url: "https://example.com"\n'
        'last_verified: 2026-04-30\nfreshness_days: 30\n'
        'captured_date: 2026-04-01\ntags: [test]\n---\n# Test\nContent here.'
    )
    result = audit_file(f)
    assert result.status == AuditResult.PASS


def test_audit_file_stale(tmp_path):
    """A file past its freshness threshold should be STALE."""
    f = tmp_path / "old.md"
    f.write_text(
        '---\ntype: source\ncategory: pricing\n'
        'source_url: "https://example.com"\n'
        'last_verified: 2025-01-01\nfreshness_days: 30\n'
        'captured_date: 2025-01-01\ntags: []\n---\n# Old\nStale content.'
    )
    result = audit_file(f)
    assert result.status == AuditResult.STALE


def test_audit_file_fail_missing_fields(tmp_path):
    """A file missing required frontmatter fields should FAIL."""
    f = tmp_path / "bad.md"
    f.write_text("---\ntype: entity\n---\n# Missing Fields")
    result = audit_file(f)
    assert result.status == AuditResult.FAIL
    assert len(result.issues) > 0


def test_audit_file_fail_no_frontmatter(tmp_path):
    """A file with no frontmatter should FAIL."""
    f = tmp_path / "none.md"
    f.write_text("# No Frontmatter\nJust content.")
    result = audit_file(f)
    assert result.status == AuditResult.FAIL


def test_audit_directory_summary(tmp_path):
    """audit_directory should return aggregate counts."""
    (tmp_path / "good.md").write_text(
        '---\ntype: entity\ncategory: test\nsource_url: "https://example.com"\n'
        'last_verified: 2026-04-30\nfreshness_days: 365\n'
        'captured_date: 2026-01-01\ntags: []\n---\n# Good\nContent.'
    )
    (tmp_path / "bad.md").write_text("# No frontmatter")

    summary = audit_directory(tmp_path)
    assert summary["total"] == 2
    assert summary["pass"] >= 1
    assert summary["fail"] >= 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_knowledge_audit.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement knowledge-audit.py**

```python
#!/usr/bin/env python3
# wiki/apv-v2/tools/knowledge-audit.py
"""Audit knowledge files for completeness, freshness, and validity.

Usage:
    python3 knowledge-audit.py [--knowledge-dir PATH]

Each file gets: PASS, STALE, or FAIL with specific issues listed.

Exit codes: 0 = all pass, 1 = stale or failures found
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.frontmatter import parse_file


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
    """Audit a single knowledge markdown file.

    Returns FileAudit with status and any issues found.
    """
    issues = []

    try:
        fm, body = parse_file(file_path)
    except Exception as e:
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=[f"Parse error: {e}"])

    # Check frontmatter exists
    if not fm:
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=["No frontmatter found"])

    # Check required fields
    missing = [f for f in REQUIRED_FIELDS if f not in fm or fm[f] is None]
    if missing:
        issues.append(f"Missing required fields: {', '.join(missing)}")

    # Check body has content
    if not body or len(body.strip()) < 10:
        issues.append("Body content too short (< 10 chars)")

    # If we have critical missing fields, it's a FAIL
    if missing:
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=issues)

    # Check freshness
    try:
        last_verified_str = str(fm.get("last_verified", ""))
        freshness_days = int(fm.get("freshness_days", 365))

        last_verified = datetime.strptime(last_verified_str, "%Y-%m-%d").date()
        days_since = (date.today() - last_verified).days

        if days_since > freshness_days:
            issues.append(
                f"Stale: {days_since} days since verification (threshold: {freshness_days})"
            )
            return FileAudit(path=file_path, status=AuditResult.STALE, issues=issues)
    except (ValueError, TypeError):
        issues.append(f"Invalid last_verified date: {fm.get('last_verified')}")
        return FileAudit(path=file_path, status=AuditResult.FAIL, issues=issues)

    return FileAudit(path=file_path, status=AuditResult.PASS, issues=issues)


def audit_directory(directory: Path) -> dict:
    """Audit all .md files in a directory tree.

    Returns summary dict: {total, pass, stale, fail, results: [FileAudit]}
    """
    results = []
    for md_file in sorted(directory.rglob("*.md")):
        results.append(audit_file(md_file))

    summary = {
        "total": len(results),
        "pass": sum(1 for r in results if r.status == AuditResult.PASS),
        "stale": sum(1 for r in results if r.status == AuditResult.STALE),
        "fail": sum(1 for r in results if r.status == AuditResult.FAIL),
        "results": results,
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description="Audit knowledge files for completeness and freshness")
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path(__file__).parent.parent / "knowledge",
        help="Root directory of knowledge markdown files",
    )
    args = parser.parse_args()

    if not args.knowledge_dir.exists():
        print(f"ERROR: Directory not found: {args.knowledge_dir}", file=sys.stderr)
        sys.exit(1)

    summary = audit_directory(args.knowledge_dir)

    print(f"\nKnowledge Audit: {args.knowledge_dir}")
    print(f"{'='*60}")

    for result in summary["results"]:
        icon = {"PASS": "✓", "STALE": "⚠", "FAIL": "✗"}[result.status.value]
        print(f"  {icon} {result.status.value:5s} {result.path.name}")
        for issue in result.issues:
            print(f"         └─ {issue}")

    print(f"\n{'='*60}")
    print(f"Total: {summary['total']}  |  "
          f"Pass: {summary['pass']}  |  "
          f"Stale: {summary['stale']}  |  "
          f"Fail: {summary['fail']}")

    sys.exit(0 if summary["stale"] == 0 and summary["fail"] == 0 else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_knowledge_audit.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/knowledge-audit.py tests/test_knowledge_audit.py
git commit -m "feat(apv-v2): add knowledge-audit.py file auditor with tests"
```

---

### Task 7: Integration Test & .gitignore

**Files:**
- Create: `wiki/apv-v2/tests/conftest.py`
- Create: `wiki/apv-v2/tests/test_integration.py`
- Create: `wiki/apv-v2/.gitignore`

- [ ] **Step 1: Create conftest.py with shared fixtures**

```python
# wiki/apv-v2/tests/conftest.py
"""Shared test fixtures for APV V2 tools."""
import sys
from pathlib import Path

# Ensure tools/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

FIXTURES_DIR = Path(__file__).parent / "fixtures"
```

- [ ] **Step 2: Write integration test**

```python
# wiki/apv-v2/tests/test_integration.py
"""End-to-end test: raw input → normalize → sync-db → audit → validate-gates."""
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from normalize import normalize_raw_inputs
from sync_db import sync_knowledge
from knowledge_audit import audit_directory
from validate_gates import check_gate

FIXTURES = Path(__file__).parent / "fixtures"


def test_full_pipeline_flow(tmp_path):
    """Simulate a project init: normalize → index knowledge → audit → gate check."""
    project = tmp_path / "test-project"

    # 1. Normalize raw inputs
    raw_dir = project / "input" / "raw"
    raw_dir.mkdir(parents=True)
    shutil.copy(FIXTURES / "raw" / "sample-rfp.txt", raw_dir / "rfp.txt")

    normalized_dir = project / "input" / "normalized"
    results = normalize_raw_inputs(raw_dir, normalized_dir)
    assert "rfp.md" in results
    assert (normalized_dir / "rfp.md").exists()
    assert (normalized_dir / "requirements-summary.md").exists()

    # 2. Sync knowledge to SQLite
    knowledge_dir = tmp_path / "knowledge"
    shutil.copytree(FIXTURES / "knowledge", knowledge_dir)

    db_path = tmp_path / "apv-v2.sqlite"
    stats = sync_knowledge(knowledge_dir, db_path)
    assert stats["errors"] == 0
    assert stats["indexed"] >= 1

    # 3. Audit knowledge
    summary = audit_directory(knowledge_dir)
    assert summary["total"] >= 1

    # 4. Validate gate for Stage 1
    gate = check_gate(project, 1)
    assert gate["pass"] is True  # We created rfp.md and requirements-summary.md

    # 5. Stage 2 gate should fail (no brainstorm output yet)
    gate2 = check_gate(project, 2)
    assert gate2["pass"] is False
```

- [ ] **Step 3: Create .gitignore**

```gitignore
# wiki/apv-v2/.gitignore
# Derived artifacts — always regenerable
apv-v2.sqlite
*.sqlite

# Python
__pycache__/
*.pyc
.pytest_cache/

# Project runtime artifacts (each project has its own dir)
apv-projects/*/working/
apv-projects/*/*.sqlite
```

- [ ] **Step 4: Run full test suite**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/ -v`
Expected: All tests PASS (frontmatter: 6, db: 4, sync_db: 4, validate_gates: 4, normalize: 4, knowledge_audit: 5, integration: 1 = **28 tests**)

- [ ] **Step 5: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tests/conftest.py tests/test_integration.py .gitignore
git commit -m "feat(apv-v2): add integration test and .gitignore"
```

---

## Next Sub-Plan

After this plan is complete, the next sub-plan covers **Priority 2: Knowledge Bootstrap** — migrating V1 knowledge, creating domain templates, and populating the initial knowledge base so the tools have real data to work with.
