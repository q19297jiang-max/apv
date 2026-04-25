---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, rfp, generator]
source: .claude/skills/rfp-generator
---

# rfp-generator Skill

## Overview

Synthesize outputs from all previous skills into a comprehensive, professional RFP response document. Enforces source URL compliance for all claims throughout the document.

## Purpose

- Create comprehensive RFP response document
- Synthesize all skill outputs
- Enforce source URL citations throughout
- Generate complete appendix with source URL index

## When to Use

- After all other skills have completed their analysis
- When generating the final RFP response document
- When creating proposal summaries for management review

## Inputs

Receives from all previous skills:
- [[rfp-brainstorm-skill]]: Executive summary, approach options, questions
- [[rfp-compliance-skill]]: Compliance mapping, requirements matrix
- [[rfp-architect-skill]]: Architecture design, component specifications
- [[rfp-calculator-skill]]: Infrastructure sizing, capacity planning
- [[rfp-pricer-skill]]: Cost estimation, pricing evidence

## Outputs

1. **Executive Summary**: High-level overview with key differentiators
2. **Technical Solution**: Detailed architecture and implementation approach
3. **Compliance Response**: Complete compliance matrix with evidence
4. **Implementation Plan**: Timeline, milestones, and deliverables
5. **Pricing Proposal**: Cost breakdown with evidence
6. **Appendices**: Supporting documentation and source URLs

## Document Structure

1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Technical Architecture
5. Compliance Response
6. Implementation Plan
7. Pricing
8. Assumptions and Qualifications
9. Appendices (including Source URL Index)

## Knowledge Sources

- `wiki/apv/templates/` - RFP response templates
- All APV knowledge files for source citations

## Source URL Enforcement

**CRITICAL**: ALL claims must have source citations:
- Compliance claims cite regulation files with source URLs
- Pricing claims cite calculator URLs with verification date
- Architecture claims cite vendor documentation URLs

## Accuracy Assurance

Document includes accuracy assurance statement:
- ✅ All compliance claims cite source URLs
- ✅ All pricing claims cite official calculator URLs
- ✅ All architecture claims cite vendor documentation
- ✅ All source URLs verified within freshness thresholds
- ✅ Evidence artifacts stored in wiki/apv/knowledge/evidence/

## Usage

```
/skill rfp-generator --rfp <path> --output <output-file>
```

## Integration

Receives from:
- ALL previous generation skills

Sends to:
- [[apv-reviewer-skill]] - For final approval verification

## Related

- [[apv-reviewer-skill]] - Final approval verification
- [[apv-orchestrator-skill]] - Complete skill chain
