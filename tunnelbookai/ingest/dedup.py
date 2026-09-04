"""Global deduplication (task §32, §77).

Priority ladder — the first rule that fires decides identity:

    1. SHA256                      exact bytes           EXACT
    2. DOI                         normalized            EXACT
    3. canonical / resolved URL    normalized            EXACT
    4. normalized exact title      + same year           STRONG
    5. fuzzy title + year + author/organization          PROBABLE (never auto-merged)

Rules 1-3 merge documents outright: one document identity, many provenance sources — the
same bytes arriving from the crawler AND the manual inbox stay ONE document with TWO sources
(§32, §77). Rule 4 merges only with a matching year. Rule 5 never merges on its own; it
raises a `DUPLICATE_CANDIDATE` for review, because a title collision is not proof.

The ledger lives in `audit/source_registry.jsonl`, one row per document identity.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from .textfold import fold_turkish

EXACT = "EXACT"
STRONG = "STRONG"
PROBABLE = "PROBABLE"

FUZZY_TITLE_THRESHOLD = 0.92
_TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
                    "fbclid", "gclid", "ref", "src"}


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    # Turkish fold BEFORE NFKD — see tunnelbookai/ingest/textfold.py for why.
    text = fold_turkish(value)
    text = unicodedata.normalize("NFKD", text).casefold()
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^0-9a-z\s]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    text = str(value).strip().casefold()
    text = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", text)
    return text.removeprefix("doi:").strip().rstrip(".")


def normalize_url(value: str | None) -> str:
    if not value:
        return ""
    try:
        parts = urlsplit(str(value).strip())
    except ValueError:
        return ""
    if not parts.netloc:
        return ""
    netloc = parts.netloc.casefold().removeprefix("www.")
    query = "&".join(sorted(
        piece for piece in parts.query.split("&")
        if piece and piece.split("=", 1)[0].casefold() not in _TRACKING_PARAMS
    ))
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.casefold() or "https", netloc, path, query, ""))


def _year(value: Any) -> str:
    match = re.search(r"(?:19|20)\d{2}", str(value or ""))
    return match.group(0) if match else ""


@dataclass
class DedupKey:
    document_id: str
    sha256: str
    doi: str = ""
    url: str = ""
    title: str = ""
    year: str = ""
    organization: str = ""
    authors: tuple[str, ...] = ()
    # A title that is only the filename is NOT evidence of identity — two unrelated files can
    # both be called "rapor.pdf". Such a title never drives a title-based merge.
    title_is_weak: bool = False

    @classmethod
    def from_metadata(cls, metadata: dict[str, Any]) -> "DedupKey":
        return cls(
            document_id=metadata["document_id"],
            sha256=(metadata.get("original_sha256") or "").lower(),
            doi=normalize_doi(metadata.get("doi")),
            url=normalize_url(metadata.get("source_url")),
            title=normalize_title(metadata.get("title")),
            year=_year(metadata.get("document_date")),
            organization=normalize_title(metadata.get("organization")),
            authors=tuple(normalize_title(a) for a in (metadata.get("authors") or [])),
            title_is_weak=bool(metadata.get("title_inferred_from_filename")),
        )


@dataclass
class DedupMatch:
    document_id: str
    rule: str
    strength: str
    detail: str


@dataclass
class SourceRegistry:
    """One row per document identity; provenance sources accumulate onto the row."""

    path: Path
    rows: dict[str, dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.path.is_file():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    self.rows[row["document_id"]] = row

    # ------------------------------------------------------------------ lookup
    def find(self, key: DedupKey) -> DedupMatch | None:
        for document_id, row in self.rows.items():
            if document_id == key.document_id:
                continue
            if key.sha256 and row.get("sha256", "").lower() == key.sha256:
                return DedupMatch(document_id, "sha256", EXACT, key.sha256[:16])
        for document_id, row in self.rows.items():
            if document_id == key.document_id:
                continue
            if key.doi and normalize_doi(row.get("doi")) == key.doi:
                return DedupMatch(document_id, "doi", EXACT, key.doi)
        for document_id, row in self.rows.items():
            if document_id == key.document_id:
                continue
            if key.url and normalize_url(row.get("url")) == key.url:
                return DedupMatch(document_id, "url", EXACT, key.url)
        for document_id, row in self.rows.items():
            if document_id == key.document_id or not key.title or key.title_is_weak:
                continue
            if row.get("title_is_weak"):
                continue
            if normalize_title(row.get("title")) == key.title:
                if key.year and _year(row.get("year")) and key.year != _year(row.get("year")):
                    continue
                return DedupMatch(document_id, "normalized_title", STRONG, key.title[:60])
        for document_id, row in self.rows.items():
            if (document_id == key.document_id or not key.title or not key.year
                    or key.title_is_weak or row.get("title_is_weak")):
                continue
            other_title = normalize_title(row.get("title"))
            if not other_title or _year(row.get("year")) != key.year:
                continue
            ratio = SequenceMatcher(None, key.title, other_title).ratio()
            if ratio < FUZZY_TITLE_THRESHOLD:
                continue
            shared_author = bool(set(key.authors) & set(row.get("authors") or []))
            same_org = bool(key.organization and key.organization == normalize_title(row.get("organization")))
            if shared_author or same_org:
                return DedupMatch(document_id, "fuzzy_title_year_author", PROBABLE,
                                  f"ratio={ratio:.3f}")
        return None

    # ------------------------------------------------------------------ writes
    def register(self, key: DedupKey, *, source_kinds: list[str], state: str,
                 provenance_sources: list[dict[str, Any]] | None = None,
                 duplicate_of: str | None = None,
                 duplicate_rule: str | None = None) -> dict[str, Any]:
        row = self.rows.setdefault(key.document_id, {"document_id": key.document_id})
        row.update({
            "sha256": key.sha256,
            "doi": key.doi or None,
            "url": key.url or None,
            "title": key.title or None,
            "year": key.year or None,
            "organization": key.organization or None,
            "authors": list(key.authors),
            "title_is_weak": key.title_is_weak,
            "state": state,
        })
        kinds = set(row.get("source_kinds") or []) | set(source_kinds)
        row["source_kinds"] = sorted(k for k in kinds if k)
        if provenance_sources is not None:
            existing = row.setdefault("provenance_sources", [])
            for source in provenance_sources:
                if source not in existing:
                    existing.append(source)
        row["provenance_source_count"] = len(row.get("provenance_sources") or []) or len(row["source_kinds"])
        if duplicate_of:
            row["duplicate_of"] = duplicate_of
            row["duplicate_rule"] = duplicate_rule
        return row

    def flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            for row in self.rows.values():
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        tmp.replace(self.path)


def resolve(registry: SourceRegistry, metadata: dict[str, Any], *,
            source_kinds: list[str], state: str,
            provenance_sources: list[dict[str, Any]] | None = None
            ) -> tuple[DedupMatch | None, list[str]]:
    """Register `metadata` and report any duplicate. Returns (match, warnings)."""
    key = DedupKey.from_metadata(metadata)
    match = registry.find(key)
    warnings: list[str] = []
    duplicate_of = duplicate_rule = None
    if match is not None:
        if match.strength == PROBABLE:
            warnings.append(f"DUPLICATE_CANDIDATE:{match.rule}:{match.document_id}")
        else:
            duplicate_of, duplicate_rule = match.document_id, match.rule
            warnings.append(f"DUPLICATE_{match.strength}:{match.rule}:{match.document_id}")
    registry.register(key, source_kinds=source_kinds, state=state,
                      provenance_sources=provenance_sources,
                      duplicate_of=duplicate_of, duplicate_rule=duplicate_rule)
    return match, warnings
