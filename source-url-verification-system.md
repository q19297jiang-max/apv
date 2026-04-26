---
type: apv-meta
category: documentation
title: "Source URL Verification System"
created: 2026-04-24
tags: [apv, verification, urls, compliance, automation]
sources:
  - "[[apv-accuracy-assurance]]"
---

# Source URL Verification System

Scripted verification system for ensuring APV source URLs are valid, accessible, and fresh. Scheduler-based automation is planned, but the repo currently proves the scripts more strongly than an always-on operating loop.

## Overview

The Source URL Verification System ensures 100% source URL compliance for all APV-generated RFP responses. It validates that:

1. **URLs are well-formed** - Valid URL syntax
2. **URLs are accessible** - Return HTTP 200-299 status
3. **URLs are from trusted sources** - Official regulatory and vendor domains
4. **URLs are fresh** - Within age limits (30 days for pricing, 365 days for compliance)

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │      APV Wiki Content               │
                    │  (compliance, pricing, templates)   │
                    └──────────────┬──────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────────────┐
                    │   URL Extractor (regex patterns)     │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                              ▼
        ┌───────────────────────┐    ┌───────────────────────┐
        │  verify-source-urls.py│    │  check-freshness.py    │
        │                       │    │                       │
        │  • URL format         │    │  • Last-Modified      │
        │  • Accessibility      │    │  • Age calculation    │
        │  • Trusted domains    │    │  • Freshness limits   │
        └───────────┬───────────┘    └───────────┬───────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌─────────────────────────────────────┐
                    │         Verification Report          │
                    │  (valid, invalid, stale, fresh)     │
                    └─────────────────────────────────────┘
```

## Tools

### verify-source-urls.py

Validates URL format, accessibility, and trusted domains.

**Usage:**
```bash
# Check single file
python tools/verify-source-urls.py wiki/apv/compliance/pci-dss-overview.md

# Check directory
python tools/verify-source-urls.py wiki/apv/

# Check all APV wiki files
python tools/verify-source-urls.py --all

# Check single URL
python tools/verify-source-urls.py --check https://pcisecuritystandards.org/
```

**What it checks:**
- URL syntax validity
- HTTP response status (200-299 = OK)
- Domain is in trusted sources list
- Rate limiting to avoid overwhelming servers

**Trusted Domains:**
- PCI-DSS: `pcisecuritystandards.org`
- Singapore: `mas.gov.sg`, `imda.gov.sg`, `pdpc.gov.sg`
- Malaysia: `bnm.gov.my`, `pdp.gov.my`
- Philippines: `bsp.gov.ph`, `npc.gov.ph`
- Indonesia: `bi.go.id`, `kominfo.go.id`
- Thailand: `bot.or.th`, `pdpc.go.th`
- Taiwan: `cbc.gov.tw`, `pdpc.gov.tw`
- Hong Kong: `hkma.gov.hk`, `pcpd.org.hk`
- Cloud pricing: `aws.amazon.com`, `azure.microsoft.com`, `cloud.google.com`

### check-freshness.py

Validates URL age against freshness requirements.

**Usage:**
```bash
# Check single file
python tools/check-freshness.py wiki/apv/sizing/aws-pricing.md

# Check directory
python tools/check-freshness.py wiki/apv/

# Check all APV wiki files
python tools/check-freshness.py --all

# Check single URL
python tools/check-freshness.py --check https://aws.amazon.com/pricing/
```

**Freshness Limits:**
| Source Type | Limit | Rationale |
|-------------|-------|-----------|
| Pricing | 30 days | Cloud prices change frequently |
| Compliance | 365 days | Regulations update annually |
| Calculator | 30 days | Calculator inputs/formulas change |
| General | 180 days | General knowledge decay |

**Detection:**
- Auto-detects URL type from URL path and context
- Checks HTTP `Last-Modified` header
- Calculates age in days
- Warns at 80% of limit, fails at 100%

## Integration with APV Skills

### rfp-compliance Skill

The compliance skill enforces source URLs for all regulatory claims:

```
For each compliance requirement:
1. Identify applicable regulation
2. Locate official source URL
3. Extract specific requirement section
4. Include in response with citation
```

### rfp-pricer Skill

The pricing skill enforces calculator URLs for all cost estimates:

```
For each pricing estimate:
1. Use official calculator
2. Capture configuration used
3. Save calculator URL
4. Include in response with link
```

## Evidence Collection

### Script-Generated Evidence

Verification scripts generate JSON reports:

```json
{
  "timestamp": "2026-04-24T10:30:00Z",
  "total_urls": 234,
  "valid": 230,
  "invalid": 0,
  "inaccessible": 2,
  "stale": 2,
  "details": [
    {
      "url": "https://pcisecuritystandards.org/documents/PCI_DSS_v4-0.pdf",
      "file": "wiki/apv/compliance/pci-dss-overview.md",
      "line": 15,
      "status": "valid",
      "last_modified": "2024-03-31T00:00:00Z",
      "days_old": 390,
      "url_type": "compliance",
      "freshness_limit": 365
    }
  ]
}
```

### Manual Evidence

For critical claims, collect manual evidence:

1. **Calculator Screenshots** - Full-page with visible inputs
2. **Regulatory Snapshots** - Specific requirement sections
3. **Date Stamps** - When evidence was captured
4. **Reviewer Sign-off** - Expert verification

See [[evidence/README.md]] for evidence templates.

## Scheduled Verification

The commands below describe a planned scheduler integration for the existing verification scripts. If no scheduler is configured in your environment, run the scripts manually.

### Planned Weekly Checks

```bash
# Run every Monday at 2 AM
0 2 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/verify-source-urls.py --all > \
  evidence/url-checks/verification-$(date +\%Y-\%m-\%d).json

0 3 * * 1 cd /Users/stevenjiang/workspace/mykb/wiki/apv && \
  python tools/check-freshness.py --all > \
  evidence/freshness-reports/freshness-$(date +\%Y-\%m-\%d).json
```

### Alert Triggers

- **Critical**: Any pricing URL > 25 days old (5-day buffer)
- **Warning**: Any compliance URL > 340 days old (25-day buffer)
- **Immediate**: Any URL returns 404/500 status
- **Review**: Any unknown URL (no date info available)

## Workflow Integration

### Pre-RFP Response

```bash
# 1. Verify all URLs
python tools/verify-source-urls.py --all

# 2. Check freshness
python tools/check-freshness.py --all

# 3. Review any issues
#    - Update stale URLs
#    - Fix inaccessible URLs
#    - Document manual verifications

# 4. Generate response
/apv rfp path/to/rfp.pdf
```

### Post-RFP Response

```bash
# 1. Package evidence
tar czf apv-evidence-$(date +%Y%m%d).tar.gz evidence/

# 2. Include in response package
#    - Verification reports
#    - Calculator screenshots
#    - Compliance citations

# 3. Store for audit trail
mv apv-evidence-*.tar.gz archive/
```

## Quality Metrics

**Target Accuracy:**
- 100% URL format validity
- 100% URL accessibility at time of response
- 100% URL freshness (within limits)
- 100% trusted domain sourcing

**Monitoring:**
- Track URL failure rate
- Monitor stale URL trends
- Alert on new accessibility issues
- Document URL changes over time

## Troubleshooting

### URL Inaccessible

**Possible causes:**
- Network connectivity issue
- Server temporarily down
- URL changed/moved
- Blocked by firewall

**Resolution:**
1. Retry verification
2. Check URL manually in browser
3. Search for updated URL
4. Document alternative source

### URL Stale

**For Pricing:**
- Recapture with current calculator
- Update wiki with new URL
- Document price change if any

**For Compliance:**
- Check if regulation updated
- Verify requirement still applicable
- Update to current version
- Document version change

### Unknown URL (No Date Info)

**Resolution:**
1. Manual verification in browser
2. Check page for publication date
3. Contact source if critical
4. Document manual verification date

## Files

- `tools/verify-source-urls.py` - URL validation script
- `tools/check-freshness.py` - Freshness checking script
- `evidence/README.md` - Evidence collection guide
- `evidence/url-checks/` - Verification reports
- `evidence/freshness-reports/` - Freshness check reports

## Related

- [[apv-accuracy-assurance]] - Overall accuracy framework
- [[apv-implementation-plan-2026-04-24]] - Task 1.12 implementation
- [[evidence/README.md]] - Evidence collection procedures
