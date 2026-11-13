# Historical Taxonomy Mapping — Human Adjudication Guide V1

## Purpose

This packet proposes label-level mappings from historical primary-domain labels to the 16 canonical domains in Taxonomy V2. It is a review aid only. A label-level suggestion is not a decision about any individual sample.

## Mandatory rules

1. Read the complete conversation for every sample before accepting a mapping.
2. Choose the canonical domain that represents the primary behavior actually trained. Use secondary capabilities in `subskills` only after separately reviewing them.
3. Treat `requires_record_level_review` as an explicit refusal to infer a domain from a vague or multi-purpose label.
4. Do not use a label's name, lexical similarity, or this suggested mapping as sufficient evidence.
5. Keep the source JSONL unchanged. Accepted decisions must later be represented as versioned superseding revisions with provenance and a traceable audit trail.
6. Do not assign semantic family IDs or final train/eval/test splits in this phase.
7. Do not mark synthetic data human-reviewed and do not approve training.

## Decision protocol

For each legacy label, the reviewer should either:
- accept the proposed canonical domain with a rationale grounded in the actual samples;
- replace it with another canonical domain and explain why; or
- mark it `needs_record_level_review` / `unresolved` if records under the same legacy label have different primary behaviors.

A single old label may legitimately split across canonical domains when its records represent different target behaviors. Do not force one mapping merely to make the CSV tidy.

## Confidence meaning

- `high`: close semantic match, still requires sample-level confirmation.
- `medium`: plausible candidate, sample-level confirmation is especially important.
- `requires_record_level_review`: no safe label-level mapping is proposed.

Confidence is not a probability and does not mean approved.

## Scope and exclusions

The generator excludes the identity track and superseded predecessor records. It counts active records per legacy label. Canonical labels are not included in this legacy mapping CSV. Missing or invalid domain values are reported separately in the generator summary.

The generator never edits staging files, assigns mappings, families, splits, or training approval.
