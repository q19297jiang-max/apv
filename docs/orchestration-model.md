---
type: apv-meta
category: design
title: "APV V2 Orchestration Model"
created: 2026-04-29
tags: [apv, v2, orchestration, workflow]
---

# APV V2 Orchestration Model

## Goal

Define the repo-governed execution flow for APV V2 from raw source intake to approval.

## Operating Principle

The orchestrator does not act as hidden intelligence. Its job is to ensure that each stage reads the required artifacts, emits the required artifacts, and stops at explicit gates when evidence or validation is missing.

## Flow

### Phase 1: Project Initialization

Actions:
- create `apv-projects/[customer]--[title]--[date]/`
- create standard subfolders
- register project summary files
- initialize `working/00-run-context.json` with explicit run authority state

Outputs:
- `README.md`
- empty scaffold folders
- `working/00-run-context.json`

Gate:
- project folder complete before any stage execution
- new projects default to `draft` mode unless an operator explicitly chooses `submission`

### Phase 2: Source Intake And Normalization

Actions:
- copy raw RFP inputs
- convert non-markdown inputs to markdown
- extract questionnaire, volume, and requirement summaries

Outputs:
- `input/raw/*`
- `input/normalized/*`

Gate:
- required normalized artifacts present

### Phase 3: Knowledge Grounding

Actions:
- identify relevant knowledge pages
- register missing knowledge as gaps
- prepare stage context artifacts

Outputs:
- initial gap log
- initial assumption log if needed

Gate:
- high-risk unknowns must be visible before downstream stages continue

### Phase 4: Stage Execution

Actions:
- execute stages in order using stage contracts
- run a stage through native adapters or an explicit stage command via `tools/apv.py run-stage`
- run a multi-stage plan through `tools/apv.py run-pipeline`
- persist every output to repo artifacts
- enforce run-authority rules before stage 1 when the project is in `submission` mode

Ordered stages:
1. brainstorm
2. compliance
3. architecture
4. sizing
5. pricing
6. response
7. approval

Gate:
- each stage must verify required upstream artifacts before running
- stage 1 must block `submission` runs that do not have approved sales intent
- each stage must verify its declared emitted artifacts after running
- primary stage outputs must carry valid `stage`/`output_class` metadata; stage 6 must retain upstream source traces
- primary stage outputs should also surface governance metadata such as `run_mode` and `release_eligible`
- stage 6 must not introduce response URLs that are absent from upstream evidence-backed outputs
- stage 6 must preserve at least one citation from each upstream evidence-backed source that contributed URLs
- stage 6 must surface compliance and pricing sections with upstream citations, and surface assumptions/caveats when pricing assumptions are recorded

### Phase 5: Verification

Actions:
- validate source URLs
- validate freshness
- validate artifact completeness
- verify pricing evidence presence

Outputs:
- `verification/source-url-validation.json`
- `verification/freshness-report.json`
- `verification/artifact-completeness.md`

Gate:
- no release without verification artifacts

### Phase 6: Approval And Release

Actions:
- run unified checklist review
- classify result as approve, conditional, or reject
- package submission artifact set
- evaluate governance authority separately from quality outcomes

Outputs:
- `outputs/07-approval.md`
- `approvals/release-decision.md`

Gate:
- only `submission` runs with approved sales intent may become release-eligible
- draft runs may complete and even produce approved quality artifacts, but they are never release-eligible
- only approved or explicitly accepted conditional runs may be released once governance authority also passes
- invalid URL reports, stale freshness reports, or placeholder text in the final response must block release

## Control Rules

- No stage may skip artifact emission.
- No approval may ignore missing verification.
- No pricing release may bypass freshness and evidence checks.
- No reusable knowledge update should happen without leaving a markdown artifact in the wiki surface.
- No project may be treated as releaseable if its run context remains in `draft` mode.
- Promotion from `draft` to `submission` must be explicit and must leave auditable artifacts.

## Failure Handling

If a gate fails:

- stop downstream execution
- create or update the relevant gap, assumption, or reviewer note artifact
- rerun only the affected stage chain once the missing input is fixed

## Run Authority

APV V2 now distinguishes between two operator-selected run modes:

- `draft`  internal exploration and acceleration mode; useful for fast document generation and review, but never release-eligible
- `submission`  governed delivery mode; requires approved sales intent and may become release-eligible if verification and approval pass

The canonical machine-readable authority artifact is `working/00-run-context.json`.

Promotion from draft to submission happens through `./bin/apv promote-to-submission`, which records:

- the selected promotion path
- the sales brief state
- urgency
- any fast-track attestation

By default, promotion requires a rerun from stage 1. Fast-track promotion is available only when the operator provides an explicit attestation that alignment has not materially changed.

## Long-Term Automation Boundary

The orchestrator now has a script entry point in `tools/apv.py` that covers scaffold, readiness, resume, single-stage execution, and multi-stage pipeline execution. `tools/stage_adapters.py` provides the current native adapter seam for deterministic stage generation, and `working/00-stage-commands.json` now provides a repo-governed bridge for automatically resolving stage-specific external commands without passing overrides on every invocation. The contract remains the same: it governs file artifacts and stage gates, not opaque hidden state. Direct invocation of Claude stage skills still depends on host/runtime support outside this repository.
