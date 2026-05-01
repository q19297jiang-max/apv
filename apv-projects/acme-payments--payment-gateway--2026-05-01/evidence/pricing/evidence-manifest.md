---
type: evidence-manifest
created: '2026-05-01'
stage: 5
output_class: evidence-backed
---

# Pricing Evidence Manifest

Knowledge files used as evidence sources for Stage 5 (Pricing) and Stage 6 (Response §6).

## Verified Pricing Sources (from aws-component-catalog.md)

| Component | Knowledge Path | Last Verified | Source URL |
|-----------|---------------|---------------|------------|
| EC2 (c6i, m6i, r6i) | `knowledge/pricing/aws.md` | 2026-04-28 | https://calculator.aws/ |
| Aurora RDS Single-AZ | `knowledge/pricing/aws.md` | 2026-04-28 | https://calculator.aws/ |
| Aurora RDS Multi-AZ | `knowledge/pricing/aws.md` | 2026-04-28 | https://calculator.aws/ |
| ElastiCache Redis | `knowledge/pricing/aws.md` | 2026-04-28 | https://calculator.aws/ |
| EKS | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/eks/pricing/ |
| EBS (gp3) | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/ebs/pricing/ |
| S3 | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/s3/pricing/ |
| ALB / NLB | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/elasticloadbalancing/pricing/ |
| KMS | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/kms/pricing/ |
| Shield Advanced | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/shield/pricing/ |
| Direct Connect | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/directconnect/pricing/ |
| VPC Flow Logs | `knowledge/pricing/aws.md` | 2026-04-28 | https://aws.amazon.com/vpc/pricing/ |
| Savings Plans (EC2, RDS, ElastiCache) | `knowledge/pricing/aws.md` | 2026-04-28 | https://calculator.aws/ |

## Estimated Pricing (NOT in verified catalog)

| Component | Monthly | Confidence | Source | Rationale |
|-----------|---------|------------|--------|-----------|
| CloudHSM (2 nodes) | $2,400.00 | **High** | https://aws.amazon.com/cloudhsm/pricing/ | AWS public pricing page, $1.20/hr/node |
| OpenSearch (3× m6g.large.search) | $420.48 | **Medium** | Estimated | 2× EC2-equivalent m6i.large rate as managed service proxy |
| db.r6g.xlarge Multi-AZ | $735.84 | **Medium-High** | Derived from catalog | 2× Single-AZ r6i.xlarge; r6g ≈ r6i pricing |
| NAT Gateway (3) | $97.50 | **High** | https://aws.amazon.com/vpc/pricing/ | AWS public pricing page, ~$32.50/gateway |
| Direct Connect port (1 Gbps) | $300.00 | **Medium** | Industry standard | Catalog shows $0.30 (ambiguous hourly vs monthly) |

## Catalog Source of Truth

| File | Knowledge Path |
|------|---------------|
| AWS Component Catalog | `knowledge/pricing/aws-component-catalog.md` |
| AWS Pricing (generated) | `knowledge/pricing/aws.md` |

## Verification

- **Freshness**: All catalog-sourced pricing verified 2026-04-28, within 30-day freshness window
- **Estimated total exposure**: ~$3,953/mo from unverified sources (20% of total)
