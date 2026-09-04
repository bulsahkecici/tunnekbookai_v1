"""Table asset extraction (task §9).

A table must never live only inside Markdown. Every reliably extracted table is written as:

    tables/TABLENNNN.json   -- authoritative (grid, OTSL, HTML, merged-cell fidelity)
    tables/TABLENNNN.csv    -- only when the table is safely rectangular
    tables/TABLENNNN.png    -- when an image can be derived from the page image

Provenance (page + bbox) comes from Docling and is left null when absent.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from . import asset_id, base_asset, prov_of
from ..paths import relpath

TABLES_DIRNAME = "tables"


def _grid_from_dataframe(item: Any, doc: Any = None
                         ) -> tuple[list[list[str]] | None, int, int, str | None]:
    # docling-core deprecated the no-argument form; keep it as the fallback for older builds.
    try:
        frame = item.export_to_dataframe(doc) if doc is not None else item.export_to_dataframe()
    except TypeError:
        try:
            frame = item.export_to_dataframe()
        except Exception as exc:
            return None, 0, 0, f"{type(exc).__name__}: {exc}"
    except Exception as exc:
        return None, 0, 0, f"{type(exc).__name__}: {exc}"
    try:
        header = [str(c) for c in frame.columns]
        rows = [[("" if v is None else str(v)) for v in record] for record in frame.values.tolist()]
        grid = [header] + rows
        return grid, len(grid), len(header), None
    except Exception as exc:
        return None, 0, 0, f"{type(exc).__name__}: {exc}"


def _grid_from_table_cells(item: Any) -> tuple[list[list[str]] | None, int, int]:
    """Fallback grid built from TableData cells; honours row/col spans by repetition."""
    data = getattr(item, "data", None)
    cells = getattr(data, "table_cells", None) if data is not None else None
    if not cells:
        return None, 0, 0
    n_rows = int(getattr(data, "num_rows", 0) or 0)
    n_cols = int(getattr(data, "num_cols", 0) or 0)
    if not n_rows or not n_cols:
        for cell in cells:
            n_rows = max(n_rows, int(getattr(cell, "end_row_offset_idx", 0) or 0))
            n_cols = max(n_cols, int(getattr(cell, "end_col_offset_idx", 0) or 0))
    if not n_rows or not n_cols:
        return None, 0, 0
    grid = [["" for _ in range(n_cols)] for _ in range(n_rows)]
    for cell in cells:
        text = str(getattr(cell, "text", "") or "")
        r0 = int(getattr(cell, "start_row_offset_idx", 0) or 0)
        r1 = int(getattr(cell, "end_row_offset_idx", r0 + 1) or r0 + 1)
        c0 = int(getattr(cell, "start_col_offset_idx", 0) or 0)
        c1 = int(getattr(cell, "end_col_offset_idx", c0 + 1) or c0 + 1)
        for r in range(r0, min(r1, n_rows)):
            for c in range(c0, min(c1, n_cols)):
                grid[r][c] = text
    return grid, n_rows, n_cols


def is_rectangular(grid: list[list[str]] | None) -> bool:
    if not grid:
        return False
    width = len(grid[0])
    return width > 0 and all(len(row) == width for row in grid)


def write_table_files(
    out_dir: Path,
    tid: str,
    grid: list[list[str]] | None,
    payload: dict[str, Any],
    *,
    emit_csv: bool,
) -> tuple[Path, Path | None]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{tid}.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    csv_path: Path | None = None
    if emit_csv and is_rectangular(grid):
        csv_path = out_dir / f"{tid}.csv"
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerows(grid)
        csv_path.write_text(buffer.getvalue(), encoding="utf-8")
    return json_path, csv_path


def extract_tables(
    docling_document: Any,
    bundle: Path,
    *,
    document_id: str,
    emit_csv: bool = True,
    emit_png: bool = True,
) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    items = list(getattr(docling_document, "tables", None) or [])
    if not items:
        return [], warnings

    out_dir = bundle / TABLES_DIRNAME
    records: list[dict[str, Any]] = []

    for index, item in enumerate(items, start=1):
        tid = asset_id("TABLE", index)
        page, bbox = prov_of(item)
        grid, rows, cols, df_error = _grid_from_dataframe(item, docling_document)
        if grid is None:
            grid, rows, cols = _grid_from_table_cells(item)
            if grid is None:
                warnings.append(f"TABLE_GRID_UNAVAILABLE:{tid}")
            elif df_error:
                warnings.append(f"TABLE_DATAFRAME_FALLBACK:{tid}")

        try:
            caption = item.caption_text(docling_document) or None
        except Exception:
            caption = None
        otsl = html = None
        try:
            otsl = item.export_to_otsl(docling_document)
        except Exception:
            warnings.append(f"TABLE_OTSL_UNAVAILABLE:{tid}")
        try:
            html = item.export_to_html(docling_document)
        except Exception:
            warnings.append(f"TABLE_HTML_UNAVAILABLE:{tid}")
        try:
            markdown = item.export_to_markdown(docling_document)
        except Exception:
            markdown = None

        payload = {
            "document_id": document_id,
            "table_id": tid,
            "page": page,
            "caption": caption,
            "bbox": bbox,
            "rows": rows,
            "columns": cols,
            "rectangular": is_rectangular(grid),
            "grid": grid,
            "otsl": otsl,
            "html": html,
            "markdown": markdown,
            "element_ref": getattr(item, "self_ref", None),
        }
        json_path, csv_path = write_table_files(out_dir, tid, grid, payload, emit_csv=emit_csv)

        png_path: Path | None = None
        if emit_png:
            try:
                image = item.get_image(docling_document)
            except Exception:
                image = None
            if image is not None:
                png_path = out_dir / f"{tid}.png"
                try:
                    image.convert("RGB").save(str(png_path))
                except Exception as exc:
                    warnings.append(f"TABLE_PNG_FAILED:{tid}:{type(exc).__name__}")
                    png_path = None
            else:
                warnings.append(f"TABLE_PNG_UNAVAILABLE:{tid}")

        record = base_asset(document_id, tid, "TABLE", json_path)
        record.update({
            "table_id": tid,
            "page": page,
            "caption": caption,
            "bbox": bbox,
            "rows": rows,
            "columns": cols,
            "rectangular": is_rectangular(grid),
            "structured_path": relpath(json_path),
            "csv_path": relpath(csv_path) if csv_path else None,
            "image_path": relpath(png_path) if png_path else None,
            "element_ref": getattr(item, "self_ref", None),
            "markdown": markdown,
        })
        records.append(record)
    return records, warnings
