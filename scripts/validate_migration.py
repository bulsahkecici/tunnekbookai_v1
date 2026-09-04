#!/usr/bin/env python3
"""Verify the copy-first TunnelBookAI V1 migration and write its manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = PROJECT_ROOT.parent
CRAWLER_SOURCE = PROJECTS_ROOT / "paper-crawler-agent"
TUNNELBOOK_SOURCE = PROJECTS_ROOT / "tunnel" / "_TunnelBookAI"
BOOK_PACKAGE_SOURCE = PROJECT_ROOT / "tunnelbookai_v1_book_inputs" / "book"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def files(root: Path) -> list[Path]:
    excluded = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.name != ".DS_Store" and path.suffix != ".pyc" and not (set(path.parts) & excluded)
    )


def git(source: Path) -> dict:
    def run(*args: str) -> str:
        result = subprocess.run(["git", *args], cwd=source, text=True, capture_output=True, check=False)
        return result.stdout.strip()
    return {
        "source_project": str(source),
        "source_git_root": str(source),
        "branch": run("branch", "--show-current"),
        "head_commit": run("rev-parse", "HEAD"),
        "remote": run("remote", "get-url", "origin"),
        "dirty": bool(run("status", "--short")),
    }


def compare_tree(source: Path, destination: Path, label: str) -> tuple[list[dict], list[str], list[str]]:
    verified: list[dict] = []
    missing: list[str] = []
    mismatches: list[str] = []
    for src in files(source):
        relative = src.relative_to(source)
        dst = destination / relative
        name = f"{label}/{relative.as_posix()}"
        if not dst.is_file():
            missing.append(name)
            continue
        source_hash = sha256(src)
        destination_hash = sha256(dst)
        if source_hash != destination_hash:
            mismatches.append(name)
            continue
        verified.append({"file": name, "sha256": source_hash, "size": src.stat().st_size})
    return verified, missing, mismatches


def count_files(roots: Iterable[Path]) -> int:
    return sum(len(files(root)) for root in roots if root.exists())


def main() -> int:
    mappings = [
        (BOOK_PACKAGE_SOURCE, PROJECT_ROOT / "book", "book"),
        (TUNNELBOOK_SOURCE / "data" / "corpus_final", PROJECT_ROOT / "corpus" / "canonical", "corpus/canonical"),
        (TUNNELBOOK_SOURCE / "data" / "metadata", PROJECT_ROOT / "corpus" / "metadata", "corpus/metadata"),
        (TUNNELBOOK_SOURCE / "data" / "temp" / "full_docling_chunks", PROJECT_ROOT / "corpus" / "sidecars" / "full_docling_chunks", "corpus/sidecars"),
    ]
    verified: list[dict] = []
    missing: list[str] = []
    mismatches: list[str] = []
    for source, destination, label in mappings:
        ok, absent, changed = compare_tree(source, destination, label)
        verified.extend(ok); missing.extend(absent); mismatches.extend(changed)

    crawler_py = list((PROJECT_ROOT / "crawler" / "src").glob("*.py"))
    crawler_tests = list((PROJECT_ROOT / "crawler" / "tests").glob("test_*.py"))
    canonical = list((PROJECT_ROOT / "corpus" / "canonical").rglob("*.md"))
    metadata = files(PROJECT_ROOT / "corpus" / "metadata")
    sidecars = files(PROJECT_ROOT / "corpus" / "sidecars")
    book_files = files(PROJECT_ROOT / "book")
    nested_git = [str(path) for path in PROJECT_ROOT.rglob(".git") if path != PROJECT_ROOT / ".git"]
    migrated_venv = [str(path) for path in PROJECT_ROOT.rglob("*") if path.is_dir() and path.name in {".venv", "venv"}]
    critical = {
        "crawler_catalog": PROJECT_ROOT / "data" / "downloads" / "catalog.json",
        "crawler_index": PROJECT_ROOT / "data" / "downloads" / "index.jsonl",
        "classification_index": PROJECT_ROOT / "data" / "downloads" / "classification_index.jsonl",
        "pipeline_state": PROJECT_ROOT / "data" / "downloads" / "audit" / "pipeline_state.json",
        "corpus_manifest": PROJECT_ROOT / "corpus" / "metadata" / "final_corpus_manifest.csv",
        "metadata_master": PROJECT_ROOT / "corpus" / "metadata" / "final_metadata_master.csv",
        "book_scope": PROJECT_ROOT / "book" / "scope" / "normalized" / "book_scope.json",
        "question_bank": PROJECT_ROOT / "book" / "question_bank" / "normalized" / "question_bank.jsonl",
    }
    critical_hashes = {name: sha256(path) for name, path in critical.items() if path.is_file()}
    checks = {
        "crawler_source_exists": bool(crawler_py),
        "corpus_exists": bool(canonical),
        "corpus_metadata_exists": bool(metadata),
        "sidecars_preserved": bool(sidecars),
        "tests_preserved": bool(crawler_tests),
        "config_preserved": bool(files(PROJECT_ROOT / "crawler" / "config")),
        "existing_book_package_preserved": len(book_files) >= len(files(BOOK_PACKAGE_SOURCE)),
        "no_critical_hash_mismatch": not mismatches,
        "no_critical_missing_files": not missing,
        "no_nested_git": not nested_git,
        "no_virtual_environment_migrated": not migrated_venv,
    }
    skipped_generated = count_files([
        CRAWLER_SOURCE / ".venv", TUNNELBOOK_SOURCE / ".venv",
        TUNNELBOOK_SOURCE / "data" / "archives",
        TUNNELBOOK_SOURCE / "data" / "converted_office",
        TUNNELBOOK_SOURCE / "data" / "temp" / "model_cache",
    ])
    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": str(PROJECT_ROOT),
        "sources": [git(CRAWLER_SOURCE), git(TUNNELBOOK_SOURCE), {"source_project": str(BOOK_PACKAGE_SOURCE), "source_git_root": None}],
        "migrated_files": count_files([PROJECT_ROOT / "crawler", PROJECT_ROOT / "corpus", PROJECT_ROOT / "data" / "downloads", PROJECT_ROOT / "book", PROJECT_ROOT / "scripts", PROJECT_ROOT / "tests"]),
        "skipped_generated_files": skipped_generated,
        "verified_files": len(verified),
        "hash_mismatches": len(mismatches),
        "missing_files": len(missing),
        "conflicts": [
            "README/config/tests collision resolved by crawler namespace and unified root layout",
            "prepared book package retained as canonical book input; legacy data/book did not overwrite it",
        ],
        "intentional_target_changes": [
            "crawler source paths normalized for crawler/src + crawler/config layout",
            "crawler taxonomy aligned to all 66 canonical scope IDs",
            "crawler regression tests extended for migration, review, and taxonomy behavior",
        ],
        "missing": missing,
        "mismatches": mismatches,
        "critical_hashes": critical_hashes,
        "counts": {
            "crawler_python_modules": len(crawler_py),
            "crawler_tests": len(crawler_tests),
            "canonical_markdown_documents": len(canonical),
            "metadata_files": len(metadata),
            "sidecar_files": len(sidecars),
            "book_files": len(book_files),
        },
        "integrity_gate": checks,
        "decision": "PASS" if all(checks.values()) else "NO_GO",
        "source_projects_safe_to_archive": False,
        "archive_note": "Paper crawler can be archived after final target tests; old TunnelBookAI remains KEEP because raw/derived stores outside canonical migration scope were intentionally not copied.",
        "verified_file_inventory": verified,
    }
    destination = PROJECT_ROOT / "audit" / "migration_manifest.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in ("decision", "migrated_files", "verified_files", "hash_mismatches", "missing_files", "counts", "integrity_gate")}, ensure_ascii=False, indent=2))
    return 0 if manifest["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
