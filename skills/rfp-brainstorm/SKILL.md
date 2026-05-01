---
name: rfp-brainstorm
description: Stage 1 — Interactive brainstorming to capture RFP intent, strategy, and knowledge gaps
version: 2.0
created: 2026-05-01
tags: [apv, v2, brainstorm, stage-1]
output_class: exploratory
---

# RFP Brainstorm (Stage 1)

## Purpose

Interactive entry point for the APV pipeline. Captures the human's strategic intent, maps it against the knowledge base, identifies gaps, and produces a brainstorm context document that guides all downstream stages.

**Output class: `exploratory`** — findings inform strategy but cannot be cited as evidence in the final response.

## When to Use

- First stage of any RFP response pipeline
- Invoked by `apv-orchestrator` after intake normalization

## Gate Check

Before starting, verify upstream artifacts exist:
- `input/normalized/rfp.md`
- `input/normalized/requirements-summary.md`

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 1`

## Three Input Modes

### Mode A: Documents + Human Direction (Recommended)
Customer documents are normalized AND the human provides strategic direction.
- Read normalized inputs for factual requirements
- Ask the human about: priorities, differentiators, known constraints, past relationship

### Mode B: Documents Only
Customer documents provided but no human available for direction.
- Extract all requirements from normalized inputs
- Make reasonable assumptions, log each one
- Flag decisions that need human review

### Mode C: Human Brief Only
No customer documents — human describes the opportunity verbally.
- Capture: customer name, business type, regions, volumes, key requirements
- Generate a synthetic requirements summary
- Flag: "No source documents — all requirements from verbal brief"

## Process

### 1. Read Normalized Inputs
```
input/normalized/rfp.md
input/normalized/requirements-summary.md
input/normalized/volume-summary.md (if exists)
```

### 2. Extract Key Dimensions
- **Business type**: issuing, acquiring, gateway, digital wallet, mixed
- **Target regions**: countries/jurisdictions
- **Scale**: transaction volumes, peak TPS
- **Compliance**: regulatory requirements (PCI-DSS, country-specific)
- **Infrastructure**: cloud provider preferences, deployment model

### 3. Knowledge Base Lookup
Query `apv-v2.sqlite` or read knowledge files directly:
- `knowledge/compliance/` — applicable regulations for target regions
- `knowledge/card-systems/` — relevant card system architecture
- `knowledge/infrastructure/` — deployment patterns
- `knowledge/sizing/` — TPS methodology

### 4. Identify Gaps
For each dimension, check:
- ✅ Knowledge exists and is fresh → note as "covered"
- ⚠️ Knowledge exists but is stale → log to gap log with severity
- ❌ No knowledge found → log to gap log, flag for human

### 5. Generate Strategic Options
Propose 2-3 approaches covering:
- Architecture approach (monolith vs microservices, cloud choice)
- Compliance strategy (minimal vs comprehensive)
- Deployment model (single-region vs multi-region)
- Build vs partner for specific capabilities

### 6. Clarification Questions
List questions that need customer or internal answers before proceeding.

## Outputs

### Primary Output: `outputs/01-brainstorm.md`
```markdown
---
output_class: exploratory
stage: 1
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
---

# RFP Brainstorm: [Customer] — [Title]

## Executive Summary
[2-3 paragraph strategic overview]

## Key Dimensions
| Dimension | Value | Source |
|-----------|-------|--------|
| Business Type | [type] | [rfp.md / human brief] |
| Regions | [list] | [rfp.md] |
| Peak TPS | [estimate] | [volume-summary.md] |
| ...

## Strategic Options
### Option A: [Name]
[Description, trade-offs, recommendation]

### Option B: [Name]
[Description, trade-offs]

## Knowledge Coverage
| Domain | Status | Notes |
|--------|--------|-------|
| Compliance | ✅ Covered | PCI-DSS + [N] country regs |
| Card Systems | ✅ Covered | [types] |
| Pricing | ⚠️ Stale | Last verified [date] |
| ...

## Gaps & Assumptions
[From gap log]

## Clarification Questions
1. [Question] — needed for [downstream stage]
```

### Working Artifact: `working/01-brainstorm-context.md`
Internal context captured during brainstorming — not included in final response.

### Gap Log: `working/00-gap-log.md` (initial entries)
```markdown
# Knowledge Gap Log

| # | Domain | Description | Severity | Stage Found | Resolved |
|---|--------|-------------|----------|-------------|----------|
| 1 | pricing | AWS pricing stale (45 days) | HIGH | brainstorm | No |
```

## Integration

- **Upstream**: `apv-orchestrator` (invokes after intake)
- **Downstream**: `rfp-compliance` (Stage 2) consumes `outputs/01-brainstorm.md`
- **Cross-stage**: Gap log is appended to by all subsequent stages
