import csv, json, tempfile, unittest
from pathlib import Path
from split_taxonomy_review_batches import split, merge

FIELDS=["sample_id","source_file","legacy_domain","legacy_subskills","language","register","message_count","conversation_json","existing_review_notes","label_level_suggestion","suggestion_confidence","suggestion_rationale","primary_behavior_assessment","adjudicated_canonical_domain","decision","reviewer","review_date","adjudication_rationale"]
CANONICAL="## Canonical primary domains\n| Domain |\n|---|\n"+ "\n".join("| `"+x+"` |" for x in ["persian_fluency","everyday_dialogue","intent_understanding","context_continuity","ambiguity_handling","multi_turn_planning","instruction_following","colloquial_noisy_input","pragmatics_tone","lexical_precision","sentence_construction","explanation_reasoning","truthfulness","correction_recovery","emotional_support","adaptive_communication"])

