---
created: '2026-05-01'
stage: 5
type: working
---

# Pricing Assumption Log — ACME Payments

## Assumptions

| # | Assumption | Impact | Risk |
|---|-----------|--------|------|
| 1 | All pricing is on-demand; Savings Plans shown separately | Overstates cost vs committed spend | Low — conservative |
| 2 | CloudHSM at $1,200/node/month ($1.20/hr) — not in aws.md catalog | May differ in ap-southeast-1 | Medium |
| 3 | OpenSearch m6g.large.search estimated at 2× EC2 equivalent ($0.192/hr) | Actual managed pricing may differ | Medium |
| 4 | db.r6g.xlarge Multi-AZ estimated at 2× Single-AZ ($1.008/hr) | aws.md only has db.r6i not db.r6g Multi-AZ | Medium |
| 5 | NAT Gateway at ~$32.50/mo base (processing charges excluded) | Data processing at $0.045/GB adds up | Medium |
| 6 | Direct Connect port fee $300/mo for 1 Gbps | aws.md lists $0.30 which appears to be per-hour or formatted differently | Medium |
| 7 | DR region (ap-southeast-3) pricing assumed same as ap-southeast-1 | Jakarta pricing may differ | Low |
| 8 | EBS gp3 at 50 GB per EC2 node (conservative baseline) | May need more for logs, temp data | Low |
| 9 | S3 archival volume estimated; actual depends on log retention implementation | 7-year retention grows significantly | Low |
| 10 | Shield Advanced at $3,000/mo flat | Additional per-resource charges may apply | Low |
| 11 | CloudWatch/CloudTrail estimated at $300-500/mo (not itemized) | Custom metrics and log volume drive cost | Low |
| 12 | LCU/NLCU charges excluded (usage-dependent) | At 750 TPS, could add $50-200/mo | Low |
| 13 | Data transfer between AZs not itemized (~$0.01/GB) | At high volume could be meaningful | Low |
