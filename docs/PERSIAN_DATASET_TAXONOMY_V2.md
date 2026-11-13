# Persian Dataset Taxonomy V2

## Purpose and compatibility

This taxonomy reduces uncontrolled domain-label growth while retaining fine-grained skill labels. It applies to new staging batches beginning with `persian_language_excellence_v4.jsonl`. Historical records remain unchanged; normalization of older records must happen only through separately reviewed, versioned revisions.

The JSON schema currently permits any non-empty string for `domain` and any string values for `subskills`; therefore this document is the project-level controlled vocabulary. CI validation should eventually enforce it.

## Canonical primary domains

Use exactly one primary domain per record:

| Canonical domain | Scope |
|---|---|
| `persian_fluency` | Idiomatic wording, grammar, natural syntax, translationese repair |
| `everyday_dialogue` | Greetings, small talk, conversational rhythm, ordinary social interaction |
| `intent_understanding` | Explicit and implied user goals, speech acts, practical intent |
| `context_continuity` | Multi-turn memory, reference resolution, ellipsis, relevant context retention |
| `ambiguity_handling` | Material ambiguity, disambiguation, focused clarification |
| `multi_turn_planning` | Evolving plans, preference changes, constraint updates |
| `instruction_following` | Format, length, ordering, exclusions, exact constraints |
| `colloquial_noisy_input` | Informal spelling, typos, phonetic input, punctuation and character variation |
| `pragmatics_tone` | Politeness, irony, humor, indirect refusal, disagreement, emotional subtext |
| `lexical_precision` | Near-synonyms, collocations, idioms, connotation, polysemy |
| `sentence_construction` | Sentence rhythm, paragraph cohesion, narrative consistency, rewriting |
| `explanation_reasoning` | Plain-language explanation, comparison, transparent calculations, practical reasoning |
| `truthfulness` | Uncertainty, evidence boundaries, no fabricated recall or current claims |
| `correction_recovery` | Specific error acknowledgement and accurate revision |
| `emotional_support` | Proportionate empathy, nonjudgmental response, practical support |
| `adaptive_communication` | Audience, register, tone, technical level, professional writing and code-switching |

If an example genuinely spans multiple domains, choose the domain that describes the main behavior being trained. Put secondary capabilities in `subskills`.

## Subskill naming rules

- Use concise snake_case labels.
- Prefer existing labels when their meaning fits; do not create a new label for a minor wording variation.
- Use two to four subskills per record where possible; each must describe an observable behavior.
- Avoid vague labels such as `good_response`, `quality`, or `advanced`.
- Keep labels distinct: for example, `indirect_request` is not the same as `indirect_refusal`; `reference_resolution` is not the same as `topic_return`.
- Do not put register or language labels in subskills when those already have dedicated fields.

## Register and language

`register` describes the dominant assistant output style:
- `colloquial`: natural informal Iranian Persian.
- `neutral`: broadly usable contemporary Persian.
- `formal`: professional or formal Persian without unnecessary bureaucratic ornament.
- `mixed`: intentionally combines registers or Persian with English terms/code identifiers in a meaningful way.

`language` describes the conversation's language composition:
- `fa`: Persian conversation; ordinary technical loanwords do not automatically make it bilingual.
- `fa-en`: meaningful Persian-English code-switching or English technical material is central to the example.
- `multilingual`: more than two languages or a genuinely multilingual task.

A record with `language=fa-en` will usually have `register=mixed`, unless the assistant output is consistently formal or neutral and the project explicitly documents that exception. Do not use `fa-en` as a register value.

## Conversation design

- Every record is a complete conversation; messages alternate user/assistant unless a documented system message is intentionally included.
- Prefer meaningful multi-turn progression over padding. A later user turn must add context, revise a constraint, challenge an answer, or request a distinct transformation.
- A substantial portion of new batches should contain 6–10 messages, but short single-turn examples remain useful for concise-answer behavior.
- Include realistic user language: short messages, incomplete clauses, typos, polite and blunt styles, but avoid exaggerated slang.
- Test context retention and selective forgetting: retain relevant constraints and ignore irrelevant details.
- Include examples where the correct response is a concise answer, not an unnecessary question.

## Quality gates for every new batch

1. **Naturalness:** each assistant message should sound like contemporary Iranian Persian appropriate to its context.
2. **Intent fidelity:** solve the user's actual goal, not merely paraphrase it.
3. **Meaning preservation:** never add unsupported details during rewriting or editing.
4. **Conversation coherence:** each turn must connect logically to prior turns.
5. **Constraint tracking:** preserve unchanged requirements after updates.
6. **Truthfulness:** no invented facts, sources, actions, memory, or certainty.
7. **Diversity:** avoid repeated scenario skeletons, opening phrases, answer formulas, and noun-swapping templates.
8. **Metadata accuracy:** correct primary domain, subskills, language, register, provenance, and review status.
9. **Deduplication:** compare both exact text and semantic scenario/response patterns against all active records.
10. **Human review:** synthetic examples remain `unreviewed` until a fluent Persian reviewer actually evaluates them.

## Batch provenance

For `persian_language_excellence_v4.jsonl`:
- IDs: `fa-exc-0086` through `fa-exc-0160`.
- 75 synthetic candidate records.
- All are staging records with `split=train`; this is not a final split assignment.
- All are marked `quality.review_status=unreviewed`.
- This batch does not contain identity or Forex/XAUUSD training examples.
- Automated structural checks do not establish native-speaker quality.

## Historical migration policy

Do not mass-edit historical files to fit this taxonomy. First produce a mapping proposal, review it, then create superseding revisions only where necessary. Preserve source records and record every accepted change in an audit trail.
