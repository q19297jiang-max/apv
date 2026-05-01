---
name: rfp-calculator
description: Stage 4 — Calculate infrastructure sizing from architecture components and volume data
version: 2.0
created: 2026-05-01
tags: [apv, v2, sizing, calculator, stage-4]
output_class: derived
---

# RFP Sizing Calculator (Stage 4)

## Purpose

Calculate infrastructure sizing for each architecture component based on transaction volumes, peak multipliers, and HA requirements. Produces explicit sizing records with traceable formulas.

**Output class: `derived`** — calculations traceable to architecture (Stage 3) and volume data.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 4`

Required:
- `outputs/03-architecture.md`
- `input/normalized/volume-summary.md`

## Process

### 1. Read Upstream Context
- `outputs/03-architecture.md` — component inventory, deployment model
- `input/normalized/volume-summary.md` — monthly transactions, average value, peak multiplier

### 2. Calculate Base TPS
```
Monthly transactions ÷ (30 days × 24 hours × 3600 seconds) = base TPS
Peak TPS = base TPS × peak multiplier
Design TPS = peak TPS × safety factor (1.5)
```

### 3. Size Each Component
For each component from architecture:

**Compute:**
- vCPU = ceil(design_TPS ÷ TPS_per_core)
- Instance type = smallest instance ≥ required vCPU + memory
- Instance count = ceil(total_vCPU ÷ instance_vCPU) × HA_factor

**Database:**
- IOPS = design_TPS × reads_per_tx + writes_per_tx
- Storage = monthly_tx × avg_record_size × retention_months
- Instance = smallest RDS class supporting required IOPS

**Network:**
- Bandwidth = design_TPS × avg_payload_size
- NAT gateway throughput
- Load balancer capacity

### 4. Apply HA/DR Multipliers
- Multi-AZ: ×2 for stateful, ×1 for stateless (auto-distributed)
- Cross-region DR: additional standby instances
- Document: which components are HA and why

### 5. Document Assumptions
Every sizing decision must state:
- The formula used
- Input values and their source
- Any assumptions made (e.g., "200 TPS per core for Java payment processing")

## Outputs

### Primary Output: `outputs/04-sizing.md`
```markdown
---
output_class: derived
stage: 4
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
---

# Infrastructure Sizing: [Customer]

## Volume Analysis
| Metric | Value | Source |
|--------|-------|--------|
| Monthly transactions | [N] | volume-summary.md |
| Base TPS | [N] | calculated |
| Peak TPS | [N] | base × [multiplier] |
| Design TPS | [N] | peak × 1.5 safety |

## Component Sizing

### Compute
| Component | Instance | Count | vCPU | RAM | Justification |
|-----------|----------|-------|------|-----|---------------|
| App servers | m6i.xlarge | 4 | 16 | 64 GiB | [design_TPS] ÷ [TPS/core] |

### Database
| Component | Instance | Storage | IOPS | Justification |
|-----------|----------|---------|------|---------------|
| Primary DB | db.r6g.xlarge | 500 GiB | [N] | [formula] |

### Network
| Component | Capacity | Justification |
|-----------|----------|---------------|
| ALB | [N] req/s | [design_TPS] |

## HA/DR Impact
| Component | Base Count | HA Factor | Final Count | Reason |
|-----------|------------|-----------|-------------|--------|
| App servers | 2 | ×2 (Multi-AZ) | 4 | PCI-DSS availability |

## Sizing Assumptions
1. [Assumption] — source: [knowledge page or industry standard]
```

### Working Artifact: `working/04-sizing-record.md`
Detailed calculation worksheet with all intermediate values.

## Knowledge Sources

- `knowledge/sizing/tps-calculator.md` — TPS methodology and reference benchmarks
- `knowledge/infrastructure/` — instance capabilities and limits

## Integration

- **Upstream**: `rfp-architect` (Stage 3) provides component list
- **Downstream**: `rfp-pricer` (Stage 5) prices the sized components
