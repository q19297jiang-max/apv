---
type: apv-template
category: approval-template
title: "Stage 4: Sizing Review Checklist"
tags: [template, approval, sizing]
---

# Stage 4: Sizing Review Checklist

## Purpose

Validate infrastructure sizing calculations and capacity planning.

## Checklist Items (3 checks, 3 minutes)

### 4.1 TPS Calculations
- [ ] Peak TPS correctly calculated
- [ ] Safety margin applied (2x recommended)
- [ ] Growth factor considered (1.5x)

### 4.2 Component Sizing
- [ ] Compute sizing justified
- [ ] Database sizing justified
- [ ] Network bandwidth calculated

### 4.3 HA Redundancy
- [ ] Multi-AZ deployment included
- [ ] Failover capacity included

## Approval Decision

**Status**: [ ] Pass [ ] Needs Adjustment

**Evidence File**: `wiki/apv/.rfp-session/{BANK_NAME}/approvals/stage-4-sizing.md`

## Related
- [[unified-checklist]] — Unified approval checklist
