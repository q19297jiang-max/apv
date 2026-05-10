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

If you are maintaining shared AWS pricing knowledge rather than running a sales workflow, use `docs/pricing-operator-cheat-sheet.md` for the shortest operator path and `knowledge/pricing/pricing-workflow.md` for the full operator playbook.

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
./bin/apv new [customer-name] [short-title] --raw-dir [folder-with-rfp-files]
```

Example:
```
./bin/apv new "dbs-bank" "card-issuing-platform" --raw-dir raw/bbc-bank-rfp/
```

The command creates the project folder under `apv-projects/`, copies files from the raw source folder, normalizes them, prepares the knowledge snapshot, and makes the project ready for stage execution.

### Choosing Your Run Mode

APV V2 supports two explicit run modes:

- **Draft mode** — internal exploration mode. Use this when you are still learning the deal, generating an internal first pass, or collecting missing context. Draft runs can produce a full artifact chain, but they are **never release-eligible**.
- **Submission mode** — governed delivery mode. Use this when the opportunity is live, the deal owner is assigned, and the sales strategy has been approved. Submission runs may become release-eligible if verification and approval pass.

New projects default to **draft** mode.

To choose a mode explicitly:

```bash
./bin/apv new [customer-name] [short-title] --raw-dir [folder-with-rfp-files] --mode draft
```

```bash
./bin/apv new [customer-name] [short-title] --raw-dir [folder-with-rfp-files] --mode submission
```

---

## 3. Step-by-Step: Running a New RFP Project

### Step 1 — Create the Project

Tell the AI:
```
./bin/apv new [customer] [title] --raw-dir [folder-with-rfp-files]
```

This creates the project folder, copies the raw files into `input/raw/`, and prepares the normalized inputs automatically.

### Step 1a — Decide Whether This Is Draft Or Submission Work

Use **draft** mode when:
- you are still exploring the customer request
- the deal is not yet ready for formal submission
- you want fast internal output without asserting release authority

Use **submission** mode when:
- the opportunity is active and owned
- the win strategy is known
- constraints are approved and documented

If a project starts in draft mode and later becomes real submission work, do not patch artifacts manually. Promote it using the dedicated workflow described later in this manual.

### Step 2 — Verify the Imported RFP Files

The raw files you passed via `--raw-dir` are copied into:
```
input/raw/
```

Any format works. You can include multiple documents in the source folder, such as the RFP, technical questionnaire, and volume spreadsheet.

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

### Step 4a — Add A Sales Brief For Submission Mode

Submission mode requires a lightweight sales brief. The default artifact is:

```text
input/normalized/sales-brief.md
```

At minimum it should include:
- **Deal Owner**
- **Win Strategy**
- **Constraints**
- **Approved By**
- **Approved Date**

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

### Promoting A Draft Project To Submission Mode

When a draft project becomes a real submission candidate, use:

```bash
./bin/apv promote-to-submission --project apv-projects/[customer]--[title]--[date] --owner "[deal-owner]" --strategy "[win-strategy]" --constraint "[constraint]"
```

This command:
- creates or updates `input/normalized/sales-brief.md`
- updates `working/00-run-context.json`
- changes the project mode from `draft` to `submission`

There are two promotion paths:

- **Full rerun** (default) — use this when the new sales intent changes strategy, priorities, or constraints enough that Stage 1 should be rerun.
- **Fast-track** — use this only when the strategy is already aligned and you can provide explicit attestation text.

Fast-track example:

```bash
./bin/apv promote-to-submission --project apv-projects/[customer]--[title]--[date] --owner "[deal-owner]" --strategy "[win-strategy]" --constraint "[constraint]" --fast-track-attestation "Strategy unchanged from draft review; aligned for submission."
```

If you use the default promotion path, APV will require a rerun from **Stage 1** before downstream submission work is considered valid.

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

### Updating Pricing Without Editing Files

If Stage 5 is missing a component, a price is stale, or you need a new AWS item for the deal, do not edit pricing markdown manually. Use the pricing commands below, then re-run from Stage 5 if needed.

If someone points at a generated pricing file such as `knowledge/pricing/aws-component-catalog.md`, `knowledge/pricing/aws.md`, or `knowledge/pricing/aws-component-catalog.report.json` and asks for a change, start with the routing command first. It tells you whether the file is generated and which source-of-truth workflow owns it.

The generated AWS pricing files now include a `3-Year Upfront Projection` column for every row.
This is a normalized 36-month estimate, not a claim that AWS offers an actual 3-year commitment model for every service.
APV calculates it as:
- hourly rows: `730 hours/month x 36 months`
- other unit-priced rows: the same billing unit repeated across `36 monthly periods`

The catalog also shows a `Verification Mode` column. Read it literally:
- `public-offer` means the row is backed by supported live public-offer validation, typically against AWS Calculator or AWS public offer data for the supported services
- `formula` means the row is derived from an established calculator-backed baseline or multiplier, not independently live-queried for every row
- `official-page` means the row comes from an AWS pricing page rather than calculator-backed live validation

This means APV tracks how each price was verified, but not every AWS row is automatically live-validated by AWS Calculator.

#### Most Common Pricing Tasks

| Situation | What to Run |
|----------|-------------|
| Someone asks to change a generated pricing KB file directly | `./bin/apv knowledge route-change --knowledge-dir knowledge --target [generated-file-path]` |
| Refresh the existing AWS pricing knowledge | `./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness` |
| Add one EC2, RDS, or CloudHSM item | `./bin/apv pricing add-item --provider aws --service [service] --instance-type [type] --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add a whole EC2 or RDS family | `./bin/apv pricing extend-family --provider aws --service [service] --family [family] --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one Redis or ElastiCache node type | `./bin/apv pricing add-item --provider aws --service redis --component [cache-node-type] --unit-price [price] --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one known single-row static AWS service such as ALB, S3, GuardDuty, WAF, KMS, Route 53, Shield Advanced, Secrets Manager, SNS, SQS, ECR, or API Gateway | `./bin/apv pricing add-item --provider aws --service [service] --unit-price [price] --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one known multi-component static AWS row such as CloudWatch logs, Route 53 DNS queries, or NAT Gateway data processing | `./bin/apv pricing add-item --provider aws --service [service] --component [component] --unit-price [price] --knowledge-dir knowledge --refresh --sync --check-freshness` |

#### New Function: Route a Generated Knowledge File Back to the Real Workflow

Use this when the starting point is a generated file path rather than a pricing requirement.

In plain English, this command does two jobs at once:
- it acts as a guardrail by blocking direct edits to generated pricing artifacts
- it acts as a router by telling you which source-of-truth workflow really owns that file

Example:

```bash
./bin/apv knowledge route-change --knowledge-dir knowledge --target knowledge/pricing/aws-component-catalog.md
```

What it does:
- inspects the target file you passed in
- checks the file metadata and APV's known generated-file routes
- blocks direct editing if the file is a generated pricing artifact
- shows the real source of truth, which is usually `knowledge/pricing/aws-pricing-manifest.json`
- shows the regeneration command to use after changing the source of truth

What a normal result means:
- `Direct edit blocked for generated knowledge file.` means the file is generated and you should not edit it
- `Source of truth: ...` tells you which manifest or workflow owns the file
- `Regenerate with: ...` tells you which command to run after updating the source of truth

Why this exists:
- generated files such as `knowledge/pricing/aws-component-catalog.md`, `knowledge/pricing/aws.md`, and `knowledge/pricing/aws-component-catalog.report.json` are outputs, not authoritative inputs
- direct edits would be overwritten the next time pricing is refreshed
- direct edits also break traceability because the real pricing logic lives in the manifest and generator workflow

Typical flow:
1. Run `knowledge route-change` on the generated file path.
2. Update the source-of-truth workflow it points to, usually with `pricing add-item`, `pricing extend-family`, or `refresh-pricing`.
3. Re-run Stage 5 for your project if the shared pricing change affects the response.

Wrong vs right example:
- Wrong: edit `knowledge/pricing/aws.md` because an ALB price looks wrong.
- Right: run `knowledge route-change` on `knowledge/pricing/aws.md`, update the source workflow it points to, regenerate pricing, then re-run Stage 5 if needed.

Pricing verification example:
- An EC2 on-demand row may show `public-offer`, which means APV can validate it through the supported live pricing path.
- A Savings Plans row may show `formula`, which means APV derived it from a validated discount pattern rather than live-querying each Savings Plans row individually.
- An ALB or S3 row may show `official-page`, which means APV uses the AWS pricing page as the source instead of calculator-backed validation.

#### Friendly Service Names You Can Use

You do not need to remember the internal AWS service names exactly. The CLI accepts friendly names and normalizes them automatically.

| You Can Type | The System Uses |
|-------------|-----------------|
| `postgres`, `postgresql`, `postgresql/rds` | `RDS` |
| `redis`, `elasticache` | `ElastiCache` |
| `alb` | `ALB` |
| `nlb` | `NLB` |
| `route53` | `Route 53` |
| `shield-advanced`, `shield` | `Shield Advanced` |
| `cloudwatch` | `CloudWatch` |
| `nat-gateway` | `NAT Gateway` |
| `secrets-manager` | `Secrets Manager` |
| `sns` | `SNS` |
| `sqs` | `SQS` |
| `ecr` | `ECR` |
| `api-gateway` | `API Gateway` |
| `security-hub` | `Security Hub` |
| `private-ca` | `ACM Private CA` |

#### Copy-and-Use Examples

Add one PostgreSQL RDS item:

```bash
./bin/apv pricing add-item --provider aws --service postgresql/rds --instance-type db.m6i.xlarge --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one Redis pricing row:

```bash
./bin/apv pricing add-item --provider aws --service redis --component cache.m7g.large --unit-price 0.312 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one ALB row with inferred defaults:

```bash
./bin/apv pricing add-item --provider aws --service alb --unit-price 0.0225 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one GuardDuty row with inferred defaults:

```bash
./bin/apv pricing add-item --provider aws --service guardduty --unit-price 4.0 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one Route 53 hosted-zone row with inferred defaults:

```bash
./bin/apv pricing add-item --provider aws --service route53 --unit-price 0.5 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one CloudWatch logs-ingest row using a controlled component alias:

```bash
./bin/apv pricing add-item --provider aws --service cloudwatch --component logs-ingest --unit-price 0.5 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Add one NAT Gateway data-processing row using a controlled component alias:

```bash
./bin/apv pricing add-item --provider aws --service nat-gateway --component data-processing --unit-price 0.045 --knowledge-dir knowledge --refresh --sync --check-freshness
```

Extend an RDS family:

```bash
./bin/apv pricing extend-family --provider aws --service postgres --family m6i --knowledge-dir knowledge --refresh --sync --check-freshness
```

Refresh pricing only:

```bash
./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness
```

Check whether a generated pricing file should be changed indirectly:

```bash
./bin/apv knowledge route-change --knowledge-dir knowledge --target knowledge/pricing/aws.md
```

After pricing changes, if your project already exists, re-run the pricing stage:

```bash
apv resume [project-path] --from-stage 5
```

#### Simple Rule for Sales Users

- Use `refresh-pricing` when the prices are stale but the component list is unchanged.
- Use `knowledge route-change` when the request starts from a generated pricing file path.
- Use `pricing add-item` when one component is missing.
- Use `pricing extend-family` when you need several sizes from the same EC2 or RDS family.
- After refresh, review the generated `3-Year Upfront Projection` column when you need a 36-month comparison for the decision maker.
- For single-row static services, `--service` plus `--unit-price` is enough.
- For componentized static services, add a controlled `--component`, such as `dns-queries`, `logs-archive`, `custom-metrics`, `standard-alarm`, or `data-processing`.
- Never edit `knowledge/pricing/aws-component-catalog.md` or `knowledge/pricing/aws.md` directly.

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

### Quality Is Not The Same As Release Authority

Stage 7 answers a **quality** question: is the output approved, conditional, or rejected?

Release authority is a separate **governance** question:

- Is the project in `submission` mode?
- Does it have approved sales intent?

This means a draft project can still produce a strong Stage 7 result, but remain **non-release-eligible**.

Check both:
- `outputs/07-approval.md` for quality status
- `approvals/release-decision.md` and `working/00-run-context.json` for final release eligibility context

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

### Project Is Approved But Still Not Releaseable

**What it means**: The quality gate passed, but the project is still in draft mode or missing approved submission authority.

**How to fix**:
- confirm whether the project should remain internal-only
- if it should be released, run `promote-to-submission`
- rerun the required stage chain if the promotion path requires Stage 1 regeneration

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

If the issue is not sizing but missing or stale AWS pricing knowledge:

```bash
./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness
apv resume [project-path] --from-stage 5
```

If one AWS item is missing, add it first, then re-run pricing:

```bash
./bin/apv pricing add-item --provider aws --service postgresql/rds --instance-type db.m6i.xlarge --knowledge-dir knowledge --refresh --sync --check-freshness
apv resume [project-path] --from-stage 5
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
│       ├── volume-summary.md
│       └── sales-brief.md     ← submission-mode sales intent artifact
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
│   ├── 00-run-context.json   ← run mode, promotion state, release eligibility
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
| `apv new [customer] [title] [--mode draft|submission]` | Start a new RFP project in the chosen run mode |
| `apv promote-to-submission --project [path] --owner ... --strategy ... --constraint ...` | Promote a draft project into governed submission mode |
| `apv resume [path] --from-stage N` | Re-run pipeline from a specific stage |
| `apv dry-run [path]` | Check knowledge readiness without running stages |
| `./bin/apv knowledge route-change --knowledge-dir knowledge --target [path]` | Check whether a knowledge file is generated and route the change back to its source-of-truth workflow |
| `./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness` | Refresh the shared AWS pricing knowledge and rebuild validation state |
| `./bin/apv pricing add-item ...` | Add one supported AWS pricing item, refresh the KB, and keep pricing markdown generated |
| `./bin/apv pricing extend-family ...` | Add a whole EC2 or RDS family into the shared AWS pricing knowledge |

### Pricing Command Examples

| Task | Example |
|------|---------|
| Add one EC2 item | `./bin/apv pricing add-item --provider aws --service EC2 --instance-type m6i.xlarge --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one RDS item with friendly alias | `./bin/apv pricing add-item --provider aws --service postgresql/rds --instance-type db.m6i.xlarge --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one Redis row with friendly alias | `./bin/apv pricing add-item --provider aws --service redis --component cache.m7g.large --unit-price 0.312 --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one ALB row with inferred defaults | `./bin/apv pricing add-item --provider aws --service alb --unit-price 0.0225 --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Add one GuardDuty row with inferred defaults | `./bin/apv pricing add-item --provider aws --service guardduty --unit-price 4.0 --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Extend a family | `./bin/apv pricing extend-family --provider aws --service postgres --family m6i --knowledge-dir knowledge --refresh --sync --check-freshness` |
| Route a generated pricing file back to the owning workflow | `./bin/apv knowledge route-change --knowledge-dir knowledge --target knowledge/pricing/aws-component-catalog.md` |
| Refresh only | `./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness` |

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

Need the operator version instead? Use `docs/pricing-operator-cheat-sheet.md`.

**Starting a project:**
1. Get the RFP document
2. `apv new [customer] [title] [--mode draft|submission]`
3. Drop RFP into `input/raw/`
4. Provide sales context when Stage 1 asks
5. Wait for pipeline to complete
6. Review `outputs/06-response.md`

**If a draft becomes a real submission:**
- run `./bin/apv promote-to-submission --project [path] --owner ... --strategy ... --constraint ...`
- rerun from Stage 1 unless you intentionally use a fast-track attestation path

**Changing something:**
- Architecture → `apv resume [path] --from-stage 3`
- Compliance → `apv resume [path] --from-stage 2`
- Pricing → `apv resume [path] --from-stage 5`
- Final doc only → `apv resume [path] --from-stage 6`

**Pricing fixes:**
- Someone asked to change `knowledge/pricing/aws-component-catalog.md` or `aws.md` directly → `./bin/apv knowledge route-change --knowledge-dir knowledge --target [file]`
- Prices stale but component list unchanged → `./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness`
- One AWS item missing → `./bin/apv pricing add-item ... --refresh --sync --check-freshness`
- Several EC2 or RDS sizes missing → `./bin/apv pricing extend-family ... --refresh --sync --check-freshness`
- After any shared pricing change → `apv resume [path] --from-stage 5`

**Friendly service names:**
- `postgresql/rds` = `RDS`
- `redis` = `ElastiCache`
- `alb` = `ALB`
- `private-ca` = `ACM Private CA`

**Approval outcomes:**
- ✅ APPROVED → ready to send
- ⚠️ CONDITIONAL → fix listed issues, re-run
- ❌ REJECTED → check `outputs/07-approval.md` for what to fix

**Governance reminder:**
- draft mode can still produce approved quality artifacts
- only submission mode can become release-eligible

**Your final deliverable:** `outputs/06-response.md`
