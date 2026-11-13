#!/usr/bin/env python3
"""Create a human-only proposal for mapping historical domain labels to Taxonomy V2."""
from __future__ import annotations
import argparse, csv, json, re, sys
from collections import Counter
from pathlib import Path

PROPOSALS = {
 "implicit_intent": ("intent_understanding","high","Direct synonym: implied user intent."),
 "contextual_understanding": ("context_continuity","high","Historical label describes retaining and interpreting conversational context; inspect each sample for primary behavior."),
 "contextual_comprehension": ("context_continuity","high","Context interpretation is the closest canonical behavior."),
 "ambiguity_resolution": ("ambiguity_handling","high","Directly concerns resolving material ambiguity."),
 "clarification_precision": ("ambiguity_handling","medium","Likely focused clarification; verify that ambiguity rather than intent inference is primary."),
 "colloquial_persian": ("colloquial_noisy_input","medium","Likely informal Persian input/output; verify whether the example is about noisy input or simply fluent colloquial output."),
 "noisy_persian": ("colloquial_noisy_input","high","Noisy spelling and informal input are in this canonical scope."),
 "multi_turn_reasoning": ("","requires_record_level_review","Could describe multi_turn_planning, context_continuity, or explanation_reasoning; label alone is insufficient."),
 "emotional_intelligence": ("","requires_record_level_review","Could be emotional_support or pragmatics_tone; inspect the actual conversational behavior."),
 "pragmatics": ("pragmatics_tone","high","Direct semantic match to the canonical pragmatics/tone domain."),
 "reasoning": ("explanation_reasoning","medium","Reasoning is broad; verify that explanation or practical reasoning is the main trained behavior."),
 "reasoning_explanation": ("explanation_reasoning","high","Direct semantic match."),
 "translation_and_rewriting": ("","requires_record_level_review","Could be persian_fluency or sentence_construction depending on whether translation naturalness or rewriting is central."),
 "professional_writing": ("adaptive_communication","high","Professional audience/register adaptation is in the canonical scope."),
 "topic_management": ("","requires_record_level_review","Could be context_continuity or multi_turn_planning; inspect turn progression."),
 "self_correction": ("correction_recovery","high","Self-correction is a correction/recovery behavior."),
 "idiomatic_persian": ("persian_fluency","high","Idiomatic wording is explicitly in the canonical fluency scope."),
 "natural_sentence_construction": ("sentence_construction","high","Direct match to natural sentence construction."),
 "register_adaptation": ("adaptive_communication","high","Register and audience adaptation are canonical adaptive communication."),
 "conversational_fluency": ("","requires_record_level_review","Could be everyday_dialogue or persian_fluency; distinguish social interaction from linguistic fluency."),
 "natural_rewrite": ("sentence_construction","medium","Likely rewriting/sentence construction; verify the target behavior."),
 "writing_quality": ("","requires_record_level_review","Too broad: may concern sentence construction, fluency, or adaptive professional writing."),
 "tone_adaptation": ("","requires_record_level_review","Could be adaptive_communication or pragmatics_tone depending on whether audience/register or social subtext is central."),
 "formal_persian": ("","requires_record_level_review","Could be persian_fluency or adaptive_communication; formal register alone is not enough to determine the primary behavior."),
 "explanation_style": ("explanation_reasoning","medium","Likely explanation quality; verify reasoning/explanation is the main task."),
 "multi_turn_style_control": ("adaptive_communication","medium","Likely maintaining style across turns; verify register adaptation is primary."),
 "persian_style": ("","requires_record_level_review","Too broad to map safely without inspecting the sample."),
 "semantic_precision": ("lexical_precision","medium","Likely lexical/semantic distinctions; inspect whether ambiguity handling is instead primary."),
 "conversation_repair": ("correction_recovery","medium","Likely repair after conversational error; verify whether correction or context continuity is central."),
 "collocation_quality": ("lexical_precision","high","Collocation choice is explicitly within lexical precision."),
 "response_quality": ("","requires_record_level_review","Non-specific quality label has no one-to-one canonical domain; decide from each record's target behavior."),
 "multilingual_persian": ("","requires_record_level_review","Language composition belongs in the language field; determine the primary behavior from the actual sample."),
 "conversation_coherence": ("","requires_record_level_review","Could be context_continuity or sentence_construction; inspect whether cross-turn continuity or within-text cohesion is central."),
 "register_style": ("adaptive_communication","medium","Likely register/style adaptation; verify the audience and style behavior."),
}
def canonical_domains(text):
    section=text.split("## Canonical primary domains",1)
    if len(section)!=2: raise ValueError("taxonomy canonical-domain section not found")
    section=section[1].split("\n## ",1)[0]
    found=re.findall(r"\|\s*`([a-z][a-z0-9_]*)`\s*\|",section)
    if not found or len(found)!=len(set(found)): raise ValueError("could not parse canonical domains")
    return set(found)
def collect(paths, canonical):
    rows=[]
    for path in paths:
        if "identity" in path.name.lower(): continue
        for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip(): continue
            r=json.loads(line)
            if not isinstance(r,dict) or not isinstance(r.get("sample_id"),str): raise ValueError(f"{path}:{n}: invalid sample")
            rows.append(r)
    ids=[r["sample_id"] for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate sample IDs")
    superseded={r.get("metadata",{}).get("supersedes_sample_id") for r in rows if isinstance(r.get("metadata"),dict) and r["metadata"].get("supersedes_sample_id")}
    if superseded-set(ids): raise ValueError("replacement references missing predecessor")
    active=[r for r in rows if r["sample_id"] not in superseded]
    unknown=sorted({r.get("domain") for r in active if r.get("domain") not in canonical and isinstance(r.get("domain"),str)})
    missing=sum(not isinstance(r.get("domain"),str) or not r.get("domain") for r in active)
    return active,unknown,missing
def build(active, labels, canonical):
    counts=Counter(r.get("domain") for r in active)
    out=[]
    for label in labels:
        if label in canonical: continue
        suggestion,confidence,rationale=PROPOSALS.get(label,("","requires_record_level_review","No defensible label-level mapping is defined; inspect individual samples."))
        if suggestion and suggestion not in canonical: raise ValueError(f"proposal for {label} is not canonical")
        out.append({"legacy_domain":label,"active_record_count":counts[label],"suggested_canonical_domain":suggestion,"confidence":confidence,"rationale":rationale,"decision":"pending_human_review","reviewer":"","review_date":"","adjudication_rationale":""})
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--taxonomy",required=True,type=Path); p.add_argument("--output",required=True,type=Path); p.add_argument("files",nargs="+",type=Path)
    a=p.parse_args()
    if a.output.exists(): p.error("refusing to overwrite existing output")
    try:
        canonical=canonical_domains(a.taxonomy.read_text(encoding="utf-8"))
        active,labels,missing=collect(a.files,canonical)
        rows=build(active,labels,canonical)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["legacy_domain","active_record_count","suggested_canonical_domain","confidence","rationale","decision","reviewer","review_date","adjudication_rationale"])
            w.writeheader(); w.writerows(rows)
        print(json.dumps({"active_general_records":len(active),"legacy_domain_label_count":len(labels),"legacy_records_in_scope":sum(x["active_record_count"] for x in rows),"missing_or_invalid_domain_records":missing,"labels_requiring_record_level_review":sum(x["confidence"]=="requires_record_level_review" for x in rows),"automatic_mapping":False,"staging_mutation":False,"family_assignment":False,"split_assignment":False,"training_approval":False},ensure_ascii=False,indent=2))
    except (OSError,ValueError,json.JSONDecodeError) as e: p.exit(1,f"LEGACY MAPPING PACKET FAILED: {e}\n")
if __name__=="__main__": main()
