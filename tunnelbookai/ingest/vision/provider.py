"""Local vision / VLM provider (task §26, §27, §80).

Three providers, selected by `config/vision.yaml`:

    DisabledVisionProvider              default; every asset -> NOT_RUN
    LocalOpenAICompatibleVisionProvider  loopback OpenAI-compatible VLM (LM Studio / llama.cpp)
    DoclingLocalVisionProvider           Docling's in-process local VLM description

Security invariant: any endpoint whose host is not 127.0.0.1 / localhost / ::1 raises
`RemoteEndpointRejected`. There is no configuration path that permits a remote host (§26).

Output contract per asset:

    {"visual_description_status", "visual_description", "provider", "model"}

`visual_description` is NEVER derived from OCR text (§24) and is never fabricated: when no
VLM is reachable the status is NOT_RUN and the description stays null (§27).
"""

from __future__ import annotations

import base64
import ipaddress
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SUCCESS = "SUCCESS"
NOT_RUN = "NOT_RUN"
FAILED = "FAILED"
DISABLED = "DISABLED"

LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class RemoteEndpointRejected(RuntimeError):
    """Raised for any non-loopback AI endpoint. Never caught into a silent fallback."""


def assert_loopback(url: str, *, allowed_hosts: set[str] | None = None) -> str:
    hosts = set(allowed_hosts or LOOPBACK_HOSTS)
    parsed = urlparse(str(url or "").strip())
    host = (parsed.hostname or "").lower()
    if not host:
        raise RemoteEndpointRejected(f"REMOTE_ENDPOINT_REJECTED: no host in {url!r}")
    if host in hosts:
        return str(url).rstrip("/")
    try:
        if ipaddress.ip_address(host).is_loopback:
            return str(url).rstrip("/")
    except ValueError:
        pass
    raise RemoteEndpointRejected(f"REMOTE_ENDPOINT_REJECTED: {host}")


def empty_result(status: str = NOT_RUN, provider: str | None = None,
                 model: str | None = None) -> dict[str, Any]:
    return {
        "visual_description_status": status,
        "visual_description": None,
        "provider": provider,
        "model": model,
    }


class VisionProvider:
    name = "base"

    def available(self) -> bool:
        return False

    def describe(self, image_path: Path, *, context: str | None = None) -> dict[str, Any]:
        return empty_result(NOT_RUN, self.name)


class DisabledVisionProvider(VisionProvider):
    name = "disabled"

    def describe(self, image_path: Path, *, context: str | None = None) -> dict[str, Any]:
        return empty_result(DISABLED, self.name)


class LocalOpenAICompatibleVisionProvider(VisionProvider):
    name = "local_openai_compatible"

    PROMPT = (
        "Bu teknik görselin ne gösterdiğini tek bir kısa cümleyle betimle. "
        "Görselde okunan yazıları kopyalama, sadece görsel içeriği tanımla. "
        "Emin değilsen 'BELIRSIZ' yaz."
    )

    def __init__(self, base_url: str, *, model: str | None = None, timeout: float = 120.0,
                 allowed_hosts: set[str] | None = None) -> None:
        self.base_url = assert_loopback(base_url, allowed_hosts=allowed_hosts)
        self.model = model
        self.timeout = timeout
        self._checked = False
        self._ok = False

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = assert_loopback(f"{self.base_url}{path}")
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _models(self) -> list[str]:
        url = assert_loopback(f"{self.base_url}/models")
        with urllib.request.urlopen(url, timeout=min(self.timeout, 15)) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return [str(m.get("id")) for m in payload.get("data", []) if m.get("id")]

    def available(self) -> bool:
        if self._checked:
            return self._ok
        self._checked = True
        try:
            models = self._models()
        except (urllib.error.URLError, OSError, ValueError):
            self._ok = False
            return False
        if self.model is None:
            preferred = [m for m in models
                         if any(t in m.lower() for t in ("vl", "vision", "llava", "smolvlm", "gemma3"))]
            self.model = (preferred or models or [None])[0]
        self._ok = self.model is not None
        return self._ok

    def describe(self, image_path: Path, *, context: str | None = None) -> dict[str, Any]:
        if not self.available():
            return empty_result(NOT_RUN, self.name, self.model)
        try:
            data = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
        except OSError:
            return empty_result(FAILED, self.name, self.model)
        suffix = Path(image_path).suffix.lower().lstrip(".") or "png"
        mime = "image/jpeg" if suffix in {"jpg", "jpeg"} else f"image/{suffix}"
        prompt = self.PROMPT if not context else f"{self.PROMPT}\nBağlam: {context[:400]}"
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}},
                ],
            }],
        }
        try:
            response = self._post("/chat/completions", payload)
            text = (response["choices"][0]["message"]["content"] or "").strip()
        except RemoteEndpointRejected:
            raise
        except Exception:
            return empty_result(FAILED, self.name, self.model)
        if not text or text.strip().upper().startswith("BELIRSIZ"):
            return empty_result(NOT_RUN, self.name, self.model)
        result = empty_result(SUCCESS, self.name, self.model)
        result["visual_description"] = text
        return result


class DoclingLocalVisionProvider(VisionProvider):
    """Docling's in-process picture description (SmolVLM / Granite Vision).

    Descriptions are produced during conversion, so this provider only reads the annotations
    a conversion already attached; it never calls out anywhere.
    """

    name = "docling_local"

    def __init__(self, model: str = "smolvlm") -> None:
        self.model = model

    def available(self) -> bool:
        try:
            from docling.datamodel.pipeline_options import PdfPipelineOptions
        except ImportError:
            return False
        return hasattr(PdfPipelineOptions(), "do_picture_description")

    def describe_from_annotations(self, picture: Any) -> dict[str, Any]:
        for annotation in getattr(picture, "annotations", None) or []:
            if str(getattr(annotation, "kind", "")).lower() == "description":
                text = str(getattr(annotation, "text", "") or "").strip()
                if text:
                    result = empty_result(SUCCESS, self.name, self.model)
                    result["visual_description"] = text
                    return result
        return empty_result(NOT_RUN, self.name, self.model)

    def describe(self, image_path: Path, *, context: str | None = None) -> dict[str, Any]:
        return empty_result(NOT_RUN, self.name, self.model)


def build_provider(config: Any, *, enabled: bool = True) -> VisionProvider:
    """Resolve the configured provider. Rejects any non-loopback endpoint outright (§26)."""
    cfg = getattr(config, "vision", {}) or {}
    if not enabled:
        return DisabledVisionProvider()
    if bool(cfg.get("remote_allowed", False)):
        raise RemoteEndpointRejected("REMOTE_ENDPOINT_REJECTED: vision.remote_allowed must be false")

    setting = cfg.get("enabled", "auto")
    if setting is False or str(setting).lower() == "false":
        return DisabledVisionProvider()

    allowed = set(cfg.get("allowed_hosts", sorted(LOOPBACK_HOSTS)))
    if not allowed <= LOOPBACK_HOSTS:
        raise RemoteEndpointRejected(
            f"REMOTE_ENDPOINT_REJECTED: vision.allowed_hosts contains non-loopback {sorted(allowed - LOOPBACK_HOSTS)}"
        )

    provider = str(cfg.get("provider", "disabled")).lower()
    auto = str(setting).lower() == "auto"

    if provider == "local_openai_compatible" or auto:
        local = cfg.get("local_openai_compatible", {}) or {}
        base_url = local.get("base_url", "http://127.0.0.1:1234/v1")
        candidate = LocalOpenAICompatibleVisionProvider(
            base_url, model=local.get("model"),
            timeout=float(local.get("timeout_seconds", 120)), allowed_hosts=allowed,
        )
        if provider == "local_openai_compatible" or candidate.available():
            return candidate
    if provider == "docling_local":
        return DoclingLocalVisionProvider(str((cfg.get("docling_local") or {}).get("model", "smolvlm")))
    return DisabledVisionProvider()


def describe_figures(provider: VisionProvider, figures: list[dict[str, Any]],
                     root: Path) -> list[str]:
    """Attach visual descriptions in place. Leaves OCR fields untouched (§24)."""
    warnings: list[str] = []
    if isinstance(provider, DisabledVisionProvider) or not provider.available():
        for figure in figures:
            figure.setdefault("visual_description_status", NOT_RUN)
            figure.setdefault("visual_description", None)
        if figures:
            warnings.append("VISION_NOT_RUN")
        return warnings
    cache: dict[str, dict[str, Any]] = getattr(provider, "_figure_result_cache", {})
    provider._figure_result_cache = cache
    for figure in figures:
        rel = figure.get("path")
        if not rel:
            continue
        path = root / rel if not Path(rel).is_absolute() else Path(rel)
        if not path.is_file():
            continue
        width = int(figure.get("width") or 0)
        height = int(figure.get("height") or 0)
        too_small = bool(width and height and (min(width, height) < 24 or width * height < 4096))
        digest = str(figure.get("pixel_digest") or "")
        cached = cache.get(digest) if digest else None
        result = (
            empty_result(NOT_RUN, provider.name, getattr(provider, "model", None))
            if too_small
            else dict(cached) if cached is not None
            else provider.describe(path, context=figure.get("caption"))
        )
        cache_hit = cached is not None
        if digest and not cache_hit and result.get("visual_description_status") in {
            SUCCESS, NOT_RUN,
        }:
            cache[digest] = dict(result)
        figure["visual_description_status"] = result["visual_description_status"]
        figure["visual_description"] = result["visual_description"]
        figure["vision_provider"] = result["provider"]
        figure["vision_model"] = result["model"]
        figure["vision_cache_hit"] = cache_hit
        figure["vision_skip_reason"] = "TOO_SMALL" if too_small else None
    return warnings
