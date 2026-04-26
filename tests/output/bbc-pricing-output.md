# RFP Pricing: BBC Bank - Credit Card Issuing System

**Date**: 2026-04-26
**Skill**: rfp-pricer
**RFP**: BBC Bank Credit Card Issuing System

---

## Executive Summary

- Recommended commercial model: SaaS multi-tenant entry package for Phase 1 credit card issuing
- Estimated monthly run rate remains aligned to low-volume launch assumptions from the BBC fixture set
- AWS Singapore remains the reference deployment region for pricing consistency and VISA connectivity assumptions

## Monthly Cost Breakdown

| Component | Quantity | Monthly Cost | Notes |
|-----------|----------|--------------|-------|
| Shared issuing platform | 1 | $3,000 | Entry SaaS base fee |
| VISA connectivity | 1 | $900 | Shared gateway allocation |
| Managed HSM/KMS | 1 | $400 | Key custody and cryptographic operations |
| Reporting and operations | 1 | $350 | Standard operational reporting |
| **Total** | - | **$4,650** | Phase 1 reference estimate |

## Pricing Assumptions

- Phase 1 scope covers credit cards only
- Peak throughput remains below 1 TPS in Year 1
- No issuer-side integration buildout is priced into the base estimate
- Final customer pricing still depends on verified Bangladesh regulatory and hosting requirements

## Source URLs

- https://aws.amazon.com/pricing/
- https://calculator.aws/
