# Persian Language Excellence V5 — Internal Structural and Similarity Audit V1

**Audit date:** 2026-11-13  
**Scope:** `data/staging/persian_language_excellence_v5_part1.jsonl` through `part10.jsonl`  
**Status:** Preliminary automated audit; human linguistic review remains required.

## 1. Inventory and integrity

- Records fetched from GitHub: 100.
- Unique sample IDs: 100.
- Expected ID range: `fa-exc-0161`–`fa-exc-0260`.
- Duplicate IDs: 0.
- Exact duplicate conversation groups within these 100 records: 0.
- Missing/empty message arrays: 0.
- Role alternation errors: 0.
- Review status: all 100 are `unreviewed`.
- The newly committed part 10 file was fetched back and matched the authored content exactly.

Message-count distribution across all ten V5 parts:
- 6 messages: 39
- 8 messages: 44
- 10 messages: 16
- 12 messages: 1

Register distribution:
- neutral: 59
- formal: 15
- mixed: 13
- colloquial: 13

## 2. Taxonomy issue requiring migration review

One legacy record uses a non-canonical primary domain:

- `fa-exc-0190`: domain `mixed`, register `mixed`, subskills `technical_explanation`, `code_switching`.

In taxonomy V2, `mixed` is a register value, not a primary domain. The content explains the distinction between “bug” and “issue” in a technical report. A possible primary-domain mapping could be `lexical_precision` or `explanation_reasoning`, but this audit does not decide the mapping.

**Action:** preserve the historical staging record unchanged. Include it in a controlled taxonomy-migration queue and require a human reviewer to select the canonical primary domain before normalized export. Do not mass-edit historical staging data.

## 3. Similarity candidates — review, do not auto-delete

A simple token-set Jaccard comparison over concatenated conversation text produced two pairs at or above 0.25:

| Pair | Jaccard | Preliminary interpretation |
|---|---:|---|
| `fa-exc-0252` / `fa-exc-0260` | 0.265 | Both address causal inference from sales, advertising and confounding variables. They use different evidence details and response tasks, but may reinforce a similar reasoning pattern. |
| `fa-exc-0189` / `fa-exc-0243` | 0.250 | Both correct an assistant's mistaken weekday for a meeting. The later record adds a reminder-message repair and explicit prevention instruction; nevertheless, the core scenario is close and deserves human adjudication. |

This is a lexical-overlap screen, not semantic equivalence detection. The threshold is intentionally used to surface review candidates, not to certify duplicates. No sample was removed or rewritten.

## 4. Domain distribution observed

| Domain value | Count |
|---|---:|
| context_continuity | 11 |
| adaptive_communication | 16 |
| pragmatics_tone | 11 |
| ambiguity_handling | 9 |
| truthfulness | 10 |
| lexical_precision | 6 |
| sentence_construction | 3 |
| emotional_support | 3 |
| multi_turn_planning | 6 |
| correction_recovery | 6 |
| intent_understanding | 3 |
| colloquial_noisy_input | 3 |
| explanation_reasoning | 5 |
| instruction_following | 6 |
| everyday_dialogue | 1 |
| **non-canonical: mixed** | **1** |

## 5. Recommended next actions

1. Human-review the two similarity candidate pairs and record explicit keep/revise/supersede decisions. Do not delete either pair automatically.
2. Add `fa-exc-0190` to the taxonomy migration queue; preserve its original staging version.
3. Conduct native-speaker linguistic review for naturalness, idiom use, register consistency, and assistant usefulness. Automated structure checks do not certify Persian quality.
4. Run a cross-dataset near-duplicate audit against the original pilot and advanced-pilot records, not only within V5.
5. Create a normalized candidate export only after taxonomy mapping, human review, provenance checks, deduplication adjudication, leakage-resistant splitting, and evaluation preparation.

## 6. Training gate

**V5's 100-record staging milestone is complete, but this batch is not approved for training.** All records remain marked `unreviewed`. This audit is preliminary and must not be represented as human linguistic certification or as proof of semantic uniqueness.
