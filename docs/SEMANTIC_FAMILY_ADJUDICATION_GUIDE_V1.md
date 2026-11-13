# Semantic Family Adjudication — Human Review Packet V1

**Status:** all candidate pairs are pending; no decisions have been made.

## Review register
The CI workflow generates `reports/SEMANTIC_FAMILY_ADJUDICATION_REGISTER_V1.csv` from the exact candidate report produced in the same run. Each row has a stable packet-local pair ID, both sample IDs, source paths, domains, lexical score, shared terms, and blank reviewer/date/rationale fields. The initial decision is `pending`. Pair IDs are not semantic-family IDs.

## Allowed decisions
- `same_family`: same underlying target behavior; a shared family ID may be assigned only after review.
- `related_distinct`: related topic or scenario, but materially different target skill/behavior.
- `not_related`: overlap is incidental or driven by generic vocabulary/entities.
- `needs_expert_review`: evidence is insufficient or specialist linguistic judgment is needed.

## Review procedure
1. Open both complete conversations from their source JSONL files; never decide from shared terms or Jaccard score alone.
2. State each sample's primary target behavior in one sentence.
3. Compare intent, pragmatic function, required reasoning, response constraints, and expected assistant behavior.
4. Choose `same_family` only when the target behavior is materially the same—not merely because both examples share a topic.
5. For every decision, fill reviewer, ISO date (YYYY-MM-DD), and a concise evidence-based rationale.
6. If uncertain, use `needs_expert_review`; do not force a classification.

## Important limitations
- This is a lexical-overlap triage queue, not a semantic duplicate detector. False positives and false negatives are expected.
- The degree cap means not every possible lexical pair is listed. Absence from this register does not prove uniqueness.
- Pair decisions alone do not define complete families. Unmatched records and connected groups must also be reviewed before family IDs are assigned.
- Do not edit staging records, assign family IDs, assign splits, or approve training during this review.
- Synthetic records remain unreviewed until actual human linguistic review. Structural CI success is not linguistic approval.
