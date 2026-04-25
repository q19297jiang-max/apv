---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, architecture]
source: .claude/skills/rfp-architect
---

# rfp-architect Skill

## Overview

Design detailed payment system architecture for RFP responses, incorporating compliance constraints, regional requirements, and card system patterns.

## Purpose

- Design architecture based on selected approach
- Specify components for each region
- Design security and HA/DR
- Generate component specifications

## When to Use

- After [[rfp-compliance-skill]] has identified all requirements
- When designing multi-region payment systems
- When specifying cloud infrastructure components
- When defining data flows and security boundaries

## Inputs

Receives from previous skills:
- [[rfp-brainstorm-skill]]: Selected architecture approach, target regions
- [[rfp-compliance-skill]]: Compliance constraints, data residency requirements
- RFP Document: Technical requirements, volume estimates, integration needs

## Outputs

1. **Architecture Overview**: High-level system design with component diagram
2. **Regional Architecture**: Deployment strategy for each target country
3. **Component Specifications**: Detailed specs for each component
4. **Data Flow Diagrams**: Transaction flows with security boundaries
5. **Infrastructure Selection**: Specific cloud services with justifications
6. **Security Architecture**: Network security, encryption, access control

## Knowledge Sources

- `wiki/apv/knowledge/card-systems/` - Card system architecture patterns
- `wiki/apv/knowledge/infrastructure/` - Cloud service specifications
- `wiki/apv/knowledge/compliance/` - Compliance constraints

## Architecture Patterns

| Card Type | Pattern | TPS Profile | Key Components |
|-----------|---------|-------------|----------------|
| Issuing | [[issuing]] | Medium (100-1000 TPS) | Core banking, card management, PIN |
| Acquiring | [[acquiring]] | High (1000-5000 TPS) | Terminal management, switching, settlement |
| Gateway | [[gateway]] | Very High (5000-10000 TPS) | API gateway, routing, orchestration, 3DS |
| Digital Wallet | [[digital-wallet]] | Medium (500-2000 TPS) | Wallet backend, provisioning, tokenization |

## Usage

```
/skill rfp-architect --rfp <path> --type <card-type> --regions SG,MY
```

## Integration

Receives from:
- [[rfp-brainstorm-skill]] - Architecture approach
- [[rfp-compliance-skill]] - Compliance constraints

Sends to:
- [[rfp-calculator-skill]] - Component list for sizing

## Related

- [[rfp-compliance-skill]] - Compliance requirements
- [[rfp-calculator-skill]] - Infrastructure sizing
- [[apv-orchestrator-skill]] - Complete skill chain
