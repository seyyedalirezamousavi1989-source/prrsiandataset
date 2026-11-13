# PersianDataset Execution Roadmap

**Status:** Phase 1 completed; Phase 2 in progress (advanced pilot batch v2 added).
**Target:** High-quality Persian conversational SFT data for Qwen3.5-4B with Unsloth.
**Owner context:** Creator/developer: Alireza Mousavi; assistant project: LocalChat Agent; associated research label: AURORA QUANT.

This file is the durable source of truth for project order and continuation. Update the status and next action here whenever a phase is completed. Do not silently skip phases.

## Non-negotiable principles
- Optimize for natural, useful Persian behavior, not raw record count.
- Keep general Persian conversational competence separate from specialist XAUUSD/financial behavior.
- Never claim synthetic data was human-reviewed. Record provenance honestly.
- Keep complete conversations together; do not split turns from one conversation across data splits.
- Do not place large generated corpora or model weights in ordinary Git history. Use versioned artifacts or Git LFS when the corpus grows.
- Do not start model training until the pilot has passed structural, linguistic, duplication, leakage, and held-out evaluation checks.
- Preserve existing pilot files as historical staging inputs; do not overwrite them.

## Ordered phases
### Phase 0 — Repository and baseline freeze
- Read README, schema, blueprint, identity profile, current pilot files, and validator before changing data.
- Record current sample counts, IDs, schema compatibility, and known limitations.
- Keep the initial pilot immutable; add versioned files for new batches.
- Exit gate: repository inventory and baseline are documented.

### Phase 1 — Taxonomy and authoring specification
- Expand the skill taxonomy into explicit subskills and observable success criteria.
- Define coverage targets for colloquial/neutral/formal Persian, short/long turns, single/multi-turn, and noisy/clean inputs.
- Define hard-negative patterns to avoid: translationese, repetitive templates, needless clarification, overexplaining, fabricated facts, and ignoring prior constraints.
- Specify how to author natural conversations and metadata consistently.
- Exit gate: each planned example family has a clear target behavior and review criteria.

### Phase 2 — Curated advanced pilot batches
- Add small, versioned batches of diverse, complete conversations.
- Prioritize underrepresented behaviors found in the current pilot rather than repeating easy one-turn Q&A.
- Include realistic multi-turn context, indirect intent, correction recovery, constraint updates, natural colloquial dialogue, and calibrated uncertainty.
- Keep general Persian data separate from identity and specialist-domain data.
- Exit gate: a materially more diverse pilot exists, with unique IDs and honest provenance.

### Phase 3 — Human linguistic and behavioral review
- Review every candidate for idiomatic Iranian Persian, intent fidelity, context use, accuracy, tone, and constraint adherence.
- Reject or revise awkward, ambiguous-by-accident, repetitive, or factually unsafe examples.
- Set human_reviewed only after an actual human review; otherwise retain unreviewed or machine_checked.
- Exit gate: review status and notes reflect work actually performed.

### Phase 4 — Automated data quality pipeline
- Validate JSONL against schemas/conversation.schema.json.
- Check unique IDs, exact duplicates, near duplicates, empty/abnormal turns, invalid role sequences, language metadata, and provenance.
- Report coverage by domain, subskill, register, turn count, and source.
- Add regression tests for the validator and produce machine-readable reports.
- Exit gate: validation is reproducible and fails loudly on bad data.

### Phase 5 — Leakage-resistant dataset splits
- Group by conversation family, source, prompt template, and semantic near-duplicate cluster before splitting.
- Create train/validation/test plus a separate frozen challenge set.
- Keep identity and XAUUSD evaluation sets separate from general Persian metrics.
- Never use test/challenge prompts or gold answers for training.
- Exit gate: split manifests are reproducible and no related conversation leaks across splits.

### Phase 6 — Base-model evaluation benchmark
- Build a held-out benchmark for Persian fluency, implicit/noisy intent, multi-turn reference resolution, clarification precision, instruction adherence, reasoning, truthfulness, self-correction, and tone adaptation.
- Record exact base-model revision, tokenizer, prompt format, decoding settings, and scoring rubric.
- Include blind review by fluent Persian speakers where possible.
- Exit gate: baseline results are saved before fine-tuning.

### Phase 7 — Qwen3.5-4B tokenizer and serialization audit
- Verify the exact model repository/revision and tokenizer actually used.
- Inspect the model native chat template, role serialization, assistant turn endings, EOS behavior, truncation, and maximum sequence length.
- Measure token-length percentiles and long-conversation truncation risk on the curated corpus.
- Confirm Unsloth support for the exact model and training path; do not guess template tokens.
- Exit gate: a reproducible audit report confirms serialization and sequence-length choices.

### Phase 8 — Unsloth training configuration
- Select the least resource-intensive stable LoRA/QLoRA configuration appropriate to RTX 3060 12GB and 48GB RAM.
- Start with a small smoke test; log peak VRAM, throughput, loss behavior, and saved adapter integrity.
- Keep validation separate from gradient updates; do not train on test/challenge data.
- Exit gate: configuration and environment are reproducible and pass a smoke test.

### Phase 9 — SFT, evaluation, and controlled iteration
- Train only after all prior gates pass.
- Compare base and fine-tuned model using identical prompts and decoding settings.
- Inspect regressions as well as gains; use error analysis to decide the next data batch.
- Save checkpoints, config, dataset manifest, metrics, and evaluation outputs.
- Exit gate: measured improvements justify the checkpoint; otherwise revise data/configuration.

### Phase 10 — Optional preference data
- Only after SFT evaluation, create chosen/rejected pairs for specific observed failure modes.
- Measure pair quality and reviewer agreement before any preference optimization.
- Keep preference optimization optional; do not assume it will improve Persian fluency.
- Exit gate: preference data has clear labels, provenance, and evidence of usefulness.

## Current progress snapshot
- Phase 1 completed: taxonomy and authoring rules are documented in docs/ADVANCED_DATA_AUTHORING_GUIDE.md.
- Phase 2 started: data/staging/advanced_pilot_v2.jsonl adds 15 original curated conversation records. They are staging data, not human-reviewed or final split data.
- Repository specification, schema, identity profile, validator draft, and initial staging pilots were previously added.
- Previously reported staging counts: pilot_v0 15 records, pilot_v1 21 records, identity_v1 8 records. Recount from repository contents before treating these totals as authoritative.
- Existing pilot records were marked train for staging convenience; these are not final training splits.
- No model training has been performed as part of this PersianDataset workflow.
- The current schema represents text-only system, user, and assistant messages; it does not define tool-call structures. Do not add tool-call traces without a deliberate schema version change.

## Exact next action
Continue Phase 2: inspect coverage across all staging batches, identify gaps, then add another small, diverse curated batch. After that, proceed to Phase 3 human linguistic and behavioral review. Do not jump to training.