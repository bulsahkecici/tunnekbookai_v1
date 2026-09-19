"""Common extraction result model shared by every format adapter (task §4, §5).

Every adapter in `tunnelbookai.ingest.adapters` returns an `ExtractionResult`. Assets are
plain JSON-shaped dicts built through the factories in `tunnelbookai.ingest.assets` so the
on-disk schemas in the task spec (§7, §8, §9, §16) are the single source of truth.

Normalized outputs are always written to:

    processing/<document_id>/normalized/
        document.json   -- structural authority
        document.md     -- retrieval / human-readable representation
        document.txt    -- plain-text fallback

The original is never touched (§5, original_archive.py).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .paths import relpath

NORMALIZED_DIRNAME = "normalized"


@dataclass
class ExtractionResult:
    document_id: str
    format: str
    adapter: str = ""
    normalized_markdown_path: str | None = None
    normalized_json_path: str | None = None
    normalized_text_path: str | None = None
    pages: list[dict[str, Any]] = field(default_factory=list)
    figures: list[dict[str, Any]] = field(default_factory=list)
    tables: list[dict[str, Any]] = field(default_factory=list)
    charts: list[dict[str, Any]] = field(default_factory=list)
    slides: list[dict[str, Any]] = field(default_factory=list)
    sheets: list[dict[str, Any]] = field(default_factory=list)
    ocr_items: list[dict[str, Any]] = field(default_factory=list)
    text_elements: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    capabilities: dict[str, bool] = field(default_factory=dict)
    engine: dict[str, Any] = field(default_factory=dict)
    page_count: int = 0
    text_char_count: int = 0
    text_repair: dict[str, Any] | None = None

    # ------------------------------------------------------------------ helpers
    def warn(self, code: str) -> None:
        if code not in self.warnings:
            self.warnings.append(code)

    def fail(self, code: str) -> None:
        if code not in self.errors:
            self.errors.append(code)

    @property
    def succeeded(self) -> bool:
        return not self.errors and self.normalized_json_path is not None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalized_dir(bundle: Path) -> Path:
    out = bundle / NORMALIZED_DIRNAME
    out.mkdir(parents=True, exist_ok=True)
    return out


def write_normalized(
    bundle: Path,
    result: ExtractionResult,
    *,
    markdown: str,
    document_json: dict[str, Any],
    text: str,
) -> None:
    """Write the three normalized representations and record their paths on `result`."""
    out = normalized_dir(bundle)
    md_path = out / "document.md"
    json_path = out / "document.json"
    txt_path = out / "document.txt"
    md_path.write_text(markdown or "", encoding="utf-8")
    json_path.write_text(
        json.dumps(document_json, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    txt_path.write_text(text or "", encoding="utf-8")
    result.normalized_markdown_path = relpath(md_path)
    result.normalized_json_path = relpath(json_path)
    result.normalized_text_path = relpath(txt_path)
    result.text_char_count = len((text or "").strip())


def write_extraction_report(bundle: Path, result: ExtractionResult) -> Path:
    path = bundle / "extraction_report.json"
    payload = result.to_dict()
    # asset bodies live in their own manifests; keep the report navigable
    payload["figures"] = [f.get("asset_id") for f in result.figures]
    payload["tables"] = [t.get("table_id") for t in result.tables]
    payload["pages"] = [p.get("asset_id") for p in result.pages]
    payload["text_elements"] = len(result.text_elements)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return path
