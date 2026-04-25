---
type: apv-approval
category: checklist
title: "Unified RFP Approval Checklist"
version: "1.0"
last_updated: 2026-04-23
tags: [approval, checklist, quality-control]
---

# Unified RFP Approval Checklist

## Review Information

- **RFP Name**: {{RFP_BANK_NAME}}
- **Reviewer**: {{REVIEWER_NAME}}
- **Review Date**: {{REVIEW_DATE}}
- **Skills Used**: rfp-brainstorm → rfp-compliance → rfp-architect → rfp-calculator → rfp-pricer → rfp-generator

## Quick Review (Target: 15 minutes)

### 1. Source URL Compliance (5 minutes)

| Category | All URLs Present? | All URLs Valid? | All URLs Official? |
|----------|-------------------|-----------------|-------------------|
| Compliance (PCI-DSS) | ☐ Yes ☐ No | ☐ Yes ☐ No | ☐ Yes ☐ No |
| Compliance (Countries) | ☐ Yes ☐ No | ☐ Yes ☐ No | ☐ Yes ☐ No |
| Architecture | ☐ Yes ☐ No | ☐ Yes ☐ No | ☐ Yes ☐ No |
| Sizing | ☐ Yes ☐ No | ☐ Yes ☐ No | ☐ Yes ☐ No |
| Pricing | ☐ Yes ☐ No | ☐ Yes ☐ No | ☐ Yes ☐ No |

**PASS Criteria**: All checked YES
**If NO**: Return to rfp-generator skill to add missing URLs

### 2. Specialist Consultation Check (3 minutes)

| Category | Expert Verification Required? | Verified By? |
|----------|------------------------------|--------------|
| Compliance (PCI-DSS) | ☐ Yes ☐ No | {{NAME IF YES}} |
| Compliance (Countries) | ☐ Yes ☐ No | {{NAME IF YES}} |
| Infrastructure Architecture | ☐ Yes ☐ No | {{NAME IF YES}} |
| Pricing Calculator | ☐ Yes ☐ No | {{NAME IF YES}} |

**Specialist Triggers**:
- New country regulation → Compliance Officer
- New card system type → Infrastructure Architect
- TPS > 5000 → Infrastructure Architect
- Custom/non-standard pricing → Infrastructure Architect

**PASS Criteria**: All required expert verifications completed
**If NO**: Schedule specialist review before approval

### 3. Accuracy Spot-Check (5 minutes)

Pick 3 random claims from each category and verify source URLs:

#### Compliance
- Claim: {{RANDOM_CLAIM_1}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_2}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_3}} → Source: {{URL}} ☐ Valid ☐ Invalid

#### Architecture
- Claim: {{RANDOM_CLAIM_1}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_2}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_3}} → Source: {{URL}} ☐ Valid ☐ Invalid

#### Pricing
- Claim: {{RANDOM_CLAIM_1}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_2}} → Source: {{URL}} ☐ Valid ☐ Invalid
- Claim: {{RANDOM_CLAIM_3}} → Source: {{URL}} ☐ Valid ☐ Invalid

**PASS Criteria**: ≥8/9 claims valid (89% spot-check accuracy)
**If NO**: Return to skill chain for corrections

### 4. Freshness Check (2 minutes)

| Category | Last Verified | Age | Pass? |
|----------|---------------|-----|-------|
| Compliance Data | {{DATE}} | {{DAYS}} days | ☐ ≤365 days ☐ >365 days |
| Pricing Data | {{DATE}} | {{DAYS}} days | ☐ ≤30 days ☐ >30 days |
| Calculator Evidence | {{DATE}} | {{DAYS}} days | ☐ ≤30 days ☐ >30 days |

**PASS Criteria**: All data within freshness thresholds
**If NO**: Refresh data before approval

## Approval Decision

### Overall Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| Source URL Compliance (100%) | ☐ Pass ☐ Fail | {{NOTES}} |
| Specialist Verification | ☐ Pass ☐ Fail | {{NOTES}} |
| Accuracy Spot-Check (≥89%) | ☐ Pass ☐ Fail | {{NOTES}} |
| Data Freshness | ☐ Pass ☐ Fail | {{NOTES}} |

### Final Approval

**Status**: ☐ APPROVED ☐ CONDITIONAL ☐ REJECTED

**If APPROVED**:
- Approved by: {{NAME}}, {{TITLE}}
- Approval date: {{DATE}}
- Valid until: {{DATE}} (90 days from pricing verification)

**If CONDITIONAL**:
- Conditions: {{LIST_CONDITIONS}}
- Re-review date: {{DATE}}

**If REJECTED**:
- Reason: {{REASON}}
- Return to skill: {{SKILL_NAME}}

## Evidence Files

Attach to RFP folder:
- [ ] Completed checklist (this file)
- [ ] Source URL validation report
- [ ] Specialist verification records (if applicable)
- [ ] Pricing calculator screenshots

Store in: `wiki/apv/.rfp-session/{{BANK_NAME}}/approvals/`

---

## Quality Metrics Tracking

| RFP Name | Review Date | Source URLs | Specialist | Spot-Check | Freshness | Status |
|----------|-------------|-------------|------------|------------|-----------|--------|
| {{BANK_1}} | {{DATE}} | 100% | ✅ | 93% | ✅ | Approved |
| {{BANK_2}} | {{DATE}} | 100% | ✅ | 100% | ✅ | Approved |
| {{BANK_3}} | {{DATE}} | 95% | ⏳ | 89% | ✅ | Conditional |

## Related

- [[apv-accuracy-assurance]] — Accuracy framework
- [[rfp-approver-skill]] — Automated approval skill
