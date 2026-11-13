# Full Dataset Semantic Audit V1

**Scope:** all 12 JSONL files currently present in `data/staging/` on the default branch.  
**Audit type:** automated lexical-overlap screening followed by contextual inspection of the strongest candidate pairs. This is not a human linguistic review.

## 1. Inventory and revision handling

| Measure | Result |
|---|---:|
| Parsed staging records | 197 |
| Unique `sample_id` values | 197 |
| General Persian records | 189 |
| Separate identity records | 8 |
| General records superseded by an explicit revision | 5 |
| Active general records after excluding superseded predecessors | 184 |

The five explicit revision links are:
- `fa-adv-0031` supersedes `fa-adv-0016`
- `fa-adv-0032` supersedes `fa-adv-0018`
- `fa-adv-0033` supersedes `fa-adv-0023`
- `fa-adv-0034` supersedes `fa-adv-0024`
- `fa-adv-0035` supersedes `fa-adv-0026`

The audit compares the active general records for duplicate screening. The identity file is counted and checked for inventory integrity but is not mixed into the general-language similarity comparison. Historical predecessor records remain in staging for traceability and must not be exported alongside their active replacements.

## 2. Method and limitations

Text from user and assistant messages was normalized for common Persian/Arabic character variants, whitespace, punctuation and diacritics, then compared using token-set Jaccard similarity. Pairs with similarity at or above 0.22 were shortlisted and inspected in context.

This method is a screening heuristic, not a semantic model:
- High overlap can arise from shared subject matter, numbers, templates or common wording without duplicated learning value.
- Low overlap can hide paraphrases and repeated skills expressed with different vocabulary.
- Multi-turn examples can share a first-turn topic while testing materially different follow-up behavior.
- Scores are not quality grades and must not be used as automatic deletion thresholds.

## 3. Strongest candidates and contextual recommendations

### A. High-priority human adjudication

| Pair | Similarity | Contextual assessment | Recommendation |
|---|---:|---|---|
| `fa-adv-0004` / `fa-gen-0036` | 0.889 | Same Persian source sentence and same English translation. The second adds an explicit “only translate” constraint, but the output is identical. | **Likely redundant.** Human reviewer should decide whether the no-extra-text constraint is sufficiently important to retain both. If not, retain the clearer representative and document the decision. |
| `fa-adv-0029` / `fa-pilot-0014` | 0.512 | Same 15% discount calculation pattern. One is multi-turn and adds a shipping charge; the other is a single-turn calculation with a different price. | **Keep provisionally.** Different interaction shape and follow-up arithmetic provide additional coverage; check whether the original pilot already has enough simple discount examples. |
| `fa-adv-0039` / `fa-gen-0020` | 0.500 | Both formalize a message about a file. The advanced record includes a correction explicitly forbidding the semantic change from “saw” to “reviewed”; the older record does change it. | **Do not merge blindly.** This is useful contrastive evidence for meaning preservation and correction recovery, but the older target may teach an unwanted semantic drift. Human reviewer should assess whether to revise or exclude the older example. |
| `fa-adv-0046` / `fa-pilot-0014` | 0.371 | Both teach percentage-discount arithmetic with different prices; one includes more explicit calculation verification. | **Keep provisionally.** Similar skill, but not a duplicate; assess whether both are needed for numerical diversity. |
| `fa-adv-0008` / `fa-pilot-0001` | 0.350 | Both infer that the user wants a stiff Persian text made more natural and ask the user to provide it. | **Possible functional duplicate.** Review alongside `fa-adv-0042` and `fa-exc-0019`; retain only if each demonstrates a clearly distinct register or noisy-input skill. |
| `fa-adv-0060` / `fa-exc-0014` | 0.349 | Both handle missing context and avoid guessing, but the first concerns unavailable prior context while the second asks which of two unspecified options is meant. | **Keep.** Related principle, distinct ambiguity type. |
| `fa-adv-0017` / `fa-adv-0047` | 0.345 | Both are multi-turn travel-planning examples. The first revises a packing checklist; the second separates car-related preparation. | **Keep provisionally.** Distinct constraints and follow-up operations. |
| `fa-adv-0009` / `fa-pilot-0012` | 0.337 | Both revise a learning plan around unavailable weekends, but differ in subject, daily time and planning constraints. | **Keep provisionally.** Similar planning template; check that the final answer correctly preserves each record’s original time budget. |
| `fa-adv-0011` / `fa-pilot-0010` | 0.329 | Both explain blockchain for a nontechnical audience, with different audience framing. | **Keep only if audience adaptation is intentional.** The two targets are close enough to warrant a human check for distinct audience-specific simplification. |
| `fa-exc-0004` / `fa-pilot-0004` | 0.324 | Both ask for natural Persian rewriting, but the source sentences and intended meanings differ. | **Keep.** Shared editing skill, different lexical and syntactic problem. |
| `fa-adv-0035` / `fa-gen-0024` | 0.308 | Both explain API to a beginner using a restaurant/waiter analogy. The advanced record explicitly asks for brevity. | **Keep provisionally.** Check whether the short-answer constraint is sufficiently represented elsewhere. |
| `fa-adv-0008` / `fa-adv-0042` | 0.286 | Both begin with informal requests to make text more fluent; the latter supplies the actual text and adds a “not too formal” constraint. | **Keep provisionally.** One is a clarification/intent-recovery turn; the other performs a constrained rewrite. |

### B. Related-skill pairs; not duplicates on current evidence

| Pair | Similarity | Why the distinction matters |
|---|---:|---|
| `fa-adv-0007` / `fa-adv-0065` | 0.360 | Three versus four titles; both test exact item count, but the requested counts and formatting constraints differ. |
| `fa-adv-0043` / `fa-adv-0055` | 0.288 | Both revise multi-day schedules, but the goals and dependency constraints are different (Excel learning versus exam preparation). |
| `fa-exc-0008` / `fa-exc-0075` | 0.274 | Both interpret ironic comments about lateness; the newer multi-turn example explores friendly humor and a witty reply. |
| `fa-adv-0067` / `fa-pilot-0002` | 0.267 | Near-identical vague references (“that/it”) and a request to prepare something for tomorrow. Strong candidate for redundancy review. |
| `fa-exc-0007` / `fa-gen-0022` | 0.258 | Both interpret indirect or potentially negative speech, but use different expressions and contextual cues. |
| `fa-adv-0030` / `fa-gen-0020` | 0.255 | Both formalize file-related messages, but the content and intended meaning differ. |
| `fa-exc-0019` / `fa-pilot-0001` | 0.255 | Both infer a request to improve stiff writing; one specifies a professional-but-not-stiff register. Review together with the other fluency-request cluster. |
| `fa-adv-0010` / `fa-adv-0060` | 0.250 | Both avoid fabricated memory, but one asks about a previously recommended book and the other about an unspecified option. |
| `fa-adv-0021` / `fa-adv-0053` | 0.250 | Both troubleshoot unexpected shutdowns, but laptop load/heat and phone battery-level symptoms are materially different. |
| `fa-adv-0034` / `fa-exc-0073` | 0.241 | Both contain meeting-invitation/date context, but one tests informal-tone correction and the other contradiction handling and date uncertainty. |
| `fa-exc-0003` / `fa-exc-0071` | 0.241 | Same idiom and core definition; the newer multi-turn record adds nuance and a natural example. Consider retaining the richer record if only one is needed. |
| `fa-adv-0012` / `fa-pilot-0007` | 0.240 | Both offer empathetic support, but respond to different emotional situations. |
| `fa-adv-0003` / `fa-adv-0067` | 0.238 | Both ask clarification about an unclear reference and a tomorrow-related action; compare the precise missing information each asks for. |
| `fa-adv-0044` / `fa-gen-0019` | 0.238 | Both explain RAM versus storage, but one uses a beginner analogy and the other enforces a one-sentence constraint. |
| `fa-adv-0028` / `fa-exc-0033` | 0.232 | Both handle polite refusal, but the first is a repeated request with a follow-up pushback; the second is a more general invitation refusal. |
| `fa-adv-0032` / `fa-pilot-0012` | 0.232 | Both involve schedule constraints, but the actual activity and constraint structure differ. |
| `fa-adv-0043` / `fa-pilot-0012` | 0.230 | Both allocate learning across weekdays/weekends, but the learning goal, duration and review requirements differ. |
| `fa-exc-0022` / `fa-exc-0029` | 0.224 | Both repair stiff nominalized Persian constructions, but use different source sentences and lexical patterns. |
| `fa-exc-0050` / `fa-exc-0083` | 0.222 | Both teach polysemy of «شیر»; the newer multi-turn example tests contextual disambiguation across multiple sentences. |

## 4. Cross-batch quality observations

1. **A small cluster of “make this text more natural” prompts is crowded.** Review `fa-adv-0008`, `fa-adv-0042`, `fa-exc-0019`, and `fa-pilot-0001` together. Distinguish intent clarification, noisy-input recovery, register selection and actual rewriting rather than keeping near-identical opening turns.
2. **Simple arithmetic appears in multiple batches.** Retain examples that add different interaction patterns, values, verification behavior or follow-up costs; avoid retaining several records that only change the amount.
3. **Ambiguous-reference clarification has several close variants.** Preserve meaningful differences (unknown object, unknown prior option, missing time or action) and avoid superficial paraphrase-only duplication.
4. **Multi-turn records often add genuine value.** Similar first turns should not trigger removal when later turns test constraint retention, correction, uncertainty or register changes.
5. **Potential target-quality issue:** `fa-gen-0020` changes “I saw the file” into “I reviewed the file.” The later correction example explicitly identifies this semantic drift. Human review should decide whether the earlier target should be corrected or excluded from the eventual training export.

## 5. Recommended next actions

1. Human-adjudicate the high-priority pairs in section 3A, especially `fa-adv-0004` / `fa-gen-0036`, the natural-rewrite cluster, and the meaning-drift case involving `fa-gen-0020`.
2. Add the 85 excellence records to the human-review register; the existing register covered the earlier 112-record inventory and must not silently omit newer batches.
3. After human decisions, create a non-destructive export candidate that resolves superseded revisions, applies approved duplicate decisions, keeps identity separate, and assigns leakage-resistant splits by semantic family rather than random individual record.
4. Run structural validation and a separate linguistic review after export preparation. A passing schema/CI check does not establish naturalness, correctness or training readiness.

**No staging records were deleted, rewritten or automatically rejected by this audit.** All recommendations remain provisional until a human reviewer records decisions.
