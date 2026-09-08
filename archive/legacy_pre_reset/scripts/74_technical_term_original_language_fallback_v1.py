from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/technical_term_fallback_v1"
CONTRACT_PATH = BASE / "contracts/technical_term_original_language_fallback_contract_v1.json"
REGISTRY_PATH = BASE / "contracts/technical_term_registry_v1.json"
LANGUAGE_PATH = ROOT / "scripts/51_draft_language_validator_v1.py"
MARKDOWN_RE = re.compile(r"\*\*(.+?)\*\*")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


language = _load_module("fallback_parent_language_validator", LANGUAGE_PATH)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def registry_index(registry: dict | None = None) -> dict[str, dict]:
    payload = registry or load_json(REGISTRY_PATH)
    return {entry["term_id"]: entry for entry in payload["entries"]}


def validate_policy(contract: dict | None = None) -> list[str]:
    payload = contract or load_json(CONTRACT_PATH)
    constraints = payload["implementation_constraints"]
    if constraints["claim_specific_branches"] or constraints["term_specific_branches"]:
        return ["TERM_CLAIM_SPECIFIC_BRANCH_FORBIDDEN"]
    return []


def validate_record(candidate: dict, registered: dict) -> list[str]:
    required = load_json(CONTRACT_PATH)["required_record_fields"]
    if any(field not in candidate for field in required):
        return ["TERM_SCHEMA_INVALID"]
    status = candidate["status"]
    if status not in {"AUTHORITATIVE_TRANSLATION", "ORIGINAL_TERM_UNRESOLVED"}:
        return ["TERM_STATUS_INVALID"]
    values = [candidate["canonical_source_term"], candidate.get("authoritative_translation")]
    if any(value and ("**" in value or "__" in value) for value in values):
        return ["TERM_MARKDOWN_IN_SEMANTIC_VALUE"]
    if (candidate["canonical_source_term"] != registered["canonical_source_term"] or
            sha256_text(candidate["canonical_source_term"]) != registered["canonical_source_term_sha256"]):
        return ["TERM_SOURCE_TERM_MISMATCH"]
    if candidate["semantic_effect"] != "lexical_identity_only":
        return ["TERM_CLAIM_MEANING_CHANGED"]
    if candidate["claim_ids"] != registered["claim_ids"]:
        return ["TERM_CROSS_CLAIM_BORROWING"]
    if candidate["source_keys"] != registered["source_keys"]:
        return ["TERM_SOURCE_OWNERSHIP_MISMATCH"]
    if status == "ORIGINAL_TERM_UNRESOLVED":
        if candidate["authoritative_translation"] is not None:
            return ["TERM_UNRESOLVED_HAS_TRANSLATION"]
        if candidate["display_mode"] != "BOLD":
            return ["TERM_DISPLAY_MODE_MISMATCH"]
    else:
        if candidate["authoritative_translation"] is None:
            return ["TERM_AUTHORITATIVE_TRANSLATION_REQUIRED"]
        if candidate["authoritative_translation"] != registered["authoritative_translation"]:
            return ["TERM_AUTHORITATIVE_TRANSLATION_MISMATCH"]
        if candidate["display_mode"] != "PLAIN":
            return ["TERM_DISPLAY_MODE_MISMATCH"]
    return []


def semantic_value(record: dict) -> str:
    if record["status"] == "AUTHORITATIVE_TRANSLATION":
        return record["authoritative_translation"]
    return record["canonical_source_term"]


def render_term(record: dict) -> str:
    value = semantic_value(record)
    return f"**{value}**" if record["display_mode"] == "BOLD" else value


def validate_presentation(record: dict, visible: str) -> list[str]:
    expected = render_term(record)
    if visible == expected:
        return []
    if record["status"] == "ORIGINAL_TERM_UNRESOLVED" and visible == record["canonical_source_term"]:
        return ["TERM_UNRESOLVED_MARKER_MISSING"]
    return ["TERM_SILENT_REPLACEMENT"]


def validate_ownership_value(record: dict, supplied_value: str) -> list[str]:
    if "**" in supplied_value or "__" in supplied_value:
        return ["TERM_PRESENTATION_CONTAMINATES_OWNERSHIP"]
    return [] if supplied_value == semantic_value(record) else ["TERM_SILENT_REPLACEMENT"]


def validate_visible_language(text: str, claim_ids: list[str], source_keys: list[str],
                              registry: dict | None = None) -> list[str]:
    entries = list(registry_index(registry).values())
    unresolved = [entry for entry in entries if entry["status"] == "ORIGINAL_TERM_UNRESOLVED"]
    masked = text
    for span in MARKDOWN_RE.findall(text):
        matches = [entry for entry in unresolved if entry["canonical_source_term"] == span]
        if not matches:
            return ["TERM_UNREGISTERED_VISIBLE_TERM"]
        record = matches[0]
        if not set(claim_ids).issubset(record["claim_ids"]):
            return ["TERM_CROSS_CLAIM_BORROWING"]
        if not set(source_keys).issubset(record["source_keys"]):
            return ["TERM_SOURCE_OWNERSHIP_MISMATCH"]
        masked = masked.replace(f"**{span}**", "FHWA")
    for record in unresolved:
        if record["canonical_source_term"] in masked:
            return ["TERM_UNRESOLVED_MARKER_MISSING"]
    failures = language.validate_unit(
        unit_id="TERM-FALLBACK-CHECK", unit_type="sentence", material=True,
        section_language="tr", text=masked, claim_ids=claim_ids)
    return [failure.code for failure in failures]


def latest_resolution(entries: list[dict], term_id: str) -> dict:
    candidates = [deepcopy(entry) for entry in entries if entry["term_id"] == term_id]
    if not candidates:
        raise KeyError(term_id)
    return max(candidates, key=lambda entry: entry["resolution_version"])


def evaluate_negative_fixture(fixture: dict, registry: dict | None = None) -> str:
    index = registry_index(registry)
    operation = fixture["operation"]
    if operation == "record":
        baseline = index[fixture["term_id"]]
        candidate = deepcopy(baseline)
        candidate.update(fixture["mutation"])
        codes = validate_record(candidate, baseline)
    elif operation == "presentation":
        record = index[fixture["term_id"]]
        codes = validate_presentation(record, fixture["visible"])
    elif operation == "ownership":
        record = index[fixture["term_id"]]
        codes = validate_ownership_value(record, fixture["supplied_value"])
    elif operation == "language":
        codes = validate_visible_language(
            fixture["text"], fixture["claim_ids"], fixture["source_keys"], registry)
    elif operation == "policy":
        contract = load_json(CONTRACT_PATH)
        contract.update(fixture["mutation"])
        codes = validate_policy(contract)
    else:
        codes = ["TERM_SCHEMA_INVALID"]
    return codes[0] if codes else "ACCEPT"


def evaluate() -> dict:
    registry = load_json(REGISTRY_PATH)
    index = registry_index(registry)
    records = []
    for term_id in sorted(index):
        record = index[term_id]
        records.append({
            "term_id": term_id,
            "status": record["status"],
            "semantic_value": semantic_value(record),
            "visible_value": render_term(record),
            "validation_codes": validate_record(record, record),
        })
    return {"status": "GO", "policy_codes": validate_policy(), "records": records}


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


if __name__ == "__main__":
    sys.stdout.buffer.write(canonical_bytes(evaluate()))
