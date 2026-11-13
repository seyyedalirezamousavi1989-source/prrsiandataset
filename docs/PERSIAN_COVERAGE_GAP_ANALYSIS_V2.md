# Persian Dataset Coverage Gap Analysis V2

**Snapshot:** 2026-11-13  
**Scope:** all 13 JSONL staging files on the default branch, fetched directly from GitHub.  
**Purpose:** measure metadata coverage and conversation-shape gaps before authoring the next large Persian-language batch.  
**Status:** metadata-based diagnostic; not a human linguistic-quality audit and not proof that a tagged skill is learned.

## 1. Inventory and counting rules

| Measure | Count |
|---|---:|
| All staging records fetched | 272 |
| General-language records, including superseded history | 264 |
| Separate identity-track records | 8 |
| Superseded general predecessors excluded from active coverage | 5 |
| Active general records used for this report | 259 |
| Staging files inspected | 13 |

The active general set excludes identity-track records and the five records carrying `metadata.supersedes_sample_id`. Historical records remain preserved in staging. The five predecessor records must not be counted alongside their replacements in a final training export without an explicit adjudication decision.

The inventory reconciles with the repository snapshot:
- Original pilot and advanced staging files: 112 records, including 8 identity records and 5 superseded predecessors.
- Persian language excellence batches V1–V4: 160 records.
- Total: 272 records.

## 2. Language, register, and conversation length

### Language metadata

| Language | Active records |
|---|---:|
| `fa` | 254 |
| `fa-en` | 5 |
| `multilingual` | 0 |

Meaningful Persian-English code-switching is very underrepresented (5/259, 1.9%). No active record is tagged multilingual. This should be expanded deliberately, not by inserting unnecessary English words into otherwise Persian conversations.

### Assistant register metadata

| Register | Active records | Share |
|---|---:|---:|
| `colloquial` | 125 | 48.3% |
| `neutral` | 112 | 43.2% |
| `formal` | 11 | 4.2% |
| `mixed` | 11 | 4.2% |

Formal and intentionally mixed-register examples are the clearest register gaps. The next batch should include real professional and institutional contexts, plus controlled register changes within a conversation. Avoid making formal Persian artificially bureaucratic.

### Number of messages per conversation

| Messages | Active records |
|---:|---:|
| 2 | 115 |
| 4 | 96 |
| 6 | 45 |
| 8 | 3 |

Only 48/259 conversations (18.5%) contain six or more messages; just three contain eight. The next batch should increase substantial conversations with 6–10 messages, while retaining some short examples for concise-response behavior. Longer conversations must contain meaningful state changes, references, corrections, or new constraints—not padding.

## 3. Primary-domain metadata observations

The active records contain many historical domain labels that predate Taxonomy V2. Examples include `ambiguity_resolution`, `contextual_understanding`, `noisy_persian`, `pragmatics`, `reasoning`, `colloquial_persian`, and `natural_sentence_construction`. Newer V4 records use the canonical vocabulary, but historical labels have intentionally not been mass-edited.

Therefore, raw label counts are not directly comparable as canonical-domain counts. A taxonomy mapping and human review are required before historical records can be normalized. Do not treat each old label as a separate skill or assume that a high tag count proves strong coverage.

### Qualitative coverage interpretation

- **Relatively visible in metadata:** lexical precision (19 records under the canonical label alone, plus legacy labels such as idiomatic Persian), pragmatics/tone (7 canonical records plus legacy pragmatics labels), instruction following (15), sentence construction (13), truthfulness (14), and correction recovery (6 canonical plus legacy self-correction/repair labels).
- **Present but fragmented across legacy labels:** intent understanding, context continuity, ambiguity handling, emotional support, adaptive communication, everyday dialogue, and multi-turn planning.
- **Needs targeted expansion and adjudication:** formal professional Persian, deliberate register switching, Persian-English technical code-switching, longer context chains, and naturally realistic multilingual situations.

These are metadata observations, not claims that every sample is linguistically excellent or that all underlying conversations were manually inspected.

## 4. Subskill and scenario diversity risks

The inventory contains a broad subskill vocabulary, but many labels occur only once. This is useful for describing specific behaviors, yet it can also signal uncontrolled taxonomy growth. New records should reuse existing subskill names whenever their meaning fits. Add a new label only when it represents a distinct, observable behavior.

The next authoring pass should avoid repeatedly using the same skeletons:
- user asks what an idiom or sarcastic phrase means;
- user asks for a rewrite and then changes tone;
- user gives a vague request and assistant asks one clarification;
- user corrects a previous answer and assistant apologizes;
- user changes one planning constraint and expects the rest to remain fixed.

These patterns remain valuable, but the next batch must vary the underlying social setting, user intent, discourse structure, lexical challenge, and assistant response strategy—not merely replace names or nouns.

A proper semantic near-duplicate review must compare full conversations and the behavior being taught. Token overlap alone is insufficient. Existing V2 audit candidates remain provisional and require human adjudication.

## 5. Recommended next-batch design

Create V5 as a focused 100-record candidate batch, guided by the following target mix. These are authoring targets, not final training proportions:

| Focus | Target records | Design emphasis |
|---|---:|---|
| Long-context continuity and selective recall | 20 | 6–10 message threads, delayed references, topic return, irrelevant-detail suppression |
| Formal/professional Persian | 18 | emails, workplace requests, reports, customer communication, respectful disagreement |
| Register and tone transitions | 15 | colloquial ↔ neutral ↔ formal, preserve meaning and user voice |
| Persian-English technical code-switching | 12 | real technical terms, error messages, identifiers, bilingual clarification |
| Pragmatics, indirect intent, humor | 12 | face-saving, indirect refusal, tact, irony, context-sensitive humor |
| Ambiguity and clarification judgment | 8 | distinguish material from harmless ambiguity; answer directly when enough context exists |
| Lexical nuance and sentence craft | 8 | collocations, near-synonyms, polysemy, paragraph cohesion, natural rhythm |
| Correction recovery and truthfulness | 7 | multi-step correction, uncertainty, evidence boundaries, no false action or memory claims |
| **Total** | **100** | |

Conversation-shape targets for V5:
- At least 60 records with 6–10 messages.
- No more than 20 records with only 2 messages.
- Include a deliberate mix of 4-message and longer threads.
- At least 18 records tagged `formal`; at least 15 `mixed`.
- At least 12 `fa-en` records, only where bilingual content is functionally necessary.
- All 100 records marked `quality.review_status=unreviewed` until a fluent reviewer evaluates them.

Each record should use one canonical primary domain from Taxonomy V2 and 2–4 meaningful subskills. Avoid inventing domain aliases. Use natural contemporary Iranian Persian and realistic dialogue; no padding, artificial slang, translationese, or unsupported facts.

## 6. Quality and release gates

Before accepting V5 into the staging repository:
1. Parse every JSONL line and validate the required schema.
2. Check unique IDs and ensure IDs do not overlap any existing batch.
3. Validate canonical primary domains, register values, language values, and review status.
4. Check alternating user/assistant turns and meaningful multi-turn progression.
5. Run exact and normalized-text duplicate checks.
6. Run scenario-level semantic triage against all active general records, not only V1–V4.
7. Inspect the strongest near-duplicate candidates in full context; do not auto-delete.
8. Confirm that no identity or Forex/XAUUSD content has leaked into the Persian fluency track.
9. Keep staging split labels provisional; create leakage-resistant final splits only after group-level deduplication.
10. Treat CI success as structural validation only. It does not certify native-speaker naturalness.

## 7. Immediate decision

Proceed with a V5 batch of 100 records using the targets above. This is a measured expansion rather than an arbitrary volume increase. After V5, repeat the coverage analysis and semantic triage before deciding whether another batch is justified.

**Important limitation:** this report measures the metadata and conversation lengths in the fetched repository snapshot. It does not claim that all 259 conversations have received human linguistic review. Human review status must remain explicit and honest.


## 8. V5 progress update (2026-11-13)

After the original snapshot above, V5 has progressed to five parts:

| V5 part | Records | IDs |
|---|---:|---|
| Part 1 | 10 | fa-exc-0161–fa-exc-0170 |
| Part 2 | 10 | fa-exc-0171–fa-exc-0180 |
| Part 3 | 10 | fa-exc-0181–fa-exc-0190 |
| Part 4 | 10 | fa-exc-0191–fa-exc-0200 |
| Part 5 | 10 | fa-exc-0201–fa-exc-0210 |
| **V5 total so far** | **50** | |

The 50 V5 records are additional to the 160 V1–V4 records, giving 210 Persian language excellence records in these batches. This does not revise the 272-record repository-wide snapshot above, which was taken before the V5 batches were added.

Part 5 was intentionally targeted toward the gaps identified in this report:
- 8- and 10-message conversations to strengthen longer context chains;
- 3 formal and 3 mixed-register records;
- 3 `fa-en` records using English technical terms only where contextually justified;
- formal workplace writing, tactful disagreement, API rate-limit explanation, dependency-aware release planning, selective constraint retention, exact-format instruction following, and proportionate emotional support.

Part 5 structural checks passed locally before commit: 10 records, IDs `fa-exc-0201` through `fa-exc-0210`, alternating roles, 6–10 messages, valid canonical domains/register/language values, and all review statuses set to `unreviewed`. The committed file was fetched back and matched the authored content exactly.

This update does not constitute human linguistic review, semantic deduplication, or approval for training. Re-run repository-wide coverage and semantic near-duplicate analysis after the full V5 candidate batch is complete.
