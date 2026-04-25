---
type: page
title: "APV System"
created: 2026-04-23
tags: [apv, rfp, overview]
---

# APV: AI-Powered RFP Velocity

## Overview

APV is a specialized AI-powered system for automating Request for Proposal (RFP) responses for fintech banking solutions. It combines structured knowledge bases with AI skills to generate accurate, compliant, and professionally formatted RFP responses in minutes instead of hours.

## System Components

### Knowledge Base
- **Compliance**: PCI-DSS + 7 Asian countries (Singapore, Malaysia, Philippines, Indonesia, Thailand, Taiwan, Hong Kong)
- **Card Systems**: Issuing, acquiring, gateway, wallet platforms
- **Infrastructure**: AWS, Azure, GCP patterns
- **Pricing**: Official calculator data with evidence

### AI Skills Chain
1. **rfp-brainstorm** - Requirements collection
2. **rfp-compliance** - Compliance mapping
3. **rfp-architect** - Architecture design
4. **rfp-calculator** - Infrastructure sizing
5. **rfp-pricer** - Pricing breakdown
6. **rfp-generator** - Document assembly

### Approval System
- Unified review checklist (15 minutes)
- Specialist consultation triggers
- Source URL validation
- Accuracy assurance

## Quick Start

```bash
# Start new RFP
/apv "Bank Name"

# Review output
/apv-review "Bank Name"

# Generate final RFP
/apv-generate "Bank Name"
```

## Accuracy Assurance

**Critical Requirements**:
- ✅ All compliance pages cite official source URLs
- ✅ All pricing pages cite official calculators
- ✅ All RFP claims cite sources
- ✅ 100% source URL compliance enforced
- ✅ Expert verification required

**Quality Targets**:
- Compliance accuracy: >95%
- Pricing accuracy: >98%
- Source URL compliance: 100%

## Directory Structure

```
wiki/apv/
├── knowledge/          # Compliance, regulations, patterns
├── templates/          # RFP templates
├── approvals/         # Approval checklists
├── skills/             # AI skills
├── meta/               # System documentation
└── .rfp-session/      # Working directory
```

## Related

- [[apv-accuracy-assurance]] - Accuracy framework
- [[apv-task-list]] - Implementation task list
- [[session-rfp-ai-system-design]] - System design

## System Status

**Version**: 1.0  
**Status**: Design complete, implementation pending  
**Target Launch**: 5 weeks from start date
