---
type: apv-knowledge
category: pricing
title: "AWS Pricing for Singapore Region"
source_url: "https://calculator.aws/"
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

### Compute Instances

**Source**: aws-component-catalog.md (Ec2)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | network | instance | monthly_(730h) | price_hour | memory | storage |
|----------|----------|----------|----------|----------|----------|----------|----------|
| 2 | https://calculator.aws/ | Up to 12.5 Gbps | m6i.large | $70.08 | $0.096 | 8 GiB | EBS-only |
| 4 | https://calculator.aws/ | Up to 12.5 Gbps | m6i.xlarge | $140.16 | $0.192 | 16 GiB | EBS-only |
| 8 | https://calculator.aws/ | Up to 12.5 Gbps | m6i.2xlarge | $280.32 | $0.384 | 32 GiB | EBS-only |
| 2 | https://calculator.aws/ | Up to 12.5 Gbps | c6i.large | $62.05 | $0.085 | 4 GiB | EBS-only |
| 4 | https://calculator.aws/ | Up to 12.5 Gbps | c6i.xlarge | $124.10 | $0.170 | 8 GiB | EBS-only |
| 8 | https://calculator.aws/ | Up to 12.5 Gbps | c6i.2xlarge | $248.20 | $0.340 | 16 GiB | EBS-only |
| 2 | https://calculator.aws/ | Up to 12.5 Gbps | r6i.large | $91.98 | $0.126 | 16 GiB | EBS-only |
| 4 | https://calculator.aws/ | Up to 12.5 Gbps | r6i.xlarge | $183.96 | $0.252 | 32 GiB | EBS-only |
| 8 | https://calculator.aws/ | Up to 12.5 Gbps | r6i.2xlarge | $367.92 | $0.504 | 64 GiB | EBS-only |

### Compute Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Ec2 Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | savings_% | on-demand_hour | savings_3yr_hour | memory |
|----------|----------|----------|----------|----------|----------|----------|----------|
| 4 | https://calculator.aws/ | m6i.xlarge | $88.86 | 36% | $0.192 | $0.122 | 16 GiB |
| 4 | https://calculator.aws/ | c6i.xlarge | $74.11 | 40% | $0.170 | $0.102 | 8 GiB |
| 4 | https://calculator.aws/ | r6i.xlarge | $115.76 | 37% | $0.252 | $0.159 | 32 GiB |

### Database Instances (Single-AZ)

**Source**: aws-component-catalog.md (Rds Single Az)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | price_hour | storage_type | memory |
|----------|----------|----------|----------|----------|----------|----------|
| 2 | https://calculator.aws/ | db.m6i.large | $137.24 | $0.188 | gp3 | 8 GiB |
| 4 | https://calculator.aws/ | db.m6i.xlarge | $274.48 | $0.376 | gp3 | 16 GiB |
| 8 | https://calculator.aws/ | db.m6i.2xlarge | $548.96 | $0.752 | gp3 | 64 GiB |
| 2 | https://calculator.aws/ | db.r6i.large | $183.96 | $0.252 | gp3 | 16 GiB |
| 4 | https://calculator.aws/ | db.r6i.xlarge | $367.92 | $0.504 | gp3 | 32 GiB |
| 8 | https://calculator.aws/ | db.r6i.2xlarge | $735.84 | $1.008 | gp3 | 64 GiB |

### Database Instances (Multi-AZ)

**Source**: aws-component-catalog.md (Rds Multi Az)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | price_hour | memory |
|----------|----------|----------|----------|----------|----------|
| 4 | https://calculator.aws/ | db.m6i.xlarge | **$838.04** | **$1.148** | 16 GiB |
| 4 | https://calculator.aws/ | db.r6i.xlarge | **$1,130.04** | **$1.548** | 32 GiB |
| 2 | https://calculator.aws/ | db.m6i.large | **$440.92** | **$0.604** | 8 GiB |

### Database Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Rds Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | savings_% | on-demand_hour | savings_3yr_hour | memory |
|----------|----------|----------|----------|----------|----------|----------|----------|
| 2 | https://calculator.aws/ | db.m6i.large | $89.06 | 35% | $0.188 | $0.122 | 8 GiB |
| 4 | https://calculator.aws/ | db.m6i.xlarge | $178.12 | 35% | $0.376 | $0.244 | 16 GiB |
| 8 | https://calculator.aws/ | db.m6i.2xlarge | $356.97 | 35% | $0.752 | $0.489 | 64 GiB |
| 2 | https://calculator.aws/ | db.r6i.large | $119.72 | 35% | $0.252 | $0.164 | 16 GiB |
| 4 | https://calculator.aws/ | db.r6i.xlarge | $239.44 | 35% | $0.504 | $0.328 | 32 GiB |
| 8 | https://calculator.aws/ | db.r6i.2xlarge | $478.15 | 35% | $1.008 | $0.655 | 64 GiB |

### Cache Instances

**Source**: aws-component-catalog.md (Elasticache)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | price_hour | memory |
|----------|----------|----------|----------|----------|----------|
| 2 | https://calculator.aws/ | cache.m6g.large | $113.88 | $0.156 | 5.3 GiB |
| 4 | https://calculator.aws/ | cache.m6g.xlarge | $227.76 | $0.312 | 13.5 GiB |
| 8 | https://calculator.aws/ | cache.m6g.2xlarge | $455.52 | $0.624 | 29 GiB |
| 2 | https://calculator.aws/ | cache.r6g.large | $151.84 | $0.208 | 13.3 GiB |
| 4 | https://calculator.aws/ | cache.r6g.xlarge | $303.68 | $0.416 | 32.3 GiB |

### Cache Savings Plans (3yr No Upfront)

**Source**: aws-component-catalog.md (Elasticache Savings Plans)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| vcpu | calculator_url | instance | monthly_(730h) | savings_% | on-demand_hour | savings_3yr_hour | memory |
|----------|----------|----------|----------|----------|----------|----------|----------|
| 2 | https://calculator.aws/ | cache.m6g.large | $73.73 | 35% | $0.156 | $0.101 | 5.3 GiB |
| 4 | https://calculator.aws/ | cache.m6g.xlarge | $148.19 | 35% | $0.312 | $0.203 | 13.5 GiB |
| 8 | https://calculator.aws/ | cache.m6g.2xlarge | $296.38 | 35% | $0.624 | $0.406 | 29 GiB |
| 2 | https://calculator.aws/ | cache.r6g.large | $98.55 | 35% | $0.208 | $0.135 | 13.3 GiB |
| 4 | https://calculator.aws/ | cache.r6g.xlarge | $197.10 | 35% | $0.416 | $0.270 | 32.3 GiB |

### Application Load Balancer (ALB)

**Source**: aws-component-catalog.md (Alb)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| billing_unit | calculator_url | price | component |
|----------|----------|----------|----------|
| per ALB-hour | https://aws.amazon.com/elasticloadbalancing/pricing/ | $0.0225 | ALB Hourly |
| per LCU-hour | https://aws.amazon.com/elasticloadbalancing/pricing/ | $0.008 | LCU Hourly |
| per 1000 requests | https://aws.amazon.com/elasticloadbalancing/pricing/ | $0.008 | LCU Processing |

### Network Load Balancer (NLB)

**Source**: aws-component-catalog.md (Nlb)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| billing_unit | calculator_url | price | component |
|----------|----------|----------|----------|
| per NLB-hour | https://aws.amazon.com/elasticloadbalancing/pricing/ | $0.0225 | NLB Hourly |
| per NLCU-hour | https://aws.amazon.com/elasticloadbalancing/pricing/ | $0.006 | NLCU Hourly |

### Amazon EKS

**Source**: aws-component-catalog.md (Eks)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| billing_unit | $0.04064 | calculator_url | per_vcpu-hour | https:__aws.amazon.com_eks_pricing_ | price | component | fargate_vcpu |
|----------|----------|----------|----------|----------|----------|----------|----------|
| per cluster-hour |  | https://aws.amazon.com/eks/pricing/ |  |  | $0.10 | EKS Cluster |  |
|  | $0.0044 |  | per GB-hour | https://aws.amazon.com/eks/pricing/ |  |  | Fargate Memory |

### Amazon EBS (gp3)

**Source**: aws-component-catalog.md (Ebs)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| calculator_url | size | price_gb-month | included_iops | included_throughput |
|----------|----------|----------|----------|----------|
| https://aws.amazon.com/ebs/pricing/ | gp3 | $0.08 | 3,000 | 125 MB/s |
| https://aws.amazon.com/ebs/pricing/ | io1 | $0.125 | - | - |
| https://aws.amazon.com/ebs/pricing/ | io2 Block Express | $0.125 | - | - |

### Amazon S3

**Source**: aws-component-catalog.md (S3)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| min_storage | calculator_url | price_gb-month | storage_class |
|----------|----------|----------|----------|
| None | https://aws.amazon.com/s3/pricing/ | $0.023 | Standard |
| None | https://aws.amazon.com/s3/pricing/ | $0.023 | Intelligent-Tiering |
| 30 days | https://aws.amazon.com/s3/pricing/ | $0.0125 | Standard-IA |
| 180 days | https://aws.amazon.com/s3/pricing/ | $0.00099 | Glacier Deep Archive |

### AWS Direct Connect

**Source**: aws-component-catalog.md (Direct Connect)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| calculator_url | price_month | port_speed | data_transfer |
|----------|----------|----------|----------|
| https://aws.amazon.com/directconnect/pricing/ | $0.30 | 1 Gbps | $0.02/GB |
| https://aws.amazon.com/directconnect/pricing/ | $2.25 | 10 Gbps | $0.02/GB |

### VPC Flow Logs

**Source**: aws-component-catalog.md (Vpc Flow Logs)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| calculator_url | component | price |
|----------|----------|----------|
| https://aws.amazon.com/vpc/pricing/ | Flow Logs | $0.50 per million records |

### AWS KMS

**Source**: aws-component-catalog.md (Kms)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| billing_unit | calculator_url | price | component |
|----------|----------|----------|----------|
| per key-month | https://aws.amazon.com/kms/pricing/ | $1.00 | KMS Key (stored) |
| per 10,000 requests | https://aws.amazon.com/kms/pricing/ | $0.03 | KMS Request (cryptographic) |

### AWS Shield Standard

**Source**: aws-component-catalog.md (Shield)

> [!NOTE] Component Catalog Pricing
> Prices below are sourced from aws-component-catalog.md (the source of truth).
> Last verified: 2026-04-25
> Calculator: https://calculator.aws/

| calculator_url | component | price |
|----------|----------|----------|
| https://aws.amazon.com/shield/pricing/ | Shield Standard | Free |

## Verification

- **Verified By**: Infrastructure Architect
- **Verification Date**: 2026-04-25
- **Verification Method**: https://calculator.aws/
- **Next Review**: 2026-05-25 (30 days)

## Related

- [[aws-pricing]] - AWS pricing reference
- [[aws-component-catalog]] - Component catalog (source of truth)
- [[tps-calculator]] - Component sizing methodology
