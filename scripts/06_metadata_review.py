from __future__ import annotations

import importlib.util
import re
from collections import Counter
from pathlib import Path

from utils import iso_time, load_config, native_path, read_csv, setup_logging, strip_front_matter, write_csv


FIELDS = [
    "document_id", "source_file", "source_relative_path", "current_title", "current_authority_level",
    "current_document_type", "current_topics", "evidence_headings", "evidence_excerpt",
    "proposed_authority_level", "proposed_document_type", "proposed_topics", "proposed_organization",
    "proposed_year", "proposed_language", "suggestion_confidence", "review_status", "reviewer",
    "reviewed_at", "review_notes",
]


def load_metadata_module():
    path = Path(__file__).resolve().parent / "04_metadata.py"
    spec = importlib.util.spec_from_file_location("metadata_review_base", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def evidence_from_markdown(path: Path) -> tuple[str, str, str]:
    body = strip_front_matter(native_path(path).read_text(encoding="utf-8-sig", errors="replace"))
    headings = [re.sub(r"^#+\s*", "", line).strip() for line in body.splitlines() if line.lstrip().startswith("#")]
    plain = re.sub(r"[`*_>#|\[\]()]", " ", body)
    plain = re.sub(r"\s+", " ", plain).strip()
    return body, " | ".join(headings[:12]), plain[:1200]


def apply_approved(existing: list[dict[str, str]], metadata_rows: list[dict[str, str]], root: Path, metadata_module, logger) -> int:
    approved = {row["document_id"]: row for row in existing if row.get("review_status", "").casefold() == "approved"}
    if not approved:
        return 0
    count = 0
    for row in metadata_rows:
        decision = approved.get(row["document_id"])
        if not decision:
            continue
        mapping = {
            "authority_level": "proposed_authority_level", "document_type": "proposed_document_type",
            "organization": "proposed_organization", "year": "proposed_year", "language": "proposed_language",
        }
        for target, source in mapping.items():
            if decision.get(source, "").strip():
                row[target] = decision[source].strip()
        if decision.get("proposed_topics", "").strip():
            row["topics"] = "|".join(part.strip() for part in decision["proposed_topics"].split("|") if part.strip())
        markdown = Path(row["markdown_file"])
        body = strip_front_matter(native_path(markdown).read_text(encoding="utf-8-sig", errors="replace")).lstrip()
        metadata = {
            "document_id": row["document_id"], "title": row["title"], "source_file": row["source_file"],
            "source_relative_path": row["source_relative_path"], "source_extension": row["source_extension"],
            "sha256": row["sha256"], "language": row["language"] or None,
            "document_type": row["document_type"] or "unknown", "organization": row["organization"] or None,
            "year": int(row["year"]) if row["year"].isdigit() else None,
            "authority_level": row["authority_level"] or None,
            "topics": [topic for topic in row["topics"].split("|") if topic],
            "duplicate_group": row["duplicate_group"] or None,
            "preferred_variant": row["preferred_variant"].casefold() in {"true", "1", "yes"},
            "conversion_engine": row["conversion_engine"],
        }
        native_path(markdown).write_text(metadata_module.render_front_matter(metadata) + body, encoding="utf-8")
        count += 1
        logger.info("Applied approved metadata review: %s", row["document_id"])
    return count


def main() -> int:
    config = load_config()
    root = config["project_root"]
    logger = setup_logging("06_metadata_review", config)
    metadata_module = load_metadata_module()
    metadata_path = root / "data/metadata/markdown_metadata.csv"
    queue_path = root / "data/metadata/metadata_review_queue.csv"
    metadata_rows = read_csv(metadata_path)
    existing = read_csv(queue_path)
    existing_by_id = {row["document_id"]: row for row in existing}
    applied = apply_approved(existing, metadata_rows, root, metadata_module, logger)
    if applied:
        write_csv(metadata_path, metadata_rows, list(metadata_rows[0].keys()))
    queue: list[dict[str, str]] = []
    for row in metadata_rows:
        if row.get("authority_level") and row.get("document_type") not in {"", "unknown"}:
            continue
        markdown = Path(row["markdown_file"])
        if not native_path(markdown).exists():
            continue
        body, headings, excerpt = evidence_from_markdown(markdown)
        injected = f"# Kaynak yolu: {row['source_relative_path']}\n{body}"
        suggestion = metadata_module.infer_metadata(row["source_file"], injected)
        old = existing_by_id.get(row["document_id"], {})
        proposed_authority = old.get("proposed_authority_level") or suggestion["authority_level"] or ""
        proposed_type = old.get("proposed_document_type") or (suggestion["document_type"] if suggestion["document_type"] != "unknown" else "")
        proposed_topics = old.get("proposed_topics") or "|".join(suggestion["topics"])
        confidence = "medium" if proposed_authority or proposed_type else "low"
        queue.append({
            "document_id": row["document_id"], "source_file": row["source_file"],
            "source_relative_path": row["source_relative_path"], "current_title": row["title"],
            "current_authority_level": row["authority_level"], "current_document_type": row["document_type"],
            "current_topics": row["topics"], "evidence_headings": headings, "evidence_excerpt": excerpt,
            "proposed_authority_level": proposed_authority, "proposed_document_type": proposed_type,
            "proposed_topics": proposed_topics, "proposed_organization": old.get("proposed_organization") or suggestion["organization"] or "",
            "proposed_year": old.get("proposed_year") or suggestion["year"] or "",
            "proposed_language": old.get("proposed_language") or suggestion["language"] or "",
            "suggestion_confidence": confidence, "review_status": old.get("review_status") or "pending_human_review",
            "reviewer": old.get("reviewer") or "", "reviewed_at": old.get("reviewed_at") or "",
            "review_notes": old.get("review_notes") or "",
        })
    write_csv(queue_path, queue, FIELDS)
    statuses = Counter(row["review_status"] for row in queue)
    report = [
        "# Metadata İnsan İnceleme Kuyruğu", "", f"- Kuyruk satırı: **{len(queue)}**",
        f"- Bu çalıştırmada uygulanan onaylı karar: **{applied}**", "",
        "## Kullanım", "",
        "1. `data/metadata/metadata_review_queue.csv` dosyasında öneri ve kanıt alanlarını inceleyin.",
        "2. Gerekirse `proposed_*` alanlarını düzeltin; `reviewer`, `review_notes` ve `reviewed_at` alanlarını doldurun.",
        "3. Kabul edilen satırda `review_status` değerini `approved` yapın.",
        "4. `06_metadata_review.py` yeniden çalıştırıldığında yalnızca onaylı kararlar Markdown ve metadata CSV'ye uygulanır.", "",
        "Otomatik öneriler insan onayı olmadan authoritative metadata olarak uygulanmaz.", "", "## Durumlar", "",
    ]
    report.extend(f"- {name}: {count}" for name, count in statuses.most_common())
    (root / "reports/metadata_review_summary.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    logger.info("Metadata review queue completed: %d rows; %d approvals applied", len(queue), applied)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

