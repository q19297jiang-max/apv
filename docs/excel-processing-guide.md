---
type: apv-meta
category: documentation
title: "APV Excel Processing Guide"
created: 2026-04-24
tags: [apv, documentation, excel, processing, rfp]
sources:
  - "[[apv-user-guide]]"
  - "[[apv-operations-guide]]"
---

# APV Excel Processing Guide

**Purpose**: Correctly process RFP Excel files to extract card volumes, transaction volumes, and calculate TPS.

---

## The Problem: Excel Formula vs Value

When reading Excel files with Python/openpyxl, there are two modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| `data_only=False` (default) | Reads **formulas** | When you need to understand the calculation logic |
| `data_only=True` | Reads **actual values** | When you need the calculated results |

**Critical Issue**: The original BBC RFP processing read formulas instead of actual values, leading to incorrect calculations.

---

## Solution: Two Approaches

### Approach 1: Improved Python Parser (Recommended)

**Tool**: `wiki/apv/tools/parse-rfp-excel.py`

**Features**:
- Uses `data_only=True` to read actual values
- Separates Phase 1 (Credit only) from Full Scope (Credit + Debit)
- Calculates TPS automatically
- Generates corrected markdown with both scopes

**Usage**:
```bash
python wiki/apv/tools/parse-rfp-excel.py <excel-file> [output-md-file]
```

**Example**:
```bash
python wiki/apv/tools/parse-rfp-excel.py \
  "wiki/apv/tests/data/BBC Bank Card Volume.xlsx" \
  bbc-volume-corrected.md
```

**Output**:
- Markdown file with card volumes, PV per card, and TPS calculations
- JSON file with parsed data
- Both Phase 1 and Full Scope calculations

---

### Approach 2: Excel to Markdown Converter

**Tool**: `wiki/apv/tools/excel-to-markdown.py`

**Features**:
- Converts Excel to markdown for easy reading
- Preserves table formatting
- Specialized questionnaire format converter

**Usage**:
```bash
# General Excel to Markdown
python wiki/apv/tools/excel-to-markdown.py <excel-file> [output-md-file]

# BBC Questionnaire format
python wiki/apv/tools/excel-to-markdown.py <excel-file> [output-md-file] --questionnaire
```

**Example**:
```bash
# Convert questionnaire
python wiki/apv/tools/excel-to-markdown.py \
  "BBC Questionnaire.xlsx" bbc-q.md --questionnaire

# Convert card volume
python wiki/apv/tools/excel-to-markdown.py \
  "BBC Bank Card Volume.xlsx" bbc-volume.md
```

---

## BBC RFP Analysis: What Went Wrong

### Original Issue

The original `bbc-rfp-summary.md` had:
- ✅ Correct Phase 1 cards: 2,200 (Credit only)
- ✅ Correct Phase 1 transactions: 3,800,000
- ❌ **Missing**: Full Scope (Credit + Debit = 10,200 cards, 8,300,000 transactions)

### Root Cause

1. **Scope Confusion**: The Excel file included both Credit and Debit cards
2. **Questionnaire Clarification**: "Credit Card First Phase, Debit Card next phase"
3. **Missing Full Scope**: Only Phase 1 was calculated, not the full projection

### Corrected Data

#### Phase 1: Credit Cards Only

| Year | Cards | Transactions | Peak TPS |
|------|-------|--------------|----------|
| Y1 | 2,200 | 3,800,000 | 0.48 |
| Y5 | 4,400 | 15,966,720 | 2.03 |

#### Full Scope: Credit + Debit

| Year | Cards | Transactions | Peak TPS |
|------|-------|--------------|----------|
| Y1 | 10,200 | 8,300,000 | 1.05 |
| Y5 | 16,600 | 30,378,240 | 3.85 |

---

## Step-by-Step: Processing a New RFP Excel File

### Step 1: Identify the Files

```bash
# List files in the RFP folder
ls apv-projects/[customer]--[title]--[date]/input/
```

Look for:
- Card Volume Excel
- Questionnaire Excel
- Other RFP documents

### Step 2: Convert to Markdown (Optional - for review)

```bash
# Convert questionnaire
python wiki/apv/tools/excel-to-markdown.py \
  "apv-projects/[customer]/input/Questionnaire.xlsx" \
  "apv-projects/[customer]/outputs/questionnaire-converted.md" \
  --questionnaire

# Convert card volume
python wiki/apv/tools/excel-to-markdown.py \
  "apv-projects/[customer]/input/Card Volume.xlsx" \
  "apv-projects/[customer]/outputs/card-volume-converted.md"
```

### Step 3: Parse and Calculate Volumes

```bash
# Parse card volume with TPS calculations
python wiki/apv/tools/parse-rfp-excel.py \
  "apv-projects/[customer]/input/Card Volume.xlsx" \
  "apv-projects/[customer]/outputs/volume-data-corrected.md"
```

### Step 4: Review the Output

Check the generated markdown file for:
- ✅ Correct card volumes
- ✅ Correct PV per card
- ✅ Correct transaction calculations
- ✅ Phase 1 vs Full Scope separated

### Step 5: Use in RFP Response

```bash
# Run APV skills with the corrected data
cd apv-projects/[customer]--[title]--[date]/
/skill rfp-brainstorm "input/rfp.pdf" > "outputs/01-brainstorm.md"
# ... continue with other skills
```

---

## TPS Calculation Formula

The `parse-rfp-excel.py` tool uses these formulas:

```python
# Total transactions per year
total_transactions = sum(cards * pv_per_card for each card type)

# Daily transactions
daily_transactions = total_transactions / 365

# Average TPS
avg_tps = daily_transactions / 86,400

# Peak TPS (standard 4x multiplier)
peak_tps = avg_tps * 4
```

**Example** (Phase 1, Year 1):
- Cards: 2,200 (1,200 Classic + 800 Platinum + 200 Infinite)
- PV per card: (1,200 × 1,000) + (800 × 2,000) + (200 × 5,000) = 3,800,000
- Daily: 3,800,000 / 365 = 10,411
- Avg TPS: 10,411 / 86,400 = 0.12
- Peak TPS: 0.12 × 4 = 0.48

---

## Common Issues and Solutions

### Issue 1: Formula Instead of Value

**Symptom**: Excel cells show formulas like `=SUM(A1:A10)` instead of values

**Solution**: Use `data_only=True` in openpyxl:
```python
wb = openpyxl.load_workbook(file_path, data_only=True)
```

### Issue 2: Wrong Card Count

**Symptom**: Card count doesn't match RFP requirements

**Solution**: Check if Debit cards are included but not in scope for Phase 1

### Issue 3: Incorrect TPS

**Symptom**: TPS seems too high or too low

**Solution**: Verify:
1. PV per card is in transactions per year (not currency)
2. Daily calculation uses 365 days
3. Peak TPS multiplier is correct (default 4x)

---

## Tool Reference

### parse-rfp-excel.py

**Purpose**: Parse RFP Excel card volume files with TPS calculations

**Input**: BBC-style Card Volume Excel file

**Output**:
- Markdown file with volumes and TPS
- JSON file with parsed data

**Features**:
- `data_only=True` for actual values
- Phase 1 vs Full Scope separation
- Automatic TPS calculation
- 5-year projection

### excel-to-markdown.py

**Purpose**: Convert Excel files to Markdown

**Input**: Any Excel file

**Output**: Markdown file

**Features**:
- General Excel to Markdown conversion
- Specialized BBC Questionnaire format (`--questionnaire`)
- Preserves table formatting

---

## Best Practices

1. **Always use `data_only=True`** when reading Excel for calculated values
2. **Separate Phase 1 from Full Scope** when RFP has phased approach
3. **Verify TPS calculations** make sense for the business
4. **Keep both markdown versions** - converted for review, parsed for calculations
5. **Document assumptions** - e.g., "PV per card = annual transaction count"

---

## Related

- [[apv-user-guide]] - Complete APV user guide
- [[apv-operations-guide]] - Daily operations guide
- [[apv-project-structure-guide]] - Project folder organization

---

**Version**: 1.0
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
