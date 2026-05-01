---
type: apv-meta
category: documentation
title: APV V2 User Manual
created: '2026-05-01'
tags:
  - apv
  - v2
  - user-manual
  - guide
---

# APV V2 User Manual

## Who This Manual Is For

This manual is for anyone using APV V2 to respond to RFPs — primarily **sales team members** and **solution architects**. No engineering background is required to follow the core workflow. Technical sections are clearly marked.

---

## Table of Contents

1. [What Is APV V2?](#1-what-is-apv-v2)
2. [Getting Started](#2-getting-started)
3. [Step-by-Step: Running a New RFP Project](#3-step-by-step-running-a-new-rfp-project)
4. [How to Guide the AI (Sales Context)](#4-how-to-guide-the-ai-sales-context)
5. [Reviewing and Revising Outputs](#5-reviewing-and-revising-outputs)
6. [Changing the Architecture](#6-changing-the-architecture)
7. [Understanding the Approval Decision](#7-understanding-the-approval-decision)
8. [Troubleshooting](#8-troubleshooting)
9. [Reference: Pipeline Stages](#9-reference-pipeline-stages)
10. [Reference: Folder Structure](#10-reference-folder-structure)
11. [Reference: Key Commands](#11-reference-key-commands)

---

## 1. What Is APV V2?

**APV V2** (AI-Powered RFP Velocity, Version 2) is an AI-assisted system that takes a customer's RFP document and produces a complete, professional RFP response — including architecture design, compliance mapping, infrastructure sizing, and itemized pricing.

### What It Produces

Given an RFP document, APV V2 automatically generates:

| Output | What It Is |
|--------|-----------|
| **Strategic options** | 2–3 architectural approaches with trade-offs |
| **Compliance mapping** | Every regulation the customer requires, mapped to how we satisfy it |
| **Architecture design** | Full infrastructure design with documented decisions |
| **Sizing** | Compute, database, and network sizing from the customer's volume numbers |
| **Pricing** | Itemized monthly cost estimate with verified AWS/Azure/GCP prices |
| **Final RFP response** | A complete, formatted document ready to send |

### What APV V2 Covers

- **Industries**: Payment gateways, card issuing, card acquiring, digital wallets, tokenization, 3DS
- **Regions**: Singapore, Malaysia, Philippines, Indonesia, Thailand, Taiwan, Hong Kong
- **Cloud providers**: AWS (primary), Azure, GCP
- **Compliance frameworks**: PCI-DSS v4.0 + 7-country regulatory frameworks (MAS, BNM, BSP, BI, BOT, FSC, HKMA)

---

## 2. Getting Started

### Prerequisites

Before running a project, you need:
- The customer's RFP document (any format: PDF, Word, email, plain text)
- Access to the `wiki/apv-v2/` directory
- Claude Code (the AI assistant) running in this workspace

### Project Location

All RFP projects are stored in:
```
wiki/apv-v2/apv-projects/[customer]--[title]--[date]/
```

Example:
```
wiki/apv-v2/apv-projects/acme-payments--payment-gateway--2026-05-01/
```

### How to Start

Type this command to the AI assistant:
```
apv new [customer-name] [short-title]
```

Example:
```
apv new "dbs-bank" "card-issuing-platform"
```

The system creates the project folder and begins the pipeline automatically.

---

## 3. Step-by-Step: Running a New RFP Project

### Step 1 — Create the Project

Tell the AI:
```
apv new [customer] [title]
```

This creates the project folder with all required subfolders.

### Step 2 — Add the RFP Document

Drop the customer's RFP file into:
```
input/raw/
```

Any format works. You can add multiple documents (e.g., RFP + technical questionnaire + volume spreadsheet).

### Step 3 — Normalize the Inputs (Automatic)

The system converts all raw documents into structured markdown. It extracts:
- Requirements summary
- Volume / transaction data
- Technical specifications

This happens automatically. You will see three files created:
```
input/normalized/rfp.md
input/normalized/requirements-summary.md
input/normalized/volume-summary.md
```

### Step 4 — Provide Your Sales Context

At Stage 1 (Brainstorm), the AI will ask you for strategic direction. This is your most important contribution. Share:

- **Customer priorities**: What matters most to them? (compliance, cost, speed to market)
- **Deal context**: Existing relationship? Incumbent vendor? Competitive situation?
- **Constraints**: Budget ceiling, preferred cloud, existing infrastructure
- **Questions**: What don't you know yet about the customer's needs?

See [Section 4](#4-how-to-guide-the-ai-sales-context) for more guidance on this step.

### Step 5 — Pipeline Runs Automatically (Stages 1–6)

The AI runs through 6 stages in sequence:

```
Stage 1: Brainstorm    → Strategic options and gap analysis
Stage 2: Compliance    → Regulatory mapping with sources
Stage 3: Architecture  → Infrastructure design
Stage 4: Sizing        → Compute/DB/network sizing
Stage 5: Pricing       → Verified cost estimate
Stage 6: Response      → Final RFP document assembled
```

Each stage produces files you can review. The AI will flag any issues or gaps it encounters.

### Step 6 — Review and Approve (Stage 7)

The system runs an automatic quality check (Stage 7) before handing the response to you. It verifies:
- All compliance claims have source URLs
- Pricing data is fresh (within 30 days)
- No placeholder text or unsupported claims

You receive one of three decisions: **APPROVED**, **CONDITIONAL**, or **REJECTED**.

### Step 7 — Deliver

Your final output is at:
```
outputs/06-response.md
```

This is a complete, formatted RFP response document ready to send to the customer.

---

## 4. How to Guide the AI (Sales Context)

Your knowledge of the deal is the AI's most valuable input. Here is what to share and when.

### At Stage 1 (Brainstorm) — Strategic Direction

| What to Share | Example |
|--------------|---------|
| Customer's top priorities | "They emphasized compliance — it's 25% of their evaluation criteria" |
| Budget signals | "They mentioned $20K/month is their ceiling" |
| Cloud preference | "Their IT team uses AWS; they'd prefer to stay on AWS" |
| Competitive context | "We know [Competitor X] is also bidding; they tend to go lowest cost" |
| Relationship history | "We've done a POC with them before — they trust our AWS expertise" |
| Unknown factors | "We don't know if they want managed services or to self-operate" |
| Phase 2 / future plans | "They mentioned Indonesia expansion in 18 months" |

### When You Don't Have the RFP Document

If the customer hasn't sent a formal RFP yet, you can still run APV V2 using a verbal brief. Just describe the opportunity to the AI:

> "The customer is a fintech in Malaysia, they need a card issuing platform, roughly 20 million transactions per month, need BNM compliance and PCI-DSS, AWS preferred, go-live in Q4 2026."

The AI will generate a synthetic requirements summary and flag that no source documents were provided.

### Clarification Questions

After Stage 1, check `outputs/01-brainstorm.md` — the AI generates a list of **Clarification Questions** you can send back to the customer to strengthen the response. These are pre-built and ready to use.

---

## 5. Reviewing and Revising Outputs

Every stage produces a readable output file. You can review and request changes at any point.

### Output Files

| Stage | File | What to Review |
|-------|------|---------------|
| 1 | `outputs/01-brainstorm.md` | Strategic options — do they match your deal strategy? |
| 2 | `outputs/02-compliance.md` | Compliance frameworks — are all required regulations covered? |
| 3 | `outputs/03-architecture.md` | Infrastructure design — does it match what the customer wants? |
| 4 | `outputs/04-sizing.md` | Instance sizes and counts — do volumes look right? |
| 5 | `outputs/05-pricing.md` | Monthly cost breakdown — is pricing competitive? |
| 6 | `outputs/06-response.md` | Final document — ready to send? |

### How to Request Changes

Simply tell the AI what you want changed and which stage to re-run from:

> "The pricing in Stage 5 is too high. Go back to Stage 3 and use ECS Fargate instead of EKS to reduce cost."

> "Stage 2 is missing Thailand compliance — the customer confirmed Phase 2 includes Thailand. Re-run Stage 2."

> "The executive summary in the final response doesn't mention our managed services capability. Update Stage 6."

The AI will re-run from the stage you specify and regenerate all downstream outputs automatically.

### Resuming a Stage

```
apv resume [project-path] --from-stage [N]
```

Example — re-run from architecture:
```
apv resume apv-projects/dbs-bank--card-issuing--2026-05-01 --from-stage 3
```

---

## 6. Changing the Architecture

Architecture is the most common area for revision. Here is how to make changes effectively.

### Method 1: Direct Instruction

Tell the AI what to change in plain language:

> "Switch from EKS to ECS Fargate — the customer's team doesn't have Kubernetes expertise."

> "Change the DR region from Jakarta to Kuala Lumpur (ap-southeast-5)."

> "Remove CloudHSM — use KMS only. The customer accepted FIPS 140-2 Level 2."

> "Add a second cloud provider (Azure) for resilience — the customer requires multi-cloud."

Then resume from Stage 3:
```
apv resume [project-path] --from-stage 3
```

### Method 2: Challenge a Specific Decision (ADR)

Every architecture decision is documented as an **Architecture Decision Record (ADR)**. You can reference them by number to request targeted changes.

Check `working/03-architecture-decision-log.md` for the full list. Common decisions include:

| ADR | Typical Decision | How to Challenge |
|-----|-----------------|-----------------|
| ADR-1 | EKS vs ECS | "Revisit ADR-1: use ECS Fargate for simpler ops" |
| ADR-2 | Aurora vs RDS | "Revisit ADR-2: standard RDS to reduce cost" |
| ADR-4 | CloudHSM vs KMS only | "Revisit ADR-4: KMS only, customer accepts Level 2" |
| ADR-5 | DR strategy and region | "Revisit ADR-5: pilot light DR instead of warm standby" |
| ADR-6 | WAF + Shield vs WAF only | "Revisit ADR-6: drop Shield Advanced, WAF only" |

### Method 3: Change Strategy (Re-run from Stage 1 or 2)

If the architecture is wrong because the strategy or compliance scope is wrong:

**Re-run from Stage 1** when:
- Switching cloud provider (AWS → Azure or GCP)
- Fundamental approach change (microservices → monolith)
- New customer brief with significantly different requirements

**Re-run from Stage 2** when:
- Compliance scope changed (adding or removing countries)
- Customer changed a compliance requirement
- New regulatory framework must be included

### What Gets Re-run Automatically

When you change the architecture, the system automatically re-runs all downstream stages:

```
Architecture (Stage 3) changed
        ↓  automatically re-runs
Sizing (Stage 4)
        ↓
Pricing (Stage 5)
        ↓
Final Response (Stage 6)
        ↓
Approval Review (Stage 7)
```

You do not need to manually update the pricing or final document.

### Cost-Driven Architecture Changes

If the pricing estimate is too high, tell the AI your budget target and ask for cost reduction options:

> "The estimate of $25,000/month is over budget. Target is $18,000/month. Go back to Stage 3 and identify what to cut, with compliance implications clearly noted."

The AI will revise the architecture with trade-offs documented in the ADRs.

---

## 7. Understanding the Approval Decision

Stage 7 is an automatic quality gate. It checks the response before handing it to you.

### Three Possible Decisions

#### ✅ APPROVED
All checks passed. The response is ready to send. Check:
```
outputs/07-approval.md
approvals/release-decision.md
```

#### ⚠️ CONDITIONAL
Minor issues found that need fixing before release. The approval document will list exactly what to fix and which stage to re-run. Common conditional issues:
- Pricing data approaching its freshness threshold (will expire soon)
- Low-severity knowledge gaps documented as caveats
- Minor formatting or consistency issues

#### ❌ REJECTED
Critical issues found. The response must not be sent. Common rejection reasons:
- Missing source URLs on compliance or pricing claims
- Stale pricing with no documented assumption
- Unresolved blocker-level gaps (e.g., a required compliance framework not covered)
- Inconsistent numbers between sections

### What the Checklist Verifies

| Check | What It Looks For |
|-------|-----------------|
| Source URL compliance | Every compliance and pricing claim has a real, verifiable URL |
| Pricing freshness | All pricing data is within its 30-day verification window |
| Evidence completeness | Supporting evidence files exist for all major claims |
| Output class trace | No unverified brainstorm-only claims appear as facts in the response |
| Assumption review | All assumptions are documented and visible in the response |
| Document quality | No placeholder text, consistent numbers, professional tone |

### Acting on a CONDITIONAL Decision

The approval document lists specific fixes. For example:
> "Issue 1: AWS pricing last verified 2026-04-01 (30 days ago, at threshold). Refresh pricing knowledge and re-run from Stage 5."

Re-run the affected stage:
```
apv resume [project-path] --from-stage 5
```

---

## 8. Troubleshooting

### Gate Failure: "Missing upstream artifacts"

**What it means**: A required file from a previous stage is missing.

**How to fix**: Check which stage the error points to, then re-run from the stage that should have produced the missing file.

```
apv resume [project-path] --from-stage [N]
```

### Stale Knowledge Warning

**What it means**: A knowledge page (pricing or compliance) has not been verified within its freshness window.

**Pricing is stale (> 30 days)**:
- For a conditional approval: document as an assumption and proceed with a note that prices should be re-verified before final submission
- For a rejected approval: pricing must be refreshed before the response can be released

**Compliance is stale (> 365 days)**:
- This is unusual — compliance frameworks change slowly
- Flag to your solutions architect to verify no major regulatory changes have occurred

### "No knowledge found" for a Country or Framework

**What it means**: The knowledge base doesn't have information for a specific regulation or country.

**How to fix**:
- Check `working/00-gap-log.md` — the system will have logged the gap with severity
- If LOW severity: the AI will make a reasonable assumption and document it
- If HIGH severity: flag to your solutions architect to add the knowledge page before proceeding
- If BLOCKER: the pipeline halts — the knowledge gap must be resolved first

### The Pricing Seems Wrong

**What to check**:
1. Open `outputs/04-sizing.md` — are the instance types and counts what you expected?
2. Open `working/05-pricing-manifest.md` — check the per-component calculations
3. Open `evidence/pricing/` — source URLs are listed; you can verify against AWS pricing directly

If you find an error, correct the sizing (Stage 4) or architecture (Stage 3) and re-run:
```
apv resume [project-path] --from-stage 4
```

> ⚠️ **Never manually edit the pricing files.** Always re-run the appropriate stage. Manual edits create untraceable changes and break the audit trail.

### Dry Run Before Starting

If you want to check whether the knowledge base is ready before committing to a full run:
```
apv dry-run [project-path]
```

This checks knowledge freshness and completeness without running any stages.

---

## 9. Reference: Pipeline Stages

| Stage | Skill | Output Class | Key Output File |
|-------|-------|-------------|----------------|
| 0 | Ingestion | — | `input/normalized/rfp.md` |
| 1 | rfp-brainstorm | exploratory | `outputs/01-brainstorm.md` |
| 2 | rfp-compliance | evidence-backed | `outputs/02-compliance.md` |
| 3 | rfp-architect | derived | `outputs/03-architecture.md` |
| 4 | rfp-calculator | derived | `outputs/04-sizing.md` |
| 5 | rfp-pricer | evidence-backed | `outputs/05-pricing.md` |
| 6 | rfp-generator | derived | `outputs/06-response.md` |
| 7 | apv-reviewer | — | `outputs/07-approval.md` |

### Output Classes Explained

| Class | Meaning | Can Be Cited as Fact? |
|-------|---------|----------------------|
| **exploratory** | Strategic thinking, options, hypotheses (Stage 1) | No — informs strategy only |
| **evidence-backed** | Every claim has a verified source URL (Stages 2, 5) | Yes |
| **derived** | Conclusions traceable to evidence-backed inputs (Stages 3, 4, 6) | Yes, with traceability |

---

## 10. Reference: Folder Structure

### Per-Project Folder

```
apv-projects/[customer]--[title]--[date]/
│
├── input/
│   ├── raw/                  ← PUT YOUR RFP DOCUMENTS HERE
│   └── normalized/           ← auto-generated markdown versions
│       ├── rfp.md
│       ├── requirements-summary.md
│       └── volume-summary.md
│
├── outputs/                  ← STAGE OUTPUTS (what you review)
│   ├── 01-brainstorm.md
│   ├── 02-compliance.md
│   ├── 03-architecture.md
│   ├── 04-sizing.md
│   ├── 05-pricing.md
│   ├── 06-response.md        ← FINAL RFP RESPONSE
│   └── 07-approval.md        ← APPROVAL DECISION
│
├── working/                  ← INTERNAL ARTIFACTS (audit trail)
│   ├── 00-gap-log.md         ← running list of knowledge gaps
│   ├── 01-brainstorm-context.md
│   ├── 02-compliance-map.md
│   ├── 03-architecture-decision-log.md  ← ADRs
│   ├── 04-sizing-record.md
│   ├── 05-pricing-manifest.md
│   └── 05-assumption-log.md
│
├── evidence/
│   ├── compliance/           ← compliance source evidence
│   └── pricing/              ← pricing source evidence
│
├── verification/
│   ├── source-url-validation.json
│   └── freshness-report.json
│
└── approvals/
    ├── release-decision.md
    └── reviewer-notes.md
```

### Knowledge Base (Shared Across All Projects)

```
wiki/apv-v2/knowledge/
├── compliance/
│   ├── pci-dss/              ← PCI-DSS v4.0 (12 requirements)
│   └── countries/            ← SG, MY, PH, ID, TH, TW, HK
├── card-systems/             ← Gateway, Issuing, Acquiring, 3DS, Tokenization, Wallets
├── infrastructure/           ← AWS, Azure, GCP patterns
├── pricing/                  ← Verified cloud pricing (refreshed every 30 days)
└── sizing/                   ← TPS calculation methodology
```

---

## 11. Reference: Key Commands

| Command | What It Does |
|---------|-------------|
| `apv new [customer] [title]` | Start a new RFP project |
| `apv resume [path] --from-stage N` | Re-run pipeline from a specific stage |
| `apv dry-run [path]` | Check knowledge readiness without running stages |

### Stage Numbers for Resume

| Use `--from-stage` | When |
|-------------------|------|
| `1` | Strategy or brief has changed |
| `2` | Compliance scope has changed |
| `3` | Architecture needs to change |
| `4` | Sizing inputs or volumes have changed |
| `5` | Pricing needs refresh or components changed |
| `6` | Final document needs editing |
| `7` | Re-run approval check after fixes |

---

## Quick Reference Card (For Sales)

**Starting a project:**
1. Get the RFP document
2. `apv new [customer] [title]`
3. Drop RFP into `input/raw/`
4. Provide sales context when Stage 1 asks
5. Wait for pipeline to complete
6. Review `outputs/06-response.md`

**Changing something:**
- Architecture → `apv resume [path] --from-stage 3`
- Compliance → `apv resume [path] --from-stage 2`
- Pricing → `apv resume [path] --from-stage 5`
- Final doc only → `apv resume [path] --from-stage 6`

**Approval outcomes:**
- ✅ APPROVED → ready to send
- ⚠️ CONDITIONAL → fix listed issues, re-run
- ❌ REJECTED → check `outputs/07-approval.md` for what to fix

**Your final deliverable:** `outputs/06-response.md`
