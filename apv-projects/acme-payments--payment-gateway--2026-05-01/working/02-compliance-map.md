---
type: working
stage: 2
created: '2026-05-01'
---

# Compliance Working Map — ACME Payments

## Scope

- **Markets:** Singapore (primary), Malaysia, Philippines
- **Business:** Card acquiring, issuing, gateway, tokenization, digital wallets, 3DS
- **Client:** MPI-licensed under SG PSA 2019
- **Compliance tier:** PCI-DSS v4.0 Level 1 (>6M txns/year = 600M/year projected)

## Regulation Inventory

### Global

| Regulation | Knowledge File | Source URL | Verified |
|-----------|---------------|------------|----------|
| PCI-DSS v4.0 | `compliance/pci-dss/overview.md` + Req 1-12 | https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf | 2026-04-24 |

### Singapore (Primary Market)

| Regulation | Knowledge File | Source URL | Verified |
|-----------|---------------|------------|----------|
| MAS TRM | `compliance/countries/sg/mas-trm.md` | https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf | 2026-04-24 |
| PDPA 2012 | `compliance/countries/sg/pdpa.md` | https://sso.agc.gov.sg/Act/PDPA2012 | 2026-04-24 |
| PSA 2019 | `compliance/countries/sg/psa.md` | https://sso.agc.gov.sg/Act/PSA2019 | 2026-04-24 |
| Cybersecurity Act | `compliance/countries/sg/csa.md` | Not extracted (gap) | — |

### Malaysia

| Regulation | Knowledge File | Source URL | Verified |
|-----------|---------------|------------|----------|
| BNM RM Guidelines | `compliance/countries/my/bnm-rm.md` | https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca | 2026-04-24 |
| PDPA 2010 | `compliance/countries/my/pdpa.md` | https://www.pdp.gov.my/index.php/en/pdpa-2010 | 2026-04-24 |
| PSA 2018 | `compliance/countries/my/psa.md` | https://www.bnm.gov.my/payment-systems-act | 2026-04-24 |
| FSA 2013 | `compliance/countries/my/fsa.md` | Not extracted (gap) | — |

### Philippines

| Regulation | Knowledge File | Source URL | Verified |
|-----------|---------------|------------|----------|
| BSP Circular 995 | `compliance/countries/ph/bsp-circular.md` | https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf | 2026-04-24 |
| DPA 2012 (RA 10173) | `compliance/countries/ph/pdpa.md` | https://privacy.gov.ph/data-privacy-act/ | 2026-04-24 |
| NPSP (BSP C1049) | `compliance/countries/ph/npsp.md` | https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf | 2026-04-24 |

## Requirement → Regulation Cross-Reference

### Explicit RFP Requirements

1. **PCI-DSS v4.0 Level 1** → PCI-DSS Req 1-12 (explicitly stated in RFP §5)
2. **MAS TRM audit logging** → MAS TRM Guidelines (explicitly stated in RFP §3)
3. **99.99% availability** → MAS TRM operational resilience + PCI-DSS Req 12
4. **TLS 1.3 + AES-256** → PCI-DSS Req 3 (stored data) + Req 4 (in-transit)
5. **Tokenization** → PCI-DSS Req 3 (minimize CDE scope)
6. **3DS 2.0** → PCI-DSS Req 8 + EMVCo 3DS specification
7. **DR capability** → MAS TRM business continuity

### Implicit Requirements (from business context)

8. **MPI licensing obligations** → SG PSA 2019 (ACME is MPI-licensed)
9. **Customer data in MY** → MY PDPA 2010 (cross-border transfer restrictions)
10. **Customer data in PH** → PH DPA 2012 (NPC registration required)
11. **Payment operations in MY** → MY PSA 2018 (operator registration with BNM)
12. **Payment operations in PH** → PH NPSP / BSP C1049 (BSP registration)
13. **Technology risk MY** → BNM RM Guidelines
14. **Technology risk PH** → BSP Circular 995

## Architecture Implications for Stage 3

- **Data residency:** MY PDPA 2010 restricts cross-border transfer of personal data. Architecture must consider whether transaction data for MY customers stays in-region or requires consent/adequacy mechanisms.
- **PH NPC registration:** Must register data processing systems with National Privacy Commission.
- **MAS TRM cloud outsourcing:** AWS deployment must comply with MAS outsourcing guidelines — notification to MAS may be required for material outsourcing.
- **PCI-DSS CDE scoping:** EKS pods handling card data must be in isolated network segments (PCI-DSS Req 1). Tokenization reduces CDE scope.
- **Key management:** CloudHSM or KMS required for PCI-DSS Req 3. HSM for production key storage.
- **Audit logging:** Centralized logging across all 3 markets (CloudTrail + CloudWatch) to satisfy MAS TRM + BSP C995 + BNM RM simultaneously.

## Open Items

- [ ] Extract SG CSA frontmatter — may apply if designated as CII
- [ ] Extract MY FSA frontmatter — additional financial services obligations
- [ ] Confirm MY PDPA cross-border transfer mechanism (consent vs adequacy)
- [ ] Confirm PH data localization requirements (if any beyond NPC registration)
- [ ] Map PCI-DSS Req 1-12 individually to architecture components (Stage 3)
