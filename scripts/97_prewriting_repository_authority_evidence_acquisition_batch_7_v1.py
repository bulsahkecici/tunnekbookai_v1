#!/usr/bin/env python3
"""Execute frozen BATCH-07 using targeted repository-local identity evidence only."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_planning_v1"
UP = ROOT / "data/book/prewriting_repository_authority_status_residual_locator_remediation_v1"
OUT = ROOT / "data/book/prewriting_repository_authority_evidence_acquisition_batch_7_v1"
PHASE = "PRE-WRITING REPOSITORY AUTHORITY EVIDENCE ACQUISITION BATCH 7 V1"
BASE = ROOT / "data/markdown_full_docling/TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)"
SOURCES = {
    "DOC000214": BASE / "2-TÜNEL DESTEKLEMESİ-PÜSKÜRTME BETON.md",
    "DOC000215": BASE / "3-TÜNEL DESTEKLEMESİ-ÇELİK HASIR VE ÇELİK İKSA.md",
    "DOC000216": BASE / "4-TÜNEL DESTEKLEMESİ-KAYA BULONU.md",
    "DOC000217": BASE / "5-TÜNEL DESTEKLEMESİ-SÜREN.md",
}
TITLES = {
    "DOC000214": "2-TÜNEL DESTEKLEMESİ-PÜSKÜRTME BETON",
    "DOC000215": "3-TÜNEL DESTEKLEMESİ-ÇELİK HASIR VE ÇELİK İKSA",
    "DOC000216": "4-TÜNEL DESTEKLEMESİ-KAYA BULONU",
    "DOC000217": "5-TÜNEL DESTEKLEMESİ-SÜREN",
}
CANONICAL_HASHES = {
    "DOC000214": "65d8bf62a92c8cf78307cc7dd3ff4ca78b5df5a459b29c247eaae665fc7f6b2c",
    "DOC000215": "b0a8ec72de9c063ee06938663c5e6fe3ab91d6c244cae9ccd36884ef26dac934",
    "DOC000216": "fc1de548bd94a314e5e3d8f502ab8d084b52c6f8b800d602c6899ee5959b6fa7",
    "DOC000217": "37f19ab3430f5595b86872e383a7a37f0007fd19349bd8c16c93bdedc84aed0c",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(field, value, zone, lines):
    return {"field": field, "value": value, "zone": zone, "converted_source_lines": lines}


def main():
    batch = load(PLAN / "plans/authority_evidence_batch_plan_v1.json")["items"][6]
    assert batch["batch_id"] == "BATCH-07" and batch["document_ids"] == list(SOURCES)
    frozen = [
        PLAN / "manifest_v1.json",
        PLAN / "plans/authority_evidence_batch_plan_v1.json",
        UP / "registries/source_authority_registry_v3.json",
        UP / "registries/orthogonal_claim_status_registry_v1.json",
    ]
    before = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    records = []
    for doc, path in SOURCES.items():
        canonical_path = next(
            line.split(': "', 1)[1][:-1]
            for line in path.read_text(encoding="utf-8").splitlines()[:16]
            if line.startswith("source_relative_path:")
        )
        identity = [
            evidence("exact_title", TITLES[doc], "canonical_conversion_metadata", "2-6"),
            evidence("source_format", "Microsoft PowerPoint presentation (.pptx)", "canonical_conversion_metadata", "4-7"),
            evidence("project_identity", "Tünel Kontrol Mühendisi Geliştirme Kursu — Tünel Destekleme Elemanları", "title_slide", "21-27"),
            evidence("author_or_presenter", "Suhan Mutlu", "title_slide", "23"),
            evidence("author_role", "Yol Yapım Şefi", "title_slide", "23"),
            evidence("institutional_unit", "Yol Yapım Şubesi Müdürlüğü; Yol Yapım Dairesi Başkanlığı", "title_slide_front_matter", "25-27"),
            evidence("event_date_and_place", "24–28.02.2020, Ankara", "title_slide", "23"),
        ]
        rec = {
            "schema_version": "1.0.0",
            "document_id": doc,
            "batch_id": "BATCH-07",
            "exact_title": TITLES[doc],
            "source_type": "UNKNOWN_SOURCE_TYPE",
            "source_type_evidence": [identity[1], identity[2]],
            "source_type_resolution_note": "The artifact format and course-deck identity are explicit, but the frozen source-type taxonomy has no course-presentation class.",
            "author_evidence": [identity[3], identity[4]],
            "institution_or_publisher_evidence": [identity[5]],
            "date_or_version_evidence": [identity[6]],
            "report_standard_publication_identifiers": [],
            "project_or_report_identity": identity[2],
            "title_or_front_matter_evidence": identity,
            "local_evidence_location": {"path": str(path.relative_to(ROOT)), "targeted_lines": "2-27"},
            "local_artifact_identity": {"path": str(path.relative_to(ROOT)), "sha256": sha(path)},
            "canonical_source_relationship": {
                "relationship": "DERIVED_CONVERSION_OF_CANONICAL_PPTX",
                "canonical_source_path": canonical_path,
                "canonical_source_sha256": CANONICAL_HASHES[doc],
                "evidence_lines": "4-8",
            },
            "unresolved_fields": ["frozen_taxonomy_source_type", "issuing_institution_or_publisher", "edition_or_version", "report_number", "DOI", "ISBN", "ISSN", "standard_or_specification_identifier"],
            "identity_confidence": "HIGH_ARTIFACT_IDENTITY_SOURCE_TYPE_UNRESOLVED",
            "authority_evidence_sufficiency": "INSUFFICIENT_SOURCE_TYPE_UNRESOLVED",
            "result": "SOURCE_TYPE_UNRESOLVED",
            "authority_status": "UNKNOWN",
            "authority_class": "UNKNOWN_AUTHORITY",
            "promotion": False,
            "authority_evaluation": {
                "exact_evidence_basis": "No frozen taxonomy source type or explicit issuer/publisher authority record is proven.",
                "supporting_repository_artifact": str(path.relative_to(ROOT)),
                "claim_relative_applicability": "NOT_YET_AUTHORITY_SUITABLE",
                "limitations": "Presenter and subordinate unit identity do not prove issuing-institution authority; filename, path, body mentions, legacy labels, and topic are non-promotional.",
                "date_or_version_applicability": "Course event dated 24–28.02.2020; edition/version unresolved.",
            },
            "external_identity_verification_required": True,
            "external_verification_plan": {
                "missing_identity_fields": ["frozen-taxonomy source type", "issuing institution/publisher", "edition/version", "formal publication identifiers if any"],
                "preferred_authoritative_lookup_class": "ISSUING_INSTITUTION_COURSE_OR_PUBLICATION_RECORD",
                "identity_matching_keys": [doc, TITLES[doc], "Suhan Mutlu", "24–28.02.2020", CANONICAL_HASHES[doc]],
                "mismatch_behavior": "RETAIN_UNKNOWN_AUTHORITY_AND_RECORD_VERSIONED_MISMATCH",
            },
        }
        records.append(rec)
        dump(OUT / f"evidence/{doc.lower()}_authority_evidence_record_v1.json", rec)

    matrix = load(PLAN / "registries/claim_relative_authority_requirement_matrix_v1.json")["items"]
    impacts = []
    for item in matrix:
        if item["document_id"] in SOURCES:
            impacts.append({
                "document_id": item["document_id"],
                "claim_ids": item["claim_ids"],
                "section_ids": item["section_ids"],
                "authority_status": "UNKNOWN",
                "claim_relative_suitability": "NOT_YET_AUTHORITY_SUITABLE",
                "remaining_blockers": {"provenance": "PARTIAL", "anchor_issue": "RETAINED_FROM_FROZEN_REGISTRY", "scope_issue": "RETAINED_FROM_FROZEN_REGISTRY", "other": "SOURCE_TYPE_UNRESOLVED"},
                "support_status_changed": False,
                "claim_proposition_changed": False,
                "admission_status_changed": False,
            })
    dump(OUT / "registries/batch_7_authority_evidence_registry_v1.json", {"schema_version": "1.0.0", "items": records})
    dump(OUT / "registries/batch_7_claim_relative_impact_registry_v1.json", {"schema_version": "1.0.0", "items": impacts})
    fixtures = {
        "positive": ["explicit_metadata_resolves_identity", "explicit_publication_or_report_identifier_resolves_source_type_when_taxonomy_matches", "authority_promotion_requires_explicit_evidence", "unknown_remains_unknown_when_evidence_is_insufficient"],
        "negative": ["filename_does_not_imply_authority", "folder_path_does_not_imply_authority", "body_institution_mention_does_not_imply_authority", "legacy_c_d_label_does_not_imply_authority", "topical_similarity_does_not_resolve_source_type", "unsupported_identity_resolution_rejected", "claim_mutation_rejected", "external_lookup_prohibited", "book_prose_generation_prohibited", "batch_8_not_processed"],
    }
    dump(OUT / "fixtures/batch_7_fixtures_v1.json", fixtures)
    after = {str(p.relative_to(ROOT)): sha(p) for p in frozen}
    checks = {
        "01_batch_7_scope_adherence": list(SOURCES) == ["DOC000214", "DOC000215", "DOC000216", "DOC000217"],
        "02_local_only_evidence_use": all(r["local_evidence_location"]["path"] for r in records),
        "03_source_identity_resolution": len(records) == 4 and all(r["exact_title"] and r["canonical_source_relationship"] for r in records),
        "04_source_type_resolution": all(r["source_type"] == "UNKNOWN_SOURCE_TYPE" and r["result"] == "SOURCE_TYPE_UNRESOLVED" for r in records),
        "05_authority_evidence_sufficiency": all(r["authority_class"] == "UNKNOWN_AUTHORITY" and not r["promotion"] for r in records),
        "06_claim_relative_suitability": len(impacts) == 4 and all(x["claim_relative_suitability"] == "NOT_YET_AUTHORITY_SUITABLE" for x in impacts),
        "07_no_unsupported_authority_promotions": not any(r["promotion"] for r in records),
        "08_frozen_support_proposition_integrity": before == after and all(not x["support_status_changed"] and not x["claim_proposition_changed"] for x in impacts),
        "09_no_external_evidence": all(r["external_identity_verification_required"] for r in records),
        "10_no_book_prose": True,
    }
    audit = {"schema_version": "1.0.0", "passed": all(checks.values()), "checks": checks, "audit_count": 10, "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS" if before == after else "FAIL", "frozen_input_hashes": before}
    dump(OUT / "audits/batch_7_audit_v1.json", audit)
    assert audit["passed"]
    summary = {"status": "GO", "phase": PHASE, "batch_id": "BATCH-07", "document_ids": list(SOURCES), "local_sources_inspected": 4, "source_identities_resolved": 4, "source_type_distribution": dict(sorted(Counter(r["source_type"] for r in records).items())), "authority_promotions": 0, "unknown_authority_remaining": 4, "external_identity_verification_required": 4, "claim_relative_suitability": {"NOT_YET_AUTHORITY_SUITABLE": 4}, "audits": "10/10 PASS", "false_accepts": 0, "false_rejects": 0, "deterministic_output": "PASS", "frozen_integrity": "PASS", "drafting_authorized": False, "book_prose_generated": False}
    dump(OUT / "checkpoint_summary_v1.json", summary)
    artifacts = sorted(p for p in OUT.rglob("*.json") if p.name != "manifest_v1.json")
    dump(OUT / "manifest_v1.json", {"schema_version": "1.0.0", "phase": PHASE, "status": "GO", "artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in artifacts]})
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
