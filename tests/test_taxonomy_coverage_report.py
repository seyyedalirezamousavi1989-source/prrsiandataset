import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_taxonomy_coverage_report import canonical_domains, load_active, build_report, band

TAXONOMY = """## Canonical primary domains

| Canonical domain | Scope |
|---|---|
| `alpha_domain` | A |
| `beta_domain` | B |

## Subskill naming rules
"""

class TaxonomyCoverageTests(unittest.TestCase):
    def test_reads_canonical_domain_vocabulary_from_taxonomy(self):
        self.assertEqual(canonical_domains(TAXONOMY), ["alpha_domain", "beta_domain"])

    def test_excludes_identity_and_superseded_records(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/"batch.jsonl"; identity=root/"identity_v1.jsonl"
            src.write_text('{"sample_id":"old","domain":"alpha_domain"}\n{"sample_id":"new","domain":"beta_domain","metadata":{"supersedes_sample_id":"old"}}\n{"sample_id":"keep","domain":"alpha_domain"}\n',encoding="utf-8")
            identity.write_text('{"sample_id":"id-only","domain":"alpha_domain"}\n',encoding="utf-8")
            rows=load_active([src,identity])
            self.assertEqual([r["sample_id"] for r in rows],["new","keep"])

    def test_reports_missing_and_invalid_metadata_without_relabeling(self):
        rows=[
          {"sample_id":"a","domain":"alpha_domain","subskills":["skill_a"],"register":"neutral","language":"fa","quality":{"review_status":"unreviewed"},"messages":[{"role":"user"},{"role":"assistant"}]},
          {"sample_id":"b","domain":"unknown","subskills":[],"register":"odd","language":None,"quality":{},"messages":[]}
        ]
        r=build_report(rows,["alpha_domain","beta_domain"])
        self.assertEqual([x["count"] for x in r["domain_coverage"]],[1,0])
        self.assertEqual(r["invalid_domain_count"],1)
        self.assertEqual(r["subskill_missing_record_count"],1)
        self.assertEqual(r["register"]["missing_or_invalid_count"],1)
        self.assertEqual(r["language"]["missing_or_invalid_count"],1)
        self.assertFalse(r["automatic_relabeling"])
        self.assertFalse(r["training_approval"])
        self.assertEqual(rows[1]["domain"],"unknown")

    def test_triage_bands_are_descriptive(self):
        self.assertEqual([band(x) for x in (0,2,7,12)],["absent","1-4","5-9","10+"])

if __name__=="__main__": unittest.main()
