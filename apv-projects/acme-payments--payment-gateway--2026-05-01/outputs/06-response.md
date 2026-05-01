---
output_class: derived
stage: 6
created: '2026-05-01'
sources:
  - outputs/01-brainstorm.md
  - outputs/02-compliance.md
  - outputs/03-architecture.md
  - outputs/04-sizing.md
  - outputs/05-pricing.md
---

# RFP Response: Cloud-Native Payment Gateway for ACME Payments Pte Ltd

---

## 1. Executive Summary

We are pleased to submit this proposal for the design and implementation of a cloud-native payment gateway for ACME Payments Pte Ltd. Our solution delivers a PCI-DSS v4.0 Level 1 compliant, multi-availability-zone architecture on AWS Singapore (ap-southeast-1), engineered to process 500 TPS sustained with 1,500 TPS burst capacity during festive peaks.

The proposed platform supports card acquiring and issuing, digital wallets, and local payment methods across Singapore, Malaysia, and the Philippines at launch, with a clear expansion path into Indonesia and Thailand in Phase 2. The architecture is built on Amazon EKS with strict Cardholder Data Environment (CDE) isolation, Aurora PostgreSQL for transactional durability, and ElastiCache Redis for sub-millisecond token lookups — all backed by warm standby disaster recovery in ap-southeast-3 (Jakarta).

**Key highlights:**

- **99.99% availability** via Multi-AZ deployment across 3 Availability Zones with automated failover
- **PCI-DSS v4.0 Level 1** compliance with CDE network segmentation, CloudHSM for FIPS 140-2 Level 3 key management, and immutable 7-year audit logging
- **Regulatory coverage** across 10 applicable frameworks spanning Singapore (MAS TRM, PDPA, PSA), Malaysia (BNM RM, PDPA, PSA), and Philippines (BSP Circular 995, DPA, NPSP)
- **Total monthly cost of ~USD $19,923** on-demand (including ~$400 monitoring estimate), reducible to ~USD $16,761/month with 3-year Savings Plans (37% average savings on eligible components)
- **Go-live by December 2026** via a 5-phase implementation commencing July 2026

---

## 2. Understanding of Requirements

We understand ACME Payments requires a greenfield cloud-native payment gateway to support its Major Payment Institution (MPI) licence obligations in Southeast Asia. The following table summarises our understanding of the core requirements:

| Requirement | Our Understanding | Source |
|-------------|-------------------|--------|
| **Transaction Volume** | 50M monthly transactions, SGD 85 average value (~SGD 4.25B monthly GMV), 40% YoY growth | RFP §4 |
| **Peak Performance** | 500 TPS sustained, 3× festive multiplier (1,500 TPS burst) | RFP §4 |
| **Availability** | 99.99% uptime SLA with disaster recovery capability | RFP §3 |
| **Compliance** | PCI-DSS v4.0 Level 1 certification | RFP §5 |
| **Geographies** | Phase 1: Singapore, Malaysia, Philippines; Phase 2: Indonesia, Thailand | RFP §1 |
| **Cloud Platform** | AWS (primary) | RFP §3 |
| **API Architecture** | REST and gRPC endpoints | RFP §3 |
| **Capabilities** | Card acquiring, card issuing, digital wallets, local payment methods, tokenisation, 3D Secure 2.0 | RFP §2 |
| **Security** | End-to-end encryption (TLS 1.3, AES-256), comprehensive audit logging | RFP §5 |
| **Timeline** | Go-live December 2026 | RFP §7 |

---

## 3. Proposed Solution

### 3.1 Architecture Overview

The solution uses a three-zone network model within a single VPC (10.0.0.0/16) deployed across 3 Availability Zones in ap-southeast-1 (Singapore):

- **Public Zone** — ALB with TLS 1.3 termination, AWS WAF (OWASP rules, rate limiting at 1,000 req/s per IP), and Shield Advanced for DDoS protection
- **Private Zone (Non-CDE)** — EKS node groups hosting API Gateway, 3DS Server, Settlement Engine, and Merchant Portal services
- **Private Zone (CDE)** — Isolated EKS node groups hosting Authorization Engine, Tokenisation Service, Fraud Scoring, and Card Network Connector, with dedicated NACLs and security groups enforcing PCI-DSS Req 1

**Key architectural decisions:**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Container orchestration | Amazon EKS (over ECS) | Kubernetes NetworkPolicy enables CDE micro-segmentation; namespace-based CDE/non-CDE isolation |
| Transaction database | Aurora PostgreSQL Multi-AZ | 5× throughput over standard PostgreSQL; Aurora Global Database for cross-region DR (RPO <5 min) |
| CDE isolation | Separate EKS node groups + subnets | Physical subnet separation with taints/tolerations ensures CDE pods run only on CDE nodes |
| Token vault key management | CloudHSM (FIPS 140-2 Level 3) | PCI-DSS Req 3.5 compliance for tokenisation master keys; dual-control key ceremonies |
| DR strategy | Warm standby in ap-southeast-3 (Jakarta) | RTO ≤15 min, RPO ≤10 min; strategically aligned with Phase 2 Indonesia expansion |
| DDoS and application protection | WAF + Shield Advanced | PCI-DSS Req 6.6 (WAF), MAS TRM DDoS requirements; DDoS cost protection included |
| Token cache | ElastiCache Redis (cluster mode) | Sub-millisecond reads reduce CloudHSM calls; cluster mode scales horizontally with token growth |

### 3.2 Services Architecture

The gateway comprises eight microservices deployed on EKS:

| Service | Zone | Function |
|---------|------|----------|
| API Gateway Service | Non-CDE | REST/gRPC ingress, rate limiting, request routing |
| Authorization Engine | CDE | Card authorization, network routing (Visa, Mastercard, AMEX, JCB) |
| Tokenisation Service | CDE | PAN tokenisation/detokenisation via CloudHSM-protected vault |
| 3DS Server | Non-CDE | EMVCo 3DS v2.3 frictionless and challenge flows |
| Fraud Scoring Service | CDE | Real-time fraud scoring, velocity checks |
| Card Network Connector | CDE | ISO 8583 / API connectivity to card networks via Direct Connect |
| Settlement Engine | Non-CDE | Batch T+1 settlement and reconciliation |
| Merchant Portal | Non-CDE | Merchant dashboard, onboarding, reporting |

### 3.3 Data Architecture

| Data Store | Service | Technology | Configuration |
|------------|---------|------------|---------------|
| Transaction Database | Aurora PostgreSQL | db.r6g.2xlarge Multi-AZ | 500 GB, 6,000 IOPS, AES-256 at rest |
| Token Vault | Aurora PostgreSQL (CDE) | db.r6g.xlarge Multi-AZ | 200 GB, CloudHSM-encrypted |
| Token Cache | ElastiCache Redis | cache.r6g.xlarge | 3 shards × 2 replicas (cluster mode) |
| Audit Log Store | Amazon OpenSearch | 3× m6g.large.search | Immutable, 7-year retention |
| Object Storage | S3 | Versioned, lifecycle policy | Settlement files, reports, backups |

### 3.4 Disaster Recovery

The warm standby DR region (ap-southeast-3, Jakarta) operates at 30% of primary capacity:

| Component | DR Configuration | Failover Behaviour |
|-----------|-----------------|-------------------|
| EKS Cluster | 1 control plane, ~12 nodes (mixed) | Auto-scales to 100% on failover |
| Aurora Global DB | db.r6g.xlarge read replica | Promotes to primary (RPO ≤10 min) |
| ElastiCache | 3× cache.r6g.xlarge | Cache warming from Aurora on failover |
| Route 53 | Health checks + automated failover | DNS failover to DR region |

**Recovery targets:** RTO ≤15 minutes, RPO ≤10 minutes.

---

## 4. Compliance & Security

### 4.1 Regulatory Framework Coverage

Our solution addresses 10 regulatory frameworks across three jurisdictions:

| Framework | Jurisdiction | Source URL |
|-----------|-------------|------------|
| PCI-DSS v4.0 Level 1 | Global | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| MAS Technology Risk Management Guidelines | Singapore | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Singapore PDPA 2012 | Singapore | [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012) |
| Singapore Payment Services Act 2019 | Singapore | [PSA 2019](https://sso.agc.gov.sg/Act/PSA2019) |
| BNM Risk Management Guidelines | Malaysia | [BNM RM](https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca) |
| Malaysia PDPA 2010 | Malaysia | [PDPA 2010](https://www.pdp.gov.my/index.php/en/pdpa-2010) |
| Malaysia Payment Systems Act 2018 | Malaysia | [PSA 2018](https://www.bnm.gov.my/payment-systems-act) |
| BSP Circular No. 995 | Philippines | [BSP C995](https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf) |
| Philippines Data Privacy Act 2012 | Philippines | [DPA 2012](https://privacy.gov.ph/data-privacy-act/) |
| BSP Circular 1049 (NPSP) | Philippines | [BSP C1049](https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf) |

### 4.2 PCI-DSS v4.0 Level 1 Compliance Architecture

| PCI-DSS Requirement | Implementation | Source URL |
|---------------------|---------------|------------|
| Req 1: Network segmentation | Three-zone VPC model with CDE-dedicated subnets, NACLs, security groups | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 2: Secure configuration | AWS Secrets Manager with auto-rotation; no default credentials | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 3: Protect stored data | AES-256 encryption via KMS; PAN rendered unreadable via tokenisation | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 3.5: Key management | CloudHSM (FIPS 140-2 Level 3) for token vault master keys | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 4: Encrypt transmission | TLS 1.3 enforced on all endpoints; mTLS between CDE services | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 6: Secure development | WAF with OWASP Top 10 rules; Amazon Inspector for vulnerability scanning | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 7: Access control | IAM + IRSA (per-pod service accounts); least-privilege enforcement | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 8: Authentication | 3D Secure v2.3 for cardholder verification (frictionless + challenge) | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 10: Audit logging | CloudTrail + CloudWatch Logs → OpenSearch; immutable 7-year retention with S3 Object Lock | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| Req 11: Security testing | Amazon Inspector + ECR image scanning; continuous vulnerability assessment | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |

### 4.3 MAS TRM Compliance

| MAS TRM Requirement | Implementation | Source URL |
|--------------------|---------------|------------|
| Operational resilience | Multi-AZ deployment + warm standby DR; 99.99% availability SLA | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Audit trail | CloudTrail for all API calls; centralised logging to OpenSearch | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Business continuity | Warm standby DR in Jakarta; RTO ≤15 min, RPO ≤10 min | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| System monitoring | CloudWatch custom metrics, dashboards, alarms (P95 latency, error rates, TPS) | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| Incident management | SNS + PagerDuty integration; tiered alerting (P1 <5 min, P2 <30 min) | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |

### 4.4 Cross-Border Data Considerations

Malaysia PDPA 2010 and Philippines DPA 2012 impose restrictions on cross-border personal data transfers. The architecture addresses this through:

- Centralised processing in Singapore with data classification controls
- Data flow mapping between SG hub and MY/PH endpoints
- Phase 2 data residency design for Indonesia (in-country data storage per BI regulations)

---

## 5. Infrastructure & Sizing

### 5.1 Volume Profile

| Metric | Value |
|--------|-------|
| Monthly Transactions | 50,000,000 |
| Average TPS (steady state) | 19.3 |
| Peak TPS (customer-stated) | 500 |
| Design TPS (1.5× safety factor) | 750 |
| Burst TPS (3× festive peak) | 1,500 |
| Monthly GMV | SGD 4.25B |
| Year 2 Design TPS (40% growth) | 1,050 |

### 5.2 Compute Sizing

| Component | Instance Type | Count | vCPU | RAM (GiB) |
|-----------|--------------|-------|------|-----------|
| API Gateway Service | c6i.xlarge (4 vCPU, 8 GiB) | 6 | 24 | 48 |
| Authorization Engine | c6i.2xlarge (8 vCPU, 16 GiB) | 6 | 48 | 96 |
| Tokenisation Service | m6i.xlarge (4 vCPU, 16 GiB) | 6 | 24 | 96 |
| 3DS Server | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 |
| Fraud Scoring Service | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 |
| Settlement Engine | m6i.large (2 vCPU, 8 GiB) | 3 | 6 | 24 |
| Merchant Portal | m6i.large (2 vCPU, 8 GiB) | 3 | 6 | 24 |
| Card Network Connector | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 |
| **Primary Total** | | **36 nodes** | **156 vCPU** | **480 GiB** |
| DR (30% warm standby) | Mixed | ~12 nodes | ~47 vCPU | ~144 GiB |

Sizing basis: 200 TPS per vCPU industry benchmark for payment processing, with 1.5× safety factor applied. Minimum 2 instances per Availability Zone for all critical services.

### 5.3 Database & Cache Sizing

| Component | Configuration | Storage | IOPS |
|-----------|--------------|---------|------|
| Transaction DB | db.r6g.2xlarge Multi-AZ (8 vCPU, 64 GiB) | 500 GB gp3 | 6,000 |
| Token Vault DB | db.r6g.xlarge Multi-AZ (4 vCPU, 32 GiB) | 200 GB gp3 | 3,000 |
| Token Cache | cache.r6g.xlarge × 6 (3 shards × 2 replicas) | In-memory | N/A |
| Audit Log Store | m6g.large.search × 3 | 1 TB | N/A |

### 5.4 Growth Accommodation

Current sizing accommodates Year 1 volumes with headroom. Year 2 growth (40% increase to 1,050 design TPS) is addressed through horizontal pod autoscaling on EKS — no instance type changes required. The EKS node groups support cluster autoscaler for adding nodes as pod density increases.

---

## 6. Pricing

### 6.1 Monthly Cost Summary

All prices are USD, on-demand, AWS ap-southeast-1 (Singapore), sourced from [AWS Calculator](https://calculator.aws/) and verified against aws-component-catalog.md (last verified: 2026-04-28).

| Category | Monthly (USD) | Annual (USD) | % of Total |
|----------|--------------|-------------|------------|
| Primary Compute (EC2 + EBS) | $5,321.16 | $63,853.92 | 26.7% |
| EKS Control Planes (×2) | $146.00 | $1,752.00 | 0.7% |
| Database (Aurora Multi-AZ) | $2,749.56 | $32,994.72 | 13.8% |
| Cache (ElastiCache Redis) | $1,822.08 | $21,864.96 | 9.1% |
| OpenSearch (Audit Logs) | $420.48 | $5,045.76 | 2.1% |
| CloudHSM (2-node cluster) | $2,400.00 | $28,800.00 | 12.0% |
| Load Balancers (ALB + NLB) | $32.85 | $394.20 | 0.2% |
| Network (NAT GW + Direct Connect) | $457.50 | $5,490.00 | 2.3% |
| Security (Shield + WAF + KMS) | $3,100.00 | $37,200.00 | 15.6% |
| Storage (S3) | $12.49 | $149.88 | 0.1% |
| DR — Warm Standby | $3,061.31 | $36,735.72 | 15.4% |
| Monitoring (CloudWatch/CloudTrail) | ~$400 | ~$4,800 | ~2.0% |
| **Total (On-Demand)** | **~$19,923** | **~$239,086** | **100%** |

> Note: 5 components are estimated from public pricing pages rather than the verified aws-component-catalog.md: CloudHSM (High confidence), OpenSearch (Medium), db.r6g.xlarge Multi-AZ (Medium-High), NAT Gateway (High), Direct Connect port (Medium). See §8.2 for details.

### 6.2 Savings Plans Opportunity

With 3-year Compute Savings Plans (No Upfront), significant savings are available on eligible components:

| Category | On-Demand/mo | Savings Plan/mo | Discount |
|----------|-------------|----------------|----------|
| EC2 c6i (12 instances) | $2,233.80 | $1,338.18 | 40% |
| EC2 m6i (24 instances) | $3,087.36 | $1,975.91 | 36% |
| Aurora DB | $1,471.68 | $956.59 | 35% |
| ElastiCache Redis | $1,822.08 | $1,182.60 | 35% |
| **Savings-eligible total** | **$8,614.92** | **$5,453.28** | **37% avg** |

**With Savings Plans applied:** ~$16,761/month (~$201,132/year), saving approximately $3,162/month or $37,940/year.

### 6.3 3-Year TCO

| Scenario | Year 1 | Year 2 | Year 3 | 3-Year Total |
|----------|--------|--------|--------|-------------|
| On-Demand | ~$239K | ~$239K | ~$239K | ~$717K |
| With Savings Plans | ~$201K | ~$201K | ~$201K | ~$604K |

> Note: Year 2 and Year 3 volumes grow 40% YoY but are accommodated through EKS horizontal scaling, which adds incremental compute cost. The figures above reflect the base infrastructure; additional nodes may add ~$2,000–4,000/month by Year 3.

---

## 7. Implementation Timeline

The following phased approach targets the December 2026 go-live deadline, with implementation commencing July 2026.

### Phase 1: Foundation (July 2026 — Weeks 1–4)

| Activity | Duration | Deliverables |
|----------|----------|-------------|
| Project kickoff and detailed design | Week 1–2 | Solution design document, RACI matrix |
| AWS account setup and landing zone | Week 1–2 | Multi-account structure (prod, staging, DR), IAM baseline |
| VPC and network provisioning | Week 2–3 | 3-tier VPC, CDE subnets, NACLs, security groups |
| EKS cluster provisioning | Week 3–4 | CDE and non-CDE node groups, namespace policies |
| CI/CD pipeline setup | Week 3–4 | Infrastructure-as-code, container registry, deployment pipelines |

### Phase 2: Core Services (August–September 2026 — Weeks 5–12)

| Activity | Duration | Deliverables |
|----------|----------|-------------|
| Authorization Engine + Card Network Connector | Week 5–8 | Card auth flows for Visa, Mastercard, AMEX, JCB |
| Tokenisation Service + CloudHSM integration | Week 5–8 | Token vault, PAN tokenisation/detokenisation |
| API Gateway Service | Week 7–9 | REST and gRPC endpoints, rate limiting, routing |
| 3DS Server (v2.3) | Week 8–10 | Frictionless and challenge flows |
| Fraud Scoring Service | Week 9–11 | Real-time scoring, velocity checks |
| Database provisioning (Aurora, ElastiCache) | Week 5–6 | Multi-AZ databases, cache clusters |

### Phase 3: Operations & Compliance (October 2026 — Weeks 13–16)

| Activity | Duration | Deliverables |
|----------|----------|-------------|
| Settlement Engine | Week 13–14 | Batch T+1 settlement, reconciliation |
| Merchant Portal | Week 14–15 | Dashboard, onboarding workflows |
| Monitoring and alerting | Week 13–15 | CloudWatch dashboards, OpenSearch, PagerDuty integration |
| Audit logging and compliance hardening | Week 14–16 | CloudTrail, immutable log retention, access reviews |
| DR region provisioning (ap-southeast-3) | Week 13–16 | Warm standby infrastructure, Aurora Global DB replication |

### Phase 4: Testing & Certification (November 2026 — Weeks 17–20)

| Activity | Duration | Deliverables |
|----------|----------|-------------|
| Integration testing (end-to-end) | Week 17–18 | All payment flows validated |
| Load testing (750 TPS sustained, 1,500 burst) | Week 18–19 | Performance benchmarks, capacity validation |
| DR failover testing | Week 19 | RTO/RPO verification |
| Card network certification testing | Week 18–20 | Visa, Mastercard, AMEX certification |
| PCI-DSS QSA pre-assessment | Week 19–20 | Gap remediation, evidence preparation |
| Security penetration testing | Week 19–20 | External pen test report |

### Phase 5: Go-Live (December 2026 — Weeks 21–22)

| Activity | Duration | Deliverables |
|----------|----------|-------------|
| Staged rollout (Singapore first) | Week 21 | Production traffic, monitoring |
| Malaysia and Philippines activation | Week 22 | Multi-market live |
| Hypercare support (30 days) | Week 21+ | Dedicated support team, daily health reviews |
| PCI-DSS QSA formal assessment | Post go-live | Level 1 Report on Compliance (ROC) |

**Critical path:** Authorization Engine → Card Network Certification → Load Testing → Go-Live

---

## 8. Assumptions & Caveats

### 8.1 Scope Assumptions

| # | Assumption | Impact if Incorrect |
|---|-----------|-------------------|
| 1 | This is a greenfield deployment with no migration from an existing gateway | Migration would add 4–6 weeks to timeline |
| 2 | 50M monthly transactions are primarily acquiring-side; issuing is a smaller supplementary workload | Separate issuing volumes would require additional sizing |
| 3 | SGD 85 average transaction value is blended across all payment methods | Different per-method averages may shift processing patterns |
| 4 | "In-store payments" refers to the gateway/acquiring backend, not physical POS terminal management | POS terminal infrastructure would be a separate workstream |
| 5 | 40% YoY growth is compounding (Y2: 70M/month, Y3: 98M/month) | Non-compounding growth would reduce Year 2–3 sizing needs |
| 6 | ACME will operate the platform with internal teams (managed services not in scope) | Managed operations would change the commercial model |

### 8.2 Pricing Assumptions

| # | Assumption | Confidence |
|---|-----------|-----------|
| 1 | All pricing is on-demand; Savings Plans shown separately as an option | N/A — conservative |
| 2 | CloudHSM at $1,200/node/month — sourced from [aws.amazon.com/cloudhsm/pricing](https://aws.amazon.com/cloudhsm/pricing/) (not in verified catalog) | **High** — stable public pricing |
| 3 | OpenSearch m6g.large.search estimated at 2× EC2 equivalent ($0.192/hr) | **Medium** — managed overhead factor approximate (±20%) |
| 4 | db.r6g.xlarge Multi-AZ estimated at 2× Single-AZ r6i.xlarge ($1.008/hr) | **Medium-High** — r6g ≈ r6i pricing; Multi-AZ = 2× is standard |
| 5 | NAT Gateway at ~$32.50/gateway/mo — sourced from [aws.amazon.com/vpc/pricing](https://aws.amazon.com/vpc/pricing/) (not in verified catalog) | **High** — stable public pricing |
| 6 | Direct Connect 1 Gbps port at $300/mo — catalog shows $0.30 (ambiguous hourly vs monthly); using industry standard | **Medium** — catalog entry ambiguous |
| 7 | DR region (ap-southeast-3) pricing assumed equivalent to ap-southeast-1 | Low risk — typically within 5% |
| 8 | LCU/NLCU load balancer usage charges excluded (usage-dependent) | Low risk |
| 9 | CloudWatch/CloudTrail estimated at ~$400/month (not itemised) | **Medium** — depends on log volume |

### 8.3 Compliance Caveats

- **PCI-DSS QSA assessment:** Level 1 certification requires annual on-site assessment by a Qualified Security Assessor. QSA engagement costs are not included in infrastructure pricing.
- **Cross-border data transfer:** Malaysia PDPA and Philippines DPA restrict cross-border personal data transfers. Detailed data flow mapping and consent mechanisms will be finalised during Phase 1 detailed design.
- **Singapore CSA:** The Cybersecurity Act may designate payment infrastructure as Critical Information Infrastructure (CII), imposing additional obligations. Proactive coverage is recommended.

### 8.4 Knowledge Gaps

The following items were identified during the analysis process and may require further clarification or verification:

| # | Gap | Severity |
|---|-----|----------|
| 1 | CloudHSM, OpenSearch, and NAT Gateway pricing not in verified catalog — estimated from public pricing pages | Medium |
| 2 | db.r6g.xlarge Multi-AZ pricing estimated (2× Single-AZ) — not confirmed in catalog | Medium |
| 3 | Direct Connect port fee listed as $0.30 in catalog (appears to be hourly); used $300/month industry standard | Medium |
| 4 | Local payment rail integration details (PayNow/FAST, GrabPay API, ShopeePay API) not fully documented | Medium |
| 5 | No payment-specific sizing benchmarks — used industry-standard 200 TPS/vCPU ratio | Medium |

---

## 9. Appendices

### Appendix A: Evidence References

| Evidence ID | Description | Source URL |
|-------------|-------------|------------|
| E-PCIDSS-01 | PCI-DSS v4.0 Standard (Requirements 1–12) | [PCI-DSS v4.0](https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf) |
| E-SG-01 | MAS Technology Risk Management Guidelines | [MAS TRM](https://www.mas.gov.sg/-/media/MAS/Technology-Risk-Managment/TRM%20Guidelines%20-%20Final.pdf) |
| E-SG-02 | Singapore PDPA 2012 | [PDPA 2012](https://sso.agc.gov.sg/Act/PDPA2012) |
| E-SG-03 | Singapore PSA 2019 | [PSA 2019](https://sso.agc.gov.sg/Act/PSA2019) |
| E-MY-01 | BNM Risk Management Guidelines | [BNM RM](https://www.bnm.gov.my/documents/20124/101659/0e422cd7-7852-4c29-8229-c8cc7f1d9dca) |
| E-MY-02 | Malaysia PDPA 2010 | [PDPA 2010](https://www.pdp.gov.my/index.php/en/pdpa-2010) |
| E-MY-03 | Malaysia PSA 2018 | [PSA 2018](https://www.bnm.gov.my/payment-systems-act) |
| E-PH-01 | BSP Circular 995 | [BSP C995](https://www.bsp.gov.ph/Regulations/Issuances/Circulars/2020/c995.pdf) |
| E-PH-02 | Philippines DPA 2012 | [DPA 2012](https://privacy.gov.ph/data-privacy-act/) |
| E-PH-03 | BSP Circular 1049 (NPSP) | [BSP C1049](https://www.bsp.gov.ph/Regulations/Issuances/Regulations/2018/Inst_1049.pdf) |

### Appendix B: Architecture Decision Records

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-1 | EKS over ECS | Kubernetes NetworkPolicy for CDE micro-segmentation |
| ADR-2 | Aurora PostgreSQL over RDS PostgreSQL | 5× throughput, built-in Multi-AZ, Global Database for DR |
| ADR-3 | Separate CDE/non-CDE EKS node groups | Physical subnet separation satisfies QSA auditors |
| ADR-4 | CloudHSM for token vault master keys | FIPS 140-2 Level 3 per PCI-DSS Req 3.5 |
| ADR-5 | Warm standby DR in Jakarta | RTO ≤15 min; aligns with Phase 2 Indonesia expansion |
| ADR-6 | WAF + Shield Advanced | PCI-DSS Req 6.6 + MAS TRM DDoS requirements |
| ADR-7 | ElastiCache Redis (cluster mode) | Sub-ms token lookups; horizontal scaling |

### Appendix C: Component Inventory

| # | Component | AWS Service | Qty | Configuration |
|---|-----------|-------------|-----|---------------|
| 1 | EKS Cluster (Primary) | EKS | 1 | Managed control plane |
| 2 | EKS Cluster (DR) | EKS | 1 | Warm standby control plane |
| 3 | API Gateway nodes | EC2 c6i.xlarge | 6 | Non-CDE, 2 per AZ |
| 4 | Authorization Engine nodes | EC2 c6i.2xlarge | 6 | CDE, 2 per AZ |
| 5 | Tokenisation Service nodes | EC2 m6i.xlarge | 6 | CDE, 2 per AZ |
| 6 | 3DS Server nodes | EC2 m6i.xlarge | 4 | Non-CDE |
| 7 | Fraud Scoring nodes | EC2 m6i.xlarge | 4 | CDE |
| 8 | Settlement Engine nodes | EC2 m6i.large | 3 | Non-CDE |
| 9 | Merchant Portal nodes | EC2 m6i.large | 3 | Non-CDE |
| 10 | Card Network Connector nodes | EC2 m6i.xlarge | 4 | CDE |
| 11 | Transaction DB | Aurora PostgreSQL | 2 inst | db.r6g.2xlarge Multi-AZ |
| 12 | Token Vault DB | Aurora PostgreSQL | 2 inst | db.r6g.xlarge Multi-AZ (CDE) |
| 13 | Token Cache | ElastiCache Redis | 6 nodes | cache.r6g.xlarge (3s×2r) |
| 14 | Audit Log Store | OpenSearch | 3 nodes | m6g.large.search |
| 15 | CloudHSM | CloudHSM | 2 nodes | FIPS 140-2 L3 cluster (CDE) |
| 16 | Public Load Balancer | ALB | 1 | TLS 1.3 termination |
| 17 | Internal Load Balancer | NLB | 1 | CDE TCP pass-through |
| 18 | DDoS Protection | Shield Advanced | 1 | Subscription |
| 19 | Application Firewall | WAF | 1 | Managed + custom rules |
| 20 | Key Management | KMS | 5 CMKs | Per data classification |
| 21 | DNS | Route 53 | 1 | Hosted zone + health checks |
| 22 | NAT Gateways | NAT GW | 3 | 1 per AZ |
| 23 | Card Network Link | Direct Connect | 1 | 1 Gbps dedicated |
| 24 | DR Compute | EC2 (mixed) | ~12 | 30% of primary |
| 25 | DR Database | Aurora Global DB | 1 | Read replica (r6g.xlarge) |
| 26 | DR Cache | ElastiCache Redis | 3 | Reduced replicas |

---

*This response was prepared on 2026-05-01. All pricing is based on publicly available AWS pricing for the ap-southeast-1 (Singapore) region, verified as of 2026-04-28. Figures are estimates and subject to change based on detailed design decisions and actual usage patterns.*
