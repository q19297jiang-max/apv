---
type: apv-meta
category: system-documentation
title: "APV V2 System Index"
created: 2026-04-29
tags: [apv, v2, index]
---

# APV V2 System Index

## Purpose

This index tracks the foundational design documents for APV V2.

## Core Documents

| Document | Purpose |
|----------|---------|
| [[authority-model]] | Defines what counts as canonical project data and authority tiers |
| [[artifact-model]] | Defines artifact types, locations, and naming rules |
| [[stage-contracts]] | Defines stage consumes/emits contracts and gates |
| [[aws-pricing-artifact-model]] | Defines AWS pricing manifests, evidence, freshness, and promotion |
| [[orchestration-model]] | Defines repo-governed execution flow and control gates |

## Project Surfaces

| Surface | Role |
|---------|------|
| `wiki/apv-v2/` | Reusable knowledge, contracts, tooling, and documentation |
| `apv-projects/` | Per-RFP runtime artifact sets |

## Design Position

APV V2 uses a wiki-first, repo-governed, artifact-based architecture:

- markdown/files are the source of truth
- git carries the complete project state
- scripts enforce deterministic transformations
- skills consume and emit explicit artifacts

## Related

- [[apv-v2]] — system overview
- [[authority-model]]
- [[artifact-model]]
- [[stage-contracts]]
- [[aws-pricing-artifact-model]]
- [[orchestration-model]]