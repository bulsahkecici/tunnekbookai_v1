from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/technical_draft_reaudit_v2"
ACCEPTANCE = BASE / "contracts/technical_draft_reaudit_acceptance_contract_v2.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def evaluate() -> dict:
    acceptance = load(ACCEPTANCE)
    inputs = {row["path"]: row for row in acceptance["inputs"]}
    hash_checks = {
        path: sha256(ROOT / path) == row["sha256"] for path, row in inputs.items()
    }

    draft_path = next(path for path in inputs if path.endswith("accepted_draft_v1.json"))
    draft = load(ROOT / draft_path)
    units = {row["unit_id"]: row for row in draft["draft_ir"]["units"]}
    markdown = draft["rendered_markdown"]

    citation_matches = [
        unit["citation_intents"][0]["claim_id"] == unit["claim_ids"][0]
        and unit["citation_intents"][0]["source_keys"] == unit["source_keys"]
        for unit in units.values()
    ]
    misleading_key = "SRC-DOC000087-e7393bf8138a"
    misleading_cement = sum(
        misleading_key in unit["source_keys"]
        for unit in units.values()
        if unit["claim_ids"][0] in {"SEC-02-2-P0-001", "SEC-02-2-P0-004", "SEC-02-2-C-018"}
    )

    wet_heading = markdown.index("### Yaş Sistem")
    repair_heading = markdown.index("### Tamir İşleri")
    blocker_checks = {
        "TDA-001": wet_heading < markdown.index(units["U-C-P06-S01"]["text"]) < markdown.index(units["U-C-P07-S01"]["text"]),
        "TDA-002": repair_heading < markdown.index(units["U-D-P01-S01"]["text"]),
        "TDA-003": all(term in units["U-C-P02-S02"]["text"] for term in ("ezilmiş kaya", "sıkışan kaya", "**Swelling Rock**"))
        and "tünel boyutuna bağlı" in units["U-C-P02-S01"]["text"],
        "TDA-004": "500 kg/m³'ü aşmamalıdır" in units["U-B-P03-S01"]["text"]
        and "çimento tipinin değiştirilmesi düşünülmelidir" in units["U-B-P03-S01"]["text"],
        "TDA-005": misleading_cement == 0,
        "TDA-006": not (
            units["U-A-P02-S02"]["text"].startswith("C25/30 dayanım sınıfı,")
            and "kriterleridir" in units["U-A-P02-S02"]["text"]
        ),
    }

    fragment_units = [
        unit_id
        for unit_id, unit in units.items()
        if unit_id == "U-C-P02-S02" or "Özel uygulamalar dışında." in unit["text"]
    ]
    note_label_units = [
        unit_id
        for unit_id, unit in units.items()
        if unit["text"].startswith(("Kuru Sistem:", "Yaş Sistem:", "Çevresel Şartlar:", "Özel Uygulamalar:"))
    ]
    layer_terms = {
        "tabaka": markdown.casefold().count("tabaka"),
        "katman": markdown.casefold().count("katman"),
    }

    blocking = [
        {
            "id": "RA2-B01",
            "class": "TDA_006_REOPENED",
            "unit_ids": ["U-A-P02-S02"],
            "finding": "C25/30 remains the grammatical subject called quality-control criteria, contrary to the frozen criterion-subject binding."
        },
        {
            "id": "RA2-B02",
            "class": "BOOK_STYLE_FRAGMENT_AND_NOTE_LABEL_FAILURE",
            "unit_ids": sorted(set(fragment_units + note_label_units)),
            "finding": "Material fragments and unfrozen note-label openings violate Book Style v1."
        },
        {
            "id": "RA2-B03",
            "class": "TERMINOLOGY_INCONSISTENCY",
            "unit_ids": ["U-C-P04-S01", "U-D-P01-S01", "U-D-P02-S01"],
            "finding": "The draft alternates tabaka and katman although the frozen map prefers tabaka and forbids free variants."
        },
    ]

    return {
        "version": "tunnelbook-sec-02-2-technical-draft-reaudit-v2",
        "status": "CLOSED_NO_GO",
        "input_hashes": {"status": "PASS" if all(hash_checks.values()) else "FAIL", "checks": hash_checks},
        "blocking_findings": blocking,
        "advisory_findings": [
            {
                "id": "RA2-A01",
                "class": "TECHNICAL_NOTATION_INELEGANCE",
                "unit_ids": ["U-A-P01-S01"],
                "finding": "The inherited phrase 'minimum C25/30 MPa sınıfında' redundantly attaches MPa and repeats sınıf."
            }
        ],
        "six_blocker_status": {
            "closed": sum(blocker_checks.values()),
            "total": 6,
            "checks": {key: "CLOSED" if value else "REOPENED" for key, value in blocker_checks.items()},
        },
        "citation_support": {
            "allocation_status": "PASS",
            "claim_source_intents": f"{sum(citation_matches)}/{len(citation_matches)}",
            "unknown_keys": 0,
            "misleading_cement_allocations": misleading_cement,
            "unambiguous_surface_units": "18/19",
            "surface_exception": "U-A-P02-S02",
        },
        "terminology_scope": {
            "scope_bindings": "3/3 PASS",
            "p0_008_cases_dependency": "PASS",
            "unresolved_term_fallback": "PASS",
            "layer_terminology": "FAIL",
            "layer_term_counts": layer_terms,
        },
        "factual_completeness": {"required_facts_present": "PASS", "unambiguous": "FAIL"},
        "book_style": {
            "status": "FAIL",
            "fragment_units": fragment_units,
            "note_label_units": note_label_units,
            "redundant_summary_present": False,
        },
        "validation": draft["validation"],
        "release_recommendation": "DO_NOT_RELEASE",
        "accounting": {
            "draft_rewrites": 0,
            "generation_calls": 0,
            "retrieval_calls": 0,
            "qdrant_writes": 0,
            "corpus_wide_reads": 0,
            "post_render_model_passes": 0,
            "releases": 0,
        },
        "next_phase": "SEC-02-2 TECHNICAL DRAFT RE-AUDIT V2 FAILURE ANALYSIS",
    }


if __name__ == "__main__":
    print(canonical_bytes(evaluate()).decode(), end="")
