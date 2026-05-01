---
type: working
stage: 1
created: '2026-05-01'
---

# Stage 1 Brainstorm — Internal Context Notes

## Pipeline Context
- **Project:** ACME Payments Payment Gateway
- **Stage:** 1 — Brainstorm (exploratory)
- **Run type:** Dry run
- **Date:** 2026-05-01

## Key Sizing Parameters for Downstream Stages

- **Steady-state TPS:** 50M txns/month ÷ 30 days ÷ 86400 sec ≈ **19 TPS average**
- **Peak TPS (stated):** 500 TPS
- **Peak TPS (calculated):** 19 × 3x peak × ~8.8 peak-hour factor ≈ 500 TPS (consistent)
- **Y2 peak TPS:** 500 × 1.4 = 700 TPS
- **Y3 peak TPS:** 700 × 1.4 = 980 TPS → design for **~1000 TPS** at 3-year horizon
- **Storage estimate:** 50M txns × 2KB avg record ≈ 100GB/month raw transaction data ≈ 1.2TB/year

## Architecture Decision Records (Pre-decisions)

1. **EKS over ECS** — Kubernetes preferred for payment workloads: better multi-region portability, service mesh (Istio) for mTLS between services, mature PCI-DSS patterns.
2. **Aurora PostgreSQL over standard RDS** — Better Multi-AZ failover, read replicas for reporting, compatible with cross-region replication.
3. **ElastiCache Redis over Memcached** — Persistence needed for tokenization cache, supports cluster mode for scaling.
4. **CloudHSM over KMS** — PCI-DSS v4.0 Level 1 typically requires FIPS 140-2 Level 3 HSM for key management. CloudHSM satisfies this; KMS is Level 2.

## Compliance Complexity Assessment

| Market | Complexity | Key Regulations | Data Residency |
|--------|-----------|-----------------|----------------|
| Singapore | High | MAS TRM, PSA, PDPA, CSA | No strict residency |
| Malaysia | Medium | BNM RMiT, PDPA, PSA | Partial |
| Philippines | Medium | BSP Circular, PDPA | Limited |
| Indonesia (Ph2) | High | BI Regulations, explicit data residency | **Strict** |
| Thailand (Ph2) | Medium | BOT, PDPA | Partial |

## Pricing Strategy Notes

- AWS pricing verified 2026-04-28, valid until 2026-05-28 — **within validity window**
- Lead with 3-year Savings Plans for compute (36-40% discount range)
- Multi-AZ RDS cost is ~2x single-AZ — significant line item
- CloudHSM is expensive (~$1.50/hr per HSM, need min 2 for HA) ≈ $2,200/month
- Consider Reserved Instances for steady-state, on-demand for burst capacity

## Risk Register (Initial)

| Risk | Impact | Mitigation |
|------|--------|------------|
| 5-month implementation timeline is aggressive | High | Phased go-live: core gateway first, then issuing, then wallets |
| 40% YoY growth requires frequent scaling | Medium | Auto-scaling design, quarterly capacity reviews |
| Multi-country compliance complexity | High | Country-specific compliance modules, dedicated compliance workstream |
| Data residency for Phase 2 Indonesia | Medium | Design multi-region data isolation from Phase 1 |
| PCI-DSS v4.0 is relatively new | Medium | Use knowledge base Req 1-12 files, reference QSA early |

## Downstream Stage Inputs

- **Stage 2 (Compliance):** Use SG, MY, PH country files + PCI-DSS Req 1-12. Flag data residency for Phase 2.
- **Stage 3 (Architecture):** EKS Multi-AZ, Aurora, ElastiCache, CloudHSM. Design for 1000 TPS at 3-year horizon.
- **Stage 4 (Sizing):** Use tps-calculator.md methodology. Size for 500 TPS peak Y1, 1000 TPS Y3.
- **Stage 5 (Pricing):** Use aws.md and aws-component-catalog.md. Savings Plans for compute, RI for RDS.
- **Stage 6 (Response):** Lead with architecture (30% weight) and compliance (25% weight).
