# Human Review Workspace and Adjudication Validation — V1

## Workflow
1. Download `SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_V1.csv` from the CI artifact.
2. Keep an untouched copy as the baseline template.
3. Review each complete conversation and fill only the adjudication columns:
   - `primary_behavior_assessment`
   - `adjudicated_canonical_domain`
   - `decision`
   - `reviewer`, `review_date`, `adjudication_rationale`
4. Allowed decisions:
   - `accepted_suggestion`: choose exactly the suggested canonical domain.
   - `changed_mapping`: choose a different canonical domain and explain why.
   - `needs_expert_review`: leave the canonical domain blank and explain the unresolved issue.
   - `pending_human_review`: leave all adjudication fields blank.
5. Do not alter sample IDs, source paths, legacy labels, or conversation content.
6. Run the validator locally before submitting the reviewed CSV.

## Validation command
```bash
python scripts/validate_taxonomy_adjudication.py \
  --taxonomy docs/PERSIAN_DATASET_TAXONOMY_V2.md \
  --template reports/SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_V1.csv \
  --reviewed reports/SAMPLE_LEVEL_TAXONOMY_ADJUDICATION_REVIEWED_V1.csv \
  --json-report reports/taxonomy_adjudication_validation.json
```

Add `--require-complete` only when all records must have a final human decision. Expert-review rows are valid unresolved outcomes, but do not count as mapped records.

## Safeguards
- The validator checks exact sample-ID coverage, duplicate IDs, protected-field integrity, canonical domain membership, decision consistency, reviewer/date/rationale, and optional completion.
- It never edits source staging or applies mappings.
- A structurally valid review is not proof of linguistic correctness or training readiness.
- Keep the baseline packet unchanged; do not overwrite it with the reviewed copy.
- No family IDs, final data splits, quality scores, or training approval are produced here.
