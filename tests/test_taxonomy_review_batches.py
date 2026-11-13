import csv, json, tempfile, unittest
from pathlib import Path
from split_taxonomy_review_batches import split, merge

FIELDS=["sample_id","source_file","legacy_domain","legacy_subskills","language","register","message_count","conversation_json","existing_review_notes","label_level_suggestion","suggestion_confidence","suggestion_rationale","primary_behavior_assessment","adjudicated_canonical_domain","decision","reviewer","review_date","adjudication_rationale"]
CANONICAL="# Taxonomy V2\n\n## Canonical primary domains
| Domain |
|---|\n"+ "\n".join("| `"+x+"` |" for x in ["persian_fluency","everyday_dialogue","intent_understanding","context_continuity","ambiguity_handling","multi_turn_planning","instruction_following","colloquial_noisy_input","pragmatics_tone","lexical_precision","sentence_construction","explanation_reasoning","truthfulness","correction_recovery","emotional_support","adaptive_communication"])
class BatchTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
  self.template=self.root/"template.csv"
  with self.template.open("w",encoding="utf-8-sig",newline="") as f:
   w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader()
   for i in range(5):
    row={k:"" for k in FIELDS};row.update(sample_id=f"fa-{i}",source_file="x.jsonl",legacy_domain="legacy",conversation_json="[]",label_level_suggestion="everyday_dialogue",suggestion_confidence="low",decision="pending_human_review")
    w.writerow(row)
  self.tax=self.root/"taxonomy.md";self.tax.write_text(CANONICAL,encoding="utf-8")
 def tearDown(self): self.tmp.cleanup()
 def test_split_exact_coverage_and_merge(self):
  d=self.root/"batches";manifest=split(self.template,d,2)
  self.assertEqual(manifest["batch_count"],3)
  out=self.root/"merged.csv"
  report=merge(self.template,d/"manifest.json",d,out,self.tax,self.root/"report.json")
  self.assertEqual(report["summary"]["reviewed_records"],5)
  self.assertTrue(out.exists())
 def test_refuses_modified_batch(self):
  d=self.root/"batches";split(self.template,d,2)
  with (d/"taxonomy_review_batch_001.csv").open("a",encoding="utf-8") as f:f.write("\n")
  with self.assertRaisesRegex(ValueError,"checksum mismatch"):
   merge(self.template,d/"manifest.json",d,self.root/"merged.csv",self.tax,None)
 def test_refuses_overwrite(self):
  d=self.root/"batches";split(self.template,d,2);out=self.root/"merged.csv";out.write_text("keep")
  with self.assertRaisesRegex(ValueError,"overwrite"):
   merge(self.template,d/"manifest.json",d,out,self.tax,None)
if __name__=="__main__":unittest.main()
