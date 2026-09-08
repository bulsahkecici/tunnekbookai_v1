"""Fresh claim audit for the Phase C confirmation run.

Reuses the audit tooling from scripts/28 rather than reimplementing it, but re-derives every
deterministic label against the fresh answers. Prior manual labels are carried only where the
audited bytes are literally identical, and anything unresolved is reported for hand review.

scripts/28 resolves the contract-results path relative to its own ROOT constant. Rather than
overwrite the frozen v1 results artifact to redirect it, ROOT is pointed at a scratch tree that
holds only the fresh results; every other input is bound to its real absolute path. No frozen
artifact is written to at any point.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "data/evaluation"
FRESH_RAW = EV / "generation_output_contract_v1_1_fresh_raw.jsonl"
FRESH_RESULTS = EV / "generation_output_contract_v1_1_fresh_results.jsonl"
OUT = EV / "generation_output_contract_v1_1_fresh_claim_audit.jsonl"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def build():
    ca = _load("claim_audit", "scripts/28_output_contract_claim_audit.py")
    scratch = Path(tempfile.mkdtemp(prefix="tunnelbook_fresh_audit_"))
    try:
        redirected = scratch / "data/evaluation"
        redirected.mkdir(parents=True)
        shutil.copyfile(FRESH_RESULTS,
                        redirected / "generation_output_contract_eval_results_v1.jsonl")
        ca.ROOT = scratch                      # only the inline contract-results lookup follows this
        ca.RAW = FRESH_RAW                     # every other input stays bound to its real path
        ca.PACKETS = EV / "generation_eval_benchmark_v2_packets.jsonl"
        ca.PHASE_B_RESULTS = EV / "generation_eval_results_v2.jsonl"
        ca.PHASE_B_CLAIMS = EV / "generation_claim_audit_v2.jsonl"
        ca.OVERRIDES = EV / "generation_output_contract_claim_manual_v1.json"
        ca.OUT = OUT
        return ca.build()
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    import collections
    result = build()
    rows, unresolved = result["rows"], result["unresolved"]
    material = [r for r in rows if r["material"]]
    print(f"claims={len(rows)} material={len(material)} nonfactual={len(rows) - len(material)}")
    print(collections.Counter(r["claim_label"] for r in rows))
    print(collections.Counter(r["label_method"] for r in rows))
    print(f"UNRESOLVED requiring manual review: {len(unresolved)}")
    for r in unresolved:
        print(f"  {r['query_id']} {r['claim_id']} cited={r['cited_evidence_ids']} "
              f"{r['claim_text'][:110]}")
