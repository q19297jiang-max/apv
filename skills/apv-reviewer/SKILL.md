---
name: apv-reviewer
description: Stage 7 — Unified approval verification for RFP responses with evidence and freshness checks
version: 2.0
created: 2026-05-01
tags: [apv, v2, reviewer, approval, stage-7]
---

# APV Reviewer (Stage 7)

## Purpose

Final quality gate before RFP response release. Verifies source URL compliance, pricing freshness, evidence completeness, and output class trace rules. Produces an approval decision: APPROVED, CONDITIONAL, or REJECTED.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 7`

Required:
- `outputs/06-response.md`

## Verification Checklist

### 1. Source URL Compliance
For every evidence-backed claim in `outputs/06-response.md`:
- [ ] Source URL is present
- [ ] Source URL format is valid
- [ ] Source URL matches knowledge page frontmatter
- Run: `python3 tools/validate_urls.py` (when available)
- Result → `verification/source-url-validation.json`

### 2. Pricing Freshness
- [ ] All pricing data within freshness threshold
- [ ] Read `verification/freshness-report.json` from Stage 5
- [ ] Any stale pricing flagged with assumption
- Threshold: pricing knowledge `freshness_days: 30`

### 3. Evidence Completeness
- [ ] All compliance claims have evidence references in `evidence/compliance/`
- [ ] All pricing claims have evidence references in `evidence/pricing/`
- [ ] Evidence artifacts exist and are non-empty

### 4. Output Class Trace Rule
- [ ] No claim in final response rests solely on `exploratory` output
- [ ] Every factual claim traceable through `evidence-backed` or `derived` chain
- [ ] Stage frontmatter `output_class` is consistent

### 5. Assumption & Gap Review
- [ ] `working/05-assumption-log.md` — all assumptions reflected in response
- [ ] `working/00-gap-log.md` — unresolved gaps noted as caveats
- [ ] No BLOCKER-severity gaps remain unresolved

### 6. Document Quality
- [ ] Numbers consistent across sections (sizing ↔ pricing)
- [ ] No placeholder text ("TBD", "TODO", "fill in")
- [ ] Professional tone, no internal notes exposed

## Approval Decisions

### APPROVED ✅
All checks pass. Response is ready for release.

### CONDITIONAL ⚠️
Minor issues found that can be fixed:
- Stale pricing with documented assumption
- Low-severity gaps with documented caveats
- Formatting issues

**Action**: List specific fixes required. Allow re-run from specific stage.

### REJECTED ❌
Critical issues found:
- Missing source URLs on evidence-backed claims
- BLOCKER-severity gaps unresolved
- Output class trace violation (exploratory-only claims as facts)
- Pricing data significantly stale with no assumption

**Action**: Halt release. Identify which stage(s) need re-run.

## Process

### 1. Read All Inputs
```
outputs/06-response.md              → the response to review
outputs/01-05-*.md                  → upstream outputs for tracing
verification/source-url-validation.json  → URL check results
verification/freshness-report.json       → freshness status
working/05-assumption-log.md        → assumptions
working/00-gap-log.md               → gaps
```

### 2. Execute Checklist
Run each verification check. For each failure:
- Record: check name, severity (BLOCKER/HIGH/LOW), description, remediation

### 3. Produce Decision
- 0 failures → APPROVED
- Only LOW/HIGH failures → CONDITIONAL (list fixes)
- Any BLOCKER → REJECTED

## Outputs

### Primary Output: `outputs/07-approval.md`
```markdown
---
stage: 7
created: YYYY-MM-DD
decision: APPROVED | CONDITIONAL | REJECTED
---

# Approval Review: [Customer]

## Decision: [APPROVED / CONDITIONAL / REJECTED]

## Checklist Results
| Check | Status | Notes |
|-------|--------|-------|
| Source URL compliance | ✅ | All [N] URLs verified |
| Pricing freshness | ✅ | All within 30-day threshold |
| Evidence completeness | ⚠️ | 2 compliance items missing evidence |
| Output class trace | ✅ | No exploratory-only claims |
| Assumptions reviewed | ✅ | [N] assumptions documented |
| Document quality | ✅ | No issues |

## Issues Found
[If CONDITIONAL or REJECTED]
1. [Issue] — severity: [BLOCKER/HIGH/LOW] — fix: [remediation]

## Recommendation
[Summary recommendation for release]
```

### Approval Artifacts
- `approvals/release-decision.md` — formal release record
- `approvals/reviewer-notes.md` — detailed review notes

## Integration

- **Upstream**: `rfp-generator` (Stage 6)
- **Downstream**: Release decision → human review → delivery
