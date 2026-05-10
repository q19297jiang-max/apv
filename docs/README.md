---
type: apv-meta
category: documentation
title: APV V2 Docs Index
created: '2026-05-02'
tags:
  - apv
  - docs
  - index
---

# APV V2 Docs Index

Use this page as the entry point for the main APV V2 documentation.

## Start Here

- `user-manual.md` — sales and solution-architect guide for running APV V2 projects
- `production-rollout-checklist.md` — operator checklist for production preflight, rollout, and recovery
- `pricing-operator-cheat-sheet.md` — fastest operator reference for AWS pricing maintenance
- `../knowledge/pricing/pricing-workflow.md` — full AWS pricing operator playbook

If you are working with live delivery readiness, read the user manual and rollout checklist with the run-authority model in mind:

- projects default to **draft** mode
- draft runs are useful for internal acceleration but are **not release-eligible**
- use `./bin/apv promote-to-submission ...` when a draft project becomes a governed submission candidate

## Core Design Docs

- `artifact-model.md` — artifact layout and file classes
- `authority-model.md` — canonical source and edit rules
- `orchestration-model.md` — stage execution and runtime contract
- `aws-pricing-artifact-model.md` — pricing-specific artifact and assurance model
- `stage-contracts.md` — stage-level consumes/emits contracts, including governance-sensitive stage behavior

## Planning And Specs

- `plans/` — implementation plans and working design notes
- `superpowers/specs/` — larger system design specifications
- `superpowers/reviews/` — implementation reviews and boundary assessments
