# Unsloth Training Preparation

## Current status

The repository contains a small, manually authored seed/pilot set. It is a development fixture, not a production training corpus. Current files:

- `data/staging/pilot_v0.jsonl`: 15 general Persian examples.
- `data/staging/pilot_v1.jsonl`: 21 additional general Persian examples.
- `data/staging/identity_v1.jsonl`: 8 creator/agent identity examples.

All 44 records are currently marked `train` for staging convenience. **Do not use this pilot as a final train/validation/test split or claim benchmark improvement from it.** Before real training, create source-grouped validation, test, and challenge sets, then freeze them.

## Recommended workflow

1. Run the repository validator:
   ```bash
   python scripts/validate_dataset.py data/staging/pilot_v0.jsonl data/staging/pilot_v1.jsonl data/staging/identity_v1.jsonl
   ```
2. Review examples with fluent Persian speakers. The validator checks structure and simple duplication only; it cannot judge naturalness, factual correctness, or intent fidelity.
3. Deduplicate across all files, not just within each file.
4. Build leakage-resistant splits by conversation family, template, and source.
5. Record the exact Hugging Face model ID/revision, tokenizer revision, Unsloth version, chat template, sequence length, EOS handling, packing policy, seed, and training configuration.
6. Use the model's actual tokenizer/chat template to serialize conversations. Do not assume that a generic ChatML template is correct for every Qwen3.5 checkpoint.
7. Establish a base-model evaluation before SFT; repeat the same frozen benchmark after each checkpoint.
8. Start with conservative LoRA/QLoRA settings supported by the installed Unsloth version and the available GPU memory. Increase context length or batch size only after measuring memory use.
9. Keep general Persian fluency and specialist XAUUSD analysis as separately labeled evaluation tracks. Do not let specialist examples distort the conversational objective.
10. Save training artifacts and checkpoints outside ordinary Git history.

## Dataset record shape

Each JSONL line is one complete conversation object with:
- `sample_id`, `domain`, `subskills`, `language`, `register`, `split`
- `messages`: ordered role/content objects
- `metadata`: provenance and creator information
- optional `quality`: review scores and review status

## Important limitation

No training has been run from this repository. A successful JSONL validation does not prove that the model will improve. Improvement must be established with held-out evaluation and human review.
