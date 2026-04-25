---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, brainstorming]
source: .claude/skills/rfp-brainstorm
---

# rfp-brainstorm Skill

## Overview

Generate comprehensive brainstorming content for RFP responses by leveraging APV knowledge base. First skill in the 6-skill chain.

## Purpose

Sets the strategic direction for the entire RFP response by:
- Analyzing RFP requirements
- Generating approach options
- Identifying compliance requirements
- Determining regional deployment strategies

## When to Use

- At the start of any new RFP response
- When exploring multiple solution approaches
- When identifying key compliance requirements
- When determining regional deployment strategies

## Inputs

```
RFP Document (PDF, DOCX, or text)
Region: [SG | MY | PH | ID | TH | TW | HK | multiple]
Card Types: [issuing | acquiring | gateway | digital-wallet | multiple]
```

## Outputs

1. **Executive Summary Brainstorm**: Key value propositions and differentiators
2. **Compliance Landscape**: All applicable regulations and standards
3. **Architecture Options**: Multiple valid approaches with trade-offs
4. **Regional Considerations**: Country-specific requirements and constraints
5. **Risk Mitigation Strategies**: Known risks and proven mitigations
6. **Questions for Clarification**: Items requiring customer input

## Knowledge Sources

- `wiki/apv/knowledge/compliance/` - All compliance requirements
- `wiki/apv/knowledge/card-systems/` - Card system architectures
- `wiki/apv/knowledge/infrastructure/` - Cloud service patterns
- `wiki/apv/knowledge/sizing/` - TPS sizing methodology
- `wiki/apv/templates/` - RFP response templates

## Process

### 1. Analyze RFP Requirements

Extract key requirements:
- Business type (issuing, acquiring, gateway, wallet)
- Target regions (countries)
- Transaction volume estimates
- Compliance requirements
- Technical constraints

### 2. Map to APV Knowledge

Query wiki for:
- Applicable compliance regulations (PCI-DSS + country-specific)
- Relevant card system patterns
- Cloud service availability in target regions
- Similar past RFP patterns (if available)

### 3. Generate Approach Options

Present 2-3 valid architectural approaches:
- Approach A: Cloud-native (EKS/AKS/GKE)
- Approach B: Container-based (ECS/Cloud Run)
- Approach C: Hybrid/edge (if connectivity constraints)

### 4. Identify Knowledge Gaps

Flag requirements not covered in wiki

### 5. Generate Clarification Questions

List questions that would improve response quality

## Usage

```
/skill rfp-brainstorm --rfp <path-to-rfp> --region <code> --type <card-type>
```

Or in chain mode:
```
/apv rfp <path-to-rfp>
```

## Integration

Outputs to:
- [[rfp-compliance-skill]] - Detailed compliance requirements matrix
- [[rfp-architect-skill]] - Architecture design based on selected approach
- [[rfp-calculator-skill]] - Precise sizing based on selected architecture

## Related

- [[rfp-compliance-skill]] - Detailed compliance analysis
- [[rfp-architect-skill]] - Architecture design
- [[apv-orchestrator-skill]] - Complete APV skill chain
