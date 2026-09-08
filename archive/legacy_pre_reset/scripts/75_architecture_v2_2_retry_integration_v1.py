from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1"
PLAN = BASE / "plan/integration_plan_v2_2_retry_v1.json"
REALIZATION = BASE / "contracts/claim_realization_contract_v2_2_retry_v1.json"
PILOT_IR = ROOT / "data/book/drafting/sec_02_2/architecture_v2/pilot_2/rendered/rendered_draft_ir_v2.json"
TECHNICAL = ROOT / "data/book/drafting/sec_02_2/technical_remediation_v1/contracts/technical_claim_scope_remediation_contract_v1.json"
REGISTRY = ROOT / "data/book/drafting/technical_term_fallback_v1/contracts/technical_term_registry_v1.json"
FALLBACK_SCRIPT = ROOT / "scripts/74_technical_term_original_language_fallback_v1.py"
VALIDATOR_SCRIPT = ROOT / "scripts/54_section_draft_validator_v1_2.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fallback = _load_module("v22_retry_term_fallback", FALLBACK_SCRIPT)
validator = _load_module("v22_retry_validator_v1_2", VALIDATOR_SCRIPT)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _intent(claim_id: str, source_keys: list[str]) -> list[dict]:
    return [{"claim_id": claim_id, "source_keys": list(source_keys)}]


def _source_unit(item: dict, source_index: dict[str, dict]) -> dict:
    sources = [source_index[unit_id] for unit_id in item["source_unit_ids"]]
    claim_ids = list(dict.fromkeys(claim for source in sources for claim in source["claim_ids"]))
    if len(claim_ids) != 1:
        raise ValueError(f"source-unit composition must remain one-claim: {claim_ids}")
    source_keys = item.get("citation_override") or list(dict.fromkeys(
        key for source in sources for key in source["source_keys"]))
    return {
        "unit_id": item["unit_id"], "unit_type": "PARAGRAPH_SENTENCE",
        "text": " ".join(source["text"] for source in sources), "material": True,
        "claim_ids": claim_ids, "source_keys": source_keys,
        "relationship_type": "INDEPENDENT",
        "citation_intents": _intent(claim_ids[0], source_keys),
    }


def _technical_unit(item: dict, technical: dict) -> dict:
    claim = next(row for row in technical["new_claims"] if row["claim_id"] == item["claim_id"])
    source_keys = [claim["source_key"]]
    return {
        "unit_id": item["unit_id"], "unit_type": "PARAGRAPH_SENTENCE",
        "text": claim["canonical_claim"], "material": True,
        "claim_ids": [claim["claim_id"]], "source_keys": source_keys,
        "relationship_type": "SOURCE_SUPPORTED_RELATION",
        "citation_intents": _intent(claim["claim_id"], source_keys),
    }


def _join_terms(values: list[str], rule: dict) -> str:
    if len(values) == 1:
        return values[0] + rule["suffix"]
    return rule["separator"].join(values[:-1]) + rule["final_separator"] + values[-1] + rule["suffix"]


def _case_unit(item: dict, realization: dict, term_index: dict[str, dict], projected: bool) -> dict:
    entry = realization["case_scope_resolution"]
    records = [term_index[term_id] for term_id in entry["term_ids"]]
    if projected:
        records = [record for record in records if record["status"] == "AUTHORITATIVE_TRANSLATION"]
        values = [fallback.semantic_value(record) for record in records]
    else:
        values = [fallback.render_term(record) for record in records]
    source_keys = list(item["source_keys"])
    return {
        "unit_id": item["unit_id"], "unit_type": "PARAGRAPH_SENTENCE",
        "text": _join_terms(values, entry["enumeration"]), "material": True,
        "claim_ids": [item["claim_id"]], "source_keys": source_keys,
        "relationship_type": "INDEPENDENT",
        "citation_intents": _intent(item["claim_id"], source_keys),
    }


def build(projected: bool = False) -> tuple[dict, list[dict]]:
    plan, realization = load(PLAN), load(REALIZATION)
    pilot = load(PILOT_IR)
    source_index = {unit["unit_id"]: unit for unit in pilot["units"]}
    technical = load(TECHNICAL)
    term_index = {entry["term_id"]: entry for entry in load(REGISTRY)["entries"]}
    units, layout = [], []
    for subsection in plan["subsections"]:
        layout.append({"kind": "SUBSECTION_HEADING", "text": subsection["heading"]})
        for item in subsection["items"]:
            if item["kind"] == "SCOPE_HEADING":
                layout.append({"kind": "SCOPE_HEADING", "text": item["heading"],
                               "binding_ids": item["binding_ids"]})
                continue
            if item["kind"] == "SOURCE_UNIT":
                unit = _source_unit(item, source_index)
            elif item["kind"] == "TECHNICAL_CLAIM":
                unit = _technical_unit(item, technical)
            elif item["kind"] == "CASE_ENUMERATION":
                unit = _case_unit(item, realization, term_index, projected)
            else:
                raise ValueError(f"unsupported integration item {item['kind']}")
            units.append(unit)
            layout.append({"kind": "MATERIAL_UNIT", "unit_id": unit["unit_id"]})
    draft = {
        "section_id": plan["section_id"],
        "draft_id": "SEC-02-2-V2-2-TECHNICAL-STYLE-RETRY-V1",
        "draft_version": "tunnelbook-rendered-draft-ir-v2.2-retry-v1",
        "language": plan["language"], "title": plan["title"], "units": units,
        "artifact_status": "V2_2_TECHNICAL_STYLE_DRAFT_ACCEPTED",
        "final_manuscript": False,
    }
    return draft, layout


def _extended_bundle():
    bundle = validator.load_bundle()
    technical = load(TECHNICAL)
    claim = deepcopy(technical["new_claims"][0])
    claim["source_keys"] = [claim.pop("source_key")]
    claim.setdefault("qualifiers", [])
    claim.setdefault("scope", {"material_scope": "shotcrete", "system_scope": "system_independent",
                               "requirement_scope": ["maximum", "conditional"]})
    bundle.allowlist[claim["claim_id"]] = claim
    bundle.composition_contract.allowlist[claim["claim_id"]] = claim
    return bundle


def validate_draft(visible: dict, projected: dict) -> dict:
    term_registry = load(REGISTRY)
    fallback_failures = []
    for unit in visible["units"]:
        if "**" not in unit["text"]:
            continue
        codes = fallback.validate_visible_language(
            unit["text"], unit["claim_ids"], unit["source_keys"], term_registry)
        fallback_failures += [{"unit_id": unit["unit_id"], "code": code} for code in codes]
    parsed = validator.parse_draft_ir(projected)
    result = validator.validate_draft(parsed, bundle=_extended_bundle())
    return {
        "status": "ACCEPT" if result.status == "ACCEPT" and not fallback_failures else "REJECT",
        "validator_version": result.validator_version,
        "failure_histogram": result.failure_histogram,
        "rejected_unit_ids": result.rejected_unit_ids,
        "rejected_units": [asdict(row) for row in result.units if row.status == "REJECT"],
        "fallback_failures": fallback_failures,
        "admitted_units": len(visible["units"]),
    }


def _citation_numbers(draft: dict) -> tuple[dict[str, int], list[str]]:
    ordered = []
    for unit in draft["units"]:
        for key in unit["source_keys"]:
            if key not in ordered:
                ordered.append(key)
    return {key: index + 1 for index, key in enumerate(ordered)}, ordered


def render_markdown(draft: dict, layout: list[dict]) -> str:
    numbers, ordered_keys = _citation_numbers(draft)
    units = {unit["unit_id"]: unit for unit in draft["units"]}
    registry = _extended_bundle().registry
    lines = ["<!-- artifact-status: V2_2_TECHNICAL_STYLE_DRAFT_ACCEPTED -->",
             f"# {draft['title']}", ""]
    paragraph_id, paragraph_parts = None, []

    def flush():
        nonlocal paragraph_parts
        if paragraph_parts:
            lines.append(" ".join(paragraph_parts))
            lines.append("")
            paragraph_parts = []

    for item in layout:
        if item["kind"] in {"SUBSECTION_HEADING", "SCOPE_HEADING"}:
            flush()
            lines.append(("## " if item["kind"] == "SUBSECTION_HEADING" else "### ") + item["text"])
            lines.append("")
            paragraph_id = None
            continue
        unit = units[item["unit_id"]]
        current = unit["unit_id"].rsplit("-S", 1)[0]
        if paragraph_id is not None and current != paragraph_id:
            flush()
        paragraph_id = current
        refs = ",".join(str(numbers[key]) for key in unit["source_keys"])
        paragraph_parts.append(f"{unit['text']}[{refs}]")
    flush()
    lines += ["## Kaynaklar", ""]
    for key in ordered_keys:
        row = registry[key]
        location = row.get("section_path") or ""
        pages = (f"s. {row['page_start']}-{row['page_end']}" if row.get("page_start") is not None
                 else "")
        detail = ", ".join(part for part in (row.get("title") or row["document_id"], location, pages) if part)
        lines.append(f"{numbers[key]}. {detail}")
    return "\n".join(lines).rstrip() + "\n"


def evaluate() -> dict:
    visible, layout = build(False)
    projected, _ = build(True)
    validation = validate_draft(visible, projected)
    markdown = render_markdown(visible, layout)
    term_records = load(REGISTRY)["entries"]
    unresolved = [record for record in term_records if record["status"] == "ORIGINAL_TERM_UNRESOLVED"]
    result = {
        "status": "GO" if validation["status"] == "ACCEPT" else "NO_GO",
        "draft_ir": visible,
        "markdown": markdown,
        "validation": validation,
        "unresolved_term_count": len(unresolved),
        "model_generation_calls": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
    }
    return result


if __name__ == "__main__":
    sys.stdout.buffer.write(canonical_bytes(evaluate()))
