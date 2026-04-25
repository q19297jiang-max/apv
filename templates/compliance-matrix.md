---
type: apv-template
category: rfp-template
title: "Compliance Matrix Template"
tags: [template, compliance-matrix, rfp]
---

# Compliance Matrix Template

## PCI-DSS Compliance Matrix

| PCI-DSS Requirement | Status | Control Description | Evidence Location | Source URL |
|-------------------|--------|-------------------|-----------------|------------|
| Req 1: Network Security | ✅ Compliant | Multi-tier VPC, security groups, WAF | wiki/apv/knowledge/evidence/pci-dss/req-1/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 2: Secure Config | ✅ Compliant | Automated config management, patch management | wiki/apv/knowledge/evidence/pci-dss/req-2/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 3: Stored Data | ✅ Compliant | Encryption at rest, tokenization | wiki/apv/knowledge/evidence/pci-dss/req-3/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 4: Data in Transit | ✅ Compliant | TLS 1.3, PFS cipher suites | wiki/apv/knowledge/evidence/pci-dss/req-4/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 5: Malware | ✅ Compliant | EDR, anti-malware, regular scanning | wiki/apv/knowledge/evidence/pci-dss/req-5/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 6: Secure Dev | ✅ Compliant | Secure SDLC, SAST/DAST, penetration testing | wiki/apv/knowledge/evidence/pci-dss/req-6/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 7: Access Control | ✅ Compliant | RBAC, least privilege, MFA | wiki/apv/knowledge/evidence/pci-dss/req-7/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 8: Authentication | ✅ Compliant | MFA for all access, strong passwords | wiki/apv/knowledge/evidence/pci-dss/req-8/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 9: Physical Access | ✅ Compliant | Cloud provider security, endpoint security | wiki/apv/knowledge/evidence/pci-dss/req-9/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 10: Logging | ✅ Compliant | CloudWatch Logging, 1-year retention | wiki/apv/knowledge/evidence/pci-dss/req-10/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 11: Security Testing | ✅ Compliant | Quarterly scans, annual pen test | wiki/apv/knowledge/evidence/pci-dss/req-11/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |
| Req 12: Security Policies | ✅ Compliant | Comprehensive policies, regular training | wiki/apv/knowledge/evidence/pci-dss/req-12/ | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf |

## Country-Specific Compliance

### Singapore
| Regulation | Status | Source URL |
|------------|--------|------------|
| MAS TRM Guidelines | ✅ Compliant | https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf |
| Payment Services Act | ✅ Compliant | https://sso.agc.gov.sg/Act/PSA2019 |
| Personal Data Protection Act | ✅ Compliant | https://sso.agc.gov.sg/Act/PDPA2012 |
| Cybersecurity Act | ✅ Compliant | https://sso.agc.gov.sg/Act/CSA2019 |

### Malaysia
| Regulation | Status | Source URL |
|------------|--------|------------|
| BNM Risk Management Guidelines | ✅ Compliant | https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca |
| Payment Services Act | ✅ Compliant | https://www.bnm.gov.my/payment-systems-act |
| Personal Data Protection Act | ✅ Compliant | https://www.pdp.gov.my/index.php/en/pdpa-2010 |

### Philippines
| Regulation | Status | Source URL |
|------------|--------|------------|
| BSP Circular TRM | ✅ Compliant | https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf |
| Data Privacy Act | ✅ Compliant | https://privacy.gov.ph/data-privacy-act/ |

### Indonesia
| Regulation | Status | Source URL |
|------------|--------|------------|
| BI IT Regulations | ✅ Compliant | https://www.bi.go.id/en/aturan-perbankan/umum/Pages/Teknologi-Informasi.aspx |
| Personal Data Protection Law | ✅ Compliant | https://www.kominfo.go.id/en/content/constitutional-court-no-20puu-xx-2022 |

### Thailand
| Regulation | Status | Source URL |
|------------|--------|------------|
| BOT Payment Systems Act | ✅ Compliant | https://www.bot.or.th/English/PaymentSystems/Pages/default.aspx |
| Personal Data Protection Act | ✅ Compliant | https://pdpc.go.th/en/law/personal-data-protection-act-2019/ |

### Taiwan
| Regulation | Status | Source URL |
|------------|--------|------------|
| FSC Payment Regulations | ✅ Compliant | https://www.fsc.gov.tw/en/home |
| Personal Data Protection Act | ✅ Compliant | https://www.moj.gov.tw/mp001.html |

### Hong Kong
| Regulation | Status | Source URL |
|------------|--------|------------|
| HKMA TRM Guidelines | ✅ Compliant | https://www.hkma.gov.hk/eng/key-functions/banking-stability/tech-risk-management/ |
| Personal Data Privacy Ordinance | ✅ Compliant | https://www.pcpd.org.hk/en/pdpo_ordinance.html |

## Usage

This template is used to create country-specific compliance matrices for each RFP response. All source URLs are verified and evidence is stored in the evidence directory.

## Related
- [[rfp-template-issuing]] — Issuing questionnaire
