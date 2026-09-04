"""Loopback embedding client for section retrieval (task §38).

Reuses the loopback discipline of `crawler/src/hybrid_classifier.py`: an OpenAI-compatible
server on 127.0.0.1 only, no cloud fallback of any kind. When no local server answers, the
classifier degrades to rules + crawler hint and records `embedding_status: UNAVAILABLE` —
it never reaches out to a remote host (§38, §80).
"""

from __future__ import annotations

import json
import math
import urllib.error
import urllib.request
from typing import Any

from ..vision.provider import RemoteEndpointRejected, assert_loopback
from .taxonomy import Taxonomy, load_taxonomy

AVAILABLE = "AVAILABLE"
UNAVAILABLE = "UNAVAILABLE"
DISABLED = "DISABLED"


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class LocalEmbeddingClient:
    def __init__(self, base_url: str, *, timeout: float = 60.0) -> None:
        self.base_url = assert_loopback(base_url)
        self.timeout = timeout
        self.model: str | None = None
        self._models: list[str] | None = None

    def _get(self, path: str) -> dict[str, Any]:
        url = assert_loopback(f"{self.base_url}{path}")
        with urllib.request.urlopen(url, timeout=min(self.timeout, 15)) as response:
            return json.loads(response.read().decode("utf-8"))

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = assert_loopback(f"{self.base_url}{path}")
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def models(self) -> list[str]:
        if self._models is None:
            try:
                payload = self._get("/models")
                self._models = [str(m.get("id")) for m in payload.get("data", []) if m.get("id")]
            except (urllib.error.URLError, OSError, ValueError):
                self._models = []
        return self._models

    def pick_model(self, preferred_terms: list[str]) -> str | None:
        models = self.models()
        for term in preferred_terms:
            for name in models:
                if term.lower() in name.lower():
                    return name
        return models[0] if models else None

    def available(self, preferred_terms: list[str]) -> bool:
        if self.model is None:
            self.model = self.pick_model(preferred_terms)
        return self.model is not None

    def embed(self, text: str) -> list[float] | None:
        if self.model is None:
            return None
        try:
            payload = self._post("/embeddings", {"model": self.model, "input": text})
            return [float(x) for x in payload["data"][0]["embedding"]]
        except RemoteEndpointRejected:
            raise
        except Exception:
            return None


class SectionEmbeddingIndex:
    """Embeds every canonical section profile once, then scores documents against them."""

    def __init__(self, client: LocalEmbeddingClient, taxonomy: Taxonomy | None = None) -> None:
        self.client = client
        self.taxonomy = taxonomy or load_taxonomy()
        self._vectors: dict[str, list[float]] = {}

    def build(self) -> int:
        for section in self.taxonomy.sections.values():
            if not section.active or section.section_id in self._vectors:
                continue
            vector = self.client.embed(section.profile)
            if vector:
                self._vectors[section.section_id] = vector
        return len(self._vectors)

    def score(self, text: str, *, top_k: int = 8, min_similarity: float = 0.30
              ) -> list[dict[str, Any]]:
        vector = self.client.embed(text)
        if not vector:
            return []
        if not self._vectors:
            self.build()
        scores: list[dict[str, Any]] = []
        for section_id, profile_vector in self._vectors.items():
            similarity = cosine(vector, profile_vector)
            # map cosine [-1,1] to [0,1] exactly as the crawler's fusion expects
            normalized = max(0.0, min(1.0, (similarity + 1.0) / 2.0))
            if normalized >= min_similarity:
                scores.append({"id": section_id, "score": round(normalized, 4)})
        scores.sort(key=lambda row: row["score"], reverse=True)
        return scores[:top_k]


def build_index(config: Any, taxonomy: Taxonomy | None = None
                ) -> tuple[SectionEmbeddingIndex | None, str, str | None]:
    """Resolve a local embedding server. Returns (index, status, model)."""
    cfg = (config.classification or {}).get("embedding", {}) or {}
    if not cfg.get("enabled", True):
        return None, DISABLED, None
    preferred = list(cfg.get("preferred_model_terms", ["nomic-embed", "embed"]))
    for server in cfg.get("local_servers", ["http://127.0.0.1:1234/v1"]):
        try:
            client = LocalEmbeddingClient(server)
        except RemoteEndpointRejected:
            raise
        if client.available(preferred):
            return SectionEmbeddingIndex(client, taxonomy), AVAILABLE, client.model
    return None, UNAVAILABLE, None
