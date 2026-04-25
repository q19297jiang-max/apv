---
type: apv-template
category: approval-template
title: "Stage 2: Compliance Review Checklist"
tags: [template, approval, compliance]
---

# Stage 2: Compliance Review Checklist (with Source URL Verification)

## Purpose

Validate all compliance claims with official source URLs and verify expert review.

## Checklist Items (5 checks + SOURCE URL CHECKS, 3 minutes)

### 2.1 PCI-DSS Compliance
- [ ] All 12 requirements addressed
- [ ] PCI-DSS certificate linked
- [ ] Evidence artifacts listed
- [ ] Source URL verification:
  - [ ] All compliance claims cite https://www.pcisecuritystandards.org/
  - [ ] All source URLs work and accessible
  - [ ] Certificate URL provided
  - [ ] Evidence screenshots linked

### 2.2 Country-Specific Compliance
- [ ] All applicable country regulations addressed
- [ ] Official regulation URLs provided
- [ ] Expert verification documented
- [ ] Source URL verification:
  - [ ] MAS/BNM/BSP/BI/BOT/FSC/HKMA URLs provided
  - [ ] All source URLs work and accessible
  - [ ] License/registration numbers provided (if applicable)
  - [ ] Evidence artifacts listed

### 2.3 Data Protection Compliance
- [ ] PDPA compliance addressed
- [ ] Data residency requirements met
- [ ] Data breach notification procedures included
- [ ] Source URL verification:
  - [ ] Official law URLs provided
  - [ ] All source URLs work and accessible

### 2.4 Expert Verification
- [ ] Compliance Officer review completed
- [ ] Expert sign-off documented
- [ ] Verification date current (<12 months)

### 2.5 Evidence Documentation
- [ ] All evidence artifacts listed
- [ ] Evidence stored in wiki/apv/knowledge/evidence/
- [ ] Evidence is accessible

## Approval Decision

**Status**: [ ] Pass [ ] Needs Specialist Review [ ] Fail

**Pass Criteria**: All source URLs verified, expert sign-off obtained

**Specialist Trigger**: New country regulation or complex compliance scenario

**Evidence File**: `wiki/apv/.rfp-session/{BANK_NAME}/approvals/stage-2-compliance.md`

## Related
- [[unified-checklist]] — Unified approval checklist
