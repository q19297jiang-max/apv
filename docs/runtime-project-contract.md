---
type: apv-meta
category: documentation
title: "APV Runtime Project Contract"
created: 2026-04-26
tags: [apv, runtime, project-structure, workflow]
sources:
  - "[[apv-user-guide]]"
  - "[[apv-project-folder-structure-guide]]"
---

# APV Runtime Project Contract

This document defines the canonical filesystem contract for an APV RFP run.

## Canonical Root

Each RFP run lives in exactly one project folder:

```text
apv-projects/[customer]--[title]--[date]/
```

All APV workflow artifacts for that run should live inside that folder.

## Canonical Layout

```text
apv-projects/[customer]--[title]--[date]/
├── README.md
├── SUMMARY.md
├── input/
├── outputs/
│   ├── 01-brainstorm.md
│   ├── 02-compliance.md
│   ├── 03-architecture.md
│   ├── 04-sizing.md
│   ├── 05-pricing.md
│   ├── 06-response.md
│   └── 07-approval.md
├── evidence/
│   ├── pricing/
│   ├── compliance/
│   └── verification/
└── approvals/
    ├── stage-1-requirements.md
    ├── stage-2-compliance.md
    ├── stage-3-architecture.md
    ├── stage-4-sizing.md
    └── stage-5-pricing.md
```

## Contract Rules

1. `input/` stores source documents and converted markdown inputs.
2. `outputs/` stores skill outputs and final customer-facing response artifacts.
3. `evidence/` stores pricing, compliance, and verification support material.
4. `approvals/` stores stage-gate or reviewer artifacts used during internal review.
5. Active APV workflow docs should not direct runtime output to `apv-output/` or `.rfp-session/`.

## Notes

- Older documents may still refer to `apv-output/` or `.rfp-session/` as historical contracts.
- For current workflow guidance, this document overrides those older runtime path references.