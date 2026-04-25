---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, compliance]
source: .claude/skills/rfp-compliance
---

# rfp-compliance Skill

## Overview

Perform detailed compliance analysis for RFP responses by mapping all requirements to applicable regulations and standards. Enforces 100% source URL compliance for all claims.

## Purpose

- Map RFP requirements to PCI-DSS requirements
- Map RFP requirements to country-specific regulations
- Generate compliance matrix with source URLs for every claim
- Identify gaps and certification requirements
- Specify evidence artifacts needed

## When to Use

- After [[rfp-brainstorm-skill]] has identified the approach
- When generating detailed compliance matrices
- When validating that all requirements have compliance coverage
- Before architecture design to ensure compliance constraints are known

## Inputs

Receives from [[rfp-brainstorm-skill]]:
- RFP requirements analysis
- Selected architecture approach
- Target regions
- Card system types

## Outputs

1. **Requirements-to-Compliance Mapping**: Each requirement mapped to specific regulations
2. **Compliance Matrix**: Detailed matrix with source URLs for every claim
3. **Gaps Analysis**: Requirements without clear compliance guidance
4. **Certification Requirements**: Required certifications and timelines
5. **Evidence Requirements**: What evidence artifacts are needed

## Knowledge Sources

- `wiki/apv/knowledge/compliance/pci-dss/` - All 12 PCI-DSS requirements
- `wiki/apv/knowledge/compliance/countries/` - All country regulations
- `wiki/apv/templates/compliance-matrix.md` - Template structure

## Source URL Enforcement

**CRITICAL**: ALL compliance claims MUST have source URLs:
- PCI-DSS: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf
- Country regulations: Official regulator URLs from frontmatter

## Usage

```
/skill rfp-compliance --rfp <path> --regions SG,MY
```

## Integration

Receives from:
- [[rfp-brainstorm-skill]] - Requirements analysis

Sends to:
- [[rfp-architect-skill]] - Compliance constraints for architecture design

## Related

- [[rfp-brainstorm-skill]] - Initial requirements analysis
- [[rfp-architect-skill]] - Architecture design with compliance
- [[apv-orchestrator-skill]] - Complete skill chain
