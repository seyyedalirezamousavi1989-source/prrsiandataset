import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_dataset import validate_record, validate_files

def record(sample_id="fa-test-1"):
    return {"sample_id": sample_id, "domain": "everyday_dialogue", "language": "fa",
            "register": "colloquial", "split": "train",
            "messages": [{"role": "user", "content": "سلام"}, {"role": "assistant", "content": "سلام، خوبی؟"}],
            "metadata": {"provenance": "original_curated", "created_by": "unit_test"},
            "quality": {"review_status": "unreviewed"}}

class ValidatorTests(unittest.TestCase):
    def test_valid_record(self):
        self.assertEqual(validate_record(record(), "x", 1)[0], [])
    def test_unknown_top_level_field(self):
        row = record(); row["surprise"] = 1
        self.assertTrue(any("unknown top-level" in e for e in validate_record(row, "x", 1)[0]))
    def test_empty_message(self):
        row = record(); row["messages"][1]["content"] = " "
        self.assertTrue(any("content must be non-empty" in e for e in validate_record(row, "x", 1)[0]))
    def test_role_alternation(self):
        row = record(); row["messages"].insert(1, {"role": "user", "content": "باز هم"})
        self.assertTrue(any("must alternate" in e for e in validate_record(row, "x", 1)[0]))
    def test_invalid_quality_score(self):
        row = record(); row["quality"]["accuracy"] = 6
        self.assertTrue(any("integer from 1 to 5" in e for e in validate_record(row, "x", 1)[0]))
    def test_legacy_quality_warning(self):
        row = record(); del row["quality"]
        self.assertTrue(validate_record(row, "x", 1)[1])
    def test_duplicate_ids_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            line = json.dumps(record(), ensure_ascii=False)
            a, b = Path(tmp)/"a.jsonl", Path(tmp)/"b.jsonl"
            a.write_text(line + "\n", encoding="utf-8"); b.write_text(line + "\n", encoding="utf-8")
            self.assertTrue(any("duplicate sample_id" in e for e in validate_files([a, b])["errors"]))
    def test_missing_supersedes_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = record(); row["metadata"]["supersedes_sample_id"] = "absent"
            p = Path(tmp)/"a.jsonl"; p.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertTrue(any("not found" in e for e in validate_files([p])["errors"]))

if __name__ == "__main__": unittest.main()
