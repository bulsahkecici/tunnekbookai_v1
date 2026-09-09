"""Stable, fail-closed errors for controlled canonical promotion."""

from __future__ import annotations

from typing import Any


class CanonicalError(RuntimeError):
    def __init__(self, code: str, message: str, *, details: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = details


POLICY_EXIT = 2
ATOMIC_EXIT = 3
