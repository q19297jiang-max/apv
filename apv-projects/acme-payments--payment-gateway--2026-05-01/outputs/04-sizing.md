---
output_class: derived
stage: 4
created: '2026-05-01'
---

# Infrastructure Sizing: ACME Payments — Payment Gateway

## Volume Analysis

| Metric | Value | Formula / Source |
|--------|-------|-----------------|
| Monthly Transactions | 50,000,000 | Customer RFP |
| Average TPS | 19.3 | 50M ÷ (30 × 24 × 3,600) |
| Customer Peak TPS | 500 | Customer RFP (3× festive peak) |
| Design TPS | 750 | 500 × 1.5 safety factor |
| Burst TPS (ceiling) | 1,500 | 500 × 3× peak multiplier |
| Average Transaction Size | SGD 85 | Customer RFP |
| Monthly GMV | SGD 4.25B | 50M × SGD 85 |
| YoY Growth | 40% | Customer RFP |
| Year 2 Design TPS | 1,050 | 750 × 1.4 |

## Component Sizing

### Compute

| Component | Instance Type | Count | vCPU Total | RAM Total | Justification |
|-----------|--------------|-------|------------|-----------|---------------|
| API Gateway Service | c6i.xlarge (4 vCPU, 8 GiB) | 6 | 24 | 48 GiB | Ingress routing, ~200 TPS/vCPU headroom; 2 per AZ × 3 AZ |
| Authorization Engine | c6i.2xlarge (8 vCPU, 16 GiB) | 6 | 48 | 96 GiB | Core auth path, compute-heavy crypto; 750 TPS ÷ ~200 TPS/vCPU = 4 vCPU min, ×6 for HA |
| Tokenization Service | m6i.xlarge (4 vCPU, 16 GiB) | 6 | 24 | 96 GiB | Token vault ops, memory for cache; 2 per AZ × 3 AZ |
| 3DS Server | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 GiB | 3DS2.3 flows, stateful sessions |
| Fraud Scoring Service | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 GiB | Real-time scoring, velocity checks |
| Settlement Engine | m6i.large (2 vCPU, 8 GiB) | 3 | 6 | 24 GiB | Batch T+1, low steady-state TPS |
| Merchant Portal | m6i.large (2 vCPU, 8 GiB) | 3 | 6 | 24 GiB | Dashboard, low compute |
| Card Network Connector | m6i.xlarge (4 vCPU, 16 GiB) | 4 | 16 | 64 GiB | ISO 8583 / API to Visa, MC, AMEX, JCB |
| **Total Primary Compute** | | **36 nodes** | **156 vCPU** | **480 GiB** | |

### Database

| Component | Instance Type | Storage | IOPS | Justification |
|-----------|--------------|---------|------|---------------|
| Transaction DB | db.r6g.2xlarge Multi-AZ (8 vCPU, 64 GiB) | 500 GB gp3 | 6,000 | 750 TPS write path, 7-year retention, Multi-AZ for 99.99% SLA |
| Token Vault DB | db.r6g.xlarge Multi-AZ (4 vCPU, 32 GiB) | 200 GB gp3 | 3,000 | Token-to-PAN persistent store, CDE-isolated, CloudHSM-encrypted |
| Audit Log Store | 3× m6g.large.search (OpenSearch) | 1 TB | — | Immutable audit logs, 7-year retention (PCI-DSS Req 10.7) |

### Cache

| Component | Instance Type | Nodes | Justification |
|-----------|--------------|-------|---------------|
| Token Cache | cache.r6g.xlarge (4 vCPU, 32.3 GiB) | 6 (3 shards × 2 replicas) | Sub-ms token lookups, reduce CloudHSM calls; cluster mode for horizontal scaling |

### Network & Security

| Component | Capacity | Justification |
|-----------|----------|---------------|
| ALB (public) | 750 TPS × 2 KB = ~12 Mbps sustained | TLS 1.3 termination, external entry |
| NLB (internal CDE) | CDE-internal east-west traffic | TCP pass-through for CDE services |
| NAT Gateway | 3 (1 per AZ) | Outbound internet for card networks, updates |
| Direct Connect | 1 Gbps | Dedicated link to Visa/MC/AMEX/JCB |
| CloudHSM | 2-node cluster | FIPS 140-2 L3, token vault master keys |
| WAF | 1,000 req/s per IP rate limit | PCI-DSS Req 6.6 |
| Shield Advanced | 1 subscription | DDoS L3/L4/L7 protection |

## HA/DR Impact

| Component | Base Count | HA Factor | Final Count | Reason |
|-----------|-----------|-----------|-------------|--------|
| Primary Compute | 36 nodes | 1× (already 3-AZ) | 36 | Sized with 2 per AZ minimum |
| Transaction DB | 1 | 2× (Multi-AZ) | 2 instances | Aurora Multi-AZ (included in pricing) |
| Token Vault DB | 1 | 2× (Multi-AZ) | 2 instances | Aurora Multi-AZ (included in pricing) |
| Token Cache | 3 shards | 2× (replicas) | 6 nodes | Cluster mode with replicas |
| CloudHSM | 1 | 2× (HA cluster) | 2 nodes | FIPS 140-2 requirement |
| DR Compute | — | 30% of primary | ~12 nodes | Warm standby ap-southeast-3 |
| DR Database | — | 1× read replica | 1 (r6g.xlarge) | Aurora Global DB async replication |
| DR Cache | — | 50% of primary | 3 nodes | Reduced replica set |
| DR EKS | — | 1 cluster | 1 | Warm standby control plane |

## Sizing Assumptions

1. **200 TPS per vCPU** for payment processing workloads (industry benchmark for card authorization)
2. **1.5× safety factor** applied to peak TPS (500 → 750 design TPS) per sizing methodology
3. **3-AZ deployment** with minimum 2 instances per AZ for all critical services
4. **Multi-AZ** for all database and cache layers (PCI-DSS + 99.99% SLA)
5. **30% DR capacity** in ap-southeast-3 for warm standby (scales up on failover)
6. **EBS gp3** storage with 3,000 baseline IOPS (sufficient for most workloads; Transaction DB upgraded to 6,000)
7. **40% YoY growth** — Year 2 design TPS = 1,050; current sizing accommodates via horizontal pod scaling on EKS
8. **Average transaction payload ~2 KB** for network bandwidth calculations
9. Instance families match architecture design: c6i (compute-optimized) for auth/API, m6i (general purpose) for services, r6g (memory-optimized) for databases and cache
