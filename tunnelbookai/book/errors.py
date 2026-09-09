"""Explicit fail-closed errors for the Book Production Engine."""

from __future__ import annotations

from typing import Any


class BookEngineError(RuntimeError):
    """Base exception carrying a stable operator-facing reason code."""

    def __init__(self, code: str, message: str, *, details: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = details


class ContractValidationError(BookEngineError):
    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__("BOOK_CONTRACT_INVALID", message, details=details)


class InputValidationError(BookEngineError):
    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__("BOOK_INPUT_INVALID", message, details=details)


class EvidenceBoundaryError(BookEngineError):
    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__("NON_CANONICAL_EVIDENCE_REJECTED", message, details=details)


class ReferenceIntegrityError(BookEngineError):
    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__("INVALID_EVIDENCE_REFERENCE", message, details=details)
