---
type: apv-knowledge
category: pricing
title: "GCP Pricing for Asia"
source_url: "https://cloud.google.com/products/calculator"
source_document: "Google Cloud Pricing Documentation"
captured_date: 2026-04-24
verified_by: "Infrastructure Architect"
price_valid_until: 2026-05-24
tags: [pricing, gcp, asia]
---

# GCP Pricing for Card Processing (Asia)

This file is currently a reference pricing snapshot, not a fully workflow-backed pricing path on par with the AWS catalog process.

## Official Calculators

| Calculator | URL | Last Updated |
|------------|-----|-------------|
| GCP Pricing Calculator | https://cloud.google.com/products/calculator | 2026-04-24 |
| Compute Engine Pricing | https://cloud.google.com/compute/pricing | 2026-04-24 |
| Cloud SQL Pricing | https://cloud.google.com/sql/pricing | 2026-04-24 |

## Regional Pricing (asia-southeast1)

### Compute Engine
**Source**: https://cloud.google.com/compute/pricing (asia-southeast1)

| Machine | vCPU | Memory | Price/Hour | Monthly (730h) | Calculator URL |
|---------|------|--------|------------|---------------|----------------|
| e2-highmem-4 | 4 | 32 GiB | $0.268 | $195.64 | https://cloud.google.com/products/calculator |
| c2-standard-8 | 8 | 32 GiB | $0.472 | $344.56 | https://cloud.google.com/products/calculator |

### GKE Pricing
**Source**: https://cloud.google.com/kubernetes-engine/pricing

| Component | Price | Calculator URL |
|-----------|-------|----------------|
| GKE Management | Free (zonal) | https://cloud.google.com/products/calculator |
| GKE Management | $0.10/hour (regional) | https://cloud.google.com/products/calculator |
| VMs | Per VM | https://cloud.google.com/products/calculator |

### Cloud SQL Pricing
**Source**: https://cloud.google.com/sql/pricing (asia-southeast1)

| Tier | vCPU | Price/Hour | Calculator URL |
|------|------|------------|----------------|
| 2nd Gen | 4 | $0.650 | https://cloud.google.com/products/calculator |

## Related Pricing Sources
- [[gcp-compute-engine-pricing]] — Compute Engine pricing

## Evidence Storage
- `wiki/apv/knowledge/evidence/pricing/2026-04-24/`

## Readiness Note

- Use this page as a quick reference during architecture and rough-order pricing.
- Treat final GCP proposal pricing as requiring manual calculator confirmation and fresh evidence capture for the specific RFP.

## Related
- [[pricing-aws]] — AWS pricing
- [[pricing-azure]] — Azure pricing
