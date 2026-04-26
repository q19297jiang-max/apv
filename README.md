---
type: page
title: "APV System"
created: 2026-04-23
tags: [apv, rfp, overview]
---

# APV: AI-Powered RFP Velocity

## Overview

APV is a specialized AI-powered system design for fintech RFP responses. It combines structured knowledge bases, skill definitions, templates, and support tools aimed at producing accurate, compliant, and professionally formatted responses. The repository currently reflects a partially implemented, partially validated workflow rather than a fully operational end-to-end system.

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

## Test Setup

APV's executable checks assume a local Python environment with the repo's dev test dependency installed.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_runtime_project_fixture.py tests/test_doc_claims.py -q
python tests/run_integration_tests.py --verbose
```

## Accuracy Assurance

**Critical Requirements**:
- ✅ All compliance pages cite official source URLs
- ✅ All pricing pages cite official calculators
- ✅ All RFP claims cite sources
- ⚠️ Source URL compliance is a design requirement and is validated for selected outputs, not yet proven for every workflow path
- ⚠️ Expert verification is part of the approval design and should be treated as a required operating policy

**Quality Targets**:
- Compliance accuracy: >95%
- Pricing accuracy: >98%
- Source URL compliance: 100%

See `docs/current-state-status.md` for the current implementation and validation scope.

## Directory Structure

```
wiki/apv/
├── knowledge/          # Compliance, regulations, patterns
├── templates/          # RFP templates
├── approvals/         # Approval checklists
├── skills/             # AI skills
├── meta/               # System documentation
└── docs/              # Guides, plans, contracts, and status docs
```

## Related

- [[apv-accuracy-assurance]] - Accuracy framework
- [[apv-task-list]] - Implementation task list
- [[session-rfp-ai-system-design]] - System design

## System Status

**Version**: 1.0  
**Status**: Design complete, partially implemented, partially validated  
**Current Reality**: Real pilot validation exists for brainstorm and compliance; the remaining workflow is documented more strongly than it is operationally proven
