# Persian Language Excellence Dataset — Development Plan V1

## Purpose
Develop the general Persian language capability of Qwen3.5-4B through a deliberately diverse, quality-controlled corpus. The target is natural contemporary Iranian Persian, accurate lexical choice, idiomatic sentence construction, pragmatic understanding, coherent multi-turn dialogue, and adaptive response style—not raw record count.

## Scope boundaries
- This is the general Persian language corpus for LocalChat Agent.
- Keep LocalChat identity/creator examples in the separate identity corpus.
- Keep Forex/XAUUSD and other specialist financial behavior in separate domain datasets.
- Do not mix raw-language continued-pretraining text with conversational SFT records; maintain distinct formats, provenance, licenses, and evaluation.
- Preserve all historical staging files. New batches are versioned additions.

## Five capability pillars
1. **Lexical breadth and precision:** contextual synonym selection, semantic nuance, collocations, idioms, proverbs, and register-sensitive word choice.
2. **Natural sentence construction:** Iranian Persian syntax, sentence rhythm, clause linking, varied sentence length, cohesive paragraphs, and meaning-preserving repair of translationese.
3. **Pragmatics and comprehension:** indirect speech acts, humor, sarcasm, politeness, emotional subtext, ambiguity, ellipsis, references, and context-dependent meaning. Avoid overconfident mind-reading.
4. **Response quality:** directness, relevance, calibrated detail, explanation at the requested level, summarization, rewriting, correction recovery, truthfulness, and uncertainty.
5. **Register and style control:** colloquial, neutral, formal, mixed, professional, explanatory, descriptive, and technical Persian; adapt without losing meaning or sounding artificially ornate.

## Data families
- Lexical contrasts and context-sensitive synonym selection.
- Natural collocations and idiomatic phrasing.
- Translationese detection and meaning-preserving rewriting.
- Colloquial/formal/neutral register transformations.
- Idioms, proverbs, slang, and pragmatic interpretation.
- Multi-turn conversations with ellipsis, topic returns, corrections, and changing constraints.
- Tone adaptation, empathy, disagreement, and uncertainty.
- Clear explanations, summaries, comparisons, and concise responses.
- Noisy Persian inputs: typos, missing punctuation, informal spelling, and restrained code-switching.
- Longer connected passages for coherence and paragraph flow.

## Corpus architecture
A. **Conversational SFT:** complete user/assistant conversations with explicit behavioral targets and realistic variation.
B. **Persian language text corpus (separate future track):** licensed/public-domain or user-created Persian prose with source/license metadata. Do not copy copyrighted books/articles without permission. This track is not chat SFT by default.
C. **Evaluation-only challenge set:** held out from training; tests lexical nuance, idiom interpretation, register control, long-context coherence, and translationese resistance.

## Quality rules
- Prefer a strong, varied example over many template substitutions.
- Vary openings, vocabulary, sentence length, dialogue rhythm, and answer shape.
- Include multiple valid phrasings when the task is stylistic; explain meaningful differences rather than asserting one universal wording.
- Preserve intended meaning and all prior constraints.
- Avoid unnatural over-formality, excessive bureaucratic phrasing, forced slang, and needless English calques.
- Do not infer emotion, sarcasm, or intent beyond available context.
- No invented facts or fake citations.
- Avoid repetitive filler and unnecessary follow-up questions.
- Synthetic records remain unreviewed until a human actually reviews them.
- Machine validation checks structure; it does not certify Persian quality.

## Initial scale targets (planning targets, not guarantees)
- First expansion milestone: 1,500 carefully varied conversational records across the five pillars.
- Second milestone: 5,000+ only after coverage analysis and human review capacity are established.
- Longer-term target: 10,000+ only if quality, diversity, and evaluation results justify expansion.
- Keep raw-text corpus targets separate and measure them in tokens, source diversity, and license quality—not record count.

## Suggested coverage monitoring
Use these as initial planning proportions, not rigid per-batch quotas:
- 20% lexical precision and idiomatic usage.
- 20% natural sentence construction and rewriting.
- 20% pragmatic comprehension and context handling.
- 20% response quality, explanation, and correction recovery.
- 20% register/style adaptation and diverse dialogue.
Cross-cut these families with short and long turns, clean and noisy inputs, and single- and multi-turn conversations. Rebalance based on measured gaps.

## Training strategy
- Evaluate the exact Qwen3.5-4B base model before training.
- Consider continued pretraining only if a separately licensed, clean, deduplicated Persian text corpus is available and the exact model/training recipe supports it.
- Use conversational SFT for instruction following, dialogue, register adaptation, and response behavior.
- Do not assume more examples automatically improve fluency. Run controlled experiments against a frozen benchmark.
- Group validation/test/challenge conversations by source, template, and semantic family to prevent leakage.

## Current development batch
`data/staging/persian_language_excellence_v1.jsonl` is the first 24-record expansion batch. `data/staging/persian_language_excellence_v2.jsonl` adds 31 more records (IDs fa-exc-0025 through fa-exc-0055), emphasizing lexical nuance, collocations, ambiguity, pragmatics, concise explanations, summary fidelity, descriptive prose, and style control. Both batches are synthetic candidate data and remain unreviewed. It focuses on lexical nuance, collocations, idioms, natural rewriting, register shifts, pragmatics, noisy input, and multi-turn continuity. All records are synthetic-generated and unreviewed. This is candidate staging data, not training-ready data.

## Acceptance gates
1. JSON/schema/validator checks pass.
2. Coverage and near-duplicate analysis completed.
3. Persian editorial review performed by a fluent human reviewer.
4. Weak or unnatural examples revised or rejected with an audit trail.
5. A held-out challenge set and base-model benchmark exist before training.
6. No final train/validation/test manifest or training run until all project gates are met.
