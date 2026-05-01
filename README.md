---
type: page
title: "APV V2"
created: 2026-04-29
tags: [apv, v2, wiki-first, artifact-pipeline]
---

# APV V2

## Overview

APV V2 is a clean restart of the APV system using a wiki-first, repo-governed, artifact-based operating model.

The design goal is to keep markdown artifacts as the canonical business data while making execution, verification, pricing evidence, and approval flow deterministic enough for long-term operation.

## Core Principles

- Wiki markdown files and related project files are the canonical project data.
- Git carries the full project artifact set and operational history.
- Scripts perform deterministic transformations and validation.
- Skills operate on explicit artifacts, not loose prompt context alone.
- Every RFP run is traceable through a complete artifact chain.

## Core Design Documents

- [docs/authority-model.md](docs/authority-model.md) — canonical data and authority rules
- [docs/artifact-model.md](docs/artifact-model.md) — artifact classes, names, and folder layout
- [docs/stage-contracts.md](docs/stage-contracts.md) — skill consumes/emits contracts
- [docs/aws-pricing-artifact-model.md](docs/aws-pricing-artifact-model.md) — AWS pricing manifests, evidence, freshness, and promotion
- [docs/orchestration-model.md](docs/orchestration-model.md) — repo-governed execution flow and gates

## Scaffold

```text
wiki/apv-v2/
├── README.md
├── approvals/
├── docs/
│   ├── authority-model.md
│   ├── artifact-model.md
│   ├── aws-pricing-artifact-model.md
│   ├── orchestration-model.md
│   ├── stage-contracts.md
│   └── plans/
├── evidence/
├── knowledge/
│   └── pricing/
├── meta/
│   └── system-index.md
├── skills/
├── templates/
├── tests/
└── tools/
```

## Runtime Boundary

APV V2 design uses two coordinated surfaces:

- `wiki/apv-v2/` for reusable knowledge, contracts, tooling, and design docs
- `apv-projects/[customer]--[title]--[date]/` for per-RFP artifact sets

APV V2 is therefore not just a wiki and not just a project runner. It is a knowledge system with repo-governed project execution.