---
type: apv-meta
category: documentation
title: "APV Evidence Collection Directory"
created: 2026-04-24
tags: [apv, evidence, verification, compliance]
---

# APV Evidence Collection

This directory stores verification evidence for APV source URLs and compliance claims.

## Directory Structure

```
evidence/
├── README.md                    # This file
├── pricing/                     # Calculator screenshots and pricing evidence
│   ├── aws/
│   ├── azure/
│   └── gcp/
├── compliance/                  # Regulatory document snapshots
│   ├── pci-dss/
│   ├── singapore/
│   ├── malaysia/
│   └── ...
├── url-checks/                  # Automated verification reports
│   └── verification-YYYY-MM-DD.json
└── freshness-reports/           # Freshness check reports
    └── freshness-YYYY-MM-DD.json
```

## Evidence Requirements

### Pricing Evidence (30-day freshness)

All pricing claims must be supported by:
1. **Calculator Screenshot**: Full-page screenshot of official calculator
2. **Configuration Details**: Exact inputs used
3. **Timestamp**: When screenshot was captured
4. **Calculator URL**: Direct link to calculator

Example naming: `pricing/aws/eks-1000-tps-2026-04-24.png`

### Compliance Evidence (365-day freshness)

All compliance claims must cite:
1. **Official Source URL**: Direct link to regulatory document
2. **Section Reference**: Specific requirement number/section
3. **Capture Date**: When source was accessed
4. **Document Version**: Version/date of the regulation

Example: `compliance/pci-dss/requirement-8-2026-04-24.pdf`

## Collection Workflow

### Before RFP Response

1. **Run Verification Scripts**
   ```bash
   python ../tools/verify-source-urls.py --all > url-checks/verification-$(date +%Y-%m-%d).json
   python ../tools/check-freshness.py --all > freshness-reports/freshness-$(date +%Y-%m-%d).json
   ```

2. **Check Stale URLs**
   - Review any URLs flagged as stale
   - Update to current versions
   - Document changes in `url-changes.md`

3. **Capture Pricing Evidence**
   - For each pricing claim, capture calculator screenshot
   - Save with naming convention above
   - Update evidence index

4. **Verify Compliance Citations**
   - Ensure all compliance claims have working URLs
   - Cross-check section references
   - Document any discrepancies

### During RFP Response

1. **Source URL Enforcer Skills**
   - rfp-compliance: Requires source URLs for all regulations
   - rfp-pricer: Requires calculator URLs for all pricing

2. **Evidence Indexing**
   - Each claim should reference its evidence file
   - Use `[[evidence/...]]` wikilinks

### After RFP Response

1. **Evidence Package**
   - Compile all evidence into response package
   - Create manifest: `manifest.json`
   - Include verification reports

2. **Audit Trail**
   - Document any manual verifications
   - Note URLs that couldn't be auto-verified
   - Record expert review confirmations

## Automated Evidence Management

### Scheduled Checks

Run daily/weekly via cron:

```bash
# Weekly URL verification
0 2 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/verify-source-urls.py --all > \
  evidence/url-checks/verification-$(date +\%Y-\%m-\%d).json

# Weekly freshness check
0 3 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/check-freshness.py --all > \
  evidence/freshness-reports/freshness-$(date +\%Y-\%m-\%d).json
```

### Alert Thresholds

- **Pricing**: Alert if > 25 days old (5-day buffer)
- **Compliance**: Alert if > 340 days old (25-day buffer)
- **URL Access**: Alert if any URL returns non-200 status

## Evidence Templates

### Pricing Screenshot Template

```markdown
---
type: pricing-evidence
calculator: aws|azure|gcp
date-captured: YYYY-MM-DD
calculator-url: https://...
configuration:
  tps: 1000
  region: us-east-1
  instance-type: m5.large
monthly-cost: $XXX.XX
screenshot: path/to/screenshot.png
---

# AWS EKS Pricing for 1000 TPS

## Configuration
- **Calculator URL**: https://calculator.aws/#/estimate
- **TPS**: 1000
- **Region**: US East (N. Virginia)
- **Instance Type**: m5.large (x instances)
- **Monthly Cost**: $XXX.XX

## Screenshot
![Pricing Calculator](screenshot.png)

## Notes
- Captured on: 2026-04-24
- Verified by: [Name]
```

### Compliance Evidence Template

```markdown
---
type: compliance-evidence
regulation: pci-dss|mas|bnm|etc
requirement: 8.x.x
date-accessed: YYYY-MM-DD
source-url: https://...
version: 4.0
---

# PCI-DSS Requirement 8.2.3 Evidence

## Source
- **Document**: PCI DSS v4.0
- **Section**: Requirement 8.2.3
- **URL**: https://...
- **Accessed**: 2026-04-24

## Requirement Text
> [Quote the exact requirement]

## APV Implementation
[How APV system addresses this]

## Notes
- Verified by: Compliance Officer
- Verification date: 2026-04-24
```

## Quality Checks

Before submitting RFP response, verify:

- [ ] All pricing claims have calculator screenshots < 30 days old
- [ ] All compliance claims have working source URLs < 365 days old
- [ ] All URLs return HTTP 200 status
- [ ] All URLs are from trusted/official sources
- [ ] Evidence files follow naming convention
- [ ] Manifest includes all evidence
- [ ] Automated verification reports attached

## Related

- [[source-url-verification-system]] - Automated verification tools
- [[apv-accuracy-assurance]] - Accuracy framework requirements
- [[apv-implementation-plan-2026-04-24]] - Implementation status
