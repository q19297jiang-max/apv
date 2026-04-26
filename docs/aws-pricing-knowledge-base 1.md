---
type: synthesis
title: "AWS Pricing Knowledge Base Workflow"
created: 2026-04-25
updated: 2026-04-25
tags:
  - aws
  - pricing
  - workflow
  - automation
  - knowledge-base
status: active
related:
  - "[[pricing-automation]]"
  - "[[savings-plans]]"
  - "[[data-freshness]]"
sources:
  - "[[aws-component-catalog]]"
---

# AWS Pricing Knowledge Base Workflow

The most developed pricing workflow in APV today. AWS pricing has the strongest combination of populated catalog content, repo-local scripts, and documented freshness rules, but it should still be treated as a manually operated workflow with script support rather than a fully automated pricing pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SOURCE OF TRUTH                           │
│  aws-component-catalog.md                                   │
│  - Manually updated with calculator-verified pricing         │
│  - Single source of truth for all AWS pricing               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  pricing-fetcher-generic.py                                 │
│  - Parses catalog dynamically (no hardcoded values)         │
│  - Generates aws.md from catalog                            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  pricing-format-validator.py                                │
│  - Validates table format compliance                        │
│  - Checks for required columns                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Base                                             │
│  wiki/apv/knowledge/pricing/aws.md                          │
└─────────────────────────────────────────────────────────────┘
```

## Key Principles

1. **Single Source of Truth**: `aws-component-catalog.md` is the only manual update point
2. **Dynamic Parsing**: No hardcoded values in scripts
3. **Calculator Verification**: All pricing verified in official calculator
4. **Format Standardization**: Consistent table formats across all sections
5. **Freshness Tracking**: 30-day validity with clear expiration
6. **Extensibility**: Easy to add new components or cloud providers

## Quarterly Update Process

### Week 1: Planning & Review
- Review AWS pricing updates from cloud provider
- Identify components needing updates
- Schedule calculator verification sessions

### Week 2: Calculator Verification
1. **Open AWS Pricing Calculator**: https://calculator.aws/
2. **Select Region**: Asia Pacific (Singapore) - ap-southeast-1
3. **Verify Pricing**:
   - EC2 instances (On-Demand)
   - Compute Savings Plans (3yr No Upfront)
   - RDS instances (Single-AZ, Multi-AZ)
   - Database Savings Plans (3yr No Upfront)
   - ElastiCache nodes
   - Cache Savings Plans (3yr No Upfront)
4. **Document Changes**: Record any price differences

### Week 3: Update Catalog
Update `aws-component-catalog.md` with verified pricing and validate format:
```bash
python3 wiki/apv/knowledge/pricing/pricing-format-validator.py --provider aws
```

### Week 4: Regenerate Knowledge Base
```bash
# Generate pricing file from catalog
python3 wiki/apv/knowledge/pricing/pricing-fetcher-generic.py --provider aws

# Commit to knowledge base
cp /tmp/apv-pricing-updates/aws.md wiki/apv/knowledge/pricing/aws.md
```

## Data Freshness Guarantees

### Frontmatter Tracking
Every pricing file includes freshness metadata:
```yaml
---
captured_date: 2026-04-25
verified_by: "Infrastructure Architect"
price_valid_until: 2026-05-25  # 30 days from captured_date
---
```

### Freshness Thresholds

| Pricing Type | Validity | Action Required |
|--------------|----------|-----------------|
| On-Demand | 30 days | Re-verify in calculator |
| Savings Plans | 90 days | Re-verify in calculator |
| Regional multipliers | 180 days | Review quarterly |

### Automated Validation
```python
# Check if pricing is stale
if datetime.now() > price_valid_until:
    warn("Pricing data exceeds 30-day freshness threshold")
    notify("Manual calculator verification required")
```

## Accuracy Assurance Mechanisms

### 1. Calculator Verification
- All pricing must be verified in https://calculator.aws/
- Document calculator configuration in callout blocks
- Include verification date in notes

### 2. Format Validation
The validator checks:
- All tables have "Calculator URL" column
- Required columns present (Instance, Price/Hour, Monthly)
- No forbidden column names (Source, Link, URL)
- Case-insensitive column matching

### 3. Multi-AZ Pricing Validation
Multi-AZ deployments cost 2-3x Single-AZ. Catalog includes explicit warnings:
```markdown
> [!IMPORTANT] Multi-AZ vs Single-AZ Pricing
> **Multi-AZ deployments** include a standby instance and cost
> approximately **2-3x** the Single-AZ price.
```

### 4. Savings Plans Pricing
Savings Plans sections show both prices for transparency:
```markdown
| Instance | On-Demand/Hour | Savings 3yr/Hour | Savings % |
|----------|----------------|-----------------|-----------|
| m6i.xlarge | $0.192 | $0.122 | 36% |
```

## Section Organization

### Hierarchical Structure
The catalog organizes pricing hierarchically:

```
## Compute Components
  #### General Purpose (m6i)
  #### Compute Optimized (c6i)
  #### Memory Optimized (r6i)
  #### Compute Savings Plans (3yr No Upfront)

## Database Components
  #### Single-AZ Instances
  #### Multi-AZ Instances
  #### Database Savings Plans (3yr No Upfront)

## Cache Components
  #### Redis Nodes
  #### Cache Savings Plans (3yr No Upfront)
```

### Dynamic Section Detection
The parser automatically detects section types:
- `ec2` → Compute instances
- `ec2_savings_plans` → Compute Savings Plans
- `rds_single_az` → RDS Single-AZ
- `rds_multi_az` → RDS Multi-AZ
- `rds_savings_plans` → Database Savings Plans
- `elasticache` → Cache nodes
- `elasticache_savings_plans` → Cache Savings Plans

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Script finds 0 items | Section headers not recognized | Check `###` or `####` format |
| Wrong pricing in generated file | Catalog not updated | Update aws-component-catalog.md first |
| Format validation fails | Missing "Calculator URL" column | Add to all tables |
| Multi-AZ pricing wrong | Using Single-AZ price | Verify Multi-AZ in calculator |
| Savings Plans missing | Not added to catalog | Add Savings Plans section |

## System Files

| File | Purpose |
|------|---------|
| `aws-component-catalog.md` | Source of truth for all AWS pricing |
| `pricing-fetcher-generic.py` | Generator script (dynamic parsing) |
| `pricing-format-validator.py` | Validation script |
| `pricing-workflow.md` | Detailed workflow guide |
| `component-catalog-template.md` | Format template |
| `aws.md` | Generated knowledge base file |

## Maintenance Schedule

| Task | Frequency | Owner | Time Estimate |
|------|-----------|-------|---------------|
| Calculator verification | Quarterly | Infrastructure Architect | 2 hours |
| Catalog updates | Quarterly | Infrastructure Architect | 1 hour |
| Format validation | Quarterly | System Architect | 15 minutes |
| Price freshness check | Monthly | Script-assisted manual review | Instant |
| Full workflow test | Quarterly | System Architect | 30 minutes |

## Test Results

The AWS pricing workflow was exercised on 2026-04-25 at the script and content level:

```
📊 Found 60 pricing items across 17 sections
   - ec2: 9 items
   - ec2_savings_plans: 3 items
   - rds_single_az: 6 items
   - rds_multi_az: 3 items
   - rds_savings_plans: 6 items
   - elasticache: 5 items
   - elasticache_savings_plans: 5 items
   - alb: 3 items
   - nlb: 2 items
   - eks: 2 items
   - ebs: 3 items
   - s3: 4 items
   - direct_connect: 2 items
   - vpc_flow_logs: 1 items
   - kms: 2 items
   - shield: 1 items

✅ Format validation passed (14 tables, 0 errors)
✅ Knowledge base updated successfully for AWS
```

## Extensibility

The system is designed to be extensible, but AWS is currently the most developed provider path in this repository:

### Adding New AWS Components
1. Add section to `aws-component-catalog.md`
2. Follow standard table format
3. Run `pricing-fetcher-generic.py`
4. No script changes required

### Adding New Cloud Providers
1. Create `[provider]-component-catalog.md`
2. Add provider config to `PROVIDERS` dict in `pricing-fetcher-generic.py`
3. No other script changes needed
