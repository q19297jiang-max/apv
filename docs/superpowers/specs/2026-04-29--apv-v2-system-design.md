# APV V2 System Design Spec

## Overview

APV V2 (AI-Powered RFP Velocity) automates payment-infrastructure RFP responses through a wiki-first, artifact-governed pipeline. The knowledge base is the central product — it grows and improves with every RFP processed.

### Business Requirements

1. **Speed** — compress RFP response time from weeks to hours
2. **Accuracy** — every price, compliance claim, and architecture choice traces to evidence
3. **Auditability** — full artifact chain in git; nothing hidden in prompt context
4. **Reusability** — knowledge grows across RFPs; gap rate decreases over time
5. **Quality gates** — no release without verified freshness, source URLs, and evidence completeness

### Design Approach

Enhanced Claude Code Skills with Python tooling. Each pipeline stage is a Claude Code skill following Anthropic SKILL.md format. Deterministic work (parsing, pricing lookups, validation, freshness checks) is handled by Python scripts. SQLite provides a derived index over the markdown knowledge base for fast structured queries.

---

## System Architecture (3 Layers + Knowledge Maintenance)

```
┌──────────────────────────────────────────────────────────┐
│  Layer 0: Knowledge Maintenance                          │
│                                                          │
│  0a. Scheduled Refresh (monthly)                         │
│  ─ pricing-fetcher.py    → pricing catalogs              │
│  ─ compliance-fetcher.py → regulation updates            │
│  ─ freshness-checker.py  → flag stale entries            │
│                                                          │
│  0b. On-Demand Fetch (triggered by pipeline gaps)        │
│  ─ Same scripts, targeted to specific components         │
│                                                          │
│  0c. Post-RFP Promotion (after each completed RFP)      │
│  ─ Review gap log → create missing knowledge pages       │
│  ─ Review corrections → update existing pages            │
│  ─ Promote reusable patterns → knowledge/patterns/       │
├──────────────────────────────────────────────────────────┤
│  Layer 1: Claude Code Skills (pipeline)                  │
│  ─ 8 skills: orchestrator + 7 stages                     │
│  ─ Each skill reads from knowledge/ via SQLite index     │
│  ─ Each skill emits artifacts + gap log entries          │
│  ─ Anthropic SKILL.md format with allowed-tools          │
├──────────────────────────────────────────────────────────┤
│  Layer 2: Python Tooling (tools/)                        │
│  ─ sync-db.py, normalize.py, pricing-lookup.py           │
│  ─ pricing-fetcher.py, freshness.py, validate-gates.py   │
│  ─ validate-urls.py, knowledge-promote.py, knowledge-    │
│    stats.py                                              │
│  ─ Deterministic, testable, no AI tokens                 │
├──────────────────────────────────────────────────────────┤
│  Layer 3: Data                                           │
│  ─ knowledge/*.md (source of truth)                      │
│  ─ apv-v2.sqlite (derived index, gitignored)             │
│  ─ evidence/ (verification artifacts)                    │
│  ─ git (everything versioned)                            │
└──────────────────────────────────────────────────────────┘
```

### Knowledge Base as the Central Product

The knowledge base is not a static reference — it is the primary product that improves with every RFP. Each RFP run validates existing knowledge and identifies gaps. Over time, gap rate decreases, coverage increases, and response quality improves.

```
Every RFP run:
  1. Reads knowledge    → produces response
  2. Logs gaps          → identifies missing knowledge
  3. Post-RFP review    → promotes new knowledge
  4. Net result         → knowledge base is more complete
```

---

## Knowledge Base Design

### 6 Domains

| Domain | Content | Freshness | Source |
|--------|---------|-----------|--------|
| Compliance | PCI-DSS v4.0 (12 reqs), country regs (7 countries × 3 regs) | 365 days | Official regulation docs |
| Card Systems | Issuing, acquiring, gateway, 3DS, tokenization, wallets | 365 days | Scheme documentation |
| Infrastructure | AWS/Azure/GCP services (EKS, RDS, AKS, GKE, etc.) | 90 days | Cloud provider docs |
| Pricing | Component catalogs per cloud provider | 30 days | Official calculators/APIs |
| Sizing | TPS methodology, peak multipliers, HA patterns | 365 days | Internal methodology |
| Patterns | Reference architectures for common payment scenarios | No expiry | Project experience |

### Knowledge File Structure

Every knowledge file has:

```yaml
---
type: apv-knowledge
category: compliance|pricing|infrastructure|card-systems|sizing|patterns
source_url: "https://official-url"        # MANDATORY
captured_date: YYYY-MM-DD
verified_by: "Role Name"
last_verified: YYYY-MM-DD
freshness_days: 365|90|30
tags: [apv, category, subcategory]
---
```

Body includes: overview, key requirements/components, tables with source URL columns, implementation guidance per cloud provider, RFP response template with `[Company Name]` placeholders, evidence checklist, common questions, and `[[wikilinks]]` to related pages.

### Knowledge Lifecycle

```
DRAFT → ACTIVE → STALE → REFRESH → ACTIVE
```

- **DRAFT**: new page, no source URL yet
- **ACTIVE**: verified, cited, in use
- **STALE**: past freshness window (`julianday('now') - julianday(last_verified) > freshness_days`)
- **REFRESH**: re-fetch from source, re-verify, update dates

### Three Refresh Mechanisms

**Scheduled (proactive)**: monthly cron runs `pricing-fetcher.py --all-providers` and `freshness.py --report`. Handles pricing, the fastest-aging domain.

**Pipeline-triggered (reactive)**: when a skill detects stale or missing knowledge, it triggers the relevant fetcher script, syncs the DB, and retries.

**Post-RFP promotion (learning)**: `knowledge-promote.py` reviews gap logs from completed RFPs and suggests new pages, updates to existing pages, and patterns to capture. Human reviews and approves each suggestion.

### Entry Points for New Knowledge

| Source | Tool | Example |
|--------|------|---------|
| Official docs (manual) | Create .md from template | New PCI-DSS amendment |
| API fetch (automated) | pricing-fetcher.py | Monthly AWS price update |
| RFP feedback (post-run) | knowledge-promote.py | Gap found during project |
| Industry update (manual) | Create .md from template | New country regulation |
| Architecture learning | knowledge-promote.py | Reusable pattern from RFP |

---

## SQLite Schema

The database is a derived index — always regenerable from markdown via `sync-db.py`. It makes structured queries fast without parsing markdown at runtime. Dedicated tables exist for domains with structured lookup needs (pricing, compliance, infrastructure). Card-systems and sizing knowledge are indexed in `knowledge_pages` for discovery but read directly from markdown — they don't require structured column queries.

```sql
CREATE TABLE knowledge_pages (
    id              INTEGER PRIMARY KEY,
    path            TEXT UNIQUE,
    domain          TEXT,
    category        TEXT,
    title           TEXT,
    source_url      TEXT,
    captured_date   DATE,
    last_verified   DATE,
    freshness_days  INTEGER,
    tags            TEXT,
    is_stale        BOOLEAN GENERATED ALWAYS AS (
                        julianday('now') - julianday(last_verified) > freshness_days
                    ) STORED
);

CREATE TABLE pricing (
    id              INTEGER PRIMARY KEY,
    page_id         INTEGER REFERENCES knowledge_pages(id),
    provider        TEXT,
    region          TEXT,
    service         TEXT,
    instance_type   TEXT,
    pricing_model   TEXT,
    hourly_price    REAL,
    monthly_price   REAL,
    currency        TEXT DEFAULT 'USD',
    source_url      TEXT,
    verified_date   DATE
);

CREATE TABLE compliance (
    id              INTEGER PRIMARY KEY,
    page_id         INTEGER REFERENCES knowledge_pages(id),
    framework       TEXT,
    country         TEXT,
    requirement_id  TEXT,
    title           TEXT,
    summary         TEXT,
    source_url      TEXT
);

CREATE TABLE infrastructure (
    id              INTEGER PRIMARY KEY,
    page_id         INTEGER REFERENCES knowledge_pages(id),
    provider        TEXT,
    service         TEXT,
    category        TEXT,
    features        TEXT,
    regions         TEXT
);

CREATE TABLE knowledge_gaps (
    id              INTEGER PRIMARY KEY,
    project         TEXT,
    domain          TEXT,
    description     TEXT,
    severity        TEXT,
    resolved        BOOLEAN DEFAULT FALSE,
    resolved_page   TEXT,
    created_date    DATE,
    resolved_date   DATE
);
```

---

## Skill Structure

### 8 Skills (Anthropic SKILL.md Format)

```
skills/
├── apv-orchestrator/SKILL.md    # Sequences stages, checks gates
├── rfp-brainstorm/SKILL.md      # Stage 1 — interactive entry point
├── rfp-compliance/SKILL.md      # Stage 2
├── rfp-architect/SKILL.md       # Stage 3
├── rfp-calculator/SKILL.md      # Stage 4
├── rfp-pricer/SKILL.md          # Stage 5 — iterative scenario engine
├── rfp-generator/SKILL.md       # Stage 6
└── apv-reviewer/SKILL.md        # Stage 7
```

Each skill folder may also contain `examples/` and `tests/` subfolders.

**Note**: Stage 0 (Ingestion/Normalization) is a tool-only stage handled by `normalize.py`, not a skill. It runs as part of the orchestrator's Phase 2.

### Uniform Skill Contract

Every skill prompt follows this structure:

```markdown
---
description: >
  [What the skill does and when to trigger it]
allowed-tools: Read Bash(python3 *) mcp__obsidian-vault__*
argument-hint: "[expected arguments]"
arguments: [named, args]
---

# Stage N: [Skill Name]

## Consumes
[Exact artifact paths to read]

## Knowledge Sources
[Knowledge directories to query via SQLite + direct read]

## Emits
[Exact artifact paths to write]

## Gate Check
[Upstream artifacts that must exist]

## Instructions
[What to do, how to use knowledge, what to cite]

## Gap Handling
[Rules for missing/stale knowledge: halt, assume, or log]
```

### Key Skill Designs

**rfp-brainstorm** accepts 3 input modes:

- **Human brief only**: `/rfp-brainstorm "Payment gateway, Singapore, 500 TPS"` — skill asks clarifying questions, builds context from knowledge base
- **Documents + human direction**: `/rfp-brainstorm "Focus on compliance gaps"` with `input/normalized/` populated — combines both
- **Documents only**: `/rfp-brainstorm` with `input/normalized/` populated — runs autonomously

This makes rfp-brainstorm the interactive entry point where human conversation is expected. Downstream stages run more autonomously because brainstorm captured the intent.

**rfp-pricer** operates as a scenario engine with 4 commands:

- `/rfp-pricer "Single-AZ, 1yr savings"` — generate a new scenario from description
- `/rfp-pricer --budget 50000` — auto-generate 2-3 scenarios fitting a budget target by adjusting commitment model, HA model, instance sizing, or provider
- `/rfp-pricer --compare` — render side-by-side comparison of all scenarios
- `/rfp-pricer --select 2` — lock a scenario as chosen, generate `outputs/05-pricing.md`

Scenario files live in `working/05-scenarios/`:

```
working/05-scenarios/
├── scenario-01-baseline.md
├── scenario-02-savings-plan.md
├── scenario-03-budget-fit.md
├── scenario-comparison.md
└── scenario-selected.md
```

Stages 1-4 produce stable inputs. Stage 5 is where commercial iteration happens. Stages 6-7 finalize based on the selected scenario.

---

## Python Tooling

### 9 Scripts (`tools/`)

| Script | Purpose | Called By |
|--------|---------|----------|
| `sync-db.py` | Parse knowledge/*.md → SQLite | Orchestrator (before pipeline), after any knowledge update |
| `normalize.py` | Convert raw inputs to markdown | Orchestrator (Phase 2) |
| `pricing-lookup.py` | Query pricing from SQLite | rfp-pricer |
| `pricing-fetcher.py` | Fetch fresh pricing from APIs/calculators | Scheduled cron, rfp-pricer (on stale) |
| `freshness.py` | Check entries against freshness_days | rfp-pricer, apv-reviewer |
| `validate-gates.py` | Verify required artifacts exist for a stage | Orchestrator (before each stage) |
| `validate-urls.py` | Check all source URLs are reachable | apv-reviewer |
| `knowledge-promote.py` | Post-RFP: review gap log → suggest new pages | Orchestrator (post-pipeline) |
| `knowledge-stats.py` | Report: coverage, staleness, gap trends | Manual / dashboard |

### Tool Contract

Every tool follows the same interface:

- **Input**: command-line args (paths, flags)
- **Output**: stdout (human-readable) + file artifacts (machine-readable)
- **Exit**: 0 = success, 1 = failure with explanation

### Key Tool Details

**`sync-db.py`** — the bridge between markdown and SQLite:

```bash
python3 tools/sync-db.py --full          # Full rebuild
python3 tools/sync-db.py --incremental   # Only changed files
python3 tools/sync-db.py --domain pricing # Single domain
```

**`pricing-lookup.py`** — what rfp-pricer calls:

```bash
python3 tools/pricing-lookup.py --provider aws --region ap-southeast-1 --instance m6i.xlarge
python3 tools/pricing-lookup.py --from-sizing outputs/04-sizing.md
# Output: JSON with price, source_url, verified_date, is_stale flag
```

**`knowledge-promote.py`** — the feedback loop engine:

```bash
python3 tools/knowledge-promote.py --project <project-path>
# Reads gap-log, assumption-log, approval output, git diffs
# Produces promote-report.md with: new pages needed, updates needed, patterns to capture
```

**`knowledge-stats.py`** — knowledge base health:

```bash
python3 tools/knowledge-stats.py --trend
# Shows: domain coverage, stale count, gap rate across recent RFPs
```

---

## Project Runtime Flow

### Phase 1: Project Initialization

```bash
/apv-orchestrator "acme-corp" "payment-gateway-singapore"
```

Creates project folder scaffold:

```
apv-projects/acme-corp--payment-gateway-singapore--2026-04-29/
├── README.md
├── SUMMARY.md
├── input/raw/ + normalized/
├── working/           # Including 00-gap-log.md (cross-stage) and 05-scenarios/
├── outputs/
├── evidence/pricing/ + compliance/ + source/
├── verification/
└── approvals/
```

### Phase 2: Three Entry Paths

- **Path A (full documents)**: user drops files into `input/raw/` → `normalize.py` → Stage 1 auto mode
- **Path B (documents + human brief)**: user provides text + drops partial docs → Stage 1 combines both
- **Path C (human brief only)**: user describes the RFP verbally → Stage 1 runs as interactive conversation

### Phase 3: Pipeline Execution

Each stage follows the same cycle:

1. **Gate check**: `validate-gates.py --stage N` — halt if upstream artifacts missing
2. **Knowledge load**: query SQLite + read relevant markdown, flag stale entries
3. **Execute**: skill reads inputs, reasons over knowledge, produces outputs
4. **Emit & validate**: write artifacts, `validate-gates.py --verify N` — halt if emit incomplete
5. **Gap log**: append any gaps or assumptions to `working/00-gap-log.md`

Stage execution order: brainstorm → compliance → architecture → sizing → pricing (iterative) → response → review.

### Phase 4: Post-RFP Feedback

```bash
python3 tools/knowledge-promote.py --project <project-path>
```

Reviews gap log, assumption log, reviewer notes, and git diffs. Produces a promote report with new pages needed, updates needed, and patterns to capture. Human reviews and approves each suggestion.

### State Tracking

Orchestrator maintains project state in `README.md`:

```markdown
| Stage | Status | Timestamp |
|-------|--------|-----------|
| Init | ✓ Complete | 2026-04-29 09:00 |
| Brainstorm | ✓ Complete | 2026-04-29 09:15 |
| ... | | |
| Review | ◐ Conditional | 2026-04-29 10:45 |
```

---

## Error Handling

### Type 1: Gate Failures (missing upstream artifacts)

Halt pipeline, report what's missing, wait for human to fix and re-run from failed stage.

### Type 2: Knowledge Failures (stale, missing, or insufficient)

Three severity levels:

- **BLOCKER**: no reasonable assumption possible → halt stage, log with severity=blocker, ask human
- **HIGH**: assumption possible but risky → continue with explicit assumption flag, log to assumption-log, flag in reviewer checklist
- **LOW**: minor gap → continue, log for post-RFP promotion

### Type 3: Tool Failures (scripts crash, APIs down, parse errors)

Halt, show error with suggestion for resolution.

### Edge Cases

**Re-running a single stage**: gate check passes if upstream artifacts exist. Stage re-runs, overwrites its output. Orchestrator detects stale downstream artifacts and prompts re-run of affected stages.

**Parallel RFPs**: each project is an independent folder. Knowledge base updates use file locking on SQLite. Second fetch for the same component sees fresh data and skips.

**Multi-provider RFP**: brainstorm identifies multi-provider scope. Architecture produces variants per provider. Pricer queries all providers and produces comparison table.

**Incomplete RFP**: Path C entry. Brainstorm asks clarifying questions interactively. Gap log will be larger. Reviewer flags higher assumption count.

**Empty knowledge base (first run)**: pipeline runs with extensive gaps logged. First 3-5 RFPs rapidly populate the knowledge base. Alternatively, bulk import from V1 knowledge as bootstrap.

### Recovery Commands

```bash
python3 tools/validate-gates.py --project <path> --all-stages
python3 tools/validate-gates.py --project <path> --check-freshness-chain
/apv-orchestrator --resume <project-path> --from-stage 5
/apv-orchestrator --dry-run <project-path>
```

---

## Two Artifact Surfaces

### Reusable Wiki Surface (`wiki/apv-v2/`)

```
wiki/apv-v2/
├── knowledge/
│   ├── compliance/
│   ├── card-systems/
│   ├── infrastructure/
│   ├── pricing/
│   ├── sizing/
│   └── patterns/
├── skills/           # 8 SKILL.md files
├── tools/            # 9 Python scripts
├── templates/        # Domain templates for new knowledge pages
├── tests/            # Expected input → output test pairs
├── evidence/         # Reusable evidence (promoted from projects)
├── docs/             # Design docs (this spec, authority model, etc.)
└── meta/             # System index
```

### Runtime Project Surface (`apv-projects/`)

```
apv-projects/[customer]--[title]--[date]/
├── README.md + SUMMARY.md
├── input/raw/ + normalized/
├── working/           # Including 05-scenarios/ for pricing iteration
├── outputs/01-07
├── evidence/pricing/ + compliance/ + source/
├── verification/
└── approvals/
```

---

## Implementation Priority

Recommended build order:

1. **Python tooling first**: `sync-db.py`, `validate-gates.py`, `normalize.py` — these are testable without AI
2. **Knowledge bootstrap**: import V1 knowledge into V2 structure, run `sync-db.py`
3. **rfp-brainstorm skill**: the interactive entry point — validates the skill format works
4. **rfp-pricer skill**: the most complex skill (scenario engine) — validates SQLite integration
5. **Remaining skills**: compliance, architect, calculator, generator, reviewer
6. **Orchestrator**: sequences everything — build last because it depends on all stages
7. **knowledge-promote.py**: the feedback loop — build after running a few real RFPs
