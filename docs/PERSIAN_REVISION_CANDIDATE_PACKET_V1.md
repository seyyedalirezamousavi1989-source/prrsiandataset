# Persian Revision Candidate Packet V1

**Date:** 2026-11-13  
**Purpose:** prepare a small, traceable set of possible edits for human adjudication.  
**Status:** all proposals are `pending_human_review`; none is accepted, applied to staging, or eligible for training.

This packet was prepared after re-fetching the exact canonical source records. The source JSONL files remain unchanged. A proposal is not a verdict: reviewers may accept, revise again, or reject each item independently.

## Candidate 1 — `fa-adv-0013`

**Source:** `data/staging/advanced_pilot_v2.jsonl`  
**Focus:** natural formal register; preserve condition and consequence.

**Current assistant answer**

> در صورت واریز نشدن وجه تا فردا، امکان ارسال سفارش وجود نخواهد داشت.

**Proposed alternative**

> اگر وجه تا فردا واریز نشود، امکان ارسال سفارش را نداریم.

**Reason:** the current sentence is grammatical and suitably formal, but uses a heavier nominal construction. The alternative is more direct and still professional. The reviewer should decide whether the sample intends ordinary professional formality or deliberately bureaucratic wording.

**Status:** pending human review. Not an error correction.

## Candidate 2 — `fa-exc-0017`

**Source:** `data/staging/persian_language_excellence_v1.jsonl`  
**Focus:** explicit register guidance.

**Current assistant answer**

> بسته به میزان رسمیت می‌تونی بنویسی: «پیشاپیش از پاسخ‌گویی شما سپاسگزارم.» یا «خواهشمندم نتیجه را در فرصت مقتضی اعلام فرمایید.» گزینه اول معمولاً گرم‌تر و کم‌تکلف‌تره.

**Proposed alternative**

> برای پایان نامه رسمی می‌تونی بنویسی: «پیشاپیش از پاسخ‌گویی شما سپاسگزارم.» این گزینه رسمی و درعین‌حال خوش‌لحنه. اگر متن خیلی اداری و تشریفاتی باشه، می‌تونی بنویسی: «خواهشمندم نتیجه را در فرصت مقتضی اعلام فرمایید.» این دومی در مکاتبات روزمره کمی سنگین‌تر به نظر می‌رسه.

**Reason:** the original is understandable, but does not clearly label how much more formal and ceremonial the second option sounds. The alternative makes the register contrast explicit.

**Status:** pending human review. The original is not grammatically wrong.

## Candidate 3 — `fa-exc-0044`

**Source:** `data/staging/persian_language_excellence_v2.jsonl`  
**Focus:** clarity and directness in professional email.

**Current assistant answer**

> سلام، وقت بخیر. فایل را دریافت کردم و آن را بررسی خواهم کرد. پس از جمع‌بندی، نتیجه را خدمتتان اطلاع می‌دهم. با سپاس

**Proposed alternative**

> سلام، وقت بخیر. فایل را دریافت کردم و آن را بررسی خواهم کرد. پس از بررسی، نتیجه را به شما اطلاع می‌دهم.  
> با سپاس

**Reason:** “پس از بررسی” directly describes the action requested by the user. “پس از جمع‌بندی” may imply an additional synthesis step that the user did not specify. “به شما اطلاع می‌دهم” is clear and professional without unnecessary ceremony.

**Status:** pending human review. Stylistic clarity refinement.

## Candidate 4 — `fa-exc-0068`

**Source:** `data/staging/persian_language_excellence_v3.jsonl`  
**Target:** the assistant's second message (the reply to “برای مادربزرگم توضیح می‌دم؛ با مثال ساده‌تر.”)  
**Focus:** technical accuracy of the analogy.

**Current message**

> فرض کن درِ خانه دو قفل داره. برای باز کردنش باید کلید هر دو قفل رو داشته باشی. در ورود دومرحله‌ای هم اول رمزت رو وارد می‌کنی و بعد یک کد جداگانه رو؛ پس اگر کسی فقط رمزت رو بدونه، هنوز نمی‌تونه به‌راحتی وارد حساب بشه.

**Proposed alternative**

> فرض کن برای ورود به یک ساختمان، علاوه بر کلید، باید کارت شناسایی‌ات رو هم نشون بدی. در ورود دومرحله‌ای هم بعد از وارد کردن رمز، یک تأیید جداگانه مثل کدی که روی گوشی‌ات میاد لازمه. این‌طوری اگر کسی فقط رمزت رو بدونه، هنوز یک مرحله دیگه برای ورود باقی می‌مونه.

**Reason:** the original “two locks/two keys” analogy may suggest two factors of the same kind. The alternative more clearly illustrates two different kinds of evidence, while remaining accessible. The final assistant message about not guaranteeing 100% security should remain unchanged.

**Status:** pending human technical and linguistic review.

## Candidate 5 — `fa-exc-0082`

**Source:** `data/staging/persian_language_excellence_v3.jsonl`  
**Target:** final assistant message.  
**Focus:** natural phrasing while preserving four sentences, calm mood, and avoiding a second use of «آرام».

**Current final sentence**

> من از پشت شیشه، رفت‌وآمد آهسته رهگذران را تماشا کردم.

**Proposed replacement sentence**

> من از پشت شیشه، رهگذرانی را تماشا کردم که بی‌شتاب از خیابان می‌گذشتند.

**Reason:** “رفت‌وآمد آهسته رهگذران” is understandable, but the alternative gives the sentence a more natural rhythm and expresses the unhurried mood without repeating «آرام». The reviewer must read the entire four-sentence paragraph after substitution and confirm the word «آرام» is not reintroduced.

**Status:** pending human review.

## Explicitly withdrawn candidate — `fa-adv-0048`

Do not edit this record. The canonical source already ends with the natural wording:

> وقتی موضوع برام روشن‌تر شد، دوباره با شما هماهنگ می‌کنم.

The earlier report quoted an outdated/incorrect sentence for this record. See [Correction Note V1](PERSIAN_LINGUISTIC_REVIEW_CORRECTION_V1.md).

## Adjudication and application protocol

For each candidate, a reviewer must record one of:
- `accept`
- `revise_again`
- `reject`

Record reviewer identity, review date, rationale and (where applicable) the final approved text. Only after explicit acceptance should a separate revision record be created with a new unique sample ID, a `supersedes_sample_id` link to the original, provenance and review metadata. Do not overwrite the original. Keep candidate files out of training exports until accepted and validated.

**Current gate:** 5 pending candidates; 1 withdrawn; 0 accepted; 0 source records changed.
