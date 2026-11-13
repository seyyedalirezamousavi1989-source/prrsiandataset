# Unmatched Record Review — V1

**Purpose:** provide human reviewers with an inventory of active general-language samples that do not appear in any retained lexical candidate pair.

## Interpretation
An unmatched sample is **not** automatically unique, high quality, or a standalone semantic family. The lexical candidate generator uses a threshold and a per-record degree cap; it can miss semantically related samples with different wording. This inventory only identifies records absent from the retained candidate-pair graph.

## Review fields
- `primary_behavior`: summarize the actual target conversational capability in one sentence after reading the full conversation.
- `family_assessment`: keep `unassessed` until a human review; do not infer uniqueness from absence in the pair queue.
- `reviewer`, `review_date`, and `rationale`: complete only after real review.
- `review_status`: initially `pending_human_review`.

## Safety boundaries
- Identity records and superseded predecessors are excluded.
- No staging JSONL is modified.
- No semantic family IDs or train/validation/test splits are assigned.
- This inventory does not certify linguistic quality or training readiness.
- Reviewers should group unmatched records by target behavior, not by surface topic, and flag uncertain cases for expert review.
