---
type: working
stage: 4
created: '2026-05-01'
---

# Sizing Calculation Worksheet — ACME Payments

## Step 1: Volume Decomposition

```
Monthly Txns:     50,000,000
Seconds/month:    30 × 24 × 3600 = 2,592,000
Average TPS:      50,000,000 ÷ 2,592,000 = 19.3 TPS

Peak TPS (customer):  500 TPS
Safety factor:        1.5×
Design TPS:           500 × 1.5 = 750 TPS

Burst ceiling:        500 × 3.0 = 1,500 TPS (festive peak)
```

## Step 2: Compute Sizing

### Authorization Engine (hot path)
```
Design TPS:           750
TPS per vCPU:         200 (payment auth benchmark)
Min vCPU required:    750 ÷ 200 = 3.75 → 4 vCPU
Instance choice:      c6i.2xlarge (8 vCPU, 16 GiB) — compute-optimized for crypto ops
Per-AZ count:         2 (N+1 redundancy within AZ)
Total instances:      2 × 3 AZ = 6
Total vCPU:           6 × 8 = 48 vCPU
Headroom:             48 × 200 = 9,600 TPS capacity (12.8× design TPS)
Rationale:            High headroom justified by PCI-DSS 99.99% SLA + burst to 1,500 TPS
```

### API Gateway Service
```
Design TPS:           750 (all traffic passes through)
Instance choice:      c6i.xlarge (4 vCPU, 8 GiB) — lightweight routing
Per-AZ count:         2
Total instances:      2 × 3 = 6
Total vCPU:           6 × 4 = 24
```

### Tokenization Service (CDE)
```
Design TPS:           ~750 (every auth needs token lookup)
Instance choice:      m6i.xlarge (4 vCPU, 16 GiB) — needs memory for token cache
Per-AZ count:         2
Total instances:      2 × 3 = 6
Total vCPU:           6 × 4 = 24
```

### 3DS Server (non-CDE)
```
3DS rate:             ~60% of txns require 3DS check
Effective TPS:        750 × 0.6 = 450 TPS
Instance choice:      m6i.xlarge (4 vCPU, 16 GiB)
Total instances:      4
Total vCPU:           4 × 4 = 16
```

### Fraud Scoring (CDE)
```
Fraud check rate:     100% of auth requests
Design TPS:           750
Instance choice:      m6i.xlarge (4 vCPU, 16 GiB)
Total instances:      4
Total vCPU:           4 × 4 = 16
```

### Settlement Engine (non-CDE, batch)
```
Batch workload:       T+1 settlement, ~55,000 merchants
Instance choice:      m6i.large (2 vCPU, 8 GiB)
Total instances:      3 (1 per AZ)
Total vCPU:           3 × 2 = 6
```

### Merchant Portal (non-CDE)
```
Concurrent users:     ~200 merchants
Instance choice:      m6i.large (2 vCPU, 8 GiB)
Total instances:      3 (1 per AZ)
Total vCPU:           3 × 2 = 6
```

### Card Network Connector (CDE)
```
Networks:             4 (Visa, MC, AMEX, JCB)
Instance choice:      m6i.xlarge (4 vCPU, 16 GiB)
Total instances:      4 (1 per network + shared spare)
Total vCPU:           4 × 4 = 16
```

## Step 3: Database Sizing

### Transaction DB (Aurora PostgreSQL Multi-AZ)
```
Write TPS:            750 (all auth writes)
Read TPS:             ~2,000 (settlement queries, dashboards)
Row size:             ~1 KB
Daily storage:        50M/30 × 1KB = 1.67M KB = ~1.6 GB/day
Annual storage:       1.6 × 365 = 584 GB → 500 GB initial (7-year retained)
Instance:             db.r6g.2xlarge (8 vCPU, 64 GiB) — memory-optimized for OLTP
IOPS:                 6,000 (gp3 upgrade from 3,000 baseline)
```

### Token Vault DB (Aurora PostgreSQL Multi-AZ, CDE)
```
Unique tokens:        ~10M cards (growing)
Row size:             ~256 bytes (token + encrypted PAN reference)
Storage:              10M × 256B = 2.56 GB → 200 GB with growth
Instance:             db.r6g.xlarge (4 vCPU, 32 GiB)
IOPS:                 3,000 (gp3 baseline sufficient)
```

## Step 4: Cache Sizing

### ElastiCache Redis (Token Cache)
```
Hot tokens:           ~2M active cards
Per-token size:       ~512 bytes
Working set:          2M × 512B = 1 GB
Cluster mode:         3 shards × 2 replicas = 6 nodes
Instance:             cache.r6g.xlarge (4 vCPU, 32.3 GiB)
Total memory:         6 × 32.3 = 193.8 GiB (massive headroom for growth)
```

## Step 5: Network Bandwidth

```
TPS:                  750
Avg payload:          2 KB
Bandwidth:            750 × 2KB × 8 = 12 Mbps sustained
Peak (burst):         1500 × 2KB × 8 = 24 Mbps
ALB capacity:         Well within ALB limits
```

## Step 6: DR Sizing (Warm Standby, ap-southeast-3)

```
DR compute:           30% of primary = 0.3 × 36 = 10.8 → 12 nodes
DR EKS cluster:       1 control plane
DR database:          1× Aurora Global DB read replica (db.r6g.xlarge)
DR cache:             3 nodes (50% of primary)
```
