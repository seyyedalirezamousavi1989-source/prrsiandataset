import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import validate_record, validate_files


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

    def test_extended_quality_scores(self):
        row = record()
        row["quality"].update({"tone_appropriateness": 5, "non_redundancy": 4})
        self.assertEqual(validate_record(row, "x", 1)[0], [])


if __name__ == "__main__":
    unittest.main()
