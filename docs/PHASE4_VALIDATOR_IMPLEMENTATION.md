# Phase 4 — Validator Implementation Note

## Changes committed

- Reworked `scripts/validate_dataset.py` using Python standard library only.
- Added record-level checks aligned with the repository conversation schema: required fields, enums, message shape, non-empty content, known roles, metadata, quality fields and score ranges.
- Added conversation-order checks: optional system message only at the beginning, alternating user/assistant turns, and assistant final turn.
- Added corpus-wide checks when all files are passed in one invocation: duplicate IDs, exact duplicate message payloads, and `supersedes_sample_id` references/cycles.
- Added coverage summaries for domain, register, language, split, turn count, provenance and review status.
- Added JSON report output and an optional strict-warning mode.
- Added regression tests in `tests/test_validate_dataset.py`.

## Important compatibility behavior

- Older records without a `quality` object are warnings, not silently upgraded to reviewed.
- Revision records remain separate staging records. Their superseded originals must be excluded from a future final training export; this validator only checks that the referenced original exists.
- Exact duplicate detection is not semantic near-duplicate detection.
- The schema file currently does not close the `metadata` object to additional properties; the validator preserves that flexibility while enforcing known metadata types.

## Verification status

The files were committed to GitHub, but the Python test suite and full-corpus validator have **not yet been executed** in this environment. Do not treat this implementation as runtime-verified. The next action is to run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_dataset.py data/staging/*.jsonl --json-report reports/staging_validation.json
```

Review the report before changing any review statuses or preparing final training data. A nonzero exit or any schema/sequence errors must be investigated rather than bypassed.


## CI automation

A GitHub Actions workflow is now committed at `.github/workflows/validate-dataset.yml`. It runs the unit tests and validates all staging JSONL files on relevant pushes and pull requests, and supports manual dispatch. The workflow file and validator/test files were fetched back from GitHub to confirm their committed contents. The actual Actions run result has not been inspected here; do not treat CI as passing until a run is confirmed in the repository Actions tab.
