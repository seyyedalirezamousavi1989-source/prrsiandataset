import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_unmatched_record_inventory import build_inventory, load_active_records


class UnmatchedInventoryTests(unittest.TestCase):
    def test_marks_records_absent_from_candidate_pairs_without_assigning_family(self):
        records = [
            {"sample_id": "fa-a", "domain": "truthfulness", "messages": [{"role": "user"}, {"role": "assistant"}], "_source_file": "a.jsonl"},
            {"sample_id": "fa-b", "domain": "truthfulness", "messages": [{"role": "user"}, {"role": "assistant"}], "_source_file": "b.jsonl"},
            {"sample_id": "fa-c", "domain": "lexical_precision", "messages": [{"role": "user"}], "_source_file": "c.jsonl"},
        ]
        report = {
            "purpose": "human_review_candidate_pairs_only",
            "automatic_family_assignment": False,
            "automatic_split_assignment": False,
            "active_record_count": 3,
            "candidate_pair_count": 1,
            "pairs": [{"sample_a": "fa-a", "sample_b": "fa-b"}],
        }
        rows, summary = build_inventory(report, records)
        self.assertEqual([r["sample_id"] for r in rows], ["fa-c"])
        self.assertEqual(rows[0]["family_assessment"], "unassessed")
        self.assertEqual(rows[0]["review_status"], "pending_human_review")
        self.assertEqual(rows[0]["reviewer"], "")
        self.assertEqual(summary["records_linked_to_at_least_one_candidate_pair"], 2)
        self.assertEqual(summary["unmatched_record_count"], 1)
        self.assertFalse(summary["automatic_family_assignment"])
        self.assertFalse(summary["training_approval"])

    def test_rejects_unknown_candidate_sample(self):
        report = {
            "purpose": "human_review_candidate_pairs_only",
            "automatic_family_assignment": False,
            "automatic_split_assignment": False,
            "active_record_count": 1,
            "candidate_pair_count": 1,
            "pairs": [{"sample_a": "fa-a", "sample_b": "missing"}],
        }
        with self.assertRaises(ValueError):
            build_inventory(report, [{"sample_id": "fa-a", "messages": []}])

    def test_rejects_active_count_mismatch(self):
        report = {
            "purpose": "human_review_candidate_pairs_only",
            "automatic_family_assignment": False,
            "automatic_split_assignment": False,
            "active_record_count": 2,
            "candidate_pair_count": 0,
            "pairs": [],
        }
        with self.assertRaises(ValueError):
            build_inventory(report, [{"sample_id": "fa-a", "messages": []}])

    def test_excludes_superseded_predecessor_and_identity_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            main = root / "batch.jsonl"
            identity = root / "identity_v1.jsonl"
            main.write_text(
                '{"sample_id":"old","messages":[]}\n'
                '{"sample_id":"new","metadata":{"supersedes_sample_id":"old"},"messages":[]}\n'
                '{"sample_id":"alone","messages":[]}\n',
                encoding="utf-8",
            )
            identity.write_text('{"sample_id":"identity-1","messages":[]}\n', encoding="utf-8")
            records = load_active_records([main, identity])
            self.assertEqual([r["sample_id"] for r in records], ["new", "alone"])


if __name__ == "__main__":
    unittest.main()
