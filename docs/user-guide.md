---
type: apv-meta
category: documentation
title: "APV User Guide"
created: 2026-04-24
tags: [apv, documentation, user-guide, quick-start]
sources:
  - "[[apv-system-index]]"
  - "[[apv-skills-directory]]"
---

# APV User Guide

**AI-Powered RFP Velocity (APV) System**
**Version**: 1.0
**Last Updated**: 2026-04-24

---

## What is APV?

APV (AI-Powered RFP Velocity) is an automated RFP response system for fintech banking. It processes Request for Proposal (RFP) documents through a chain of 7 specialized skills, generating comprehensive, compliant responses in **60-90 minutes** instead of weeks.

### Key Benefits

- **90% Time Reduction**: 60-90 minutes vs 150 minutes (old 5-gate process)
- **100% Source URL Compliance**: Every claim cites official sources
- **15-Minute Review**: Unified approval replaces 5-gate process
- **High Accuracy**: PCI-DSS and Asian banking regulations from official sources

---

## Quick Start

### Prerequisites

1. **Claude Code** installed and configured
2. **APV Wiki** at `/Users/stevenjiang/workspace/mykb/wiki/apv/`
3. **Skills** installed at `~/.claude/skills/`
4. **Microsoft markitdown** installed: `pip3 install --user --break-system-packages markitdown`
5. **RFP Document** (PDF, DOCX, XLSX, PPTX, or markdown)

### Basic Usage

#### Step 1: Create Project Folder (NEW - Required)

```bash
# Set project details
CUSTOMER="bbc-bank"
TITLE="credit-card-issuing"
DATE=$(date +%Y-%m-%d)

# Create project folder
mkdir -p "apv-projects/${CUSTOMER}--${TITLE}--${DATE}"/"{input,outputs,evidence/{pricing,compliance,verification}}

# Copy RFP to project
cp /path/to/rfp.pdf "apv-projects/${CUSTOMER}--${TITLE}--${DATE}/input/"
```

**Project Folder Structure**:
```
apv-projects/[customer]--[title]--[date]/
├── input/                    # Original + converted RFP
│   ├── original-rfp.pdf      # Original document
│   └── converted.md          # Converted to markdown
├── outputs/                  # All skill outputs
│   ├── 01-brainstorm.md
│   ├── 02-compliance.md
│   ├── 03-architecture.md
│   ├── 04-sizing.md
│   ├── 05-pricing.md
│   ├── 06-response.md
│   └── 07-approval.md
└── evidence/                  # Evidence for this RFP
    ├── pricing/              # Calculator screenshots
    ├── compliance/           # Regulatory snapshots
    └── verification/         # Verification reports
```

#### Step 2: Convert to Markdown (NEW - Required for non-markdown files)

**IMPORTANT**: Always convert non-markdown files to markdown BEFORE processing.

```bash
# Navigate to project folder
cd apv-projects/${CUSTOMER}--${TITLE}--${DATE}

# Convert RFP to markdown (if not already .md)
python3 wiki/apv/tools/convert-to-markdown.py "input/original-rfp.pdf" "input/converted.md"
```

**Supported Formats**: PDF, DOCX, XLSX, PPTX, HTML, TXT, and more

**Why convert?**
- LLM processes markdown more accurately than binary formats
- Preserves document structure (tables, headings, lists)
- Reduces extraction errors

#### Step 3: Run Full Skill Chain

```bash
# Navigate to project folder
cd apv-projects/${CUSTOMER}--${TITLE}--${DATE}

# Use converted markdown file for all skills
RFP_MD="input/converted.md"  # Or use original if already markdown

# Run all skills (outputs go to outputs/ folder)
/skill rfp-brainstorm "$RFP_MD" > outputs/01-brainstorm.md
/skill rfp-compliance "$RFP_MD" > outputs/02-compliance.md
/skill rfp-architect "$RFP_MD" > outputs/03-architecture.md
/skill rfp-calculator "$RFP_MD" > outputs/04-sizing.md
/skill rfp-pricer "$RFP_MD" > outputs/05-pricing.md
/skill rfp-generator "$RFP_MD" > outputs/06-response.md
/skill apv-reviewer --response outputs/06-response.md > outputs/07-approval.md
```

**Total Time**: 60-90 minutes
**Output**: Complete RFP response in `outputs/06-response.md`
**Approval**: Verification report in `outputs/07-approval.md`

---

## The 7 APV Skills

### Skill 1: rfp-brainstorm

**Purpose**: Generate approach options and strategic direction

**Input**: RFP document
**Output**: Executive summary, compliance landscape, 2-3 architecture options
**Time**: 5-10 minutes

**What it does**:
- Analyzes RFP requirements
- Identifies applicable regulations (PCI-DSS, country-specific)
- Presents 2-3 valid architectural approaches
- Flags knowledge gaps
- Generates clarification questions

**Use when**: Starting any new RFP response

---

### Skill 2: rfp-compliance

**Purpose**: Map requirements to regulations with source URL enforcement

**Input**: RFP document + brainstorm output
**Output**: Detailed compliance matrix with source URLs
**Time**: 10-15 minutes

**What it does**:
- Maps all requirements to PCI-DSS requirements (1-12)
- Maps to country-specific regulations (SG, MY, PH, ID, TH, TW, HK)
- EVERY claim includes source URL from official sources
- Identifies compliance gaps
- Specifies evidence requirements

**Use when**: Need detailed compliance mapping

**Critical**: 100% source URL compliance enforced

---

### Skill 3: rfp-architect

**Purpose**: Design detailed payment architecture

**Input**: RFP document + compliance output
**Output**: Architecture design with component specifications
**Time**: 10-15 minutes

**What it does**:
- Designs card system architecture (issuing, acquiring, gateway)
- Selects cloud provider and region
- Specifies components (compute, database, storage, network)
- Maps security controls to PCI-DSS requirements
- Plans high availability and disaster recovery

**Use when**: Need technical architecture design

---

### Skill 4: rfp-calculator

**Purpose**: Calculate precise infrastructure sizing

**Input**: RFP document + architecture output
**Output**: Sizing calculations with capacity planning
**Time**: 5-10 minutes

**What it does**:
- Calculates TPS from transaction volumes
- Sizes compute instances
- Plans capacity for growth
- Configures auto-scaling
- Calculates resource requirements by region

**Use when**: Need infrastructure sizing

**Formulas**:
```
Average TPS = Daily Transactions / 86,400
Peak TPS = Average TPS × 4 (default peak multiplier)
Min Instances = (Average TPS / TPS per Instance) + 1
Max Instances = (Peak TPS × 1.5) / TPS per Instance
```

---

### Skill 5: rfp-pricer

**Purpose**: Generate cost estimates with calculator URLs

**Input**: RFP document + calculator output
**Output**: Detailed cost breakdown with source URLs
**Time**: 5-10 minutes

**What it does**:
- Generates pricing for AWS/Azure/GCP
- Calculates compute, database, storage, data transfer costs
- Includes optimization opportunities (reserved instances)
- EVERY pricing claim cites official calculator URLs
- Provides 3-year cost projections

**Use when**: Need cost estimates

**Critical**: 100% source URL compliance enforced

---

### Skill 6: rfp-generator

**Purpose**: Synthesize all outputs into comprehensive RFP response

**Input**: All previous skill outputs
**Output**: Complete RFP response document
**Time**: 10-15 minutes

**What it does**:
- Combines outputs from skills 1-5
- Follows RFP response template structure
- Ensures all claims have source citations
- Includes source URL index in appendix
- Adds accuracy assurance statement

**Use when**: Need final RFP response document

**Critical**: 100% source URL compliance enforced

---

### Skill 7: apv-reviewer

**Purpose**: Unified 15-minute approval verification

**Input**: Complete RFP response
**Output**: Approval decision with confidence score
**Time**: 15 minutes

**What it does**:
- Verifies source URL compliance (30% weight)
- Checks content completeness (25% weight)
- Validates accuracy (25% weight)
- Reviews compliance coverage (15% weight)
- Assesses quality (5% weight)

**Approval Criteria**:
| Decision | Source URL % | Confidence | Notes |
|----------|--------------|------------|-------|
| ✅ Approve | ≥ 95% | ≥ 90% | All critical pass |
| ⚠️ Conditional | ≥ 90% | ≥ 80% | Minor issues OK |
| ❌ Reject | < 90% | < 80% | Critical fails |

**Use when**: Ready to submit RFP response

**Replaces**: Original 5-gate approval process (150 minutes → 15 minutes)

---

## Common Use Cases

### Use Case 1: New Credit Card Issuing RFP

```bash
# Given: RFP for credit card issuing system for Singapore bank
# Run: Full APV chain

/apv rfp singapore-bank-issuing-rfp.pdf
```

**Expected Outputs**:
- Compliance: PCI-DSS + MAS regulations (Singapore)
- Architecture: EKS/AKS/GKE with ap-southeast-1 region
- Sizing: Based on transaction volume
- Pricing: With official calculator URLs

---

### Use Case 2: Low Volume SaaS Opportunity

```bash
# Given: Small bank, 2,000 cards, 0.5 TPS
# Run: rfp-brainstorm first to get recommendation

/skill rfp-brainstorm --rfp small-bank-rfp.pdf
```

**Expected**: Recommends SaaS multi-tenant (cost-effective for low volume)

---

### Use Case 3: Multi-Region Deployment

```bash
# Given: RFP requiring deployment in 3 Asian countries
# Run: rfp-compliance to map all country regulations

/skill rfp-compliance --rfp multi-region-rfp.pdf
```

**Expected**: Compliance matrix for all 3 countries with source URLs

---

## Reference Data

### Supported Card Types

| Type | Wiki Reference |
|------|----------------|
| Issuing | [[issuing]] |
| Acquiring | [[acquiring]] |
| Gateway | [[gateway]] |
| Digital Wallet | [[digital-wallet]] |

### Supported Cloud Providers

| Provider | Region (Singapore) | Wiki Reference |
|----------|-------------------|----------------|
| AWS | ap-southeast-1 | [[aws-eks]], [[aws-rds]] |
| Azure | southeastasia | [[azure-aks]], [[azure-db]] |
| GCP | asia-southeast1 | [[gcp-gke]], [[gcp-cloudsql]] |

### Supported Countries

| Country | Regulations | Wiki Reference |
|----------|-------------|----------------|
| Singapore | MAS TRM, PSA, PDPA, CSA | [[mas-trm]], [[psa]], [[pdpa-sg]], [[csa]] |
| Malaysia | BNM RM, PSA, PDPA, FSA | [[bnm-rm]], [[psa-my]], [[pdpa-my]], [[fsa]] |
| Philippines | BSP Circular, PDPA, NPSP | [[bsp-circular]], [[pdpa-ph]], [[npsp]] |
| Indonesia | BI Regulations, PDPA | [[bi-regulations]], [[pdpa-id]] |
| Thailand | BOT Payment, PDPA | [[bot-payment]], [[pdpa-th]] |
| Taiwan | FSC Payment, PDPA | [[fsc-payment]], [[pdpa-tw]] |
| Hong Kong | HKMA GM, PDPO | [[hkma-gm]], [[pdpo-hk]] |

---

## Troubleshooting

### Issue: Skill Not Found

**Error**: `Skill not found: rfp-xxx`

**Solution**:
```bash
# Check skill installation
ls ~/.claude/skills/

# Expected: rfp-brainstorm, rfp-compliance, rfp-architect, rfp-calculator, rfp-pricer, rfp-generator, apv-reviewer, apv
```

---

### Issue: No Knowledge Found

**Error**: `No knowledge on [topic]`

**Solutions**:
1. Check if country is supported (only 7 Asian countries)
2. Check if card type is supported (issuing, acquiring, gateway, wallet)
3. Add knowledge to wiki if missing

---

### Issue: Source URL Missing

**Error**: `Source URL not found for [claim]`

**Solutions**:
1. Check knowledge file frontmatter for `source_url` field
2. Verify source URL is valid and accessible
3. Run `python wiki/apv/tools/verify-source-urls.py --all` to check all URLs

---

### Issue: High Execution Time

**Symptom**: Skills taking longer than estimated

**Solutions**:
1. Check if reading too many knowledge files (optimize by reading only relevant files)
2. Check if RFP document is very large (consider splitting)
3. Run `python wiki/apv/tools/check-freshness.py --all` to verify URL freshness

---

## Tips for Best Results

### 1. Prepare Your RFP

- Ensure RFP is in searchable format (PDF, DOCX)
- Include all requirements and questions
- Note target countries and regions
- Note expected transaction volumes

### 2. Start with Brainstorm

- Always run rfp-brainstorm first to understand options
- Review the recommended approach before proceeding
- Ask clarification questions early

### 3. Verify Source URLs

- Run verification scripts before finalizing response
- Check freshness of pricing sources (30-day limit)
- Check freshness of compliance sources (365-day limit)

```bash
python wiki/apv/tools/verify-source-urls.py --all
python wiki/apv/tools/check-freshness.py --all
```

### 4. Review Before Submitting

- Always run apv-reviewer before submitting
- Check confidence score (should be ≥90%)
- Address any "Conditional" or "Reject" items

### 5. Collect Evidence

- Save calculator screenshots for pricing claims
- Save regulatory document snapshots for compliance claims
- Store in `wiki/apv/evidence/` with proper naming

---

## File Structure

```
wiki/apv/
├── knowledge/               # Compliance and technical knowledge
│   ├── compliance/         # PCI-DSS, country regulations
│   ├── card-systems/       # Issuing, acquiring, gateway, etc.
│   ├── infrastructure/     # Cloud service patterns
│   └── sizing/             # TPS calculator, pricing
├── skills/                 # Skill documentation (wiki level)
│   ├── rfp-brainstorm/     # Individual skill docs
│   ├── rfp-compliance/
│   └── ...
├── templates/              # RFP response templates
├── tests/                  # Test infrastructure
├── tools/                  # Verification scripts
│   ├── verify-source-urls.py
│   └── check-freshness.py
└── evidence/               # Evidence storage
    ├── pricing/           # Calculator screenshots
    ├── compliance/        # Regulatory snapshots
    └── url-checks/        # Verification reports
```

---

## Next Steps

After reading this guide:

1. **Try the Quick Start**: Process a sample RFP
2. **Read Skill Guides**: Detailed documentation for each skill
3. **Run Verification Scripts**: Ensure source URLs are valid
4. **Check Examples**: Review sample outputs in `wiki/apv/tests/output/`

---

## Getting Help

### Documentation

- [[apv-system-index]] - Complete APV system documentation
- [[apv-skills-directory]] - All skills directory
- [[source-url-verification-system]] - Verification system guide

### Troubleshooting

See "Troubleshooting" section above or check:
- `wiki/apv/tools/` - Verification scripts with help output
- `wiki/apv/tests/` - Test examples and expected outputs

### Support

For issues or questions:
1. Check this guide first
2. Check skill-specific documentation
3. Review test examples
4. Check implementation plan status

---

**Version**: 1.0
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
