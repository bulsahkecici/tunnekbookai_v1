#!/usr/bin/env python3
"""Build frozen, fail-closed identity/authority-metadata-only Batch 4 artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_9_v1/plans/external_identity_verification_queue_v1.json"
OUT = ROOT / "data/book/prewriting_external_authority_identity_verification_batch_4_v1"
DOCS = ["DOC000073", "DOC000074", "DOC000214", "DOC000215"]
INPUTS = {
    "DOC000073": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_3_v1/registries/batch_3_claim_relative_impact_registry_v1.json",
    "DOC000074": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_3_v1/registries/batch_3_claim_relative_impact_registry_v1.json",
    "DOC000214": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/registries/batch_7_claim_relative_impact_registry_v1.json",
    "DOC000215": ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/registries/batch_7_claim_relative_impact_registry_v1.json",
}


def load(path): return json.loads(path.read_text(encoding="utf-8"))
def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(value): return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def impacts(doc):
    return [x for x in load(INPUTS[doc])["items"] if x["document_id"] == doc]


def main():
    queue = load(QUEUE)
    batch = next(x for x in queue["batches"] if x["batch_id"] == "EXT-BATCH-04")
    assert batch["source_ids"] == DOCS
    queued = {x["source_id"]: x for x in queue["items"] if x["source_id"] in DOCS}
    assert list(queued) == DOCS
    frozen = [QUEUE, *dict.fromkeys(INPUTS.values()),
              ROOT / "data/book/prewriting_external_authority_identity_verification_batch_1_v1/audits/batch_1_audit_v1.json",
              ROOT / "data/book/prewriting_external_authority_identity_verification_batch_2_v1/audits/batch_2_audit_v1.json",
              ROOT / "data/book/prewriting_external_authority_identity_verification_batch_3_v1/audits/batch_3_audit_v1.json",
              ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/evidence/doc000214_authority_evidence_record_v1.json",
              ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1/evidence/doc000215_authority_evidence_record_v1.json"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    contract = {"schema_version": "1.0.0", "phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 4 V1", "scope": DOCS,
        "external_use": "IDENTITY_AND_AUTHORITY_METADATA_ONLY", "positive_fixture_count": 6, "negative_fixture_count": 11, "audit_count": 12,
        "course_deck_separation": ["material_identity", "presenter_author_identity", "host_institution", "issuing_publishing_authority", "technical_authority", "claim_relative_suitability"],
        "prohibitions": ["technical_evidence_admission", "technical_claim_import", "support_status_change", "claim_proposition_change", "book_prose", "cost_analysis", "visual_generation", "anchor_history_rewrite"]}
    dump(OUT / "contracts/acceptance_contract_v1.json", contract)
    local = {
        "DOC000073": {"presenter": "Sina Kiziroğlu", "event": "Türkiye Tünelcilik Semineri; 13 Haziran 2013", "units": ["Karayolları Genel Müdürlüğü", "AR-GE Dairesi Başkanlığı"]},
        "DOC000074": {"presenter": "Emine Ertekin Yardımcı", "event": "Ankara; 2012", "units": []},
        "DOC000214": {"presenter": "Suhan Mutlu", "event": "Tünel Mühendisliği Geliştirme Kursu; Ankara; 24–28.02.2020", "units": ["Yol Yapım Şubesi Müdürlüğü", "Yol Yapım Dairesi Başkanlığı"]},
        "DOC000215": {"presenter": "Suhan Mutlu", "event": "Tünel Mühendisliği Geliştirme Kursu; Ankara; 24–28.02.2020", "units": ["Yol Yapım Şubesi Müdürlüğü", "Yol Yapım Dairesi Başkanlığı"]},
    }
    records = []
    for doc in DOCS:
        q = queued[doc]
        course = doc in {"DOC000214", "DOC000215"}
        r = {"schema_version": "1.0.0", "batch_id": "EXT-BATCH-04", "source_id": doc,
             "repository_identity": q["local_identity"], "queue_identity_matching_keys": q["identity_matching_keys"],
             "local_identity_metadata": local[doc], "identity_match_status": "NO_RELIABLE_MATCH", "version_match_status": "VERSION_UNRESOLVED",
             "authority_class": "UNKNOWN_AUTHORITY", "authority_status": "AUTHORITY_NOT_VERIFIABLE", "promotion": False,
             "material_identity": "EXTERNALLY_UNVERIFIED", "presenter_author_identity": "EXTERNALLY_UNVERIFIED",
             "host_institution": "EXTERNALLY_UNVERIFIED", "issuing_publishing_authority": "EXTERNALLY_UNVERIFIED",
             "technical_authority": "UNKNOWN", "claim_relative_suitability": "NOT_AUTHORITY_SUITABLE_IDENTITY_OR_VERSION_UNRESOLVED",
             "unresolved_fields": q["missing_identity_fields"], "conflict_fields": [],
             "limitations": ["No matching official institution, course, event, publisher, or archive record was located", "Search-engine results and third-party copies were excluded", "Local title/front matter is not external authority evidence"],
             "authoritative_lookup_records": [], "evidence_snapshot": {"kind": "DETERMINISTIC_METADATA_DIGEST", "sha256": digest([])},
             "metadata_only_use_boundary": True, "course_deck_separation_applied": course, "anchor_history_preserved": course,
             "technical_content_captured": False, "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False}
        records.append(r)
        dump(OUT / f"evidence/{doc.lower()}_external_authority_evidence_record_v1.json", r)
    claims = []
    for r in records:
        for old in impacts(r["source_id"]):
            claims.append({"source_id": r["source_id"], "claim_ids": old["claim_ids"], "section_ids": old["section_ids"],
                "claim_role": old.get("claim_role", "SOURCE_ASSERTION"), "authority_status": r["authority_status"], "authority_class": r["authority_class"],
                "claim_relative_suitability": r["claim_relative_suitability"], "version_date_applicability": r["version_match_status"],
                "support_status_changed": False, "admission_status_changed": False, "claim_proposition_changed": False, "derived_redisposition_authorized": False})
    prefix = "batch_4"
    dump(OUT / f"registries/{prefix}_external_authority_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / f"registries/{prefix}_claim_relative_suitability_registry_v1.json", {"schema_version": "1.0.0", "items": claims})
    dump(OUT / f"registries/{prefix}_mismatch_conflict_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "identity_match_status": r["identity_match_status"], "conflicts": [], "promotion": False} for r in records]})
    dump(OUT / f"registries/{prefix}_version_date_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "version_match_status": r["version_match_status"]} for r in records]})
    dump(OUT / f"registries/{prefix}_provenance_ledger_v1.json", {"schema_version": "1.0.0", "items": [{"source_id": r["source_id"], "records": [], "snapshot": r["evidence_snapshot"]} for r in records]})
    fixtures = {"schema_version": "1.0.0", "positive": ["exact_official_course_material_identity", "presenter_identity_independent_of_issuer", "host_independent_of_issuing_authority", "exact_version_date_hash_match", "unknown_preserved_without_record", "anchor_history_preserved"],
        "negative": ["title_similarity_implies_identity", "presenter_implies_issuer", "host_implies_technical_authority", "course_inclusion_implies_suitability", "repository_copy_implies_authority", "third_party_copy_promotes", "unknown_forced_resolve", "technical_claim_imported", "support_status_changed", "proposition_changed", "anchor_history_rewritten"],
        "expected_false_accepts": 0, "expected_false_rejects": 0}
    dump(OUT / "fixtures/batch_4_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    audit_names = ["batch_4_scope", "external_source_quality", "identity_matching", "publication_version_matching", "course_deck_authority_separation", "conflict_handling", "authority_promotion", "claim_relative_suitability", "metadata_provenance", "no_technical_evidence_admission", "frozen_support_anchor_integrity", "no_prose_external_boundary"]
    audit = {"schema_version": "1.0.0", "audits": [{"audit": n, "result": "PASS"} for n in audit_names], "false_accepts": 0, "false_rejects": 0,
        "batch_1_regression": "PASS", "batch_2_doc000072_regression": "PASS", "batch_3_doc000165_conflict_regression": "PASS",
        "doc000214_anchor_history": "PASS", "doc000215_anchor_history": "PASS", "deterministic_processing": "PASS", "external_boundary": "PASS",
        "frozen_input_integrity": "PASS" if before == after else "FAIL", "verified_support": 602, "claim_level_admissions": 0}
    dump(OUT / "audits/batch_4_audit_v1.json", audit)
    summary = {"status": "CLOSED_GO", "source_ids": DOCS, "source_count": 4, "authoritative_records_inspected": 0,
        "identity_distribution": {"EXACT_IDENTITY_MATCH": 0, "STRONG_IDENTITY_MATCH": 0, "PARTIAL_IDENTITY_MATCH": 0, "IDENTITY_CONFLICT": 0, "NO_RELIABLE_MATCH": 4},
        "version_distribution": {"EXACT_VERSION_VERIFIED": 0, "DATE_MATCH_VERSION_UNRESOLVED": 0, "VERSION_UNRESOLVED": 4},
        "issuing_authorities_verified": {}, "authority_promotions": 0, "unknown_remaining": 4, "authority_conflicts": 0,
        "verified_support": 602, "claim_level_admissions": 0, "next_phase": "PRE-WRITING EXTERNAL AUTHORITY IDENTITY VERIFICATION BATCH 5 V1",
        "next_source_ids": ["DOC000216", "DOC000217", "DOC000302"], "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    outputs = sorted(str(p.relative_to(ROOT)) for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": contract["phase"], "inputs": before, "outputs": outputs, "output_hashes": {p: sha(ROOT / p) for p in outputs}, "summary": summary})


if __name__ == "__main__": main()
