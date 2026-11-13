# Assistant-Turn-Level SFT Review and Safe Export V1

## Purpose
The record-level exporter is unsafe for correction demonstrations because it serializes every assistant message as a positive target. This stage introduces a separate, read-only annotation file and an opt-in per-turn exporter. It does not modify staging records or grant training approval.

## Annotation JSONL contract
One line per active sample:
- `sample_id`
- `review_status: ai_provisional`
- `reviewer_type: ai`
- `review_model`: exact model/version if known; otherwise null (never guess)
- `annotation_version: assistant_turn_review_v1`
- `assistant_turns`: one entry for every assistant message, keyed by its zero-based `message_index`, with:
  - `label`: `positive_target`, `negative_or_demonstration_only`, or `needs_revision`
  - `rationale`: concise evidence-based explanation
  - `confidence`: number from 0 to 1

Annotations are separate from source JSONL. AI review is provisional and is not human certification.

## Export behavior
Run:
```bash
python scripts/export_turn_level_sft.py --annotations path/to/turn_annotations.jsonl --output-dir build/turn_sft data/staging/*.jsonl
```

The exporter:
- requires annotation coverage for every assistant turn in every active source record;
- emits only `positive_target` turns;
- includes preceding conversation context, so a correction target can learn from the prior exchange without making the flawed turn a target;
- excludes superseded predecessors and rejects annotations for them;
- requires the existing independent human record review, all seven human scores, a valid split, and a semantic family ID;
- rejects family leakage across splits;
- records source and annotation SHA-256 hashes;
- refuses to overwrite output;
- always sets `training_approval=false`.

No automatic AI annotation generation is claimed: this repository workflow has no configured reviewer-model runtime. The annotations must come from a separately executed review pass and remain explicitly provisional. Do not fabricate model identity or reviewer evidence.

## Current limitation
This is the safe export contract and implementation, not a ready-to-run corpus export. Existing 359 active general records do not yet have complete turn-level annotation files, and most remain without human record review, scores, semantic family IDs, or approved splits. Therefore export is expected to block until all independent gates are genuinely satisfied.

## Tests
Unit tests cover flawed-first-answer/correction pairs, positive correction targets, context preservation, negative/needs-revision exclusion, missing annotation coverage, human-gate enforcement, superseded records, provisional status, and family split leakage.
