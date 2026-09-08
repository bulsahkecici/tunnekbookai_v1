#!/usr/bin/env python3
"""Create the blocking recoverability gate for the legacy corpus reset.

The reset may empty active corpus/original/processing state, but it must not make
any source byte sequence unrecoverable.  This tool records one JSONL row per
legacy source artifact and verifies recovery either from committed Git history
(canonical text only) or from a byte-identical source outside reset targets.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RESET_ROOTS = (
    ROOT / "corpus" / "canonical",
    ROOT / "corpus" / "staging",
    ROOT / "corpus" / "metadata",
    ROOT / "originals",
    ROOT / "processing",
)
RECOVERY_ROOTS = {
    "external_archive": ROOT / "data" / "downloads",
    "papercrawler_source": ROOT / "incoming" / "papercrawler" / "releases",
    "legacy_papercrawler_source": ROOT / "incoming" / "crawler" / "releases",
    "manual_source": ROOT / "incoming" / "manual" / "inbox",
    "verified_test_fixture": ROOT / "tests" / "ingest" / "fixtures",
}
SOURCE_SUFFIXES = {".pdf", ".docx", ".pptx", ".xlsx", ".png", ".jpg", ".jpeg", ".txt", ".md", ".csv", ".html", ".rtf"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def is_git_tracked(path: Path) -> bool:
    """Ask Git about the filesystem path directly.

    macOS file names can be decomposed while Git's index retains composed Unicode;
    comparing Python strings from ``git ls-files`` would falsely mark those files
    as untracked.  Git pathspec resolution is the authority here.
    """
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def is_source(path: Path) -> bool:
    if path.suffix.lower() not in SOURCE_SUFFIXES:
        return False
    if path.is_relative_to(ROOT / "corpus" / "canonical"):
        return True
    return path.name.startswith("source.")


def legacy_sources() -> Iterable[tuple[str, Path]]:
    for root, kind in (
        (ROOT / "corpus" / "canonical", "canonical_text"),
        (ROOT / "corpus" / "staging", "staging_source"),
        (ROOT / "originals", "original_source"),
    ):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and is_source(path):
                yield kind, path


@dataclass(frozen=True)
class RecoveryMatch:
    category: str
    path: str


def recovery_index(target_sizes: set[int]) -> dict[int, list[tuple[str, Path]]]:
    by_size: dict[int, list[tuple[str, Path]]] = defaultdict(list)
    for category, root in RECOVERY_ROOTS.items():
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
                size = path.stat().st_size
                if size in target_sizes:
                    by_size[size].append((category, path))
    return by_size


def main() -> int:
    sources = list(legacy_sources())
    size_index = recovery_index({path.stat().st_size for _, path in sources})
    rows: list[dict[str, object]] = []
    unrecoverable: list[dict[str, object]] = []

    for artifact_type, path in sources:
        path_rel = rel(path)
        digest = sha256(path)
        matches: list[RecoveryMatch] = []
        for category, candidate in size_index[path.stat().st_size]:
            if sha256(candidate) == digest:
                matches.append(RecoveryMatch(category, rel(candidate)))
        is_tracked = is_git_tracked(path)
        git_recoverable = is_tracked and artifact_type == "canonical_text"
        row = {
            "document_id": path.parent.name if path.name.startswith("source.") else path.stem,
            "content_sha256": digest,
            "current_path": path_rel,
            "artifact_type": artifact_type,
            "tracked_by_git": is_tracked,
            "recoverable_from_git": git_recoverable,
            "recoverable_from_external_archive": any(m.category == "external_archive" for m in matches),
            "recoverable_from_papercrawler_source": any("papercrawler_source" in m.category for m in matches),
            "recoverable_from_manual_source": any(m.category == "manual_source" for m in matches),
            "recoverable_from_other_verified_copy": [m.path for m in matches if m.category not in {"external_archive", "manual_source", "papercrawler_source", "legacy_papercrawler_source"}],
            "verified_recovery_locations": [m.path for m in matches],
            "planned_action": "RESET_ACTIVE_STATE_AFTER_GATE",
        }
        if not (git_recoverable or matches):
            row["blocking_reason"] = "UNRECOVERABLE_UNIQUE_SOURCE"
            unrecoverable.append(row)
        rows.append(row)

    audit_dir = ROOT / "audit"
    reports_dir = ROOT / "reports"
    audit_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    audit_path = audit_dir / "pre_reset_recoverability.jsonl"
    audit_path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")

    delete_plan = []
    for root in RESET_ROOTS:
        files = [path for path in root.rglob("*") if path.is_file()] if root.is_dir() else []
        delete_plan.append({
            "path": rel(root),
            "absolute_path": str(root.resolve()),
            "is_descendant_of_repo_root": root.resolve().is_relative_to(ROOT.resolve()),
            "file_count": len(files),
            "planned_action": "EMPTY_CONTENT_KEEP_DIRECTORY",
        })
    (audit_dir / "pre_reset_delete_plan.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in delete_plan), encoding="utf-8"
    )

    decision = "GO" if not unrecoverable else "NO_GO"
    lines = [
        "# Pre-reset Recoverability Gate",
        "",
        f"Decision: **{decision}**",
        "",
        f"- Legacy source artifacts audited: {len(rows)}",
        f"- Unrecoverable unique sources: {len(unrecoverable)}",
        "- Recovery locations were SHA-256 verified; Git recovery is accepted only for tracked canonical text.",
        "- Active reset targets are listed in `audit/pre_reset_delete_plan.jsonl`.",
        "",
        "## Result",
        "",
    ]
    if unrecoverable:
        lines += ["**NO_GO — UNRECOVERABLE_UNIQUE_SOURCE**", ""]
        lines += [f"- `{row['current_path']}`" for row in unrecoverable]
    else:
        lines += ["Every legacy source byte sequence has at least one verified recovery route outside the active state slated for reset."]
    (reports_dir / "pre_reset_recoverability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"decision": decision, "sources": len(rows), "unrecoverable": len(unrecoverable)}))
    return 0 if decision == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
