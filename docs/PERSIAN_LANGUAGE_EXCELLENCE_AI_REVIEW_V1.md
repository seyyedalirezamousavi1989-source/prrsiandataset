# Persian Language Excellence — AI Linguistic Review V1

**Review date:** 2026-11-13  
**Scope:** Persian Language Excellence V1–V5, 260 records (fa-exc-0001 through fa-exc-0260).  
**Review type:** Full-conversation AI editorial inspection by the assistant, with record-level findings below.  
**Status:** AI-reviewed / provisional. This is not a human linguistic certification, not a training approval, and not a change to staging records.

## Executive result

All 260 conversations across V1–V5 were read in context. The corpus has a useful foundation: most examples use understandable contemporary Persian, cover varied conversational tasks, and often demonstrate useful behaviors such as clarification, preserving constraints, uncertainty calibration, and correction.

However, the corpus is **not ready for SFT export**. The most important issue is not spelling: several examples intentionally include an incorrect assistant answer followed by a correction. The current exporter serializes every assistant message as a positive SFT target. Unless turn-level quality is represented and applied, the model can be trained to imitate the initial mistake as well as the later correction.

No source JSONL file was modified by this review. Existing quality.review_status=unreviewed values remain unchanged. No scores, semantic-family IDs, split assignments, or training approvals were created.

## Blocking corpus-level issue: assistant-turn supervision

The current scripts/export_training.py copies the complete messages array into the SFT output. It does not distinguish:
- a correct assistant answer;
- an intentionally flawed answer included to demonstrate recovery;
- an answer later corrected because it violated the user's constraints;
- an incomplete answer that promises to do the task but never delivers it.

This makes some correction/recovery records unsafe as ordinary next-token SFT conversations. Examples requiring turn-level treatment include:

| Sample | Problematic turn / behavior | Recommended handling |
|---|---|---|
| fa-exc-0104 | The first résumé rewrite invents duties ("پیگیری نیازها و پاسخ‌گویی") not supplied by the user; the next assistant turn admits and removes them. | Do not train the invented first answer as a positive target. Retain the correction behavior as a target. |
| fa-exc-0156 | The first edit removes «ما» even though the user asked only for punctuation; the next turn correctly restores it. | Exclude or explicitly mark the first assistant turn as a negative example. |
| fa-exc-0254 | The product description invents "طراحی ارگونومیک" without evidence; the assistant later acknowledges and retracts it. | Do not train the unsupported claim as a positive target. |
| fa-exc-0212 | The user says the assistant wrote «پنجشنبه آینده», but the preceding assistant message in this sample says only «تا روز پنجشنبه». The assistant accepts a correction that is not supported by the visible context. | Repair the scenario so the alleged erroneous phrase actually appears, or rewrite the correction exchange. |
| fa-exc-0101 | The initial two-sentence summary omits the important qualifier «فقط اندکی»; the correction restores the nuance but collapses the answer to one sentence despite the original two-sentence constraint. | Rewrite the corrected answer to preserve both the nuance and the two-sentence constraint. |

**Required pipeline change before training:** introduce assistant-turn-level review labels (for example, positive_target, negative_or_demonstration_only, needs_revision) and make the exporter emit only approved positive assistant targets. Do not simply delete the user correction turns: the correction behavior itself is valuable supervision. Preserve context safely when constructing per-turn training examples.

## Record-level findings

### A. Clear or high-confidence content / completion issues

| Sample | Finding | Severity | Recommendation |
|---|---|---|---|
| fa-exc-0024 | Assistant acknowledges that it confused "simpler" with "shorter", but never supplies the promised corrected text. | Medium | Add the actual rewrite at the same length and simpler wording. |
| fa-exc-0096 | User asks for a three-day travel plan and then requests only day two be lighter; assistant promises to adjust but gives no concrete revised itinerary. No prior itinerary is present in the record. | High | Supply a complete three-day plan or change the prompt to ask only for a planning approach. |
| fa-exc-0148 | User refers to a text "that I sent", but no text is present in the conversation. Assistant confirms the reference and promises a rewrite without requesting the missing text. | High | Ask the user to resend/paste the missing text; do not imply it is available. |
| fa-exc-0161 | User requests a three-day Shiraz itinerary. The assistant gives day one and day two only; day three is missing. | High | Complete all three days, or explicitly ask for information needed to plan day three. |
| fa-exc-0163 | User explicitly requests a four-week table. The assistant gives a general weekly routine in prose, not a four-week table or week-by-week progression. | Medium | Provide the requested table and meaningful progression across four weeks. |
| fa-exc-0171 | User asks for a program for a 20-person workshop. The assistant captures constraints but never produces a usable timetable or activity sequence. | Medium | Add an actionable schedule, with group sizes that total exactly 20. |
| fa-exc-0205 | User supplies 09:00–16:00 hours, lunch duration and break constraints, but the final response still does not allocate actual time slots. | Medium | Produce a complete timetable that fits the stated hours and constraints. |
| fa-exc-0101 | The correction turn does not preserve the original two-sentence output constraint. | Medium | Keep the corrected summary in two sentences. |
| fa-exc-0209 | User asks to retain only the first English technical term. Final answer still retains "regression" in English as well as "breaking change". | Medium | Translate the second term (for example, «آزمون بازگشت»). |
| fa-exc-0162 | Food planning for a guest with a nut allergy mentions checking labels, but omits cross-contact / shared-equipment caution. | Medium | Add a concise warning to verify ingredients and cross-contact with the allergic guest; avoid implying that label-checking alone is sufficient. |

### B. Taxonomy candidates requiring correction or adjudication

These are AI suggestions, not final taxonomy decisions:

| Sample | Current domain | AI observation | Suggested review |
|---|---|---|---|
| fa-exc-0103 | colloquial_noisy_input | The sample teaches interpretation of «باشه هرطور راحتی» in a conflict context; the core behavior is pragmatic tone/subtext, not noisy input. | Consider pragmatics_tone. |
| fa-exc-0207 | ambiguity_handling | The user supplies the audience and asks for a shorter reminder; the main behavior is tone/register adaptation and constraint retention, not ambiguity resolution. | Consider adaptive_communication or a better-supported primary domain after review. |
| fa-exc-0227 | colloquial_noisy_input | The sample is about interpreting sarcastic praise and responding without conflict; it does not contain noisy input. | Consider pragmatics_tone. |
| fa-exc-0190 | mixed (exception) | Distinguishing "bug" from the broader term "issue" is primarily lexical/semantic precision, with a brief explanation component. | Candidate: lexical_precision; remove the exception only after a reviewed, versioned correction. |

### C. Near-duplicate / repeated teaching patterns

| Candidate group | Observation | Recommendation |
|---|---|---|
| fa-exc-0003 / fa-exc-0071 | Same idiom «آب پاکی رو دست کسی ریختن», with essentially the same core definition. The existing semantic audit already identifies this as a strong near-duplicate. | Keep the richer multi-turn item provisionally; do not export both blindly. |
| fa-exc-0008 / fa-exc-0075 | Both interpret sarcastic remarks about lateness. The latter adds follow-up nuance and response generation. Existing audit treats them as related, not exact duplicates. | Keep both only if the pragmatic progression is considered useful. |
| fa-exc-0050 / fa-exc-0083 / fa-exc-0129 | All teach contextual disambiguation of «شیر» (milk/tap/lion). The latter two are especially close in the "شیر را بستم" context. | Treat as a duplicate-family candidate; retain the richest examples only after contextual adjudication. |
| fa-exc-0176 / fa-exc-0193 | Both explain the difference between «احتمالاً» and «ظاهراً», including the example of a possibly cancelled meeting. | Strong near-duplicate candidate; keep the richer example or diversify the second into a genuinely different contrast. |

## Positive observations

- V1–V3 contain useful foundational examples for lexical distinctions, idioms, sentence construction, colloquial Persian, and pragmatic interpretation.
- V4 adds more multi-turn constraint retention, corrections, planning, and audience/register adaptation.
- V5 expands long-context behavior, preserving constraints through topic changes, uncertainty calibration, and explicit recovery from unsupported assumptions.
- Many examples correctly avoid overclaiming intent from short social messages and distinguish evidence from inference.
- Several records model good correction behavior, provided the flawed preceding assistant turn is not used as a positive SFT target.

## Recommended automated review policy

Human review of every record is not a scalable requirement. Use a staged AI-assisted process instead:

1. **Automated structural checks:** schema, role order, IDs, revisions, metadata, exact duplicates and taxonomy validity.
2. **AI conversation review:** evaluate every full conversation for Persian naturalness, factual/semantic correctness, user-intent fidelity, constraint retention, completeness, tone, and domain fit.
3. **Assistant-turn review:** identify any assistant turn contradicted, retracted, or materially corrected later. Such turns must not silently enter positive SFT targets.
4. **Semantic deduplication:** AI proposes near-duplicate groups with explanations; merge decisions remain separate from lexical similarity scores.
5. **Confidence-based human sampling:** humans inspect only high-risk, low-confidence, disagreement, safety-sensitive, and randomly sampled records—not every record.
6. **Independent validation:** run a second reviewer model or independent pass on flagged records and on a random sample. AI review must remain labelled as AI review, not human review.
7. **Training export:** include only approved positive assistant targets, enforce family-level split isolation, and retain a complete provenance manifest.

## What this review does not authorize

- It does not change any staging JSONL.
- It does not mark any sample human_reviewed.
- It does not assign human scores, semantic-family IDs, or final data splits.
- It does not approve training.
- It does not certify all linguistic nuances as error-free; the listed findings are a first AI review pass and should be followed by an independent second pass on flagged/high-risk items.

## Immediate priority

Before adding more samples, fix the turn-level SFT supervision problem. Then revise the clearly incomplete examples, resolve the taxonomy candidates, and run a second independent AI pass. Increasing corpus size before these fixes would amplify avoidable training noise.
