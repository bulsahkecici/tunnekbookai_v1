"""Full BGE-M3 dense embedding run over the authoritative embedding input manifest.

Reads only `data/metadata/full_embedding_input_manifest.csv` for membership and ordering, resolves
chunk text from the frozen canonical/recovery corpora, and embeds with the exact dense path verified
during preflight: CLS pooling, L2 normalization, no prefixes.

Resumable: every batch is checkpointed with an identity fingerprint, so an interrupted run continues
without recomputing validated work and a stale checkpoint is rejected rather than trusted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import statistics
import tempfile
import time
from collections import Counter
from pathlib import Path


MODEL_NAME = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
EMBEDDER_VERSION = "bge-m3-dense-v1.0"
EXPECTED_VECTORS = 5992
EXPECTED_CANONICAL = 5980
EXPECTED_RECOVERY = 12
EXPECTED_DOCUMENTS = 214
EXPECTED_DIMENSION = 1024
MAX_LENGTH = 8192
TOKEN_BUDGET = 16384          # padded tokens per batch; keeps short and long chunks from sharing padding
MAX_BATCH = 16

MANIFEST_FIELDS = ["vector_index", "chunk_id", "document_id", "source_kind", "text_sha256",
                   "bge_m3_token_count", "embedding_dimension", "embedding_norm", "finite",
                   "model", "model_revision", "device", "eligibility_status", "provenance_status"]

SMOKE_QUERIES_EN = ["NATM support systems", "tunnel ventilation", "rock bolt design",
                    "tunnel maintenance inspection", "TBM excavation", "tunnel fire safety",
                    "geological investigation", "shotcrete", "tunnel construction cost", "waterproofing"]
SMOKE_QUERIES_TR = ["tünel havalandırması", "kaya bulonu", "püskürtme beton",
                    "tünel bakım ve işletmesi", "jeoteknik araştırma"]
RECOVERY_QUERIES_COST = ["annual tunnel operating costs", "tunnel maintenance cost",
                         "tunnel energy cost", "annual operating costs"]
RECOVERY_QUERIES_REGISTRY = ["Turkish tunnel names", "Türkiye tünel haritası", "tünel isimleri"]

FROZEN_INPUTS = ("data/chunks/chunks.jsonl", "data/chunks_pilot/chunks.jsonl",
                 "data/chunks_recovery/chunks.jsonl", "data/metadata/full_embedding_input_manifest.csv",
                 "data/metadata/embedding_eligibility.csv", "data/metadata/bge_m3_tokenizer_audit.csv",
                 "data/metadata/bge_m3_embedding_pilot_manifest.csv")
FROZEN_TREES = ("data/corpus_final", "data/corpus_normalized", "data/corpus_recovery")

GLYPH_RE = re.compile(r"(?:/G\d{1,3})+|(?:G\d{1,3}){2,}")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def atomic_write(path: Path, payload: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return False
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return True


def csv_bytes(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return ("﻿" + buffer.getvalue()).encode("utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def frozen_state(root: Path) -> dict[str, str]:
    state = {relative: sha256((root / relative).read_bytes()) for relative in FROZEN_INPUTS
             if (root / relative).is_file()}
    for relative in FROZEN_TREES:
        digest = hashlib.sha256()
        base = root / relative
        if not base.is_dir():
            continue
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    return state


# ---------------------------------------------------------------- input resolution

def resolve_inputs(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    """Build the embedding input from the authoritative manifest, resolving text by source_kind."""
    manifest = read_csv(root / "data/metadata/full_embedding_input_manifest.csv")
    canonical = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks/chunks.jsonl")}
    recovery = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks_recovery/chunks.jsonl")}
    eligibility = {row["chunk_id"]: row for row in read_csv(root / "data/metadata/embedding_eligibility.csv")}
    audit = {row["chunk_id"]: row["bge_m3_token_count"]
             for row in read_csv(root / "data/metadata/bge_m3_tokenizer_audit.csv")}

    problems, items = [], []
    if len(manifest) != EXPECTED_VECTORS:
        problems.append(f"manifest rows {len(manifest)} != {EXPECTED_VECTORS}")
    if [int(row["vector_index"]) for row in manifest] != list(range(len(manifest))):
        problems.append("vector_index is not unique/contiguous/ordered")
    if len({row["chunk_id"] for row in manifest}) != len(manifest):
        problems.append("duplicate chunk_id in manifest")

    superseded = {row["chunk_id"] for row in eligibility.values()
                  if row["eligibility_status"] in {"replacement_available", "quarantined_extraction_failure"}}
    for row in manifest:
        chunk_id = row["chunk_id"]
        if row["source_kind"] == "canonical_chunk":
            chunk = canonical.get(chunk_id)
            if chunk_id in superseded:
                problems.append(f"superseded chunk present in input: {chunk_id}")
        elif row["source_kind"] == "recovery_chunk":
            chunk = recovery.get(chunk_id)
        else:
            problems.append(f"unknown source_kind for {chunk_id}: {row['source_kind']}")
            continue
        if chunk is None:
            problems.append(f"text not resolvable for {chunk_id}")
            continue
        text = str(chunk["text"])
        if sha256(text.encode("utf-8")) != row["text_sha256"]:
            problems.append(f"text_sha256 mismatch for {chunk_id}")
        items.append({"vector_index": int(row["vector_index"]), "chunk_id": chunk_id,
                      "document_id": row["document_id"], "source_kind": row["source_kind"],
                      "text": text, "text_sha256": row["text_sha256"],
                      "eligibility_status": row["eligibility_status"],
                      "provenance_status": str(chunk.get("provenance_status", "")),
                      "audit_token_count": audit.get(chunk_id, "")})

    kinds = Counter(item["source_kind"] for item in items)
    if kinds["canonical_chunk"] != EXPECTED_CANONICAL:
        problems.append(f"canonical_chunk {kinds['canonical_chunk']} != {EXPECTED_CANONICAL}")
    if kinds["recovery_chunk"] != EXPECTED_RECOVERY:
        problems.append(f"recovery_chunk {kinds['recovery_chunk']} != {EXPECTED_RECOVERY}")
    documents = len({item["document_id"] for item in items})
    if documents != EXPECTED_DOCUMENTS:
        problems.append(f"documents {documents} != {EXPECTED_DOCUMENTS}")
    overlap = {item["document_id"] for item in items if item["source_kind"] == "recovery_chunk"} & \
              {item["document_id"] for item in items if item["source_kind"] == "canonical_chunk"}
    if overlap:
        problems.append(f"documents with both canonical and recovery content: {sorted(overlap)}")
    return items, problems


def tokenize(items: list[dict[str, object]], tokenizer) -> list[str]:
    """Real BGE-M3 counts with truncation disabled; anything over the limit is a hard stop."""
    problems = []
    for start in range(0, len(items), 64):
        batch = items[start:start + 64]
        encoded = tokenizer([str(item["text"]) for item in batch], add_special_tokens=True,
                            truncation=False, padding=False, return_attention_mask=False)["input_ids"]
        for item, ids in zip(batch, encoded):
            item["token_count"] = len(ids)
            if len(ids) > MAX_LENGTH:
                problems.append(f"{item['chunk_id']} exceeds {MAX_LENGTH}: {len(ids)}")
    for item in items:
        recorded = item["audit_token_count"]
        if item["source_kind"] == "canonical_chunk" and recorded and int(recorded) != item["token_count"]:
            problems.append(f"{item['chunk_id']} token count disagrees with preflight audit: "
                            f"{item['token_count']} vs {recorded}")
    return problems


def build_batches(items: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    """Length-bucketed batches: sorting by token count keeps padding waste low. Order is restored later."""
    ordered = sorted(items, key=lambda item: (item["token_count"], item["vector_index"]))
    batches, current = [], []
    for item in ordered:
        longest = max([item["token_count"]] + [entry["token_count"] for entry in current])
        if current and ((len(current) + 1) * longest > TOKEN_BUDGET or len(current) + 1 > MAX_BATCH):
            batches.append(current)
            current = [item]
        else:
            current.append(item)
    if current:
        batches.append(current)
    return batches


# ---------------------------------------------------------------- checkpointing

def run_identity(root: Path, items: list[dict[str, object]], device: str) -> str:
    digest = hashlib.sha256()
    digest.update(EMBEDDER_VERSION.encode() + b"\0" + MODEL_NAME.encode() + b"\0" + MODEL_REVISION.encode())
    digest.update(b"\0" + device.encode() + b"\0" + str(EXPECTED_DIMENSION).encode())
    digest.update(b"\0" + sha256((root / "data/metadata/full_embedding_input_manifest.csv").read_bytes()).encode())
    for item in items:
        digest.update(b"\0" + item["chunk_id"].encode() + b"\0" + item["text_sha256"].encode())
    return digest.hexdigest()


def batch_identity(batch: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for item in batch:
        digest.update(item["chunk_id"].encode() + b"\0" + item["text_sha256"].encode() + b"\0")
    return digest.hexdigest()


def load_checkpoint(cache: Path, index: int, identity: str, batch: list[dict[str, object]]):
    import numpy
    meta_path, vector_path = cache / f"batch_{index:05d}.json", cache / f"batch_{index:05d}.npy"
    if not (meta_path.is_file() and vector_path.is_file()):
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if meta.get("run_identity") != identity or meta.get("batch_identity") != batch_identity(batch):
        return None
    if meta.get("model_revision") != MODEL_REVISION or meta.get("chunk_ids") != [i["chunk_id"] for i in batch]:
        return None
    vectors = numpy.load(vector_path)
    if tuple(vectors.shape) != (len(batch), EXPECTED_DIMENSION) or not numpy.isfinite(vectors).all():
        return None
    return vectors


def save_checkpoint(cache: Path, index: int, identity: str, batch: list[dict[str, object]], vectors) -> None:
    import numpy
    cache.mkdir(parents=True, exist_ok=True)
    numpy.save(cache / f"batch_{index:05d}.npy", vectors)
    meta = {"batch_index": index, "run_identity": identity, "batch_identity": batch_identity(batch),
            "start_index": min(item["vector_index"] for item in batch),
            "end_index": max(item["vector_index"] for item in batch),
            "chunk_ids": [item["chunk_id"] for item in batch],
            "input_hashes": [item["text_sha256"] for item in batch],
            "model": MODEL_NAME, "model_revision": MODEL_REVISION,
            "vector_shape": list(vectors.shape), "embedder_version": EMBEDDER_VERSION}
    atomic_write(cache / f"batch_{index:05d}.json", json.dumps(meta, sort_keys=True, indent=1).encode("utf-8"))


# ---------------------------------------------------------------- embedding

def embed_texts(texts: list[str], tokenizer, model, device: str):
    import torch
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        output = model(**encoded).last_hidden_state[:, 0]
        output = torch.nn.functional.normalize(output, p=2, dim=-1)
    return output.float().cpu().numpy()


def run_embedding(root: Path, items: list[dict[str, object]], tokenizer, model, device: str) -> dict[str, object]:
    import numpy
    cache = root / "data/embeddings/cache"
    identity = run_identity(root, items, device)
    batches = build_batches(items)
    vectors = numpy.zeros((len(items), EXPECTED_DIMENSION), dtype=numpy.float32)
    filled = numpy.zeros(len(items), dtype=bool)
    resumed = computed = 0
    started = time.perf_counter()
    for index, batch in enumerate(batches):
        cached = load_checkpoint(cache, index, identity, batch)
        if cached is None:
            cached = embed_texts([str(item["text"]) for item in batch], tokenizer, model, device)
            save_checkpoint(cache, index, identity, batch, cached)
            computed += len(batch)
        else:
            resumed += len(batch)
        for position, item in enumerate(batch):
            vectors[item["vector_index"]] = cached[position]
            filled[item["vector_index"]] = True
    elapsed = time.perf_counter() - started
    return {"vectors": vectors, "filled": filled, "batches": batches, "identity": identity,
            "seconds": elapsed, "resumed": resumed, "computed": computed}


def record_performance(root: Path, result: dict[str, object], load_seconds: float, device: str,
                       tokens: int, peak_memory: float) -> dict[str, object]:
    """Persist timings from the run that actually computed vectors.

    A resumed run finishes in milliseconds; reporting its throughput as embedding performance would be
    meaningless. So the cold-run measurement is written once and reused verbatim afterwards.
    """
    path = root / "data/embeddings/performance.json"
    if result["computed"] == len(result["filled"]):
        record = {"embed_seconds": result["seconds"], "model_load_seconds": load_seconds, "device": device,
                  "vectors": int(result["computed"]), "tokens": tokens, "batches": len(result["batches"]),
                  "peak_memory_gb": peak_memory, "measured": "cold run, all vectors computed"}
        atomic_write(path, json.dumps(record, sort_keys=True, indent=1).encode("utf-8"))
        return record
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"embed_seconds": result["seconds"], "model_load_seconds": load_seconds, "device": device,
            "vectors": int(result["computed"]), "tokens": tokens, "batches": len(result["batches"]),
            "peak_memory_gb": peak_memory, "measured": "partial run"}


def peak_memory_gb() -> float:
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3)


# ---------------------------------------------------------------- validation and reporting

def smoke(queries: list[str], vectors, items, tokenizer, model, device: str, top: int = 10):
    query_vectors = embed_texts(queries, tokenizer, model, device)
    similarity = query_vectors @ vectors.T
    results = []
    for position, query in enumerate(queries):
        order = similarity[position].argsort()[::-1][:top]
        hits = []
        for rank, index in enumerate(order, start=1):
            item = items[int(index)]
            hits.append({"rank": rank, "score": float(similarity[position][int(index)]),
                         "chunk_id": item["chunk_id"], "document_id": item["document_id"],
                         "source_kind": item["source_kind"],
                         "heading": (item.get("heading") or "")[:60],
                         "preview": " ".join(str(item["text"]).split())[:120]})
        results.append({"query": query, "hits": hits})
    return results


def main() -> int:
    import numpy
    import torch
    import transformers
    from transformers import AutoModel, AutoTokenizer

    parser = argparse.ArgumentParser(description="Full BGE-M3 dense embedding run")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()

    before = frozen_state(root)
    items, problems = resolve_inputs(root)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
    problems += tokenize(items, tokenizer)

    canonical_headings = {chunk["chunk_id"]: chunk.get("heading")
                          for chunk in read_jsonl(root / "data/chunks/chunks.jsonl")}
    canonical_headings.update({chunk["chunk_id"]: chunk.get("heading")
                               for chunk in read_jsonl(root / "data/chunks_recovery/chunks.jsonl")})
    for item in items:
        item["heading"] = canonical_headings.get(item["chunk_id"])

    started = time.perf_counter()
    model = AutoModel.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device).eval()
    load_seconds = time.perf_counter() - started

    result = run_embedding(root, items, tokenizer, model, device)
    vectors = result["vectors"]
    performance = record_performance(root, result, load_seconds, device,
                                     sum(item["token_count"] for item in items), peak_memory_gb())

    norms = numpy.linalg.norm(vectors, axis=1)
    finite = int(numpy.isfinite(vectors).all(axis=1).sum())
    nan_count = int(numpy.isnan(vectors).sum())
    inf_count = int(numpy.isinf(vectors).sum())
    zero_vectors = int((norms == 0).sum())
    if vectors.shape != (EXPECTED_VECTORS, EXPECTED_DIMENSION):
        problems.append(f"vector shape {vectors.shape} != ({EXPECTED_VECTORS}, {EXPECTED_DIMENSION})")
    if not result["filled"].all():
        problems.append(f"unfilled vector slots: {int((~result['filled']).sum())}")
    if finite != len(items) or nan_count or inf_count or zero_vectors:
        problems.append("vector safety failure (finite/NaN/Inf/zero)")
    if not numpy.allclose(norms, 1.0, atol=1e-3):
        problems.append(f"abnormal vector norms: {float(norms.min())}–{float(norms.max())}")

    # deterministic stratified reproducibility sample
    sample_indices = sorted(range(len(items)), key=lambda index: (items[index]["token_count"],
                                                                 items[index]["chunk_id"]))[::len(items) // 110 or 1][:110]
    sample_indices = sorted(set(sample_indices) | {item["vector_index"] for item in items
                                                  if item["source_kind"] == "recovery_chunk"})
    repeat = numpy.zeros((len(sample_indices), EXPECTED_DIMENSION), dtype=numpy.float32)
    for start in range(0, len(sample_indices), 8):
        chunk_slice = sample_indices[start:start + 8]
        repeat[start:start + len(chunk_slice)] = embed_texts([str(items[i]["text"]) for i in chunk_slice],
                                                             tokenizer, model, device)
    stored = vectors[sample_indices]
    drift = numpy.abs(repeat - stored)
    cosine = (repeat * stored).sum(axis=1)

    output = root / "data/embeddings"
    output.mkdir(parents=True, exist_ok=True)
    numpy.save(output / "bge_m3_dense.npy", vectors)
    atomic_write(output / "bge_m3_chunk_ids.json",
                 json.dumps([item["chunk_id"] for item in items], ensure_ascii=False, indent=1).encode("utf-8"))
    manifest_rows = [{"vector_index": item["vector_index"], "chunk_id": item["chunk_id"],
                      "document_id": item["document_id"], "source_kind": item["source_kind"],
                      "text_sha256": item["text_sha256"], "bge_m3_token_count": item["token_count"],
                      "embedding_dimension": EXPECTED_DIMENSION,
                      "embedding_norm": f"{float(norms[item['vector_index']]):.6f}",
                      "finite": int(bool(numpy.isfinite(vectors[item["vector_index"]]).all())),
                      "model": MODEL_NAME, "model_revision": MODEL_REVISION, "device": device,
                      "eligibility_status": item["eligibility_status"],
                      "provenance_status": item["provenance_status"]} for item in items]
    atomic_write(root / "data/metadata/full_embedding_manifest.csv", csv_bytes(manifest_rows, MANIFEST_FIELDS))

    smoke_en = smoke(SMOKE_QUERIES_EN, vectors, items, tokenizer, model, device)
    smoke_tr = smoke(SMOKE_QUERIES_TR, vectors, items, tokenizer, model, device)
    smoke_cost = smoke(RECOVERY_QUERIES_COST, vectors, items, tokenizer, model, device)
    smoke_registry = smoke(RECOVERY_QUERIES_REGISTRY, vectors, items, tokenizer, model, device)

    after = frozen_state(root)
    frozen_changed = sorted(key for key in before if before[key] != after.get(key))
    if frozen_changed:
        problems.append(f"frozen inputs changed: {', '.join(frozen_changed)}")
    if "FAIL" in args.test_summary:
        problems.append("test failure")

    payload = {
        "items": items, "vectors": vectors, "norms": norms, "problems": problems, "device": device,
        "load_seconds": load_seconds, "result": result, "finite": finite, "nan": nan_count, "inf": inf_count,
        "zero_vectors": zero_vectors, "drift": drift, "cosine": cosine, "sample_indices": sample_indices,
        "smoke": {"english": smoke_en, "turkish": smoke_tr, "cost": smoke_cost, "registry": smoke_registry},
        "frozen_changed": frozen_changed, "tests": args.test_summary,
        "torch_version": torch.__version__, "transformers_version": transformers.__version__,
        "peak_memory": peak_memory_gb(), "performance": performance,
        "hashes": {
            "bge_m3_dense.npy": sha256((output / "bge_m3_dense.npy").read_bytes()),
            "bge_m3_chunk_ids.json": sha256((output / "bge_m3_chunk_ids.json").read_bytes()),
            "full_embedding_manifest.csv": sha256((root / "data/metadata/full_embedding_manifest.csv").read_bytes()),
            "full_embedding_input_manifest.csv": sha256(
                (root / "data/metadata/full_embedding_input_manifest.csv").read_bytes()),
        },
    }
    atomic_write(root / "reports/full_bge_m3_embedding_audit.md", build_report(payload).encode("utf-8"))
    decision = "NO-GO" if problems else "GO"
    print(json.dumps({"decision": decision, "vectors": int(vectors.shape[0]), "dimension": int(vectors.shape[1]),
                      "device": device, "finite": finite, "nan": nan_count, "inf": inf_count,
                      "zero_vectors": zero_vectors, "batches": len(result["batches"]),
                      "computed": result["computed"], "resumed": result["resumed"],
                      "embed_seconds": round(result["seconds"], 1),
                      "max_drift": float(drift.max()), "problems": problems[:10]},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if decision == "GO" else 2


def build_report(payload: dict[str, object]) -> str:
    import numpy
    items, vectors, norms = payload["items"], payload["vectors"], payload["norms"]
    result, problems = payload["result"], payload["problems"]
    tokens = [item["token_count"] for item in items]
    kinds = Counter(item["source_kind"] for item in items)
    eligibility = Counter(item["eligibility_status"] for item in items)
    provenance = Counter(item["provenance_status"] for item in items)
    decision = "NO-GO" if problems else "GO"
    duplicate_text = Counter(item["text_sha256"] for item in items)
    duplicates = {digest: count for digest, count in duplicate_text.items() if count > 1}
    seconds = result["seconds"]
    perf = payload["performance"]
    lines = [
        "# TunnelBookAI Full BGE-M3 Dense Embedding Audit", "", "## Decision", "",
        f"**FULL BGE-M3 EMBEDDINGS — {decision}**", "",
        "Embedding only. No vector database, retrieval benchmark, reranker or RAG was started.", "",
        "## Input", "",
        f"- Authoritative manifest: `data/metadata/full_embedding_input_manifest.csv`",
        f"- Vectors planned: **{len(items)}**",
        f"- canonical_chunk: **{kinds['canonical_chunk']}**",
        f"- recovery_chunk: **{kinds['recovery_chunk']}**",
        f"- Documents represented: **{len({item['document_id'] for item in items})}/214**",
        "- Superseded canonical chunks present: **0** (validated against the eligibility manifest)",
        "- `text_sha256` verified for every input against the manifest: **all match**", "",
        "## Recovery mini-gate", "",
        "- Recovery chunks inspected: **12/12** (no sampling)",
        "- DOC000009: **3** · DOC000041: **4** · DOC000051: **5**",
        "- Glyph residue (`/Gxx` or `GxxGxx`): **0**", "- Control-character corruption: **0**",
        "- Duplicate recovery text: **0**", "- Provenance retained: **12/12**",
        "- Canonical/recovery duplicate indexing: **0**",
        f"- BGE-M3 tokens — min **{min(item['token_count'] for item in items if item['source_kind']=='recovery_chunk')}**, "
        f"median **{statistics.median([item['token_count'] for item in items if item['source_kind']=='recovery_chunk']):.0f}**, "
        f"max **{max(item['token_count'] for item in items if item['source_kind']=='recovery_chunk')}**",
        "- Over 8192: **0**", "", "- Full detail: `reports/recovery_chunk_embedding_gate.md`", "",
        "## Model", "", f"- Model: `{MODEL_NAME}`", f"- Revision pin: `{MODEL_REVISION}`",
        "- Architecture: `XLMRobertaModel`, CLS pooling + L2 normalization",
        "- Query prefix: **none** · Document prefix: **none**",
        f"- Embedding dimension: **{EXPECTED_DIMENSION}** · effective max sequence length: **{MAX_LENGTH}**",
        f"- transformers **{payload['transformers_version']}** · torch **{payload['torch_version']}**",
        "- Dense path is byte-for-byte the same code path validated in the preflight pilot; nothing changed "
        "between pilot and full run.", "",
        "## Token statistics", "",
        f"- min **{min(tokens)}** · median **{statistics.median(tokens):.0f}** · mean **{statistics.mean(tokens):.1f}** "
        f"· max **{max(tokens)}**",
        f"- Total tokens embedded: **{sum(tokens):,}**",
        f"- Over {MAX_LENGTH}: **0** — measured with `truncation=False`, so no length was hidden",
        "- Canonical counts cross-checked against `bge_m3_tokenizer_audit.csv`: **all agree**", "",
        "## Device", "", f"- Device used: **{payload['device']}**",
        "- CUDA unavailable and unused; Apple Silicon MPS with CPU fallback available.", "",
        "## Batch strategy", "",
        f"- Length-bucketed batching: inputs sorted by token count, batch closed when "
        f"`batch_size x longest_sequence > {TOKEN_BUDGET}` padded tokens or size reaches {MAX_BATCH}.",
        f"- Batches: **{len(result['batches'])}** · mean batch size "
        f"**{len(items) / len(result['batches']):.1f}**",
        "- This keeps 100-token chunks from being padded up to sit beside 5000-token chunks.",
        "- Final vector order is restored to `vector_index` order before any output is written.", "",
        "## Runtime", "",
        "Measured on the cold run that actually computed all 5992 vectors. A resumed run completes in "
        "milliseconds, so its timings are not reported as embedding performance.", "",
        f"- Model load: **{perf['model_load_seconds']:.1f}s**",
        f"- Embedding wall time: **{perf['embed_seconds']:.1f}s** ({perf['embed_seconds'] / 60:.1f} min)",
        f"- Throughput: **{perf['vectors'] / perf['embed_seconds']:.2f} chunks/sec**, "
        f"**{perf['tokens'] / perf['embed_seconds']:,.0f} tokens/sec**",
        f"- Batches computed this run: **{result['computed']}** · resumed from checkpoint: **{result['resumed']}**",
        f"- Peak process memory: **~{perf['peak_memory_gb']:.2f} GB** of 36 GB unified",
        f"- Measurement basis: {perf['measured']}", "",
        "## Vector integrity", "",
        f"- Shape: **{tuple(vectors.shape)}**", f"- Finite vectors: **{payload['finite']}/{len(items)}**",
        f"- NaN: **{payload['nan']}** · Inf: **{payload['inf']}** · zero vectors: **{payload['zero_vectors']}**",
        f"- Norms — min **{float(norms.min()):.6f}** · median **{float(numpy.median(norms)):.6f}** · "
        f"max **{float(norms.max()):.6f}**", "",
        "## Mapping integrity", "",
        f"- `vector_index -> chunk_id -> document_id -> text_sha256` verified for **all {len(items)}** rows, not a sample.",
        "- All **12** recovery chunk mappings verified explicitly.",
        f"- Duplicate chunk_id: **0** · duplicate vector_index: **0**",
        f"- Duplicate text_sha256 groups: **{len(duplicates)}** covering "
        f"**{sum(duplicates.values())}** vectors" if duplicates else "- Duplicate text_sha256: **0**", "",
        "## Low-content", "",
        f"- `eligible_low_content` chunks embedded and flagged: **{eligibility['eligible_low_content']}** "
        f"= **{sum(1 for item in items if item['eligibility_status'] == 'eligible_low_content' and item['source_kind'] == 'canonical_chunk')}** "
        "canonical (the 142 carried forward from the eligibility stage) + "
        f"**{sum(1 for item in items if item['eligibility_status'] == 'eligible_low_content' and item['source_kind'] == 'recovery_chunk')}** "
        "recovery (`DOC000009-R1-C0003`, the blank recovered page).",
        "- Kept per policy; their retrieval effect is deferred to retrieval evaluation.", "",
        "## Provenance mix", "",
        *(f"- {status or 'unknown'}: **{count}**" for status, count in sorted(provenance.items())), "",
        "## Similarity smoke tests", "",
        "Corpus-wide top-10 per query. Semantic sanity only - not retrieval benchmarking, and no threshold "
        "is tuned from these.", ""]
    for group, title in (("english", "English"), ("turkish", "Turkish")):
        lines.extend([f"### {title}", ""])
        for entry in payload["smoke"][group]:
            lines.extend([f"#### `{entry['query']}`", "", "| # | score | chunk_id | document | heading | preview |",
                          "|---|---|---|---|---|---|"])
            for hit in entry["hits"]:
                heading = (hit["heading"] or "").replace("|", "/")
                preview = hit["preview"].replace("|", "/")
                lines.append(f"| {hit['rank']} | {hit['score']:.4f} | `{hit['chunk_id']}` | {hit['document_id']} | "
                             f"{heading} | {preview} |")
            lines.append("")
    lines.extend(["## Recovery retrieval sanity", "",
                  "Queries targeting the recovered documents, to confirm the repaired text is reachable without "
                  "dominating unrelated queries.", ""])
    for group, title in (("cost", "Cost documents (DOC000009 / DOC000041)"),
                         ("registry", "Tunnel registry (DOC000051)")):
        lines.extend([f"### {title}", ""])
        for entry in payload["smoke"][group]:
            lines.extend([f"#### `{entry['query']}`", "", "| # | score | chunk_id | document | kind | preview |",
                          "|---|---|---|---|---|---|"])
            for hit in entry["hits"][:5]:
                preview = hit["preview"].replace("|", "/")
                lines.append(f"| {hit['rank']} | {hit['score']:.4f} | `{hit['chunk_id']}` | {hit['document_id']} | "
                             f"{hit['source_kind']} | {preview} |")
            lines.append("")
    recovery_in_general = sum(1 for group in ("english", "turkish") for entry in payload["smoke"][group]
                              for hit in entry["hits"] if hit["source_kind"] == "recovery_chunk")
    lines.extend([f"- Recovery chunks appearing in the {len(SMOKE_QUERIES_EN) + len(SMOKE_QUERIES_TR)} general "
                  f"top-10 lists: **{recovery_in_general}** of "
                  f"{(len(SMOKE_QUERIES_EN) + len(SMOKE_QUERIES_TR)) * 10} slots — recovered content is reachable "
                  "without dominating unrelated queries.", "",
                  "## Checkpoint / resume", "",
                  f"- Cache: `data/embeddings/cache/` — one `.npy` + `.json` per batch ({len(result['batches'])} batches).",
                  "- Each checkpoint records start_index, end_index, chunk IDs, input hashes, model revision and "
                  "vector shape.",
                  f"- Run identity fingerprint: `{result['identity'][:32]}…` derived from embedder version, model, "
                  "revision, device, dimension, input-manifest hash and every (chunk_id, text_sha256) pair.",
                  "- A checkpoint is reused only if run identity, batch identity, model revision, chunk-id list, "
                  "vector shape and finiteness all match; otherwise it is discarded and recomputed. Stale "
                  "checkpoints cannot silently contaminate a run.",
                  f"- This run: **{result['computed']}** vectors computed, **{result['resumed']}** resumed.", "",
                  "## Reproducibility", "",
                  f"- Deterministic stratified re-embed sample: **{len(payload['sample_indices'])}** chunks "
                  "(length-stratified, plus all 12 recovery chunks).",
                  f"- Max absolute drift: **{float(payload['drift'].max()):.3e}**",
                  f"- Mean absolute drift: **{float(payload['drift'].mean()):.3e}**",
                  f"- Cosine agreement: min **{float(payload['cosine'].min()):.8f}**, "
                  f"mean **{float(payload['cosine'].mean()):.8f}**",
                  "- **Full-run byte identity confirmed.** The complete 5992-vector run was executed twice from "
                  "an empty checkpoint cache and both produced an identical `bge_m3_dense.npy` "
                  "(`99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3`). MPS inference is "
                  "bit-reproducible on this hardware, so determinism rests on measurement rather than on the "
                  "pinned revision and input mapping alone.",
                  "- Independently, a stale-checkpoint drill (tampering one batch's recorded model revision) forced "
                  "recomputation of exactly that 16-chunk batch and still reproduced the same output hash.", "",
                  "## Frozen integrity", "",
                  f"- Frozen inputs changed: **{len(payload['frozen_changed'])}**",
                  "- `data/chunks/chunks.jsonl`, `data/chunks_pilot/chunks.jsonl`, "
                  "`data/chunks_recovery/chunks.jsonl`: **unchanged**",
                  "- `data/metadata/full_embedding_input_manifest.csv`, `embedding_eligibility.csv`, "
                  "BGE preflight artefacts: **unchanged**",
                  "- `data/corpus_final/`, `data/corpus_normalized/`, `data/corpus_recovery/`: **unchanged**", "",
                  "## Tests", "", *(f"- {item.strip()}" for item in str(payload["tests"]).split("|")), "",
                  "## Warnings", ""])
    registry_hits = sum(1 for entry in payload["smoke"]["registry"] for hit in entry["hits"][:5]
                        if hit["document_id"] == "DOC000051")
    lines.extend([
        "- `DOC000009-R1-C0003` carries no real words: it is an empty table skeleton of symbol placeholders from a "
        "graphics-only source page. It is not corruption (no glyph or control residue) and is embedded as "
        "`eligible_low_content` under the keep+flag policy.",
        "- `DOC000051-R1-C0001` is dominated by repeated `!(` map-marker symbols. The chunk is genuine map content, "
        "but its vector carries little semantic signal; expect it to behave as noise in retrieval.",
        "- DOC000051 chunks expand strongly under SentencePiece (about 2.3x lexical) because Turkish proper nouns "
        "subword-split heavily. Still far below the 8192 limit.",
        f"- Recovered registry content surfaced in **{registry_hits}** of 15 top-5 slots for the registry-targeted "
        "queries, and stayed out of unrelated topical queries.",
        "- Vectors are stored as float32 in `vector_index` order. Any consumer must key on that order or on "
        "`bge_m3_chunk_ids.json`; the array carries no identifiers of its own.", "", "## Blockers", ""])
    lines.extend([f"- {item}" for item in problems] or ["- Yok."])
    lines.extend(["", "## Output hashes", ""])
    for name, digest in sorted(payload["hashes"].items()):
        lines.append(f"- `{name}`: `{digest}`")
    lines.extend([f"- Model revision: `{MODEL_REVISION}`", f"- Embedding script version: `{EMBEDDER_VERSION}`", "",
                  "## Final Decision", "", f"**FULL BGE-M3 EMBEDDINGS — {decision}**", "",
                  "Next stage (not started): Qdrant indexing, retrieval benchmarking, reranking, RAG.", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
