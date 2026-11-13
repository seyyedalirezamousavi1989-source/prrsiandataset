#!/usr/bin/env python3
"""Create a human-review inventory for active records absent from lexical candidate pairs."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

FIELDS = [
    "sample_id", "source_file", "domain", "subskill", "register",
    "language", "message_count", "user_turn_count", "assistant_turn_count",
    "review_status", "reviewer", "review_date", "primary_behavior",
    "family_assessment", "rationale",
]

def load_active_records(paths: list[Path]) -> list[dict]:
    records = []
    for path in paths:
        if "identity" in path.name.lower():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("sample_id"), str):
                raise ValueError(f"{path}:{line_no}: invalid record or missing sample_id")
            row["_source_file"] = str(path)
            records.append(row)
    ids = [r["sample_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate sample_id across supplied staging files")
    superseded = {
        r.get("metadata", {}).get("supersedes_sample_id")
        for r in records
        if isinstance(r.get("metadata"), dict) and r["metadata"].get("supersedes_sample_id")
    }
    missing = superseded - set(ids)
    if missing:
        raise ValueError(f"replacement references missing predecessor(s): {sorted(missing)}")
    return [r for r in records if r["sample_id"] not in superseded]

def build_inventory(candidate_report: dict, records: list[dict]) -> tuple[list[dict], dict]:
    if candidate_report.get("purpose") != "human_review_candidate_pairs_only":
        raise ValueError("input is not a semantic-family candidate report")
    if candidate_report.get("automatic_family_assignment") is not False or candidate_report.get("automatic_split_assignment") is not False:
        raise ValueError("automatic family/split assignment is not permitted")
    pairs = candidate_report.get("pairs")
    if not isinstance(pairs, list) or len(pairs) != candidate_report.get("candidate_pair_count"):
        raise ValueError("candidate pair list/count mismatch")
    known = {r["sample_id"] for r in records}
    linked = set()
    for pair in pairs:
        a, b = pair.get("sample_a"), pair.get("sample_b")
        if not isinstance(a, str) or not isinstance(b, str) or a == b:
            raise ValueError("invalid candidate pair")
        if a not in known or b not in known:
            raise ValueError(f"candidate pair references unknown sample: {a}, {b}")
        linked.update((a, b))
    if candidate_report.get("active_record_count") != len(records):
        raise ValueError("active_record_count does not match staging inventory")
    unmatched = [r for r in records if r["sample_id"] not in linked]
    rows = []
    for r in unmatched:
        messages = r.get("messages", [])
        rows.append({
            "sample_id": r["sample_id"],
            "source_file": r["_source_file"],
            "domain": r.get("domain") or "",
            "subskill": r.get("subskill") or "",
            "register": r.get("register") or "",
            "language": r.get("language") or "",
            "message_count": len(messages),
            "user_turn_count": sum(m.get("role") == "user" for m in messages if isinstance(m, dict)),
            "assistant_turn_count": sum(m.get("role") == "assistant" for m in messages if isinstance(m, dict)),
            "review_status": "pending_human_review",
            "reviewer": "",
            "review_date": "",
            "primary_behavior": "",
            "family_assessment": "unassessed",
            "rationale": "",
        })
    summary = {
        "purpose": "human_review_unmatched_record_inventory_only",
        "active_record_count": len(records),
        "candidate_pair_count": len(pairs),
        "records_linked_to_at_least_one_candidate_pair": len(linked),
        "unmatched_record_count": len(unmatched),
        "identity_track_excluded": True,
        "superseded_predecessors_excluded": True,
        "automatic_family_assignment": False,
        "automatic_split_assignment": False,
        "training_approval": False,
    }
    return rows, summary

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--csv-output", required=True, type=Path)
    parser.add_argument("--summary-output", required=True, type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    if args.csv_output.exists() or args.summary_output.exists():
        parser.error("refusing to overwrite an existing output")
    try:
        report = json.loads(args.candidates.read_text(encoding="utf-8"))
        records = load_active_records(args.files)
        rows, summary = build_inventory(report, records)
        args.csv_output.parent.mkdir(parents=True, exist_ok=True)
        with args.csv_output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        args.summary_output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(1, f"UNMATCHED INVENTORY GENERATION FAILED: {exc}\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
