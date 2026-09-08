"""Local Qwen arbitration (task §39, §44).

The arbiter is called ONLY when the deterministic signals cannot settle the section:

    * top fused score below the configured llm_review threshold
    * the top two candidates are within the disagreement margin
    * rules and embeddings disagree on the top section
    * the crawler's provisional section disagrees with the computed top section
    * multi-section ambiguity

Strong agreement never reaches the model (§37). The endpoint is loopback-only; a non-loopback
base_url raises `RemoteEndpointRejected` rather than falling back to anything (§80).
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from ..vision.provider import RemoteEndpointRejected, assert_loopback
from .taxonomy import Taxonomy

NOT_RUN = "NOT_RUN"
SUCCESS = "SUCCESS"
UNAVAILABLE = "UNAVAILABLE"
FAILED = "FAILED"
REJECTED_INVALID_SECTION = "REJECTED_INVALID_SECTION"


class LocalChatClient:
    def __init__(self, base_url: str, *, timeout: float = 90.0) -> None:
        self.base_url = assert_loopback(base_url)
        self.timeout = timeout
        self._models: list[str] | None = None

    def models(self) -> list[str]:
        if self._models is None:
            try:
                url = assert_loopback(f"{self.base_url}/models")
                with urllib.request.urlopen(url, timeout=min(self.timeout, 15)) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                self._models = [str(m.get("id")) for m in payload.get("data", []) if m.get("id")]
            except (urllib.error.URLError, OSError, ValueError):
                self._models = []
        return self._models

    def has_model(self, model: str) -> bool:
        return model in self.models()

    def chat_json(self, model: str, system: str, user: str) -> dict[str, Any]:
        url = assert_loopback(f"{self.base_url}/chat/completions")
        payload = {
            "model": model, "temperature": 0.1,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
        }
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"] or ""
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("no JSON object in the arbiter response")
        return json.loads(match.group(0))


@dataclass
class ArbiterResult:
    status: str
    primary_section: str | None = None
    secondary_sections: list[str] = None
    confidence: float | None = None
    reason: str | None = None
    model: str | None = None

    def __post_init__(self) -> None:
        self.secondary_sections = self.secondary_sections or []


SYSTEM_PROMPT = (
    "Sen bir tünel mühendisliği kitabı için bölüm sınıflandırma hakemisin. "
    "Sana bir belgeden kanıtlar ve aday bölüm listesi verilecek. "
    "SADECE verilen aday bölüm kimliklerinden seç; yeni bölüm kimliği uydurma. "
    "Belge birden fazla bölüme aitse ikincil bölümleri de listele. "
    "Yanıtı yalnızca şu JSON ile ver: "
    '{"primary_section": "<id>", "secondary_sections": ["<id>"], '
    '"confidence": 0.0, "reason": "<kısa gerekçe>"}'
)


def arbitrate(
    evidence_text: str,
    candidates: list[dict[str, Any]],
    taxonomy: Taxonomy,
    config: Any,
) -> ArbiterResult:
    cfg = (config.classification or {}).get("llm_arbiter", {}) or {}
    model_cfg = (config.models or {}).get("llm", {}) or {}
    if not cfg.get("enabled", True):
        return ArbiterResult(NOT_RUN, reason="arbiter disabled in config")
    try:
        endpoint = os.getenv(str(model_cfg.get("endpoint_env") or "LLM_SERVER"),
                             str(model_cfg.get("default_endpoint") or ""))
        client = LocalChatClient(endpoint,
                                 timeout=float(cfg.get("timeout_seconds", 90)))
    except RemoteEndpointRejected:
        raise
    model = str(model_cfg.get("model") or "").strip()
    if not model or not client.has_model(model):
        return ArbiterResult(UNAVAILABLE, reason="configured local LLM model is unavailable")

    limit = int(cfg.get("max_candidate_sections", 8))
    shortlist = candidates[:limit]
    allowed = {str(c["id"]) for c in shortlist}
    lines = [f"- {c['id']}: {taxonomy.title_of(str(c['id'])) or ''} (skor {c['score']})"
             for c in shortlist]
    user = (
        f"ADAY BÖLÜMLER:\n" + "\n".join(lines) + "\n\n"
        + f"BELGE KANITI:\n{evidence_text[:8000]}"
    )
    try:
        payload = client.chat_json(model, SYSTEM_PROMPT, user)
    except RemoteEndpointRejected:
        raise
    except Exception as exc:
        return ArbiterResult(FAILED, reason=f"{type(exc).__name__}: {exc}", model=model)

    primary = str(payload.get("primary_section") or "").strip()
    if primary not in allowed or primary not in taxonomy:
        return ArbiterResult(REJECTED_INVALID_SECTION, model=model,
                             reason=f"arbiter returned {primary!r}, not in the candidate set")
    max_selected = int(cfg.get("max_selected_sections", 5))
    secondary = [str(s) for s in (payload.get("secondary_sections") or [])
                 if str(s) in taxonomy and str(s) != primary][: max_selected - 1]
    confidence = payload.get("confidence")
    try:
        confidence = max(0.0, min(1.0, float(confidence)))
    except (TypeError, ValueError):
        confidence = None
    return ArbiterResult(SUCCESS, primary_section=primary, secondary_sections=secondary,
                         confidence=confidence, reason=str(payload.get("reason") or "")[:400],
                         model=model)
