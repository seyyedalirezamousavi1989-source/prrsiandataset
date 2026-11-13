# Persian Language Excellence Semantic Audit V2

**Date:** 2026-11-13  
**Scope:** `persian_language_excellence_v1.jsonl`, `v2.jsonl`, and `v3.jsonl` (85 records; IDs `fa-exc-0001` through `fa-exc-0085`).  
**Status:** Automated lexical triage plus manual contextual inspection of the strongest candidates. This is not a full human linguistic review.

## Integrity checks

- Parsed all three JSONL files successfully.
- 85 records and 85 unique sample IDs.
- No duplicate IDs were found within these three batches.
- V3 contains 30 multi-turn records; all are marked `unreviewed`.
- V3 schema/validator CI passed after correcting two unsupported register labels:
  [Run 43467781974](https://github.com/seyyedalirezamousavi1989-source/prrsiandataset/actions/runs/43467781974).
- CI success confirms structural validation, not linguistic correctness or human approval.

## Method and limitations

Normalized Persian text and compared token-set Jaccard similarity across the combined user/assistant messages. A threshold of 0.23 surfaced two pairs for contextual inspection. This lightweight lexical heuristic is conservative: it can miss paraphrases with low word overlap and can flag examples that share a conversational pattern while teaching different skills. The pairs below were then read in full context.

## Candidate pairs

| Pair | Similarity | Contextual assessment | Recommendation |
|---|---:|---|---|
| `fa-exc-0003` / `fa-exc-0071` | 0.234 | Both teach the idiom «آب پاکی رو دست کسی ریختن» and give essentially the same core definition. V3 adds a follow-up about whether the expression is always negative and a new example. | **Strong near-duplicate candidate.** Keep `fa-exc-0071` as the richer multi-turn teaching example; consider excluding `fa-exc-0003` from the eventual training export, but preserve it in staging/history until human adjudication. |
| `fa-exc-0008` / `fa-exc-0075` | 0.253 | Both interpret ironic remarks about lateness. The first is a single-turn interpretation of a sarcastic compliment; the second explores tone, friendly humor versus complaint, and asks for a witty reply. | **Related, not an exact duplicate.** Keep both provisionally because the second teaches multi-turn pragmatic refinement and response generation. Human reviewer should check whether the overlap is useful reinforcement or unnecessary repetition. |

## Important editorial notes

1. No records were deleted or rewritten as part of this audit.
2. No AI-generated recommendation is recorded as a human decision.
3. The `split=train` labels in staging remain provisional; do not use them as final leakage-resistant splits.
4. Do not export both members of the strong idiom pair blindly. Resolve the pair during human review and final export construction.
5. Continue reviewing at conversation level, not only by isolated messages. Multi-turn records may be intentionally related while testing distinct context-tracking behaviors.

## Next review actions

- Human adjudication required for the two pairs above.
- Expand semantic review to the legacy 112-record staging set and compare across all 197 records, while respecting the identity-data separation and supersedes revision chains.
- After adjudication, run deduplication and leakage-resistant split assignment on the export candidate set; keep the raw staging files immutable.
