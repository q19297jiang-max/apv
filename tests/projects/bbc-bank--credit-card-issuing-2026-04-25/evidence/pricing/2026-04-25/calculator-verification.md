---
type: apv-evidence
category: calculator-verification
title: "BBC Bank Credit Card Issuing - Calculator Verification"
created: 2026-04-25
verified: 2026-04-25
verified_by: Infrastructure Architect
price_valid_until: 2026-05-25
source_url: "Internal SaaS Rate Sheet v2.3"
source_urls:
  - "Internal SaaS Rate Sheet v2.3"
  - "https://aws.amazon.com/cloudhsm/pricing/"
  - "https://calculator.aws/"
tags: [apv, verification, evidence]
---

# Calculator Verification: BBC Bank - Credit Card Issuing Platform

**Date**: 2026-04-25
**Project**: BBC Bank Credit Card Issuing RFP

---

## SaaS Pricing Verification

### Pricing Source: Internal SaaS Rate Sheet v2.3

**Verification Method**: Internal rate sheet reference

**Rate Sheet Reference**:
- **Document**: Internal SaaS Pricing Schedule v2.3
- **Version**: Current as of 2026-04-25
- **Approved By**: Pricing Team
- **Next Review**: 2026-05-25

**Components Verified**:
| Component | Unit Price | Verified Date | Status |
|-----------|-----------|---------------|--------|
| Card Management Core | $500/month | 2026-04-25 | ✅ Verified |
| Web Portal | $200/month | 2026-04-25 | ✅ Verified |
| VISA Gateway | $50/month | 2026-04-25 | ✅ Verified |
| HSM Service | $30/month | 2026-04-25 | ✅ Verified |
| Database | $20/month (included) | 2026-04-25 | ✅ Verified |

**Verification Status**: ✅ All components verified

---

## AWS Pricing Verification (for comparison)

### CloudHSM Pricing

**Source**: https://aws.amazon.com/cloudhsm/pricing/
**Calculator**: https://calculator.aws/
**Verified Date**: 2026-04-25

**Pricing Verified**:
| Component | Unit Price | Source URL |
|-----------|-----------|------------|
| CloudHSM (single) | $567/month | https://aws.amazon.com/cloudhsm/pricing/ |
| CloudHSM (shared allocation) | $30/month | Internal calculation |

**Verification Method**: AWS pricing calculator
**Verification Status**: ✅ Verified

---

## AWS Pricing Verification (for comparison)

**Source**: [[aws-pricing]] (wiki/apv/knowledge/pricing/aws.md)
**Region**: Singapore (ap-southeast-1) - Default pricing baseline
**Verified Date**: 2026-04-24

**Pricing Verified**:
| Instance Type | vCPU | Memory | Price/Hour | Price/Month (730h) | Source URL |
|---------------|------|--------|------------|-------------------|------------|
| m6i.xlarge | 4 | 16 GiB | $0.208 | $151.84 | [[aws-pricing]] |
| db.m6i.xlarge | 4 | 16 GiB | $0.424 | $309.52 | [[aws-pricing]] |
| cache.m6g.xlarge | 4 | 13.5 GiB | $0.312 | $227.76 | [[aws-pricing]] |
| EKS Cluster | - | - | $0.10 | $73.00 | [[aws-pricing]] |
| ALB | - | - | $0.0225 | $16.43 | [[aws-pricing]] |

**Verification Method**: AWS pricing knowledge base (Singapore region)
**Verification Status**: ✅ Verified

**Verification Method**: AWS pricing calculator
**Verification Status**: ✅ Verified

---

## Verification Summary

**Total Components Verified**: 12
**Verification Pass Rate**: 100%

**Source URLs**:
- Internal SaaS Rate Sheet v2.3
- https://aws.amazon.com/cloudhsm/pricing/
- https://calculator.aws/

**Next Verification**: 2026-05-25 (30-day freshness threshold)
