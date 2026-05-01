---
name: rfp-architect
description: Stage 3 — Design payment infrastructure architecture based on requirements and compliance constraints
version: 2.0
created: 2026-05-01
tags: [apv, v2, architecture, stage-3]
output_class: derived
---

# RFP Architecture Design (Stage 3)

## Purpose

Design the payment infrastructure architecture informed by brainstorm strategy (Stage 1) and compliance constraints (Stage 2). Produces architecture decisions with explicit rationale traceable to upstream outputs.

**Output class: `derived`** — conclusions traceable to evidence-backed inputs from Stages 1-2.

## Gate Check

Run: `python3 tools/validate_gates.py --project [PROJECT] --stage 3`

Required:
- `outputs/01-brainstorm.md`
- `outputs/02-compliance.md`

## Process

### 1. Read Upstream Context
- `outputs/01-brainstorm.md` — strategic direction, business type, regions, scale
- `outputs/02-compliance.md` — compliance constraints, required security controls

### 2. Determine Architecture Drivers
- **Scale**: peak TPS → compute/network sizing class
- **Compliance**: PCI-DSS scope → network segmentation, encryption, access control
- **Regions**: multi-region → DR strategy, data residency
- **Business type**: issuing/acquiring/gateway → specific component needs

### 3. Design Architecture Components
For each major component:
1. Select cloud services from `knowledge/infrastructure/`
2. Define deployment pattern (HA, multi-AZ, cross-region)
3. Document why this choice satisfies compliance requirements
4. Note alternatives considered and why rejected

### 4. Architecture Decision Records
For each significant decision:
- **Context**: what problem we're solving
- **Decision**: what we chose
- **Rationale**: why (linked to compliance/requirements)
- **Consequences**: trade-offs accepted

### 5. Generate Component Inventory
List all infrastructure components for downstream sizing (Stage 4) and pricing (Stage 5).

## Outputs

### Primary Output: `outputs/03-architecture.md`
```markdown
---
output_class: derived
stage: 3
snapshot_sha: [from knowledge snapshot]
created: YYYY-MM-DD
---

# Architecture Design: [Customer]

## Overview
[2-3 paragraph architecture summary]

## Architecture Diagram (Text)
[ASCII/mermaid diagram of major components and data flow]

## Components

### Compute
| Component | Service | Config | Purpose | Compliance |
|-----------|---------|--------|---------|------------|
| App servers | ECS/EKS | [spec] | Transaction processing | PCI-DSS Req 1 |
| ...

### Data
| Component | Service | Config | Purpose | Compliance |
|-----------|---------|--------|---------|------------|
| Primary DB | RDS PostgreSQL | Multi-AZ | Transaction storage | PCI-DSS Req 3 |
| ...

### Network & Security
[Network segmentation, encryption, access control]

### Monitoring & Operations
[Logging, alerting, DR strategy]

## Architecture Decisions
### ADR-1: [Decision Title]
- **Context**: [problem]
- **Decision**: [choice]
- **Rationale**: [why, linked to Stage 1/2 outputs]
- **Consequences**: [trade-offs]

## Component Inventory for Sizing
[Summary list for Stage 4 consumption]
```

### Working Artifact: `working/03-architecture-decision-log.md`
Complete ADR log with all alternatives considered.

## Knowledge Sources

- `knowledge/infrastructure/aws/*.md` — AWS service patterns
- `knowledge/infrastructure/azure/*.md` — Azure service patterns
- `knowledge/infrastructure/gcp/*.md` — GCP service patterns
- `knowledge/card-systems/*.md` — payment system architectures
- `knowledge/patterns/*.md` — reference architectures (when populated)

## Integration

- **Upstream**: `rfp-brainstorm` (Stage 1), `rfp-compliance` (Stage 2)
- **Downstream**: `rfp-calculator` (Stage 4) sizes components, `rfp-pricer` (Stage 5) prices them
