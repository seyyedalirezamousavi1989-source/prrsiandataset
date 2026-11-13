import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from build_legacy_taxonomy_mapping import canonical_domains,collect,build
TAX="""## Canonical primary domains

| Canonical domain | Scope |
|---|---|
| `intent_understanding` | intent |
| `context_continuity` | context |
| `ambiguity_handling` | ambiguity |
| `pragmatics_tone` | tone |

## Subskill naming rules
"""
class LegacyMappingTests(unittest.TestCase):
 def test_extracts_canonical_domains(self):
  self.assertEqual(canonical_domains(TAX),{"intent_understanding","context_continuity","ambiguity_handling","pragmatics_tone"})
 def test_excludes_identity_and_superseded_predecessors(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"old.jsonl"; i=Path(d)/"identity_v1.jsonl"
   p.write_text('{"sample_id":"old","domain":"pragmatics"}\n{"sample_id":"new","domain":"pragmatics","metadata":{"supersedes_sample_id":"old"}}\n',encoding="utf-8")
   i.write_text('{"sample_id":"id","domain":"pragmatics"}\n',encoding="utf-8")
   rows,labels,missing=collect([p,i],canonical_domains(TAX))
   self.assertEqual(len(rows),1); self.assertEqual(rows[0]["sample_id"],"new"); self.assertEqual(labels,["pragmatics"]); self.assertEqual(missing,0)
 def test_uncertain_labels_are_not_forced_into_a_domain(self):
  rows=[{"sample_id":"a","domain":"response_quality"},{"sample_id":"b","domain":"pragmatics"}]
  out=build(rows,["pragmatics","response_quality"],canonical_domains(TAX))
  self.assertEqual(out[0]["suggested_canonical_domain"],"pragmatics_tone")
  self.assertEqual(out[1]["suggested_canonical_domain"],"")
  self.assertEqual(out[1]["decision"],"pending_human_review")
if __name__=="__main__": unittest.main()
