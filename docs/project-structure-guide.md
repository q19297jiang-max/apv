---
type: apv-meta
category: documentation
title: "APV Project Folder Structure Guide"
created: 2026-04-24
tags: [apv, documentation, project-structure, workflow]
sources:
  - "[[apv-user-guide]]"
---

# APV Project Folder Structure Guide

**Each RFP gets its own dedicated project folder for organization and separation.**

---

## Project Folder Concept

When processing a new RFP, the APV system creates a dedicated project folder that contains:
- The original RFP document
- All skill outputs
- All evidence collected
- Verification reports
- Summary documentation

This ensures:
- **Separation**: Different RFP responses never mix
- **Traceability**: Complete history for each RFP
- **Archival**: Easy to archive or share entire project
- **Collaboration**: Team can work on multiple RFPs simultaneously

---

## Project Folder Structure

### Complete Structure

```
apv-projects/
├── [customer-name]--[rfp-title]--[YYYY-MM-DD]/
│   ├── README.md                    # Project summary
│   ├── input/
│   │   └── [original-rfp-document]
│   ├── outputs/
│   │   ├── 01-brainstorm.md
│   │   ├── 02-compliance.md
│   │   ├── 03-architecture.md
│   │   ├── 04-sizing.md
│   │   ├── 05-pricing.md
│   │   ├── 06-response.md
│   │   └── 07-approval.md
│   ├── evidence/
│   │   ├── pricing/              # Calculator screenshots
│   │   │   ├── aws/
│   │   │   ├── azure/
│   │   │   └── gcp/
│   │   ├── compliance/           # Regulatory snapshots
│   │   │   ├── pci-dss/
│   │   │   ├── sg/
│   │   │   ├── my/
│   │   │   └── ...
│   │   └── verification/         # Verification reports
│   │       ├── url-checks.json
│   │       └── freshness.json
│   └── SUMMARY.md                  # Execution summary
└── [customer-name]--[rfp-title-2]--[YYYY-MM-DD]/
    └── ...
```

---

## Folder Naming Convention

### Format

```
[customer-name]--[rfp-title]--[YYYY-MM-DD]
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| customer-name | Bank or institution name (lowercase, hyphens for spaces) | `bbc-bank`, `dbs-bank`, `abc-corp` |
| rfp-title | Brief description of RFP (lowercase, hyphens for spaces) | `credit-card-issuing`, `acquiring-platform`, `digital-wallet` |
| date | Start date (YYYY-MM-DD) | `2026-04-24` |

### Examples

```
bbc-bank--credit-card-issuing--2026-04-24/
dbs-bank--acquiring-platform--2026-04-25/
abc-corp--digital-wallet--2026-04-26/
maybank--gateway-multi-region--2026-04-27/
singtel--prepaid-cards--2026-04-28/
```

---

## Output Files

### Standard Output Files (in outputs/)

| File | Skill | Content |
|------|-------|---------|
| `01-brainstorm.md` | rfp-brainstorm | Strategic analysis, approach options |
| `02-compliance.md` | rfp-compliance | Compliance matrix with source URLs |
| `03-architecture.md` | rfp-architect | Technical architecture design |
| `04-sizing.md` | rfp-calculator | Infrastructure sizing calculations |
| `05-pricing.md` | rfp-pricer | Cost breakdown with calculator URLs |
| `06-response.md` | rfp-generator | Final RFP response document |
| `07-approval.md` | apv-reviewer | Approval decision and confidence score |

### Supporting Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, customer info, status |
| `SUMMARY.md` | Execution summary, times, approval decision |

---

## Workflow

### Step 1: Create Project Folder

When starting a new RFP:

```bash
# Set project details
CUSTOMER="bbc-bank"
TITLE="credit-card-issuing"
DATE=$(date +%Y-%m-%d)

# Create project folder
PROJECT="apv-projects/${CUSTOMER}--${TITLE}--${DATE}"
mkdir -p "$PROJECT"/{input,outputs,evidence/{pricing,compliance,verification}}

# Verify
ls -R "$PROJECT"
```

### Step 2: Copy RFP Document

```bash
# Copy RFP to project input folder
cp /path/to/rfp.pdf "$PROJECT/input/"

# Or for text RFP
echo "# RFP Content" > "$PROJECT/input/rfp-summary.txt"
```

### Step 3: Run Skills (All Outputs to Project)

```bash
# Set project as working directory
cd "$PROJECT"

# Run skills (outputs automatically go to outputs/)
/skill rfp-brainstorm "input/[rfp-document]" > "outputs/01-brainstorm.md"
/skill rfp-compliance "input/[rfp-document]" > "outputs/02-compliance.md"
/skill rfp-architect "input/[rfp-document]" > "outputs/03-architecture.md"
/skill rfp-calculator "input/[rfp-document]" > "outputs/04-sizing.md"
/skill rfp-pricer "input/[rfp-document]" > "outputs/05-pricing.md"
/skill rfp-generator "input/[rfp-document]" > "outputs/06-response.md"
/skill apv-reviewer --response "outputs/06-response.md" > "outputs/07-approval.md"
```

### Step 4: Create Project README

```bash
cat > "$PROJECT/README.md" << EOF
# [Customer] - [RFP Title] Project

**Project Started**: [Date]
**Status**: In Progress | Complete | Approved | Rejected

## Project Details
- **Customer**: [Customer Name]
- **RFP Title**: [Title]
- **RFP Document**: [File in input/]
- **Card Type**: [Issuing/Acquiring/Gateway/Wallet]
- **Target Regions**: [Countries]

## Outputs
- [ ] 01-brainstorm.md - Strategic analysis
- [ ] 02-compliance.md - Compliance matrix
- [ ] 03-architecture.md - Technical design
- [ ] 04-sizing.md - Infrastructure sizing
- [ ] 05-pricing.md - Cost breakdown
- [ ] 06-response.md - Final response
- [ ] 07-approval.md - Approval decision

## Evidence
- Pricing screenshots: evidence/pricing/
- Compliance documents: evidence/compliance/
- Verification reports: evidence/verification/

## Summary
See SUMMARY.md for execution details.

## Next Steps
- [ ] Review approval decision
- [ ] Make any requested changes
- [ ] Submit to customer
- [ ] Archive project
EOF
```

### Step 5: Create Execution Summary

```bash
cat > "$PROJECT/SUMMARY.md" << EOF
# APV Execution Summary

**Project**: [Customer] - [RFP Title]
**Date**: [Date]
**Duration**: [Total time]

## Execution Timeline
| Skill | Start | End | Duration | Status |
|-------|-------|-----|----------|--------|
| rfp-brainstorm | [time] | [time] | [X min] | ✅ |
| rfp-compliance | [time] | [time] | [X min] | ✅ |
| rfp-architect | [time] | [time] | [X min] | ✅ |
| rfp-calculator | [time] | [time] | [X min] | ✅ |
| rfp-pricer | [time] | [time] | [X min] | ✅ |
| rfp-generator | [time] | [time] | [X min] | ✅ |
| apv-reviewer | [time] | [time] | [X min] | ✅ |

## Approval Decision
**Decision**: [Approve | Conditional | Reject]
**Confidence**: [X]%
**Critical Issues**: [N]
**Minor Issues**: [N]

## Output Files
All outputs located in: outputs/

## Evidence
- Pricing: evidence/pricing/
- Compliance: evidence/compliance/
- Verification: evidence/verification/
EOF
```

---

## Using Project Folders

### Switching Between Projects

```bash
# List all projects
ls apv-projects/

# Work on specific project
cd apv-projects/bbc-bank--credit-card-issuing--2026-04-24/

# View outputs
ls outputs/

# View summary
cat SUMMARY.md
```

### Comparing Multiple RFPs

```bash
# Compare responses for different customers
diff apv-projects/bbc-bank--issuing--2026-04-24/outputs/06-response.md \
     apv-projects/dbs-bank--issuing--2026-04-25/outputs/06-response.md
```

### Archiving Projects

```bash
# Archive completed project
tar czf apv-archives/bbc-bank--issuing--2026-04-24.tar.gz \
  apv-projects/bbc-bank--issuing--2026-04-24/

# Remove from active projects
rm -rf apv-projects/bbc-bank--issuing--2026-04-24/
```

---

## Multiple RFP Workflow

### Scenario: Processing Multiple RFPs Simultaneously

```bash
# Project 1: BBC Bank
PROJECT1="apv-projects/bbc-bank--issuing--2026-04-24"
mkdir -p "$PROJECT1"/{input,outputs,evidence}
cp bbc-rfp.pdf "$PROJECT1/input/"

# Project 2: DBS Bank
PROJECT2="apv-projects/dbs-bank--acquiring--2026-04-24"
mkdir -p "$PROJECT2"/{input,outputs,evidence}
cp dbs-rfp.pdf "$PROJECT2/input/"

# Process Project 1
cd "$PROJECT1"
/skill rfp-brainstorm "input/bbc-rfp.pdf" > "outputs/01-brainstorm.md"
# ... continue skills

# Process Project 2
cd "$PROJECT2"
/skill rfp-brainstorm "input/dbs-rfp.pdf" > "outputs/01-brainstorm.md"
# ... continue skills
```

---

## Team Collaboration

### Sharing Projects

To share a project with team members:

```bash
# Create shared location
SHARED="/shared/apv-projects"
cp -r apv-projects/bbc-bank--issuing--2026-04-24/ "$SHARED/"

# Team member can work in their own copy
cd "$SHARED/bbc-bank--issuing--2026-04-24/"
# Review outputs, add notes, etc.
```

### Project Handoff

When handing off RFP response to another team member:

```bash
# Project contains everything needed
apv-projects/bbc-bank--issuing--2026-04-24/
├── outputs/06-response.md     # Final response
├── outputs/07-approval.md     # Approval status
├── evidence/                   # All evidence
└── SUMMARY.md                  # Execution summary
```

---

## Project Folder Best Practices

### DO ✅

- Create new project folder for each RFP
- Use consistent naming convention
- Keep all outputs in `outputs/` folder
- Store evidence in project's `evidence/` folder
- Create README.md for project context
- Archive completed projects

### DON'T ❌

- Mix multiple RFP outputs in same folder
- Save outputs to root directory
- Skip project folder creation
- Use inconsistent naming
- Lose evidence (keep with project!)

---

## Migration: Old to New Structure

If you have existing RFP outputs not in project folders:

```bash
# Create project folder
mkdir -p "apv-projects/old-rfps--2026-04-24/outputs"

# Move existing outputs
mv brainstorm-output.md compliance-output.md architecture-output.md \
   sizing-output.md pricing-output.md rfp-response.md review-report.md \
   "apv-projects/old-rfps--2026-04-24/outputs/"

# Rename with numbers
cd "apv-projects/old-rfps--2026-04-24/outputs/"
mv brainstorm-output.md 01-brainstorm.md
mv compliance-output.md 02-compliance.md
mv architecture-output.md 03-architecture.md
mv sizing-output.md 04-sizing.md
mv pricing-output.md 05-pricing.md
mv rfp-response.md 06-response.md
mv review-report.md 07-approval.md
```

---

## Quick Reference

### Create New Project

```bash
CUSTOMER="[customer]"
TITLE="[brief-title]"
DATE=$(date +%Y-%m-%d)

mkdir -p "apv-projects/${CUSTOMER}--${TITLE}--${DATE}"/"{input,outputs,evidence/{pricing,compliance,verification}}
```

### Process RFP

```bash
PROJECT="apv-projects/${CUSTOMER}--${TITLE}--${DATE}"
cp rfp.pdf "$PROJECT/input/"
cd "$PROJECT"
# Run all skills, save to outputs/
```

### List Projects

```bash
ls apv-projects/
```

---

**Version**: 1.0
**Last Updated**: 2026-04-24
**Related**: [[apv-user-guide]], [[apv-operations-guide]]
