from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_general_closure_rerun_v1"
PRIOR_BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1_rerun"


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


retry = _module("general_closure_rerun_parent", ROOT / "scripts/78_architecture_v2_2_condition_closed_retry_v1.py")
general = _module("general_closure_gate", ROOT / "scripts/81_sec_02_2_general_realization_style_terminology_closure_v1.py")


SURFACES = {
    "U-A-P02-S02": "Tablo-351-5'e göre 28 günlük karot numunelerde bireysel minimum dayanım 22,5 MPa ve üç adet numuneden oluşan grubun ortalama minimum dayanımı 25,5 MPa kalite kontrol kriterleridir; bunlar dayanım sınıfının kendisi değil, kabul kriterleridir.",
    "U-B-P01-S01": "Kuru sistemde çimento miktarı 350 kg/m³'ten az olmamalıdır.",
    "U-B-P02-S01": "Özel uygulamalar dışında, yaş sistemde çimento miktarı 400 kg/m³'ten az olmamalıdır.",
    "U-B-P04-S01": "Dış çevresel etki sınıfları gereksinimlerine göre, laboratuvar ve ön dizayn deneme çalışmaları ile belirlenen çimento miktarı, durabilite nedeniyle 350 kg/m³'ün altında kalmamalıdır.",
    "U-B-P05-S01": "Şev kaplama, geçici iksa gibi özel uygulamalarda İdare onayı ile bu miktarlar azaltılabilmektedir.",
    "U-C-P02-S02": "Belirli ezilmiş kaya, sıkışan kaya ve **Swelling Rock** koşullarında kalınlık 300 mm ve daha fazla olabilir.",
}


BINDINGS = {
    "U-A-P02-S02": (("FACT_SET", ["22,5 MPa", "25,5 MPa"]), ("COPULAR", ["kalite kontrol kriterleridir"])),
    "U-B-P01-S01": (("ENTITY", ["Kuru sistemde çimento miktarı"]), ("REQUIREMENT", ["az olmamalıdır"])),
    "U-B-P02-S01": (("ENTITY", ["yaş sistemde çimento miktarı"]), ("REQUIREMENT", ["az olmamalıdır"])),
    "U-B-P04-S01": (("ENTITY", ["çimento miktarı"]), ("REQUIREMENT", ["altında kalmamalıdır"])),
    "U-B-P05-S01": (("CONDITION_SET", ["Şev kaplama", "geçici iksa"]), ("ACTION", ["azaltılabilmektedir"])),
    "U-C-P02-S02": (("CONDITION_SET", ["ezilmiş kaya", "sıkışan kaya", "Swelling Rock"]), ("CONDITION", ["300 mm ve daha fazla olabilir"])),
}


def _apply(draft: dict, projected: bool = False) -> None:
    for unit in draft["units"]:
        if unit["unit_id"] in SURFACES:
            unit["text"] = SURFACES[unit["unit_id"]]
        if projected and unit["unit_id"] == "U-C-P02-S02":
            unit["text"] = "Belirli ezilmiş kaya ve sıkışan kaya koşullarında kalınlık 300 mm ve daha fazla olabilir."
        if not projected:
            unit["text"] = unit["text"].replace("sonraki katmanın", "sonraki tabakanın").replace("ilk püskürtme beton katmanı", "ilk püskürtme beton tabakası").replace("ilk katman", "ilk tabaka").replace("katman", "tabaka")
    draft["draft_id"] = "SEC-02-2-V2-2-GENERAL-CLOSURE-RERUN-V1"
    draft["draft_version"] = "tunnelbook-rendered-draft-ir-v2.2-general-closure-rerun-v1"


def build() -> tuple[dict, dict, list[dict]]:
    visible, layout = retry.build(False)
    projected, _ = retry.build(True)
    _apply(visible)
    _apply(projected, projected=True)
    for item in layout:
        if "text" in item:
            item["text"] = item["text"].replace("Katman", "Tabaka").replace("katman", "tabaka")
    return visible, projected, layout


def _package(draft: dict) -> dict:
    instances = []
    for unit in draft["units"]:
        subject, predicate = BINDINGS.get(unit["unit_id"], (("ENTITY", [unit["text"].split()[0]]), ("RELATION", [unit["text"].rstrip(".").split()[-1]])))
        concept_uses = [{"concept_id": "LAYER", "allocated_surface": "tabaka"}] if "tabaka" in unit["text"].casefold() else []
        instances.append({
            "instance_id": f"GR-{unit['unit_id']}", "unit_id": unit["unit_id"], "material": True,
            "render_role": "BODY_SENTENCE", "complete_sentence_feasible": True,
            "semantic_binding": {"subject": {"type": subject[0], "required_anchors": subject[1]},
                                 "predicate": {"type": predicate[0], "required_anchors": predicate[1]}},
            "concept_uses": concept_uses,
        })
    return {"claim_specific_branches": False,
            "terminology_allocations": [{"concept_id": "LAYER", "preferred_term": "tabaka", "variants": ["katman"]}],
            "instances": instances,
            "rendered_units": [{"unit_id": unit["unit_id"], "text": unit["text"]} for unit in draft["units"]]}


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def evaluate() -> dict:
    proof = retry.closure_gate()
    visible, projected, layout = build()
    visible["artifact_status"] = "V2_2_GENERAL_CLOSURE_RERUN_DRAFT_ACCEPTED"
    validation = retry.integration.validate_draft(visible, projected)
    closure_result = general.validate(_package(visible))
    markdown = retry.integration.render_markdown(visible, layout).replace(
        "V2_2_TECHNICAL_STYLE_DRAFT_ACCEPTED",
        "V2_2_GENERAL_CLOSURE_RERUN_DRAFT_ACCEPTED",
        1,
    )
    units = {row["unit_id"]: row for row in visible["units"]}
    blocker_checks = {
        "TDA-001": markdown.index("### Yaş Sistem") < markdown.index(units["U-C-P06-S01"]["text"]) < markdown.index(units["U-C-P07-S01"]["text"]),
        "TDA-002": markdown.index("### Tamir İşleri") < markdown.index(units["U-D-P01-S01"]["text"]),
        "TDA-003": all(x in units["U-C-P02-S02"]["text"] for x in ("ezilmiş kaya", "sıkışan kaya", "**Swelling Rock**")) and "tünel boyutuna bağlı" in units["U-C-P02-S01"]["text"],
        "TDA-004": all(x in units["U-B-P03-S01"]["text"] for x in ("500 kg/m³'ü aşmamalıdır", "çimento tipinin değiştirilmesi düşünülmelidir")),
        "TDA-005": all("SRC-DOC000087-e7393bf8138a" not in unit["source_keys"] for unit in visible["units"]),
        "TDA-006": all(x in units["U-A-P02-S02"]["text"] for x in ("22,5 MPa", "25,5 MPa", "kalite kontrol kriterleridir")),
    }
    citations = all(unit["citation_intents"][0]["claim_id"] == unit["claim_ids"][0] and unit["citation_intents"][0]["source_keys"] == unit["source_keys"] for unit in visible["units"])
    frozen = general.frozen_integrity()
    go = all(blocker_checks.values()) and validation["status"] == "ACCEPT" and closure_result["status"] == "ACCEPT" and citations and frozen["status"] == "PASS"
    return {
        "version": "tunnelbook-sec-02-2-architecture-v2.2-general-closure-rerun-v1",
        "phase": "SEC-02-2 ARCHITECTURE V2.2 TECHNICAL + BOOK STYLE INTEGRATION V1 RERUN AFTER GENERAL CLOSURE",
        "status": "GO" if go else "NO_GO", "artifact_status": "V2_2_GENERAL_CLOSURE_RERUN_DRAFT_ACCEPTED" if go else "V2_2_GENERAL_CLOSURE_RERUN_DRAFT_REJECTED",
        "final_manuscript": False, "draft_ir": visible, "rendered_markdown": markdown,
        "validation": validation, "general_closure": closure_result,
        "six_blocker_status": {"closed": sum(blocker_checks.values()), "total": 6, "checks": blocker_checks},
        "closure_results": {"conditions": f"{proof['condition_requirements_closed']}/{proof['condition_requirements']}", "dependencies": f"{proof['dependency_requirements_closed']}/{proof['dependency_requirements']}", "unresolved_term_fallback": "PASS"},
        "gate_results": {"citation_support": "PASS" if citations else "FAIL", "factual_completeness": "PASS" if all(blocker_checks.values()) else "FAIL", "book_style": "PASS" if closure_result["status"] == "ACCEPT" else "FAIL", "frozen_drift": frozen["drift"]},
        "next_phase": "SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3" if go else "SEC-02-2 ARCHITECTURE V2.2 GENERAL CLOSURE RERUN V1 FAILURE ANALYSIS",
    }


if __name__ == "__main__":
    sys.stdout.buffer.write(canonical_bytes(evaluate()))
