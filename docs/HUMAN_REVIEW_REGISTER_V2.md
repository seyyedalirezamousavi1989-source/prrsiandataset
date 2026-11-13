# Human Review Register V2 — Complete 197-Record Inventory

**Snapshot:** 2026-11-13  
**Scope:** all 12 JSONL staging files fetched from the repository default branch.  
**Purpose:** provide a complete, auditable queue for native-Persian linguistic and behavioral review.  
**Important:** this is an inventory and blank decision register, not evidence that any record has been human-reviewed. No human scores or decisions have been fabricated.

## 1. Inventory status

| Measure | Count |
|---|---:|
| Total records | 197 |
| Unique sample IDs | 197 |
| General Persian records | 189 |
| Separate identity records | 8 |
| General records active after excluding superseded predecessors | 184 |
| Explicit revision predecessors | 5 |
| Records with `quality.review_status=unreviewed` | 138 |
| Records with missing review status | 59 |
| Human decisions recorded in this register | 0 |

The five superseding revisions are preserved as separate records and linked to their predecessors. The predecessor and replacement must not both be included in a final training export unless there is an explicit, reviewed reason. Staging files remain immutable during this review process.

## 2. Review rubric

Score each dimension from 1 (unacceptable) to 5 (excellent):

1. Intent fidelity — answers the actual request without changing its meaning.
2. Context use — retains prior turns, constraints, references and corrections.
3. Persian fluency — natural contemporary Iranian Persian, syntax, collocations, rhythm and punctuation.
4. Factual accuracy — correct, appropriately qualified and not fabricated.
5. Instruction adherence — follows format, length, language and other constraints.
6. Tone/register — fits the social situation and requested level of formality.
7. Non-redundancy — adds distinct learning value rather than repeating an existing example.

Suggested decision rules:
- **Accept:** every dimension >=4 and no material defect.
- **Revise:** no fatal defect, but at least one dimension is 3 or a specific repair is required. Create a versioned patch and link it with `supersedes_sample_id`; do not silently overwrite history.
- **Reject:** any dimension <=2, material unnaturalness, factual error, meaning drift, fabricated context, or serious instruction failure.
- **Duplicate adjudication:** keep both / keep one / revision chain / needs adjudication. Similar topic alone is not sufficient reason to remove a record.

A reviewer must record actual scores, their identity, date and evidence-based notes. Automated checks, model suggestions and this inventory do not count as human review.

## 3. Review workflow

1. Read the complete conversation, not just the first user message.
2. Evaluate every assistant turn against the user intent and all retained constraints.
3. Read Persian aloud where useful. Flag translationese, stiff constructions, unnatural collocations, inconsistent register and robotic phrasing.
4. Independently verify factual claims where correctness matters.
5. Compare candidate near-duplicates in context; distinguish same topic from same teaching objective.
6. Record a decision in a separate human review log. Keep the original staging data unchanged until an approved versioned patch is prepared.
7. Review identity samples in their own track. Do not combine identity coverage statistics with general Persian-language coverage.
8. Do not finalize train/validation/test/challenge splits until duplicate families and revision chains are resolved. Split by semantic family to reduce leakage.

## 4. Review log template

| sample_id | reviewer | date | intent | context | fluency | accuracy | instructions | tone | non-redundancy | decision | evidence / notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

## 5. General Persian corpus — 189 records

All decisions are currently **pending**. The `review_status` column reports source metadata only.

| sample_id | source file | domain | subskills | register | language | messages | source review_status | supersedes | human decision |
|---|---|---|---|---|---|---:|---|---|---|
| `fa-adv-0001` | `data/staging/advanced_pilot_v2.jsonl` | implicit_intent | indirect_request, practical_goal_inference | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0002` | `data/staging/advanced_pilot_v2.jsonl` | contextual_understanding | multi_turn, constraint_preservation, reference_resolution | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0003` | `data/staging/advanced_pilot_v2.jsonl` | ambiguity_resolution | material_ambiguity, single_clarification | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0004` | `data/staging/advanced_pilot_v2.jsonl` | clarification_precision | answer_when_sufficient, avoid_needless_questions | neutral | fa | 2 | missing | — | pending |
| `fa-adv-0005` | `data/staging/advanced_pilot_v2.jsonl` | colloquial_persian | idiom_interpretation, pragmatic_uncertainty | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0006` | `data/staging/advanced_pilot_v2.jsonl` | correction_recovery | accept_correction, revise_output, no_defensiveness | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0007` | `data/staging/advanced_pilot_v2.jsonl` | instruction_following | format_constraint, exact_item_count | neutral | fa | 2 | missing | — | pending |
| `fa-adv-0008` | `data/staging/advanced_pilot_v2.jsonl` | noisy_persian | typo_tolerance, intent_recovery, polite_response | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0009` | `data/staging/advanced_pilot_v2.jsonl` | multi_turn_reasoning | constraint_update, partial_plan_revision, context_retention | colloquial | fa | 4 | missing | — | pending |
| `fa-adv-0010` | `data/staging/advanced_pilot_v2.jsonl` | truthfulness | uncertainty, no_fake_memory, request_context | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0011` | `data/staging/advanced_pilot_v2.jsonl` | adaptive_communication | audience_adaptation, plain_language, technical_explanation | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0012` | `data/staging/advanced_pilot_v2.jsonl` | emotional_intelligence | empathy, nonjudgmental_support, one_practical_step | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0013` | `data/staging/advanced_pilot_v2.jsonl` | persian_fluency | natural_rewrite, meaning_preservation, register_control | formal | fa | 2 | missing | — | pending |
| `fa-adv-0014` | `data/staging/advanced_pilot_v2.jsonl` | pragmatics | sarcasm_detection, contextual_interpretation, calibrated_uncertainty | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0015` | `data/staging/advanced_pilot_v2.jsonl` | instruction_following | negative_constraint, scope_control, concise_answer | colloquial | fa | 2 | missing | — | pending |
| `fa-adv-0016` | `data/staging/advanced_pilot_v3.jsonl` | everyday_dialogue | natural_small_talk, conversational_turn_taking | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0017` | `data/staging/advanced_pilot_v3.jsonl` | contextual_understanding | ellipsis_resolution, context_retention, minimal_follow_up | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0018` | `data/staging/advanced_pilot_v3.jsonl` | multi_turn_planning | multiple_constraint_tracking, schedule_revision, preserve_unchanged_constraints | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0019` | `data/staging/advanced_pilot_v3.jsonl` | colloquial_persian | natural_code_switching, informal_input_recovery, meaning_preservation | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0020` | `data/staging/advanced_pilot_v3.jsonl` | pragmatics | polite_disagreement, tone_adaptation, deescalation | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0021` | `data/staging/advanced_pilot_v3.jsonl` | truthfulness | technical_uncertainty, evidence_seeking, avoid_false_diagnosis | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0022` | `data/staging/advanced_pilot_v3.jsonl` | instruction_following | multi_constraint_output, format_adherence, negative_constraint | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0023` | `data/staging/advanced_pilot_v3.jsonl` | ambiguity_resolution | contextual_disambiguation, answer_when_context_suffices, avoid_redundant_question | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0024` | `data/staging/advanced_pilot_v3.jsonl` | correction_recovery | specific_error_acknowledgement, constraint_repair, non_defensive_revision | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0025` | `data/staging/advanced_pilot_v3.jsonl` | everyday_dialogue | practical_social_advice, context_sensitive_response, concise_helpfulness | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0026` | `data/staging/advanced_pilot_v3.jsonl` | adaptive_communication | technical_explanation, audience_adaptation, plain_language | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0027` | `data/staging/advanced_pilot_v3.jsonl` | contextual_understanding | topic_shift_detection, selective_context_retention, multi_turn_dialogue | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0028` | `data/staging/advanced_pilot_v3.jsonl` | pragmatics | indirect_refusal, boundary_setting, polite_tone | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0029` | `data/staging/advanced_pilot_v3.jsonl` | reasoning | simple_calculation, show_assumptions, practical_explanation | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0030` | `data/staging/advanced_pilot_v3.jsonl` | persian_fluency | register_conversion, meaning_preservation, natural_professional_writing | formal | fa | 2 | unreviewed | — | pending |
| `fa-adv-0031` | `data/staging/advanced_pilot_v4_patch.jsonl` | everyday_dialogue | natural_small_talk, conversational_turn_taking | colloquial | fa | 4 | unreviewed | `fa-adv-0016` | pending |
| `fa-adv-0032` | `data/staging/advanced_pilot_v4_patch.jsonl` | multi_turn_planning | multiple_constraint_tracking, schedule_revision, preserve_unchanged_constraints, focused_clarification | colloquial | fa | 6 | unreviewed | `fa-adv-0018` | pending |
| `fa-adv-0033` | `data/staging/advanced_pilot_v4_patch.jsonl` | ambiguity_resolution | contextual_disambiguation, answer_when_context_suffices, avoid_redundant_question, truthful_context_boundary | colloquial | fa | 4 | unreviewed | `fa-adv-0023` | pending |
| `fa-adv-0034` | `data/staging/advanced_pilot_v4_patch.jsonl` | correction_recovery | specific_error_acknowledgement, constraint_repair, non_defensive_revision, meaning_preservation | colloquial | fa | 4 | unreviewed | `fa-adv-0024` | pending |
| `fa-adv-0035` | `data/staging/advanced_pilot_v4_patch.jsonl` | adaptive_communication | technical_explanation, audience_adaptation, plain_language, natural_persian | neutral | fa | 2 | unreviewed | `fa-adv-0026` | pending |
| `fa-adv-0036` | `data/staging/advanced_pilot_v5.jsonl` | contextual_understanding | reference_resolution, constraint_preservation, multi_turn_followup | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0037` | `data/staging/advanced_pilot_v5.jsonl` | ambiguity_resolution | material_ambiguity_detection, single_focused_question, avoid_assumption | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0038` | `data/staging/advanced_pilot_v5.jsonl` | instruction_following | exact_format, word_limit, negative_constraint | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0039` | `data/staging/advanced_pilot_v5.jsonl` | correction_recovery | specific_acknowledgement, meaning_preservation, minimal_revision | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0040` | `data/staging/advanced_pilot_v5.jsonl` | truthfulness | uncertainty_calibration, avoid_false_current_claim, evidence_request | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0041` | `data/staging/advanced_pilot_v5.jsonl` | emotional_support | proportionate_empathy, practical_next_step, avoid_generic_reassurance | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0042` | `data/staging/advanced_pilot_v5.jsonl` | colloquial_persian | typo_tolerance, intent_recovery, nonjudgmental_response | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0043` | `data/staging/advanced_pilot_v5.jsonl` | multi_turn_planning | plan_revision, preserve_constraints, dependency_awareness | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0044` | `data/staging/advanced_pilot_v5.jsonl` | adaptive_communication | beginner_explanation, analogy, technical_accuracy | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0045` | `data/staging/advanced_pilot_v5.jsonl` | pragmatics | polite_boundary_setting, indirect_refusal, tone_adaptation | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0046` | `data/staging/advanced_pilot_v5.jsonl` | reasoning_explanation | transparent_calculation, stepwise_reasoning, answer_verification | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0047` | `data/staging/advanced_pilot_v5.jsonl` | contextual_understanding | multi_turn_context, selective_information_retention, followup_answer | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0048` | `data/staging/advanced_pilot_v5.jsonl` | translation_and_rewriting | meaning_preservation, register_adaptation, idiomatic_translation | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0049` | `data/staging/advanced_pilot_v5.jsonl` | ambiguity_resolution | contextual_inference, avoid_unnecessary_clarification, concise_response | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0050` | `data/staging/advanced_pilot_v5.jsonl` | truthfulness | capability_boundary, no_false_memory_claim, helpful_alternative | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0051` | `data/staging/advanced_pilot_v6.jsonl` | contextual_understanding | long_context_retention, selective_recall, constraint_preservation | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0052` | `data/staging/advanced_pilot_v6.jsonl` | correction_recovery | error_acknowledgement, scope_correction, no_defensiveness | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0053` | `data/staging/advanced_pilot_v6.jsonl` | truthfulness | diagnostic_uncertainty, evidence_based_troubleshooting, safe_next_step | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0054` | `data/staging/advanced_pilot_v6.jsonl` | pragmatics | sarcasm_detection, context_sensitivity, avoid_overconfident_emotion_reading | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0055` | `data/staging/advanced_pilot_v6.jsonl` | multi_turn_planning | dependency_management, schedule_revision, preserve_goal | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0056` | `data/staging/advanced_pilot_v6.jsonl` | adaptive_communication | audience_adaptation, plain_language, technical_precision | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0057` | `data/staging/advanced_pilot_v6.jsonl` | colloquial_persian | natural_code_switching, register_preservation, meaning_clarity | mixed | fa-en | 4 | unreviewed | — | pending |
| `fa-adv-0058` | `data/staging/advanced_pilot_v6.jsonl` | reasoning_explanation | comparison, explicit_tradeoffs, decision_support | neutral | fa | 4 | unreviewed | — | pending |
| `fa-adv-0059` | `data/staging/advanced_pilot_v6.jsonl` | instruction_following | ordered_steps, scope_limitation, beginner_friendly_guidance | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-adv-0060` | `data/staging/advanced_pilot_v6.jsonl` | truthfulness | missing_context_awareness, no_fabricated_recall, request_minimal_context | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0061` | `data/staging/advanced_pilot_v7.jsonl` | professional_writing | formal_email, clear_request | formal | fa | 2 | unreviewed | — | pending |
| `fa-adv-0062` | `data/staging/advanced_pilot_v7.jsonl` | topic_management | topic_switching, deferred_thread, context_retrieval | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-adv-0063` | `data/staging/advanced_pilot_v7.jsonl` | everyday_dialogue | natural_small_talk, reciprocal_turn_taking | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0064` | `data/staging/advanced_pilot_v7.jsonl` | pragmatics | respectful_disagreement, reasoned_alternative | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0065` | `data/staging/advanced_pilot_v7.jsonl` | instruction_following | strict_length_control, exact_count, no_preface | neutral | fa | 2 | unreviewed | — | pending |
| `fa-adv-0066` | `data/staging/advanced_pilot_v7.jsonl` | adaptive_communication | plain_language, audience_adaptation | mixed | fa | 2 | unreviewed | — | pending |
| `fa-adv-0067` | `data/staging/advanced_pilot_v7.jsonl` | ambiguity_resolution | ambiguity_detection, minimal_clarification | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-adv-0068` | `data/staging/advanced_pilot_v7.jsonl` | multi_turn_planning | budget_constraint, priority_revision, tradeoff_explanation | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-exc-0001` | `data/staging/persian_language_excellence_v1.jsonl` | lexical_precision | synonym_discrimination | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0002` | `data/staging/persian_language_excellence_v1.jsonl` | lexical_precision | collocation, word_choice | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0003` | `data/staging/persian_language_excellence_v1.jsonl` | idiomatic_persian | idiom_meaning | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0004` | `data/staging/persian_language_excellence_v1.jsonl` | natural_sentence_construction | translationese_repair, meaning_preservation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0005` | `data/staging/persian_language_excellence_v1.jsonl` | register_adaptation | formal_to_colloquial | mixed | fa | 2 | unreviewed | — | pending |
| `fa-exc-0006` | `data/staging/persian_language_excellence_v1.jsonl` | register_adaptation | colloquial_to_formal | formal | fa | 2 | unreviewed | — | pending |
| `fa-exc-0007` | `data/staging/persian_language_excellence_v1.jsonl` | pragmatics | indirect_meaning, uncertainty | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0008` | `data/staging/persian_language_excellence_v1.jsonl` | pragmatics | sarcasm, contextual_interpretation | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0009` | `data/staging/persian_language_excellence_v1.jsonl` | conversational_fluency | natural_follow_up, turn_taking | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-exc-0010` | `data/staging/persian_language_excellence_v1.jsonl` | contextual_understanding | ellipsis_resolution, context_retention | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0011` | `data/staging/persian_language_excellence_v1.jsonl` | natural_rewrite | style_variants, semantic_precision | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0012` | `data/staging/persian_language_excellence_v1.jsonl` | lexical_precision | semantic_contrast, contextual_word_choice | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0013` | `data/staging/persian_language_excellence_v1.jsonl` | writing_quality | remove_redundancy, concise_editing | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0014` | `data/staging/persian_language_excellence_v1.jsonl` | ambiguity_resolution | single_question, material_ambiguity | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0015` | `data/staging/persian_language_excellence_v1.jsonl` | tone_adaptation | proportionate_empathy, practical_support | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0016` | `data/staging/persian_language_excellence_v1.jsonl` | colloquial_persian | slang_interpretation, register_awareness | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0017` | `data/staging/persian_language_excellence_v1.jsonl` | formal_persian | formal_expression, politeness | formal | fa | 2 | unreviewed | — | pending |
| `fa-exc-0018` | `data/staging/persian_language_excellence_v1.jsonl` | explanation_style | simple_explanation, semantic_contrast | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0019` | `data/staging/persian_language_excellence_v1.jsonl` | noisy_persian | typo_tolerance, intent_recovery | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0020` | `data/staging/persian_language_excellence_v1.jsonl` | multi_turn_style_control | style_constraint_update, context_retention | colloquial | fa | 4 | unreviewed | — | pending |
| `fa-exc-0021` | `data/staging/persian_language_excellence_v1.jsonl` | idiomatic_persian | proverb_interpretation, nonliteral_language | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0022` | `data/staging/persian_language_excellence_v1.jsonl` | persian_style | sentence_rhythm, avoid_stiffness | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0023` | `data/staging/persian_language_excellence_v1.jsonl` | semantic_precision | near_synonym_choice, contextual_fit | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0024` | `data/staging/persian_language_excellence_v1.jsonl` | conversation_repair | misunderstanding_recovery, meaning_preservation | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0025` | `data/staging/persian_language_excellence_v2.jsonl` | lexical_precision | semantic_nuance | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0026` | `data/staging/persian_language_excellence_v2.jsonl` | lexical_precision | meaning_contrast | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0027` | `data/staging/persian_language_excellence_v2.jsonl` | collocation_quality | natural_collocation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0028` | `data/staging/persian_language_excellence_v2.jsonl` | lexical_precision | connotation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0029` | `data/staging/persian_language_excellence_v2.jsonl` | natural_sentence_construction | remove_nominalization | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0030` | `data/staging/persian_language_excellence_v2.jsonl` | natural_sentence_construction | paragraph_cohesion | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0031` | `data/staging/persian_language_excellence_v2.jsonl` | natural_sentence_construction | meaning_preservation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0032` | `data/staging/persian_language_excellence_v2.jsonl` | natural_sentence_construction | ambiguity_resolution | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0033` | `data/staging/persian_language_excellence_v2.jsonl` | pragmatics | polite_refusal | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0034` | `data/staging/persian_language_excellence_v2.jsonl` | pragmatics | indirect_request | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0035` | `data/staging/persian_language_excellence_v2.jsonl` | pragmatics | irony_detection | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0036` | `data/staging/persian_language_excellence_v2.jsonl` | pragmatics | politeness_interpretation | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0037` | `data/staging/persian_language_excellence_v2.jsonl` | contextual_understanding | constraint_tracking | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0038` | `data/staging/persian_language_excellence_v2.jsonl` | contextual_understanding | multi_turn_revision | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0039` | `data/staging/persian_language_excellence_v2.jsonl` | response_quality | answer_calibration | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0040` | `data/staging/persian_language_excellence_v2.jsonl` | response_quality | explanation_depth_control | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0041` | `data/staging/persian_language_excellence_v2.jsonl` | response_quality | simple_explanation | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0042` | `data/staging/persian_language_excellence_v2.jsonl` | response_quality | summary_fidelity | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0043` | `data/staging/persian_language_excellence_v2.jsonl` | conversation_repair | correction_acceptance | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0044` | `data/staging/persian_language_excellence_v2.jsonl` | register_adaptation | natural_formality | formal | fa | 2 | unreviewed | — | pending |
| `fa-exc-0045` | `data/staging/persian_language_excellence_v2.jsonl` | register_adaptation | neutral_to_colloquial | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0046` | `data/staging/persian_language_excellence_v2.jsonl` | writing_quality | descriptive_writing | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0047` | `data/staging/persian_language_excellence_v2.jsonl` | writing_quality | narrative_coherence | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0048` | `data/staging/persian_language_excellence_v2.jsonl` | noisy_persian | typo_tolerance | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0049` | `data/staging/persian_language_excellence_v2.jsonl` | multilingual_persian | code_switching | mixed | fa | 2 | unreviewed | — | pending |
| `fa-exc-0050` | `data/staging/persian_language_excellence_v2.jsonl` | lexical_precision | polysemy | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0051` | `data/staging/persian_language_excellence_v2.jsonl` | pragmatics | speech_act | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0052` | `data/staging/persian_language_excellence_v2.jsonl` | response_quality | criteria_based_comparison | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0053` | `data/staging/persian_language_excellence_v2.jsonl` | conversation_coherence | topic_shift | colloquial | fa | 2 | unreviewed | — | pending |
| `fa-exc-0054` | `data/staging/persian_language_excellence_v2.jsonl` | natural_sentence_construction | parallel_structure | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0055` | `data/staging/persian_language_excellence_v2.jsonl` | lexical_precision | intensity_scale | neutral | fa | 2 | unreviewed | — | pending |
| `fa-exc-0056` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | multi_turn_reference, constraint_tracking | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0057` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | long_context, reference_resolution | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0058` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | changing_constraints, format_adaptation | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0059` | `data/staging/persian_language_excellence_v3.jsonl` | pragmatics | indirect_request, politeness | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0060` | `data/staging/persian_language_excellence_v3.jsonl` | sentence_construction | paragraph_coherence, editing | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0061` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | ellipsis, multi_turn | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0062` | `data/staging/persian_language_excellence_v3.jsonl` | lexical_precision | register_shift, word_choice | formal | fa | 6 | unreviewed | — | pending |
| `fa-exc-0063` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | uncertainty, avoid_assumption | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0064` | `data/staging/persian_language_excellence_v3.jsonl` | sentence_construction | narrative_coherence, tense_consistency | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0065` | `data/staging/persian_language_excellence_v3.jsonl` | pragmatics | sarcasm, context_dependence | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0066` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | long_context, multi_constraint | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0067` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | correction_recovery, factual_fidelity | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0068` | `data/staging/persian_language_excellence_v3.jsonl` | register_style | audience_adaptation, plain_language | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0069` | `data/staging/persian_language_excellence_v3.jsonl` | pragmatics | ambiguous_reply, contextual_inference | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0070` | `data/staging/persian_language_excellence_v3.jsonl` | sentence_construction | paragraph_revision, cohesion | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0071` | `data/staging/persian_language_excellence_v3.jsonl` | lexical_precision | idiom_meaning, literal_vs_figural | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0072` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | instruction_memory, format_constraints | neutral | fa | 8 | unreviewed | — | pending |
| `fa-exc-0073` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | contradiction_detection, clarification | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0074` | `data/staging/persian_language_excellence_v3.jsonl` | register_style | tone_control, sensitive_feedback | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0075` | `data/staging/persian_language_excellence_v3.jsonl` | pragmatics | humor_interpretation, non_literal_language | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0076` | `data/staging/persian_language_excellence_v3.jsonl` | sentence_construction | summarization, information_preservation | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0077` | `data/staging/persian_language_excellence_v3.jsonl` | lexical_precision | collocation, naturalness | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0078` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | multi_turn_planning, changing_preference | neutral | fa | 8 | unreviewed | — | pending |
| `fa-exc-0079` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | error_acknowledgement, repair | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0080` | `data/staging/persian_language_excellence_v3.jsonl` | register_style | formal_to_colloquial, meaning_preservation | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0081` | `data/staging/persian_language_excellence_v3.jsonl` | pragmatics | contextual_ellipsis, dialogue_interpretation | colloquial | fa | 6 | unreviewed | — | pending |
| `fa-exc-0082` | `data/staging/persian_language_excellence_v3.jsonl` | sentence_construction | long_form_coherence, paragraph_writing | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0083` | `data/staging/persian_language_excellence_v3.jsonl` | lexical_precision | polysemy, context_disambiguation | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0084` | `data/staging/persian_language_excellence_v3.jsonl` | response_quality | scope_control, no_unrequested_additions | neutral | fa | 6 | unreviewed | — | pending |
| `fa-exc-0085` | `data/staging/persian_language_excellence_v3.jsonl` | contextual_comprehension | long_context, contradiction_resolution | neutral | fa | 8 | unreviewed | — | pending |
| `fa-pilot-0001` | `data/staging/pilot_v0.jsonl` | intent_understanding | implicit_intent, concise_response | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0002` | `data/staging/pilot_v0.jsonl` | ambiguity_resolution | clarification, reference_resolution | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0003` | `data/staging/pilot_v0.jsonl` | contextual_understanding | multi_turn, constraint_retention | colloquial | fa | 4 | missing | — | pending |
| `fa-pilot-0004` | `data/staging/pilot_v0.jsonl` | persian_fluency | rewrite, natural_persian | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0005` | `data/staging/pilot_v0.jsonl` | noisy_persian | typo_tolerance, intent_understanding | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0006` | `data/staging/pilot_v0.jsonl` | instruction_following | format_constraints, exact_output | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0007` | `data/staging/pilot_v0.jsonl` | emotional_intelligence | empathy, nonjudgmental_support | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0008` | `data/staging/pilot_v0.jsonl` | truthfulness | uncertainty, no_hallucination | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0009` | `data/staging/pilot_v0.jsonl` | colloquial_persian | idiom, pragmatics | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0010` | `data/staging/pilot_v0.jsonl` | adaptive_communication | audience_adaptation, simple_explanation | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0011` | `data/staging/pilot_v0.jsonl` | self_correction | acknowledge_error, repair | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0012` | `data/staging/pilot_v0.jsonl` | multi_turn_reasoning | constraint_tracking, planning | neutral | fa | 4 | missing | — | pending |
| `fa-pilot-0013` | `data/staging/pilot_v0.jsonl` | ambiguity_resolution | minimal_clarification, avoid_guessing | colloquial | fa | 2 | missing | — | pending |
| `fa-pilot-0014` | `data/staging/pilot_v0.jsonl` | reasoning | stepwise_explanation, arithmetic | neutral | fa | 2 | missing | — | pending |
| `fa-pilot-0015` | `data/staging/pilot_v0.jsonl` | intent_understanding | implicit_request, editing_scope | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0016` | `data/staging/pilot_v1.jsonl` | intent_understanding | indirect_request, summarization | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0017` | `data/staging/pilot_v1.jsonl` | contextual_understanding | pronoun_resolution, multi_turn | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0018` | `data/staging/pilot_v1.jsonl` | ambiguity_resolution | clarify_one_key_detail | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0019` | `data/staging/pilot_v1.jsonl` | instruction_following | length_control, format | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0020` | `data/staging/pilot_v1.jsonl` | persian_fluency | natural_rewrite, register_adaptation | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0021` | `data/staging/pilot_v1.jsonl` | persian_fluency | natural_rewrite, avoid_translationese | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0022` | `data/staging/pilot_v1.jsonl` | colloquial_persian | pragmatics, tone_detection | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0023` | `data/staging/pilot_v1.jsonl` | contextual_understanding | correction_recovery, context_retention | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0024` | `data/staging/pilot_v1.jsonl` | adaptive_communication | explain_for_beginner, analogy | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0025` | `data/staging/pilot_v1.jsonl` | reasoning | compare, criteria_based | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0026` | `data/staging/pilot_v1.jsonl` | truthfulness | uncertainty, ask_for_source | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0027` | `data/staging/pilot_v1.jsonl` | self_correction | acknowledge, correct | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0028` | `data/staging/pilot_v1.jsonl` | instruction_following | multiple_constraints, preserve_scope | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0029` | `data/staging/pilot_v1.jsonl` | emotional_intelligence | empathy, practical_support | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0030` | `data/staging/pilot_v1.jsonl` | ambiguity_resolution | answer_when_clear, no_unnecessary_question | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0031` | `data/staging/pilot_v1.jsonl` | noisy_persian | typo_tolerance, intent_recovery | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0032` | `data/staging/pilot_v1.jsonl` | multi_turn_reasoning | constraint_update, plan_revision | colloquial | fa | 4 | missing | — | pending |
| `fa-gen-0033` | `data/staging/pilot_v1.jsonl` | persian_fluency | natural_dialogue, concise | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0034` | `data/staging/pilot_v1.jsonl` | intent_understanding | implicit_complaint, offer_repair | colloquial | fa | 2 | missing | — | pending |
| `fa-gen-0035` | `data/staging/pilot_v1.jsonl` | truthfulness | distinguish_fact_from_opinion | neutral | fa | 2 | missing | — | pending |
| `fa-gen-0036` | `data/staging/pilot_v1.jsonl` | instruction_following | language_constraint, no_extra_text | neutral | fa | 2 | missing | — | pending |

## 6. Separate identity track — 8 records

Identity samples are reviewed separately and are not part of general Persian-language coverage metrics.

| sample_id | source file | domain | subskills | register | language | messages | source review_status | supersedes | human decision |
|---|---|---|---|---|---|---:|---|---|---|
| `fa-id-0001` | `data/staging/identity_v1.jsonl` | identity | assistant_self_identification | neutral | fa | 2 | missing | — | pending |
| `fa-id-0002` | `data/staging/identity_v1.jsonl` | identity | creator_identification | neutral | fa | 2 | missing | — | pending |
| `fa-id-0003` | `data/staging/identity_v1.jsonl` | identity | project_association, creator_identification | neutral | fa | 2 | missing | — | pending |
| `fa-id-0004` | `data/staging/identity_v1.jsonl` | identity | base_model_distinction | neutral | fa | 2 | missing | — | pending |
| `fa-id-0005` | `data/staging/identity_v1.jsonl` | identity | identity_boundary, non_human | colloquial | fa | 2 | missing | — | pending |
| `fa-id-0006` | `data/staging/identity_v1.jsonl` | identity | unknown_creator_details, truthfulness | neutral | fa | 2 | missing | — | pending |
| `fa-id-0007` | `data/staging/identity_v1.jsonl` | identity | relevance, avoid_unprompted_intro | colloquial | fa | 2 | missing | — | pending |
| `fa-id-0008` | `data/staging/identity_v1.jsonl` | identity | project_label_boundary, truthfulness | neutral | fa | 2 | missing | — | pending |

## 7. Coverage snapshot (descriptive only)

The following is a count of the current `domain` labels across general records. It is not a quality score and does not imply balanced coverage.

- `pragmatics`: 18
- `contextual_understanding`: 12
- `lexical_precision`: 12
- `ambiguity_resolution`: 11
- `response_quality`: 11
- `instruction_following`: 10
- `truthfulness`: 9
- `adaptive_communication`: 8
- `colloquial_persian`: 7
- `contextual_comprehension`: 7
- `persian_fluency`: 6
- `natural_sentence_construction`: 6
- `correction_recovery`: 5
- `noisy_persian`: 5
- `multi_turn_planning`: 5
- `sentence_construction`: 5
- `everyday_dialogue`: 4
- `register_adaptation`: 4
- `intent_understanding`: 4
- `multi_turn_reasoning`: 3
- `emotional_intelligence`: 3
- `reasoning`: 3
- `writing_quality`: 3
- `register_style`: 3
- `reasoning_explanation`: 2
- `idiomatic_persian`: 2
- `conversation_repair`: 2
- `self_correction`: 2
- `implicit_intent`: 1
- `clarification_precision`: 1
- `emotional_support`: 1
- `translation_and_rewriting`: 1
- `professional_writing`: 1
- `topic_management`: 1
- `conversational_fluency`: 1
- `natural_rewrite`: 1
- `tone_adaptation`: 1
- `formal_persian`: 1
- `explanation_style`: 1
- `multi_turn_style_control`: 1
- `persian_style`: 1
- `semantic_precision`: 1
- `collocation_quality`: 1
- `multilingual_persian`: 1
- `conversation_coherence`: 1

## 8. Known adjudication queue from the full semantic audit

Start human comparison with these groups; do not treat automated recommendations as verdicts:

- Very high overlap: `fa-adv-0004` / `fa-gen-0036`.
- Meaning-preservation concern: `fa-adv-0039` / `fa-gen-0020`; inspect the older target for “saw” versus “reviewed” drift.
- Natural-rewrite cluster: `fa-adv-0008`, `fa-adv-0042`, `fa-exc-0019`, `fa-pilot-0001`.
- Ambiguous-reference cluster: `fa-adv-0003`, `fa-adv-0067`, `fa-pilot-0002`.
- Idiom pair: `fa-exc-0003` / `fa-exc-0071`.
- Irony/humor pair: `fa-exc-0008` / `fa-exc-0075`.

See [Full Dataset Semantic Audit V1](FULL_DATASET_SEMANTIC_AUDIT_V1.md) for contextual notes and additional pairs.

## 9. Export and training gates

- Do not export superseded predecessors alongside their replacements by default.
- Do not merge identity records into the general Persian SFT corpus.
- Do not mark records human-reviewed based on automated validation or model-generated suggestions.
- Do not use the staging `split=train` values as final leakage-resistant splits.
- Do not begin Unsloth fine-tuning until human review, duplicate adjudication, grouped split design, base-model benchmark, tokenizer/serialization checks and training configuration review are complete.

**Register integrity:** 197 rows were generated from the fetched staging JSONL records. Every sample ID is unique in this snapshot. Human review decisions remain blank/pending.
