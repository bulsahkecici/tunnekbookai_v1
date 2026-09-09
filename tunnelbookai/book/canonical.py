"""Book-facing compatibility adapter for the sole canonical verifier."""

from __future__ import annotations

from pathlib import Path

from tunnelbookai.canonical.models import CanonicalInventory
from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.verifier import inspect_canonical

from .contract import BookContract
from .errors import EvidenceBoundaryError, InputValidationError


class CanonicalEvidenceAccess:
    def __init__(self, contract: BookContract) -> None:
        self.contract = contract
        self.context = CanonicalContext.load(contract.project_root)
        self.root = self.context.canonical_root
        self.manifest_path = self.context.manifest_path

    def assert_canonical_path(self, path: Path | str) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.contract.project_root / candidate
        resolved = candidate.resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise EvidenceBoundaryError(
                "book evidence path is outside corpus/canonical", details={"path": str(path)}
            )
        return resolved

    def inspect(self) -> CanonicalInventory:
        return inspect_canonical(context=self.context)


def require_ready_canonical(access: CanonicalEvidenceAccess) -> CanonicalInventory:
    inventory = access.inspect()
    if not inventory.ready:
        raise InputValidationError("canonical evidence is not ready", details=inventory.to_dict())
    return inventory


__all__ = ["CanonicalEvidenceAccess", "CanonicalInventory", "require_ready_canonical"]
