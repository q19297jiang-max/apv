---
output_class: exploratory
stage: 1
created: '2026-05-01'
---

# RFP Brainstorm: ACME Payments — Payment Gateway

## Executive Summary

ACME Payments Pte Ltd, a licensed Major Payment Institution (MPI) in Singapore, is seeking a cloud-native payment gateway to support card acquiring/issuing, digital wallets, and local payment methods across Southeast Asia. The initial launch covers Singapore, Malaysia, and the Philippines, with Phase 2 expansion into Indonesia and Thailand. This is a greenfield deployment with aggressive timelines — go-live targeted for December 2026, just 5 months from implementation start.

The opportunity is significant: 50M monthly transactions in Year 1 at SGD 85 average value represents ~SGD 4.25B in monthly processing volume. With 40% YoY growth and a 3x peak multiplier, the infrastructure must be designed for substantial headroom from day one. The 99.99% availability SLA and PCI-DSS v4.0 Level 1 requirement place this firmly in the enterprise-grade tier, requiring Multi-AZ deployment with DR capabilities.

The evaluation criteria weight technical architecture (30%) and compliance/security (25%) equally with pricing/TCO (25%), signaling that ACME values a robust, compliant solution over the cheapest option. Our response should lead with architecture and compliance depth, supported by competitive pricing.

## Key Dimensions

| Dimension | Value | Source |
|-----------|-------|--------|
| Client | ACME Payments Pte Ltd (MPI-licensed) | RFP §1 |
| Solution | Cloud-native payment gateway | RFP §1 |
| Launch Markets | Singapore, Malaysia, Philippines | RFP §1 |
| Phase 2 Markets | Indonesia, Thailand | RFP §1 |
| Cloud Platform | AWS (primary), DR required | RFP §3 |
| Primary Region | ap-southeast-1 (Singapore) | RFP §3 |
| Monthly Txns (Y1) | 50,000,000 | RFP §4 |
| Avg Txn Value | SGD 85 | RFP §4 |
| Monthly Volume | ~SGD 4.25B | Calculated |
| Peak TPS | 500 | RFP §4 |
| Peak Multiplier | 3x (festive) | RFP §4 |
| Growth Rate | 40% YoY | RFP §4 |
| Availability SLA | 99.99% | RFP §3 |
| Compliance | PCI-DSS v4.0 Level 1 | RFP §5 |
| Response Due | 2026-05-15 | RFP §7 |
| Go-live Target | 2026-12-01 | RFP §7 |
| Implementation Duration | ~5 months | RFP §7 |

## Strategic Options

### Option A: Full-Stack AWS Multi-AZ with Cross-Region DR (Recommended)

**Architecture:** Multi-AZ deployment in ap-southeast-1 with warm standby DR in ap-southeast-3 (Jakarta) or ap-southeast-5 (Malaysia). EKS-based microservices architecture for the gateway core, RDS Multi-AZ for transactional data, ElastiCache for session/token caching.

**Rationale:**
- Multi-AZ in Singapore satisfies 99.99% SLA requirement
- Cross-region DR addresses business continuity and positions well for Phase 2 Indonesia/Thailand expansion
- EKS provides container orchestration suited for microservices payment processing
- Aligns with MAS TRM requirements for operational resilience

**Key components:**
- EKS cluster (3 AZ) for gateway services
- RDS Aurora PostgreSQL Multi-AZ for transaction store
- ElastiCache Redis for tokenization cache and session management
- AWS KMS / CloudHSM for encryption key management (PCI-DSS Req 3)
- API Gateway + NLB for ingress
- WAF + Shield Advanced for DDoS protection
- CloudTrail + CloudWatch for audit logging (MAS TRM)

**Pros:** Best compliance posture, highest availability, natural Phase 2 expansion path
**Cons:** Higher upfront cost, more complex operations

### Option B: Simplified Multi-AZ with Pilot Light DR

**Architecture:** Multi-AZ in ap-southeast-1 only, with pilot light DR (minimal standby resources, scaled up on failover). ECS Fargate instead of EKS for simpler operations.

**Rationale:**
- Lower operational complexity and cost
- ECS Fargate reduces Kubernetes overhead
- Pilot light DR saves ~40% on DR costs vs warm standby
- Acceptable for initial launch phase

**Key components:**
- ECS Fargate clusters across 3 AZs
- RDS PostgreSQL Multi-AZ
- ElastiCache Redis
- Simplified DR with automated scaling playbooks

**Pros:** Lower cost (~20-30% savings), faster to deploy, simpler operations
**Cons:** Higher RTO for DR failover (~30 min vs ~5 min), less mature for Phase 2 multi-region, may not fully satisfy MAS TRM operational resilience expectations

### Recommendation

**Option A** is recommended. The 99.99% SLA, PCI-DSS L1, and MAS TRM requirements demand enterprise-grade infrastructure. The additional cost is justified by compliance posture and the natural expansion path into Phase 2 markets. Option B can be presented as a phased approach where Phase 1 starts simplified and evolves.

## Knowledge Coverage

| Domain | Status | Files Available | Notes |
|--------|--------|----------------|-------|
| Card Systems — Gateway | ✅ Covered | `gateway.md` | Verified 2026-04-24 |
| Card Systems — 3DS | ✅ Covered | `3ds.md` | EMVCo v2.3, verified 2026-04-24 |
| Card Systems — Tokenization | ✅ Covered | `tokenization.md` | Available |
| Card Systems — Acquiring | ✅ Covered | `acquiring.md` | Available |
| Card Systems — Issuing | ✅ Covered | `issuing.md` | Available |
| Card Systems — Digital Wallet | ✅ Covered | `digital-wallet.md` | Available |
| PCI-DSS v4.0 | ✅ Covered | `overview.md` + 12 requirement files | Full coverage Req 1-12 |
| Compliance — Singapore | ✅ Covered | `mas-trm.md`, `pdpa.md`, `psa.md`, `csa.md` | 4 files |
| Compliance — Malaysia | ✅ Covered | `bnm-rm.md`, `pdpa.md`, `psa.md`, `fsa.md` | 4 files |
| Compliance — Philippines | ✅ Covered | `bsp-circular.md`, `pdpa.md`, `npsp.md` | 3 files |
| Compliance — Indonesia (Phase 2) | ✅ Covered | `bi-regulations.md`, `data-residency.md`, `pdpa.md` | 3 files |
| Compliance — Thailand (Phase 2) | ✅ Covered | `bot-payment.md`, `pdpa.md`, `financial-act.md` | 3 files |
| Infrastructure — AWS | ✅ Covered | `ecs.md`, `eks.md`, `rds.md`, `dr.md` | 4 files |
| Pricing — AWS | ✅ Covered | `aws.md`, `aws-component-catalog.md` | Verified 2026-04-28, valid until 2026-05-28 |
| Sizing | ✅ Covered | `tps-calculator.md` | Methodology available |
| Patterns | ⚠️ Template only | `.template.md` | No patterns documented yet |
| Commercial | ❓ Unknown | Not checked | May contain commercial templates |

## Gaps & Assumptions

### Knowledge Gaps

1. **Patterns domain is empty** — No reference architectures or design patterns documented. Will need to construct architecture from first principles using infrastructure and card-systems knowledge.
2. **Local payment methods (PayNow, GrabPay, ShopeePay)** — Digital wallet knowledge exists but coverage of Singapore-specific local payment rails (PayNow/FAST) is uncertain.
3. **Multi-region data residency architecture** — Indonesia and Philippines have data residency requirements. Knowledge files exist for ID data residency but architecture patterns for multi-region data isolation are not documented.
4. **gRPC endpoint patterns** — RFP requires both REST and gRPC. No specific knowledge on gRPC deployment patterns for payment systems.
5. **CloudHSM / KMS pricing** — Critical for PCI-DSS Req 3 (stored data protection). Need to verify coverage in AWS pricing knowledge.
6. **Settlement and reconciliation architecture** — Real-time settlement is a business requirement; no specific patterns documented.

### Assumptions

1. **AWS ap-southeast-1 is primary** — DR region will be determined during architecture stage; likely ap-southeast-3 (Jakarta) for Phase 2 alignment.
2. **PCI-DSS v4.0 scope** — Assuming full CDE (Cardholder Data Environment) scope for the gateway, not SAQ-based.
3. **50M monthly transactions are acquiring-side** — Issuing volumes not specified separately; assuming issuing is a smaller supplementary workload.
4. **SGD 85 average includes all payment methods** — Card and wallet transactions blended.
5. **40% YoY growth is compounding** — Y2: 70M, Y3: 98M monthly transactions. Sizing should account for 3-year horizon.
6. **"In-store payments" implies POS integration** — May require additional terminal management infrastructure not detailed in RFP.

## Clarification Questions

1. **Issuing volume split:** What percentage of the 50M monthly transactions are issuing vs. acquiring? Are there separate volume projections for card issuing?
2. **In-store POS scope:** Does "in-store payments" require us to provide or integrate with physical POS terminals, or is this limited to the gateway/acquiring backend?
3. **DR RTO/RPO targets:** The RFP specifies 99.99% availability and DR capability. What are the specific RTO and RPO targets for disaster recovery?
4. **Data residency specifics:** For Malaysia and Philippines, are there explicit data residency requirements, or is this only for Phase 2 markets (Indonesia)?
5. **Existing infrastructure:** Is ACME migrating from an existing gateway or is this a greenfield deployment? Any existing integrations to consider?
6. **Settlement rails:** Which settlement rails and banking partners are in scope? Does ACME have existing banking relationships for settlement, or do we need to include settlement network connectivity?
7. **Phase 2 timeline:** When is Phase 2 (Indonesia, Thailand) expected? This affects whether we design multi-region from day one or retrofit later.
8. **Team and operations model:** Will ACME operate the platform internally, or is managed services / outsourced operations in scope?
9. **Load testing expectations:** Are there specific load testing or certification requirements before go-live (e.g., card network certification testing)?
10. **Budget range:** Is there an indicative budget range or TCO ceiling for the solution?
