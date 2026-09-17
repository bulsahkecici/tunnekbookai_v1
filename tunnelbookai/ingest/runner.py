"""Public single-writer entry point used by corpus-population orchestration."""

from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable

from . import cli
from .sources import DiscoveredInput


def run_selected(
    inputs: list[DiscoveredInput], *, outcome_callback: Callable[[dict], None] | None = None,
    progress_callback: Callable[[dict], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
    resume: bool = True, force_reprocess: bool = False, no_ocr: bool = False,
    no_vision: bool = False, no_arbiter: bool = False,
) -> int:
    """Run selected discovered inputs through the existing Unified Ingest engine."""
    args = Namespace(
        resume=resume,
        force_reprocess=force_reprocess,
        no_ocr=no_ocr,
        no_vision=no_vision,
        no_arbiter=no_arbiter,
        no_chunking=False,
        embedding_server=None,
        embedding_model=None,
        llm_server=None,
        llm_model=None,
        outcome_callback=outcome_callback,
        progress_callback=progress_callback,
        should_stop=should_stop,
    )
    return cli._run(inputs, [], args)


__all__ = ["run_selected"]
