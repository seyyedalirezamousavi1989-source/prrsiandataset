# Correction Note — Persian Linguistic Review V1

**Date:** 2026-11-13  
**Related report:** [Persian Linguistic Review V1](PERSIAN_LINGUISTIC_REVIEW_V1.md)

## Important correction: `fa-adv-0048`

The initial review report incorrectly quoted the final assistant message as:

> به‌محض اینکه تصویر روشن‌تری از موضوع داشته باشم، دوباره با شما هماهنگ می‌کنم.

A fresh retrieval of the canonical staging record `data/staging/advanced_pilot_v5.jsonl` confirms that the actual current final message is:

> وقتی موضوع برام روشن‌تر شد، دوباره با شما هماهنگ می‌کنم.

This current wording is already natural and appropriate for the user's request (“a little more formal, but not stiff”). The proposed change for this sample is therefore withdrawn. **Do not revise `fa-adv-0048` on the basis of the earlier report.**

This correction illustrates why every proposed edit must be checked against the current source record immediately before creating a patch.

## Updated disposition

- `fa-adv-0048`: retain current wording; remove from revision candidates.
- `fa-adv-0013`: optional clarity/register refinement; current wording is grammatically acceptable.
- `fa-exc-0017`: clarify the register distinction for the very formal option; not a grammar error.
- `fa-exc-0044`: optional clarity refinement (“پس از بررسی” rather than “پس از جمع‌بندی”).
- `fa-exc-0068`: inspect the two-factor analogy for technical precision.
- `fa-exc-0082`: consider a more idiomatic final sentence while preserving the calm atmosphere and four-sentence constraint.

No source JSONL records were modified. This note supersedes the incorrect `fa-adv-0048` recommendation in the earlier review report.
