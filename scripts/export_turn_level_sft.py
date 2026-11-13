#!/usr/bin/env python3
"""Export assistant-turn-level SFT examples using explicit AI-provisional annotations.

This exporter is intentionally stricter than the legacy record exporter:
- every assistant turn in every active source record needs exactly one annotation;
- only positive_target turns become targets;
- AI annotations never satisfy the independent human-review/score/split/family gates;
- source staging files and annotation files are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from scripts.validate_dataset import SPLITS, validate_files

LABELS = {"positive_target", "negative_or_demonstration_only", "needs_revision"}
REQUIRED_SCORES = {
    "intent_fidelity", "context_use", "persian_fluency", "accuracy",
    "instruction_adherence", "tone_appropriateness", "non_redundancy",
}


class ExportError(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sources(paths):
    exception_path = Path(__file__).resolve().parent.parent / "config" / "taxonomy_exceptions_v1.json"
    exceptions = json.loads(exception_path.read_text(encoding="utf-8")) if exception_path.exists() else {}
    validation = validate_files(paths, strict_taxonomy=True, training_ready=False, taxonomy_exceptions=exceptions)
    if validation["errors"]:
        raise ExportError("Dataset validation failed:\n" + "\n".join(validation["errors"]))
    rows = []
    replacements = {}
    for path in paths:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            rows.append((row, path, line_no))
            old = row.get("metadata", {}).get("supersedes_sample_id")
            if old:
                if old in replacements:
                    raise ExportError(f"multiple replacements declared for {old!r}")
                replacements[old] = row["sample_id"]
    by_id = {row["sample_id"]: row for row, _, _ in rows}
    for old, replacement in replacements.items():
        if old not in by_id:
            raise ExportError(f"replacement {replacement!r} references missing predecessor {old!r}")
    active = [(r, p, n) for r, p, n in rows if r["sample_id"] not in replacements]
    return rows, active, replacements


def load_annotations(path: Path):
    annotations = {}
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        item = json.loads(raw)
        sample_id = item.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id:
            raise ExportError(f"{path}:{line_no}: sample_id is required")
        if sample_id in annotations:
            raise ExportError(f"{path}:{line_no}: duplicate annotation for {sample_id}")
        if item.get("review_status") != "ai_provisional" or item.get("reviewer_type") != "ai":
            raise ExportError(f"{path}:{line_no}: annotations must remain explicitly ai_provisional")
        turns = item.get("assistant_turns")
        if not isinstance(turns, list):
            raise ExportError(f"{path}:{line_no}: assistant_turns must be a list")
        indexed = {}
        for turn in turns:
            idx = turn.get("message_index")
            if not isinstance(idx, int) or isinstance(idx, bool) or idx < 0 or idx in indexed:
                raise ExportError(f"{path}:{line_no}: invalid/duplicate message_index")
            if turn.get("label") not in LABELS:
                raise ExportError(f"{path}:{line_no}: invalid turn label")
            if not isinstance(turn.get("rationale"), str) or not turn["rationale"].strip():
                raise ExportError(f"{path}:{line_no}: rationale is required")
            confidence = turn.get("confidence")
            if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
                raise ExportError(f"{path}:{line_no}: confidence must be between 0 and 1")
            indexed[idx] = turn
        item["_indexed_turns"] = indexed
        annotations[sample_id] = item
    return annotations


def prepare_turn_export(source_paths, annotation_path):
    rows, active, replacements = load_sources(source_paths)
    annotations = load_annotations(annotation_path)
    active_ids = {r["sample_id"] for r, _, _ in active}
    unknown = set(annotations) - active_ids
    if unknown:
        raise ExportError("annotations contain unknown or superseded sample IDs: " + ", ".join(sorted(unknown)))

    family_splits = {}
    output = {}
    target_count = Counter()
    for row, path, line_no in active:
        sid = row["sample_id"]
        annotation = annotations.get(sid)
        if annotation is None:
            raise ExportError(f"missing AI turn annotation for active record {sid}")
        expected = {i for i, msg in enumerate(row["messages"]) if msg["role"] == "assistant"}
        actual = set(annotation["_indexed_turns"])
        if expected != actual:
            raise ExportError(
                f"{sid}: assistant turn annotation coverage mismatch; "
                f"missing={sorted(expected-actual)}, extra={sorted(actual-expected)}"
            )

        quality = row.get("quality") if isinstance(row.get("quality"), dict) else {}
        if quality.get("review_status") != "human_reviewed":
            raise ExportError(f"{sid}: independent human record review is still required")
        for score in REQUIRED_SCORES:
            value = quality.get(score)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise ExportError(f"{sid}: valid human score {score!r} is required")
        split = row.get("split")
        if split not in SPLITS:
            raise ExportError(f"{sid}: valid human-approved split is required")
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        family = metadata.get("semantic_family_id")
        if not isinstance(family, str) or not family.strip():
            raise ExportError(f"{sid}: semantic_family_id is required")
        previous = family_splits.setdefault(family, split)
        if previous != split:
            raise ExportError(f"semantic-family leakage: {family!r} appears in {previous!r} and {split!r}")

        for index in sorted(expected):
            turn = annotation["_indexed_turns"][index]
            if turn["label"] != "positive_target":
                continue
            # Keep the full preceding context, including a flawed prior assistant turn
            # when the target is its correction. Only the selected assistant turn is target.
            context = row["messages"][:index]
            target = row["messages"][index]
            if not context or context[-1]["role"] != "user":
                raise ExportError(f"{sid}:{index}: target assistant turn must immediately follow a user turn")
            example_id = f"{sid}::assistant::{index}"
            output.setdefault(split, []).append({
                "example_id": example_id,
                "sample_id": sid,
                "target_message_index": index,
                "messages": context + [target],
                "domain": row["domain"],
                "language": row["language"],
                "register": row["register"],
                "subskills": row.get("subskills", []),
                "semantic_family_id": family,
            })
            target_count[split] += 1

    if set(annotations) != active_ids:
        missing = active_ids - set(annotations)
        raise ExportError("incomplete annotation coverage: " + ", ".join(sorted(missing)))
    for split in output:
        output[split].sort(key=lambda x: x["example_id"])

    manifest = {
        "format": "assistant_turn_chat_sft_jsonl",
        "purpose": "supervised_fine_tuning_candidate_export",
        "status": "not_training_approved",
        "source_record_count": len(rows),
        "active_record_count": len(active),
        "excluded_superseded_count": len(replacements),
        "assistant_turn_annotation_count": sum(len(a["_indexed_turns"]) for a in annotations.values()),
        "positive_target_count": sum(target_count.values()),
        "split_target_counts": dict(sorted(target_count.items())),
        "source_files": [{"path": str(p), "sha256": sha256(p)} for p in source_paths],
        "annotation_file": {"path": str(annotation_path), "sha256": sha256(annotation_path)},
        "annotation_provenance": "AI-provisional; not human certification",
        "record_gate": "human_reviewed_with_all_seven_scores",
        "split_gate": "semantic_family_isolated",
        "superseded_policy": "exclude_predecessor_keep_active_replacement",
        "target_policy": "positive_target_only; negative and needs_revision are never targets",
        "context_policy": "retain all preceding messages through selected positive assistant target",
        "training_approval": False,
    }
    return output, manifest


def write_export(source_paths, annotation_path, output_dir: Path):
    if output_dir.exists():
        raise ExportError(f"output directory already exists; refusing to overwrite: {output_dir}")
    splits, manifest = prepare_turn_export(source_paths, annotation_path)
    output_dir.mkdir(parents=True)
    for split, examples in splits.items():
        (output_dir / f"{split}.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in examples), encoding="utf-8"
        )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(write_export(args.files, args.annotations, args.output_dir), ensure_ascii=False, indent=2))
    except (OSError, json.JSONDecodeError, ExportError) as exc:
        print(f"TURN EXPORT BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
