# APV Runtime Fixture Testing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a runtime-oriented APV test that validates canonical `apv-projects/...` folder structure and key output content markers using repo fixtures.

**Architecture:** Keep the existing `tests/run_integration_tests.py` runner as the contract-level surface, and add a new runtime fixture test under `tests/` that assembles a temporary APV project folder from existing fixture data and output files. This change should strengthen test credibility without claiming execution of the full APV skill chain.

**Tech Stack:** Python 3, pytest, pathlib, shutil, existing markdown fixtures under `tests/data/` and `tests/output/`

---

### Task 1: Add Missing Runtime Output Fixtures

**Files:**
- Create: `wiki/apv/tests/output/bbc-pricing-output.md`
- Create: `wiki/apv/tests/output/bbc-response-output.md`
- Test: `test -f wiki/apv/tests/output/bbc-pricing-output.md && test -f wiki/apv/tests/output/bbc-response-output.md`

**Step 1: Write the failing test**

Define the failure as an incomplete runtime fixture set: the repo has brainstorm and compliance sample outputs but no pricing or final response files for a canonical fixture-backed runtime test.

**Step 2: Run test to verify it fails**

Run: `test -f wiki/apv/tests/output/bbc-pricing-output.md && test -f wiki/apv/tests/output/bbc-response-output.md`
Expected: command exits non-zero because one or both files are missing.

**Step 3: Write minimal implementation**

Create `wiki/apv/tests/output/bbc-pricing-output.md` with at least:

```markdown
# RFP Pricing: BBC Bank - Credit Card Issuing System

## Executive Summary

## Monthly Cost Breakdown

## Pricing Assumptions

## Source URLs
```

Create `wiki/apv/tests/output/bbc-response-output.md` with at least:

```markdown
# BBC Bank Credit Card Issuing System Proposal

## Executive Summary

## Proposed Solution

## Compliance Position

## Commercial Summary
```

**Step 4: Run test to verify it passes**

Run: `test -f wiki/apv/tests/output/bbc-pricing-output.md && test -f wiki/apv/tests/output/bbc-response-output.md`
Expected: command exits zero.

**Step 5: Commit**

```bash
git add wiki/apv/tests/output/bbc-pricing-output.md wiki/apv/tests/output/bbc-response-output.md
git commit -m "test: add APV runtime output fixtures"
```

### Task 2: Write The Failing Runtime Fixture Test

**Files:**
- Create: `wiki/apv/tests/test_runtime_project_fixture.py`
- Test: `wiki/apv/tests/test_runtime_project_fixture.py`

**Step 1: Write the failing test**

Create a pytest module that assembles a temporary APV project folder and asserts both folder shape and content markers.

Target test structure:

```python
from pathlib import Path
import shutil


def test_runtime_project_fixture_matches_contract(tmp_path):
    project_root = tmp_path / "apv-projects" / "bbc-bank--credit-card-issuing--2026-04-26"
    (project_root / "input").mkdir(parents=True)
    (project_root / "outputs").mkdir()
    (project_root / "evidence" / "pricing").mkdir(parents=True)
    (project_root / "evidence" / "compliance").mkdir(parents=True)
    (project_root / "evidence" / "verification").mkdir(parents=True)
    (project_root / "approvals").mkdir()

    fixtures_root = Path(__file__).parent
    shutil.copy(fixtures_root / "data" / "bbc-rfp-summary.md", project_root / "input" / "bbc-rfp-summary.md")
    shutil.copy(fixtures_root / "output" / "bbc-brainstorm-output.md", project_root / "outputs" / "01-brainstorm.md")
    shutil.copy(fixtures_root / "output" / "bbc-compliance-output.md", project_root / "outputs" / "02-compliance.md")
    shutil.copy(fixtures_root / "output" / "bbc-pricing-output.md", project_root / "outputs" / "05-pricing.md")
    shutil.copy(fixtures_root / "output" / "bbc-response-output.md", project_root / "outputs" / "06-response.md")

    assert (project_root / "input").is_dir()
    assert (project_root / "outputs" / "01-brainstorm.md").exists()
    assert "Executive Summary" in (project_root / "outputs" / "01-brainstorm.md").read_text()
    assert "PCI-DSS" in (project_root / "outputs" / "02-compliance.md").read_text()
    assert "Monthly Cost Breakdown" in (project_root / "outputs" / "05-pricing.md").read_text()
    assert "Executive Summary" in (project_root / "outputs" / "06-response.md").read_text()
```

**Step 2: Run test to verify it fails**

Run: `pytest wiki/apv/tests/test_runtime_project_fixture.py -q`
Expected: FAIL because the new file does not exist yet, or because runtime fixtures are incomplete.

**Step 3: Write minimal implementation**

Implement the test file with one test for canonical folder shape and one test for content markers. Keep markers narrow and durable.

**Step 4: Run test to verify it passes**

Run: `pytest wiki/apv/tests/test_runtime_project_fixture.py -q`
Expected: PASS.

**Step 5: Commit**

```bash
git add wiki/apv/tests/test_runtime_project_fixture.py
git commit -m "test: validate APV runtime project fixture contract"
```

### Task 3: Update Test Documentation To Reflect The New Surface

**Files:**
- Modify: `wiki/apv/tests/README.md`
- Modify: `wiki/apv/tests/integration/integration-test-report.md`
- Test: `rg -n "runtime fixture|contract-level|end-to-end" wiki/apv/tests/README.md wiki/apv/tests/integration/integration-test-report.md`

**Step 1: Write the failing test**

Define the failure as test documentation that still describes only the contract-level runner and does not explain the new runtime fixture layer.

**Step 2: Run test to verify it fails**

Run: `rg -n "runtime fixture" wiki/apv/tests/README.md wiki/apv/tests/integration/integration-test-report.md`
Expected: no matches.

**Step 3: Write minimal implementation**

Update `wiki/apv/tests/README.md` to distinguish:

- contract-level integration checks
- runtime fixture checks
- future end-to-end execution checks

Update `wiki/apv/tests/integration/integration-test-report.md` so it keeps the contract-level classification and points to runtime fixture testing as a stronger but still non-execution-based layer.

**Step 4: Run test to verify it passes**

Run: `rg -n "runtime fixture|contract-level|end-to-end" wiki/apv/tests/README.md wiki/apv/tests/integration/integration-test-report.md`
Expected: matches found with honest scope wording.

**Step 5: Commit**

```bash
git add wiki/apv/tests/README.md wiki/apv/tests/integration/integration-test-report.md
git commit -m "docs: describe APV runtime fixture testing layer"
```

### Task 4: Extend The Existing Runner To Announce Both Test Layers

**Files:**
- Modify: `wiki/apv/tests/run_integration_tests.py`
- Test: `python3 wiki/apv/tests/run_integration_tests.py --verbose`

**Step 1: Write the failing test**

Define the failure as a runner that describes only contract-level integration, even after APV gains a runtime fixture validation slice.

**Step 2: Run test to verify it fails**

Run: `python3 wiki/apv/tests/run_integration_tests.py --verbose`
Expected: output mentions only contract-level integration and does not reference runtime fixture coverage.

**Step 3: Write minimal implementation**

Update the runner banner and saved metadata so it clearly states:

- this script remains contract-level
- runtime fixture validation exists separately in pytest

Minimal wording target:

```python
print("Contract-level integration tests: documentation and handoff markers only")
print("See pytest tests/test_runtime_project_fixture.py for runtime fixture validation")
```

**Step 4: Run test to verify it passes**

Run: `python3 wiki/apv/tests/run_integration_tests.py --verbose`
Expected: output clearly distinguishes the two layers.

**Step 5: Commit**

```bash
git add wiki/apv/tests/run_integration_tests.py
git commit -m "test: distinguish APV contract and runtime fixture checks"
```

### Task 5: Run The Focused Validation Set

**Files:**
- Test: `wiki/apv/tests/test_runtime_project_fixture.py`
- Test: `wiki/apv/tests/run_integration_tests.py`
- Test: `wiki/apv/tests/test_doc_claims.py`

**Step 1: Write the failing test**

This task has no new failing test. It validates that the new runtime fixture layer coexists cleanly with existing APV checks.

**Step 2: Run test set**

Run: `pytest wiki/apv/tests/test_runtime_project_fixture.py wiki/apv/tests/test_doc_claims.py -q`
Expected: PASS.

Run: `python3 wiki/apv/tests/run_integration_tests.py --verbose`
Expected: PASS with contract-level wording and runtime fixture pointer.

**Step 3: Commit**

```bash
git add wiki/apv/tests
git commit -m "test: add runtime fixture validation for APV outputs"
```