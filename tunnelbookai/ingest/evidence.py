"""TunnelBookAI final evidence model (task §42).

This is the ingest engine's OWN evidence level. PaperCrawler's crawler-side evidence is a
discovery-time signal about a *link*; it is never reused as the final evidence about a
*document* (stop condition §90).

    FULL_TEXT             a real, continuous text layer carries the document
    STRUCTURED_DOCUMENT   structure (headings/slides) carries it, text is present but thinner
    STRUCTURED_TABULAR    a workbook: the authority is the cell/formula model
    IMAGE_OCR             the text exists only because OCR produced it
    VISUAL_ONLY           a valid visual asset with no recoverable text
    PARTIAL               extraction succeeded but lost part of the document
    UNUSABLE              nothing dependable came out
"""

from __future__ import annotations

from typing import Any

FULL_TEXT = "FULL_TEXT"
STRUCTURED_DOCUMENT = "STRUCTURED_DOCUMENT"
STRUCTURED_TABULAR = "STRUCTURED_TABULAR"
IMAGE_OCR = "IMAGE_OCR"
VISUAL_ONLY = "VISUAL_ONLY"
PARTIAL = "PARTIAL"
UNUSABLE = "UNUSABLE"

LEVELS = (FULL_TEXT, STRUCTURED_DOCUMENT, STRUCTURED_TABULAR, IMAGE_OCR, VISUAL_ONLY,
          PARTIAL, UNUSABLE)

# a document needs at least this much native text per page to count as FULL_TEXT
MIN_CHARS_PER_PAGE = 200
MIN_TOTAL_CHARS = 400

CAPABILITY_KEYS = ("text", "tables", "figures", "page_snapshots", "ocr", "vision",
                   "formulas", "charts", "slides", "sheets")


def content_capabilities(extraction: Any) -> dict[str, bool]:
    """Normalized capability flags, every key always present (§42)."""
    raw = dict(getattr(extraction, "capabilities", {}) or {})
    return {key: bool(raw.get(key, False)) for key in CAPABILITY_KEYS}


def _ocr_carried_the_text(extraction: Any) -> bool:
    """True when the document only has text because OCR produced it — either our own page
    OCR fallback, or Docling's OCR on a PDF whose own text layer was empty."""
    warnings = getattr(extraction, "warnings", []) or []
    if "NATIVE_TEXT_LAYER_THIN_DOCLING_OCR_RECOVERED" in warnings:
        return True
    ocr_success = any(item.get("ocr_status") == "SUCCESS"
                      for item in (getattr(extraction, "ocr_items", []) or []))
    if not ocr_success:
        return False
    return ("NATIVE_TEXT_LAYER_THIN_OCR_FALLBACK" in warnings
            or getattr(extraction, "adapter", "") == "image")


def determine(extraction: Any) -> tuple[str, list[str]]:
    """Returns (final_evidence_level, reasons)."""
    reasons: list[str] = []
    if getattr(extraction, "errors", None):
        return UNUSABLE, [f"extraction_error:{e}" for e in extraction.errors]
    if not getattr(extraction, "normalized_json_path", None):
        return UNUSABLE, ["no normalized document.json"]

    capabilities = content_capabilities(extraction)
    chars = int(getattr(extraction, "text_char_count", 0) or 0)
    pages = max(1, int(getattr(extraction, "page_count", 0) or 0))
    adapter = getattr(extraction, "adapter", "")

    if capabilities["sheets"]:
        reasons.append("workbook cell/formula model is the authority")
        return STRUCTURED_TABULAR, reasons

    if adapter == "image" or (capabilities["figures"] and not capabilities["text"]
                              and not capabilities["tables"]):
        if capabilities["ocr"] and chars >= 20:
            reasons.append("text recovered from a standalone image by OCR")
            return IMAGE_OCR, reasons
        reasons.append("valid visual asset with no recoverable text")
        return VISUAL_ONLY, reasons

    if _ocr_carried_the_text(extraction) and chars >= 20:
        reasons.append("the native text layer was unusable; OCR carried the document")
        return IMAGE_OCR, reasons

    if chars >= MIN_TOTAL_CHARS and chars / pages >= MIN_CHARS_PER_PAGE:
        reasons.append(f"{chars} characters over {pages} page(s)")
        return FULL_TEXT, reasons

    if capabilities["text"] and (capabilities["slides"] or capabilities["tables"]
                                 or capabilities["figures"]):
        reasons.append("structure carries the document; text layer is thin")
        return STRUCTURED_DOCUMENT, reasons

    if capabilities["text"] and chars > 0:
        reasons.append(f"only {chars} characters of text and no structural assets")
        return PARTIAL, reasons

    reasons.append("no usable text, tables, sheets or figures")
    return UNUSABLE, reasons
