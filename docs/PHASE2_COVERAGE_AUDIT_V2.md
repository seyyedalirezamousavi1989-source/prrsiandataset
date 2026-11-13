# Phase 2 Coverage Audit — staging snapshot v2

**Audit date:** 2026-11-13  
**Purpose:** Reassess the complete staging inventory after advanced pilot batches v3–v7. This is a structural inventory and editorial planning aid, not a native-speaker review or full JSON Schema validation.

## Inventory

| File | Records |
|---|---:|
| pilot_v0.jsonl | 15 |
| pilot_v1.jsonl | 21 |
| identity_v1.jsonl | 8 |
| advanced_pilot_v2.jsonl | 15 |
| advanced_pilot_v3.jsonl | 15 |
| advanced_pilot_v4_patch.jsonl | 5 |
| advanced_pilot_v5.jsonl | 15 |
| advanced_pilot_v6.jsonl | 10 |
| advanced_pilot_v7.jsonl | 8 |
| **Total staging records** | **112** |

The fetched inventory before v7 contained 104 records with 104 unique sample IDs and no exact ID collisions. V7 adds 8 records, IDs fa-adv-0061–0068. Its fetched-back checks passed: JSON parsing, unique IDs within the batch, complete user-to-assistant boundaries, original_curated provenance, and unreviewed status.

## Important interpretation

- The 112 count is a staging-record count, not a final independent training-example count.
- The five v4 records are revision records linked to earlier v3 samples via supersedes_sample_id. The old and revised versions must be resolved before final corpus assembly; both must not enter training by default.
- The initial 59 records (pilot_v0, pilot_v1, identity_v1, advanced_pilot_v2) have no quality.review_status field. Do not silently treat them as human-reviewed.
- The v3–v7 advanced batches and v4 patch remain unreviewed. Automated structural checks do not establish Persian fluency or factual quality.
- The identity corpus is a separate evaluation/training domain and should not be used to inflate general conversation coverage.
- Current split=train values are staging labels only. Final splits must be assigned by conversation family and near-duplicate group.
- XAUUSD and specialist financial data remain outside this general Persian corpus.

## Register balance in the pre-v7 inventory

Across the 104 records fetched before v7: colloquial 67, neutral 32, formal 2, mixed 3. This indicates a major formal-register gap. V7 deliberately adds one formal email, one mixed-register simplification, and six varied conversational examples; it does not by itself solve the register imbalance.

## Coverage direction after v7

V7 adds professional email writing, topic switching and deferred-context return, ordinary small talk, respectful disagreement, exact-count output, plain-language adaptation, focused ambiguity clarification, and budget/priority revision.

Next authoring priorities:
1. Increase formal and professional Persian substantially, including emails, notices, reports, requests, and respectful refusals.
2. Expand 6–10-message conversations with topic switching, deferred references, and selective recall.
3. Add diverse real-world dialogue: scheduling, customer support, workplace coordination, learning, and everyday decisions.
4. Increase natural mixed Persian-English examples without gratuitous English.
5. Reduce repeated short one-turn patterns; include realistic follow-up and correction turns.
6. Normalize domain labels and review missing legacy quality metadata before final dataset assembly.

## Remaining gates

1. Native-speaker human review of all candidate records.
2. Full JSON Schema validation and regression-tested validator.
3. Semantic deduplication, including supersedes relationships and template/phrase repetition.
4. Reconcile missing legacy review metadata and separate identity data.
5. Grouped train/validation/test/challenge splits.
6. Base-model benchmark before any Unsloth fine-tuning.

No model training is authorized by this audit.