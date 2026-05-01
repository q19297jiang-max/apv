---
type: working
stage: 3
created: '2026-05-01'
---

# Architecture Decision Log — ACME Payments Gateway

## Session: 2026-05-01

### Inputs Consumed
- `outputs/01-brainstorm.md` — Option A (Full-Stack Multi-AZ + Cross-Region DR) selected
- `outputs/02-compliance.md` — 10 regulatory frameworks mapped, 5 compliance gaps identified
- Knowledge files: `eks.md`, `ecs.md`, `rds.md`, `dr.md`, `gateway.md`, `tokenization.md`, `3ds.md`

### Key Design Drivers

| Driver | Source | Architecture Impact |
|--------|--------|-------------------|
| 500 TPS peak, 3x burst (1,500 TPS) | RFP §4 | Sized compute for 1,500 TPS headroom |
| PCI-DSS v4.0 Level 1 | RFP §5, Stage 2 | CDE subnet isolation, CloudHSM, dedicated node groups |
| 99.99% availability | RFP §3 | Multi-AZ everything, warm standby DR |
| 40% YoY growth | RFP §4 | 3-year horizon: Y1 500→Y3 980 TPS peak |
| Phase 2: Indonesia, Thailand | RFP §1 | DR in ap-southeast-3 (Jakarta) — dual-purpose |
| MAS TRM | Stage 2 | Audit logging, operational resilience, DR |
| Cross-border data transfer | Stage 2 gap | MY/PH data stays in SG region; ID data residency addressed by Jakarta DR |

### Decisions Made

| ADR | Decision | Alternatives Considered | Why Rejected |
|-----|----------|------------------------|--------------|
| ADR-1 | EKS over ECS | ECS Fargate (Option B from brainstorm) | Lacks Kubernetes NetworkPolicy for CDE micro-segmentation |
| ADR-2 | Aurora PG over RDS PG | Standard RDS PostgreSQL | No Global Database for DR; lower throughput |
| ADR-3 | Separate CDE/non-CDE node groups | Single node group with namespace isolation | QSA auditors prefer physical subnet separation |
| ADR-4 | CloudHSM for token keys | KMS only | KMS is FIPS 140-2 Level 2; Req 3.5 needs Level 3 |
| ADR-5 | Warm standby DR (Jakarta) | Pilot light, Active-Active | Pilot light too slow (1-4h RTO); Active-Active overkill for Phase 1 |
| ADR-6 | WAF + Shield Advanced | WAF only | Shield Advanced needed for DDoS cost protection at this volume |
| ADR-7 | ElastiCache Redis cluster mode | Memcached, DynamoDB DAX | Redis supports encryption + persistence; cluster mode scales horizontally |

### CDE Boundary Definition

Services **inside CDE** (handle raw PAN):
- Authorization Engine
- Tokenization Service
- Fraud Scoring Service
- Card Network Connector
- Aurora Token Vault DB
- ElastiCache Redis (token cache)
- CloudHSM

Services **outside CDE** (no raw PAN):
- API Gateway Service (receives tokenized data or routes to CDE)
- 3DS Server (authenticates cardholder, no PAN access)
- Settlement Engine (uses tokenized references)
- Merchant Portal (dashboard, no CHD)
- OpenSearch (logs are masked/tokenized)

### Open Items for Stage 4

1. **Savings Plans vs On-Demand pricing** — All compute should be priced with 1-year No Upfront Compute Savings Plans
2. **Data transfer costs** — Cross-AZ and internet egress need estimation based on 50M txns/month
3. **CloudHSM pricing** — $1.20/hr per HSM node (2 nodes = ~$1,752/month) — verify in calculator
4. **Shield Advanced** — $3,000/month subscription + data transfer — verify
5. **NAT Gateway costs** — 3 NAT GWs processing payment traffic can be significant
6. **DR region pricing** — ap-southeast-3 may have different pricing than ap-southeast-1
7. **Growth projection** — Size for Y1 but provide Y2/Y3 scaling cost estimates

### Compliance Traceability

| PCI-DSS Requirement | Architecture Component |
|---------------------|----------------------|
| Req 1 (Firewall/Network) | VPC subnets, SGs, NACLs, CDE isolation |
| Req 2 (No defaults) | Secrets Manager, automated rotation |
| Req 3 (Protect stored data) | KMS, CloudHSM, Aurora encryption, tokenization |
| Req 4 (Encrypt transmission) | TLS 1.3, mTLS in CDE, Direct Connect to networks |
| Req 6 (Secure systems) | WAF, ECR scanning, Amazon Inspector |
| Req 7 (Restrict access) | IAM, IRSA, namespace RBAC |
| Req 8 (Identify users) | IAM, 3DS2.3 for cardholders |
| Req 10 (Track/monitor) | CloudTrail, CloudWatch, OpenSearch, S3 Object Lock |
| Req 11 (Test security) | Inspector, WAF logging, penetration testing |
