import sys,tempfile,unittest,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from validate_taxonomy_adjudication import validate
FIELDS=["sample_id","source_file","legacy_domain","legacy_subskills","language","register","message_count","conversation_json","existing_review_notes","label_level_suggestion","suggestion_confidence","suggestion_rationale","primary_behavior_assessment","adjudicated_canonical_domain","decision","reviewer","review_date","adjudication_rationale"]
CAN={"intent_understanding","context_continuity","ambiguity_handling","pragmatics_tone"}
class AdjudicationValidationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.d=Path(self.tmp.name)
  self.template=self.d/"template.csv";self.reviewed=self.d/"reviewed.csv"
  self.row=dict.fromkeys(FIELDS,"");self.row.update(sample_id="s1",source_file="x.jsonl",legacy_domain="pragmatics",conversation_json='[{"role":"user","content":"x"}]',label_level_suggestion="pragmatics_tone",suggestion_confidence="high",decision="pending_human_review")
  self.write(self.template,[self.row]);self.write(self.reviewed,[self.row])
 def write(self,p,rows):
  with p.open("w",encoding="utf-8-sig",newline="") as f:
   w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
 def test_blank_template_is_valid_non_strict(self):
  errors,s=validate(self.template,self.reviewed,CAN);self.assertEqual(errors,[]);self.assertEqual(s["decision_counts"]["pending_human_review"],1)
 def test_accepted_suggestion_requires_matching_canonical_domain_and_evidence(self):
  r=dict(self.row,decision="accepted_suggestion",adjudicated_canonical_domain="pragmatics_tone",reviewer="Reviewer",review_date="2026-11-13",primary_behavior_assessment="Interprets indirect refusal.",adjudication_rationale="The user asks what the hedged reply implies.")
  self.write(self.reviewed,[r]);errors,_=validate(self.template,self.reviewed,CAN);self.assertEqual(errors,[])
 def test_rejects_protected_content_change(self):
  r=dict(self.row,conversation_json="[]");self.write(self.reviewed,[r]);errors,_=validate(self.template,self.reviewed,CAN);self.assertTrue(any("protected field changed" in e for e in errors))
 def test_rejects_invalid_domain_and_missing_reviewer(self):
  r=dict(self.row,decision="changed_mapping",adjudicated_canonical_domain="made_up",review_date="2026-11-13",primary_behavior_assessment="x",adjudication_rationale="x");self.write(self.reviewed,[r]);errors,_=validate(self.template,self.reviewed,CAN);self.assertTrue(any("canonical domain" in e for e in errors));self.assertTrue(any("reviewer is required" in e for e in errors))
 def test_needs_expert_review_keeps_domain_blank(self):
  r=dict(self.row,decision="needs_expert_review",adjudicated_canonical_domain="pragmatics_tone",reviewer="R",review_date="2026-11-13",primary_behavior_assessment="x",adjudication_rationale="x");self.write(self.reviewed,[r]);errors,_=validate(self.template,self.reviewed,CAN);self.assertTrue(any("must leave adjudicated domain blank" in e for e in errors))
 def test_requires_complete_blocks_pending_rows(self):
  errors,_=validate(self.template,self.reviewed,CAN,True);self.assertTrue(any("pending rows remain" in e for e in errors))
if __name__=="__main__":unittest.main()
