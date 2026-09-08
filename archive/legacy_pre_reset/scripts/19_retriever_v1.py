"""TunnelBookAI Retriever v1 - frozen production dense retriever.

DENSE_V1 only: query -> BGE-M3 dense embedding -> Qdrant cosine search -> ranked results.

Deliberately excluded, each because it was measured and rejected:
  * BM25 / RRF hybrid      - wrecked cross-lingual retrieval (probe v2 R@10 0.111 vs dense 0.259)
  * language routing       - every variant made cross-lingual worse, not better (0.074-0.111)
  * query translation      - failed production preflight (latency, reliability, terminology drift)
  * reranker               - lowered R@1 and MRR at ~100x the search cost
  * neighbour expansion    - significantly worse on every metric
  * score threshold / low-content penalty / document cap - no measured benefit

This module is standalone by design. It must not import the experimental retrieval scripts
(17_retrieval_improvement, 18_language_aware_retrieval); those are audit code, not production code.

FROZEN. Changes require retriever v1.1 or v2, not edits here.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


RELEASE_NAME = "tunnelbook-retriever-v1"
RELEASE_VERSION = "1.0.0"
RETRIEVER = "DENSE_V1"

DENSE_MODEL = "BAAI/bge-m3"
DENSE_MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
EMBEDDING_DIMENSION = 1024
MAX_SEQUENCE_LENGTH = 8192

QDRANT_COLLECTION = "tunnelbook_dense_v1"
QDRANT_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
DISTANCE = "COSINE"
EXPECTED_POINTS = 5992

DEFAULT_TOP_K = 10
MAXIMUM_TOP_K = 100

# Filters the caller may pass explicitly. Nothing here is ever applied automatically - in particular
# `language`, because a Turkish query legitimately needs English sources and auto-filtering by
# detected query language was measured to destroy cross-lingual recall.
SUPPORTED_FILTERS = ("document_id", "language", "document_type", "authority_level", "year",
                     "source_kind", "topics")

PAYLOAD_FIELDS = ("chunk_id", "document_id", "text", "title", "heading", "section_path",
                  "parent_heading", "source_kind", "citation_mode", "provenance_status",
                  "original_page_start", "original_page_end", "slide_start", "slide_end",
                  "source_relative_path", "source_extension", "language", "document_type",
                  "authority_level", "year", "topics", "contains_table",
                  "contains_formula_placeholder", "contains_image_placeholder", "is_low_content",
                  "recovery_version", "recovery_method")


class RetrieverUnavailable(RuntimeError):
    """Qdrant (or the model) could not be reached. Never silently degrade to an empty result."""


class QueryTooLong(ValueError):
    """The query exceeds the model's effective context. Truncating silently would corrupt the search."""


@dataclass(frozen=True)
class RetrievalResult:
    rank: int
    score: float
    point_id: int
    chunk_id: str
    document_id: str
    text: str
    title: str | None
    heading: str | None
    section_path: str | None
    parent_heading: str | None
    source_kind: str
    citation_mode: str | None
    provenance_status: str | None
    original_page_start: int | None
    original_page_end: int | None
    slide_start: int | None
    slide_end: int | None
    source_relative_path: str | None
    source_extension: str | None
    language: str | None
    document_type: str | None
    authority_level: str | None
    year: int | None
    topics: list[str] | None
    contains_table: bool
    contains_formula_placeholder: bool
    contains_image_placeholder: bool
    is_low_content: bool
    recovery_version: str | None = None
    recovery_method: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _build_filter(filters: dict[str, Any] | None):
    """Translate an explicit caller filter dict into a Qdrant filter. Never called implicitly."""
    if not filters:
        return None
    from qdrant_client import models
    unsupported = set(filters) - set(SUPPORTED_FILTERS)
    if unsupported:
        raise ValueError(f"unsupported filter fields: {sorted(unsupported)}; "
                         f"supported: {sorted(SUPPORTED_FILTERS)}")
    conditions = []
    for field_name, value in filters.items():
        if isinstance(value, (list, tuple, set)):
            conditions.append(models.FieldCondition(key=field_name,
                                                    match=models.MatchAny(any=list(value))))
        else:
            conditions.append(models.FieldCondition(key=field_name,
                                                    match=models.MatchValue(value=value)))
    return models.Filter(must=conditions)


class RetrieverV1:
    """Frozen dense retriever. Loads the pinned model once and queries the pinned collection."""

    def __init__(self, qdrant_url: str = QDRANT_URL, device: str | None = None, lazy: bool = True):
        self.qdrant_url = qdrant_url
        self._device = device
        self._model = None
        self._tokenizer = None
        self._client = None
        if not lazy:
            self._ensure_model()
            self._ensure_client()

    # ---- resources -----------------------------------------------------------------------
    def _ensure_model(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(DENSE_MODEL, revision=DENSE_MODEL_REVISION)
            model = AutoModel.from_pretrained(DENSE_MODEL, revision=DENSE_MODEL_REVISION)
            if self._device is None:
                self._device = "mps" if torch.backends.mps.is_available() else "cpu"
            self._model = model.to(self._device).eval()
        except Exception as error:
            raise RetrieverUnavailable(f"dense model unavailable: {type(error).__name__}: {error}") from error

    def _ensure_client(self):
        if self._client is not None:
            return
        try:
            from qdrant_client import QdrantClient
            client = QdrantClient(url=self.qdrant_url, timeout=60)
            client.get_collection(QDRANT_COLLECTION)
            self._client = client
        except Exception as error:
            raise RetrieverUnavailable(
                f"Qdrant collection '{QDRANT_COLLECTION}' unavailable at {self.qdrant_url}: "
                f"{type(error).__name__}: {error}") from error

    # ---- query embedding -----------------------------------------------------------------
    def token_count(self, query: str) -> int:
        self._ensure_model()
        return len(self._tokenizer(query, add_special_tokens=True, truncation=False,
                                   padding=False)["input_ids"])

    def embed_query(self, query: str):
        """CLS pooling + L2 normalisation, no prefix - exactly the behaviour the index was built with."""
        import torch
        self._ensure_model()
        length = self.token_count(query)
        if length > MAX_SEQUENCE_LENGTH:
            raise QueryTooLong(
                f"query is {length} tokens, exceeding the model limit of {MAX_SEQUENCE_LENGTH}. "
                "Refusing to truncate silently; shorten or split the query.")
        encoded = self._tokenizer([query], padding=True, truncation=False, return_tensors="pt")
        encoded = {key: value.to(self._device) for key, value in encoded.items()}
        with torch.inference_mode():
            output = self._model(**encoded).last_hidden_state[:, 0]
            output = torch.nn.functional.normalize(output, p=2, dim=-1)
        return output.float().cpu().numpy()[0]

    # ---- retrieval -----------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = DEFAULT_TOP_K,
                 filters: dict[str, Any] | None = None) -> list[RetrievalResult]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        if top_k > MAXIMUM_TOP_K:
            raise ValueError(f"top_k {top_k} exceeds maximum {MAXIMUM_TOP_K}")
        vector = self.embed_query(query)
        self._ensure_client()
        try:
            points = self._client.query_points(
                collection_name=QDRANT_COLLECTION, query=vector.tolist(), limit=top_k,
                query_filter=_build_filter(filters), with_payload=True).points
        except Exception as error:
            raise RetrieverUnavailable(f"dense search failed: {type(error).__name__}: {error}") from error
        # Deterministic ordering: Qdrant returns score-descending; ties broken by point id so the
        # same query against the same release always yields the same ranking.
        ordered = sorted(points, key=lambda point: (-float(point.score), int(point.id)))
        results = []
        for rank, point in enumerate(ordered, start=1):
            payload = point.payload or {}
            results.append(RetrievalResult(
                rank=rank, score=float(point.score), point_id=int(point.id),
                chunk_id=payload.get("chunk_id", ""), document_id=payload.get("document_id", ""),
                text=payload.get("text", ""), title=payload.get("title"),
                heading=payload.get("heading"), section_path=payload.get("section_path"),
                parent_heading=payload.get("parent_heading"),
                source_kind=payload.get("source_kind", ""),
                citation_mode=payload.get("citation_mode"),
                provenance_status=payload.get("provenance_status"),
                original_page_start=payload.get("original_page_start"),
                original_page_end=payload.get("original_page_end"),
                slide_start=payload.get("slide_start"), slide_end=payload.get("slide_end"),
                source_relative_path=payload.get("source_relative_path"),
                source_extension=payload.get("source_extension"),
                language=payload.get("language"), document_type=payload.get("document_type"),
                authority_level=payload.get("authority_level"), year=payload.get("year"),
                topics=payload.get("topics"),
                contains_table=bool(payload.get("contains_table")),
                contains_formula_placeholder=bool(payload.get("contains_formula_placeholder")),
                contains_image_placeholder=bool(payload.get("contains_image_placeholder")),
                is_low_content=bool(payload.get("is_low_content")),
                recovery_version=payload.get("recovery_version"),
                recovery_method=payload.get("recovery_method")))
        return results

    def health(self) -> dict[str, Any]:
        self._ensure_client()
        count = self._client.count(collection_name=QDRANT_COLLECTION, exact=True).count
        return {"collection": QDRANT_COLLECTION, "exact_points": count,
                "expected_points": EXPECTED_POINTS, "healthy": count == EXPECTED_POINTS,
                "retriever": RETRIEVER, "release": RELEASE_NAME, "version": RELEASE_VERSION}


def release_config() -> dict[str, Any]:
    """The frozen configuration, as data. Anything absent here is absent from production."""
    return {
        "release_name": RELEASE_NAME, "release_version": RELEASE_VERSION, "retriever": RETRIEVER,
        "dense_model": DENSE_MODEL, "dense_model_revision": DENSE_MODEL_REVISION,
        "embedding_dimension": EMBEDDING_DIMENSION, "max_sequence_length": MAX_SEQUENCE_LENGTH,
        "pooling": "cls", "normalization": "l2", "query_prefix": None, "document_prefix": None,
        "qdrant_collection": QDRANT_COLLECTION, "distance": DISTANCE,
        "qdrant_expected_points": EXPECTED_POINTS,
        "default_top_k": DEFAULT_TOP_K, "maximum_top_k": MAXIMUM_TOP_K,
        "supported_filters": list(SUPPORTED_FILTERS),
        "automatic_translation": False, "automatic_language_filter": False,
        "bm25": False, "rrf": False, "reranker": False, "neighbor_expansion": False,
        "score_threshold": None, "low_content_penalty": None, "document_cap": None,
    }


def script_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


if __name__ == "__main__":
    import json
    import sys
    retriever = RetrieverV1()
    if len(sys.argv) > 1:
        for result in retriever.retrieve(" ".join(sys.argv[1:])):
            print(f"{result.rank:>3} {result.score:.4f} {result.chunk_id:<24} "
                  f"{(result.heading or '')[:50]}")
    else:
        print(json.dumps({**release_config(), "health": retriever.health(),
                          "script_sha256": script_sha256()}, indent=2, sort_keys=True))
