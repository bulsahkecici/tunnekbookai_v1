"""Canonical section taxonomy (task §35).

`book/scope/normalized/book_scope.json` is the SINGLE taxonomy. Nothing here creates
another one. `crawler/config/taxonomy.yaml` is loaded only as a *term dictionary* attached to
those same section ids — any id in it that is not in the canonical scope is ignored and
reported, never adopted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..paths import PROJECT_ROOT

DEFAULT_TAXONOMY = "book/scope/normalized/book_scope.json"
DEFAULT_TERMS = "crawler/config/taxonomy.yaml"


@dataclass(frozen=True)
class Section:
    section_id: str
    title: str
    parent_section: str | None
    level: int
    active: bool
    is_question_bank_section: bool
    strong_terms: tuple[str, ...] = ()
    medium_terms: tuple[str, ...] = ()

    @property
    def profile(self) -> str:
        """Text used to embed the section (mirrors crawler/src/hybrid_classifier.py)."""
        terms = [*self.strong_terms, *self.medium_terms]
        return f"{self.section_id} {self.title}. " + "; ".join(terms)


@dataclass(frozen=True)
class Taxonomy:
    sections: dict[str, Section]
    source_path: str
    unknown_term_sections: tuple[str, ...]

    def __contains__(self, section_id: object) -> bool:
        return str(section_id) in self.sections

    def get(self, section_id: str) -> Section | None:
        return self.sections.get(str(section_id))

    def title_of(self, section_id: str) -> str | None:
        section = self.get(section_id)
        return section.title if section else None

    def ancestors(self, section_id: str) -> list[str]:
        out: list[str] = []
        current = self.get(section_id)
        while current is not None and current.parent_section:
            out.append(current.parent_section)
            current = self.get(current.parent_section)
        return out

    @property
    def section_ids(self) -> list[str]:
        return list(self.sections)


def _load_terms(path: Path) -> dict[str, dict[str, list[str]]]:
    if not path.is_file():
        return {}
    try:
        import yaml
    except ImportError:  # pragma: no cover
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, list[str]]] = {}
    for section_id, cfg in (payload.get("sections") or {}).items():
        out[str(section_id)] = {
            "strong_terms": [str(t) for t in (cfg.get("strong_terms") or [])],
            "medium_terms": [str(t) for t in (cfg.get("medium_terms") or [])],
        }
    return out


@lru_cache(maxsize=4)
def load_taxonomy(taxonomy_path: str = DEFAULT_TAXONOMY,
                  terms_path: str = DEFAULT_TERMS) -> Taxonomy:
    scope_file = PROJECT_ROOT / taxonomy_path
    payload = json.loads(scope_file.read_text(encoding="utf-8"))
    terms = _load_terms(PROJECT_ROOT / terms_path)

    sections: dict[str, Section] = {}
    for row in payload.get("sections", []):
        section_id = str(row["section_id"])
        term_cfg = terms.get(section_id, {})
        sections[section_id] = Section(
            section_id=section_id,
            title=str(row.get("title") or section_id),
            parent_section=(str(row["parent_section"]) if row.get("parent_section") else None),
            level=int(row.get("level") or 1),
            active=bool(row.get("active", True)),
            is_question_bank_section=bool(row.get("is_question_bank_section", False)),
            strong_terms=tuple(term_cfg.get("strong_terms", [])),
            medium_terms=tuple(term_cfg.get("medium_terms", [])),
        )
    unknown = tuple(sorted(set(terms) - set(sections)))
    return Taxonomy(sections=sections, source_path=taxonomy_path, unknown_term_sections=unknown)


def is_valid_section(section_id: Any, taxonomy: Taxonomy | None = None) -> bool:
    taxonomy = taxonomy or load_taxonomy()
    return bool(section_id) and str(section_id) in taxonomy
