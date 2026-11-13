# Persian V5 Human Adjudication Packet V1

**Date:** 2026-11-13  
**Scope:** three review cases surfaced by the V5 post-build audit.  
**Status:** pending human decisions; no decision is pre-filled.

This packet is a decision aid, not a human review. The authoring assistant has not marked any candidate accepted, rejected, or linguistically certified. Keep source staging records unchanged until a reviewer records an explicit decision.

## Reviewer instructions

For each case:
1. Read the full source conversations in the linked JSONL files.
2. Decide whether the records teach distinct transferable behaviors or substantially the same behavior.
3. For taxonomy, select the primary domain that best describes the main behavior, not the incidental topic.
4. Record reviewer, date, rationale, and evidence.
5. Use only the decision vocabulary shown below. Do not infer a human decision from automated similarity scores.

Allowed duplicate-pair decisions:
- `keep_both`
- `keep_one`
- `revise_one`
- `needs_more_review`

Allowed taxonomy decisions:
- `lexical_precision`
- `explanation_reasoning`
- `other_canonical_domain` (name it and explain)
- `needs_more_review`

## Case A — Meeting-date correction pair

**Records**
- `fa-exc-0189` — `data/staging/advanced_pilot_v3.jsonl`
- `fa-exc-0243` — `data/staging/persian_language_excellence_v5_part9.jsonl`

**Why flagged:** both conversations correct the assistant's mistaken weekday for a meeting, preserving Wednesday as the correct day.

**Observable difference:** `fa-exc-0189` is a short, six-message exchange that explicitly preserves the unchanged 10:00 time and states that only the weekday changed. `fa-exc-0243` is longer; it revises a reminder message, acknowledges that the prior draft also contained the error, and responds to a user instruction not to guess dates.

**Reviewer question:** Is the added reminder repair and explicit source-of-truth instruction sufficiently distinct to justify keeping both, or is the teaching objective still too close?

**Decision:** ____________________  
**Reviewer / date:** ____________________  
**Rationale and evidence:**  
________________________________________________________________

## Case B — Sales, advertising, and causal inference pair

**Records**
- `fa-exc-0252` — `data/staging/persian_language_excellence_v5_part10.jsonl`
- `fa-exc-0260` — `data/staging/persian_language_excellence_v5_part10.jsonl`

**Why flagged:** both reject an unsupported conclusion that a change in advertising caused a sales outcome and discuss confounding factors.

**Observable difference:** `fa-exc-0252` focuses on a 12% sales increase, a campaign, and increased inventory; the final task is a concise management statement. `fa-exc-0260` focuses on falling sales, reduced advertising spend, and increased prices; it asks what analysis can be done with weekly data and requests a three-sentence executive summary.

**Reviewer question:** Do the different direction of change, confounders, and final tasks provide distinct learning value, or should one be revised to target a more distinct causal-reasoning skill?

**Decision:** ____________________  
**Reviewer / date:** ____________________  
**Rationale and evidence:**  
________________________________________________________________

## Case C — Non-canonical primary domain

**Record:** `fa-exc-0190` in `data/staging/advanced_pilot_v3.jsonl`

**Current metadata:** `domain=mixed`, `register=mixed`, `language=fa`, subskills `technical_explanation` and `code_switching`.

**Content focus:** explaining the difference between “bug” and “issue” for a team report.

Taxonomy V2 defines `mixed` as a register value, not a primary domain. It describes `lexical_precision` as distinctions among terms and `explanation_reasoning` as plain-language explanation and comparison. The sample's main teaching objective appears to be distinguishing two related technical terms, while explaining that distinction in a team-report context.

**Provisional mapping for reviewer consideration:** `lexical_precision`. This is a proposal only, not an accepted correction. The `code_switching` subskill may also need review because the conversation contains English technical terms, but the project taxonomy says ordinary technical loanwords alone do not automatically make a conversation `fa-en`.

**Decision:** ____________________  
**Reviewer / date:** ____________________  
**Rationale and evidence:**  
________________________________________________________________

## Record of decisions

| Case | Decision | Reviewer | Date | Approved action / revision ID |
|---|---|---|---|---|
| A — 0189 / 0243 | pending |  |  |  |
| B — 0252 / 0260 | pending |  |  |  |
| C — 0190 taxonomy | pending |  |  |  |

## After review

- Do not overwrite the original records.
- If a wording change is accepted, create a new revision record with a unique ID and `supersedes_sample_id`.
- If a taxonomy correction is accepted, record it as a versioned migration/revision; retain the original historical record.
- Keep all unresolved candidates out of any approved training export.
- Update the human review register only from actual reviewer-submitted decisions.

**Current status:** 3 cases prepared; 0 human decisions recorded; 0 source records changed.
