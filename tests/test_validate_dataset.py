import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import validate_record, validate_files
from scripts.export_training import prepare_export, ExportError


def record(sample_id="fa-test-1"):
    return {
        "sample_id": sample_id,
        "domain": "everyday_dialogue",
        "language": "fa",
        "register": "colloquial",
        "split": "train",
        "messages": [
            {"role": "user", "content": "سلام"},
            {"role": "assistant", "content": "سلام، خوبی؟"},
        ],
        "metadata": {"provenance": "original_curated", "created_by": "unit_test"},
        "quality": {"review_status": "unreviewed"},
    }


class ValidatorTests(unittest.TestCase):
    def test_valid_record(self):
        self.assertEqual(validate_record(record(), "x", 1)[0], [])

    def test_unknown_top_level_field(self):
        row = record()
        row["surprise"] = 1
        self.assertTrue(any("unknown top-level" in e for e in validate_record(row, "x", 1)[0]))

    def test_empty_message(self):
        row = record()
        row["messages"][1]["content"] = " "
        self.assertTrue(any("content must be non-empty" in e for e in validate_record(row, "x", 1)[0]))

    def test_role_alternation(self):
        row = record()
        row["messages"].insert(1, {"role": "user", "content": "باز هم"})
        self.assertTrue(any("must alternate" in e for e in validate_record(row, "x", 1)[0]))

    def test_invalid_quality_score(self):
        row = record()
        row["quality"]["accuracy"] = 6
        self.assertTrue(any("integer from 1 to 5" in e for e in validate_record(row, "x", 1)[0]))

    def test_legacy_quality_warning(self):
        row = record()
        del row["quality"]
        self.assertTrue(validate_record(row, "x", 1)[1])

    def test_duplicate_ids_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            line = json.dumps(record(), ensure_ascii=False)
            a, b = Path(tmp) / "a.jsonl", Path(tmp) / "b.jsonl"
            a.write_text(line + "\n", encoding="utf-8")
            b.write_text(line + "\n", encoding="utf-8")
            self.assertTrue(any("duplicate sample_id" in e for e in validate_files([a, b])["errors"]))

    def test_missing_supersedes_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["metadata"]["supersedes_sample_id"] = "absent"
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertTrue(any("not found" in e for e in validate_files([p])["errors"]))

    def test_human_review_requires_reviewer_and_date(self):
        row = record()
        row["quality"]["review_status"] = "human_reviewed"
        errors = validate_record(row, "x", 1)[0]
        self.assertTrue(any("requires quality.reviewer" in e for e in errors))
        self.assertTrue(any("requires quality.reviewed_at" in e for e in errors))

    def test_human_review_with_evidence(self):
        row = record()
        row["quality"].update({
            "review_status": "human_reviewed",
            "reviewer": "reviewer-1",
            "reviewed_at": "2026-11-13",
        })
        self.assertEqual(validate_record(row, "x", 1)[0], [])

    def test_invalid_review_date(self):
        row = record()
        row["quality"].update({"reviewer": "reviewer-1", "reviewed_at": "13/11/2026"})
        self.assertTrue(any("ISO date" in e for e in validate_record(row, "x", 1)[0]))


    def test_strict_taxonomy_rejects_noncanonical_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["domain"] = "mixed"
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertTrue(any("non-canonical primary domain" in e for e in validate_files([p], strict_taxonomy=True)["errors"]))


    def test_taxonomy_exception_is_exact_and_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["domain"] = "mixed"
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            exceptions = {row["sample_id"]: {"domain": "mixed", "reason": "pending human taxonomy adjudication"}}
            report = validate_files([p], strict_taxonomy=True, taxonomy_exceptions=exceptions)
            self.assertEqual(report["errors"], [])
            self.assertTrue(any("temporary taxonomy exception" in w for w in report["warnings"]))

    def test_taxonomy_exception_does_not_allow_different_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["domain"] = "mixed"
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            exceptions = {row["sample_id"]: {"domain": "identity", "reason": "wrong domain"}}
            report = validate_files([p], strict_taxonomy=True, taxonomy_exceptions=exceptions)
            self.assertTrue(any("non-canonical primary domain" in e for e in report["errors"]))

    def test_training_ready_rejects_unreviewed_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(record(), ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertTrue(any("requires quality.review_status=human_reviewed" in e for e in validate_files([p], training_ready=True)["errors"]))

    def test_training_ready_requires_all_human_scores(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["quality"].update({"review_status": "human_reviewed", "reviewer": "reviewer-1", "reviewed_at": "2026-11-13"})
            p = Path(tmp) / "a.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertTrue(any("missing valid human scores" in e for e in validate_files([p], training_ready=True)["errors"]))

    def test_training_ready_rejects_superseded_predecessor(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = record("fa-old")
            new = record("fa-new")
            new["metadata"]["supersedes_sample_id"] = "fa-old"
            scores = {k: 4 for k in ("intent_fidelity", "context_use", "persian_fluency", "accuracy", "instruction_adherence", "tone_appropriateness", "non_redundancy")}
            for row in (old, new):
                row["quality"].update({"review_status": "human_reviewed", "reviewer": "reviewer-1", "reviewed_at": "2026-11-13", **scores})
            p = Path(tmp) / "a.jsonl"
            p.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in (old, new)), encoding="utf-8")
            self.assertTrue(any("superseded predecessor" in e for e in validate_files([p], training_ready=True)["errors"]))


    def reviewed_export_record(self, sample_id="fa-export-1", family="family-1", split="train"):
        row = record(sample_id)
        row["split"] = split
        row["metadata"]["semantic_family_id"] = family
        scores = {k: 4 for k in ("intent_fidelity", "context_use", "persian_fluency", "accuracy", "instruction_adherence", "tone_appropriateness", "non_redundancy")}
        row["quality"].update({"review_status": "human_reviewed", "reviewer": "human-reviewer", "reviewed_at": "2026-11-13", **scores})
        return row

    def test_export_requires_human_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record()
            row["metadata"]["semantic_family_id"] = "family-1"
            p = Path(tmp) / "data.jsonl"
            p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            with self.assertRaises(ExportError):
                prepare_export([p])

    def test_export_blocks_semantic_family_split_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = self.reviewed_export_record("fa-export-a", "same-family", "train")
            b = self.reviewed_export_record("fa-export-b", "same-family", "test")
            b["messages"][0]["content"] = "یک گفت‌وگوی متفاوت"
            p = Path(tmp) / "data.jsonl"
            p.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in (a, b)), encoding="utf-8")
            with self.assertRaisesRegex(ExportError, "semantic-family leakage"):
                prepare_export([p])

    def test_export_excludes_superseded_predecessor(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = self.reviewed_export_record("fa-old", "family-old")
            new = self.reviewed_export_record("fa-new", "family-new")
            new["metadata"]["supersedes_sample_id"] = "fa-old"
            new["messages"][0]["content"] = "نسخه اصلاح‌شده"
            p = Path(tmp) / "data.jsonl"
            p.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in (old, new)), encoding="utf-8")
            splits, manifest = prepare_export([p])
            self.assertEqual(manifest["active_record_count"], 1)
            self.assertEqual(manifest["excluded_superseded_count"], 1)
            self.assertEqual([x["sample_id"] for x in splits["train"]], ["fa-new"])

    def test_extended_quality_scores(self):
        row = record()
        row["quality"].update({"tone_appropriateness": 5, "non_redundancy": 4})
        self.assertEqual(validate_record(row, "x", 1)[0], [])


if __name__ == "__main__":
    unittest.main()
