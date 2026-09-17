"""Apply the 2026-09-13 human review decisions as one auditable repair.

This is intentionally run-specific.  It updates every upstream artifact that canonical
eligibility verifies, but never writes to ``corpus/canonical``.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tunnelbookai.canonical.eligibility import inspect_candidate
from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.ingest.chunking.chunker import (
    ChunkingContext,
    build_text_chunks,
    deduplicate,
    read_chunks,
    write_chunks,
)
from tunnelbookai.ingest.chunking.manifest import build_rows, merge_into
from tunnelbookai.ingest.chunking.policy import FIGURE_CHUNK, TEXT_CHUNK, ChunkPolicy, chunk_id
from tunnelbookai.ingest.chunking.quality import evaluate
from tunnelbookai.ingest.config import load_config
from tunnelbookai.ingest.dedup import DedupKey, SourceRegistry, active_document_ids
from tunnelbookai.ingest.paths import PATHS, relpath
from tunnelbookai.ingest.staging import stage_document, staging_dir
from tunnelbookai.ingest.state import IngestState, State
from tunnelbookai.population.models import PopulationState, atomic_json, load_object, now


APPROVALS: dict[str, dict[str, Any]] = {
    # Recovered zero-chunk records, content-checked after reprocessing.
    "ING_099561279b8b8ee35d23": {
        "primary": "1.2",
        "secondary": ["5.4"],
        "note": "Road-tunnel categorisation and dangerous-goods QRA presentation verified after recovery.",
    },
    "ING_118ff7fa533b54f5bb33": {
        "primary": "2.1.2",
        "note": "Steel-fibre reinforced shotcrete support presentation verified after recovery.",
    },
    "ING_1ae6c3af5113537e857e": {
        "primary": "6.2.2",
        "note": "International TBM construction cost-estimation study verified after recovery.",
    },
    "ING_33492a3e3e95d6e412e6": {
        "primary": "5.7",
        "note": "Sloped-tunnel ventilation modelling study verified after recovery.",
    },
    "ING_41d2c9398626bde710c0": {
        "primary": "2.2.1",
        "note": "NATM urban-metro construction-method paper verified after recovery.",
    },
    "ING_4ab4f078440c18fa18d4": {
        "primary": "2.2.2",
        "note": "Bertha soft-ground tunnel-boring-machine case study verified after recovery.",
    },
    "ING_4ddfacba06240aa3a164": {
        "primary": "2.1.2",
        "secondary": ["2.2.2"],
        "note": "Shield-tunnel segmental-lining FEM study verified after recovery.",
    },
    "ING_83f9b702512fb05b106d": {
        "primary": "5.7",
        "note": "Baikal tunnel emergency ventilation operating modes verified after recovery.",
    },
    "ING_945f8f6f7b425afc57c0": {
        "primary": "2.2.2",
        "secondary": ["2.4.1.1"],
        "note": "Twin-tunnel soft-ground settlement prediction study verified after recovery.",
    },
    # Original dashboard review queue.
    "ING_09816e42debecc51360d": {"primary": "2.2.3"},
    "ING_8fe8fef7af0d690a8c07": {"primary": "2.2.1"},
    "ING_9a2ffc561cb5b6efbca1": {"primary": "6.2.2"},
    "ING_aebfb2790f94d4239847": {"primary": "6.2.2"},
    "ING_b4f94b799877cc9a1caf": {"primary": "2.1.2"},
    "ING_d9c66f67c8cd3a7175f3": {"primary": "2.2.1"},
    "ING_de42fd6ef4103d8d294a": {"primary": "2.4.1", "secondary": ["6.2.2"]},
    "ING_ead747fa32f53391bef5": {"primary": "2.2.3"},
    "ING_1c8cf251c81e8ae5e70c": {
        "primary": "5.4",
        "page_window": [14, 20],
        "note": "Only the Tunnel Operation Regulation on pages 14-20 was retained.",
    },
    "ING_686f2fed7a37fea40455": {
        "primary": "5.9.1",
        "note": "Approved as an issue-level national tunnelling literature source; article boundaries remain represented by chunk/page provenance.",
    },
    "ING_3b434b03f09745ed6d9c": {
        "primary": "2.1.2",
        "figure_text": "Tünel aynasında enjeksiyon ve delgi çalışması yapan çok kollu makine ile saha ekibi görülmektedir.",
    },
    "ING_c5b8b61e1d07edae30e7": {
        "primary": "2.1.2",
        "figure_text": "Kaya yüzeyinde su sızıntısına karşı yüksek basınçlı enjeksiyon uygulaması yapan tünel ekipmanı görülmektedir.",
    },
    "ING_c77a14960e997ca95740": {
        "primary": "2.1.1",
        "figure_text": "Tünel tabanında invert betonu dökümü ve kalıp uygulaması için kullanılan hareketli saha ekipmanı görülmektedir.",
    },
    # Recovered hard-limit failures, content-checked after the chunker repair.
    "ING_296bae6c6d0e76f84818": {
        "primary": "3",
        "secondary": ["1.4.2"],
        "note": "KGM/Türkiye tünel envanterini tamamlanan, yapımı süren ve planlanan tüneller olarak özetleyen 2019 tarihli icmal doğrulandı.",
    },
    "ING_e5a3c44428f7d13e2a85": {
        "primary": "3",
        "secondary": ["1.4.2"],
        "note": "KGM/Türkiye tünel envanteri icmalinin kilometre ve metre sürümleri içerik üzerinden doğrulandı.",
    },
    "ING_991a4bf2e475e795b041": {
        "primary": "2.2.1",
        "note": "Sert kaya TBM penetrasyon hızını makine öğrenmesiyle tahmin eden uluslararası çalışma içerik üzerinden doğrulandı.",
    },
    "ING_017a281e3b7e47690da6": {
        "primary": "2.1.2",
        "secondary": ["2.4"],
        "note": "Ulaşım tünellerinin sonlu elemanlar modeli; kaplama, çelik iksa, ankraj ve püskürtme beton girdileri içerik üzerinden doğrulandı.",
    },
    "ING_1c5a56abfaae6e524858": {
        "primary": "2.4.1.2",
        "note": "Kazı sırasında deplasman, konverjans ve ayna ilerlemesi izleme yöntemleri içerik üzerinden doğrulandı.",
    },
    "ING_746d18498e07a8a0f397": {
        "primary": "5.4",
        "secondary": ["5.9.1"],
        "note": "KGM'nin trafiğe açık devlet ve il yolu tünellerine yönelik bakım, onarım ve işletme kurs notları içerik üzerinden doğrulandı.",
    },
}

ANTI_BOT = {"ING_52f7020c336219779269", "ING_c16b0af8b0176e8970a4"}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    tmp.replace(path)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    tmp.replace(path)


def _replace_ledger_row(path: Path, document_id: str, updates: dict[str, Any]) -> None:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    matches = [row for row in rows if row.get("document_id") == document_id]
    if len(matches) != 1:
        raise RuntimeError(f"expected one {path.name} row for {document_id}, found {len(matches)}")
    matches[0].update(updates)
    _write_jsonl(path, rows)


def _overlaps_page(value: dict[str, Any], first: int, last: int) -> bool:
    start = value.get("page_start") or value.get("page")
    end = value.get("page_end") or start
    return bool(start and end and int(start) <= last and int(end) >= first)


def _filtered_extraction(report: dict[str, Any], first: int, last: int) -> dict[str, list[dict[str, Any]]]:
    return {
        "elements": [row for row in report.get("text_elements", []) if _overlaps_page(row, first, last)],
        "tables": [row for row in report.get("tables", []) if _overlaps_page(row, first, last)],
        "figures": [row for row in report.get("figures", []) if _overlaps_page(row, first, last)],
        "slides": [],
        "sheets": [],
        "ocr_items": [row for row in report.get("ocr_items", []) if _overlaps_page(row, first, last)],
    }


def _all_extraction(bundle: Path, report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    normalized = _load_json(bundle / "normalized" / "document.json")

    def records(name: str) -> list[dict[str, Any]]:
        value = normalized.get(name)
        if isinstance(value, list) and all(isinstance(row, dict) for row in value):
            return list(value)
        value = report.get(name)
        if isinstance(value, list) and all(isinstance(row, dict) for row in value):
            return list(value)
        return []

    return {
        "elements": records("elements"),
        "tables": records("tables"),
        "figures": records("figures"),
        "slides": records("slides"),
        "sheets": records("sheets"),
        "ocr_items": records("ocr_items"),
    }


def _evidence_level(metadata: dict[str, Any], manifest_row: dict[str, Any]) -> str:
    return str(manifest_row.get("final_evidence_level") or metadata.get("final_evidence_level") or "FULL_TEXT")


def _ensure_identity_ledgers(
    document_id: str,
    metadata: dict[str, Any],
    *,
    registry: SourceRegistry,
) -> None:
    """Repair a legacy partial ingest whose archived identity is complete but ledgers are not."""
    original = _load_json(PATHS.original_dir(document_id) / "original.json")
    provenance = _load_json(PATHS.processing_bundle(document_id) / "provenance.json")
    sha256 = str(metadata["original_sha256"])

    map_rows = [
        json.loads(line) for line in PATHS.document_id_map_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not any(row.get("document_id") == document_id for row in map_rows):
        map_rows.append({
            "document_id": document_id,
            "sha256": sha256,
            "aliases": {"manual": [str(original.get("original_filename") or "source")]},
        })
        _write_jsonl(PATHS.document_id_map_path, map_rows)

    if document_id not in registry.rows:
        registry.register(
            DedupKey.from_metadata(metadata),
            source_kinds=list(original.get("source_kinds") or [metadata.get("source_kind")]),
            state=State.REVIEW.value,
            provenance_sources=list(provenance.get("sources") or []),
        )

    manifest_rows = [
        json.loads(line) for line in PATHS.ingest_manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not any(row.get("document_id") == document_id for row in manifest_rows):
        manifest_rows.append({
            "document_id": document_id,
            "source_kind": metadata.get("source_kind"),
            "input_path": original.get("archive_path"),
            "sha256": sha256,
            "format": metadata.get("format"),
            "status": "REVIEW",
            "processing_path": relpath(PATHS.processing_bundle(document_id)),
            "quality_decision": "REVIEW",
            "final_primary_section": metadata.get("final_primary_section"),
            "final_evidence_level": "VISUAL_ONLY",
            "chunk_count": len(read_chunks(PATHS.processing_bundle(document_id))),
            "chunk_quality_status": _load_json(
                PATHS.processing_bundle(document_id) / "chunk_quality.json"
            ).get("status"),
            "embedding_ready_chunks": 0,
            "staging_path": None,
            "duplicate_of": None,
        })
        _write_jsonl(PATHS.ingest_manifest_path, manifest_rows)


def _approve(
    document_id: str,
    spec: dict[str, Any],
    *,
    policy: ChunkPolicy,
    titles: dict[str, str],
    state: IngestState,
    registry: SourceRegistry,
) -> dict[str, Any]:
    bundle = PATHS.processing_bundle(document_id)
    metadata = _load_json(bundle / "metadata.json")
    classification = _load_json(bundle / "classification.json")
    gate = _load_json(bundle / "quality_gate.json")
    report = _load_json(bundle / "extraction_report.json")
    _ensure_identity_ledgers(document_id, metadata, registry=registry)
    manifest_rows = [
        json.loads(line) for line in PATHS.ingest_manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    manifest_matches = [row for row in manifest_rows if row.get("document_id") == document_id]
    if len(manifest_matches) != 1:
        raise RuntimeError(f"missing ingest manifest row for {document_id}")
    manifest_row = manifest_matches[0]

    primary = str(spec["primary"])
    secondary = list(spec.get("secondary", []))
    if primary not in titles or any(section not in titles for section in secondary):
        raise RuntimeError(f"invalid manual taxonomy assignment for {document_id}")

    context = ChunkingContext(
        document_id=document_id,
        original_sha256=metadata.get("original_sha256"),
        source_kind=metadata.get("source_kind"),
        final_primary_section=primary,
        final_secondary_sections=secondary,
        format=metadata.get("format"),
        evidence_level=_evidence_level(metadata, manifest_row),
    )
    extraction = _all_extraction(bundle, report)
    original_chunks = read_chunks(bundle)
    dropped: list[dict[str, Any]] = []
    if "page_window" in spec:
        first, last = spec["page_window"]
        extraction = {
            name: [row for row in rows if _overlaps_page(row, int(first), int(last))]
            if name in {"elements", "tables", "figures", "ocr_items"} else rows
            for name, rows in extraction.items()
        }
        chunks = build_text_chunks(extraction["elements"], context, policy)
        chunks += [
            chunk for chunk in original_chunks
            if chunk.get("chunk_type") != TEXT_CHUNK
            and _overlaps_page(chunk, int(first), int(last))
        ]
        chunks, dropped = deduplicate(chunks, policy)
    else:
        chunks = original_chunks
        for chunk in chunks:
            chunk["final_primary_section"] = primary
            chunk["final_secondary_sections"] = secondary

    if spec.get("figure_text"):
        figures = [chunk for chunk in chunks if chunk.get("chunk_type") == FIGURE_CHUNK]
        if len(figures) != 1:
            raise RuntimeError(f"expected one figure chunk for {document_id}, found {len(figures)}")
        figure = figures[0]
        figure["text"] = str(spec["figure_text"])
        from tunnelbookai.ingest.chunking import tokenizer
        figure["token_count"] = tokenizer.count(figure["text"])
        figure["chunk_id"] = chunk_id(
            document_id, FIGURE_CHUNK, list(figure.get("source_elements") or []), figure["text"], policy,
        )

    for ordinal, chunk in enumerate(chunks, 1):
        chunk["ordinal"] = ordinal
        chunk["final_primary_section"] = primary
        chunk["final_secondary_sections"] = secondary
    if not chunks:
        raise RuntimeError(f"manual approval produced no chunks for {document_id}")

    methods = list(classification.get("classification_methods") or [])
    if "manual_review" not in methods:
        methods.append("manual_review")
    classification.update({
        "document_id": document_id,
        "final_primary_section": primary,
        "final_secondary_sections": secondary,
        "final_section_confidence": 0.95,
        "classification_methods": methods,
        "section_evidence": [
            {"section_id": section, "section_title": titles[section], "supporting_elements": []}
            for section in [primary, *secondary]
        ],
        "manual_review": {
            "status": "APPROVED",
            "reviewed_at": now(),
            "note": spec.get("note") or "Section assignment verified by manual content review.",
        },
    })
    metadata.update({
        "final_primary_section": primary,
        "final_secondary_sections": secondary,
        "final_section_confidence": 0.95,
    })
    gate["decision"] = "GO"
    gate["reject_reasons"] = []
    gate["review_reasons"] = []
    gate_note = "MANUAL_REVIEW_APPROVED: " + (
        spec.get("note") or "content and section assignment verified"
    )
    if gate_note not in gate.setdefault("notes", []):
        gate["notes"].append(gate_note)

    quality_tables = list(extraction["tables"])
    known_table_ids = {row.get("table_id") or row.get("asset_id") for row in quality_tables}
    quality_figures = list(extraction["figures"])
    known_figure_ids = {row.get("asset_id") for row in quality_figures}
    for chunk in chunks:
        table_id = chunk.get("table_id")
        if table_id and table_id not in known_table_ids:
            quality_tables.append({"table_id": table_id, "page": chunk.get("page_start")})
            known_table_ids.add(table_id)
        figure_id = chunk.get("figure_id")
        if figure_id and figure_id not in known_figure_ids:
            quality_figures.append({"asset_id": figure_id, "page": chunk.get("page_start")})
            known_figure_ids.add(figure_id)

    quality = evaluate(
        document_id=document_id,
        chunks=chunks,
        elements=extraction["elements"],
        tables=quality_tables,
        figures=quality_figures,
        sheets=extraction["sheets"],
        slides=extraction["slides"],
        policy=policy,
        dropped=dropped,
    )
    if quality["status"] == "FAIL":
        raise RuntimeError(f"manual chunks failed quality for {document_id}: {quality['errors']}")

    _write_json(bundle / "classification.json", classification)
    _write_json(bundle / "metadata.json", metadata)
    _write_json(bundle / "quality_gate.json", gate)
    _write_json(bundle / "chunk_quality.json", quality)
    write_chunks(bundle, chunks)
    ready_rows = build_rows(chunks, policy, document_staged=True, chunk_quality_ok=True)
    _write_jsonl(bundle / "chunks" / "embedding_ready.jsonl", ready_rows)
    ready_count = sum(1 for row in ready_rows if row.get("eligible") is True)
    if ready_count < 1:
        raise RuntimeError(f"manual approval produced no embedding-ready chunks for {document_id}")

    staged, warnings = stage_document(
        document_id=document_id,
        bundle=bundle,
        metadata=metadata,
        classification=classification,
        gate=gate,
        evidence_level=context.evidence_level or "FULL_TEXT",
        chunk_count=len(chunks),
        chunk_quality_status=quality["status"],
    )
    merge_into(
        PATHS.audit_root / "embedding_ready_manifest.jsonl",
        ready_rows,
        document_ids={document_id},
    )
    detail = {
        "final_primary_section": primary,
        "confidence": 0.95,
        "decision": "GO",
        "review_reasons": [],
        "chunk_count": len(chunks),
        "chunk_quality": quality["status"],
        "embedding_ready_chunks": ready_count,
        "manual_review": "APPROVED",
    }
    current_state = state.get(document_id) or {}
    if (current_state.get("detail") or {}).get("manual_review") != "APPROVED":
        state.transition(
            document_id,
            State.EMBEDDING_READY,
            source_kind=metadata.get("source_kind"),
            sha256=metadata.get("original_sha256"),
            detail=detail,
            warnings=warnings,
        )
    if document_id not in registry.rows:
        raise RuntimeError(f"missing source registry row for {document_id}")
    registry.rows[document_id]["state"] = State.EMBEDDING_READY.value

    updates = {
        "status": "EMBEDDING_READY",
        "quality_decision": "GO",
        "final_primary_section": primary,
        "chunk_count": len(chunks),
        "chunk_quality_status": quality["status"],
        "embedding_ready_chunks": ready_count,
        "staging_path": relpath(staged),
    }
    _replace_ledger_row(PATHS.ingest_manifest_path, document_id, updates)
    return {
        "document_id": document_id,
        "disposition": "STAGED",
        "state": "EMBEDDING_READY",
        "engine_state": "EMBEDDING_READY",
        "quality_decision": "GO",
        "final_primary_section": primary,
        "final_evidence_level": context.evidence_level,
        "chunk_count": len(chunks),
        "chunk_quality_status": quality["status"],
        "embedding_ready_chunks": ready_count,
        "staging_path": relpath(staged),
        "duplicate_of": None,
        "warnings": warnings,
        "errors": [],
        "manual_review": classification["manual_review"],
    }


def _quarantine_antibot(
    document_id: str,
    *,
    recovery_root: Path,
    state: IngestState,
    registry: SourceRegistry,
) -> dict[str, Any]:
    bundle = PATHS.processing_bundle(document_id)
    gate = _load_json(bundle / "quality_gate.json")
    gate["decision"] = "REVIEW"
    gate["reject_reasons"] = []
    gate["review_reasons"] = ["MANUAL_REVIEW_REACQUIRE_ANTIBOT_CAPTURE"]
    gate.setdefault("notes", []).append("Manual review found an Incapsula anti-bot response instead of article content.")
    _write_json(bundle / "quality_gate.json", gate)

    source = staging_dir(document_id)
    quarantine = recovery_root / "quarantined_staging" / document_id
    quarantine.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        if quarantine.exists():
            raise RuntimeError(f"quarantine target already exists: {quarantine}")
        source.rename(quarantine)
    elif not quarantine.exists():
        raise RuntimeError(f"neither staging nor quarantine exists for {document_id}")

    merge_into(PATHS.audit_root / "embedding_ready_manifest.jsonl", [], document_ids={document_id})
    metadata = _load_json(bundle / "metadata.json")
    state.transition(
        document_id,
        State.REVIEW,
        source_kind=metadata.get("source_kind"),
        sha256=metadata.get("original_sha256"),
        detail={"decision": "REVIEW", "review_reasons": gate["review_reasons"], "manual_review": "REACQUIRE"},
    )
    registry.rows[document_id]["state"] = State.REVIEW.value
    _replace_ledger_row(PATHS.ingest_manifest_path, document_id, {
        "status": "REVIEW",
        "quality_decision": "REVIEW",
        "embedding_ready_chunks": 0,
        "staging_path": None,
    })
    return {
        "disposition": "NEEDS_REVIEW",
        "state": "REVIEW",
        "engine_state": "REVIEW",
        "quality_decision": "REVIEW",
        "embedding_ready_chunks": 0,
        "staging_path": None,
        "warnings": ["MANUAL_REVIEW_REACQUIRE_ANTIBOT_CAPTURE"],
        "errors": [],
        "accounted_exclusion": {
            "reason": "Captured content is an Incapsula anti-bot response; authoritative article must be reacquired.",
            "recorded_at": now(),
        },
    }


def apply(
    run_path: Path,
    dashboard_path: Path,
    recovery_root: Path,
    *,
    only: set[str] | None = None,
) -> dict[str, Any]:
    run = load_object(run_path)
    dashboard = load_object(dashboard_path)
    config = load_config()
    policy = ChunkPolicy.from_config(config)
    scope = _load_json(PATHS.root / "book" / "scope" / "normalized" / "book_scope.json")
    titles = {str(row["section_id"]): str(row["title"]) for row in scope["sections"]}
    state = IngestState(PATHS.ingest_state_path)
    registry = SourceRegistry(
        PATHS.source_registry_path,
        active_document_ids=active_document_ids(PATHS.root),
    )

    selected_approvals = {
        document_id: spec for document_id, spec in APPROVALS.items()
        if only is None or document_id in only
    }
    missing = sorted((only or set()) - set(selected_approvals))
    if missing:
        raise RuntimeError(f"unknown manual approval document ids: {missing}")

    approved: list[dict[str, Any]] = []
    for document_id, spec in selected_approvals.items():
        result = _approve(document_id, spec, policy=policy, titles=titles, state=state, registry=registry)
        run["documents"][document_id] = result
        approved.append(result)

    quarantined: list[str] = []
    if only is None:
        for document_id in sorted(ANTI_BOT):
            updates = _quarantine_antibot(document_id, recovery_root=recovery_root, state=state, registry=registry)
            run["documents"][document_id].update(updates)
            quarantined.append(document_id)

    registry.flush()

    accounted: list[str] = []
    if only is None:
        for document_id, review in dashboard["documents"].items():
            if document_id in APPROVALS or document_id in ANTI_BOT:
                continue
            note = str(review.get("note") or "")
            if "YENİDEN İŞLE" in note:
                continue
            row = run["documents"].get(document_id)
            if row is None or row.get("disposition") not in {
                "FAILED", "NEEDS_REVIEW", "REJECTED", "UNSUPPORTED", "DUPLICATE"
            }:
                continue
            if "KORPUSTAN DIŞLA" in note:
                reason = note.split("KORPUSTAN DIŞLA.", 1)[-1].strip()
            elif "YENİDEN EDİN" in note:
                reason = "Captured source contains no usable evidence; authoritative content must be reacquired. " + note
            else:
                continue
            row["accounted_exclusion"] = {"reason": reason, "recorded_at": now()}
            accounted.append(document_id)

    unresolved = [
        document_id for document_id, row in run["documents"].items()
        if row.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not row.get("accounted_exclusion")
    ]
    run["state"] = (
        PopulationState.INGEST_ACCOUNTED.value if not unresolved else PopulationState.INGESTING.value
    )
    run["updated_at"] = now()
    atomic_json(run_path, run)

    context = CanonicalContext.load(project_root=PATHS.root)
    verified: list[str] = []
    for document_id in selected_approvals:
        candidate = inspect_candidate(
            context, staging_dir(document_id), source_registry=registry,
        )
        if candidate.action.value not in {"PROMOTE", "IDEMPOTENT_NO_CHANGE"}:
            raise RuntimeError(
                f"manual candidate not eligible: {document_id}: {candidate.action.value}: "
                f"{list(candidate.warnings)}"
            )
        verified.append(document_id)

    report = {
        "schema_version": "1.0",
        "applied_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": run["run_id"],
        "approved": approved,
        "quarantined_staging": quarantined,
        "accounted_exclusions": sorted(accounted),
        "unresolved": sorted(unresolved),
        "canonical_candidates_verified": verified,
        "canonical_written": False,
    }
    report_name = "application_report.json" if only is None else "application_report_incremental.json"
    _write_json(recovery_root / report_name, report)
    return report


def verify_current(run_path: Path, recovery_root: Path) -> dict[str, Any]:
    """Verify the applied state and finish the report without mutating reviewed artifacts."""
    run = load_object(run_path)
    context = CanonicalContext.load(project_root=PATHS.root)
    registry = SourceRegistry(
        PATHS.source_registry_path,
        active_document_ids=active_document_ids(PATHS.root),
    )
    verified: list[dict[str, Any]] = []
    for document_id in APPROVALS:
        candidate = inspect_candidate(
            context, staging_dir(document_id), source_registry=registry,
        )
        if candidate.action.value not in {"PROMOTE", "IDEMPOTENT_NO_CHANGE"}:
            raise RuntimeError(f"candidate verification failed: {document_id}: {candidate.action.value}")
        verified.append({
            "document_id": document_id,
            "action": candidate.action.value,
            "chunk_count": candidate.chunk_count,
            "retrieval_ready_chunk_count": candidate.retrieval_ready_chunk_count,
            "warnings": list(candidate.warnings),
        })
    quarantined = sorted(
        document_id for document_id in ANTI_BOT
        if (recovery_root / "quarantined_staging" / document_id).is_dir()
        and not staging_dir(document_id).exists()
    )
    unresolved = sorted(
        document_id for document_id, row in run["documents"].items()
        if row.get("disposition") in {"PENDING", "RECOVERY_REQUIRED", "FAILED", "NEEDS_REVIEW"}
        and not row.get("accounted_exclusion")
    )
    accounted = sorted(
        document_id for document_id, row in run["documents"].items()
        if row.get("accounted_exclusion")
    )
    report = {
        "schema_version": "1.0",
        "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run_id": run["run_id"],
        "run_state": run["state"],
        "approved_candidates": verified,
        "quarantined_staging": quarantined,
        "accounted_exclusions": accounted,
        "unresolved": unresolved,
        "canonical_written": False,
    }
    _write_json(recovery_root / "application_report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--dashboard", required=True, type=Path)
    parser.add_argument("--recovery-root", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument(
        "--only", action="append",
        help="apply only the named approval; repeat for multiple documents",
    )
    args = parser.parse_args()
    if args.verify_only:
        report = verify_current(args.run.resolve(), args.recovery_root.resolve())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    if not args.apply:
        print(json.dumps({"status": "DRY_RUN", "approvals": len(APPROVALS), "anti_bot": len(ANTI_BOT)}))
        return 0
    report = apply(
        args.run.resolve(), args.dashboard.resolve(), args.recovery_root.resolve(),
        only=set(args.only) if args.only else None,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
