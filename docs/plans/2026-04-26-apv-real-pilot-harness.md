# APV Real Pilot Harness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a repeatable real-pilot validation harness for the BBC sample APV project and fix the validator behavior that currently blocks trustworthy project-level results.

**Architecture:** Extend the existing URL validator just enough to stop treating internal fragment links as external URLs and to handle official source accessibility checks more robustly. Then add a pilot harness script that runs the URL validator and pricing freshness checks against the known BBC sample project and prints a concise status summary without pretending to be a full orchestration engine.

**Tech Stack:** Python 3, pytest, pathlib, urllib, subprocess, existing APV tools under `tools/`

---

### Task 1: Add Failing Validator Tests For Internal Links And Accessibility Fallback

**Files:**
- Create: `wiki/apv/tests/test_validate_source_urls.py`
- Test: `wiki/apv/tests/test_validate_source_urls.py`

**Step 1: Write the failing test**

Create tests that prove:

- fragment-only links like `#1-executive-summary` should not be treated as external URLs
- official URLs should still be treated as accessible when `HEAD` fails but a fallback `GET` succeeds

Target test outline:

```python
def test_extract_urls_from_content_ignores_internal_anchor_links():
    content = "[Executive Summary](#1-executive-summary)"
    assert extract_urls_from_content(content) == []


def test_check_url_accessible_falls_back_to_get_when_head_fails():
    ...
    assert check_url_accessible("https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf") is True
```

**Step 2: Run test to verify it fails**

Run: `pytest wiki/apv/tests/test_validate_source_urls.py -q`
Expected: FAIL because the current validator includes fragment links and has no verified fallback path.

**Step 3: Write minimal implementation**

Do not implement in the test file. Leave production changes for Task 2.

**Step 4: Commit**

Do not commit yet.

### Task 2: Fix Source URL Validator Behavior

**Files:**
- Modify: `wiki/apv/tools/validate-source-urls.py`
- Test: `wiki/apv/tests/test_validate_source_urls.py`

**Step 1: Implement minimal code to pass the new tests**

Update `extract_urls_from_content` so fragment-only markdown links are skipped.

Example target logic:

```python
if url.startswith('#'):
    continue
```

Update `check_url_accessible` so it tries `HEAD` first and falls back to `GET` when `HEAD` is rejected or unsupported.

**Step 2: Run test to verify it passes**

Run: `pytest wiki/apv/tests/test_validate_source_urls.py -q`
Expected: PASS.

**Step 3: Run focused behavior check against the BBC sample project**

Run: `python3 wiki/apv/tools/validate-source-urls.py --project wiki/apv/tests/projects/bbc-bank--credit-card-issuing-2026-04-25`
Expected: fewer false positives than current behavior, ideally eliminating fragment-link failures.

**Step 4: Commit**

```bash
git add wiki/apv/tools/validate-source-urls.py wiki/apv/tests/test_validate_source_urls.py
git commit -m "fix: reduce false positives in APV source URL validation"
```

### Task 3: Add The Real Pilot Harness Script

**Files:**
- Create: `wiki/apv/tests/run_real_pilot_harness.py`
- Test: `wiki/apv/tests/run_real_pilot_harness.py`

**Step 1: Write the failing test**

Define the failure as having no single script that runs current project-level validators against the real BBC pilot folder and reports one summarized outcome.

**Step 2: Run test to verify it fails**

Run: `test -f wiki/apv/tests/run_real_pilot_harness.py`
Expected: non-zero because the file does not yet exist.

**Step 3: Write minimal implementation**

Create a script that:

- targets `tests/projects/bbc-bank--credit-card-issuing-2026-04-25/` by default
- runs `tools/validate-source-urls.py --project ...`
- runs `tools/check-pricing-freshness.py --project ...`
- returns a concise status summary and non-zero exit when a blocking check fails

**Step 4: Run test to verify it passes**

Run: `python3 wiki/apv/tests/run_real_pilot_harness.py`
Expected: script executes and reports URL validation plus pricing freshness status for the BBC sample project.

**Step 5: Commit**

```bash
git add wiki/apv/tests/run_real_pilot_harness.py
git commit -m "test: add APV real pilot harness"
```

### Task 4: Document The New Real-Pilot Layer

**Files:**
- Modify: `wiki/apv/tests/README.md`
- Modify: `wiki/apv/tests/pilot-test-report.md`
- Test: `rg -n "real pilot harness|runtime fixture|bbc-bank--credit-card-issuing-2026-04-25" wiki/apv/tests/README.md wiki/apv/tests/pilot-test-report.md`

**Step 1: Write the failing test**

Define the failure as documentation that describes partial real-pilot history but not the new repeatable harness.

**Step 2: Run test to verify it fails**

Run: `rg -n "real pilot harness" wiki/apv/tests/README.md wiki/apv/tests/pilot-test-report.md`
Expected: no matches.

**Step 3: Write minimal implementation**

Update test docs so they distinguish:

- fixture-based runtime validation
- repeatable real-pilot harness validation against the BBC sample project
- future full orchestration execution

**Step 4: Run test to verify it passes**

Run: `rg -n "real pilot harness|runtime fixture|bbc-bank--credit-card-issuing-2026-04-25" wiki/apv/tests/README.md wiki/apv/tests/pilot-test-report.md`
Expected: matches found.

**Step 5: Commit**

```bash
git add wiki/apv/tests/README.md wiki/apv/tests/pilot-test-report.md
git commit -m "docs: describe APV real pilot harness"
```

### Task 5: Run The Focused Validation Set

**Files:**
- Test: `wiki/apv/tests/test_validate_source_urls.py`
- Test: `wiki/apv/tests/run_real_pilot_harness.py`
- Test: `wiki/apv/tests/test_runtime_project_fixture.py`
- Test: `wiki/apv/tests/test_doc_claims.py`

**Step 1: Run test set**

Run: `pytest wiki/apv/tests/test_validate_source_urls.py wiki/apv/tests/test_runtime_project_fixture.py wiki/apv/tests/test_doc_claims.py -q`
Expected: PASS.

Run: `python3 wiki/apv/tests/run_real_pilot_harness.py`
Expected: executes against the BBC sample project and reports status.

**Step 2: Commit**

```bash
git add wiki/apv/tests wiki/apv/tools/validate-source-urls.py
git commit -m "test: add APV real pilot harness and validator fixes"
```