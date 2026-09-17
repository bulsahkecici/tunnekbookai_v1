"""Supported-format registry and detection (task §9).

Detection order: file-signature sniff (handles mislabelled PDF and OOXML files), then
extension, then mimetypes. An unsupported format is never silently accepted (stop condition
§93) — it becomes a REJECT with reason UNSUPPORTED_FORMAT, or a quarantine entry.
"""

from __future__ import annotations

import mimetypes
import zipfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Format(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    PPTX = "PPTX"
    XLSX = "XLSX"
    PNG = "PNG"
    JPG = "JPG"
    TXT = "TXT"
    MD = "MD"
    CSV = "CSV"
    HTML = "HTML"
    DOC = "DOC"       # legacy
    PPT = "PPT"       # legacy
    XLS = "XLS"       # legacy
    RTF = "RTF"       # legacy
    UNKNOWN = "UNKNOWN"


_EXT_MAP: dict[str, Format] = {
    ".pdf": Format.PDF, ".docx": Format.DOCX, ".pptx": Format.PPTX, ".pptm": Format.PPTX,
    ".xlsx": Format.XLSX, ".png": Format.PNG, ".jpg": Format.JPG, ".jpeg": Format.JPG,
    ".txt": Format.TXT, ".md": Format.MD, ".markdown": Format.MD, ".csv": Format.CSV,
    ".html": Format.HTML, ".htm": Format.HTML,
    ".doc": Format.DOC, ".ppt": Format.PPT, ".xls": Format.XLS, ".rtf": Format.RTF,
}

_LEGACY = {Format.DOC, Format.PPT, Format.XLS, Format.RTF}

# Which pipeline adapter handles each format.
ADAPTER: dict[Format, str] = {
    Format.PDF: "pdf", Format.DOCX: "docx", Format.PPTX: "pptx", Format.XLSX: "xlsx",
    Format.PNG: "image", Format.JPG: "image",
    Format.TXT: "text", Format.MD: "text", Format.CSV: "text", Format.HTML: "text",
    Format.DOC: "docx", Format.PPT: "pptx", Format.XLS: "xlsx", Format.RTF: "docx",
}


@dataclass(frozen=True)
class Detection:
    fmt: Format
    is_legacy: bool
    mime_type: str
    detected_by: str
    adapter: str


def _ooxml_sniff(path: Path) -> Format | None:
    try:
        with path.open("rb") as handle:
            if handle.read(2) != b"PK":
                return None
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
    except (OSError, zipfile.BadZipFile):
        return None
    if any(n.startswith("word/") for n in names):
        return Format.DOCX
    if any(n.startswith("ppt/") for n in names):
        return Format.PPTX
    if any(n.startswith("xl/") for n in names):
        return Format.XLSX
    return None


def _pdf_sniff(path: Path) -> bool:
    """Recognize a PDF even when an upstream producer supplied the wrong suffix."""
    try:
        with path.open("rb") as handle:
            return handle.read(5) == b"%PDF-"
    except OSError:
        return False


def detect(path: Path) -> Detection:
    ext = path.suffix.lower()
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

    sniffed = _ooxml_sniff(path)
    if sniffed is not None:
        return Detection(sniffed, False, mime, "ooxml_magic", ADAPTER[sniffed])

    if _pdf_sniff(path):
        return Detection(Format.PDF, False, mime, "pdf_magic", ADAPTER[Format.PDF])

    fmt = _EXT_MAP.get(ext, Format.UNKNOWN)
    if fmt is Format.UNKNOWN:
        return Detection(fmt, False, mime, "unknown", "")
    return Detection(fmt, fmt in _LEGACY, mime, "extension", ADAPTER[fmt])


def is_supported(det: Detection, *, libreoffice_available: bool) -> bool:
    if det.fmt is Format.UNKNOWN:
        return False
    if det.is_legacy:
        return libreoffice_available
    return True
