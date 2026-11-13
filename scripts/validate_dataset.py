#!/usr/bin/env python3
"""Validate PersianDataset JSONL records and cross-file corpus integrity (stdlib only)."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import date
from collections import Counter
from pathlib import Path

ROLES = {"system", "user", "assistant"}
SPLITS = {"train", "validation", "test", "challenge"}
LANGUAGES = {"fa", "fa-en", "multilingual"}
REGISTERS = {"colloquial", "neutral", "formal", "mixed"}
TOP = {"sample_id", "messages", "domain", "split", "language", "register", "subskills", "quality", "metadata"}
QUALITY = {"intent_fidelity", "context_use", "persian_fluency", "accuracy", "instruction_adherence", "tone_appropriateness", "non_redundancy", "review_status", "reviewer", "reviewed_at"}
QUALITY_SCORES = {"intent_fidelity", "context_use", "persian_fluency", "accuracy", "instruction_adherence", "tone_appropriateness", "non_redundancy"}
PERSIAN = re.compile(r"[\u0600-\u06FF]")
CANONICAL_DOMAINS = {
    "persian_fluency", "everyday_dialogue", "intent_understanding",
    "context_continuity", "ambiguity_handling", "multi_turn_planning",
    "instruction_following", "colloquial_noisy_input", "pragmatics_tone",
    "lexical_precision", "sentence_construction", "explanation_reasoning",
    "truthfulness", "correction_recovery", "emotional_support",
    "adaptive_communication",
}

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def validate_record(row, path, line):
    errors, warnings, where = [], [], f"{path}:{line}"
    if not isinstance(row, dict):
        return [f"{where}: record must be a JSON object"], warnings
    extra = set(row) - TOP
    if extra: errors.append(f"{where}: unknown top-level fields: {sorted(extra)}")
    for key in ("sample_id", "domain"):
        if not nonempty(row.get(key)): errors.append(f"{where}: {key} must be a non-empty string")
    if row.get("language") not in LANGUAGES: errors.append(f"{where}: unsupported or missing language")
    if row.get("register") not in REGISTERS: errors.append(f"{where}: unsupported or missing register")
    if row.get("split") not in SPLITS: errors.append(f"{where}: unsupported or missing split")
    if "subskills" in row:
        skills = row["subskills"]
        if not isinstance(skills, list) or any(not nonempty(x) for x in skills) or (isinstance(skills, list) and len(skills) != len(set(skills))):
            errors.append(f"{where}: subskills must be unique non-empty strings")
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) < 2:
        errors.append(f"{where}: messages must contain at least two items")
        messages = []
    roles, texts = [], []
    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            errors.append(f"{where}: message {i} must be an object"); continue
        if set(msg) - {"role", "content"}: errors.append(f"{where}: message {i} has unknown fields")
        role, text = msg.get("role"), msg.get("content")
        if role not in ROLES: errors.append(f"{where}: message {i} has invalid role {role!r}")
        else: roles.append(role)
        if not nonempty(text): errors.append(f"{where}: message {i} content must be non-empty text")
        else: texts.append(text)
    if roles:
        if roles[0] not in {"user", "system"}: errors.append(f"{where}: conversation must begin with user or system")
        if "user" not in roles or "assistant" not in roles: errors.append(f"{where}: conversation needs user and assistant turns")
        if roles[-1] != "assistant": errors.append(f"{where}: conversation must end with assistant")
        if "system" in roles[1:]: errors.append(f"{where}: system message is only allowed first")
        conversational = [r for r in roles if r != "system"]
        if any(a == b for a, b in zip(conversational, conversational[1:])):
            errors.append(f"{where}: user and assistant roles must alternate")
    if row.get("language") in {"fa", "fa-en"} and texts and not PERSIAN.search("\n".join(texts)):
        errors.append(f"{where}: Persian-language record contains no Persian-script text")
    meta = row.get("metadata")
    if not isinstance(meta, dict): errors.append(f"{where}: metadata must be an object")
    else:
        for key in ("provenance", "created_by"):
            if not nonempty(meta.get(key)): errors.append(f"{where}: metadata.{key} must be non-empty")
        for key in ("source_reference", "license", "generator_model", "review_notes", "supersedes_sample_id"):
            if key in meta and meta[key] is not None and not isinstance(meta[key], str):
                errors.append(f"{where}: metadata.{key} must be a string or null")
    quality = row.get("quality")
    if quality is None: warnings.append(f"{where}: quality.review_status missing; legacy record is not assumed reviewed")
    elif not isinstance(quality, dict): errors.append(f"{where}: quality must be an object")
    else:
        unknown = set(quality) - QUALITY
        if unknown: errors.append(f"{where}: unknown quality fields: {sorted(unknown)}")
        for key, value in quality.items():
            if key == "review_status":
                if value not in {"unreviewed", "machine_checked", "human_reviewed", "rejected"}:
                    errors.append(f"{where}: invalid quality.review_status")
            elif key in QUALITY_SCORES:
                if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                    errors.append(f"{where}: quality.{key} must be an integer from 1 to 5")
            elif key == "reviewer":
                if not nonempty(value): errors.append(f"{where}: quality.reviewer must be a non-empty string")
            elif key == "reviewed_at":
                try: date.fromisoformat(value)
                except (TypeError, ValueError): errors.append(f"{where}: quality.reviewed_at must be an ISO date (YYYY-MM-DD)")
        if isinstance(quality, dict) and quality.get("review_status") in {"human_reviewed", "rejected"}:
            if not nonempty(quality.get("reviewer")): errors.append(f"{where}: human review status requires quality.reviewer")
            try: date.fromisoformat(quality.get("reviewed_at", ""))
            except (TypeError, ValueError): errors.append(f"{where}: human review status requires quality.reviewed_at as YYYY-MM-DD")
    return errors, warnings

def validate_files(paths, strict_taxonomy=False, training_ready=False):
    errors, warnings, ids, payloads, supersedes = [], [], {}, {}, {}
    file_counts, coverage = Counter(), {k: Counter() for k in ("domain", "register", "language", "split", "turn_count", "provenance", "review_status")}
    total = 0
    for path in paths:
        try: lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc: errors.append(f"{path}: cannot read: {exc}"); continue
        for number, raw in enumerate(lines, 1):
            if not raw.strip(): errors.append(f"{path}:{number}: blank JSONL line"); continue
            total += 1; file_counts[str(path)] += 1
            try: row = json.loads(raw)
            except json.JSONDecodeError as exc: errors.append(f"{path}:{number}: invalid JSON: {exc.msg}"); continue
            e, w = validate_record(row, path, number); errors.extend(e); warnings.extend(w)
            if strict_taxonomy and row.get("domain") not in CANONICAL_DOMAINS:
                errors.append(f"{path}:{number}: non-canonical primary domain {row.get('domain')!r}")
            if training_ready:
                q = row.get("quality") if isinstance(row.get("quality"), dict) else {}
                if q.get("review_status") != "human_reviewed":
                    errors.append(f"{path}:{number}: training-ready export requires quality.review_status=human_reviewed")
                valid_scores = {k for k, v in q.items() if k in QUALITY_SCORES and isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 5}
                missing_scores = QUALITY_SCORES - valid_scores
                if missing_scores:
                    errors.append(f"{path}:{number}: training-ready export missing valid human scores: {sorted(missing_scores)}")
            if not isinstance(row, dict): continue
            sid = row.get("sample_id")
            if nonempty(sid):
                if sid in ids: errors.append(f"{path}:{number}: duplicate sample_id {sid!r}; first at {ids[sid]}")
                else: ids[sid] = f"{path}:{number}"
            messages = row.get("messages")
            if isinstance(messages, list):
                payload = json.dumps(messages, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
                if digest in payloads: errors.append(f"{path}:{number}: duplicate conversation payload; first at {payloads[digest]}")
                else: payloads[digest] = f"{path}:{number}"
                coverage["turn_count"][str(len(messages))] += 1
            for key in ("domain", "register", "language", "split"):
                if isinstance(row.get(key), str): coverage[key][row[key]] += 1
            meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            if isinstance(meta.get("provenance"), str): coverage["provenance"][meta["provenance"]] += 1
            q = row.get("quality") if isinstance(row.get("quality"), dict) else {}
            coverage["review_status"][str(q.get("review_status", "missing"))] += 1
            old = meta.get("supersedes_sample_id")
            if nonempty(sid) and nonempty(old): supersedes[sid] = old
    if training_ready:
        for old in sorted(set(supersedes.values())):
            if old in ids:
                errors.append(f"{old}: superseded predecessor must be excluded from training-ready input")
    for new, old in supersedes.items():
        if old not in ids: errors.append(f"{new}: superseded sample {old!r} not found in supplied files")
        if new == old: errors.append(f"{new}: cannot supersede itself")
    for start in supersedes:
        seen, node = set(), start
        while node in supersedes:
            if node in seen: errors.append(f"{start}: supersedes cycle detected"); break
            seen.add(node); node = supersedes[node]
    return {"total_records": total, "unique_sample_ids": len(ids), "files": dict(file_counts),
            "coverage": {k: dict(v) for k, v in coverage.items()}, "errors": errors, "warnings": warnings}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="Pass all staging JSONL files together for global checks")
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--strict-warnings", action="store_true")
    parser.add_argument("--strict-taxonomy", action="store_true", help="Reject primary domains outside Taxonomy V2")
    parser.add_argument("--training-ready", action="store_true", help="Require human-reviewed records, all seven human scores, and no superseded predecessors")
    args = parser.parse_args()
    report = validate_files(args.files, strict_taxonomy=args.strict_taxonomy, training_ready=args.training_ready)
    print(f"TOTAL: {report['total_records']} records | {report['unique_sample_ids']} unique IDs | {len(report['errors'])} errors | {len(report['warnings'])} warnings")
    for name, count in report["files"].items(): print(f"{name}: {count} records")
    for key, values in report["coverage"].items(): print(f"{key}: {json.dumps(values, ensure_ascii=False, sort_keys=True)}")
    for item in report["warnings"]: print("WARNING: " + item)
    for item in report["errors"]: print("ERROR: " + item)
    if args.json_report: args.json_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if report["errors"] or (args.strict_warnings and report["warnings"]) else 0

if __name__ == "__main__": sys.exit(main())
