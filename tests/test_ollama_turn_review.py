import json
import tempfile
import unittest
from pathlib import Path

from scripts.review_assistant_turns_ollama import (
    ReviewError, parse_model_response, load_existing, atomic_json,
)


class OllamaTurnReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output = self.root / "annotations.jsonl"
        self.manifest = self.output.with_suffix(self.output.suffix + ".manifest.json")
        self.expected = {
            "format": "ollama_assistant_turn_review_jsonl",
            "annotation_version": "assistant_turn_review_v1",
            "prompt_version": "persian_turn_reviewer_v1",
            "requested_model": "qwen3.5:9b",
            "base_url": "http://127.0.0.1:11434",
            "prompt_sha256": "abc",
            "source_file_sha256": {"staging.jsonl": "def"},
        }

    def tearDown(self):
        self.tmp.cleanup()

    def turn(self, idx, label="positive_target"):
        return {
            "message_index": idx,
            "label": label,
            "rationale": "پاسخ با درخواست کاربر سازگار است.",
            "confidence": 0.91,
            "evidence_message_indices": [idx - 1],
            "issues": [],
        }

    def test_valid_complete_annotation_is_sorted_by_turn_index(self):
        payload = {"assistant_turns": [self.turn(3), self.turn(1, "negative_or_demonstration_only")]}
        result = parse_model_response(json.dumps(payload, ensure_ascii=False), {1, 3}, "fa-test", 4)
        self.assertEqual([x["message_index"] for x in result], [1, 3])

    def test_missing_assistant_turn_is_rejected(self):
        payload = {"assistant_turns": [self.turn(1)]}
        with self.assertRaisesRegex(ReviewError, "coverage mismatch"):
            parse_model_response(json.dumps(payload, ensure_ascii=False), {1, 3}, "fa-test", 4)

    def test_duplicate_assistant_turn_is_rejected(self):
        payload = {"assistant_turns": [self.turn(1), self.turn(1)]}
        with self.assertRaisesRegex(ReviewError, "invalid/duplicate"):
            parse_model_response(json.dumps(payload, ensure_ascii=False), {1}, "fa-test", 3)

    def test_invalid_evidence_index_is_rejected(self):
        item = self.turn(1)
        item["evidence_message_indices"] = [99]
        with self.assertRaisesRegex(ReviewError, "invalid evidence"):
            parse_model_response(json.dumps({"assistant_turns": [item]}, ensure_ascii=False), {1}, "fa-test", 3)

    def test_unknown_fields_are_rejected(self):
        payload = {"assistant_turns": [dict(self.turn(1), extra="not allowed")]}
        with self.assertRaisesRegex(ReviewError, "invalid turn annotation fields"):
            parse_model_response(json.dumps(payload, ensure_ascii=False), {1}, "fa-test", 3)

    def test_resume_requires_manifest(self):
        self.output.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ReviewError, "sidecar manifest"):
            load_existing(self.output, True, self.manifest, self.expected)

    def test_resume_rejects_model_or_source_mismatch(self):
        self.output.write_text("", encoding="utf-8")
        atomic_json(self.manifest, dict(self.expected, requested_model="other-model"))
        with self.assertRaisesRegex(ReviewError, "requested_model"):
            load_existing(self.output, True, self.manifest, self.expected)

    def test_resume_accepts_matching_empty_checkpoint(self):
        self.output.write_text("", encoding="utf-8")
        atomic_json(self.manifest, self.expected)
        self.assertEqual(load_existing(self.output, True, self.manifest, self.expected), {})

    def test_new_run_refuses_existing_output(self):
        self.output.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ReviewError, "refusing overwrite"):
            load_existing(self.output, False, self.manifest, self.expected)


if __name__ == "__main__":
    unittest.main()
