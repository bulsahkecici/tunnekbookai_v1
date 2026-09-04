"""Config loading for the Unified Ingest Engine.

Loads config/{ingest,ocr,vision,metadata,classification,quality_gate}.yaml. PyYAML is a
declared dependency (shared/tunnelbookai-requirements.txt) and present in .venv; if it is
somehow missing we fail loudly rather than silently mis-parsing.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .paths import PATHS

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "PyYAML is required for the ingest engine. Activate .venv and "
        "`uv pip install -r shared/tunnelbookai-requirements.txt`."
    ) from exc

_CONFIG_NAMES = ("ingest", "ocr", "vision", "metadata", "classification", "quality_gate",
                 "chunking")


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping at the top level")
    return data


@dataclass(frozen=True)
class IngestConfig:
    ingest: dict[str, Any]
    ocr: dict[str, Any]
    vision: dict[str, Any]
    metadata: dict[str, Any]
    classification: dict[str, Any]
    quality_gate: dict[str, Any]
    chunking: dict[str, Any]

    @property
    def local_only(self) -> bool:
        return bool(self.ingest.get("local_only", True))

    @property
    def docling_options(self) -> dict[str, Any]:
        return dict(self.ingest.get("docling", {}))

    @property
    def supported_extensions(self) -> set[str]:
        fmt = self.ingest.get("formats", {})
        out: set[str] = set()
        for group in ("primary", "additional"):
            out.update(e.lower() for e in fmt.get(group, []))
        return out

    @property
    def legacy_extensions(self) -> set[str]:
        return {e.lower() for e in self.ingest.get("formats", {}).get("legacy", [])}

    @property
    def allowed_vision_hosts(self) -> set[str]:
        return set(self.vision.get("allowed_hosts", ["127.0.0.1", "localhost", "::1"]))


@lru_cache(maxsize=1)
def load_config() -> IngestConfig:
    loaded = {name: _load_yaml(PATHS.config_root / f"{name}.yaml") for name in _CONFIG_NAMES}
    return IngestConfig(**loaded)
