import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from scripts.review_assistant_turns_ollama import ReviewError, parse_model_response, read_jsonl, review_corpus

class ReviewerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.source=self.root/"source.jsonl"; self.output=self.root/"annotations.jsonl"
        self.row={"sample_id":"fa-review-1","domain":"everyday_dialogue","language":"fa","register":"neutral","messages":[{"role":"user","content":"متن را اصلاح کن."},{"role":"assistant","content":"پاسخ اولیه."},{"role":"user","content":"این پاسخ اشتباه بود."},{"role":"assistant","content":"نسخه اصلاح‌شده."}],"metadata":{"provenance":"test"}}
        self.source.write_text(json.dumps(self.row,ensure_ascii=False)+"\n",encoding="utf-8")
    def tearDown(self): self.tmp.cleanup()
    def response(self):
        return "reviewer-test:latest",json.dumps({"assistant_turns":[
        {"message_index":1,"label":"negative_or_demonstration_only","rationale":"پاسخ اولیه با درخواست ناسازگار است.","confidence":0.92,"evidence_message_indices":[0,2],"issues":["intent_mismatch"]},
        {"message_index":3,"label":"positive_target","rationale":"پاسخ اصلاحی درخواست را برآورده می‌کند.","confidence":0.88,"evidence_message_indices":[0,2],"issues":[]} ]},ensure_ascii=False)
    def test_exact_turn_coverage(self):
        _,content=self.response(); self.assertEqual(len(parse_model_response(content,{1,3},"id",4)),2)
    def test_missing_turn_rejected(self):
        _,content=self.response(); d=json.loads(content); d["assistant_turns"].pop()
        with self.assertRaisesRegex(ReviewError,"coverage mismatch"): parse_model_response(json.dumps(d),{1,3},"id",4)
    def test_invalid_label_and_confidence_rejected(self):
        _,content=self.response(); d=json.loads(content); d["assistant_turns"][0]["label"]="approved"
        with self.assertRaises(ReviewError): parse_model_response(json.dumps(d),{1,3},"id",4)
        d["assistant_turns"][0]["label"]="positive_target"; d["assistant_turns"][0]["confidence"]=1.4
        with self.assertRaises(ReviewError): parse_model_response(json.dumps(d),{1,3},"id",4)
    @patch("scripts.review_assistant_turns_ollama.ollama_chat")
    def test_ai_provisional_and_source_unchanged(self,mock):
        mock.return_value=self.response(); before=self.source.read_bytes()
        result=review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30)
        ann=json.loads(self.output.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(ann["review_status"],"ai_provisional"); self.assertEqual(ann["reviewer_type"],"ai")
        self.assertEqual(ann["review_model"],"reviewer-test:latest"); self.assertFalse(result["training_approval"])
        self.assertEqual(before,self.source.read_bytes()); self.assertEqual(result["newly_reviewed_records"],1)
    @patch("scripts.review_assistant_turns_ollama.ollama_chat")
    def test_resume_skips_existing_record(self,mock):
        mock.return_value=self.response(); review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30)
        result=review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30,resume=True)
        self.assertEqual(result["newly_reviewed_records"],0); self.assertEqual(mock.call_count,1)
    @patch("scripts.review_assistant_turns_ollama.ollama_chat")
    def test_resume_rejects_changed_source(self,mock):
        mock.return_value=self.response(); review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30)
        changed=dict(self.row); changed["messages"]=self.row["messages"]+[{"role":"user","content":"تغییر"}]
        self.source.write_text(json.dumps(changed,ensure_ascii=False)+"\n",encoding="utf-8")
        with self.assertRaisesRegex(ReviewError,"source record changed"):
            review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30,resume=True)
    def test_existing_output_never_overwritten(self):
        self.output.write_text("keep\n",encoding="utf-8")
        with self.assertRaisesRegex(ReviewError,"refusing overwrite"): review_corpus([self.source],self.output,"m","http://localhost",30)
        self.assertEqual(self.output.read_text(encoding="utf-8"),"keep\n")
    def test_superseded_predecessor_excluded(self):
        old=dict(self.row); old["sample_id"]="old"; new=dict(self.row); new["sample_id"]="new"; new["metadata"]={"supersedes_sample_id":"old"}
        path=self.root/"revisions.jsonl"; path.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in [old,new])+"\n",encoding="utf-8")
        _,active,repl=read_jsonl([path]); self.assertEqual([x[0]["sample_id"] for x in active],["new"]); self.assertEqual(repl,{"old":"new"})

    @patch("scripts.review_assistant_turns_ollama.ollama_chat")
    def test_resume_rejects_tampered_annotation(self,mock):
        mock.return_value=self.response()
        review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30)
        saved=json.loads(self.output.read_text(encoding="utf-8").splitlines()[0])
        saved["assistant_turns"][0]["label"]="human_approved"
        self.output.write_text(json.dumps(saved,ensure_ascii=False)+"\n",encoding="utf-8")
        with self.assertRaises(ReviewError):
            review_corpus([self.source],self.output,"reviewer-test:latest","http://localhost:11434",30,resume=True)

if __name__=="__main__": unittest.main()
