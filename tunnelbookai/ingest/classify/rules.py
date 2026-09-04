"""Deterministic rule scoring over the canonical taxonomy (task §34, §36).

The saturating score from `crawler/src/classification_engine.py:score_sections` is reused
verbatim in spirit — strong terms in the title count most, medium terms in the body least —
but the input is the FULL document evidence bundle (title, headings, body, table and figure
captions, OCR text, metadata), not a bibliographic record (§36).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from ..textfold import fold_turkish
from .taxonomy import Taxonomy, load_taxonomy


def normalize(value: Any) -> str:
    # Turkish fold BEFORE NFKD: without it "KAZI" folds to "kazi" while "kazı" stays
    # "kazı", so an ALL-CAPS Turkish heading never matches its lowercase taxonomy term
    # (§13). Same table as dedup.normalize_title — see tunnelbookai/ingest/textfold.py.
    text = unicodedata.normalize("NFKD", fold_turkish(str(value or ""))).casefold()
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text)


@dataclass
class DocumentEvidence:
    """Everything the final classifier is allowed to look at (§36)."""
    title: str = ""
    abstract: str = ""
    headings: list[str] = None
    body: str = ""
    table_captions: list[str] = None
    figure_captions: list[str] = None
    ocr_text: str = ""
    metadata_terms: list[str] = None
    crawler_provisional_section: str | None = None

    def __post_init__(self) -> None:
        self.headings = self.headings or []
        self.table_captions = self.table_captions or []
        self.figure_captions = self.figure_captions or []
        self.metadata_terms = self.metadata_terms or []

    @property
    def strong_blob(self) -> str:
        """Title + headings + captions — high-signal surfaces."""
        return normalize(" \n ".join(
            [self.title, *self.headings, *self.table_captions, *self.figure_captions,
             *self.metadata_terms]))

    @property
    def full_blob(self) -> str:
        return normalize(" \n ".join(
            [self.title, self.abstract, *self.headings, self.body,
             *self.table_captions, *self.figure_captions, self.ocr_text,
             *self.metadata_terms]))

    def embedding_text(self, limit: int = 12000) -> str:
        parts = [
            f"Title: {self.title}",
            f"Abstract: {self.abstract}",
            "Headings: " + "; ".join(self.headings[:40]),
            "Tables: " + "; ".join(self.table_captions[:20]),
            "Figures: " + "; ".join(self.figure_captions[:20]),
            f"Body: {self.body}",
        ]
        return "\n".join(parts)[:limit]


@dataclass
class RuleScore:
    section_id: str
    title: str
    score: float
    strong_matches: list[str]
    medium_matches: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.section_id, "title": self.title, "score": round(self.score, 4),
                "strong_matches": self.strong_matches, "medium_matches": self.medium_matches}


def score_sections(evidence: DocumentEvidence, *, taxonomy: Taxonomy | None = None,
                   max_sections: int = 8) -> list[RuleScore]:
    taxonomy = taxonomy or load_taxonomy()
    strong_blob = evidence.strong_blob
    full_blob = evidence.full_blob
    scored: list[RuleScore] = []

    for section in taxonomy.sections.values():
        if not section.active:
            continue
        strong = [t for t in section.strong_terms if normalize(t) in full_blob]
        medium = [t for t in section.medium_terms if normalize(t) in full_blob]
        title_hit = normalize(section.title) in strong_blob and len(section.title) > 6
        if not strong and not medium and not title_hit:
            continue
        raw = 0.0
        for term in strong:
            raw += 5.0 if normalize(term) in strong_blob else 3.0
        for term in medium:
            raw += 2.0 if normalize(term) in strong_blob else 1.0
        if title_hit:
            raw += 4.0
        scored.append(RuleScore(
            section_id=section.section_id, title=section.title,
            # saturating 0..1 score — interpretable without training data
            score=min(0.99, raw / (raw + 4.0)),
            strong_matches=[normalize(t) for t in strong],
            medium_matches=[normalize(t) for t in medium],
        ))
    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:max_sections]


def chunk_votes(chunk_texts: list[str], *, taxonomy: Taxonomy | None = None,
                top_k: int = 3) -> dict[str, float]:
    """Structural-chunk level votes (§37): each chunk votes for its own best sections."""
    taxonomy = taxonomy or load_taxonomy()
    votes: dict[str, float] = {}
    if not chunk_texts:
        return votes
    for text in chunk_texts:
        scores = score_sections(DocumentEvidence(body=text), taxonomy=taxonomy,
                                max_sections=top_k)
        for rank, score in enumerate(scores):
            # a chunk's first choice counts fully, later choices decay
            votes[score.section_id] = votes.get(score.section_id, 0.0) + score.score / (rank + 1)
    total = sum(votes.values()) or 1.0
    return {sid: round(value / total, 4) for sid, value in votes.items()}
