"""Input source adapters: manual inbox (§6) and PaperCrawler contract consumer (§5)."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DiscoveredInput:
    """One incoming file, before any processing."""
    input_path: Path
    source_kind: str                      # MANUAL_INTERNAL | EXTERNAL_DISCOVERY
    provenance: dict = field(default_factory=dict)
    crawler_record: dict | None = None    # full handoff manifest record, when source_kind is crawler
    notes: list[str] = field(default_factory=list)
