# PersianDataset

A quality-first Persian language and conversational-behavior dataset for fine-tuning **Qwen3.5-4B** with **Unsloth**.

## Project identity

- Creator/developer: **Alireza Mousavi**
- Assistant/agent: **LocalChat Agent**
- Associated research project/team label: **AURORA QUANT**

See [Creator and Assistant Identity Profile](docs/IDENTITY_PROFILE_TEMPLATE.md) for the confirmed identity wording and strict anti-hallucination boundaries.

## Mission

Build a carefully curated dataset that improves:
- Natural, fluent, idiomatic Persian, with correct contemporary Iranian usage.
- Understanding of user intent, including indirect, incomplete, colloquial, misspelled, and ambiguous messages.
- Multi-turn context tracking, reference resolution, and continuity.
- Reasoning, explanations, instruction following, and adaptive tone.
- Emotional awareness, self-correction, calibrated uncertainty, and truthful communication.
- Accurate self-identification of LocalChat Agent and its creator when relevant.

The general Persian capability layer is distinct from specialist domain skills. The wider AURORA QUANT workflow may separately train/evaluate XAUUSD analysis using market data supplied by LocalChat Agent. Domain-specific financial behavior must not be mistaken for general language competence.

## Training target

- Base model: Qwen3.5-4B (record exact model revision).
- Framework: Unsloth.
- Primary method: supervised fine-tuning (SFT).
- Optional later phase: preference optimization with curated chosen/rejected pairs.
- Data: UTF-8 JSONL conversation records, converted to the exact native chat template expected by the tokenizer and training stack.

## Quality principles

1. Quality, diversity, and verified usefulness take priority over raw record count.
2. Keep full multi-turn conversations together.
3. Deduplicate exact and near-duplicate examples.
4. Split by conversation/source/template family to prevent leakage.
5. Keep validation, test, and challenge prompts out of training.
6. Preserve Persian Unicode and use documented normalization only.
7. Record provenance and licensing; do not redistribute unlicensed corpora.
8. Never invent creator facts or teach unconditional obedience to the creator.
9. Do not commit large generated datasets or model weights to ordinary Git history; use Git LFS or versioned artifact storage.
10. Validate the exact Qwen3.5 chat template, EOS behavior, packing, and Unsloth compatibility before training.

## Repository map

- `docs/DATASET_BLUEPRINT.md`: taxonomy, data mixture, quality criteria, evaluation, and training plan.
- `docs/IDENTITY_PROFILE_TEMPLATE.md`: confirmed creator and assistant identity.
- `schemas/conversation.schema.json`: canonical conversation schema.
- `data/staging/pilot_v0.jsonl`: first curated Persian pilot.
- `data/staging/identity_v1.jsonl`: creator/agent identity examples.
- `data/{raw,staging,processed}/`: data lifecycle directories.

## Status

Project specification and initial curated pilot are committed. The pilot is not yet a large-scale training corpus, and no model training has been performed by this repository workflow. Expand only after schema validation, human review, deduplication, and baseline evaluation.
