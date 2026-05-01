---
name: rfp-generator
description: Stage 6 — Assemble final RFP response from all stage outputs with traceability
version: 2.0
created: 2026-05-01
tags: [apv, v2, generator, response, stage-6]
output_class: derived
---

# RFP Response Generator (Stage 6)

## Purpose

Assemble the final RFP response document from all upstream stage outputs (1-5). Ensures no unsupported claims, all facts are traceable, and the document follows professional RFP response conventions.

**Output class: `derived`** — all content traceable to evidence-backed or derived upstream outputs.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 6`

Required:
- `outputs/01-brainstorm.md`
- `outputs/02-compliance.md`
- `outputs/03-architecture.md`
- `outputs/04-sizing.md`
- `outputs/05-pricing.md`

## Critical Rules

### No Unsupported Claims
- Every factual statement MUST be traceable to a stage output
- Claims from `exploratory` (Stage 1) may appear as background/context only, NEVER as evidence
- Claims from `evidence-backed` (Stages 2, 5) can be cited directly
- Claims from `derived` (Stages 3, 4) are traceable through their upstream evidence

### Assumption Transparency
- Read `working/05-assumption-log.md` — include relevant assumptions in the response
- Read `working/00-gap-log.md` — note any unresolved gaps as caveats

### Output Trace Rule
No claim in the final response may rest solely on `exploratory` output. Every factual claim must trace back through at least one `evidence-backed` or `derived` stage.

## Process

### 1. Read All Stage Outputs
```
outputs/01-brainstorm.md     → strategic context
outputs/02-compliance.md     → compliance mapping
outputs/03-architecture.md   → architecture design
outputs/04-sizing.md         → infrastructure sizing
outputs/05-pricing.md        → cost estimates
working/05-assumption-log.md → assumptions
working/00-gap-log.md        → knowledge gaps
```

### 2. Structure Response
Follow standard RFP response structure:
1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution (architecture)
4. Compliance & Security
5. Infrastructure & Sizing
6. Pricing & Commercial Terms
7. Implementation Timeline
8. Assumptions & Caveats
9. Appendices

### 3. Assemble Content
For each section:
- Extract relevant content from stage outputs
- Rewrite for professional tone and consistency
- Add cross-references between sections
- Ensure source URLs are preserved for evidence-backed claims

### 4. Quality Checks
Before finalizing:
- Verify no orphan claims (every fact traced to a stage)
- Check consistency (numbers match between sections)
- Ensure assumptions section is complete
- Verify no exploratory-only claims in factual sections

## Outputs

### Primary Output: `outputs/06-response.md`
```markdown
---
output_class: derived
stage: 6
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
sources:
  - outputs/01-brainstorm.md
  - outputs/02-compliance.md
  - outputs/03-architecture.md
  - outputs/04-sizing.md
  - outputs/05-pricing.md
---

# RFP Response: [Customer] — [Title]

## 1. Executive Summary
[Strategic overview from brainstorm, key value propositions]

## 2. Understanding of Requirements
[Customer requirements as understood, from normalized inputs]

## 3. Proposed Solution
[Architecture from Stage 3, including diagrams]

## 4. Compliance & Security
[Compliance mapping from Stage 2, with source URLs]

## 5. Infrastructure & Sizing
[Sizing from Stage 4, component tables]

## 6. Pricing & Commercial Terms
[Pricing from Stage 5, cost tables with source URLs]

## 7. Implementation Timeline
[Phased delivery plan]

## 8. Assumptions & Caveats
[All assumptions from assumption log]
[Unresolved gaps from gap log]

## Appendices
- A: Detailed Compliance Matrix
- B: Component Pricing Detail
- C: Evidence References
```

## Integration

- **Upstream**: All stages 1-5
- **Downstream**: `apv-reviewer` (Stage 7) reviews this document
