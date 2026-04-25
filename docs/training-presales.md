---
type: apv-meta
category: documentation
title: "APV Pre-Sales Training Guide"
created: 2026-04-24
tags: [apv, documentation, training, presales]
---

# APV Pre-Sales Training Guide

**Audience**: Pre-sales Team
**Duration**: 1 hour
**Prerequisites**: Basic understanding of RFP process

---

## Learning Objectives

After this training, you will be able to:
1. Understand the APV system and its benefits
2. Create project folders and organize RFP documents
3. Run the 7-skill chain to generate RFP responses
4. Review and approve generated responses
5. Handle common issues

---

## What is APV?

**APV (AI-Powered RFP Velocity)** is an automated RFP response system that:
- Processes RFP documents through 7 specialized skills
- Generates compliant, accurate responses in 60-90 minutes
- Ensures 100% source URL compliance
- Reduces review time to 15 minutes

**Key Benefits**:
- **90% Time Reduction**: 60-90 minutes vs weeks
- **100% Compliance**: Every claim cites official sources
- **High Accuracy**: PCI-DSS and Asian regulations from official sources

---

## Quick Start: Your First RFP

### Step 1: Create Project Folder

```bash
# Set project details
CUSTOMER="bank-name"
TITLE="credit-card-issuing"
DATE=$(date +%Y-%m-%d)

# Create project folder
mkdir -p "apv-projects/${CUSTOMER}--${TITLE}--${DATE}"/"{input,outputs,evidence/{pricing,compliance,verification}}

# Copy RFP to project
cp /path/to/rfp.pdf "apv-projects/${CUSTOMER}--${TITLE}--${DATE}/input/"
```

### Step 2: Convert to Markdown (if needed)

```bash
cd "apv-projects/${CUSTOMER}--${TITLE}--${DATE}"

# If RFP is PDF, DOCX, XLSX, etc., convert to markdown
python3 wiki/apv/tools/convert-to-markdown.py "input/rfp.pdf" "input/converted.md"

# If already markdown, skip conversion
RFP_MD="input/converted.md"  # or "input/rfp.md"
```

### Step 3: Run All Skills

```bash
# All skills use the markdown file
/skill rfp-brainstorm "$RFP_MD" > outputs/01-brainstorm.md
/skill rfp-compliance "$RFP_MD" > outputs/02-compliance.md
/skill rfp-architect "$RFP_MD" > outputs/03-architecture.md
/skill rfp-calculator "$RFP_MD" > outputs/04-sizing.md
/skill rfp-pricer "$RFP_MD" > outputs/05-pricing.md
/skill rfp-generator "$RFP_MD" > outputs/06-response.md
/skill apv-reviewer --response outputs/06-response.md > outputs/07-approval.md
```

**Total Time**: 60-90 minutes

### Step 4: Review and Approve

```bash
# Check approval decision
cat outputs/07-approval.md

# View confidence score (should be ≥90%)
# Address any issues if marked "Conditional" or "Reject"
```

---

## The 7 APV Skills Explained

### Skill 1: rfp-brainstorm (5-10 min)

**What it does**: Analyzes RFP, generates approach options

**Output**: Executive summary, compliance landscape, 2-3 architecture options

**Your role**: Review the recommended approach before proceeding

### Skill 2: rfp-compliance (10-15 min)

**What it does**: Maps requirements to regulations with source URLs

**Output**: Detailed compliance matrix

**Your role**: Verify all regulations are covered

### Skill 3: rfp-architect (10-15 min)

**What it does**: Designs technical architecture

**Output**: Architecture design with component specifications

**Your role**: Review cloud provider and region selection

### Skill 4: rfp-calculator (5-10 min)

**What it does**: Calculates infrastructure sizing

**Output**: Sizing calculations with capacity planning

**Your role**: Verify TPS calculations make sense

### Skill 5: rfp-pricer (5-10 min)

**What it does**: Generates cost estimates with calculator URLs

**Output**: Detailed cost breakdown

**Your role**: Review pricing assumptions

### Skill 6: rfp-generator (10-15 min)

**What it does**: Synthesizes all outputs into RFP response

**Output**: Complete RFP response document

**Your role**: Final review before submission

### Skill 7: apv-reviewer (15 min)

**What it does**: Unified approval verification

**Output**: Approval decision with confidence score

**Your role**: Approve or request changes

---

## Common Use Cases

### Use Case 1: New Credit Card Issuing RFP

**Input**: RFP for credit card issuing system

**Expected Output**:
- Compliance: PCI-DSS + country regulations
- Architecture: Cloud-native (EKS/AKS/GKE)
- Sizing: Based on transaction volume
- Pricing: With official calculator URLs

### Use Case 2: Low Volume Opportunity

**Input**: Small bank, 2,000 cards, 0.5 TPS

**Expected**: Recommends SaaS multi-tenant

### Use Case 3: Multi-Region Deployment

**Input**: RFP requiring deployment in 3 countries

**Expected**: Compliance matrix for all 3 countries

---

## Troubleshooting

### Issue: Skill Not Found

**Error**: `Skill not found: rfp-xxx`

**Solution**:
```bash
ls ~/.claude/skills/
# Expected: rfp-brainstorm, rfp-compliance, rfp-architect, etc.
```

### Issue: No Knowledge Found

**Error**: `No knowledge on [topic]`

**Solution**:
- Check if country is supported (SG, MY, PH, ID, TH, TW, HK)
- Check if card type is supported
- If missing, add to wiki or note as limitation

### Issue: Source URL Missing

**Error**: `Source URL not found for [claim]`

**Solution**:
```bash
python wiki/apv/tools/verify-source-urls.py --all
```

### Issue: Low Confidence Score

**Error**: apv-reviewer shows <90% confidence

**Solution**:
1. Check outputs/07-approval.md for issues
2. Address missing source URLs
3. Add missing content
4. Re-run skills if needed

---

## Tips for Best Results

### 1. Prepare Your RFP

- Ensure RFP is searchable (PDF, DOCX)
- Include all requirements and questions
- Note target countries and regions
- Note expected transaction volumes

### 2. Start with Brainstorm

- Always run rfp-brainstorm first
- Review the recommended approach
- Ask clarification questions early

### 3. Verify Source URLs

- Run verification before finalizing
- Check freshness of sources
- Collect evidence for key claims

### 4. Review Before Submitting

- Always run apv-reviewer
- Check confidence score (≥90%)
- Address any "Conditional" or "Reject" items

---

## Project Folder Structure

```
apv-projects/[customer]--[title]--[date]/
├── input/
│   ├── original-rfp.pdf
│   └── converted.md          # Converted to markdown
├── outputs/
│   ├── 01-brainstorm.md
│   ├── 02-compliance.md
│   ├── 03-architecture.md
│   ├── 04-sizing.md
│   ├── 05-pricing.md
│   ├── 06-response.md        # Final RFP response
│   └── 07-approval.md        # Approval decision
└── evidence/
    ├── pricing/              # Calculator screenshots
    ├── compliance/           # Regulatory snapshots
    └── verification/         # Verification reports
```

---

## Quality Checklist

Before submitting RFP response:

- [ ] All 7 skills completed successfully
- [ ] apv-reviewer confidence ≥90%
- [ ] All source URLs are valid
- [ ] All compliance requirements addressed
- [ ] Pricing includes calculator URLs
- [ ] Architecture design is complete
- [ ] Evidence collected for key claims

---

## Getting Help

### Documentation

- [[apv-user-guide]] - Complete user guide
- [[apv-skill-reference]] - All skills reference
- [[apv-troubleshooting]] - Common issues

### Tools

- `wiki/apv/tools/verify-source-urls.py` - Verify source URLs
- `wiki/apv/tools/check-freshness.py` - Check URL freshness
- `wiki/apv/tools/convert-to-markdown.py` - Convert documents

### Support

For issues or questions:
1. Check this guide first
2. Check troubleshooting guide
3. Review test examples

---

## Next Steps

After completing this training:

1. **Process a Sample RFP**: Practice with a test RFP
2. **Review Documentation**: Read skill-specific guides
3. **Run Verification**: Test URL verification scripts
4. **Ask Questions**: Clarify any uncertainties

---

**Training Duration**: 1 hour
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
