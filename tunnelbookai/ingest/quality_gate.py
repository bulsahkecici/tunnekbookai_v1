"""Per-document quality gate (task §43, §44, §45).

    GO      every minimum requirement holds; the document may be staged
    REVIEW  usable, but something needs a human look (thin evidence, missing renderer,
            low section confidence, crawler/final disagreement)
    REJECT  a minimum requirement failed — the document must not be staged

Format-specific rules (§45): a missing Office renderer is a REVIEW reason, never a REJECT;
an XLSX must yield a structured workbook; an image with no OCR text can still be a valid
VISUAL_ONLY document.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .classify.taxonomy import is_valid_section
from .evidence import UNUSABLE, content_capabilities
from .metadata.schema import validate as validate_metadata

GO = "GO"
REVIEW = "REVIEW"
REJECT = "REJECT"

LOW_SECTION_CONFIDENCE = 0.50


@dataclass
class GateResult:
    decision: str
    checks: dict[str, bool] = field(default_factory=dict)
    reject_reasons: list[str] = field(default_factory=list)
    review_reasons: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self, document_id: str) -> dict[str, Any]:
        return {
            "document_id": document_id,
            "decision": self.decision,
            "checks": self.checks,
            "reject_reasons": self.reject_reasons,
            "review_reasons": self.review_reasons,
            "notes": self.notes,
        }


def _format_checks(fmt: str, extraction: Any, config: Any, result: GateResult) -> None:
    cfg = (config.quality_gate or {}).get("format_specific", {}) or {}
    warnings = set(getattr(extraction, "warnings", []) or [])
    capabilities = content_capabilities(extraction)
    fmt = (fmt or "").upper()

    if fmt == "PDF":
        expected = int(getattr(extraction, "page_count", 0) or 0)
        rendered = len(getattr(extraction, "pages", []) or [])
        ratio_min = float((cfg.get("pdf", {}) or {}).get("page_snapshot_ratio_min", 0.95))
        ratio = (rendered / expected) if expected else 0.0
        ok = expected > 0 and ratio >= ratio_min
        result.checks["pdf_page_snapshot_ratio"] = ok
        if expected <= 0:
            result.reject_reasons.append("PDF_PAGE_COUNT_INCOHERENT")
        elif not ok:
            result.review_reasons.append(f"PDF_SNAPSHOT_INCOMPLETE:{rendered}/{expected}")

    elif fmt in {"DOCX", "PPTX", "DOC", "PPT", "RTF"}:
        renderer_missing = "VISUAL_RENDERER_UNAVAILABLE" in warnings
        result.checks["office_visual_snapshots"] = not renderer_missing
        if renderer_missing:
            # explicitly NOT a rejection (§11, §14, §45)
            result.review_reasons.append("VISUAL_RENDERER_UNAVAILABLE")

    elif fmt in {"XLSX", "XLS"}:
        ok = bool(getattr(extraction, "sheets", None))
        result.checks["xlsx_structured_workbook"] = ok
        if not ok and (cfg.get("xlsx", {}) or {}).get("require_structured_workbook", True):
            result.reject_reasons.append("XLSX_NO_STRUCTURED_WORKBOOK")
        lost = [w for w in warnings if w.startswith("XLSX_CACHED_VALUES_UNAVAILABLE")]
        if lost:
            result.notes.append("workbook has formulas with no cached values (kept as null)")

    elif fmt in {"PNG", "JPG"}:
        has_text = capabilities["text"]
        result.checks["image_ocr_text"] = has_text
        if not has_text:
            # a valid image with no OCR text is still a valid VISUAL_ONLY document (§45)
            result.review_reasons.append("OCR_EMPTY_TEXT_IMAGE")


def evaluate(
    *,
    document_id: str,
    archive_meta: dict[str, Any],
    provenance_doc: dict[str, Any],
    extraction: Any,
    metadata: dict[str, Any],
    classification: Any,
    evidence_level: str,
    config: Any,
    original_path: Path | None = None,
) -> GateResult:
    result = GateResult(decision=GO)
    checks = result.checks

    # ------------------------------------------------------------ minimum GO rules (§44)
    checks["original_exists"] = bool(
        original_path is not None and Path(original_path).is_file())
    if not checks["original_exists"]:
        result.reject_reasons.append("ORIGINAL_MISSING")

    sha = (archive_meta.get("original_sha256") or "").lower()
    checks["sha256_valid"] = len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)
    if not checks["sha256_valid"]:
        result.reject_reasons.append("SHA256_INVALID")

    fmt = (archive_meta.get("format") or "").upper()
    checks["supported_format"] = fmt not in {"", "UNKNOWN"}
    if not checks["supported_format"]:
        result.reject_reasons.append("UNSUPPORTED_FORMAT")

    checks["structural_extraction_success"] = bool(
        getattr(extraction, "normalized_json_path", None) and not getattr(extraction, "errors", []))
    if not checks["structural_extraction_success"]:
        result.reject_reasons.append("EXTRACTION_FAILED")

    checks["provenance_present"] = bool((provenance_doc or {}).get("sources"))
    if not checks["provenance_present"]:
        result.reject_reasons.append("PROVENANCE_MISSING")

    metadata_problems = validate_metadata(metadata)
    checks["metadata_schema_valid"] = not metadata_problems
    if metadata_problems:
        result.reject_reasons.append("METADATA_SCHEMA_INVALID")
        result.notes += metadata_problems[:5]

    primary = getattr(classification, "final_primary_section", None)
    checks["final_section_in_taxonomy"] = is_valid_section(primary)
    if not checks["final_section_in_taxonomy"]:
        result.reject_reasons.append("FINAL_SECTION_INVALID_OR_MISSING")

    checks["no_critical_extraction_error"] = not getattr(extraction, "errors", [])
    checks["evidence_usable"] = evidence_level != UNUSABLE
    if evidence_level == UNUSABLE:
        result.reject_reasons.append("EVIDENCE_UNUSABLE")

    # ------------------------------------------------------------ format-specific (§45)
    _format_checks(fmt, extraction, config, result)

    # ------------------------------------------------------------------- review triggers
    confidence = getattr(classification, "final_section_confidence", None)
    if confidence is not None and float(confidence) < LOW_SECTION_CONFIDENCE:
        result.review_reasons.append("LOW_SECTION_CONFIDENCE")
    if getattr(classification, "crawler_final_agreement", None) is False:
        result.review_reasons.append("CRAWLER_FINAL_SECTION_DISAGREEMENT")
    if evidence_level == "PARTIAL":
        result.review_reasons.append("PARTIAL_EVIDENCE")
    capabilities = content_capabilities(extraction)
    if capabilities["figures"] and not capabilities["vision"] and not capabilities["text"]:
        result.review_reasons.append("VISION_UNAVAILABLE_VISUAL_ASSET")

    if result.reject_reasons:
        result.decision = REJECT
    elif result.review_reasons:
        result.decision = REVIEW
    else:
        result.decision = GO
    return result


def write_gate(bundle: Path, document_id: str, result: GateResult) -> Path:
    bundle.mkdir(parents=True, exist_ok=True)
    path = bundle / "quality_gate.json"
    path.write_text(json.dumps(result.to_dict(document_id), ensure_ascii=False, indent=2),
                    encoding="utf-8")
    return path
