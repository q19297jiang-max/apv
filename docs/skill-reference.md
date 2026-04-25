---
type: apv-meta
category: documentation
title: "APV Skill Reference Guide"
created: 2026-04-24
tags: [apv, documentation, skills, reference]
sources:
  - "[[apv-user-guide]]"
---

# APV Skill Reference Guide

Quick reference for all 7 APV skills.

---

## Skill Summary

| # | Skill | Purpose | Time | Input | Output |
|---|-------|---------|------|-------|--------|
| 1 | rfp-brainstorm | Generate approach options | 5-10 min | RFP | Brainstorm analysis |
| 2 | rfp-compliance | Map to regulations with URLs | 10-15 min | RFP + brainstorm | Compliance matrix |
| 3 | rfp-architect | Design architecture | 10-15 min | RFP + compliance | Architecture design |
| 4 | rfp-calculator | Calculate sizing | 5-10 min | RFP + architecture | Sizing calculations |
| 5 | rfp-pricer | Generate pricing with URLs | 5-10 min | RFP + calculator | Cost breakdown |
| 6 | rfp-generator | Create RFP response | 10-15 min | All previous | Final response |
| 7 | apv-reviewer | Approve/verify | 15 min | Final response | Approval decision |

**Total Chain Time**: 60-90 minutes

---

## Skill 1: rfp-brainstorm

### Command
```bash
/skill rfp-brainstorm --rfp <path-to-rfp>
```

### Purpose
Generate strategic approach options for RFP response.

### Input Requirements
- RFP document (any format)
- Target regions (optional, will detect)
- Card types (optional, will detect)

### Output Sections
1. Executive Summary Points (3-5 key differentiators)
2. Compliance Landscape (PCI-DSS + country regulations)
3. Architecture Options (2-3 approaches with trade-offs)
4. Regional Considerations (cloud regions, data residency)
5. Risk Mitigation Strategies
6. Questions for Customer (5-10 clarifying questions)
7. Knowledge Gaps (explicitly stated)
8. Recommended Approach

### When to Use
- Starting any new RFP
- Exploring multiple solution approaches
- Need high-level strategic direction

### Key Outputs
- **Recommended Approach**: Which architecture option to use
- **Compliance Requirements**: What regulations apply
- **Knowledge Gaps**: What information is missing

### Wiki References
- [[pci-dss-overview]] - PCI-DSS requirements
- Country regulations: [[mas-trm]], [[bnm-rm]], etc.
- [[issuing]], [[acquiring]], [[gateway]] - Card system patterns

---

## Skill 2: rfp-compliance

### Command
```bash
/skill rfp-compliance --rfp <path-to-rfp>
```

### Purpose
Map all RFP requirements to applicable regulations with source URL enforcement.

### Input Requirements
- RFP document
- Brainstorm output (recommended)

### Output Sections
1. Executive Summary (compliance coverage %)
2. PCI-DSS Requirements Mapping (12 requirements)
3. Country-Specific Regulations (by target country)
4. Detailed Compliance Matrix (per requirement)
5. Gaps Analysis
6. Certification Requirements
7. Evidence Artifacts Checklist
8. Compliance Status Summary

### Source URL Enforcement
**CRITICAL**: 100% of compliance claims must have source URLs
- PCI-DSS: https://www.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf
- Country regulations: Official government/regulator URLs
- Evidence locations specified

### When to Use
- Need detailed compliance requirements matrix
- Must cite official sources for all claims
- Preparing for compliance review

### Key Outputs
- **Compliance Matrix**: Every requirement mapped to regulation
- **Source URLs**: All claims backed by official sources
- **Evidence List**: What artifacts prove compliance

### Wiki References
- [[pci-dss-overview]] - PCI-DSS framework
- [[pci-dss-req-1]] through [[pci-dss-req-12]] - All 12 requirements
- Country files: `wiki/apv/knowledge/compliance/countries/`

---

## Skill 3: rfp-architect

### Command
```bash
/skill rfp-architect --rfp <path-to-rfp>
```

### Purpose
Design detailed payment system architecture.

### Input Requirements
- RFP document
- Compliance output (recommended)

### Output Sections
1. Architecture Overview (system type, regions, pattern)
2. Component Specifications (compute, data, network, security)
3. Regional Architecture (by target country)
4. Data Flow (transaction flows with security)
5. Infrastructure Selection Matrix (AWS vs Azure vs GCP)
6. Security Architecture (network, encryption, access, logging)
7. Disaster Recovery (backup, failover)
8. Capacity Planning (TPS capacity, instance sizing)

### Architecture Patterns
| Card Type | Pattern | Wiki Reference |
|-----------|---------|----------------|
| Issuing | Card issuing platform | [[issuing]] |
| Acquiring | Merchant acquiring | [[acquiring]] |
| Gateway | Payment gateway | [[gateway]] |

### When to Use
- Need technical architecture design
- Must specify components and configurations
- Preparing for technical review

### Key Outputs
- **Architecture Diagram**: Component relationships
- **Component Specs**: Instance types, sizing, configuration
- **Security Mapping**: Controls to PCI-DSS requirements

### Wiki References
- [[issuing]] - Issuing platform architecture
- [[aws-eks]], [[azure-aks]], [[gcp-gke]] - Container orchestration
- [[aws-rds]], [[azure-db]], [[gcp-cloudsql]] - Databases

---

## Skill 4: rfp-calculator

### Command
```bash
/skill rfp-calculator --rfp <path-to-rfp>
```

### Purpose
Calculate precise infrastructure sizing from transaction volumes.

### Input Requirements
- RFP document with transaction volumes
- Architecture output (recommended)

### Output Sections
1. TPS Analysis (average, peak, by type, by region)
2. Component Sizing (instance selection, count, capacity)
3. Capacity Planning (current + growth projections)
4. Scaling Strategy (auto-scaling configuration)
5. Performance Expectations (latency, throughput)
6. Resource Summary (by component, by region)

### Key Formulas
```
Average TPS = Daily Transactions / 86,400
Peak TPS = Average TPS × 4 (default multiplier)
Min Instances = (Average TPS / TPS per Instance) + 1
Max Instances = (Peak TPS × 1.5) / TPS per Instance
```

### Instance Capacity Reference
| Component | TPS per Instance | Recommended Instance |
|-----------|------------------|-------------------|
| API Gateway | 500-1000 TPS | c5.xlarge |
| Application | 200-500 TPS | c5.2xlarge |
| DB Write | 1000-5000 TPS | db.r5.xlarge |
| DB Read | 5000-10000 TPS | db.r5.2xlarge |

### When to Use
- Need to size infrastructure for TPS requirements
- Planning capacity for growth
- Calculating auto-scaling thresholds

### Key Outputs
- **Instance Counts**: Min/max instances per component
- **TPS Capacity**: Current and projected capacity
- **Headroom**: Growth capacity planned

### Wiki References
- [[tps-calculator]] - TPS calculation methodology
- [[aws-eks]], [[azure-aks]], [[gcp-gke]] - Container services

---

## Skill 5: rfp-pricer

### Command
```bash
/skill rfp-pricer --rfp <path-to-rfp>
```

### Purpose
Generate cost estimates with official calculator URLs.

### Input Requirements
- RFP document
- Calculator output (sizing)

### Output Sections
1. Executive Summary (monthly, annual, 3-year totals)
2. Detailed Cost Breakdown (compute, database, storage, transfer)
3. Cost Breakdown by Region
4. Cost Optimization Opportunities (reserved instances)
5. Pricing Evidence (calculator screenshots, verification)
6. Pricing Assumptions

### Source URL Enforcement
**CRITICAL**: 100% of pricing claims must cite calculator URLs
- AWS: https://calculator.aws/
- Azure: https://azure.microsoft.com/pricing/
- GCP: https://cloud.google.com/products/calculator

### Regional Multipliers (AWS)
| Country | Region | Multiplier |
|---------|--------|------------|
| Singapore | ap-southeast-1 | 1.0x |
| Malaysia | ap-southeast-3 | 1.1x |
| Thailand | ap-southeast-1 | 1.0x |
| Taiwan | ap-northeast-1 | 1.05x |
| Hong Kong | ap-east-1 | 1.1x |

### When to Use
- Need accurate cost estimates
- Must cite official pricing sources
- Comparing cloud provider options

### Key Outputs
- **Total Cost**: Monthly, annual, 3-year projections
- **Breakdown**: By component, by region
- **Optimization**: Reserved instance savings

### Wiki References
- [[aws-pricing]], [[azure-pricing]], [[gcp-pricing]] - Pricing files

---

## Skill 6: rfp-generator

### Command
```bash
/skill rfp-generator --rfp <path-to-rfp>
```

### Purpose
Synthesize all skill outputs into comprehensive RFP response document.

### Input Requirements
- All previous skill outputs (brainstorm, compliance, architect, calculator, pricer)

### Output Structure
1. Table of Contents
2. Executive Summary
3. Understanding of Requirements
4. Proposed Solution
5. Technical Architecture
6. Compliance Response (with matrices)
7. Implementation Plan
8. Pricing (with breakdown)
9. Assumptions and Qualifications
10. Appendices:
    - Appendix A: Source URL Index (MANDATORY)
    - Appendix B: Evidence Artifacts
    - Appendix C: Technical Specifications
    - Appendix D: Company Qualifications
    - Appendix E: Team Resumes

### Source URL Enforcement
**CRITICAL**: Appendix A must list ALL sources with URLs:
- PCI-DSS requirements with official PDF URLs
- Country regulations with official URLs
- Pricing with calculator URLs
- Last verified dates

### When to Use
- Need final RFP response document
- All analysis complete
- Ready for submission

### Key Outputs
- **Complete Response**: Professional RFP document
- **Source Index**: All sources cited with URLs
- **Accuracy Statement**: Verification framework compliance

### Wiki References
- RFP template: `wiki/apv/templates/.rfp-response-template.md`
- All previous skill outputs

---

## Skill 7: apv-reviewer

### Command
```bash
/skill apv-reviewer --response <path-to-response>
```

### Purpose
Unified 15-minute approval verification.

### Input Requirements
- Complete RFP response document

### Review Process (15 minutes)
| Step | Time | Activity |
|------|------|----------|
| 1 | 2 min | Read response (executive summary, structure) |
| 2 | 3 min | Run automated checks (URL validation, freshness) |
| 3 | 3 min | Content verification (completeness scan) |
| 4 | 3 min | Accuracy spot-check (3-5 random claims) |
| 5 | 2 min | Compliance verification (PCI-DSS, countries) |
| 6 | 1 min | Quality check (formatting, appendices) |
| 7 | 1 min | Calculate and decide |

### Approval Criteria

| Decision | Source URL % | Confidence | Requirements |
|----------|--------------|------------|--------------|
| ✅ Approve | ≥ 95% | ≥ 90% | All critical pass |
| ⚠️ Conditional | ≥ 90% | ≥ 80% | Minor issues OK |
| ❌ Reject | < 90% | < 80% | Critical fails |

### Weighted Score
```
Overall = (SourceURL% × 0.30) + (Content% × 0.25) + (Accuracy% × 0.25) + (Compliance% × 0.15) + (Quality% × 0.05)
```

### When to Use
- Before submitting RFP response
- After making final revisions
- Final quality gate

### Key Outputs
- **Approval Decision**: Approve/Conditional/Reject
- **Confidence Score**: Overall confidence %
- **Issues List**: Critical and minor issues
- **Automated Checks**: URL validation and freshness results

---

## Quick Command Reference

```bash
# Full chain (recommended)
/apv rfp <path-to-rfp>

# Individual skills
/skill rfp-brainstorm --rfp <path-to-rfp>
/skill rfp-compliance --rfp <path-to-rfp>
/skill rfp-architect --rfp <path-to-rfp>
/skill rfp-calculator --rfp <path-to-rfp>
/skill rfp-pricer --rfp <path-to-rfp>
/skill rfp-generator --rfp <path-to-rfp>

# Review
/skill apv-reviewer --response <path-to-response>
```

---

## Output Files

| Skill | Output File | Content |
|-------|-------------|---------|
| rfp-brainstorm | `brainstorm-output.md` | Strategic analysis |
| rfp-compliance | `compliance-output.md` | Compliance matrix |
| rfp-architect | `architecture-output.md` | Technical design |
| rfp-calculator | `sizing-output.md` | Capacity planning |
| rfp-pricer | `pricing-output.md` | Cost breakdown |
| rfp-generator | `rfp-response.md` | Final response |
| apv-reviewer | `review-report.md` | Approval decision |

---

## See Also

- [[apv-user-guide]] - Complete user guide
- [[apv-troubleshooting]] - Troubleshooting guide
- [[apv-skills-directory]] - All skills index
