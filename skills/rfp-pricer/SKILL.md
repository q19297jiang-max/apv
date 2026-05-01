---
name: rfp-pricer
description: Stage 5 — Calculate evidence-backed pricing from sized components with source URL enforcement
version: 2.0
created: 2026-05-01
tags: [apv, v2, pricing, stage-5]
output_class: evidence-backed
---

# RFP Pricing (Stage 5)

## Purpose

Calculate infrastructure costs for all sized components using verified pricing data. Every price must cite an official source URL. Produces a pricing manifest with full traceability.

**Output class: `evidence-backed`** — all prices must reference verified `source_url` entries.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 5`

Required:
- `outputs/03-architecture.md`
- `outputs/04-sizing.md`

## Critical Rules

### Source URL Enforcement (MANDATORY)
- Every price MUST cite an official source URL (e.g., AWS pricing page, calculator)
- If no verified price exists → log to gap log, use placeholder with UNVERIFIED flag
- NEVER fabricate pricing or use unverified numbers

### Freshness Check
- Before pricing, check `knowledge/pricing/*.md` frontmatter for `last_verified`
- If pricing is stale (> freshness_days): log to assumption log, flag in output
- Generate `verification/freshness-report.json`

### Commercial Overrides
- Check `working/05-commercial-overrides.md` if it exists
- Overrides MUST have `approved_by` and `valid_until` fields
- Overrides take precedence over catalog pricing

## Process

### 1. Read Upstream Context
- `outputs/03-architecture.md` — component list
- `outputs/04-sizing.md` — instance types, counts, storage
- `knowledge/pricing/*.md` — verified pricing data

### 2. Price Each Component
For each sized component:
1. Look up pricing from `knowledge/pricing/[provider].md`
2. Apply pricing model: on-demand (default) or Savings Plans if specified
3. Calculate: monthly_cost = hourly_price × 730 hours × instance_count
4. Record source_url from knowledge page frontmatter
5. If Multi-AZ: apply appropriate multiplier

### 3. Generate Pricing Summary
- Group by category (compute, database, network, storage, support)
- Calculate subtotals and grand total
- Show monthly and annual costs
- Note any assumptions or estimated prices

### 4. Create Evidence Artifacts
- `evidence/pricing/[provider]-lookup-[date].md` — pricing evidence
- `verification/freshness-report.json` — freshness status of all pricing data

### 5. Log Assumptions & Gaps
- Missing prices → gap log (severity: HIGH)
- Stale prices → assumption log with date and % risk
- Estimated prices → assumption log with basis

## Outputs

### Primary Output: `outputs/05-pricing.md`
```markdown
---
output_class: evidence-backed
stage: 5
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
---

# Pricing Estimate: [Customer]

## Pricing Summary

### Monthly Cost Breakdown
| Category | Monthly (USD) | Annual (USD) | % of Total |
|----------|--------------|--------------|------------|
| Compute | $X,XXX | $XX,XXX | XX% |
| Database | $X,XXX | $XX,XXX | XX% |
| Network | $XXX | $X,XXX | X% |
| Storage | $XXX | $X,XXX | X% |
| Support | $XXX | $X,XXX | X% |
| **Total** | **$XX,XXX** | **$XXX,XXX** | **100%** |

### Detailed Component Pricing
| Component | Type | Count | Hourly | Monthly | Source |
|-----------|------|-------|--------|---------|--------|
| App servers | m6i.xlarge | 4 | $0.192 | $560.64 | [source_url] |
| Primary DB | db.r6g.xlarge | 2 | $0.48 | $700.80 | [source_url] |

### Pricing Model
- Base: On-Demand pricing
- Savings Plans: [if applicable, show comparison]

## Assumptions
[From working/05-assumption-log.md]

## Freshness Status
| Source | Last Verified | Freshness | Status |
|--------|--------------|-----------|--------|
| AWS pricing | 2026-04-28 | 30 days | ✅ Fresh |

## Evidence
- `evidence/pricing/aws-lookup-2026-05-01.md`
```

### Working Artifacts
- `working/05-pricing-manifest.md` — detailed calculation worksheet
- `working/05-assumption-log.md` — all pricing assumptions
- `working/05-gap-log.md` — pricing gaps (appends to `working/00-gap-log.md`)

### Evidence Artifacts
- `evidence/pricing/[provider]-lookup-[date].md`

### Verification Artifacts
- `verification/freshness-report.json`

## Knowledge Sources

- `knowledge/pricing/aws.md` — AWS pricing for Singapore
- `knowledge/pricing/azure.md` — Azure pricing
- `knowledge/pricing/gcp.md` — GCP pricing
- `knowledge/pricing/aws-component-catalog.md` — detailed component catalog

## Integration

- **Upstream**: `rfp-architect` (Stage 3), `rfp-calculator` (Stage 4)
- **Downstream**: `rfp-generator` (Stage 6) includes pricing in final response
