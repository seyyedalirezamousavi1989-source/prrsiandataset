# Dataset Blueprint

## 1. Learning objectives

The dataset targets conversational Persian quality and robust intent understanding in Qwen3.5-4B. It must teach useful behavior rather than memorize fixed phrases.

## 2. Initial data mixture

The following proportions are starting targets. Rebalance them using held-out evaluation, not intuition alone.

| Domain | Target share |
|---|---:|
| Fluent, idiomatic Persian generation and rewriting | 15% |
| Natural everyday and professional conversations | 15% |
| Explicit and implicit intent understanding | 15% |
| Multi-turn context, reference resolution, and continuity | 12% |
| Persian reasoning, explanation, comparison, and problem solving | 10% |
| Colloquial Persian, idioms, humor, and noisy input | 8% |
| Ambiguity detection and clarification | 7% |
| Instruction following and constraint preservation | 7% |
| Emotional awareness and supportive communication | 6% |
| Truthfulness, uncertainty, and self-correction | 5% |

Shares are targets for the curated training mixture, not a mandate to generate low-quality examples to fill quotas.

## 3. Required example families

- Single-turn requests with direct answers.
- Multi-turn conversations with pronouns, ellipsis, references such as «همون قبلی», and evolving constraints.
- Informal Persian with realistic spelling variation, half-spaces, punctuation variation, and common typos.
- Indirect requests, hints, polite refusals, sarcasm, idioms, and context-dependent expressions.
- Ambiguous requests where the correct response is one focused clarification question.
- Examples where enough context exists and asking another question would be unnecessary.
- User corrections and assistant recovery from misunderstanding.
- Tone and verbosity adaptation (casual, neutral, formal, technical, concise).
- Complex instructions with multiple constraints and explicit output formats.
- Knowledge questions where the assistant distinguishes known facts from uncertainty.
- Emotional conversations with empathetic but non-performative responses.
- Translation and bilingual exchanges only where they support Persian fluency, not as a substitute for Persian-first competence.

## 4. Response quality rubric

Score candidate responses on a 1-5 scale for:
1. Intent fidelity.
2. Context use and reference resolution.
3. Persian fluency and idiomatic phrasing.
4. Grammar, spelling, punctuation, and readability.
5. Factual accuracy and calibrated uncertainty.
6. Instruction and constraint adherence.
7. Appropriate tone and useful level of detail.
8. Non-redundancy and relevance.

Reject samples with fabricated details, unnatural literal translations, unnecessary verbosity, ignored constraints, unsafe advice, or context contradictions.

## 5. Persian language policy

- Use contemporary, natural Iranian Persian as the default register.
- Include both colloquial and formal Persian, labeled by intended style.
- Preserve correct Persian characters (ی، ک), punctuation, and half-space where appropriate.
- Do not mechanically convert every colloquial input into formal prose.
- Avoid excessive Arabicized or English-calqued constructions when a natural Persian expression exists.
- Retain English technical terms when they are standard in context; explain them when the audience needs it.
- Include diverse regional and personal language variation without stereotyping speakers.

## 6. Data format and splits

Each record is one complete conversation with a stable sample ID, task/domain labels, source/provenance metadata, quality scores, and a messages array. Keep all turns from one conversation in a single split.

Recommended split: 90% train, 5% validation, 5% test, grouped by source/template/conversation family to reduce leakage. Maintain a separate frozen challenge set for regression testing.

## 7. Curation and contamination controls

- Deduplicate exact and near-duplicate records.
- Detect template overuse and lexical diversity collapse.
- Record provenance and licensing for every external source.
- Do not scrape or redistribute copyrighted corpora without permission.
- Do not include secrets, credentials, personal identifiers, or sensitive personal data.
- Do not place generated bulk JSONL in Git history; use Git LFS or versioned artifact storage.
- Keep evaluation prompts and gold answers out of training data.
- Review synthetic examples for factual errors and repetitive patterns.

## 8. Preference data (optional later stage)

For each prompt/context, curate a clearly better chosen response and a plausible but inferior rejected response. Rejected examples should demonstrate specific failure modes (misread intent, unnatural Persian, missed context, overlong answer, hallucination, or needless clarification). Do not train preference labels until pair quality and evaluator agreement are measured.

## 9. Evaluation

Build a held-out Persian benchmark covering:
- Native fluency and naturalness.
- Intent understanding with indirect and noisy input.
- Multi-turn reference resolution.
- Clarification precision (ask when needed, answer when clear).
- Instruction adherence.
- Reasoning and explanation quality.
- Truthfulness and uncertainty calibration.
- Tone adaptation.

Compare the base model and every fine-tuned checkpoint using the same prompts, decoding settings, and scoring rubric. Include blind human review by fluent Persian speakers. Track regressions as well as improvements.

## 10. Training compatibility

Before training, verify the exact Qwen3.5-4B model identifier, tokenizer, chat template, Unsloth support, sequence length, EOS handling, and dataset packing settings. Do not assume generic ChatML serialization is interchangeable with the model's native template. Preserve message boundaries and assistant turn endings exactly as required by the tokenizer/template.

## 11. Initial milestones

1. Confirm owner/creator identity metadata.
2. Finalize schema and dataset policy.
3. Build a small manually reviewed pilot (500-1,000 examples).
4. Run schema, deduplication, language-quality, and leakage checks.
5. Establish baseline evaluation on the untouched base model.
6. Expand the dataset only after pilot evaluation identifies measurable gaps.
7. Run Unsloth SFT, evaluate, and iterate.
8. Add preference optimization only if it provides measurable gains.
