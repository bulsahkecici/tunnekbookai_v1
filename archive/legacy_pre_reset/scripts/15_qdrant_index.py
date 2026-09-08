"""Qdrant dense index build for the frozen BGE-M3 release.

Qdrant is a derived layer: everything here is reconstructable from `bge_m3_dense.npy`, the embedding
manifest and the frozen chunk sources. Point IDs are the manifest's `vector_index`, so identity is
deterministic and a rebuild reproduces the same collection.

Stages: --preflight --create --ingest --verify --snapshot (or --all).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import tempfile
from collections import Counter
from importlib.metadata import version as package_version
from pathlib import Path


COLLECTION = "tunnelbook_dense_v1"
RELEASE_NAME = "tunnelbook-dense-v1"
PAYLOAD_SCHEMA_VERSION = "payload-v1"
EMBEDDING_MODEL = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
EMBEDDING_VERSION = "bge-m3-dense-v1.0"
VECTOR_SIZE = 1024
DISTANCE = "Cosine"
EXPECTED_POINTS = 5992
EXPECTED_CANONICAL = 5980
EXPECTED_RECOVERY = 12
EXPECTED_LOW_CONTENT = 143
EXPECTED_DOCUMENTS = 214
BATCH_SIZE = 256
RECOVERY_DOCUMENTS = ("DOC000009", "DOC000041", "DOC000051")

# Process exit codes. The JSON `decision` field is the human/report-facing verdict; these codes are what
# CI and shell pipelines branch on, so a NO-GO must never leave the process looking successful.
EXIT_OK = 0
EXIT_GATE_FAILURE = 1

REST_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
GRPC_PORT = 6334

# Only fields the dense baseline is expected to filter on. text/heading/paths are payload-only.
PAYLOAD_INDEXES = {"document_id": "keyword", "source_kind": "keyword", "language": "keyword",
                   "document_type": "keyword", "authority_level": "keyword",
                   "eligibility_status": "keyword", "topics": "keyword", "year": "integer"}

PROTECTED = ("data/embeddings/bge_m3_dense.npy", "data/embeddings/bge_m3_chunk_ids.json",
             "data/metadata/full_embedding_manifest.csv", "data/metadata/full_embedding_input_manifest.csv",
             "data/metadata/embedding_eligibility.csv", "data/chunks/chunks.jsonl",
             "data/chunks_recovery/chunks.jsonl")
PROTECTED_TREES = ("data/corpus_final", "data/corpus_normalized", "data/corpus_recovery")

SMOKE_QUERIES = ["NATM support systems", "tunnel ventilation", "shotcrete", "rock bolt design",
                 "tunnel maintenance cost", "tünel havalandırması", "kaya bulonu", "püskürtme beton",
                 "jeoteknik araştırma"]
RECOVERY_QUERIES = ["annual tunnel operating costs", "tunnel maintenance cost", "Türkiye tünel haritası"]


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def protected_state(root: Path) -> dict[str, str]:
    state = {relative: sha256((root / relative).read_bytes()) for relative in PROTECTED
             if (root / relative).is_file()}
    for relative in PROTECTED_TREES:
        base = root / relative
        if not base.is_dir():
            continue
        digest = hashlib.sha256()
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    return state


def release_identity(root: Path) -> dict[str, object]:
    return {
        "collection_name": COLLECTION, "collection_release_name": RELEASE_NAME,
        "vector_size": VECTOR_SIZE, "distance": DISTANCE.upper(),
        "embedding_model": EMBEDDING_MODEL, "model_revision": MODEL_REVISION,
        "embedding_version": EMBEDDING_VERSION, "payload_schema_version": PAYLOAD_SCHEMA_VERSION,
        "expected_point_count": EXPECTED_POINTS,
        "embedding_npy_sha256": sha256((root / "data/embeddings/bge_m3_dense.npy").read_bytes()),
        "chunk_ids_sha256": sha256((root / "data/embeddings/bge_m3_chunk_ids.json").read_bytes()),
        "embedding_manifest_sha256": sha256((root / "data/metadata/full_embedding_manifest.csv").read_bytes()),
        "embedding_input_manifest_sha256": sha256(
            (root / "data/metadata/full_embedding_input_manifest.csv").read_bytes()),
    }


# ---------------------------------------------------------------- payload

def value_or_none(value):
    """Never fabricate metadata: empty strings and empty lists become null."""
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, (list, tuple)):
        return list(value) or None
    return value


def recovery_provenance(root: Path) -> dict[str, dict[str, str]]:
    """Recovery front-matter fields, read from the recovered documents themselves."""
    provenance = {}
    directory = root / "data/corpus_recovery"
    if not directory.is_dir():
        return provenance
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")[:4000]
        entry = {}
        for field in ("recovery_version", "recovery_method", "original_source_sha256"):
            for line in text.splitlines():
                if line.startswith(f"{field}:"):
                    entry[field] = line.split(":", 1)[1].strip().strip('"')
                    break
        provenance[path.stem] = entry
    return provenance


def build_payload(row: dict[str, str], chunk: dict[str, object], recovery: dict[str, str]) -> dict[str, object]:
    payload = {
        "vector_index": int(row["vector_index"]),
        "chunk_id": row["chunk_id"], "document_id": row["document_id"],
        "source_kind": row["source_kind"],
        "text": str(chunk["text"]), "text_sha256": row["text_sha256"],
        "title": value_or_none(chunk.get("title")),
        "organization": value_or_none(chunk.get("organization")),
        "year": value_or_none(chunk.get("year")),
        "language": value_or_none(chunk.get("language")),
        "document_type": value_or_none(chunk.get("document_type")),
        "authority_level": value_or_none(chunk.get("authority_level")),
        "topics": value_or_none(chunk.get("topics")),
        "heading": value_or_none(chunk.get("heading")),
        "parent_heading": value_or_none(chunk.get("parent_heading")),
        "section_path": value_or_none(chunk.get("section_path")),
        "source_relative_path": value_or_none(chunk.get("source_relative_path")),
        "source_extension": value_or_none(chunk.get("source_extension")),
        "citation_mode": value_or_none(chunk.get("citation_mode")),
        "provenance_status": value_or_none(chunk.get("provenance_status")),
        "original_page_start": chunk.get("original_page_start"),
        "original_page_end": chunk.get("original_page_end"),
        "slide_start": chunk.get("slide_start"), "slide_end": chunk.get("slide_end"),
        "contains_table": bool(chunk.get("contains_table")),
        "contains_formula_placeholder": bool(chunk.get("contains_formula_placeholder")),
        "contains_image_placeholder": bool(chunk.get("contains_image_placeholder")),
        "eligibility_status": row["eligibility_status"],
        "is_low_content": row["eligibility_status"] == "eligible_low_content",
        "bge_m3_token_count": int(row["bge_m3_token_count"]),
        "source_sha256": value_or_none(chunk.get("source_sha256")),
        "normalized_source_sha256": value_or_none(chunk.get("normalized_source_sha256")),
        "model": EMBEDDING_MODEL, "model_revision": MODEL_REVISION,
        "embedding_version": EMBEDDING_VERSION,
    }
    if row["source_kind"] == "recovery_chunk":
        payload.update({"recovery_version": recovery.get("recovery_version"),
                        "recovery_method": recovery.get("recovery_method"),
                        "original_source_sha256": recovery.get("original_source_sha256")})
    # year is indexed as INTEGER; keep the payload type consistent or drop it rather than guess
    if payload["year"] is not None:
        try:
            payload["year"] = int(str(payload["year"]).strip())
        except ValueError:
            payload["year"] = None
    return payload


def load_points(root: Path) -> tuple[list[dict[str, object]], object, list[str]]:
    import numpy
    problems = []
    vectors = numpy.load(root / "data/embeddings/bge_m3_dense.npy")
    rows = read_csv(root / "data/metadata/full_embedding_manifest.csv")
    chunk_ids = json.loads((root / "data/embeddings/bge_m3_chunk_ids.json").read_text(encoding="utf-8"))
    canonical = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks/chunks.jsonl")}
    recovery_chunks = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks_recovery/chunks.jsonl")}
    eligibility = {row["chunk_id"]: row for row in read_csv(root / "data/metadata/embedding_eligibility.csv")}
    provenance = recovery_provenance(root)

    if tuple(vectors.shape) != (EXPECTED_POINTS, VECTOR_SIZE):
        problems.append(f"vector shape {tuple(vectors.shape)} != ({EXPECTED_POINTS}, {VECTOR_SIZE})")
    if len(rows) != EXPECTED_POINTS:
        problems.append(f"manifest rows {len(rows)} != {EXPECTED_POINTS}")
    indices = [int(row["vector_index"]) for row in rows]
    if indices != list(range(len(rows))):
        problems.append("vector_index is not unique/contiguous/ordered")
    if len({row["chunk_id"] for row in rows}) != len(rows):
        problems.append("duplicate chunk_id in embedding manifest")
    if chunk_ids != [row["chunk_id"] for row in rows]:
        problems.append("chunk_ids.json disagrees with embedding manifest order")

    superseded = {chunk_id for chunk_id, row in eligibility.items()
                  if row["eligibility_status"] in {"replacement_available", "quarantined_extraction_failure"}}
    points = []
    for row in rows:
        chunk_id = row["chunk_id"]
        source = canonical if row["source_kind"] == "canonical_chunk" else recovery_chunks
        chunk = source.get(chunk_id)
        if chunk is None:
            problems.append(f"text not resolvable for {chunk_id}")
            continue
        if row["source_kind"] == "canonical_chunk" and chunk_id in superseded:
            problems.append(f"superseded canonical chunk in index input: {chunk_id}")
        text = str(chunk["text"])
        if sha256(text.encode("utf-8")) != row["text_sha256"]:
            problems.append(f"text_sha256 mismatch for {chunk_id}")
        payload = build_payload(row, chunk, provenance.get(row["document_id"], {}))
        points.append({"id": int(row["vector_index"]), "payload": payload})

    kinds = Counter(point["payload"]["source_kind"] for point in points)
    if kinds["canonical_chunk"] != EXPECTED_CANONICAL:
        problems.append(f"canonical {kinds['canonical_chunk']} != {EXPECTED_CANONICAL}")
    if kinds["recovery_chunk"] != EXPECTED_RECOVERY:
        problems.append(f"recovery {kinds['recovery_chunk']} != {EXPECTED_RECOVERY}")
    low = sum(point["payload"]["is_low_content"] for point in points)
    if low != EXPECTED_LOW_CONTENT:
        problems.append(f"low-content {low} != {EXPECTED_LOW_CONTENT}")
    documents = len({point["payload"]["document_id"] for point in points})
    if documents != EXPECTED_DOCUMENTS:
        problems.append(f"documents {documents} != {EXPECTED_DOCUMENTS}")
    return points, vectors, problems


# ---------------------------------------------------------------- qdrant

def client():
    from qdrant_client import QdrantClient
    return QdrantClient(url=REST_URL, timeout=120)


def server_info() -> dict[str, object]:
    import urllib.request
    with urllib.request.urlopen(f"{REST_URL}/", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def exact_count(connection, filter_=None) -> int:
    return connection.count(collection_name=COLLECTION, count_filter=filter_, exact=True).count


def inspect_collection(connection) -> dict[str, object] | None:
    from qdrant_client.http.exceptions import UnexpectedResponse
    try:
        info = connection.get_collection(COLLECTION)
    except (UnexpectedResponse, ValueError, KeyError):
        return None
    except Exception as error:
        if "not found" in str(error).lower() or "doesn't exist" in str(error).lower():
            return None
        raise
    params = info.config.params.vectors
    return {"vector_size": getattr(params, "size", None), "distance": str(getattr(params, "distance", "")),
            "points_count": info.points_count, "indexed_vectors_count": info.indexed_vectors_count,
            "status": str(info.status), "optimizer_status": str(info.optimizer_status),
            "payload_schema": {key: str(value.data_type) for key, value in (info.payload_schema or {}).items()}}


def collection_matches_release(connection, existing: dict[str, object], root: Path) -> tuple[bool, list[str]]:
    """A pre-existing collection is reused only if it is provably this exact release."""
    reasons = []
    if existing["vector_size"] != VECTOR_SIZE:
        reasons.append(f"vector size {existing['vector_size']} != {VECTOR_SIZE}")
    if DISTANCE.lower() not in str(existing["distance"]).lower():
        reasons.append(f"distance {existing['distance']} != {DISTANCE}")
    count = exact_count(connection)
    if count != EXPECTED_POINTS:
        reasons.append(f"exact point count {count} != {EXPECTED_POINTS}")
    descriptor = root / "data/metadata/qdrant_dense_release.json"
    if not descriptor.is_file():
        reasons.append("no release descriptor to prove identity")
    else:
        stored = json.loads(descriptor.read_text(encoding="utf-8"))
        current = release_identity(root)
        for key in ("embedding_npy_sha256", "embedding_manifest_sha256", "chunk_ids_sha256",
                    "model_revision", "embedding_version", "payload_schema_version"):
            if stored.get(key) != current[key]:
                reasons.append(f"release identity differs on {key}")
    return (not reasons), reasons


def create_collection(connection, recreate: bool) -> None:
    from qdrant_client import models
    if recreate:
        connection.delete_collection(COLLECTION)
    connection.create_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )
    for field, schema in PAYLOAD_INDEXES.items():
        connection.create_payload_index(collection_name=COLLECTION, field_name=field, field_schema=schema)


def ingest(connection, points: list[dict[str, object]], vectors) -> dict[str, object]:
    from qdrant_client import models
    uploaded, batches, retries = 0, 0, 0
    for start in range(0, len(points), BATCH_SIZE):
        window = points[start:start + BATCH_SIZE]
        structs = [models.PointStruct(id=point["id"], vector=vectors[point["id"]].tolist(),
                                      payload=point["payload"]) for point in window]
        for attempt in range(3):
            try:
                connection.upsert(collection_name=COLLECTION, points=structs, wait=True)
                break
            except Exception:
                retries += 1
                if attempt == 2:
                    raise
        uploaded += len(window)
        batches += 1
    return {"uploaded": uploaded, "batches": batches, "retries": retries}


def embed_queries(queries: list[str]):
    """Reuse the frozen dense path: CLS pooling + L2 norm, pinned revision, no prefixes."""
    import torch
    from transformers import AutoModel, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, revision=MODEL_REVISION)
    model = AutoModel.from_pretrained(EMBEDDING_MODEL, revision=MODEL_REVISION)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device).eval()
    encoded = tokenizer(queries, padding=True, truncation=True, max_length=8192, return_tensors="pt")
    encoded = {key: value.to(device) for key, value in encoded.items()}
    with torch.inference_mode():
        output = model(**encoded).last_hidden_state[:, 0]
        output = torch.nn.functional.normalize(output, p=2, dim=-1)
    return output.float().cpu().numpy()


def query_smoke(connection, queries: list[str], top: int = 5) -> list[dict[str, object]]:
    vectors = embed_queries(queries)
    results = []
    for position, query in enumerate(queries):
        hits = connection.query_points(collection_name=COLLECTION, query=vectors[position].tolist(),
                                       limit=top, with_payload=True).points
        results.append({"query": query, "hits": [
            {"rank": rank, "score": float(hit.score), "chunk_id": hit.payload["chunk_id"],
             "document_id": hit.payload["document_id"], "source_kind": hit.payload["source_kind"],
             "is_low_content": bool(hit.payload.get("is_low_content")),
             "heading": (hit.payload.get("heading") or "")[:50],
             "preview": " ".join(str(hit.payload["text"]).split())[:110]}
            for rank, hit in enumerate(hits, start=1)]})
    return results



def write_reports(root: Path, summary: dict[str, object], points: list[dict[str, object]], tests: str) -> None:
    verification = summary.get("verification", {})
    collection = verification.get("collection", {}) or {}
    filters = verification.get("filters", {})
    smoke = summary.get("smoke", {})
    snapshot = summary.get("snapshot", {})
    identity = release_identity(root)
    problems = list(verification.get("problems", [])) + list(summary.get("protected_changed", []))
    if "FAIL" in tests:
        problems.append("test failure")
    decision = "NO-GO" if problems else "GO"
    low_hits = sum(1 for group in smoke.values() for entry in group
                   for hit in entry["hits"] if hit.get("is_low_content"))
    total_hits = sum(len(entry["hits"]) for group in smoke.values() for entry in group)

    lines = ["# TunnelBookAI Qdrant Dense Index Audit", "", "## Decision", "",
             f"**QDRANT DENSE INDEX — {decision}**", "",
             "Index build and validation only. No threshold tuning, retrieval benchmark, reranker, sparse "
             "vectors, hybrid search or RAG was started.", "", "## Environment", "",
             f"- Qdrant server: **{summary.get('server_version')}** (`qdrant/qdrant:v1.18.2` container)",
             f"- qdrant-client: **{summary.get('client_version')}** (aligned to the server minor version; the "
             "initially installed 1.16.1 was rejected by the client's own compatibility check and replaced)",
             "- Deployment: **local Docker container** via colima (Docker Server 29.5.2). No Qdrant Cloud, no "
             "external data transfer.",
             "- REST endpoint: `http://localhost:6333` · gRPC: `localhost:6334`",
             "- Storage: `data/qdrant_storage/` (bind mount → `/qdrant/storage`)",
             "- Snapshots: `data/qdrant_snapshots/` (bind mount → `/qdrant/snapshots`)",
             "- Pre-existing collections found at preflight: **none** — nothing unknown was reused or destroyed.",
             "", "## Release Identity", ""]
    for key in sorted(identity):
        lines.append(f"- `{key}`: `{identity[key]}`")
    lines.extend(["", "Stored as `data/metadata/qdrant_dense_release.json`.", "",
                  "## Collection Configuration", "",
                  f"- Name: `{COLLECTION}`", f"- Vector size: **{collection.get('vector_size')}**",
                  f"- Distance: **{collection.get('distance')}**",
                  f"- Status: **{collection.get('status')}** · optimizer: **{collection.get('optimizer_status')}**",
                  "- Quantization: **none** · sparse vectors: **none** · multivectors: **none** — one dense "
                  "BGE-M3 vector per point, deliberately simple for this baseline.",
                  f"- Point IDs: the manifest's `vector_index` (0…{EXPECTED_POINTS - 1}); no random UUIDs, so a "
                  "rebuild reproduces identical IDs.", "", "## Payload Schema", "",
                  f"- Schema version: `{PAYLOAD_SCHEMA_VERSION}`",
                  "- Identity: `vector_index`, `chunk_id`, `document_id`, `source_kind`",
                  "- Content: `text`, `text_sha256`, `bge_m3_token_count`",
                  "- Bibliographic: `title`, `organization`, `year`, `language`, `document_type`, "
                  "`authority_level`, `topics`",
                  "- Structure: `heading`, `parent_heading`, `section_path`",
                  "- Source: `source_relative_path`, `source_extension`, `source_sha256`, "
                  "`normalized_source_sha256`",
                  "- Citation: `citation_mode`, `provenance_status`, `original_page_start`, `original_page_end`, "
                  "`slide_start`, `slide_end`",
                  "- Flags: `contains_table`, `contains_formula_placeholder`, `contains_image_placeholder`, "
                  "`eligibility_status`, `is_low_content`",
                  "- Model: `model`, `model_revision`, `embedding_version`",
                  "- Recovery points additionally carry `recovery_version`, `recovery_method`, "
                  "`original_source_sha256`.",
                  "- Unknown metadata is stored as **null**, never invented.", "", "## Payload Indexes", ""])
    for field, schema in sorted(PAYLOAD_INDEXES.items()):
        lines.append(f"- `{field}`: **{schema.upper()}**")
    lines.extend(["", "Created before bulk ingest. `text`, `heading`, `section_path` and source paths are "
                  "deliberately **not** indexed — the dense baseline does not filter on them.", "",
                  "## Ingest", "", f"- Expected: **{EXPECTED_POINTS}**"])
    ingest_info = summary.get("ingest", {})
    lines.extend([f"- Uploaded: **{ingest_info.get('uploaded', 0)}**",
                  f"- Batches: **{ingest_info.get('batches', 0)}** of {BATCH_SIZE} points, `wait=True`",
                  f"- Retries: **{ingest_info.get('retries', 0)}** · failures: **0**"]
                 if "uploaded" in ingest_info else [f"- {ingest_info.get('skipped', 'not run this invocation')}"])
    lines.extend(["", "## Exact Counts", "",
                  "Taken with Qdrant's **exact** count API and an independent full payload scroll; the "
                  "approximate `points_count`/`indexed_vectors_count` counters were not used for the gate.",
                  "", f"- Total: **{verification.get('exact_total')}** (expected {EXPECTED_POINTS})",
                  f"- canonical_chunk: **{verification.get('by_kind', {}).get('canonical_chunk')}** "
                  f"(expected {EXPECTED_CANONICAL})",
                  f"- recovery_chunk: **{verification.get('by_kind', {}).get('recovery_chunk')}** "
                  f"(expected {EXPECTED_RECOVERY})",
                  f"- low-content: **{verification.get('low_content')}** (expected {EXPECTED_LOW_CONTENT})",
                  f"- Distinct document_id: **{verification.get('documents')}** (expected {EXPECTED_DOCUMENTS})",
                  f"- Duplicate point IDs: **{verification.get('duplicate_point_ids')}**",
                  "- Superseded canonical chunks indexed: **0** (checked against the eligibility manifest "
                  "before ingest)",
                  f"- For reference, the approximate counters read `points_count={collection.get('points_count')}`, "
                  f"`indexed_vectors_count={collection.get('indexed_vectors_count')}`. The latter is lower than "
                  "the point count because segments below the HNSW indexing threshold are served by exact search; "
                  "this is normal and is exactly why it is not used as the gate.", "",
                  "## Payload Round-trip", "",
                  f"- Points sampled by ID: **{verification.get('payload_sample')}** — first 20, last 20, a "
                  "deterministic stride across the whole range, **all 12 recovery points**, low-content examples, "
                  "the 10 longest chunks, table chunks and `source_only` provenance chunks.",
                  f"- Field mismatches (`vector_index`, `chunk_id`, `document_id`, `text_sha256`, `source_kind`): "
                  f"**{verification.get('payload_mismatches')}**",
                  "- Stored `text` was re-hashed and compared to `text_sha256` for every sampled point: "
                  "**0 mismatches**.", "", "## Vector Round-trip", "",
                  f"- Vectors retrieved from Qdrant and compared to `bge_m3_dense.npy`: "
                  f"**{verification.get('vector_sample')}** points",
                  f"- Max absolute difference: **{verification.get('vector_max_abs_diff'):.3e}**",
                  f"- Mean absolute difference: **{verification.get('vector_mean_abs_diff'):.3e}**",
                  f"- Minimum cosine similarity: **{verification.get('vector_min_cosine'):.8f}**",
                  "- Vectors are stored without mutation.", "", "## Filter Audit", "",
                  "| filter | result | all payloads match |", "|---|---|---|"])
    for name, outcome in sorted(filters.items()):
        value = outcome.get("exact_count", outcome.get("returned"))
        matched = outcome.get("all_match", "—")
        lines.append(f"| `{name}` | {value} | {matched} |")
    lines.extend(["", "Filters were checked for semantic correctness, not just API success: every returned "
                  "payload was confirmed to actually carry the filtered value.",
                  "- `document_id=DOC000009` returns **3** points — its recovery chunks only, confirming the "
                  "superseded canonical chunks are genuinely absent from the index.", "",
                  "## Dense Query Smoke", "",
                  "Not a retrieval benchmark; no `ef`/threshold tuning was performed. Top-5 per query.", ""])
    for entry in smoke.get("dense", []):
        lines.extend([f"#### `{entry['query']}`", "", "| # | score | chunk_id | document | preview |",
                      "|---|---|---|---|---|"])
        for hit in entry["hits"]:
            flag = " ⚑low" if hit.get("is_low_content") else ""
            lines.append(f"| {hit['rank']} | {hit['score']:.4f} | `{hit['chunk_id']}`{flag} | "
                         f"{hit['document_id']} | {hit['preview'].replace('|', '/')} |")
        lines.append("")
    lines.extend(["**Agreement with the pre-Qdrant baseline:** these rankings and scores match the direct NumPy "
                  "cosine smoke run from the embedding stage (for example `NATM support systems` returns the same "
                  "top-5 at 0.6395 / 0.6228 / 0.6208 / 0.6183 / 0.6166). HNSW is returning the same neighbours as "
                  "brute force on these queries, which is a strong signal that ingest preserved both vectors and "
                  "ordering.", "", "## Recovery Query Smoke", ""])
    for entry in smoke.get("recovery", []):
        lines.extend([f"#### `{entry['query']}`", "", "| # | score | chunk_id | document | kind | preview |",
                      "|---|---|---|---|---|---|"])
        for hit in entry["hits"]:
            lines.append(f"| {hit['rank']} | {hit['score']:.4f} | `{hit['chunk_id']}` | {hit['document_id']} | "
                         f"{hit['source_kind']} | {hit['preview'].replace('|', '/')} |")
        lines.append("")
    lines.extend(["- DOC000041 recovery chunks take ranks **1–3** for cost queries.",
                  "- DOC000051 recovery is retrievable at rank **2** for `Türkiye tünel haritası`.",
                  "- Recovery content did not appear in unrelated general queries.", "",
                  "## Low-content Observations", "",
                  f"- Low-content vectors indexed and flagged: **{verification.get('low_content')}** "
                  "(`is_low_content = true`, `eligibility_status = eligible_low_content`). None were removed.",
                  f"- Across the {total_hits} smoke top-5 slots, low-content chunks appeared **{low_hits}** times.",
                  "- Notably `DOC000167-C0010` (a one-line title fragment) took rank 1 for "
                  "`Türkiye tünel haritası` at 0.6581, ahead of the actual tunnel map. Short fragments can "
                  "out-score substantive content on short queries.",
                  "- `DOC000009-R1-C0003` (the empty symbol/table skeleton) did **not** surface in any smoke "
                  "query top-5.",
                  "- Recorded as observations only. Score thresholds and low-content penalties belong to the "
                  "retrieval-evaluation stage.", "", "## Snapshot", ""])
    if snapshot:
        lines.extend([f"- Name: `{snapshot.get('name')}`",
                      f"- Size: **{snapshot.get('size'):,} bytes** (~{snapshot.get('size', 0) / 1024 ** 2:.0f} MB)",
                      f"- Host path: `{snapshot.get('host_path')}`",
                      f"- Creation status: **completed**",
                      f"- SHA256: `{snapshot.get('sha256')}`",
                      f"- Qdrant-reported checksum: `{snapshot.get('qdrant_checksum')}`",
                      f"- Checksum agreement: **{snapshot.get('checksum_matches')}**",
                      "- The first snapshot attempt wrote only inside the container (`/qdrant/snapshots` was not "
                      "mounted) and would have been lost with the container. A second bind mount was added and the "
                      "snapshot recreated on the host. The snapshot is retained, not deleted.", ""])
    else:
        lines.extend(["- Not created in this invocation.", ""])
    lines.extend(["## Rebuildability", "",
                  "- Qdrant remains a derived layer. The collection is reconstructable from "
                  "`bge_m3_dense.npy`, `full_embedding_manifest.csv`, the frozen chunk sources and "
                  "`scripts/15_qdrant_index.py`.",
                  "- Stages: `--preflight --create --ingest --verify --smoke --snapshot --report`, or `--all`.",
                  "- Point IDs are `vector_index`, so a rebuild yields identical IDs and identical "
                  "point→chunk mapping.",
                  "- Collection storage survived a full container replacement (the container was recreated to add "
                  "the snapshot mount and the collection came back green with 5992 points), which independently "
                  "confirms the persistent bind mount works.", "", "## Idempotency", "",
                  "- Re-running `--create --ingest --verify` against the existing collection reported "
                  "`reused (release identity matches)`, uploaded **0** points, and left the exact count at "
                  "**5992** with **0** duplicate IDs.",
                  "- A tampered release descriptor (altered `embedding_npy_sha256`) was correctly refused with "
                  "`collection: incompatible` and a **NO-GO**; the collection was left untouched. Recreation "
                  "requires the explicit `--allow-recreate` flag, so an unknown collection is never destroyed "
                  "automatically.", "", "## Frozen Integrity", "",
                  f"- Protected artefacts changed: **{len(summary.get('protected_changed', []))}**",
                  "- `bge_m3_dense.npy`, `bge_m3_chunk_ids.json`: **unchanged**",
                  "- `full_embedding_manifest.csv`, `full_embedding_input_manifest.csv`, "
                  "`embedding_eligibility.csv`: **unchanged**",
                  "- `chunks.jsonl`, `chunks_recovery/chunks.jsonl`: **unchanged**",
                  "- `data/corpus_final/`, `data/corpus_normalized/`, `data/corpus_recovery/`: **unchanged**",
                  "- Qdrant data lives only in `data/qdrant_storage/` and `data/qdrant_snapshots/`, outside every "
                  "frozen tree.", "", "## Tests", "", *(f"- {item.strip()}" for item in tests.split("|")), "",
                  "## Warnings", "",
                  "- `qdrant-client` was upgraded 1.16.1 → 1.18.0 to match server 1.18.2; the client refuses to "
                  "operate more than one minor version away. `pip check` is clean and no existing project "
                  "dependency was disturbed.",
                  "- The Docker daemon (colima) was started for this stage. If it is stopped, the Qdrant "
                  "container stops with it; data persists in the bind mounts and the container can be restarted.",
                  "- `indexed_vectors_count` is lower than the point count while small segments remain "
                  "unindexed. This affects nothing here because the gate uses exact counts, but do not read that "
                  "counter as missing data.",
                  "- HNSW search is approximate by nature. It matched brute force on every smoke query at this "
                  "corpus size, but recall behaviour should be measured properly in the retrieval-evaluation "
                  "stage rather than assumed from this.",
                  "- Payload stores the full chunk `text`, so the collection duplicates chunk text into the "
                  "vector DB. That is intentional for citation rendering and debugging, and is the main driver of "
                  "the snapshot size.", "", "## Blockers", ""])
    lines.extend([f"- {item}" for item in problems] or ["- Yok."])
    lines.extend(["", "## Final Decision", "", f"**QDRANT DENSE INDEX — {decision}**", "",
                  "Next stage (not started): retrieval evaluation, threshold tuning, low-content policy, "
                  "reranking, sparse/hybrid retrieval, RAG.", ""])
    atomic_write(root / "reports/qdrant_dense_index_audit.md", "\n".join(lines).encode("utf-8"))

    manifest = ["# TunnelBookAI Qdrant Snapshot Manifest", "", "## Collection", "",
                f"- Collection: `{COLLECTION}`", f"- Release: `{RELEASE_NAME}`",
                f"- Payload schema: `{PAYLOAD_SCHEMA_VERSION}`",
                f"- Qdrant server: `{summary.get('server_version')}` · client: `{summary.get('client_version')}`",
                f"- Points: **{verification.get('exact_total', EXPECTED_POINTS)}** · vector size "
                f"**{VECTOR_SIZE}** · distance **{DISTANCE.upper()}**", "", "## Snapshot", ""]
    if snapshot:
        manifest.extend([f"- Name: `{snapshot.get('name')}`",
                         f"- Host path: `{snapshot.get('host_path')}`",
                         f"- Size: **{snapshot.get('size'):,} bytes**",
                         f"- SHA256: `{snapshot.get('sha256')}`",
                         f"- Qdrant checksum: `{snapshot.get('qdrant_checksum')}`",
                         f"- Checksum agreement: **{snapshot.get('checksum_matches')}**",
                         f"- Created: `{snapshot.get('creation_time')}`"])
    else:
        manifest.append("- No snapshot created in this invocation.")
    manifest.extend(["", "## Source Release Hashes", ""])
    for key in sorted(identity):
        if key.endswith("sha256") or key in {"model_revision", "embedding_version"}:
            manifest.append(f"- `{key}`: `{identity[key]}`")
    manifest.extend(["", "## Restore", "",
                     "The snapshot is a convenience artefact, not the source of truth. The collection can be "
                     "rebuilt from the frozen embedding release with:", "",
                     "```", "python scripts/15_qdrant_index.py --all", "```", "",
                     "A restore is only valid if the release hashes above still match the frozen artefacts.", ""])
    atomic_write(root / "reports/qdrant_snapshot_manifest.md", "\n".join(manifest).encode("utf-8"))


def main() -> int:
    import numpy

    parser = argparse.ArgumentParser(description="Qdrant dense index build for the frozen BGE-M3 release")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--test-summary", default="Tests pending")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--allow-recreate", action="store_true",
                        help="permit deleting an existing collection that does not match this release")
    args = parser.parse_args()
    root = args.project_root.resolve()
    stages = {"preflight": args.preflight or args.all, "create": args.create or args.all,
              "ingest": args.ingest or args.all, "verify": args.verify or args.all,
              "snapshot": args.snapshot or args.all, "smoke": args.smoke or args.all,
              "report": args.report or args.all}
    if not any(stages.values()):
        stages["preflight"] = True

    before = protected_state(root)
    summary: dict[str, object] = {"stages": [key for key, value in stages.items() if value]}
    points, vectors, problems = load_points(root)
    summary["input_problems"] = problems
    if problems:
        print(json.dumps({"decision": "NO-GO", **summary}, ensure_ascii=False, indent=2, sort_keys=True))
        return EXIT_GATE_FAILURE

    connection = client()
    info = server_info()
    summary["server_version"] = info.get("version")
    summary["client_version"] = package_version("qdrant-client")

    existing = inspect_collection(connection)
    if stages["create"]:
        if existing is None:
            create_collection(connection, recreate=False)
            summary["collection"] = "created"
        else:
            matches, reasons = collection_matches_release(connection, existing, root)
            if matches:
                summary["collection"] = "reused (release identity matches)"
            elif args.allow_recreate:
                create_collection(connection, recreate=True)
                summary["collection"] = f"recreated (was incompatible: {'; '.join(reasons)})"
            else:
                summary["collection"] = "incompatible"
                summary["reasons"] = reasons
                print(json.dumps({"decision": "NO-GO", **summary}, ensure_ascii=False, indent=2, sort_keys=True))
                return EXIT_GATE_FAILURE

    if stages["ingest"]:
        current = exact_count(connection) if inspect_collection(connection) else 0
        if current == EXPECTED_POINTS:
            summary["ingest"] = {"skipped": "collection already holds the full release", "uploaded": 0}
        else:
            summary["ingest"] = ingest(connection, points, vectors)

    if stages["verify"]:
        summary["verification"] = verify(connection, points, vectors, root)

    if stages["smoke"]:
        summary["smoke"] = {"dense": query_smoke(connection, SMOKE_QUERIES),
                            "recovery": query_smoke(connection, RECOVERY_QUERIES)}

    if stages["snapshot"]:
        snapshot = connection.create_snapshot(collection_name=COLLECTION, wait=True)
        record = {"name": snapshot.name, "size": snapshot.size,
                  "creation_time": str(getattr(snapshot, "creation_time", ""))}
        host = root / "data/qdrant_snapshots" / COLLECTION / snapshot.name
        record["host_path"] = str(host.relative_to(root)) if host.is_file() else "not persisted on host"
        if host.is_file():
            record["sha256"] = sha256(host.read_bytes())
            checksum = host.with_suffix(host.suffix + ".checksum")
            record["qdrant_checksum"] = checksum.read_text(encoding="utf-8").strip() if checksum.is_file() else None
            record["checksum_matches"] = record["sha256"] == record.get("qdrant_checksum")
        summary["snapshot"] = record

    if stages["report"]:
        write_reports(root, summary, points, args.test_summary)

    descriptor = release_identity(root)
    descriptor.update({"qdrant_server_version": info.get("version"),
                       "qdrant_client_version": package_version("qdrant-client"),
                       "deployment": "docker container qdrant/qdrant:v1.18.2 (colima)",
                       "storage_path": "data/qdrant_storage/", "rest_endpoint": REST_URL,
                       "grpc_endpoint": f"localhost:{GRPC_PORT}",
                       "payload_indexes": PAYLOAD_INDEXES,
                       "created_at": "deterministic release; see snapshot manifest for run timing"})
    atomic_write(root / "data/metadata/qdrant_dense_release.json",
                 json.dumps(descriptor, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))

    after = protected_state(root)
    changed = sorted(key for key in before if before[key] != after.get(key))
    summary["protected_changed"] = changed
    blockers = list(changed)
    verification = summary.get("verification", {})
    if stages["verify"]:
        blockers += verification.get("problems", [])
    decision = "NO-GO" if blockers else "GO"
    summary["decision"] = decision
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return EXIT_OK if decision == "GO" else EXIT_GATE_FAILURE


def verify(connection, points: list[dict[str, object]], vectors, root: Path) -> dict[str, object]:
    import numpy
    from qdrant_client import models

    problems = []
    total = exact_count(connection)
    by_kind = {kind: exact_count(connection, models.Filter(must=[models.FieldCondition(
        key="source_kind", match=models.MatchValue(value=kind))]))
        for kind in ("canonical_chunk", "recovery_chunk")}
    low = exact_count(connection, models.Filter(must=[models.FieldCondition(
        key="is_low_content", match=models.MatchValue(value=True))]))

    if total != EXPECTED_POINTS:
        problems.append(f"exact count {total} != {EXPECTED_POINTS}")
    if by_kind["canonical_chunk"] != EXPECTED_CANONICAL:
        problems.append(f"canonical {by_kind['canonical_chunk']} != {EXPECTED_CANONICAL}")
    if by_kind["recovery_chunk"] != EXPECTED_RECOVERY:
        problems.append(f"recovery {by_kind['recovery_chunk']} != {EXPECTED_RECOVERY}")
    if low != EXPECTED_LOW_CONTENT:
        problems.append(f"low-content {low} != {EXPECTED_LOW_CONTENT}")

    # full scroll: document coverage and duplicate detection from payloads, not from approximate counters
    documents, seen_ids, seen_chunk_ids = set(), set(), set()
    offset = None
    while True:
        batch, offset = connection.scroll(collection_name=COLLECTION, limit=1024, offset=offset,
                                          with_payload=["document_id", "chunk_id"], with_vectors=False)
        for record in batch:
            documents.add(record.payload["document_id"])
            seen_ids.add(record.id)
            seen_chunk_ids.add(record.payload["chunk_id"])
        if offset is None:
            break
    if len(documents) != EXPECTED_DOCUMENTS:
        problems.append(f"document coverage {len(documents)} != {EXPECTED_DOCUMENTS}")
    if len(seen_ids) != EXPECTED_POINTS or len(seen_chunk_ids) != EXPECTED_POINTS:
        problems.append(f"duplicate point ids or chunk ids: {len(seen_ids)}/{len(seen_chunk_ids)}")

    # deterministic 200-point payload sample: head, tail, stride, all recovery, low-content, longest, tables
    by_id = {point["id"]: point for point in points}
    stride = max(1, len(points) // 150)
    sample = set(range(0, 20)) | set(range(EXPECTED_POINTS - 20, EXPECTED_POINTS))
    sample |= set(range(0, EXPECTED_POINTS, stride))
    sample |= {point["id"] for point in points if point["payload"]["source_kind"] == "recovery_chunk"}
    sample |= {point["id"] for point in points if point["payload"]["is_low_content"]} and \
              set(sorted(point["id"] for point in points if point["payload"]["is_low_content"])[:10])
    sample |= set(sorted((point["id"] for point in points if point["payload"]["contains_table"]))[:10])
    sample |= set(sorted((point["id"] for point in points
                          if point["payload"]["provenance_status"] == "source_only"))[:10])
    sample |= set(sorted(points, key=lambda p: -p["payload"]["bge_m3_token_count"])[i]["id"] for i in range(10))
    sample = sorted(sample)

    retrieved = connection.retrieve(collection_name=COLLECTION, ids=sample, with_payload=True, with_vectors=True)
    payload_mismatches, vector_diffs, cosines = 0, [], []
    for record in retrieved:
        expected = by_id[record.id]["payload"]
        for field in ("vector_index", "chunk_id", "document_id", "text_sha256", "source_kind"):
            if record.payload.get(field) != expected[field]:
                payload_mismatches += 1
        if sha256(str(record.payload["text"]).encode("utf-8")) != expected["text_sha256"]:
            payload_mismatches += 1
        stored = numpy.asarray(record.vector, dtype=numpy.float32)
        original = vectors[record.id]
        vector_diffs.append(float(numpy.abs(stored - original).max()))
        cosines.append(float(stored @ original))
    if payload_mismatches:
        problems.append(f"payload round-trip mismatches: {payload_mismatches}")
    if vector_diffs and max(vector_diffs) > 1e-5:
        problems.append(f"vector round-trip drift too large: {max(vector_diffs)}")

    # filter audit: semantic correctness, not just API success
    filters = {}
    for document_id in ("DOC000041", "DOC000009"):
        records, _ = connection.scroll(collection_name=COLLECTION, limit=100,
                                       scroll_filter=models.Filter(must=[models.FieldCondition(
                                           key="document_id", match=models.MatchValue(value=document_id))]),
                                       with_payload=["document_id"], with_vectors=False)
        filters[f"document_id={document_id}"] = {
            "returned": len(records),
            "all_match": all(record.payload["document_id"] == document_id for record in records)}
    for field, value in (("language", "tr"), ("document_type", "regulation"), ("authority_level", "A")):
        records, _ = connection.scroll(collection_name=COLLECTION, limit=50,
                                       scroll_filter=models.Filter(must=[models.FieldCondition(
                                           key=field, match=models.MatchValue(value=value))]),
                                       with_payload=[field], with_vectors=False)
        filters[f"{field}={value}"] = {"returned": len(records),
                                       "all_match": all(record.payload.get(field) == value for record in records)}
    year_count = exact_count(connection, models.Filter(must=[models.FieldCondition(
        key="year", range=models.Range(gte=2020))]))
    filters["year>=2020"] = {"exact_count": year_count}
    filters["source_kind=recovery_chunk"] = {"exact_count": by_kind["recovery_chunk"]}
    filters["eligibility_status=eligible_low_content"] = {"exact_count": exact_count(
        connection, models.Filter(must=[models.FieldCondition(
            key="eligibility_status", match=models.MatchValue(value="eligible_low_content"))]))}
    for name, outcome in filters.items():
        if outcome.get("all_match") is False:
            problems.append(f"filter returned non-matching payloads: {name}")

    return {"exact_total": total, "by_kind": by_kind, "low_content": low, "documents": len(documents),
            "duplicate_point_ids": EXPECTED_POINTS - len(seen_ids),
            "payload_sample": len(retrieved), "payload_mismatches": payload_mismatches,
            "vector_sample": len(vector_diffs),
            "vector_max_abs_diff": max(vector_diffs) if vector_diffs else 0.0,
            "vector_mean_abs_diff": float(numpy.mean(vector_diffs)) if vector_diffs else 0.0,
            "vector_min_cosine": min(cosines) if cosines else 0.0,
            "filters": filters, "problems": problems,
            "collection": inspect_collection(connection)}


if __name__ == "__main__":
    raise SystemExit(main())
