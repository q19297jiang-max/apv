---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, pricing]
source: .claude/skills/rfp-pricer
---

# rfp-pricer Skill

## Overview

Generate accurate cost estimates for RFP responses by applying official pricing from cloud provider calculators. Enforces 100% source URL compliance for all pricing claims.

## Purpose

- Apply official pricing from cloud calculators
- Generate cost breakdown with source URLs
- Store pricing evidence (screenshots)
- Calculate TCO (1-year and 3-year)

## When to Use

- After [[rfp-calculator-skill]] has determined component sizing
- When generating cost estimates for proposals
- When comparing pricing across cloud providers
- When validating pricing estimates against official calculators

## Inputs

Receives from previous skills:
- [[rfp-calculator-skill]]: Component sizing, instance counts, by region
- [[rfp-architect-skill]]: Infrastructure selection, cloud provider choice

## Outputs

1. **Cost Breakdown**: Detailed costs by component, region, and provider
2. **Pricing Evidence**: Source URLs for all pricing claims
3. **Cost Optimization**: Recommendations for cost savings
4. **Total Cost of Ownership**: 1-year and 3-year projections
5. **Price Comparison**: Compare across providers (if applicable)

## Knowledge Sources

- `wiki/apv/knowledge/pricing/` - Official pricing data with calculator URLs
- `wiki/apv/knowledge/infrastructure/` - Instance specifications for pricing

## CRITICAL: Source URL Enforcement

**ALL pricing claims MUST have source URLs**:
1. **Pricing Source**: Use official cloud calculator URLs
2. **Evidence Screenshot**: Store calculator screenshots in `evidence/pricing/`
3. **Freshness**: Pricing must be verified within 30 days
4. **Verification**: Include `last_verified` date for all pricing

## Cost Calculation Formula

```
Component Cost = (Instance Cost × Hours/Month × Instance Count) + Additional Costs

Where:
- Instance Cost: From official calculator
- Hours/Month: 730 (24 × 30.416)
- Instance Count: From rfp-calculator output
- Additional Costs: Storage, data transfer, support, etc.
```

## Usage

```
/skill rfp-pricer --rfp <path> --provider aws
```

## Integration

Receives from:
- [[rfp-calculator-skill]] - Component sizing
- [[rfp-architect-skill]] - Cloud provider selection

Sends to:
- [[rfp-generator-skill]] - Cost tables for proposal

## Related

- [[rfp-calculator-skill]] - Component sizing
- [[rfp-generator-skill]] - Proposal document generation
- [[apv-orchestrator-skill]] - Complete skill chain
