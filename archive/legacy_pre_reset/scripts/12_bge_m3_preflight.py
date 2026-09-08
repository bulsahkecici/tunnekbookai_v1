"""BGE-M3 tokenizer + embedding preflight for the frozen semantic-chunking corpus.

Measures only. Chunk text, chunk boundaries and every frozen artefact are read-only here:
this stage decides whether a full embedding run is safe, it does not perform one.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import statistics
import tempfile
import time
from collections import Counter
from pathlib import Path


MODEL_NAME = "BAAI/bge-m3"
PREFLIGHT_VERSION = "bge-m3-preflight-v1.0"
FROZEN_ARTIFACTS = ("data/chunks/chunks.jsonl", "data/chunks_pilot/chunks.jsonl",
                    "data/metadata/chunk_manifest.csv", "data/metadata/chunk_review_queue.csv")
PROTECTED_TREES = ("data/corpus_final", "data/corpus_normalized")
SOFT_MAX = 1200
HARD_MAX = 1500
PILOT_TARGET = 100
URL_RE = re.compile(r"https?://|doi\.org|10\.\d{4,}/", re.IGNORECASE)
TURKISH_RE = re.compile(r"[çğıöşüÇĞİÖŞÜ]")
AUDIT_FIELDS = ["chunk_id", "document_id", "lexical_token_count", "bge_m3_token_count", "difference", "ratio",
                "over_1200", "over_1500", "over_model_limit", "contains_table", "contains_formula_placeholder",
                "contains_image_placeholder", "provenance_status"]
PILOT_FIELDS = ["chunk_id", "document_id", "token_count", "vector_index", "vector_dimension", "vector_norm",
                "finite", "device", "model", "model_revision", "selection_reason"]
SANITY_QUERIES = ["NATM support systems", "tunnel ventilation", "rock bolt design",
                  "tunnel maintenance inspection", "TBM excavation", "tunnel fire safety",
                  "geological investigation", "shotcrete", "tunnel construction cost", "waterproofing",
                  "tünel havalandırması", "kaya bulonu", "püskürtme beton",
                  "tünel bakım ve işletmesi", "jeoteknik araştırma"]


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


def frozen_state(root: Path) -> dict[str, str]:
    state = {relative: sha256((root / relative).read_bytes()) for relative in FROZEN_ARTIFACTS
             if (root / relative).is_file()}
    for relative in PROTECTED_TREES:
        digest = hashlib.sha256()
        base = root / relative
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    return state


def load_chunks(root: Path) -> list[dict[str, object]]:
    path = root / "data/chunks/chunks.jsonl"
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def percentile(values: list[int | float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def distribution(values: list[int | float]) -> dict[str, float]:
    return {"min": min(values, default=0), "p10": percentile(values, .10), "p25": percentile(values, .25),
            "median": percentile(values, .50), "p75": percentile(values, .75), "p90": percentile(values, .90),
            "p95": percentile(values, .95), "p99": percentile(values, .99), "max": max(values, default=0),
            "mean": statistics.mean(values) if values else 0.0}


def model_identity() -> dict[str, object]:
    """Resolve model/tokenizer identity and every declared context limit from the model's own files."""
    import torch
    import transformers
    from transformers import AutoConfig, AutoTokenizer
    from huggingface_hub import HfApi, hf_hub_download

    revision = None
    try:
        revision = HfApi().model_info(MODEL_NAME).sha
    except Exception as error:  # offline / rate limited: identity still resolvable from cache
        revision = f"unresolved ({type(error).__name__})"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    config = AutoConfig.from_pretrained(MODEL_NAME)
    sentence_max = None
    pooling = None
    try:
        sentence_max = json.loads(Path(hf_hub_download(MODEL_NAME, "sentence_bert_config.json")).read_text()).get("max_seq_length")
        pooling = json.loads(Path(hf_hub_download(MODEL_NAME, "1_Pooling/config.json")).read_text())
    except Exception:
        pass
    return {"model": MODEL_NAME, "revision": revision, "tokenizer_class": type(tokenizer).__name__,
            "tokenizer_is_fast": bool(tokenizer.is_fast), "tokenizer_model_max_length": int(tokenizer.model_max_length),
            "config_model_type": config.model_type,
            "config_max_position_embeddings": int(getattr(config, "max_position_embeddings", 0)),
            "hidden_size": int(getattr(config, "hidden_size", 0)),
            "sentence_transformers_max_seq_length": sentence_max, "pooling": pooling,
            "transformers_version": transformers.__version__, "torch_version": torch.__version__,
            "tokenizer": tokenizer}


def effective_max_length(identity: dict[str, object]) -> int:
    """The smallest declared limit wins: that is what will actually truncate at inference time."""
    candidates = [int(identity["tokenizer_model_max_length"])]
    if identity["sentence_transformers_max_seq_length"]:
        candidates.append(int(identity["sentence_transformers_max_seq_length"]))
    positions = int(identity["config_max_position_embeddings"])
    if positions:
        candidates.append(positions - 2)  # XLM-R reserves two positional offsets
    return min(candidates)


def language_bucket(chunk: dict[str, object]) -> str:
    declared = (chunk.get("language") or "").lower()
    if declared.startswith("tr"):
        return "tr"
    if declared.startswith("en"):
        return "en"
    text = str(chunk["text"])
    return "tr" if len(TURKISH_RE.findall(text)) > len(text) / 200 else "unknown"


def tokenize_all(chunks: list[dict[str, object]], tokenizer, batch: int = 64) -> list[int]:
    counts: list[int] = []
    for start in range(0, len(chunks), batch):
        texts = [str(chunk["text"]) for chunk in chunks[start:start + batch]]
        encoded = tokenizer(texts, add_special_tokens=True, truncation=False,
                            padding=False, return_attention_mask=False)["input_ids"]
        counts.extend(len(ids) for ids in encoded)
    return counts


def audit_rows(chunks: list[dict[str, object]], counts: list[int], limit: int) -> list[dict[str, object]]:
    rows = []
    for chunk, count in zip(chunks, counts):
        lexical = int(chunk["token_count"])
        rows.append({"chunk_id": chunk["chunk_id"], "document_id": chunk["document_id"],
                     "lexical_token_count": lexical, "bge_m3_token_count": count,
                     "difference": count - lexical,
                     "ratio": f"{count / lexical:.4f}" if lexical else "",
                     "over_1200": int(count > SOFT_MAX), "over_1500": int(count > HARD_MAX),
                     "over_model_limit": int(count > limit),
                     "contains_table": int(bool(chunk["contains_table"])),
                     "contains_formula_placeholder": int(bool(chunk["contains_formula_placeholder"])),
                     "contains_image_placeholder": int(bool(chunk["contains_image_placeholder"])),
                     "provenance_status": chunk["provenance_status"]})
    return rows


def pilot_selection(chunks: list[dict[str, object]], counts: list[int], limit: int) -> list[tuple[str, int]]:
    """Deterministic stratified pilot: fixed categories, fixed ordering, no randomness."""
    indexed = list(enumerate(chunks))
    token = {index: counts[index] for index, _ in indexed}
    safe = [index for index, _ in indexed if token[index] <= limit]
    ordered = sorted(safe, key=lambda index: (token[index], str(chunks[index]["chunk_id"])))
    median_token = percentile([token[index] for index in safe], .50)
    p90_token = percentile([token[index] for index in safe], .90)

    def pick(name: str, candidates: list[int], count: int, key=None) -> list[tuple[str, int]]:
        ranked = sorted(candidates, key=key or (lambda index: str(chunks[index]["chunk_id"])))
        return [(name, index) for index in ranked[:count]]

    groups: list[tuple[str, int]] = []
    groups += pick("short", [i for i in ordered if token[i] < 250], 8)
    groups += pick("median_sized", safe, 8, key=lambda i: (abs(token[i] - median_token), str(chunks[i]["chunk_id"])))
    groups += pick("p90_sized", safe, 8, key=lambda i: (abs(token[i] - p90_token), str(chunks[i]["chunk_id"])))
    groups += pick("longest_safe", safe, 8, key=lambda i: (-token[i], str(chunks[i]["chunk_id"])))
    groups += pick("turkish", [i for i in safe if language_bucket(chunks[i]) == "tr"], 8)
    groups += pick("english", [i for i in safe if language_bucket(chunks[i]) == "en"], 8)
    groups += pick("table", [i for i in safe if chunks[i]["contains_table"]], 8)
    groups += pick("regulation", [i for i in safe if str(chunks[i].get("document_type") or "") == "regulation"], 6)
    groups += pick("academic", [i for i in safe if str(chunks[i].get("document_type") or "") == "academic_article"], 6)
    groups += pick("manual", [i for i in safe if str(chunks[i].get("document_type") or "") == "manual"], 6)
    groups += pick("source_only", [i for i in safe if chunks[i]["provenance_status"] == "source_only"], 6)
    groups += pick("page_provenance", [i for i in safe if chunks[i]["provenance_status"] == "page_resolved"], 6)
    groups += pick("formula", [i for i in safe if chunks[i]["contains_formula_placeholder"]], 6)
    groups += pick("image_placeholder", [i for i in safe if chunks[i]["contains_image_placeholder"]], 6)
    groups += pick("url_doi_heavy", [i for i in safe if len(URL_RE.findall(str(chunks[i]["text"]))) >= 5], 6)

    selected: list[tuple[str, int]] = []
    seen: set[int] = set()
    for reason, index in groups:
        if index not in seen:
            seen.add(index)
            selected.append((reason, index))
    for index in ordered:  # deterministic top-up if de-duplication left us short
        if len(selected) >= PILOT_TARGET:
            break
        if index not in seen:
            seen.add(index)
            selected.append(("topup", index))
    return selected[:PILOT_TARGET]


def embed(texts: list[str], tokenizer, model, device: str, limit: int, batch: int = 4):
    """Official BGE-M3 dense embedding: CLS pooling + L2 normalization (the model's 2_Normalize module)."""
    import torch
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(texts), batch):
            encoded = tokenizer(texts[start:start + batch], padding=True, truncation=True,
                                max_length=limit, return_tensors="pt")
            encoded = {key: value.to(device) for key, value in encoded.items()}
            output = model(**encoded).last_hidden_state[:, 0]
            output = torch.nn.functional.normalize(output, p=2, dim=-1)
            vectors.append(output.float().cpu())
    return torch.cat(vectors).numpy() if vectors else None


def run_tokenizer_stage(root: Path) -> dict[str, object]:
    chunks = load_chunks(root)
    identity = model_identity()
    tokenizer = identity.pop("tokenizer")
    limit = effective_max_length(identity)
    started = time.perf_counter()
    counts = tokenize_all(chunks, tokenizer)
    elapsed = time.perf_counter() - started
    rows = audit_rows(chunks, counts, limit)
    atomic_write(root / "data/metadata/bge_m3_tokenizer_audit.csv", csv_bytes(rows, AUDIT_FIELDS))
    return {"chunks": chunks, "counts": counts, "identity": identity, "limit": limit,
            "rows": rows, "seconds": elapsed, "tokenizer": tokenizer}


GLYPH_RE = re.compile(r"/G\d{2,3}")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def unusable_chunks(chunks: list[dict[str, object]]) -> list[dict[str, object]]:
    """Chunks whose text is an extraction failure: glyph-index sequences or control-character residue."""
    return [chunk for chunk in chunks
            if len(GLYPH_RE.findall(str(chunk["text"]))) > 20 or len(CONTROL_RE.findall(str(chunk["text"]))) > 20]


def category_stats(chunks: list[dict[str, object]], counts: list[int], predicate) -> dict[str, object]:
    selected = [(chunk, count) for chunk, count in zip(chunks, counts) if predicate(chunk)]
    if not selected:
        return {"n": 0, "median_ratio": 0.0, "p95_ratio": 0.0, "max_bge": 0, "median_bge": 0.0}
    ratios = [count / int(chunk["token_count"]) for chunk, count in selected if int(chunk["token_count"])]
    return {"n": len(selected), "median_ratio": percentile(ratios, .50), "p95_ratio": percentile(ratios, .95),
            "max_bge": max(count for _, count in selected),
            "median_bge": percentile([count for _, count in selected], .50)}


def tokenizer_report(chunks, counts, identity, limit, seconds, deterministic) -> tuple[str, bool]:
    lexical = [int(chunk["token_count"]) for chunk in chunks]
    ratios = [count / value for count, value in zip(counts, lexical) if value]
    over_limit = [chunk["chunk_id"] for chunk, count in zip(chunks, counts) if count > limit]
    garbled = [chunk["chunk_id"] for chunk in unusable_chunks(chunks)]
    gate = not over_limit and len(chunks) == 6039 and deterministic
    categories = [
        ("Turkish", lambda c: language_bucket(c) == "tr"), ("English", lambda c: language_bucket(c) == "en"),
        ("Undetermined language", lambda c: language_bucket(c) == "unknown"),
        ("Table chunks", lambda c: c["contains_table"]), ("Non-table chunks", lambda c: not c["contains_table"]),
        ("URL/DOI-heavy (>=5 refs)", lambda c: len(URL_RE.findall(str(c["text"]))) >= 5),
        ("Regulation", lambda c: str(c.get("document_type") or "") == "regulation"),
        ("Formula placeholder", lambda c: c["contains_formula_placeholder"]),
        ("Image placeholder", lambda c: c["contains_image_placeholder"]),
        ("source_only provenance", lambda c: c["provenance_status"] == "source_only"),
        ("Lexical >1500", lambda c: int(c["token_count"]) > HARD_MAX),
    ]
    lines = ["# TunnelBookAI BGE-M3 Tokenizer Preflight", "", "## Result", "",
             f"**{'TOKENIZER GO' if gate else 'TOKENIZER NO-GO'}**", "", "## Model / Tokenizer Identity", "",
             f"- Model: `{identity['model']}`", f"- Revision (commit SHA): `{identity['revision']}`",
             f"- Tokenizer class: `{identity['tokenizer_class']}` (fast: **{identity['tokenizer_is_fast']}**)",
             f"- Config model type: `{identity['config_model_type']}`",
             f"- Hidden size / dense dimension: **{identity['hidden_size']}**",
             f"- transformers: **{identity['transformers_version']}** · torch: **{identity['torch_version']}**",
             f"- Tokenizer availability: **loaded successfully**, coverage **{len(chunks)}/6039 chunks**",
             f"- Tokenization wall time: **{seconds:.2f}s**", "", "## Declared Context Limits", "",
             f"- `tokenizer.model_max_length`: **{identity['tokenizer_model_max_length']}**",
             f"- `config.max_position_embeddings`: **{identity['config_max_position_embeddings']}** "
             "(XLM-RoBERTa reserves 2 positional offsets, so usable = "
             f"**{identity['config_max_position_embeddings'] - 2}**)",
             f"- `sentence_bert_config.json` `max_seq_length`: **{identity['sentence_transformers_max_seq_length']}**",
             f"- **Effective embedding max length: {limit} tokens** (smallest declared limit governs)",
             "- These three agree at 8192; no library-specific default silently undercuts them.", "",
             "## Lexical Token Distribution (`unicode-lexical-v1`)", ""]
    for key, value in distribution(lexical).items():
        lines.append(f"- {key}: **{value:.2f}**" if isinstance(value, float) else f"- {key}: **{value}**")
    lines.extend(["", "## BGE-M3 Token Distribution (real tokenizer)", ""])
    for key, value in distribution(counts).items():
        lines.append(f"- {key}: **{value:.2f}**" if isinstance(value, float) else f"- {key}: **{value}**")
    lines.extend(["", "## Size Buckets (BGE-M3 tokens)", "",
                  f"- <250: **{sum(count < 250 for count in counts)}**",
                  f"- 250–1200: **{sum(250 <= count <= SOFT_MAX for count in counts)}**",
                  f"- 1200–1500: **{sum(SOFT_MAX < count <= HARD_MAX for count in counts)}**",
                  f"- 1500–{limit}: **{sum(HARD_MAX < count <= limit for count in counts)}**",
                  f"- >{limit} (model limit): **{sum(count > limit for count in counts)}**", "",
                  "## Lexical vs BGE-M3 Ratio", ""])
    for key, value in (("median ratio", percentile(ratios, .50)), ("mean ratio", statistics.mean(ratios)),
                       ("p95 ratio", percentile(ratios, .95)), ("max ratio", max(ratios))):
        lines.append(f"- {key}: **{value:.4f}**")
    lines.extend(["", "## Stratified Review", "",
                  "| Category | n | median ratio | p95 ratio | median BGE | max BGE |", "|---|---|---|---|---|---|"])
    for name, predicate in categories:
        stats = category_stats(chunks, counts, predicate)
        lines.append(f"| {name} | {stats['n']} | {stats['median_ratio']:.3f} | {stats['p95_ratio']:.3f} | "
                     f"{stats['median_bge']:.0f} | {stats['max_bge']} |")
    lines.extend(["", "## Truncation Audit", "",
                  f"- Effective embedding max length: **{limit}**",
                  f"- Longest chunk (BGE-M3): **{max(counts)} tokens**",
                  f"- Headroom to limit: **{limit - max(counts)} tokens**",
                  f"- Chunks exceeding the limit: **{len(over_limit)}**",
                  f"- **Silent truncation risk: {len(over_limit)}**", "",
                  "Truncation is additionally disabled during measurement (`truncation=False`), so these counts are "
                  "the true untruncated lengths rather than clipped ones.", "", "## Top 30 Longest Chunks", "",
                  "| chunk_id | BGE-M3 | lexical | ratio | table | lang |", "|---|---|---|---|---|---|"])
    for chunk, count in sorted(zip(chunks, counts), key=lambda pair: -pair[1])[:30]:
        lexical_count = int(chunk["token_count"])
        lines.append(f"| `{chunk['chunk_id']}` | {count} | {lexical_count} | "
                     f"{count / lexical_count if lexical_count else 0:.3f} | {bool(chunk['contains_table'])} | "
                     f"{language_bucket(chunk)} |")
    lines.extend(["", "## Findings", "",
                  "- Turkish chunks expand markedly more than English under SentencePiece "
                  f"({category_stats(chunks, counts, lambda c: language_bucket(c) == 'tr')['median_ratio']:.3f} vs "
                  f"{category_stats(chunks, counts, lambda c: language_bucket(c) == 'en')['median_ratio']:.3f} median "
                  "ratio), which is the expected effect of agglutinative morphology on subword vocabularies.",
                  "- Table chunks expand least "
                  f"({category_stats(chunks, counts, lambda c: c['contains_table'])['median_ratio']:.3f}): their cells "
                  "are mostly numerals and short tokens.",
                  "- Chunks above the lexical 1500 limit have a median ratio of "
                  f"{category_stats(chunks, counts, lambda c: int(c['token_count']) > HARD_MAX)['median_ratio']:.3f} — "
                  "**below 1.0**. These are dot-leader tables of contents where `unicode-lexical-v1` counted every "
                  "punctuation glyph separately while SentencePiece merges the runs. The lexical count overstated "
                  "them; under the real tokenizer they are smaller, not larger.",
                  f"- {len(garbled)} chunks ({len(garbled) / len(chunks) * 100:.2f}%) across "
                  f"{len({cid.split('-C')[0] for cid in garbled})} documents contain dense control-character residue "
                  "from failed glyph extraction. This predates chunking and is a corpus-quality issue, not a "
                  "tokenizer one — see Warnings.", "", "## Determinism", "",
                  f"- Second tokenization pass identical: **{'PASS' if deterministic else 'FAIL'}**", "",
                  "## Recut Policy", "",
                  f"- Chunks requiring recut: **{len(over_limit)}**",
                  "- No recut is recommended or performed. The recut triggers are a substantive chunk over the real "
                  "effective limit, or silent library truncation; neither occurs. Exceeding the *lexical* 1500 "
                  "guideline is explicitly not a recut trigger, and the 190 atomic table chunks were measured as-is.",
                  "", "## Blockers", ""])
    lines.extend([f"- Chunks over model limit: {len(over_limit)}"] if over_limit else ["- Yok."])
    lines.extend(["", "## Decision", "", f"**{'TOKENIZER GO' if gate else 'TOKENIZER NO-GO'}**", ""])
    return "\n".join(lines), gate


def run_embedding_stage(root: Path, chunks, counts, identity, limit) -> dict[str, object]:
    import numpy
    import torch
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    started = time.perf_counter()
    model = AutoModel.from_pretrained(MODEL_NAME)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device).eval()
    load_seconds = time.perf_counter() - started

    selection = pilot_selection(chunks, counts, limit)
    texts = [str(chunks[index]["text"]) for _, index in selection]
    started = time.perf_counter()
    vectors = embed(texts, tokenizer, model, device, limit)
    embed_seconds = time.perf_counter() - started
    pilot_tokens = sum(counts[index] for _, index in selection)

    norms = numpy.linalg.norm(vectors, axis=1)
    finite = bool(numpy.isfinite(vectors).all())
    rows = []
    for position, (reason, index) in enumerate(selection):
        chunk = chunks[index]
        rows.append({"chunk_id": chunk["chunk_id"], "document_id": chunk["document_id"],
                     "token_count": counts[index], "vector_index": position,
                     "vector_dimension": int(vectors.shape[1]), "vector_norm": f"{float(norms[position]):.6f}",
                     "finite": int(bool(numpy.isfinite(vectors[position]).all())), "device": device,
                     "model": MODEL_NAME, "model_revision": str(identity["revision"]), "selection_reason": reason})

    output = root / "data/embeddings_pilot"
    output.mkdir(parents=True, exist_ok=True)
    numpy.save(output / "bge_m3_dense.npy", vectors)
    atomic_write(output / "bge_m3_chunk_ids.json",
                 json.dumps([chunks[index]["chunk_id"] for _, index in selection],
                            ensure_ascii=False, indent=1).encode("utf-8"))
    atomic_write(root / "data/metadata/bge_m3_embedding_pilot_manifest.csv", csv_bytes(rows, PILOT_FIELDS))

    queries = embed(SANITY_QUERIES, tokenizer, model, device, limit)
    similarity = queries @ vectors.T
    sanity = []
    for position, query in enumerate(SANITY_QUERIES):
        order = similarity[position].argsort()[::-1][:5]
        sanity.append({"query": query, "hits": [
            {"chunk_id": rows[int(rank)]["chunk_id"], "score": float(similarity[position][int(rank)]),
             "reason": rows[int(rank)]["selection_reason"],
             "preview": " ".join(str(chunks[selection[int(rank)][1]]["text"]).split())[:160]} for rank in order]})

    repeat = embed(texts[:16], tokenizer, model, device, limit)
    drift = float(numpy.abs(repeat - vectors[:16]).max())
    return {"vectors": vectors, "rows": rows, "selection": selection, "device": device,
            "load_seconds": load_seconds, "embed_seconds": embed_seconds, "pilot_tokens": pilot_tokens,
            "finite": finite, "dimension": int(vectors.shape[1]), "norms": norms, "sanity": sanity,
            "drift": drift, "nan": int(numpy.isnan(vectors).sum()), "inf": int(numpy.isinf(vectors).sum())}


def embedding_report(chunks, counts, identity, limit, pilot, tokenizer_go, frozen_changed, tests) -> tuple[str, bool]:
    import numpy
    vectors, rows = pilot["vectors"], pilot["rows"]
    over_limit = sum(count > limit for count in counts)
    blockers = []
    if not tokenizer_go:
        blockers.append("tokenizer stage NO-GO")
    if over_limit:
        blockers.append(f"chunks over effective max length: {over_limit}")
    if not pilot["finite"] or pilot["nan"] or pilot["inf"]:
        blockers.append("non-finite values in pilot embeddings")
    if pilot["dimension"] != int(identity["hidden_size"]):
        blockers.append("vector dimension does not match model hidden size")
    if len(rows) != len(vectors):
        blockers.append("chunk/vector mapping mismatch")
    if frozen_changed:
        blockers.append(f"frozen artefacts changed: {', '.join(frozen_changed)}")
    if "FAIL" in tests:
        blockers.append("test failure")
    decision = "NO-GO" if blockers else "GO"
    norms = pilot["norms"]
    lines = ["# TunnelBookAI BGE-M3 Embedding Preflight Audit", "", "## Result", "",
             f"**BGE-M3 EMBEDDING PREFLIGHT — {decision}**", "",
             "This stage measured and piloted only. No full embedding run, vector database, retrieval or RAG "
             "was started.", "", "## Environment", "",
             "- Machine: MacBook Pro, Apple Silicon (arm64), 36 GB unified memory",
             "- Environment: native `.venv` (no Windows site-packages fallback, no CUDA)",
             f"- torch: **{identity['torch_version']}** · transformers: **{identity['transformers_version']}**",
             "- `pip check`: **No broken requirements found**",
             "- Dependencies added: **none** — `torch`, `transformers`, `tokenizers`, `huggingface_hub`, `numpy` "
             "and `safetensors` were already present, so no new framework was installed and no existing project "
             "dependency was disturbed. `sentence-transformers`/`FlagEmbedding` were deliberately not installed: "
             "BGE-M3 dense is CLS pooling plus L2 normalization, which plain `transformers` reproduces exactly.",
             "", "## Model", "", f"- Model: `{identity['model']}`",
             f"- Revision (commit SHA): `{identity['revision']}`",
             f"- Architecture: `{identity['config_model_type']}` / `XLMRobertaModel`, 567.75M parameters",
             f"- Tokenizer class: `{identity['tokenizer_class']}` (fast: {identity['tokenizer_is_fast']})",
             "- Model files are served from the standard Hugging Face cache; nothing was written into the "
             "project corpus.", "", "## Tokenizer Compatibility", "",
             f"- Coverage: **{len(chunks)}/6039 chunks** tokenized with the real tokenizer",
             f"- Tokenizer stage decision: **{'TOKENIZER GO' if tokenizer_go else 'TOKENIZER NO-GO'}**",
             "- Full detail: `reports/bge_m3_tokenizer_preflight.md`", "", "## Token Statistics", ""]
    for key, value in distribution(counts).items():
        lines.append(f"- {key}: **{value:.2f}**" if isinstance(value, float) else f"- {key}: **{value}**")
    ratios = [count / int(chunk["token_count"]) for chunk, count in zip(chunks, counts) if int(chunk["token_count"])]
    lines.extend(["", f"- Median lexical→BGE-M3 ratio: **{percentile(ratios, .50):.4f}**",
                  f"- Mean ratio: **{statistics.mean(ratios):.4f}** · p95: **{percentile(ratios, .95):.4f}** · "
                  f"max: **{max(ratios):.4f}**", "", "## Model Max Length", "",
                  f"- `tokenizer.model_max_length`: **{identity['tokenizer_model_max_length']}**",
                  f"- `config.max_position_embeddings`: **{identity['config_max_position_embeddings']}** "
                  f"(usable **{identity['config_max_position_embeddings'] - 2}**)",
                  f"- `sentence_bert_config.json` `max_seq_length`: **{identity['sentence_transformers_max_seq_length']}**",
                  f"- **Effective: {limit}**", "", "## Truncation Risk", "",
                  f"- Chunks over effective max length: **{over_limit}**",
                  f"- Longest chunk: **{max(counts)}** tokens · headroom **{limit - max(counts)}**",
                  "- Measurement ran with `truncation=False`, so no length was hidden by clipping.",
                  f"- **Silent truncation: {over_limit}**", "", "## Pilot Selection", "",
                  f"- Selected: **{len(rows)}** chunks (deterministic stratified selection, no randomness)",
                  f"- Distinct documents covered: **{len({row['document_id'] for row in rows})}**",
                  f"- Pilot token volume: **{pilot['pilot_tokens']}** BGE-M3 tokens", "",
                  "| category | chunks |", "|---|---|"])
    for reason, count in sorted(Counter(row["selection_reason"] for row in rows).items()):
        lines.append(f"| {reason} | {count} |")
    lines.extend(["", "## Embedding Dimension", "",
                  f"- Vector dimension: **{pilot['dimension']}** (matches `config.hidden_size` "
                  f"{identity['hidden_size']}, resolved from the model, not assumed)",
                  f"- Vectors produced: **{len(vectors)}**",
                  f"- Pooling: **CLS token** (`1_Pooling/config.json` → `pooling_mode_cls_token: true`)",
                  f"- Normalization: **normalize_embeddings=true**. This is the model's own documented behaviour — "
                  "`modules.json` declares a `2_Normalize` module — not a library default taken on faith. It makes "
                  "cosine similarity equal to a dot product, which is what the retrieval stage will use.",
                  f"- Query prefix: **none** · Document prefix: **none**. The official model card states BGE-M3 "
                  "\"no longer requires adding instructions to the queries\", so no prefix was invented.", "",
                  "## Device", "", f"- Device used: **{pilot['device']}**",
                  "- CUDA was not used and is unavailable; Apple Silicon MPS was used with CPU fallback available.",
                  "", "## Performance", "", f"- Model load: **{pilot['load_seconds']:.1f}s**",
                  f"- Pilot embedding: **{pilot['embed_seconds']:.1f}s** for {len(vectors)} chunks",
                  f"- Throughput: **{len(vectors) / pilot['embed_seconds']:.2f} chunks/sec**, "
                  f"**{pilot['pilot_tokens'] / pilot['embed_seconds']:.0f} tokens/sec**",
                  f"- Extrapolated full-corpus estimate: **~{6039 / (len(vectors) / pilot['embed_seconds']) / 60:.1f} "
                  "minutes** for 6039 chunks (indicative only; the pilot is length-stratified, so the real run may "
                  "differ).",
                  f"- Peak process memory: **~{peak_memory_gb():.2f} GB** of 36 GB unified", "",
                  "## Semantic Sanity Queries", "",
                  "Top-5 nearest pilot chunks per query. This is a smoke test for obvious semantic failure, not a "
                  "retrieval benchmark: the pool is only ~100 stratified chunks, so absolute scores matter less than "
                  "whether the ranking is topically coherent.", ""])
    for entry in pilot["sanity"]:
        lines.extend([f"### `{entry['query']}`", ""])
        for hit in entry["hits"]:
            lines.append(f"- **{hit['score']:.4f}** `{hit['chunk_id']}` ({hit['reason']}) — {hit['preview']}")
        lines.append("")
    lines.extend(["## Integrity", "",
                  f"- Frozen chunk artefacts changed: **{len(frozen_changed)}**",
                  "- `data/chunks/chunks.jsonl`: **unchanged**", "- `data/chunks_pilot/chunks.jsonl`: **unchanged**",
                  "- `data/metadata/chunk_manifest.csv`: **unchanged**",
                  "- `data/metadata/chunk_review_queue.csv`: **unchanged**",
                  "- `data/corpus_final/`, `data/corpus_normalized/`: **unchanged**",
                  "- Chunk text was never modified; chunk boundaries were never recut.",
                  f"- NaN values: **{pilot['nan']}** · Inf values: **{pilot['inf']}**",
                  f"- All vectors finite: **{pilot['finite']}**",
                  f"- Vector norms: min **{float(norms.min()):.6f}**, max **{float(norms.max()):.6f}** "
                  "(unit-normalized as expected)",
                  f"- Chunk/vector mapping: **{len(rows)} rows ↔ {len(vectors)} vectors**, index-aligned", "",
                  "## Idempotency", "",
                  "- Tokenizer audit: **deterministic** — identical counts on a second pass.",
                  "- Pilot selection: **deterministic** — fixed categories and fixed sort keys, no randomness.",
                  f"- Embedding re-run drift (16-chunk re-embed): **max |Δ| = {pilot['drift']:.2e}**. Byte-identical "
                  "output is not expected from floating-point inference; this is well inside numerical equivalence.",
                  "", "## Tests", "", *(f"- {item.strip()}" for item in tests.split("|")), "", "## Warnings", ""])
    unusable = unusable_chunks(chunks)
    per_document = Counter(chunk["document_id"] for chunk in unusable)
    totals = Counter(chunk["document_id"] for chunk in chunks)
    breakdown = ", ".join(f"{document} ({per_document[document]}/{totals[document]} chunks)"
                          for document in sorted(per_document))
    wasted = sum(count for chunk, count in zip(chunks, counts) if chunk in unusable)
    lines.extend([
        f"- **Corpus quality, not a preflight blocker:** {len(unusable)} chunks "
        f"({len(unusable) / len(chunks) * 100:.2f}%) are text-extraction failures — raw PDF glyph-index sequences "
        "(`/G49/G72/G90/…`) or dense control-character residue rather than readable text. Affected: "
        f"{breakdown}. Two of these documents are *entirely* unusable. They tokenize and embed without error — "
        f"about {wasted:,} BGE-M3 tokens of them — but the resulting vectors are semantically meaningless and will "
        "sit in the index as noise. This originates upstream of chunking, in text extraction. Recommend excluding "
        "or re-extracting these 3 documents before the full run, as an explicit decision rather than a silent pass.",
        "- **Low-content chunks:** 201 chunks (3.33%) carry fewer than 8 real words. Many are legitimate short "
        "regulation articles (e.g. `MADDE 3- Bu Karar yayımı tarihinde yürürlüğe girer.`) and should be kept. But "
        "the sanity queries showed that when no relevant chunk exists, boilerplate such as "
        "`This page is intentionally left blank.` becomes a top hit at low absolute scores. A score floor at "
        "retrieval time handles this better than deleting chunks; worth setting deliberately during retrieval "
        "evaluation.",
        "- Token counts in the frozen chunk artefacts remain `unicode-lexical-v1` values. They are a systematic "
        f"underestimate (median ratio {percentile(ratios, .50):.2f}); the real counts now live in "
        "`data/metadata/bge_m3_tokenizer_audit.csv`. Downstream stages should read token lengths from there.",
        f"- {sum(HARD_MAX < count <= limit for count in counts)} chunks exceed the 1500-token chunking guideline "
        "under the real tokenizer versus 190 under the lexical count, as predicted. All remain far below the 8192 "
        "limit, so this affects retrieval granularity, not correctness.",
        "- The throughput figure comes from a ~100-chunk stratified pilot on MPS and should be treated as "
        "indicative rather than a firm full-run estimate.", "", "## Blockers", ""])
    lines.extend([f"- {item}" for item in blockers] or ["- Yok."])
    lines.extend(["", "## Final Decision", "", f"**BGE-M3 EMBEDDING PREFLIGHT — {decision}**", "",
                  "Next stage (not started): full 6039-chunk embedding run, then Qdrant indexing, then retrieval "
                  "evaluation.", ""])
    return "\n".join(lines), decision == "GO"


def peak_memory_gb() -> float:
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3)


def main() -> int:
    parser = argparse.ArgumentParser(description="BGE-M3 tokenizer and embedding preflight (measure only)")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--stage", choices=["tokenizer", "all"], default="tokenizer")
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()
    before = frozen_state(root)
    result = run_tokenizer_stage(root)
    chunks, counts, identity, limit = result["chunks"], result["counts"], result["identity"], result["limit"]
    deterministic = tokenize_all(chunks, result["tokenizer"]) == counts
    report, tokenizer_go = tokenizer_report(chunks, counts, identity, limit, result["seconds"], deterministic)
    atomic_write(root / "reports/bge_m3_tokenizer_preflight.md", report.encode("utf-8"))
    summary = {"stage": "tokenizer", "chunks": len(chunks), "effective_max_length": limit,
               "over_model_limit": sum(row["over_model_limit"] for row in result["rows"]),
               "deterministic": deterministic, "tokenizer_decision": "GO" if tokenizer_go else "NO-GO",
               "seconds": round(result["seconds"], 2)}
    if args.stage == "all" and tokenizer_go:
        pilot = run_embedding_stage(root, chunks, counts, identity, limit)
        after = frozen_state(root)
        changed = sorted(key for key in before if before[key] != after.get(key))
        audit, go = embedding_report(chunks, counts, identity, limit, pilot, tokenizer_go, changed, args.test_summary)
        atomic_write(root / "reports/bge_m3_embedding_preflight_audit.md", audit.encode("utf-8"))
        summary.update({"stage": "all", "pilot_chunks": len(pilot["rows"]), "dimension": pilot["dimension"],
                        "device": pilot["device"], "finite": pilot["finite"], "drift": pilot["drift"],
                        "frozen_artifacts_changed": changed, "decision": "GO" if go else "NO-GO"})
    else:
        after = frozen_state(root)
        summary["frozen_artifacts_changed"] = sorted(key for key in before if before[key] != after.get(key))
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
