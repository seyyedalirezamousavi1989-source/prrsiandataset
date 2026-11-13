#!/usr/bin/env python3
"""Generate human-review candidates for semantic-family grouping; never assigns families."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
STOPWORDS = {
    "از", "به", "با", "برای", "در", "را", "که", "و", "یا", "این", "آن",
    "یک", "من", "تو", "ما", "شما", "او", "هم", "همه", "اگر", "اما",
    "پس", "چه", "چرا", "چطور", "چگونه", "است", "هست", "بود", "شد",
    "می", "کنم", "کنید", "کرد", "کردن", "دارد", "دارم", "داره",
    "the", "a", "an", "and", "or", "to", "of", "in", "is", "it", "for",
}


def normalize(text: str) -> str:
    return text.replace("ي", "ی").replace("ك", "ک").replace("ۀ", "ه").replace("ؤ", "و")


def tokenize_record(row: dict) -> set[str]:
    messages = row.get("messages", [])
    text = " ".join(m.get("content", "") for m in messages if isinstance(m, dict))
    tokens = {t for t in TOKEN_RE.findall(normalize(text).lower()) if len(t) > 1 and t not in STOPWORDS}
    return tokens


def load_records(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        if "identity" in path.name.lower():
            continue
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            if not isinstance(row, dict) or not isinstance(row.get("sample_id"), str):
                raise ValueError(f"{path}:{line_no}: expected object with sample_id")
            row["_source_file"] = str(path)
            rows.append(row)

    ids = [r["sample_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate sample_id across supplied files")

    superseded = {
        r.get("metadata", {}).get("supersedes_sample_id")
        for r in rows
        if isinstance(r.get("metadata"), dict) and r["metadata"].get("supersedes_sample_id")
    }
    missing = superseded - set(ids)
    if missing:
        raise ValueError(f"replacement references predecessor absent from inputs: {sorted(missing)}")
    return [r for r in rows if r["sample_id"] not in superseded]


def similarity(a: set[str], b: set[str]) -> tuple[float, list[str]]:
    common = a & b
    union = a | b
    return (len(common) / len(union) if union else 0.0, sorted(common))


def build_candidates(rows: list[dict], threshold: float = 0.18, min_shared: int = 3, top_k: int = 5) -> list[dict]:
    docs = [(r, tokenize_record(r)) for r in rows]
    candidates = []
    for i, (left, ltokens) in enumerate(docs):
        for right, rtokens in docs[i + 1:]:
            score, shared = similarity(ltokens, rtokens)
            if score < threshold or len(shared) < min_shared:
                continue
            candidates.append({
                "sample_a": left["sample_id"],
                "sample_b": right["sample_id"],
                "source_a": left["_source_file"],
                "source_b": right["_source_file"],
                "domain_a": left.get("domain"),
                "domain_b": right.get("domain"),
                "jaccard": round(score, 4),
                "shared_terms": shared[:30],
                "decision": "pending_human_review",
            })
    candidates.sort(key=lambda x: (-x["jaccard"], x["sample_a"], x["sample_b"]))
    # Keep a bounded, deterministic review workload per sample while retaining pair identity.
    degree = Counter()
    selected = []
    for item in candidates:
        if degree[item["sample_a"]] >= top_k or degree[item["sample_b"]] >= top_k:
            continue
        selected.append(item)
        degree[item["sample_a"]] += 1
        degree[item["sample_b"]] += 1
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--threshold", type=float, default=0.18)
    parser.add_argument("--min-shared", type=int, default=3)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    if not 0 <= args.threshold <= 1 or args.min_shared < 1 or args.top_k < 1:
        parser.error("threshold must be 0..1; min-shared and top-k must be positive")
    if args.output.exists():
        print(f"Refusing to overwrite: {args.output}", file=sys.stderr)
        return 2
    try:
        rows = load_records(args.files)
        candidates = build_candidates(rows, args.threshold, args.min_shared, args.top_k)
        payload = {
            "purpose": "human_review_candidate_pairs_only",
            "automatic_family_assignment": False,
            "automatic_split_assignment": False,
            "active_record_count": len(rows),
            "candidate_pair_count": len(candidates),
            "threshold": args.threshold,
            "minimum_shared_terms": args.min_shared,
            "maximum_candidates_per_sample": args.top_k,
            "excluded_identity_track": True,
            "pairs": candidates,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CANDIDATE GENERATION FAILED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({k: v for k, v in payload.items() if k != "pairs"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
