"""Book Citation Renderer v1.

Everything upstream of this module addresses sources by packet-local handles - [E001], [E004] -
which are positions in a retrieval packet, not identities. Two packets built for two questions put
different documents at [E001]. Rendering one into a book would produce a reference that is stable
only for as long as nobody runs retrieval again.

So the renderer's first job is a translation: source_key -> reference number, where the source key
is the stable identity from the frozen registry and the number is local to this section. Its
second job is harder and matters more:

    **It may print only metadata that exists.**

A bibliography is a claim about the world. "KGM Teknik Şartnamesi 2013, s. 226-250" is a claim
that can be checked. "KGM Teknik Şartnamesi 2013, Karayolları Genel Müdürlüğü, Ankara, 2013,
s. 231" is four claims, three of which this project cannot support - and the fabricated ones are
the ones that make the citation look authoritative. A model asked to "format a reference" will
supply a publisher and a page, because that is what references look like. This module never asks.
It reads the registry row and prints its fields; a null is an omission, never a guess.

The page ranges in the registry are 25-page buckets, which is coarse. It is rendered as the range
it is - 's. 226-250' - rather than narrowed to a single page. A range is honest about its own
precision; 's. 231' would not be, and would be indistinguishable from real page-level provenance
in the reference list.

Determinism is a requirement rather than a nicety (§118): numbering follows first appearance in
accepted prose, sources dedupe by key, multi-source citations render in ascending numeric order,
and nothing in the output carries a timestamp. Byte-identical DraftIR renders byte-identical
Markdown, which is what makes a rendered draft reviewable as a diff.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

RENDERER_VERSION = "tunnelbook-book-citation-renderer-v1"
CITATION_CONTRACT_VERSION = "tunnelbook-book-citation-rendering-contract-v1"
SECTION_ID = "SEC-02-2"

CITATION_CONTRACT_PATH = (ROOT / "data" / "book" / "drafting" / "contracts"
                          / "book_citation_rendering_contract_v1.json")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


draft_validator = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")

REFERENCES_HEADING = "Kaynaklar"
PACKET_EID_RE = draft_validator.PACKET_EID_RE
SOURCE_KEY_RE = draft_validator.SOURCE_KEY_RE
CLAIM_ID_RE = draft_validator.CLAIM_ID_RE


class RenderRefused(ValueError):
    """The renderer will not emit a reference it cannot back. There is no fallback rendering."""


# ================================================================ 1. reference formatting

def _page_location(row: dict) -> str | None:
    """Whatever positional provenance the registry actually holds, in its own precision.

    A start with no end renders as a single page because that is what the registry asserts; a
    range renders as a range. Neither is narrowed, and absence renders as nothing at all.
    """
    start, end = row.get("page_start"), row.get("page_end")
    if start is not None:
        return f"s. {start}" if end is None or end == start else f"s. {start}-{end}"
    start, end = row.get("slide_start"), row.get("slide_end")
    if start is not None:
        return f"slayt {start}" if end is None or end == start else f"slayt {start}-{end}"
    return None


def format_reference(row: dict) -> str:
    """Render one registry row. Every component is a field that is present and non-null.

    No author, no publisher, no year, no edition, no URL, no standard number: the registry holds
    none of them for this corpus, and the whole point of this function is that a field it does not
    have does not appear.
    """
    title = (row.get("title") or "").strip()
    if not title:
        raise RenderRefused(
            f"{row.get('source_key')} has no title in the registry; there is no honest way to "
            f"render a reference for it and inventing one is forbidden")
    parts = [title]
    section_path = (row.get("section_path") or "").strip()
    if section_path:
        parts.append(section_path)
    location = _page_location(row)
    if location:
        parts.append(location)
    return ", ".join(parts)


# ================================================================ 2. citation map

@dataclass
class CitationEntry:
    rendered_number: int
    source_key: str
    document_id: str
    known_title: str
    known_location: str | None
    provenance: dict[str, Any]
    first_unit_id: str
    claim_ids: list[str]
    rendered_reference: str


def build_citation_map(units: Iterable[Any], registry: dict[str, dict]) -> list[CitationEntry]:
    """Number sources by first appearance in accepted prose, deduplicated by source key.

    First appearance rather than lexical order (§130): a reader following [1] expects the first
    reference they met, and sorting by key would make the numbering an artifact of a hash.
    """
    order: list[str] = []
    first_unit: dict[str, str] = {}
    claims: dict[str, list[str]] = {}
    for unit in units:
        if not getattr(unit, "material", False):
            continue
        for intent in unit.citation_intents:
            for key in intent.get("source_keys", []):
                if key not in first_unit:
                    order.append(key)
                    first_unit[key] = unit.unit_id
                bucket = claims.setdefault(key, [])
                if intent["claim_id"] not in bucket:
                    bucket.append(intent["claim_id"])

    entries: list[CitationEntry] = []
    for number, key in enumerate(order, start=1):
        row = registry.get(key)
        if row is None:
            raise RenderRefused(
                f"{key} resolves against no frozen registry; the renderer will not emit a "
                f"reference for an unknown source")
        entries.append(CitationEntry(
            rendered_number=number, source_key=key, document_id=row.get("document_id") or "",
            known_title=(row.get("title") or "").strip(), known_location=_page_location(row),
            provenance={"citation_mode": row.get("citation_mode"),
                        "provenance_status": row.get("provenance_status"),
                        "language": row.get("language"),
                        "section_path": row.get("section_path"),
                        "page_start": row.get("page_start"), "page_end": row.get("page_end"),
                        "slide_start": row.get("slide_start"), "slide_end": row.get("slide_end"),
                        "authority_level": row.get("authority_level")},
            first_unit_id=first_unit[key], claim_ids=list(claims.get(key, [])),
            rendered_reference=format_reference(row)))
    return entries


def marker_for(unit: Any, numbering: dict[str, int]) -> str:
    """[1] for one source, [2,3] for several - ascending, deduplicated, deterministic."""
    numbers = sorted({numbering[key] for intent in unit.citation_intents
                      for key in intent.get("source_keys", []) if key in numbering})
    return f"[{','.join(str(n) for n in numbers)}]" if numbers else ""


# ================================================================ 3. markdown rendering

def layout(ir: Any) -> list[str]:
    """Lay units out as Markdown, rebuilding paragraphs from unit ids.

    One DraftIR unit is one sentence, so a paragraph has to be reassembled: units sharing a
    paragraph id join with a space, and a change of paragraph id opens a new block. Each unit
    carries its own marker by this point, which is what stops reflow from moving a citation away
    from the proposition it supports.
    """
    lines: list[str] = [f"# {ir.title}", ""]
    buffer: list[str] = []
    current: str | None = None

    def flush() -> None:
        nonlocal buffer, current
        if buffer:
            lines.extend([" ".join(buffer), ""])
            buffer = []
        current = None

    for unit in ir.units:
        text = unit.text.strip()
        marker = getattr(unit, "rendered_marker", "")
        piece = f"{text}{marker}"
        if unit.unit_type == "HEADING":
            flush()
            lines.extend([f"## {text}", ""])
            continue
        if unit.unit_type == "LIST_ITEM":
            flush()
            lines.append(f"- {piece}")
            continue
        if unit.unit_type == "TABLE_CELL":
            flush()
            lines.append(f"| {piece} |")
            continue
        if current is not None and unit.paragraph_id != current:
            flush()
        current = unit.paragraph_id
        buffer.append(piece)
    flush()
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def render(ir: Any, registry: dict[str, dict]) -> tuple[str, list[CitationEntry]]:
    """Render accepted DraftIR to Markdown plus its citation map.

    Markers are attached to the units before layout so paragraph reflow cannot separate a citation
    from the proposition it supports.
    """
    entries = build_citation_map(ir.units, registry)
    numbering = {entry.source_key: entry.rendered_number for entry in entries}
    for unit in ir.units:
        unit.rendered_marker = marker_for(unit, numbering) if unit.material else ""

    lines = layout(ir)
    lines += ["", f"## {REFERENCES_HEADING}", ""]
    for entry in entries:
        lines.append(f"{entry.rendered_number}. {entry.rendered_reference}")
    markdown = "\n".join(lines).rstrip() + "\n"

    audit = audit_rendered(markdown, entries)
    if audit["failures"]:
        raise RenderRefused(f"rendered output failed its own audit: {audit['failures']}")
    return markdown, entries


# ================================================================ 4. rendered-output audit

def audit_rendered(markdown: str, entries: list[CitationEntry]) -> dict[str, Any]:
    """What the rendered page must never contain, checked on the bytes that would be published."""
    prose = markdown.split(f"## {REFERENCES_HEADING}")[0]
    failures: list[str] = []

    eid_leaks = PACKET_EID_RE.findall(markdown)
    if eid_leaks:
        failures.append(f"packet-local evidence handles in rendered output: {eid_leaks}")
    key_leaks = SOURCE_KEY_RE.findall(markdown)
    if key_leaks:
        failures.append(f"stable source keys leaked into rendered output: {sorted(set(key_leaks))}")
    claim_leaks = CLAIM_ID_RE.findall(prose)
    if claim_leaks:
        failures.append(f"internal claim ids in visible prose: {sorted(set(claim_leaks))}")

    numbers = [entry.rendered_number for entry in entries]
    if numbers != list(range(1, len(numbers) + 1)):
        failures.append(f"reference numbering is not contiguous from 1: {numbers}")
    if len({entry.source_key for entry in entries}) != len(entries):
        failures.append("the same source key was assigned more than one reference number")

    cited = {int(n) for marker in re.findall(r"\[(\d+(?:,\d+)*)\]", prose)
             for n in marker.split(",")}
    unknown = sorted(cited - set(numbers))
    if unknown:
        failures.append(f"prose cites reference numbers with no bibliography entry: {unknown}")

    # These end in punctuation, so they cannot be closed with \b - a trailing word boundary after
    # '?' or '.' never matches, and the guard would silently pass everything it was meant to catch.
    for pattern, label in ((r"(?<![a-zçğıöşü])s\.\s*\?", "placeholder page"),
                           (r"(?<![a-zçğıöşü])n\.d\.", "fabricated 'no date' marker"),
                           (r"(?<![a-zçğıöşü])(?:yayınevi|publisher|ed\.)(?![a-zçğıöşü])",
                            "invented publication metadata")):
        if re.search(pattern, markdown, re.IGNORECASE):
            failures.append(f"rendered output contains a {label}")

    return {"failures": failures, "eid_leaks": len(eid_leaks),
            "source_key_leaks": len(set(key_leaks)), "claim_id_leaks": len(set(claim_leaks)),
            "references": len(entries), "cited_numbers": sorted(cited),
            "uncited_references": sorted(set(numbers) - cited)}


# ================================================================ 5. fixture harness

def run_fixtures(fixtures: list[dict]) -> dict[str, Any]:
    """Citation fixtures work on registry rows and synthetic units, never on retrieval.

    Each case declares either an expected rendering, an expected refusal, or an expected absence -
    the last being the one that matters most: a field the registry lacks must not appear anywhere
    in the output.
    """
    rows, failed = [], []
    for fixture in fixtures:
        case_id = fixture["case_id"]
        outcome, detail = "PASS", ""
        try:
            registry = {row["source_key"]: row for row in fixture.get("registry", [])}
            units = [_fixture_unit(u) for u in fixture.get("units", [])]
            if fixture.get("mode") == "reference":
                actual = format_reference(fixture["row"])
                if actual != fixture["expected_reference"]:
                    outcome, detail = "FAIL", f"{actual!r} != {fixture['expected_reference']!r}"
            elif fixture.get("mode") == "refuse":
                try:
                    if "row" in fixture:
                        format_reference(fixture["row"])
                    else:
                        build_citation_map(units, registry)
                    outcome, detail = "FAIL", "expected RenderRefused, none raised"
                except RenderRefused:
                    pass
            elif fixture.get("mode") == "numbering":
                entries = build_citation_map(units, registry)
                actual = [[e.rendered_number, e.source_key] for e in entries]
                expected = [list(pair) for pair in fixture["expected_numbering"]]
                if actual != expected:
                    outcome, detail = "FAIL", f"{actual} != {expected}"
            elif fixture.get("mode") == "marker":
                entries = build_citation_map(units, registry)
                numbering = {e.source_key: e.rendered_number for e in entries}
                actual = marker_for(units[fixture.get("marker_unit", 0)], numbering)
                if actual != fixture["expected_marker"]:
                    outcome, detail = "FAIL", f"{actual!r} != {fixture['expected_marker']!r}"
            elif fixture.get("mode") == "absent":
                entries = build_citation_map(units, registry)
                rendered = " | ".join(e.rendered_reference for e in entries)
                present = [needle for needle in fixture["forbidden_substrings"]
                           if needle.lower() in rendered.lower()]
                if present:
                    outcome, detail = "FAIL", f"forbidden metadata rendered: {present}"
            elif fixture.get("mode") == "audit":
                entries = build_citation_map(units, registry)
                result = audit_rendered(fixture["markdown"], entries)
                clean = not result["failures"]
                if clean != fixture["expected_clean"]:
                    outcome, detail = "FAIL", f"audit failures {result['failures']}"
            else:
                outcome, detail = "FAIL", f"unknown fixture mode {fixture.get('mode')!r}"
        except RenderRefused as error:
            if fixture.get("mode") != "refuse":
                outcome, detail = "FAIL", f"unexpected refusal: {error}"
        except Exception as error:                                  # noqa: BLE001
            outcome, detail = "FAIL", f"{type(error).__name__}: {error}"
        if outcome == "FAIL":
            failed.append(case_id)
        rows.append({"case_id": case_id, "mode": fixture.get("mode"), "outcome": outcome,
                     "detail": detail})
    return {"total": len(rows), "passed": len(rows) - len(failed), "failed": failed,
            "rows": rows, "all_pass": not failed}


def _fixture_unit(payload: dict) -> Any:
    return draft_validator.DraftUnit(
        unit_id=payload.get("unit_id", "U-X-P01-S01"),
        unit_type=payload.get("unit_type", "PARAGRAPH_SENTENCE"),
        text=payload.get("text", "x"), material=payload.get("material", True),
        claim_ids=list(payload.get("claim_ids", [])),
        source_keys=list(payload.get("source_keys", [])),
        citation_intents=list(payload.get("citation_intents", [])))


if __name__ == "__main__":
    print(f"{RENDERER_VERSION}\nThis module is a library. Run "
          f"scripts/47_section_drafting_contract_v1.py to render an accepted DraftIR.")
