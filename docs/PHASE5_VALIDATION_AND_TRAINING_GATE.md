# Phase 5 — Taxonomy Enforcement and Training Readiness Gate

**Date:** 2026-11-13  
**Status:** validator and CI gate implemented; full CI result pending.

## What CI enforces

The regular validation workflow continues to validate every staging JSONL file for structural correctness, metadata, role order, duplicate IDs, exact duplicate conversations, and revision-chain integrity.

A separate strict-taxonomy pass now runs on:
- `data/staging/persian_language_excellence_v4.jsonl`
- `data/staging/persian_language_excellence_v5_part*.jsonl`

These batches were authored under Taxonomy V2 and must use one of its canonical primary domains. Older historical files are intentionally not mass-migrated or made CI-blocking by this new rule. Their taxonomy migration remains a separately reviewed task.

## Training readiness command

Before any training export, run the validator across the exact input files with:

```bash
python scripts/validate_dataset.py --training-ready data/staging/*.jsonl
```

The gate rejects an input set if any record:
- is not explicitly marked `quality.review_status=human_reviewed`;
- lacks any of the seven valid human scores (1–5): intent fidelity, context use, Persian fluency, accuracy, instruction adherence, tone appropriateness, and non-redundancy;
- is a superseded predecessor while its replacement is present in the same input set.

Existing record-level validation also requires reviewer identity and ISO review date for human-reviewed/rejected records. A rejected record cannot pass the human-reviewed status requirement.

The training-ready flag is a gate/check only; it does not create an export, assign final splits, or certify the linguistic quality of a reviewer. Final train/validation/test/challenge assignment and semantic-family leakage checks remain required before training.

## Important current state

The current staging corpus is not expected to pass `--training-ready`: the V5 records remain unreviewed, and historical review decisions are still pending. This is intentional. Do not weaken the gate to make the current corpus pass.

## Local checks

```bash
python -m unittest discover -s tests -v
python scripts/validate_dataset.py data/staging/*.jsonl
python scripts/validate_dataset.py --strict-taxonomy data/staging/persian_language_excellence_v4.jsonl data/staging/persian_language_excellence_v5_part*.jsonl
```

The CI workflow executes the regression tests, full structural validation, and strict taxonomy validation. Check the GitHub Actions run associated with the latest commit before treating this phase as verified.
