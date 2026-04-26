---
type: apv-meta
category: status
title: "APV Refactor Status Summary"
created: 2026-04-26
tags: [apv, refactor, status, summary]
sources:
  - "[[current-state-status]]"
  - "[[runtime-project-contract]]"
  - "[[pilot-test-report]]"
  - "[[integration-test-report]]"
---

# APV Refactor Status Summary

This summary captures the outcome of the documentation and workflow truth-gap refactor completed on 2026-04-26.

## What Changed

- Top-level APV docs now distinguish current validated capability from target-state workflow design.
- APV has a canonical runtime contract under `apv-projects/[customer]--[title]--[date]/`.
- Operations, verification, and evidence docs now describe the current workflow as manual or script-assisted where appropriate.
- Pricing docs now distinguish the stronger AWS path from lighter Azure and GCP reference snapshots.
- Integration and pilot test docs now state their real scope more precisely.
- A small automated guardrail now protects against reintroducing specific unqualified readiness claims.

## Current Classification

### Validated

- Brainstorm and compliance have real pilot evidence.
- Contract-level integration checks run successfully as a scoped documentation and asset check.
- Documentation truthfulness guardrail test passes.

### Manual Or Script-Assisted

- End-to-end APV workflow execution
- Source URL verification operations
- Evidence capture and freshness review
- Pricing evidence capture for live proposals

### Planned Or Partial

- Full multi-skill real-RFP validation for architecture, sizing, pricing, generator, and reviewer
- Scheduler-based automation for verification and monitoring
- A stronger end-to-end integration runner based on APV project outputs rather than skill-file inspection
- A fully workflow-backed Azure and GCP pricing process comparable to AWS

## Recommended Next Steps

1. Run a full real-RFP execution through the remaining unvalidated skills.
2. Decide whether APV should become a truly automated runtime or remain a guided operator workflow.
3. Upgrade integration testing from contract-level checks to output-based end-to-end checks.
4. Complete the pricing workflow for Azure and GCP or explicitly scope APV pricing to AWS-first.

## Bottom Line

APV now presents itself more honestly: strong as a design and guided workflow repository, partially validated in practice, and not yet a fully operational automated RFP platform.