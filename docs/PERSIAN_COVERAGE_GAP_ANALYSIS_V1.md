# Persian Language Coverage Gap Analysis V1

**Repository:** `seyyedalirezamousavi1989-source/prrsiandataset`  
**Scope:** all 12 current JSONL staging files on the default branch  
**Purpose:** identify evidence-based coverage gaps before creating another SFT batch  
**Status:** analytical report only; no dataset records changed, accepted, deleted, or reclassified

## 1. Executive summary

The repository contains **197 parseable records** with unique IDs across 12 staging files. Of these, **8 belong to the separate identity track** and are excluded from general Persian-language coverage.

The general track contains **189 records**. Five records are explicit superseding revisions of five earlier records. For a non-duplicative coverage view, the working active set is therefore **184 general records** (189 minus 5 superseded predecessors). This is a staging-level accounting view, not a finalized training export.

The corpus already has useful breadth in pragmatic interpretation, contextual understanding, lexical precision, response quality, and instruction following. The main issue is not simply a lack of examples: it is **uneven depth and inconsistent taxonomy**. There are 46 distinct domain labels and a very long tail of one-off subskill labels. Consequently, raw tag counts can overstate breadth or make related capabilities look artificially separate.

The clearest quantitative gaps are:
- Formal and mixed-register coverage is small compared with colloquial and neutral.
- Most active examples are single-turn; long multi-turn conversations exist but are not yet the dominant training shape.
- Spoken-style variation, regional varieties, robust orthographic/noisy-input recovery, and broad code-switching are not yet demonstrated at meaningful depth.
- Several advanced language abilities appear only as isolated examples or narrow subskill labels; they need contrastive and varied contexts rather than repeated near-identical prompts.
- There is no final train/validation/test split: every staging record currently says `split=train`.

**Recommendation:** do not create a large generic batch yet. First build a targeted next batch around the prioritized gaps in Section 7, then run human linguistic review and a normalized coverage report.

## 2. Counting method and caveats

All 12 files were fetched from the repository and parsed as JSONL:
- 197 records parsed successfully.
- 0 JSONL parse failures.
- 197 distinct sample IDs in the current inventory.
- Identity track: 8 records, kept separate.
- General track: 189 records.
- 5 records carry `metadata.supersedes_sample_id`; their five predecessors are excluded from the active general view.
- Active general working set: 184 records.

The active set is used for the coverage distributions below. A record is considered active when its ID is not referenced as the predecessor of a superseding record.

Important limitations:
1. Domain and subskill tags are self-reported metadata, not an independent assessment of actual linguistic performance.
2. Counts measure record assignment, not quality, difficulty, or successful model learning.
3. The current taxonomy is fragmented: equivalent or closely related concepts appear under different names (for example, sentence construction, natural sentence construction, paragraph cohesion, and long-form coherence).
4. This is a structural and metadata-based coverage audit. It does **not** certify native-level fluency or replace expert human review.
5. The five revision chains must be resolved carefully in any eventual export; historical staging records should remain preserved.

## 3. Active general-track profile

### 3.1 Register

| Register | Active records |
|---|---:|
| Colloquial | 95 |
| Neutral | 76 |
| Formal | 7 |
| Mixed | 6 |
| **Total** | **184** |

Colloquial and neutral account for 171/184 records (92.9%). Formal and mixed together account for only 13/184 (7.1%). The formal subset is too small to establish reliable coverage across formal email, administrative writing, professional communication, respectful disagreement, and nuanced levels of formality.

### 3.2 Language labels

| Language label | Active records |
|---|---:|
| fa | 181 |
| fa-en | 3 |
| **Total** | **184** |

Only three records are explicitly labelled Persian-English mixed language. This is not enough to cover natural code-switching across technical vocabulary, workplace conversation, product names, transliterated terms, and cases where English is unnecessary or awkward.

### 3.3 Conversation length

| Message count per conversation | Active records |
|---|---:|
| 2 (single user/assistant exchange) | 115 |
| 4 | 32 |
| 6 | 34 |
| 8 | 3 |
| **Total** | **184** |

There are 69 multi-turn records (37.5%) and 115 two-message records (62.5%). Multi-turn work is present, especially in the latest excellence batches, but longer interaction patterns remain comparatively thin. Only three active records have eight messages.

### 3.4 Most frequent domain labels

| Domain label | Active records |
|---|---:|
| pragmatics | 18 |
| contextual_understanding | 12 |
| lexical_precision | 12 |
| response_quality | 11 |
| ambiguity_resolution | 10 |
| instruction_following | 10 |
| truthfulness | 9 |
| colloquial_persian | 7 |
| adaptive_communication | 7 |
| contextual_comprehension | 7 |
| persian_fluency | 6 |
| natural_sentence_construction | 6 |
| noisy_persian | 5 |
| sentence_construction | 5 |

There are **46 distinct domain labels** in the active set. Many labels have only one or a few records. This is a taxonomy problem as much as a data-volume problem: future batches should use a controlled, documented domain vocabulary and place finer distinctions in normalized subskills.

### 3.5 Frequent subskills

The most frequent active subskill labels are:
- meaning_preservation: 10
- typo_tolerance: 6
- audience_adaptation: 6
- uncertainty: 5
- context_retention: 5
- plain_language: 5
- reference_resolution: 4
- multi_turn: 4
- indirect_request: 4
- intent_recovery: 4

Most other subskill labels occur only one to three times. This long tail should not automatically be interpreted as 100+ distinct uncovered skills: many are synonyms, variants, or narrowly named manifestations of broader abilities.

## 4. Strengths already represented

The active general corpus has a useful foundation in:
- Understanding implied requests, indirect speech acts, politeness, sarcasm, humor, and non-literal language.
- Resolving references, ellipsis, ambiguity, and context-dependent meaning.
- Preserving meaning while rewriting, summarizing, changing tone, or adapting register.
- Tracking constraints and preferences across multiple turns.
- Responding to corrections, acknowledging errors, and revising without defensiveness.
- Calibrating uncertainty and avoiding unsupported assumptions.
- Explaining concepts for different audiences and controlling response length.
- Natural word choice, collocations, idioms, and sentence/paragraph cohesion.

These strengths should be extended through variation and adversarial contrasts, not by producing many paraphrases of the same scenario.

## 5. Coverage gaps and risks

### Gap A — Formal and mixed-register Persian

**Evidence:** 7 formal and 6 mixed records out of 184 active general records.

Needed variation:
- Professional email: request, follow-up, refusal, apology, escalation, and concise status updates.
- Administrative and service communication without unnatural bureaucratic over-formality.
- Respectful disagreement and boundary-setting at several levels of politeness.
- Switching between colloquial, neutral, and formal while preserving meaning.
- Mixed-register conversations where the user is colloquial but the requested output must be formal, and vice versa.

### Gap B — Longer, sustained conversations

**Evidence:** 115/184 active records contain only one user/assistant exchange; just 3 contain eight messages.

Needed variation:
- 8–12 message conversations with evolving goals and corrections.
- Delayed references to earlier details, selective context retention, and topic returns.
- User changes one constraint while expecting all other constraints to remain intact.
- Multi-step collaborative writing/editing, planning, troubleshooting, and decision support.
- Explicit tests for both remembering relevant context and ignoring irrelevant old details.

### Gap C — Real-world spoken Persian and conversational rhythm

**Evidence:** colloquial records exist, but register tags alone do not demonstrate spoken-language breadth.

Needed variation:
- Natural turn-taking, interruptions, incomplete sentences, self-repair, fillers, and short acknowledgements.
- Common informal reductions and spelling variants without turning the dataset into caricatured slang.
- Different conversational situations: friends, family, customer support, colleagues, and unfamiliar people.
- Distinguish natural spoken Persian from overly literary or translated phrasing.

### Gap D — Orthographic variation and noisy input

**Evidence:** typo_tolerance occurs 6 times and noisy_persian is a small domain group (5 records).

Needed variation:
- Persian/Arabic character variants (ی/ي, ک/ك), half-space inconsistency, spacing, punctuation, and common typing errors.
- Missing punctuation, phonetic spelling, repeated characters, and fragmented mobile messages.
- Recover intended meaning when clear; ask one focused question when ambiguity materially changes the answer.
- Avoid silently changing names, numbers, dates, or technical terms.

### Gap E — Persian-English code-switching

**Evidence:** only 3 active records carry the `fa-en` language label.

Needed variation:
- Natural English technical terms embedded in Persian sentences.
- Mixed-language workplace and software conversations.
- Appropriate Persian equivalents when requested, without forced translation of standard terms.
- Preserve exact product names, code identifiers, acronyms, and quoted English text.
- Detect when code-switching is user style versus an explicit output requirement.

### Gap F — Lexical nuance and contrastive word choice

**Evidence:** lexical_precision is represented (12 domain-tagged records), but many finer subskills occur only once or twice.

Needed variation:
- Near-synonyms with different connotation, register, intensity, and collocation.
- Context-sensitive choices between everyday and literary vocabulary.
- Idioms and proverbs across literal, figurative, ironic, and context-dependent uses.
- Detect semantic drift in rewrites and explain why one phrase fits better in a specific context.

### Gap G — Extended writing and discourse structure

**Evidence:** sentence/paragraph skills are distributed across multiple domain labels; long-form coherence appears only as a small tail of tags.

Needed variation:
- Coherent multi-paragraph Persian writing with topic progression and transitions.
- Editing for cohesion, rhythm, redundancy, and paragraph structure.
- Summaries that preserve hierarchy, qualifications, and uncertainty.
- Maintain tense, point of view, terminology, and tone across longer text.
- Distinguish a request for proofreading from a request for substantive rewriting.

### Gap H — Conversational diversity and pragmatic robustness

**Evidence:** several pragmatic skills appear, but many named subskills have only one or two examples.

Needed variation:
- Humor, irony, sarcasm, teasing, indirect refusal, complaints, and polite pressure with context contrasts.
- Emotionally charged messages where the assistant must not over-read the user's emotional state.
- Ambiguous short replies whose meaning changes with prior context.
- Politeness differences across relationships and situations.
- Cases where the best response is a concise acknowledgement, not an explanation or follow-up question.

### Gap I — Broad domain vocabulary and terminology

**Evidence:** the dataset is primarily a general-language corpus and its current metadata does not establish balanced domain-specific Persian.

Needed variation:
- Everyday services, shopping, travel, education, work, technology, household tasks, and public services.
- Correct Persian terminology with plain-language explanations.
- Preserve distinctions between general advice and claims requiring current or specialist information.
- Keep domain facts controlled and avoid turning language SFT into a factual knowledge dump.

## 6. Taxonomy and data-management issues

1. **Normalize domains before expanding volume.** Create a small controlled domain list (roughly 10–15 broad domains) and retain detailed capabilities in subskills.
2. **Create a canonical subskill vocabulary.** Merge obvious naming variants only through a documented mapping; do not silently rewrite historical records.
3. **Separate register of input from register of desired output.** One `register` field cannot fully describe conversations where the user speaks colloquially but requests a formal email.
4. **Add task-shape metadata.** Suggested fields: `task_type`, `input_noise`, `conversation_depth`, `output_form`, `code_switching`, and `requires_clarification`.
5. **Distinguish record-level and message-level language.** A conversation can contain Persian prose, English terms, code, and quoted source text without the whole record being equally bilingual.
6. **Do not treat tag frequency as a quality score.** Human review and challenge-set performance are required.

## 7. Recommended next batch

Create a focused batch of **40–50 new records**, only after agreeing on the taxonomy. Suggested allocation:

| Priority area | Target records | Design emphasis |
|---|---:|---|
| Formal and mixed-register Persian | 8 | professional, administrative, polite disagreement, register switching |
| Sustained multi-turn conversations | 8 | 8–12 messages, evolving constraints, delayed references |
| Spoken Persian and conversational rhythm | 6 | turn-taking, repair, natural informal phrasing |
| Noisy input and orthographic variation | 5 | realistic mobile typing, half-space and character variants |
| Persian-English code-switching | 4 | technical and workplace contexts |
| Lexical nuance and idiomatic choice | 5 | contrastive minimal pairs, collocations, connotation |
| Extended writing and discourse cohesion | 5 | multi-paragraph drafting, editing, summarization |
| Pragmatic edge cases | 4 | indirect refusal, irony, short ambiguous replies |
| **Total** | **45** | |

These are targets for a balanced pilot, not quotas to fill mechanically. If an example overlaps multiple areas, assign one primary domain and multiple normalized subskills. Prefer difficult, realistic contrasts over repetitive examples.

## 8. Acceptance gates before training

- Human review of all new examples by a fluent Persian reviewer, with explicit decisions and revision history.
- Resolve or explicitly retain all semantic near-duplicate candidates; do not auto-delete based on similarity scores.
- Normalize metadata vocabulary and validate all enum values.
- Create leakage-resistant train/validation/test splits at conversation and semantic-cluster level.
- Keep identity and Forex/XAUUSD datasets separate from general Persian SFT.
- Keep synthetic examples marked as unreviewed until a human actually reviews them.
- Run a held-out Persian challenge set covering register, naturalness, pragmatic interpretation, long-context retention, noisy input, and code-switching.
- Benchmark the base Qwen3.5-4B before fine-tuning; compare the same held-out prompts after training.
- Audit serialization, tokenizer behavior, truncation, and Unsloth training configuration before any run.

## 9. Decision

**Do next:** normalize the metadata taxonomy and create the 45-record targeted pilot described above.

**Do not do yet:** generate hundreds of additional generic conversations, merge identity records into the general corpus, or start fine-tuning from the current staging files.

This report does not approve the corpus for training. It is a coverage map to guide the next controlled data-generation and human-review cycle.
