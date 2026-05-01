---
name: apv-orchestrator
description: Orchestrate the APV V2 RFP response pipeline — scaffold project, sequence stages, enforce gates
version: 2.0
created: 2026-05-01
tags: [apv, v2, orchestrator, pipeline]
---

# APV V2 Orchestrator

## Purpose

Orchestrate a complete RFP response through 7 pipeline stages with artifact governance. Creates the project scaffold, snapshots knowledge, sequences stages with gate checks, and manages the full lifecycle from intake to approval.

## When to Use

- Starting a new RFP response
- Resuming a partially-completed RFP response
- Running a dry-run to check readiness

## Commands

- `apv new [customer] [title]` — create new project, scaffold, and start pipeline
- `apv resume [project-path] --from-stage N` — resume from a specific stage
- `apv dry-run [project-path]` — check knowledge readiness without executing

## Pipeline Phases

### Phase 1: Project Init
1. Create project directory: `apv-projects/[customer]--[title]--[YYYY-MM-DD]/`
2. Scaffold subdirectories:
   ```
   input/raw/          — original customer documents
   input/normalized/   — markdown conversions
   outputs/            — stage output files (01-07)
   working/            — intermediate artifacts
   evidence/           — verification artifacts
   verification/       — freshness/URL checks
   approvals/          — release decisions
   ```
3. Create project `README.md` with status tracking

### Phase 2: Source Intake
1. Copy raw inputs to `input/raw/`
2. Run: `python3 tools/normalize.py --raw-dir input/raw --output-dir input/normalized`
3. Verify normalized files exist: `rfp.md`, `requirements-summary.md`, `volume-summary.md`

### Phase 3: Knowledge Grounding
1. Run: `python3 tools/sync_db.py --knowledge-dir knowledge --db-path apv-v2.sqlite`
2. Run: `python3 tools/knowledge_audit.py --knowledge-dir knowledge`
3. Check freshness — if critical knowledge is STALE, halt and report
4. Snapshot: record git SHA of `knowledge/` → `working/00-knowledge-snapshot.json`
5. **Knowledge is NEVER refreshed mid-pipeline**

### Phase 4: Stage Execution
For each stage 1-7:
1. Run gate check: `python3 tools/validate_gates.py --project . --stage N`
2. If gate fails → halt, report missing artifacts, wait for resolution
3. Invoke skill: `rfp-brainstorm` → `rfp-compliance` → `rfp-architect` → `rfp-calculator` → `rfp-pricer` → `rfp-generator` → `apv-reviewer`
4. Verify stage output was emitted
5. Update project `README.md` with stage completion status

### Phase 5: Verification
1. Run: `python3 tools/validate_urls.py` (when available)
2. Check freshness report: `verification/freshness-report.json`
3. Verify all evidence artifacts linked

### Phase 6: Approval & Release
1. `apv-reviewer` skill produces approval decision
2. Possible outcomes: APPROVED / CONDITIONAL / REJECTED
3. If CONDITIONAL: list required fixes, allow re-run from specific stage
4. If APPROVED: generate `approvals/release-decision.md`

### Phase 7: Post-Pipeline (Knowledge Promotion)
1. Review `working/05-gap-log.md` for knowledge gaps
2. Suggest new knowledge pages from findings
3. Run: `python3 tools/knowledge_promote.py` (when available)

## Gate Check Protocol

Before each stage, the orchestrator runs `validate_gates.py`:
- **PASS**: proceed to stage execution
- **FAIL**: halt pipeline, list missing artifacts, options:
  - Fix missing inputs and resume: `apv resume --from-stage N`
  - Skip stage (NOT recommended, breaks downstream)

## Project README Template

The orchestrator maintains `README.md` in each project directory:

```markdown
# [Customer] — [Title]
Created: YYYY-MM-DD

## Status
| Stage | Status | Completed |
|-------|--------|-----------|
| 0. Intake | ✅ | YYYY-MM-DD HH:MM |
| 1. Brainstorm | 🔄 | — |
| 2. Compliance | ⏳ | — |
| ... | | |

## Knowledge Snapshot
- SHA: [commit hash]
- Stale items: [count]
- Critical gaps: [count]

## Assumptions
- [from working/05-assumption-log.md]

## Gaps
- [from working/05-gap-log.md]
```

## Knowledge Sources

- `knowledge/` — all 7 domains (compliance, card-systems, infrastructure, pricing, commercial, sizing, patterns)
- `apv-v2.sqlite` — derived index for fast lookups

## Tools Used

| Tool | When | Purpose |
|------|------|---------|
| `normalize.py` | Phase 2 | Convert raw inputs |
| `sync_db.py` | Phase 3 | Build knowledge index |
| `knowledge_audit.py` | Phase 3 | Check freshness |
| `validate_gates.py` | Phase 4 | Gate checks per stage |

## Error Handling

| Error | Action |
|-------|--------|
| Gate failure | Halt, report missing artifacts |
| Knowledge STALE (critical) | Halt, require refresh before continuing |
| Knowledge STALE (non-critical) | Log assumption, continue |
| Tool failure | Halt, show error + remediation |
| Stage failure | Halt, allow re-run from failed stage |

## Integration

This skill invokes the following skills in sequence:
- `rfp-brainstorm` (Stage 1)
- `rfp-compliance` (Stage 2)
- `rfp-architect` (Stage 3)
- `rfp-calculator` (Stage 4)
- `rfp-pricer` (Stage 5)
- `rfp-generator` (Stage 6)
- `apv-reviewer` (Stage 7)
