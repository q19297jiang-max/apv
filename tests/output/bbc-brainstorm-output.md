# RFP Brainstorm: BBC Bank - Credit Card Issuing System

**Date**: 2026-04-24
**Skill**: rfp-brainstorm
**RFP**: BBC Bank Credit Card Issuing System

---

## Executive Summary Points

- **SaaS-First Approach**: Entry-level SaaS solution ideal for low-volume launch (2,200 cards Y1), scales to 4,400 cards by Y5
- **VISA-Certified Platform**: Full compliance with VISA standards for magnetic, chip/EMV, and contactless cards (Source: [[issuing]])
- **Rapid Deployment**: Standalone Phase 1 with no interface dependencies enables fast go-live in 3-4 months
- **Growth-Ready Architecture**: Designed to support future debit cards, mobile app, and tokenization without re-architecture
- **Cost-Effective**: Low TPS requirements (<1 TPS) allow shared infrastructure, reducing initial investment

---

## Compliance Landscape

### PCI-DSS Requirements

BBC Bank issuing platform must comply with all 12 PCI-DSS v4.0 requirements (Source: [[pci-dss-overview]])

| Requirement | Focus Area for Issuing | Source |
|-------------|----------------------|--------|
| Req 1 | Network security for authorization engine | [[pci-dss-req-1-network-security]] |
| Req 2 | Secure configuration of card systems | [[pci-dss-req-2-secure-configuration]] |
| Req 3 | Encrypted PAN/cardholder storage | [[pci-dss-req-3-stored-data]] |
| Req 4 | TLS 1.3 for authorization in transit | [[pci-dss-req-4-data-in-transit]] |
| Req 8 | Strong authentication for 20 users | [[pci-dss-req-8-authentication]] |
| Req 10 | Audit logging for all card operations | [[pci-dss-req-10-logging]] |

**Source URL**: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf

### Country Regulations

**⚠️ Knowledge Gap**: No Bangladesh-specific regulations in APV knowledge base. Current coverage includes SG, MY, PH, ID, TH, TW, HK.

**Recommendation**: Verify Bangladesh Bank requirements for:
- Licensing for credit card issuance
- Data residency requirements
- Financial reporting standards
- Consumer protection regulations

### VISA Compliance Requirements

All card types must follow VISA standards (Source: [[issuing]]):

- **Magnetic Stripe**: VISA magnetic stripe standard
- **Chip/EMV**: EMVCo contact chip specifications
- **Contactless**: VISA payWave standard
- **DCC**: Dynamic Currency Conversion standard

---

## Architecture Approach Options

### Option 1: SaaS Multi-Tenant (RECOMMENDED)

- **Pattern**: Cloud-native SaaS (Source: [[issuing]])
- **Cloud Provider**: AWS ap-south-1 (Mumbai) or ap-southeast-1 (Singapore)
- **Architecture**: Shared infrastructure with logical isolation
- **TPS Capacity**: 10 TPS shared capacity (sufficient for BBC's 0.5 TPS peak)
- **Regional Deployment**: Single-region deployment with disaster recovery

**Compliance Alignment**:
- PCI-DSS certified shared infrastructure (Source: [[pci-dss-overview]])
- VISA certified authorization engine
- HSM provided via cloud KMS

**Pros**:
- Lowest initial cost (shared infrastructure)
- Fastest deployment (3-4 months)
- Automatic updates and maintenance
- Scales seamlessly to Y5 volumes

**Cons**:
- Less customization flexibility
- Dependency on SaaS provider roadmap
- Potential regional compliance concerns

**Cost**: $2,000-5,000/month base + per-card fees

---

### Option 2: Dedicated Single-Tenant

- **Pattern**: Dedicated cloud deployment (Source: [[issuing]])
- **Cloud Provider**: AWS ap-south-1 (Mumbai) or ap-southeast-1 (Singapore)
- **Architecture**: EKS cluster with dedicated components
- **TPS Capacity**: 100 TPS dedicated capacity
- **Regional Deployment**: Multi-region for DR

**Compliance Alignment**:
- Full PCI-DSS control (Source: [[pci-dss-overview]])
- Dedicated VISA certification
- Customer-managed HSM

**Pros**:
- Full control over customization
- Easier regulatory compliance
- Predictable performance
- Future-proof for expansion

**Cons**:
- Higher initial cost ($15,000-25,000/month)
- Longer deployment (6-8 months)
- Customer manages operations

**Cost**: $15,000-25,000/month fixed

---

### Option 3: Hybrid (On-Premise Core + Cloud Authorization)

- **Pattern**: Hybrid deployment (not recommended for low volume)
- **Architecture**: On-premise CMS + cloud-based authorization
- **Consideration**: Not cost-effective for 2,200 cards

**NOT RECOMMENDED** for BBC Bank's volume.

---

## Regional Considerations

### Bangladesh Deployment

**Cloud Regions**:
- **AWS ap-south-1** (Mumbai, India): 1,500 km from Dhaka
- **AWS ap-southeast-1** (Singapore): 2,500 km from Dhaka

**Recommendation**: Use ap-southeast-1 (Singapore) for:
- Better VISA network connectivity
- Established financial services ecosystem
- Lower regulatory uncertainty

**Data Residency**: ⚠️ **Verify Bangladesh requirements** - no knowledge in wiki

**Network Connectivity**:
- Authorization latency to VISA: <200ms achievable from Singapore
- Branch connectivity: VPN or dedicated line required

**Certifications Required**:
- VISA Issuer certification
- PCI-DSS v4.0 compliance (Source: [[pci-dss-overview]])
- Bangladesh Bank license (verify requirement)

---

## Risk Mitigation Strategies

| Risk | Mitigation | Source |
|------|------------|--------|
| Low volume makes on-premise uneconomical | Recommend SaaS multi-tenant | [[issuing]] |
| Bangladesh regulations not covered | Engage local compliance expert | Knowledge gap |
| VISA certification timeline | Use VISA-certified SaaS platform | [[issuing]] |
| Phase 2 scope creep (debit/mobile) | Design architecture for future expansion | [[issuing]] |
| Branch connectivity for 20 users | Provide VPN/SD-WAN solution | Infrastructure best practices |
| Card embossing vendor integration | Standard SFTP interface to existing vendor | RFP requirements |

---

## Questions for Customer

1. **Bangladesh Regulations**: What are Bangladesh Bank's specific licensing and compliance requirements for credit card issuers?

2. **Data Residency**: Does Bangladesh have data residency requirements that would prevent using Singapore cloud region?

3. **VISA License**: Does BBC Bank already have a VISA issuer license, or is this part of the implementation?

4. **Growth Timeline**: When are debit cards, mobile app, and tokenization planned? (Helps architecture planning)

5. **Card Personalization**: Can the embossing vendor accept SFTP instead of email/FTP for security?

6. **Disaster Recovery**: What are the specific RTO/RPO requirements beyond "CNN SaaS standard"?

7. **User Training**: Will the 20 users need training, or is existing credit card experience assumed?

8. **Reporting Requirements**: Beyond "PSS standard reports," are there Bangladesh-specific regulatory reports needed?

---

## Knowledge Gaps

- **Bangladesh Regulations**: No knowledge on Bangladesh Bank licensing, data residency, or financial reporting requirements
  - **Suggest**: Consult Bangladesh Bank guidelines or local legal counsel

- **Bangladesh Data Privacy**: No knowledge on Bangladesh data protection laws (if any exist)
  - **Suggest**: Verify if PDPA-like regulations exist

- **Local Certifications**: Unknown if Bangladesh requires certifications beyond PCI-DSS and VISA
  - **Suggest**: Engage local compliance expert

---

## Recommended Approach

**Option 1: SaaS Multi-Tenant Platform**

**Rationale**:

1. **Volume Alignment**: BBC's 2,200 cards (0.5 TPS peak) is ideal for SaaS entry-level offering
2. **Cost Efficiency**: 80-90% lower cost than dedicated deployment
3. **Speed to Market**: 3-4 month deployment vs 6-8 months for dedicated
4. **Low Risk**: VISA-certified, PCI-DSS compliant platform (Source: [[pci-dss-overview]], [[issuing]])
5. **Future-Proof**: Can migrate to dedicated when volumes justify it (Y3-Y5)

**Key Design Decisions**:
- Cloud region: Singapore (ap-southeast-1) for VISA connectivity
- Authorization: Shared VISA-certified engine
- Database: Encrypted multi-tenant storage (PCI-DSS compliant)
- Branch access: Web portal + VPN for 20 users
- Embossing: SFTP integration to existing vendor

**Phase 1 Scope**:
- Credit card issuing (Classic, Gold/Platinum, Infinite)
- Plastic cards (magnetic, chip/EMV, contactless)
- Manual key-in by branch staff
- Standard VISA authorization and settlement
- Basic reporting and dashboard

**Future Phases** (architecture supports):
- Debit card issuance
- Mobile app integration
- Tokenization (virtual cards, digital wallet)
- Loyalty program integration

---

## Next Steps

1. **Verify Bangladesh Regulations**: Confirm Bangladesh Bank requirements before finalizing approach
2. **Proceed to rfp-compliance**: Generate detailed compliance matrix for PCI-DSS and VISA requirements
3. **Proceed to rfp-architect**: Design detailed SaaS-based credit card issuing architecture
4. **Proceed to rfp-calculator**: Calculate precise sizing for Y1-Y5 growth
5. **Proceed to rfp-pricer**: Generate SaaS pricing model with per-card costs

---

## Sources

### Compliance
- PCI-DSS v4.0: [[pci-dss-overview]] (source_url: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf)
- PCI-DSS Requirements 1-12: [[pci-dss-req-1]] through [[pci-dss-req-12]] (source_urls in individual files)

### Card Systems
- Issuing Platform: [[issuing]] (source_url: https://www.emvco.com/emv-technologies/payment-tokenization)

### Infrastructure
- Cloud patterns: [[aws-eks]], [[aws-rds]], [[aws-dr]] (vendor documentation)

### Knowledge Gaps
- Bangladesh regulations: Not covered in APV knowledge base
- Bangladesh data privacy: Not covered in APV knowledge base

---

**Skill Status**: ✅ COMPLETE
**Next Skill**: rfp-compliance
