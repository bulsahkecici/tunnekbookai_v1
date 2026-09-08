#!/usr/bin/env python3
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "data/book/master_structure/book_master_structure_v1.json"
MANIFEST = ROOT / "data/metadata/final_corpus_manifest.csv"
OUTPUT = ROOT / "data/book/coverage/corpus_to_book_coverage_mapping_v1.json"

DOMAIN_TERMS = {
    "maliyet": ["maliyet", "cost"],
    "bakım": ["bakım", "maintenance"],
    "jeolojik": ["jeoloji", "geolog", "jeoteknik", "geotech"],
    "jeoteknik": ["jeoteknik", "geotech"],
    "destek": ["destek", "support"],
    "kaza": ["kaza", "accident"],
    "felaket": ["felaket", "disaster", "kaza", "accident"],
    "enerji": ["enerji", "energy"],
    "projelendirilmesi": ["proje", "design"],
    "projelendirme": ["proje", "design"],
    "güzergah": ["guzergah", "route", "alignment"],
    "yapım": ["yapım", "insaat", "construction"],
    "yöntemleri": ["yontem", "method"],
    "tarihçesi": ["tarih", "history"],
    "literatür": ["literatur", "literature"]
}

def norm(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9çğıöşü]+", " ", value).strip()

def terms(value):
    title_terms = set(norm(value).split())
    return {needle for concept, needles in DOMAIN_TERMS.items() if any(word.startswith(concept) for word in title_terms) for needle in needles}

with STRUCTURE.open(encoding="utf-8") as handle:
    structure = json.load(handle)
with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
    docs = list(csv.DictReader(handle))

records = []
for index, section in enumerate(structure["sections"], 1):
    section_id = section.get("section_id") or section.get("id") or f"ORDER-{index:03d}"
    title = section["source_title"]
    query_terms = terms(title)
    candidates = []
    for doc in docs:
        haystack = norm(" ".join([doc.get("source_relative_path", ""), doc.get("topics", ""), doc.get("document_type", "")]))
        matched = sorted(t for t in query_terms if t in haystack)
        if matched:
            candidates.append({
                "document_id": doc["document_id"],
                "matched_terms": matched,
                "provenance": "final_corpus_manifest.csv:source_relative_path/topics/document_type"
            })
    candidates.sort(key=lambda item: (-len(item["matched_terms"]), item["document_id"]))
    primary = []
    secondary = [item["document_id"] for item in candidates][:10]
    status = "WEAK" if secondary else "UNOBSERVED"
    records.append({
        "section_id": section_id,
        "source_title": title,
        "candidate_source_count": len(candidates),
        "primary_source_ids": primary,
        "secondary_source_ids": secondary,
        "evidence_classes_present": ["canonical_metadata_title_path_match"] if candidates else [],
        "evidence_classes_missing": ["source_content_validation", "claim_level_support"],
        "temporal_freshness_sensitivity": "UNRESOLVED",
        "coverage_status": status,
        "confidence_evidence_basis": "LOW_METADATA_ONLY" if candidates else "NONE_METADATA_ONLY",
        "unresolved_source_conflicts": [],
        "mapping_basis": "normalized exact token occurrence; no corpus content read"
    })

payload = {
    "schema_version": "corpus-to-book-coverage-mapping-v1",
    "status": "FROZEN",
    "scoring": "CATEGORICAL",
    "source_documents_observed": len(docs),
    "source_content_reads": 0,
    "broad_corpus_scans": 0,
    "section_count": len(records),
    "sections": records,
    "drafting_authorized": False
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
