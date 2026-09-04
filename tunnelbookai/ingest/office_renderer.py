"""Office visual renderer abstraction (task §11, §14, §18).

    available()        -- is a renderer usable right now?
    render_to_pdf()    -- DOCX/PPTX/XLSX -> a temporary PDF (derived data, discarded)
    render_pages()     -- that temporary PDF -> PNG page/slide snapshots

LibreOffice headless is the preferred (and currently only) backend. When it is absent the
caller records the warning VISUAL_RENDERER_UNAVAILABLE and continues: a DOCX/PPTX/XLSX is
never rejected merely because no renderer exists (§11, §45).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

VISUAL_RENDERER_UNAVAILABLE = "VISUAL_RENDERER_UNAVAILABLE"


def find_libreoffice() -> Path | None:
    candidates = [Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")]
    if os.name == "nt":
        candidates += [
            Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
            Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        ]
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    return next((c for c in candidates if c.exists()), None)


class OfficeRenderer:
    """Renders Office documents to page images. Every failure is non-fatal."""

    def __init__(self, timeout_seconds: int = 300) -> None:
        self.timeout_seconds = timeout_seconds
        self._binary: Path | None = find_libreoffice()

    # ------------------------------------------------------------------ interface
    def available(self) -> bool:
        return self._binary is not None

    @property
    def backend(self) -> str | None:
        return "libreoffice" if self._binary else None

    def render_to_pdf(self, source: Path, out_dir: Path) -> tuple[Path | None, list[str]]:
        """Convert `source` to a PDF inside `out_dir`. The PDF is derived data only (§11)."""
        if not self.available():
            return None, [VISUAL_RENDERER_UNAVAILABLE]
        out_dir = out_dir.resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        profile = out_dir / "_lo_profile"
        # `as_uri()` percent-encodes: a profile path holding spaces, parentheses or Turkish
        # characters otherwise produces a malformed file:// URL and LibreOffice aborts (§17).
        # Absolute paths also stop a leading-dash filename being read as an option.
        command = [
            str(self._binary), "--headless", "--norestore", "--invisible",
            f"-env:UserInstallation={profile.as_uri()}",
            "--convert-to", "pdf", "--outdir", str(out_dir), str(Path(source).resolve()),
        ]
        try:
            proc = subprocess.run(command, capture_output=True, text=True,
                                  timeout=self.timeout_seconds, check=False,
                                  encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            return None, ["OFFICE_RENDER_TIMEOUT"]
        except Exception as exc:
            return None, [f"OFFICE_RENDER_FAILED:{type(exc).__name__}"]
        produced = out_dir / (Path(source).stem + ".pdf")
        if produced.is_file():
            return produced, []
        candidates = sorted(out_dir.glob("*.pdf"))
        if candidates:
            return candidates[0], []
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()[-1:] or [""]
        return None, [f"OFFICE_RENDER_NO_OUTPUT:{detail[0][:120]}"]

    def render_pages(
        self,
        source: Path,
        bundle: Path,
        *,
        document_id: str,
        scale: float = 2.0,
        dirname: str = "pages",
        prefix: str = "page",
        kind: str = "PAGE",
        id_prefix: str = "PAGE",
    ) -> tuple[list[dict[str, Any]], list[str]]:
        """Office document -> temporary PDF -> PNG snapshots. Temp PDF is always removed."""
        from .assets.snapshots import render_pdf_pages

        if not self.available():
            return [], [VISUAL_RENDERER_UNAVAILABLE]
        with tempfile.TemporaryDirectory(prefix="tbai_office_") as tmp:
            pdf_path, warnings = self.render_to_pdf(Path(source), Path(tmp))
            if pdf_path is None:
                return [], warnings or [VISUAL_RENDERER_UNAVAILABLE]
            records, render_warnings = render_pdf_pages(
                pdf_path, bundle / dirname, document_id=document_id, scale=scale,
                prefix=prefix, kind=kind, id_prefix=id_prefix,
            )
            for record in records:
                record["renderer"] = "libreoffice+pypdfium2"
                record["derived_from"] = "temporary_rendered_pdf"
            return records, warnings + render_warnings
