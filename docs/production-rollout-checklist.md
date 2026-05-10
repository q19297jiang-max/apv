# Production Rollout Checklist

Use this when you want to treat APV V2 as an operator-run production candidate rather than a development sandbox.

## Production Candidate Criteria

Do not start a production rollout unless all of the following are true:

- The full repo test suite is green.
- The platform bootstrap threshold is satisfied for compliance, card systems, infrastructure, pricing, and sizing coverage.
- The knowledge base in `knowledge/` is the intended canonical snapshot source for the run.
- The target project has normalized input artifacts present.
- The project can pass stage gates without manual artifact patching.
- The target project is in `submission` mode, not `draft` mode.
- Approved sales intent exists for the target submission candidate.

Minimum platform threshold from the system design:

| Domain | Minimum for Production Run |
| --- | --- |
| Compliance | PCI-DSS overview plus at least one target-country regulation |
| Card Systems | Payment types relevant to the RFP |
| Infrastructure | At least one cloud provider's core services |
| Pricing | Component catalog for at least one provider, verified within 30 days |
| Sizing | TPS calculator methodology |

## Preflight Commands

Run these from `wiki/apv-v2/` for an existing production candidate.

Preferred one-shot command:

```bash
./bin/apv-preflight --project apv-projects/[customer]--[title]--[date]
```

Structured output for CI or automation:

```bash
./bin/apv-preflight --project apv-projects/[customer]--[title]--[date] --json
```

What it checks:

- full repo test suite
- snapshot boundary integrity
- stage gate contracts across the selected stage range
- stage 7 release readiness, including conditional approval state and manual-review verification blockers
- run authority state, including whether the project remains in draft mode
- commercial override evidence rules at stage 5 when overrides exist
- remediation hint to run `./bin/apv dry-run ... --knowledge-dir knowledge` when snapshot artifacts are missing

Equivalent manual commands:

```bash
/Users/stevenjiang/workspace/mykb/.venv/bin/python -m pytest -q /Users/stevenjiang/workspace/mykb/wiki/apv-v2
```

```bash
python3 tools/validate_gates.py --project apv-projects/[customer]--[title]--[date] --stage 0 --check-snapshot
```

```bash
python3 -c "from pathlib import Path; import sys; sys.path.insert(0, 'tools'); from apv import validate_release_readiness; import json; print(json.dumps(validate_release_readiness(Path('apv-projects/[customer]--[title]--[date]')), indent=2))"
```

If pricing knowledge changed before rollout, refresh and sync it first:

```bash
./bin/apv refresh-pricing --provider aws --knowledge-dir knowledge --sync --check-freshness
```

## Dry-Run Before Release

Before the first production submission for a project, confirm the orchestrator can resolve the project and knowledge boundary cleanly:

```bash
./bin/apv dry-run --project apv-projects/[customer]--[title]--[date] --knowledge-dir knowledge
```

What a healthy dry run should confirm:

- project scaffold is complete
- the knowledge snapshot can be prepared from the current `knowledge/` tree
- stage inputs are discoverable without ad hoc overrides
- readiness blockers surface before downstream stage execution

## Rollout Sequence

Use this order for a live run:

1. Create or verify the project scaffold and normalized inputs.
2. Confirm whether the project is still in `draft` mode or is already a governed `submission` candidate.
3. If the project is still draft-only, run `./bin/apv promote-to-submission ...` and decide whether the promotion path is full rerun or fast-track.
4. Run the dry run and fix any readiness blockers.
5. Execute the pipeline from stage 1 through stage 7, or resume from the earliest affected stage if rerunning.
6. Validate the verification artifacts before approval review.
7. Release only after approval is explicit, no blocking verification issue remains, and the project is submission-eligible.

Typical commands:

```bash
./bin/apv run-pipeline --project apv-projects/[customer]--[title]--[date] --from-stage 1 --to-stage 7
```

```bash
./bin/apv resume --project apv-projects/[customer]--[title]--[date] --from-stage [n]
```

```bash
./bin/apv promote-to-submission --project apv-projects/[customer]--[title]--[date] --owner "[deal-owner]" --strategy "[win-strategy]" --constraint "[constraint]"
```

## Hard Release Blockers

Do not release if any of these conditions is true:

- `verification/source-url-validation.json` is missing or reports invalid URLs.
- `verification/source-url-validation.json` reports `manual_review_required: true`.
- `verification/freshness-report.json` is missing or reports stale required knowledge.
- `approvals/unified-checklist.md` is missing.
- approval artifacts remain `CONDITIONAL` or otherwise non-`APPROVED`.
- stage 6 output contains placeholder text.
- stage 7 approval was attempted without the required verification artifacts.
- the project knowledge snapshot no longer matches the knowledge files captured at snapshot time.
- the project still shows `run_mode = draft` in `working/00-run-context.json`.

## Required Artifacts Before Approval

Approval review should not begin until these artifacts exist:

- `outputs/06-response.md`
- `verification/source-url-validation.json`
- `verification/freshness-report.json`
- `approvals/unified-checklist.md`
- `working/00-run-context.json`
- `input/normalized/sales-brief.md` for governed submission candidates

Treat these as gate inputs, not as optional review aids.

## Snapshot And Knowledge Boundary Checks

The project snapshot is part of the production boundary.

- Snapshot creation must record the knowledge root and per-file knowledge checksums when `knowledge_dir` is supplied.
- Validation must fail if a knowledge file used by the snapshot is changed, removed, or newly added after snapshot creation.
- If the shared knowledge base changes mid-run, start a fresh project snapshot and rerun from the earliest affected stage instead of forcing approval through a stale boundary.

## Recovery Commands

Use the built-in recovery path instead of patching artifacts manually:

```bash
./bin/apv-preflight --project apv-projects/[customer]--[title]--[date] --skip-tests
```

```bash
python3 tools/validate_gates.py --project apv-projects/[customer]--[title]--[date] --stage 0 --check-snapshot
```

```bash
./bin/apv resume --project apv-projects/[customer]--[title]--[date] --from-stage 5
```

```bash
./bin/apv run-stage --project apv-projects/[customer]--[title]--[date] --stage 7
```

If the project is still in draft mode and you intend to submit it:

```bash
./bin/apv promote-to-submission --project apv-projects/[customer]--[title]--[date] --owner "[deal-owner]" --strategy "[win-strategy]" --constraint "[constraint]"
```

Use `run-stage` only when the upstream contract already passes. It is not a bypass around gate enforcement.

## Operator Rules

- Do not patch generated outputs to get past a gate.
- Do not treat review as valid if verification artifacts are absent.
- Do not reuse a stale knowledge snapshot after shared knowledge changes.
- Do not release a project that only passes in draft mode.
- Do not treat stage 7 quality approval as sufficient if the project has not been promoted into governed submission mode.
- Fix the earliest failing stage or boundary, then rerun the affected chain.
