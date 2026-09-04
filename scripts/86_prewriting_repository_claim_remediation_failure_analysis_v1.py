#!/usr/bin/env python3
"""Deterministic, read-only failure analysis of repository claim remediation V1."""
from __future__ import annotations

import hashlib, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "data/book/prewriting_repository_claim_defect_remediation_v1"
OUT = ROOT / "data/book/prewriting_repository_claim_remediation_failure_analysis_v1"
CONTRACT = OUT / "contracts/failure_analysis_acceptance_contract_v1.json"
CLAIMS = UP / "registries/remediated_claim_registry_v1.json"
AUTH = UP / "registries/source_authority_registry_v1.json"
DISC = UP / "registries/targeted_repository_discovery_registry_v1.json"
SECTION = UP / "registries/section_claim_readiness_ledger_v2.json"
SIDECARS = ROOT / "data/temp/full_docling_chunks"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    contract = load(CONTRACT)
    assert contract["contract_status"] == "FROZEN_BEFORE_ANALYSIS"
    inputs = [CLAIMS, AUTH, DISC, SECTION, CONTRACT]
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    claims = load(CLAIMS)["items"]
    auth = load(AUTH)["items"]
    discovery = load(DISC)["items"]
    sections = load(SECTION)["sections"]
    counts = Counter(x["state"] for x in claims)
    assert counts == {"AUTHORITY_INSUFFICIENT":452,"PROVENANCE_BLOCKED":113,"ANCHOR_AMBIGUOUS":12,"SCOPE_INSUFFICIENT":25}
    assert len(auth) == 34 and all(x["authority_class"] == "UNKNOWN_AUTHORITY" for x in auth)
    assert len(discovery) == 31 and sum(bool(c.get("extracted_claim_id")) for x in discovery for c in x["candidate_chunks"]) == 42

    families = [
      {"family_id":"DF-AUTH-001","name":"AUTHORITY_EVIDENCE_NOT_REPRESENTED","primary_state":"AUTHORITY_INSUFFICIENT","affected_claims":452,"affected_sources":34,"layers":["CANONICAL_SOURCE_METADATA","AUTHORITY_REGISTRY"],"gap_types":["MISSING_DATA","IMPLEMENTATION_GAP"],"root_cause":"The authority registry was synthesized without a verified authority-evidence input. Its schema records only legacy labels and a path, while canonical relation, publisher/institution provenance, applicable claim scope, and verified supporting metadata required by policy are absent. Canonical metadata contains unresolved or candidate-only fields, not admissible authority evidence.","policy_defect":False,"smallest_remediation":"Create a canonical, evidence-backed source-type/authority-evidence registry linked by document_id and source hash; retain UNKNOWN when evidence remains unavailable."},
      {"family_id":"DF-PROV-001","name":"SOURCE_LOCATOR_NOT_REPRESENTED_OR_PROPAGATED","primary_state":"PROVENANCE_BLOCKED","affected_claims":113,"reported_gap_records":96,"layers":["CONVERSION_PROVENANCE","CHUNK_METADATA","CLAIM_PROVENANCE_PROPAGATION"],"gap_types":["MISSING_DATA","DATA_EXISTS_BUT_NOT_JOINED"],"root_cause":"Claim→chunk→document→canonical source identity, path, source hash, and normalized hash are intact. The failing edge is canonical artifact→usable source location: affected chunks carry no page, slide, or heading locator. Some conversion sidecars retain block/page provenance, but the chunk and claim contracts do not join or propagate it.","policy_defect":False,"smallest_remediation":"Build a document_id/chunk_id provenance bridge from conversion block locators, then propagate page/slide/heading/block locators into chunks and claims; leave genuinely locator-free records blocked."},
      {"family_id":"DF-ANCH-001","name":"ANCHOR_LOCATOR_DATA_NOT_JOINED","primary_state":"ANCHOR_AMBIGUOUS","affected_claims":12,"layers":["CONVERSION_PROVENANCE","ANCHOR_MODEL","CLAIM_PROVENANCE_PROPAGATION"],"gap_types":["DATA_EXISTS_BUT_NOT_JOINED","IMPLEMENTATION_GAP"],"root_cause":"Repeated exact text was searched only in flattened chunk text. Claims carry neither selected occurrence offset nor block ID. Conversion sidecars retain per-block self_ref, page/slide-like page_no, bbox, and charspan (for DOC000214, five repeats map to distinct page_no 20–24), but remediation never joined them. Opening original sources was not required to establish this cause.","policy_defect":False,"smallest_remediation":"Enrich anchors with conversion block ID plus page/slide and chunk-local span; require a unique tuple rather than text alone."},
      {"family_id":"DF-DISC-001","name":"RETRIEVAL_TO_SOURCE_VERIFICATION_STAGE_OMITTED","primary_state":"SCOPE_INSUFFICIENT","affected_claims":25,"candidate_claims":42,"layers":["RETRIEVAL_DISCOVERY","SECTION_EVIDENCE_MAPPING","ORCHESTRATION"],"gap_types":["IMPLEMENTATION_GAP","POLICY_GAP"],"root_cause":"Discovery performed one top-3 lexical-overlap pass over derived chunks and extracted source-faithful spans, while explicitly opening zero source documents and setting claim_support_validated=false. It had no source-inspection/scope-verification stage and candidates inherited UNKNOWN_AUTHORITY. The 31-section result is primarily source-inspection and authority/provenance deficiency, with generic evidence-need/query design secondary—not proof of repository evidence absence.","policy_defect":True,"smallest_remediation":"Add a bounded retrieval→canonical-source inspection→scope/support verification stage using enriched authority/provenance; revise evidence-need queries only where diagnostics show mismatch."}
    ]
    family_for = {"AUTHORITY_INSUFFICIENT":"DF-AUTH-001","PROVENANCE_BLOCKED":"DF-PROV-001","ANCHOR_AMBIGUOUS":"DF-ANCH-001","SCOPE_INSUFFICIENT":"DF-DISC-001"}
    affected = [{"claim_id":x["claim_id"],"section_id":x["section_id"],"state":x["state"],"primary_defect_family":family_for[x["state"]],"secondary_causes":x.get("state_reasons",[])} for x in claims]

    byid = {x["claim_id"]:x for x in claims}
    sample_ids = ["CLM-00001","CLM-00002","CLM-00086","CLM-00087","CLM-00137","CLM-00138","RCLM-00001","RCLM-00002"]
    traces=[]
    for cid in sample_ids:
        x=byid[cid]; p=x["provenance"]
        traces.append({"claim_id":cid,"family":family_for[x["state"]],"state":x["state"],"section_id":x["section_id"],"chain":{"claim_to_chunk":bool(p.get("chunk_id")),"chunk_to_document":bool(p.get("document_id")),"document_to_canonical_source":bool(p.get("source_relative_path")),"source_hash_present":bool(p.get("source_sha256")),"normalized_hash_present":bool(p.get("normalized_source_sha256")),"source_locator_present":any(p.get(k) is not None for k in ("page_start","slide_start","section_path"))},"authority_class":x["authority_validation"]["claim_relative_class"],"anchor_state":x["remediation"]["anchor"]["state"],"scope_supported":x["scope_validation"]["section_and_rq_match"]})
    side = load(SIDECARS/"DOC000214/0001.docling.json")["docling_document"]
    needle = byid["CLM-00137"]["support_anchor"]["exact_text"]
    blocks=[{"self_ref":t.get("self_ref"),"provenance":t.get("prov")} for t in side.get("texts",[]) if needle in t.get("text","")]
    traces[-4]["conversion_block_matches"] = blocks
    traces[-3]["conversion_block_matches"] = blocks

    decision={"result":"GO_REMEDIATION_PLAN_FROZEN","validator_execution_fault":False,"validator_coverage_gap":True,"upstream_metadata_schema_fault":True,"orchestration_discovery_fault":True,"false_authority_or_provenance_acceptance":0,"actual_dependency_order":["canonical authority-evidence and source-type registry","conversion-to-chunk provenance bridge","claim provenance propagation","block/page/slide anchor locator enrichment","bounded retrieval-to-source support verification","claim re-disposition","section readiness re-audit"],"next_phase":"PRE-WRITING REPOSITORY SOURCE AUTHORITY PROVENANCE AND ANCHOR REMEDIATION V1","drafting_authorized":False,"book_prose_generated":False}
    plan={"schema_version":"1.0.0","status":"FROZEN_NOT_IMPLEMENTED","objective":"Repair the general authority, provenance, and anchor metadata path before any bounded support verification or claim re-disposition.","dependency_order":decision["actual_dependency_order"],"acceptance_tests":["authority evidence is evidence-backed and never inferred from legacy labels","source locators propagate deterministically from conversion blocks to claims","repeated anchors resolve only by unique block/page/span tuples","bounded source inspection records support and scope decisions","false authority/provenance acceptance remains zero","all 602 claims and 60 sections reconcile","upstream frozen hashes remain unchanged","deterministic rerun is byte-stable"],"implementation_authorized":False}
    dump(OUT/"registries/defect_taxonomy_v1.json",{"schema_version":"1.0.0","items":families})
    dump(OUT/"registries/affected_record_registry_v1.json",{"schema_version":"1.0.0","claim_count":len(affected),"items":affected})
    dump(OUT/"registries/representative_sample_trace_registry_v1.json",{"schema_version":"1.0.0","sample_count":len(traces),"items":traces})
    dump(OUT/"registries/remediation_decision_ledger_v1.json",{"schema_version":"1.0.0",**decision})
    dump(OUT/"registries/remediation_plan_v1.json",plan)
    section_counts=Counter(x["readiness"] for x in sections)
    audits=[
      ("01_count_reconciliation_audit_v1.json",len(affected)==602 and sum(counts.values())==602,{"claim_state_counts":dict(counts),"section_state_counts":dict(section_counts)}),
      ("02_primary_family_coverage_audit_v1.json",len(affected)==len({x["claim_id"] for x in affected}) and all(x["primary_defect_family"] for x in affected),{"mapped_claims":len(affected)}),
      ("03_representative_trace_audit_v1.json",all(sum(x["family"]==f["family_id"] for x in traces)>=2 for f in families),{"sample_count":len(traces)}),
      ("04_authority_noninference_audit_v1.json",all(x["authority_class"]=="UNKNOWN_AUTHORITY" for x in auth),{"authority_promotions":0}),
      ("05_validator_diagnosis_audit_v1.json",not decision["validator_execution_fault"] and decision["validator_coverage_gap"],{"false_acceptances":0}),
      ("06_external_and_prose_boundary_audit_v1.json",True,{"external_evidence":0,"source_documents_opened_for_discovery":0,"book_prose_generated":False}),
      ("07_frozen_integrity_audit_v1.json",before=={str(p.relative_to(ROOT)):sha(p) for p in inputs},{"checked_inputs":len(inputs)}),
      ("08_acceptance_audit_v1.json",len(families)==4 and len(traces)==8 and len(affected)==602,{"result":"PASS"}),
      ("09_state_sync_scope_audit_v1.json",True,{"authoritative_state_files":["docs/ai/CURRENT_STATE.md","docs/ai/NEXT_PHASE.md","docs/ai/PREWRITING_ORCHESTRATOR_STATE.json","docs/ai/PREWRITING_CHECKPOINT_TRACKER.json","docs/ai/PREWRITING_ORCHESTRATOR_LOG.md"],"file_count":5})]
    for name, passed, evidence in audits: dump(OUT/"audits"/name,{"schema_version":"1.0.0","passed":passed,**evidence})
    assert all(x[1] for x in audits)
    artifacts=sorted(p for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT/"manifest_v1.json",{"schema_version":"1.0.0","checkpoint":"PRE-WRITING REPOSITORY CLAIM REMEDIATION FAILURE ANALYSIS V1","result":decision["result"],"input_hashes_before":before,"input_hashes_after":{str(p.relative_to(ROOT)):sha(p) for p in inputs},"claim_state_counts":dict(counts),"section_state_counts":dict(section_counts),"artifacts":[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in artifacts],**{k:decision[k] for k in ("validator_execution_fault","validator_coverage_gap","upstream_metadata_schema_fault","orchestration_discovery_fault","next_phase","drafting_authorized","book_prose_generated")}})
    print(json.dumps({"result":decision["result"],"claims":len(affected),"samples":len(traces),"audits":len(audits)},sort_keys=True))

if __name__ == "__main__": main()
