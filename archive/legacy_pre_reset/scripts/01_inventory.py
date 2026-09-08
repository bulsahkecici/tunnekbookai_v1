from __future__ import annotations

import os
from collections import Counter, defaultdict
from pathlib import Path

from utils import (
    display_bytes, ensure_project_dirs, is_excluded, iso_time, load_config,
    mime_type_for, setup_logging, sha256_file, write_csv, write_jsonl,
)


FIELDS = [
    "document_id", "file_name", "stem", "extension", "absolute_path", "relative_path",
    "parent_folder", "size_bytes", "size_mb", "created_time", "modified_time", "sha256",
    "mime_type", "is_supported", "conversion_candidate", "hash_error",
]


def collect_inventory(config: dict, logger=None) -> list[dict]:
    source_root: Path = config["source_root"]
    excluded = config.get("exclude_directories", [])
    supported = {ext for group in config.get("extensions", {}).values() for ext in group}
    conversion = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".pptm", ".xls", ".xlsx", ".txt", ".rtf"}
    rows: list[dict] = []
    paths: list[Path] = []
    for current, dirs, files in os.walk(source_root):
        current_path = Path(current)
        dirs[:] = sorted(d for d in dirs if not is_excluded(current_path / d, source_root, excluded))
        for file_name in sorted(files):
            path = current_path / file_name
            if not is_excluded(path, source_root, excluded):
                paths.append(path)
    for index, path in enumerate(sorted(paths, key=lambda p: str(p).casefold()), 1):
        hash_value, hash_error = "", ""
        try:
            stat = path.stat()
            hash_value = sha256_file(path)
        except Exception as exc:  # one unreadable file must not abort the archive
            hash_error = f"{type(exc).__name__}: {exc}"
            if logger:
                logger.exception("Could not inspect/hash %s", path)
            try:
                stat = path.stat()
            except Exception:
                stat = None
        relative = path.relative_to(source_root)
        extension = path.suffix.lower()
        size = stat.st_size if stat else 0
        rows.append({
            "document_id": f"DOC{index:06d}", "file_name": path.name, "stem": path.stem,
            "extension": extension, "absolute_path": str(path),
            "relative_path": relative.as_posix(), "parent_folder": relative.parent.as_posix(),
            "size_bytes": size, "size_mb": round(size / 1048576, 6),
            "created_time": iso_time(stat.st_ctime) if stat else "",
            "modified_time": iso_time(stat.st_mtime) if stat else "", "sha256": hash_value,
            "mime_type": mime_type_for(path), "is_supported": extension in supported,
            "conversion_candidate": extension in conversion, "hash_error": hash_error,
        })
    return rows


def write_summary(rows: list[dict], path: Path) -> None:
    counts, sizes, folders = Counter(), defaultdict(int), Counter()
    for row in rows:
        ext = row["extension"] or "[uzantısız]"
        counts[ext] += 1
        sizes[ext] += int(row["size_bytes"])
        folders[row["parent_folder"] or "."] += 1
    total = sum(int(row["size_bytes"]) for row in rows)
    lines = [
        "# Dosya Envanteri Özeti", "", f"- Toplam dosya sayısı: **{len(rows)}**",
        f"- Toplam boyut: **{display_bytes(total)}** ({total} byte)",
        f"- Desteklenen dosya sayısı: **{sum(bool(r['is_supported']) for r in rows)}**",
        f"- Desteklenmeyen dosya sayısı: **{sum(not bool(r['is_supported']) for r in rows)}**",
        f"- 0 byte dosyalar: **{sum(int(r['size_bytes']) == 0 for r in rows)}**",
        f"- Hash hesaplanamayan dosyalar: **{sum(not r['sha256'] for r in rows)}**", "",
        "## Uzantılara göre sayı ve boyut", "", "| Uzantı | Adet | Toplam boyut |", "|---|---:|---:|",
    ]
    lines.extend(f"| {ext} | {counts[ext]} | {display_bytes(sizes[ext])} |" for ext in sorted(counts))
    lines.extend(["", "## Klasörlere göre dosya sayısı", "", "| Klasör | Adet |", "|---|---:|"])
    lines.extend(f"| {folder.replace('|', '\\|')} | {count} |" for folder, count in folders.most_common())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    config = load_config()
    ensure_project_dirs(config)
    logger = setup_logging("01_inventory", config)
    logger.info("Inventory started: %s", config["source_root"])
    rows = collect_inventory(config, logger)
    root = config["project_root"]
    write_csv(root / "data/inventory/inventory.csv", rows, FIELDS)
    write_jsonl(root / "data/inventory/inventory.jsonl", rows)
    write_summary(rows, root / "reports/inventory_summary.md")
    logger.info("Inventory completed: %d files", len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
