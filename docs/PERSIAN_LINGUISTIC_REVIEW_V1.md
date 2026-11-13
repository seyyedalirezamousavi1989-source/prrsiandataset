# Persian Linguistic Review — Targeted Findings V1

**Date:** 2026-11-13  
**Scope:** targeted manual reading of representative records from the legacy pilots and Persian Language Excellence batches, including multi-turn, rewriting, formal-register, explanation and pragmatic examples. This is a triage pass, not a claim that all 197 records have received full human linguistic certification.

## 1. Outcome

The reviewed material is generally understandable and often demonstrates useful conversational behaviors. Several examples are strong enough to retain provisionally. The main opportunities are not basic spelling failures; they are finer points of idiomatic phrasing, register calibration, translationese and analogy precision.

**No source JSONL record was changed in this pass.** Proposed edits below are review candidates. They must be adjudicated before being applied to staging or included in a training export.

## 2. Priority revision candidates

### P1 — `fa-adv-0048`: literal translation of an English idiom

**Current final answer**

> به‌محض اینکه تصویر روشن‌تری از موضوع داشته باشم، دوباره با شما هماهنگ می‌کنم.

The phrase «تصویر روشن‌تری از موضوع داشته باشم» is understandable, but it follows the English “a clearer picture” too closely and sounds less conversational than the requested “a little more formal, but not stiff” register.

**Suggested alternative**

> وقتی موضوع برام روشن‌تر شد، دوباره با شما هماهنگ می‌کنم.

This preserves the intended meaning while using a more idiomatic Persian construction. The user asked for a natural translation, then a moderately more formal version; this revision keeps that target.

**Disposition:** revise candidate; preserve original in history.

### P1 — `fa-exc-0082`: awkward collocation in the final sentence

**Current final sentence**

> من از پشت شیشه، رفت‌وآمد آهسته رهگذران را تماشا کردم.

«رفت‌وآمد آهسته رهگذران» is understandable, but «آهسته» describes the speed of their movement in a slightly unnatural way in this context. The task asks for a calm atmosphere, not necessarily slow walkers.

**Suggested alternative**

> من از پشت شیشه، عبور رهگذران را تماشا کردم.

This is simpler, natural and retains the quiet scene without repeating «آرام».

**Disposition:** revise candidate; re-check the complete four-sentence paragraph after replacement.

### P2 — `fa-adv-0013`: formal sentence is heavier than necessary

**Current answer**

> در صورت واریز نشدن وجه تا فردا، امکان ارسال سفارش وجود نخواهد داشت.

This is grammatically acceptable, but the nominal construction makes it sound bureaucratic. The sample is labelled formal and fluent, so a clearer formal version would teach a more useful target.

**Suggested alternative**

> اگر وجه تا فردا واریز نشود، امکان ارسال سفارش را نداریم.

**Disposition:** optional revision; retain the more formal version only if the intended target is explicitly administrative/legal prose.

### P2 — `fa-exc-0017`: one suggested closing is excessively formal

**Current option**

> خواهشمندم نتیجه را در فرصت مقتضی اعلام فرمایید.

This is valid in highly formal correspondence, but «فرصت مقتضی» and «اعلام فرمایید» together create a stiff, old-fashioned tone. The assistant already gives a warmer alternative, so the issue is mainly missing register guidance.

**Suggested clarification**

Label this option as «بسیار رسمی و اداری» and, for ordinary professional correspondence, prefer:

> ممنون می‌شوم نتیجه را در زمان مناسب به من اطلاع دهید.

**Disposition:** metadata/teaching clarification candidate, not an outright language error.

### P2 — `fa-exc-0044`: vague wording in a work email

**Current answer**

> سلام، وقت بخیر. فایل را دریافت کردم و آن را بررسی خواهم کرد. پس از جمع‌بندی، نتیجه را خدمتتان اطلاع می‌دهم. با سپاس

«پس از جمع‌بندی» is not wrong, but the user asked to say they received the file and will review it. «پس از بررسی» states the next action more directly.

**Suggested alternative**

> سلام، وقت بخیر. فایل را دریافت کردم و آن را بررسی خواهم کرد. پس از بررسی، نتیجه را به شما اطلاع می‌دهم.  
> با سپاس

**Disposition:** optional clarity revision.

## 3. Technical explanation candidate

### `fa-exc-0068`: two-factor authentication analogy

The sample explains two-factor authentication using a door with two locks and two keys. It is accessible, but may accidentally suggest that both factors are simply two keys of the same kind. Real two-factor authentication is strongest when the factors come from different categories (for example, something you know and something you have).

**Safer alternative for the analogy**

> فرض کن برای ورود به یک ساختمان، علاوه بر کلید، باید کارت شناسایی‌ات را هم نشان بدهی. در ورود دومرحله‌ای هم بعد از وارد کردن رمز، یک تأیید جداگانه مثل کدی که روی گوشی‌ات می‌آید لازم است.

Keep the existing final calibration statement that no method guarantees 100% security.

**Disposition:** technical-accuracy review candidate; verify terminology and explanation before changing the source record.

## 4. Examples that appear useful and should be retained provisionally

- `fa-exc-0001`: distinguishes «نگران»، «دلواپس» and «مضطرب» with context-sensitive examples.
- `fa-exc-0011`: gives alternatives for «اهمیت زیادی دارد» and correctly warns that «حساسیت خاصی دارم» is not always an exact synonym.
- `fa-exc-0030`: distinguishes a contrast relation from simple chronological sequence instead of choosing a conjunction blindly.
- `fa-exc-0032`: identifies pronoun-reference ambiguity and offers two explicit repairs.
- `fa-exc-0039`: distinguishes grammatical acceptability from contemporary stylistic naturalness.
- `fa-exc-0054`: repairs parallel structure without changing the intended meaning.
- `fa-exc-0067`: updates a corrected product weight and retains it in the shortened version.
- `fa-exc-0073`: follows successive corrections and removes the unsupported weekday when the user asks to say only «فردا».
- `fa-exc-0084`: respects the scope “spelling only” before producing a separate formal rewrite.
- `fa-exc-0085`: updates the session frequency from three to two and preserves the other constraints.

“Retain provisionally” does not mean human-approved or ready for training.

## 5. Cross-cutting recommendations

1. **Prefer idiomatic Persian over word-for-word equivalence.** Preserve intent, not the source-language metaphor.
2. **Teach register as a spectrum.** “Formal” should not automatically mean bureaucratic or archaic.
3. **Make examples contrastive.** When two phrases differ in formality or nuance, label the difference and give a natural context for each.
4. **Check analogies for hidden technical distortions.** A simple analogy must not teach the wrong underlying structure.
5. **Read multi-turn outputs as a whole.** A locally fluent sentence can still break an earlier constraint or make the final artifact inconsistent.
6. **Keep revision history.** Apply accepted changes as explicit superseding revisions rather than silently overwriting the original sample.

## 6. Recommended next operation

Create a small, reviewed revision batch containing only the candidates accepted by a Persian-language reviewer. Do not automatically apply all suggestions in this report. After approval, update the corresponding records with traceable supersession metadata, rerun schema/CI checks, and refresh semantic-deduplication findings.

**Status:** targeted linguistic triage complete; five language/style candidates and one technical-analogy candidate identified; no record has been marked human-reviewed and no staging data was modified.
