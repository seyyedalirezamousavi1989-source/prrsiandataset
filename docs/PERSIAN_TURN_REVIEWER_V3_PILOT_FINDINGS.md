# Persian Turn Reviewer V3 Pilot Findings

Status: AI-reviewer evaluation note; not human certification.
Date: 2026-11-14
Reviewer model: qwen3.5:9b
Prompt: persian_turn_reviewer_v3
Pilot scope: first 10 records of `data/staging/persian_language_excellence_v1.jsonl`
Source staging: read-only; no records modified.

## Recorded result

- Reviewed records: 10 of 24
- Assistant turns: 13
- `positive_target`: 12
- `needs_revision`: 1
- `negative_or_demonstration_only`: 0
- Output annotations: AI-provisional only
- Human certification: false
- Training approval: false
- Run completion for source: false (14 records remain)

## Findings to test in prompt V4

### fa-exc-0009 — context-dependent colloquial reference
The assistant says «پس از اون کتاب‌ها بوده که باید کمی بهش فرصت بدی تا راه بیفته» after the user explains that a historical novel started slowly. This is a natural contextual reference to books that take time to get going. V3 marked the turn `needs_revision` with `unclear_reference` and `incomplete_response`. The pilot analysis considers this a likely false positive because the context resolves the phrase and the assistant directly addresses the slow start.

### fa-exc-0005 — urgency weakened in rewrite
The requested phrase includes «در اسرع وقت». The assistant rewrite «ممنون می‌شم هر وقت فرصت کردی جوابم رو بدی» is polite and natural but weakens the urgency. A meaning-preserving alternative could be «ممنون می‌شم هرچه زودتر جوابم رو بدی». V4 should detect the lost time constraint as a concrete semantic-preservation issue.

### fa-exc-0003 — inaccurate rationale
The assistant's explanation of «آب پاکی رو دستش ریختن» is broadly aligned with giving someone a definitive negative answer / ending their hope. The V3 rationale described it as «شکست دادن کسی در چیزی که انتظار موفقیت داشته», which is not an accurate paraphrase. This highlights rationale quality independently of label correctness.

## Interpretation and next gate

A 10-record pilot is too small to establish reviewer precision/recall or statistical calibration. These findings are targeted regression cases, not a substitute for human adjudication. V4 should be tested against the same 10 records using a new output and manifest; never resume the V3 output with V4. Do not scale to the full 260-record Persian Language Excellence track until V4 comparison and targeted adjudication are complete.
