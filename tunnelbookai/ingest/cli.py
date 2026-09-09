"""Unified Ingest Engine CLI (task §62, §63).

    python scripts/ingest_incoming.py --source all --dry-run
    python scripts/ingest_incoming.py --source manual --resume
    python scripts/ingest_incoming.py --source papercrawler --resume

Default is production-safe: no canonical promotion, ever.

A normal successful run performs, per document (§67):

    discovery -> archive -> extract -> assets -> OCR/vision -> metadata -> dedup
      -> classification -> quality gate -> staging -> chunking -> chunk validation
      -> embedding-ready manifest

`--dry-run` performs NONE of it: no archive, no Docling, no OCR, no staging, no chunks —
only an inventory of what would happen (§69).
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .config import load_config
from .format_registry import detect, is_supported
from .ids import DocumentIdMap, document_id_for_file
from .office_renderer import find_libreoffice
from .paths import PATHS, relpath
from .sources import DiscoveredInput
from .sources import manual_inbox, papercrawler_contract
from .state import IngestState, State

def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _gather(source: str, *, release_id: str | None = None) -> tuple[list[DiscoveredInput], list[dict]]:
    config = load_config()
    inputs: list[DiscoveredInput] = []
    skipped: list[dict] = []
    if source in ("manual", "all"):
        inputs += manual_inbox.discover(config)
    if source in ("papercrawler", "all"):
        results = papercrawler_contract.discover(release_id=release_id)
        if release_id and not results:
            skipped.append({"release": release_id, "blockers": ["release_not_found"]})
        for result in results:
            if result.blockers:
                skipped.append({"release": result.release_dir.name, "blockers": result.blockers})
            inputs += result.accepted
            skipped += [{"release": result.release_dir.name, **s} for s in result.skipped]
    return inputs, skipped


def _dry_run(inputs: list[DiscoveredInput], skipped: list[dict]) -> int:
    libre = find_libreoffice()
    rows = []
    by_format: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for item in inputs:
        det = detect(item.input_path)
        supported = is_supported(det, libreoffice_available=libre is not None)
        try:
            doc_id, sha = document_id_for_file(item.input_path)
        except Exception as exc:  # unreadable file must not abort inventory
            doc_id, sha = "", f"ERROR:{exc}"
        by_format[det.fmt.value] = by_format.get(det.fmt.value, 0) + 1
        by_source[item.source_kind] = by_source.get(item.source_kind, 0) + 1
        rows.append({
            "document_id": doc_id,
            "sha256": sha,
            "source_kind": item.source_kind,
            "release": item.provenance.get("release"),
            "input_path": relpath(item.input_path),
            "format": det.fmt.value,
            "is_legacy": det.is_legacy,
            "supported": supported,
            "notes": item.notes,
        })

    # dedup preview by sha256
    seen: dict[str, list[str]] = {}
    for r in rows:
        if r["sha256"].startswith("ERROR:"):
            continue
        seen.setdefault(r["sha256"], []).append(r["source_kind"])
    duplicates = {sha: kinds for sha, kinds in seen.items() if len(kinds) > 1}

    release_names = sorted({
        str(row.get("release")) for row in rows if row.get("release")
    } | {
        str(row.get("release")) for row in skipped if row.get("release")
    })
    release_summaries: dict[str, dict] = {}
    for release in release_names:
        release_rows = [row for row in rows if row.get("release") == release]
        release_skipped = [row for row in skipped if row.get("release") == release]
        formats: dict[str, int] = {}
        for row in release_rows:
            formats[row["format"]] = formats.get(row["format"], 0) + 1
        release_summaries[release] = {
            "accepted": len(release_rows),
            "skipped": sum(1 for row in release_skipped if "reason" in row),
            "blockers": [
                blocker for row in release_skipped for blocker in row.get("blockers", [])
            ],
            "formats": formats,
        }

    cross_release_shas: dict[str, list[str]] = {}
    for row in rows:
        if row.get("release") and not str(row["sha256"]).startswith("ERROR:"):
            cross_release_shas.setdefault(row["sha256"], []).append(row["release"])
    release_collisions = {
        sha: sorted(set(releases)) for sha, releases in cross_release_shas.items()
        if len(set(releases)) > 1
    }

    out = {
        "generated_at": _now(),
        "mode": "dry-run",
        "libreoffice_available": libre is not None,
        "inputs_detected": len(inputs),
        "by_source": by_source,
        "by_format": by_format,
        "duplicate_sha256_across_sources": len(duplicates),
        "duplicate_sha256_across_releases": release_collisions,
        "unsupported": sum(1 for r in rows if not r["supported"]),
        "releases": release_summaries,
        "skipped_records": skipped,
        "rows": rows,
    }
    report_path = PATHS.audit_root / "ingest_dry_run.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("TUNNELBOOKAI UNIFIED INGEST — DRY RUN")
    print("=" * 40)
    print(f"Inputs detected:  {len(inputs)}")
    for k, v in sorted(by_source.items()):
        print(f"  {k}: {v}")
    print("Formats:")
    for k, v in sorted(by_format.items()):
        print(f"  {k}: {v}")
    if release_summaries:
        print("Releases:")
        for release, summary in release_summaries.items():
            print(
                f"  {release}: accepted={summary['accepted']} skipped={summary['skipped']} "
                f"blockers={len(summary['blockers'])}"
            )
    print(f"Unsupported:                    {out['unsupported']}")
    print(f"Duplicate SHA256 across sources: {len(duplicates)}")
    print(f"Duplicate SHA256 across releases: {len(release_collisions)}")
    if skipped:
        print(f"Skipped crawler records:        {len(skipped)}")
    print(f"\nNothing was processed. Report: {relpath(report_path)}")
    unreadable = any(str(row["sha256"]).startswith("ERROR:") for row in rows)
    has_blockers = any(row.get("blockers") for row in skipped)
    return 2 if out["unsupported"] or unreadable or has_blockers else 0


def _build_services(args, config):
    """Construct the shared, expensive resources once per run."""
    from .dedup import SourceRegistry, active_document_ids
    from .classify import embeddings as embedding_module
    from .classify.taxonomy import load_taxonomy
    from .ocr.provider import OcrProvider
    from .office_renderer import OfficeRenderer
    from .pipeline import PipelineServices
    from .vision.provider import build_provider

    do_ocr = not args.no_ocr
    do_vision = not args.no_vision
    ocr = OcrProvider(config, enabled=do_ocr)
    vision = build_provider(config, enabled=do_vision)      # raises on a non-loopback host
    renderer = OfficeRenderer()
    registry = SourceRegistry(
        PATHS.source_registry_path,
        active_document_ids=active_document_ids(PATHS.root),
    )

    taxonomy = load_taxonomy(
        (config.classification or {}).get("taxonomy_source",
                                          "book/scope/normalized/book_scope.json"),
        (config.classification or {}).get("taxonomy_terms",
                                          "config/taxonomy.yaml"))
    if args.embedding_server:
        config.models.setdefault("embedding", {})["default_endpoint"] = args.embedding_server
    if args.embedding_model:
        config.models.setdefault("embedding", {})["model"] = args.embedding_model
    if args.llm_server:
        config.models.setdefault("llm", {})["default_endpoint"] = args.llm_server
    if args.llm_model:
        config.models.setdefault("llm", {})["model"] = args.llm_model
    index, status, model = embedding_module.build_index(config, taxonomy)

    return PipelineServices(
        config=config, ocr=ocr, vision=vision, office_renderer=renderer, registry=registry,
        embedding_index=index, embedding_status=status, embedding_model=model,
        do_ocr=do_ocr, do_vision=do_vision, do_chunking=not args.no_chunking,
        allow_arbiter=not args.no_arbiter, root=PATHS.root,
    )


def _group_by_identity(inputs: list[DiscoveredInput]) -> tuple[dict, list[dict]]:
    """Collapse the run's inputs onto document identities BEFORE any processing.

    The same bytes can arrive from the crawler and from the manual inbox in one run. That is
    ONE document with TWO provenance sources (§32, §77) — so identity is resolved first and
    every source contributes its provenance, even though extraction runs once.
    """
    groups: dict[str, dict] = {}
    unreadable: list[dict] = []
    for item in inputs:
        try:
            doc_id, sha = document_id_for_file(item.input_path)
        except Exception as exc:
            unreadable.append({"input_path": relpath(item.input_path), "error": str(exc)})
            continue
        group = groups.setdefault(doc_id, {"document_id": doc_id, "sha256": sha, "items": []})
        group["items"].append(item)
    return groups, unreadable


def _canonical_documents() -> dict[str, dict]:
    """Return verified canonical records, failing closed on an invalid snapshot."""
    from tunnelbookai.canonical.verifier import inspect_canonical, load_snapshot

    # Older isolated ingest fixtures predate the Book Contract and contain only a decoy
    # canonical file used to prove ingest never writes there. A real manifest without the
    # authority files is still a hard failure; marker/decoy-only fixtures have no members.
    if not (PATHS.root / "book" / "config" / "book_contract.json").is_file():
        if (PATHS.canonical_corpus_root / "canonical_manifest.json").is_file():
            raise RuntimeError("canonical manifest exists but Book Contract is unavailable")
        return {}
    inventory = inspect_canonical(project_root=PATHS.root)
    if inventory.state.value == "INVALID":
        raise RuntimeError("canonical corpus is INVALID; ingest is blocked")
    if not inventory.ready:
        return {}
    snapshot = load_snapshot(project_root=PATHS.root)
    return {record.document_id: record.to_dict() for record in snapshot.manifest.documents}


def _terminal_artifacts_complete(state: IngestState, document_id: str, sha256: str) -> bool:
    """A ledger state is reusable only when its expected artifacts still exist."""
    from .ids import sha256_file

    current = state.state_of(document_id)
    if current not in {
        State.EMBEDDING_READY, State.REVIEW, State.REJECTED, State.DUPLICATE,
        State.ALREADY_PROCESSED,
    }:
        return False
    row = state.get(document_id) or {}
    if str(row.get("sha256") or "") != sha256:
        return False
    if current is State.REJECTED and (row.get("detail") or {}).get("reason") == "UNSUPPORTED_FORMAT":
        return True
    original = PATHS.original_dir(document_id)
    sources = [path for path in original.glob("source.*") if path.is_file() and not path.is_symlink()]
    if len(sources) != 1 or not (original / "original.json").is_file():
        return False
    if sha256_file(sources[0]) != sha256:
        return False
    bundle = PATHS.processing_bundle(document_id)
    if not all(
        (bundle / name).is_file()
        for name in ("metadata.json", "provenance.json", "extraction_report.json")
    ):
        return False
    if current in {State.REVIEW, State.REJECTED, State.EMBEDDING_READY, State.ALREADY_PROCESSED}:
        if not all((bundle / name).is_file() for name in ("classification.json", "quality_gate.json")):
            return False
    if current in {State.EMBEDDING_READY, State.ALREADY_PROCESSED}:
        required = (
            bundle / "chunks" / "chunk_manifest.jsonl",
            bundle / "chunks" / "embedding_ready.jsonl",
            PATHS.corpus_staging_root / "v2" / document_id / "bundle.json",
        )
        return all(path.is_file() and not path.is_symlink() for path in required)
    return True


def _run(inputs: list[DiscoveredInput], skipped: list[dict], args) -> int:
    from .original_archive import archive_original
    from .pipeline import process_document
    from .chunking.manifest import merge_into
    from .chunking.policy import ChunkPolicy

    config = load_config()
    state = IngestState(PATHS.ingest_state_path)
    id_map = DocumentIdMap(PATHS.document_id_map_path)
    manifest_rows: list[dict] = []
    outcomes: list = []
    archived = reused = failed = 0
    libre = find_libreoffice()

    groups, unreadable = _group_by_identity(inputs)
    canonical_documents = _canonical_documents()
    services = None
    callback = getattr(args, "outcome_callback", None)
    for row in unreadable:
        failed += 1
        print(f"  FAILED (unreadable): {row['input_path']}: {row['error']}")

    for doc_id, group in groups.items():
        items = group["items"]
        primary = items[0]
        sha = group["sha256"]
        det = detect(primary.input_path)

        canonical = canonical_documents.get(doc_id)
        if canonical is not None:
            if canonical.get("source_sha256") != sha:
                raise RuntimeError(f"canonical document identity conflict: {doc_id}")
            reused += 1
            print(f"  {doc_id}  {det.fmt.value:5}  ALREADY_CANONICAL")
            if callback:
                callback({"document_id": doc_id, "disposition": "ALREADY_CANONICAL", "engine_state": None})
            continue

        if not is_supported(det, libreoffice_available=libre is not None):
            state.transition(doc_id, State.REJECTED, source_kind=primary.source_kind, sha256=sha,
                             detail={"reason": "UNSUPPORTED_FORMAT", "format": det.fmt.value})
            manifest_rows.append(_manifest_row(doc_id, primary, det, sha, "REJECTED",
                                               "UNSUPPORTED_FORMAT"))
            if callback:
                callback({"document_id": doc_id, "disposition": "UNSUPPORTED", "engine_state": State.REJECTED.value})
            continue


        if args.resume and not args.force_reprocess and _terminal_artifacts_complete(state, doc_id, sha):
            reused += 1
            current = state.state_of(doc_id)
            disposition = {
                State.EMBEDDING_READY: "ALREADY_PROCESSED",
                State.ALREADY_PROCESSED: "ALREADY_PROCESSED",
                State.REVIEW: "NEEDS_REVIEW",
                State.REJECTED: "REJECTED",
                State.DUPLICATE: "DUPLICATE",
            }[current]
            print(f"  {doc_id}  {det.fmt.value:5}  {disposition}")
            if callback:
                callback({"document_id": doc_id, "disposition": disposition, "engine_state": current.value})
            continue

        if services is None:
            services = _build_services(args, config)

        # Archive once, then fold in EVERY source's provenance — this happens even when the
        # document is already processed, so a later crawler sighting still registers (§77).
        bundle = PATHS.processing_bundle(doc_id)
        bundle.mkdir(parents=True, exist_ok=True)
        meta = None
        try:
            for item in items:
                meta = archive_original(item.input_path, source_kind=item.source_kind)
                _merge_provenance(bundle / "provenance.json", item, meta)
                id_map.register(doc_id, sha,
                                "crawler" if item.crawler_record else "manual",
                                item.provenance.get("canonical_id")
                                or item.provenance.get("original_filename"))
        except Exception as exc:
            failed += 1
            state.transition(doc_id, State.FAILED, source_kind=primary.source_kind, sha256=sha,
                             error=f"archive: {exc}")
            if callback:
                callback({"document_id": doc_id, "disposition": "FAILED",
                          "engine_state": State.FAILED.value, "error": str(exc)})
            continue

        source_kinds = sorted({item.source_kind for item in items})
        for kind in source_kinds:
            state.transition(doc_id, State.ORIGINAL_ARCHIVED, source_kind=kind, sha256=sha,
                             detail={"format": det.fmt.value,
                                     "provenance_sources": len(items)})
        if meta["archive_mode"] == "copied":
            archived += 1
        else:
            reused += 1

        try:
            outcome = process_document(
                document_id=doc_id, detection=det, archive_meta=meta, services=services,
                state=state, source_kind=primary.source_kind)
        except Exception as exc:
            failed += 1
            state.transition(
                doc_id, State.FAILED, source_kind=primary.source_kind, sha256=sha,
                error=f"pipeline: {type(exc).__name__}: {exc}"[:500],
            )
            print(f"  FAILED {doc_id}: {type(exc).__name__}: {exc}")
            if callback:
                callback({"document_id": doc_id, "disposition": "FAILED", "engine_state": State.FAILED.value, "error": str(exc)})
            continue
        outcomes.append(outcome)
        manifest_rows.append(_manifest_row(doc_id, primary, det, sha, outcome.state.value,
                                           outcome.decision or "", outcome))
        print(f"  {doc_id}  {det.fmt.value:5}  {outcome.state.value:18} "
              f"{outcome.decision or '-':7} section={outcome.primary_section or '-':8} "
              f"chunks={outcome.chunk_count} sources={len(items)}")
        if callback:
            disposition = {
                State.EMBEDDING_READY: "STAGED",
                State.STAGED: "STAGED",
                State.REVIEW: "NEEDS_REVIEW",
                State.REJECTED: "REJECTED",
                State.DUPLICATE: "DUPLICATE",
                State.FAILED: "FAILED",
            }.get(outcome.state, "FAILED")
            callback({"document_id": doc_id, "disposition": disposition,
                      "engine_state": outcome.state.value, **outcome.as_row()})

    if services is not None:
        id_map.flush()
        if services.registry is not None:
            services.registry.flush()
    _write_manifest(manifest_rows)

    # audit/embedding_ready_manifest.jsonl — one row per chunk across the run (§64)
    policy = ChunkPolicy.from_config(config)
    ready_rows: list[dict] = []
    touched: set[str] = set()
    for outcome in outcomes:
        path = PATHS.processing_bundle(outcome.document_id) / "chunks" / "embedding_ready.jsonl"
        touched.add(outcome.document_id)
        if path.is_file():
            ready_rows += [json.loads(line) for line in
                           path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if touched:
        merge_into(PATHS.audit_root / "embedding_ready_manifest.jsonl", ready_rows,
                   document_ids=touched)

    if services is not None:
        _write_quality_summary(outcomes, services)
    _print_summary(inputs, outcomes, archived, reused, failed, manifest_rows, services)
    return 1 if failed or any(outcome.state is State.FAILED for outcome in outcomes) else 0


def _register_existing(services, document_id: str, bundle: Path,
                       source_kinds: list[str]) -> None:
    """Refresh the dedup ledger for a document that is already processed (§32, §77)."""
    if services.registry is None:
        return
    metadata_path = bundle / "metadata.json"
    if not metadata_path.is_file():
        return
    from .dedup import resolve as dedup_resolve
    from .state import State as _State

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    provenance_doc = {}
    provenance_path = bundle / "provenance.json"
    if provenance_path.is_file():
        provenance_doc = json.loads(provenance_path.read_text(encoding="utf-8"))
    dedup_resolve(services.registry, metadata, source_kinds=source_kinds,
                  state=_State.ALREADY_PROCESSED.value,
                  provenance_sources=provenance_doc.get("sources"))


def _print_summary(inputs, outcomes, archived, reused, failed, manifest_rows, services) -> None:
    staged = sum(1 for o in outcomes if o.state in (State.STAGED, State.EMBEDDING_READY))
    review = sum(1 for o in outcomes if o.state is State.REVIEW)
    rejected = sum(1 for o in outcomes if o.state is State.REJECTED)
    duplicates = sum(1 for o in outcomes if o.state is State.DUPLICATE)
    pipeline_failed = sum(1 for o in outcomes if o.state is State.FAILED)
    chunks = sum(o.chunk_count for o in outcomes)
    ready = sum(o.embedding_ready_count for o in outcomes)

    print()
    print("TUNNELBOOKAI UNIFIED INGEST")
    print("=" * 40)
    print(f"Inputs detected:            {len(inputs)}")
    print(f"Originals archived:         {archived}")
    print(f"Reused / already processed: {reused}")
    print(f"Staged (GO):                {staged}")
    print(f"Review:                     {review}")
    print(f"Duplicates:                 {duplicates}")
    print(f"Rejected:                   {rejected + sum(1 for r in manifest_rows if r['status'] == 'REJECTED')}")
    print(f"Failed:                     {failed + pipeline_failed}")
    print(f"Chunks produced:            {chunks}")
    print(f"Embedding-ready chunks:     {ready}")
    print(f"Embeddings computed:        0 (never in this engine)")
    print(f"Canonical promoted:         0")
    print()
    print(f"State:    {relpath(PATHS.ingest_state_path)}")
    print(f"Manifest: {relpath(PATHS.ingest_manifest_path)}")
    print(f"Quality:  {relpath(PATHS.unified_ingest_quality_path)}")


def _write_quality_summary(outcomes, services) -> None:
    from .office_renderer import OfficeRenderer

    by_state: dict[str, int] = {}
    by_decision: dict[str, int] = {}
    by_evidence: dict[str, int] = {}
    by_chunk_type: dict[str, int] = {}
    for outcome in outcomes:
        by_state[outcome.state.value] = by_state.get(outcome.state.value, 0) + 1
        if outcome.decision:
            by_decision[outcome.decision] = by_decision.get(outcome.decision, 0) + 1
        if outcome.evidence_level:
            by_evidence[outcome.evidence_level] = by_evidence.get(outcome.evidence_level, 0) + 1
        report = PATHS.processing_bundle(outcome.document_id) / "chunk_quality.json"
        if report.is_file():
            data = json.loads(report.read_text(encoding="utf-8"))
            for chunk_type, count in (data.get("chunks_by_type") or {}).items():
                by_chunk_type[chunk_type] = by_chunk_type.get(chunk_type, 0) + count

    payload = {
        "generated_at": _now(),
        "documents": len(outcomes),
        "by_state": by_state,
        "by_quality_decision": by_decision,
        "by_evidence_level": by_evidence,
        "chunks_by_type": by_chunk_type,
        "chunks_total": sum(o.chunk_count for o in outcomes),
        "embedding_ready_chunks": sum(o.embedding_ready_count for o in outcomes),
        "environment": {
            "libreoffice_available": services.office_renderer.available(),
            "office_renderer_backend": services.office_renderer.backend,
            "ocr_available": services.ocr.available() if services.ocr else False,
            "ocr_engine": services.ocr.engine_id() if services.ocr else None,
            "vision_provider": type(services.vision).__name__ if services.vision else None,
            "vision_available": bool(services.vision and services.vision.available()),
            "embedding_status": services.embedding_status,
            "embedding_model": services.embedding_model,
        },
        "canonical_promoted": 0,
        "embeddings_computed": 0,
        "documents_detail": [o.as_row() for o in outcomes],
    }
    path = PATHS.unified_ingest_quality_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")


def _manifest_row(doc_id, item, det, sha, status, quality, outcome=None) -> dict:
    row = {
        "document_id": doc_id,
        "source_kind": item.source_kind,
        "input_path": relpath(item.input_path),
        "sha256": sha,
        "format": det.fmt.value,
        "status": status,
        "processing_path": f"processing/{doc_id}",
        "quality_decision": quality,
    }
    if outcome is not None:
        row.update({
            "final_primary_section": outcome.primary_section,
            "final_evidence_level": outcome.evidence_level,
            "chunk_count": outcome.chunk_count,
            "chunk_quality_status": outcome.chunk_quality_status,
            "embedding_ready_chunks": outcome.embedding_ready_count,
            "staging_path": outcome.staging_path,
            "duplicate_of": outcome.duplicate_of,
        })
    return row


def _write_manifest(rows: list[dict]) -> None:
    if not rows:
        return
    path = PATHS.ingest_manifest_path
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, dict] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                existing[r["document_id"]] = r
    for r in rows:
        existing[r["document_id"]] = r
    with path.open("w", encoding="utf-8") as handle:
        for r in existing.values():
            handle.write(json.dumps(r, ensure_ascii=False) + "\n")


def _merge_provenance(path: Path, item: DiscoveredInput, archive_meta: dict) -> None:
    doc = {"document_id": archive_meta["document_id"], "sources": []}
    if path.is_file():
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc.setdefault("sources", [])
    entry = {"kind": item.source_kind, **item.provenance}
    if item.crawler_record:
        # The full handoff record must survive here: metadata/enrich.py prefers a crawler
        # manifest title/author/date over its body-heading heuristic, and reads the record
        # back out of provenance.json. Dropping it silently degraded every crawler document
        # to `_first_heading`, which on a real journal PDF picked the page-1 masthead
        # ("Kocaeli University") over the article title -- and a generic institutional title
        # is a dedup false-merge hazard (real-data pilot defect D1, §19/§20/§22).
        entry["crawler_record"] = item.crawler_record

    def _same_source(existing: dict) -> bool:
        return (existing.get("kind") == entry["kind"]
                and existing.get("inbox_relative_path") == entry.get("inbox_relative_path")
                and existing.get("canonical_id") == entry.get("canonical_id"))

    match = next((s for s in doc["sources"] if _same_source(s)), None)
    if match is None:
        doc["sources"].append(entry)
    else:
        # Re-merge must refresh the recorded source rather than skip it, so a bundle written
        # by an older engine backfills fields it never stored (defect D1). Only real values
        # overwrite: a re-sighting must never blank out provenance that is already there.
        match.update({k: v for k, v in entry.items() if v not in (None, "", {}, [])})
    doc["original"] = {k: archive_meta[k] for k in ("original_filename", "original_sha256", "mime_type", "format")}
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def _unused_write_source_registry(state: IngestState) -> None:
    """Superseded by dedup.SourceRegistry, which carries the dedup keys as well (§32)."""
    path = PATHS.source_registry_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in state.all_rows():
            handle.write(json.dumps({
                "document_id": row["document_id"],
                "sha256": row.get("sha256"),
                "source_kinds": row.get("source_kinds", []),
                "state": row.get("state"),
            }, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ingest_incoming", description="TunnelBookAI Unified Ingest Engine")
    p.add_argument("--source", choices=["papercrawler", "manual", "all"], default="all")
    p.add_argument("--dry-run", action="store_true", help="inventory only; process nothing")
    p.add_argument("--resume", action="store_true", help="skip documents already past a stage")
    p.add_argument("--force-reprocess", action="store_true", help="rebuild derived outputs (never the original)")
    p.add_argument("--document-id", default=None, help="restrict to one document id")
    p.add_argument("--release", default=None,
                   help="discover only this PaperCrawler release directory")
    p.add_argument("--max-documents", type=int, default=0)
    p.add_argument("--no-ocr", action="store_true")
    p.add_argument("--no-vision", action="store_true")
    p.add_argument("--embedding-server", default=None)
    p.add_argument("--embedding-model", default=None)
    p.add_argument("--llm-server", default=None)
    p.add_argument("--llm-model", default=None)
    p.add_argument("--no-chunking", action="store_true",
                   help="stop after staging; chunking is part of a normal successful run")
    p.add_argument("--no-arbiter", action="store_true",
                   help="never call the local LLM arbiter, even on an unsettled section")
    p.add_argument("--from-stage", default=None,
                   choices=[s.value for s in State],
                   help="reprocess documents already at or past this stage")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.release and args.source == "manual":
        raise SystemExit("--release requires --source papercrawler or --source all")
    inputs, skipped = _gather(args.source, release_id=args.release)
    if args.document_id:
        inputs = [i for i in inputs if document_id_for_file(i.input_path)[0] == args.document_id]
    if args.from_stage:
        # Reprocess only the documents that already reached (or passed) this stage, and
        # rebuild their derived outputs. The immutable original is never rebuilt.
        from .state import rank as _rank

        state = IngestState(PATHS.ingest_state_path)
        floor = _rank(State(args.from_stage))
        selected = []
        for item in inputs:
            try:
                doc_id = document_id_for_file(item.input_path)[0]
            except Exception:
                continue
            current = state.state_of(doc_id)
            if current is not None and _rank(current) >= floor:
                selected.append(item)
        inputs = selected
        args.force_reprocess = True
    if args.max_documents:
        inputs = inputs[: args.max_documents]
    if args.dry_run:
        return _dry_run(inputs, skipped)
    if any(row.get("blockers") for row in skipped):
        for row in skipped:
            if row.get("blockers"):
                print(f"BLOCKED release={row.get('release')}: {', '.join(row['blockers'])}")
        return 2
    return _run(inputs, skipped, args)


if __name__ == "__main__":
    raise SystemExit(main())
