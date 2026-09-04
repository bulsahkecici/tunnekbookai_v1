"""Text-family adapter — TXT / MD / CSV / HTML (task §20).

    TXT / MD   normalized without any model call
    CSV        preserved as a table, not flattened into prose
    HTML       structural extraction from the ORIGINAL html (headings, lists, tables)

No OCR, no vision, no network. Encoding is sniffed conservatively (utf-8 -> utf-8-sig ->
cp1254 for Turkish legacy files -> latin-1 as a last resort) and the choice is recorded.
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from ..assets import asset_id, base_asset
from ..assets import tables as tables_assets
from ..elements import ElementBuilder, HEADING, LIST_ITEM, PARAGRAPH, TABLE_REF
from ..extraction import ExtractionResult, write_normalized
from ..paths import relpath
from . import AdapterContext

ENCODINGS = ("utf-8", "utf-8-sig", "cp1254", "latin-1")


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8/replace"


def _markdown_elements(text: str, builder: ElementBuilder) -> None:
    for block in [b.strip() for b in text.split("\n\n")]:
        if not block:
            continue
        if block.startswith("#"):
            hashes = len(block) - len(block.lstrip("#"))
            builder.add(HEADING, block.lstrip("#").strip(), level=min(hashes, 6))
            continue
        lines = block.splitlines()
        if all(line.lstrip().startswith(("-", "*", "+")) or line.lstrip()[:2].rstrip(".").isdigit()
               for line in lines if line.strip()):
            for line in lines:
                if line.strip():
                    builder.add(LIST_ITEM, line.lstrip("-*+ ").strip())
            continue
        builder.add(PARAGRAPH, block)


def _plain_elements(text: str, builder: ElementBuilder) -> None:
    for block in [b.strip() for b in text.split("\n\n")]:
        if block:
            builder.add(PARAGRAPH, block)


def _csv_elements(path: Path, text: str, bundle: Path, document_id: str,
                  builder: ElementBuilder, result: ExtractionResult) -> list[dict[str, Any]]:
    try:
        dialect = csv.Sniffer().sniff(text[:8192])
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(io.StringIO(text), dialect))
    if not rows:
        result.warn("CSV_EMPTY")
        return []
    tid = asset_id("TABLE", 1)
    payload = {
        "document_id": document_id, "table_id": tid, "page": None, "caption": None,
        "bbox": None, "rows": len(rows), "columns": len(rows[0]),
        "rectangular": tables_assets.is_rectangular(rows), "grid": rows,
        "otsl": None, "html": None, "markdown": None, "element_ref": None,
    }
    json_path, csv_path = tables_assets.write_table_files(
        bundle / tables_assets.TABLES_DIRNAME, tid, rows, payload, emit_csv=True)
    record = base_asset(document_id, tid, "TABLE", json_path)
    record.update({
        "table_id": tid, "page": None, "caption": None, "bbox": None,
        "rows": len(rows), "columns": len(rows[0]),
        "rectangular": payload["rectangular"],
        "structured_path": relpath(json_path),
        "csv_path": relpath(csv_path) if csv_path else None,
        "image_path": None, "element_ref": None, "markdown": None,
    })
    builder.add(HEADING, path.stem, level=1)
    builder.add(TABLE_REF, "", asset_id=tid)
    return [record]


def _html_elements(text: str, bundle: Path, document_id: str, builder: ElementBuilder,
                   result: ExtractionResult) -> list[dict[str, Any]]:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        result.warn("HTML_PARSER_UNAVAILABLE")
        _plain_elements(text, builder)
        return []
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else None
    if title:
        builder.add(HEADING, title, level=1)

    tables: list[dict[str, Any]] = []
    index = 0
    body = soup.body or soup
    for node in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "table", "pre"]):
        name = node.name.lower()
        if name == "table":
            index += 1
            tid = asset_id("TABLE", index)
            grid = [[cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
                    for row in node.find_all("tr")]
            grid = [row for row in grid if row]
            if not grid:
                continue
            payload = {
                "document_id": document_id, "table_id": tid, "page": None,
                "caption": None, "bbox": None, "rows": len(grid), "columns": len(grid[0]),
                "rectangular": tables_assets.is_rectangular(grid), "grid": grid,
                "otsl": None, "html": str(node)[:200_000], "markdown": None, "element_ref": None,
            }
            json_path, csv_path = tables_assets.write_table_files(
                bundle / tables_assets.TABLES_DIRNAME, tid, grid, payload, emit_csv=True)
            record = base_asset(document_id, tid, "TABLE", json_path)
            record.update({
                "table_id": tid, "page": None, "caption": None, "bbox": None,
                "rows": len(grid), "columns": len(grid[0]),
                "rectangular": payload["rectangular"],
                "structured_path": relpath(json_path),
                "csv_path": relpath(csv_path) if csv_path else None,
                "image_path": None, "element_ref": None, "markdown": None,
            })
            tables.append(record)
            builder.add(TABLE_REF, "", asset_id=tid)
            continue
        content = node.get_text(" ", strip=True)
        if not content:
            continue
        if name.startswith("h") and len(name) == 2 and name[1].isdigit():
            builder.add(HEADING, content, level=int(name[1]))
        elif name == "li":
            builder.add(LIST_ITEM, content)
        else:
            builder.add(PARAGRAPH, content)
    return tables


def run(context: AdapterContext) -> ExtractionResult:
    fmt = context.detection.fmt.value
    result = ExtractionResult(document_id=context.document_id, format=fmt, adapter="text")
    source = context.original_path

    try:
        text, encoding = read_text(source)
    except OSError as exc:
        result.fail(f"TEXT_UNREADABLE:{exc}")
        return result
    if encoding.endswith("replace"):
        result.warn("TEXT_ENCODING_LOSSY")

    builder = ElementBuilder()
    tables: list[dict[str, Any]] = []
    if fmt == "CSV":
        tables = _csv_elements(source, text, context.bundle, context.document_id, builder, result)
    elif fmt == "HTML":
        tables = _html_elements(text, context.bundle, context.document_id, builder, result)
    elif fmt == "MD":
        _markdown_elements(text, builder)
    else:
        _plain_elements(text, builder)

    if fmt == "MD":
        markdown = text
    elif fmt == "CSV" and tables:
        grid = json.loads(Path(context.root / tables[0]["structured_path"]).read_text(
            encoding="utf-8"))["grid"]
        header, *rows = grid
        markdown = "\n".join([
            f"# {context.display_name}", "",
            "| " + " | ".join(header) + " |",
            "| " + " | ".join("---" for _ in header) + " |",
            *["| " + " | ".join(str(v) for v in row) + " |" for row in rows[:500]],
        ])
    else:
        parts = [f"# {context.display_name}", ""]
        for element in builder.elements:
            if element["type"] == HEADING:
                parts.append("#" * min(6, (element["level"] or 1) + 1) + " " + element["text"])
            elif element["type"] == LIST_ITEM:
                parts.append(f"- {element['text']}")
            elif element["text"]:
                parts.append(element["text"])
            parts.append("")
        markdown = "\n".join(parts).strip()

    plain = "\n\n".join(e["text"] for e in builder.elements if e["text"])
    document_json = {
        "document_id": context.document_id,
        "format": fmt,
        "adapter": "text",
        "source_filename": context.original_filename,
        "encoding": encoding,
        "structural_authority": "original_source_text",
        "elements": builder.elements,
        "tables": tables,
        "pages": [],
    }
    write_normalized(context.bundle, result, markdown=markdown,
                     document_json=document_json, text=plain or text.strip())

    if not (plain or text.strip()):
        result.fail("TEXT_EMPTY_DOCUMENT")

    result.tables = tables
    result.text_elements = builder.elements
    result.page_count = 0
    result.engine = {"native_parser": "python", "encoding": encoding}
    result.capabilities = {
        "text": bool(plain or text.strip()),
        "tables": bool(tables),
        "figures": False,
        "page_snapshots": False,
        "ocr": False,
        "vision": False,
        "formulas": False,
        "charts": False,
        "slides": False,
        "sheets": False,
    }
    return result
