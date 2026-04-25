---
type: apv-meta
category: documentation
title: "Markitdown Integration Summary"
created: 2026-04-24
tags: [apv, documentation, markitdown, integration]
---

# Markitdown Integration Summary

**Status**: ✅ COMPLETE (2026-04-24)

---

## Overview

Microsoft's **markitdown** tool has been integrated into the APV workflow to automatically convert non-markdown documents (PDF, DOCX, XLSX, PPTX, etc.) to markdown before processing with LLM skills.

---

## What Was Done

### 1. Installed Microsoft markitdown

```bash
pip3 install --user --break-system-packages markitdown
```

**Location**: `/Users/stevenjiang/Library/Python/3.14/bin/markitdown`

### 2. Created APV Wrapper Tool

**File**: `wiki/apv/tools/convert-to-markdown.py`

**Features**:
- Wraps Microsoft markitdown with APV-specific metadata
- Adds frontmatter to converted files
- Handles multiple file formats
- Error handling and validation

**Usage**:
```bash
python3 wiki/apv/tools/convert-to-markdown.py <input-file> [output-file]
```

### 3. Updated APV Orchestrator

**File**: `~/.claude/skills/apv/prompt.md`

**Changes**:
- Added Step 2.5: "Convert Non-Markdown Files"
- Updated all skill commands to use converted markdown
- Updated quality rules to require conversion first
- Updated example workflow

### 4. Updated User Guide

**File**: `wiki/apv/docs/user-guide.md`

**Changes**:
- Added markitdown to prerequisites
- Added Step 2: Convert to Markdown
- Updated skill chain commands to use `$RFP_MD`

---

## New Workflow

### Before (Direct Processing)

```bash
# Copy RFP to project
cp rfp.pdf project/input/

# Process directly (PROBLEM: LLM struggles with binary formats)
/skill rfp-brainstorm "input/rfp.pdf" > outputs/01-brainstorm.md
```

### After (Convert First)

```bash
# Copy RFP to project
cp rfp.pdf project/input/

# Convert to markdown (NEW STEP)
python3 wiki/apv/tools/convert-to-markdown.py "input/rfp.pdf" "input/converted.md"

# Process using markdown (BETTER: LLM handles markdown accurately)
/skill rfp-brainstorm "input/converted.md" > outputs/01-brainstorm.md
```

---

## Supported Formats

Microsoft markitdown supports converting these formats to markdown:

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Preserves text structure |
| Word | `.docx`, `.doc` | Converts headings, lists, tables |
| Excel | `.xlsx`, `.xls` | Converts to markdown tables |
| PowerPoint | `.pptx`, `.ppt` | Extracts text content |
| HTML | `.html`, `.htm` | Strips to markdown |
| Text | `.txt` | Adds markdown metadata |
| Images | `.png`, `.jpg` | Uses OCR to extract text |
| And more... | | See [markitdown docs](https://github.com/microsoft/markitdown) |

---

## Benefits

1. **Improved Accuracy**: LLM processes markdown more accurately than binary formats
2. **Structure Preservation**: Tables, headings, and lists are preserved
3. **Reduced Errors**: No more extraction issues from PDF/DOCX
4. **Better Context**: Document structure helps LLM understand content
5. **Universal Input**: Accept any document format

---

## File Changes

### New Files

1. `wiki/apv/tools/convert-to-markdown.py` - APV wrapper for markitdown

### Modified Files

1. `~/.claude/skills/apv/prompt.md` - Added conversion step
2. `wiki/apv/docs/user-guide.md` - Updated Quick Start guide

### Tools Already Existing (No Changes)

1. `wiki/apv/tools/parse-rfp-excel.py` - For Excel-specific parsing with TPS calculations
2. `wiki/apv/tools/excel-to-markdown.py` - Alternative Excel converter

**Note**: `parse-rfp-excel.py` is still recommended for Excel card volume files because it includes TPS calculations and Phase 1/Full Scope separation.

---

## Usage Examples

### Example 1: Convert PDF

```bash
python3 wiki/apv/tools/convert-to-markdown.py "rfp.pdf" "converted.md"
```

### Example 2: Convert Excel Questionnaire

```bash
python3 wiki/apv/tools/convert-to-markdown.py "questionnaire.xlsx" "converted.md"
```

### Example 3: Full APV Workflow

```bash
# Create project
mkdir -p "apv-projects/bank-issuing--2026-04-24"/{input,outputs,evidence}
cp "bank-rfp.pdf" "apv-projects/bank-issuing--2026-04-24/input/"

# Convert to markdown
cd "apv-projects/bank-issuing--2026-04-24"
python3 wiki/apv/tools/convert-to-markdown.py "input/bank-rfp.pdf" "input/converted.md"

# Process with skills
RFP_MD="input/converted.md"
/skill rfp-brainstorm "$RFP_MD" > outputs/01-brainstorm.md
# ... continue with other skills
```

---

## Conversion Quality

### Test Results: BBC Questionnaire.xlsx

**Original**: Excel file with 87 questions

**Converted to Markdown**:
- ✅ All questions preserved
- ✅ Table structure maintained
- ✅ Answers preserved
- ✅ Section headers intact
- ✅ APV metadata added

**Sample Output**:
```markdown
---
type: apv-meta
category: rfp-document
title: "Converted from BBC Questionnaire.xlsx"
created: 2026-04-24 22:41
tags: [apv, rfp, converted, markitdown]
source_file: BBC Questionnaire.xlsx
---

## Questionnaire
| No. | Question | Answers |
|-----|----------|---------|
| 1 | Applications Form | Branch staff will do Manual Key-in... |
...
```

---

## Troubleshooting

### Issue: markitdown command not found

**Solution**:
```bash
# Install markitdown
pip3 install --user --break-system-packages markitdown

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$PATH:/Users/stevenjiang/Library/Python/3.14/bin"
```

### Issue: Conversion produces empty output

**Possible Causes**:
1. Password-protected PDF
2. Scanned PDF (no text layer)
3. Corrupted file

**Solution**: Use OCR tools or manual transcription for scanned documents.

### Issue: Large file timeout

**Solution**: The wrapper has a 60-second timeout. For larger files, run markitdown directly:
```bash
markitdown large-file.pdf -o output.md
```

---

## Comparison: markitdown vs Existing Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **convert-to-markdown.py** | General document conversion | PDF, DOCX, PPTX → Markdown |
| **parse-rfp-excel.py** | Excel card volume parsing | Excel → Markdown + TPS calculations |
| **excel-to-markdown.py** | Excel table conversion | Excel → Markdown tables |

**Recommendation**:
- Use `convert-to-markdown.py` for general RFP documents (PDF, DOCX)
- Use `parse-rfp-excel.py` for Excel card volume files (includes TPS calculations)
- Use `excel-to-markdown.py` for Excel questionnaires (specialized format)

---

## Related

- [Microsoft markitdown GitHub](https://github.com/microsoft/markitdown)
- [[apv-user-guide]] - Complete APV user guide
- [[apv-excel-processing-guide]] - Excel-specific processing guide

---

**Version**: 1.0
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
