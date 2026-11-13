# Near-Duplicate Adjudication Packet V1

**Date:** 2026-11-13
**Purpose:** Put the six highest-priority candidate pairs in one readable place so a Persian-fluent human reviewer can make explicit keep/revise/exclude decisions.
**Status:** AI-assisted triage only. No human decisions have been entered; no source records have been modified.

## How to use this packet

For each pair, read both full conversations, assess whether they teach meaningfully different behavior, then fill the human decision fields. Similar subject matter is not sufficient reason to delete a sample. Keep the original staging records unchanged until decisions are approved and versioned.

Decision options: `keep_both`, `keep_a_only`, `keep_b_only`, `revision_chain`, `revise_a`, `revise_b`, `reject_a`, `reject_b`, `needs_more_review`.

---

## fa-adv-0004 vs fa-gen-0036 — ترجمه جمله و محدودیت خروجی

**AI-assisted recommendation (not a human verdict):** فعلاً هر دو را نگه داریم؛ نمونه دوم صراحتاً «فقط ترجمه» را آموزش می‌دهد. اگر در بررسی انسانی تفاوت رفتاری معناداری دیده نشد، یکی در manifest نهایی انتخاب شود.

### fa-adv-0004
- **کاربر:** لطفاً این جمله رو به انگلیسی ترجمه کن: فردا باهات تماس می‌گیرم.
- **دستیار:** I'll call you tomorrow.

### fa-gen-0036
- **کاربر:** فقط این جمله رو به انگلیسی ترجمه کن: فردا باهات تماس می‌گیرم.
- **دستیار:** I'll call you tomorrow.

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  


## fa-adv-0024 vs fa-adv-0034 — زنجیره اصلاح نسخه

**AI-assisted recommendation (not a human verdict):** این‌ها دو نمونه مستقل نیستند. fa-adv-0034 نسخه جایگزین fa-adv-0024 است. نسخه جدید در manifest فعال باشد؛ نسخه قدیمی برای تاریخچه حفظ شود.

### fa-adv-0024
- **کاربر:** یه متن دعوت برای جلسه فردا ساعت ۱۰ بنویس، خیلی کوتاه.
- **دستیار:** از شما دعوت می‌کنیم فردا ساعت ۱۰ در جلسه حضور داشته باشید.
- **کاربر:** نگفتم رسمی باشه؛ برای گروه دوستامه.
- **دستیار:** درست می‌گی، لحنش زیادی رسمی شد: «بچه‌ها، فردا ساعت ۱۰ یه جلسه کوتاه داریم؛ خوشحال می‌شم همتون باشید.»

### fa-adv-0034
- **کاربر:** یه متن دعوت برای جلسه فردا ساعت ۱۰ بنویس، خیلی کوتاه.
- **دستیار:** از شما دعوت می‌کنیم فردا ساعت ۱۰ در جلسه حضور داشته باشید.
- **کاربر:** نگفتم رسمی باشه؛ برای گروه دوستامه.
- **دستیار:** درست می‌گی، لحنش زیادی رسمی شد: «بچه‌ها، فردا ساعت ۱۰ جلسه داریم؛ خوشحال می‌شم همتون باشید.»

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  


## fa-adv-0029 vs fa-pilot-0014 — محاسبه تخفیف

**AI-assisted recommendation (not a human verdict):** هر دو را موقتاً نگه داریم: نمونه ساده، محاسبه تخفیف را می‌سنجد؛ نمونه چندمرحله‌ای، حفظ زمینه و افزودن هزینه ارسال را نیز می‌سنجد.

### fa-adv-0029
- **کاربر:** یه محصول ۸۰۰ هزار تومنی ۱۵ درصد تخفیف خورده. قیمت نهاییش چقدر می‌شه؟
- **دستیار:** مقدار تخفیف ۱۲۰ هزار تومنه (۸۰۰٬۰۰۰ × ۰٫۱۵). پس قیمت نهایی می‌شه ۶۸۰ هزار تومان.
- **کاربر:** اگه هزینه ارسال ۴۵ هزار تومن هم داشته باشه؟
- **دستیار:** مبلغ قابل پرداخت با احتساب ارسال می‌شه ۷۲۵ هزار تومان؛ یعنی ۶۸۰ هزار تومان قیمت محصول به‌علاوه ۴۵ هزار تومان ارسال.

### fa-pilot-0014
- **کاربر:** اگه یه محصول ۸۰۰ هزار تومن باشه و ۱۵ درصد تخفیف بخوره، قیمت نهاییش چقدره؟
- **دستیار:** مقدار تخفیف می‌شه ۱۲۰ هزار تومان (۸۰۰٬۰۰۰ × ۰٫۱۵). پس قیمت نهایی برابر با **۶۸۰ هزار تومان** است.

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  


## fa-adv-0039 vs fa-gen-0020 — بازنویسی رسمی و اصلاح معنای ناخواسته

**AI-assisted recommendation (not a human verdict):** نمونه چندنوبتی را برای آموزش اصلاح خطا نگه داریم، اما نمونه تک‌نوبتی را هم بررسی کنیم: در هر دو پاسخ «دیدم» به «بررسی کردم» تبدیل شده و این تغییر معنا باید در بازنویسی اولیه هم اصلاح شود.

### fa-adv-0039
- **کاربر:** این جمله رو رسمی کن: «فایل رو دیدم، اوکیه، بفرستش.»
- **دستیار:** فایل را بررسی کردم و مورد تأیید است؛ لطفاً آن را ارسال کنید.
- **کاربر:** «بررسی کردم» رو نگو، فقط دیدمش.
- **دستیار:** درست می‌گی؛ نباید معنای بررسی‌کردن رو اضافه می‌کردم: «فایل را مشاهده کردم و مورد تأیید است؛ لطفاً آن را ارسال کنید.»

### fa-gen-0020
- **کاربر:** این رو رسمی‌تر کن: سلام، فایل رو دیدم، اوکیه، بفرست بره.
- **دستیار:** سلام، فایل را بررسی کردم و مورد تأیید است؛ لطفاً آن را ارسال کنید.

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  


## fa-adv-0007 vs fa-adv-0065 — تعداد دقیق و قالب عنوان‌ها

**AI-assisted recommendation (not a human verdict):** هر دو را نگه داریم؛ تعداد، شماره‌گذاری و ممنوعیت توضیح متفاوت‌اند. در بازبینی، دقیقاً تعداد و قالب خروجی کنترل شود.

### fa-adv-0007
- **کاربر:** سه تا عنوان برای مقاله درباره خواب بهتر پیشنهاد بده؛ فقط عنوان‌ها رو بنویس.
- **دستیار:** ۱. خواب باکیفیت؛ از کجا شروع کنیم؟
۲. عادت‌های ساده برای داشتن خوابی آرام‌تر
۳. نقش برنامه منظم در بهبود کیفیت خواب

### fa-adv-0065
- **کاربر:** چهار عنوان برای مقاله درباره خواب سالم پیشنهاد بده. فقط عنوان‌ها، بدون شماره و توضیح.
- **دستیار:** چرا خواب باکیفیت مهم‌تر از خواب طولانی است؟
عادت‌های ساده برای داشتن خواب آرام
تأثیر نور صفحه‌نمایش بر چرخه خواب
چطور برنامه خواب منظمی بسازیم؟

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  


## fa-adv-0026 vs fa-gen-0024 — توضیح API با تشبیه پیشخدمت رستوران

**AI-assisted recommendation (not a human verdict):** هر دو از یک تشبیه تکراری استفاده می‌کنند. تفاوت طول و سطح مخاطب وجود دارد، اما برای تنوع بهتر است یکی از دو پاسخ در نسخه بعدی با تشبیه یا توضیح متفاوت بازنویسی شود؛ فعلاً حذف خودکار نشود.

### fa-adv-0026
- **کاربر:** API رو برای کسی توضیح بده که برنامه‌نویس نیست؛ خیلی کوتاه.
- **دستیار:** API مثل پیشخدمت رستورانه: درخواستت رو به بخش مربوط می‌رسونه و نتیجه رو برمی‌گردونه. در نرم‌افزار هم کمک می‌کنه دو برنامه بدون دونستن جزئیات داخلی هم، با هم ارتباط بگیرن.

### fa-gen-0024
- **کاربر:** API رو خیلی ساده توضیح بده؛ فرض کن هیچی از برنامه‌نویسی نمی‌دونم.
- **دستیار:** API رو مثل پیشخدمت رستوران تصور کن: تو درخواستت رو به پیشخدمت می‌گی، اون درخواست رو به آشپزخونه می‌رسونه و نتیجه رو برمی‌گردونه. در نرم‌افزار هم API راهی مشخصه که دو برنامه از طریقش از هم درخواست می‌گیرن و جواب می‌دن.

**Human decision:** ____________________  
**Reviewer:** ____________________  
**Date:** ____________________  
**Reason / required edit:** ____________________  

---

## Consolidated decision log

| Pair | Human decision | Reviewer | Date | Reason / patch ID |
|---|---|---|---|---|
| `fa-adv-0004` / `fa-gen-0036` | pending | — | — | — |
| `fa-adv-0024` / `fa-adv-0034` | pending | — | — | — |
| `fa-adv-0029` / `fa-pilot-0014` | pending | — | — | — |
| `fa-adv-0039` / `fa-gen-0020` | pending | — | — | — |
| `fa-adv-0007` / `fa-adv-0065` | pending | — | — | — |
| `fa-adv-0026` / `fa-gen-0024` | pending | — | — | — |

## Important data-integrity rules

1. Do not delete or overwrite staging examples as part of adjudication.
2. For a revised sample, create a new versioned record and set `supersedes_sample_id` to the exact prior sample ID.
3. Keep revision history out of the final training manifest except the selected active revision.
4. Do not change `quality.review_status` to `human_reviewed` unless a human actually reviewed the full sample.
5. Identity records and specialist Forex/XAUUSD records remain outside this general-Persian adjudication packet.
6. After the decisions are recorded, update the review register and only then prepare grouped split manifests.