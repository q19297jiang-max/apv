---
type: apv-meta
category: documentation
title: "APV Compliance Officer Training Guide"
created: 2026-04-24
tags: [apv, documentation, training, compliance]
---

# APV Compliance Officer Training Guide

**Audience**: Compliance Officers
**Duration**: 45 minutes
**Prerequisites**: Understanding of PCI-DSS and banking regulations

---

## Learning Objectives

After this training, you will be able to:
1. Understand APV's compliance framework
2. Verify source URL compliance
3. Review compliance matrices
4. Run verification scripts
5. Validate regulatory coverage

---

## APV Compliance Framework

### 100% Source URL Compliance

**Rule**: Every compliance claim MUST cite an official source

**Enforcement**:
- rfp-compliance skill requires source URLs
- rfp-pricer skill requires calculator URLs
- apv-reviewer validates source URL presence (30% weight)
- Verification scripts check URL accessibility

**Trusted Sources**:
- PCI-DSS: https://www.pcisecuritystandards.org/
- Singapore MAS: https://www.mas.gov.sg/
- Malaysia BNM: https://www.bnm.gov.my/
- Philippines BSP: https://www.bsp.gov.ph/
- Indonesia BI: https://www.bi.go.id/
- Thailand BOT: https://www.bot.or.th/
- Taiwan FSC: https://www.fsc.gov.tw/
- Hong Kong HKMA: https://www.hkma.gov.hk/

### Supported Regulations

| Region | Regulations | Wiki Reference |
|--------|-------------|----------------|
| Singapore | MAS TRM, PSA, PDPA, CSA | [[mas-trm]], [[psa]], [[pdpa-sg]], [[csa]] |
| Malaysia | BNM RM, PSA, PDPA, FSA | [[bnm-rm]], [[psa-my]], [[pdpa-my]], [[fsa]] |
| Philippines | BSP Circular, PDPA, NPSP | [[bsp-circular]], [[pdpa-ph]], [[npsp]] |
| Indonesia | BI Regulations, PDPA | [[bi-regulations]], [[pdpa-id]] |
| Thailand | BOT Payment, PDPA | [[bot-payment]], [[pdpa-th]] |
| Taiwan | FSC Payment, PDPA | [[fsc-payment]], [[pdpa-tw]] |
| Hong Kong | HKMA GM, PDPO | [[hkma-gm]], [[pdpo-hk]] |

---

## Verification Tools

### Tool 1: verify-source-urls.py

**Purpose**: Validate URL format, accessibility, trusted domains

**Usage**:
```bash
# Verify all source URLs in knowledge base
python wiki/apv/tools/verify-source-urls.py --all

# Verify specific file
python wiki/apv/tools/verify-source-urls.py wiki/apv/knowledge/compliance/pci-dss-req-1.md
```

**Output**:
- ✅ Valid URLs: Format OK, accessible, trusted domain
- ❌ Invalid URLs: Format error, not accessible, untrusted domain

**Exit Codes**:
- 0: All URLs valid
- 1: One or more URLs invalid

### Tool 2: check-freshness.py

**Purpose**: Check URL age against freshness limits

**Limits**:
- Pricing sources: 30 days
- Compliance sources: 365 days

**Usage**:
```bash
# Check all URLs
python wiki/apv/tools/check-freshness.py --all

# Check specific category
python wiki/apv/tools/check-freshness.py --category pricing
```

**Output**:
- ✅ Fresh: Within limit
- ⚠️ Warning: Expiring soon
- ❌ Stale: Exceeded limit

---

## Review Process

### Step 1: Review Compliance Matrix

**File**: `outputs/02-compliance.md`

**Check**:
- [ ] All requirements mapped to regulations
- [ ] Each regulation has source URL
- [ ] PCI-DSS requirements 1-12 covered
- [ ] Country-specific regulations covered
- [ ] Compliance gaps identified

### Step 2: Verify Source URLs

**Run verification**:
```bash
python wiki/apv/tools/verify-source-urls.py --all
```

**Check**:
- [ ] All URLs accessible (no 404)
- [ ] All URLs from trusted domains
- [ ] URL format correct (https://)
- [ ] No broken or expired links

### Step 3: Check Freshness

**Run freshness check**:
```bash
python wiki/apv/tools/check-freshness.py --all
```

**Check**:
- [ ] Pricing sources < 30 days old
- [ ] Compliance sources < 365 days old
- [ ] No stale sources

### Step 4: Review Final Response

**File**: `outputs/06-response.md`

**Check**:
- [ ] Source URL index in appendix
- [ ] All claims cite sources
- [ ] Accuracy assurance statement included
- [ ] No unsubstantiated claims

### Step 5: Approve Review

**File**: `outputs/07-approval.md`

**Check**:
- [ ] Source URL score ≥95%
- [ ] Overall confidence ≥90%
- [ ] No critical compliance failures
- [ ] Decision: "Approve"

---

## Common Issues

### Issue 1: Source URL Missing

**Symptom**: Claim without source citation

**Solution**:
1. Check knowledge base file for source_url in frontmatter
2. Add source URL if missing
3. Re-run skill

### Issue 2: URL Not Accessible

**Symptom**: 404 error or timeout

**Solution**:
1. Check if URL is correct
2. Find alternative official source
3. Update knowledge base
4. Re-run verification

### Issue 3: Stale Source

**Symptom**: Source exceeds freshness limit

**Solution**:
1. For pricing: Re-calculate with current calculator
2. For compliance: Verify regulation still current
3. Update source_url with newer version
4. Update last_verified date

### Issue 4: Untrusted Domain

**Symptom**: URL from non-official source

**Solution**:
1. Find official source (government, regulator)
2. Replace with trusted source
3. Re-run verification

---

## Evidence Collection

### What to Collect

**Pricing Evidence**:
- Calculator screenshots
- Configuration details
- Date of calculation

**Compliance Evidence**:
- Regulatory document snapshots
- Requirement mappings
- Certification details

**Where to Store**:
```
apv-projects/[customer]--[title]--[date]/evidence/
├── pricing/          # Calculator screenshots
├── compliance/       # Regulatory snapshots
└── verification/     # Verification reports
```

### How to Collect

**Pricing**:
1. Use official calculator (AWS/Azure/GCP)
2. Screenshot configuration
3. Save with date stamp
4. Store in evidence/pricing/

**Compliance**:
1. Download from official regulator site
2. Save with date stamp
3. Store in evidence/compliance/

---

## Quality Metrics

### Source URL Compliance

**Metric**: % of claims with valid source URLs

**Target**: 100%

**Calculation**: (Claims with URLs / Total claims) × 100

**Measurement**: apv-reviewer skill

### URL Accessibility

**Metric**: % of URLs that are accessible

**Target**: 100%

**Measurement**: verify-source-urls.py

### Source Freshness

**Metric**: % of sources within freshness limits

**Target**: 100%

**Measurement**: check-freshness.py

---

## Best Practices

### 1. Always Verify

- Run verification before finalizing response
- Check both URL validity and freshness
- Document verification results

### 2. Use Official Sources

- Prioritize regulator websites
- Use official documentation
- Avoid third-party summaries

### 3. Keep Sources Current

- Update pricing monthly
- Review regulations quarterly
- Document review dates

### 4. Document Everything

- Save evidence for key claims
- Date-stamp all evidence
- Store with project files

---

## Compliance Coverage

### PCI-DSS v4.0

All 12 requirements covered:

| Req | Area | Source |
|-----|------|--------|
| 1 | Network Security | PCI SSC official |
| 2 | Secure Configuration | PCI SSC official |
| 3 | Card Data Protection | PCI SSC official |
| 4 | Encryption | PCI SSC official |
| 5 | Anti-Malware | PCI SSC official |
| 6 | Secure Development | PCI SSC official |
| 7 | Access Control | PCI SSC official |
| 8 | Authentication | PCI SSC official |
| 9 | Physical Access | PCI SSC official |
| 10 | Logging | PCI SSC official |
| 11 | Monitoring | PCI SSC official |
| 12 | Security Policy | PCI SSC official |

### Asian Countries (7)

All 7 countries covered with full regulatory mappings:

| Country | Regulations | Status |
|---------|-------------|--------|
| Singapore | MAS TRM, PSA, PDPA, CSA | ✅ |
| Malaysia | BNM RM, PSA, PDPA, FSA | ✅ |
| Philippines | BSP Circular, PDPA, NPSP | ✅ |
| Indonesia | BI Regulations, PDPA | ✅ |
| Thailand | BOT Payment, PDPA | ✅ |
| Taiwan | FSC Payment, PDPA | ✅ |
| Hong Kong | HKMA GM, PDPO | ✅ |

---

## Getting Help

### Documentation

- [[apv-user-guide]] - Complete user guide
- [[source-url-verification-system]] - Verification system details
- [[apv-accuracy-assurance]] - Accuracy framework

### Tools

- `verify-source-urls.py --help` - Verification help
- `check-freshness.py --help` - Freshness check help

### Knowledge Base

- `wiki/apv/knowledge/compliance/` - All compliance files

---

**Training Duration**: 45 minutes
**Last Updated**: 2026-04-24
**Maintained By**: APV Development Team
