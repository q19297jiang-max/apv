---
type: apv-meta
category: system
title: "APV Source URL Verification System"
version: "1.0"
created: 2026-04-24
verified_by: "Infrastructure Architect"
tags: [apv, meta, verification, automation]
---

# APV Source URL Verification System

## Overview

Automated system to verify source URL compliance across all APV knowledge files, ensuring 100% compliance with the accuracy assurance framework.

## Components

### 1. URL Validator Script
**Purpose**: Check all source URLs in APV knowledge files

**Location**: `wiki/apv/meta/verify-source-urls.py`

**Functions**:
- Scan all markdown files in `wiki/apv/knowledge/`
- Extract source URLs from frontmatter
- Check URL accessibility (HTTP 200)
- Flag broken or missing URLs
- Generate compliance report

### 2. Freshness Tracker
**Purpose**: Track when source URLs were last verified

**Location**: `wiki/apv/meta/url-freshness.json`

**Data Schema**:
```json
{
  "last_check": "2026-04-24T10:00:00Z",
  "urls": {
    "wiki/apv/knowledge/compliance/pci-dss/req-1.md": {
      "source_url": "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf",
      "last_verified": "2026-04-24",
      "status": "valid",
      "http_status": 200
    }
  },
  "summary": {
    "total_urls": 61,
    "valid": 61,
    "invalid": 0,
    "missing": 0,
    "compliance_rate": "100%"
  }
}
```

### 3. Evidence Directory Structure
**Purpose**: Store source URL evidence (screenshots, documents)

**Location**: `wiki/apv/knowledge/evidence/`

```
evidence/
├── pci-dss/
│   ├── req-1/
│   │   ├── pci-dss-v4_0.pdf
│   │   └── verification-2026-04-24.md
├── countries/
│   ├── sg/
│   │   ├── mas-trm.pdf
│   │   └── verification-2026-04-24.md
│   └── ...
├── pricing/
│   ├── 2026-04-24/
│   │   ├── aws-calculator-screenshot.png
│   │   ├── azure-calculator-screenshot.png
│   │   └── verification-2026-04-24.md
│   └── ...
└── reports/
    ├── url-compliance-2026-04-24.json
    └── url-compliance-history.json
```

### 4. Compliance Report Template
**Purpose**: Standard format for source URL compliance reports

**Location**: `wiki/apv/knowledge/evidence/reports/url-compliance-YYYY-MM-DD.json`

**Data Schema**:
```json
{
  "report_date": "2026-04-24T10:00:00Z",
  "report_version": "1.0",
  "verified_by": "Infrastructure Architect",
  "summary": {
    "total_files_checked": 61,
    "total_urls_checked": 61,
    "valid_urls": 61,
    "invalid_urls": 0,
    "missing_urls": 0,
    "compliance_percentage": 100
  },
  "files": [
    {
      "file": "wiki/apv/knowledge/compliance/pci-dss/req-1.md",
      "has_source_url": true,
      "source_url": "https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf",
      "url_accessible": true,
      "http_status": 200,
      "ssl_valid": true,
      "last_verified": "2026-04-24"
    }
  ],
  "issues": [],
  "recommendations": []
}
```

## Verification Schedule

| Task | Frequency | Responsible |
|------|-----------|-------------|
| URL Validation Scan | Weekly | Wiki Curator |
| Freshness Check | Weekly | Wiki Curator |
| Compliance Report Generation | Weekly | Wiki Curator |
| Expert Verification | Monthly | Compliance Officer / Infrastructure Architect |

## Frontmatter Requirements

All APV knowledge files MUST include:

```yaml
---
type: apv-knowledge
source_url: "https://official-source-url"  # REQUIRED
source_document: "Document Name"           # REQUIRED for compliance
source_version: "1.0"                      # REQUIRED if versioned
captured_date: YYYY-MM-DD                 # REQUIRED
verified_by: "Role Name"                   # REQUIRED
last_verified: YYYY-MM-DD                # REQUIRED
freshness_days: 365                      # REQUIRED (compliance: 365, pricing: 30)
tags: [apv, category, topic]
---
```

## Verification Checklist

### For Compliance Pages (PCI-DSS, Country Regulations)
- [ ] source_url present and valid
- [ ] Source URL is official (regulator or standards body)
- [ ] Source URL is accessible (HTTP 200)
- [ ] Source document/version specified
- [ ] Capture date within 12 months
- [ ] Verification by Compliance Officer
- [ ] Evidence artifact stored

### For Pricing Pages
- [ ] source_url present (calculator URL)
- [ ] Source URL is official calculator
- [ ] Source URL is accessible
- [ ] Calculator screenshot stored in evidence/
- [ ] Capture date within 30 days
- [ ] Verification by Infrastructure Architect
- [ ] Calculator comparison stored (if applicable)

### For Architecture/Technical Pages
- [ ] source_url present (documentation URL)
- [ ] Source URL is official vendor documentation
- [ ] Source URL is accessible
- [ ] Capture date within 12 months
- [ ] Verification by Infrastructure Architect

## Automated Checks

### Weekly Checks (Every Monday)
```bash
# Run URL validation script
python3 wiki/apv/meta/verify-source-urls.py

# Generate compliance report
python3 wiki/apv/meta/generate-compliance-report.py

# Check freshness
python3 wiki/apv/meta/check-freshness.py

# Alert if any issues found
```

### Freshness Alerts

| Page Type | Freshness Threshold | Alert If |
|-----------|-------------------|----------|
| Compliance | 365 days (12 months) | >365 days since verification |
| Pricing | 30 days | >30 days since verification |
| Architecture | 365 days | >365 days since verification |

## Usage

### Running Verification
```bash
# Full verification
python3 wiki/apv/meta/verify-source-urls.py --path wiki/apv/knowledge

# Compliance report
python3 wiki/apv/meta/generate-compliance-report.py

# Freshness check
python3 wiki/apv/meta/check-freshness.py --days 30
```

### Integration with APV Workflow

- Run before generating any RFP response
- Run as part of apv-reviewer skill
- Include compliance percentage in unified checklist
- Flag any compliance issues for human review

## Related

- [[apv-accuracy-assurance]] - Accuracy framework requirements
- [[apv-task-list-revised]] - Task 1.12 details
- [[unified-checklist]] - Approval checklist with source URL checks
