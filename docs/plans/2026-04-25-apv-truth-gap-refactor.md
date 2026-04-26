# APV Truth Gap Refactor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bring APV's documentation, workflow contracts, and validation claims into alignment with what is actually implemented and tested in this repository.

**Architecture:** This refactor treats the documentation set as the product surface and splits it into three concerns: current validated capability, target-state workflow, and canonical runtime contract. The first wave is doc-first and evidence-first: reduce false confidence, standardize the project/output model, and make pricing, testing, and operations claims traceable to real repo artifacts.

**Tech Stack:** Markdown documentation, repo-local Python utilities under `tools/` and `tests/`, ripgrep-based validation, git

---

### Task 1: Establish A Single Source Of Status Truth

**Files:**
- Create: `wiki/apv/docs/current-state-status.md`
- Modify: `wiki/apv/README.md`
- Modify: `wiki/apv/meta/system-index.md`
- Test: `rg -n "Design complete, implementation pending|60-90 minutes|100% source URL compliance enforced" wiki/apv`

**Step 1: Write the failing test**

Define the failure as contradictory repo messaging that mixes target-state claims with current-state status. Record the contradictions that must disappear from top-level entry points:

```text
- README says implementation pending while also stating enforcement is already achieved.
- system-index says all phases are pending while other docs read as operational.
- no single file explains what is validated vs designed vs planned.
```

**Step 2: Run test to verify it fails**

Run: `rg -n "Design complete, implementation pending|60-90 minutes|100% source URL compliance enforced" wiki/apv/README.md wiki/apv/meta/system-index.md wiki/apv/docs/user-guide.md`

Expected: matches found in top-level docs without qualification.

**Step 3: Write minimal implementation**

- Create `wiki/apv/docs/current-state-status.md` with a table that classifies each subsystem as `designed`, `implemented`, `validated`, or `operational`.
- Update `wiki/apv/README.md` to summarize APV honestly and link to the status file.
- Update `wiki/apv/meta/system-index.md` so it points readers to the status file before any workflow claims.

Suggested status table seed:

```markdown
| Subsystem | Designed | Implemented | Validated | Operational Notes |
|-----------|----------|-------------|-----------|-------------------|
| Brainstorm | yes | yes | real RFP pilot | manual execution only |
| Compliance | yes | yes | real RFP pilot | Bangladesh gap noted |
| Architecture | yes | partial | no real pilot | template and docs present |
| Sizing | yes | partial | no real pilot | methodology present |
| Pricing | yes | partial | AWS docs stronger than execution evidence | multi-cloud not production-ready |
| Generator | yes | partial | no real pilot | output contract documented |
| Reviewer | yes | partial | checklist present | approval flow not fully operationalized |
| Orchestrator | yes | partial | doc-level only | path contract inconsistent |
```

**Step 4: Run test to verify it passes**

Run: `rg -n "Design complete, implementation pending|100% source URL compliance enforced" wiki/apv/README.md wiki/apv/meta/system-index.md`

Expected: no unqualified top-level claims remain.

**Step 5: Commit**

```bash
git add wiki/apv/docs/current-state-status.md wiki/apv/README.md wiki/apv/meta/system-index.md
git commit -m "docs: add current-state status model for APV"
```

### Task 2: Canonicalize The Runtime Project Contract

**Files:**
- Create: `wiki/apv/docs/runtime-project-contract.md`
- Modify: `wiki/apv/docs/user-guide.md`
- Modify: `wiki/apv/docs/project-structure-guide.md`
- Modify: `wiki/apv/skills/apv/apv-orchestrator.md`
- Modify: `wiki/apv/approvals/unified-checklist.md`
- Test: `rg -n "apv-output/|apv-projects/|\.rfp-session/" wiki/apv`

**Step 1: Write the failing test**

Define the failure as three competing storage contracts in one system:

```text
apv-projects/ for user docs,
apv-output/ for orchestrator docs,
.rfp-session/ for approvals.
```

**Step 2: Run test to verify it fails**

Run: `rg -n "apv-output/|apv-projects/|\.rfp-session/" wiki/apv`

Expected: matches across user guide, orchestrator, approvals, and structure docs.

**Step 3: Write minimal implementation**

- Create `wiki/apv/docs/runtime-project-contract.md` as the canonical run-folder specification.
- Choose one root contract, preferably `apv-projects/[customer]--[title]--[date]/`.
- Define exact locations for `input/`, `outputs/`, `evidence/`, and `approvals/`.
- Update `wiki/apv/docs/user-guide.md`, `wiki/apv/docs/project-structure-guide.md`, `wiki/apv/skills/apv/apv-orchestrator.md`, and `wiki/apv/approvals/unified-checklist.md` to reference the same paths.

Canonical structure target:

```text
apv-projects/[customer]--[title]--[date]/
  input/
  outputs/
  evidence/
    pricing/
    compliance/
    verification/
  approvals/
```

**Step 4: Run test to verify it passes**

Run: `rg -n "apv-output/|\.rfp-session/" wiki/apv/docs wiki/apv/skills wiki/apv/approvals`

Expected: only historical or explicitly deprecated references remain.

**Step 5: Commit**

```bash
git add wiki/apv/docs/runtime-project-contract.md wiki/apv/docs/user-guide.md wiki/apv/docs/project-structure-guide.md wiki/apv/skills/apv/apv-orchestrator.md wiki/apv/approvals/unified-checklist.md
git commit -m "docs: standardize APV runtime project contract"
```

### Task 3: Reclassify Operations From Operational Reality Versus Target State

**Files:**
- Modify: `wiki/apv/docs/operations-guide.md`
- Modify: `wiki/apv/evidence/README.md`
- Modify: `wiki/apv/source-url-verification-system.md`
- Test: `rg -n "health-check\.sh|overnight|every Monday|cron|automated" wiki/apv/docs/operations-guide.md wiki/apv/source-url-verification-system.md wiki/apv/evidence/README.md`

**Step 1: Write the failing test**

Define the failure as operational instructions that assume automation exists when the repo does not provide the complete automation surface.

**Step 2: Run test to verify it fails**

Run: `rg -n "health-check\.sh|overnight|cron|weekly|automated" wiki/apv/docs/operations-guide.md wiki/apv/source-url-verification-system.md wiki/apv/evidence/README.md`

Expected: operational automation claims appear without a complete in-repo implementation path.

**Step 3: Write minimal implementation**

- Split `wiki/apv/docs/operations-guide.md` into `current manual procedure` versus `target automated procedure` sections.
- Replace any direct dependency on nonexistent files like `tools/health-check.sh` with either:
  - actual existing tools under `wiki/apv/tools/`, or
  - explicit `planned automation` labels.
- Update `wiki/apv/source-url-verification-system.md` and `wiki/apv/evidence/README.md` so scheduled jobs and evidence generation are labeled as manual, scripted, or planned.

**Step 4: Run test to verify it passes**

Run: `rg -n "health-check\.sh" wiki/apv`

Expected: no live documentation depends on missing `health-check.sh`, unless clearly marked as future work.

**Step 5: Commit**

```bash
git add wiki/apv/docs/operations-guide.md wiki/apv/evidence/README.md wiki/apv/source-url-verification-system.md
git commit -m "docs: separate current and target-state operations"
```

### Task 4: Bring Pricing Documentation In Line With Actual Readiness

**Files:**
- Modify: `wiki/apv/docs/aws-pricing-knowledge-base 1.md`
- Modify: `wiki/apv/knowledge/pricing/pricing-workflow.md`
- Modify: `wiki/apv/knowledge/pricing/azure.md`
- Modify: `wiki/apv/knowledge/pricing/gcp.md`
- Test: `rg -n "pricing-fetcher.py|pricing-verify.py|pricing-commit.py|AWS, Azure, GCP pricing with calculator URLs" wiki/apv/knowledge/pricing wiki/apv/tests`

**Step 1: Write the failing test**

Define the failure as pricing docs overstating implementation symmetry and multi-cloud readiness.

**Step 2: Run test to verify it fails**

Run: `rg -n "pricing-fetcher.py|pricing-verify.py|pricing-commit.py|AWS, Azure, GCP pricing with calculator URLs" wiki/apv/knowledge/pricing wiki/apv/tests`

Expected: generic workflow and test summaries refer to tools or readiness levels that do not match the repo’s actual pricing surface.

**Step 3: Write minimal implementation**

- Update `wiki/apv/docs/aws-pricing-knowledge-base 1.md` to explicitly mark AWS pricing as the most developed provider path.
- Update `wiki/apv/knowledge/pricing/pricing-workflow.md` to reference actual repo scripts such as `pricing-fetcher-generic.py` and `pricing-format-validator.py`, or clearly mark missing steps as planned.
- Reword `wiki/apv/knowledge/pricing/azure.md` and `wiki/apv/knowledge/pricing/gcp.md` as `reference pricing snapshots` unless they are supported by the same evidence and workflow guarantees as AWS.

**Step 4: Run test to verify it passes**

Run: `rg -n "pricing-fetcher.py|pricing-verify.py|pricing-commit.py" wiki/apv/knowledge/pricing`

Expected: outdated script references are removed or explicitly labeled as design-only.

**Step 5: Commit**

```bash
git add "wiki/apv/docs/aws-pricing-knowledge-base 1.md" wiki/apv/knowledge/pricing/pricing-workflow.md wiki/apv/knowledge/pricing/azure.md wiki/apv/knowledge/pricing/gcp.md
git commit -m "docs: align pricing readiness claims with implementation evidence"
```

### Task 5: Tighten Testing And Performance Claims To Match Evidence

**Files:**
- Modify: `wiki/apv/tests/pilot-test-report.md`
- Modify: `wiki/apv/tests/integration/integration-test-report.md`
- Modify: `wiki/apv/tests/run_integration_tests.py`
- Modify: `wiki/apv/performance-analysis.md`
- Test: `python3 wiki/apv/tests/run_integration_tests.py --verbose`

**Step 1: Write the failing test**

Define the failure as test reports claiming stronger validation than the underlying runner and pilot evidence support.

**Step 2: Run test to verify it fails**

Run: `python3 wiki/apv/tests/run_integration_tests.py --verbose`

Expected: current behavior reveals that tests are based on file existence and string checks against skill files, not true end-to-end execution of APV project outputs.

**Step 3: Write minimal implementation**

- Update `wiki/apv/tests/pilot-test-report.md` so untested skills remain explicitly unvalidated in real-RFP terms.
- Update `wiki/apv/tests/integration/integration-test-report.md` to describe the runner as `contract/documentation-level integration testing` unless the runner is strengthened.
- Update `wiki/apv/performance-analysis.md` to distinguish completed analysis from optimizations that still require deployment.
- Improve `wiki/apv/tests/run_integration_tests.py` minimally so the report output reflects what it truly checks.

Minimal runner wording target:

```python
print("Contract-level integration test: checks skill-file presence and documented data-flow markers")
```

**Step 4: Run test to verify it passes**

Run: `python3 wiki/apv/tests/run_integration_tests.py --verbose`

Expected: output and documentation now describe the test scope honestly.

**Step 5: Commit**

```bash
git add wiki/apv/tests/pilot-test-report.md wiki/apv/tests/integration/integration-test-report.md wiki/apv/tests/run_integration_tests.py wiki/apv/performance-analysis.md
git commit -m "docs: narrow APV validation and performance claims to tested scope"
```

### Task 6: Add A Drift Check For Future Documentation Regressions

**Files:**
- Create: `wiki/apv/tests/test_doc_claims.py`
- Modify: `wiki/apv/tests/README.md` (create if missing)
- Test: `pytest wiki/apv/tests/test_doc_claims.py -q`

**Step 1: Write the failing test**

Create a documentation guardrail test that fails when forbidden unqualified claims reappear.

```python
from pathlib import Path

FORBIDDEN = {
    "wiki/apv/README.md": [
        "100% source URL compliance enforced",
        "implementation pending",
    ],
}
```

**Step 2: Run test to verify it fails**

Run: `pytest wiki/apv/tests/test_doc_claims.py -q`

Expected: FAIL until the targeted docs are rewritten or exceptions are made explicit.

**Step 3: Write minimal implementation**

- Add a small pytest file that scans a short allowlist of top-level docs.
- Fail if contradictory phrases appear without a qualifier such as `planned`, `target state`, or `validated only for`.
- Add a `wiki/apv/tests/README.md` note explaining this test protects documentation truthfulness rather than business logic.

**Step 4: Run test to verify it passes**

Run: `pytest wiki/apv/tests/test_doc_claims.py -q`

Expected: PASS.

**Step 5: Commit**

```bash
git add wiki/apv/tests/test_doc_claims.py wiki/apv/tests/README.md
git commit -m "test: add APV documentation truthfulness guardrail"
```

### Task 7: Final Verification And Release Notes

**Files:**
- Create: `wiki/apv/docs/refactor-status-summary.md`
- Test: `rg -n "target state|planned|validated|manual|operational" wiki/apv/README.md wiki/apv/docs wiki/apv/meta wiki/apv/tests`

**Step 1: Write the failing test**

Define completion failure as not having a concise summary of what changed and what remains intentionally unimplemented.

**Step 2: Run test to verify it fails**

Run: `test -f wiki/apv/docs/refactor-status-summary.md; echo $?`

Expected: `1`

**Step 3: Write minimal implementation**

- Create `wiki/apv/docs/refactor-status-summary.md`.
- Summarize what is now classified as validated, manual, planned, or operational.
- Include remaining follow-up items such as true end-to-end RFP execution and deeper pricing automation.

**Step 4: Run test to verify it passes**

Run: `rg -n "target state|planned|validated|manual|operational" wiki/apv/README.md wiki/apv/docs wiki/apv/meta wiki/apv/tests`

Expected: repository language now reflects maturity distinctions consistently.

**Step 5: Commit**

```bash
git add wiki/apv/docs/refactor-status-summary.md
git commit -m "docs: publish APV refactor status summary"
```