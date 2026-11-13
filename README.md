# PersianDataset

A quality-first Persian conversational dataset project for supervised fine-tuning and preference optimization of Qwen3.5-4B with Unsloth.

## Mission

Improve the model's ability to:
- Understand natural Persian, including colloquial language, typos, incomplete messages, idioms, and indirect intent.
- Respond in fluent, idiomatic, readable Persian without translation-like phrasing.
- Track multi-turn context and resolve references to earlier messages.
- Ask concise clarification questions when intent is genuinely ambiguous.
- Adapt tone, detail, and register to the user's needs.
- Reason carefully, acknowledge uncertainty, and avoid fabricated claims.
- Follow instructions while maintaining safety and appropriate boundaries.

This project optimizes conversational behavior and Persian-language competence; fine-tuning alone is not a source of unlimited or automatically up-to-date factual knowledge.

## Current target

- Base model: Qwen3.5-4B (exact model revision and chat template must be recorded for each training run).
- Training framework: Unsloth.
- Primary stage: supervised fine-tuning (SFT).
- Optional later stage: preference optimization using separately curated chosen/rejected responses.
- Data format: UTF-8 JSONL using the model's supported conversational message format.

## Quality principles

1. Prefer verified, diverse examples over raw volume.
2. Keep complete multi-turn conversations together.
3. Deduplicate semantically, not only by exact string.
4. Separate train, validation, and test data before training.
5. Prevent benchmark and test leakage.
6. Preserve Persian orthography and Unicode; normalize only with documented, reversible rules.
7. Do not encode invented personal facts or an unconfirmed creator identity.
8. Treat creator identity as descriptive metadata, never as an instruction to obey a person unconditionally.

## Repository map

- `docs/DATASET_BLUEPRINT.md`: dataset taxonomy, curation rules, and acceptance criteria.
- `docs/IDENTITY_PROFILE_TEMPLATE.md`: creator and assistant identity profile awaiting owner-confirmed details.
- `schemas/conversation.schema.json`: canonical conversation record schema.
- `data/{raw,staging,processed}/`: data lifecycle directories (large generated datasets should be stored with Git LFS or external artifact storage).
- `training/`: Unsloth training configuration and evaluation scripts.

## Status

Initial project specification. No training dataset has been generated or model trained yet.
