# Phase 4 — Validator Implementation Note

## Implemented and runtime-verified

- Standard-library validator: `scripts/validate_dataset.py`.
- Record-level checks for required fields, enums, message shape/order, metadata, quality fields and score ranges.
- Corpus-wide checks for duplicate IDs, exact duplicate message payloads, and `supersedes_sample_id` references/cycles.
- Coverage summaries and JSON report output.
- Regression tests in `tests/test_validate_dataset.py`.
- GitHub Actions runs tests and validates all staging JSONL files.

## Schema/validator alignment hardening — 2026-11-13

A consistency audit found two gaps: the canonical JSON Schema did not declare `metadata.supersedes_sample_id` used by revision records, and the documented seven-part review rubric was not fully represented in the quality schema. The validator also allowed a record to claim `human_reviewed` or `rejected` without reviewer/date evidence.

Safeguards added:

- Declare `metadata.supersedes_sample_id` as string or null.
- Add `tone_appropriateness` and `non_redundancy` scores (1–5).
- Add optional `quality.reviewer` and `quality.reviewed_at`.
- Require reviewer and ISO date evidence for `human_reviewed` and `rejected` statuses.
- Trigger CI when the canonical schema changes.

These fields remain optional for legacy and unreviewed records. No existing record was rewritten or upgraded.

## Verification

Previous CI run `43464530793` passed 8 regression tests and validated 112 staging records with 0 structural errors. The changes in this commit require a new Actions run; do not claim the new tests pass until that run completes.

Run locally:

```bash
python -m unittest discover -s tests -v
python scripts/validate_dataset.py data/staging/*.jsonl --json-report reports/staging_validation.json
```

## Limits

- Structural validation does not certify Persian fluency, factual correctness, human review, or semantic uniqueness.
- Exact duplicate detection is not semantic near-duplicate detection.
- Revision records remain in staging; a future final manifest must select the active revision and keep related examples in one split.
- Never add reviewer/date fields or mark a record reviewed unless a human actually completed the review.
