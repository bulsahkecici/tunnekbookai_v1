"""Per-document stage orchestration (task §66, §67).

    ORIGINAL_ARCHIVED -> EXTRACTING -> EXTRACTED -> ASSETS_EXTRACTED -> OCR_COMPLETED
      -> METADATA_COMPLETED -> DEDUP_COMPLETED -> CLASSIFIED -> QUALITY_GATED -> STAGED
      -> CHUNKING -> CHUNKED -> CHUNK_QUALITY_GATED -> EMBEDDING_READY

REVIEW / REJECTED / FAILED remain branches off this line. Every stage writes its artifact
into `processing/<document_id>/` before the state transition, so `--resume` always finds a
coherent bundle.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import evidence as evidence_module
from . import quality_gate as gate_module
from . import staging as staging_module
from .adapters import AdapterContext, get_adapter
from .chunking import manifest as manifest_module
from .chunking import quality as chunk_quality_module
from .chunking.chunker import ChunkingContext, chunk_document, write_chunks
from .chunking.policy import ChunkPolicy
from .classify import pipeline as classify_module
from .config import IngestConfig
from .dedup import SourceRegistry, resolve as dedup_resolve
from .extraction import ExtractionResult, write_extraction_report
from .glyph_repair import repair_extraction
from .format_registry import Detection
from .metadata.enrich import build_metadata, write_metadata
from .paths import PATHS, relpath
from .state import IngestState, State


@dataclass
class DocumentOutcome:
    document_id: str
    state: State
    decision: str | None = None
    evidence_level: str | None = None
    primary_section: str | None = None
    chunk_count: int = 0
    chunk_quality_status: str | None = None
    embedding_ready_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    staging_path: str | None = None
    duplicate_of: str | None = None

    def as_row(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "state": self.state.value,
            "quality_decision": self.decision,
            "final_evidence_level": self.evidence_level,
            "final_primary_section": self.primary_section,
            "chunk_count": self.chunk_count,
            "chunk_quality_status": self.chunk_quality_status,
            "embedding_ready_chunks": self.embedding_ready_count,
            "staging_path": self.staging_path,
            "duplicate_of": self.duplicate_of,
            "warnings": self.warnings,
            "errors": self.errors,
        }


@dataclass
class PipelineServices:
    """Shared, expensive resources built once per run."""
    config: IngestConfig
    ocr: Any = None
    vision: Any = None
    office_renderer: Any = None
    registry: SourceRegistry | None = None
    embedding_index: Any = None
    embedding_status: str | None = None
    embedding_model: str | None = None
    do_ocr: bool = True
    do_vision: bool = True
    do_chunking: bool = True
    allow_arbiter: bool = True
    root: Path = PATHS.root

    @property
    def chunk_policy(self) -> ChunkPolicy:
        return ChunkPolicy.from_config(self.config)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def process_document(
    *,
    document_id: str,
    detection: Detection,
    archive_meta: dict[str, Any],
    services: PipelineServices,
    state: IngestState,
    source_kind: str,
) -> DocumentOutcome:
    bundle = PATHS.processing_bundle(document_id)
    bundle.mkdir(parents=True, exist_ok=True)
    original_path = services.root / archive_meta["archive_path"]
    provenance_doc = _read_json(bundle / "provenance.json")
    outcome = DocumentOutcome(document_id=document_id, state=State.ORIGINAL_ARCHIVED)

    # ------------------------------------------------------------------ extraction
    state.transition(document_id, State.EXTRACTING, source_kind=source_kind)
    context = AdapterContext(
        document_id=document_id, original_path=original_path,
        original_filename=archive_meta.get("original_filename") or original_path.name,
        bundle=bundle,
        detection=detection, config=services.config, ocr=services.ocr,
        vision=services.vision, office_renderer=services.office_renderer,
        root=services.root, do_ocr=services.do_ocr, do_vision=services.do_vision,
    )
    try:
        extraction = get_adapter(detection.adapter)(context)
    except Exception as exc:
        extraction = ExtractionResult(document_id=document_id, format=detection.fmt.value,
                                      adapter=detection.adapter)
        extraction.fail(f"ADAPTER_CRASHED:{type(exc).__name__}: {exc}")
    if extraction.succeeded:
        # Some Turkish PDFs isolate ı/ş/ğ/ü/ö/ç glyphs with spaces; repair the derived text
        # before metadata, classification and chunking read it (original bytes untouched).
        try:
            repair_extraction(extraction, bundle, services.root)
        except Exception as exc:  # never let a repair bug fail a valid extraction
            extraction.warn(f"TURKISH_GLYPH_SPACING_REPAIR_FAILED:{type(exc).__name__}")
    write_extraction_report(bundle, extraction)
    outcome.warnings += extraction.warnings
    outcome.errors += extraction.errors

    if not extraction.succeeded:
        state.transition(document_id, State.FAILED, source_kind=source_kind,
                         error="; ".join(extraction.errors)[:500],
                         warnings=extraction.warnings)
        outcome.state = State.FAILED
        return outcome

    state.transition(document_id, State.EXTRACTED, source_kind=source_kind,
                     detail={"adapter": extraction.adapter,
                             "pages": extraction.page_count})
    state.transition(document_id, State.ASSETS_EXTRACTED, source_kind=source_kind,
                     detail={"tables": len(extraction.tables), "figures": len(extraction.figures),
                             "charts": len(extraction.charts), "snapshots": len(extraction.pages)})

    # ------------------------------------------------------------------ vision on figures
    if services.do_vision and services.vision is not None and extraction.figures:
        from .vision.provider import describe_figures

        outcome.warnings += describe_figures(services.vision, extraction.figures, services.root)
    # Vision runs AFTER the adapter, so the adapter's capability flags are stale here —
    # recompute the ones the vision/OCR stage can change, then rewrite the report.
    extraction.capabilities["vision"] = any(
        f.get("visual_description_status") == "SUCCESS" for f in extraction.figures)
    extraction.capabilities["ocr"] = bool(extraction.capabilities.get("ocr")) or any(
        f.get("ocr_status") == "SUCCESS" for f in extraction.figures)
    write_extraction_report(bundle, extraction)
    state.transition(document_id, State.OCR_COMPLETED, source_kind=source_kind,
                     detail={"vision": extraction.capabilities["vision"],
                             "ocr": extraction.capabilities["ocr"]})

    # ------------------------------------------------------------------ metadata
    metadata, provenance_log, metadata_warnings = build_metadata(
        document_id=document_id, archive_meta=archive_meta, provenance_doc=provenance_doc,
        extraction=extraction, config=services.config, original_path=original_path)
    outcome.warnings += metadata_warnings

    evidence_level, evidence_reasons = evidence_module.determine(extraction)
    metadata["final_evidence_level"] = evidence_level
    metadata["content_capabilities"] = evidence_module.content_capabilities(extraction)
    outcome.evidence_level = evidence_level

    write_metadata(bundle, metadata, provenance_log)
    state.transition(document_id, State.METADATA_COMPLETED, source_kind=source_kind,
                     detail={"evidence_level": evidence_level,
                             "evidence_reasons": evidence_reasons})

    # ------------------------------------------------------------------ dedup
    registry = services.registry
    match = None
    if registry is not None:
        match, dedup_warnings = dedup_resolve(
            registry, metadata,
            source_kinds=list(archive_meta.get("source_kinds") or [source_kind]),
            state=State.DEDUP_COMPLETED.value,
            provenance_sources=provenance_doc.get("sources"))
        outcome.warnings += dedup_warnings
        if match is not None and match.strength != "PROBABLE":
            outcome.duplicate_of = match.document_id
    state.transition(document_id, State.DEDUP_COMPLETED, source_kind=source_kind,
                     detail={"duplicate_of": outcome.duplicate_of})

    if match is not None and match.strength != "PROBABLE":
        state.transition(
            document_id, State.DUPLICATE, source_kind=source_kind,
            detail={"duplicate_of": match.document_id, "duplicate_rule": match.rule},
        )
        if registry is not None:
            registry.rows[document_id]["state"] = State.DUPLICATE.value
        outcome.state = State.DUPLICATE
        return outcome

    # ------------------------------------------------------------------ classification
    normalized_text = ""
    if extraction.normalized_text_path:
        text_path = services.root / extraction.normalized_text_path
        if text_path.is_file():
            normalized_text = text_path.read_text(encoding="utf-8", errors="replace")

    classification = classify_module.classify(
        metadata=metadata, elements=extraction.text_elements, tables=extraction.tables,
        figures=extraction.figures, normalized_text=normalized_text, config=services.config,
        embedding_index=services.embedding_index,
        embedding_status=services.embedding_status,
        embedding_model=services.embedding_model,
        allow_arbiter=services.allow_arbiter)
    classify_module.write_classification(bundle, classification)
    outcome.warnings += classification.warnings
    outcome.primary_section = classification.final_primary_section

    metadata["final_primary_section"] = classification.final_primary_section
    metadata["final_secondary_sections"] = classification.final_secondary_sections
    metadata["final_section_confidence"] = classification.final_section_confidence
    write_metadata(bundle, metadata, provenance_log)
    state.transition(document_id, State.CLASSIFIED, source_kind=source_kind,
                     detail={"final_primary_section": classification.final_primary_section,
                             "confidence": classification.final_section_confidence})

    # ------------------------------------------------------------------ quality gate
    gate = gate_module.evaluate(
        document_id=document_id, archive_meta=archive_meta, provenance_doc=provenance_doc,
        extraction=extraction, metadata=metadata, classification=classification,
        evidence_level=evidence_level, config=services.config, original_path=original_path)
    if match is not None and match.strength == "PROBABLE":
        gate.review_reasons.append(
            f"DUPLICATE_CANDIDATE:{match.rule}:{match.document_id}"
        )
        if gate.decision == gate_module.GO:
            gate.decision = gate_module.REVIEW
    gate_module.write_gate(bundle, document_id, gate)
    outcome.decision = gate.decision
    outcome.warnings += gate.review_reasons
    state.transition(document_id, State.QUALITY_GATED, source_kind=source_kind,
                     detail={"decision": gate.decision,
                             "reject_reasons": gate.reject_reasons,
                             "review_reasons": gate.review_reasons})

    if gate.decision == gate_module.REJECT:
        state.transition(document_id, State.REJECTED, source_kind=source_kind,
                         error="; ".join(gate.reject_reasons)[:500])
        outcome.state = State.REJECTED
        return outcome

    # ------------------------------------------------------------------ chunking (§48)
    chunks: list[dict[str, Any]] = []
    chunk_report: dict[str, Any] = {}
    policy = services.chunk_policy
    if services.do_chunking:
        state.transition(document_id, State.CHUNKING, source_kind=source_kind)
        chunk_context = ChunkingContext(
            document_id=document_id,
            original_sha256=metadata.get("original_sha256"),
            source_kind=metadata.get("source_kind"),
            final_primary_section=classification.final_primary_section,
            final_secondary_sections=classification.final_secondary_sections,
            format=metadata.get("format"),
            evidence_level=evidence_level,
        )
        chunks, dropped = chunk_document(
            context=chunk_context, elements=extraction.text_elements,
            tables=extraction.tables, figures=extraction.figures,
            slides=extraction.slides, sheets=extraction.sheets,
            ocr_items=extraction.ocr_items, policy=policy, root=services.root)
        write_chunks(bundle, chunks)
        outcome.chunk_count = len(chunks)
        state.transition(document_id, State.CHUNKED, source_kind=source_kind,
                         detail={"chunk_count": len(chunks), "deduplicated": len(dropped)})

        chunk_report = chunk_quality_module.evaluate(
            document_id=document_id, chunks=chunks, elements=extraction.text_elements,
            tables=extraction.tables, figures=extraction.figures, sheets=extraction.sheets,
            slides=extraction.slides, policy=policy, dropped=dropped)
        chunk_quality_module.write_report(bundle, chunk_report)
        outcome.chunk_quality_status = chunk_report["status"]
        outcome.warnings += chunk_report["warnings"][:10]
        outcome.errors += chunk_report["errors"][:10]
        state.transition(document_id, State.CHUNK_QUALITY_GATED, source_kind=source_kind,
                         detail={"chunk_quality": chunk_report["status"]})

    # ------------------------------------------------------------------ staging (§46)
    if gate.decision == gate_module.GO:
        staging_path, staging_warnings = staging_module.stage_document(
            document_id=document_id, bundle=bundle, metadata=metadata,
            classification=classification.to_dict(), gate=gate.to_dict(document_id),
            evidence_level=evidence_level, chunk_count=len(chunks),
            chunk_quality_status=chunk_report.get("status"))
        outcome.staging_path = relpath(staging_path)
        outcome.warnings += staging_warnings
        state.transition(document_id, State.STAGED, source_kind=source_kind,
                         detail={"staging_path": outcome.staging_path})
        outcome.state = State.STAGED
    else:
        state.transition(document_id, State.REVIEW, source_kind=source_kind,
                         detail={"review_reasons": gate.review_reasons})
        outcome.state = State.REVIEW

    # ------------------------------------------------------- embedding-ready rows (§64)
    if services.do_chunking and chunks:
        rows = manifest_module.build_rows(
            chunks, policy,
            document_staged=(outcome.state == State.STAGED),
            chunk_quality_ok=(chunk_report.get("status") != chunk_quality_module.FAIL))
        (bundle / "chunks").mkdir(parents=True, exist_ok=True)
        (bundle / "chunks" / "embedding_ready.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows),
            encoding="utf-8")
        outcome.embedding_ready_count = sum(1 for r in rows if r["eligible"])
        if outcome.state == State.STAGED and outcome.embedding_ready_count:
            state.transition(document_id, State.EMBEDDING_READY, source_kind=source_kind,
                             detail={"eligible_chunks": outcome.embedding_ready_count})
            outcome.state = State.EMBEDDING_READY
    return outcome
