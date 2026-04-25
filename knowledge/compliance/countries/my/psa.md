---
type: apv-knowledge
category: compliance
subcategory: country-regulation
country: my
title: "Malaysia Payment Systems Act"
source_url: "https://www.bnm.gov.my/payment-systems-act"
source_document: "Payment Systems Act 2018 (Act 748)"
source_version: "2018"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, malaysia, payment-systems, licensing, bnm]
---

# Malaysia Payment Systems Act (PSA)

## Regulatory Authority

**Authority**: Bank Negara Malaysia (BNM)
**Website**: https://www.bnm.gov.my/
**Source URL**: https://www.bnm.gov.my/payment-systems-act

## Overview

The Payment Systems Act 2018 (Act 748) is Malaysia's primary legislation regulating payment systems and payment service providers. It established a comprehensive regulatory framework for payment systems in Malaysia.

## Key Requirements

### 1. Designation of Payment Systems
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 5)

- BNM may designate any payment system as a designated payment system
- Designated payment systems require approval from BNM
- Operators must comply with regulatory requirements

### 2. Licensing Regime
**Source**: https://www.bnm.gov.my/payment-systems-act (Part III)

**License Types**:
- **Payment System Operator (PSO)**: For operators of payment systems
- **Remittance Service Provider**: For cross-border remittance services
- **Merchant Acquirer**: For merchant acquisition services

### 3. Capital Requirements
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 18)

- Minimum capital requirements for license holders
- Capital adequacy requirements
- Financial resource maintenance

### 4. Risk Management
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 20)

- Implement robust risk management framework
- Technology and cybersecurity risk management
- Operational risk management
- Liquidity risk management

### 5. Safeguarding of Funds
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 23)

- Safeguard customer funds against insolvency
- Keep funds in trust accounts or designated accounts
- Daily reconciliation of safeguarded funds
- Annual audit of safeguarding arrangements

### 6. Technology and Security
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 24)

- Implement secure payment systems
- Comply with technology risk management guidelines
- Regular security testing and audits
- Business continuity and disaster recovery planning

### 7. Anti-Money Laundering (AML) and Countering Financing of Terrorism (CFT)
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 25)

- Implement AML/CFT controls and processes
- Customer due diligence
- Transaction monitoring
- Suspicious transaction reporting

### 8. Data Protection
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 26)

- Comply with Personal Data Protection Act 2010
- Protect customer data
- Obtain consent for data collection and use
- Data breach notification

### 9. Reporting and Disclosure
**Source**: https://www.bnm.gov.my/payment-systems-act (Section 27)

- Periodic regulatory returns to BNM
- Annual audited financial statements
- Disclosure of material information
- Notification of significant events

## Card-Specific Requirements

For card payment processing:

**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca

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

### Question: "How do you comply with the Payment Systems Act?"

```
[Company Name] maintains full compliance with Malaysia's Payment Systems Act 2018:

1. Licensing
   - Payment System Operator License No: [LICENSE_NUMBER]
   - Licensed for: [list payment activities]
   - License issued: [DATE]
   Source: https://www.bnm.gov.my/payment-systems-act (Part III)

2. Financial Requirements
   - Minimum capital maintained: RM [AMOUNT]
   - Annual audit completed by [AUDIT FIRM]
   - Quarterly financial returns to BNM
   Source: https://www.bnm.gov.my/payment-systems-act (Section 18)

3. Fund Safeguarding
   - Customer funds safeguarded via [trust account/designated account]
   - Daily reconciliation performed
   - Annual audit of safeguarding arrangements
   - Funds segregated from operating capital
   Source: https://www.bnm.gov.my/payment-systems-act (Section 23)

4. Technology and Security
   - Full compliance with BNM Risk Management Guidelines
   - PCI-DSS v4.0 certified (Certificate: [LINK])
   - Annual penetration testing
   - 24/7 security monitoring
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca

5. AML/CFT Compliance
   - AML/CFT program approved by BNM
   - Customer due diligence procedures
   - Transaction monitoring
   - STR reporting to BNM
   Source: https://www.bnm.gov.my/payment-systems-act (Section 25)

6. Data Protection
   - Full compliance with PDPA 2010 requirements
   - Data protection policies in place
   - Data breach notification procedures
   Source: https://www.bnm.gov.my/payment-systems-act (Section 26)

Compliance verified by: [Compliance Officer] on [DATE]
License renewal due: [DATE]

Related regulations:
- BNM Risk Management Guidelines: [[my-bnm-rm]]
- Personal Data Protection Act: [[my-pdpa]]
- Financial Services Act: [[my-fsa]]
```

## Evidence Storage
- `wiki/apv/knowledge/evidence/countries/my/`
- [ ] PSA License certificate
- [ ] Capital adequacy reports
- [ ] Fund safeguarding audit reports
- [ ] AML/CFT procedures
- [ ] BNM regulatory returns

## Related
- [[my-bnm-rm]] — BNM Risk Management Guidelines
- [[my-pdpa]] — Personal Data Protection Act
- [[pci-dss-overview]] — PCI-DSS compliance
