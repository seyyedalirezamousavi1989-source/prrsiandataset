#!/usr/bin/env python3
"""Split and safely merge human taxonomy-review CSV batches."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path
from validate_taxonomy_adjudication import read_csv, validate
from build_legacy_taxonomy_mapping import canonical_domains

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def split(template_path,out_dir,batch_size):
    if batch_size<1: raise ValueError("batch size must be >= 1")
    if out_dir.exists() and any(out_dir.iterdir()): raise ValueError(f"refusing to overwrite non-empty directory: {out_dir}")
    rows=read_csv(template_path)
    ids=[r["sample_id"].strip() for r in rows]
    if any(not x for x in ids) or len(ids)!=len(set(ids)): raise ValueError("template has blank or duplicate sample IDs")
    fields=list(rows[0]) if rows else []
    if not fields: raise ValueError("template contains no records")
    out_dir.mkdir(parents=True,exist_ok=True)
    batches=[]
    for offset in range(0,len(rows),batch_size):
        part=rows[offset:offset+batch_size]
        number=len(batches)+1
        name=f"taxonomy_review_batch_{number:03d}.csv"
        path=out_dir/name
        write_csv(path,fields,part)
        batches.append({"batch_id":f"B{number:03d}","file":name,"sample_ids":[r["sample_id"] for r in part],"record_count":len(part),"sha256":digest(path),"status":"not_started"})
    manifest={"manifest_version":1,"template_file":template_path.name,"template_sha256":digest(template_path),"template_record_count":len(rows),"batch_size":batch_size,"batch_count":len(batches),"batches":batches,"human_review_only":True,"automatic_adjudication":False,"source_staging_mutation":False,"family_assignment":False,"split_assignment":False,"training_approval":False}
    (out_dir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def merge(template_path,manifest_path,batch_dir,output_path,taxonomy_path,report_path,require_complete=False):
    if output_path.exists(): raise ValueError(f"refusing to overwrite output: {output_path}")
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("manifest_version")!=1: raise ValueError("unsupported manifest version")
    if digest(template_path)!=manifest.get("template_sha256"): raise ValueError("template checksum mismatch; baseline template changed")
    template=read_csv(template_path)
    if len(template)!=manifest.get("template_record_count"): raise ValueError("template record count mismatch")
    expected={r["sample_id"]:r for r in template}
    batch_defs=manifest.get("batches",[])
    seen_files=set(); seen_ids=set(); merged={}
    for b in batch_defs:
        name=b.get("file","")
        if not name or Path(name).name!=name or name in seen_files: raise ValueError("invalid or duplicate batch filename in manifest")
        seen_files.add(name)
        path=batch_dir/name
        if not path.is_file(): raise ValueError(f"missing batch file: {name}")
        if digest(path)!=b.get("sha256"): raise ValueError(f"batch checksum mismatch: {name}; if reviewed, use a reviewed copy and do not modify the original batch")
        rows=read_csv(path)
        ids=[r["sample_id"] for r in rows]
        if len(rows)!=b.get("record_count") or ids!=b.get("sample_ids"): raise ValueError(f"batch membership/order mismatch: {name}")
        for r in rows:
            sid=r["sample_id"]
            if sid not in expected: raise ValueError(f"unknown sample ID: {sid}")
            if sid in seen_ids: raise ValueError(f"sample appears in multiple batches: {sid}")
            seen_ids.add(sid); merged[sid]=r
    if seen_ids!=set(expected): raise ValueError(f"batch coverage mismatch: missing={len(set(expected)-seen_ids)} unexpected={len(seen_ids-set(expected))}")
    # Preserve master-template order and columns; validator enforces protected-field integrity.
    fields=list(template[0]) if template else []
    ordered=[merged[r["sample_id"]] for r in template]
    output_path.parent.mkdir(parents=True,exist_ok=True)
    write_csv(output_path,fields,ordered)
    errors,summary=validate(template_path,output_path,canonical_domains(taxonomy_path.read_text(encoding="utf-8")),require_complete)
    report={"summary":summary,"errors":errors,"batch_count":len(batch_defs),"batch_files":sorted(seen_files),"automatic_adjudication":False,"source_staging_mutation":False,"training_approval":False}
    if report_path:
        report_path.parent.mkdir(parents=True,exist_ok=True)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if errors:
        output_path.unlink(missing_ok=True)
        raise ValueError("merged review failed validation: "+"; ".join(errors[:10]))
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest="command",required=True)
    s=sub.add_parser("split");s.add_argument("--template",type=Path,required=True);s.add_argument("--out-dir",type=Path,required=True);s.add_argument("--batch-size",type=int,default=10)
    m=sub.add_parser("merge");m.add_argument("--template",type=Path,required=True);m.add_argument("--manifest",type=Path,required=True);m.add_argument("--batch-dir",type=Path,required=True);m.add_argument("--output",type=Path,required=True);m.add_argument("--taxonomy",type=Path,required=True);m.add_argument("--json-report",type=Path);m.add_argument("--require-complete",action="store_true")
    a=p.parse_args()
    try:
        if a.command=="split": result=split(a.template,a.out_dir,a.batch_size)
        else: result=merge(a.template,a.manifest,a.batch_dir,a.output,a.taxonomy,a.json_report,a.require_complete)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,csv.Error,json.JSONDecodeError) as e:
        print(f"TAXONOMY REVIEW BATCH FAILED: {e}",file=sys.stderr);return 1
if __name__=="__main__": raise SystemExit(main())
