---
type: apv-template
category: rfp-template
title: "Card Issuing RFP Questionnaire"
tags: [template, rfp-questionnaire, issuing]
---

# Card Issuing RFP Questionnaire

## Essential Questions (20)

### Card System Requirements
1. **Card Type**: [ ] Credit [ ] Debit [ ] Prepaid [ ] Corporate
2. **Card Brand**: [ ] Visa [ ] Mastercard [ ] UnionPay [ ] JCB
3. **Peak TPS**: ______ transactions/second
4. **Average TPH**: ______ transactions/hour
5. **Daily Volume**: ______ transactions/day
6. **Annual Volume**: ______ transactions/year
7. **Growth Rate**: ______% per year

### SLA Requirements
8. **Availability**: [ ] 99.9% [ ] 99.95% [ ] 99.99%
9. **RTO**: ______ hours/minutes
10. **RPO**: ______ hours/minutes
11. **Disaster Recovery**: [ ] Active-Active [ ] Warm Standby [ ] Pilot Light

### Compliance Requirements
12. **Country**: [Singapore|Malaysia|Philippines|Indonesia|Thailand|Taiwan|Hong Kong]
13. **PCI-DSS Required**: [ ] Yes [ ] No
14. **Additional Regulations**: [ ] MAS [ ] BNM [ ] BSP [ ] BI [ ] BOT [ ] FSC [ ] HKMA
15. **Data Residency**: [ ] Required [ ] Not Required

### Technical Requirements
16. **Cloud Provider**: [ ] AWS [ ] Azure [ ] GCP [ ] On-Premise [ ] Hybrid
17. **Region Preference**: ______
18. **Integration Requirements**: _______________________
19. **Existing Systems**: _______________________
20. **Timeline**: [ ] <3 months [ ] 3-6 months [ ] 6-12 months

## RFP Response Sections

Based on your answers, we will provide:

1. **Executive Summary** - Overview of proposed solution
2. **Compliance Matrix** - PCI-DSS and country-specific regulations
3. **Solution Architecture** - Detailed technical design with diagrams
4. **Infrastructure Sizing** - Component count and specifications
5. **Pricing Breakdown** - Monthly/annual costs with calculator evidence
6. **Implementation Plan** - Timeline and milestones

## Source URL Requirements

All responses will include:
- ✅ Official source URLs for compliance claims
- ✅ Official calculator URLs for pricing claims
- ✅ Technical documentation URLs for architecture claims
- ✅ Evidence screenshots for calculator outputs

## Related Templates
- [[rfp-template-acquiring]] — Acquiring questionnaire
- [[rfp-template-gateway]] — Payment gateway questionnaire
