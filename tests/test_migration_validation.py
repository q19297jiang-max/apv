"""Post-migration validation — ensures all migrated knowledge is well-formed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import pytest
from knowledge_audit import audit_directory, AuditResult
from sync_db import sync_knowledge

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


def test_no_knowledge_files_fail_audit():
    """Every migrated knowledge file must have valid V2 frontmatter (no FAIL on content files)."""
    if not KNOWLEDGE_DIR.exists() or not list(KNOWLEDGE_DIR.rglob("*.md")):
        pytest.skip("No knowledge files found — run migration first")

    summary = audit_directory(KNOWLEDGE_DIR)
    failed = [r for r in summary["results"] if r.status == AuditResult.FAIL]
    # Allow known non-knowledge files to fail (README, workflow docs, templates)
    non_knowledge = {"README.md", "pricing-workflow.md", "component-catalog-template.md", ".country-template.md"}
    real_failures = [r for r in failed if r.path.name not in non_knowledge]
    assert len(real_failures) == 0, (
        f"{len(real_failures)} knowledge files failed audit:\n"
        + "\n".join(f"  - {r.path.name}: {r.issues}" for r in real_failures)
    )


def test_all_domains_have_files():
    """Each of the 5 core knowledge domains should have at least 1 file."""
    expected_domains = ["card-systems", "compliance", "infrastructure", "pricing", "sizing"]
    for domain in expected_domains:
        domain_dir = KNOWLEDGE_DIR / domain
        md_files = list(domain_dir.rglob("*.md")) if domain_dir.exists() else []
        content_files = [f for f in md_files if not f.name.startswith(".")]
        assert len(content_files) > 0, f"Domain {domain} has no content files"


def test_sync_db_indexes_all_migrated_files(tmp_path):
    """sync_db should index every migrated knowledge file without errors."""
    if not KNOWLEDGE_DIR.exists() or not list(KNOWLEDGE_DIR.rglob("*.md")):
        pytest.skip("No knowledge files found — run migration first")

    db_path = tmp_path / "test.sqlite"
    stats = sync_knowledge(KNOWLEDGE_DIR, db_path)
    assert stats["errors"] == 0
    assert stats["indexed"] >= 50, f"Expected ≥50 indexed, got {stats['indexed']}"
