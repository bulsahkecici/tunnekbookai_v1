#!/usr/bin/env python3
"""Prepare a local-only evidence remediation packet for a configured book section.

This script never writes book prose and never mutates frozen corpus/retrieval assets.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


SECTION_ID = ""
SECTION_TITLE = ""
RELATED_IDS: tuple[str, ...] = ()
SEARCH_QUERIES: tuple[str, ...] = ()
SCOPE_EXCLUSIONS: tuple[str, ...] = ()
SECTION_CONFIG: dict[str, Any] = {}
TEXT_SUFFIXES = {".json", ".jsonl", ".yaml", ".yml", ".md", ".txt", ".csv"}
DISCOVERY_DIRS = ("data/book", "config", "docs", "reports")
SKIP_PARTS = {
    ".git", ".venv", "node_modules", "corpus_final", "markdown",
    "markdown_full_docling", "qdrant_storage", "embeddings",
}
READINESS_VALUES = {
    "READY", "READY_WITH_LIMITATIONS", "TRUE_CORPUS_EVIDENCE_GAP",
    "NEEDS_LOCAL_REVIEW",
}
DISPOSITIONS = {
    "ADMITTED_STRONG", "ADMITTED_LIMITED", "REJECT_SCOPE", "REJECT_SUPPORT",
    "REJECT_PROVENANCE", "REJECT_OTHER",
}
LOG = logging.getLogger("section_evidence_remediation")



def section_slug(section_id: str) -> str:
    return section_id.lower().replace("-", "_")


def load_section_config(root: Path, section_id: str) -> dict[str, Any]:
    path = root / "config" / "book_sections.json"
    if not path.is_file():
        raise RemediationError("SECTION_CONFIG_NOT_FOUND")

    try:
        all_sections = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RemediationError(f"SECTION_CONFIG_INVALID: {exc}") from exc

    if not isinstance(all_sections, dict):
        raise RemediationError("SECTION_CONFIG_INVALID")

    config = all_sections.get(section_id)
    if not isinstance(config, dict):
        raise RemediationError(f"SECTION_CONFIG_NOT_FOUND: {section_id}")

    title = config.get("section_title")
    queries = config.get("search_queries")

    if not isinstance(title, str) or not title.strip():
        raise RemediationError("SECTION_TITLE_NOT_CONFIGURED")

    if not isinstance(queries, list) or not queries:
        raise RemediationError("SECTION_SEARCH_QUERIES_NOT_CONFIGURED")

    if any(not isinstance(q, str) or not q.strip() for q in queries):
        raise RemediationError("SECTION_SEARCH_QUERIES_INVALID")

    return config


def configure_section(root: Path, section_id: str) -> None:
    global SECTION_ID
    global SECTION_TITLE
    global RELATED_IDS
    global SEARCH_QUERIES
    global SCOPE_EXCLUSIONS
    global SECTION_CONFIG

    config = load_section_config(root, section_id)

    SECTION_ID = section_id
    SECTION_TITLE = config["section_title"].strip()

    related = config.get("related_ids") or []
    if not isinstance(related, list):
        raise RemediationError("SECTION_RELATED_IDS_INVALID")

    SECTION_CONFIG = config
    RELATED_IDS = tuple(
        dict.fromkeys(
            [
                SECTION_ID,
                SECTION_TITLE,
                *[
                    str(value).strip()
                    for value in related
                    if str(value).strip()
                ],
            ]
        )
    )

    SEARCH_QUERIES = tuple(
        q.strip() for q in config["search_queries"] if q.strip()
    )

    exclusions = config.get("scope_exclusions") or []
    if not isinstance(exclusions, list):
        raise RemediationError("SECTION_SCOPE_EXCLUSIONS_INVALID")

    SCOPE_EXCLUSIONS = tuple(
        str(value).strip()
        for value in exclusions
        if str(value).strip()
    )


class RemediationError(RuntimeError):
    """Fail-closed remediation error with a stable status code."""


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_text(path: Path, limit: int = 8 * 1024 * 1024) -> str | None:
    try:
        if path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def find_project_artifacts(root: Path) -> list[Path]:
    """Find only small, relevant project text artifacts."""
    found: list[Path] = []
    needles = tuple(value.casefold() for value in RELATED_IDS)
    for relative_dir in DISCOVERY_DIRS:
        base = root / relative_dir
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in SKIP_PARTS for part in path.relative_to(root).parts):
                continue
            text = _safe_text(path)
            if text is not None and any(needle in text.casefold() for needle in needles):
                found.append(path)
    return sorted(set(found), key=lambda p: p.as_posix())


def _json_documents(path: Path) -> list[Any]:
    text = _safe_text(path)
    if text is None:
        return []
    try:
        if path.suffix.lower() == ".jsonl":
            return [json.loads(line) for line in text.splitlines() if line.strip()]
        if path.suffix.lower() == ".json":
            return [json.loads(text)]
    except json.JSONDecodeError:
        return []
    return []


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _first(records: Iterable[dict[str, Any]], keys: tuple[str, ...]) -> Any:
    for record in records:
        for key in keys:
            if key in record and record[key] not in (None, "", [], {}):
                return record[key]
    return None


def load_section_state(artifacts: list[Path], root: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    source_files: list[str] = []
    for path in artifacts:
        documents = _json_documents(path)
        matched = False
        for document in documents:
            for record in _walk(document):
                rendered = json.dumps(record, ensure_ascii=False)
                if any(identifier in rendered for identifier in RELATED_IDS):
                    records.append(record)
                    matched = True
        if matched:
            source_files.append(path.relative_to(root).as_posix())
    if not records:
        raise RemediationError("SECTION_STATE_NOT_RESOLVED")

    section_ids = {str(r.get("section_id")) for r in records if r.get("section_id")}
    if SECTION_ID not in section_ids:
        raise RemediationError("SECTION_STATE_NOT_RESOLVED")

    claims: list[dict[str, Any]] = []
    for record in records:
        for key in ("admitted_claims", "existing_claims", "claims", "permitted_claims_used"):
            value = record.get(key)
            if isinstance(value, list):
                claims.extend(item for item in value if isinstance(item, dict))
    return {
        "section_id": SECTION_ID,
        "section_title": _first(records, ("section_title", "title")) or SECTION_TITLE,
        "section_scope": (
            _first(records, ("section_scope", "scope"))
            or SECTION_CONFIG.get("section_scope")
        ),
        "research_question": (
            _first(records, ("research_question", "research_question_text", "question"))
            or SECTION_CONFIG.get("research_question")
        ),
        "research_question_id": _first(records, ("research_question_id", "rq_id")),
        "packet_id": _first(records, ("packet_id", "evidence_packet_id")),
        "packet_state": _first(records, ("packet_readiness", "packet_state", "evidence_gate")),
        "current_readiness": _first(records, ("readiness", "readiness_before_drafting", "section_status")),
        "admission_state": _first(records, ("admission_state", "admission_status", "use_decision")),
        "citation_mapping": _first(records, ("citation_mapping", "material_units", "bibliography")),
        "provenance_rules": _first(records, ("provenance_rules", "provenance_policy")),
        "terminology_constraints": _first(records, ("terminology_constraints", "controlled_terms")),
        "existing_claims": claims,
        "source_artifacts": sorted(set(source_files)),
    }


def resolve_retriever(root: Path) -> tuple[Any, Path, dict[str, Any]]:
    path = root / "scripts" / "19_retriever_v1.py"
    if not path.is_file():
        raise RemediationError("RETRIEVER_INTERFACE_NOT_RESOLVED")
    spec = importlib.util.spec_from_file_location("tunnelbook_retriever_v1", path)
    if spec is None or spec.loader is None:
        raise RemediationError("RETRIEVER_INTERFACE_NOT_RESOLVED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise RemediationError("RETRIEVER_INTERFACE_NOT_RESOLVED") from exc
    cls = getattr(module, "RetrieverV1", None)
    release_config = getattr(module, "release_config", None)
    if cls is None or not callable(getattr(cls, "retrieve", None)) or not callable(release_config):
        raise RemediationError("RETRIEVER_INTERFACE_NOT_RESOLVED")
    return cls(), path, release_config()


def run_retrieval_queries(retriever: Any, top_k: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for query in SEARCH_QUERIES:
        LOG.info("Retrieving query %r", query)
        try:
            results = retriever.retrieve(query, top_k=top_k)
        except Exception as exc:
            raise RemediationError(f"NO_RETRIEVAL_RESULTS: {type(exc).__name__}: {exc}") from exc
        for result in results:
            item = asdict(result) if is_dataclass(result) else dict(result)
            item["query"] = query
            item["retrieval_rank"] = item.pop("rank", None)
            item["retrieval_score"] = item.pop("score", None)
            item["locator"] = _candidate_locator(item)
            item["source_type"] = item.get("document_type") or item.get("source_kind")
            item["authority_state"] = item.get("authority_level") or "UNKNOWN"
            item["provenance"] = item.get("provenance_status")
            candidates.append(item)
    if not candidates:
        raise RemediationError("NO_RETRIEVAL_RESULTS")
    return candidates


def _candidate_locator(item: dict[str, Any]) -> str | None:
    if item.get("original_page_start") is not None:
        start, end = item["original_page_start"], item.get("original_page_end")
        return f"page:{start}" if end in (None, start) else f"pages:{start}-{end}"
    if item.get("slide_start") is not None:
        start, end = item["slide_start"], item.get("slide_end")
        return f"slide:{start}" if end in (None, start) else f"slides:{start}-{end}"
    return item.get("section_path") or item.get("heading")


def _candidate_key(item: dict[str, Any]) -> str:
    if item.get("chunk_id"):
        return f"chunk:{item['chunk_id']}"
    if item.get("document_id") and item.get("locator"):
        return f"location:{item['document_id']}:{item['locator']}"
    text_hash = hashlib.sha256(str(item.get("text", "")).encode("utf-8")).hexdigest()
    return f"text:{item.get('document_id', '')}:{text_hash}"


def deduplicate_candidates(candidates: list[dict[str, Any]], max_candidates: int) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    ordered = sorted(candidates, key=lambda c: (-(float(c.get("retrieval_score") or 0)), c.get("query", ""), c.get("retrieval_rank") or 999))
    for item in ordered:
        key = _candidate_key(item)
        if key not in merged:
            copy = dict(item)
            copy["retrieval_hits"] = [{"query": item.get("query"), "rank": item.get("retrieval_rank"), "score": item.get("retrieval_score")}]
            merged[key] = copy
        else:
            merged[key]["retrieval_hits"].append({"query": item.get("query"), "rank": item.get("retrieval_rank"), "score": item.get("retrieval_score")})
    return list(merged.values())[:max_candidates]


def validate_local_endpoint(api_base: str) -> str:
    parsed = urlparse(api_base)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise RuntimeError("api-base must be an HTTP loopback endpoint")
    if parsed.username or parsed.password or not parsed.port:
        raise RuntimeError("api-base must contain a loopback host and explicit port")
    return api_base.rstrip("/")


def _native_chat_endpoint(api_base: str) -> str:
    parsed = urlparse(validate_local_endpoint(api_base))
    return f"{parsed.scheme}://{parsed.netloc}/api/v1/chat"


def _extract_final_text(body: dict[str, Any]) -> str | None:
    output = body.get("output")
    if not isinstance(output, list):
        return None

    messages: list[str] = []
    for item in output:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "message":
            content = item.get("content")
            if isinstance(content, str) and content.strip():
                messages.append(content.strip())

    if not messages:
        return None
    return messages[-1]


def _classification_system_prompt() -> str:
    exclusions = ", ".join(SCOPE_EXCLUSIONS) if SCOPE_EXCLUSIONS else "later-section topics"
    return (
        f"Classify atomic claims for {SECTION_ID} — {SECTION_TITLE} only. "
        "Use only the supplied candidate text; use no pretrained knowledge or external facts. "
        "Do not strengthen, combine, repair, or infer claims. Topical similarity is not support. "
        f"Exclude material outside this section, including: {exclusions}. "
        "Return JSON only as {\\\"claims\\\": [...]}. Each claim must contain "
        "claim_text, document_id, source_relative_path, locator, scope, qualifier, "
        "source_type, authority_state, support_status, section_applicability, disposition, reason. "
        f"disposition must be one of {sorted(DISPOSITIONS)}. Preserve qualifiers."
    )

def _llm_prompt(candidate: dict[str, Any]) -> str:
    payload = {key: candidate.get(key) for key in (
        "document_id", "source_relative_path", "locator", "source_type",
        "authority_state", "provenance", "text",
    )}
    return "Candidate:\n" + json.dumps(payload, ensure_ascii=False)


def _parse_model_json(content: str) -> dict[str, Any]:
    """Parse model JSON while tolerating Markdown code fences only."""
    text = content.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    if not text:
        raise ValueError("model returned empty message")

    parsed = json.loads(text)

    if not isinstance(parsed, dict):
        raise ValueError("model message is not a JSON object")

    return parsed


def _native_chat_json(model: str, api_base: str, system_prompt: str, input_text: str) -> dict[str, Any]:
    request_body = json.dumps({
        "model": model,
        "system_prompt": system_prompt,
        "input": input_text,
        "temperature": 0,
        "store": False,
    }, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        _native_chat_endpoint(api_base),
        data=request_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
        if not isinstance(body, dict):
            raise ValueError("native response body is not an object")
        content = _extract_final_text(body)
        if content is None:
            raise ValueError("native response has no final message")
        return _parse_model_json(content)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        raise RemediationError(f"LOCAL_LLM_CLASSIFICATION_FAILED: {exc}") from exc


def smoke_test_local_llm(model: str, api_base: str) -> None:
    parsed = _native_chat_json(
        model,
        api_base,
        "You are a local JSON test.",
        'Return only:\n{"status":"OK"}',
    )
    if parsed.get("status") != "OK":
        raise RemediationError("LOCAL_LLM_CLASSIFICATION_FAILED: smoke test status is not OK")


def classify_claims_local(
    candidates: list[dict[str, Any]],
    model: str,
    api_base: str,
) -> list[dict[str, Any]]:
    """
    Fail-closed local classifier.

    Important:
    - Candidates are processed independently.
    - Progress is printed before each LLM call.
    - A timeout/error identifies the exact candidate.
    - No automatic same-config retry.
    - No partial claim list is returned after a failed candidate.
    """

    import time

    smoke_test_local_llm(
        model,
        api_base,
    )

    claims: list[dict[str, Any]] = []

    total = len(candidates)

    for index, candidate in enumerate(
        candidates,
        1,
    ):
        text = str(
            candidate.get("text") or ""
        )

        candidate_id = (
            candidate.get("chunk_id")
            or candidate.get("document_id")
            or f"candidate-{index}"
        )

        print(
            f"classification_candidate="
            f"{index}/{total} "
            f"id={candidate_id} "
            f"chars={len(text)}",
            flush=True,
        )

        started = time.monotonic()

        try:
            parsed = _native_chat_json(
                model,
                api_base,
                _classification_system_prompt(),
                _llm_prompt(candidate),
            )

        except RemediationError as exc:
            elapsed = (
                time.monotonic()
                - started
            )

            raise RemediationError(
                "LOCAL_LLM_CLASSIFICATION_FAILED: "
                f"candidate_index={index} "
                f"candidate_id={candidate_id} "
                f"chars={len(text)} "
                f"elapsed_seconds={elapsed:.1f} "
                f"cause={exc}"
            ) from exc

        elapsed = (
            time.monotonic()
            - started
        )

        model_claims = parsed.get(
            "claims"
        )

        if not isinstance(
            model_claims,
            list,
        ):
            raise RemediationError(
                "LOCAL_LLM_CLASSIFICATION_FAILED: "
                f"candidate_index={index} "
                f"candidate_id={candidate_id} "
                "model response has no claims list"
            )

        admitted_here = 0

        for claim in model_claims:
            normalized = _validate_claim(
                claim,
                candidate,
            )

            if normalized is not None:
                claims.append(
                    normalized
                )
                admitted_here += 1

        print(
            f"classification_candidate_done="
            f"{index}/{total} "
            f"id={candidate_id} "
            f"claims={admitted_here} "
            f"elapsed_seconds={elapsed:.1f}",
            flush=True,
        )

    return claims



def _validate_claim(claim: Any, candidate: dict[str, Any]) -> dict[str, Any] | None:
    required = (
        "claim_text", "document_id", "source_relative_path", "locator", "scope", "qualifier",
        "source_type", "authority_state", "support_status", "section_applicability", "disposition", "reason",
    )
    if not isinstance(claim, dict) or any(key not in claim for key in required):
        return None
    if claim["disposition"] not in DISPOSITIONS:
        return None
    # Source identity is authoritative from retrieval, not model output.
    for key in ("document_id", "source_relative_path", "locator", "source_type", "authority_state"):
        claim[key] = candidate.get(key)
    claim["source_text"] = candidate.get("text")
    claim["chunk_id"] = candidate.get("chunk_id")
    if not claim["claim_text"] or not claim["document_id"] or not claim["source_text"]:
        return None
    return claim


def _deduplicate_claims(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[tuple[str, str, str], dict[str, Any]] = {}
    for claim in claims:
        key = (str(claim.get("document_id")), str(claim.get("locator")), re.sub(r"\s+", " ", str(claim.get("claim_text", "")).strip().casefold()))
        unique.setdefault(key, claim)
    return list(unique.values())


def determine_readiness(claims: list[dict[str, Any]], use_local_llm: bool, preexisting_validated: bool = False) -> str:
    if not use_local_llm:
        return "READY_WITH_LIMITATIONS" if preexisting_validated else "NEEDS_LOCAL_REVIEW"
    admitted = [c for c in claims if c.get("disposition") in {"ADMITTED_STRONG", "ADMITTED_LIMITED"}]
    if len(admitted) < 2:
        return "TRUE_CORPUS_EVIDENCE_GAP"
    strong = [c for c in admitted if c.get("disposition") == "ADMITTED_STRONG"]
    # Conservative minimum: at least two independently located atomic claims, one strong.
    locations = {(c.get("document_id"), c.get("locator")) for c in admitted}
    if strong and len(locations) >= 2:
        return "READY" if len(strong) >= 2 else "READY_WITH_LIMITATIONS"
    return "TRUE_CORPUS_EVIDENCE_GAP"


def build_writer_packet(state: dict[str, Any], claims: list[dict[str, Any]], readiness: str, generated_at: str) -> dict[str, Any] | None:
    admitted = [c for c in claims if c.get("disposition") in {"ADMITTED_STRONG", "ADMITTED_LIMITED"}]
    if not admitted or readiness not in {"READY", "READY_WITH_LIMITATIONS"}:
        return None
    for index, claim in enumerate(admitted, start=1):
        claim.setdefault("claim_id", f"{SECTION_ID}-REM-{index:03d}")
    citation_mapping = [{
        "claim_id": c["claim_id"], "document_id": c["document_id"],
        "source_relative_path": c.get("source_relative_path"), "locator": c.get("locator"),
    } for c in admitted]
    return {
        "section_id": SECTION_ID, "section_title": SECTION_TITLE,
        "section_scope": state.get("section_scope"),
        "scope_exclusions": list(SCOPE_EXCLUSIONS),
        "research_question": state.get("research_question") or state.get("research_question_id"),
        "readiness": readiness, "admitted_claims": admitted, "citation_mapping": citation_mapping,
        "source_locators": sorted({str(c.get("locator")) for c in admitted if c.get("locator")}),
        "provenance": [{"claim_id": c["claim_id"], "document_id": c["document_id"], "source_relative_path": c.get("source_relative_path")} for c in admitted],
        "qualifiers": [{"claim_id": c["claim_id"], "qualifier": c.get("qualifier")} for c in admitted],
        "evidence_limitations": [c.get("reason") for c in admitted if c.get("disposition") == "ADMITTED_LIMITED"],
        "generated_at": generated_at, "generator": "scripts/section_evidence_remediation.py",
        "privacy_mode": "LOCAL_ONLY",
    }


def versioned_path(directory: Path, basename: str, stamp: str) -> Path:
    target = directory / basename
    if not target.exists():
        return target
    path = Path(basename)
    stamped = directory / f"{path.stem}_{stamp}{path.suffix}"
    if not stamped.exists():
        return stamped
    counter = 2
    while True:
        candidate = directory / f"{path.stem}_{stamp}_v{counter}{path.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _jsonl_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def validate_outputs(candidates: list[dict[str, Any]], claims: list[dict[str, Any]], readiness: str, packet: dict[str, Any] | None) -> None:
    if readiness not in READINESS_VALUES:
        raise RemediationError("invalid readiness")
    if any(c.get("section_id") not in (None, SECTION_ID) for c in candidates):
        raise RemediationError("unrelated section candidate detected")
    admitted = [c for c in claims if c.get("disposition") in {"ADMITTED_STRONG", "ADMITTED_LIMITED"}]
    if any(not c.get("source_text") or not c.get("document_id") for c in admitted):
        raise RemediationError("admitted claim missing source evidence")
    if len(_deduplicate_claims(admitted)) != len(admitted):
        raise RemediationError("duplicate admitted claims")
    if packet:
        claim_ids = {c["claim_id"] for c in packet["admitted_claims"]}
        if packet.get("section_id") != SECTION_ID or packet.get("privacy_mode") != "LOCAL_ONLY":
            raise RemediationError("writer packet scope/privacy validation failed")
        if any(mapping.get("claim_id") not in claim_ids for mapping in packet["citation_mapping"]):
            raise RemediationError("citation mapping references unknown claim")


def _report(summary: dict[str, Any], state: dict[str, Any], outputs: list[str]) -> str:
    return "\n".join([
        f"# {SECTION_ID} Remediation Report", "", f"- Generated (UTC): {summary['generated_at']}",
        f"- Privacy: LOCAL_ONLY", f"- Mode: {summary['mode']}",
        f"- Candidates: {summary['candidate_count']}", f"- Strong claims: {summary['strong_claims']}",
        f"- Limited claims: {summary['limited_claims']}", f"- Rejected claims: {summary['rejected_claims']}",
        f"- Readiness: {summary['readiness']}", f"- Existing packet state: {state.get('packet_state') or 'UNKNOWN'}",
        "", "## Generated artifacts", "", *(f"- `{path}`" for path in outputs), "",
        "No book prose was generated. Frozen corpus, embeddings, Qdrant data, and retriever configuration were not modified.", "",
    ])


def write_artifacts(output_dir: Path, stamp: str, candidates: list[dict[str, Any]], packet: dict[str, Any] | None,
                    manifest: dict[str, Any], report_builder: Any) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = section_slug(SECTION_ID)
    paths = {
        "candidates": versioned_path(output_dir, f"{slug}_candidates.jsonl", stamp),
        "packet": versioned_path(output_dir, f"{slug}_writer_evidence_packet.json", stamp) if packet else None,
        "report": versioned_path(output_dir, f"{slug}_remediation_report.md", stamp),
        "manifest": versioned_path(output_dir, f"{slug}_remediation_manifest.json", stamp),
    }
    paths["candidates"].write_bytes(b"".join(_jsonl_bytes(c) for c in candidates))
    if packet and paths["packet"]:
        paths["packet"].write_bytes(_json_bytes(packet))
    generated = [p for key, p in paths.items() if p is not None and key != "manifest"]
    relative_outputs = [p.name for p in generated]
    paths["report"].write_text(report_builder(relative_outputs), encoding="utf-8")
    manifest["generated_artifacts"] = [{"path": p.name, "sha256": sha256_file(p)} for p in generated]
    paths["manifest"].write_bytes(_json_bytes(manifest))

    latest = {
        "section_id": SECTION_ID,
        "generated_at": manifest.get("generated_at"),
        "manifest_path": paths["manifest"].relative_to(output_dir.parents[3]).as_posix(),
        "manifest_sha256": sha256_file(paths["manifest"]),
        "packet_path": (
            paths["packet"].relative_to(output_dir.parents[3]).as_posix()
            if paths["packet"] is not None
            else None
        ),
        "packet_sha256": (
            sha256_file(paths["packet"])
            if paths["packet"] is not None
            else None
        ),
        "privacy_mode": "LOCAL_ONLY",
    }

    latest_path = output_dir / f"{section_slug(SECTION_ID)}_latest_run.json"
    tmp_path = latest_path.with_suffix(".tmp")

    tmp_path.write_bytes(_json_bytes(latest))
    tmp_path.replace(latest_path)

    return [paths["manifest"], *generated]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section-id", required=True)
    parser.add_argument("--use-local-llm", action="store_true")
    parser.add_argument("--model", default="qwen3.6-35b-a3b-mlx")
    parser.add_argument("--api-base", default="http://127.0.0.1:1234/v1")
    parser.add_argument("--max-candidates", type=int, default=15)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)
    if not 5 <= args.max_candidates <= 15:
        parser.error("--max-candidates must be between 5 and 15")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING, format="%(levelname)s: %(message)s")
    root = Path(__file__).resolve().parents[1]
    stamp = utc_stamp()
    try:
        configure_section(root, args.section_id)
        if args.use_local_llm:
            validate_local_endpoint(args.api_base)
        artifacts = find_project_artifacts(root)
        state = load_section_state(artifacts, root)
        retriever, retriever_path, retriever_config = resolve_retriever(root)
        raw = run_retrieval_queries(retriever, top_k=args.max_candidates)
        candidates = deduplicate_candidates(raw, args.max_candidates)
        if not candidates:
            raise RemediationError("NO_RETRIEVAL_RESULTS")
        classification_error = None
        try:
            claims = classify_claims_local(candidates, args.model, args.api_base) if args.use_local_llm else []
        except RemediationError as exc:
            if not str(exc).startswith("LOCAL_LLM_CLASSIFICATION_FAILED"):
                raise
            claims = []
            classification_error = str(exc)
        claims = _deduplicate_claims(claims)
        readiness = (
            "NEEDS_LOCAL_REVIEW"
            if classification_error
            else determine_readiness(claims, args.use_local_llm, preexisting_validated=False)
        )
        generated_at = datetime.now(timezone.utc).isoformat()
        packet = build_writer_packet(state, claims, readiness, generated_at)
        validate_outputs(candidates, claims, readiness, packet)
        counts = {
            "strong_claims": sum(c.get("disposition") == "ADMITTED_STRONG" for c in claims),
            "limited_claims": sum(c.get("disposition") == "ADMITTED_LIMITED" for c in claims),
            "rejected_claims": sum(str(c.get("disposition", "")).startswith("REJECT_") for c in claims),
        }
        summary = {"generated_at": generated_at, "mode": "LOCAL_LLM" if args.use_local_llm else "DETERMINISTIC_EXPORT",
                   "candidate_count": len(candidates), "readiness": readiness,
                   "classification_error": classification_error, **counts}
        source_hashes = [{"path": p.relative_to(root).as_posix(), "sha256": sha256_file(p)} for p in artifacts]
        manifest = {
            "section_id": SECTION_ID, "section_title": SECTION_TITLE, "generated_at": generated_at,
            "generator": "scripts/section_evidence_remediation.py", "privacy_mode": "LOCAL_ONLY", "summary": summary,
            "section_state": state, "search_queries": list(SEARCH_QUERIES), "retriever_config": retriever_config,
            "integrity": {"source_artifacts": source_hashes, "retriever": {"path": retriever_path.relative_to(root).as_posix(), "sha256": sha256_file(retriever_path)}},
            "validation": {"target_only": True, "frozen_assets_written": False, "outputs_validated": True},
        }
        output_dir = root / "data" / "book" / "remediation" / section_slug(SECTION_ID)
        if not args.dry_run:
            write_artifacts(output_dir, stamp, candidates, packet, manifest, lambda outputs: _report(summary, state, outputs))
        print(f"section={SECTION_ID}")
        print(f"candidate_count={len(candidates)}")
        print(f"strong_claims={counts['strong_claims']}")
        print(f"limited_claims={counts['limited_claims']}")
        print(f"rejected_claims={counts['rejected_claims']}")
        print(f"readiness={readiness}")
        if classification_error:
            print(f"classification_error={classification_error}")
        print(f"output_directory={output_dir.relative_to(root) if not args.dry_run else 'DRY_RUN'}")
        print(f"next_action={'review candidate bundle locally' if not args.use_local_llm else 'review admitted claims before drafting'}")
        return 0
    except RemediationError as exc:
        LOG.error("%s", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
