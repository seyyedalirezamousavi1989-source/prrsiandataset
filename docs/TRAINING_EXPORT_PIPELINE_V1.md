# Guarded Conversational SFT Export Pipeline V1

**Date:** 2026-11-13  
**Status:** exporter implemented; no training export generated.

## Purpose

Build per-split JSONL files containing conversational `messages` for later Qwen/Unsloth SFT, but only from records that pass structural validation, canonical Taxonomy V2 validation, human review, and semantic-family split isolation.

## Command

```bash
python scripts/export_training.py \
  --output-dir data/exports/persian_sft_v1 \
  data/staging/persian_language_excellence_v4.jsonl \
  data/staging/persian_language_excellence_v5_part*.jsonl
```

Use explicit, reviewed source files. The output directory must not already exist; the exporter refuses to overwrite it.

## Blocking gates

- All selected records must pass the dataset validator and use canonical primary domains.
- Every active record must have `quality.review_status=human_reviewed`.
- All seven human scores must be integers from 1 through 5.
- Every active record must have a valid split from `train`, `validation`, `test`, or `challenge`.
- Every active record must have `metadata.semantic_family_id`.
- All records in one semantic family must remain in exactly one split.
- Superseded predecessors are excluded from output; their replacement must be present in the selected input set.
- The exporter writes split-specific JSONL files and a manifest containing source files, counts, and gate descriptions.

## Current limitations / readiness

The existing Persian excellence staging records are not export-ready. V5 records remain unreviewed, and the current corpus has not yet received complete human semantic-family IDs or leakage-resistant final split assignments. The exporter is expected to block the current staging corpus. Do not add guessed reviewer scores, semantic-family IDs, or final splits just to make it pass.

The pipeline creates data files only after all gates pass. It does not start model training, select hyperparameters, or claim that a model has been trained.
