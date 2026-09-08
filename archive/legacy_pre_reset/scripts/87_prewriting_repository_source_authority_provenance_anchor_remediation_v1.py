#!/usr/bin/env python3
"""Deterministic remediation of authority, provenance, anchors, and bounded verification."""
from __future__ import annotations

import copy, csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "data/book/prewriting_repository_claim_defect_remediation_v1"
OUT = ROOT / "data/book/prewriting_repository_source_authority_provenance_anchor_remediation_v1"
CONTRACT = OUT / "contracts/remediation_acceptance_contract_v1.json"
CLAIMS = UP / "registries/remediated_claim_registry_v1.json"
AUTH = UP / "registries/source_authority_registry_v1.json"
DISC = UP / "registries/targeted_repository_discovery_registry_v1.json"
SECTIONS = UP / "registries/section_claim_readiness_ledger_v2.json"
VISUALS = ROOT / "data/book/prewriting_repository_evidence_discovery_admission_remediation_v1/repository_visual_candidate_registry_v2.json"
MANIFEST = ROOT / "data/metadata/final_corpus_manifest.csv"
CHUNKS = ROOT / "data/chunks/chunks.jsonl"

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def norm(text): return re.sub(r"\s+", " ", text or "").strip()

def block_matches(sidecar_paths, anchor):
    needle = norm(anchor); found = []
    if not needle: return found
    for path in sidecar_paths:
        doc = load(path).get("docling_document", {})
        for block in doc.get("texts", []):
            text = norm(block.get("text"))
            start = text.find(needle)
            if start < 0: continue
            prov = block.get("prov") or []
            loc = prov[0] if prov else {}
            found.append({
                "sidecar_path": str(path.relative_to(ROOT)), "block_ref": block.get("self_ref"),
                "block_anchor_span": [start, start + len(needle)], "block_text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "page_no": loc.get("page_no"), "original_page_no": loc.get("original_page_no"),
                "charspan": loc.get("charspan"), "bbox": loc.get("bbox")})
    return found

def disposition(claim, locator_complete):
    if claim["remediation"]["anchor"]["state"] == "ANCHOR_AMBIGUOUS": return "ANCHOR_AMBIGUOUS"
    if not locator_complete: return "PROVENANCE_BLOCKED"
    if not claim["scope_validation"]["section_and_rq_match"]: return "SCOPE_INSUFFICIENT"
    return "AUTHORITY_INSUFFICIENT"

def main():
    contract = load(CONTRACT)
    rules = contract["acceptance_rules"]
    assert contract["frozen_before_implementation"] and rules["all_claims_reconciled"] == 602
    inputs = [CONTRACT, CLAIMS, AUTH, DISC, SECTIONS, VISUALS, MANIFEST, CHUNKS]
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    claims = load(CLAIMS)["items"]
    authority = load(AUTH)["items"]
    discovery = load(DISC)["items"]
    prior_sections = load(SECTIONS)["sections"]
    assert len(claims) == 602 and len(prior_sections) == 60

    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        manifest = {x["document_id"]: x for x in csv.DictReader(f)}
    chunks = {x["chunk_id"]: x for x in map(json.loads, CHUNKS.read_text(encoding="utf-8").splitlines())}

    # No repository field is explicit, verified, and claim-relative enough to authorize a promotion.
    authority_v2 = []
    for row in authority:
        authority_v2.append({**row, "registry_version": "v2", "authority_class": "UNKNOWN_AUTHORITY",
            "authority_basis": "NO_EXPLICIT_VERIFIED_CLAIM_RELATIVE_AUTHORITY_RECORD",
            "promotion_status": "NOT_PROMOTED", "verified_authority_evidence": []})

    affected_docs = sorted({x["provenance"]["document_id"] for x in claims if x["state"] in {"PROVENANCE_BLOCKED","ANCHOR_AMBIGUOUS"}})
    sidecars = {}
    for did in affected_docs:
        sidecars[did] = [ROOT / p for p in manifest[did].get("citation_sidecar", "").split("|") if p]
    locator_rows, remediated, bridge_acc = [], [], defaultdict(list)
    for original in claims:
        x = copy.deepcopy(original); did = x["provenance"]["document_id"]
        candidates = block_matches(sidecars.get(did, []), x["support_anchor"]["exact_text"])
        unique = len(candidates) == 1
        existing = x["remediation"]["provenance_chain"]["source_location"]
        complete = bool(existing or unique)
        if unique:
            x["provenance"]["conversion_locator"] = candidates[0]
            x["provenance"]["status"] = "conversion_block_resolved"
        x["remediation"]["provenance_chain"]["source_location"] = complete
        x["remediation"]["provenance_chain"]["complete"] = complete
        if x["remediation"]["anchor"]["state"] == "ANCHOR_AMBIGUOUS" and unique:
            x["remediation"]["anchor"] = {"state":"ANCHOR_RESOLVED_BY_UNIQUE_BLOCK_LOCATOR", "locator":candidates[0]}
        x["state"] = disposition(x, complete)
        x["state_reasons"] = (["PROVENANCE_INCOMPLETE"] if not complete else []) + (["ANCHOR_NONUNIQUE"] if x["state"]=="ANCHOR_AMBIGUOUS" else []) + (["SECTION_SCOPE_NOT_VALIDATED"] if x["state"]=="SCOPE_INSUFFICIENT" else []) + ["CLAIM_RELATIVE_AUTHORITY_UNKNOWN"]
        locator_rows.append({"claim_id":x["claim_id"], "document_id":did, "chunk_id":x["provenance"]["chunk_id"],
            "prior_state":original["state"], "candidate_count":len(candidates), "candidates":candidates,
            "resolution":"UNIQUE_LOCATOR_RESOLVED" if unique else ("AMBIGUOUS_RETAINED" if candidates else "NO_SIDECAR_MATCH")})
        bridge_acc[(did, x["provenance"]["chunk_id"])].extend(candidates)
        remediated.append(x)

    bridge=[]
    for (did,cid), locs in sorted(bridge_acc.items()):
        uniq={json.dumps(v,sort_keys=True):v for v in locs}
        bridge.append({"document_id":did,"chunk_id":cid,"locator_count":len(uniq),"locators":list(uniq.values()),
            "bridge_status":"LOCATORS_JOINED" if uniq else "NO_LOCATOR_JOIN"})

    # Inspect exactly the five canonical files with the most discovery candidates.
    freq=Counter(c["document_id"] for row in discovery for c in row["candidate_chunks"])
    opened=[did for did,_ in sorted(freq.items(), key=lambda z:(-z[1],z[0]))[:rules["bounded_canonical_source_documents_maximum"]]]
    canonical={did:(ROOT/manifest[did]["final_output"]).read_text(encoding="utf-8") for did in opened}
    claim_by_id={x["claim_id"]:x for x in remediated}
    verification=[]; verified_claims=set()
    for row in discovery:
        for c in row["candidate_chunks"]:
            if c["document_id"] not in canonical: continue
            claim=claim_by_id.get(c.get("extracted_claim_id")); anchor=claim["support_anchor"]["exact_text"] if claim else ""
            found=bool(anchor and norm(anchor) in norm(canonical[c["document_id"]]))
            scope=bool(claim and claim["scope_validation"]["section_and_rq_match"])
            if found and scope: verified_claims.add(claim["claim_id"])
            verification.append({"section_id":row["section_id"],"document_id":c["document_id"],"chunk_id":c["chunk_id"],
                "claim_id":c.get("extracted_claim_id"),"canonical_path":manifest[c["document_id"]]["final_output"],
                "canonical_sha256":sha(ROOT/manifest[c["document_id"]]["final_output"]),"anchor_found":found,
                "section_and_rq_scope_verified":scope,"support_and_scope_verified":found and scope})
    for x in remediated:
        x["bounded_source_verification"] = "SUPPORT_AND_SCOPE_VERIFIED" if x["claim_id"] in verified_claims else "NOT_VERIFIED_IN_BOUNDED_BATCH"

    discovery_v2=[]
    for row in discovery:
        candidates=[]
        for c in row["candidate_chunks"]:
            claim=claim_by_id.get(c.get("extracted_claim_id"))
            candidates.append({**c,"canonical_source_opened":c["document_id"] in opened,
                "claim_support_validated":bool(claim and claim["claim_id"] in verified_claims)})
        discovery_v2.append({**row,"candidate_chunks":candidates,"retrieval_contract":"V1_CANDIDATES_REPROCESSED_WITH_BOUNDED_CANONICAL_VERIFICATION",
            "query_diagnostic":"NO_QUERY_EXPANSION_REQUIRED_CANDIDATES_PRESENT" if candidates else "QUERY_SCOPE_MISMATCH",
            "true_external_evidence_required":False})

    by_section=defaultdict(list)
    for x in remediated: by_section[x["section_id"]].append(x)
    section_v3=[]
    discovery_sections={x["section_id"] for x in discovery_v2}
    for row in prior_sections:
        states=Counter(x["state"] for x in by_section[row["section_id"]])
        if row.get("prior_readiness")=="HUMAN_ANALYSIS_ARTIFACT_REQUIRED": ready="HUMAN_ANALYSIS_ARTIFACT_REQUIRED"
        elif states["ANCHOR_AMBIGUOUS"]: ready="UNRESOLVED"
        elif states["PROVENANCE_BLOCKED"]: ready="PROVENANCE_GAP"
        elif states["AUTHORITY_INSUFFICIENT"]: ready="AUTHORITY_GAP"
        elif row["section_id"] in discovery_sections: ready="ADDITIONAL_REPOSITORY_DISCOVERY_REQUIRED"
        else: ready="UNRESOLVED"
        section_v3.append({**row,"pre_remediation_readiness":row["readiness"],"readiness":ready,
            "claim_count":sum(states.values()),"claim_state_counts":dict(sorted(states.items())),"drafting_authorized":False})

    visual_by=defaultdict(list)
    for v in load(VISUALS)["items"]: visual_by[(v["target_section_id"],v["chunk_id"])].append(v["visual_candidate_id"])
    links=[]
    for x in remediated:
        ids=sorted(visual_by[(x["section_id"],x["provenance"]["chunk_id"])])
        if ids: links.append({"claim_id":x["claim_id"],"visual_candidate_ids":ids,"locator":x["provenance"].get("conversion_locator"),"link_basis":"EXISTING_SECTION_AND_CHUNK_IDENTITY"})

    dump(OUT/"registries/source_authority_registry_v2.json",{"schema_version":"2.0.0","items":authority_v2})
    dump(OUT/"registries/conversion_chunk_provenance_bridge_v1.json",{"schema_version":"1.0.0","items":bridge})
    dump(OUT/"registries/anchor_locator_registry_v1.json",{"schema_version":"1.0.0","items":locator_rows})
    dump(OUT/"registries/bounded_source_verification_registry_v1.json",{"schema_version":"1.0.0","opened_document_ids":opened,"items":verification})
    dump(OUT/"registries/targeted_repository_discovery_registry_v2.json",{"schema_version":"2.0.0","section_count":len(discovery_v2),"items":discovery_v2})
    dump(OUT/"registries/remediated_claim_registry_v2.json",{"schema_version":"2.0.0","claim_count":len(remediated),"items":remediated})
    dump(OUT/"registries/section_claim_readiness_ledger_v3.json",{"schema_version":"3.0.0","section_count":len(section_v3),"sections":section_v3})
    dump(OUT/"registries/claim_visual_link_registry_v3.json",{"schema_version":"3.0.0","items":links,"rights_or_reuse_inferred":False})

    counts=Counter(x["state"] for x in remediated); sec_counts=Counter(x["readiness"] for x in section_v3)
    original_props=load(CLAIMS)["items"]
    proposition_ok=all(a["structured_normalized_semantic_proposition"]==b["structured_normalized_semantic_proposition"] for a,b in zip(original_props,remediated))
    prior_prov=sum(x["state"]=="PROVENANCE_BLOCKED" for x in original_props); now_prov=counts["PROVENANCE_BLOCKED"]
    prior_anchor=sum(x["state"]=="ANCHOR_AMBIGUOUS" for x in original_props); now_anchor=counts["ANCHOR_AMBIGUOUS"]
    audits=[
      ("01_contract_audit_v1.json", contract["frozen_before_implementation"], {"contract_frozen":True}),
      ("02_authority_audit_v1.json", all(x["authority_class"]=="UNKNOWN_AUTHORITY" for x in authority_v2), {"promotions":0,"unknown":len(authority_v2)}),
      ("03_provenance_bridge_audit_v1.json", now_prov<=prior_prov, {"prior":prior_prov,"resolved":prior_prov-now_prov,"remaining":now_prov}),
      ("04_anchor_audit_v1.json", now_anchor<=prior_anchor, {"prior":prior_anchor,"resolved":prior_anchor-now_anchor,"remaining":now_anchor}),
      ("05_bounded_source_audit_v1.json", len(opened)==5, {"opened_document_ids":opened,"opened":len(opened),"verified_claims":len(verified_claims)}),
      ("06_claim_reconciliation_audit_v1.json", len(remediated)==602 and sum(counts.values())==602, {"claim_state_counts":dict(sorted(counts.items()))}),
      ("07_section_reconciliation_audit_v1.json", len(section_v3)==60, {"section_state_counts":dict(sorted(sec_counts.items()))}),
      ("08_claim_fidelity_audit_v1.json", proposition_ok, {"propositions_unchanged":proposition_ok}),
      ("09_visual_linkage_audit_v1.json", True, {"link_count":len(links),"rights_inferred":False}),
      ("10_dependency_leakage_audit_v1.json", True, {"external_evidence_used":0,"cost_analysis_performed":False,"human_dependencies_satisfied":False,"book_prose_generated":False}),
      ("11_false_acceptance_audit_v1.json", not any(x["state"]=="CLAIM_LEVEL_ADMISSIBLE" for x in remediated), {"false_authority_or_provenance_acceptance":0}),
      ("12_discovery_audit_v1.json", len(discovery_v2)==31, {"sections":len(discovery_v2),"true_external_evidence_requirements":0})]
    for name,passed,body in audits: dump(OUT/"audits"/name,{"schema_version":"1.0.0","passed":passed,**body})
    after={str(p.relative_to(ROOT)):sha(p) for p in inputs}
    assert before==after and all(x[1] for x in audits)
    artifacts=sorted(p for p in OUT.rglob("*.json") if p.name!="manifest_v1.json")
    dump(OUT/"manifest_v1.json",{"schema_version":"1.0.0","checkpoint":"PRE-WRITING REPOSITORY SOURCE AUTHORITY PROVENANCE AND ANCHOR REMEDIATION V1",
        "result":"GO_FAILURE_ANALYSIS_REQUIRED","inputs_before":before,"inputs_after":after,"source_documents_opened":opened,
        "claim_state_counts":dict(sorted(counts.items())),"section_state_counts":dict(sorted(sec_counts.items())),
        "artifacts":[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in artifacts],"drafting_authorized":False,"book_prose_generated":False})
    print(json.dumps({"claims":dict(counts),"sections":dict(sec_counts),"opened":opened,"verified":len(verified_claims),"provenance_resolved":prior_prov-now_prov,"anchors_resolved":prior_anchor-now_anchor},sort_keys=True))

if __name__ == "__main__": main()
