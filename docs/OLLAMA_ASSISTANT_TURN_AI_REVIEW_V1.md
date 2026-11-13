# Local Ollama Assistant-Turn AI Review V1

## What it does
`scripts/review_assistant_turns_ollama.py` reads explicitly supplied general-track JSONL files, excludes superseded predecessors, sends each active conversation to a local Ollama chat endpoint, and writes one AI-provisional annotation per sample. Source files are read-only.

Each assistant message is reviewed independently with:
- `positive_target`
- `negative_or_demonstration_only`
- `needs_revision`

The model must return a Persian rationale, self-reported confidence, evidence message indices, and issue tags for every assistant turn. The program validates exact turn coverage and evidence indices before saving an annotation.

## Run a small pilot first (PowerShell)
Make sure Ollama is running and the exact model tag is installed. Example:
```powershell
ollama list
python scripts/review_assistant_turns_ollama.py --model qwen3.5:9b --limit 10 --output reports/ai_turn_review_pilot.jsonl data/staging/advanced_pilot_v1.jsonl data/staging/advanced_pilot_v2.jsonl
```
The model name above is an example only. Use the exact installed tag shown by `ollama list`.

Continue a partially completed run using the same model, endpoint, and identical source files:
```powershell
python scripts/review_assistant_turns_ollama.py --model qwen3.5:9b --resume --output reports/ai_turn_review_pilot.jsonl data/staging/advanced_pilot_v1.jsonl data/staging/advanced_pilot_v2.jsonl
```

For a full corpus review, use a new output path and explicitly list all intended general-track files. Keep the separate identity and Forex tracks out of this run.

Optional controls:
- `--base-url`: Ollama endpoint (default `http://127.0.0.1:11434`)
- `--timeout`: request timeout in seconds (default 300)
- `--num-ctx`: optional Ollama context size
- `--pause`: seconds between records
- `--limit`: number of new records in this invocation

## Safety and provenance
- AI results are always `ai_provisional`; they are not human certification.
- The model cannot assign human scores, semantic families, dataset splits, or training approval.
- Source record hashes are embedded in each annotation.
- A sidecar manifest binds resume to the exact source-file hashes, model tag, endpoint, prompt version, and annotation version. Resume is rejected if any of these differ.
- Output is append-only; existing output is never overwritten.
- Each successful record is flushed to disk before continuing.
- The manifest's `complete` field means only that every active source record was processed, not that the judgments are correct.
- Conversation contents are treated as untrusted data. Prompt-injection resistance is not guaranteed.
- Confidence is self-reported by the model and is not calibrated.

## Recommended evaluation before scaling
Run a 10-record pilot using a modest model, then repeat the same pilot with a second independent reviewer model. Compare disagreements and low-confidence decisions, inspect all flagged high-impact cases, and only then decide whether to scale. Do not blindly average labels or feed AI annotations directly into the training exporter.

The guarded turn-level exporter still independently requires human-reviewed record status, all seven human scores, semantic family IDs, and valid leakage-safe splits. This reviewer does not bypass those gates.
