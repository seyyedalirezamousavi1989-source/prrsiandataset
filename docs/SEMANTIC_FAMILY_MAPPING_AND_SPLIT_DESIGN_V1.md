# Semantic Family Mapping and Split Design — Phase 6

**Date:** 2026-11-13  
**Status:** candidate-generation tool and CI artifact implemented; human adjudication and final split assignment pending.

## Why this phase exists

A semantic family groups examples that teach substantially the same underlying conversational behavior, even when their wording, entities, or surface scenario differ. Families are the unit used to prevent related examples from leaking across train, validation, test, and challenge splits.

## Candidate generator

Run locally:

```bash
python scripts/propose_semantic_families.py \
  --output reports/semantic_family_candidates.json \
  data/staging/**/*.jsonl
```

The tool:
- normalizes common Persian Arabic/Persian character variants;
- tokenizes the complete conversation, not just the first user turn;
- proposes pairs using lexical Jaccard overlap;
- sorts candidates deterministically and limits review load per sample;
- excludes the separate identity track by default;
- excludes superseded predecessors when their replacement is included;
- rejects duplicate IDs and unresolved predecessor references.

The default threshold is 0.18 with at least three shared content terms and at most five candidate links per sample. These values are triage settings, not calibrated semantic-similarity probabilities.

## Strict human-review boundary

The tool does **not**:
- decide that two records are semantically equivalent;
- assign `semantic_family_id`;
- delete, merge, rewrite, or supersede records;
- assign train/validation/test/challenge splits;
- certify linguistic quality.

Every proposed pair is marked `pending_human_review`. A high lexical score can be a false positive; a low score can miss a true semantic relationship. Reviewers must compare the full conversations and the behavior each example is intended to teach.

## Human adjudication outcomes

For each candidate pair, record one of:
- `same_family`: same underlying target behavior; assign the same family ID;
- `related_distinct`: related topic but meaningfully different skill; retain separate families;
- `not_related`: lexical overlap is incidental;
- `needs_expert_review`: insufficient evidence to decide.

For examples with no candidate link, do not automatically assume uniqueness. Review taxonomy/subskills and sample content when creating the final family inventory.

## Split design

Only after family adjudication:
1. Freeze the family inventory.
2. Assign each entire family to exactly one split.
3. Keep challenge examples separate from ordinary test examples when they represent deliberately difficult edge cases.
4. Check domain, register, language, conversation-length, and skill coverage in each split.
5. Run the guarded exporter; it blocks any family appearing in multiple splits.

Do not use random row-level splitting. Do not split before family IDs have been reviewed.

## CI integration

The dataset-validation workflow now generates `reports/semantic_family_candidates.json` and uploads it alongside the structural validation report as a workflow artifact. This report is a review queue, not a machine-approved family map.

## Current status

No semantic-family IDs or final splits have been written into staging records. Historical staging files remain unchanged. Human review, family adjudication, and split assignment are still required before an Unsloth training export can pass.


## First CI-generated candidate inventory

Workflow run `43476706218` completed successfully:
- 25 regression tests passed.
- 359 active general-language records were scanned.
- The separate identity track was excluded.
- 63 lexical-overlap pairs were emitted for human review.
- No family IDs or splits were assigned.

The candidate report is available as the `staging-validation-and-semantic-review` artifact in [this workflow run](https://github.com/seyyedalirezamousavi1989-source/prrsiandataset/actions/runs/43476706218). These 63 pairs are a review queue, not 63 confirmed duplicates or semantic families.
