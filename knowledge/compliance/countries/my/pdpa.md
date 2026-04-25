---
type: apv-knowledge
category: compliance
subcategory: country-regulation
country: my
title: "Malaysia Personal Data Protection Act"
source_url: "https://www.pdp.gov.my/index.php/en/pdpa-2010"
source_document: "Personal Data Protection Act 2010 (Act 709)"
source_version: "2010"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, malaysia, data-protection, privacy, pdp]
---

# Malaysia Personal Data Protection Act (PDPA)

## Regulatory Authority

**Authority**: Personal Data Protection Department (PDP)
**Website**: https://www.pdp.gov.my/
**Source URL**: https://www.pdp.gov.my/index.php/en/pdpa-2010

## Overview

The Personal Data Protection Act 2010 (Act 709) governs the processing of personal data in commercial transactions in Malaysia. It aims to protect individuals' personal data while allowing organizations to use data for legitimate purposes.

## Key Requirements

### 1. Principles of Data Protection
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Part II)

The PDPA establishes 7 principles of data protection:
1. General Principle
2. Notice and Choice Principle
3. Disclosure Principle
4. Security Principle
5. Retention Principle
6. Data Integrity Principle
7. Access Principle

### 2. General Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 5)

- Obtain consent before collecting, using, or disclosing personal data
- Consent must be informed and specific
- Use personal data only for stated purposes

### 3. Notice and Choice Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 6, 7)

- Inform individuals of purposes of collection, use, and disclosure
- Provide information on data protection policies
- Notify before collecting data

### 4. Disclosure Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 8)

- Disclose personal data only for stated purposes
- Obtain consent for new purposes
- Maintain disclosure records

### 5. Security Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 9)

- Secure personal data against unauthorized access, collection, use, disclosure, or similar risks
- Implement appropriate security measures
- Prevent similar risks arising from disposal of data

### 6. Retention Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 10)

- Cease retention of personal data when no longer needed for purpose
- Dispose data securely
- Exceptions exist for legal or business purposes

### 7. Data Integrity Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 11)

- Ensure personal data is accurate, complete, and not misleading
- Update data when necessary
- Take reasonable steps to ensure data quality

### 8. Access Principle
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 12)

- Provide individuals access to their personal data upon request
- Correct inaccurate or incomplete data upon request
- Respond within specified timeline

### 9. Data Breach Notification
**Source**: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Part IV)

- Notify PDP of data breaches
- Notify affected individuals when required
- Maintain breach records

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
- `wiki/apv/knowledge/evidence/countries/my/`
- [ ] PDPA policies and procedures
- [ ] Consent management records
- [ ] Data access request logs
- [ ] Data breach notification records
- [ ] Data retention schedules
- [ ] Data transfer agreements

## RFP Response Template

### Question: "How do you comply with PDPA?"

```
[Company Name] maintains full compliance with Malaysia's Personal Data Protection Act 2010:

1. Data Protection Framework
   - Comprehensive data protection policies covering all 7 PDPA principles
   - Data Protection Officer (DPO) appointed
   - Regular PDPA training for all staff
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Part II)

2. Consent Management
   - Explicit consent obtained before data collection
   - Granular consent for different purposes
   - Easy withdrawal mechanism provided
   - Consent records maintained
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 5)

3. Data Security
   - Encryption of personal data at rest (AES-256) and in transit (TLS 1.3)
   - Access controls based on least privilege
   - Regular security assessments
   - Secure disposal procedures
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 9)

4. Data Access and Correction
   - 21-day response time for data access requests
   - Online portal for data access and correction
   - Identity verification before access
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 12)

5. Data Retention
   - Data retention schedule aligned with business needs
   - Automatic deletion when data no longer needed
   - Secure disposal methods
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 10)

6. Data Integrity
   - Regular data quality checks
   - Update mechanisms for inaccurate data
   - Data validation procedures
   Source: https://www.pdp.gov.my/index.php/en/pdpa-2010 (Section 11)

Compliance verified by: [Compliance Officer] on [DATE]
Next DPO report: [DATE + 12 months]

Related regulations:
- BNM Risk Management Guidelines: [[my-bnm-rm]]
- Payment Systems Act: [[my-psa]]
- Financial Services Act: [[my-fsa]]
```

## Related
- [[my-bnm-rm]] — BNM Risk Management Guidelines
- [[my-psa]] — Payment Systems Act
- [[pci-dss-overview]] — PCI-DSS compliance
