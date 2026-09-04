#!/usr/bin/env python3
"""Content-addressed cache for LLM audit calls.

Purpose: stop the "retry the same model call until it happens to PASS"
pattern. An audit identity is the exact tuple of everything that could
change the model's answer:

    sha256(draft_bytes + packet_bytes + prompt_bytes + model + model_config + contract_version)

Only a *deterministically gated* result (one that already passed the
relevant hard gate) is ever cached. A HOLD is never cached: HOLD means
the draft must change (revision), which changes draft_bytes and therefore
the key — so there is nothing useful to cache for a HOLD, and caching it
would only make it easier to hide a rejected result and re-ask later.

This module never talks to an LLM itself. Callers ask `get()` before
invoking the model, and `put()` after a call passes its hard gate.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class AuditCacheError(RuntimeError):
    pass


def compute_key(
    *,
    draft_path: Path,
    packet_path: Path,
    prompt_path: Path,
    model: str,
    contract_version: str,
    model_config: dict | None = None,
) -> str:
    h = hashlib.sha256()

    for path in (draft_path, packet_path, prompt_path):
        h.update(path.read_bytes())
        h.update(b"\x00")

    h.update(model.encode("utf-8"))
    h.update(b"\x00")
    h.update(
        json.dumps(model_config or {}, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )
    h.update(b"\x00")
    h.update(contract_version.encode("utf-8"))

    return h.hexdigest()


class AuditCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _entry_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> dict | None:
        path = self._entry_path(key)

        if not path.exists():
            return None

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise AuditCacheError(
                f"CORRUPT_AUDIT_CACHE_ENTRY: {path}: {exc}"
            ) from exc

    def put(
        self,
        key: str,
        *,
        section_id: str,
        kind: str,
        audit_json: dict,
        gate_result: dict,
    ) -> Path:
        path = self._entry_path(key)

        entry = {
            "key": key,
            "section_id": section_id,
            "kind": kind,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "audit": audit_json,
            "gate_result": gate_result,
        }

        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))

            if existing.get("audit") != audit_json:
                raise AuditCacheError(
                    f"AUDIT_CACHE_COLLISION: {key} already holds a "
                    "different validated audit; cache entries are "
                    "immutable"
                )

            return path

        path.write_text(
            json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        return path
