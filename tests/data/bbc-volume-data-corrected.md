---
type: apv-meta
category: rfp-data
title: "RFP Volume Data - Corrected Excel Extraction"
created: 2026-04-24
tags: [apv, rfp, volume-data, corrected, bbc-bank]
---

# RFP Volume Data - Corrected Excel Extraction

**Source File**: `BBC Bank Card Volume.xlsx`
**Parsed**: 2026-04-24T22:31:43.034970
**Scope**: Phase 1 (Credit Cards Only)

## IMPORTANT: Scope Clarification

> **Note**: This RFP includes **both Credit and Debit cards** in the Excel projection. However, the questionnaire states:
> - "Implement Credit Card First Phase"
> - "Debit Card next phase"

**This summary provides BOTH Phase 1 (Credit only) and Full Scope (Credit + Debit) calculations.**

## Card Volumes by Year

### Credit Cards (Phase 1)

| Product | Y1 | Y2 | Y3 | Y4 | Y5 |
|---------|----|----|----|----|----|
| Infinite | 200 | 250 | 300 | 350 | 400 |
| Platinium | 800 | 1,000 | 1,300 | 1,500 | 1,700 |
| Classic | 1,200 | 1,500 | 1,700 | 2,000 | 2,300 |

### Debit Cards (Future Phase)

| Product | Y1 | Y2 | Y3 | Y4 | Y5 |
|---------|----|----|----|----|----|
| Platinium | 1,000 | 1,100 | 1,300 | 1,500 | 1,700 |
| Classic | 7,000 | 7,700.000000000001 | 8,500 | 9,500 | 10,500 |

### Payment Volume (PV) per Card

#### Credit Cards (Phase 1)

| Product | Y1 | Y2 | Y3 | Y4 | Y5 |
|---------|----|----|----|----|----|
| Infinite | 5,000 | 6,000 | 7,200 | 8,640 | 10368.0 |
| Platinium | 2,000 | 2,400 | 2,880 | 3,456 | 4147.2 |
| Classic | 1,000 | 1,200 | 1,440 | 1,728 | 2073.6 |

#### Debit Cards (Future Phase)

| Product | Y1 | Y2 | Y3 | Y4 | Y5 |
|---------|----|----|----|----|----|
| Platinium | 1,000 | 1,200 | 1,440 | 1,728 | 2073.6 |
| Classic | 500 | 600 | 720 | 864 | 1036.8 |

## Transaction Calculations

### Phase 1: Credit Cards Only

#### Year-by-Year Breakdown

| Year | Total Cards | Total Transactions | Daily | Avg TPS | Peak TPS (4x) |
|------|-------------|-------------------|-------|---------|---------------|
| Y1 | 2,200 | 3,800,000 | 10,411 | 0.12 | 0.48 |
| Y2 | 2,750 | 5,700,000 | 15,616 | 0.18 | 0.72 |
| Y3 | 3,300 | 8,352,000 | 22,882 | 0.26 | 1.06 |
| Y4 | 3,850 | 11,664,000 | 31,956 | 0.37 | 1.48 |
| Y5 | 4,400 | 15,966,720 | 43,744 | 0.51 | 2.03 |

#### Detailed Year 1 Breakdown (Credit Only)

| Product | Cards | PV/Card | Transactions |
|---------|-------|---------|---------------|
| Infinite | 200 | 5,000 | 1,000,000 |
| Platinium | 800 | 2,000 | 1,600,000 |
| Classic | 1,200 | 1,000 | 1,200,000 |

| **Total Phase 1** | **2,200** | - | **3,800,000** |

### Full Scope: Credit + Debit Cards

#### Year-by-Year Breakdown

| Year | Total Cards | Total Transactions | Daily | Avg TPS | Peak TPS (4x) |
|------|-------------|-------------------|-------|---------|---------------|
| Y1 | 10,200 | 8,300,000 | 22,740 | 0.26 | 1.05 |
| Y2 | 11,550.0 | 11,640,000 | 31,890 | 0.37 | 1.48 |
| Y3 | 13,100 | 16,344,000 | 44,778 | 0.52 | 2.07 |
| Y4 | 14,850 | 22,464,000 | 61,545 | 0.71 | 2.85 |
| Y5 | 16,600 | 30,378,240 | 83,228 | 0.96 | 3.85 |

#### Detailed Year 1 Breakdown (All Cards)

| Product | Cards | PV/Card | Transactions |
|---------|-------|---------|---------------|
| Debit Platinium | 1,000 | 1,000 | 1,000,000 |
| Debit Classic | 7,000 | 500 | 3,500,000 |
| Credit Infinite | 200 | 5,000 | 1,000,000 |
| Credit Platinium | 800 | 2,000 | 1,600,000 |
| Credit Classic | 1,200 | 1,000 | 1,200,000 |

| **Total Full Scope** | **10,200** | - | **8,300,000** |

## TPS Calculation Notes

- **Daily transactions**: Total transactions / 365
- **Average TPS**: Daily transactions / 86,400 seconds
- **Peak TPS**: Average TPS × 4 (standard peak multiplier)

## Sizing Recommendation

### Phase 1 (Credit Only)
- **Y1 Cards**: 2,200
- **Y5 Cards**: 4,400
- **5-Year Growth**: 100%
- **Y5 Peak TPS**: 2.03 TPS
- **Recommended Model**: SaaS

### Full Scope (Credit + Debit)
- **Y1 Cards**: 10,200
- **Y5 Cards**: 16,600
- **5-Year Growth**: 63%
- **Y5 Peak TPS**: 3.85 TPS
- **Recommended Model**: SaaS

## Data Quality

- ✅ Extracted directly from Excel using `data_only=True` (actual values, not formulas)
- ✅ Card volumes verified (both Credit and Debit)
- ✅ PV per card verified
- ✅ Transaction calculations automated
- ✅ Phase 1 vs Full Scope properly separated

## Corrections from Original Summary

| Metric | Original (Incorrect) | Corrected | Notes |
|--------|---------------------|-----------|-------|
| Y1 Cards (Phase 1) | 2,200 | 2,200 | ✅ Correct (Credit only) |
| Y1 Transactions (Phase 1) | 3,800,000 | 3,800,000 | ✅ Correct |
| Y1 Cards (Full Scope) | Not calculated | 10,200 | ❌ Missing (includes 8,000 Debit) |
| Y1 Transactions (Full Scope) | Not calculated | 8,300,000 | ❌ Missing |
| Y5 Peak TPS (Phase 1) | ~0.5 TPS | 0.48 TPS | ✅ Correct |
| Y5 Peak TPS (Full Scope) | Not calculated | 3.85 TPS | ❌ Missing |

## Next Steps

1. **For Phase 1 RFP Response**: Use Phase 1 (Credit only) calculations
2. **For Future Planning**: Reference Full Scope calculations when Debit cards are added
3. **Sizing**: Both Phase 1 and Full Scope are suitable for SaaS entry-level solution (< 5 TPS)