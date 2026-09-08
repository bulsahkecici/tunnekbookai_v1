from __future__ import annotations

import argparse
import importlib.util
import time
from collections import Counter
from pathlib import Path

from utils import iso_time, load_config, native_path, read_csv, setup_logging, write_csv


FIELDS = [
    "document_id", "source_file", "source_relative_path", "source_extension", "source_sha256",
    "previous_converter", "output_md", "status", "started_at", "finished_at",
    "duration_seconds", "error_message",
]
ELIGIBLE = {".pdf", ".docx", ".pptx", ".pptm", ".xlsx"}


def load_script(file_name: str, module_name: str):
    path = Path(__file__).resolve().parent / file_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def full_output_path(root: Path, relative_path: str) -> Path:
    return (root / "data/markdown_full_docling" / Path(relative_path)).with_suffix(".md")


def metadata_for_document(metadata_rows: dict[str, dict[str, str]], document_id: str, converter: str) -> dict:
    row = metadata_rows.get(document_id, {})
    year = row.get("year") or None
    try:
        year = int(year) if year else None
    except ValueError:
        year = None
    return {
        "document_id": document_id,
        "title": row.get("title") or row.get("source_file") or document_id,
        "source_file": row.get("source_file") or None,
        "source_relative_path": row.get("source_relative_path") or None,
        "source_extension": row.get("source_extension") or None,
        "sha256": row.get("sha256") or None,
        "language": row.get("language") or None,
        "document_type": row.get("document_type") or "unknown",
        "organization": row.get("organization") or None,
        "year": year,
        "authority_level": row.get("authority_level") or None,
        "topics": [topic for topic in (row.get("topics") or "").split("|") if topic],
        "duplicate_group": row.get("duplicate_group") or None,
        "preferred_variant": str(row.get("preferred_variant", "true")).casefold() in {"true", "1", "yes"},
        "conversion_engine": converter,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resumable full Docling layout/OCR pass")
    parser.add_argument("--max-files", type=int, default=0, help="0 processes every remaining candidate")
    args = parser.parse_args()

    config = load_config()
    root = config["project_root"]
    logger = setup_logging("05_full_docling", config)
    convert = load_script("03_convert.py", "convert_script_full")
    metadata_module = load_script("04_metadata.py", "metadata_script_full")
    inventory = {row["document_id"]: row for row in read_csv(root / "data/inventory/inventory.csv")}
    conversion = read_csv(root / "data/metadata/conversion_manifest.csv")
    metadata_rows = {row["document_id"]: row for row in read_csv(root / "data/metadata/markdown_metadata.csv")}
    manifest_path = root / "data/metadata/full_docling_manifest.csv"
    previous = {row["document_id"]: row for row in read_csv(manifest_path)}
    candidates = [
        row for row in conversion
        if row.get("status") == "success"
        and row.get("source_extension", "").lower() in ELIGIBLE
        and "docling" not in row.get("converter", "").lower()
    ]
    candidates.sort(key=lambda row: (int(inventory[row["document_id"]]["size_bytes"]), row["source_relative_path"].casefold()))
    if args.max_files:
        candidates = candidates[: args.max_files]
    results: list[dict] = []
    candidate_ids = {row["document_id"] for row in candidates}
    for doc_id, row in previous.items():
        if doc_id not in candidate_ids:
            results.append(row)
    logger.info("Full Docling pass started: %d candidates", len(candidates))
    for index, row in enumerate(candidates, 1):
        doc_id = row["document_id"]
        inv = inventory[doc_id]
        source = Path(inv["absolute_path"])
        output = full_output_path(root, row["source_relative_path"])
        old = previous.get(doc_id)
        if old and old.get("status") == "success" and old.get("source_sha256") == inv["sha256"] and native_path(output).exists():
            results.append(old)
            logger.info("Resume skip %d/%d: %s", index, len(candidates), row["source_relative_path"])
            continue
        started = time.monotonic()
        record = {
            "document_id": doc_id, "source_file": row["source_file"],
            "source_relative_path": row["source_relative_path"], "source_extension": row["source_extension"],
            "source_sha256": inv["sha256"], "previous_converter": row["converter"],
            "output_md": str(output), "status": "", "started_at": iso_time(), "finished_at": "",
            "duration_seconds": 0, "error_message": "",
        }
        logger.info("Processing %d/%d: %s", index, len(candidates), row["source_relative_path"])
        try:
            text = convert.docling_convert(source)
            if not convert.meaningful_text(text, source.stem):
                record.update(status="empty_output", error_message="Full Docling produced no meaningful text")
            else:
                metadata = metadata_for_document(metadata_rows, doc_id, "docling_full_layout_ocr")
                native_path(output.parent).mkdir(parents=True, exist_ok=True)
                native_path(output).write_text(metadata_module.render_front_matter(metadata) + text.strip() + "\n", encoding="utf-8")
                record["status"] = "success"
        except Exception as exc:
            record.update(status="failed", error_message=f"{type(exc).__name__}: {exc}")
            logger.exception("Full Docling failed: %s", source)
        record["finished_at"] = iso_time()
        record["duration_seconds"] = round(time.monotonic() - started, 3)
        results.append(record)
        write_csv(manifest_path, results, FIELDS)
    write_csv(manifest_path, results, FIELDS)
    counts = Counter(row["status"] for row in results if row["document_id"] in candidate_ids)
    report = [
        "# Full Docling Layout/OCR Özeti", "", f"- Aday: **{len(candidates)}**",
        f"- Başarılı: **{counts['success']}**", f"- Empty output: **{counts['empty_output']}**",
        f"- Failed: **{counts['failed']}**", "",
        "Çıktılar ana Markdown dosyalarının üzerine yazılmaz; `data/markdown_full_docling` altında karşılaştırmalı olarak tutulur.",
    ]
    (root / "reports/full_docling_summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    logger.info("Full Docling pass completed: %s", dict(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

