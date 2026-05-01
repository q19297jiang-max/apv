---
type: source
category: compliance
subcategory: country-regulation
country: sg
title: Singapore Personal Data Protection Act
source_url: "https://sso.agc.gov.sg/Act/PDPA2012"
source_document: Personal Data Protection Act 2012
source_version: 2012 (Revised 2024)
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, singapore, data-protection, privacy, pdpc]
---

# Singapore Personal Data Protection Act (PDPA)

## Regulatory Authority

**Authority**: Personal Data Protection Commission (PDPC)
**Website**: https://www.pdpc.gov.sg/
**Source URL**: https://sso.agc.gov.sg/Act/PDPA2012

## Overview

The Personal Data Protection Act 2012 (PDPA) governs the collection, use, and disclosure of personal data by organizations in Singapore. It aims to protect individuals' personal data while enabling organizations to use data for legitimate purposes.

## Key Requirements

### 1. Obligations (Overview)
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Part 2)

The PDPA establishes 9 main obligations for organizations:
1. Consent Obligation
2. Purpose Limitation Obligation
3. Notification Obligation
4. Access and Correction Obligation
5. Accuracy Obligation
6. Protection Obligation
7. Retention Limitation Obligation
8. Transfer Limitation Obligation
9. Openness Obligation

### 2. Consent Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 13)

- Obtain consent before collecting, using, or disclosing personal data
- Consent must be informed and specific
- Consent can be withdrawn (where appropriate)
- Exceptions exist for certain situations

### 3. Purpose Limitation Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 18)

- Use or disclose personal data only for purposes that individual would reasonably expect
- Notify individuals of new purposes
- Obtain consent for unrelated purposes

### 4. Notification Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 20)

- Inform individuals of purposes of collection, use, and disclosure
- Provide information on data protection policies
- Notify before collecting data

### 5. Access and Correction Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 21, 22)

- Provide individuals access to their personal data upon request
- Correct inaccurate or incomplete data upon request
- Respond within 30 days (can be extended)

### 6. Protection Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 24)

- Secure personal data against unauthorized access, collection, use, disclosure, or similar risks
- Implement appropriate security measures
- Prevent similar risks arising from disposal of data

### 7. Retention Limitation Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 25)

- Cease retention of personal data when no longer needed for purpose
- Dispose data securely
- Exceptions exist for legal or business purposes

### 8. Transfer Limitation Obligation
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Section 26)

- Transfer personal data overseas only if recipient has comparable protection
- Ensure standard of protection is comparable to PDPA
- Exceptions exist for certain transfers

### 9. Data Breach Notification
**Source**: https://sso.agc.gov.sg/Act/PDPA2012 (Part 6A)

- Notify PDPC of data breaches affecting 500+ individuals
- Notify affected individuals if breach likely to result in significant harm
- Notify as soon as practicable (within 3 days for significant breaches)
- Keep records of all data breaches

## Cardholder Data Considerations

For payment card processing:

**Personal Data Under PDPA**:
- Cardholder name (when linked to other identifying information)
- Card number (when linked to other identifying information)
- Transaction history
- Account information

**PDPA + PCI-DSS Alignment**:
| Data Element | PDPA | PCI-DSS |
|--------------|------|---------|
| PAN | Personal Data | Must Protect (Req 3) |
| Cardholder Name | Personal Data | Must Protect (Req 3) |
| Expiration Date | Personal Data | Must Protect (Req 3) |
| CVC/CVV | Not PDPA (never store) | Never Store (Req 3.2) |

## Evidence Storage
- `wiki/apv/knowledge/evidence/countries/sg/`
- [ ] PDPA policies and procedures
- [ ] Consent management records
- [ ] Data access request logs
- [ ] Data breach notification records
- [ ] Data retention schedules
- [ ] Data transfer agreements

## RFP Response Template

### Question: "How do you comply with PDPA?"

```
[Company Name] maintains full compliance with Singapore's Personal Data Protection Act 2012:

1. Data Protection Framework
   - Comprehensive data protection policies covering all 9 PDPA obligations
   - Data Protection Officer (DPO) appointed
   - Regular PDPA training for all staff
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Part 2)

2. Consent Management
   - Explicit consent obtained before data collection
   - Granular consent for different purposes
   - Easy withdrawal mechanism provided
   - Consent records maintained
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Section 13)

3. Data Security
   - Encryption of personal data at rest (AES-256) and in transit (TLS 1.3)
   - Access controls based on least privilege
   - Regular security assessments
   - Secure disposal procedures
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Section 24)

4. Data Access and Correction
   - 30-day response time for data access requests
   - Online portal for data access and correction
   - Identity verification before access
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Section 21, 22)

5. Data Retention
   - Data retention schedule aligned with business needs
   - Automatic deletion when data no longer needed
   - Secure disposal methods
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Section 25)

6. Data Breach Management
   - Data breach response team established
   - Notification to PDPC within 3 days for significant breaches
   - Notification to affected individuals when required
   - Breach records maintained
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Part 6A)

7. International Data Transfers
   - Data transfer agreements for overseas transfers
   - Standard Contractual Clauses (SCC) implemented
   - Recipient data protection verified
   Source: https://sso.agc.gov.sg/Act/PDPA2012 (Section 26)

Compliance verified by: [Compliance Officer] on [DATE]
Next DPO report: [DATE + 12 months]

Related regulations:
- MAS TRM Guidelines: [[sg-mas-trm]]
- Payment Services Act: [[sg-psa]]
- Cybersecurity Act: [[sg-csa]]
```

## Related
- [[sg-mas-trm]] — MAS Technology Risk Management Guidelines
- [[sg-psa]] — Payment Services Act
- [[sg-csa]] — Cybersecurity Act
- [[pci-dss-overview]] — PCI-DSS compliance
