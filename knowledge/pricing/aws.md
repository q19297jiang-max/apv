---
type: source
category: pricing
title: AWS Pricing for Singapore Region
source_url: "https://calculator.aws/"
captured_date: 2026-04-28
verified_by: Infrastructure Architect
price_valid_until: 2026-05-28
tags: [pricing, aws, singapore, calculator]
freshness_days: 30
last_verified: 2026-04-28
---

# AWS Pricing for Card Processing (Singapore Region)

## Official Calculators

| Calculator | URL | Last Updated |
|------------|-----|-------------|
| AWS Pricing Calculator | https://calculator.aws/ | 2026-04-28 |

### Compute Instances

**Source**: aws-component-catalog.md (Ec2)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | storage | network | price_hour | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|----------|----------|
| m6i.large | 2 | 8 GiB | EBS-only | Up to 12.5 Gbps | $0.096 | $70.08 | https://calculator.aws/ |
| m6i.xlarge | 4 | 16 GiB | EBS-only | Up to 12.5 Gbps | $0.192 | $140.16 | https://calculator.aws/ |
| m6i.2xlarge | 8 | 32 GiB | EBS-only | Up to 12.5 Gbps | $0.384 | $280.32 | https://calculator.aws/ |
| c6i.large | 2 | 4 GiB | EBS-only | Up to 12.5 Gbps | $0.085 | $62.05 | https://calculator.aws/ |
| c6i.xlarge | 4 | 8 GiB | EBS-only | Up to 12.5 Gbps | $0.170 | $124.10 | https://calculator.aws/ |
| c6i.2xlarge | 8 | 16 GiB | EBS-only | Up to 12.5 Gbps | $0.340 | $248.20 | https://calculator.aws/ |
| r6i.large | 2 | 16 GiB | EBS-only | Up to 12.5 Gbps | $0.126 | $91.98 | https://calculator.aws/ |
| r6i.xlarge | 4 | 32 GiB | EBS-only | Up to 12.5 Gbps | $0.252 | $183.96 | https://calculator.aws/ |
| r6i.2xlarge | 8 | 64 GiB | EBS-only | Up to 12.5 Gbps | $0.504 | $367.92 | https://calculator.aws/ |

### Compute Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Ec2 Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | on-demand_hour | savings_3yr_hour | savings_% | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|----------|----------|
| m6i.large | 2 | 8 GiB | $0.096 | $0.061 | 36% | $44.85 | https://calculator.aws/ |
| m6i.xlarge | 4 | 16 GiB | $0.192 | $0.122 | 36% | $88.86 | https://calculator.aws/ |
| m6i.2xlarge | 8 | 32 GiB | $0.384 | $0.246 | 36% | $179.40 | https://calculator.aws/ |
| c6i.large | 2 | 4 GiB | $0.085 | $0.051 | 40% | $37.23 | https://calculator.aws/ |
| c6i.xlarge | 4 | 8 GiB | $0.170 | $0.102 | 40% | $74.11 | https://calculator.aws/ |
| c6i.2xlarge | 8 | 16 GiB | $0.340 | $0.204 | 40% | $148.92 | https://calculator.aws/ |
| r6i.large | 2 | 16 GiB | $0.126 | $0.079 | 37% | $57.95 | https://calculator.aws/ |
| r6i.xlarge | 4 | 32 GiB | $0.252 | $0.159 | 37% | $115.76 | https://calculator.aws/ |
| r6i.2xlarge | 8 | 64 GiB | $0.504 | $0.318 | 37% | $231.79 | https://calculator.aws/ |

### Database Instances (Single-AZ)

**Source**: aws-component-catalog.md (Rds Single Az)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | storage_type | price_hour | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|----------|
| db.m6i.large | 2 | 8 GiB | gp3 | $0.188 | $137.24 | https://calculator.aws/ |
| db.m6i.xlarge | 4 | 16 GiB | gp3 | $0.376 | $274.48 | https://calculator.aws/ |
| db.m6i.2xlarge | 8 | 64 GiB | gp3 | $0.752 | $548.96 | https://calculator.aws/ |
| db.r6i.large | 2 | 16 GiB | gp3 | $0.252 | $183.96 | https://calculator.aws/ |
| db.r6i.xlarge | 4 | 32 GiB | gp3 | $0.504 | $367.92 | https://calculator.aws/ |
| db.r6i.2xlarge | 8 | 64 GiB | gp3 | $1.008 | $735.84 | https://calculator.aws/ |

### Database Instances (Multi-AZ)

**Source**: aws-component-catalog.md (Rds Multi Az)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | price_hour | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|
| db.m1.large | 2 | 6.1 GiB | **$0.699** | **$510.13** | https://calculator.aws/ |
| db.m6i.2xlarge | 8 | 32 GiB | **$2.258** | **$1,648.20** | https://calculator.aws/ |
| db.m6i.xlarge | 4 | 16 GiB | **$1.148** | **$837.90** | https://calculator.aws/ |
| db.r6i.2xlarge | 8 | 64 GiB | **$2.682** | **$1,957.72** | https://calculator.aws/ |
| db.r6i.large | 2 | 16 GiB | **$0.699** | **$510.13** | https://calculator.aws/ |

### Database Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Rds Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | on-demand_hour | savings_3yr_hour | savings_% | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|----------|----------|
| db.m6i.large | 2 | 8 GiB | $0.188 | $0.122 | 35% | $89.06 | https://calculator.aws/ |
| db.m6i.xlarge | 4 | 16 GiB | $0.376 | $0.244 | 35% | $178.12 | https://calculator.aws/ |
| db.m6i.2xlarge | 8 | 64 GiB | $0.752 | $0.489 | 35% | $356.97 | https://calculator.aws/ |
| db.r6i.large | 2 | 16 GiB | $0.252 | $0.164 | 35% | $119.72 | https://calculator.aws/ |
| db.r6i.xlarge | 4 | 32 GiB | $0.504 | $0.328 | 35% | $239.44 | https://calculator.aws/ |
| db.r6i.2xlarge | 8 | 64 GiB | $1.008 | $0.655 | 35% | $478.15 | https://calculator.aws/ |

### Cache Instances

**Source**: aws-component-catalog.md (Elasticache)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | price_hour | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|
| cache.m6g.large | 2 | 5.3 GiB | $0.156 | $113.88 | https://calculator.aws/ |
| cache.m6g.xlarge | 4 | 13.5 GiB | $0.312 | $227.76 | https://calculator.aws/ |
| cache.m6g.2xlarge | 8 | 29 GiB | $0.624 | $455.52 | https://calculator.aws/ |
| cache.r6g.large | 2 | 13.3 GiB | $0.208 | $151.84 | https://calculator.aws/ |
| cache.r6g.xlarge | 4 | 32.3 GiB | $0.416 | $303.68 | https://calculator.aws/ |

### Cache Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Elasticache Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| instance | vcpu | memory | on-demand_hour | savings_3yr_hour | savings_% | monthly_(730h) | calculator_url |
|----------|----------|----------|----------|----------|----------|----------|----------|
| cache.m6g.large | 2 | 5.3 GiB | $0.156 | $0.101 | 35% | $73.73 | https://calculator.aws/ |
| cache.m6g.xlarge | 4 | 13.5 GiB | $0.312 | $0.203 | 35% | $148.19 | https://calculator.aws/ |
| cache.m6g.2xlarge | 8 | 29 GiB | $0.624 | $0.406 | 35% | $296.38 | https://calculator.aws/ |
| cache.r6g.large | 2 | 13.3 GiB | $0.208 | $0.135 | 35% | $98.55 | https://calculator.aws/ |
| cache.r6g.xlarge | 4 | 32.3 GiB | $0.416 | $0.270 | 35% | $197.10 | https://calculator.aws/ |

### Application Load Balancer (ALB)

**Source**: aws-component-catalog.md (Alb)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | billing_unit | price |
|----------|----------|----------|----------|
| https://aws.amazon.com/elasticloadbalancing/pricing/ | ALB Hourly | per ALB-hour | $0.0225 |
| https://aws.amazon.com/elasticloadbalancing/pricing/ | LCU Hourly | per LCU-hour | $0.008 |
| https://aws.amazon.com/elasticloadbalancing/pricing/ | LCU Processing | per 1000 requests | $0.008 |

### Network Load Balancer (NLB)

**Source**: aws-component-catalog.md (Nlb)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | billing_unit | price |
|----------|----------|----------|----------|
| https://aws.amazon.com/elasticloadbalancing/pricing/ | NLB Hourly | per NLB-hour | $0.0225 |
| https://aws.amazon.com/elasticloadbalancing/pricing/ | NLCU Hourly | per NLCU-hour | $0.006 |

### Amazon EKS

**Source**: aws-component-catalog.md (Eks)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | billing_unit | price | $0.04064 | fargate_vcpu | https:__aws.amazon.com_eks_pricing_ | per_vcpu-hour |
|----------|----------|----------|----------|----------|----------|----------|----------|
| https://aws.amazon.com/eks/pricing/ | EKS Cluster | per cluster-hour | $0.10 |  |  |  |  |
|  |  |  |  | $0.0044 | Fargate Memory | https://aws.amazon.com/eks/pricing/ | per GB-hour |

### Amazon EBS (gp3)

**Source**: aws-component-catalog.md (Ebs)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | size | included_iops | included_throughput | price_gb-month |
|----------|----------|----------|----------|----------|
| https://aws.amazon.com/ebs/pricing/ | gp3 | 3,000 | 125 MB/s | $0.08 |
| https://aws.amazon.com/ebs/pricing/ | io1 | - | - | $0.125 |
| https://aws.amazon.com/ebs/pricing/ | io2 Block Express | - | - | $0.125 |

### Amazon S3

**Source**: aws-component-catalog.md (S3)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | min_storage | price_gb-month | storage_class |
|----------|----------|----------|----------|
| https://aws.amazon.com/s3/pricing/ | None | $0.023 | Standard |
| https://aws.amazon.com/s3/pricing/ | None | $0.023 | Intelligent-Tiering |
| https://aws.amazon.com/s3/pricing/ | 30 days | $0.0125 | Standard-IA |
| https://aws.amazon.com/s3/pricing/ | 180 days | $0.00099 | Glacier Deep Archive |

### AWS Direct Connect

**Source**: aws-component-catalog.md (Direct Connect)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | data_transfer | port_speed | price_month |
|----------|----------|----------|----------|
| https://aws.amazon.com/directconnect/pricing/ | $0.02/GB | 1 Gbps | $0.30 |
| https://aws.amazon.com/directconnect/pricing/ | $0.02/GB | 10 Gbps | $2.25 |

### VPC Flow Logs

**Source**: aws-component-catalog.md (Vpc Flow Logs)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | price |
|----------|----------|----------|
| https://aws.amazon.com/vpc/pricing/ | Flow Logs | $0.50 per million records |

### AWS KMS

**Source**: aws-component-catalog.md (Kms)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | billing_unit | price |
|----------|----------|----------|----------|
| https://aws.amazon.com/kms/pricing/ | KMS Key (stored) | per key-month | $1.00 |
| https://aws.amazon.com/kms/pricing/ | KMS Request (cryptographic) | per 10,000 requests | $0.03 |

### AWS Shield Standard

**Source**: aws-component-catalog.md (Shield)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-28
> Calculator: https://calculator.aws/

| calculator_url | component | price |
|----------|----------|----------|
| https://aws.amazon.com/shield/pricing/ | Shield Standard | Free |

## Verification

- **Verified By**: Infrastructure Architect
- **Verification Date**: 2026-04-28
- **Verification Method**: https://calculator.aws/
- **Next Review**: 2026-05-28 (30 days)

## Related

- [[aws-pricing]] - AWS pricing reference
- [[aws-component-catalog]] - Component catalog (source of truth)
- [[tps-calculator]] - Component sizing methodology
