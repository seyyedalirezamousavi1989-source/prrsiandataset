import sys,tempfile,unittest,csv,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from build_sample_taxonomy_adjudication import build_rows
CAN={"intent_understanding","context_continuity","ambiguity_handling","pragmatics_tone"}
class SamplePacketTests(unittest.TestCase):
 def test_includes_full_conversation_and_blank_human_decisions(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"pilot.jsonl"
   p.write_text(json.dumps({"sample_id":"x1","domain":"pragmatics","subskills":["indirect_refusal"],"language":"fa","register":"colloquial","messages":[{"role":"user","content":"یعنی چی؟"},{"role":"assistant","content":"بستگی داره."}],"metadata":{"review_notes":"inspect tone"}},ensure_ascii=False)+"\n",encoding="utf-8")
   rows,summary=build_rows([p],CAN)
   self.assertEqual(len(rows),1)
   self.assertEqual(json.loads(rows[0]["conversation_json"])[0]["content"],"یعنی چی؟")
   self.assertEqual(rows[0]["adjudicated_canonical_domain"],"")
   self.assertEqual(rows[0]["decision"],"pending_human_review")
   self.assertFalse(summary["automatic_adjudication"])
 def test_uncertain_label_has_no_forced_suggestion(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"pilot.jsonl"
   p.write_text('{"sample_id":"x2","domain":"response_quality","messages":[]}\n',encoding="utf-8")
   rows,_=build_rows([p],CAN)
   self.assertEqual(rows[0]["label_level_suggestion"],"")
   self.assertEqual(rows[0]["suggestion_confidence"],"requires_record_level_review")
 def test_excludes_identity_and_superseded(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"pilot.jsonl"; ident=Path(d)/"identity_v1.jsonl"
   p.write_text('{"sample_id":"old","domain":"pragmatics","messages":[]}\n{"sample_id":"new","domain":"pragmatics","messages":[],"metadata":{"supersedes_sample_id":"old"}}\n',encoding="utf-8")
   ident.write_text('{"sample_id":"id","domain":"pragmatics","messages":[]}\n',encoding="utf-8")
   rows,summary=build_rows([p,ident],CAN)
   self.assertEqual([r["sample_id"] for r in rows],["new"])
   self.assertTrue(summary["identity_excluded"])
if __name__=="__main__":unittest.main()
