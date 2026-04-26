# APV Tests

This directory contains a mix of executable checks, contract-level integration tests, and report artifacts.

## Test Scope Notes

- `run_integration_tests.py` is a contract-level runner. It checks skill-file presence, documented handoff markers, and selected knowledge files.
- It does not execute a full APV RFP project from input through final response.
- Test reports in this directory should describe their scope explicitly as real-pilot, contract-level, or script-level.

## Documentation Guardrail

`test_doc_claims.py` protects a small set of top-level docs from reintroducing unqualified readiness claims.