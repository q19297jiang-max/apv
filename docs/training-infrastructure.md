---
type: apv-meta
category: documentation
title: "APV Infrastructure Architect Training Guide"
created: 2026-04-24
tags: [apv, documentation, training, infrastructure]
---

# APV Infrastructure Architect Training Guide

**Audience**: Infrastructure Architects
**Duration**: 30 minutes
**Prerequisites**: Understanding of cloud infrastructure and sizing

---

## Learning Objectives

After this training, you will be able to:
1. Understand APV's sizing calculation process
2. Review TPS calculations
3. Validate infrastructure sizing
4. Verify cost estimates
5. Approve infrastructure recommendations

---

## APV Infrastructure Process

### Skill 4: rfp-calculator

**Purpose**: Calculate precise infrastructure sizing

**Input**: RFP document + architecture output

**Output**: Sizing calculations with capacity planning

**Time**: 5-10 minutes

**What it does**:
- Calculates TPS from transaction volumes
- Sizes compute instances
- Plans capacity for growth
- Configures auto-scaling
- Calculates resource requirements by region

### Skill 5: rfp-pricer

**Purpose**: Generate cost estimates with calculator URLs

**Input**: RFP document + calculator output

**Output**: Detailed cost breakdown with source URLs

**Time**: 5-10 minutes

**What it does**:
- Generates pricing for AWS/Azure/GCP
- Calculates compute, database, storage, data transfer costs
- Includes optimization opportunities
- Provides 3-year cost projections

---

## TPS Calculation Formulas

### Basic Formulas

```
Average TPS = Daily Transactions / 86,400
Peak TPS = Average TPS × 4 (default peak multiplier)
```

### From Card Volumes

```
Total Transactions = Σ(Cards × PV per Card)
Daily Transactions = Total Transactions / 365
Average TPS = Daily Transactions / 86,400
```

### Capacity Planning

```
Min Instances = (Average TPS / TPS per Instance) + 1
Max Instances = (Peak TPS × 1.5) / TPS per Instance
```

---

## Sizing Reference

### TPS per Instance

| Instance Type | TPS Capacity | Use Case |
|---------------|--------------|----------|
| Small (t3.medium) | 10-50 TPS | Low volume |
| Medium (m5.large) | 50-200 TPS | Medium volume |
| Large (m5.xlarge) | 200-500 TPS | High volume |

### Database Sizing

| TPS | DB Instance | Storage |
|-----|-------------|---------|
| < 10 | db.t3.medium | 100 GB |
| 10-50 | db.m5.large | 500 GB |
| 50-200 | db.m5.xlarge | 1 TB |
| > 200 | db.m5.2xlarge | 2 TB+ |

---

## Sizing Review Checklist

### Step 1: Review TPS Calculations

**File**: `outputs/04-sizing.md`

**Check**:
- [ ] Transaction volumes correct
- [ ] Daily calculations accurate
- [ ] Peak multiplier appropriate (4x default)
- [ ] TPS formulas applied correctly

### Step 2: Validate Instance Sizing

**Check**:
- [ ] Instance type matches TPS requirements
- [ ] Min/max instances configured correctly
- [ ] Auto-scaling configured
- [ ] Headroom for growth included

### Step 3: Review Database Sizing

**Check**:
- [ ] DB instance sized for TPS
- [ ] Storage adequate for data volume
- [ ] IOPS requirements met
- [ ] Backup storage included

### Step 4: Verify Network Sizing

**Check**:
- [ ] Bandwidth adequate for TPS
- [ ] Data transfer costs estimated
- [ ] Network architecture supports volume
- [ ] Latency requirements met

### Step 5: Review Cost Estimates

**File**: `outputs/05-pricing.md`

**Check**:
- [ ] All components priced
- [ ] Calculator URLs included
- [ ] 3-year projection provided
- [ ] Optimization opportunities noted

---

## Cost Calculator URLs

### AWS Calculator

**URL**: https://calculator.aws/

**Components**:
- EC2/EKS: Compute costs
- RDS: Database costs
- S3: Storage costs
- Data Transfer: Network costs

### Azure Calculator

**URL**: https://azure.microsoft.com/pricing/calculator/

**Components**:
- AKS/VMs: Compute costs
- Database: Database costs
- Storage: Storage costs
- Bandwidth: Network costs

### GCP Calculator

**URL**: https://cloud.google.com/products/calculator/

**Components**:
- GKE: Compute costs
- Cloud SQL: Database costs
- Cloud Storage: Storage costs
- Network: Network costs

---

## Cost Optimization

### Optimization 1: Reserved Instances

**When**: 1-3 year commitment possible

**Savings**: 30-60% vs on-demand

**Use For**: Base workload (not auto-scaled instances)

### Optimization 2: Spot Instances

**When**: Fault-tolerant workloads

**Savings**: 60-90% vs on-demand

**Use For**: Batch processing, non-critical workloads

### Optimization 3: Right-Sizing

**When**: Over-provisioned

**Savings**: 20-50% by using correct instance size

**Use For**: All workloads

### Optimization 4: Multi-Region vs Single Region

**When**: Data residency allows

**Savings**: 30-50% by using single region

**Use For**: Most deployments

---

## Sizing Examples

### Example 1: Low Volume (SaaS)

**Requirements**:
- 2,200 cards
- 3.8M transactions/year
- ~10,411 transactions/day
- ~0.12 TPS average
- ~0.48 TPS peak

**Sizing**:
- Compute: 1 small instance (t3.medium)
- Database: db.t3.medium (100 GB)
- Storage: 50 GB
- **Recommendation**: SaaS multi-tenant

**Estimated Cost**: $500-1,000/month

### Example 2: Medium Volume (EKS/AKS)

**Requirements**:
- 50,000 cards
- 100M transactions/year
- ~274,000 transactions/day
- ~3.2 TPS average
- ~12.8 TPS peak

**Sizing**:
- Compute: 2-4 medium instances (m5.large)
- Min: 2 instances
- Max: 6 instances
- Database: db.m5.large (500 GB)
- Storage: 200 GB
- **Recommendation**: EKS/AKS

**Estimated Cost**: $3,000-5,000/month

### Example 3: High Volume (Dedicated)

**Requirements**:
- 500,000 cards
- 1B transactions/year
- ~2.7M transactions/day
- ~31 TPS average
- ~124 TPS peak

**Sizing**:
- Compute: 4-8 large instances (m5.xlarge)
- Min: 4 instances
- Max: 12 instances
- Database: db.m5.2xlarge (2 TB)
- Storage: 1 TB
- **Recommendation**: Dedicated EKS/AKS

**Estimated Cost**: $15,000-25,000/month

---

## Common Issues

### Issue 1: TPS Underestimated

**Symptom**: TPS seems too low for card volume

**Solution**:
1. Verify PV per card is in transactions (not currency)
2. Check if all card types included
3. Verify peak multiplier applied

### Issue 2: Over-Provisioned

**Symptom**: Sizing seems excessive

**Solution**:
1. Review TPS calculations
2. Check if peak multiplier too high
3. Consider growth rate realistic
4. Use auto-scaling instead of fixed capacity

### Issue 3: Cost Too High

**Symptom**: Pricing exceeds budget

**Solution**:
1. Consider SaaS multi-tenant
2. Use reserved instances
3. Optimize instance sizes
4. Consider alternative regions

### Issue 4: Calculator URL Missing

**Symptom**: Pricing without source URL

**Solution**:
1. Use official calculator
2. Screenshot configuration
3. Save evidence
4. Update response

---

## Infrastructure Templates

### Template 1: SaaS Entry-Level

```
Compute: 1 shared instance
Database: Multi-tenant DB
Storage: Shared storage
Network: Shared VPC
Cost: $500-1,000/month
When: TPS < 1
```

### Template 2: Cloud-Native Small

```
Compute: 2 instances (min 1, max 3)
Database: Managed DB (100-500 GB)
Storage: Block storage (100-200 GB)
Network: VPC with 2 AZs
Cost: $2,000-4,000/month
When: TPS 1-10
```

### Template 3: Cloud-Native Medium

```
Compute: 4 instances (min 2, max 8)
Database: Managed DB (500 GB-1 TB)
Storage: Block storage (200-500 GB)
Network: VPC with 3 AZs
Cost: $5,000-10,000/month
When: TPS 10-50
```

### Template 4: Cloud-Native Large

```
Compute: 8+ instances (min 4, max 16)
Database: Managed DB (1-2 TB)
Storage: Block storage (500 GB-1 TB)
Network: VPC with 3 AZs
Cost: $15,000+/month
When: TPS 50+
```

---

## Knowledge Base References

### Sizing

- `wiki/apv/knowledge/sizing/tps-calculator.md` - TPS calculation methodology
- `wiki/apv/knowledge/sizing/aws-pricing.md` - AWS pricing reference
- `wiki/apv/knowledge/sizing/azure-pricing.md` - Azure pricing reference
- `wiki/apv/knowledge/sizing/gcp-pricing.md` - GCP pricing reference

### Infrastructure

- `wiki/apv/knowledge/infrastructure/aws-eks.md` - AWS EKS patterns
- `wiki/apv/knowledge/infrastructure/azure-aks.md` - Azure AKS patterns
- `wiki/apv/knowledge/infrastructure/gcp-gke.md` - GCP GKE patterns

---

## Getting Help

### Documentation

- [[apv-user-guide]] - Complete user guide
- [[apv-skill-reference]] - rfp-calculator and rfp-pricer details
- [[apv-excel-processing-guide]] - Excel data extraction

### Tools

- `wiki/apv/tools/parse-rfp-excel.py` - Extract card volumes from Excel
- `wiki/apv/tools/convert-to-markdown.py` - Convert RFP documents

### Examples

- `wiki/apv/tests/data/bbc-volume-data-corrected.md` - Sample volume data
- `wiki/apv/tests/output/bbc-sizing-output.md` - Sample sizing output

---

## Quick Reference

### TPS Calculation

```
Daily Transactions = Annual Transactions / 365
Average TPS = Daily Transactions / 86,400
Peak TPS = Average TPS × 4
```

### Instance Sizing

```
Small: 10-50 TPS (t3.medium)
Medium: 50-200 TPS (m5.large)
Large: 200-500 TPS (m5.xlarge)
```

### Cost Estimation

```
SaaS: $500-1,000/month
Small: $2,000-4,000/month
Medium: $5,000-10,000/month
Large: $15,000+/month
```

---

**Training Duration**: 30 minutes
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
