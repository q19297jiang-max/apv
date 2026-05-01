---
type: apv-meta
category: review
title: APV V2 Implementation Review
created: 2026-05-01
tags: [apv, v2, review, hygiene, pricing]
---

# APV V2 Implementation Review

## Scope

This review captures the current implemented assurance boundary of APV V2 after the 2026-05-01 hygiene cleanup.

## Verified Knowledge Hygiene State

- `tools/knowledge_audit.py --knowledge-dir knowledge` reports 57 audited knowledge pages, 0 stale, 0 fail.
- `tools/knowledge_stats.py --db apv-v2.sqlite --json` reports 57 indexed knowledge pages, 0 stale, 0 missing source URLs.
- Hidden templates and documentation support files are no longer counted as canonical knowledge pages in the derived index.

## What Is Currently Enforced

### Knowledge Hygiene

- markdown frontmatter/body checks via `tools/knowledge_audit.py`
- freshness-window checks via `tools/freshness.py` and pricing freshness checks via `tools/pricing_fetcher.py`
- source URL format checks via `tools/validate_urls.py`
- derived SQLite rebuild from curated markdown via `tools/sync_db.py`

### Stage Gating

- `tools/validate_gates.py` enforces required upstream artifact presence by stage
- `tools/validate_gates.py --check-snapshot` validates snapshot artifacts, required snapshot fields, and checksum mismatches for tracked boundary files
- `tools/validate_gates.py --check-commercial-overrides` validates `approved_by`, `valid_until`, expiry, and evidence presence when overrides exist

### Pricing Governance

- AWS pricing pages are source-linked and freshness-tagged
- pricing outputs can disclose assumptions, estimates, and evidence links
- MCP is not a runtime dependency for pricing lookup or freshness review

## What Is Only Partially Enforced Or Documented

### Pricing Accuracy

- freshness is metadata-backed, not live-source-backed
- current tooling does not automatically verify catalog values against live AWS calculator output or API responses
- `validate_urls.py` checks URL shape, not remote reachability or content correctness

### Snapshot Model

- the design specifies `00-knowledge-snapshot.json`, project-local snapshot SQLite, checksum boundaries, and mutation rejection
- `validate_gates.py` now implements local snapshot artifact and checksum validation
- current repository still does not wire snapshot creation and validation end-to-end through an orchestrator command path

### Commercial Overrides

- the design and skill contracts define `working/05-commercial-overrides.md`, `approved_by`, `valid_until`, and evidence expectations
- `validate_gates.py` now enforces override metadata and evidence requirements when the commercial override check is invoked
- current repository still does not automatically require that check through every stage-5+ execution path

### Stage Contract Depth

- gate checks currently validate upstream file existence only
- gate checks can now optionally validate snapshot boundaries and commercial override metadata
- there is still no implemented downstream completeness verifier for all stage outputs
- freshness-chain checks and mandatory orchestration wiring remain design targets

## Pricing MCP Boundary

APV V2 currently uses a strict boundary:

- local Python tools plus markdown artifacts are the authoritative pricing runtime
- MCP/web-reader/browser helpers are optional operator conveniences for evidence collection
- lack of MCP subscriptions should not block pricing refresh review; it should only make the workflow more manual

## MCP-Free AWS Pricing Refresh Workflow

1. Open `https://calculator.aws/` manually in a browser.
2. Recreate the exact region, SKU, HA, and commitment configuration.
3. Save screenshots or exports into `evidence/pricing/aws/`.
4. Update `knowledge/pricing/aws-component-catalog.md` with values and verification date.
5. Run `tools/pricing_fetcher.py` to review freshness state.
6. Run `tools/sync_db.py` and `tools/freshness.py` to rebuild and validate the local index.
7. Re-run downstream pricing generation or reviewer checks before release.

## Residual Risks

- AWS pricing freshness can be demonstrated only relative to `last_verified`, not to live AWS state at run time.
- Pricing accuracy still depends on disciplined human refresh and evidence capture.
- The spec currently describes stronger snapshot and commercial-governance guarantees than the code enforces.

## Recommended Next Steps

1. Implement a structured pricing catalog importer or verifier that compares curated catalog values against authoritative sources.
2. Wire snapshot creation and snapshot/commercial validation into a single orchestrator path so they are mandatory rather than opt-in.
3. Add reviewer-stage enforcement for commercial override violations.
4. Add an explicit stage-output completeness verifier rather than file-existence-only gating.