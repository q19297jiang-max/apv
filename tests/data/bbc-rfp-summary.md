---
type: apv-meta
category: rfp-data
title: "BBC Bank RFP Data Summary"
created: 2026-04-24
tags: [apv, rfp, bbc-bank, pilot-test]
---

# BBC Bank RFP Data Summary

**Customer**: BBC Bank
**RFP Date**: 2026
**Project**: Credit Card Issuing System Implementation
**Vendor**: CNN (proposing PaySuit Credit Card System - PSS)

## RFP Documents

1. **BBC Questionnaire.xlsx** - Requirements questionnaire
2. **BBC Bank Card Volume.xlsx** - Volume projections (5 years)

## Key Requirements Extracted

### Card Products (Phase 1)
- **Credit Card Issuance** (3 types):
  - Classic: 1,200 cards (Y1) → 2,300 cards (Y5)
  - Gold/Platinum: 800 cards (Y1) → 1,700 cards (Y5)
  - Infinite: 200 cards (Y1) → 400 cards (Y5)
- **Debit Card**: Future phase (not Phase 1)
- **Prepaid Card**: Future phase

### Card Type Requirements
- Magnetic stripe (VISA standard)
- Chip/EMV (VISA standard)
- Contactless (VISA standard)
- Chip-and-signature (VISA standard)
- Chip-and-PIN (VISA standard)
- DCC (Dynamic Currency Conversion)
- **Plastic cards only** (Phase 1)
- Virtual card: Future phase
- Tokenization: Future phase
- QR Payment: Future phase

### Volume Requirements

> **IMPORTANT**: The Excel file includes **both Credit and Debit cards**. Based on the questionnaire ("Credit Card First Phase, Debit Card next phase"), we provide **both Phase 1 and Full Scope calculations**.

#### Phase 1: Credit Cards Only (Year 1)

| Card Type | Cards | PV/Card | Total Transactions |
|-----------|-------|---------|-------------------|
| Credit Classic | 1,200 | 1,000 | 1,200,000 |
| Credit Platinum | 800 | 2,000 | 1,600,000 |
| Credit Infinite | 200 | 5,000 | 1,000,000 |
| **Total** | **2,200** | - | **3,800,000** |

**TPS Calculation (Phase 1)**:
- Daily transactions: 3,800,000 / 365 = ~10,411 transactions/day
- Average TPS: 10,411 / 86,400 = ~0.12 TPS
- Peak TPS (4x): ~0.48 TPS

#### Full Scope: Credit + Debit Cards (Year 1 - Future Reference)

| Card Type | Cards | PV/Card | Total Transactions |
|-----------|-------|---------|-------------------|
| Debit Classic | 7,000 | 500 | 3,500,000 |
| Debit Platinum | 1,000 | 1,000 | 1,000,000 |
| Credit Classic | 1,200 | 1,000 | 1,200,000 |
| Credit Platinum | 800 | 2,000 | 1,600,000 |
| Credit Infinite | 200 | 5,000 | 1,000,000 |
| **Total** | **10,200** | - | **8,300,000** |

**TPS Calculation (Full Scope)**:
- Daily transactions: 8,300,000 / 365 = ~22,740 transactions/day
- Average TPS: 22,740 / 86,400 = ~0.26 TPS
- Peak TPS (4x): ~1.05 TPS

**Note**: Both Phase 1 and Full Scope are suitable for SaaS entry-level solution (< 5 TPS)

#### 5-Year Growth Projection (Phase 1 - Credit Only)

| Year | Total Cards | Total Transactions | Daily | Peak TPS (4x) |
|------|-------------|-------------------|-------|---------------|
| Y1 | 2,200 | 3,800,000 | ~10,411 | 0.48 |
| Y2 | 2,750 | 5,700,000 | ~15,616 | 0.72 |
| Y3 | 3,300 | 8,352,000 | ~22,882 | 1.06 |
| Y4 | 3,850 | 11,664,000 | ~31,956 | 1.48 |
| Y5 | 4,400 | 15,966,720 | ~43,744 | 2.03 |

**5-Year Growth**: 2,200 → 4,400 cards (100% growth)
**Y5 Peak TPS**: 2.03 TPS (still suitable for SaaS)

### Integration Requirements
- **No interfaces required** (Phase 1)
- Manual key-in by branch staff
- Existing systems: KYC, Origination/Credit Scoring (not interfacing)
- Future: Mobile app, BI Dashboard, Loyalty

### Hardware Requirements
- **HSM**: SaaS model (included)
- **VISA Gateway**: SaaS model (included)
- **MasterCard**: Phase 1 (VISA only)

### Users
- 20 concurrent users (branch staff)

### Performance Requirements
- RTO: CNN SaaS standard
- RPO: CNN SaaS standard
- SLA: CNN SaaS standard

### Compliance
- VISA standards compliance required
- Card embossing: External vendor (email/FTP)

### Reports
- BOL reports: PSS standard reports
- Internal/external: PSS standard reports
- APIs: For future mobile/internet integration

## Regional Notes

This appears to be a bank from Bangladesh (BCC = likely BBC Credit).
- Target deployment: Likely Bangladesh region
- Cloud regions to consider: AWS ap-south-1 (Mumbai), ap-southeast-1 (Singapore)
- Data residency: Bangladesh may have requirements

## APV Skill Chain Test Plan

### Skill 1: rfp-brainstorm
- [x] Analyze requirements
- [x] Identify approach options
- [x] Map compliance landscape

### Skill 2: rfp-compliance
- [ ] Map PCI-DSS requirements
- [ ] Check Bangladesh regulations (if in knowledge base)
- [ ] Verify VISA compliance requirements

### Skill 3: rfp-architect
- [ ] Design credit card issuing architecture
- [ ] Select cloud provider and region
- [ ] Define components (card management, PIN, EMV, etc.)

### Skill 4: rfp-calculator
- [ ] Calculate infrastructure sizing for low TPS
- [ ] Plan for growth to Year 5

### Skill 5: rfp-pricer
- [ ] Generate cost estimates for SaaS model
- [ ] Calculate pricing for VISA integration

### Skill 6: rfp-generator
- [ ] Synthesize complete RFP response

### Skill 7: apv-reviewer
- [ ] Verify source URLs
- [ ] Check completeness
- [ ] Approve response

## Notes for Testing

1. **Low Volume**: This is an entry-level implementation with very low TPS
2. **SaaS Model**: Customer expects SaaS, not on-premise
3. **Phase 1 Scope**: Credit cards only, plastic only, VISA only
4. **Growth**: Year 5 cards = 4,400 (2x growth)
5. **Integration**: No interfaces Phase 1 - purely standalone

## Data Quality

- ✅ Volume data available (5-year projection)
- ✅ Requirements questionnaire complete
- ✅ Corrected Excel extraction using `data_only=True` (actual values, not formulas)
- ✅ Phase 1 vs Full Scope properly separated
- ⚠️ No explicit compliance requirements listed
- ⚠️ Regional location inferred (BCC)
- ⚠️ No explicit SLA numbers (uses "CNN standard")

## Data Extraction Notes

**Original Issue**: The Excel file contained both Credit and Debit cards, but only Credit cards were in scope for Phase 1.

**Fix Applied**:
1. Used improved Python parser with `data_only=True` to extract actual values (not formulas)
2. Separated Phase 1 (Credit only) from Full Scope (Credit + Debit)
3. Generated corrected markdown with both calculations
4. See `bbc-volume-data-corrected.md` for detailed breakdown

**Tools Used**:
- `wiki/apv/tools/parse-rfp-excel.py` - Corrected Excel parser with TPS calculations
- `wiki/apv/tools/excel-to-markdown.py` - Excel to Markdown converter
