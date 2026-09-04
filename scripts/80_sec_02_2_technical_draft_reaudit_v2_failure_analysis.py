#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/book/drafting/sec_02_2/technical_draft_reaudit_v2_failure_analysis/contracts/failure_analysis_acceptance_contract_v1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate():
    contract = _load(CONTRACT)
    inputs = {item["path"]: item for item in contract["inputs"]}
    hashes = {path: _sha(ROOT / path) == item["sha256"] for path, item in inputs.items()}
    draft = _load(ROOT / contract["inputs"][0]["path"])
    reaudit = _load(ROOT / contract["inputs"][1]["path"])
    units = {unit["unit_id"]: unit["text"] for unit in draft["draft_ir"]["units"]}

    probes = {
        "tda_006_subject_misbinding": units["U-A-P02-S02"].startswith("C25/30 dayanım sınıfı") and "kalite kontrol kriterleridir" in units["U-A-P02-S02"],
        "fragment_special_applications": "Özel uygulamalar dışında." in units["U-B-P02-S01"],
        "fragment_named_cases": units["U-C-P02-S02"] == "Belirli ezilmiş kaya, sıkışan kaya ve **Swelling Rock**.",
        "note_labels": all(":" in units[uid].split(".")[0] for uid in ["U-B-P01-S01", "U-B-P02-S01", "U-B-P04-S01", "U-B-P05-S01"]),
        "mixed_layer_terms": reaudit["terminology_scope"]["layer_term_counts"] == {"tabaka": 10, "katman": 6},
        "notation_redundancy": "C25/30 MPa sınıfında" in units["U-A-P01-S01"],
        "validator_accepted": reaudit["validation"]["status"] == "ACCEPT" and reaudit["validation"]["failure_histogram"] == {},
    }

    causes = {
        "RA2-B01": {
            "primary": "REALIZER_SEMANTIC_SUBJECT_BINDING_FAILURE",
            "realization_contract_fault": False,
            "renderer_fault": True,
            "validator_coverage_gap": True,
            "independently_blocking": True
        },
        "RA2-B02": {
            "primary": "STYLE_INTEGRATION_PROJECTION_FAILURE",
            "style_contract_fault": False,
            "renderer_fault": True,
            "validator_coverage_gap": True,
            "independently_blocking": True
        },
        "RA2-B03": {
            "primary": "TERMINOLOGY_ALLOCATION_CLOSURE_GAP",
            "renderer_fault": False,
            "validator_coverage_gap": True,
            "independently_blocking": True
        },
        "RA2-A01": {
            "primary": "INHERITED_WORDING_QUALITY_GAP",
            "renderer_fault": False,
            "validator_coverage_gap": True,
            "independently_blocking": False
        }
    }

    return {
        "version": "tunnelbook-sec-02-2-technical-draft-reaudit-v2-failure-analysis-v1",
        "status": "CLOSED_GO" if all(hashes.values()) and all(probes.values()) else "CLOSED_NO_GO",
        "input_hashes": {"status": "PASS" if all(hashes.values()) else "FAIL", "checks": hashes},
        "causes": causes,
        "validator_fault": {"answer": True, "kind": "COVERAGE_GAP_NOT_EXECUTION_DEFECT"},
        "renderer_fault": {"answer": True, "scope": ["RA2-B01", "RA2-B02"]},
        "style_contract_fault": False,
        "smallest_general_remediation": {
            "name": "VERSIONED_REALIZATION_STYLE_TERMINOLOGY_CLOSURE_GATE_V1",
            "pre_render": ["typed semantic subject/predicate binding", "single preferred-term allocation", "complete-sentence and label-role feasibility"],
            "post_render": ["semantic binding", "fragment", "material note-label", "no-free-variant terminology"],
            "advisory_lint": ["strength-class unit duplication"],
            "claim_specific_rules": 0
        },
        "probes": probes,
        "accounting": {"corpus_wide_reads": 0, "draft_rewrites": 0, "validator_changes": 0, "generation_calls": 0, "retrieval_calls": 0, "qdrant_writes": 0, "commits": 0, "pushes": 0},
        "next_phase": "SEC-02-2 GENERAL REALIZATION STYLE TERMINOLOGY CLOSURE REMEDIATION V1"
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
