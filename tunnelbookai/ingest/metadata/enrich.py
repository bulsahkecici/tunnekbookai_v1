"""Metadata enrichment (task §28-§31).

Evidence discipline, reused from `scripts/09_metadata_enrichment.py`:

  * a value is written only when the document, its package properties, its filename or the
    crawler manifest actually supports it;
  * anything else stays `null` / `UNKNOWN`;
  * an inferred value always carries `inferred=true` + `reason` + `confidence` (§31).

Optional loopback-Qwen enrichment is off by default. When enabled it may only *extract* or
*normalize* what is already in the text; every field it touches is marked `inferred=true`
with source `local_llm`, and organization / date / author / department / approval are never
accepted from it unless the same string is present verbatim in the extracted text.
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any

from ..extraction import ExtractionResult
from .provenance import ProvenanceLog
from .schema import empty_metadata, legacy_vocabularies, validate

DATE_PATTERNS = (
    re.compile(r"\b(\d{2})[./](\d{2})[./]((?:19|20)\d{2})\b"),
    re.compile(r"\b((?:19|20)\d{2})-(\d{2})-(\d{2})\b"),
)
REVISION_PATTERN = re.compile(
    r"\b(?:rev(?:izyon|ision)?|sürüm|version|v)\s*[.:]?\s*([0-9]+(?:\.[0-9]+)?[A-Za-z]?)\b",
    re.IGNORECASE)
CONFIDENTIALITY_PATTERNS = (
    ("RESTRICTED", re.compile(r"\b(gizli|çok gizli|confidential|restricted|hizmete özel)\b", re.I)),
    ("INTERNAL", re.compile(r"\b(kuruma özel|internal use only|iç kullanım)\b", re.I)),
)
STATUS_PATTERNS = (
    ("APPROVED", re.compile(r"\b(onaylanmıştır|onaylandı|approved by|approval date)\b", re.I)),
    ("DRAFT", re.compile(r"\b(taslak|draft|ön rapor|preliminary)\b", re.I)),
    ("FINAL", re.compile(r"\b(nihai rapor|final report|son rapor)\b", re.I)),
)
DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")


def _ooxml_core_properties(path: Path) -> dict[str, str]:
    """docProps/core.xml — authoring-app metadata, a genuine (not inferred) source."""
    try:
        with zipfile.ZipFile(path) as archive:
            if "docProps/core.xml" not in archive.namelist():
                return {}
            raw = archive.read("docProps/core.xml").decode("utf-8", errors="replace")
    except (OSError, zipfile.BadZipFile):
        return {}
    out: dict[str, str] = {}
    for tag in ("title", "subject", "creator", "lastModifiedBy", "revision", "category",
                "description", "created", "modified"):
        match = re.search(rf"<(?:\w+:)?{tag}[^>]*>(.*?)</(?:\w+:)?{tag}>", raw, re.DOTALL)
        if match:
            value = match.group(1).strip()
            if value:
                out[tag] = value
    return out


def _first_heading(elements: list[dict[str, Any]]) -> str | None:
    """The document's own first heading. A heading an adapter synthesised from the filename
    (origin="filename") is not one — it must fall through to the filename branch so its
    provenance is recorded honestly as inferred (§30, §31)."""
    for element in elements:
        if (element.get("type") == "heading" and element.get("text")
                and element.get("origin") != "filename"):
            return element["text"].strip()
    return None


def _document_date(text: str) -> tuple[str | None, str | None]:
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        groups = match.groups()
        if len(groups[0]) == 4:
            iso = f"{groups[0]}-{groups[1]}-{groups[2]}"
        else:
            iso = f"{groups[2]}-{groups[1]}-{groups[0]}"
        return iso, match.group(0)
    return None, None


def _authors_from_crawler(record: dict[str, Any]) -> list[str]:
    authors = record.get("authors") or record.get("author") or []
    if isinstance(authors, str):
        authors = [a.strip() for a in re.split(r"[;,]", authors) if a.strip()]
    return [str(a) for a in authors if a]


def build_metadata(
    *,
    document_id: str,
    archive_meta: dict[str, Any],
    provenance_doc: dict[str, Any],
    extraction: ExtractionResult,
    config: Any,
    original_path: Path,
) -> tuple[dict[str, Any], ProvenanceLog, list[str]]:
    """Assemble metadata.json + metadata_provenance.json. Returns (metadata, log, warnings)."""
    warnings: list[str] = []
    legacy = legacy_vocabularies()
    metadata = empty_metadata(document_id)
    log = ProvenanceLog()

    sources = provenance_doc.get("sources", []) or []
    crawler_record: dict[str, Any] = {}
    for source in sources:
        if source.get("kind") == "EXTERNAL_DISCOVERY":
            crawler_record = source.get("crawler_record") or source
    source_kind = archive_meta.get("source_kind") or (sources[0].get("kind") if sources else None)
    if len(sources) > 1:
        # a document seen by both the crawler and a human keeps the manual (internal) kind
        kinds = {s.get("kind") for s in sources}
        source_kind = "MANUAL_INTERNAL" if "MANUAL_INTERNAL" in kinds else source_kind

    metadata["source_kind"] = source_kind
    metadata["original_filename"] = archive_meta.get("original_filename")
    metadata["original_sha256"] = archive_meta.get("original_sha256")
    metadata["format"] = archive_meta.get("format")
    metadata["mime_type"] = archive_meta.get("mime_type")
    metadata["ingest_method"] = ("crawler_handoff" if source_kind == "EXTERNAL_DISCOVERY"
                                 else "manual_inbox")

    text = ""
    if extraction.normalized_text_path:
        candidate = Path(extraction.normalized_text_path)
        if not candidate.is_absolute():
            from ..paths import PROJECT_ROOT
            candidate = PROJECT_ROOT / candidate
        if candidate.is_file():
            text = candidate.read_text(encoding="utf-8", errors="replace")
    excerpt = legacy.analysis_excerpt(text, 2500)

    core = _ooxml_core_properties(original_path) if original_path.suffix.lower() in {
        ".docx", ".pptx", ".xlsx", ".pptm"} else {}

    # ---------------------------------------------------------------- title
    heading = _first_heading(extraction.text_elements)
    if crawler_record.get("title"):
        log.set(metadata, "title", str(crawler_record["title"]).strip(),
                source="crawler_manifest", confidence="high")
    elif core.get("title"):
        log.set(metadata, "title", core["title"], source="ooxml_properties", confidence="high")
    elif heading:
        log.set(metadata, "title", heading, source="document_heading", confidence="high")
    else:
        stem = Path(archive_meta.get("original_filename") or original_path.name).stem
        stem = stem.replace("_", " ").strip()
        if stem:
            log.set(metadata, "title", stem, source="original_file", confidence="low",
                    inferred=True, reason="no heading or package title; fell back to the filename")
            metadata["title_inferred_from_filename"] = True
        else:
            log.miss("title")

    # -------------------------------------------------------------- authors
    authors = _authors_from_crawler(crawler_record)
    if authors:
        log.set(metadata, "authors", authors, source="crawler_manifest", confidence="high")
    elif core.get("creator") and core["creator"].lower() not in {"user", "unknown", "python-docx",
                                                                "python-pptx", "openpyxl"}:
        log.set(metadata, "authors", [core["creator"]], source="ooxml_properties",
                confidence="medium")
    else:
        log.miss("authors", "no author in the crawler manifest or package properties")

    # --------------------------------------------------------- organization
    organization = crawler_record.get("organization") or crawler_record.get("publisher")
    if organization:
        log.set(metadata, "organization", str(organization), source="crawler_manifest",
                confidence="medium")
    else:
        # Never guessed from filename or content patterns (§31, stop condition §90).
        log.miss("organization", "organization is never inferred from filename or body text")
    log.miss("department", "department is never inferred")

    # ------------------------------------------------------------------ date
    display_name = archive_meta.get("original_filename") or original_path.name
    iso_date, matched = _document_date(f"{display_name}\n{excerpt[:4000]}")
    if crawler_record.get("published_date") or crawler_record.get("date"):
        log.set(metadata, "document_date",
                str(crawler_record.get("published_date") or crawler_record.get("date")),
                source="crawler_manifest", confidence="high")
    elif crawler_record.get("year"):
        # The handoff manifest carries `year`, not `published_date`. Ignoring it dropped a
        # recorded publication year and left document_date null even though the crawler knew
        # it (real-data pilot defect D2). A bare year is the same shape the body-text
        # fallback below already writes, but this one is bibliographic, not inferred.
        log.set(metadata, "document_date", str(crawler_record["year"]).strip(),
                source="crawler_manifest", confidence="medium",
                reason="publication year from the crawler handoff manifest (year only)")
    elif iso_date:
        log.set(metadata, "document_date", iso_date, source="document_content",
                confidence="medium", inferred=True,
                reason=f"explicit date literal in the document: {matched}")
    else:
        year, evidence, confidence, conflict = legacy.infer_year(
            display_name, metadata.get("title") or "", text, "")
        if year and not conflict:
            log.set(metadata, "document_date", year, source="document_content",
                    confidence=confidence, inferred=True, reason=evidence)
        else:
            log.miss("document_date", evidence if evidence else "no reliable date evidence")

    # -------------------------------------------------------------- revision
    revision_match = REVISION_PATTERN.search(f"{display_name} {excerpt[:2000]}")
    if core.get("revision") and core["revision"] not in {"1", "0"}:
        log.set(metadata, "revision", core["revision"], source="ooxml_properties",
                confidence="medium")
    elif revision_match:
        log.set(metadata, "revision", revision_match.group(1), source="document_content",
                confidence="medium", inferred=True,
                reason=f"revision literal: {revision_match.group(0)}")
    else:
        log.miss("revision", "no revision marker found")

    # -------------------------------------------------------------- language
    language, language_confidence = legacy.infer_language(text, "")
    if language != "unknown":
        log.set(metadata, "language", language, source="document_content",
                confidence=language_confidence, inferred=True,
                reason="lexical language detection over the extracted text")
    else:
        log.miss("language", "too little text for reliable language detection")

    # --------------------------------------------------------- document_type
    document_type, dt_evidence, dt_confidence = legacy.infer_document_type(
        display_name, metadata.get("title") or "", text, "", original_path.suffix.lower())
    if document_type != "unknown":
        log.set(metadata, "document_type", document_type, source="document_content",
                confidence=dt_confidence, inferred=True, reason=dt_evidence)
    else:
        metadata["document_type"] = None
        log.miss("document_type", dt_evidence)

    topics, topic_evidence, topic_confidence = legacy.infer_topics(
        display_name, metadata.get("title") or "", text, "")
    if topics:
        log.set(metadata, "topics", list(topics), source="document_content",
                confidence=topic_confidence, inferred=True, reason=topic_evidence)

    # ------------------------------------------------------------ url / doi
    url = crawler_record.get("resolved_url") or crawler_record.get("url") or crawler_record.get("source_url")
    if url:
        log.set(metadata, "source_url", str(url), source="crawler_manifest", confidence="high")
    doi = crawler_record.get("doi")
    if not doi:
        match = DOI_PATTERN.search(excerpt[:6000])
        if match:
            doi = match.group(0).rstrip(".")
            log.set(metadata, "doi", doi, source="document_content", confidence="high")
    else:
        log.set(metadata, "doi", str(doi), source="crawler_manifest", confidence="high")

    # ------------------------------------------ confidentiality / status
    metadata["confidentiality"] = str(
        (config.metadata or {}).get("confidentiality_default", "UNKNOWN"))
    for value, pattern in CONFIDENTIALITY_PATTERNS:
        match = pattern.search(excerpt[:6000])
        if match:
            metadata["confidentiality"] = value
            log.set(metadata, "confidentiality", value, source="document_content",
                    confidence="medium", inferred=True,
                    reason=f"confidentiality marking: {match.group(0)}")
            break
    metadata["document_status"] = str(
        (config.metadata or {}).get("document_status_default", "UNKNOWN"))
    for value, pattern in STATUS_PATTERNS:
        match = pattern.search(excerpt[:6000])
        if match:
            metadata["document_status"] = value
            log.set(metadata, "document_status", value, source="document_content",
                    confidence="medium", inferred=True,
                    reason=f"status marking: {match.group(0)}")
            break

    metadata["content_capabilities"] = dict(extraction.capabilities)

    llm_cfg = (config.metadata or {}).get("llm_enrichment", {}) or {}
    if llm_cfg.get("enabled"):
        warnings += _llm_enrich(metadata, log, text, llm_cfg)

    problems = validate(metadata)
    warnings += [f"METADATA_{p}" for p in problems]
    return metadata, log, warnings


def _llm_enrich(metadata: dict[str, Any], log: ProvenanceLog, text: str,
                cfg: dict[str, Any]) -> list[str]:
    """Optional loopback-only Qwen pass. Only fills fields still null, never overwrites."""
    from ..classify.arbiter import LocalChatClient
    from ..vision.provider import RemoteEndpointRejected

    targets = [f for f in ("title", "organization", "document_date") if metadata.get(f) is None]
    if not targets:
        return []
    try:
        client = LocalChatClient(cfg.get("base_url", "http://127.0.0.1:1234/v1"),
                                 timeout=float(cfg.get("timeout_seconds", 120)))
    except RemoteEndpointRejected:
        raise
    if not client.available():
        return ["METADATA_LLM_UNAVAILABLE"]
    model = cfg.get("model") or client.pick_model(["qwen"])
    if not model:
        return ["METADATA_LLM_NO_MODEL"]
    system = (
        "Sen bir belge üstveri çıkarıcısısın. SADECE verilen metinde birebir geçen bilgileri "
        "döndür. Tahmin etme. Emin değilsen null yaz. Yanıtı JSON ver: "
        '{"title": null, "organization": null, "document_date": null}'
    )
    try:
        payload = client.chat_json(model, system, text[:8000])
    except RemoteEndpointRejected:
        raise
    except Exception:
        return ["METADATA_LLM_CALL_FAILED"]

    warnings: list[str] = []
    haystack = text.lower()
    for field in targets:
        value = payload.get(field)
        if not value or not isinstance(value, str):
            continue
        # verbatim-presence guard: the model may extract, never invent (§31)
        if value.strip().lower() not in haystack:
            warnings.append(f"METADATA_LLM_REJECTED_NOT_VERBATIM:{field}")
            continue
        log.set(metadata, field, value.strip(), source="local_llm", confidence="low",
                inferred=True, reason="loopback LLM extraction, verified verbatim in the text")
    return warnings


def write_metadata(bundle: Path, metadata: dict[str, Any], log: ProvenanceLog) -> tuple[Path, Path]:
    bundle.mkdir(parents=True, exist_ok=True)
    metadata_path = bundle / "metadata.json"
    provenance_path = bundle / "metadata_provenance.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=str),
                             encoding="utf-8")
    provenance_path.write_text(
        json.dumps(log.to_dict(metadata["document_id"]), ensure_ascii=False, indent=2, default=str),
        encoding="utf-8")
    return metadata_path, provenance_path
