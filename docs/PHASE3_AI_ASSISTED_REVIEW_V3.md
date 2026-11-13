# AI-Assisted Linguistic and Behavioral Review — Advanced Pilot v3

**Review scope:** all 15 records in `data/staging/advanced_pilot_v3.jsonl`  
**Review type:** model-assisted editorial inspection, not human review and not an automated validator run.  
**Source blob inspected:** `f6ccf2647b368170bb324b29c7d27593379ffdd1`  
**Review date:** 2026-11-13

## Important status boundary

This report records a preliminary AI-assisted review only. It does not change any record's `quality.review_status`; all 15 records remain `unreviewed`. No human linguistic review, full JSON Schema validation, tokenizer audit, benchmark, or model training was performed.

## Record-by-record findings

| Sample | Preliminary result | Findings / recommended action |
|---|---|---|
| fa-adv-0016 | Minor style improvement | Natural and proportionate overall. The closing sentence is slightly therapeutic/formulaic for a casual greeting. Consider a simpler line such as «خوش اومدی؛ امیدوارم بقیه روزت آروم‌تر بگذره.» Optional, not a blocker. |
| fa-adv-0017 | Pass | Correctly incorporates the raincoat and preserves the rest of the checklist. Final list is coherent and context-aware. «لباس گرم» is a little broad but acceptable. |
| fa-adv-0018 | **Revise — material constraint issue** | The user changes Saturday to Friday, then says Tuesday is better than Monday. The assistant's final answer unexpectedly changes Friday to Sunday and Wednesday to Thursday. This violates the rule to preserve unchanged constraints and invents a schedule change. Do not silently choose a new day. Better final response: «پس جمعه و سه‌شنبه رو نگه می‌داریم. برای اینکه جلسه سوم هم پشت‌سرهم با این دو روز نباشه، چهارشنبه مناسب نیست؛ ترجیح می‌دی یکشنبه باشه یا پنجشنبه؟» However, Thursday is adjacent to Friday, so the best single clarification is which third day the user prefers, while preserving Friday and Tuesday. |
| fa-adv-0019 | Pass | Natural Persian-English code-switching for a software team. The message clearly distinguishes postponement from cancellation. |
| fa-adv-0020 | Pass | Tone adjustment is successful: firmer without becoming rude. The response stays focused on delivery risk and workload. |
| fa-adv-0021 | Pass with small precision note | Properly avoids diagnosing the battery from limited evidence and asks relevant follow-up questions. «فشار زیاد به سیستم» is broad; it may be more precise to ask whether the laptop gets hot or the fan becomes loud under load. |
| fa-adv-0022 | Pass | Meets the requested friendly announcement, stays under 12 words, and contains no exclamation mark. |
| fa-adv-0023 | **Revise — unsupported confirmation** | The assistant first says «درسته» as if it can confirm the two earlier versions, although neither version appears in this record. The later honesty about not seeing the full text is good. Replace the first assistant turn with a neutral acknowledgment such as «متوجه‌ام؛ منظورت همون نسخه خودمونی‌تره.» Then keep the final request to resend the missing text. |
| fa-adv-0024 | Minor factual/intent drift | The rewrite is friendly and short, but it adds «جلسه کوتاه» even though the user did not say the meeting would be short. Remove «کوتاه» to preserve meaning: «بچه‌ها، فردا ساعت ۱۰ جلسه داریم؛ خوشحال می‌شم همتون باشید.» |
| fa-adv-0025 | Pass | Advice adapts appropriately to the limited budget and avoids pressuring the user. |
| fa-adv-0026 | **Revise — awkward phrasing** | «بدون دونستن جزئیات داخلی هم» is understandable but clunky. More idiomatic: «در نرم‌افزار هم کمک می‌کنه دو برنامه بدون اینکه لازم باشه از سازوکار داخلی هم خبر داشته باشن، با هم ارتباط بگیرن.» A shorter alternative: «...بدون اینکه لازم باشه از جزئیات فنی هم خبر داشته باشن، با هم ارتباط بگیرن.» |
| fa-adv-0027 | Pass | Handles the topic switch and explicitly retains the interview-question context for later. The final reference is supported by the earlier visible list. |
| fa-adv-0028 | Pass | Clear, respectful boundary-setting; the follow-up does not encourage overexplaining or making promises. |
| fa-adv-0029 | Pass | Both calculations are correct: 15% of 800,000 is 120,000; discounted price is 680,000; with 45,000 shipping the total is 725,000. |
| fa-adv-0030 | Pass | The formal rewrite preserves the message and deadline while remaining natural rather than overly stiff. |

## Summary

- Records inspected: **15 / 15**
- Clear revision candidates: **3** — fa-adv-0018, fa-adv-0023, fa-adv-0026
- Minor optional refinements: **2** — fa-adv-0016, fa-adv-0024
- Other records: **10** have no material issue identified in this preliminary pass; fa-adv-0021 has only a small precision suggestion.
- JSON parse and structural checks are tracked separately; this editorial pass does not replace them.

## Recommended next actions

1. Correct the three material candidates and decide whether to apply the two optional refinements. Preserve the original v3 file as an immutable staging snapshot; create a new versioned batch or patch rather than silently overwriting it.
2. Have a fluent Persian-speaking human review the actual wording and approve/reject each proposed change. Only then may the corresponding records be marked `human_reviewed`.
3. After editorial decisions, run the repository's validator and a dedicated schema/deduplication pipeline. Do not begin training yet.
