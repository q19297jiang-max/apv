---
type: apv-meta
category: plan
title: "APV Runtime Fixture Testing Design"
created: 2026-04-26
tags: [apv, testing, runtime, fixtures]
sources:
  - "[[apv-runtime-project-contract]]"
  - "[[apv-tests]]"
---

# APV Runtime Fixture Testing Design

## Goal

Add a runtime-oriented APV test slice that validates a canonical `apv-projects/...` run folder using real repo fixtures, not just documentation strings or skill-file presence.

## Problem

The current integration runner in `tests/run_integration_tests.py` is honest about being contract-level, but it still only checks file presence and text markers inside skills and documentation. It does not validate whether APV run artifacts match the runtime contract defined in `docs/runtime-project-contract.md`.

## Recommended Approach

Use a fixture-backed runtime validation test.

- Create a representative project folder under the test workspace using existing inputs from `tests/data/` and stage outputs from `tests/output/`.
- Validate canonical folder structure: `input/`, `outputs/`, `evidence/`, and `approvals/`.
- Validate a minimal set of content markers inside stage outputs so the test proves more than file existence.
- Keep this slice separate from the existing contract-level runner so APV can report both test scopes clearly.

## Why This Approach

- It is materially stronger than documentation-only checks.
- It uses assets already present in the repository.
- It is cheap to run and stable in CI.
- It avoids pretending that the full APV skill chain is executable end-to-end today.

## Scope

The first slice should validate:

- Canonical runtime folder layout.
- Presence of required stage files.
- Minimal semantic markers in key stage outputs.

Recommended output checks:

- `01-brainstorm.md`: executive summary or recommended approach markers.
- `02-compliance.md`: compliance summary or PCI-DSS mapping markers.
- `05-pricing.md`: pricing table, calculator URL, or cost breakdown markers.
- `06-response.md`: executive summary or proposal/response markers.

## Non-Goals

- Do not execute the real APV skill chain.
- Do not claim this is full end-to-end workflow validation.
- Do not broaden into performance or pricing freshness testing in this change.

## Proposed Files

- Create `tests/test_runtime_project_fixture.py`
- Create `tests/output/bbc-pricing-output.md`
- Create `tests/output/bbc-response-output.md`
- Modify `tests/README.md`
- Modify `tests/run_integration_tests.py`
- Modify `tests/integration/integration-test-report.md`

## Test Model

The runtime fixture test should:

1. Create a temporary project root matching `apv-projects/[customer]--[title]--[date]/`.
2. Copy fixture inputs into `input/`.
3. Copy fixture outputs into `outputs/` using canonical stage filenames.
4. Create expected `evidence/` and `approvals/` folders.
5. Assert the folder contract.
6. Assert content markers in selected outputs.

## Expected Outcome

After this work, APV will have two clearly distinct automated test surfaces:

- Contract-level integration checks for documentation and handoff assumptions.
- Runtime fixture checks for canonical APV project artifacts.

That is a credible next step toward eventual output-based end-to-end testing.