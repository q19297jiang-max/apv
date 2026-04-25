---
type: apv-knowledge
category: compliance
subcategory: country-regulation
country: my
title: "Malaysia BNM Risk Management Guidelines"
source_url: "https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca"
source_document: "BNM Risk Management Guidelines for Technology and Cyber Risk"
source_version: "Latest"
captured_date: 2026-04-24
verified_by: "Compliance Officer"
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, malaysia, bnm, technology-risk, banking]
---

# Malaysia BNM Risk Management Guidelines

## Regulatory Authority

**Authority**: Bank Negara Malaysia (BNM)
**Website**: https://www.bnm.gov.my/
**Source URL**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca

## Overview

The BNM Risk Management Guidelines for Technology and Cyber Risk provide financial institutions in Malaysia with comprehensive guidance on managing technology and cybersecurity risks. These guidelines are mandatory for all financial institutions under BNM supervision.

## Key Requirements

### 1. Governance and Oversight
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 4)

- Board of Directors responsible for technology and cyber risk
- Senior management accountable for implementation
- Clear roles and responsibilities
- Regular reporting to board and senior management

### 2. Technology Risk Management
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 5)

- Technology risk identification and assessment
- Risk mitigation strategies
- Risk monitoring and reporting
- Technology risk culture

### 3. Cybersecurity Risk Management
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 6)

- Cybersecurity risk assessment
- Threat and vulnerability management
- Security awareness training
- Incident management

### 4. Data Security and Protection
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 7)

- Encryption requirements for sensitive data
- Data classification and handling
- Access control and authentication
- Data loss prevention

### 5. Business Continuity and Disaster Recovery
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 8)

- Business Impact Analysis (BIA)
- Business Continuity Plan (BCP)
- Disaster Recovery Plan (DRP)
- Regular testing and drills

### 6. Third-Party Risk Management
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 9)

- Due diligence on service providers
- Contractual requirements
- Ongoing monitoring
- Exit strategies

### 7. Emerging Technologies
**Source**: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 10)

- Cloud computing
- Application Programming Interfaces (APIs)
- Artificial Intelligence and Machine Learning
- Distributed Ledger Technology

## PCI-DSS Equivalency

| BNM Requirement | PCI-DSS Equivalent | Source URL |
|-----------------|-------------------|------------|
| Data Security | Req 3, 4 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Access Control | Req 7, 8 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Incident Management | Req 10, 12 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| System Development | Req 6 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |

## RFP Response Template

### Question: "How do you comply with BNM Risk Management Guidelines?"

```
[Company Name] maintains full compliance with BNM Risk Management Guidelines for Technology and Cyber Risk:

1. Governance and Oversight
   - Board-level technology risk committee
   - Dedicated Chief Information Security Officer (CISO)
   - Quarterly technology risk reporting to board
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 4)

2. Data Security and Protection
   - Encryption of all sensitive data at rest (AES-256) and in transit (TLS 1.3)
   - Data classification aligned with BNM requirements
   - Multi-factor authentication for all access
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 7)

3. Business Continuity and Disaster Recovery
   - RTO: 4 hours for critical systems, 24 hours for non-critical
   - RPO: 15 minutes for critical systems, 4 hours for non-critical
   - Multi-region deployment in Malaysia ap-southeast-1
   - Annual BCP and DRP testing
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 8)

4. Cybersecurity Risk Management
   - 24/7 Security Operations Center (SOC)
   - Incident response to BNM within prescribed timelines
   - Root cause analysis for all significant incidents
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 6)

5. Cloud Computing Compliance
   - BNM cloud outsourcing requirements met
   - Data residency in Malaysia region
   - Cloud provider risk assessments completed
   Source: https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca (Section 10)

Compliance verified by: [Compliance Officer] on [DATE]
Next review: [DATE + 12 months]

Related regulations:
- Payment Systems Act: [[my-psa]]
- Personal Data Protection Act: [[my-pdpa]]
- Financial Services Act: [[my-fsa]]
```

## Evidence Storage
- `wiki/apv/knowledge/evidence/countries/my/`
- [ ] BNM Risk Management Guidelines PDF
- [ ] Technology risk assessment reports
- [ ] BCP and DRP documents
- [ ] Board meeting minutes

## Related
- [[my-psa]] — Payment Systems Act
- [[my-pdpa]] — Personal Data Protection Act
- [[pci-dss-overview]] — PCI-DSS compliance
