"""Read-only corpus explorer and manual-review projection for the dashboard."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

from tunnelbookai.population.batching import _verify_run
from tunnelbookai.population.models import atomic_json, load_object, now


PROBLEM_DISPOSITIONS = {"FAILED", "NEEDS_REVIEW", "RECOVERY_REQUIRED", "REJECTED", "UNSUPPORTED"}
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".jsonl", ".csv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PREVIEW_EXTENSIONS = TEXT_EXTENSIONS | IMAGE_EXTENSIONS
MAX_CHUNK_TEXT = 20_000

# These codes describe an intentional fallback or a successful recovery.  They are
# useful operational telemetry, but presenting them as improvement candidates makes
# a healthy run look broken.
INFORMATIONAL_WARNING_CODES = {
    "CHART_EXTRACTION_DISABLED_BY_CONFIG",
    "CHUNK_SHORT_STRUCTURAL",
    "DUPLICATE_EXACT",
    "DUPLICATE_STRONG",
    "FIGURE_OCR_SKIPPED_PAGE_OCR_ALREADY_RUN",
    "NATIVE_TEXT_LAYER_THIN_DOCLING_OCR_RECOVERED",
    "NATIVE_TEXT_LAYER_THIN_OCR_FALLBACK",
    "PPT_CONVERTED_TO_PPTX",
    "XLS_CONVERTED_TO_XLSX",
    "XLSX_CSV_SKIPPED_MERGED_CELLS",
}


def _object(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file() or path.is_symlink():
        return []
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if not line.strip():
                    continue
                value = json.loads(line)
                if isinstance(value, dict):
                    rows.append(value)
    except (OSError, ValueError):
        return []
    return rows


def _inventory(run: dict[str, Any], root: Path) -> dict[str, dict[str, Any]]:
    path = root / "audit" / "corpus_population" / "inventories" / f"{run['inventory_id']}.json"
    payload = _object(path)
    documents = payload.get("documents") or []
    return {
        str(row["document_id"]): row
        for row in documents
        if isinstance(row, dict) and row.get("document_id")
    }


def _source_summary(inventory: dict[str, Any]) -> dict[str, Any]:
    aliases = inventory.get("source_aliases") or []
    primary = next((row for row in aliases if row.get("alias_classification") == "PRIMARY"), None)
    primary = primary or (aliases[0] if aliases else {})
    path = str(primary.get("path") or "")
    return {
        "format": inventory.get("format") or primary.get("format") or "—",
        "size": int(inventory.get("size") or primary.get("size") or 0),
        "source_path": path or None,
        "source_name": PurePosixPath(path).name if path else None,
        "source_kind": primary.get("source_kind"),
    }


def outcome_reason(row: dict[str, Any], report: dict[str, Any], quality: dict[str, Any]) -> str:
    disposition = str(row.get("disposition") or "PENDING")
    chunks = int(row.get("chunk_count") or 0)
    section = row.get("final_primary_section")
    errors = list(row.get("errors") or report.get("errors") or [])
    review = list(quality.get("review_reasons") or [])
    rejects = list(quality.get("reject_reasons") or [])
    if disposition == "PENDING":
        return "Henüz işlem sırası gelmedi."
    if disposition == "RECOVERY_REQUIRED":
        return "Önceki işlem yarıda kesildi; güvenli checkpoint üzerinden yeniden denenecek."
    if disposition == "DUPLICATE":
        return f"Kopya belge; chunk ve bölüm asıl belgede tutuluyor: {row.get('duplicate_of') or 'bilinmiyor'}."
    if disposition == "ALREADY_CANONICAL":
        return "Belge zaten canonical corpus içinde; yeniden chunk üretilmedi."
    if disposition == "ALREADY_PROCESSED":
        return "Önceki geçerli processing çıktısı kullanıldı; bu run satırında sayaçlar yeniden yazılmamış olabilir."
    if disposition == "UNSUPPORTED":
        return "Dosya türü mevcut ingest hattı tarafından desteklenmiyor."
    if disposition == "STAGED" and chunks > 0 and section:
        return "İşlem tamamlandı. Uyarılar belge ayrıntısındaki raporlarda görülebilir."
    if errors:
        return f"Okuma/çıkarma hatası: {errors[0]}"
    if rejects:
        return f"Kalite kapısı reddetti: {rejects[0]}"
    if review:
        return f"Manuel inceleme gerekiyor: {review[0]}"
    if chunks == 0:
        chars = int(report.get("text_char_count") or 0)
        if chars == 0:
            return "Okunabilir metin çıkarılamadığı için chunk oluşturulmadı."
        return f"Metin çıkarıldı ({chars:,} karakter) fakat chunk üretimi 0 sonuç verdi; chunker incelemesi gerekiyor."
    if not section:
        return "Chunk üretildi fakat sınıflandırma güvenilir bir kitap bölümü seçemedi."
    return "İşlem tamamlandı."


def _document_row(document_id: str, row: dict[str, Any], inventory: dict[str, Any], root: Path) -> dict[str, Any]:
    bundle = root / "processing" / document_id
    report = _object(bundle / "extraction_report.json")
    quality = _object(bundle / "quality_gate.json")
    source = _source_summary(inventory)
    chunks = int(row.get("chunk_count") or 0)
    if not chunks:
        chunks = len(_jsonl(bundle / "chunks" / "chunk_manifest.jsonl"))
    section = row.get("final_primary_section")
    if not section:
        section = _object(bundle / "classification.json").get("final_primary_section")
    result = {
        "document_id": document_id,
        "disposition": row.get("disposition") or "PENDING",
        "section": section,
        "chunks": chunks,
        "embedding_ready_chunks": int(row.get("embedding_ready_chunks") or 0),
        "pages": int(report.get("page_count") or len(report.get("pages") or [])),
        "tables": len(report.get("tables") or []),
        "figures": len(report.get("figures") or []),
        "warnings": list(row.get("warnings") or report.get("warnings") or [])[:8],
        "errors": list(row.get("errors") or report.get("errors") or [])[:8],
        "reason": outcome_reason(row, report, quality),
        "has_processing": bundle.is_dir(),
        **source,
    }
    result["needs_attention"] = (
        result["disposition"] in PROBLEM_DISPOSITIONS
        or (result["disposition"] == "STAGED" and result["chunks"] == 0)
        or (result["disposition"] == "STAGED" and not result["section"])
    )
    return result


def documents_projection(
    run_path: Path,
    project_root: Path,
    *,
    query: str = "",
    disposition: str = "ALL",
    page: int = 1,
    page_size: int = 50,
) -> dict[str, Any]:
    run = load_object(run_path)
    _verify_run(run)
    inventory = _inventory(run, project_root)
    rows = [
        _document_row(document_id, row, inventory.get(document_id, {}), project_root)
        for document_id, row in run["documents"].items()
    ]
    needle = query.casefold().strip()
    if needle:
        rows = [row for row in rows if needle in " ".join(str(row.get(key) or "") for key in (
            "document_id", "source_name", "source_path", "format", "disposition", "section", "reason"
        )).casefold()]
    if disposition == "ATTENTION":
        rows = [row for row in rows if row["needs_attention"]]
    elif disposition != "ALL":
        rows = [row for row in rows if row["disposition"] == disposition]
    rows.sort(key=lambda row: (row["disposition"] == "PENDING", row["document_id"]))
    total = len(rows)
    page_size = min(100, max(10, int(page_size)))
    pages = max(1, (total + page_size - 1) // page_size)
    page = min(pages, max(1, int(page)))
    start = (page - 1) * page_size
    return {"documents": rows[start:start + page_size], "total": total, "page": page, "pages": pages, "page_size": page_size}


def _preview_assets(document_id: str, root: Path) -> list[dict[str, Any]]:
    bundle = root / "processing" / document_id
    if not bundle.is_dir() or bundle.is_symlink():
        return []
    assets: list[dict[str, Any]] = []
    for path in sorted(bundle.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in PREVIEW_EXTENSIONS:
            continue
        relative = path.relative_to(bundle).as_posix()
        kind = "image" if path.suffix.lower() in IMAGE_EXTENSIONS else "text"
        assets.append({
            "name": relative,
            "kind": kind,
            "size": path.stat().st_size,
            "url": f"/api/preview?document_id={quote(document_id)}&path={quote(relative)}",
        })
    return assets


def document_projection(run_path: Path, project_root: Path, document_id: str) -> dict[str, Any]:
    run = load_object(run_path)
    _verify_run(run)
    if document_id not in run["documents"]:
        raise ValueError("document is not part of this run")
    inventory = _inventory(run, project_root).get(document_id, {})
    bundle = project_root / "processing" / document_id
    detail = _document_row(document_id, run["documents"][document_id], inventory, project_root)
    detail["classification"] = _object(bundle / "classification.json")
    detail["quality_gate"] = _object(bundle / "quality_gate.json")
    detail["extraction"] = _object(bundle / "extraction_report.json")
    detail["metadata"] = _object(bundle / "metadata.json")
    chunks = []
    for row in _jsonl(bundle / "chunks" / "chunk_manifest.jsonl"):
        body = str(row.get("text") or row.get("embedding_text") or "")
        chunks.append({
            "chunk_id": row.get("chunk_id"),
            "ordinal": row.get("ordinal"),
            "chunk_type": row.get("chunk_type"),
            "section": row.get("final_primary_section") or row.get("section_id"),
            "heading_path": row.get("heading_path") or [],
            "token_count": row.get("token_count"),
            "page_start": row.get("page_start"),
            "page_end": row.get("page_end"),
            "text": body[:MAX_CHUNK_TEXT],
            "truncated": len(body) > MAX_CHUNK_TEXT,
        })
    detail["chunk_items"] = chunks
    detail["assets"] = _preview_assets(document_id, project_root)
    return detail


def _duration_seconds(start: Any, finish: Any) -> float:
    try:
        return max(0.0, (datetime.fromisoformat(str(finish)) - datetime.fromisoformat(str(start))).total_seconds())
    except (TypeError, ValueError):
        return 0.0


def statistics_projection(run_path: Path, project_root: Path) -> dict[str, Any]:
    run = load_object(run_path)
    _verify_run(run)
    inventory = _inventory(run, project_root)
    assets = Counter()
    formats = Counter()
    warnings = Counter()
    informational_warnings = Counter()
    processed = 0
    chunk_types = Counter()
    for document_id, row in run["documents"].items():
        disposition = str(row.get("disposition") or "PENDING")
        if disposition not in {"PENDING", "RECOVERY_REQUIRED"}:
            processed += 1
        formats[str(inventory.get(document_id, {}).get("format") or "UNKNOWN")] += 1
        report = _object(project_root / "processing" / document_id / "extraction_report.json")
        assets["pages"] += int(report.get("page_count") or len(report.get("pages") or []))
        for key in ("tables", "figures", "charts", "slides", "sheets", "ocr_items"):
            assets[key] += len(report.get(key) or [])
        assets["text_characters"] += int(report.get("text_char_count") or 0)
        if (report.get("capabilities") or {}).get("ocr"):
            assets["ocr_documents"] += 1
        if report.get("normalized_markdown_path"):
            assets["markdown_documents"] += 1
        # Run checkpoints intentionally copy extraction warnings.  Count each code
        # once per document so that the dashboard reports affected documents rather
        # than double-counting the same persisted warning.
        warning_codes = {
            str(item).split(":", 1)[0]
            for item in list(row.get("warnings") or []) + list(report.get("warnings") or [])
        }
        for code in warning_codes:
            target = informational_warnings if code in INFORMATIONAL_WARNING_CODES else warnings
            target[code] += 1
        for chunk in _jsonl(project_root / "processing" / document_id / "chunks" / "chunk_manifest.jsonl"):
            chunk_types[str(chunk.get("chunk_type") or "UNKNOWN")] += 1

    elapsed = 0.0
    checkpointed = 0
    attempt_statuses = Counter()
    for attempt_id in run.get("attempt_ids") or []:
        attempt = _object(project_root / "audit" / "corpus_population" / "attempts" / f"{attempt_id}.json")
        attempt_statuses[str(attempt.get("status") or "UNKNOWN")] += 1
        elapsed += _duration_seconds(attempt.get("started_at"), attempt.get("finished_at"))
        checkpointed += int((attempt.get("summary") or {}).get("documents_checkpointed") or 0)
    seconds_per_document = elapsed / checkpointed if checkpointed else None
    remaining = sum(1 for row in run["documents"].values() if (row.get("disposition") or "PENDING") in {"PENDING", "RECOVERY_REQUIRED"})
    return {
        "processed_documents": processed,
        "total_documents": len(run["documents"]),
        "remaining_documents": remaining,
        "assets": dict(assets),
        "chunk_types": dict(sorted(chunk_types.items())),
        "formats": dict(sorted(formats.items(), key=lambda item: (-item[1], item[0]))),
        "top_warnings": [{"code": code, "count": count} for code, count in warnings.most_common(10)],
        "informational_warnings": [
            {"code": code, "count": count}
            for code, count in informational_warnings.most_common(10)
        ],
        "warning_note": (
            "Sayılar etkilenen benzersiz belge sayısını gösterir. Bilgi kayıtları, "
            "başarılı fallback veya bilinçli yapılandırma kararlarıdır."
        ),
        "attempts": dict(sorted(attempt_statuses.items())),
        "observed_seconds": round(elapsed),
        "seconds_per_document": round(seconds_per_document, 1) if seconds_per_document else None,
        "estimated_remaining_seconds": round(seconds_per_document * remaining) if seconds_per_document else None,
        "note": "Süre tahmini tamamlanan checkpoint’lerin gerçek duvar saati süresinden hesaplanır; büyük taranmış PDF’ler nedeniyle değişebilir.",
    }


def review_path(project_root: Path) -> Path:
    return project_root / "audit" / "dashboard" / "manual_review.json"


def _review_state(project_root: Path) -> dict[str, Any]:
    path = review_path(project_root)
    value = _object(path)
    if value.get("schema_version") != "1.0":
        return {"schema_version": "1.0", "documents": {}}
    return value


def review_projection(run_path: Path, project_root: Path) -> dict[str, Any]:
    run = load_object(run_path)
    _verify_run(run)
    inventory = _inventory(run, project_root)
    state = _review_state(project_root)
    rows = []
    for document_id, run_row in run["documents"].items():
        row = _document_row(document_id, run_row, inventory.get(document_id, {}), project_root)
        saved = (state.get("documents") or {}).get(document_id) or {}
        if not row["needs_attention"] and saved.get("status") != "OPEN":
            continue
        row["review_status"] = saved.get("status") or "OPEN"
        row["review_note"] = saved.get("note") or ""
        row["review_updated_at"] = saved.get("updated_at")
        rows.append(row)
    rows.sort(key=lambda row: (row["review_status"] == "RESOLVED", row["document_id"]))
    return {"documents": rows, "open": sum(row["review_status"] == "OPEN" for row in rows), "total": len(rows)}


def update_review(run_path: Path, project_root: Path, document_id: str, status: str, note: str = "") -> dict[str, Any]:
    run = load_object(run_path)
    _verify_run(run)
    if document_id not in run["documents"]:
        raise ValueError("document is not part of this run")
    if status not in {"OPEN", "RESOLVED"}:
        raise ValueError("review status must be OPEN or RESOLVED")
    state = _review_state(project_root)
    state.setdefault("documents", {})[document_id] = {
        "status": status,
        "note": str(note).strip()[:1000],
        "updated_at": now(),
    }
    atomic_json(review_path(project_root), state)
    return state["documents"][document_id]


def resolve_preview(project_root: Path, run_path: Path, document_id: str, relative_path: str) -> tuple[Path, str]:
    run = load_object(run_path)
    if document_id not in run.get("documents", {}):
        raise ValueError("document is not part of this run")
    relative = PurePosixPath(relative_path)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError("invalid preview path")
    base = (project_root / "processing" / document_id).resolve()
    candidate = base.joinpath(*relative.parts)
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError("preview file not found")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(base) or resolved.suffix.lower() not in PREVIEW_EXTENSIONS:
        raise ValueError("preview file is not allowed")
    return resolved, "image" if resolved.suffix.lower() in IMAGE_EXTENSIONS else "text"


__all__ = [
    "document_projection", "documents_projection", "outcome_reason", "resolve_preview",
    "review_projection", "statistics_projection", "update_review",
]
