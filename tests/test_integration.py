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
