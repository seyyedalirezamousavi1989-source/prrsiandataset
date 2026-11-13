# Human Review Register V1

**Purpose:** Track native-Persian linguistic and behavioral review without falsely changing source metadata.
**Snapshot:** 2026-11-13; 112 staging records across nine JSONL files.
**Important:** This register is not proof that any record has been human-reviewed. All review decisions start blank. Do not change `quality.review_status` until a human has actually reviewed the record.

## Review rubric

Score each dimension from 1 (reject) to 5 (excellent): intent fidelity, context use, Persian fluency, factual accuracy, instruction adherence, tone appropriateness, and non-redundancy.

- **Accept:** all dimensions >=4; no material factual, linguistic, or instruction-following defect.
- **Revise:** no fatal defect, but one or more dimensions =3 or a specific repair is needed. Preserve the original and create a versioned patch with `supersedes_sample_id`.
- **Reject:** any dimension <=2, materially unnatural Persian, fabricated facts, serious context contradiction, or unsafe/incorrect guidance.
- **Duplicate decision:** keep both / keep one / revision chain / needs adjudication. Topic similarity alone is not enough to reject.
- **Identity records:** review separately; never mix them into general Persian coverage metrics.

## Review procedure

1. Open the source JSONL record and read the complete conversation.
2. Judge the assistant response against the user's actual intent and all previous constraints.
3. Read Persian aloud where useful; flag translationese, unnatural collocations, punctuation, register mismatch, and robotic phrasing.
4. Check factual claims independently when correctness matters; do not reward confident unsupported claims.
5. Record scores, decision, reviewer, date, and a concise reason in a separate review log.
6. Only after a human completes the review may the source record be updated to `human_reviewed`; keep an audit trail and never silently upgrade legacy records.

## Review log template

| sample_id | reviewer | date | intent | context | fluency | accuracy | instructions | tone | non-redundancy | decision | notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

## Inventory

| sample_id | source file | domain | register | language | messages | current review metadata | supersedes | decision |
|---|---|---|---|---|---:|---|---|---|
| `fa-adv-0001` | `data/staging/advanced_pilot_v2.jsonl` | implicit_intent | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0002` | `data/staging/advanced_pilot_v2.jsonl` | contextual_understanding | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0003` | `data/staging/advanced_pilot_v2.jsonl` | ambiguity_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0004` | `data/staging/advanced_pilot_v2.jsonl` | clarification_precision | neutral | fa | 2 | missing | — | pending |
| `fa-adv-0005` | `data/staging/advanced_pilot_v2.jsonl` | colloquial_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0006` | `data/staging/advanced_pilot_v2.jsonl` | correction_recovery | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0007` | `data/staging/advanced_pilot_v2.jsonl` | instruction_following | neutral | fa | 2 | missing | — | pending |
| `fa-adv-0008` | `data/staging/advanced_pilot_v2.jsonl` | noisy_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0009` | `data/staging/advanced_pilot_v2.jsonl` | multi_turn_reasoning | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0010` | `data/staging/advanced_pilot_v2.jsonl` | truthfulness | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0011` | `data/staging/advanced_pilot_v2.jsonl` | adaptive_communication | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0012` | `data/staging/advanced_pilot_v2.jsonl` | emotional_intelligence | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0013` | `data/staging/advanced_pilot_v2.jsonl` | persian_fluency | formal | fa | 2 | missing | — | pending |
| `fa-adv-0014` | `data/staging/advanced_pilot_v2.jsonl` | pragmatics | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0015` | `data/staging/advanced_pilot_v2.jsonl` | instruction_following | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0016` | `data/staging/advanced_pilot_v3.jsonl` | everyday_dialogue | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0017` | `data/staging/advanced_pilot_v3.jsonl` | contextual_understanding | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0018` | `data/staging/advanced_pilot_v3.jsonl` | multi_turn_planning | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0019` | `data/staging/advanced_pilot_v3.jsonl` | colloquial_persian | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0020` | `data/staging/advanced_pilot_v3.jsonl` | pragmatics | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0021` | `data/staging/advanced_pilot_v3.jsonl` | truthfulness | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0022` | `data/staging/advanced_pilot_v3.jsonl` | instruction_following | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0023` | `data/staging/advanced_pilot_v3.jsonl` | ambiguity_resolution | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0024` | `data/staging/advanced_pilot_v3.jsonl` | correction_recovery | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0025` | `data/staging/advanced_pilot_v3.jsonl` | everyday_dialogue | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0026` | `data/staging/advanced_pilot_v3.jsonl` | adaptive_communication | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0027` | `data/staging/advanced_pilot_v3.jsonl` | contextual_understanding | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0028` | `data/staging/advanced_pilot_v3.jsonl` | pragmatics | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0029` | `data/staging/advanced_pilot_v3.jsonl` | reasoning | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0030` | `data/staging/advanced_pilot_v3.jsonl` | persian_fluency | formal | fa | 2 | unreviewed | — | pending |
| `fa-adv-0031` | `data/staging/advanced_pilot_v4_patch.jsonl` | everyday_dialogue | colloquial | fa | 4 | unreviewed | `fa-adv-0016` | pending |
| `fa-adv-0032` | `data/staging/advanced_pilot_v4_patch.jsonl` | multi_turn_planning | colloquial | fa | 6 | unreviewed | `fa-adv-0018` | pending |
| `fa-adv-0033` | `data/staging/advanced_pilot_v4_patch.jsonl` | ambiguity_resolution | colloquial | fa | 4 | unreviewed | `fa-adv-0023` | pending |
| `fa-adv-0034` | `data/staging/advanced_pilot_v4_patch.jsonl` | correction_recovery | colloquial | fa | 4 | unreviewed | `fa-adv-0024` | pending |
| `fa-adv-0035` | `data/staging/advanced_pilot_v4_patch.jsonl` | adaptive_communication | neutral | fa | 2 | unreviewed | `fa-adv-0026` | pending |
| `fa-adv-0036` | `data/staging/advanced_pilot_v5.jsonl` | contextual_understanding | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0037` | `data/staging/advanced_pilot_v5.jsonl` | ambiguity_resolution | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0038` | `data/staging/advanced_pilot_v5.jsonl` | instruction_following | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0039` | `data/staging/advanced_pilot_v5.jsonl` | correction_recovery | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0040` | `data/staging/advanced_pilot_v5.jsonl` | truthfulness | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0041` | `data/staging/advanced_pilot_v5.jsonl` | emotional_support | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0042` | `data/staging/advanced_pilot_v5.jsonl` | colloquial_persian | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0043` | `data/staging/advanced_pilot_v5.jsonl` | multi_turn_planning | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0044` | `data/staging/advanced_pilot_v5.jsonl` | adaptive_communication | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0045` | `data/staging/advanced_pilot_v5.jsonl` | pragmatics | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0046` | `data/staging/advanced_pilot_v5.jsonl` | reasoning_explanation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0047` | `data/staging/advanced_pilot_v5.jsonl` | contextual_understanding | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0048` | `data/staging/advanced_pilot_v5.jsonl` | translation_and_rewriting | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0049` | `data/staging/advanced_pilot_v5.jsonl` | ambiguity_resolution | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0050` | `data/staging/advanced_pilot_v5.jsonl` | truthfulness | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0051` | `data/staging/advanced_pilot_v6.jsonl` | contextual_understanding | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0052` | `data/staging/advanced_pilot_v6.jsonl` | correction_recovery | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0053` | `data/staging/advanced_pilot_v6.jsonl` | truthfulness | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0054` | `data/staging/advanced_pilot_v6.jsonl` | pragmatics | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0055` | `data/staging/advanced_pilot_v6.jsonl` | multi_turn_planning | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0056` | `data/staging/advanced_pilot_v6.jsonl` | adaptive_communication | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0057` | `data/staging/advanced_pilot_v6.jsonl` | colloquial_persian | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0058` | `data/staging/advanced_pilot_v6.jsonl` | reasoning_explanation | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0059` | `data/staging/advanced_pilot_v6.jsonl` | instruction_following | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0060` | `data/staging/advanced_pilot_v6.jsonl` | truthfulness | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0061` | `data/staging/advanced_pilot_v7.jsonl` | professional_writing | formal | fa | 2 | unreviewed | — | pending |
| `fa-adv-0062` | `data/staging/advanced_pilot_v7.jsonl` | topic_management | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0063` | `data/staging/advanced_pilot_v7.jsonl` | everyday_dialogue | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0064` | `data/staging/advanced_pilot_v7.jsonl` | pragmatics | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0065` | `data/staging/advanced_pilot_v7.jsonl` | instruction_following | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0066` | `data/staging/advanced_pilot_v7.jsonl` | adaptive_communication | mixed | fa | 2 | unreviewed | — | pending |
| `fa-adv-0067` | `data/staging/advanced_pilot_v7.jsonl` | ambiguity_resolution | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0068` | `data/staging/advanced_pilot_v7.jsonl` | multi_turn_planning | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-id-0001` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-id-0002` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-id-0003` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-id-0004` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-id-0005` | `data/staging/identity_v1.jsonl` | identity | colloquial | fa | 2 | missing | — | pending |
| `fa-id-0006` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-id-0007` | `data/staging/identity_v1.jsonl` | identity | colloquial | fa | 2 | missing | — | pending |
| `fa-id-0008` | `data/staging/identity_v1.jsonl` | identity | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0001` | `data/staging/pilot_v0.jsonl` | intent_understanding | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0002` | `data/staging/pilot_v0.jsonl` | ambiguity_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0003` | `data/staging/pilot_v0.jsonl` | contextual_understanding | colloquial | fa | 4 | missing | — | pending |
| `fa-pilot-0004` | `data/staging/pilot_v0.jsonl` | persian_fluency | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0005` | `data/staging/pilot_v0.jsonl` | noisy_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0006` | `data/staging/pilot_v0.jsonl` | instruction_following | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0007` | `data/staging/pilot_v0.jsonl` | emotional_intelligence | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0008` | `data/staging/pilot_v0.jsonl` | truthfulness | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0009` | `data/staging/pilot_v0.jsonl` | colloquial_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0010` | `data/staging/pilot_v0.jsonl` | adaptive_communication | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0011` | `data/staging/pilot_v0.jsonl` | self_correction | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0012` | `data/staging/pilot_v0.jsonl` | multi_turn_reasoning | neutral | fa | 4 | missing | — | pending |
| `fa-pilot-0013` | `data/staging/pilot_v0.jsonl` | ambiguity_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0014` | `data/staging/pilot_v0.jsonl` | reasoning | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0015` | `data/staging/pilot_v0.jsonl` | intent_understanding | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0016` | `data/staging/pilot_v1.jsonl` | intent_understanding | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0017` | `data/staging/pilot_v1.jsonl` | contextual_understanding | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0018` | `data/staging/pilot_v1.jsonl` | ambiguity_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0019` | `data/staging/pilot_v1.jsonl` | instruction_following | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0020` | `data/staging/pilot_v1.jsonl` | persian_fluency | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0021` | `data/staging/pilot_v1.jsonl` | persian_fluency | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0022` | `data/staging/pilot_v1.jsonl` | colloquial_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0023` | `data/staging/pilot_v1.jsonl` | contextual_understanding | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0024` | `data/staging/pilot_v1.jsonl` | adaptive_communication | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0025` | `data/staging/pilot_v1.jsonl` | reasoning | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0026` | `data/staging/pilot_v1.jsonl` | truthfulness | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0027` | `data/staging/pilot_v1.jsonl` | self_correction | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0028` | `data/staging/pilot_v1.jsonl` | instruction_following | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0029` | `data/staging/pilot_v1.jsonl` | emotional_intelligence | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0030` | `data/staging/pilot_v1.jsonl` | ambiguity_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0031` | `data/staging/pilot_v1.jsonl` | noisy_persian | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0032` | `data/staging/pilot_v1.jsonl` | multi_turn_reasoning | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0033` | `data/staging/pilot_v1.jsonl` | persian_fluency | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0034` | `data/staging/pilot_v1.jsonl` | intent_understanding | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0035` | `data/staging/pilot_v1.jsonl` | truthfulness | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0036` | `data/staging/pilot_v1.jsonl` | instruction_following | neutral | fa | 2 | missing | — | pending |

## First adjudication queue

- `fa-adv-0004` vs `fa-gen-0036`: decide whether the explicit output-only constraint warrants retaining both translation examples.
- `fa-adv-0024` vs `fa-adv-0034`: revision chain; V4 supersedes V3. Do not train on both.
- `fa-adv-0029` vs `fa-pilot-0014`: retain provisionally; one is multi-turn and adds shipping cost.
- `fa-adv-0039` vs `fa-gen-0020`: assess whether correction recovery justifies keeping the multi-turn example; inspect initial semantic drift.
- `fa-adv-0007` vs `fa-adv-0065`: retain provisionally; exact count and formatting constraints differ.
- `fa-adv-0026` vs `fa-gen-0024`: retain provisionally but note repeated restaurant-server analogy.

## Review status cautions

- 59 legacy records currently have no `quality.review_status`; missing is not equivalent to reviewed.
- Later pilot batches are marked `unreviewed` and must remain so until an actual human review occurs.
- This register includes eight identity records; review them separately from the general conversational corpus.
- Do not create final train/validation/test/challenge splits from this staging register.
- Do not begin Unsloth fine-tuning until review, duplicate adjudication, grouped splitting, and base-model benchmark gates are complete.

## Inventory totals

- Total staging records: 112
- Records with missing review status: 59
- Records explicitly marked unreviewed: 53
- Identity records: 8
- Review decisions recorded in this document: 0 (all pending).