---
type: apv-skill
created: 2026-04-24
tags: [apv, skill, orchestrator, automation]
source: .claude/skills/apv
---

# APV Orchestrator

## Overview

Orchestrate the complete RFP response generation process by chaining all APV skills in sequence. Transforms raw RFP documents into compliant, accurate, professional responses.

## Purpose

- Chain all 6 generation skills in sequence
- Transform RFP documents into complete responses
- Enforce source URL compliance throughout
- 60-90 minute total execution time

## The 6-Skill Chain

```
RFP Document
     ↓
1. rfp-brainstorm → Analyze RFP, generate approach options
     ↓
2. rfp-compliance → Map requirements to regulations with source URLs
     ↓
3. rfp-architect → Design detailed architecture
     ↓
4. rfp-calculator → Calculate precise sizing
     ↓
5. rfp-pricer → Generate cost estimates with calculator URLs
     ↓
6. rfp-generator → Create comprehensive RFP response document
     ↓
7. apv-reviewer → Unified 15-minute approval verification
     ↓
RFP Response Document (Ready for Submission)
```

## When to Use

- When receiving a new RFP that requires a response
- When needing a complete RFP response with compliance verification
- When requiring fast turnaround with accuracy assurance

## Inputs

- **RFP Document**: Customer RFP (PDF, DOCX, or text)
- **Target Regions**: Countries (SG, MY, PH, ID, TH, TW, HK)
- **Card System Type**: issuing, acquiring, gateway, digital-wallet
- **Cloud Provider**: AWS, Azure, GCP, or best-fit

## Outputs

1. **Complete RFP Response Document**: Professional submission-ready document
2. **Compliance Matrix**: Full requirements-to-regulations mapping
3. **Architecture Diagrams**: System design with regional deployment
4. **Cost Breakdown**: Detailed pricing with source URLs
5. **Verification Report**: Unified review with approval status

## Success Metrics

- **Time Savings**: 60-90 minutes vs 2-3 weeks traditional
- **Accuracy**: >95% compliance accuracy, >98% pricing accuracy
- **Source URL Compliance**: 100% of claims cite sources
- **Review Time**: 15-minute unified review vs 150-minute 5-gate process

## Execution Time

| Skill | Estimated Time |
|-------|----------------|
| rfp-brainstorm | 5-10 minutes |
| rfp-compliance | 10-15 minutes |
| rfp-architect | 10-15 minutes |
| rfp-calculator | 5-10 minutes |
| rfp-pricer | 5-10 minutes |
| rfp-generator | 10-15 minutes |
| apv-reviewer | 15 minutes |
| **Total** | **~60-90 minutes** |

## Usage

### Basic
```bash
/apv rfp <path-to-rfp-document>
```

### With Parameters
```bash
/apv rfp <path-to-rfp> --regions SG,MY --type issuing --provider aws
```

### Interactive
```bash
/apv rfp <path-to-rfp> --interactive
```

## Output Files

```
apv-projects/[customer]--[rfp-title]--[date]/
├── input/
├── outputs/
│   ├── 01-brainstorm.md
│   ├── 02-compliance.md
│   ├── 03-architecture.md
│   ├── 04-sizing.md
│   ├── 05-pricing.md
│   ├── 06-response.md          (Main deliverable)
│   └── 07-approval.md
├── evidence/
└── approvals/
```

Use the canonical runtime contract in `docs/runtime-project-contract.md` for active APV runs.

## Related Skills

- [[rfp-brainstorm-skill]] - Initial analysis and approach
- [[rfp-compliance-skill]] - Requirements mapping
- [[rfp-architect-skill]] - Architecture design
- [[rfp-calculator-skill]] - Infrastructure sizing
- [[rfp-pricer-skill]] - Cost estimation
- [[rfp-generator-skill]] - Document generation
- [[apv-reviewer-skill]] - Unified approval
