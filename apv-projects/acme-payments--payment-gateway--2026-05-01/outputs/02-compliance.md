---
output_class: evidence-backed
stage: 2
created: '2026-05-01'
---

# Compliance Mapping: ACME Payments

## Applicable Frameworks

| Framework | Scope | Country | Source URL |
|-----------|-------|---------|------------|
| PCI-DSS v4.0 Level 1 | Cardholder data environment — card acquiring, issuing, tokenization, gateway processing | Global | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| MAS Technology Risk Management Guidelines | Technology risk, audit logging, operational resilience, access controls | Singapore | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Singapore PDPA 2012 | Personal data protection for customer/cardholder data | Singapore | [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012) |
| Singapore Payment Services Act 2019 | MPI licensing, payment service provider obligations | Singapore | [PSA 2019](https://sso.agc.gov.sg/Act/PSA2019) |
| Malaysia BNM Risk Management Guidelines | Technology and cyber risk management for financial services | Malaysia | [BNM RM](https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca) |
| Malaysia PDPA 2010 | Personal data protection for Malaysian customers | Malaysia | [PDPA 2010](https://www.pdp.gov.my/index.php/en/pdpa-2010) |
| Malaysia Payment Systems Act 2018 | Payment system operator licensing and obligations | Malaysia | [PSA 2018](https://www.bnm.gov.my/payment-systems-act) |
| Philippines BSP Circular No. 995 | Technology risk management for BSP-supervised institutions | Philippines | [BSP C995](https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf) |
| Philippines Data Privacy Act 2012 | Data privacy for Philippine customers (RA 10173) | Philippines | [DPA 2012](https://privacy.gov.ph/data-privacy-act/) |
| Philippines NPSP (BSP Circular 1049) | National payment system regulatory framework | Philippines | [BSP C1049](https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf) |

## Requirement-to-Regulation Map

### PCI-DSS v4.0 Level 1 Compliance

| RFP Requirement | Regulation | Specific Control | Source URL |
|-----------------|-----------|-----------------|------------|
| End-to-end encryption (TLS 1.3, AES-256) | PCI-DSS Req 3 & 4 | Protect stored data; encrypt transmission over open networks | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Tokenization service for recurring payments | PCI-DSS Req 3 | Minimize cardholder data storage via tokenization | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| 3D Secure 2.0 authentication | PCI-DSS Req 8 | Strong authentication for cardholder verification | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Comprehensive audit logging | PCI-DSS Req 10 | Track and monitor all access to network resources and cardholder data | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| API-first architecture (REST, gRPC) | PCI-DSS Req 6 | Develop and maintain secure systems and applications | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |

### Singapore Regulations

| RFP Requirement | Regulation | Mapping | Source URL |
|-----------------|-----------|---------|------------|
| Comprehensive audit logging per MAS TRM | MAS TRM Guidelines | Audit trail, event logging, access monitoring | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| 99.99% availability SLA | MAS TRM Guidelines | Operational resilience, system availability requirements | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| DR capability | MAS TRM Guidelines | Business continuity planning, disaster recovery | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Cloud-native on AWS | MAS TRM Guidelines | Cloud outsourcing risk management, technology risk assessment | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Customer data handling | SG PDPA 2012 | Consent, purpose limitation, data protection obligations | [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012) |
| MPI-licensed payment gateway | PSA 2019 | Major Payment Institution licensing, AML/CFT obligations | [PSA 2019](https://sso.agc.gov.sg/Act/PSA2019) |

### Malaysia Regulations

| RFP Requirement | Regulation | Mapping | Source URL |
|-----------------|-----------|---------|------------|
| Technology risk management | BNM RM Guidelines | Cyber risk, technology governance, incident response | [BNM RM](https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca) |
| Customer data handling (MY) | MY PDPA 2010 | Data processing principles, cross-border transfer restrictions | [PDPA 2010](https://www.pdp.gov.my/index.php/en/pdpa-2010) |
| Payment processing in Malaysia | MY PSA 2018 | Payment system operator registration | [PSA 2018](https://www.bnm.gov.my/payment-systems-act) |

### Philippines Regulations

| RFP Requirement | Regulation | Mapping | Source URL |
|-----------------|-----------|---------|------------|
| Technology risk management | BSP Circular 995 | IT risk governance, cybersecurity, incident management | [BSP C995](https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf) |
| Customer data handling (PH) | PH DPA 2012 | Data subject rights, NPC registration, breach notification | [DPA 2012](https://privacy.gov.ph/data-privacy-act/) |
| Payment processing in Philippines | BSP Circular 1049 (NPSP) | Payment system operator registration with BSP | [BSP C1049](https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf) |

## Compliance Gaps

| Gap | Impact | Mitigation |
|-----|--------|------------|
| No SG Cybersecurity Act (CSA) mapping | CSA may designate payment infrastructure as Critical Information Infrastructure (CII) — additional obligations | Knowledge file `csa.md` exists but was not explicitly required in RFP; should be included in response as proactive coverage |
| Malaysia FSA coverage | Financial Services Act 2013 may impose additional requirements for payment operators | Knowledge file `fsa.md` exists; review during architecture stage |
| Indonesia/Thailand Phase 2 compliance not mapped | Data residency (ID), BOT regulations (TH) not in scope for Stage 2 | Defer to Phase 2 planning; knowledge files available |
| PCI-DSS QSA assessment process | RFP requires Level 1 — needs annual on-site assessment by QSA; operational process not addressed | Include QSA engagement in implementation timeline |
| Cross-border data transfer mechanisms | MY PDPA and PH DPA restrict cross-border transfers; architecture must address data flows between SG hub and MY/PH | Address in architecture stage with data residency design |

## Evidence References

| Evidence ID | Description | Source |
|-------------|-------------|--------|
| E-PCIDSS-01 | PCI-DSS v4.0 Standard (Requirements 1-12) | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| E-SG-01 | MAS Technology Risk Management Guidelines | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| E-SG-02 | Singapore PDPA 2012 | [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012) |
| E-SG-03 | Singapore PSA 2019 | [PSA 2019](https://sso.agc.gov.sg/Act/PSA2019) |
| E-MY-01 | BNM Risk Management Guidelines | [BNM RM](https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca) |
| E-MY-02 | Malaysia PDPA 2010 | [PDPA 2010](https://www.pdp.gov.my/index.php/en/pdpa-2010) |
| E-MY-03 | Malaysia PSA 2018 | [PSA 2018](https://www.bnm.gov.my/payment-systems-act) |
| E-PH-01 | BSP Circular 995 | [BSP C995](https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf) |
| E-PH-02 | Philippines DPA 2012 | [DPA 2012](https://privacy.gov.ph/data-privacy-act/) |
| E-PH-03 | BSP Circular 1049 (NPSP) | [BSP C1049](https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf) |
