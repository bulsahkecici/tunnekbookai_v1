#!/usr/bin/env python3
"""One-command PaperCrawler → TunnelBookAI handoff preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import classify_catalog
import free_discovery
import gap_discovery
import handoff_export
import light_pdf_extract
import source_dedup_audit
import supplemental_discovery
import run_summary
import corpus_quality_gate
import pipeline_state
import tunnel_harvest as harvest


def _log(message: str) -> None:
    print(f"[pipeline] {message}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover, enrich, classify, gap-fill, audit and export TunnelBookAI source handoff.")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--destination", default=None)
    parser.add_argument("--max-queries", type=int, default=60)
    parser.add_argument("--per-source", type=int, default=10)
    parser.add_argument("--max-book-queries", type=int, default=18)
    parser.add_argument("--light-pdf-pages", type=int, default=3)
    parser.add_argument("--rules-only", action="store_true", help="Disable local embedding/LLM classification.")
    parser.add_argument("--embedding-server", default=None, help="Loopback OpenAI-compatible embedding server.")
    parser.add_argument("--embedding-model", default=None, help="Embedding model ID or unique model-name fragment.")
    parser.add_argument("--llm-server", default=None, help="Loopback OpenAI-compatible chat model server.")
    parser.add_argument("--llm-model", default=None, help="Chat model ID or unique model-name fragment.")
    parser.add_argument("--skip-gap-pass", action="store_true", help="Skip coverage-driven second discovery pass.")
    parser.add_argument("--skip-news-books", action="store_true", help="Skip RSS/Atom institutional news and book metadata discovery.")
    parser.add_argument("--no-dynamic-expansion", action="store_true")
    parser.add_argument("--resume", action="store_true", default=True, help="Resume completed stages (default).")
    parser.add_argument("--fresh-run", action="store_true", help="Create a new checkpoint state; existing documents are preserved.")
    parser.add_argument("--from-stage", choices=pipeline_state.STAGES, default=None, help="Rerun this stage and all downstream stages without deleting durable artifacts.")
    parser.add_argument("--bootstrap-legacy-checkpoint", action="store_true", help="Adopt validated pre-checkpoint artifacts and resume at the interrupted gap stage.")
    parser.add_argument("--checkpoint-only", action="store_true", help="Write/inspect checkpoint state without running pipeline stages.")
    return parser.parse_args()


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def main() -> None:
    args = parse_args()
    if args.output_dir is not None:
        harvest.set_output_dir(args.output_dir)
    root = harvest.OUTPUT_DIR
    state = pipeline_state.PipelineState(root, fresh=args.fresh_run)
    if args.from_stage:
        state.restart_from(args.from_stage)
    if args.bootstrap_legacy_checkpoint:
        adopted = state.bootstrap_legacy()
        _log(f"legacy checkpoint adopted: {adopted}")
    if args.checkpoint_only:
        print(json.dumps(state.data, ensure_ascii=False, indent=2), flush=True)
        return
    _log("1/7 free discovery started")
    discovery_report = state.run("free_discovery", lambda: free_discovery.discover_all(
        output_dir=args.output_dir, max_queries=max(1, args.max_queries), per_source=max(1, args.per_source),
        acquire=True, expand_dynamic=not args.no_dynamic_expansion,
        embedding_server=args.embedding_server, embedding_model=args.embedding_model,
        use_local_embedding=not args.rules_only,
    )) or _read_json(root / "audit" / "discovery_audit.json")
    supplemental_report = None
    if not args.skip_news_books:
        _log("2/7 institutional news and book discovery started")
        supplemental_report = state.run("institutional_discovery", lambda: supplemental_discovery.run_supplemental_discovery(
            output_dir=args.output_dir,
            max_book_queries=max(1, args.max_book_queries),
            per_source=max(1, args.per_source),
            acquire_news=True,
        )) or _read_json(root / "audit" / "supplemental_discovery_audit.json")
    elif not state.completed("institutional_discovery"):
        state.mark("institutional_discovery", "COMPLETED", skipped=True)
    _log("3/7 lightweight PDF text extraction started")
    light_extract_report = state.run("pdf_enrichment", lambda: light_pdf_extract.enrich_catalog(
        args.output_dir, max_pages=max(1, args.light_pdf_pages),
    )) or _read_json(root / "audit" / "light_pdf_extract_audit.json")
    _log("4/7 initial classification started")
    first_classification = state.run("initial_classification", lambda: classify_catalog.classify_catalog(
        args.output_dir,
        use_local_ai=not args.rules_only,
        embedding_server=args.embedding_server,
        embedding_model=args.embedding_model,
        llm_server=args.llm_server,
        llm_model=args.llm_model,
    )) or _read_json(root / "audit" / "classification_audit.json")
    gap_report = None
    final_classification = first_classification
    if not args.skip_gap_pass:
        _log("5/7 coverage-gap discovery started")
        gap_report = state.run("gap_discovery", lambda: gap_discovery.run_gap_discovery(
            args.output_dir, embedding_server=args.embedding_server, embedding_model=args.embedding_model,
            use_local_embedding=not args.rules_only,
        )) or _read_json(root / "audit" / "gap_discovery_audit.json")
        if int(gap_report.get("catalog_additions") or 0) > 0:
            light_pdf_extract.enrich_catalog(args.output_dir, max_pages=max(1, args.light_pdf_pages))
            final_classification = state.run("reclassification", lambda: classify_catalog.classify_catalog(
                args.output_dir,
                use_local_ai=not args.rules_only,
                embedding_server=args.embedding_server,
                embedding_model=args.embedding_model,
                llm_server=args.llm_server,
                llm_model=args.llm_model,
            )) or _read_json(root / "audit" / "classification_audit.json")
        elif not state.completed("reclassification"):
            state.mark("reclassification", "COMPLETED", skipped=True)
    else:
        if not state.completed("gap_discovery"):
            state.mark("gap_discovery", "COMPLETED", skipped=True)
        if not state.completed("reclassification"):
            state.mark("reclassification", "COMPLETED", skipped=True)
    _log("6/7 source duplicate/version audit started")
    source_audit = state.run("source_audit", lambda: source_dedup_audit.audit(args.output_dir)) or _read_json(root / "audit" / "source_dedup_version_audit.json")
    _log("7/7 TunnelBookAI handoff export started")
    handoff = state.run("handoff", lambda: handoff_export.export_handoff(args.output_dir, destination=args.destination)) or _read_json(root / "exports" / "TunnelBookAI_Source_Pack" / "99_audit" / "handoff_audit.json")
    _log("run summary started")
    summary = run_summary.write(args.output_dir)
    quality_gate = corpus_quality_gate.evaluate(root, package_root=args.destination)
    report = {
        "discovery": discovery_report,
        "news_and_books": supplemental_report,
        "light_pdf_extract": light_extract_report,
        "initial_classification": {
            "documents": first_classification.get("documents"),
            "status_counts": first_classification.get("status_counts"),
        },
        "gap_pass": gap_report,
        "final_classification": {
            "documents": final_classification.get("documents"),
            "status_counts": final_classification.get("status_counts"),
            "section_coverage": final_classification.get("section_coverage"),
        },
        "source_dedup_version_audit": {
            "documents": source_audit.get("documents"),
            "exact_duplicate_groups": source_audit.get("exact_duplicate_groups"),
            "same_doi_groups": source_audit.get("same_doi_groups"),
            "fuzzy_review_pairs": source_audit.get("fuzzy_review_pairs"),
        },
        "handoff": handoff,
        "run_summary": summary,
        "corpus_quality_gate": quality_gate,
    }
    _log("pipeline finished")
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
