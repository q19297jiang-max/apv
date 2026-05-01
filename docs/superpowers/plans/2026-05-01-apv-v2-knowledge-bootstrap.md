# APV V2 Knowledge Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate 59 V1 knowledge files into V2 with compliant frontmatter, create missing domain directories, build a migration script for automated frontmatter enrichment, and validate the full knowledge base with `knowledge_audit.py`.

**Architecture:** A Python migration script reads V1 files, enriches frontmatter to V2 schema (adding `freshness_days`, `last_verified`, normalizing `type`), copies to V2 directory structure, then runs `sync_db.py` + `knowledge_audit.py` to validate. Templates are updated to match V2 schema.

**Tech Stack:** Python 3.10+ (stdlib only), existing V2 tools (`sync_db.py`, `knowledge_audit.py`, `lib/frontmatter.py`)

---

## File Structure

```
wiki/apv-v2/
├── tools/
│   └── migrate_v1.py                 # V1→V2 migration script
├── tests/
│   └── test_migrate_v1.py            # Migration tests
├── knowledge/
│   ├── card-systems/                 # Renamed from product/
│   │   ├── issuing.md ... (7 files)
│   │   └── .template.md
│   ├── compliance/
│   │   ├── pci-dss/                  # 13 files
│   │   └── countries/                # 7 subdirs × 3-4 files = 24 files
│   ├── infrastructure/
│   │   ├── aws/ azure/ gcp/          # 7 files
│   │   └── .template.md
│   ├── pricing/
│   │   ├── aws.md, azure.md, gcp.md
│   │   ├── aws-component-catalog.md
│   │   └── .template.md
│   ├── sizing/                       # NEW directory
│   │   ├── tps-calculator.md
│   │   └── .template.md
│   ├── commercial/                   # NEW directory (empty, per-deal)
│   │   └── .template.md
│   └── patterns/                     # Stays (empty for now, no V1 source)
│       └── .template.md
└── templates/
    └── knowledge-page.md             # Universal V2 knowledge template
```

---

### Task 1: Fix V2 Scaffold — Rename & Create Directories

**Files:**
- Rename: `wiki/apv-v2/knowledge/product/` → `wiki/apv-v2/knowledge/card-systems/`
- Create: `wiki/apv-v2/knowledge/sizing/`
- Create: `wiki/apv-v2/knowledge/commercial/`
- Create: `wiki/apv-v2/knowledge/compliance/pci-dss/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/sg/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/my/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/ph/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/id/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/hk/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/th/`
- Create: `wiki/apv-v2/knowledge/compliance/countries/tw/`
- Create: `wiki/apv-v2/knowledge/infrastructure/aws/`
- Create: `wiki/apv-v2/knowledge/infrastructure/azure/`
- Create: `wiki/apv-v2/knowledge/infrastructure/gcp/`

- [ ] **Step 1: Rename product → card-systems**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
mv knowledge/product knowledge/card-systems
```

- [ ] **Step 2: Create missing directories**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
mkdir -p knowledge/sizing
mkdir -p knowledge/commercial
mkdir -p knowledge/compliance/pci-dss
mkdir -p knowledge/compliance/countries/{sg,my,ph,id,hk,th,tw}
mkdir -p knowledge/infrastructure/{aws,azure,gcp}
```

- [ ] **Step 3: Verify structure**

```bash
find knowledge -type d | sort
```

Expected: 18+ directories matching the design spec's 7 domains.

- [ ] **Step 4: Commit**

```bash
git add knowledge/
git commit -m "chore(apv-v2): fix knowledge scaffold — rename product→card-systems, add missing dirs"
```

---

### Task 2: Build migrate_v1.py — Migration Script

**Files:**
- Create: `wiki/apv-v2/tools/migrate_v1.py`
- Create: `wiki/apv-v2/tests/test_migrate_v1.py`

- [ ] **Step 1: Write failing tests**

```python
# wiki/apv-v2/tests/test_migrate_v1.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from migrate_v1 import enrich_frontmatter, map_v1_path_to_v2


# V1 frontmatter format (missing freshness_days, last_verified, wrong type)
V1_CARD_SYSTEM_FM = {
    "type": "apv-knowledge",
    "category": "card-systems",
    "title": "Card Issuing Platform",
    "source_url": "https://www.emvco.com/emv-technologies/payment-tokenization",
    "source_document": "EMVCo Specifications",
    "captured_date": "2026-04-24",
    "verified_by": "Infrastructure Architect",
    "tags": ["card-systems", "issuing", "cards"],
}

V1_COMPLIANCE_FM = {
    "type": "apv-knowledge",
    "category": "compliance",
    "subcategory": "country-regulation",
    "country": "sg",
    "title": "Singapore MAS Technology Risk Management Guidelines",
    "source_url": "https://www.mas.gov.sg/...",
    "captured_date": "2026-04-24",
    "tags": ["compliance", "singapore", "mas"],
}

V1_PRICING_FM = {
    "type": "apv-knowledge",
    "category": "pricing",
    "title": "AWS EC2 Pricing",
    "source_url": "https://aws.amazon.com/ec2/pricing/",
    "captured_date": "2026-04-20",
    "tags": ["pricing", "aws"],
}


def test_enrich_adds_freshness_days():
    """V2 requires freshness_days — should be added based on category."""
    result = enrich_frontmatter(V1_CARD_SYSTEM_FM.copy())
    assert "freshness_days" in result
    assert result["freshness_days"] == 365  # card-systems = 365 days


def test_enrich_adds_last_verified():
    """V2 requires last_verified — should default to captured_date."""
    result = enrich_frontmatter(V1_CARD_SYSTEM_FM.copy())
    assert "last_verified" in result
    assert result["last_verified"] == "2026-04-24"


def test_enrich_normalizes_type():
    """V1 uses 'apv-knowledge', V2 uses 'source'."""
    result = enrich_frontmatter(V1_CARD_SYSTEM_FM.copy())
    assert result["type"] == "source"


def test_enrich_pricing_gets_30_day_freshness():
    """Pricing domain should get 30-day freshness."""
    result = enrich_frontmatter(V1_PRICING_FM.copy())
    assert result["freshness_days"] == 30


def test_enrich_compliance_gets_365_day_freshness():
    """Compliance domain should get 365-day freshness."""
    result = enrich_frontmatter(V1_COMPLIANCE_FM.copy())
    assert result["freshness_days"] == 365


def test_map_v1_path_card_systems():
    v1 = Path("wiki/apv/knowledge/card-systems/issuing.md")
    v2 = map_v1_path_to_v2(v1)
    assert v2 == Path("knowledge/card-systems/issuing.md")


def test_map_v1_path_compliance_country():
    v1 = Path("wiki/apv/knowledge/compliance/countries/sg/mas-trm.md")
    v2 = map_v1_path_to_v2(v1)
    assert v2 == Path("knowledge/compliance/countries/sg/mas-trm.md")


def test_map_v1_path_pricing():
    v1 = Path("wiki/apv/knowledge/pricing/aws.md")
    v2 = map_v1_path_to_v2(v1)
    assert v2 == Path("knowledge/pricing/aws.md")


def test_map_v1_skips_templates():
    """Template files should return None (not migrated)."""
    v1 = Path("wiki/apv/knowledge/card-systems/.template.md")
    v2 = map_v1_path_to_v2(v1)
    assert v2 is None


def test_map_v1_skips_scripts():
    """Python scripts should return None (not migrated as knowledge)."""
    v1 = Path("wiki/apv/knowledge/pricing/pricing-format-validator.py")
    v2 = map_v1_path_to_v2(v1)
    assert v2 is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_migrate_v1.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement migrate_v1.py**

```python
#!/usr/bin/env python3
# wiki/apv-v2/tools/migrate_v1.py
"""Migrate V1 APV knowledge files to V2 format.

Usage:
    python3 migrate_v1.py --v1-dir PATH --v2-dir PATH [--dry-run]

Enriches frontmatter:
- type: apv-knowledge → source
- Adds freshness_days based on category
- Adds last_verified (defaults to captured_date)
- Preserves all other fields

Skips: templates (.template.md), scripts (.py), backups dir
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.frontmatter import parse_file


# Freshness thresholds per domain (from system design spec)
DOMAIN_FRESHNESS = {
    "compliance": 365,
    "card-systems": 365,
    "infrastructure": 90,
    "pricing": 30,
    "commercial": 0,  # per-deal, no expiry
    "sizing": 365,
    "patterns": 0,  # no expiry
}


def enrich_frontmatter(fm: dict) -> dict:
    """Enrich V1 frontmatter to V2 schema.

    - Normalize type: apv-knowledge → source
    - Add freshness_days based on category
    - Add last_verified (default to captured_date)
    """
    result = dict(fm)

    # Normalize type
    if result.get("type") == "apv-knowledge":
        result["type"] = "source"

    # Add freshness_days based on category
    category = result.get("category", "")
    # Handle subcategories: "compliance" covers pci-dss and countries
    base_category = category.split("/")[0] if "/" in category else category
    if "freshness_days" not in result:
        result["freshness_days"] = DOMAIN_FRESHNESS.get(base_category, 365)

    # Add last_verified (default to captured_date)
    if "last_verified" not in result:
        result["last_verified"] = str(result.get("captured_date", "")) or None

    return result


def map_v1_path_to_v2(v1_path: Path) -> Path | None:
    """Map a V1 knowledge file path to its V2 destination.

    Returns None for files that should be skipped (templates, scripts, etc.).
    """
    # Skip non-markdown
    if v1_path.suffix != ".md":
        return None

    # Skip templates
    if v1_path.name.startswith("."):
        return None

    # Skip backups
    if "backups" in v1_path.parts:
        return None

    # Extract path relative to knowledge/
    parts = v1_path.parts
    try:
        knowledge_idx = parts.index("knowledge")
        rel_parts = parts[knowledge_idx:]  # knowledge/domain/...
        return Path(*rel_parts)
    except ValueError:
        return None


def migrate_file(v1_path: Path, v2_base: Path, dry_run: bool = False) -> dict:
    """Migrate a single V1 file to V2.

    Returns: {"status": "migrated"|"skipped"|"error", "v2_path": str, ...}
    """
    v2_rel = map_v1_path_to_v2(v1_path)
    if v2_rel is None:
        return {"status": "skipped", "reason": "template/script/non-md", "v1_path": str(v1_path)}

    v2_path = v2_base / v2_rel

    try:
        fm, body = parse_file(v1_path)
        enriched = enrich_frontmatter(fm) if fm else {}

        if dry_run:
            return {"status": "would_migrate", "v1_path": str(v1_path), "v2_path": str(v2_path)}

        # Write enriched file
        v2_path.parent.mkdir(parents=True, exist_ok=True)

        # Reconstruct file with enriched frontmatter
        lines = ["---"]
        for key, value in enriched.items():
            if isinstance(value, list):
                lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
            elif isinstance(value, bool):
                lines.append(f"{key}: {'true' if value else 'false'}")
            elif value is None:
                lines.append(f"{key}:")
            elif isinstance(value, str) and (" " in value or ":" in value or '"' in value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")
        lines.append("---")
        lines.append(body)

        v2_path.write_text("\n".join(lines), encoding="utf-8")

        return {"status": "migrated", "v1_path": str(v1_path), "v2_path": str(v2_path)}

    except Exception as e:
        return {"status": "error", "v1_path": str(v1_path), "error": str(e)}


def migrate_all(v1_knowledge_dir: Path, v2_base: Path, dry_run: bool = False) -> dict:
    """Migrate all V1 knowledge files to V2.

    Returns: {"total": N, "migrated": N, "skipped": N, "errors": N, "results": [...]}
    """
    results = []
    for md_file in sorted(v1_knowledge_dir.rglob("*")):
        if md_file.is_dir():
            continue
        result = migrate_file(md_file, v2_base, dry_run=dry_run)
        results.append(result)

    stats = {
        "total": len(results),
        "migrated": sum(1 for r in results if r["status"] in ("migrated", "would_migrate")),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "results": results,
    }
    return stats


def main():
    parser = argparse.ArgumentParser(description="Migrate V1 knowledge to V2 format")
    parser.add_argument("--v1-dir", type=Path, required=True, help="V1 knowledge directory")
    parser.add_argument("--v2-dir", type=Path, required=True, help="V2 base directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    print(f"{'DRY RUN: ' if args.dry_run else ''}Migrating {args.v1_dir} → {args.v2_dir}")
    stats = migrate_all(args.v1_dir, args.v2_dir, dry_run=args.dry_run)

    for r in stats["results"]:
        icon = {"migrated": "✓", "would_migrate": "~", "skipped": "·", "error": "✗"}[r["status"]]
        print(f"  {icon} {r['status']:15s} {r.get('v1_path', '')}")

    print(f"\nTotal: {stats['total']}  |  Migrated: {stats['migrated']}  |  "
          f"Skipped: {stats['skipped']}  |  Errors: {stats['errors']}")

    sys.exit(1 if stats["errors"] > 0 else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_migrate_v1.py -v`
Expected: All 10 tests PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tools/migrate_v1.py tests/test_migrate_v1.py
git commit -m "feat(apv-v2): add V1→V2 knowledge migration script with tests"
```

---

### Task 3: Create V2 Knowledge Templates

**Files:**
- Create: `wiki/apv-v2/templates/knowledge-page.md`
- Create: `wiki/apv-v2/knowledge/card-systems/.template.md`
- Create: `wiki/apv-v2/knowledge/compliance/.template.md`
- Create: `wiki/apv-v2/knowledge/infrastructure/.template.md`
- Create: `wiki/apv-v2/knowledge/pricing/.template.md`
- Create: `wiki/apv-v2/knowledge/sizing/.template.md`
- Create: `wiki/apv-v2/knowledge/commercial/.template.md`
- Create: `wiki/apv-v2/knowledge/patterns/.template.md`

- [ ] **Step 1: Create universal template**

Write `wiki/apv-v2/templates/knowledge-page.md`:

```markdown
---
type: source
category: {{CATEGORY}}
source_url: "{{SOURCE_URL}}"
captured_date: {{YYYY-MM-DD}}
last_verified: {{YYYY-MM-DD}}
freshness_days: {{FRESHNESS_DAYS}}
tags: [{{TAGS}}]
---

# {{TITLE}}

{{DESCRIPTION}}

## Key Facts

- {{FACT_1}}
- {{FACT_2}}

## Sources

- [{{SOURCE_NAME}}]({{SOURCE_URL}}) — captured {{YYYY-MM-DD}}
```

- [ ] **Step 2: Create domain-specific templates**

Each domain template inherits from the universal template but pre-fills `category` and `freshness_days`:

**card-systems/.template.md** — category: card-systems, freshness_days: 365
**compliance/.template.md** — category: compliance, freshness_days: 365
**infrastructure/.template.md** — category: infrastructure, freshness_days: 90
**pricing/.template.md** — category: pricing, freshness_days: 30
**sizing/.template.md** — category: sizing, freshness_days: 365
**commercial/.template.md** — category: commercial, freshness_days: 0 (per-deal)
**patterns/.template.md** — category: patterns, freshness_days: 0 (no expiry)

Each template should include domain-specific sections. For example:
- pricing: includes "## On-Demand Pricing" and "## Savings Plans" sections
- compliance: includes "## Requirements", "## Implementation Guidance"
- infrastructure: includes "## Configuration", "## Deployment Patterns"

- [ ] **Step 3: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add templates/ knowledge/*/.template.md
git commit -m "feat(apv-v2): add V2 knowledge templates for all 7 domains"
```

---

### Task 4: Run Migration — V1 → V2

**Files:**
- Modify: All files under `wiki/apv-v2/knowledge/` (populated by migration)

- [ ] **Step 1: Dry run migration**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
python3 tools/migrate_v1.py \
  --v1-dir ../apv/knowledge \
  --v2-dir . \
  --dry-run
```

Review output: confirm ~59 files would be migrated, ~7 templates + ~3 scripts skipped.

- [ ] **Step 2: Execute migration**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
python3 tools/migrate_v1.py \
  --v1-dir ../apv/knowledge \
  --v2-dir .
```

Expected: ~59 files migrated, 0 errors.

- [ ] **Step 3: Verify with knowledge_audit.py**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
python3 tools/knowledge_audit.py --knowledge-dir knowledge
```

Expected: All migrated files have PASS or STALE status (no FAIL — all should have required frontmatter after enrichment).

- [ ] **Step 4: Build SQLite index**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
python3 tools/sync_db.py --knowledge-dir knowledge --db-path apv-v2.sqlite
```

Expected: All files indexed, 0 errors.

- [ ] **Step 5: Spot-check 3 migrated files**

Read and verify enriched frontmatter on:
1. `knowledge/card-systems/issuing.md` — should have freshness_days: 365, type: source
2. `knowledge/compliance/countries/sg/mas-trm.md` — should have freshness_days: 365
3. `knowledge/pricing/aws.md` — should have freshness_days: 30

- [ ] **Step 6: Commit migrated knowledge**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add knowledge/
git commit -m "feat(apv-v2): migrate 59 V1 knowledge files with enriched frontmatter"
```

---

### Task 5: Post-Migration Validation & Index Update

**Files:**
- Create: `wiki/apv-v2/tests/test_migration_validation.py`

- [ ] **Step 1: Write validation test**

```python
# wiki/apv-v2/tests/test_migration_validation.py
"""Post-migration validation — ensures all migrated knowledge is well-formed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from knowledge_audit import audit_directory, AuditResult
from sync_db import sync_knowledge

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


def test_no_knowledge_files_fail_audit():
    """Every migrated knowledge file must have valid V2 frontmatter (no FAIL)."""
    if not KNOWLEDGE_DIR.exists() or not list(KNOWLEDGE_DIR.rglob("*.md")):
        import pytest
        pytest.skip("No knowledge files found — run migration first")

    summary = audit_directory(KNOWLEDGE_DIR)
    failed = [r for r in summary["results"] if r.status == AuditResult.FAIL]
    assert len(failed) == 0, (
        f"{len(failed)} files failed audit:\n"
        + "\n".join(f"  - {r.path.name}: {r.issues}" for r in failed)
    )


def test_all_domains_have_files():
    """Each of the 7 knowledge domains should have at least 1 file."""
    expected_domains = ["card-systems", "compliance", "infrastructure", "pricing", "sizing"]
    for domain in expected_domains:
        domain_dir = KNOWLEDGE_DIR / domain
        md_files = list(domain_dir.rglob("*.md")) if domain_dir.exists() else []
        # Filter out templates
        content_files = [f for f in md_files if not f.name.startswith(".")]
        assert len(content_files) > 0, f"Domain {domain} has no content files"


def test_sync_db_indexes_all_migrated_files(tmp_path):
    """sync_db should index every migrated knowledge file."""
    if not KNOWLEDGE_DIR.exists() or not list(KNOWLEDGE_DIR.rglob("*.md")):
        import pytest
        pytest.skip("No knowledge files found — run migration first")

    db_path = tmp_path / "test.sqlite"
    stats = sync_knowledge(KNOWLEDGE_DIR, db_path)
    assert stats["errors"] == 0
    # Count non-template .md files
    expected = len([f for f in KNOWLEDGE_DIR.rglob("*.md") if not f.name.startswith(".")])
    assert stats["indexed"] == expected, (
        f"Expected {expected} indexed, got {stats['indexed']}"
    )
```

- [ ] **Step 2: Run validation**

Run: `cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2 && python3 -m pytest tests/test_migration_validation.py -v`
Expected: All 3 tests PASS (assuming migration ran in Task 4)

- [ ] **Step 3: Commit**

```bash
cd /Users/stevenjiang/workspace/mykb/wiki/apv-v2
git add tests/test_migration_validation.py
git commit -m "feat(apv-v2): add post-migration validation tests"
```

---

## Next Sub-Plan

After this plan is complete, the next sub-plan covers **Priority 3: SKILL.md Files** — writing all 8 Claude Code skills (orchestrator + 7 pipeline stages) that read from the knowledge base and emit artifacts per the stage contracts.
