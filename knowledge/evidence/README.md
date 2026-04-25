---
type: apv-meta
category: documentation
title: "APV Evidence Directory README"
version: "1.0"
created: 2026-04-24
tags: [apv, meta, evidence, documentation]
---

# APV Evidence Directory

## Purpose

Store evidence artifacts for all source URL claims in APV knowledge files, ensuring traceability and verification capability.

## Directory Structure

```
wiki/apv/knowledge/evidence/
├── pci-dss/              # PCI-DSS evidence
│   ├── req-1/            # Requirement 1 evidence
│   │   ├── pci-dss-v4_0.pdf
│   │   └── verification-2026-04-24.md
│   ├── req-2/            # Requirement 2 evidence
│   └── ...
├── countries/           # Country regulation evidence
│   ├── sg/              # Singapore
│   │   ├── mas-trm.pdf
│   │   ├── psa.pdf
│   │   ├── pdpa.pdf
│   │   └── verification-2026-04-24.md
│   ├── my/              # Malaysia
│   ├── ph/              # Philippines
│   ├── id/              # Indonesia
│   ├── th/              # Thailand
│   ├── tw/              # Taiwan
│   └── hk/              # Hong Kong
├── pricing/             # Pricing calculator evidence
│   ├── 2026-04-24/     # Dated pricing evidence
│   │   ├── aws-calculator-screenshot.png
│   │   ├── azure-calculator-screenshot.png
│   │   ├── gcp-calculator-screenshot.png
│   │   └── verification-2026-04-24.md
│   └── ...
└── reports/             # Compliance reports
    ├── url-compliance-2026-04-24.json
    ├── url-compliance-history.json
    └── freshness-reports.json
```

## Evidence Types

### Compliance Evidence
- **Official Documents**: PDF copies of regulations, standards
- **Verification Reports**: Date and verifier information
- **Screenshot Evidence**: Screenshots of official websites

### Pricing Evidence
- **Calculator Screenshots**: Full screenshots of official calculators
- **Configuration Details**: Input values and outputs
- **Verification Reports**: Date and verifier information

## File Naming Convention

### Verification Reports
- Format: `verification-YYYY-MM-DD.md`
- Contains: verification date, verified by, findings

### Screenshots
- Format: `{service}-calculator-screenshot-YYYY-MM-DD.png`
- Examples: `aws-calculator-screenshot-2026-04-24.png`

### Official Documents
- Use original document filename where possible
- Format: `{document-name}-{version}.{ext}`
- Examples: `pci-dss-v4_0.pdf`, `mas-trm-guidelines.pdf`

## Verification Report Template

```markdown
# Source URL Verification Report

**Date**: 2026-04-24
**Verified By**: Infrastructure Architect
**Scope**: All APV knowledge files

## Summary

| Metric | Result |
|--------|--------|
| Total Files Checked | 61 |
| Total URLs Checked | 61 |
| Valid URLs | 61 |
| Invalid URLs | 0 |
| Missing URLs | 0 |
| Compliance Rate | 100% |

## Freshness Summary

| Category | Threshold | Within Threshold | Stale |
|----------|-----------|-----------------|-------|
| Compliance | 365 days | 61 | 0 |
| Pricing | 30 days | 4 | 0 |
| Architecture | 365 days | 57 | 0 |

## Issues Found

No issues found. All files compliant with source URL requirements.

## Recommendations

Continue weekly verification to maintain 100% compliance.
```

## Related

- [[source-url-verification-system]] - Verification system documentation
- [[apv-accuracy-assurance]] - Accuracy framework requirements
