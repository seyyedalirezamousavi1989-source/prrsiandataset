#!/usr/bin/env python3
"""Validate human taxonomy adjudication decisions against the generated review packet."""
from __future__ import annotations
import argparse,csv,json,re,sys
from datetime import date
from pathlib import Path
from build_legacy_taxonomy_mapping import canonical_domains

REQUIRED={"sample_id","source_file","legacy_domain","conversation_json","label_level_suggestion","suggestion_confidence","primary_behavior_assessment","adjudicated_canonical_domain","decision","reviewer","review_date","adjudication_rationale"}
PROTECTED={"sample_id","source_file","legacy_domain","legacy_subskills","language","register","message_count","conversation_json","existing_review_notes","label_level_suggestion","suggestion_confidence","suggestion_rationale"}
DECISIONS={"pending_human_review","accepted_suggestion","changed_mapping","needs_expert_review"}

def read_csv(path):
 with path.open(encoding="utf-8-sig",newline="") as f:
  reader=csv.DictReader(f)
  if not reader.fieldnames: raise ValueError(f"{path}: missing CSV header")
  missing=REQUIRED-set(reader.fieldnames)
  if missing: raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
  rows=list(reader)
 return rows

def validate(template_path,reviewed_path,canonical,require_complete=False):
 template=read_csv(template_path); reviewed=read_csv(reviewed_path); errors=[]
 def index(rows,label):
  out={}
  for n,r in enumerate(rows,2):
   sid=r.get("sample_id","").strip()
   if not sid: errors.append(f"{label} row {n}: blank sample_id")
   elif sid in out: errors.append(f"{label}: duplicate sample_id {sid}")
   else: out[sid]=r
  return out
 base=index(template,"template"); done=index(reviewed,"reviewed")
 if set(base)!=set(done):
  errors.append(f"sample ID set mismatch: missing={len(set(base)-set(done))}, unexpected={len(set(done)-set(base))}")
 counts={k:0 for k in DECISIONS}
 for sid,orig in base.items():
  r=done.get(sid)
  if r is None: continue
  for key in PROTECTED:
   if r.get(key,"")!=orig.get(key,""): errors.append(f"{sid}: protected field changed: {key}")
  decision=(r.get("decision") or "").strip()
  if decision not in DECISIONS: errors.append(f"{sid}: invalid decision {decision!r}"); continue
  counts[decision]+=1
  domain=(r.get("adjudicated_canonical_domain") or "").strip()
  reviewer=(r.get("reviewer") or "").strip()
  review_date=(r.get("review_date") or "").strip()
  rationale=(r.get("adjudication_rationale") or "").strip()
  assessment=(r.get("primary_behavior_assessment") or "").strip()
  if decision=="pending_human_review":
   if any((domain,reviewer,review_date,rationale,assessment)): errors.append(f"{sid}: pending row must not contain adjudication fields")
   continue
  if not reviewer: errors.append(f"{sid}: reviewer is required")
  try: date.fromisoformat(review_date)
  except ValueError: errors.append(f"{sid}: review_date must be ISO YYYY-MM-DD")
  if not rationale: errors.append(f"{sid}: adjudication_rationale is required")
  if not assessment: errors.append(f"{sid}: primary_behavior_assessment is required")
  if decision in {"accepted_suggestion","changed_mapping"}:
   if domain not in canonical: errors.append(f"{sid}: adjudicated domain must be one canonical domain")
   suggestion=(orig.get("label_level_suggestion") or "").strip()
   if decision=="accepted_suggestion" and domain!=suggestion: errors.append(f"{sid}: accepted_suggestion must equal label-level suggestion")
   if decision=="changed_mapping" and (not suggestion or domain==suggestion): errors.append(f"{sid}: changed_mapping must differ from a non-empty suggestion")
  elif decision=="needs_expert_review" and domain:
   errors.append(f"{sid}: needs_expert_review must leave adjudicated domain blank")
 if require_complete and counts["pending_human_review"]:
  errors.append(f"review incomplete: {counts['pending_human_review']} pending rows remain")
 summary={"template_records":len(base),"reviewed_records":len(done),"decision_counts":counts,"complete":counts["pending_human_review"]==0,"errors":len(errors),"automatic_adjudication":False,"source_staging_mutation":False,"training_approval":False}
 return errors,summary

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--taxonomy",required=True,type=Path);p.add_argument("--template",required=True,type=Path);p.add_argument("--reviewed",required=True,type=Path);p.add_argument("--json-report",type=Path);p.add_argument("--require-complete",action="store_true")
 a=p.parse_args()
 try:
  errors,summary=validate(a.template,a.reviewed,canonical_domains(a.taxonomy.read_text(encoding="utf-8")),a.require_complete)
  print(json.dumps(summary,ensure_ascii=False,indent=2))
  if a.json_report:
   a.json_report.parent.mkdir(parents=True,exist_ok=True);a.json_report.write_text(json.dumps({"summary":summary,"errors":errors},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  for e in errors: print("ERROR: "+e,file=sys.stderr)
  return 1 if errors else 0
 except (OSError,ValueError,csv.Error,json.JSONDecodeError) as e:
  print(f"ADJUDICATION VALIDATION FAILED: {e}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
