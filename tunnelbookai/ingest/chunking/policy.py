"""Chunk policy + stable chunk identity (task §61, §62)."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any

from . import tokenizer

TEXT_CHUNK = "TEXT_CHUNK"
TABLE_CHUNK = "TABLE_CHUNK"
FIGURE_CHUNK = "FIGURE_CHUNK"
OCR_CHUNK = "OCR_CHUNK"
SLIDE_CHUNK = "SLIDE_CHUNK"
SHEET_CHUNK = "SHEET_CHUNK"

CHUNK_TYPES = (TEXT_CHUNK, TABLE_CHUNK, FIGURE_CHUNK, OCR_CHUNK, SLIDE_CHUNK, SHEET_CHUNK)

_WS = re.compile(r"\s+")


@dataclass(frozen=True)
class ChunkPolicy:
    schema_version: str = "1.0"
    policy_version: str = "structure-aware-v1"
    tokenizer_name: str = tokenizer.TOKENIZER_NAME
    target_tokens: int = 850
    min_tokens: int = 250
    max_tokens: int = 1200
    hard_max_tokens: int = 1500
    overlap_tokens: int = 80
    embedding_min_tokens: int = 12
    enabled_types: frozenset[str] = frozenset(CHUNK_TYPES)
    dedup_enabled: bool = True
    dedup_shingle: int = 5
    dedup_threshold: float = 0.92
    prefer_native_over_ocr: bool = True
    skip_ocr_chunk_if_in_figure: bool = True
    max_rows_per_sheet_chunk: int = 60
    include_speaker_notes: bool = True
    figure_requires_content: bool = True

    @classmethod
    def from_config(cls, config: Any) -> "ChunkPolicy":
        cfg = getattr(config, "chunking", {}) or {}
        tokens_cfg = cfg.get("tokens", {}) or {}
        types_cfg = cfg.get("types", {}) or {}
        dedup_cfg = cfg.get("dedup", {}) or {}
        sheets_cfg = cfg.get("sheets", {}) or {}
        slides_cfg = cfg.get("slides", {}) or {}
        figures_cfg = cfg.get("figures", {}) or {}
        ocr_cfg = cfg.get("ocr", {}) or {}
        ready_cfg = cfg.get("embedding_ready", {}) or {}

        name_map = {
            "text": TEXT_CHUNK, "table": TABLE_CHUNK, "figure": FIGURE_CHUNK,
            "ocr": OCR_CHUNK, "slide": SLIDE_CHUNK, "sheet": SHEET_CHUNK,
        }
        enabled = frozenset(
            chunk_type for key, chunk_type in name_map.items() if types_cfg.get(key, True))

        return cls(
            schema_version=str(cfg.get("schema_version", "1.0")),
            policy_version=str(cfg.get("policy_version", "structure-aware-v1")),
            tokenizer_name=str(tokens_cfg.get("tokenizer", tokenizer.TOKENIZER_NAME)),
            target_tokens=int(tokens_cfg.get("target", 850)),
            min_tokens=int(tokens_cfg.get("min", 250)),
            max_tokens=int(tokens_cfg.get("max", 1200)),
            hard_max_tokens=int(tokens_cfg.get("hard_max", 1500)),
            overlap_tokens=int(tokens_cfg.get("overlap", 80)),
            embedding_min_tokens=int(ready_cfg.get("min_tokens", 12)),
            enabled_types=enabled,
            dedup_enabled=bool(dedup_cfg.get("enabled", True)),
            dedup_shingle=int(dedup_cfg.get("shingle_size", 5)),
            dedup_threshold=float(dedup_cfg.get("similarity_threshold", 0.92)),
            prefer_native_over_ocr=bool(dedup_cfg.get("prefer_native_text_over_ocr", True)),
            skip_ocr_chunk_if_in_figure=bool(ocr_cfg.get("skip_if_in_figure_chunk", True)),
            max_rows_per_sheet_chunk=int(sheets_cfg.get("max_rows_per_chunk", 60)),
            include_speaker_notes=bool(slides_cfg.get("include_speaker_notes", True)),
            figure_requires_content=bool(figures_cfg.get("require_content", True)),
        )

    def allows(self, chunk_type: str) -> bool:
        return chunk_type in self.enabled_types


def normalize_for_id(text: str) -> str:
    return _WS.sub(" ", (text or "").strip()).casefold()


def chunk_id(document_id: str, chunk_type: str, source_elements: list[str],
             text: str, policy: ChunkPolicy, identity_part: str | None = None) -> str:
    """Deterministic id from identity + type + source boundaries + policy + content (§61).

    A pure ordinal would silently reuse an id when the content changes; hashing the source
    element boundaries AND the normalized text means a changed chunk gets a changed id.
    """
    fields = [
        document_id,
        chunk_type,
        ",".join(source_elements),
        policy.policy_version,
        policy.schema_version,
    ]
    if identity_part is not None:
        fields.append(identity_part)
    fields.append(normalize_for_id(text))
    payload = "␟".join(fields)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{document_id}_CH_{digest[:10]}"
