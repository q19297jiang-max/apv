---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, sizing, calculator]
source: .claude/skills/rfp-calculator
---

# rfp-calculator Skill

## Overview

Perform precise infrastructure sizing calculations for RFP responses based on transaction volume requirements and architecture design.

## Purpose

- Calculate TPS requirements (peak and average)
- Size components (instance types, counts)
- Plan capacity and scaling
- Define performance metrics

## When to Use

- After [[rfp-architect-skill]] has defined the architecture
- When calculating TPS capacity requirements
- When sizing compute, database, and storage components
- When planning for growth and scaling thresholds

## Inputs

Receives from previous skills:
- [[rfp-architect-skill]]: Component list, architecture design, target regions
- RFP Document: Transaction volume requirements, growth projections

## Outputs

1. **TPS Analysis**: Peak and average TPS calculations
2. **Component Sizing**: Instance types, counts, and configurations
3. **Capacity Plan**: Current and future capacity requirements
4. **Scaling Strategy**: Auto-scaling rules and thresholds
5. **Resource Summary**: Total resources by region and component
6. **Performance Metrics**: Expected latency, throughput, headroom

## Knowledge Sources

- `wiki/apv/knowledge/sizing/tps-calculator.md` - TPS calculation methodology
- `wiki/apv/knowledge/infrastructure/` - Instance specifications and capabilities

## TPS Calculation Formula

```
Peak TPS = (Daily Transactions × Peak Multiplier) / (Seconds in Peak Period)

Where:
- Daily Transactions: From RFP requirements
- Peak Multiplier: Typically 3-5x average (industry standard)
- Peak Period: Typically 4 hours (14,400 seconds)
```

## Instance Sizing Reference

| Component | TPS per Instance | Instance Type | Source |
|-----------|------------------|---------------|--------|
| API Gateway | 500-1000 TPS | c5.large/c5.xlarge | [[tps-calculator]] |
| Application | 200-500 TPS | c5.xlarge/c5.2xlarge | [[tps-calculator]] |
| Database (Write) | 1000-5000 TPS | db.r5.large/db.r5.xlarge | [[tps-calculator]] |
| Database (Read) | 5000-10000 TPS | db.r5.2xlarge/read replica | [[tps-calculator]] |

## Usage

```
/skill rfp-calculator --rfp <path> --tps <peak-tps>
```

## Integration

Receives from:
- [[rfp-architect-skill]] - Architecture design

Sends to:
- [[rfp-pricer-skill]] - Component sizing for cost calculation

## Related

- [[rfp-architect-skill]] - Architecture design
- [[rfp-pricer-skill]] - Cost estimation
- [[apv-orchestrator-skill]] - Complete skill chain
