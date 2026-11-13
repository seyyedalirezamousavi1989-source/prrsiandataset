#!/usr/bin/env python3
"""Build leakage-checked, human-reviewed JSONL splits for conversational SFT."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from scripts.validate_dataset import SPLITS, validate_files

REQUIRED_SCORES = {
    "intent_fidelity", "context_use", "persian_fluency", "accuracy",
    "instruction_adherence", "tone_appropriateness", "non_redundancy",
}


class ExportError(ValueError):
    pass


def prepare_export(paths):
    report = validate_files(paths, strict_taxonomy=True, training_ready=False)
    if report["errors"]:
        raise ExportError("Dataset validation failed:\n" + "\n".join(report["errors"]))

    rows = []
    superseded_to_replacement = {}
    for path in paths:
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            rows.append((row, str(path), line_no))
            old = row.get("metadata", {}).get("supersedes_sample_id")
            if old:
                if old in superseded_to_replacement:
                    raise ExportError(f"multiple replacements declared for superseded sample {old!r}")
                superseded_to_replacement[old] = row["sample_id"]

    by_id = {row["sample_id"]: row for row, _, _ in rows}
    for old, replacement in superseded_to_replacement.items():
        if old not in by_id:
            raise ExportError(f"replacement {replacement!r} references missing predecessor {old!r}")

    active = [(row, path, line) for row, path, line in rows
              if row["sample_id"] not in superseded_to_replacement]

    family_splits = {}
    for row, path, line in active:
        quality = row.get("quality") if isinstance(row.get("quality"), dict) else {}
        if quality.get("review_status") != "human_reviewed":
            raise ExportError(f"{path}:{line}: record {row.get('sample_id')!r} is not human_reviewed")
        for score in REQUIRED_SCORES:
            value = quality.get(score)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise ExportError(f"{path}:{line}: record {row.get('sample_id')!r} lacks valid human score {score!r}")
        split = row.get("split")
        if split not in SPLITS:
            raise ExportError(f"{path}:{line}: invalid or missing split {split!r}")
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        family = metadata.get("semantic_family_id")
        if not isinstance(family, str) or not family.strip():
            raise ExportError(f"{path}:{line}: metadata.semantic_family_id is required for leakage-safe export")
        previous = family_splits.setdefault(family, split)
        if previous != split:
            raise ExportError(
                f"semantic-family leakage: {family!r} appears in both {previous!r} and {split!r}"
            )

    output = defaultdict(list)
    for row, _, _ in active:
        item = {
            "sample_id": row["sample_id"],
            "messages": row["messages"],
            "domain": row["domain"],
            "language": row["language"],
            "register": row["register"],
            "subskills": row.get("subskills", []),
            "semantic_family_id": row["metadata"]["semantic_family_id"],
        }
        output[row["split"]].append(item)

    for split in output:
        output[split].sort(key=lambda item: item["sample_id"])

    manifest = {
        "format": "chat_messages_jsonl",
        "purpose": "supervised_fine_tuning",
        "source_record_count": len(rows),
        "active_record_count": len(active),
        "excluded_superseded_count": len(rows) - len(active),
        "split_counts": dict(sorted(Counter(row["split"] for row, _, _ in active).items())),
        "semantic_family_count": len(family_splits),
        "source_files": [str(p) for p in paths],
        "review_gate": "human_reviewed_with_all_seven_scores",
        "taxonomy_gate": "canonical_v2",
        "leakage_gate": "semantic_family_id_must_belong_to_one_split",
    }
    return dict(output), manifest


def write_export(paths, output_dir: Path):
    if output_dir.exists():
        raise ExportError(f"output directory already exists; refusing to overwrite: {output_dir}")
    splits, manifest = prepare_export(paths)
    output_dir.mkdir(parents=True)
    for split, rows in splits.items():
        target = output_dir / f"{split}.jsonl"
        target.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        manifest = write_export(args.files, args.output_dir)
    except (OSError, json.JSONDecodeError, ExportError) as exc:
        print(f"EXPORT BLOCKED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
