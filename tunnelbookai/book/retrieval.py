"""Manifest-bound, rebuildable local vector retrieval over canonical evidence only."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

import numpy as np
import yaml

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.canonical.verifier import require_ready
from tunnelbookai.ingest.classify.embeddings import LocalEmbeddingClient
from tunnelbookai.ingest.vision.provider import assert_loopback

from .errors import BookEngineError
from .inputs import BookInputs, load_book_inputs
from .lexical import LexicalIndex, build_lexical_index, lexical_root


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "book-retrieval-v1"
SOFTWARE_VERSION = "book-retrieval-v1"
PROMPT_VERSION = "not-applicable-embedding-v1"
RETRIEVAL_POLICY_VERSION = "hybrid-rrf-v1"


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
    lexical: Mapping[str, Any] | None = None

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
        return {"ready": self.ready, "reason": self.reason, "manifest": summary, "lexical": self.lexical}


def inspect_lexical(project_root: Path | str, index_id: str) -> dict[str, Any] | None:
    """Summarise the lexical index bound to ``index_id`` without loading its matrix."""

    manifest_path = lexical_root(Path(project_root).resolve(), index_id) / "manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return {
        key: manifest.get(key)
        for key in ("lexical_index_id", "contract_version", "tokenizer_version", "row_count", "vocabulary_size")
    }


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
        return IndexStatus(True, "READY", manifest, inspect_lexical(root, str(manifest["index_id"])))
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
    previous_vectors: dict[str, np.ndarray] = {}
    if active_manifest.is_file():
        status = inspect_index(root)
        if status.ready and status.manifest and status.manifest.get("index_id") == index_id:
            if status.lexical is None:
                lexical = ensure_lexical_index(root, status.manifest, records=records)
                return {"status": "LEXICAL_BUILT", "lexical": lexical, **status.manifest}
            return {"status": "NO_CHANGE", "lexical": status.lexical, **status.manifest}
        # The previous index is normally stale here (the canonical digest changed), but its
        # shards are still hash-verifiable: vectors for unchanged canonical text are reused
        # (keyed by embedding text hash) so re-promoting a few documents does not re-embed
        # the whole corpus.
        previous_vectors = _load_previous_vectors(root, active_manifest, model=model, dimension=dimension)
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
    reused = int(state.get("reused") or 0)

    def commit(rows: list[dict[str, Any]]) -> None:
        nonlocal processed, state, reused
        matrix = np.zeros((len(rows), dimension), dtype=np.float32)
        missing = [index for index, row in enumerate(rows) if row["embedding_text_sha256"] not in previous_vectors]
        for index, row in enumerate(rows):
            if index not in missing:
                matrix[index] = previous_vectors[row["embedding_text_sha256"]]
        reused += len(rows) - len(missing)
        if missing:
            vectors = embedding_client.embed_many([str(rows[index]["_embedding_text"]) for index in missing])
            if not vectors:
                raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "embedding batch request failed")
            fresh = _normalise(vectors, expected_dimension=dimension)
            for target, source in zip(missing, fresh):
                matrix[target] = source
        matrix = _normalise(matrix.tolist(), expected_dimension=dimension)
        shard_number = len(state["shards"])
        vector_name = f"vectors_{shard_number:05d}.npy"
        rows_name = f"rows_{shard_number:05d}.jsonl"
        _atomic_npy(work_dir / vector_name, matrix)
        _atomic_jsonl(work_dir / rows_name, (_public_row(row) for row in rows))
        shard = {"number": shard_number, "count": len(rows), "vectors_file": vector_name, "rows_file": rows_name}
        state = {**state, "processed": processed + len(rows), "reused": reused, "shards": [*state["shards"], shard]}
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
        "reused_vector_count": reused,
        "shard_count": len(shards),
        "shards": shards,
    }
    _atomic_json(active_manifest, manifest)
    status = inspect_index(root)
    if not status.ready:
        active_manifest.unlink(missing_ok=True)
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", status.reason)
    lexical = ensure_lexical_index(root, manifest, records=records)
    return {"status": "BUILT", "lexical": lexical, **manifest}


def _load_previous_vectors(root: Path, manifest_path: Path, *, model: str, dimension: int) -> dict[str, np.ndarray]:
    """Hash-verified vectors of an earlier index of the same exact model, keyed by text hash."""

    vectors: dict[str, np.ndarray] = {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("model_id") != model or int(manifest.get("dimension") or 0) != dimension:
            return vectors
        index_root = _safe_path(root, manifest.get("index_root"), within=root / "book" / "retrieval" / "indexes")
        for shard in manifest.get("shards") or []:
            vector_path = _safe_path(root, shard.get("vectors_path"), within=index_root)
            rows_path = _safe_path(root, shard.get("rows_path"), within=index_root)
            if sha256_file(vector_path) != shard.get("vectors_sha256") or sha256_file(rows_path) != shard.get("rows_sha256"):
                return {}
            matrix = np.asarray(np.load(vector_path, allow_pickle=False))
            lines = [line for line in rows_path.read_text(encoding="utf-8").splitlines() if line]
            if matrix.shape != (len(lines), dimension) or not np.isfinite(matrix).all():
                return {}
            for position, line in enumerate(lines):
                vectors[str(json.loads(line)["embedding_text_sha256"])] = matrix[position]
    except (OSError, ValueError, KeyError, TypeError, BookEngineError):
        return {}
    return vectors


def _index_rows(root: Path, manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shard in manifest["shards"]:
        rows.extend(json.loads(line) for line in (root / shard["rows_path"]).read_text(encoding="utf-8").splitlines() if line)
    return rows


def ensure_lexical_index(
    root: Path,
    manifest: Mapping[str, Any],
    *,
    records: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the BM25 companion of a verified dense index from the same canonical rows."""

    index_id = str(manifest["index_id"])
    existing = inspect_lexical(root, index_id)
    if existing is not None:
        return existing
    if records is None:
        snapshot = require_ready(root)
        records = [record.to_dict() for record in snapshot.manifest.documents]
    dense_rows = _index_rows(root, manifest)
    canonical = list(_canonical_rows(root, records))
    if [row["chunk_id"] for row in canonical] != [row["chunk_id"] for row in dense_rows]:
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", "canonical rows no longer match the dense index order")
    built = build_lexical_index(root, index_id=index_id, rows=dense_rows, texts=(row["_embedding_text"] for row in canonical))
    return {
        key: built.get(key)
        for key in ("lexical_index_id", "contract_version", "tokenizer_version", "row_count", "vocabulary_size")
    }


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


@dataclass(frozen=True)
class RetrievalPolicy:
    """Deterministic hybrid ranking policy; every knob is recorded in audit identities."""

    version: str = RETRIEVAL_POLICY_VERSION
    rrf_k: int = 60
    candidate_pool: int = 60
    min_chars: int = 150
    exclude_toc_like: bool = True
    chunk_type_weights: Mapping[str, float] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.chunk_type_weights is None:
            object.__setattr__(self, "chunk_type_weights", {
                "TEXT_CHUNK": 1.0,
                "OCR_CHUNK": 1.0,
                "SHEET_CHUNK": 0.9,
                "SLIDE_CHUNK": 0.9,
                "TABLE_CHUNK": 0.85,
                "FIGURE_CHUNK": 0.6,
            })
        if self.rrf_k < 1 or self.candidate_pool < 1 or self.min_chars < 0:
            raise BookEngineError("INVALID_RETRIEVAL_POLICY", "retrieval policy values must be positive")

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "rrf_k": self.rrf_k,
            "candidate_pool": self.candidate_pool,
            "min_chars": self.min_chars,
            "exclude_toc_like": self.exclude_toc_like,
            "chunk_type_weights": dict(sorted(self.chunk_type_weights.items())),
        }


DEFAULT_POLICY = RetrievalPolicy()


class HybridRetriever:
    """Dense (BGE-M3 cosine) + lexical (BM25) reciprocal-rank fusion over one verified index.

    Both signals rank the same canonical rows.  For every query the top ``candidate_pool``
    rows of each signal are fused with ``1 / (rrf_k + rank)``; the fused score is then
    scaled by the chunk-type weight so short figure captions no longer crowd out prose, and
    rows failing the noise policy (too short, table-of-contents like) are excluded before
    ranking.  Ties break on chunk id so results are reproducible.
    """

    def __init__(
        self,
        project_root: Path | str | None = None,
        *,
        client: LocalEmbeddingClient | None = None,
        policy: RetrievalPolicy = DEFAULT_POLICY,
        inputs: BookInputs | None = None,
    ) -> None:
        self.root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
        status = inspect_index(self.root)
        if not status.ready or not status.manifest:
            raise BookEngineError("RETRIEVAL_INDEX_NOT_READY", status.reason)
        self.manifest = status.manifest
        self.policy = policy
        book_inputs = inputs or load_book_inputs(self.root)
        model, endpoint, _ = _model_settings(book_inputs)
        if model != self.manifest["model_id"]:
            raise BookEngineError("RETRIEVAL_INDEX_STALE", "configured embedding model differs from index")
        self.client = client or LocalEmbeddingClient(endpoint, model, timeout=600.0)
        if not self.client.available():
            raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", f"exact embedding model is unavailable: {model}")
        matrices: list[np.ndarray] = []
        self.rows: list[dict[str, Any]] = []
        for shard in self.manifest["shards"]:
            matrices.append(np.asarray(np.load(self.root / shard["vectors_path"], allow_pickle=False)))
            self.rows.extend(json.loads(line) for line in (self.root / shard["rows_path"]).read_text(encoding="utf-8").splitlines() if line)
        self.matrix = np.vstack(matrices).astype(np.float32, copy=False)
        if self.matrix.shape != (len(self.rows), int(self.manifest["dimension"])):
            raise BookEngineError("RETRIEVAL_INDEX_INVALID", "loaded matrix does not match index rows")
        self.lexical = LexicalIndex.load(self.root, index_id=str(self.manifest["index_id"]), expected_chunk_ids=[row["chunk_id"] for row in self.rows])
        weights = np.zeros(len(self.rows), dtype=np.float32)
        for position, (row, meta) in enumerate(zip(self.rows, self.lexical.metadata)):
            if int(meta.get("chars") or 0) < policy.min_chars:
                continue
            if policy.exclude_toc_like and meta.get("toc_like"):
                continue
            weights[position] = float(policy.chunk_type_weights.get(str(row.get("chunk_type")), 0.0))
        self.weights = weights

    @property
    def identity(self) -> dict[str, Any]:
        return {
            "retrieval_index_id": self.manifest["index_id"],
            "lexical_index_id": self.lexical.manifest["lexical_index_id"],
            "retrieval_policy": self.policy.to_dict(),
        }

    def _eligible(self, section: str | None) -> np.ndarray:
        mask = self.weights > 0
        if section:
            section_mask = np.fromiter((_section_matches(row, section) for row in self.rows), dtype=bool, count=len(self.rows))
            mask &= section_mask
        return mask

    def search(
        self,
        dense_queries: Sequence[str],
        lexical_queries: Sequence[str] | None = None,
        *,
        top_k: int,
        section: str | None = None,
    ) -> list[list[dict[str, Any]]]:
        if not dense_queries:
            return []
        if top_k < 1:
            raise BookEngineError("INVALID_TOP_K", "top_k must be positive")
        lexical_queries = list(lexical_queries or dense_queries)
        if len(lexical_queries) != len(dense_queries):
            raise BookEngineError("INVALID_QUERY", "dense and lexical query lists differ in length")
        vectors = self.client.embed_many([str(query) for query in dense_queries])
        if not vectors:
            raise BookEngineError("MODEL_SERVICE_UNAVAILABLE", "query embedding batch failed")
        queries = _normalise(vectors, expected_dimension=int(self.manifest["dimension"]))
        dense_scores = np.dot(self.matrix, queries.T)
        if not np.isfinite(dense_scores).all():
            raise BookEngineError("RETRIEVAL_INDEX_INVALID", "similarity scores contain non-finite values")
        mask = self._eligible(section)
        eligible = np.flatnonzero(mask)
        results: list[list[dict[str, Any]]] = []
        pool = self.policy.candidate_pool
        for number, lexical_query in enumerate(lexical_queries):
            if eligible.size == 0:
                results.append([])
                continue
            dense_column = dense_scores[eligible, number]
            lexical_column = self.lexical.score(str(lexical_query))[eligible]
            fused: dict[int, float] = {}
            ranks: dict[int, dict[str, Any]] = {}
            dense_order = sorted(range(eligible.size), key=lambda i: (-float(dense_column[i]), self.rows[int(eligible[i])]["chunk_id"]))[:pool]
            for rank, local in enumerate(dense_order, 1):
                fused[local] = fused.get(local, 0.0) + 1.0 / (self.policy.rrf_k + rank)
                ranks.setdefault(local, {})["dense_rank"] = rank
            lexical_order = [i for i in sorted(range(eligible.size), key=lambda i: (-float(lexical_column[i]), self.rows[int(eligible[i])]["chunk_id"])) if lexical_column[i] > 0][:pool]
            for rank, local in enumerate(lexical_order, 1):
                fused[local] = fused.get(local, 0.0) + 1.0 / (self.policy.rrf_k + rank)
                ranks.setdefault(local, {})["lexical_rank"] = rank
            scored = []
            for local, value in fused.items():
                position = int(eligible[local])
                scored.append((value * float(self.weights[position]), position, local))
            scored.sort(key=lambda item: (-item[0], self.rows[item[1]]["chunk_id"]))
            rows: list[dict[str, Any]] = []
            for fused_score, position, local in scored[:top_k]:
                rows.append({
                    **self.rows[position],
                    "score": round(fused_score, 6),
                    "dense_score": round(float(dense_column[local]), 6),
                    "dense_rank": ranks[local].get("dense_rank"),
                    "lexical_score": round(float(lexical_column[local]), 6),
                    "lexical_rank": ranks[local].get("lexical_rank"),
                    "retrieval_weight": round(float(self.weights[position]), 3),
                })
            results.append(rows)
        return results

    def text(self, row: Mapping[str, Any]) -> str:
        return _canonical_text(self.root, row)


def search_index(
    query: str,
    project_root: Path | str | None = None,
    *,
    section: str | None = None,
    top_k: int = 10,
    client: LocalEmbeddingClient | None = None,
    policy: RetrievalPolicy = DEFAULT_POLICY,
) -> dict[str, Any]:
    root = Path(project_root or Path(__file__).resolve().parents[2]).resolve()
    if not query.strip():
        raise BookEngineError("EMPTY_QUERY", "retrieval query must not be empty")
    if top_k < 1 or top_k > 100:
        raise BookEngineError("INVALID_TOP_K", "top_k must be between 1 and 100")
    retriever = HybridRetriever(root, client=client, policy=policy)
    results = []
    for row in retriever.search([query], top_k=top_k, section=section)[0]:
        text = retriever.text(row)
        results.append({**row, "snippet": " ".join(text.split())[:500]})
    return {
        "query": query,
        "section": section,
        "top_k": top_k,
        "index_id": retriever.manifest["index_id"],
        "lexical_index_id": retriever.lexical.manifest["lexical_index_id"],
        "retrieval_policy": policy.to_dict(),
        "canonical_corpus_digest": retriever.manifest["canonical_corpus_digest"],
        "model_id": retriever.manifest["model_id"],
        "results": results,
    }


__all__ = ["DEFAULT_POLICY", "HybridRetriever", "IndexStatus", "RetrievalPolicy", "build_index", "ensure_lexical_index", "inspect_index", "search_index"]
