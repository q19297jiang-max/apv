---
type: apv-meta
category: documentation
title: "Issue #2 Fix: BBC Excel RFP Processing"
created: 2026-04-24
tags: [apv, issue-fix, excel, bbc-bank, corrected]
---

# Issue #2 Fix: BBC Excel RFP Processing

**Status**: ✅ FIXED (2026-04-24)

---

## Problem Statement

When processing the BBC Bank RFP Excel files, the card volumes and transaction volumes were incorrectly calculated.

**User Report**: "the total card volume 1 year and 5 years are wrong, as well as the transaction volume"

---

## Root Cause Analysis

### What Was Wrong

1. **Scope Confusion**: The Excel file `BBC Bank Card Volume.xlsx` included **both Credit and Debit cards**
2. **Missing Full Scope**: The original summary only calculated Credit cards (Phase 1)
3. **Data Extraction**: Used default Excel reading mode which may read formulas instead of values

### Excel File Contents

**Credit Cards (Phase 1)**:
- Infinite: 200 cards (Y1) → 400 cards (Y5)
- Platinum: 800 cards (Y1) → 1,700 cards (Y5)
- Classic: 1,200 cards (Y1) → 2,300 cards (Y5)
- **Total Y1**: 2,200 cards

**Debit Cards (Future Phase)**:
- Platinum: 1,000 cards (Y1) → 1,700 cards (Y5)
- Classic: 7,000 cards (Y1) → 10,500 cards (Y5)
- **Total Y1**: 8,000 cards

**Full Scope (Credit + Debit)**:
- **Total Y1**: 10,200 cards
- **Total Y5**: 16,600 cards

---

## Solution Implemented

### Approach 1: Improved Python Parser

**Created**: `wiki/apv/tools/parse-rfp-excel.py`

**Features**:
- Uses `data_only=True` to read actual Excel values (not formulas)
- Separates Phase 1 (Credit only) from Full Scope (Credit + Debit)
- Calculates TPS automatically
- Generates corrected markdown with both scopes

**Usage**:
```bash
python wiki/apv/tools/parse-rfp-excel.py <excel-file> [output-md-file]
```

### Approach 2: Excel to Markdown Converter

**Created**: `wiki/apv/tools/excel-to-markdown.py`

**Features**:
- Converts Excel files to markdown for easy review
- Specialized BBC Questionnaire format converter
- Preserves table formatting

**Usage**:
```bash
python wiki/apv/tools/excel-to-markdown.py <excel-file> [output-md-file] [--questionnaire]
```

---

## Corrected Data

### Phase 1: Credit Cards Only

| Year | Cards | Transactions | Daily | Peak TPS |
|------|-------|--------------|-------|----------|
| Y1 | 2,200 | 3,800,000 | 10,411 | 0.48 |
| Y2 | 2,750 | 5,700,000 | 15,616 | 0.72 |
| Y3 | 3,300 | 8,352,000 | 22,882 | 1.06 |
| Y4 | 3,850 | 11,664,000 | 31,956 | 1.48 |
| Y5 | 4,400 | 15,966,720 | 43,744 | 2.03 |

### Full Scope: Credit + Debit

| Year | Cards | Transactions | Daily | Peak TPS |
|------|-------|--------------|-------|----------|
| Y1 | 10,200 | 8,300,000 | 22,740 | 1.05 |
| Y2 | 11,550 | 11,640,000 | 31,890 | 1.48 |
| Y3 | 13,100 | 16,344,000 | 44,778 | 2.07 |
| Y4 | 14,850 | 22,464,000 | 61,545 | 2.85 |
| Y5 | 16,600 | 30,378,240 | 83,228 | 3.85 |

---

## Files Created/Updated

### New Files Created

1. `wiki/apv/tools/parse-rfp-excel.py` - Corrected Excel parser
2. `wiki/apv/tools/excel-to-markdown.py` - Excel to Markdown converter
3. `wiki/apv/tests/data/bbc-volume-data-corrected.md` - Corrected volume data
4. `wiki/apv/tests/data/bbc-questionnaire-converted.md` - Converted questionnaire
5. `wiki/apv/tests/data/bbc-card-volume-converted.md` - Converted card volume
6. `wiki/apv/docs/excel-processing-guide.md` - Excel processing documentation

### Files Updated

1. `wiki/apv/tests/data/bbc-rfp-summary.md` - Updated with corrected calculations
   - Added Phase 1 vs Full Scope separation
   - Added 5-year growth projection
   - Added data extraction notes

---

## Verification

### Test Results

```bash
$ python wiki/apv/tools/parse-rfp-excel.py "wiki/apv/tests/data/BBC Bank Card Volume.xlsx"

=== Phase 1: Credit Cards Only ===
Y1: 2,200 cards, 3,800,000 transactions, 0.48 TPS peak
Y5: 4,400 cards, 15,966,720 transactions, 2.03 TPS peak

=== Full Scope: Credit + Debit Cards ===
Y1: 10,200 cards, 8,300,000 transactions, 1.05 TPS peak
Y5: 16,600 cards, 30,378,240 transactions, 3.85 TPS peak
```

### Original vs Corrected

| Metric | Original | Corrected | Status |
|--------|----------|-----------|--------|
| Y1 Cards (Phase 1) | 2,200 | 2,200 | ✅ Correct |
| Y1 Transactions (Phase 1) | 3,800,000 | 3,800,000 | ✅ Correct |
| Y1 Cards (Full Scope) | Not calculated | 10,200 | ✅ Fixed |
| Y1 Transactions (Full Scope) | Not calculated | 8,300,000 | ✅ Fixed |
| Y5 Peak TPS (Phase 1) | ~0.5 TPS | 2.03 TPS | ✅ Fixed |
| Y5 Peak TPS (Full Scope) | Not calculated | 3.85 TPS | ✅ Fixed |

---

## Key Learnings

1. **Always use `data_only=True`** when reading Excel files for calculated values
2. **Check for phased approach** - RFPs may have Phase 1 vs Full Scope
3. **Verify card types** - Credit vs Debit may have different deployment phases
4. **Provide both scopes** - Show Phase 1 (current) and Full Scope (future) calculations
5. **Document assumptions** - Clearly state what's included/excluded

---

## Recommendations

1. **For Future RFPs**: Always use `parse-rfp-excel.py` to process Excel card volume files
2. **For Review**: Use `excel-to-markdown.py` to convert Excel to markdown for manual review
3. **For Documentation**: Keep both Phase 1 and Full Scope calculations in summaries
4. **For Skills**: Update APV skills to use the corrected parser when processing Excel files

---

## Related

- [[apv-excel-processing-guide]] - Complete Excel processing guide
- [[apv-user-guide]] - APV user guide
- [[bbc-rfp-summary]] - Updated BBC RFP summary

---

**Fixed By**: APV Development Team
**Date**: 2026-04-24
**Status**: ✅ RESOLVED
