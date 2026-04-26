---
type: apv-meta
category: system-documentation
title: "APV System Documentation Index"
version: "1.0"
created: 2026-04-23
tags: [apv, meta, index]
---

# APV System Documentation Index

Complete documentation for the APV (AI-Powered RFP Velocity) system.

## System Overview

| Document | Description |
|----------|-------------|
| [[apv-readme]] | APV system overview and quick start |
| [[current-state-status]] | Canonical implementation and validation status |
| [[session-rfp-ai-system-design]] | Complete system design with 6-skill chain |
| [[apv-accuracy-assurance]] | Accuracy framework with source URL requirements |
| [[apv-task-list-revised]] | 5-week implementation task list |

## Read This First

Read [[current-state-status]] before treating workflow, operations, or timing guidance in this repository as production-ready behavior. Several APV documents describe target-state workflow design, while the current validated scope is narrower.

## Directory Structure

```
wiki/apv/
├── README.md                          # System overview (this file)
├── knowledge/                         # Knowledge base
│   ├── compliance/                    # Compliance and regulations
│   │   ├── pci-dss/                   # PCI-DSS requirements (12 files)
│   │   └── countries/                 # Asian country regulations
│   │       ├── sg/                    # Singapore (MAS)
│   │       ├── my/                    # Malaysia (BNM)
│   │       ├── ph/                    # Philippines (BSP)
│   │       ├── id/                    # Indonesia (BI)
│   │       ├── th/                    # Thailand (BOT)
│   │       ├── tw/                    # Taiwan (FSC)
│   │       └── hk/                    # Hong Kong (HKMA)
│   ├── card-systems/                  # Card system types
│   ├── infrastructure/                # Cloud infrastructure patterns
│   │   ├── aws/                       # AWS patterns
│   │   ├── azure/                     # Azure patterns
│   │   └── gcp/                       # GCP patterns
│   ├── sizing/                        # Infrastructure sizing methodology
│   ├── pricing/                       # Pricing calculation methodology
│   └── evidence/                      # Source URL evidence storage
│       ├── pci-dss/                   # Compliance evidence
│       ├── countries/                 # Country regulation evidence
│       └── pricing/                   # Calculator screenshots
├── templates/                         # RFP response templates
│   ├── rfp-response-template.md       # Master template
│   └── section-templates/             # Section-specific templates
├── approvals/                         # Approval system
│   └── unified-checklist.md           # Single-gate approval checklist
├── skills/                            # AI skills
│   ├── rfp-brainstorm/                # Requirements collection
│   ├── rfp-compliance/                # Compliance mapping
│   ├── rfp-architect/                 # Architecture design
│   ├── rfp-calculator/                # Infrastructure sizing
│   ├── rfp-pricer/                    # Pricing calculation
│   ├── rfp-generator/                 # Document assembly
│   └── rfp-approver/                  # Unified approval review
├── meta/                              # System documentation
│   └── system-index.md                # This file
└── docs/                              # Guides, plans, and runtime contracts
```

## Knowledge Base Templates

### Compliance Templates
- `wiki/apv/knowledge/compliance/pci-dss/.template.md` — PCI-DSS requirement template
- `wiki/apv/knowledge/compliance/countries/.country-template.md` — Country regulation template

### Infrastructure Templates
- `wiki/apv/knowledge/card-systems/.template.md` — Card system type template
- `wiki/apv/knowledge/infrastructure/.template.md` — Cloud provider pattern template
- `wiki/apv/knowledge/sizing/.template.md` — Sizing methodology template
- `wiki/apv/knowledge/pricing/.template.md` — Pricing calculation template

### Skill Templates
- `wiki/apv/skills/.skill-template.md` — Generic skill template

## Key Workflows

### Creating New RFP Response
```
/apv "Bank Name" (rfp-brainstorm)
  → rfp-compliance
  → rfp-architect
  → rfp-calculator
  → rfp-pricer
  → rfp-generator
  → /apv-review "Bank Name" (rfp-approver)
  → Final RFP document
```

### Adding New Knowledge
1. Create file from appropriate template
2. Fill in content with source URLs
3. Verify source URLs are official sources
4. Save evidence screenshots to evidence/
5. Add wikilinks to related pages
6. Update index.md

### Source URL Verification
1. All compliance pages require official regulation URLs
2. All pricing pages require official calculator URLs
3. All architecture pages require reference pattern URLs
4. Evidence screenshots stored in evidence/ folders
5. Freshness checked: compliance (365 days), pricing (30 days)

## Quality Assurance

### Accuracy Targets
- Compliance accuracy: >95%
- Pricing accuracy: >98%
- Source URL compliance: 100%

These are design targets, not blanket proof that every APV subsystem has already achieved them in a real end-to-end run.

### Approval Gate
- Single unified approval (15 minutes)
- Source URL validation
- Specialist consultation triggers
- Accuracy spot-check (8/9 claims minimum)

### Evidence Storage
- Compliance: `wiki/apv/knowledge/evidence/pci-dss/`, `wiki/apv/knowledge/evidence/countries/`
- Pricing: `wiki/apv/knowledge/evidence/pricing/YYYY-MM-DD/`
- Screenshots required for all calculator outputs

## Implementation Status

Current repo status is best summarized in [[current-state-status]]. The phased table below reflects the original implementation roadmap and should not be interpreted as the only status signal.

| Phase | Tasks | Status |
|-------|-------|--------|
| Week 1: Foundation | 8 tasks | ⏳ Pending |
| Week 2: Knowledge Base | 8 tasks | ⏳ Pending |
| Week 3: Skills | 8 tasks | ⏳ Pending |
| Week 4: Testing | 8 tasks | ⏳ Pending |
| Week 5: Deployment | 6 tasks | ⏳ Pending |

**Total**: 38 tasks, 272 hours, 5 weeks

## Quick Reference

### Source URL Requirements
- **Compliance**: Official government/standards body URLs only
- **Pricing**: Official cloud provider calculator URLs only
- **Architecture**: Reference architecture URLs from vendor docs
- **Sizing**: Methodology reference URLs with calculations shown

### Expert Consultation Triggers
- New country regulation → Compliance Officer
- New card system type → Infrastructure Architect
- TPS > 5000 → Infrastructure Architect
- Custom pricing → Infrastructure Architect

### Freshness Thresholds
- Compliance data: 12 months
- Pricing data: 30 days
- Calculator evidence: 30 days

## Related

- [[apv-readme]] — System overview
- [[apv-accuracy-assurance]] — Accuracy framework
- [[apv-task-list-revised]] — Implementation tasks
