#!/usr/bin/env python3
"""Build descriptive taxonomy coverage metrics without modifying staging records."""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

REGISTERS = ("colloquial", "neutral", "formal", "mixed")
LANGUAGES = ("fa", "fa-en", "multilingual")
BANDS = ((0, 0, "absent"), (1, 4, "1-4"), (5, 9, "5-9"), (10, 10**9, "10+"))

def canonical_domains(text: str) -> list[str]:
    section = text.split("## Canonical primary domains", 1)
    if len(section) != 2:
        raise ValueError("taxonomy document lacks Canonical primary domains section")
    section = section[1].split("\n## ", 1)[0]
    found = re.findall(r"\|\s*`([a-z][a-z0-9_]*)`\s*\|", section)
    if not found or len(found) != len(set(found)):
        raise ValueError("could not parse unique canonical domains from taxonomy table")
    return found

def load_active(paths: list[Path]) -> list[dict]:
    rows=[]
    for path in paths:
        if "identity" in path.name.lower():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip(): continue
            row=json.loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("sample_id"), str):
                raise ValueError(f"{path}:{n}: invalid record or missing sample_id")
            row["_source_file"]=str(path)
            rows.append(row)
    ids=[r["sample_id"] for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate sample_id across supplied staging files")
    superseded={r.get("metadata",{}).get("supersedes_sample_id") for r in rows if isinstance(r.get("metadata"),dict) and r["metadata"].get("supersedes_sample_id")}
    missing=superseded-set(ids)
    if missing: raise ValueError(f"replacement references missing predecessor(s): {sorted(missing)}")
    return [r for r in rows if r["sample_id"] not in superseded]

def band(n: int) -> str:
    for low, high, label in BANDS:
        if low <= n <= high: return label
    raise AssertionError(n)

def count_values(rows, field, allowed):
    counts=Counter()
    invalid=[]
    for r in rows:
        value=r.get(field)
        if value in allowed: counts[value]+=1
        else: invalid.append({"sample_id":r["sample_id"],"value":value})
    return {"counts":{v:counts[v] for v in allowed},"missing_or_invalid_count":len(invalid),"missing_or_invalid_samples":invalid}

def build_report(rows: list[dict], domains: list[str]) -> dict:
    domain_counts=Counter()
    subskills=Counter()
    missing_subskill=[]
    invalid_domains=[]
    for r in rows:
        d=r.get("domain")
        if d in domains: domain_counts[d]+=1
        else: invalid_domains.append({"sample_id":r["sample_id"],"value":d})
        ss=r.get("subskills")
        if not isinstance(ss,list) or not ss:
            missing_subskill.append(r["sample_id"])
        else:
            for s in set(x for x in ss if isinstance(x,str) and x.strip()): subskills[s]+=1
    domain_rows=[{"domain":d,"count":domain_counts[d],"triage_band":band(domain_counts[d])} for d in domains]
    status=Counter()
    message_counts=Counter()
    user_turns=Counter()
    assistant_turns=Counter()
    for r in rows:
        q=r.get("quality")
        status[(q.get("review_status") if isinstance(q,dict) else None) or "missing_or_invalid"]+=1
        msgs=r.get("messages") if isinstance(r.get("messages"),list) else []
        message_counts[len(msgs)]+=1
        user_turns[sum(isinstance(m,dict) and m.get("role")=="user" for m in msgs)]+=1
        assistant_turns[sum(isinstance(m,dict) and m.get("role")=="assistant" for m in msgs)]+=1
    return {
      "purpose":"descriptive_taxonomy_coverage_audit_only",
      "active_record_count":len(rows),
      "excluded_identity_track":True,"superseded_predecessors_excluded":True,
      "canonical_domain_count":len(domains),
      "domain_coverage":domain_rows,
      "subskill_counts":dict(sorted(subskills.items())),
      "subskill_missing_record_count":len(missing_subskill),
      "subskill_missing_sample_ids":missing_subskill,
      "invalid_domain_count":len(invalid_domains),"invalid_domain_samples":invalid_domains,
      "register":count_values(rows,"register",REGISTERS),
      "language":count_values(rows,"language",LANGUAGES),
      "review_status_counts":dict(sorted(status.items())),
      "message_count_distribution":{str(k):message_counts[k] for k in sorted(message_counts)},
      "user_turn_count_distribution":{str(k):user_turns[k] for k in sorted(user_turns)},
      "assistant_turn_count_distribution":{str(k):assistant_turns[k] for k in sorted(assistant_turns)},
      "triage_band_policy":{"absent":"0 records","1-4":"1 to 4 records","5-9":"5 to 9 records","10+":"10 or more records","warning":"Descriptive workload bands only; not evidence of quality or statistical sufficiency."},
      "interpretation_limits":["Counts describe metadata coverage, not linguistic quality, correctness, diversity, or training value.","Subskill counts count records containing a label, not total label occurrences.","No records were relabeled or modified.","No semantic family IDs or final splits were assigned.","No training approval is granted."],
      "automatic_relabeling":False,"automatic_family_assignment":False,"automatic_split_assignment":False,"training_approval":False
    }

def render_markdown(report: dict) -> str:
    lines=["# Persian Taxonomy Coverage Report V1","",
      f"- Active general records: **{report['active_record_count']}**",
      f"- Canonical primary domains: **{report['canonical_domain_count']}**",
      f"- Records with missing/invalid subskills: **{report['subskill_missing_record_count']}**",
      f"- Records with invalid/missing primary domain: **{report['invalid_domain_count']}**","",
      "## Primary-domain coverage","","| Domain | Records | Triage band |","|---|---:|---|"]
    for x in report["domain_coverage"]: lines.append(f"| `{x['domain']}` | {x['count']} | {x['triage_band']} |")
    lines += ["","## Subskill coverage","","| Subskill | Records |","|---|---:|"]
    for k,v in report["subskill_counts"].items(): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Register coverage","","| Register | Records |","|---|---:|"]
    for k,v in report["register"]["counts"].items(): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Language coverage","","| Language | Records |","|---|---:|"]
    for k,v in report["language"]["counts"].items(): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Review status","","| Status | Records |","|---|---:|"]
    for k,v in report["review_status_counts"].items(): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Interpretation and guardrails","",
      "The triage bands are descriptive counts, not quality thresholds or claims of statistical sufficiency. An absent or low-count domain is a candidate for human review and targeted generation, not proof that existing samples are poor.",
      "Subskill frequencies count the number of records carrying each label. They do not measure the quality or depth with which a skill is demonstrated.",
      "This report does not change staging data, normalize metadata, assign semantic families or final splits, or approve training.","",
      "### Suggested next review actions","",
      "1. Inspect low-count and absent domains against the intended skill coverage before generating more samples.",
      "2. Review subskill labels for synonymous naming and inconsistent granularity; do not mass-rename historical records.",
      "3. Compare register and language counts with the intended user population and task mix.",
      "4. Prioritize human linguistic review of samples; metadata balance alone cannot establish Persian naturalness."]
    return "\n".join(lines)+"\n"

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--taxonomy",required=True,type=Path)
    p.add_argument("--json-output",required=True,type=Path)
    p.add_argument("--markdown-output",required=True,type=Path)
    p.add_argument("files",nargs="+",type=Path)
    a=p.parse_args()
    if a.json_output.exists() or a.markdown_output.exists(): p.error("refusing to overwrite existing outputs")
    try:
        domains=canonical_domains(a.taxonomy.read_text(encoding="utf-8"))
        rows=load_active(a.files)
        report=build_report(rows,domains)
        a.json_output.parent.mkdir(parents=True,exist_ok=True)
        a.json_output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        a.markdown_output.write_text(render_markdown(report),encoding="utf-8")
    except (OSError,json.JSONDecodeError,ValueError) as e:
        p.exit(1,f"TAXONOMY COVERAGE REPORT FAILED: {e}\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("subskill_counts","domain_coverage")},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
