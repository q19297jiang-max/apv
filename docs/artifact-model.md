---
type: apv-meta
category: design
title: "APV V2 Artifact Model"
created: 2026-04-29
tags: [apv, v2, artifacts, runtime]
---

# APV V2 Artifact Model

## Goal

Define the standard artifact classes, exact folder layout, and expected file names for APV V2.

## Surfaces

APV V2 has two artifact surfaces:

1. `wiki/apv-v2/` — reusable knowledge and operating model
2. `apv-projects/[customer]--[title]--[date]/` — single RFP runtime artifact set

## Reusable Wiki Surface

```text
wiki/apv-v2/
├── README.md
├── approvals/
├── docs/
├── evidence/
├── knowledge/
│   ├── compliance/
│   ├── infrastructure/
│   ├── patterns/
│   ├── pricing/
│   └── product/
├── meta/
├── skills/
├── templates/
├── tests/
└── tools/
```

## Runtime Project Surface

```text
apv-projects/[customer]--[title]--[date]/
├── README.md
├── SUMMARY.md
├── input/
│   ├── raw/
│   └── normalized/
├── working/
├── outputs/
├── evidence/
│   ├── pricing/
│   ├── compliance/
│   └── source/
├── verification/
└── approvals/
```

## Artifact Classes

### Raw Source Artifacts

Purpose:
- preserve original customer and evidence inputs

Examples:
- `input/raw/rfp-original.pdf`
- `input/raw/questionnaire.xlsx`
- `input/raw/card-volume.xlsx`

### Normalized Source Artifacts

Purpose:
- provide markdown/script-readable project inputs

Examples:
- `input/normalized/rfp.md`
- `input/normalized/questionnaire.md`
- `input/normalized/card-volume.md`
- `input/normalized/requirements-summary.md`
- `input/normalized/volume-summary.md`
- `input/normalized/sales-brief.md`

### Working Artifacts

Purpose:
- capture grounded intermediate outputs between stages

Examples:
- `working/00-run-context.json`
- `working/01-brainstorm-context.md`
- `working/02-compliance-map.md`
- `working/03-architecture-decision-log.md`
- `working/04-sizing-record.md`
- `working/05-pricing-manifest.md`
- `working/05-assumption-log.md`
- `working/05-gap-log.md`

### Run Context Artifacts

Purpose:
- capture machine-readable governance state for a specific project run

Examples:
- `working/00-run-context.json`

Typical fields:
- `mode`
- `promotion_state`
- `sales_brief_present`
- `sales_brief_approved`
- `release_eligible`
- `current_blocker`
- `promotion_path`
- `promotion_attestation`

### Stage Output Artifacts

Purpose:
- store the primary user-facing result of each stage
- surface run-level metadata such as whether the output is draft-only or release-eligible

Examples:
- `outputs/01-brainstorm.md`
- `outputs/02-compliance.md`
- `outputs/03-architecture.md`
- `outputs/04-sizing.md`
- `outputs/05-pricing.md`
- `outputs/06-response.md`
- `outputs/07-approval.md`

### Evidence Artifacts

Purpose:
- support claims with captured source evidence

Examples:
- `evidence/pricing/aws/calculator-2026-04-29.png`
- `evidence/pricing/aws/pricing-evidence.md`
- `evidence/compliance/pci-dss/req-3-2026-04-29.pdf`
- `evidence/source/url-capture-index.md`

### Verification Artifacts

Purpose:
- record deterministic checks and freshness state

Examples:
- `verification/source-url-validation.json`
- `verification/freshness-report.json`
- `verification/artifact-completeness.md`

### Approval Artifacts

Purpose:
- capture review outcomes and release decisions

Examples:
- `approvals/unified-checklist.md`
- `approvals/reviewer-notes.md`
- `approvals/release-decision.md`

## Naming Rules

- Use two-digit numeric prefixes for ordered stage files.
- Use `00-` prefixes for pre-stage governance and boundary artifacts.
- Use lowercase kebab-case for non-stage artifacts.
- Include dates in evidence captures where freshness matters.
- Use `summary`, `record`, `manifest`, `map`, `log`, and `decision` suffixes consistently.

## Promotion Rule

If a project artifact becomes reusable beyond one RFP, promote it into `wiki/apv-v2/knowledge/` as a curated knowledge page rather than leaving it buried only inside a project folder.

When a project transitions from `draft` to `submission`, the governance artifacts become part of the runtime boundary for that run:

- `working/00-run-context.json`
- `input/normalized/sales-brief.md`

Promotion may also require rerunning downstream stages if the new sales intent materially changes strategy.
