#!/usr/bin/env python3
"""Validate PersianDataset JSONL conversation files using only the Python stdlib."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_ROLES = {"system", "user", "assistant"}
ALLOWED_SPLITS = {"train", "validation", "test", "challenge"}
PERSIAN_RE = re.compile(r"[\u0600-\u06FF]")


def validate_file(path: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_conversations: set[str] = set()
    count = 0

    try:
        stream = path.open("r", encoding="utf-8")
    except OSError as exc:
        return [f"{path}: cannot open file: {exc}"], 0

    with stream:
        for line_no, raw in enumerate(stream, 1):
            if not raw.strip():
                errors.append(f"{path}:{line_no}: blank lines are not allowed in JSONL")
                continue
            count += 1
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_no}: invalid JSON: {exc.msg}")
                continue

            prefix = f"{path}:{line_no}"
            if not isinstance(row, dict):
                errors.append(f"{prefix}: record must be a JSON object")
                continue

            sample_id = row.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id.strip():
                errors.append(f"{prefix}: sample_id must be a non-empty string")
            elif sample_id in seen_ids:
                errors.append(f"{prefix}: duplicate sample_id {sample_id!r}")
            else:
                seen_ids.add(sample_id)

            if not isinstance(row.get("domain"), str) or not row["domain"].strip():
                errors.append(f"{prefix}: domain must be a non-empty string")
            if row.get("language") not in {"fa", "fa-en", "multilingual"}:
                errors.append(f"{prefix}: unsupported or missing language")
            if row.get("register") not in {"colloquial", "neutral", "formal", "mixed"}:
                errors.append(f"{prefix}: unsupported or missing register")
            if row.get("split") not in ALLOWED_SPLITS:
                errors.append(f"{prefix}: unsupported or missing split")

            messages = row.get("messages")
            if not isinstance(messages, list) or len(messages) < 2:
                errors.append(f"{prefix}: messages must contain at least two turns")
                messages = []
            conversation_text = []
            for index, message in enumerate(messages):
                if not isinstance(message, dict):
                    errors.append(f"{prefix}: message {index} must be an object")
                    continue
                role, content = message.get("role"), message.get("content")
                if role not in ALLOWED_ROLES:
                    errors.append(f"{prefix}: message {index} has invalid role {role!r}")
                if not isinstance(content, str) or not content.strip():
                    errors.append(f"{prefix}: message {index} content must be non-empty text")
                    continue
                conversation_text.append(content)
            if messages and not any(m.get("role") == "user" for m in messages if isinstance(m, dict)):
                errors.append(f"{prefix}: conversation has no user message")
            if messages and not any(m.get("role") == "assistant" for m in messages if isinstance(m, dict)):
                errors.append(f"{prefix}: conversation has no assistant response")

            metadata = row.get("metadata")
            if not isinstance(metadata, dict):
                errors.append(f"{prefix}: metadata must be an object")
            else:
                for key in ("provenance", "created_by"):
                    if not isinstance(metadata.get(key), str) or not metadata[key].strip():
                        errors.append(f"{prefix}: metadata.{key} must be a non-empty string")

            if row.get("language") in {"fa", "fa-en"} and conversation_text:
                if not PERSIAN_RE.search("\n".join(conversation_text)):
                    errors.append(f"{prefix}: Persian-language record contains no Persian-script text")

            fingerprint = json.dumps(messages, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            if fingerprint in seen_conversations:
                errors.append(f"{prefix}: duplicate conversation payload")
            else:
                seen_conversations.add(fingerprint)

    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="JSONL files to validate")
    args = parser.parse_args()

    total = 0
    all_errors: list[str] = []
    for path in args.files:
        errors, count = validate_file(path)
        total += count
        all_errors.extend(errors)
        print(f"{path}: {count} records, {len(errors)} issue(s)")

    print(f"TOTAL: {total} records, {len(all_errors)} issue(s)")
    for error in all_errors:
        print(f"ERROR: {error}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
