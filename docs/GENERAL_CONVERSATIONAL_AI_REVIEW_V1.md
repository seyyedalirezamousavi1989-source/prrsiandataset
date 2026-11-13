# General Conversational Staging — AI Review V1

**Review date:** 2026-11-13  
**Scope:** Historical general conversational staging: pilot_v0, pilot_v1, advanced_pilot_v2 through v7, and the V4 patch.  
**Coverage:** 104 raw records; five superseded predecessors excluded from the active review set, leaving 99 active general records. The separate 8-record identity track is intentionally not merged into this review.  
**Status:** AI-reviewed / provisional; not human-certified and not training-approved.

## Executive result

The 99 active general records were inspected in conversation context. This track is broadly usable as a compact conversational foundation: Persian is mostly natural, tasks are varied, and the examples cover clarification, tone adaptation, simple explanations, correction, planning, and truthfulness.

The main weaknesses are uneven sample depth, a few unsupported assumptions, some underdeveloped plans, and legacy taxonomy labels that do not always identify the actual behavior. The corpus should not be treated as ready for SFT solely because it passes structural CI.

## Record-level findings

| Sample | Finding | Severity | Recommendation |
|---|---|---|---|
| fa-adv-0049 | User asks for a short apology saying they will arrive late. Assistant adds «در راه هستم» even though the user never said they were already on the way. | High | Remove the unsupported status: «ببخشید، چند دقیقه‌ای تأخیر دارم. به‌محض مشخص‌شدن زمان رسیدنم اطلاع می‌دهم.» Or keep the original if no follow-up promise is intended. |
| fa-adv-0052 | First assistant answer invents a personal reason for arriving late; the next assistant turn correctly removes it after the user objects. | High, turn-level | Do not use the invented-reason assistant turn as a positive SFT target. Keep the correction turn as a positive target. |
| fa-adv-0043 | User requests a two-week Excel learning plan. The answer gives broad weekly topics and then says to divide them across ten workdays, but does not provide the actual day-by-day plan. | Medium | Produce a two-week schedule with the user's daily 45-minute limit and clearly stated weekend review/rest rules. |
| fa-adv-0055 | After the user removes day five and reserves the final two days for review, the assistant says it will redistribute the work but does not show the revised 10-day schedule. | Medium | Return the actual revised schedule, preserving the final two review-only days and one unavailable day. |
| fa-adv-0039 | The first rewrite changes «دیدم» into «بررسی کردم». The correction removes that implication but retains «مورد تأیید است», which can still imply approval. | Medium | If the user only viewed the file and did not approve it, use a neutral phrase such as «فایل را مشاهده کردم؛ لطفاً برای ارسال نهایی اقدام کنید» only if that matches the intended meaning. |
| fa-pilot-0012 | The assistant assumes the five available days are Saturday through Wednesday. The user did not specify country/weekend convention. | Low | Ask which five days or state the assumption explicitly. |
| fa-gen-0022 | Main behavior is interpreting possible subtext in «باشه، هر جور راحتی»; current label colloquial_persian is too broad. | Low / taxonomy | Consider pragmatics_tone. |
| fa-gen-0030 | User asks the meaning of «دستت درد نکنه»; this is idiom/lexical meaning, not ambiguity resolution. | Low / taxonomy | Consider lexical_precision or everyday_dialogue depending on intended primary behavior. |
| fa-adv-0004 | A direct translation request is labelled clarification_precision, although no clarification is needed. | Low / taxonomy | Consider instruction_following or translation_and_rewriting. |

## Repeated or related teaching patterns

These are candidates, not automatic duplicate decisions:

| Candidate group | Observation | Recommendation |
|---|---|---|
| fa-pilot-0010 / fa-adv-0011 | Both explain blockchain through a shared/distributed ledger analogy. The audience differs, but the core explanation is very similar. | Keep both only if audience adaptation is a deliberate training objective; otherwise diversify one example. |
| fa-gen-0019 / fa-exc-0099 / fa-adv-0044 | All explain RAM versus persistent storage with a temporary-workspace analogy. | Treat as a cross-file near-duplicate family candidate; retain variants only if they teach different levels or registers. |
| fa-pilot-0014 / fa-adv-0029 / fa-exc-0125 | Same 800,000 toman and 15% discount calculation appears in multiple records. | Replace repeated arithmetic values or make the follow-up reasoning materially different. |
| fa-adv-0045 / fa-exc-0157 | Both address setting boundaries with a colleague who messages after work. | Keep only if the conversational goals differ enough; otherwise consolidate or diversify. |
| fa-gen-0032 / fa-exc-0161 | Both are three-day travel-planning patterns, though destinations and constraints differ. | Keep as separate examples if destination-specific constraints and output completeness differ. |

## Superseded revisions

The five V4 patch records correctly supersede earlier records:
- fa-adv-0031 supersedes fa-adv-0016
- fa-adv-0032 supersedes fa-adv-0018
- fa-adv-0033 supersedes fa-adv-0023
- fa-adv-0034 supersedes fa-adv-0024
- fa-adv-0035 supersedes fa-adv-0026

The review and eventual exporter must continue to use active revisions only. Do not delete the historical predecessors.

## Quality observations

- The pilot records are mostly short, often one-turn examples. They are useful for basic response patterns but provide limited evidence of context retention over longer conversations.
- Advanced V2–V7 improve multi-turn behavior and constraint handling.
- The V4 patch is an appropriate non-destructive revision strategy, but a replacement should be checked for full task completion, not only the corrected phrase.
- Some records are intentionally short clarification prompts; shortness itself is not a defect when the task is to ask a necessary question.
- Keep identity training separate from general conversational SFT.

## Pipeline implications

The assistant-turn supervision issue identified in Persian Language Excellence AI Review V1 also applies here. In particular, fa-adv-0052 contains an unsupported initial assistant response followed by a correction. The current exporter copies every assistant turn, so turn-level labels and selective positive-target export are required before training.

No staging JSONL was changed. No human review status, quality score, semantic-family ID, final split, or training approval was assigned.

## Recommended next actions

1. Fix turn-level SFT supervision before exporting any conversational track.
2. Revise the high-severity unsupported assumption in fa-adv-0049 and mark the flawed turn in fa-adv-0052 as non-positive.
3. Complete the two underdeveloped plans.
4. Apply taxonomy review to the flagged legacy labels.
5. Run semantic near-duplicate review across all general and Persian Language Excellence files together, while keeping identity data separate.
6. Use AI review for the full corpus and reserve human spot checks for flagged, low-confidence, and random samples rather than requiring line-by-line human review.
