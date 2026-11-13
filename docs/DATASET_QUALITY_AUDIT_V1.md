# Dataset Quality Audit V1 — Structural and Linguistic Risk Screening

**Snapshot:** 2026-11-13  
**Scope:** 197 records across all 12 JSONL staging files.  
**Audit type:** automated integrity checks plus targeted contextual inspection of flagged and mixed-language cases. This is not a substitute for native-speaker human review of every assistant turn.

## 1. Executive summary

| Check | Result |
|---|---:|
| Records parsed | 197 |
| Unique sample IDs | 197 |
| Missing core metadata (domain, subskills, language, register, metadata) | 0 |
| Empty message contents | 0 |
| Exact duplicate conversations after Persian normalization | 0 |
| Assistant replies below 12-character heuristic threshold | 0 |
| Obvious placeholder markers detected | 0 |
| Candidate stiff/formulaic phrases detected by limited phrase list | 0 |
| Candidate punctuation anomalies detected by limited regex checks | 0 |
| Missing `quality.review_status` | 59 |
| Explicitly `unreviewed` | 138 |
| Staging records labelled `train` | 197 |

**Interpretation:** structural integrity is encouraging, but these checks do not prove that the Persian is idiomatic, every answer is correct, or the examples are pedagogically optimal.

## 2. Corpus profile

### Records by file

| Staging file | Records | Mean assistant characters |
|---|---:|---:|
| `advanced_pilot_v2.jsonl` | 15 | 142 |
| `advanced_pilot_v3.jsonl` | 15 | 249 |
| `advanced_pilot_v4_patch.jsonl` | 5 | 212 |
| `advanced_pilot_v5.jsonl` | 15 | 192 |
| `advanced_pilot_v6.jsonl` | 10 | 287 |
| `advanced_pilot_v7.jsonl` | 8 | 159 |
| `identity_v1.jsonl` | 8 | 114 |
| `persian_language_excellence_v1.jsonl` | 24 | 182 |
| `persian_language_excellence_v2.jsonl` | 31 | 162 |
| `persian_language_excellence_v3.jsonl` | 30 | 322 |
| `pilot_v0.jsonl` | 15 | 163 |
| `pilot_v1.jsonl` | 21 | 166 |

### Register

| Register | Records |
|---|---:|
| Colloquial | 101 |
| Neutral | 83 |
| Formal | 7 |
| Mixed | 6 |

Formal coverage is limited (7/197). This is a coverage observation, not an instruction to generate more formal records indiscriminately. Human review should first verify the labels and naturalness of the existing formal examples.

### Language labels

| Label | Records |
|---|---:|
| `fa` | 194 |
| `fa-en` | 3 |

The three `fa-en` records contain code-switching, English source text or technical English terms in a Persian conversation; their labels are consistent with their content.

### Conversation shape

| Total messages | Records |
|---|---:|
| 2 | 124 |
| 4 | 35 |
| 6 | 35 |
| 8 | 3 |

124/197 records are single user/assistant exchanges. Preserve multi-turn examples that teach context retention and correction, but avoid inflating them with repetitive templates.

### Assistant response length

| Statistic | Characters |
|---|---:|
| Minimum | 23 |
| 25th percentile | 127 |
| Median | 182 |
| 75th percentile | 251 |
| 95th percentile | 423 |
| Maximum | 593 |

Length alone is not a quality score. Concise answers can be excellent when requested; longer answers can still be inaccurate or unnatural.

## 3. Findings requiring action

### 3.1 Review metadata is incomplete

- 59 records have no `quality.review_status` field.
- 138 records are explicitly `unreviewed`.
- No record was upgraded to human-reviewed by this audit.

Do not infer that missing status means accepted. Use [Human Review Register V2](HUMAN_REVIEW_REGISTER_V2.md) to record actual reviewer, date, scores and rationale. Do not bulk-edit source metadata merely to make the counts look complete.

### 3.2 All staging records currently carry `split=train`

This is a staging label, not a safe final split. Using it directly would put every record in training and leave no held-out validation or test data.

Before training, create a separate export candidate with group-aware train/validation/test/challenge assignment. Keep revision chains and semantically related examples in the same split group to reduce leakage. Keep identity and Forex datasets separate from this general Persian corpus.

### 3.3 Formal-register coverage is limited

Only 7 records are labelled `formal`, compared with 101 colloquial, 83 neutral and 6 mixed. During human review, verify the labels and identify genuinely underrepresented formal tasks. Add examples only where they fill a demonstrated gap.

### 3.4 Exact duplicates not found; semantic redundancy remains unresolved

The normalized exact-conversation comparison found no identical conversations. This does not override the semantic audit: near-duplicates can differ lexically while teaching the same behavior.

Adjudicate the candidates in [Full Dataset Semantic Audit V1](FULL_DATASET_SEMANTIC_AUDIT_V1.md), especially the identical-translation candidate, natural-rewrite cluster and meaning-preservation example involving `fa-gen-0020`.

## 4. Targeted contextual checks

### `fa-adv-0015` — intentional English output, not a language-label defect

The user asks in Persian for five non-Persian app names and explicitly requests no explanation. The assistant returns five English-style names and nothing else. A naive language-ratio heuristic flagged this as English-heavy, but contextual inspection confirms that the response is appropriate and the `fa` conversation label is correct.

**Decision:** no correction recommended.

### Mixed-language examples

- `fa-adv-0019`: Persian conversation with terms such as “feature”, “bug” and “login”; the assistant clarifies that the feature is postponed, not cancelled.
- `fa-adv-0048`: English source sentence translated into Persian, then revised to a more formal but not stiff register.
- `fa-adv-0057`: the user asks to replace “meeting” with «جلسه»; the assistant follows the lexical correction.

These have distinct language and correction objectives. Keep provisionally, subject to native-speaker review.

### `fa-exc-0068` — calibrated security explanation

The multi-turn example explains two-factor authentication with a simple analogy and then explicitly rejects a claim of 100% security. The final answer avoids promising absolute security.

**Decision:** keep provisionally; human reviewer should check the analogy and technical nuance.

## 5. Automated checks and limitations

Checks included JSONL parsing, required metadata, unique IDs, empty messages, exact normalized conversation duplicates, limited placeholder/formulaic-phrase/punctuation patterns, coarse language-ratio screening, response-length distribution and review metadata coverage.

A zero count from a phrase detector means only that its narrow patterns did not match. It does not prove the absence of grammar errors, unnatural collocations, factual mistakes, subtle translationese, poor examples or semantic drift. No automated result here should be interpreted as human acceptance.

## 6. Human review priorities

1. **Meaning fidelity and factual correctness:** inspect translations, rewrites, summaries and explanations for introduced meaning or unsupported claims.
2. **Natural contemporary Iranian Persian:** read responses aloud; assess word choice, collocations, syntax, rhythm, punctuation and register.
3. **Multi-turn coherence:** verify that corrections and follow-ups preserve prior constraints.
4. **Instruction precision:** check exact counts, “no explanation”, tone, length and output format.
5. **Pedagogical value:** ensure each sample teaches a distinct capability, not merely a new surface topic.
6. **Metadata correctness:** verify domain, subskills, language and register against the actual conversation.
7. **Duplicate adjudication:** apply documented decisions while preserving history and revision links.

Record actual decisions in [Human Review Register V2](HUMAN_REVIEW_REGISTER_V2.md). Do not fill scores based on this automated audit.

## 7. Release gate

The corpus is **not yet approved for fine-tuning**. Before preparing an Unsloth export:
- complete human linguistic and factual review;
- resolve semantic duplicate candidates and revision chains;
- correct or exclude answers with meaning drift or unnatural Persian;
- verify register/domain/subskill labels;
- construct leakage-resistant splits by semantic family;
- keep identity and Forex/XAUUSD corpora separate;
- run schema and serialization tests on the exact export;
- benchmark the untouched base model on a held-out Persian challenge set.

**Final status:** structural screening passed for this 197-record snapshot; linguistic quality remains pending human adjudication. No staging record was edited, deleted, accepted or rejected by this audit.
