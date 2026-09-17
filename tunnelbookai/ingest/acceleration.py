"""Resolve local inference acceleration without weakening offline guarantees."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


ACCELERATOR_ENV = "TUNNELBOOKAI_ACCELERATOR"
OCR_ACCELERATOR_ENV = "TUNNELBOOKAI_OCR_ACCELERATOR"
SUPPORTED_ACCELERATORS = {"auto", "cpu", "cuda", "mps"}


@dataclass(frozen=True)
class AcceleratorSelection:
    requested: str
    resolved: str
    reason: str


def _torch_device_available(device: str) -> bool:
    try:
        import torch
    except ImportError:
        return False

    if device == "cuda":
        return bool(torch.cuda.is_available())
    if device == "mps":
        return bool(torch.backends.mps.is_built() and torch.backends.mps.is_available())
    return device == "cpu"


def resolve_accelerator(config: Any) -> AcceleratorSelection:
    """Choose CUDA/MPS when available and otherwise fall back deterministically to CPU.

    The environment override is intentionally outside the population config identity so an
    existing checkpoint can move between machines without invalidating its immutable plan.
    The resolved device is still written to each extraction report for provenance.
    """
    ocr = getattr(config, "ocr", {}) or {}
    requested = str(os.environ.get(ACCELERATOR_ENV, ocr.get("accelerator", "auto"))).lower()
    if requested not in SUPPORTED_ACCELERATORS:
        allowed = ", ".join(sorted(SUPPORTED_ACCELERATORS))
        raise ValueError(f"unsupported accelerator {requested!r}; expected one of: {allowed}")

    if requested == "auto":
        for candidate in ("cuda", "mps"):
            if _torch_device_available(candidate):
                return AcceleratorSelection(requested, candidate, f"auto_selected_{candidate}")
        return AcceleratorSelection(requested, "cpu", "no_supported_gpu_available")

    if requested != "cpu" and not _torch_device_available(requested):
        return AcceleratorSelection(requested, "cpu", f"{requested}_unavailable_cpu_fallback")
    return AcceleratorSelection(requested, requested, "explicit_selection")


def resolve_ocr_accelerator(config: Any) -> AcceleratorSelection:
    """Choose the RapidOCR device, defaulting to CPU for long-run stability.

    RapidOCR's torch MPS backend can abort the entire process in native MPSGraph
    deallocation code.  That failure bypasses Python exception handling, so the safe
    default must be selected before the engine is created.  MPS/CUDA remain available
    as an explicit opt-in through ``TUNNELBOOKAI_OCR_ACCELERATOR``.
    """
    ocr = getattr(config, "ocr", {}) or {}
    configured = ocr.get("ocr_accelerator")
    overridden = os.environ.get(OCR_ACCELERATOR_ENV)
    if overridden is None and configured is None:
        return AcceleratorSelection("cpu", "cpu", "rapidocr_stability_default")

    requested = str(overridden if overridden is not None else configured).lower()
    if requested not in SUPPORTED_ACCELERATORS:
        allowed = ", ".join(sorted(SUPPORTED_ACCELERATORS))
        raise ValueError(f"unsupported OCR accelerator {requested!r}; expected one of: {allowed}")
    if requested == "auto":
        for candidate in ("cuda", "mps"):
            if _torch_device_available(candidate):
                return AcceleratorSelection(requested, candidate, f"auto_selected_{candidate}")
        return AcceleratorSelection(requested, "cpu", "no_supported_gpu_available")
    if requested != "cpu" and not _torch_device_available(requested):
        return AcceleratorSelection(requested, "cpu", f"{requested}_unavailable_cpu_fallback")
    return AcceleratorSelection(requested, requested, "explicit_selection")


def rapidocr_torch_params(device: str) -> dict[str, bool]:
    """Return explicit, mutually exclusive RapidOCR torch device flags."""
    return {
        "EngineConfig.torch.use_cuda": device == "cuda",
        "EngineConfig.torch.use_mps": device == "mps",
    }


__all__ = [
    "ACCELERATOR_ENV",
    "OCR_ACCELERATOR_ENV",
    "AcceleratorSelection",
    "rapidocr_torch_params",
    "resolve_accelerator",
    "resolve_ocr_accelerator",
]
