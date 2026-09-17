"""Quarantine stale staging and reset six current quality failures for reprocessing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tunnelbookai.population.models import PopulationState, atomic_json, load_object, now


QUALITY_FAILURE_BATCHES = {
    "ING_1c5a56abfaae6e524858": "CPB_3b9303d1c141fca00c3297de9d30de23393c0e2652b55057deed1ba6886dceb8",
    "ING_296bae6c6d0e76f84818": "CPB_969c9a9f037b2fe51d32dc52c4fdc68a4d1f640ee7576405c0f685db5799fee7",
    "ING_746d18498e07a8a0f397": "CPB_cf18c5c2c51ff6555aafdc21a850c97cee390076290feb71143c5f5e8c55df07",
    "ING_e5a3c44428f7d13e2a85": "CPB_50a6acee15c7bd138927125d25e88beef2651afe27cf4f8b2592199b1379f8c4",
    "ING_017a281e3b7e47690da6": "CPB_d261c0de9c7434ebec2eb9b5d6c39e56db92de9168c24eeb218a5d7673aeb23e",
    "ING_991a4bf2e475e795b041": "CPB_205ab196a58bc83bb75cb021967153a4dc36a769a4a96f7ddfce6262910738b4",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--recovery-root", required=True, type=Path)
    parser.add_argument(
        "--only", action="append", choices=sorted(QUALITY_FAILURE_BATCHES),
        help="reset only the named document; repeat for multiple documents",
    )
    parser.add_argument("--report-name", default="quality_recovery_reset.json")
    args = parser.parse_args()

    run = load_object(args.run)
    audit = load_object(args.audit)
    quality_ids = set(args.only or QUALITY_FAILURE_BATCHES)
    # Stale staging was part of the original full reset. Targeted retries must
    # not revisit that already-quarantined population.
    stale_ids = [] if args.only else sorted(
        row["document_id"] for row in audit["ineligible_staging"]
        if row["document_id"] not in set(QUALITY_FAILURE_BATCHES)
    )
    quarantine = args.recovery_root / "stale_staging_quarantine"
    quarantine.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    for document_id in stale_ids:
        source = Path("corpus/staging/v2") / document_id
        target = quarantine / document_id
        if source.is_dir():
            if target.exists():
                raise RuntimeError(f"quarantine target exists: {target}")
            source.rename(target)
            moved.append(document_id)
        elif not target.is_dir():
            raise RuntimeError(f"stale staging directory missing: {document_id}")

    for document_id, batch_id in QUALITY_FAILURE_BATCHES.items():
        if document_id not in quality_ids:
            continue
        previous = dict(run["documents"][document_id])
        run["documents"][document_id] = {
            "document_id": document_id,
            "disposition": "RECOVERY_REQUIRED",
            "engine_state": previous.get("engine_state"),
            "recovery_reason": "STAGING_AUDIT_CHUNK_QUALITY_FAILED",
            "previous_outcome": previous,
        }
        run["completed_batches"] = [
            value for value in run["completed_batches"] if value != batch_id
        ]
    run["state"] = PopulationState.INGESTING.value
    run["updated_at"] = now()
    atomic_json(args.run, run)

    report = {
        "reset_at": now(),
        "quality_failure_documents": sorted(quality_ids),
        "batches_reopened": sorted({
            batch_id for document_id, batch_id in QUALITY_FAILURE_BATCHES.items()
            if document_id in quality_ids
        }),
        "stale_staging_quarantined": moved,
    }
    atomic_json(args.recovery_root / args.report_name, report, readonly=True)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
