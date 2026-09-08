from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urlparse


PROMPT_VERSION = "metadata-suggestion-v2.2"
FIELDS = ("title", "organization", "year", "language", "document_type", "authority_level", "topics")
CONFIDENCES = {"high", "medium", "low"}
LANGUAGES = {"tr", "en", "de", "mixed", "unknown"}
AUTHORITY_LEVELS = {"A", "B", "C", "D", "unclassified"}
DOCUMENT_TYPES = {
    "regulation", "technical_specification", "standard", "manual", "handbook",
    "academic_article", "thesis", "conference_paper", "conference_proceedings",
    "technical_report", "presentation", "training_material", "project_document",
    "inspection_form", "cost_analysis", "inventory", "web_article", "magazine",
    "book_or_book_chapter", "drawing", "spreadsheet", "other", "unknown",
}
TOPICS = {
    "tunnel_general", "natm", "tbm", "geotechnical_investigation", "geology",
    "rock_mechanics", "route_selection", "excavation", "blasting", "shotcrete",
    "steel_mesh", "steel_rib", "rock_bolt", "forepoling", "support_systems",
    "ground_improvement", "jet_grouting", "injection", "karst", "water", "gas",
    "drainage", "waterproofing", "final_lining", "fiber_reinforced_concrete", "portal",
    "monitoring", "instrumentation", "risk", "safety", "fire_safety", "ventilation",
    "traffic", "operations", "maintenance", "inspection", "regulation", "standards",
    "cost", "unit_price", "payment", "contracts", "construction_management",
    "quality_control", "accident", "collapse", "case_study", "history", "inventory",
}
MISSING = {"", "unknown", "unclassified", "null", "none"}
OUTPUT_FIELDS = [
    "document_id", "field", "current_value", "deterministic_suggestion", "llm_suggestion",
    "llm_evidence", "llm_confidence", "agreement_status", "requires_human_review",
    "model", "prompt_version", "source_sha256", "processed_at",
]
QUEUE_FIELDS = [
    "priority", "document_id", "source_relative_path", "field", "current_value",
    "deterministic_suggestion", "llm_suggestion", "evidence", "confidence",
    "agreement_status", "reviewer_value", "reviewer_note", "review_status", "reviewed_at",
]
CURRENT_COLUMN = {
    "title": "", "organization": "", "year": "year_current", "language": "language_current",
    "document_type": "document_type_current", "authority_level": "authority_level_current",
    "topics": "topics_current",
}
DETERMINISTIC_COLUMN = {
    "title": "title_suggested", "organization": "organization_suggested", "year": "year_suggested",
    "language": "language_suggested", "document_type": "document_type_suggested",
    "authority_level": "authority_level_suggested", "topics": "topics_suggested",
}
CONFIDENCE_COLUMN = {
    "title": "", "organization": "", "year": "year_confidence", "language": "language_confidence",
    "document_type": "document_type_confidence", "authority_level": "authority_confidence",
    "topics": "topics_confidence",
}


class LLMReviewError(RuntimeError):
    pass


class InvalidStructuredOutput(LLMReviewError):
    pass


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(rows: Iterable[dict[str, object]], fields: list[str]) -> bytes:
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return False
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return True


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_yaml(path: Path) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip("'\"")
        if value.casefold() in {"true", "false"}:
            result[key.strip()] = value.casefold() == "true"
        elif re.fullmatch(r"-?\d+", value):
            result[key.strip()] = int(value)
        elif re.fullmatch(r"-?\d+\.\d+", value):
            result[key.strip()] = float(value)
        else:
            result[key.strip()] = value
    return result


def assert_local_endpoint(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise LLMReviewError("Yalnız local HTTP OpenAI-compatible endpoint kullanılabilir")


def strip_front_matter(text: str) -> str:
    match = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n?", text, flags=re.DOTALL)
    return text[match.end():] if match else text


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", (text or "").casefold())
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def meaningful_headings(body: str) -> list[str]:
    headings = []
    for line in body.splitlines():
        match = re.match(r"^#{1,4}\s+(.+?)\s*$", line.strip())
        if match and len(match.group(1).split()) <= 40:
            headings.append(match.group(1).strip())
    return headings[:20]


def context_package(row: dict[str, str], markdown: str) -> dict[str, object]:
    body = strip_front_matter(markdown)
    words = body.split()
    # Word targets preserve the requested semantic window, while deterministic
    # character caps prevent dense OCR text from exceeding a locally loaded
    # model's context window.
    first = " ".join(words[:2000])[:12000].rstrip()
    tail = " ".join(words[-750:]) if len(words) > 2000 else ""
    if len(tail) > 4000:
        tail = tail[-4000:].lstrip()
    requested = fields_requiring_llm(row)
    return {
        "document_id": row["document_id"],
        "filename": row["source_filename"],
        "relative_path": row["source_relative_path"],
        "source_extension": row["source_extension"],
        "current_metadata": {field: current_value(row, field) for field in FIELDS},
        "deterministic_suggestions": {field: deterministic_value(row, field) for field in FIELDS},
        "requested_fields": requested,
        "headings": meaningful_headings(body),
        "first_excerpt": first,
        "tail_publication_or_references_excerpt": tail,
    }


def missing(value: object) -> bool:
    if isinstance(value, list):
        return not value
    return str(value or "").strip().casefold() in MISSING


def current_value(row: dict[str, str], field: str) -> str:
    column = CURRENT_COLUMN[field]
    return row.get(column, "") if column else ""


def deterministic_value(row: dict[str, str], field: str) -> str:
    return row.get(DETERMINISTIC_COLUMN[field], "")


def title_is_weak(value: str, filename: str) -> bool:
    normalized = normalize(value)
    stem = normalize(Path(filename).stem)
    return not normalized or normalized == stem and (len(normalized) < 5 or bool(re.fullmatch(r"[\d _-]+", Path(filename).stem)))


def fields_requiring_llm(row: dict[str, str]) -> list[str]:
    requested = []
    for field in FIELDS:
        current = current_value(row, field)
        deterministic = deterministic_value(row, field)
        confidence_column = CONFIDENCE_COLUMN[field]
        confidence = row.get(confidence_column, "") if confidence_column else ""
        verified = not missing(current)
        if verified:
            continue
        if field == "authority_level" and (confidence in {"medium", "low"} or deterministic == "unclassified"):
            requested.append(field)
        elif field == "document_type" and (confidence == "low" or deterministic == "unknown"):
            requested.append(field)
        elif field == "year" and (missing(deterministic) or confidence == "low"):
            requested.append(field)
        elif field == "organization" and missing(deterministic):
            requested.append(field)
        elif field == "title" and title_is_weak(deterministic, row["source_filename"]):
            requested.append(field)
        elif field == "language" and deterministic in {"mixed", "unknown", ""}:
            requested.append(field)
        elif field == "topics" and (missing(deterministic) or confidence == "low"):
            requested.append(field)
    return requested


def system_prompt() -> str:
    return f"""You are a conservative metadata suggestion engine. Return exactly one JSON object and nothing else.
Never invent an author, organization, year, title, or authority. Evidence must be a short verbatim or directly checkable phrase from the supplied headings/excerpts, not merely a filename claim. If evidence is absent, use an unknown/empty value with low confidence.
Authority A requires strong in-document proof that the document itself is an official KGM, Resmi Gazete/mevzuat, FHWA, PIARC, official technical specification, or official institutional manual. A filename alone is never sufficient. Thesis/academic article is normally B; professional training/presentation C; Wikipedia/general web D; otherwise unclassified.
For fields not listed in requested_fields, copy the supplied current/deterministic value and use evidence='not_requested'.
Allowed confidence: high, medium, low.
Allowed language: {', '.join(sorted(LANGUAGES))}.
Allowed authority_level: {', '.join(sorted(AUTHORITY_LEVELS))}.
Allowed document_type: {', '.join(sorted(DOCUMENT_TYPES))}.
Allowed topics: {', '.join(sorted(TOPICS))}.
Required schema: every key title, organization, year, language, document_type, authority_level, topics maps to an object with value, confidence, evidence. Topics value is an array. Year value is a four-digit integer or null. All other values are strings."""


def parse_structured_json(raw: str) -> dict[str, dict[str, object]]:
    stripped = raw.strip()
    fence = re.fullmatch(r"```(?:json)?\s*\n(?P<body>.*?)\n?```", stripped, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        stripped = fence.group("body").strip()
    if not stripped.startswith("{") or not stripped.endswith("}") or "```" in stripped:
        raise InvalidStructuredOutput("Yanıt saf JSON nesnesi değil")
    try:
        result = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise InvalidStructuredOutput(f"Geçersiz JSON: {exc}") from exc
    if not isinstance(result, dict) or set(result) != set(FIELDS):
        raise InvalidStructuredOutput("JSON alanları zorunlu schema ile eşleşmiyor")
    for field in FIELDS:
        item = result[field]
        if not isinstance(item, dict) or set(item) != {"value", "confidence", "evidence"}:
            raise InvalidStructuredOutput(f"{field} nesnesi value/confidence/evidence içermeli")
        if item["confidence"] not in CONFIDENCES or not isinstance(item["evidence"], str):
            raise InvalidStructuredOutput(f"{field} confidence/evidence geçersiz")
        if field == "topics" and not isinstance(item["value"], list):
            raise InvalidStructuredOutput("topics.value array olmalı")
    return result


def evidence_grounded(evidence: str, package: dict[str, object]) -> bool:
    if evidence == "not_requested":
        return True
    source = normalize(" ".join([
        " ".join(package.get("headings", [])), str(package.get("first_excerpt", "")),
        str(package.get("tail_publication_or_references_excerpt", "")),
    ]))
    tokens = [token for token in normalize(evidence).split() if len(token) >= 4]
    if not tokens:
        return False
    return sum(token in source for token in tokens) / len(tokens) >= 0.6


def value_supported_by_evidence(field: str, value: object, evidence: str) -> bool:
    if missing(value):
        return True
    evidence_normalized = normalize(evidence)
    if field == "year":
        return str(value) in evidence
    if field not in {"title", "organization"}:
        return True
    tokens = [token for token in normalize(str(value)).split() if len(token) >= 3]
    return bool(tokens) and sum(token in evidence_normalized for token in tokens) / len(tokens) >= 0.6


def validated_item(field: str, item: dict[str, object], package: dict[str, object]) -> dict[str, object]:
    value = item["value"]
    confidence = str(item["confidence"])
    evidence = str(item["evidence"]).strip()
    invalid = False
    if field == "language" and value not in LANGUAGES:
        value, invalid = "unknown", True
    elif field == "document_type" and value not in DOCUMENT_TYPES:
        value, invalid = "unknown", True
    elif field == "authority_level" and value not in AUTHORITY_LEVELS:
        value, invalid = "unclassified", True
    elif field == "topics":
        filtered = sorted({str(topic) for topic in value if str(topic) in TOPICS})
        invalid = len(filtered) != len(value)
        value = filtered
    elif field == "year":
        if value is not None and (not isinstance(value, int) or not 1800 <= value <= 2100):
            value, invalid = None, True
    elif field in {"title", "organization"} and not isinstance(value, str):
        value, invalid = "", True
    grounded = evidence_grounded(evidence, package)
    value_grounded = value_supported_by_evidence(field, value, evidence)
    if invalid or not grounded or not value_grounded:
        confidence = "low"
        if invalid:
            suffix = "controlled_vocabulary_rejected"
        elif not grounded:
            suffix = "evidence_not_grounded_in_context"
        else:
            suffix = "suggested_value_not_supported_by_evidence"
        evidence = f"{evidence} [{suffix}]".strip()
    if field == "authority_level" and value in {"A", "B", "C", "D"}:
        evidence_source = normalize(evidence)
        authority_patterns = {
            "A": r"karayollari genel mudurlugu|(?:^| )kgm(?: |$)|resmi gazete|mevzuat|federal highway administration|(?:^| )fhwa(?: |$)|world road association|(?:^| )piarc(?: |$)|teknik sartname|technical specification",
            "B": r"academic|university|universit|thesis|doctoral|master s degree|peer reviewed|journal article|scientific paper",
            "C": r"professional|industry|training|course|seminar|presentation|workshop|egitim|kurs|seminer|sunum",
            "D": r"wikipedia|web article|blog|secondary source|general web",
        }
        supported = re.search(authority_patterns[str(value)], evidence_source)
        if not supported or not grounded:
            value, confidence = "unclassified", "low"
            evidence = f"{evidence} [authority_{item['value']}_evidence_class_mismatch]".strip()
    return {"value": value, "confidence": confidence, "evidence": evidence}


def validate_response(response: dict[str, dict[str, object]], package: dict[str, object]) -> dict[str, dict[str, object]]:
    return {field: validated_item(field, response[field], package) for field in FIELDS}


Transport = Callable[[str, dict[str, object], int], str]


def structured_response_format() -> dict[str, object]:
    scalar = {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
            "confidence": {"type": "string", "enum": sorted(CONFIDENCES)},
            "evidence": {"type": "string"},
        },
        "required": ["value", "confidence", "evidence"],
        "additionalProperties": False,
    }
    properties: dict[str, object] = {field: dict(scalar) for field in FIELDS}
    properties["year"] = {
        **scalar,
        "properties": {**scalar["properties"], "value": {"anyOf": [{"type": "integer"}, {"type": "null"}]}},
    }
    properties["language"] = {
        **scalar, "properties": {**scalar["properties"], "value": {"type": "string"}}
    }
    properties["document_type"] = {
        **scalar, "properties": {**scalar["properties"], "value": {"type": "string"}}
    }
    properties["authority_level"] = {
        **scalar, "properties": {**scalar["properties"], "value": {"type": "string"}}
    }
    properties["topics"] = {
        **scalar,
        "properties": {
            **scalar["properties"],
            "value": {"type": "array", "items": {"type": "string"}},
        },
    }
    schema = {"type": "object", "properties": properties, "required": list(FIELDS), "additionalProperties": False}
    return {"type": "json_schema", "json_schema": {"name": "metadata_suggestions", "strict": True, "schema": schema}}


def http_transport(url: str, payload: dict[str, object], timeout: int) -> str:
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))
    message = result["choices"][0]["message"]
    content = str(message.get("content") or "").strip()
    # Some LM Studio reasoning models place schema-constrained JSON in
    # reasoning_content. It is accepted only when content is empty; the normal
    # strict parser still rejects prose or mixed reasoning.
    if not content:
        content = str(message.get("reasoning_content") or "").strip()
    return content


def call_with_retry(base_url: str, model: str, package: dict[str, object], temperature: float,
                    timeout: int, max_retries: int, transport: Transport = http_transport) -> tuple[dict[str, dict[str, object]], int]:
    payload = {
        "model": model, "temperature": temperature,
        "messages": [{"role": "system", "content": system_prompt()},
                     {"role": "user", "content": json.dumps(package, ensure_ascii=False)}],
        "response_format": structured_response_format(),
    }
    retries = 0
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            raw = transport(base_url.rstrip("/") + "/chat/completions", payload, timeout)
            return validate_response(parse_structured_json(raw), package), retries
        except (InvalidStructuredOutput, KeyError, TypeError, ValueError, urllib.error.HTTPError,
                urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            retries += 1
            time.sleep(min(0.25 * retries, 0.5))
    raise InvalidStructuredOutput(f"Structured JSON retry tükendi: {last_error}")


def discover_model(base_url: str, timeout: int, preferred: str = "") -> str:
    request = urllib.request.Request(base_url.rstrip("/") + "/models", method="GET")
    with urllib.request.urlopen(request, timeout=min(timeout, 10)) as response:
        payload = json.loads(response.read().decode("utf-8"))
    models = [str(item.get("id", "")).strip() for item in payload.get("data", []) if item.get("id")]
    if not models:
        raise LLMReviewError("Local endpoint açık ancak yüklü model bildirmedi")
    if preferred:
        exact = next((item for item in models if item == preferred), "")
        if exact:
            return exact
        normalized = normalize(preferred)
        equivalent = [item for item in models if normalize(item) == normalized]
        if len(equivalent) == 1:
            return equivalent[0]
        raise LLMReviewError(f"Yapılandırılmış model endpoint'te yok: {preferred}")
    return models[0]


def cache_identity(row: dict[str, str], model: str) -> str:
    identity = "\0".join((row["document_id"], row["source_sha256"], model, PROMPT_VERSION))
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def cache_path(root: Path, row: dict[str, str], model: str) -> Path:
    return root / "data/metadata/cache/metadata_llm" / row["document_id"] / f"{cache_identity(row, model)}.json"


def read_cache(path: Path, document: dict[str, str] | None = None, model: str = "") -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if payload.get("prompt_version") != PROMPT_VERSION:
        return None
    if document is not None and (
        payload.get("document_id") != document["document_id"]
        or payload.get("source_sha256") != document["source_sha256"]
        or payload.get("model") != model
    ):
        return None
    return payload


def agreement(field: str, current: str, deterministic: str, llm_value: object, llm_confidence: str) -> str:
    if not missing(current):
        return "existing_verified"
    llm_text = "|".join(llm_value) if isinstance(llm_value, list) else "" if llm_value is None else str(llm_value)
    if missing(llm_text):
        return "unresolved"
    if missing(deterministic):
        return "llm_only"
    if field == "topics":
        agrees = set(filter(None, deterministic.split("|"))) == set(filter(None, llm_text.split("|")))
    else:
        agrees = normalize(deterministic) == normalize(llm_text)
    return "deterministic_llm_agree" if agrees else "deterministic_llm_conflict"


def review_priority(row: dict[str, str]) -> str:
    field, status = row["field"], row["agreement_status"]
    deterministic, llm = row["deterministic_suggestion"], row["llm_suggestion"]
    if status in {"deterministic_llm_conflict", "unresolved"}:
        return "P0"
    if field == "authority_level" and {deterministic, llm} & {"A", "B"} and deterministic != llm:
        return "P0"
    if field in {"authority_level", "document_type", "organization", "title", "year"}:
        return "P1"
    return "P2"


def base_rows(master: list[dict[str, str]], model: str) -> list[dict[str, str]]:
    # The result CSV represents fields actually requested from the LLM only.
    # Verified/high-confidence deterministic fields are counted in the audit but not re-predicted.
    return []


def suggestion_rows_for_document(document: dict[str, str], response: dict[str, dict[str, object]], model: str,
                                 processed_at: str) -> list[dict[str, str]]:
    rows = []
    for field in fields_requiring_llm(document):
        item = response[field]
        value = "|".join(item["value"]) if isinstance(item["value"], list) else "" if item["value"] is None else str(item["value"])
        current = current_value(document, field)
        deterministic = deterministic_value(document, field)
        status = agreement(field, current, deterministic, item["value"], str(item["confidence"]))
        requires_review = status != "deterministic_llm_agree" or item["confidence"] != "high"
        rows.append({
            "document_id": document["document_id"], "field": field, "current_value": current,
            "deterministic_suggestion": deterministic, "llm_suggestion": value,
            "llm_evidence": str(item["evidence"]), "llm_confidence": str(item["confidence"]),
            "agreement_status": status, "requires_human_review": str(requires_review).lower(),
            "model": model, "prompt_version": PROMPT_VERSION,
            "source_sha256": document["source_sha256"], "processed_at": processed_at,
        })
    return rows


def unresolved_rows(document: dict[str, str], model: str, reason: str) -> list[dict[str, str]]:
    return [{
        "document_id": document["document_id"], "field": field,
        "current_value": current_value(document, field),
        "deterministic_suggestion": deterministic_value(document, field),
        "llm_suggestion": "", "llm_evidence": reason, "llm_confidence": "low",
        "agreement_status": "unresolved", "requires_human_review": "true", "model": model,
        "prompt_version": PROMPT_VERSION, "source_sha256": document["source_sha256"], "processed_at": "",
    } for field in fields_requiring_llm(document)]


def queue_v2(suggestions: list[dict[str, str]], master_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for item in suggestions:
        if item["requires_human_review"] != "true":
            continue
        rows.append({
            "priority": review_priority(item), "document_id": item["document_id"],
            "source_relative_path": master_by_id[item["document_id"]]["source_relative_path"],
            "field": item["field"], "current_value": item["current_value"],
            "deterministic_suggestion": item["deterministic_suggestion"],
            "llm_suggestion": item["llm_suggestion"], "evidence": item["llm_evidence"],
            "confidence": item["llm_confidence"], "agreement_status": item["agreement_status"],
            "reviewer_value": "", "reviewer_note": "", "review_status": "pending", "reviewed_at": "",
        })
    order = {"P0": 0, "P1": 1, "P2": 2}
    return sorted(rows, key=lambda row: (order[row["priority"]], row["document_id"], row["field"]))


def audit_text(summary: dict[str, object], config: dict[str, object], tests: str) -> str:
    return "\n".join([
        "# TunnelBookAI Local LLM Metadata Suggestion Audit", "", "## Sonuç", "",
        f"- Karar: **{summary['decision']}**",
        f"- Seçilen belge sayısı: **{summary['selected_documents']}**",
        f"- Bu çalıştırmanın kapsamı: **{summary['run_scope_documents']}**",
        f"- İşlenen belge sayısı: **{summary['processed_documents']}**",
        f"- LLM'e gönderilen belge sayısı: **{summary['documents_sent']}**",
        f"- Cache'den kullanılan belge sayısı: **{summary['cache_hits']}**",
        f"- Kapsam dışında/sonraya bırakılan: **{summary['skipped_documents']}**",
        f"- Field suggestion sayısı: **{summary['field_suggestions']}**",
        f"- High confidence: **{summary['high']}**", f"- Medium confidence: **{summary['medium']}**",
        f"- Low confidence: **{summary['low']}**",
        f"- Deterministic + LLM agreement: **{summary['agreement']}**",
        f"- Deterministic + LLM conflict: **{summary['conflict']}**",
        f"- Yalnız LLM suggestion: **{summary['llm_only']}**",
        f"- Existing verified: **{summary['existing_verified']}**",
        f"- Unresolved: **{summary['unresolved']}**", "", "## Review queue V2", "",
        f"- P0: **{summary['P0']}**", f"- P1: **{summary['P1']}**", f"- P2: **{summary['P2']}**", "",
        "## Runtime", "", f"- Endpoint: `{config.get('base_url', '')}`",
        f"- Model: `{summary['model'] or '(yüklenmedi)'}`", f"- Prompt version: `{PROMPT_VERSION}`",
        f"- Başarısız LLM çağrısı: **{summary['failed_calls']}**", f"- Parse retry: **{summary['parse_retries']}**",
        f"- Ortalama gerçek inference süresi: **{summary['average_processing_seconds']} saniye**",
        f"- Endpoint durumu: **{summary['endpoint_status']}**", "",
        "## Güvenlik ve bütünlük", "",
        f"- Verified/current metadata değişti: **{str(summary['verified_changed']).lower()}**",
        f"- `data/corpus_final/` değişti: **{str(summary['corpus_changed']).lower()}**",
        "- Tüm LLM çıktıları suggestion-only kaldı; verified metadata'ya uygulanmadı.",
        "- Mevcut `final_metadata_review_queue.csv` korunarak ayrı V2 üretildi.",
        "- Yalnız loopback local endpoint kabul edildi; harici/ücretli API kullanılmadı.", "",
        "## Test sonucu", "", f"- {tests or 'Henüz çalıştırılmadı'}", "",
    ])


def directory_state(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix().casefold()):
        stat = path.stat()
        digest.update(f"{path.relative_to(root).as_posix()}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode("utf-8"))
    return digest.hexdigest()


def corpus_document_index(corpus_root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(corpus_root.rglob("*.md"), key=lambda item: item.as_posix().casefold()):
        prefix = path.read_text(encoding="utf-8-sig", errors="replace")[:4096]
        match = re.search(r"(?m)^document_id:\s*[\"']?([^\"'\s]+)", prefix)
        if not match:
            continue
        document_id = match.group(1)
        if document_id in index:
            raise LLMReviewError(f"Corpus içinde duplicate document_id: {document_id}")
        index[document_id] = path
    return index


def resolve_markdown_path(project_root: Path, document: dict[str, str], index: dict[str, Path]) -> Path:
    expected = project_root / "data/corpus_final" / Path(
        unicodedata.normalize("NFC", document["source_relative_path"])
    ).with_suffix(".md")
    if expected.is_file():
        return expected
    resolved = index.get(document["document_id"])
    if resolved is None:
        raise LLMReviewError(f"Final Markdown bulunamadı: {document['document_id']}")
    return resolved


def run(project_root: Path, config: dict[str, object], explicit_run: bool, limit: int = 0,
        tests: str = "", transport: Transport = http_transport,
        model_discovery: Callable[[str, int, str], str] = discover_model) -> dict[str, object]:
    base_url = str(config.get("base_url", "http://127.0.0.1:1234/v1"))
    assert_local_endpoint(base_url)
    master_path = project_root / "data/metadata/final_metadata_master.csv"
    master_before = master_path.read_bytes()
    corpus_before = directory_state(project_root / "data/corpus_final")
    master = read_csv(master_path)
    master_by_id = {row["document_id"]: row for row in master}
    corpus_index = corpus_document_index(project_root / "data/corpus_final")
    all_candidates = [row for row in master if fields_requiring_llm(row)]
    candidates = all_candidates
    if limit > 0:
        candidates = candidates[:limit]
    model = str(config.get("model", "")).strip()
    enabled = bool(config.get("enabled", False)) or explicit_run
    endpoint_status = "disabled"
    endpoint_failure = ""
    if enabled:
        try:
            model = model_discovery(base_url, int(config.get("timeout_seconds", 120)), model)
            endpoint_status = "available"
        except Exception as exc:
            endpoint_status = "unavailable"
            endpoint_failure = f"{type(exc).__name__}: {exc}"
    rows = base_rows(master, model)
    successful_documents = failed_calls = parse_retries = cache_hits = documents_sent = 0
    inference_seconds: list[float] = []
    suggestions_path = project_root / "data/metadata/metadata_llm_suggestions.csv"
    queue_path = project_root / "data/metadata/final_metadata_review_queue_v2.csv"
    report_path = project_root / "reports/metadata_llm_suggestion_audit.md"

    def checkpoint() -> None:
        ordered = sorted(rows, key=lambda row: (row["document_id"], FIELDS.index(row["field"])))
        atomic_write(suggestions_path, csv_bytes(ordered, OUTPUT_FIELDS))
        atomic_write(queue_path, csv_bytes(queue_v2(ordered, master_by_id), QUEUE_FIELDS))

    for document in candidates:
        if not enabled:
            rows.extend(unresolved_rows(document, model, "local_llm_disabled"))
            continue
        if endpoint_status != "available":
            rows.extend(unresolved_rows(document, model, f"local_endpoint_unavailable: {endpoint_failure}"))
            continue
        cached = read_cache(cache_path(project_root, document, model), document, model)
        if cached:
            response = cached["response"]
            processed_at = str(cached["processed_at"])
            parse_retries += int(cached.get("parse_retries", 0))
            cache_hits += 1
            successful_documents += 1
        else:
            markdown_path = resolve_markdown_path(project_root, document, corpus_index)
            package = context_package(document, markdown_path.read_text(encoding="utf-8-sig", errors="replace"))
            try:
                started = time.monotonic()
                documents_sent += 1
                response, retries = call_with_retry(
                    base_url, model, package, float(config.get("temperature", 0.1)),
                    int(config.get("timeout_seconds", 120)), int(config.get("max_retries", 2)), transport,
                )
                inference_seconds.append(time.monotonic() - started)
                parse_retries += retries
            except Exception as exc:
                failed_calls += 1
                rows.extend(unresolved_rows(document, model, f"llm_call_failed: {type(exc).__name__}: {exc}"))
                checkpoint()
                continue
            processed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            payload = {"document_id": document["document_id"], "source_sha256": document["source_sha256"],
                       "model": model, "prompt_version": PROMPT_VERSION, "processed_at": processed_at,
                       "parse_retries": retries, "response": response}
            atomic_write(cache_path(project_root, document, model), json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8"))
            successful_documents += 1
        rows.extend(suggestion_rows_for_document(document, response, model, processed_at))
        checkpoint()
    rows.sort(key=lambda row: (row["document_id"], FIELDS.index(row["field"])))
    queue = queue_v2(rows, master_by_id)
    confidence = Counter(row["llm_confidence"] for row in rows if row["llm_suggestion"] or row["agreement_status"] == "unresolved")
    statuses = Counter(row["agreement_status"] for row in rows)
    priorities = Counter(row["priority"] for row in queue)
    existing_verified = sum(
        not missing(current_value(document, field))
        for document in master for field in FIELDS
    )
    summary: dict[str, object] = {
        "selected_documents": len(all_candidates), "run_scope_documents": len(candidates),
        "processed_documents": successful_documents, "documents_sent": documents_sent, "cache_hits": cache_hits,
        "skipped_documents": len(all_candidates) - len(candidates),
        "field_suggestions": sum(bool(row["llm_suggestion"]) for row in rows),
        "high": confidence["high"], "medium": confidence["medium"], "low": confidence["low"],
        "agreement": statuses["deterministic_llm_agree"], "conflict": statuses["deterministic_llm_conflict"],
        "llm_only": statuses["llm_only"], "existing_verified": existing_verified,
        "unresolved": statuses["unresolved"], "P0": priorities["P0"], "P1": priorities["P1"], "P2": priorities["P2"],
        "failed_calls": failed_calls + (1 if enabled and endpoint_status == "unavailable" else 0),
        "parse_retries": parse_retries, "endpoint_status": endpoint_status, "model": model,
        "average_processing_seconds": round(sum(inference_seconds) / len(inference_seconds), 3) if inference_seconds else 0.0,
        "verified_changed": master_path.read_bytes() != master_before,
        "corpus_changed": directory_state(project_root / "data/corpus_final") != corpus_before,
    }
    summary["decision"] = "GO" if enabled and endpoint_status == "available" and not summary["failed_calls"] and not summary["verified_changed"] and not summary["corpus_changed"] else "NO-GO"
    atomic_write(suggestions_path, csv_bytes(rows, OUTPUT_FIELDS))
    atomic_write(queue_path, csv_bytes(queue, QUEUE_FIELDS))
    atomic_write(report_path, audit_text(summary, config, tests).encode("utf-8"))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Local suggestion-only LM Studio metadata pass")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--config", type=Path)
    parser.add_argument("--run", action="store_true", help="Explicitly enable local LLM calls")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--test-summary", default="")
    args = parser.parse_args()
    root = args.project_root.resolve()
    config = load_yaml(args.config or root / "config/metadata_llm.yaml")
    try:
        summary = run(root, config, args.run, args.limit, args.test_summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["decision"] == "GO" or not args.run else 2
    except LLMReviewError as exc:
        print(f"NO-GO: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
