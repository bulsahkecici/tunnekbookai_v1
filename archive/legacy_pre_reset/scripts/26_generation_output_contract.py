"""TunnelBookAI deterministic generation output contract v1.

An enforcement layer over the unchanged system prompt v5. It is NOT another model: every decision
is a deterministic, testable rule over the answer text plus the packet's exposed evidence IDs.

Policy is fail-closed and repair-free. The contract validates and rejects; it never rewrites an
abstention marker, never normalises a malformed citation, and never inserts a handle. Repairing
output would hide the defects it exists to surface - rewriting GEV062's opening marker, for
instance, would mask the fact that its entire body is in the wrong language.

Named 26_ because scripts/25_generation_phase_b_v2.py already occupies that slot.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_VERSION = "tunnelbook-generation-output-contract-v1"
REPAIR_POLICY = "none_fail_closed"
SUPPORTED_LANGUAGES = ("tr", "en")
MARKER_FOR_LANGUAGE = {"tr": "YETERSİZ KANIT", "en": "INSUFFICIENT EVIDENCE"}
ANY_MARKER = re.compile(r"(YETERSİZ\s+KANIT|INSUFFICIENT\s+EVIDENCE)", re.I)
MARKER_AT_START = re.compile(r"^\s*[*_#>\s]*(YETERSİZ\s+KANIT|INSUFFICIENT\s+EVIDENCE)", re.I)
THINKING_MARKERS = ("<think>", "</think>", "<|im_start|>", "<|im_end|>")
HANDLE = re.compile(r"\[E\d{3}\]")

MIN_BODY_TOKENS = 8
LANGUAGE_MARGIN = 1.5
TURKISH_CHARS = set("ğışĞİŞ")
TURKISH_WORDS = {
    "ve", "ile", "bir", "bu", "için", "gibi", "olarak", "olan", "ise", "ancak", "ayrıca", "daha",
    "veya", "göre", "kadar", "sonra", "önce", "her", "tüm", "değil", "olup", "üzere", "bulunan",
    "yapılır", "edilir", "olmalıdır", "gerekir", "kullanılır", "verilmiştir", "belirtilen",
    "sağlanır", "arasında", "içinde", "nedeniyle", "şekilde", "vardır", "yoktur", "ilgili",
}
ENGLISH_WORDS = {
    "the", "and", "of", "to", "in", "for", "on", "with", "is", "are", "be", "as", "by", "from",
    "that", "this", "these", "those", "which", "such", "shall", "must", "should", "not", "than",
    "when", "where", "while", "their", "they", "it", "its", "at", "or", "can", "may", "used",
    "provided", "between", "during", "according", "however", "also", "each", "both",
}


class ContractConfigError(RuntimeError):
    """The contract cannot be applied under the given inputs."""


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gen = _load("generation_eval", "scripts/21_generation_model_eval.py")
VALIDATOR_VERSION = gen.VALIDATOR_VERSION


def implementation_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _strip_non_lexical(text: str) -> str:
    """Remove everything carrying no language signal: handles, numbers, units, acronyms, symbols."""
    out = HANDLE.sub(" ", text)
    out = re.sub(r"https?://\S+", " ", out)
    out = re.sub(r"[A-Z]{2,}(?:[ -]?\d+)?(?:[/-]\d+)*", " ", out)
    out = re.sub(r"\b\d+(?:[.,]\d+)?\s*(?:cm|mm|m|km|kg/m³|kg/m3|MPa|kN|ppm|%|psi|ft|in)\b", " ", out)
    out = re.sub(r"\d+(?:[.,]\d+)?", " ", out)
    out = re.sub(r"[^\w\sçğıöşüâîûÇĞİÖŞÜ]", " ", out)
    return out


def detect_language(text: str) -> dict[str, Any]:
    """Deterministic tr/en identification with an explicit ambiguous verdict. Never guesses."""
    lexical = _strip_non_lexical(text)
    tokens = [t for t in lexical.lower().split() if t]
    if len(tokens) < MIN_BODY_TOKENS:
        return {"language": None, "status": "insufficient_text", "tokens": len(tokens),
                "turkish_score": 0.0, "english_score": 0.0}
    turkish_chars = sum(1 for ch in lexical if ch in TURKISH_CHARS)
    turkish_hits = sum(1 for t in tokens if t in TURKISH_WORDS)
    english_hits = sum(1 for t in tokens if t in ENGLISH_WORDS)
    turkish_score = turkish_hits + 2.0 * min(turkish_chars, len(tokens))
    english_score = float(english_hits)
    if turkish_score == 0 and english_score == 0:
        return {"language": None, "status": "ambiguous", "tokens": len(tokens),
                "turkish_score": 0.0, "english_score": 0.0}
    if turkish_score >= english_score * LANGUAGE_MARGIN:
        language, status = "tr", "confident"
    elif english_score >= turkish_score * LANGUAGE_MARGIN:
        language, status = "en", "confident"
    else:
        language, status = None, "ambiguous"
    return {"language": language, "status": status, "tokens": len(tokens),
            "turkish_score": round(turkish_score, 2), "english_score": round(english_score, 2)}


def _body_after_marker(answer: str) -> str:
    stripped = answer.lstrip()
    match = MARKER_AT_START.match(stripped)
    return stripped[match.end():] if match else stripped


def _segment(answer: str) -> list[str]:
    text = re.sub(r"\r", "", answer)
    parts = [b.strip() for b in re.split(r"\n(?=\s*(?:[-*•]|\d{1,2}[.)]))|\n{2,}", text) if b.strip()]
    return [re.sub(r"\s+", " ", b).strip() for b in parts if len(b.strip()) >= 12]


def _is_material(block: str) -> bool:
    stripped = block.strip()
    if MARKER_AT_START.match(stripped) and len(stripped.split()) < 8:
        return False
    if re.search(r":\s*$", stripped) and not HANDLE.search(stripped):
        return False
    body = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", stripped)
    lexical = _strip_non_lexical(body)
    return len([t for t in lexical.split() if len(t) > 3]) >= 4 or bool(re.search(r"\d", body))


def coverage_telemetry(answer: str):
    """Coverage is measured and reported, never enforced and never repaired."""
    material = [b for b in _segment(answer) if _is_material(b)]
    cited = [b for b in material if HANDLE.search(b)]
    ratio = round(len(cited) / len(material), 4) if material else None
    return len(material), len(cited), ratio


@dataclass
class ContractResult:
    contract_version: str
    contract_sha256: str
    validator_version: str
    repair_policy: str
    raw_answer_sha: str
    query_language: str | None
    query_language_status: str
    abstention_detected: bool
    expected_abstention_marker: str | None
    actual_abstention_marker: str | None
    marker_at_start: bool | None
    marker_language_valid: bool | None
    answer_body_language: str | None
    answer_body_language_status: str
    body_language_valid: bool | None
    malformed_citations: list
    unknown_handles: list
    citation_syntax_valid: bool
    doc_leaks: list
    page_leaks: list
    slide_leaks: list
    path_leaks: list
    template_leaks: list
    thinking_marker_leaks: list
    material_claim_count: int
    claims_with_citation: int
    citation_coverage: float | None
    citation_coverage_status: str
    contract_valid: bool
    failure_reasons: list

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def enforce(answer: str, query_language: str | None, exposed_evidence_ids,
            answerability: str | None = None) -> ContractResult:
    """Validate one generated answer. Returns a verdict; never modifies the answer."""
    if query_language is not None and query_language not in SUPPORTED_LANGUAGES:
        raise ContractConfigError(f"unsupported query language {query_language!r}; "
                                  f"supported: {SUPPORTED_LANGUAGES}")
    reasons: list[str] = []

    if query_language is None:
        detected = detect_language(answer)
        query_language, query_language_status = detected["language"], f"inferred_{detected['status']}"
        if query_language is None:
            reasons.append("query_language_ambiguous")
    else:
        query_language_status = "provided"

    if not answer.strip():
        reasons.append("empty_answer")

    citations = gen.validate_citations(answer, set(exposed_evidence_ids))
    malformed, unknown = citations["malformed_citations"], citations["unknown_handles"]
    if malformed:
        reasons.append("malformed_citation")
    if unknown:
        reasons.append("unknown_citation")
    for field_name, reason in (("doc_leaks", "source_coordinate_leak"),
                               ("page_leaks", "source_coordinate_leak"),
                               ("slide_leaks", "source_coordinate_leak"),
                               ("path_leaks", "source_coordinate_leak"),
                               ("template_leaks", "template_leak")):
        if citations[field_name] and reason not in reasons:
            reasons.append(reason)
    leaks = [m for m in THINKING_MARKERS if m in answer]
    if leaks:
        reasons.append("thinking_marker_leak")

    found = ANY_MARKER.search(answer)
    actual_marker = None
    if found:
        actual_marker = ("YETERSİZ KANIT" if found.group(1).upper().startswith("YET")
                         else "INSUFFICIENT EVIDENCE")
    at_start = bool(MARKER_AT_START.match(answer.lstrip())) if found else None
    abstained = bool(at_start)
    expected_marker = MARKER_FOR_LANGUAGE.get(query_language) if query_language else None
    marker_valid = None
    if abstained:
        marker_valid = actual_marker == expected_marker
        if not marker_valid:
            reasons.append("wrong_abstention_marker_language")
    elif found and at_start is False:
        reasons.append("abstention_marker_not_at_start")

    body = _body_after_marker(answer)
    detected_body = detect_language(body)
    body_language, body_status = detected_body["language"], detected_body["status"]
    body_valid = None
    if body_status == "confident" and query_language:
        body_valid = body_language == query_language
        if not body_valid:
            reasons.append("answer_body_language_mismatch")
    elif body_status == "ambiguous" and query_language:
        reasons.append("answer_body_language_ambiguous")

    material, cited, coverage = coverage_telemetry(answer)

    return ContractResult(
        contract_version=CONTRACT_VERSION, contract_sha256=implementation_sha256(),
        validator_version=VALIDATOR_VERSION, repair_policy=REPAIR_POLICY,
        raw_answer_sha=hashlib.sha256(answer.encode("utf-8")).hexdigest(),
        query_language=query_language, query_language_status=query_language_status,
        abstention_detected=abstained, expected_abstention_marker=expected_marker,
        actual_abstention_marker=actual_marker, marker_at_start=at_start,
        marker_language_valid=marker_valid, answer_body_language=body_language,
        answer_body_language_status=body_status, body_language_valid=body_valid,
        malformed_citations=malformed, unknown_handles=unknown,
        citation_syntax_valid=not malformed and not unknown,
        doc_leaks=citations["doc_leaks"], page_leaks=citations["page_leaks"],
        slide_leaks=citations["slide_leaks"], path_leaks=citations["path_leaks"],
        template_leaks=citations["template_leaks"], thinking_marker_leaks=leaks,
        material_claim_count=material, claims_with_citation=cited, citation_coverage=coverage,
        citation_coverage_status="telemetry_only_not_enforced",
        contract_valid=not reasons, failure_reasons=reasons)


if __name__ == "__main__":
    print(json.dumps({"contract_version": CONTRACT_VERSION,
                      "implementation_sha256": implementation_sha256(),
                      "validator_version": VALIDATOR_VERSION,
                      "repair_policy": REPAIR_POLICY,
                      "supported_languages": list(SUPPORTED_LANGUAGES),
                      "marker_mapping": MARKER_FOR_LANGUAGE}, indent=2, ensure_ascii=False))
