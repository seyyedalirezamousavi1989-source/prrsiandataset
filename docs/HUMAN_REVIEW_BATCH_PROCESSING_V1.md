# Human Taxonomy Review Batches — V1

## Goal and safeguards
This utility divides the 120-record sample-level taxonomy adjudication packet into manageable CSV files. It preserves every source column and conversation, uses deterministic source-row order, and writes a manifest containing exact sample membership and SHA-256 checksums. It never makes a taxonomy decision.

Keep the original generated master CSV, manifest, and baseline batch files unchanged. Copy the batch CSVs to a separate reviewed-batches directory and edit only the adjudication columns. The merge command verifies baseline files against the manifest, then compares each reviewed copy with its baseline and rejects any protected-field change.

## Split
```bash
python scripts/split_taxonomy_review_batches.py split \
  --template reports/SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_V1.csv \
  --out-dir reports/taxonomy_review_batches_v1 \
  --batch-size 10
```

The output is a manifest and numbered CSVs. Default size is 10; choose another positive integer if desired. The output directory must be absent or empty.

## Merge
```bash
python scripts/split_taxonomy_review_batches.py merge \
  --template reports/SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_V1.csv \
  --manifest reports/taxonomy_review_batches_v1/manifest.json \
  --batch-dir reports/taxonomy_review_batches_v1 \
  --output reports/SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_REVIEWED_V1.csv \
  --taxonomy docs/PERSIAN_DATASET_TAXONOMY_V2.md \
  --json-report reports/taxonomy_review_batch_merge_report.json
```

Before merging, copy all baseline CSVs to `reports/taxonomy_review_batches_v1_reviewed/` and edit those copies. Merge checks the unchanged baseline template and batch checksums, exact batch membership/order, protected-field equality, no missing/duplicate/unknown sample IDs, and complete packet coverage. It restores master-template order and validates the merged decisions using the existing adjudication validator. The output is not overwritten. Add `--require-complete` only when every row must have a final human decision; expert-review outcomes are allowed but remain unresolved.

Baseline CSVs and the manifest are immutable reference inputs. Reviewed CSVs are separate working copies; never rewrite baseline hashes or manifest contents to make a modified baseline appear valid.
