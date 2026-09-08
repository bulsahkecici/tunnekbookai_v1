from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


FINAL_FIELDS = [
    "document_id", "source_relative_path", "source_sha256", "baseline_output",
    "full_docling_output", "final_output", "selected_variant", "selection_reason",
    "baseline_converter", "full_docling_status", "quality_status", "authority_level",
    "document_type", "language", "year", "topics", "citation_sidecar",
    "original_page_provenance_available",
]
REQUIRED_METADATA = ("document_id", "source_relative_path", "sha256")
REPORTED_METADATA = ("authority_level", "document_type", "language", "year", "topics")
TRUE_VALUES = {"1", "true", "yes"}
MISSING_METADATA_VALUES = {"", "unknown", "unclassified", "null", "none"}


class FinalCorpusError(RuntimeError):
    pass


def as_bool(value: object) -> bool:
    return str(value).strip().casefold() in TRUE_VALUES


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FinalCorpusError(f"Gerekli manifest bulunamadı: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return digest.hexdigest()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix().casefold()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def tree_state_digest(root: Path) -> str:
    """Fast immutable-source/idempotence signature using name, size and mtime."""
    digest = hashlib.sha256()
    if not root.exists():
        return digest.hexdigest()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix().casefold()):
        stat = path.stat()
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(stat.st_size).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(stat.st_mtime_ns).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return False
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return True


def copy_if_changed(source: Path, destination: Path) -> bool:
    """Copy bytes/front matter unchanged and preserve source mtime for fast resume."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_stat = source.stat()
    if destination.exists():
        destination_stat = destination.stat()
        if (
            destination_stat.st_size == source_stat.st_size
            and destination_stat.st_mtime_ns == source_stat.st_mtime_ns
        ):
            return False
        if destination_stat.st_size == source_stat.st_size and sha256_file(destination) == sha256_file(source):
            os.utime(destination, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))
            return False
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    os.close(fd)
    try:
        shutil.copy2(source, temporary_name)
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return True


def csv_payload(rows: Iterable[dict[str, object]]) -> bytes:
    import io

    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=FINAL_FIELDS, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + text.getvalue()).encode("utf-8")


def markdown_relative(source_relative_path: str) -> Path:
    source = Path(unicodedata.normalize("NFC", source_relative_path.replace("\\", "/")))
    return source.with_suffix(".md")


def project_relative(value: str) -> str:
    normalized = (value or "").replace("\\", "/")
    marker = "_TunnelBookAI/"
    if marker in normalized:
        normalized = normalized.split(marker, 1)[1]
    normalized = normalized.lstrip("/")
    if not normalized.startswith("data/"):
        raise FinalCorpusError(f"Proje dışı artifact yolu: {value}")
    return Path(normalized).as_posix()


def ensure_nonempty(path: Path, label: str) -> None:
    if not path.is_file():
        raise FinalCorpusError(f"{label} bulunamadı: {path}")
    if path.stat().st_size == 0 or not path.read_text(encoding="utf-8-sig", errors="replace").strip():
        raise FinalCorpusError(f"{label} boş: {path}")


def valid_sha(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdefABCDEF" for character in value)


def metadata_is_missing(value: str) -> bool:
    return (value or "").strip().casefold() in MISSING_METADATA_VALUES


def duplicate_values(rows: list[dict[str, str]], field: str) -> list[str]:
    counts = Counter(row[field] for row in rows)
    return sorted(value for value, count in counts.items() if value and count > 1)


def sidecar_info(
    project_root: Path,
    document_id: str,
    chunks_by_document: dict[str, list[dict[str, str]]],
) -> tuple[str, bool, list[str]]:
    chunks = sorted(chunks_by_document.get(document_id, []), key=lambda row: row.get("chunk_id", ""))
    sidecars: list[str] = []
    problems: list[str] = []
    provenance_flags: list[bool] = []
    for chunk in chunks:
        if chunk.get("status") != "success":
            problems.append(f"{document_id}:{chunk.get('chunk_id', '?')}:chunk_not_success")
            continue
        raw_sidecar = chunk.get("output_chunk_json", "")
        if not raw_sidecar:
            problems.append(f"{document_id}:{chunk.get('chunk_id', '?')}:sidecar_reference_missing")
            continue
        relative = project_relative(raw_sidecar)
        if not (project_root / relative).is_file():
            problems.append(f"{document_id}:{chunk.get('chunk_id', '?')}:sidecar_file_missing")
        sidecars.append(relative)
        has_ranges = bool(chunk.get("original_page_start") and chunk.get("original_page_end"))
        has_map = False
        if chunk.get("page_map_json"):
            try:
                page_map = json.loads(chunk["page_map_json"])
                has_map = isinstance(page_map, dict) and bool(page_map)
            except json.JSONDecodeError:
                problems.append(f"{document_id}:{chunk.get('chunk_id', '?')}:invalid_page_map")
        provenance_flags.append(has_ranges and has_map)
    if not chunks:
        problems.append(f"{document_id}:chunk_manifest_missing")
    return "|".join(sidecars), bool(provenance_flags) and all(provenance_flags), problems


def build_rows(project_root: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    metadata_dir = project_root / "data/metadata"
    metadata = [row for row in read_csv(metadata_dir / "markdown_metadata.csv") if as_bool(row.get("preferred_variant", "true"))]
    quality_rows = read_csv(metadata_dir / "full_docling_quality_manifest.csv")
    conversion_rows = read_csv(metadata_dir / "conversion_manifest.csv")
    chunk_rows = read_csv(metadata_dir / "full_docling_chunk_manifest.csv")

    duplicate_document_ids = duplicate_values(metadata, "document_id")
    if duplicate_document_ids:
        raise FinalCorpusError(f"Duplicate canonical document_id: {', '.join(duplicate_document_ids)}")
    source_sha_duplicates = duplicate_values(metadata, "sha256")
    if source_sha_duplicates:
        raise FinalCorpusError(f"Exact duplicate canonical SHA256: {', '.join(source_sha_duplicates)}")

    quality_by_id = {row["document_id"]: row for row in quality_rows}
    if len(quality_by_id) != len(quality_rows):
        raise FinalCorpusError("Full Docling quality manifestinde duplicate document_id var")
    conversion_by_id = {row["document_id"]: row for row in conversion_rows}
    chunks_by_document: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in chunk_rows:
        chunks_by_document[row["document_id"]].append(row)

    rows: list[dict[str, str]] = []
    provenance_problems: list[str] = []
    missing_metadata = Counter()
    persistent_failures = 0
    for metadata_row in sorted(metadata, key=lambda row: row["document_id"]):
        document_id = metadata_row["document_id"]
        source_sha = metadata_row.get("sha256", "").strip()
        for field in REQUIRED_METADATA:
            if not metadata_row.get(field, "").strip():
                missing_metadata[field] += 1
        for field in REPORTED_METADATA:
            if metadata_is_missing(metadata_row.get(field, "")):
                missing_metadata[field] += 1
        if not valid_sha(source_sha):
            raise FinalCorpusError(f"Geçersiz source SHA256: {document_id}")

        conversion = conversion_by_id.get(document_id, {})
        if conversion.get("status") in {"skipped_exact_duplicate", "skipped_preferred_variant"}:
            raise FinalCorpusError(f"Canonical corpus'a duplicate/non-preferred belge sızdı: {document_id}")
        if conversion.get("source_sha256") and conversion["source_sha256"] != source_sha:
            raise FinalCorpusError(f"Conversion/metadata SHA uyuşmazlığı: {document_id}")

        relative_markdown = markdown_relative(metadata_row["source_relative_path"])
        baseline_relative = (Path("data/markdown") / relative_markdown).as_posix()
        full_relative = (Path("data/markdown_full_docling") / relative_markdown).as_posix()
        final_relative = (Path("data/corpus_final") / relative_markdown).as_posix()
        baseline_path = project_root / baseline_relative
        full_path = project_root / full_relative
        quality = quality_by_id.get(document_id)

        citation_sidecar = ""
        original_page_provenance = False
        if quality is None:
            selected_variant = "baseline"
            selection_reason = "canonical_baseline_not_full_docling_candidate"
            full_status = "not_candidate"
            quality_status = "not_applicable"
        elif quality.get("source_sha256") and quality["source_sha256"] != source_sha:
            raise FinalCorpusError(f"Quality/metadata SHA uyuşmazlığı: {document_id}")
        elif quality.get("recommended_variant") == "full_docling":
            selected_variant = "full_docling"
            selection_reason = "quality_passed_use_full_docling"
            full_status = quality.get("full_docling_status", "")
            quality_status = quality.get("quality_status", "")
            if full_status != "success" or quality_status != "passed":
                raise FinalCorpusError(f"Tutarsız Full Docling önerisi: {document_id}")
            citation_sidecar, original_page_provenance, problems = sidecar_info(
                project_root, document_id, chunks_by_document
            )
            provenance_problems.extend(problems)
        elif quality.get("recommended_variant") == "baseline":
            selected_variant = "baseline"
            full_status = quality.get("full_docling_status", "")
            quality_status = quality.get("quality_status", "")
            if full_status == "quality_reject_use_baseline":
                selection_reason = "quality_reject_use_baseline"
            elif full_status == "no_improvement_use_baseline":
                selection_reason = "no_improvement_use_baseline"
            else:
                raise FinalCorpusError(f"Bilinmeyen baseline fallback durumu: {document_id} ({full_status})")
        elif quality.get("full_docling_status") == "failed":
            selected_variant = "baseline"
            selection_reason = "persistent_docling_failure_use_baseline"
            full_status = "failed"
            quality_status = quality.get("quality_status", "not_evaluated")
            persistent_failures += 1
        else:
            raise FinalCorpusError(f"Çözümlenemeyen quality kararı: {document_id}")

        selected_path = full_path if selected_variant == "full_docling" else baseline_path
        ensure_nonempty(selected_path, f"Seçilen {selected_variant} Markdown ({document_id})")
        rows.append({
            "document_id": document_id,
            "source_relative_path": metadata_row["source_relative_path"],
            "source_sha256": source_sha,
            "baseline_output": baseline_relative,
            "full_docling_output": full_relative if quality else "",
            "final_output": final_relative,
            "selected_variant": selected_variant,
            "selection_reason": selection_reason,
            "baseline_converter": quality.get("baseline_converter", "") if quality else metadata_row.get("conversion_engine", conversion.get("converter", "")),
            "full_docling_status": full_status,
            "quality_status": quality_status,
            "authority_level": metadata_row.get("authority_level", ""),
            "document_type": metadata_row.get("document_type", ""),
            "language": metadata_row.get("language", ""),
            "year": metadata_row.get("year", ""),
            "topics": metadata_row.get("topics", ""),
            "citation_sidecar": citation_sidecar,
            "original_page_provenance_available": str(original_page_provenance).lower(),
        })

    duplicate_final_paths = duplicate_values(rows, "final_output")
    if duplicate_final_paths:
        raise FinalCorpusError(f"Duplicate final path: {', '.join(duplicate_final_paths)}")
    quality_counts = Counter(row.get("full_docling_status", "") for row in quality_rows)
    diagnostics: dict[str, object] = {
        "baseline_canonical": len(metadata),
        "quality_reject": quality_counts["quality_reject_use_baseline"],
        "no_improvement": quality_counts["no_improvement_use_baseline"],
        "persistent_failure": persistent_failures,
        "missing_metadata": dict(missing_metadata),
        "provenance_problems": provenance_problems,
        "duplicate_document_ids": duplicate_document_ids,
        "duplicate_final_paths": duplicate_final_paths,
        "exact_duplicate_sha": source_sha_duplicates,
    }
    return rows, diagnostics


def audit_markdown(
    rows: list[dict[str, str]], diagnostics: dict[str, object], integrity: dict[str, object]
) -> str:
    selected = Counter(row["selected_variant"] for row in rows)
    missing = diagnostics["missing_metadata"]
    lines = [
        "# TunnelBookAI Final Corpus Audit",
        "",
        "## Sonuç",
        "",
        f"- Karar: **{'GO' if integrity['go'] else 'NO-GO'}**",
        f"- Ana baseline canonical belge sayısı: **{diagnostics['baseline_canonical']}**",
        f"- Full Docling ile değiştirilen belge sayısı: **{selected['full_docling']}**",
        f"- Baseline kalan belge sayısı: **{selected['baseline']}**",
        f"- Quality reject sayısı: **{diagnostics['quality_reject']}**",
        f"- No improvement sayısı: **{diagnostics['no_improvement']}**",
        f"- Persistent Docling failure sayısı: **{diagnostics['persistent_failure']}**",
        f"- Final corpus toplam belge sayısı: **{len(rows)}**",
        "",
        "## Integrity kontrolleri",
        "",
        f"- Eksik final output: **{integrity['missing_final_outputs']}**",
        f"- Boş final output: **{integrity['empty_final_outputs']}**",
        f"- Duplicate document_id: **{len(diagnostics['duplicate_document_ids'])}**",
        f"- Duplicate final path: **{len(diagnostics['duplicate_final_paths'])}**",
        f"- Exact duplicate SHA tekrar dahil edilmiş: **{len(diagnostics['exact_duplicate_sha'])}**",
        f"- SHA/provenance problemi: **{integrity['sha_provenance_problems']}**",
        f"- Baseline kaynak ağacı değişti: **{str(integrity['baseline_changed']).lower()}**",
        f"- Full Docling kaynak ağacı değişti: **{str(integrity['full_docling_changed']).lower()}**",
        f"- Her canonical document_id için tek final Markdown: **{str(integrity['one_per_canonical']).lower()}**",
        "",
        "## Metadata eksiklikleri",
        "",
        "Bu aşamada metadata LLM ile doldurulmadı; aşağıdaki boşluklar mevcut canonical metadata'dan aynen taşındı:",
        "",
    ]
    for field in (*REQUIRED_METADATA, *REPORTED_METADATA):
        lines.append(f"- `{field}`: **{missing.get(field, 0)}**")
    lines.extend([
        "",
        "## Provenance",
        "",
        f"- Citation sidecar referansı bulunan Full Docling belge: **{sum(bool(row['citation_sidecar']) for row in rows if row['selected_variant'] == 'full_docling')}**",
        f"- Original-page provenance mevcut Full Docling belge: **{sum(row['original_page_provenance_available'] == 'true' for row in rows if row['selected_variant'] == 'full_docling')}**",
        "- Citation-safe Docling JSON sidecar dosyaları yerinde bırakıldı; manifest yalnız referanslarını taşır.",
        "- Final Markdown dosyaları seçilen kaynaktan byte-for-byte kopyalandı; front matter değiştirilmedi.",
        "",
        "## Kapsam dışı",
        "",
        "OCR normalization, LLM metadata tamamlama, chunking, embedding, Qdrant ve RAG çalıştırılmadı.",
        "",
    ])
    return "\n".join(lines)


def assemble(project_root: Path) -> dict[str, object]:
    project_root = project_root.resolve()
    baseline_root = project_root / "data/markdown"
    full_root = project_root / "data/markdown_full_docling"
    final_root = project_root / "data/corpus_final"
    manifest_path = project_root / "data/metadata/final_corpus_manifest.csv"
    report_path = project_root / "reports/final_corpus_audit.md"
    baseline_before = tree_state_digest(baseline_root)
    full_before = tree_state_digest(full_root)

    rows, diagnostics = build_rows(project_root)
    expected_paths = {Path(row["final_output"]).relative_to("data/corpus_final").as_posix() for row in rows}
    changed_outputs = 0
    for row in rows:
        source_relative = row["full_docling_output"] if row["selected_variant"] == "full_docling" else row["baseline_output"]
        source = project_root / source_relative
        destination = project_root / row["final_output"]
        if copy_if_changed(source, destination):
            changed_outputs += 1
    if final_root.exists():
        for path in sorted((p for p in final_root.rglob("*") if p.is_file()), reverse=True):
            if path.relative_to(final_root).as_posix() not in expected_paths:
                path.unlink()

    missing_outputs = [row["document_id"] for row in rows if not (project_root / row["final_output"]).is_file()]
    empty_outputs = [
        row["document_id"] for row in rows
        if (project_root / row["final_output"]).is_file()
        and not (project_root / row["final_output"]).read_text(encoding="utf-8-sig", errors="replace").strip()
    ]
    copy_mismatches = [
        row["document_id"] for row in rows
        if (project_root / row["final_output"]).stat().st_size != (
            project_root / (row["full_docling_output"] if row["selected_variant"] == "full_docling" else row["baseline_output"])
        ).stat().st_size
    ]
    baseline_after = tree_state_digest(baseline_root)
    full_after = tree_state_digest(full_root)
    sha_provenance_problems = len(diagnostics["provenance_problems"]) + len(copy_mismatches)
    integrity = {
        "missing_final_outputs": len(missing_outputs),
        "empty_final_outputs": len(empty_outputs),
        "sha_provenance_problems": sha_provenance_problems,
        "baseline_changed": baseline_before != baseline_after,
        "full_docling_changed": full_before != full_after,
        "one_per_canonical": len(rows) == diagnostics["baseline_canonical"] and len({row["document_id"] for row in rows}) == len(rows),
    }
    integrity["go"] = not any([
        integrity["missing_final_outputs"], integrity["empty_final_outputs"],
        integrity["sha_provenance_problems"], integrity["baseline_changed"],
        integrity["full_docling_changed"], not integrity["one_per_canonical"],
        diagnostics["duplicate_document_ids"], diagnostics["duplicate_final_paths"],
        diagnostics["exact_duplicate_sha"],
    ])
    atomic_write(manifest_path, csv_payload(rows))
    atomic_write(report_path, audit_markdown(rows, diagnostics, integrity).encode("utf-8"))
    return {
        "go": integrity["go"], "total": len(rows),
        "full_docling": sum(row["selected_variant"] == "full_docling" for row in rows),
        "baseline": sum(row["selected_variant"] == "baseline" for row in rows),
        "quality_reject": diagnostics["quality_reject"],
        "no_improvement": diagnostics["no_improvement"],
        "persistent_failure": diagnostics["persistent_failure"],
        "changed_outputs": changed_outputs,
        "manifest": str(manifest_path), "report": str(report_path),
    }


def artifact_digest(project_root: Path) -> str:
    digest = hashlib.sha256()
    for path in (
        project_root / "data/metadata/final_corpus_manifest.csv",
        project_root / "reports/final_corpus_audit.md",
    ):
        digest.update(sha256_file(path).encode("ascii"))
    digest.update(tree_state_digest(project_root / "data/corpus_final").encode("ascii"))
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble one canonical final Markdown variant per document")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify-idempotent", action="store_true")
    args = parser.parse_args()
    try:
        summary = assemble(args.project_root)
        if args.verify_idempotent:
            first_digest = artifact_digest(args.project_root)
            second = assemble(args.project_root)
            second_digest = artifact_digest(args.project_root)
            if first_digest != second_digest or second["changed_outputs"] != 0:
                raise FinalCorpusError("Final Corpus Assembly idempotent değil")
            summary["idempotent"] = True
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["go"] else 2
    except FinalCorpusError as exc:
        print(f"NO-GO: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
