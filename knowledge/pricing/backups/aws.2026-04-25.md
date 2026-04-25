---
type: apv-knowledge
category: pricing
title: "AWS Pricing for Singapore Region"
source_url: "https://calculator.aws/"
source_api: "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSComputeService"
captured_date: 2026-04-25
verified_by: "Infrastructure Architect"
price_valid_until: 2026-05-25
tags: [pricing, aws, singapore, calculator]
---

# AWS Pricing for Card Processing (Singapore Region)

## Official Calculators

| Calculator | URL | Last Updated |
|------------|-----|-------------|
| AWS Pricing Calculator | https://calculator.aws/ | 2026-04-25 |
| AWS EC2 Pricing | https://aws.amazon.com/ec2/pricing/ | 2026-04-25 |
| AWS EKS Pricing | https://aws.amazon.com/eks/pricing/ | 2026-04-25 |
| AWS RDS Pricing | https://aws.amazon.com/rds/pricing/ | 2026-04-25 |
| AWS ElastiCache Pricing | https://aws.amazon.com/elasticache/pricing/ | 2026-04-25 |
| AWS ALB Pricing | https://aws.amazon.com/elasticloadbalancing/pricing/ | 2026-04-25 |

## Regional Pricing (Singapore ap-southeast-1)

> [!IMPORTANT] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

### EC2 Instances (Single-AZ)

**Source**: aws-component-catalog.md (EC2 Instances)

| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|------------|---------------|----------------|
| m6i.large | 2 | 8 GiB | $0.096 | $70.08 | https://calculator.aws/ |
| m6i.xlarge | 4 | 16 GiB | $0.192 | $140.16 | https://calculator.aws/ |
| m6i.2xlarge | 8 | 32 GiB | $0.384 | $280.32 | https://calculator.aws/ |
| c6i.large | 2 | 4 GiB | $0.085 | $62.05 | https://calculator.aws/ |
| c6i.xlarge | 4 | 8 GiB | $0.170 | $124.10 | https://calculator.aws/ |
| c6i.2xlarge | 8 | 16 GiB | $0.340 | $248.20 | https://calculator.aws/ |
| r6i.large | 2 | 16 GiB | $0.126 | $91.98 | https://calculator.aws/ |
| r6i.xlarge | 4 | 32 GiB | $0.252 | $183.96 | https://calculator.aws/ |
| r6i.2xlarge | 8 | 64 GiB | $0.504 | $367.92 | https://calculator.aws/ |

### EC2 Instances - Compute Savings Plans (3yr No Upfront)

> [!NOTE] Calculator-Verified Savings Plans Pricing
> Pricing below was verified on 2026-04-25 from https://calculator.aws/
> **3-year commitment required** for these prices.
> Calculator Configuration: Region: Asia Pacific (Singapore), Tenancy: Shared, OS: Linux, Workload: Consistent

| Instance | vCPU | Memory | On-Demand/Hour | Savings 3yr/Hour | Monthly (730h) | Savings % | Calculator URL |
|----------|------|--------|----------------|-----------------|---------------|-----------|----------------|
| m6i.xlarge | 4 | 16 GiB | $0.192 | $0.122 | $88.86 | 36% | https://calculator.aws/ |
| c6i.xlarge | 4 | 8 GiB | $0.170 | $0.102 | $74.11 | 40% | https://calculator.aws/ |
| r6i.xlarge | 4 | 32 GiB | $0.252 | $0.159 | $115.76 | 37% | https://calculator.aws/ |

### EKS Pricing

**Source**: aws-component-catalog.md (Container Components)

| Component | Price | Calculator URL |
|-----------|-------|----------------|
| EKS Cluster | $0.10/hour | https://calculator.aws/ |
| Fargate vCPU | $0.04064/vCPU-hour | https://calculator.aws/ |
| Fargate GB | $0.0044/GB-hour | https://calculator.aws/ |

### RDS Pricing (Single-AZ)

**Source**: aws-component-catalog.md (Database Components)

> [!NOTE] Multi-AZ Pricing
> Multi-AZ pricing is approximately 2-3x Single-AZ pricing.
> See "RDS Pricing (Verified from Calculator)" section below for calculator-verified Multi-AZ pricing.

| Engine | Instance | vCPU | Memory | Price/Hour (Single-AZ) | Price/Hour (Multi-AZ) | Calculator URL |
|--------|----------|------|--------|---------------------|------------------|----------------|
| PostgreSQL | db.m6i.large | 2 | 8 GiB | $0.188 | $0.376 | https://calculator.aws/ |
| PostgreSQL | db.m6i.xlarge | 4 | 16 GiB | $0.376 | $0.752 | https://calculator.aws/ |
| PostgreSQL | db.m6i.2xlarge | 8 | 64 GiB | $0.752 | $1.504 | https://calculator.aws/ |
| PostgreSQL | db.r6i.large | 2 | 16 GiB | $0.252 | $0.504 | https://calculator.aws/ |
| PostgreSQL | db.r6i.xlarge | 4 | 32 GiB | $0.504 | $1.008 | https://calculator.aws/ |
| PostgreSQL | db.r6i.2xlarge | 8 | 64 GiB | $1.008 | $2.016 | https://calculator.aws/ |

### RDS Pricing (Verified from Calculator)

> [!IMPORTANT] Calculator-Verified Multi-AZ Pricing
> Verified on 2026-04-25 from https://calculator.aws/

| Engine | Instance | vCPU | Price/Hour (Multi-AZ) | Monthly (730h) | Calculator URL |
|--------|----------|------|---------------------|--------------|----------------|
| PostgreSQL | db.m6i.xlarge | 4 | **$1.148** | **$838.04** | https://calculator.aws/ |
| PostgreSQL | db.r6i.xlarge | 4 | **$1.548** | **$1130.04** | https://calculator.aws/ |
| PostgreSQL | db.m6i.large | 2 | **$0.604** | **$440.92** | https://calculator.aws/ |

**Calculator Configuration**:
- Region: Asia Pacific (Singapore)
- Engine: PostgreSQL
- Instance Class: Memory Optimized (db.m6i)
- Instance Type: db.m6i.xlarge
- Deployment Option: Multi-AZ
- Storage: General Purpose SSD (gp2), 100 GB
- Utilization: 100% Utilized/Month

### ElastiCache Pricing

**Source**: aws-component-catalog.md (Cache Components)

| Instance | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|----------|------|--------|------------|----------------|----------------|
| cache.m6g.large | 2 | 5.3 GiB | $0.156 | $113.88 | https://calculator.aws/ |
| cache.m6g.xlarge | 4 | 13.5 GiB | $0.312 | $227.76 | https://calculator.aws/ |
| cache.m6g.2xlarge | 8 | 29 GiB | $0.624 | $455.52 | https://calculator.aws/ |
| cache.r6g.large | 2 | 13.3 GiB | $0.208 | $151.84 | https://calculator.aws/ |
| cache.r6g.xlarge | 4 | 32.3 GiB | $0.416 | $303.68 | https://calculator.aws/ |

### Load Balancer Pricing

**Source**: aws-component-catalog.md (Load Balancing Components)

| Component | Price | Billing Unit | Calculator URL |
|-----------|-------|--------------|--------|
| ALB Hourly | $0.0225 | per ALB-hour | https://calculator.aws/ |
| LCU Hourly | $0.008 | per LCU-hour | https://calculator.aws/ |

## Verification

- **Verified By**: Infrastructure Architect
- **Verification Date**: 2026-04-25
- **Verification Method**: https://calculator.aws/
- **Next Review**: 2026-05-25 (30 days)

## Related

- [[aws-pricing]] - AWS pricing reference
- [[aws-component-catalog]] - Component catalog (source of truth)
- [[tps-calculator]] - Component sizing methodology
