"""Section evidence — which document elements support which section (task §40).

`section_evidence` links every selected section back to concrete element ids from the
extraction bundle (PARA0012, TABLE0003, FIG0008, ...). The refs are verifiable: the chunk
quality gate re-checks each one against `normalized/document.json` (§63).
"""

from __future__ import annotations

from typing import Any

from .rules import DocumentEvidence, normalize, score_sections
from .taxonomy import Taxonomy

MAX_ELEMENTS_PER_SECTION = 25


def collect(
    section_ids: list[str],
    elements: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    figures: list[dict[str, Any]],
    taxonomy: Taxonomy,
) -> list[dict[str, Any]]:
    """For each section, the elements whose text actually contains one of its terms."""
    out: list[dict[str, Any]] = []
    caption_by_asset = {t["table_id"]: (t.get("caption") or "") for t in tables}
    caption_by_asset.update({f["asset_id"]: (f.get("caption") or "") for f in figures})
    ocr_by_asset = {f["asset_id"]: (f.get("ocr_text") or "") for f in figures}

    for section_id in section_ids:
        section = taxonomy.get(section_id)
        if section is None:
            continue
        terms = [normalize(t) for t in (*section.strong_terms, *section.medium_terms)]
        title_term = normalize(section.title)
        supporting: list[str] = []
        for element in elements:
            haystack = normalize(element.get("text") or "")
            asset = element.get("asset_id")
            if asset:
                haystack += " " + normalize(caption_by_asset.get(asset, ""))
                haystack += " " + normalize(ocr_by_asset.get(asset, ""))
            if not haystack.strip():
                continue
            if any(term and term in haystack for term in terms) or (
                    len(title_term) > 6 and title_term in haystack):
                supporting.append(element.get("asset_id") or element["element_id"])
            if len(supporting) >= MAX_ELEMENTS_PER_SECTION:
                break
        out.append({
            "section_id": section_id,
            "section_title": section.title,
            "supporting_elements": supporting,
        })
    return out


def per_chunk_sections(chunk_texts: list[str], taxonomy: Taxonomy, *, top_k: int = 2
                       ) -> list[list[str]]:
    """Best sections per structural chunk — used for chunk-level votes (§37)."""
    out: list[list[str]] = []
    for text in chunk_texts:
        scores = score_sections(DocumentEvidence(body=text), taxonomy=taxonomy, max_sections=top_k)
        out.append([s.section_id for s in scores])
    return out
