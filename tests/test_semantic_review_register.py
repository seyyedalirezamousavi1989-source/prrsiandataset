import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_semantic_review_register import build_rows


def payload(pairs):
    return {
        "purpose": "human_review_candidate_pairs_only",
        "automatic_family_assignment": False,
        "automatic_split_assignment": False,
        "candidate_pair_count": len(pairs),
        "pairs": pairs,
    }


class SemanticReviewRegisterTests(unittest.TestCase):
    def test_builds_pending_rows_without_family_or_split_assignment(self):
        rows = build_rows(payload([{
            "sample_a": "fa-a", "sample_b": "fa-b",
            "source_a": "a.jsonl", "source_b": "b.jsonl",
            "domain_a": "truthfulness", "domain_b": "truthfulness",
            "jaccard": 0.25, "shared_terms": ["گزارش", "داده"],
        }]))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["pair_id"], "SF-001")
        self.assertEqual(rows[0]["decision"], "pending")
        self.assertEqual(rows[0]["reviewer"], "")
        self.assertEqual(rows[0]["review_date"], "")
        self.assertEqual(rows[0]["rationale"], "")
        self.assertEqual(rows[0]["shared_terms"], "گزارش | داده")
        self.assertNotIn("semantic_family_id", rows[0])
        self.assertNotIn("split", rows[0])

    def test_rejects_wrong_report_purpose(self):
        data = payload([])
        data["purpose"] = "training_export"
        with self.assertRaises(ValueError):
            build_rows(data)

    def test_rejects_auto_assignment_enabled(self):
        data = payload([])
        data["automatic_split_assignment"] = True
        with self.assertRaises(ValueError):
            build_rows(data)

    def test_rejects_duplicate_pair(self):
        pair = {"sample_a": "fa-a", "sample_b": "fa-b"}
        with self.assertRaises(ValueError):
            build_rows(payload([pair, pair]))

    def test_rejects_candidate_count_mismatch(self):
        data = payload([])
        data["candidate_pair_count"] = 1
        with self.assertRaises(ValueError):
            build_rows(data)


if __name__ == "__main__":
    unittest.main()
