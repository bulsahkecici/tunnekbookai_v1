#!/usr/bin/env python3
"""Generic, section-agnostic local-only evidence remediation engine.

Production replacement for the ad hoc CLI in
scripts/section_evidence_remediation.py (kept only as legacy reference,
hardcoded to CH-A-S01, and not used here). This engine:

- Consumes section config via configure_section(root, section_id); no
  section is hardcoded.
- Checkpoints each candidate classification independently to disk under
  data/book/remediation/<slug>/checkpoints/, keyed by a stable candidate
  identity (chunk_id, or document_id+locator, or a text hash).
- Supports --resume, which reuses checkpointed CLASSIFIED candidates and
  only re-attempts candidates that were not yet observed or that
  previously failed.
- Never discards claims from successfully classified candidates because a
  later candidate fails or times out.
- Reports a genuine local-LLM/infra failure as DEPENDENCY_FAILURE, distinct
  from TRUE_CORPUS_EVIDENCE_GAP (which means the evidence was fully
  observed and found insufficient) and from UNOBSERVED (a candidate the run
  never reached).

This script never writes book prose and never mutates frozen corpus/
retrieval assets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import section_evidence_remediation as ser

ENGINE_VERSION = "REMEDIATION_ENGINE_V1"
CANDIDATE_STATUS_VALUES = {"CLASSIFIED", "DEPENDENCY_FAILURE", "UNOBSERVED"}
READINESS_VALUES = ser.READINESS_VALUES | {"DEPENDENCY_FAILURE"}
LOG = logging.getLogger("remediation_engine")


def checkpoint_dir(root: Path, section_id: str) -> Path:
    return root / "data" / "book" / "remediation" / ser.section_slug(section_id) / "checkpoints"


def _checkpoint_path(cdir: Path, candidate_key: str) -> Path:
    digest = hashlib.sha256(candidate_key.encode("utf-8")).hexdigest()[:24]
    return cdir / f"{digest}.json"


def _load_checkpoint(cdir: Path, candidate_key: str) -> dict[str, Any] | None:
    path = _checkpoint_path(cdir, candidate_key)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_checkpoint(cdir: Path, candidate_key: str, record: dict[str, Any]) -> None:
    cdir.mkdir(parents=True, exist_ok=True)
    path = _checkpoint_path(cdir, candidate_key)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def classify_claims_checkpointed(
    candidates: list[dict[str, Any]],
    model: str,
    api_base: str,
    cdir: Path,
    resume: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Classify candidates independently, checkpointing each one to disk.

    Returns (claims, candidate_statuses). candidate_statuses has one row
    per candidate: {candidate_key, candidate_id, status, elapsed_seconds}.
    """
    ser.smoke_test_local_llm(model, api_base)

    claims: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    total = len(candidates)

    for index, candidate in enumerate(candidates, 1):
        candidate_key = ser._candidate_key(candidate)
        candidate_id = candidate.get("chunk_id") or candidate.get("document_id") or f"candidate-{index}"
        text = str(candidate.get("text") or "")

        if resume:
            cached = _load_checkpoint(cdir, candidate_key)
            if cached is not None and cached.get("status") == "CLASSIFIED":
                claims.extend(cached.get("claims", []))
                statuses.append({
                    "candidate_key": candidate_key,
                    "candidate_id": candidate_id,
                    "status": "CLASSIFIED",
                    "elapsed_seconds": cached.get("elapsed_seconds"),
                    "source": "checkpoint",
                })
                print(f"classification_candidate_reused={index}/{total} id={candidate_id}", flush=True)
                continue

        print(f"classification_candidate={index}/{total} id={candidate_id} chars={len(text)}", flush=True)
        started = time.monotonic()
        try:
            parsed = ser._native_chat_json(
                model, api_base, ser._classification_system_prompt(), ser._llm_prompt(candidate),
            )
            model_claims = parsed.get("claims")
            if not isinstance(model_claims, list):
                raise ser.RemediationError("model response has no claims list")
            candidate_claims = []
            for claim in model_claims:
                normalized = ser._validate_claim(claim, candidate)
                if normalized is not None:
                    candidate_claims.append(normalized)
        except ser.RemediationError as exc:
            elapsed = time.monotonic() - started
            record = {
                "candidate_key": candidate_key,
                "candidate_id": candidate_id,
                "status": "DEPENDENCY_FAILURE",
                "elapsed_seconds": round(elapsed, 1),
                "cause": str(exc),
                "classified_at": datetime.now(timezone.utc).isoformat(),
                "model": model,
                "api_base": api_base,
            }
            _write_checkpoint(cdir, candidate_key, record)
            statuses.append({k: record[k] for k in ("candidate_key", "candidate_id", "status", "elapsed_seconds")})
            print(f"classification_candidate_dependency_failure={index}/{total} id={candidate_id} cause={exc}", flush=True)
            continue

        elapsed = time.monotonic() - started
        record = {
            "candidate_key": candidate_key,
            "candidate_id": candidate_id,
            "status": "CLASSIFIED",
            "elapsed_seconds": round(elapsed, 1),
            "claims": candidate_claims,
            "classified_at": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "api_base": api_base,
        }
        _write_checkpoint(cdir, candidate_key, record)
        claims.extend(candidate_claims)
        statuses.append({
            "candidate_key": candidate_key,
            "candidate_id": candidate_id,
            "status": "CLASSIFIED",
            "elapsed_seconds": round(elapsed, 1),
        })
        print(
            f"classification_candidate_done={index}/{total} id={candidate_id} "
            f"claims={len(candidate_claims)} elapsed_seconds={elapsed:.1f}",
            flush=True,
        )

    return claims, statuses


def determine_readiness_checkpointed(
    claims: list[dict[str, Any]],
    candidate_statuses: list[dict[str, Any]],
    use_local_llm: bool,
    preexisting_validated: bool = False,
) -> str:
    """Like section_evidence_remediation.determine_readiness, but a
    DEPENDENCY_FAILURE on any candidate is reported as DEPENDENCY_FAILURE
    and never folded into TRUE_CORPUS_EVIDENCE_GAP or NEEDS_LOCAL_REVIEW.
    """
    if any(status["status"] == "DEPENDENCY_FAILURE" for status in candidate_statuses):
        return "DEPENDENCY_FAILURE"
    return ser.determine_readiness(claims, use_local_llm, preexisting_validated)


def validate_outputs_checkpointed(
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    readiness: str,
    packet: dict[str, Any] | None,
) -> None:
    if readiness not in READINESS_VALUES:
        raise ser.RemediationError("invalid readiness")
    if any(c.get("section_id") not in (None, ser.SECTION_ID) for c in candidates):
        raise ser.RemediationError("unrelated section candidate detected")
    admitted = [c for c in claims if c.get("disposition") in {"ADMITTED_STRONG", "ADMITTED_LIMITED"}]
    if any(not c.get("source_text") or not c.get("document_id") for c in admitted):
        raise ser.RemediationError("admitted claim missing source evidence")
    if len(ser._deduplicate_claims(admitted)) != len(admitted):
        raise ser.RemediationError("duplicate admitted claims")
    if packet:
        claim_ids = {c["claim_id"] for c in packet["admitted_claims"]}
        if packet.get("section_id") != ser.SECTION_ID or packet.get("privacy_mode") != "LOCAL_ONLY":
            raise ser.RemediationError("writer packet scope/privacy validation failed")
        if any(mapping.get("claim_id") not in claim_ids for mapping in packet["citation_mapping"]):
            raise ser.RemediationError("citation mapping references unknown claim")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section-id", required=True)
    parser.add_argument("--use-local-llm", action="store_true")
    parser.add_argument("--model", default="qwen3.6-35b-a3b-mlx")
    parser.add_argument("--api-base", default="http://127.0.0.1:1234/v1")
    parser.add_argument("--max-candidates", type=int, default=15)
    parser.add_argument("--resume", action="store_true", help="reuse checkpointed candidate classifications")
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
    stamp = ser.utc_stamp()
    try:
        ser.configure_section(root, args.section_id)
        if args.use_local_llm:
            ser.validate_local_endpoint(args.api_base)
        artifacts = ser.find_project_artifacts(root)
        state = ser.load_section_state(artifacts, root)
        retriever, retriever_path, retriever_config = ser.resolve_retriever(root)
        raw = ser.run_retrieval_queries(retriever, top_k=args.max_candidates)
        candidates = ser.deduplicate_candidates(raw, args.max_candidates)
        if not candidates:
            raise ser.RemediationError("NO_RETRIEVAL_RESULTS")

        cdir = checkpoint_dir(root, args.section_id)
        candidate_statuses: list[dict[str, Any]] = []
        if args.use_local_llm:
            claims, candidate_statuses = classify_claims_checkpointed(
                candidates, args.model, args.api_base, cdir, args.resume,
            )
        else:
            claims = []

        readiness = determine_readiness_checkpointed(
            claims, candidate_statuses, args.use_local_llm, preexisting_validated=False,
        )
        generated_at = datetime.now(timezone.utc).isoformat()
        packet = ser.build_writer_packet(state, claims, readiness, generated_at)
        validate_outputs_checkpointed(candidates, claims, readiness, packet)

        counts = {
            "strong_claims": sum(c.get("disposition") == "ADMITTED_STRONG" for c in claims),
            "limited_claims": sum(c.get("disposition") == "ADMITTED_LIMITED" for c in claims),
            "rejected_claims": sum(str(c.get("disposition", "")).startswith("REJECT_") for c in claims),
        }
        dependency_failures = [s for s in candidate_statuses if s["status"] == "DEPENDENCY_FAILURE"]
        summary = {
            "generated_at": generated_at,
            "mode": "LOCAL_LLM" if args.use_local_llm else "DETERMINISTIC_EXPORT",
            "engine_version": ENGINE_VERSION,
            "candidate_count": len(candidates),
            "readiness": readiness,
            "dependency_failures": [s["candidate_id"] for s in dependency_failures],
            **counts,
        }
        source_hashes = [{"path": p.relative_to(root).as_posix(), "sha256": ser.sha256_file(p)} for p in artifacts]
        manifest = {
            "section_id": ser.SECTION_ID,
            "section_title": ser.SECTION_TITLE,
            "generated_at": generated_at,
            "generator": "scripts/remediation_engine.py",
            "engine_version": ENGINE_VERSION,
            "privacy_mode": "LOCAL_ONLY",
            "summary": summary,
            "section_state": state,
            "search_queries": list(ser.SEARCH_QUERIES),
            "retriever_config": retriever_config,
            "candidate_statuses": candidate_statuses,
            "integrity": {
                "source_artifacts": source_hashes,
                "retriever": {"path": retriever_path.relative_to(root).as_posix(), "sha256": ser.sha256_file(retriever_path)},
            },
            "validation": {"target_only": True, "frozen_assets_written": False, "outputs_validated": True},
        }
        output_dir = root / "data" / "book" / "remediation" / ser.section_slug(ser.SECTION_ID)
        if not args.dry_run:
            ser.write_artifacts(
                output_dir, stamp, candidates, packet, manifest,
                lambda outputs: ser._report(summary, state, outputs),
            )
        print(f"section={ser.SECTION_ID}")
        print(f"candidate_count={len(candidates)}")
        print(f"strong_claims={counts['strong_claims']}")
        print(f"limited_claims={counts['limited_claims']}")
        print(f"rejected_claims={counts['rejected_claims']}")
        print(f"readiness={readiness}")
        if dependency_failures:
            print(f"dependency_failures={len(dependency_failures)}")
        print(f"output_directory={output_dir.relative_to(root) if not args.dry_run else 'DRY_RUN'}")
        print(f"next_action={'review candidate bundle locally' if not args.use_local_llm else 'review admitted claims before drafting'}")
        return 0
    except ser.RemediationError as exc:
        LOG.error("%s", exc)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
