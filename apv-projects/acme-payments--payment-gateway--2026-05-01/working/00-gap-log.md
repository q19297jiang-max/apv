---
type: working
stage: 0
created: '2026-05-01'
---

# Knowledge Gap Log

| # | Domain | Description | Severity | Stage Found | Resolved |
|---|--------|-------------|----------|-------------|----------|
| 1 | Patterns | No reference architecture patterns documented (template only) | Medium | 1-Brainstorm | No |
| 2 | Card Systems | Local payment rails (PayNow/FAST, GrabPay API, ShopeePay API) integration details | Medium | 1-Brainstorm | No |
| 3 | Infrastructure | Multi-region data isolation patterns for data residency compliance | Medium | 1-Brainstorm | No |
| 4 | Infrastructure | gRPC deployment and load balancing patterns on EKS/NLB | Low | 1-Brainstorm | No |
| 5 | Pricing | CloudHSM pricing not confirmed in aws.md | Low | 1-Brainstorm | No |
| 6 | Card Systems | Real-time settlement and reconciliation architecture patterns | Medium | 1-Brainstorm | No |
| 7 | Sizing | No payment-specific sizing benchmarks (e.g., vCPU per TPS ratios) | Medium | 1-Brainstorm | No |
| 8 | Commercial | Commercial templates and pricing models not checked | Low | 1-Brainstorm | No |
| 9 | Pricing | db.r6g.xlarge Multi-AZ pricing not in aws.md — estimated at 2× Single-AZ | Medium | 5-Pricing | No |
| 10 | Pricing | OpenSearch m6g.large.search pricing not in aws.md — estimated from EC2 equivalent | Medium | 5-Pricing | No |
| 11 | Pricing | CloudHSM pricing not in aws-component-catalog.md — using $1.20/hr industry reference | Medium | 5-Pricing | No |
| 12 | Pricing | NAT Gateway pricing not in aws.md — using public pricing page estimate | Low | 5-Pricing | No |
| 13 | Pricing | Direct Connect aws.md lists $0.30 as price_month for 1 Gbps (seems low) — used $300/mo industry standard | Medium | 5-Pricing | No |
| 14 | Pricing | CloudWatch/CloudTrail costs not itemized — estimated $300-500/mo | Low | 5-Pricing | No |
