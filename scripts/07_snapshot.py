from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from utils import display_bytes, iso_time, load_config, read_csv, setup_logging, write_csv, write_jsonl


OFFICE_IMAGES = ["WINWORD.EXE", "EXCEL.EXE", "POWERPNT.EXE", "SOFFICE.EXE"]


def active_office_processes() -> list[str]:
    if os.name != "nt":
        return []
    active = []
    for image in OFFICE_IMAGES:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {image}", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        line = result.stdout.strip()
        if line.startswith('"') and image.casefold() in line.casefold():
            active.append(image)
    return active


def archive_digest(rows: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda item: item["relative_path"].casefold()):
        digest.update(row["relative_path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(row["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a lock-aware immutable inventory snapshot")
    parser.add_argument("--allow-active-office", action="store_true")
    args = parser.parse_args()
    config = load_config()
    root = config["project_root"]
    logger = setup_logging("07_snapshot", config)
    active = active_office_processes()
    if active and not args.allow_active_office:
        logger.error("Snapshot refused because Office processes are active: %s", ", ".join(active))
        return 3
    rows = read_csv(root / "data/inventory/inventory.csv")
    if not rows:
        logger.error("Inventory missing; run 01_inventory.py first")
        return 2
    lock_files = [row["relative_path"] for row in rows if row["file_name"].startswith("~$")]
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    snapshot_dir = root / "data/inventory/snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    csv_path = snapshot_dir / f"source_snapshot_{timestamp}.csv"
    jsonl_path = snapshot_dir / f"source_snapshot_{timestamp}.jsonl"
    fields = list(rows[0].keys())
    write_csv(csv_path, rows, fields)
    write_jsonl(jsonl_path, rows)
    shutil.copy2(csv_path, root / "data/inventory/source_snapshot.csv")
    shutil.copy2(jsonl_path, root / "data/inventory/source_snapshot.jsonl")
    total_bytes = sum(int(row["size_bytes"]) for row in rows)
    manifest = {
        "snapshot_id": timestamp, "created_at": iso_time(), "source_root": str(config["source_root"]),
        "file_count": len(rows), "total_bytes": total_bytes, "archive_sha256": archive_digest(rows),
        "hash_error_count": sum(not row["sha256"] for row in rows),
        "active_office_processes": active, "office_lock_files": lock_files,
        "inventory_csv": str(csv_path), "inventory_jsonl": str(jsonl_path),
    }
    manifest_path = snapshot_dir / f"source_snapshot_{timestamp}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "data/inventory/source_snapshot.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = [
        "# Kaynak Arşiv Snapshot", "", f"- Snapshot ID: `{timestamp}`",
        f"- Dosya: **{len(rows)}**", f"- Boyut: **{display_bytes(total_bytes)}** ({total_bytes} byte)",
        f"- Birleşik arşiv SHA256: `{manifest['archive_sha256']}`",
        f"- Hash hatası: **{manifest['hash_error_count']}**",
        f"- Aktif Office süreci: **{len(active)}**", f"- Office lock dosyası: **{len(lock_files)}**", "",
    ]
    if lock_files:
        report.extend(["## Kaynakta kalan lock dosyaları", ""] + [f"- `{path}`" for path in lock_files] + [""])
    report.append("Snapshot kaynakları kopyalamaz veya değiştirmez; dosya yolu + gerçek içerik SHA256 birleşimini mühürler.")
    (root / "reports/source_snapshot.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    logger.info("Snapshot completed: %d files; digest=%s", len(rows), manifest["archive_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
