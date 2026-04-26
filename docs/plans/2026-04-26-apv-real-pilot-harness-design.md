---
type: apv-meta
category: plan
title: "APV Real Pilot Harness Design"
created: 2026-04-26
tags: [apv, testing, pilot, validation]
sources:
  - "[[apv-runtime-project-contract]]"
  - "[[task-3.3-real-rfp-pilot-test-report]]"
---

# APV Real Pilot Harness Design

## Goal

Turn the existing BBC sample project into a repeatable real-pilot validation target that APV can check automatically under the canonical `apv-projects/...` contract.

## Current Findings

- A real sample project exists and can be stored as a repo-tracked pilot fixture under `tests/projects/bbc-bank--credit-card-issuing-2026-04-25/`.
- That project already contains stage outputs, pricing evidence, and approval artifacts.
- `check-pricing-freshness.py --project` passes cleanly against it.
- `validate-source-urls.py --project` fails for two local reasons:
  - markdown table-of-contents links like `#1-executive-summary` are treated as invalid URLs
  - at least one official source URL is flagged inaccessible via the current network check path

## Approaches Considered

### Approach 1: Wrapper-Only Harness

Add a pilot harness that runs the existing validators and simply reports the current failures.

Pros:
- Minimal code
- Fastest to add

Cons:
- Preserves known false positives
- Produces noisy pilot results
- Does not improve the validator itself

### Approach 2: Fix Validator Root Cause, Then Wrap It

Improve `validate-source-urls.py` so it ignores internal fragment links and handles official URL accessibility checks more robustly, then add a pilot harness that runs current validators against the BBC sample project.

Pros:
- Fixes the real control point
- Makes pilot results materially more trustworthy
- Reuses existing validator and freshness tooling

Cons:
- Slightly larger change set
- Requires new tests around validator behavior

### Approach 3: Full Skill-Execution Pilot Harness

Attempt to invoke APV generation steps end-to-end from source inputs and compare produced artifacts.

Pros:
- Strongest possible evidence

Cons:
- Too large for the next slice
- Current repo is not operationally mature enough for this to be a low-risk change

## Recommendation

Choose Approach 2.

It is the smallest change that increases truthfulness and usefulness at the same time. The sample project is already a viable real-pilot artifact set. The missing piece is reliable validation against that artifact set.

## Proposed Scope

1. Add unit tests for `validate-source-urls.py` covering internal anchor links and accessibility fallback behavior.
2. Fix `validate-source-urls.py` so fragment-only markdown links are ignored and accessibility checks degrade more gracefully for official sources.
3. Add a small pilot harness script that runs URL validation and freshness checks against the real BBC project folder and emits a summarized pass/fail result.
4. Document the new harness and how it differs from fixture-only runtime tests.

## Non-Goals

- Do not execute the full APV skill chain.
- Do not broaden this slice into orchestration automation.
- Do not reclassify APV as fully operational based on one pilot harness.

## Expected Outcome

After this work, APV will have:

- fixture-based runtime validation for canonical artifact shape
- a repeatable real-pilot harness for one known sample project
- a cleaner source URL validator with fewer local false positives

That is a credible bridge from fixture testing toward broader real-project validation.