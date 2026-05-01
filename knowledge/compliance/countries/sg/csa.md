---
type: source
category: compliance
subcategory: country-regulation
country: sg
title: Singapore Cybersecurity Act
source_url: "https://sso.agc.gov.sg/Act/CSA2019"
source_document: Cybersecurity Act 2019
source_version: 2019 (Revised 2024)
captured_date: 2026-04-24
verified_by: Compliance Officer
last_verified: 2026-04-24
freshness_days: 365
tags: [compliance, singapore, cybersecurity, csa, critical-infrastructure]
---

# Singapore Cybersecurity Act (CSA)

## Regulatory Authority

**Authority**: Cyber Security Agency of Singapore (CSA)
**Website**: https://www.csa.gov.sg/
**Source URL**: https://sso.agc.gov.sg/Act/CSA2019

## Overview

The Cybersecurity Act 2019 establishes a comprehensive cybersecurity framework for Singapore. It aims to protect Critical Information Infrastructure (CII), regulate cybersecurity service providers, and enhance cybersecurity response.

## Key Requirements

### 1. Critical Information Infrastructure (CII)
**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Part 2)

**CII Sectors**:
- Banking and Finance
- Energy
- Infocomm
- Water
- Health
- Transport
- Media
- Security and Emergency Services
- Government

**CII Operator Responsibilities**:
- Register with CSA
- Conduct cybersecurity risk assessments
- Implement cybersecurity controls
- Report cybersecurity incidents
- Participate in cybersecurity exercises

### 2. Licensing of Cybersecurity Service Providers
**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Part 3)

**Regulated Services**:
1. Penetration Testing
2. Managed Security Operations Centre (SOC) Monitoring
3. Security Operations Centre (SOC) Monitoring
4. Forensic Investigation
5. Vulnerability Assessment

**License Types**:
- Individual license for practitioners
- Organization license for companies

### 3. Incident Reporting
**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Part 4)

**Reporting Requirements**:
- Report cybersecurity incidents to CSA
- Report within specified timelines based on severity
- Provide updates on incident status
- Cooperate with incident response

**Severity Levels**| Severity | Reporting Timeline |
|----------|-------------------|
| Critical | Within 2 hours |
| High | Within 12 hours |
| Medium | Within 72 hours |
| Low | Within 7 days |

### 4. Cybersecurity Codes of Practice
**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Section 11)

**Code of Practice for CII**:
- Governance and risk management
- Asset management
- Access control
- Data security
- Network security
- Incident management
- Business continuity
- Compliance monitoring

### 5. CSA's Powers
**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Part 5)

- Investigate cybersecurity incidents and threats
- Issue directives to CII operators
- Share cybersecurity information
- Conduct inspections and audits

## Banking and Finance Specifics

**Source**: https://www.csa.gov.sg/publications/codes-of-practice

For financial institutions, CSA works closely with MAS:

- **Shared Responsibility**: CSA and MAS jointly regulate cybersecurity in financial sector
- **MAS TRM Alignment**: Cybersecurity Act requirements align with MAS TRM Guidelines
- **Reporting**: CII incidents reported to both CSA and MAS

### Cybersecurity for Financial Institutions

| Requirement | CSA | MAS TRM |
|-------------|-----|---------|
| Risk Assessment | Required | Required |
| Incident Response | Required | Required |
| Security Testing | Required | Required |
| Business Continuity | Required | Required |

## PCI-DSS Equivalency

| CSA Requirement | PCI-DSS Equivalent | Source URL |
|-----------------|-------------------|------------|
| Incident Reporting | Req 10, 12 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Access Control | Req 7, 8 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Security Testing | Req 11 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Data Protection | Req 3, 4 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |

## Evidence Storage
- `wiki/apv/knowledge/evidence/countries/sg/`
- [ ] CII registration (if applicable)
- [ ] Cybersecurity risk assessment reports
- [ ] Incident response plans
- [ ] Incident reports
- [ ] CSA audit reports
- [ ] License certificates (if applicable)

## RFP Response Template

### Question: "How do you comply with the Cybersecurity Act?"

```
[Company Name] maintains full compliance with Singapore's Cybersecurity Act 2019:

1. Cybersecurity Framework
   - Comprehensive cybersecurity policies aligned with CSA Code of Practice
   - Chief Information Security Officer (CISO) appointed
   - Cybersecurity risk management program
   Source: https://sso.agc.gov.sg/Act/CSA2019 (Part 2)

2. [If CII Operator]
   - CII Registration No: [REGISTRATION_NUMBER]
   - Designated CII systems: [LIST]
   - Compliance with CII Code of Practice
   Source: https://sso.agc.gov.sg/Act/CSA2019 (Part 2)

3. [If Licensed Service Provider]
   - CSA License No: [LICENSE_NUMBER]
   - Licensed services: [Pen Testing/SOC Monitoring/Forensics]
   - License expiry: [DATE]
   Source: https://sso.agc.gov.sg/Act/CSA2019 (Part 3)

4. Incident Response
   - 24/7 Security Operations Center (SOC)
   - Incident response to CSA within prescribed timelines
   - Critical incidents: Within 2 hours
   - High incidents: Within 12 hours
   Source: https://sso.agc.gov.sg/Act/CSA2019 (Part 4)

5. Security Testing
   - Annual penetration testing
   - Quarterly vulnerability scanning
   - Regular security assessments
   Source: https://sso.agc.gov.sg/Act/CSA2019 (Section 11)

6. Cybersecurity Controls
   - Network security controls (firewalls, IPS/IDS)
   - Endpoint security (anti-malware, EDR)
   - Application security (WAF, code review)
   - Data security (encryption, DLP)
   Source: https://www.csa.gov.sg/publications/codes-of-practice

7. Collaboration with MAS
   - Alignment with MAS TRM Guidelines
   - Joint incident reporting where applicable
   - Regular compliance reviews
   Source: https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf

Compliance verified by: [Compliance Officer] on [DATE]
Next CSA review: [DATE + 12 months]

Related regulations:
- MAS TRM Guidelines: [[sg-mas-trm]]
- Payment Services Act: [[sg-psa]]
- Personal Data Protection Act: [[sg-pdpa]]
```

## Common Questions

### Q: Is my financial institution considered CII?
A: Most financial institutions are considered CII under the Cybersecurity Act. You should confirm your CII status with MAS and CSA.

**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Section 5)

### Q: What are the reporting timelines for cybersecurity incidents?
A: Critical incidents must be reported within 2 hours, high incidents within 12 hours, medium within 72 hours, and low within 7 days.

**Source**: https://sso.agc.gov.sg/Act/CSA2019 (Section 16)

## Related
- [[sg-mas-trm]] — MAS Technology Risk Management Guidelines
- [[sg-psa]] — Payment Services Act
- [[sg-pdpa]] — Personal Data Protection Act
- [[pci-dss-overview]] — PCI-DSS compliance
