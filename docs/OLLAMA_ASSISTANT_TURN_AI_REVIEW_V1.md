# Local Ollama Assistant-Turn AI Review V1

## What it does
`scripts/review_assistant_turns_ollama.py` reads explicitly supplied general-track JSONL files, excludes superseded predecessors, sends each active conversation to a local Ollama chat endpoint, and writes one AI-provisional annotation per sample. Source files are read-only.

Each assistant message is reviewed independently with:
- `positive_target`
- `negative_or_demonstration_only`
- `needs_revision`

The model must return a Persian rationale, self-reported confidence, evidence message indices, and issue tags for every assistant turn. `message_index` always means the original position in the complete conversation array. For compatibility with local models that mistakenly number assistant-only turns from zero, the parser can safely map a complete `0..N-1` assistant-ordinal sequence back to the original assistant message indices; saved annotations always use canonical original indices. Exact original indices take precedence.

## Run a small pilot first (PowerShell)
Make sure Ollama is running and the exact model tag is installed. Example:
```powershell
ollama list
python scripts/review_assistant_turns_ollama.py --model qwen3.5:9b --limit 10 --num-predict 2048 --output reports/ai_turn_review_pilot.jsonl data/staging/persian_language_excellence_v1.jsonl
```
The model name above is an example only. Use the exact installed tag shown by `ollama list`.

Continue a partially completed run using the same model, endpoint, and identical source files:
```powershell
python scripts/review_assistant_turns_ollama.py --model qwen3.5:9b --resume --num-predict 2048 --output reports/ai_turn_review_pilot.jsonl data/staging/persian_language_excellence_v1.jsonl
```

For a full corpus review, use a new output path and explicitly list all intended general-track files. Keep the separate identity and Forex tracks out of this run.

Optional controls:
- `--base-url`: Ollama endpoint (default `http://127.0.0.1:11434`)
- `--timeout`: request timeout in seconds (default 300)
- `--num-ctx`: optional Ollama context size
- `--num-predict`: maximum output tokens per reviewed conversation (default `2048`)
- `--pause`: seconds between records
- `--limit`: number of new records in this invocation

## Strict JSON-schema output (prompt V3)
- Ollama receives a JSON Schema via its `format` field, not merely the generic `format: json` mode. The schema requires the six exact assistant-turn fields and rejects additional properties.
- Parser errors now show expected, actual, missing, and extra field names, so a model-format regression is diagnosable without exposing the entire conversation.

## Index compatibility fix (prompt V3)
- Prompt version `persian_turn_reviewer_v3` explicitly demonstrates that assistant messages at original positions 1 and 3 must be returned as indices 1 and 3, not 0 and 1.
- If a model still returns a complete assistant-only ordinal sequence (`0..N-1`), the parser maps it to the sorted original assistant message positions. Partial, duplicated, or otherwise ambiguous index sets are rejected.
- The normalized JSONL stores only original conversation indices, so downstream turn-level export remains consistent.

## Safety and provenance
- AI results are always `ai_provisional`; they are not human certification.
- The model cannot assign human scores, semantic families, dataset splits, or training approval.
- Source record hashes are embedded in each annotation.
- A sidecar manifest binds resume to the exact source-file hashes, model tag, endpoint, prompt version, and annotation version. Resume is rejected if any of these differ.
- Output is append-only; existing output is never overwritten.
- Each successful JSONL annotation is flushed and `fsync`'d before the manifest is atomically updated. The manifest's `completed_records` count is updated after every saved record.
- On `--resume`, the script validates the saved annotations against source hashes and recomputes progress from the append-only JSONL. This repairs stale progress counters produced by older versions; it does not invent or alter annotations.
- The manifest's `complete` field becomes true only when every active source record has a validated annotation. It means only that processing finished, not that the judgments are correct.
- Empty or malformed Ollama responses are retried up to three times. Final errors include the sample ID and available Ollama response metadata (such as `done_reason`, token counts, and message keys). The output-token limit can be raised with `--num-predict` when a conversation has many assistant turns.
- The `/api/chat` request explicitly sets top-level `think: false`. The reviewer requires a final JSON annotation, not a separate reasoning trace; this also avoids a known Qwen3.5 failure mode where the thinking channel can consume generation while `message.content` stays empty.
- Conversation contents are treated as untrusted data. Prompt-injection resistance is not guaranteed.
- Confidence is self-reported by the model and is not calibrated.

## Recommended evaluation before scaling
Run a 10-record pilot using a modest model, then repeat the same pilot with a second independent reviewer model. Compare disagreements and low-confidence decisions, inspect all flagged high-impact cases, and only then decide whether to scale. Do not blindly average labels or feed AI annotations directly into the training exporter.

The guarded turn-level exporter still independently requires human-reviewed record status, all seven human scores, semantic family IDs, and valid leakage-safe splits. This reviewer does not bypass those gates.
