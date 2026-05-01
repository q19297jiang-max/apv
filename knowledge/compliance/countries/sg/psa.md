---
type: source
category: compliance
subcategory: country-regulation
country: sg
title: Singapore Payment Services Act
source_url: "https://sso.agc.gov.sg/Act/PSA2019"
source_document: Payment Services Act 2019
source_version: 2019 (Revised 2024)
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, singapore, payment-services, licensing, mas]
---

# Singapore Payment Services Act (PSA)

## Regulatory Authority

**Authority**: Monetary Authority of Singapore (MAS)
**Website**: https://www.mas.gov.sg/
**Source URL**: https://sso.agc.gov.sg/Act/PSA2019

## Overview

The Payment Services Act 2019 (PSA) is Singapore's primary legislation regulating payment services and payment service providers. It established a flexible and activity-based licensing framework that allows MAS to regulate payment activities effectively.

## Key Requirements

### 1. Licensing Regime
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 5)

**License Types**:
- **Money-Changing License**: For money-changing services
- **Standard Payment Institution (SPI)**: For lower-risk payment services with transaction limits
- **Major Payment Institution (MPI)**: For higher-risk payment services without transaction limits

**Payment Activities Regulated**:
- Account issuance
- Domestic money transfer
- Cross-border money transfer
- Merchant acquisition
- E-money issuance
- Digital payment token services

### 2. Capital Requirements
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 12)

| License Type | Base Capital | Variable Capital |
|--------------|-------------|------------------|
| Money-Changing | SGD 50,000 | - |
| Standard Payment Institution | SGD 100,000 | Based on payment volume |
| Major Payment Institution | SGD 250,000 | Based on payment volume |

### 3. Safeguarding of Funds
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 25)

- Safeguard customer funds against insolvency
- Keep funds in trust accounts or specified investments
- Daily reconciliation of safeguarded funds
- Annual audit of safeguarding arrangements

### 4. Technology Risk Management
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 24)

- Comply with MAS Technology Risk Management Guidelines
- Implement robust security measures
- Regular security testing and audits
- Business continuity and disaster recovery planning

### 5. Anti-Money Laundering (AML) and Countering Financing of Terrorism (CFT)
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 20)

- Implement AML/CFT controls and processes
- Customer due diligence
- Transaction monitoring
- Suspicious transaction reporting

### 6. Data Protection
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 22)

- Comply with Personal Data Protection Act (PDPA)
- Protect customer data
- Obtain consent for data collection and use
- Data breach notification

### 7. Outsourcing Requirements
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 27)

- Obtain MAS approval for material outsourcing
- Ensure service provider meets regulatory standards
- Maintain oversight of outsourced functions
- Exit planning

### 8. Reporting and Disclosure
**Source**: https://sso.agc.gov.sg/Act/PSA2019 (Section 26)

- Annual audited financial statements
- Periodic regulatory returns to MAS
- Disclosure of material information
- Notification of significant events

## Transaction Limits

**Source**: https://www.mas.gov.sg/-/media/MAS/Payment-Regulations/Regulated-Payment-Activities/License-Eligibility-and-Criteria.pdf

| License Type | Monthly Transaction Limit | Transaction Type |
|--------------|--------------------------|------------------|
| Standard Payment Institution | SGD 3 million | Per payment activity |
| Major Payment Institution | No limit | All payment activities |

## Card-Specific Requirements

For card payment processing:

**Source**: https://www.mas.gov.sg/-/media/MAS/Payment-Systems/Payment-Cards/Card-Scheme-Advisory.pdf

- PCI-DSS compliance required for card processing
- Secure cardholder data handling
- Fraud monitoring and prevention
- Chargeback management

## PCI-DSS Equivalency

| PSA Requirement | PCI-DSS Equivalent | Source URL |
|-----------------|-------------------|------------|
| Technology Risk | All Requirements | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Data Protection | Req 3, 4 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Safeguarding Funds | Req 9 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Security Testing | Req 11 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |

## RFP Response Template

### Question: "How do you comply with the Payment Services Act?"

```
[Company Name] maintains full compliance with Singapore's Payment Services Act 2019:

1. Licensing
   - [SPI/MPI] License No: [LICENSE_NUMBER]
   - Licensed for: [list payment activities]
   - License issued: [DATE]
   Source: https://sso.agc.gov.sg/Act/PSA2019 (Section 5)

2. Financial Requirements
   - Base capital maintained: SGD [AMOUNT]
   - Variable capital: SGD [AMOUNT] based on transaction volume
   - Annual audit completed by [AUDIT FIRM]
   Source: https://sso.agc.gov.sg/Act/PSA2019 (Section 12)

3. Fund Safeguarding
   - Customer funds safeguarded via [trust account/specified investment]
   - Daily reconciliation performed
   - Annual audit of safeguarding arrangements
   - Funds segregated from operating capital
   Source: https://sso.agc.gov.sg/Act/PSA2019 (Section 25)

4. Technology and Security
   - Full compliance with MAS TRM Guidelines
   - PCI-DSS v4.0 certified (Certificate: [LINK])
   - Annual penetration testing
   - 24/7 security monitoring
   Source: https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf

5. AML/CFT Compliance
   - AML/CFT program approved by MAS
   - Customer due diligence procedures
   - Transaction monitoring
   - STR reporting to MAS
   Source: https://sso.agc.gov.sg/Act/PSA2019 (Section 20)

6. Data Protection
   - Full compliance with PDPA requirements
   - Data protection policies in place
   - Data breach notification procedures
   Source: https://sso.agc.gov.sg/Act/PSA2019 (Section 22)

Compliance verified by: [Compliance Officer] on [DATE]
License renewal due: [DATE]

Related regulations:
- MAS TRM Guidelines: [[sg-mas-trm]]
- Personal Data Protection Act: [[sg-pdpa]]
- Cybersecurity Act: [[sg-csa]]
```

## Evidence Storage
- `wiki/apv/knowledge/evidence/countries/sg/`
- [ ] PSA License certificate
- [ ] Capital adequacy reports
- [ ] Fund safeguarding audit reports
- [ ] AML/CFT procedures
- [ ] MAS regulatory returns

## Related
- [[sg-mas-trm]] — MAS Technology Risk Management Guidelines
- [[sg-pdpa]] — Personal Data Protection Act
- [[sg-csa]] — Cybersecurity Act
- [[pci-dss-overview]] — PCI-DSS compliance
