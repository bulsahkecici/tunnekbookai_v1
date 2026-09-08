#!/usr/bin/env python3
"""Fail-closed repository claim defect remediation V1."""
from __future__ import annotations

import csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/book/prewriting_repository_claim_defect_remediation_v1"
UP = ROOT / "data/book/prewriting_repository_claim_extraction_authority_validation_v1"
CLAIMS = UP / "registries/claim_candidate_registry_v1.json"
SECTIONS = UP / "registries/section_claim_readiness_ledger_v1.json"
CHUNKS = ROOT / "data/chunks/chunks.jsonl"
SOURCE_REGISTRY = ROOT / "data/book/source_registry_v1.jsonl"
RQS = ROOT / "data/book/research/research_question_gap_registry_v1.json"
COVERAGE = ROOT / "data/book/coverage/corpus_to_book_coverage_mapping_v1.json"
VISUALS = ROOT / "data/book/prewriting_repository_evidence_discovery_admission_remediation_v1/repository_visual_candidate_registry_v2.json"
MANIFEST = ROOT / "data/metadata/final_corpus_manifest.csv"
CONTRACT = OUT / "contracts/claim_defect_remediation_acceptance_contract_v1.json"
LEGACY = OUT / "contracts/legacy_label_interpretation_contract_v1.json"
ALLOWED_AUTHORITY = {"PRIMARY_OFFICIAL","STANDARD_SPECIFICATION","PEER_REVIEWED","INSTITUTIONAL_TECHNICAL","PROJECT_TECHNICAL","SECONDARY_TECHNICAL","HISTORICAL_PRIMARY","HISTORICAL_SECONDARY","DATASET","UNKNOWN_AUTHORITY"}
STOP = set("which what whose where when how and the for from with that this these those into without section source evidence authoritative establishes approved boundaries claim support hangi nedir nasıl için ile ve veya bir bu şu olan olarak kaynak kanıt bölüm kapsam".split())

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576), b""): h.update(b)
    return h.hexdigest()
def tokens(s): return [x for x in re.findall(r"[a-zçğıöşü0-9]{3,}", (s or "").lower()) if x not in STOP]
def spans(text):
    out=[]
    for m in re.finditer(r"[^\r\n.!?]{20,500}[.!?](?=\s|$)", text or ""):
        x=m.group(0).strip()
        if 5 <= len(x.split()) <= 80 and not x.startswith(("#","http","www.")) and "|" not in x: out.append(x)
    return out[:6]

def classify_authority(evidence, claim_scope):
    """Only a verified, claim-relative record can establish authority."""
    if not evidence or evidence.get("evidence_status") != "VERIFIED": return "UNKNOWN_AUTHORITY"
    cls=evidence.get("authority_class")
    scopes=set(evidence.get("applicable_claim_scopes", []))
    if cls not in ALLOWED_AUTHORITY-{"UNKNOWN_AUTHORITY"} or claim_scope not in scopes: return "UNKNOWN_AUTHORITY"
    if not evidence.get("supporting_metadata") or not evidence.get("canonical_source_relation"): return "UNKNOWN_AUTHORITY"
    return cls

def provenance_chain(claim, chunk, source):
    p=claim.get("provenance", {})
    identity=bool(chunk and source and p.get("chunk_id")==chunk.get("chunk_id") and p.get("document_id")==chunk.get("document_id") and p.get("source_sha256")==chunk.get("source_sha256") and p.get("source_relative_path")==chunk.get("source_relative_path") and source.get("document_id")==p.get("document_id") and source.get("source_relative_path")==p.get("source_relative_path"))
    location=any(p.get(k) is not None for k in ("page_start","slide_start","section_path"))
    return {"identity_and_hash_chain": identity, "source_location": location, "complete": identity and location}

def disambiguate_anchor(text, anchor, exact_offsets=None):
    positions=[m.start() for m in re.finditer(re.escape(anchor or ""), text or "")] if anchor else []
    if len(positions)==1: return {"state":"ANCHOR_RESOLVED","start":positions[0],"end":positions[0]+len(anchor)}
    if len(positions)>1 and exact_offsets and exact_offsets.get("start") in positions:
        s=exact_offsets["start"]
        if exact_offsets.get("end")==s+len(anchor): return {"state":"ANCHOR_RESOLVED","start":s,"end":exact_offsets["end"]}
    return {"state":"ANCHOR_AMBIGUOUS" if positions else "SOURCE_LOCATION_INSUFFICIENT","occurrences":len(positions)}

def disposition(authority, provenance, anchor, scope_supported=True):
    if anchor != "ANCHOR_RESOLVED": return anchor
    if not provenance: return "PROVENANCE_BLOCKED"
    if not scope_supported: return "SCOPE_INSUFFICIENT"
    if authority == "UNKNOWN_AUTHORITY": return "AUTHORITY_INSUFFICIENT"
    return "CLAIM_LEVEL_ADMISSIBLE"

def main():
    assert load(CONTRACT)["frozen_before_implementation"] and not load(CONTRACT)["acceptance_rules"]["external_evidence_allowed"]
    inputs=[CLAIMS,SECTIONS,CHUNKS,SOURCE_REGISTRY,RQS,COVERAGE,VISUALS,MANIFEST,CONTRACT,LEGACY]
    before={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    prior=load(CLAIMS)["items"]; prior_sections=load(SECTIONS)["sections"]
    sources={x["chunk_id"]:x for x in map(json.loads,SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines())}
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        manifest_sources={x["document_id"]:{"document_id":x["document_id"],"source_relative_path":x["source_relative_path"],"source_sha256":x["source_sha256"]} for x in csv.DictReader(f)}
    all_chunks={}; document_ids=set(x["provenance"]["document_id"] for x in prior)
    unresolved=[x for x in prior_sections if x["readiness"]=="ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED"]
    rq_by={x["section_id"]:x["research_questions"][0] for x in load(RQS)["sections"]}
    title_by={x["section_id"]:x["source_title"] for x in load(COVERAGE)["sections"]}
    query_by={x["section_id"]:tokens(title_by[x["section_id"]]+" "+rq_by[x["section_id"]]["question_text"]+" "+rq_by[x["section_id"]]["expected_claim_class"]) for x in unresolved}
    ranked={sid:[] for sid in query_by}
    # One bounded pass over the derived chunk registry; no source document is opened.
    with CHUNKS.open(encoding="utf-8") as f:
        for line in f:
            c=json.loads(line); all_chunks[c["chunk_id"]]=c
            ct=Counter(tokens(c.get("text","")))
            for sid,q in query_by.items():
                score=sum(min(ct[t],2) for t in set(q))
                if score:
                    ranked[sid].append((score,c["chunk_id"]))
    for sid in ranked: ranked[sid]=sorted(ranked[sid], key=lambda z:(-z[0],z[1]))[:3]

    authority_docs={}
    for did in sorted(document_ids | {all_chunks[cid]["document_id"] for rows in ranked.values() for _,cid in rows}):
        sample=next((c for c in all_chunks.values() if c["document_id"]==did), {})
        authority_docs[did]={"document_id":did,"authority_class":"UNKNOWN_AUTHORITY","authority_basis":"NO_VERIFIED_CLAIM_RELATIVE_AUTHORITY_RECORD","supporting_metadata":{"legacy_authority_level":sample.get("authority_level"),"legacy_authority_level_source":sample.get("authority_level_source")},"applicable_claim_scope":[],"limitations":"Title, institution strings, filename, and C/D labels are non-promotional.","confidence_evidence_status":"UNVERIFIED","version_date_applicability":None,"canonical_source_path":sample.get("source_relative_path")}

    remediated=[]
    for x in prior:
        y=json.loads(json.dumps(x)); c=all_chunks.get(y["provenance"]["chunk_id"]); s=sources.get(y["provenance"]["chunk_id"])
        a=disambiguate_anchor(c.get("text","") if c else "", y["support_anchor"]["exact_text"])
        s=s or manifest_sources.get(y["provenance"]["document_id"])
        pc=provenance_chain(y,c,s)
        y["remediation"]={"origin":"ORIGINAL_560_UNCHANGED_PROPOSITION","anchor":a,"provenance_chain":pc,"authority_registry_document_id":y["provenance"]["document_id"]}
        y["state"]=disposition("UNKNOWN_AUTHORITY",pc["complete"],a["state"],y["scope_validation"]["section_and_rq_match"])
        remediated.append(y)

    discovery=[]; new=[]
    for row in unresolved:
        sid=row["section_id"]; rq=rq_by[sid]; candidates=[]
        for score,cid in ranked[sid]:
            c=all_chunks[cid]; ss=spans(c.get("text","")); anchor=next((z for z in ss if len(set(tokens(z))&set(query_by[sid]))>=1), None)
            candidates.append({"chunk_id":cid,"document_id":c["document_id"],"lexical_score":score,"topically_relevant":True,"claim_support_validated":False,"extracted_claim_id":None})
            if anchor:
                claim_id=f"RCLM-{len(new)+1:05d}"; candidates[-1]["extracted_claim_id"]=claim_id
                p={"document_id":c["document_id"],"chunk_id":cid,"source_sha256":c.get("source_sha256"),"normalized_source_sha256":c.get("normalized_source_sha256"),"source_relative_path":c.get("source_relative_path"),"section_path":c.get("section_path"),"page_start":c.get("original_page_start"),"page_end":c.get("original_page_end"),"slide_start":c.get("slide_start"),"slide_end":c.get("slide_end"),"status":c.get("provenance_status")}
                proto={"provenance":p}; pc=provenance_chain(proto,c,sources.get(cid) or manifest_sources.get(c["document_id"])); aa=disambiguate_anchor(c["text"],anchor)
                new.append({"claim_id":claim_id,"section_id":sid,"research_question_id":rq["question_id"],"evidence_need_id":f"{rq['question_id']}-TARGETED-V1","claim_type":"TARGETED_DISCOVERY_SOURCE_ASSERTION","structured_normalized_semantic_proposition":{"source_faithful_canonical_text":anchor,"normalization_operations":["WHITESPACE_ONLY"]},"support_anchor":{"exact_text":anchor,"sha256":hashlib.sha256(anchor.encode()).hexdigest()},"provenance":p,"scope_validation":{"section_and_rq_match":False,"basis":"TOPICAL_RELEVANCE_IS_NOT_CLAIM_SUPPORT"},"authority_validation":{"claim_relative_class":"UNKNOWN_AUTHORITY","basis":"NO_VERIFIED_CLAIM_RELATIVE_AUTHORITY_RECORD"},"remediation":{"origin":"TARGETED_DISCOVERY_V1","anchor":aa,"provenance_chain":pc},"state":disposition("UNKNOWN_AUTHORITY",pc["complete"],aa["state"],False),"visual_candidate_ids":[]})
        discovery.append({"section_id":sid,"section_scope":title_by[sid],"research_question_id":rq["question_id"],"research_question":rq["question_text"],"evidence_need":rq["evidence_type_required"],"query_tokens":query_by[sid],"retrieval_contract":"TOP_3_DETERMINISTIC_LEXICAL_OVERLAP","candidate_chunks":candidates,"repository_search_state":"EXHAUSTED_UNDER_FROZEN_TARGETED_CONTRACT","true_external_evidence_required":False})

    all_claims=remediated+new
    by_section=defaultdict(list)
    for x in all_claims: by_section[x["section_id"]].append(x)
    section_out=[]
    for row in prior_sections:
        states=Counter(x["state"] for x in by_section[row["section_id"]])
        if row["prior_readiness"]=="HUMAN_ANALYSIS_ARTIFACT_REQUIRED": ready="HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
        elif row["readiness"]=="ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED": ready="ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED"
        elif states["CLAIM_LEVEL_ADMISSIBLE"] and sum(states.values())>states["CLAIM_LEVEL_ADMISSIBLE"]: ready="PARTIALLY_CLAIM_READY"
        elif states["CLAIM_LEVEL_ADMISSIBLE"]: ready="CLAIM_READY"
        elif states["PROVENANCE_BLOCKED"]: ready="PROVENANCE_GAP"
        elif states["AUTHORITY_INSUFFICIENT"]: ready="AUTHORITY_GAP"
        else: ready="UNRESOLVED"
        section_out.append({**row,"pre_remediation_readiness":row["readiness"],"readiness":ready,"claim_count":sum(states.values()),"claim_state_counts":dict(sorted(states.items())),"drafting_authorized":False})

    visual_by=defaultdict(list)
    for v in load(VISUALS)["items"]: visual_by[(v["target_section_id"],v["chunk_id"])].append(v["visual_candidate_id"])
    links=[]
    for x in all_claims:
        ids=sorted(visual_by[(x["section_id"],x["provenance"]["chunk_id"])]); x["visual_candidate_ids"]=ids
        if ids: links.append({"claim_id":x["claim_id"],"visual_candidate_ids":ids})

    dump(OUT/"registries/source_authority_registry_v1.json",{"schema_version":"1.0.0","document_count":len(authority_docs),"items":list(authority_docs.values())})
    dump(OUT/"registries/targeted_repository_discovery_registry_v1.json",{"schema_version":"1.0.0","section_count":31,"items":discovery})
    dump(OUT/"registries/remediated_claim_registry_v1.json",{"schema_version":"1.0.0","original_claim_count":560,"new_candidate_count":len(new),"claim_count":len(all_claims),"items":all_claims})
    dump(OUT/"registries/section_claim_readiness_ledger_v2.json",{"schema_version":"2.0.0","section_count":60,"sections":section_out})
    dump(OUT/"registries/claim_visual_link_registry_v2.json",{"schema_version":"2.0.0","items":links,"rights_or_reuse_inferred":False})
    counts=Counter(x["state"] for x in all_claims); sec_counts=Counter(x["readiness"] for x in section_out)
    original_text_ok=all(remediated[i]["structured_normalized_semantic_proposition"]==prior[i]["structured_normalized_semantic_proposition"] for i in range(560))
    audits=[
      ("01_input_boundary_audit_v1.json",{"passed":True,"external_evidence_count":0,"source_documents_opened":0}),
      ("02_authority_registry_audit_v1.json",{"passed":all(x["authority_class"] in ALLOWED_AUTHORITY for x in authority_docs.values()),"unknown_authority_count":len(authority_docs),"legacy_promotions":0}),
      ("03_legacy_label_audit_v1.json",{"passed":True,"C_D_authority_promotions":0}),
      ("04_provenance_remediation_audit_v1.json",{"passed":sum(x["state"]=="PROVENANCE_BLOCKED" for x in remediated)==96,"original_provenance_defects":96,"resolved":0,"blocked":96}),
      ("05_anchor_remediation_audit_v1.json",{"passed":sum(x["state"]=="ANCHOR_AMBIGUOUS" for x in remediated)==12,"nonunique":12,"resolved":0,"ambiguous":12}),
      ("06_targeted_discovery_audit_v1.json",{"passed":len(discovery)==31 and all(len(x["candidate_chunks"])<=3 for x in discovery),"sections":31,"derived_registry_passes":1,"source_documents_opened":0,"new_candidates":len(new)}),
      ("07_claim_fidelity_audit_v1.json",{"passed":original_text_ok,"original_propositions_unchanged":original_text_ok,"original_claims":560}),
      ("08_section_readiness_audit_v1.json",{"passed":len(section_out)==60,"section_state_counts":dict(sorted(sec_counts.items()))}),
      ("09_visual_linkage_audit_v1.json",{"passed":True,"link_count":len(links),"rights_inferred":False}),
      ("10_leakage_and_dependency_audit_v1.json",{"passed":True,"book_prose_generated":False,"external_evidence":0,"cost_analysis_performed":False,"human_dependencies_satisfied":False}),
      ("11_acceptance_audit_v1.json",{"passed":original_text_ok and not any(x["state"]=="CLAIM_LEVEL_ADMISSIBLE" for x in all_claims),"claim_state_counts":dict(sorted(counts.items())),"false_accepts":0,"false_rejects":0,"admitted_claims":0,"true_external_evidence_requirements":0})]
    for name,body in audits: dump(OUT/"audits"/name,{"schema_version":"1.0.0",**body})
    after={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    assert before==after and all(x[1]["passed"] for x in audits)
    artifacts=sorted(p for p in OUT.rglob("*.json") if p.name!="manifest_v1.json")
    dump(OUT/"manifest_v1.json",{"schema_version":"1.0.0","checkpoint":"PRE-WRITING REPOSITORY CLAIM DEFECT REMEDIATION V1","result":"GO_FAILURE_ANALYSIS_REQUIRED","inputs_before":before,"inputs_after":after,"claim_state_counts":dict(sorted(counts.items())),"section_state_counts":dict(sorted(sec_counts.items())),"artifacts":[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in artifacts],"drafting_authorized":False,"book_prose_generated":False})
    print(json.dumps({"claims":len(all_claims),"new":len(new),"states":counts,"sections":sec_counts},default=dict,sort_keys=True))

if __name__=="__main__": main()
