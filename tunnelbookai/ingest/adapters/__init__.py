"""Per-format extraction adapters (task §3).

Every adapter has the same shape:

    run(context: AdapterContext) -> ExtractionResult

`AdapterContext` carries everything an adapter may touch: the immutable original, the
processing bundle it may write into, resolved config, and the OCR / vision / office-renderer
providers. Adapters never write outside their bundle and never read the incoming inbox.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from ..config import IngestConfig
from ..extraction import ExtractionResult
from ..format_registry import Detection


@dataclass
class AdapterContext:
    document_id: str
    original_path: Path          # the immutable archive copy: originals/<id>/source.<ext>
    original_filename: str       # the name the file arrived with (NOT the archive name)
    bundle: Path
    detection: Detection
    config: IngestConfig
    ocr: Any = None
    vision: Any = None
    office_renderer: Any = None
    root: Path = field(default_factory=Path)
    do_ocr: bool = True
    do_vision: bool = True

    @property
    def display_name(self) -> str:
        """Human-facing document name: the incoming filename without its extension."""
        return Path(self.original_filename or self.original_path.name).stem

    @property
    def snapshot_scale(self) -> float:
        snap = self.config.ingest.get("snapshots", {}) or {}
        return float(snap.get("scale", self.config.docling_options.get("images_scale", 2.0)))

    @property
    def snapshots_enabled(self) -> bool:
        return bool((self.config.ingest.get("snapshots", {}) or {}).get("enabled", True))

    @property
    def tables_cfg(self) -> dict[str, Any]:
        return self.config.ingest.get("tables", {}) or {}


def get_adapter(name: str) -> Callable[[AdapterContext], ExtractionResult]:
    from . import docx as docx_adapter
    from . import image as image_adapter
    from . import pdf as pdf_adapter
    from . import pptx as pptx_adapter
    from . import text as text_adapter
    from . import xlsx as xlsx_adapter

    table = {
        "pdf": pdf_adapter.run,
        "docx": docx_adapter.run,
        "pptx": pptx_adapter.run,
        "xlsx": xlsx_adapter.run,
        "image": image_adapter.run,
        "text": text_adapter.run,
    }
    if name not in table:
        raise KeyError(f"no adapter registered for {name!r}")
    return table[name]
