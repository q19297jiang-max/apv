---
output_class: derived
stage: 3
created: '2026-05-01'
---

# Architecture Design: ACME Payments — Payment Gateway

## Overview

This architecture delivers a PCI-DSS v4.0 Level 1 compliant payment gateway on AWS ap-southeast-1 (Singapore), designed for 500 TPS sustained (1,500 TPS burst during festive peaks). The design uses Amazon EKS across 3 Availability Zones with strict CDE network segmentation, RDS Aurora PostgreSQL for transactional data, ElastiCache Redis for tokenization cache and session management, and warm standby DR in ap-southeast-3 (Jakarta).

The architecture enforces a three-zone network model — Public, Private (non-CDE), and CDE — with all cardholder data processing isolated in dedicated CDE subnets protected by security groups, NACLs, and WAF. KMS provides envelope encryption for data at rest; CloudHSM secures the token vault's master keys per PCI-DSS Requirement 3.5.

## Architecture Diagram (Text)

```
                            ┌─────────────────────────────────────────────────────┐
                            │                    INTERNET                         │
                            └──────────────────────┬──────────────────────────────┘
                                                   │
                                          ┌────────▼────────┐
                                          │   Route 53      │
                                          │   (DNS + Health) │
                                          └────────┬────────┘
                                                   │
                            ┌──────────────────────▼──────────────────────────────┐
                            │              VPC: 10.0.0.0/16                       │
                            │                                                     │
                            │  ┌──────────────────────────────────────────────┐   │
                            │  │         PUBLIC SUBNETS (3 AZs)               │   │
                            │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
                            │  │  │ ALB      │  │ WAF +    │  │ Shield   │   │   │
                            │  │  │ (TLS     │  │ Rate     │  │ Advanced │   │   │
                            │  │  │  term)   │  │ Limiting │  │          │   │   │
                            │  │  └────┬─────┘  └──────────┘  └──────────┘   │   │
                            │  └───────┼──────────────────────────────────────┘   │
                            │          │                                          │
                            │  ┌───────▼──────────────────────────────────────┐   │
                            │  │      PRIVATE SUBNETS — NON-CDE (3 AZs)      │   │
                            │  │                                              │   │
                            │  │  ┌─────────────────────────────────────┐     │   │
                            │  │  │        EKS CLUSTER (Non-CDE)        │     │   │
                            │  │  │  ┌───────────┐  ┌───────────────┐   │     │   │
                            │  │  │  │ API       │  │ 3DS Server    │   │     │   │
                            │  │  │  │ Gateway   │  │ (Frictionless │   │     │   │
                            │  │  │  │ Service   │  │  + Challenge) │   │     │   │
                            │  │  │  └─────┬─────┘  └───────┬───────┘   │     │   │
                            │  │  │  ┌─────┴─────┐  ┌───────┴───────┐   │     │   │
                            │  │  │  │ Merchant  │  │ Settlement    │   │     │   │
                            │  │  │  │ Portal    │  │ Engine        │   │     │   │
                            │  │  │  └───────────┘  └───────────────┘   │     │   │
                            │  │  └─────────────────────────────────────┘     │   │
                            │  │                                              │   │
                            │  │  ┌─────────────┐  ┌───────────────────────┐  │   │
                            │  │  │ CloudWatch  │  │ OpenSearch (Logs)     │  │   │
                            │  │  └─────────────┘  └───────────────────────┘  │   │
                            │  └──────────────────────┬───────────────────────┘   │
                            │                         │ (Security Group boundary) │
                            │  ┌──────────────────────▼───────────────────────┐   │
                            │  │      PRIVATE SUBNETS — CDE (3 AZs)          │   │
                            │  │      PCI-DSS Cardholder Data Environment     │   │
                            │  │                                              │   │
                            │  │  ┌─────────────────────────────────────┐     │   │
                            │  │  │        EKS NODE GROUP (CDE)         │     │   │
                            │  │  │  ┌───────────┐  ┌───────────────┐   │     │   │
                            │  │  │  │ Auth      │  │ Tokenization  │   │     │   │
                            │  │  │  │ Engine    │  │ Service       │   │     │   │
                            │  │  │  │ (card     │  │ (token vault  │   │     │   │
                            │  │  │  │  auth)    │  │  + detokenize)│   │     │   │
                            │  │  │  └───────────┘  └───────────────┘   │     │   │
                            │  │  │  ┌───────────┐  ┌───────────────┐   │     │   │
                            │  │  │  │ Fraud     │  │ Card Network  │   │     │   │
                            │  │  │  │ Scoring   │  │ Connector     │   │     │   │
                            │  │  │  │ Service   │  │ (Visa/MC/AMEX)│   │     │   │
                            │  │  │  └───────────┘  └───────────────┘   │     │   │
                            │  │  └─────────────────────────────────────┘     │   │
                            │  │                                              │   │
                            │  │  ┌─────────────┐  ┌────────────┐             │   │
                            │  │  │ Aurora PG   │  │ ElastiCache│             │   │
                            │  │  │ Multi-AZ    │  │ Redis      │             │   │
                            │  │  │ (txn store) │  │ (token     │             │   │
                            │  │  │             │  │  cache)    │             │   │
                            │  │  └─────────────┘  └────────────┘             │   │
                            │  │                                              │   │
                            │  │  ┌─────────────┐  ┌────────────┐             │   │
                            │  │  │ CloudHSM    │  │ KMS        │             │   │
                            │  │  │ (token      │  │ (envelope  │             │   │
                            │  │  │  master key)│  │  encrypt)  │             │   │
                            │  │  └─────────────┘  └────────────┘             │   │
                            │  └──────────────────────────────────────────────┘   │
                            │                                                     │
                            │  ┌──────────────────────────────────────────────┐   │
                            │  │  VPN / Direct Connect to Card Networks       │   │
                            │  │  (Visa, Mastercard, AMEX, JCB)               │   │
                            │  └──────────────────────────────────────────────┘   │
                            └─────────────────────────────────────────────────────┘

                            ┌─────────────────────────────────────────────────────┐
                            │  DR REGION: ap-southeast-3 (Jakarta)                │
                            │  Strategy: Warm Standby                             │
                            │  ┌────────────┐ ┌────────────┐ ┌────────────┐       │
                            │  │ EKS (scaled│ │ Aurora     │ │ ElastiCache│       │
                            │  │  down)     │ │ Read       │ │ Replica    │       │
                            │  │            │ │ Replica    │ │            │       │
                            │  └────────────┘ └────────────┘ └────────────┘       │
                            └─────────────────────────────────────────────────────┘
```

## Components

### Compute

| Component | AWS Service | Instance / Config | Purpose | Compliance Requirement |
|-----------|-------------|-------------------|---------|----------------------|
| API Gateway Service | EKS (non-CDE node group) | c6i.xlarge × 6 (2 per AZ) | REST/gRPC ingress, rate limiting, request routing | PCI-DSS Req 1 (firewall), Req 6 (secure dev) |
| Authorization Engine | EKS (CDE node group) | c6i.2xlarge × 6 (2 per AZ) | Card authorization, routing to networks | PCI-DSS Req 3, 4 (protect CHD in transit/storage) |
| Tokenization Service | EKS (CDE node group) | m6i.xlarge × 6 (2 per AZ) | Token vault, tokenize/detokenize PAN | PCI-DSS Req 3.5 (cryptographic key mgmt) |
| 3DS Server | EKS (non-CDE node group) | m6i.xlarge × 4 (min) | 3DS2.3 frictionless + challenge flows | PCI-DSS Req 8 (strong auth), EMVCo 3DS |
| Fraud Scoring Service | EKS (CDE node group) | m6i.xlarge × 4 | Real-time fraud scoring, velocity checks | PCI-DSS Req 6 (secure systems) |
| Settlement Engine | EKS (non-CDE node group) | m6i.large × 3 | Batch settlement, reconciliation (T+1) | MAS TRM (operational resilience) |
| Merchant Portal | EKS (non-CDE node group) | m6i.large × 3 | Merchant dashboard, onboarding | PCI-DSS Req 7 (access control) |
| Card Network Connector | EKS (CDE node group) | m6i.xlarge × 4 | ISO 8583 / API connectivity to Visa, MC, AMEX | PCI-DSS Req 4 (encrypted transmission) |

### Data

| Component | AWS Service | Config | Purpose | Compliance |
|-----------|-------------|--------|---------|------------|
| Transaction Database | Aurora PostgreSQL Multi-AZ | db.r6g.2xlarge, 2 instances, encrypted | Transaction records, merchant configs, settlement data | PCI-DSS Req 3 (AES-256 at rest), Req 10 (audit trail) |
| Token Cache | ElastiCache Redis (cluster mode) | cache.r6g.xlarge, 3 shards × 2 replicas | Token-to-PAN mapping cache, session storage, 3DS context | PCI-DSS Req 3 (minimize CHD storage duration) |
| Audit Log Store | Amazon OpenSearch | 3 × m6g.large.search | Immutable audit logs (7-year retention) | PCI-DSS Req 10.7, MAS TRM (audit trail) |
| Token Vault (persistent) | Aurora PostgreSQL (CDE) | db.r6g.xlarge, encrypted + CloudHSM | Persistent token-to-PAN mappings | PCI-DSS Req 3.4, 3.5 (render PAN unreadable) |
| Object Storage | S3 (encrypted) | Versioned, lifecycle policy | Settlement files, reports, backups | PCI-DSS Req 3 (AES-256), MAS TRM |

### Network & Security

| Layer | Component | Config | Purpose |
|-------|-----------|--------|---------|
| Edge | AWS Shield Advanced | Enabled on ALB, Route 53 | DDoS protection (L3/L4/L7) |
| Edge | AWS WAF | Rate limiting (1000 req/s per IP), geo-blocking, OWASP rules | Application-layer protection, PCI-DSS Req 6.6 |
| Load Balancer | ALB (public) | TLS 1.3 termination, target groups per service | External traffic entry point |
| Load Balancer | NLB (internal, CDE) | TCP pass-through | CDE-internal service communication |
| Network Segmentation | VPC Subnets | 3-tier: Public, Private (non-CDE), Private (CDE) | PCI-DSS Req 1 (CDE isolation) |
| Micro-segmentation | Security Groups | Per-service SGs, deny-all default | PCI-DSS Req 1.3 (restrict inbound/outbound) |
| Network ACL | NACLs | Stateless rules on CDE subnets | Defense-in-depth, CDE boundary enforcement |
| Encryption (at rest) | AWS KMS | CMK per data classification, automatic rotation | PCI-DSS Req 3.4 (render PAN unreadable) |
| Encryption (HSM) | CloudHSM | FIPS 140-2 Level 3, 2-node cluster | PCI-DSS Req 3.5 (token vault master keys) |
| Encryption (in transit) | TLS 1.3 | Enforced on all endpoints, mTLS between CDE services | PCI-DSS Req 4 (encrypt open network transmission) |
| Secrets Management | AWS Secrets Manager | Auto-rotation, IAM-scoped access | PCI-DSS Req 2 (no default credentials) |
| Identity | IAM + IRSA | Service accounts per pod, least-privilege | PCI-DSS Req 7 (restrict access by need-to-know) |
| Card Network Connectivity | AWS Direct Connect / VPN | Dedicated connections to Visa, MC, AMEX, JCB | PCI-DSS Req 4 (encrypted transmission to networks) |

### Monitoring & Operations

| Function | AWS Service | Config | Compliance |
|----------|-------------|--------|------------|
| Metrics & Alerting | CloudWatch | Custom metrics, dashboards, alarms (P95 latency, error rates, TPS) | MAS TRM (system monitoring) |
| Centralized Logging | CloudWatch Logs → OpenSearch | All pod logs, VPC flow logs, WAF logs | PCI-DSS Req 10 (track all access) |
| Audit Trail | CloudTrail | All API calls, multi-region trail, S3 archival | PCI-DSS Req 10.2 (automated audit trails) |
| Log Integrity | CloudWatch Logs + S3 Object Lock | Immutable, 7-year retention | PCI-DSS Req 10.7 (retain logs ≥1 year) |
| Incident Response | SNS + PagerDuty integration | Tiered alerting: P1 (<5 min), P2 (<30 min) | MAS TRM (incident management) |
| Vulnerability Scanning | Amazon Inspector + ECR scanning | Continuous container image scanning | PCI-DSS Req 6.3, 11.3 (vulnerability mgmt) |
| DR Failover | Route 53 health checks | Automated failover to ap-southeast-3 | MAS TRM (business continuity) |
| Backup | AWS Backup | Aurora: continuous + 35-day PITR; Redis: daily snapshots | PCI-DSS Req 9, MAS TRM (data protection) |

## Architecture Decisions

### ADR-1: EKS over ECS for Container Orchestration

- **Context:** Need container orchestration for 8+ microservices with CDE isolation, service mesh, and fine-grained network policies. Both EKS and ECS are PCI-DSS certified on AWS.
- **Decision:** Use Amazon EKS with managed node groups.
- **Rationale:** EKS provides Kubernetes NetworkPolicy for CDE micro-segmentation (critical for PCI-DSS Req 1), namespace-based isolation between CDE and non-CDE workloads, and a richer ecosystem for service mesh (Istio/Linkerd for mTLS). ECS lacks native NetworkPolicy equivalents.
- **Consequences:** Higher operational complexity; requires Kubernetes expertise. Mitigated by managed node groups and EKS add-ons.

### ADR-2: Aurora PostgreSQL over RDS PostgreSQL

- **Context:** Transaction database must support Multi-AZ HA, cross-region replication for DR, and high write throughput at 500 TPS.
- **Decision:** Use Aurora PostgreSQL (Multi-AZ).
- **Rationale:** Aurora provides 5× throughput over standard PostgreSQL, built-in Multi-AZ with 6-way storage replication, and Aurora Global Database for fast cross-region DR replication (RPO <5 min). Aligns with warm standby DR strategy.
- **Consequences:** ~20% cost premium over standard RDS PostgreSQL. Justified by performance and DR capabilities.

### ADR-3: Separate CDE and Non-CDE EKS Node Groups

- **Context:** PCI-DSS Req 1 mandates CDE isolation. Cardholder data processing (authorization, tokenization, fraud) must be separated from non-CDE services (merchant portal, settlement, 3DS).
- **Decision:** Two dedicated EKS node groups — CDE nodes in CDE subnets, non-CDE nodes in private subnets — with Kubernetes namespace + NetworkPolicy enforcement.
- **Rationale:** Physical subnet separation satisfies QSA auditors. Kubernetes taints/tolerations ensure CDE pods only schedule on CDE nodes. NetworkPolicy denies all traffic except explicitly allowed flows.
- **Consequences:** Increased node count and cost. Some services (3DS) placed in non-CDE because they don't handle raw PAN — they receive tokenized references.

### ADR-4: CloudHSM for Token Vault Master Keys

- **Context:** PCI-DSS Req 3.5 requires cryptographic key management with FIPS 140-2 Level 3 hardware. KMS alone uses FIPS 140-2 Level 2 for most operations.
- **Decision:** CloudHSM cluster (2 nodes) for token vault master key operations. KMS for all other encryption (EBS, S3, Aurora).
- **Rationale:** CloudHSM satisfies FIPS 140-2 Level 3 requirement for tokenization master keys. Dual-control key ceremonies supported. KMS is cost-effective for non-token encryption where Level 2 is acceptable.
- **Consequences:** CloudHSM adds ~$2,400/month (2 nodes). Required for PCI-DSS Level 1 certification of the tokenization subsystem.

### ADR-5: Warm Standby DR in ap-southeast-3 (Jakarta)

- **Context:** 99.99% availability SLA and MAS TRM require DR capability. Phase 2 expansion targets Indonesia, making Jakarta strategically valuable.
- **Decision:** Warm standby DR in ap-southeast-3. Aurora Global Database for async replication. EKS cluster scaled to 30% of primary capacity.
- **Rationale:** Warm standby provides RTO ≤15 min, RPO ≤10 min — exceeding typical MAS TRM expectations. Jakarta aligns with Phase 2 Indonesia expansion. Latency ~30ms from Singapore.
- **Consequences:** DR cost ~40-50% of primary. Trade-off accepted for compliance and strategic value. Pilot light alternative would save ~20% but increases RTO to 1-4 hours.

### ADR-6: WAF + Shield Advanced for DDoS and Application Protection

- **Context:** Payment gateway is internet-facing. PCI-DSS Req 6.6 requires WAF or code review. MAS TRM requires DDoS protection.
- **Decision:** AWS WAF on ALB with managed rule groups (OWASP Top 10, bot control, rate limiting). Shield Advanced for volumetric DDoS protection.
- **Rationale:** WAF satisfies PCI-DSS Req 6.6. Shield Advanced provides financial protection (DDoS cost protection) and 24/7 DDoS Response Team access. Rate limiting at 1,000 req/s per IP prevents abuse while allowing legitimate 500 TPS.
- **Consequences:** Shield Advanced costs $3,000/month + data transfer fees. Justified for a payment gateway processing SGD 4.25B monthly.

### ADR-7: ElastiCache Redis for Token Cache and Session Management

- **Context:** Tokenization detokenization must complete in <50ms. 3DS challenge flows require session state. Authorization routing needs sub-millisecond lookups.
- **Decision:** ElastiCache Redis in cluster mode (3 shards, 2 replicas each) deployed in CDE subnets.
- **Rationale:** Redis provides sub-millisecond reads for token cache hits, reducing CloudHSM calls. Cluster mode provides horizontal scaling for token cache growth. Encryption at rest and in transit enabled. Multi-AZ automatic failover.
- **Consequences:** Token cache is a hot path — cache miss falls back to Aurora + CloudHSM (adds ~80ms). Cache warming strategy needed for DR failover.

## Component Inventory for Sizing

The following components require pricing in Stage 4:

| # | Component | Service | Qty | Config | Zone |
|---|-----------|---------|-----|--------|------|
| 1 | EKS Cluster | EKS | 1 | Control plane | Primary |
| 2 | Non-CDE Node Group | EC2 (c6i.xlarge) | 6 | API GW service | Primary |
| 3 | Non-CDE Node Group | EC2 (m6i.xlarge) | 4 | 3DS Server | Primary |
| 4 | Non-CDE Node Group | EC2 (m6i.large) | 6 | Settlement + Portal | Primary |
| 5 | CDE Node Group | EC2 (c6i.2xlarge) | 6 | Auth Engine | Primary |
| 6 | CDE Node Group | EC2 (m6i.xlarge) | 14 | Token + Fraud + Network | Primary |
| 7 | Transaction DB | Aurora PostgreSQL | 2 | db.r6g.2xlarge Multi-AZ | Primary |
| 8 | Token Vault DB | Aurora PostgreSQL | 2 | db.r6g.xlarge Multi-AZ | Primary (CDE) |
| 9 | Token Cache | ElastiCache Redis | 6 | cache.r6g.xlarge (3s×2r) | Primary (CDE) |
| 10 | Audit/Log Search | OpenSearch | 3 | m6g.large.search | Primary |
| 11 | HSM | CloudHSM | 2 | FIPS 140-2 L3 cluster | Primary (CDE) |
| 12 | Load Balancer | ALB | 1 | Public, TLS termination | Primary |
| 13 | Load Balancer | NLB | 1 | Internal, CDE | Primary |
| 14 | DDoS Protection | Shield Advanced | 1 | Subscription | Primary |
| 15 | WAF | AWS WAF | 1 | Managed rules + custom | Primary |
| 16 | Key Management | KMS | 5 | CMKs (data classification) | Primary |
| 17 | DNS | Route 53 | 1 | Hosted zone + health checks | Global |
| 18 | DR EKS Cluster | EKS | 1 | Control plane | DR |
| 19 | DR Compute | EC2 (mixed) | ~12 | 30% of primary capacity | DR |
| 20 | DR Database | Aurora Global DB | 1 | Read replica, r6g.xlarge | DR |
| 21 | DR Cache | ElastiCache Redis | 3 | Reduced replicas | DR |
| 22 | Networking | VPC, NAT GW, PrivateLink | — | 3 NAT GWs (1 per AZ) | Primary |
| 23 | Storage | S3 | — | Logs, backups, settlements | Primary + DR |
| 24 | Monitoring | CloudWatch + CloudTrail | — | Enhanced monitoring | Primary + DR |
