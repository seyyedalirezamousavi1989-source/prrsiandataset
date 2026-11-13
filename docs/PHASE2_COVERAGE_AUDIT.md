# Phase 2 Coverage Audit — staging snapshot

**Audit date:** 2026-11-13  
**Scope:** pilot_v0.jsonl, pilot_v1.jsonl, identity_v1.jsonl, and advanced_pilot_v2.jsonl, read from the repository default branch before adding v3.

## Structural inventory

| File | Records | JSON parse errors | ID range |
|---|---:|---:|---|
| pilot_v0 | 15 | 0 | fa-pilot-0001–0015 |
| pilot_v1 | 21 | 0 | fa-gen-0016–0036 |
| identity_v1 | 8 | 0 | fa-id-0001–0008 |
| advanced_pilot_v2 | 15 | 0 | fa-adv-0001–0015 |
| **Total before v3** | **59** | **0** | **No duplicate IDs found across these files** |

This was a JSONL parse and inventory check, not full JSON Schema validation or native-speaker review. Existing records use split=train for staging convenience; these are not final dataset splits. The earlier records do not set quality.review_status, so they must not be described as human-reviewed.

## Coverage observations

- Stronger existing coverage: intent inference, ambiguity and clarification, instruction constraints, correction recovery, uncertainty/truthfulness, colloquial typo tolerance, and some multi-turn planning.
- Underrepresented or missing: ordinary small talk and everyday social dialogue; natural Persian-English technical code-switching; polite disagreement and boundary-setting; multi-constraint revisions across several turns; topic switching while retaining a deferred thread; professional email register; practical low-stakes reasoning; and longer conversations with 4–8 messages.
- The 15-record v2 batch contained 12 colloquial, 2 neutral, and 1 formal examples. Formal and mixed-register examples need deliberate expansion.
- Identity examples are a separate domain and should remain separately evaluated rather than inflating general conversational coverage.
- XAUUSD/financial specialist behavior remains outside this general Persian corpus.

## New batch

Added data/staging/advanced_pilot_v3.jsonl with 15 original-curated records (IDs fa-adv-0016 through fa-adv-0030). It targets the gaps above with colloquial, neutral, formal, and mixed-register conversations. All v3 records are staging-only and explicitly marked quality.review_status=unreviewed; provenance is original_curated and created_by=advanced_pilot_v3.

## Remaining gates

1. Conduct actual fluent-Iranian-Persian linguistic and behavioral review (Phase 3); revise or reject awkward/weak examples.
2. Run the repository validator and full JSON Schema validation across all staging files (Phase 4). The validator script is a draft and was not executed as part of this remote repository audit.
3. Deduplicate semantically, not only by exact IDs/payloads; inspect template and phrase repetition.
4. Do not create final train/validation/test/challenge splits or begin Unsloth training until the roadmap gates are satisfied.
