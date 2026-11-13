#!/usr/bin/env python3
"""Turn lexical candidate pairs into a blank human adjudication CSV."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

FIELDS = [
    "pair_id", "sample_a", "sample_b", "source_a", "source_b",
    "domain_a", "domain_b", "jaccard", "shared_terms", "decision",
    "reviewer", "review_date", "rationale",
]

def build_rows(payload: dict) -> list[dict]:
    if payload.get("purpose") != "human_review_candidate_pairs_only":
        raise ValueError("input is not a semantic-family candidate report")
    if payload.get("automatic_family_assignment") is not False or payload.get("automatic_split_assignment") is not False:
        raise ValueError("candidate report violates no-auto-assignment policy")
    pairs = payload.get("pairs")
    if not isinstance(pairs, list):
        raise ValueError("candidate report must contain a pairs array")
    rows = []
    seen = set()
    for index, pair in enumerate(pairs, 1):
        a, b = pair.get("sample_a"), pair.get("sample_b")
        if not isinstance(a, str) or not isinstance(b, str) or not a or not b or a == b:
            raise ValueError(f"invalid sample pair at index {index}")
        key = tuple(sorted((a, b)))
        if key in seen:
            raise ValueError(f"duplicate candidate pair: {key}")
        seen.add(key)
        rows.append({
            "pair_id": f"SF-{index:03d}",
            "sample_a": a, "sample_b": b,
            "source_a": pair.get("source_a", ""),
            "source_b": pair.get("source_b", ""),
            "domain_a": pair.get("domain_a") or "",
            "domain_b": pair.get("domain_b") or "",
            "jaccard": pair.get("jaccard", ""),
            "shared_terms": " | ".join(pair.get("shared_terms", [])),
            "decision": "pending",
            "reviewer": "", "review_date": "", "rationale": "",
        })
    if len(rows) != payload.get("candidate_pair_count"):
        raise ValueError("candidate_pair_count does not match pairs array")
    return rows

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"refusing to overwrite {args.output}")
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        rows = build_rows(payload)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.exit(1, f"REVIEW REGISTER GENERATION FAILED: {exc}\n")
    print(f"Generated {len(rows)} pending human-review rows; no decisions or family IDs assigned.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
