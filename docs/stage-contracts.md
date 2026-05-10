---
type: apv-meta
category: design
title: "APV V2 Stage Contracts"
created: 2026-04-29
tags: [apv, v2, stages, contracts]
---

# APV V2 Stage Contracts

## Goal

Define exact consumes/emits contracts for each APV stage so the workflow runs on explicit artifacts rather than hidden context.

## Stage 0: Ingestion

Consumes:
- `input/raw/*`

Emits:
- `input/normalized/rfp.md`
- `input/normalized/questionnaire.md`
- `input/normalized/card-volume.md`
- `input/normalized/requirements-summary.md`
- `input/normalized/volume-summary.md`
- `working/00-run-context.json`

Required checks:
- conversion completed
- required normalized files present
- run context initialized with the intended mode (`draft` by default, `submission` only with explicit operator intent)

## Stage 1: rfp-brainstorm

Consumes:
- `input/normalized/rfp.md`
- `input/normalized/requirements-summary.md`
- `working/00-run-context.json`
- `input/normalized/sales-brief.md` (required when `run_mode = submission`)
- relevant reusable knowledge pages

Emits:
- `working/01-brainstorm-context.md`
- `working/05-gap-log.md` (initial entries allowed)
- `outputs/01-brainstorm.md`

Required checks:
- knowledge gaps clearly listed
- target regions/type/provider assumptions visible
- submission mode must block if approved sales intent is missing
- draft mode must remain visibly draft-only even when downstream work proceeds

## Stage 2: rfp-compliance

Consumes:
- `outputs/01-brainstorm.md`
- `input/normalized/requirements-summary.md`
- compliance knowledge pages

Emits:
- `working/02-compliance-map.md`
- `outputs/02-compliance.md`
- `evidence/compliance/...`

Required checks:
- all compliance claims cite source URLs
- missing regulations or gaps explicitly logged

## Stage 3: rfp-architect

Consumes:
- `outputs/01-brainstorm.md`
- `outputs/02-compliance.md`
- infrastructure and product knowledge pages

Emits:
- `working/03-architecture-decision-log.md`
- `outputs/03-architecture.md`

Required checks:
- architecture assumptions explicit
- compliance-impacting architecture choices documented

## Stage 4: rfp-calculator

Consumes:
- `outputs/03-architecture.md`
- `input/normalized/volume-summary.md`
- sizing methodology knowledge

Emits:
- `working/04-sizing-record.md`
- `outputs/04-sizing.md`

Required checks:
- formulas and peak multipliers explicit
- major resource sizing traceable to input volumes

## Stage 5: rfp-pricer

Consumes:
- `outputs/03-architecture.md`
- `outputs/04-sizing.md`
- pricing knowledge pages
- project pricing evidence

Emits:
- `working/05-pricing-manifest.md`
- `working/05-assumption-log.md`
- `outputs/05-pricing.md`
- `evidence/pricing/...`
- `verification/freshness-report.json`

Required checks:
- official pricing source URLs present
- evidence capture linked
- freshness thresholds satisfied or exception logged

## Stage 6: rfp-generator

Consumes:
- `outputs/01-brainstorm.md`
- `outputs/02-compliance.md`
- `outputs/03-architecture.md`
- `outputs/04-sizing.md`
- `outputs/05-pricing.md`
- active assumption and gap logs

Emits:
- `outputs/06-response.md`

Required checks:
- final response does not introduce unsupported claims
- major claims traceable back to stage outputs
- response artifacts should preserve governance metadata such as `run_mode` and `release_eligible`

## Stage 7: apv-reviewer

Consumes:
- `outputs/06-response.md`
- `verification/source-url-validation.json`
- `verification/freshness-report.json`
- `approvals/unified-checklist.md`

Emits:
- `outputs/07-approval.md`
- `approvals/release-decision.md`
- `approvals/reviewer-notes.md`

Required checks:
- source URL compliance
- freshness compliance
- evidence completeness
- conditional/reject items clearly listed
- release eligibility requires both an acceptable quality outcome and `run_mode = submission`
- draft mode never becomes release-eligible regardless of quality outcome

## Global Contract Rules

- A stage may not emit final output unless required upstream artifacts exist.
- Missing data must be recorded in gap or assumption artifacts, not silently ignored.
- All stage outputs must remain valid markdown project artifacts suitable for git review.
- A submission-candidate run may not proceed through stage 1 without approved sales intent.
- Promotion from `draft` to `submission` is a separate workflow that updates run context and may require rerunning the affected stage chain.
