# Sample-Level Taxonomy Adjudication Packet — Guide V1

## Purpose
This packet contains the complete conversation for every active general-track record whose primary domain is not one of the Taxonomy V2 canonical domains. Review the conversation itself and determine its actual primary trained behavior. The label-level suggestion is only a navigation aid.

## Required review procedure
1. Read every message in `conversation_json` in order. Do not adjudicate from the legacy label, subskills, or suggested mapping alone.
2. Write a concise description in `primary_behavior_assessment` identifying what behavior the assistant is expected to demonstrate.
3. Select exactly one canonical primary domain in `adjudicated_canonical_domain` only when the evidence supports it.
4. Set `decision` to `accepted_suggestion`, `changed_mapping`, or `needs_expert_review`. If the sample genuinely combines inseparable objectives or does not fit, explain it and request expert review rather than forcing a mapping.
5. Fill reviewer, date, and rationale. Rationale must cite specific turns or behavior in the conversation, not just repeat the domain name.
6. Preserve the CSV's sample IDs and source paths. Do not edit the source JSONL.

## Canonical choices
Use only the 16 domains listed in `docs/PERSIAN_DATASET_TAXONOMY_V2.md`. A primary domain represents the central behavior being trained; secondary skills may be documented separately only in a later reviewed migration.

## Important safeguards
- Label-level suggestions and confidence values are not decisions.
- A single historical label may map to different canonical domains for different samples.
- Do not assign semantic family IDs, data splits, review scores, or training approval in this phase.
- Do not mark synthetic records as human-reviewed merely because their taxonomy was adjudicated.
- Accepted mappings must later be applied through traceable, versioned superseding revisions after a separate migration review.
