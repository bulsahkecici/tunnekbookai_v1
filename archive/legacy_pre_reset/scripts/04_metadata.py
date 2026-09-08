from __future__ import annotations

import csv
import os
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path

from utils import (
    display_bytes, load_config, native_path, read_csv, setup_logging, strip_front_matter, write_csv,
    yaml_scalar,
)


TOPIC_RULES = {
    "tunnel_history": [r"tünel tarihi", r"tunnel history"],
    "geology": [r"jeoloji", r"geology"],
    "geotechnics": [r"geoteknik", r"geotechnic"],
    "route_selection": [r"güzerg[aâ]h seç", r"route selection"],
    "NATM": [r"\bnatm\b", r"new austrian tunn"],
    "TBM": [r"\btbm\b", r"tunnel boring machine"],
    "drill_and_blast": [r"delme.{0,5}patlatma", r"drill.{0,5}blast"],
    "excavation": [r"kazı", r"excavation"],
    "support_systems": [r"destek sistem", r"support system"],
    "shotcrete": [r"püskürtme beton", r"shotcrete"],
    "steel_mesh": [r"çelik hasır", r"steel mesh"],
    "steel_rib": [r"çelik iksa", r"steel rib"],
    "rock_bolt": [r"kaya bulonu", r"rock bolt"],
    "forepoling": [r"süren", r"forepol"],
    "waterproofing": [r"su yalıt", r"waterproof"],
    "drainage": [r"drenaj", r"drainage"],
    "final_lining": [r"nihai kaplama", r"final lining"],
    "portal": [r"\bportal\b"],
    "monitoring": [r"izleme", r"monitoring"],
    "instrumentation": [r"enstrümantasyon", r"instrumentation"],
    "safety": [r"güvenlik", r"safety"],
    "fire_safety": [r"yangın güven", r"fire safety"],
    "maintenance": [r"bakım", r"maintenance"],
    "operation": [r"işletme", r"operation"],
    "cost": [r"maliyet", r"\bcost\b"],
    "regulation": [r"yönetmelik", r"regulation"],
    "accident": [r"kaza", r"accident"],
    "collapse": [r"çökme", r"collapse"],
    "risk": [r"\brisk\b", r"risk anal"],
    "traffic": [r"trafik", r"traffic"],
    "special_solutions": [r"özel çözüm", r"special solution"],
    "fiber_reinforcement": [r"fiber", r"lif takviye"],
}


def infer_metadata(file_name: str, markdown_body: str) -> dict:
    stem = Path(file_name).stem
    headings = "\n".join(line for line in markdown_body.splitlines()[:300] if line.lstrip().startswith("#"))
    evidence = f"{stem}\n{headings}".translate(str.maketrans({"İ": "I"})).casefold()
    evidence = unicodedata.normalize("NFC", evidence)
    first_h1 = next((re.sub(r"^#\s+", "", line).strip() for line in markdown_body.splitlines() if re.match(r"^#\s+", line)), "")
    title = first_h1 or stem
    years = [int(value) for value in re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", evidence)]
    year = years[0] if len(set(years)) == 1 else None
    tr_hits = sum(token in evidence for token in (" tünel", " ve ", " için ", "kazı", "yönetmelik", "şartname", "eğitim"))
    en_hits = sum(token in evidence for token in (" tunnel", " and ", " for ", "excavation", "guideline", "manual"))
    language = "tr" if tr_hits > en_hits and tr_hits >= 1 else ("en" if en_hits > tr_hits and en_hits >= 2 else None)

    organization = None
    if re.search(r"\bkgm\b|karayolları genel müdürlüğü", evidence):
        organization = "Karayolları Genel Müdürlüğü"
    elif re.search(r"\bfhwa\b", evidence):
        organization = "FHWA"
    elif re.search(r"\bpiarc\b", evidence):
        organization = "PIARC"

    document_type, authority = "unknown", None
    if re.search(r"teknik şartname|technical specification", evidence):
        document_type, authority = "technical_specification", "A"
    elif re.search(r"yönetmelik|resmi gazete|regulation", evidence):
        document_type, authority = "regulation", "A"
    elif re.search(r"yüksek lisans tez|doktora tez|\btez\b|\bthesis\b", evidence):
        document_type, authority = "thesis", "B"
    elif re.search(r"hakemli|academic paper|journal article", evidence):
        document_type, authority = "academic_paper", "B"
    elif re.search(r"bildiri|conference paper", evidence):
        document_type, authority = "conference_paper", "C"
    elif re.search(r"kurs|seminer|eğitim|training material", evidence):
        document_type, authority = "training_material", "C"
    elif re.search(r"sunum|presentation", evidence):
        document_type, authority = "presentation", "C"
    elif re.search(r"wikipedia", evidence):
        document_type, authority = "web_article", "D"
    elif re.search(r"manual|el kitabı|handbook", evidence):
        document_type = "manual"
        if organization in {"Karayolları Genel Müdürlüğü", "FHWA", "PIARC"}:
            authority = "A"
    elif Path(file_name).suffix.casefold() in {".xls", ".xlsx"}:
        document_type = "spreadsheet"

    if authority is None and organization in {"Karayolları Genel Müdürlüğü", "FHWA", "PIARC"}:
        authority = "A"
    topics = [topic for topic, patterns in TOPIC_RULES.items() if any(re.search(pattern, evidence, re.IGNORECASE) for pattern in patterns)]
    return {
        "title": title, "year": year, "language": language, "organization": organization,
        "document_type": document_type, "authority_level": authority, "topics": topics,
    }


def build_front_matter(row: dict[str, str], inventory: dict[str, dict[str, str]], duplicate_group: str | None) -> dict:
    inv = inventory[row["document_id"]]
    output = Path(row["output_md"])
    body = strip_front_matter(native_path(output).read_text(encoding="utf-8-sig", errors="replace"))
    inferred = infer_metadata(row["source_file"], body)
    return {
        "document_id": row["document_id"], "title": inferred["title"],
        "source_file": row["source_file"], "source_relative_path": row["source_relative_path"],
        "source_extension": row["source_extension"], "sha256": inv["sha256"],
        "language": inferred["language"], "document_type": inferred["document_type"],
        "organization": inferred["organization"], "year": inferred["year"],
        "authority_level": inferred["authority_level"], "topics": inferred["topics"],
        "duplicate_group": duplicate_group, "preferred_variant": str(row["preferred_variant"]).casefold() in {"true", "1", "yes"},
        "conversion_engine": row["converter"],
    }


def render_front_matter(metadata: dict) -> str:
    return "---\n" + "\n".join(f"{key}: {yaml_scalar(value)}" for key, value in metadata.items()) + "\n---\n\n"


def write_pipeline_reports(config: dict, inventory_rows: list[dict], manifest: list[dict], metadata_rows: list[dict], elapsed: float) -> None:
    root = config["project_root"]
    exact = read_csv(root / "data/duplicates/exact_duplicates.csv")
    logical = read_csv(root / "data/duplicates/logical_duplicates.csv")
    ext_counts = Counter(row["extension"].casefold() for row in inventory_rows)
    statuses = Counter(row["status"] for row in manifest)
    authorities = Counter(row["authority_level"] or "Unclassified" for row in metadata_rows)
    document_types = Counter(row["document_type"] for row in metadata_rows)
    topics = Counter(topic for row in metadata_rows for topic in row["topics"].split("|") if topic)
    total_size = sum(int(row["size_bytes"]) for row in inventory_rows)
    image_count = sum(ext_counts[ext] for ext in (".jpg", ".jpeg", ".png"))
    lines = [
        "# TunnelBookAI Pipeline Özeti", "",
        f"- Toplam kaynak dosya: **{len(inventory_rows)}**", f"- Toplam boyut: **{display_bytes(total_size)}** ({total_size} byte)", "",
        "## Format sayıları", "",
        f"- PDF: {ext_counts['.pdf']}", f"- DOC: {ext_counts['.doc']}", f"- DOCX: {ext_counts['.docx']}",
        f"- PPT: {ext_counts['.ppt']}", f"- PPTX: {ext_counts['.pptx']}", f"- XLS: {ext_counts['.xls']}",
        f"- XLSX: {ext_counts['.xlsx']}", f"- Görsel: {image_count}", "",
        "## Duplicate sonuçları", "",
        f"- Exact duplicate grup sayısı: {len({r['duplicate_group_id'] for r in exact})}",
        f"- Exact duplicate dosya sayısı: {len(exact)}",
        f"- Logical duplicate grup sayısı: {len({r['logical_group_id'] for r in logical})}",
        f"- Preferred variant sayısı: {sum(str(r['preferred_source']).casefold() in {'true','1','yes'} for r in logical)}", "",
        "## Dönüşüm sonuçları", "",
        f"- Markdown'a başarıyla çevrilen: {statuses['success']}",
        f"- Duplicate nedeniyle atlanan: {statuses['skipped_exact_duplicate']}",
        f"- Preferred variant nedeniyle atlanan: {statuses['skipped_preferred_variant']}",
        f"- Unsupported: {statuses['unsupported']}", f"- LibreOffice gereken: {statuses['requires_libreoffice']}",
        f"- Conversion failed: {statuses['failed']}", f"- Empty output: {statuses['empty_output']}", "",
        f"- Metadata eklenen Markdown sayısı: **{len(metadata_rows)}**", "", "## Authority", "",
        f"- A: {authorities['A']}", f"- B: {authorities['B']}", f"- C: {authorities['C']}",
        f"- D: {authorities['D']}", f"- Unclassified: {authorities['Unclassified']}", "",
        "## Document types dağılımı", "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in document_types.most_common())
    lines.extend(["", "## En sık topic'ler", ""])
    lines.extend(f"- {name}: {count}" for name, count in topics.most_common())
    if not topics:
        lines.append("- Topic atanmadı")
    lines.extend(["", f"- Toplam uçtan uca çalışma süresi (rapor yazım anına kadar): **{elapsed:.2f} saniye**", "- Kesin bitiş kaydı: `reports/pipeline_timing.txt`."])
    (root / "reports/pipeline_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    failed = [row for row in manifest if row["status"] in {"failed", "empty_output", "requires_libreoffice"}]
    write_csv(root / "reports/failed_files.csv", failed, [
        "document_id", "source_file", "source_relative_path", "source_extension", "status", "converter", "error_message",
    ])


def main() -> int:
    started = time.monotonic()
    config = load_config()
    logger = setup_logging("04_metadata", config)
    root = config["project_root"]
    inventory_rows = read_csv(root / "data/inventory/inventory.csv")
    manifest = read_csv(root / "data/metadata/conversion_manifest.csv")
    inventory = {row["document_id"]: row for row in inventory_rows}
    exact = {row["document_id"]: row["duplicate_group_id"] for row in read_csv(root / "data/duplicates/exact_duplicates.csv")}
    logical = {row["document_id"]: row["logical_group_id"] for row in read_csv(root / "data/duplicates/logical_duplicates.csv")}
    metadata_rows: list[dict] = []
    for row in manifest:
        if row["status"] != "success" or row["document_id"] not in inventory:
            continue
        output = Path(row["output_md"])
        if not native_path(output).exists():
            logger.warning("Successful manifest row has no output: %s", output)
            continue
        body = strip_front_matter(native_path(output).read_text(encoding="utf-8-sig", errors="replace")).lstrip()
        metadata = build_front_matter(row, inventory, exact.get(row["document_id"]) or logical.get(row["document_id"]))
        native_path(output).write_text(render_front_matter(metadata) + body, encoding="utf-8")
        metadata_rows.append({**metadata, "topics": "|".join(metadata["topics"]), "markdown_file": str(output)})
    write_csv(root / "data/metadata/markdown_metadata.csv", metadata_rows, [
        "document_id", "title", "source_file", "source_relative_path", "source_extension", "sha256",
        "language", "document_type", "organization", "year", "authority_level", "topics",
        "duplicate_group", "preferred_variant", "conversion_engine", "markdown_file",
    ])
    elapsed = time.monotonic() - started
    pipeline_started_ms = os.environ.get("TUNNELBOOK_PIPELINE_STARTED_MS")
    reported_elapsed = elapsed
    if pipeline_started_ms:
        try:
            reported_elapsed = max(elapsed, time.time() - (float(pipeline_started_ms) / 1000))
        except ValueError:
            pass
    write_pipeline_reports(config, inventory_rows, manifest, metadata_rows, reported_elapsed)
    logger.info("Metadata completed: %d Markdown files", len(metadata_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
