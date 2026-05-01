---
type: apv-meta
category: documentation
title: Pricing Workflow Guide
created: 2026-04-25
tags: [pricing, workflow, guide]
status: active
freshness_days: 30
last_verified: null
---

# Cloud Pricing Workflow Guide

## Overview

This workflow ensures accurate, up-to-date pricing for all cloud components (AWS, Azure, GCP) with minimal manual effort and maximum automation.

> [!NOTE] Current V2 implementation boundary
> `tools/pricing_fetcher.py` currently checks freshness metadata and prints a manual refresh plan. The V2 repo does not currently ship `pricing-verify.py`, `pricing-commit.py`, or a generic pricing fetcher that pulls live calculator values automatically.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SOURCE OF TRUTH                           │
│  [provider]-component-catalog.md                            │
│  - Manually updated with calculator-verified pricing         │
│  - Follows component-catalog-template.md format             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  pricing-fetcher.py (FRESHNESS + REFRESH PLAN)               │
│  - Reads pricing page metadata                               │
│  - Flags stale/expired pricing                               │
│  - Generates manual calculator refresh steps                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Local validation scripts                                    │
│  - freshness.py checks freshness windows                     │
│  - validate_urls.py checks URL format                        │
│  - knowledge_audit.py checks markdown hygiene                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Manual catalog update + sync_db.py                          │
│  - Operator updates component catalog                        │
│  - Evidence is stored alongside the update                   │
│  - sync_db.py rebuilds the local index                       │
└─────────────────────────────────────────────────────────────┘
```

## Adding New Cloud Providers

### 1. Create Provider Catalog

```bash
wiki/apv/knowledge/pricing/
├── aws-component-catalog.md
├── azure-component-catalog.md
├── gcp-component-catalog.md
└── [new-provider]-component-catalog.md
```

### 2. Update pricing-fetcher.py

Add provider configuration:

```python
PROVIDERS = {
    'aws': {
        'catalog_file': 'aws-component-catalog.md',
        'calculator_url': 'https://calculator.aws/',
        'regions': {'ap-southeast-1': 'Singapore'}
    },
    'azure': {
        'catalog_file': 'azure-component-catalog.md',
        'calculator_url': 'https://azure.microsoft.com/pricing/',
        'regions': {'southeastasia': 'Singapore'}
    },
    'gcp': {
        'catalog_file': 'gcp-component-catalog.md',
        'calculator_url': 'https://cloud.google.com/products/calculator',
        'regions': {'asia-southeast1': 'Singapore'}
    }
}
```

### 3. Current Script Status

Current V2 behavior is simpler than the target workflow:
- pricing catalogs are curated manually
- `pricing_fetcher.py` checks freshness metadata only
- `sync_db.py` rebuilds the local index after catalog updates
- no generic live-pricing importer is currently implemented in `wiki/apv-v2/tools/`

## Quarterly Update Workflow

### Week 1: Planning
- [ ] Review pricing updates from cloud providers
- [ ] Identify components needing updates
- [ ] Schedule calculator verification sessions

### Week 2: Calculator Verification
- [ ] Open https://calculator.[cloud].com
- [ ] Select target region
- [ ] Verify pricing for critical components
- [ ] Document any pricing changes

### Week 3: Catalog Updates
- [ ] Update [provider]-component-catalog.md
- [ ] Follow component-catalog-template.md format
- [ ] Add Calculator URL to all tables
- [ ] Include regional multipliers

### Week 4: Regenerate Pricing Files
```bash
# For each provider with updates:
python tools/pricing_fetcher.py --knowledge-dir knowledge
python tools/sync_db.py --knowledge-dir knowledge --db-path apv-v2.sqlite
python tools/freshness.py --db apv-v2.sqlite --domain pricing --json
```

## Savings Plans Verification

### AWS Savings Plans Types

AWS offers multiple Savings Plans types that provide significant discounts:

| Savings Plan Type | Commitment | Discount | Applies To |
|-------------------|------------|----------|------------|
| Compute Savings Plans | 1 or 3 years | Up to 72% | EC2, Fargate, Lambda |
| Database Savings Plans | 1 or 3 years | Up to 51% | RDS, ElastiCache, DocumentDB |
| SageMaker Savings Plans | 1 or 3 years | Up to 64% | SageMaker |

### Verification Process

1. **Open AWS Pricing Calculator**
   - Navigate to https://calculator.aws/
   - Select region (e.g., Asia Pacific (Singapore))
   - Choose "Savings Plans" from left menu

2. **Configure Savings Plan**
   - Select plan type (Compute, Database, or SageMaker)
   - Set commitment term (3 years No Upfront for maximum savings)
   - Configure workload (Consistent for predictable usage)

3. **Verify Pricing**
   - Select instance types (e.g., m6i.xlarge, db.m6i.xlarge)
   - Compare On-Demand vs Savings Plan price
   - Document monthly cost and savings percentage

4. **Update Catalog**
   - Add calculator-verified Savings Plans section to component catalog
   - Include both On-Demand and Savings Plan prices
   - Document savings percentage and monthly cost

### Savings Plans Section Format

Add to [provider]-component-catalog.md:

```markdown
#### [Service] Savings Plans (3yr No Upfront)

> [!NOTE] Calculator-Verified Savings Plans Pricing
> Savings Plans pricing below was verified on YYYY-MM-DD from https://calculator.aws/
> **3-year commitment required** for these prices.
> Calculator Configuration: Region: [region], Engine: [engine if applicable]

| Instance | vCPU | Memory | On-Demand/Hour | Savings 3yr/Hour | Monthly (730h) | Savings % | Calculator URL |
|----------|------|--------|----------------|-----------------|---------------|-----------|----------------|
| [instance-name] | [vcpu] | [memory] | $[ondemand-price] | $[savings-price] | $[monthly-cost] | [savings%] | https://calculator.aws/ |
```

### Current V2 Handling

Savings Plans sections are currently maintained as curated markdown in the pricing catalog.
There is no implemented V2 parser that automatically imports Savings Plans data from calculator output.

### Common Mistakes

❌ **Wrong**: Mixing On-Demand and Savings Plans pricing in same table
❌ **Wrong**: Using 1-year pricing instead of 3-year
❌ **Wrong**: Forgetting to document calculator configuration

✅ **Correct**: Separate Savings Plans section with both prices shown
✅ **Correct**: Using 3-year No Upfront for maximum savings comparison
✅ **Correct**: Documenting exact calculator configuration for reproducibility

## Format Validation Rules

### Table Format Requirements

1. **Calculator URL Column**: REQUIRED for all tables
2. **Pricing Column**: Must use "Price/Hour" or "Price" format
3. **Monthly Cost**: Required format "Monthly (730h)"
4. **Source Attribution**: Must include official pricing URL

### Common Format Violations

❌ **Wrong**:
```markdown
| Instance | vCPU | Memory | Cost | Source |
|----------|------|--------|------|--------|
```

✅ **Correct**:
```markdown
| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|------------|----------------|----------------|
```

### Section Header Requirements

❌ **Wrong**:
```markdown
## Pricing
## Database
```

✅ **Correct**:
```markdown
### RDS Pricing (Single-AZ)
### RDS Pricing (Verified from Calculator)
```

## Troubleshooting

### Issue: Script finds 0 items

**Cause**: Section headers not recognized

**Solution**: 
- Check section headers follow format: `### [Component] [Type]`
- Ensure tables have proper column headers
- Verify table rows have enough columns

### Issue: Missing Calculator URL column

**Cause**: Table format doesn't follow template

**Solution**:
- Add Calculator URL column to all tables
- Use "Calculator URL" not "Source" or "Link"

### Issue: Wrong pricing in generated file

**Cause**: Catalog not updated as source of truth

**Solution**:
- Update [provider]-component-catalog.md first
- Re-run pricing-fetcher.py
- Verify catalog has correct pricing

## Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Calculator verification | Quarterly | Infrastructure Architect |
| Catalog updates | Quarterly | Infrastructure Architect |
| Price validity check | Monthly | Automated |
| Script validation | Quarterly | System Architect |

## Related

- [[component-catalog-template]] - Component catalog format template
- [[aws-component-catalog]] - AWS catalog example
- [[pricing-accuracy]] - Pricing accuracy requirements
