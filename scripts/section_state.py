#!/usr/bin/env python3
"""Immutable, versioned revision checkpoints for a section's draft/audit cycle.

Each revision (R0, R1, R2, ...) gets its own directory holding an exact
snapshot of draft, sentence_map, evidence_audit and editorial_audit at
that point in time. A directory is written once and never overwritten,
so an R1 PASS artifact can never be silently clobbered by an R2 attempt,
and rollback means "copy R{n} back out", not "hope an overwrite didn't
happen yet".
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class SectionStateError(RuntimeError):
    pass


ARTIFACT_NAMES = (
    "draft.md",
    "sentence_map.json",
    "evidence_audit_input.txt",
    "evidence_audit.json",
    "editorial_input.txt",
    "editorial_audit.json",
    "state.json",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def revisions_root(remediation_dir: Path) -> Path:
    return remediation_dir / "revisions"


def revision_dir(remediation_dir: Path, revision: int) -> Path:
    return revisions_root(remediation_dir) / f"r{revision}"


def checkpoint_revision(
    *,
    remediation_dir: Path,
    revision: int,
    draft_path: Path,
    sentence_map_path: Path,
    evidence_audit_path: Path,
    editorial_audit_path: Path | None,
    status: str,
    evidence_audit_input_path: Path | None = None,
    editorial_input_path: Path | None = None,
    state: dict | None = None,
) -> Path:
    """Snapshot the current artifacts as revision R{revision}.

    Fails closed if the revision directory already exists — revisions
    are write-once. Missing optional artifacts (e.g. editorial_audit
    before the first editorial pass) are simply omitted.
    """

    target = revision_dir(remediation_dir, revision)

    if target.exists():
        raise SectionStateError(
            f"REVISION_ALREADY_CHECKPOINTED: r{revision}"
        )

    target.mkdir(parents=True)

    sources = {
        "draft.md": draft_path,
        "sentence_map.json": sentence_map_path,
        "evidence_audit_input.txt": evidence_audit_input_path,
        "evidence_audit.json": evidence_audit_path,
        "editorial_input.txt": editorial_input_path,
        "editorial_audit.json": editorial_audit_path,
    }

    hashes: dict[str, str] = {}

    for name, source in sources.items():
        if source is None or not source.exists():
            continue

        data = source.read_bytes()
        (target / name).write_bytes(data)
        hashes[name] = sha256_bytes(data)

    if state is not None:
        state_bytes = (
            json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        (target / "state.json").write_bytes(state_bytes)
        hashes["state.json"] = sha256_bytes(state_bytes)

    manifest = {
        "revision": revision,
        "status": status,
        "checkpointed_at": datetime.now(timezone.utc).isoformat(),
        "artifact_sha256": hashes,
    }

    (target / "revision_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return target


def load_revision_manifest(remediation_dir: Path, revision: int) -> dict:
    path = revision_dir(remediation_dir, revision) / "revision_manifest.json"

    if not path.exists():
        raise SectionStateError(f"REVISION_NOT_FOUND: r{revision}")

    return json.loads(path.read_text(encoding="utf-8"))


def restore_revision(
    *,
    remediation_dir: Path,
    revision: int,
    draft_path: Path,
    sentence_map_path: Path,
    evidence_audit_path: Path,
    editorial_audit_path: Path | None,
    evidence_audit_input_path: Path | None = None,
    editorial_input_path: Path | None = None,
) -> dict:
    """Restore working artifacts from a checkpointed revision.

    Verifies each restored file's hash against the revision manifest
    before returning — a tampered or corrupted checkpoint is rejected
    rather than silently used to roll back into.
    """

    source_dir = revision_dir(remediation_dir, revision)
    manifest = load_revision_manifest(remediation_dir, revision)
    hashes = manifest.get("artifact_sha256", {})

    targets = {
        "draft.md": draft_path,
        "sentence_map.json": sentence_map_path,
        "evidence_audit_input.txt": evidence_audit_input_path,
        "evidence_audit.json": evidence_audit_path,
        "editorial_input.txt": editorial_input_path,
        "editorial_audit.json": editorial_audit_path,
    }

    restored = []

    for name, dest in targets.items():
        source = source_dir / name

        if not source.exists():
            continue

        data = source.read_bytes()
        expected = hashes.get(name)

        if expected and sha256_bytes(data) != expected:
            raise SectionStateError(
                f"REVISION_CHECKPOINT_HASH_MISMATCH: r{revision}: {name}"
            )

        if dest is None:
            continue

        dest.write_bytes(data)
        restored.append(name)

    return {"revision": revision, "restored": restored}


def list_revisions(remediation_dir: Path) -> list[int]:
    root = revisions_root(remediation_dir)

    if not root.exists():
        return []

    out = []

    for child in root.iterdir():
        if child.is_dir() and child.name.startswith("r"):
            try:
                out.append(int(child.name[1:]))
            except ValueError:
                continue

    return sorted(out)
