# Semantic Near-Duplicate Audit V1

**Date:** 2026-11-13  
**Scope:** All nine current `data/staging/*.jsonl` files (112 records).  
**Purpose:** Identify overlapping examples before final conversation-level splitting. This is a conservative editorial triage, not an embedding-based semantic deduplicator and not a human linguistic review.

## Method

- Parsed all 112 JSONL records from the repository.
- Compared normalized user and assistant message text using token-set Jaccard similarity.
- Reviewed the strongest candidate pairs in their full conversational context.
- Excluded explicit `supersedes_sample_id` revision pairs from the independent-duplicate candidate list.
- No staging record was deleted or modified during this audit.

The heuristic can miss paraphrases and can flag examples that share a topic but teach different behavior. All decisions below remain editorial recommendations.

## Findings

| Candidate pair | Relationship | Recommendation |
|---|---|---|
| `fa-adv-0004` / `fa-gen-0036` | Same Persian sentence translated to the exact same English answer; user instructions differ slightly (polite direct translation vs. explicit output-only constraint). | Keep as a review candidate, not an automatic duplicate. Decide whether the distinct instruction-following label justifies both. If not, retain one representative in the final training manifest. |
| `fa-adv-0024` / `fa-adv-0034` | Explicit revision chain. V4 patch supersedes V3; the revised answer removes the unsupported claim that the meeting is short. | Keep V4 as the active revision; exclude V3 from the final train manifest. Preserve both source records for history. |
| `fa-adv-0029` / `fa-pilot-0014` | Shared discount calculation; V2/V3 advanced example adds a follow-up about shipping and computes the total payable amount. | Retain both provisionally: one tests a single calculation, the other tests context retention and incremental calculation. |
| `fa-adv-0039` / `fa-gen-0020` | Similar formal rewriting task and same initial semantic drift ("saw" becomes "reviewed"). The advanced record adds a user correction and assistant recovery. | Retain the multi-turn correction example only if its purpose is explicitly correction recovery; otherwise revise the pair to avoid teaching the same unsupported inference twice. Human review required. |
| `fa-adv-0007` / `fa-adv-0065` | Both request article titles about sleep, but item counts and formatting constraints differ (three numbered titles vs. four unnumbered titles). | Retain both; they test distinct exact-count and formatting constraints. |
| `fa-adv-0026` / `fa-gen-0024` | Both explain APIs to non-programmers using a restaurant-server analogy; one explicitly requests brevity. | Retain provisionally, but diversify the analogy or explanation in a future batch to reduce template repetition. |

## Structural validation result

The CI run `43464530793` completed successfully on commit `0482673512776fecd1f41e1f2f19d03b2d1a3548`.

- Unit tests: 8 passed.
- Full staging validation: 112 records, 112 unique sample IDs, 0 errors.
- Warnings: 59 legacy records lack `quality.review_status`; they are not treated as human-reviewed.
- All nine staging files were included in the report.
- This confirms structural validation only; it does not certify Persian fluency, factual correctness, or semantic uniqueness.

## Required follow-up

1. Human/editorial decision on the candidate pairs above.
2. Reconcile the 59 legacy review-status warnings without falsely marking them reviewed.
3. Preserve the V4 supersedes relationship when creating the final manifest.
4. Build semantic clusters and group-aware train/validation/test/challenge splits only after editorial decisions.
5. Do not begin fine-tuning yet.
