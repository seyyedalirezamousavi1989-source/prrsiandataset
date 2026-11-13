# Human Taxonomy Review Batches — V1

## Goal and safeguards
This utility divides the 120-record sample-level taxonomy adjudication packet into manageable CSV files. It preserves every source column and conversation, uses deterministic source-row order, and writes a manifest containing exact sample membership and SHA-256 checksums. It never makes a taxonomy decision.

Keep the original generated master CSV unchanged. The manifest and original batch files are the baseline. To review, copy batch CSVs to a separate working directory and edit only the adjudication columns. Do not edit the manifest or baseline batch files. The merge command currently verifies the baseline batch checksums, so reviewed copies must be placed in a separate reviewed-batches directory and their hashes must be updated through a future explicit review-import workflow; do not manually alter the manifest.

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

Merge checks the unchanged baseline template checksum, every batch checksum, exact batch membership and order, no missing/duplicate/unknown sample IDs, and complete packet coverage. It restores master-template order and validates the merged decisions using the existing adjudication validator. The output is not overwritten. Add `--require-complete` only when every row must have a final human decision; expert-review outcomes are allowed but remain unresolved.

## Important current limitation
V1 intentionally refuses edited baseline batch files. This protects the checksum chain, but means reviewed CSVs cannot yet be imported by the merge command. A subsequent reviewed-batch import feature must explicitly verify each reviewed file against the baseline batch, permit changes only in adjudication columns, then merge. Do not bypass this safeguard by editing the manifest.

No semantic families, splits, quality scores, source staging revisions, or training approval are created.
