#!/usr/bin/env python3
"""Build a sample-level, human-only taxonomy adjudication CSV for legacy records."""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
from build_legacy_taxonomy_mapping import PROPOSALS,canonical_domains,collect

FIELDS=["sample_id","source_file","legacy_domain","legacy_subskills","language","register","message_count","conversation_json","existing_review_notes","label_level_suggestion","suggestion_confidence","suggestion_rationale","primary_behavior_assessment","adjudicated_canonical_domain","decision","reviewer","review_date","adjudication_rationale"]

def build_rows(paths,canonical):
    active,labels,missing=collect(paths,canonical)
    superseded={r.get("metadata",{}).get("supersedes_sample_id") for r in active if isinstance(r.get("metadata"),dict) and r["metadata"].get("supersedes_sample_id")}
    # collect() has already removed predecessors; reconstruct source path by unique sample ID.
    source={}
    for path in paths:
        if "identity" in path.name.lower(): continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r=json.loads(line); source[r["sample_id"]]=path.as_posix()
    out=[]
    for r in active:
        domain=r.get("domain")
        if domain in canonical: continue
        suggestion,confidence,rationale=PROPOSALS.get(domain,("","requires_record_level_review","No defensible label-level mapping is defined; inspect this sample."))
        meta=r.get("metadata") if isinstance(r.get("metadata"),dict) else {}
        out.append({
          "sample_id":r["sample_id"],"source_file":source.get(r["sample_id"],""),
          "legacy_domain":domain or "","legacy_subskills":json.dumps(r.get("subskills",[]),ensure_ascii=False),
          "language":r.get("language",""),"register":r.get("register",""),
          "message_count":len(r.get("messages",[])),
          "conversation_json":json.dumps(r.get("messages",[]),ensure_ascii=False,separators=(",",":")),
          "existing_review_notes":meta.get("review_notes",""),
          "label_level_suggestion":suggestion,"suggestion_confidence":confidence,
          "suggestion_rationale":rationale,"primary_behavior_assessment":"",
          "adjudicated_canonical_domain":"","decision":"pending_human_review",
          "reviewer":"","review_date":"","adjudication_rationale":""
        })
    return out,{"active_general_records":len(active),"legacy_sample_count":len(out),"legacy_label_count":len(labels),"missing_or_invalid_domain_records":missing,"identity_excluded":True,"superseded_predecessors_excluded":True,"full_conversation_included":True,"automatic_adjudication":False,"staging_mutation":False,"family_assignment":False,"split_assignment":False,"training_approval":False}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--taxonomy",required=True,type=Path);p.add_argument("--csv-output",required=True,type=Path);p.add_argument("--summary-output",required=True,type=Path);p.add_argument("files",nargs="+",type=Path)
 a=p.parse_args()
 if a.csv_output.exists() or a.summary_output.exists():p.error("refusing to overwrite existing output")
 try:
  canonical=canonical_domains(a.taxonomy.read_text(encoding="utf-8"))
  rows,summary=build_rows(a.files,canonical)
  a.csv_output.parent.mkdir(parents=True,exist_ok=True)
  with a.csv_output.open("w",encoding="utf-8-sig",newline="") as f:
   w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
  a.summary_output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps(summary,ensure_ascii=False,indent=2))
 except (OSError,ValueError,json.JSONDecodeError,KeyError) as e:p.exit(1,f"SAMPLE-LEVEL ADJUDICATION PACKET FAILED: {e}\n")
if __name__=="__main__":main()
