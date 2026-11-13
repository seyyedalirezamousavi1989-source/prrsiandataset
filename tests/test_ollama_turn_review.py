import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.review_assistant_turns_ollama import (
    ReviewError, parse_model_response, load_existing, atomic_json, review_corpus,
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

    def test_empty_model_content_is_rejected_with_clear_diagnostic(self):
        with self.assertRaisesRegex(ReviewError, "empty content"):
            parse_model_response("", {1}, "fa-empty", 2)

    def test_invalid_json_includes_response_preview(self):
        with self.assertRaisesRegex(ReviewError, "response preview"):
            parse_model_response("not-json", {1}, "fa-bad-json", 2)

    def test_manifest_tracks_partial_run_and_resume_completion(self):
        source = self.root / "source.jsonl"
        records = []
        for sid in ("fa-one", "fa-two"):
            records.append({
                "sample_id": sid,
                "domain": "persian_fluency",
                "language": "fa",
                "register": "neutral",
                "messages": [
                    {"role": "user", "content": "این عبارت طبیعی است؟"},
                    {"role": "assistant", "content": "بله، طبیعی است."}
                ]
            })
        source.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records),
            encoding="utf-8"
        )

        response = json.dumps({"assistant_turns": [self.turn(1)]}, ensure_ascii=False)
        with patch("scripts.review_assistant_turns_ollama.ollama_chat", return_value=("qwen3.5:9b", response)):
            first = review_corpus(
                [source], self.output, "qwen3.5:9b", "http://127.0.0.1:11434", 30,
                limit=1, pause=0
            )
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(first["newly_reviewed_records"], 1)
        self.assertEqual(first["remaining_records"], 1)
        self.assertEqual(manifest["completed_records"], 1)
        self.assertFalse(manifest["complete"])

        # Simulate the stale count written by the pre-fix script. Resume must
        # reconcile it from the validated append-only JSONL before making calls.
        manifest["completed_records"] = 0
        manifest["complete"] = False
        atomic_json(self.manifest, manifest)

        def second_response(*args, **kwargs):
            checkpoint = json.loads(self.manifest.read_text(encoding="utf-8"))
            self.assertEqual(checkpoint["completed_records"], 1)
            return "qwen3.5:9b", response

        with patch("scripts.review_assistant_turns_ollama.ollama_chat", side_effect=second_response):
            second = review_corpus(
                [source], self.output, "qwen3.5:9b", "http://127.0.0.1:11434", 30,
                resume=True, limit=1, pause=0
            )
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        lines = [line for line in self.output.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(second["already_annotated_records"], 1)
        self.assertEqual(second["newly_reviewed_records"], 1)
        self.assertEqual(second["remaining_records"], 0)
        self.assertEqual(len(lines), 2)
        self.assertEqual(manifest["completed_records"], 2)
        self.assertTrue(manifest["complete"])


if __name__ == "__main__":
    unittest.main()
