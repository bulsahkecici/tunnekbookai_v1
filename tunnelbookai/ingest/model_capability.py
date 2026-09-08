"""Capability verification for the exact local models configured by ``models.yaml``."""

from __future__ import annotations

import os
from typing import Any

from .classify.arbiter import LocalChatClient
from .classify.embeddings import LocalEmbeddingClient
from .vision.provider import RemoteEndpointRejected, assert_loopback


UNAVAILABLE = "MODEL_SERVICE_UNAVAILABLE"
AVAILABLE = "AVAILABLE"


def _service(cfg: dict[str, Any], fallback_env: str) -> tuple[str, str]:
    model = str(cfg.get("model") or "").strip()
    endpoint = os.getenv(str(cfg.get("endpoint_env") or fallback_env),
                         str(cfg.get("default_endpoint") or "")).strip()
    if not model or not endpoint:
        raise ValueError("missing exact local model or endpoint configuration")
    return assert_loopback(endpoint), model


def probe(config: Any) -> dict[str, Any]:
    """Probe exact configured models without any model selection fallback."""
    result: dict[str, Any] = {"embedding": {}, "llm": {}, "decision": UNAVAILABLE}
    try:
        embedding_endpoint, embedding_model = _service(config.models.get("embedding", {}), "EMBEDDING_SERVER")
        client = LocalEmbeddingClient(embedding_endpoint, embedding_model)
        first = client.embed("TunnelBookAI capability probe.") if client.available() else None
        second = client.embed("TunnelBookAI capability probe.") if client.available() else None
        stable = bool(first and second and len(first) == len(second))
        result["embedding"] = {
            "endpoint": embedding_endpoint,
            "model": embedding_model,
            "model_available": client.available(),
            "request_succeeds": bool(first),
            "non_empty_vector": bool(first),
            "vector_dimension": len(first or []),
            "stable_dimension": stable,
            "status": AVAILABLE if stable else UNAVAILABLE,
        }
    except (RemoteEndpointRejected, ValueError, OSError):
        result["embedding"] = {"status": UNAVAILABLE}

    try:
        llm_endpoint, llm_model = _service(config.models.get("llm", {}), "LLM_SERVER")
        client = LocalChatClient(llm_endpoint)
        payload = client.chat_json(llm_model, "Return JSON only.", "Return {\"ok\": true}.") if client.has_model(llm_model) else None
        result["llm"] = {
            "endpoint": llm_endpoint,
            "model": llm_model,
            "model_available": client.has_model(llm_model),
            "structured_request_succeeds": isinstance(payload, dict),
            "status": AVAILABLE if isinstance(payload, dict) else UNAVAILABLE,
        }
    except (RemoteEndpointRejected, ValueError, OSError):
        result["llm"] = {"status": UNAVAILABLE}

    if result["embedding"].get("status") == AVAILABLE and result["llm"].get("status") == AVAILABLE:
        result["decision"] = AVAILABLE
    return result
