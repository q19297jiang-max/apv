# APV Tests

This directory contains a mix of executable checks, contract-level integration tests, and report artifacts.

## Setup

Use the workspace virtual environment and install the declared test dependency set before running pytest-based checks.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Test Scope Notes

- `run_integration_tests.py` is a contract-level runner. It checks skill-file presence, documented handoff markers, and selected knowledge files.
- It does not execute a full APV RFP project from input through final response.
- `test_runtime_project_fixture.py` is a runtime fixture check. It assembles a canonical `apv-projects/...` folder in a temporary workspace and validates both folder shape and key stage-output markers.
- The runtime fixture check is stronger than documentation-only validation, but it still does not execute the real APV skill chain end-to-end.
- `run_real_pilot_harness.py` is a repeatable real pilot harness. It runs the current source URL and pricing freshness validators against `tests/projects/bbc-bank--credit-card-issuing-2026-04-25/`.
- The real pilot harness validates one repo-tracked sample project under the canonical runtime contract, but it is still not a full skill-execution orchestrator.
- When a local external BBC project exists at `apv-projects/bbc-bank--credit-card-issuing-2026-04-25/`, the harness also compares selected output artifacts (`02-compliance.md`, `05-pricing.md`, `06-response.md`) against that project.
- A future end-to-end layer should validate actual APV generation from source inputs through final outputs.
- Test reports in this directory should describe their scope explicitly as real-pilot, contract-level, or script-level.

## Documentation Guardrail

`test_doc_claims.py` protects a small set of top-level docs from reintroducing unqualified readiness claims.

## Common Commands

```bash
python -m pytest tests/test_runtime_project_fixture.py tests/test_doc_claims.py -q
python -m pytest tests/test_validate_source_urls.py -q
python tests/run_integration_tests.py --verbose
python tests/run_real_pilot_harness.py
```