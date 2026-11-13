import json
import tempfile
import unittest
from pathlib import Path

from scripts.export_turn_level_sft import prepare_turn_export, ExportError


def make_record(sample_id="fa-turn-1", family="fam-1", split="train"):
    scores = {k: 4 for k in ("intent_fidelity", "context_use", "persian_fluency", "accuracy", "instruction_adherence", "tone_appropriateness", "non_redundancy")}
    return {
        "sample_id": sample_id, "domain": "everyday_dialogue", "language": "fa",
        "register": "colloquial", "split": split,
        "messages": [
            {"role": "user", "content": "این متن را اصلاح کن."},
            {"role": "assistant", "content": "نسخه نادرست."},
            {"role": "user", "content": "این بخش را اشتباه تغییر دادی."},
            {"role": "assistant", "content": "حق با توست؛ نسخه اصلاح‌شده این است."},
        ],
        "metadata": {"provenance": "original_curated", "created_by": "test", "semantic_family_id": family},
        "quality": {"review_status": "human_reviewed", "reviewer": "human-1", "reviewed_at": "2026-11-13", **scores},
    }


def annotation(sid="fa-turn-1", labels=("negative_or_demonstration_only", "positive_target")):
    return {
        "sample_id": sid, "review_status": "ai_provisional", "reviewer_type": "ai",
        "review_model": None, "annotation_version": "assistant_turn_review_v1",
        "assistant_turns": [
            {"message_index": idx, "label": label, "rationale": "برچسب آزمایشی برای آزمون قرارداد.", "confidence": 0.9}
            for idx, label in zip((1, 3), labels)
        ],
    }


class TurnLevelExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.jsonl"
        self.ann = self.root / "annotations.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rows, anns):
        self.source.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
        self.ann.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in anns), encoding="utf-8")

    def test_bad_first_turn_excluded_and_correction_is_positive_with_context(self):
        self.write([make_record()], [annotation()])
        splits, manifest = prepare_turn_export([self.source], self.ann)
        items = splits["train"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["target_message_index"], 3)
        self.assertEqual(items[0]["messages"][-1]["content"], "حق با توست؛ نسخه اصلاح‌شده این است.")
        self.assertEqual(items[0]["messages"][1]["content"], "نسخه نادرست.")
        self.assertEqual(manifest["positive_target_count"], 1)
        self.assertFalse(manifest["training_approval"])

    def test_nonpositive_turn_never_becomes_target(self):
        self.write([make_record()], [annotation(labels=("negative_or_demonstration_only", "needs_revision"))])
        splits, _ = prepare_turn_export([self.source], self.ann)
        self.assertEqual(splits, {})

    def test_missing_annotation_blocks(self):
        self.write([make_record()], [])
        with self.assertRaisesRegex(ExportError, "missing AI turn annotation"):
            prepare_turn_export([self.source], self.ann)

    def test_missing_turn_label_blocks(self):
        a = annotation()
        a["assistant_turns"] = a["assistant_turns"][:1]
        self.write([make_record()], [a])
        with self.assertRaisesRegex(ExportError, "coverage mismatch"):
            prepare_turn_export([self.source], self.ann)

    def test_ai_review_does_not_replace_human_gate(self):
        row = make_record()
        row["quality"]["review_status"] = "unreviewed"
        self.write([row], [annotation()])
        with self.assertRaisesRegex(ExportError, "human record review"):
            prepare_turn_export([self.source], self.ann)

    def test_family_split_leakage_blocks(self):
        a, b = make_record("fa-a", "same", "train"), make_record("fa-b", "same", "test")
        b["messages"][0]["content"] = "درخواست دیگری"
        self.write([a, b], [annotation("fa-a"), annotation("fa-b")])
        with self.assertRaisesRegex(ExportError, "semantic-family leakage"):
            prepare_turn_export([self.source], self.ann)

    def test_superseded_predecessor_annotation_is_not_allowed(self):
        old, new = make_record("fa-old", "old"), make_record("fa-new", "new")
        new["metadata"]["supersedes_sample_id"] = "fa-old"
        self.write([old, new], [annotation("fa-old"), annotation("fa-new")])
        with self.assertRaisesRegex(ExportError, "unknown or superseded"):
            prepare_turn_export([self.source], self.ann)

    def test_annotations_are_provisional_only(self):
        a = annotation()
        a["review_status"] = "human_reviewed"
        self.write([make_record()], [a])
        with self.assertRaisesRegex(ExportError, "ai_provisional"):
            prepare_turn_export([self.source], self.ann)


if __name__ == "__main__":
    unittest.main()
