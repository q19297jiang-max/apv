# APV Accuracy Assurance Refactoring

**Date**: 2026-04-25
**Purpose**: Refactor APV system to ensure HIGH accuracy of pricing per apv-accuracy-assurance.md

## Overview

This refactoring implements the APV Accuracy Assurance Framework across all components of the APV system to ensure >98% accuracy for AWS pricing and >95% for other pricing data.

## Refactored Components

### 1. Source URL Validator Tool

**File**: `wiki/apv/tools/validate-source-urls.py`

**Purpose**: Validates that source URLs in wiki pages and RFP responses are:
- Present and not empty
- Properly formatted
- From official/primary sources
- Accessible (HTTP check)

**Features**:
- Checks frontmatter for source_url fields
- Validates content for embedded URLs
- Identifies forbidden sources (wikipedia, blogs)
- Flags unofficial sources
- Tests URL accessibility

**Usage**:
```bash
# Validate single file
python3 wiki/apv/tools/validate-source-urls.py --file <markdown-file>

# Validate directory
python3 wiki/apv/tools/validate-source-urls.py --directory <wiki-directory>

# Validate APV project
python3 wiki/apv/tools/validate-source-urls.py --project <project-path>

# Output to JSON
python3 wiki/apv/tools/validate-source-urls.py --project <project-path> --output results.json
```

**Exit Codes**:
- 0: All validations passed
- 1: Validation failed (issues found)

### 2. Pricing Freshness Checker Tool

**File**: `wiki/apv/tools/check-pricing-freshness.py`

**Purpose**: Ensures pricing data is current and alerts when refresh is needed.

**Freshness Rules**:
- Pricing pages: max 30 days old
- Alert at 25 days
- Block from RFP use if expired

**Features**:
- Extracts dates from frontmatter (verified_date, captured_date, price_valid_until)
- Calculates age of pricing data
- Categorizes as current, warning, or expired
- Lists files needing refresh

**Usage**:
```bash
# Check single file
python3 wiki/apv/tools/check-pricing-freshness.py --file <markdown-file>

# Check directory
python3 wiki/apv/tools/check-pricing-freshness.py --directory <pricing-directory>

# Check APV project
python3 wiki/apv/tools/check-pricing-freshness.py --project <project-path>

# Custom age limits
python3 wiki/apv/tools/check-pricing-freshness.py --project <project-path> --max-age 30 --warning-age 25
```

**Exit Codes**:
- 0: All pricing current
- 1: Pricing refresh required

### 3. Enhanced rfp-pricer Skill

**File**: `~/.claude/skills/rfp-pricer/prompt.md`

**Added Sections**:

#### Accuracy Assurance Validation
- Source URL validation requirements
- Pricing freshness validation requirements
- Evidence file validation requirements
- Accuracy validation requirements

#### Required Frontmatter
Every pricing output must include:
```yaml
---
type: apv-pricing
deployment_model: [SaaS Multi-Tenant / Dedicated Infrastructure]
cloud_provider: [AWS / Azure / GCP / Internal]
region: [region-code]
created: YYYY-MM-DD
verified: YYYY-MM-DD
verified_by: Infrastructure Architect
price_valid_until: YYYY-MM-DD
source_urls:
  - [primary source URL]
  - [calculator URL]
evidence_location: evidence/pricing/YYYY-MM-DD/
accuracy_target: ">98%"
---
```

#### Post-Generation Validation
After generating pricing output and BOM evidence files:
1. Run source URL validation
2. Run pricing freshness check
3. Only proceed to rfp-generator if all validations pass

#### Validation Exit Criteria
**DO NOT proceed to rfp-generator unless**:
- ✅ Source URL validation passes (0 issues)
- ✅ Freshness check passes (all pricing current)
- ✅ All evidence files created successfully
- ✅ BOM includes detailed specifications

### 4. Enhanced BOM Generator

**File**: `wiki/apv/tools/generate-bom.py`

**Added Features**:

#### Validation Functions
- `validate_component()`: Validates a single component
- `validate_components()`: Validates all components
- `is_official_domain()`: Checks if URL is from official domain
- `is_forbidden_domain()`: Checks if URL is from forbidden domain

#### Validation Checks
- Missing source URLs
- Forbidden sources (wikipedia, blogs)
- Unofficial sources
- Missing specifications
- Missing pricing data

#### Enhanced Output
- Validation summary in evidence files
- Validation status in BOM frontmatter
- Accuracy assurance metadata

**Usage**:
```bash
# Generate BOM with validation (default)
python3 wiki/apv/tools/generate-bom.py --project <project-path> --components '<json>'

# Skip validation (not recommended)
python3 wiki/apv/tools/generate-bom.py --project <project-path> --components '<json>' --skip-validation
```

### 5. Enhanced APV Orchestrator

**File**: `~/.claude/skills/apv/prompt.md`

**Added Workflow Steps**:

#### Step 5.6: Accuracy Validation Checks
After BOM generation:
1. Run source URL validation
2. Run pricing freshness check
3. Block progression to rfp-generator if validation fails

#### Accuracy Assurance Requirements
- Source URL mandatory
- Primary sources only
- No forbidden sources
- Freshness required (30 days max)
- Validation required
- Evidence files required

#### Accuracy Targets
| Content Type | Target Accuracy | Verification Method | Max Age |
|--------------|-----------------|---------------------|---------|
| AWS Pricing | >98% | Calculator verification | 30 days |
| Azure Pricing | >95% | Calculator verification | 30 days |
| GCP Pricing | >95% | Calculator verification | 30 days |
| SaaS Pricing | >95% | Internal rate sheet | 30 days |
| PCI-DSS Compliance | >95% | Expert review + source citation | 12 months |

### 6. Accuracy Audit Tool

**File**: `wiki/apv/tools/run-accuracy-audit.py`

**Purpose**: Runs monthly accuracy audits on compliance and pricing content.

**Audit Scope**:
- Compliance pages: Check for source URLs, verification dates, versions
- Pricing pages: Check for source URLs, verification dates, freshness
- Projects: Check source URL validation, freshness checks, evidence files

**Usage**:
```bash
# Audit wiki directory
python3 wiki/apv/tools/run-accuracy-audit.py --wiki <wiki-directory>

# Audit projects directory
python3 wiki/apv/tools/run-accuracy-audit.py --projects <projects-directory>

# Run full audit
python3 wiki/apv/tools/run-accuracy-audit.py --full

# Output to JSON
python3 wiki/apv/tools/run-accuracy-audit.py --full --output audit-results.json
```

**Audit Report**:
- Total items audited
- Total issues found
- Compliance rate percentage
- Action required items

## New Knowledge Base Files

### AWS Component Catalog
**File**: `wiki/apv/knowledge/pricing/aws-component-catalog.md`

**Content**: Detailed catalog of AWS components with:
- Exact instance types
- Hardware specifications (vCPU, memory, storage)
- Exact unit pricing with source URLs
- Regional multipliers
- Sizing guidelines

### Quick Reference Guide
**File**: `wiki/apv/docs/bom-component-quick-reference.md`

**Content**: Quick reference for creating detailed BOM entries
- Component templates for AWS services
- SaaS component templates
- Common instance types reference
- Cost calculation formulas
- Verification checklist

## Updated Documentation

### Detailed BOM Specifications
**File**: `wiki/apv/docs/detailed-bom-specifications.md`

**Content**: Enhancement documentation for detailed BOM specifications

## Workflow Changes

### Before (Old Workflow)
1. rfp-brainstorm
2. rfp-compliance
3. rfp-architect
4. rfp-calculator
5. rfp-pricer
6. Generate BOM (manual, no validation)
7. rfp-generator
8. apv-reviewer

### After (New Workflow)
1. rfp-brainstorm
2. rfp-compliance
3. rfp-architect
4. rfp-calculator
5. rfp-pricer (with validation rules)
6. **Generate BOM with validation**
7. **Source URL validation check**
8. **Pricing freshness check**
9. **Block if validation fails**
10. rfp-generator (only if validation passed)
11. apv-reviewer

## Validation Exit Criteria

**DO NOT proceed to rfp-generator unless**:
- ✅ Source URL validation passes (0 issues)
- ✅ Freshness check passes (all pricing current)
- ✅ All evidence files created successfully
- ✅ BOM includes detailed specifications for all components

**If validation fails**:
1. Identify and fix issues
2. Re-run failed validation
3. Only proceed when all validations pass

## Quality Metrics

### Accuracy Targets
- AWS Pricing: >98%
- Azure/GCP Pricing: >95%
- SaaS Pricing: >95%
- PCI-DSS Compliance: >95%

### Compliance Metrics
- % of compliance pages with source URLs: 100%
- % of pricing pages with source URLs: 100%
- % of RFP claims with citations: 100%
- % of source URLs that work: >99%
- % of pages verified by experts: 100%

## Related Documentation

- [[apv-accuracy-assurance]] — Original accuracy assurance framework
- [[bom-generation-improvements]] — BOM generation enhancement
- [[detailed-bom-specifications]] — Detailed BOM specifications
- [[aws-component-catalog]] — AWS component reference catalog
- [[bom-component-quick-reference]] — Quick reference guide

## Summary

This refactoring implements the complete APV Accuracy Assurance Framework across all components:

**Non-Negotiable Requirements**:
1. ✅ Source URL Mandatory - Every pricing claim must cite source
2. ✅ Primary Sources Only - No secondary sources or blogs
3. ✅ Expert Verification - Infrastructure Architect must verify
4. ✅ Date Tracking - All pricing must have verification dates
5. ✅ Freshness Monitoring - Pricing must be <30 days old
6. ✅ Evidence Files - BOM and verification documents required
7. ✅ Validation Checks - Must pass all validations before proceeding
8. ✅ Monthly Audits - Automated audits for accuracy monitoring

**Quality Goal**: >98% accuracy for AWS pricing, >95% for other pricing.

**Tools Created**:
- `validate-source-urls.py` - Source URL validation
- `check-pricing-freshness.py` - Pricing freshness monitoring
- `run-accuracy-audit.py` - Monthly accuracy audits

**Skills Updated**:
- `rfp-pricer` - Added validation rules and exit criteria
- `apv` (orchestrator) - Added accuracy validation workflow

**Tools Enhanced**:
- `generate-bom.py` - Added validation checks and reporting

**Knowledge Base Created**:
- `aws-component-catalog.md` - Detailed AWS component specifications
- `bom-component-quick-reference.md` - Quick reference for BOM creation
