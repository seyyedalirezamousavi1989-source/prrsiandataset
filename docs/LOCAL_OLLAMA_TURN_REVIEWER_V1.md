# Local Ollama Assistant-Turn Reviewer V1

## Purpose
The script scripts/review_assistant_turns_ollama.py uses an installed local Ollama model to review each assistant turn in complete conversations. It creates a separate annotation JSONL file and does not modify source staging data.

Each assistant turn receives one of three labels:
- positive_target
- negative_or_demonstration_only
- needs_revision

Each label includes a Persian rationale, confidence estimate, evidence message indices, and issue tags.

## Pilot
First confirm the exact installed model tag:
    ollama list

Then review a small sample (replace the model and paths with those actually installed/present):
    python scripts/review_assistant_turns_ollama.py --model qwen3.5:4b --limit 10 --output reports/ai_turn_annotations_pilot.jsonl data/staging/persian_language_excellence_v1.jsonl

Do not include the separate identity or Forex tracks in this Persian-language review.

## Resume
The script flushes one complete record at a time. Continue an interrupted run using the same source files and output path:
    python scripts/review_assistant_turns_ollama.py --model qwen3.5:4b --resume --output reports/ai_turn_annotations_pilot.jsonl data/staging/persian_language_excellence_v1.jsonl

It checks each existing annotation against a hash of the exact source record and refuses to resume if that record changed. Existing output is never overwritten.

## Options
- --base-url: Ollama endpoint; default http://127.0.0.1:11434
- --timeout: request timeout in seconds; default 300
- --num-ctx: optional context override; omitted to respect the runtime default
- --limit: maximum new records per run
- --pause: delay between records
- --resume: append only missing records

## Safety and limitations
- Source JSONL is read-only. Superseded predecessors are excluded.
- The exact model tag returned by Ollama is recorded; no model identity is guessed.
- Conversation content is treated as untrusted data, not reviewer instructions.
- Invalid JSON, missing/extra turns, invalid labels, missing rationales, invalid confidence, or invalid evidence indices stop processing before that record is appended.
- Every record is flushed immediately so interrupted runs can resume.
- All results remain ai_provisional with reviewer_type=ai. No human scores, semantic families, splits, or training approvals are assigned.
- AI confidence is an estimate, not a calibrated probability. Local models can miss subtle Persian, pragmatic, and factual errors. Start with a small pilot and compare results with the existing expert review reports.
- This tool does not automatically approve annotations for training; all independent exporter gates remain in force.
