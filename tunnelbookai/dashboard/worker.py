"""Background worker that advances a population run one resumable batch at a time."""

from __future__ import annotations

import argparse
import traceback
from pathlib import Path

from tunnelbookai.ingest.paths import PROJECT_ROOT
from tunnelbookai.population.models import load_object
from tunnelbookai.population.runner import run_batch

from .controller import resolve_run, stop_path, update_control


def execute(run_value: str, project_root: Path | str | None = None) -> int:
    root = Path(project_root or PROJECT_ROOT).resolve()
    run_path = resolve_run(run_value, root)

    def stop_requested() -> bool:
        return stop_path(root).is_file()

    def progress(event: dict) -> None:
        update_control(
            root,
            status="STOP_REQUESTED" if stop_requested() else "RUNNING",
            current_document_id=event.get("document_id"),
            message="Belge güvenli checkpoint hattında işleniyor.",
        )

    try:
        update_control(root, status="RUNNING", message="Corpus population çalışıyor.")
        while True:
            run = load_object(run_path)
            pending_batches = [
                batch_id for batch_id in run["batch_ids"]
                if batch_id not in run["completed_batches"]
            ]
            if not pending_batches:
                update_control(
                    root,
                    status="FINISHED",
                    worker_pid=None,
                    current_batch_id=None,
                    current_document_id=None,
                    message="Bütün batch’ler işlendi; sonuçlar incelemeye hazır.",
                )
                return 0
            if stop_requested():
                update_control(
                    root,
                    status="PAUSED",
                    worker_pid=None,
                    current_batch_id=None,
                    current_document_id=None,
                    message="Checkpoint kaydedildi. Devam komutu bekleniyor.",
                )
                return 0
            batch_id = pending_batches[0]
            batch_path = root / "audit" / "corpus_population" / "batches" / f"{batch_id}.json"
            update_control(
                root,
                status="RUNNING",
                current_batch_id=batch_id,
                current_document_id=None,
                message="Sıradaki batch işleniyor.",
            )
            result = run_batch(
                batch_path,
                root,
                resume=True,
                stop_requested=stop_requested,
                progress_callback=progress,
            )
            if result["status"] == "PAUSED":
                update_control(
                    root,
                    status="PAUSED",
                    worker_pid=None,
                    current_batch_id=batch_id,
                    current_document_id=None,
                    message="Checkpoint kaydedildi. Devam komutu bekleniyor.",
                )
                return 0
            if int(result.get("exit_code") or 0) != 0:
                update_control(
                    root,
                    status="ERROR",
                    worker_pid=None,
                    current_batch_id=batch_id,
                    current_document_id=None,
                    message="Batch hata ile durdu; checkpoint üzerinden yeniden denenebilir.",
                    last_error=f"batch {batch_id} exit={result.get('exit_code')}",
                )
                return 2
    except BaseException as exc:
        traceback.print_exc()
        update_control(
            root,
            status="ERROR",
            worker_pid=None,
            current_document_id=None,
            message="Worker beklenmeyen hata ile durdu; tamamlanan checkpoint’ler korundu.",
            last_error=f"{type(exc).__name__}: {exc}"[:1000],
        )
        return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    return execute(args.run)


if __name__ == "__main__":
    raise SystemExit(main())
