"""Manifest-bound, rebuildable local vector retrieval over canonical evidence only."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

import numpy as np
import yaml

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.canonical.verifier import require_ready
from tunnelbookai.ingest.classify.embeddings import LocalEmbeddingClient
from tunnelbookai.ingest.vision.provider import assert_loopback

from .errors import BookEngineError
from .inputs import BookInputs, load_book_inputs


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "book-retrieval-v1"
SOFTWARE_VERSION = "book-retrieval-v1"
PROMPT_VERSION = "not-applicable-embedding-v1"


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_npy(path: Path, matrix: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        np.save(handle, matrix, allow_pickle=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _safe_path(root: Path, relative: object, *, within: Path) -> Path:
    value = Path(str(relative or ""))
    if not str(relative or "").strip() or value.is_absolute() or ".." in value.parts:
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", f"unsafe path: {relative!r}")
    candidate = (root / value).resolve()
    boundary = within.resolve()
    if candidate != boundary and boundary not in candidate.parents:
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", f"path escapes retrieval boundary: {relative}")
    return candidate


def _model_settings(inputs: BookInputs) -> tuple[str, str, str]:
    model_path = inputs.contract.project_root / "config" / "models.yaml"
    payload = yaml.safe_load(model_path.read_text(encoding="utf-8")) or {}
    settings = payload.get("embedding") or {}
    model = str(settings.get("model") or "").strip()
    endpoint = os.getenv(
        str(settings.get("endpoint_env") or "EMBEDDING_SERVER"),
        str(settings.get("default_endpoint") or ""),
    ).strip()
    if not model or not endpoint:
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "embedding model configuration is incomplete")
    return model, assert_loopback(endpoint), sha256_file(model_path)


def _canonical_source_digest(records: Iterable[Mapping[str, Any]]) -> str:
    return canonical_sha256([
        {
            "document_id": row["document_id"],
            "retrieval_manifest_sha256": row["chunks"]["retrieval_manifest_sha256"],
            "retrieval_ready_count": row["chunks"]["retrieval_ready_count"],
        }
        for row in records
    ])


def _canonical_rows(root: Path, records: Iterable[Mapping[str, Any]]) -> Iterator[dict[str, Any]]:
    canonical_root = root / "corpus" / "canonical"
    for record in records:
        relative = str(record["chunks"]["retrieval_manifest_path"])
        path = _safe_path(root, relative, within=canonical_root)
        if not path.is_file() or path.is_symlink():
            raise BookEngineError("CANONICAL_CORPUS_INVALID", f"canonical retrieval file missing: {relative}")
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("eligible") is not True:
                    continue
                text = str(row.get("embedding_text") or "").strip()
                if not text:
                    raise BookEngineError("CANONICAL_CORPUS_INVALID", f"empty embedding text: {row.get('chunk_id')}")
                yield {
                    "chunk_id": row["chunk_id"],
                    "document_id": row["document_id"],
                    "chunk_type": row.get("chunk_type"),
                    "section_id": row.get("section_id"),
                    "secondary_section_ids": row.get("secondary_section_ids") or [],
                    "page_start": row.get("page_start"),
                    "page_end": row.get("page_end"),
                    "slide_number": row.get("slide_number"),
                    "sheet_name": row.get("sheet_name"),
                    "canonical_retrieval_path": relative,
                    "canonical_line_number": line_number,
                    "embedding_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "_embedding_text": text,
                }


def _public_row(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if not key.startswith("_")}


def _normalise(vectors: list[list[float]], *, expected_dimension: int | None = None) -> np.ndarray:
    try:
        matrix = np.asarray(vectors, dtype=np.float32)
    except (TypeError, ValueError) as exc:
        raise BookEngineError("EMBEDDING_RESPONSE_INVALID", "embedding matrix is not numeric") from exc
    if matrix.ndim != 2 or matrix.shape[0] == 0:
        raise BookEngineError("EMBEDDING_RESPONSE_INVALID", "embedding matrix shape is invalid")
    if expected_dimension is not None and matrix.shape[1] != expected_dimension:
        raise BookEngineError(
            "EMBEDDING_DIMENSION_CHANGED",
            f"expected dimension {expected_dimension}, received {matrix.shape[1]}",
        )
    if not np.isfinite(matrix).all():
        raise BookEngineError("EMBEDDING_RESPONSE_INVALID", "embedding matrix contains non-finite values")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise BookEngineError("EMBEDDING_RESPONSE_INVALID", "embedding matrix contains a zero vector")
    return matrix / norms


@dataclass(frozen=True)
class IndexStatus:
    ready: bool
    reason: str
    manifest: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        summary = None
        if self.manifest:
            summary = {
                key: self.manifest.get(key)
                for key in (
                    "index_id", "contract_version", "canonical_corpus_digest",
                    "model_id", "dimension", "metric", "vector_count", "shard_count",
                )
            }
        return {"ready": self.ready, "reason": self.reason, "manifest": summary}


def inspect_index(project_root: Path | str | None = None) -> IndexStatus:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    manifest_path = root / "book" / "retrieval" / "index_manifest.json"
    if not manifest_path.is_file():
        return IndexStatus(False, "INDEX_MANIFEST_MISSING")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        snapshot = require_ready(root)
        if manifest.get("schema_version") != SCHEMA_VERSION or manifest.get("contract_version") != CONTRACT_VERSION:
            raise ValueError("unsupported index manifest version")
        if manifest.get("canonical_corpus_digest") != snapshot.inventory.corpus_digest:
            raise ValueError("canonical corpus digest changed")
        if manifest.get("canonical_manifest_sha256") != snapshot.inventory.manifest_sha256:
            raise ValueError("canonical manifest changed")
        index_root = _safe_path(root, manifest.get("index_root"), within=root / "book" / "retrieval" / "indexes")
        if not index_root.is_dir() or index_root.is_symlink():
            raise ValueError("index root missing")
        count = 0
        dimension = int(manifest["dimension"])
        for shard in manifest.get("shards") or []:
            vector_path = _safe_path(root, shard.get("vectors_path"), within=index_root)
            rows_path = _safe_path(root, shard.get("rows_path"), within=index_root)
            if sha256_file(vector_path) != shard.get("vectors_sha256") or sha256_file(rows_path) != shard.get("rows_sha256"):
                raise ValueError("index shard hash mismatch")
            matrix = np.load(vector_path, mmap_mode="r", allow_pickle=False)
            with rows_path.open(encoding="utf-8") as handle:
                row_count = sum(1 for line in handle if line.strip())
            if matrix.shape != (row_count, dimension) or row_count != int(shard["count"]):
                raise ValueError("index shard shape/count mismatch")
            if matrix.dtype != np.float32 or not np.isfinite(matrix).all():
                raise ValueError("index shard vectors are not finite float32 values")
            norms = np.linalg.norm(matrix, axis=1)
            if not np.allclose(norms, 1.0, rtol=1e-5, atol=1e-6):
                raise ValueError("index shard vectors are not L2-normalised")
            count += row_count
        if count != int(manifest.get("vector_count") or -1):
            raise ValueError("index vector count mismatch")
        if count != snapshot.inventory.retrieval_ready_chunk_count:
            raise ValueError("index does not cover every retrieval-ready chunk")
        return IndexStatus(True, "READY", manifest)
    except Exception as exc:
        return IndexStatus(False, f"INDEX_INVALID:{exc}")


def build_index(
    project_root: Path | str | None = None,
    *,
    batch_size: int = 32,
    resume: bool = True,
    client: LocalEmbeddingClient | None = None,
    progress: Any = None,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if batch_size < 1 or batch_size > 256:
        raise BookEngineError("INVALID_BATCH_SIZE", "batch size must be between 1 and 256")
    inputs = load_book_inputs(root)
    snapshot = require_ready(root)
    records = [record.to_dict() for record in snapshot.manifest.documents]
    model, endpoint, model_config_sha = _model_settings(inputs)
    embedding_client = client or LocalEmbeddingClient(endpoint, model, timeout=600.0)
    if not embedding_client.available():
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact embedding model is unavailable: {model}")
    probe = embedding_client.embed("TunnelBookAI retrieval index dimension probe.")
    if not probe:
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "embedding dimension probe failed")
    dimension = len(probe)
    identity = {
        "scope_sha256": inputs.identities["scope_sha256"],
        "question_bank_sha256": inputs.identities["question_bank_sha256"],
        "canonical_corpus_digest": snapshot.inventory.corpus_digest,
        "canonical_manifest_sha256": snapshot.inventory.manifest_sha256,
        "canonical_source_digest": _canonical_source_digest(records),
        "model_id": model,
        "model_configuration": model_config_sha,
        "prompt_version": PROMPT_VERSION,
        "software_version": SOFTWARE_VERSION,
        "dimension": dimension,
        "metric": "cosine",
        "normalised": True,
    }
    index_id = "BRI_" + canonical_sha256(identity)
    retrieval_root = root / "book" / "retrieval"
    final_dir = retrieval_root / "indexes" / index_id
    active_manifest = retrieval_root / "index_manifest.json"
    if active_manifest.is_file():
        status = inspect_index(root)
        if status.ready and status.manifest and status.manifest.get("index_id") == index_id:
            return {"status": "NO_CHANGE", **status.manifest}
    work_dir = retrieval_root / "builds" / index_id
    state_path = work_dir / "build_state.json"
    if work_dir.exists() and not resume:
        raise BookEngineError("INDEX_BUILD_EXISTS", f"resumable build already exists: {work_dir}")
    work_dir.mkdir(parents=True, exist_ok=True)
    state: dict[str, Any] = {
        "index_id": index_id,
        "identity": identity,
        "processed": 0,
        "shards": [],
    }
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("index_id") != index_id or state.get("identity") != identity:
            raise BookEngineError("INDEX_BUILD_STALE", "existing retrieval build identity differs")
    processed = int(state.get("processed") or 0)
    expected = snapshot.inventory.retrieval_ready_chunk_count
    batch: list[dict[str, Any]] = []
    seen = 0

    def commit(rows: list[dict[str, Any]]) -> None:
        nonlocal processed, state
        texts = [str(row["_embedding_text"]) for row in rows]
        vectors = embedding_client.embed_many(texts)
        if not vectors:
            raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "embedding batch request failed")
        matrix = _normalise(vectors, expected_dimension=dimension)
        shard_number = len(state["shards"])
        vector_name = f"vectors_{shard_number:05d}.npy"
        rows_name = f"rows_{shard_number:05d}.jsonl"
        _atomic_npy(work_dir / vector_name, matrix)
        _atomic_jsonl(work_dir / rows_name, (_public_row(row) for row in rows))
        shard = {"number": shard_number, "count": len(rows), "vectors_file": vector_name, "rows_file": rows_name}
        state = {**state, "processed": processed + len(rows), "shards": [*state["shards"], shard]}
        _atomic_json(state_path, state)
        processed += len(rows)
        if progress:
            progress({"index_id": index_id, "processed": processed, "expected": expected, "shard": shard_number})

    for row in _canonical_rows(root, records):
        if seen < processed:
            seen += 1
            continue
        seen += 1
        batch.append(row)
        if len(batch) >= batch_size:
            commit(batch)
            batch = []
    if batch:
        commit(batch)
    if seen != expected or processed != expected:
        raise BookEngineError(
            "INDEX_COVERAGE_MISMATCH",
            f"canonical rows/index coverage mismatch: seen={seen}, processed={processed}, expected={expected}",
        )
    if final_dir.exists():
        raise BookEngineError("INDEX_TARGET_EXISTS", f"index target already exists without an active valid manifest: {final_dir}")
    final_dir.parent.mkdir(parents=True, exist_ok=True)
    state_path.unlink(missing_ok=True)
    os.replace(work_dir, final_dir)
    shards = []
    for shard in state["shards"]:
        vector_path = final_dir / shard["vectors_file"]
        rows_path = final_dir / shard["rows_file"]
        shards.append({
            "number": shard["number"],
            "count": shard["count"],
            "vectors_path": vector_path.relative_to(root).as_posix(),
            "vectors_sha256": sha256_file(vector_path),
            "rows_path": rows_path.relative_to(root).as_posix(),
            "rows_sha256": sha256_file(rows_path),
        })
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "index_id": index_id,
        **identity,
        "endpoint_policy": "loopback-only",
        "index_root": final_dir.relative_to(root).as_posix(),
        "vector_count": expected,
        "shard_count": len(shards),
        "shards": shards,
    }
    _atomic_json(active_manifest, manifest)
    status = inspect_index(root)
    if not status.ready:
        active_manifest.unlink(missing_ok=True)
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", status.reason)
    return {"status": "BUILT", **manifest}


def _section_matches(row: Mapping[str, Any], section: str | None) -> bool:
    if not section:
        return True
    values = [str(row.get("section_id") or ""), *[str(value) for value in row.get("secondary_section_ids") or []]]
    return any(value == section or value.startswith(section + ".") for value in values)


def _canonical_text(root: Path, row: Mapping[str, Any]) -> str:
    path = _safe_path(root, row["canonical_retrieval_path"], within=root / "corpus" / "canonical")
    wanted = int(row["canonical_line_number"])
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if number == wanted:
                payload = json.loads(line)
                if payload.get("chunk_id") != row.get("chunk_id"):
                    raise BookEngineError("RETRIEVAL_INDEX_INVALID", "canonical row identity changed")
                return str(payload.get("embedding_text") or "")
    raise BookEngineError("RETRIEVAL_INDEX_INVALID", "canonical row locator is missing")


def search_index(
    query: str,
    project_root: Path | str | None = None,
    *,
    section: str | None = None,
    top_k: int = 10,
    client: LocalEmbeddingClient | None = None,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if not query.strip():
        raise BookEngineError("EMPTY_QUERY", "retrieval query must not be empty")
    if top_k < 1 or top_k > 100:
        raise BookEngineError("INVALID_TOP_K", "top_k must be between 1 and 100")
    status = inspect_index(root)
    if not status.ready or not status.manifest:
        raise BookEngineError("RETRIEVAL_INDEX_NOT_READY", status.reason)
    manifest = status.manifest
    inputs = load_book_inputs(root)
    model, endpoint, _ = _model_settings(inputs)
    if model != manifest["model_id"]:
        raise BookEngineError("RETRIEVAL_INDEX_STALE", "configured embedding model differs from index")
    embedding_client = client or LocalEmbeddingClient(endpoint, model, timeout=600.0)
    vector = embedding_client.embed(query)
    if not vector:
        raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "query embedding failed")
    query_vector = _normalise([vector], expected_dimension=int(manifest["dimension"]))[0]
    candidates: list[tuple[float, dict[str, Any]]] = []
    for shard in manifest["shards"]:
        matrix = np.load(root / shard["vectors_path"], mmap_mode="r", allow_pickle=False)
        rows = [json.loads(line) for line in (root / shard["rows_path"]).read_text(encoding="utf-8").splitlines() if line]
        # np.matmul emits spurious floating-point warnings for these finite
        # float32 mmap arrays on some NumPy/Accelerate combinations. np.dot is
        # equivalent for matrix-vector scoring and is stable on those builds.
        scores = np.dot(matrix, query_vector)
        if not np.isfinite(scores).all():
            raise BookEngineError("RETRIEVAL_INDEX_INVALID", "similarity scores contain non-finite values")
        for score, row in zip(scores.tolist(), rows):
            if _section_matches(row, section):
                candidates.append((float(score), row))
    candidates.sort(key=lambda item: (-item[0], str(item[1]["chunk_id"])))
    results = []
    for score, row in candidates[:top_k]:
        text = _canonical_text(root, row)
        results.append({**row, "score": round(score, 6), "snippet": " ".join(text.split())[:500]})
    return {
        "query": query,
        "section": section,
        "top_k": top_k,
        "index_id": manifest["index_id"],
        "canonical_corpus_digest": manifest["canonical_corpus_digest"],
        "model_id": manifest["model_id"],
        "results": results,
    }


__all__ = ["IndexStatus", "build_index", "inspect_index", "search_index"]
