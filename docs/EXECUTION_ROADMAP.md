# PersianDataset Execution Roadmap

**Status:** Phase 4 structural validation is runtime-verified (12 tests passed; 112 records validated with 0 errors). Semantic near-duplicate triage V1 and a complete 112-record human review register are committed. Actual human review and editorial decisions remain pending.
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
- Implemented: schema-aligned record validation, message-order checks, corpus-wide duplicate ID and exact-payload checks, supersedes-reference checks, coverage summary, JSON report output.
- Added regression tests: `tests/test_validate_dataset.py`.
- Verified in GitHub Actions run `43464530793` on commit `0482673512776fecd1f41e1f2f19d03b2d1a3548`: all 12 regression tests passed and all staging files validated with 0 errors.
- The successful report contains 112 records and 112 unique IDs; 59 legacy records still warn because `quality.review_status` is missing. They are not assumed human-reviewed.
- Fixed a Bash variable-escaping defect discovered in the first CI run; the corrected workflow was fetched back and the next run passed.
- Added `docs/SEMANTIC_DEDUP_AUDIT_V1.md` with conservative near-duplicate candidates and editorial recommendations. No records were deleted or changed by this audit.
- Added `docs/HUMAN_REVIEW_REGISTER_V1.md`: inventory of all 112 staging records, review rubric, review procedure, blank decision fields, and first adjudication queue. Snapshot counts: 59 records missing review metadata, 53 explicitly unreviewed, and 8 identity records; identity remains separate.
- Added `docs/NEAR_DUPLICATE_ADJUDICATION_PACKET_V1.md` with the full conversation text for all six candidate pairs, cautious AI-assisted recommendations, and blank human decision/reviewer/date fields. This makes editorial review actionable without pretending that an AI audit is human approval.
- Hardened schema/validator alignment: declared `metadata.supersedes_sample_id`, added the remaining two review rubric scores, and require reviewer plus ISO review date for `human_reviewed`/`rejected` statuses. CI now also triggers on schema changes. New regression coverage added; the latest run is pending after correcting a test-file formatting issue.
- Exit gate: structural validation is reproducible; remaining Phase 4 work is resolving legacy metadata warnings and applying human/editorial duplicate decisions before final split creation.

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
- Phase 1 completed: taxonomy and authoring rules are documented in `docs/ADVANCED_DATA_AUTHORING_GUIDE.md`.
- Phase 2: pilot batches v0–v7 exist as staging inputs; the current inventory previously counted 112 records across nine files, including eight identity records and five revision records. Recount from the repository before using this as an authoritative current total.
- Coverage audit V2 documents register imbalance, legacy missing review metadata, supersedes handling and remaining quality gates.
- Phase 3 human review is still pending. AI-assisted editorial checks are not human review.
- Phase 4 CI is green: 8 tests passed; 112 records and 112 unique IDs; 0 structural errors. See `docs/PHASE4_VALIDATOR_IMPLEMENTATION.md` and the CI run `43464530793`.
- Semantic near-duplicate triage is recorded in `docs/SEMANTIC_DEDUP_AUDIT_V1.md`; it is a heuristic editorial audit, not a full semantic model or human review.
- The complete review queue is in `docs/HUMAN_REVIEW_REGISTER_V1.md`; no records have been marked human-reviewed by this automated preparation.
- No model training has been performed in this workflow.
- Keep identity and specialist XAUUSD data separate from the general Persian dataset.
- Existing `train` values are staging labels, not final leakage-resistant splits.

## Exact next action
Complete the six candidate-pair decisions in `docs/NEAR_DUPLICATE_ADJUDICATION_PACKET_V1.md` with a Persian-fluent human reviewer, then record outcomes in `docs/HUMAN_REVIEW_REGISTER_V1.md`. Continue the full general-Persian review afterward; review identity records separately. Do not change review metadata without actual human review evidence. Do not create final train/validation/test/challenge splits or start training until review and dedup decisions are recorded.
