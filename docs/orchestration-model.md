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

Outputs:
- `README.md`
- empty scaffold folders

Gate:
- project folder complete before any stage execution

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
- persist every output to repo artifacts

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

Outputs:
- `outputs/07-approval.md`
- `approvals/release-decision.md`

Gate:
- only approved or explicitly accepted conditional runs may be released

## Control Rules

- No stage may skip artifact emission.
- No approval may ignore missing verification.
- No pricing release may bypass freshness and evidence checks.
- No reusable knowledge update should happen without leaving a markdown artifact in the wiki surface.

## Failure Handling

If a gate fails:

- stop downstream execution
- create or update the relevant gap, assumption, or reviewer note artifact
- rerun only the affected stage chain once the missing input is fixed

## Long-Term Automation Boundary

The orchestrator may later become a script or command entry point, but the contract remains the same: it governs file artifacts and stage gates, not opaque hidden state.