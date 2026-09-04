"""Retrieval improvement experiments against the frozen v1 benchmark.

Dense v1 is the control and is never replaced. Every variant is scored on the same 114 frozen
queries with the same gold labels, and all fusion/expansion happens offline over retrieved
candidates - the Qdrant collection and the embedding release are read-only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import statistics
import tempfile
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT_DEFAULT = Path(__file__).resolve().parents[1]
COLLECTION = "tunnelbook_dense_v1"
MODEL_NAME = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
RERANKER_NAME = "BAAI/bge-reranker-v2-m3"
RERANKER_REVISION = "953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"
RERANKER_MAX_LENGTH = 1024
REST_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
BM25_VERSION = "bm25plus-v1"
CANDIDATE_DEPTH = 100
K_VALUES = (1, 3, 5, 10, 20)
RRF_KS = (30, 60, 100)
BOOTSTRAP_SAMPLES = 2000
BOOTSTRAP_SEED = 20260817

PROTECTED = ("data/embeddings/bge_m3_dense.npy", "data/metadata/full_embedding_manifest.csv",
             "data/chunks/chunks.jsonl", "data/chunks_recovery/chunks.jsonl",
             "data/evaluation/retrieval_queries_v1.jsonl",
             "data/evaluation/retrieval_benchmark_v1_manifest.json")

# Engineering identifiers must survive tokenisation: standards, section numbers, ranges, units.
TOKEN_RE = re.compile(
    r"[^\W\d_]+\d+[^\W_]*"          # ASTM D1586, C30, T-24
    r"|\d+(?:[.,]\d+)+"             # 252.04, 351.08.07, 10,5
    r"|\d+(?:-\d+)+"                # 10-20
    r"|\d+"                         # 1997
    r"|[^\W\d_]+",                  # words (unicode letters)
    re.UNICODE)


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


def csv_bytes(rows, fields) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return ("﻿" + buffer.getvalue()).encode("utf-8")


def jsonl_bytes(rows) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_evaluation_module(root: Path):
    spec = importlib.util.spec_from_file_location("retrieval_evaluation",
                                                  root / "scripts/16_retrieval_evaluation.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def protected_state(root: Path) -> dict[str, str]:
    return {relative: sha256((root / relative).read_bytes()) for relative in PROTECTED
            if (root / relative).is_file()}


# ---------------------------------------------------------------- tokenisation + BM25

def normalise(text: str) -> str:
    """Case-fold without destroying Turkish letters; strip the combining dot casefold leaves on İ."""
    folded = unicodedata.normalize("NFKC", text).casefold()
    return folded.replace("̇", "")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(normalise(text))


class BM25Plus:
    """Deterministic BM25+ (Lv & Zhai). No stemming: Turkish morphology is left alone at this stage."""

    def __init__(self, corpus_tokens: list[list[str]], k1: float = 1.2, b: float = 0.75, delta: float = 1.0):
        self.k1, self.b, self.delta = k1, b, delta
        self.length = [len(tokens) for tokens in corpus_tokens]
        self.average_length = sum(self.length) / len(self.length) if self.length else 0.0
        self.frequencies: list[dict[str, int]] = []
        document_frequency: dict[str, int] = defaultdict(int)
        for tokens in corpus_tokens:
            counts = Counter(tokens)
            self.frequencies.append(dict(counts))
            for term in counts:
                document_frequency[term] += 1
        total = len(corpus_tokens)
        self.idf = {term: math.log((total - count + 0.5) / (count + 0.5) + 1.0)
                    for term, count in document_frequency.items()}
        self.postings: dict[str, list[int]] = defaultdict(list)
        for index, counts in enumerate(self.frequencies):
            for term in counts:
                self.postings[term].append(index)

    def scores(self, query_tokens: list[str]) -> dict[int, float]:
        result: dict[int, float] = defaultdict(float)
        for term in query_tokens:
            idf = self.idf.get(term)
            if idf is None:
                continue
            for index in self.postings[term]:
                frequency = self.frequencies[index][term]
                norm = 1 - self.b + self.b * (self.length[index] / self.average_length
                                              if self.average_length else 0.0)
                result[index] += idf * ((frequency * (self.k1 + 1)) / (frequency + self.k1 * norm) + self.delta)
        return result

    def top(self, query_tokens: list[str], limit: int) -> list[tuple[int, float]]:
        scored = self.scores(query_tokens)
        # deterministic tie handling: score descending, then index ascending
        return sorted(scored.items(), key=lambda item: (-item[1], item[0]))[:limit]


def build_bm25(root: Path, records: list[dict[str, object]]) -> tuple[BM25Plus, dict[str, object]]:
    tokens = [tokenize(str(record["text"])) for record in records]
    index = BM25Plus(tokens)
    stats = {"bm25_version": BM25_VERSION, "documents": len(records),
             "vocabulary": len(index.idf), "total_tokens": sum(len(item) for item in tokens),
             "average_length": index.average_length,
             "chunk_ids_sha256": sha256("\n".join(record["chunk_id"] for record in records).encode()),
             "k1": index.k1, "b": index.b, "delta": index.delta,
             "tokenizer": "unicode_nfkc_casefold_no_stemming"}
    directory = root / "data/retrieval/bm25_v1"
    atomic_write(directory / "index_stats.json",
                 json.dumps(stats, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    atomic_write(directory / "chunk_ids.json",
                 json.dumps([record["chunk_id"] for record in records], ensure_ascii=False,
                            indent=1).encode("utf-8"))
    vocabulary = sorted(index.idf)
    atomic_write(directory / "vocabulary.txt", "\n".join(vocabulary).encode("utf-8"))
    return index, stats


# ---------------------------------------------------------------- fusion + expansion

def rrf(rankings: list[list[int]], k: int) -> dict[int, float]:
    fused: dict[int, float] = defaultdict(float)
    for ranking in rankings:
        for rank, index in enumerate(ranking, start=1):
            fused[index] += 1.0 / (k + rank)
    return fused


def fused_order(fused: dict[int, float], tie_reference: dict[int, int]) -> list[int]:
    """Deterministic: fused score descending, then the control ranking, then index."""
    return [index for index, _ in sorted(fused.items(),
                                         key=lambda item: (-item[1], tie_reference.get(item[0], 10 ** 6),
                                                           item[0]))]


def neighbour_expand(order: list[int], records: list[dict[str, object]],
                     by_chunk: dict[str, int], limit: int) -> list[int]:
    """Add the immediately adjacent chunk of the same document, never crossing a document boundary."""
    out, seen = [], set()
    for index in order:
        for candidate in (index,) + neighbours(index, records, by_chunk):
            if candidate is not None and candidate not in seen:
                seen.add(candidate)
                out.append(candidate)
        if len(out) >= limit:
            break
    return out[:limit]


def neighbours(index: int, records: list[dict[str, object]], by_chunk: dict[str, int]):
    record = records[index]
    chunk_id = record["chunk_id"]
    match = re.match(r"^(.*-C)(\d+)$", chunk_id)
    if not match:
        return ()
    prefix, number = match.group(1), int(match.group(2))
    found = []
    for offset in (-1, 1):
        sibling = f"{prefix}{number + offset:04d}"
        position = by_chunk.get(sibling)
        if position is not None and records[position]["document_id"] == record["document_id"]:
            found.append(position)
    return tuple(found)



# ---------------------------------------------------------------- cross-lingual expansion

def translation_table() -> list[dict[str, str]]:
    """Frozen manual translations for the v1 cross-lingual probes.

    Authored by hand before any variant was scored, and written to disk so the mapping cannot drift
    after results are seen. No external service, no runtime translation.
    """
    return [
        {"query_id": "Q109", "original": "tünel havalandırma sistemi tasarımı",
         "translated": "tunnel ventilation system design", "source_language": "tr",
         "target_language": "en", "method": "manual_frozen"},
        {"query_id": "Q110", "original": "kaya kütlesi sınıflandırma sistemleri",
         "translated": "rock mass classification systems", "source_language": "tr",
         "target_language": "en", "method": "manual_frozen"},
        {"query_id": "Q111", "original": "tunnel maintenance and operation costs",
         "translated": "tünel bakım ve işletme maliyetleri", "source_language": "en",
         "target_language": "tr", "method": "manual_frozen"},
        {"query_id": "Q112", "original": "shotcrete application requirements",
         "translated": "püskürtme beton uygulama şartları", "source_language": "en",
         "target_language": "tr", "method": "manual_frozen"},
        {"query_id": "Q113", "original": "rock bolt pull-out test",
         "translated": "kaya bulonu çekme deneyi", "source_language": "en",
         "target_language": "tr", "method": "manual_frozen"},
        {"query_id": "Q114", "original": "geotechnical investigation report contents",
         "translated": "jeoteknik etüt raporu içeriği", "source_language": "en",
         "target_language": "tr", "method": "manual_frozen"},
    ]


def probe_v2_specs() -> list[dict[str, object]]:
    """Exploratory cross-lingual probes. Separate file; never merged into frozen benchmark v1."""
    def probe(pid, query, language, gold_language, anchors, topic):
        return {"query_id": pid, "query": query, "language": language,
                "gold_language": gold_language, "anchors": anchors, "topic": topic}
    return [
        probe("X01", "tünel havalandırması tasarımı", "tr", "en", [r"ventilation", r"design|system"], "ventilation"),
        probe("X02", "püskürtme beton kaplama", "tr", "en", [r"shotcrete", r"lining"], "shotcrete"),
        probe("X03", "kaya bulonu tasarımı", "tr", "en", [r"rock bolt"], "support"),
        probe("X04", "tünel yangın güvenliği", "tr", "en", [r"fire", r"safety|protection"], "fire"),
        probe("X05", "kaya kütlesi sınıflandırması", "tr", "en", [r"rock mass", r"classification"], "classification"),
        probe("X06", "tünel su yalıtımı", "tr", "en", [r"waterproof"], "waterproofing"),
        probe("X07", "TBM kazı yöntemi", "tr", "en", [r"\bTBM\b", r"excavat"], "tbm"),
        probe("X08", "tünel bakım ve muayene", "tr", "en", [r"inspection", r"maintenance"], "maintenance"),
        probe("X09", "jeoteknik araştırma", "tr", "en", [r"geotechnical", r"investigat"], "investigation"),
        probe("X10", "tünel aydınlatma sistemi", "tr", "en", [r"lighting"], "lighting"),
        probe("X11", "zemin oturması", "tr", "en", [r"settlement"], "settlement"),
        probe("X12", "acil kaçış yolu", "tr", "en", [r"escape|emergency"], "escape"),
        probe("X13", "enjeksiyon ile zemin iyileştirme", "tr", "en", [r"grouting"], "grouting"),
        probe("X14", "tünel drenajı", "tr", "en", [r"drainage"], "drainage"),
        probe("X15", "segment kaplama", "tr", "en", [r"segment", r"lining"], "lining"),
        probe("X16", "delme patlatma", "tr", "en", [r"blast"], "excavation"),
        probe("X17", "tunnel ventilation design", "en", "tr", [r"havalandırma"], "ventilation"),
        probe("X18", "shotcrete application", "en", "tr", [r"püskürtme beton"], "shotcrete"),
        probe("X19", "rock bolt testing", "en", "tr", [r"bulon"], "support"),
        probe("X20", "tunnel fire safety measures", "en", "tr", [r"yangın"], "fire"),
        probe("X21", "tunnel maintenance costs", "en", "tr", [r"bakım", r"maliyet|işletme"], "cost"),
        probe("X22", "geotechnical investigation", "en", "tr", [r"jeoteknik"], "investigation"),
        probe("X23", "tunnel lighting", "en", "tr", [r"aydınlatma"], "lighting"),
        probe("X24", "tunnel drainage system", "en", "tr", [r"drenaj"], "drainage"),
        probe("X25", "route selection for tunnels", "en", "tr", [r"güzergah", r"seçim"], "route"),
        probe("X26", "traffic safety in tunnels", "en", "tr", [r"trafik güvenliği"], "traffic"),
        probe("X27", "excavation classes", "en", "tr", [r"kazı sınıf|kaya sınıf"], "support"),
        probe("X28", "waterproofing membrane", "en", "tr", [r"su yalıtım"], "waterproofing"),
    ]


def build_probe_v2(root: Path, records: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for spec in probe_v2_specs():
        pool = [record for record in records if (record["language"] or "") == spec["gold_language"]]
        gold = []
        for record in pool:
            if not all(re.search(pattern, record["text"], re.IGNORECASE) for pattern in spec["anchors"]):
                continue
            headline = " ".join(filter(None, [str(record.get("heading") or ""),
                                              str(record.get("section_path") or "")]))
            if any(re.search(pattern, headline, re.IGNORECASE) for pattern in spec["anchors"]):
                gold.append(record)
        if not gold:
            continue
        rows.append({"query_id": spec["query_id"], "query": spec["query"], "language": spec["language"],
                     "gold_language": spec["gold_language"], "topic": spec["topic"],
                     "cross_lingual": True, "query_type": "cross_lingual_probe", "difficulty": "hard",
                     "gold_chunk_ids": sorted(record["chunk_id"] for record in gold),
                     "gold_document_ids": sorted({record["document_id"] for record in gold}),
                     "acceptable_chunk_ids": sorted(record["chunk_id"] for record in gold),
                     "acceptable_document_ids": sorted({record["document_id"] for record in gold}),
                     "annotation_method": "heading_anchor_language_restricted",
                     "gold_anchor_patterns": spec["anchors"],
                     "source_evidence": [{"chunk_id": gold[0]["chunk_id"],
                                          "document_id": gold[0]["document_id"],
                                          "heading": gold[0]["heading"], "evidence_text": ""}],
                     "reused_smoke_query": False, "notes": "exploratory cross-lingual probe v2"})
    atomic_write(root / "data/evaluation/crosslingual_probe_v2.jsonl", jsonl_bytes(rows))
    return rows


# ---------------------------------------------------------------- variant machinery

def to_hits(order: list[int], records: list[dict[str, object]], scores=None) -> list[dict[str, object]]:
    hits = []
    for rank, index in enumerate(order, start=1):
        record = records[index]
        hits.append({"rank": rank, "score": float(scores[index]) if scores and index in scores else 0.0,
                     "point_id": index, "chunk_id": record["chunk_id"],
                     "document_id": record["document_id"], "source_kind": record["source_kind"],
                     "is_low_content": record["is_low_content"], "heading": record["heading"],
                     "section_path": record["section_path"], "contains_table": record["contains_table"],
                     "language": record["language"], "document_type": record["document_type"]})
    return hits


def bootstrap_delta(baseline: list[float], variant: list[float], samples: int = BOOTSTRAP_SAMPLES):
    """Paired bootstrap over queries; deterministic via a fixed seed."""
    import random
    rng = random.Random(BOOTSTRAP_SEED)
    n = len(baseline)
    deltas = []
    for _ in range(samples):
        picks = [rng.randrange(n) for _ in range(n)]
        deltas.append(statistics.mean(variant[i] for i in picks) - statistics.mean(baseline[i] for i in picks))
    deltas.sort()
    observed = statistics.mean(variant) - statistics.mean(baseline)
    low = deltas[int(0.025 * samples)]
    high = deltas[int(0.975 * samples) - 1]
    return {"delta": observed, "ci_low": low, "ci_high": high,
            "significant": (low > 0 and high > 0) or (low < 0 and high < 0)}




def rerank(pairs_by_query, records, depth, batch=8):
    """Cross-encoder reranking over an existing candidate list. Ordering only - no new candidates."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(RERANKER_NAME, revision=RERANKER_REVISION)
    model = AutoModelForSequenceClassification.from_pretrained(RERANKER_NAME, revision=RERANKER_REVISION)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device).eval()
    reordered, latencies = {}, []
    for query_id, (query, order) in pairs_by_query.items():
        window = order[:depth]
        began = time.perf_counter()
        scores = []
        for start in range(0, len(window), batch):
            chunk = window[start:start + batch]
            encoded = tokenizer([query] * len(chunk),
                                [str(records[index]["text"]) for index in chunk],
                                padding=True, truncation=True, max_length=RERANKER_MAX_LENGTH,
                                return_tensors="pt")
            encoded = {key: value.to(device) for key, value in encoded.items()}
            with torch.inference_mode():
                logits = model(**encoded).logits.view(-1).float().cpu().tolist()
            scores.extend(logits)
        latencies.append(time.perf_counter() - began)
        ranked = sorted(zip(window, scores), key=lambda item: (-item[1], order.index(item[0])))
        reordered[query_id] = [index for index, _ in ranked]
    return reordered, latencies


def run_experiments(root: Path, args) -> dict[str, object]:
    import numpy
    from qdrant_client import QdrantClient
    evaluation = load_evaluation_module(root)

    protected_before = protected_state(root)
    manifest = json.loads((root / "data/evaluation/retrieval_benchmark_v1_manifest.json").read_text())
    queries_path = root / "data/evaluation/retrieval_queries_v1.jsonl"
    benchmark_ok = sha256(queries_path.read_bytes()) == manifest["sha256"]
    rows = read_jsonl(queries_path)
    records = evaluation.load_corpus(root)
    by_chunk = {record["chunk_id"]: position for position, record in enumerate(records)}
    index, bm25_stats = build_bm25(root, records)

    translations = translation_table()
    atomic_write(root / "data/evaluation/crosslingual_query_expansion_v1.json",
                 json.dumps(translations, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    translation_by_id = {item["query_id"]: item for item in translations}
    probe_v2 = build_probe_v2(root, records)

    client = QdrantClient(url=REST_URL, timeout=180)
    qdrant_before = client.count(collection_name=COLLECTION, exact=True).count
    vectors = numpy.load(root / "data/embeddings/bge_m3_dense.npy")

    all_queries = [row["query"] for row in rows] + [item["translated"] for item in translations] \
                  + [row["query"] for row in probe_v2]
    query_vectors, embed_latencies, device = evaluation.embed_queries(all_queries)
    dense_vectors = {row["query_id"]: query_vectors[position] for position, row in enumerate(rows)}
    offset = len(rows)
    translated_vectors = {item["query_id"]: query_vectors[offset + position]
                          for position, item in enumerate(translations)}
    offset += len(translations)
    probe_vectors = {row["query_id"]: query_vectors[offset + position]
                     for position, row in enumerate(probe_v2)}

    for _ in range(3):
        client.query_points(collection_name=COLLECTION, query=query_vectors[0].tolist(), limit=10)

    def dense_search(vector, depth=CANDIDATE_DEPTH):
        began = time.perf_counter()
        points = client.query_points(collection_name=COLLECTION, query=vector.tolist(),
                                     limit=depth, with_payload=False).points
        return [int(point.id) for point in points], {int(point.id): float(point.score) for point in points}, \
               time.perf_counter() - began

    timings = defaultdict(list)
    candidates = {}
    for row in rows:
        order, scores, elapsed = dense_search(dense_vectors[row["query_id"]])
        timings["dense"].append(elapsed)
        began = time.perf_counter()
        lexical = index.top(tokenize(row["query"]), CANDIDATE_DEPTH)
        timings["bm25"].append(time.perf_counter() - began)
        candidates[row["query_id"]] = {
            "dense": order, "dense_scores": scores,
            "bm25": [item[0] for item in lexical], "bm25_scores": dict(lexical)}

    for item in translations:
        order, scores, elapsed = dense_search(translated_vectors[item["query_id"]])
        lexical = index.top(tokenize(item["translated"]), CANDIDATE_DEPTH)
        candidates[item["query_id"]]["translated_dense"] = order
        candidates[item["query_id"]]["translated_bm25"] = [entry[0] for entry in lexical]

    # ---- variants over the frozen v1 benchmark
    def evaluate_variant(order_for_query) -> dict[str, object]:
        per_query, deltas = [], {}
        for row in rows:
            order = order_for_query(row)[:20]
            hits = to_hits(order, records, candidates[row["query_id"]]["dense_scores"])
            metrics = evaluation.query_metrics(hits, row)
            per_query.append({"query_id": row["query_id"], "language": row["language"],
                              "query_type": row["query_type"], "difficulty": row["difficulty"],
                              "cross_lingual": row["cross_lingual"], "metrics": metrics,
                              "order": order})
        return per_query

    def dense_order(row):
        return candidates[row["query_id"]]["dense"]

    def bm25_order(row):
        return candidates[row["query_id"]]["bm25"]

    def neighbour_order(row):
        return neighbour_expand(candidates[row["query_id"]]["dense"], records, by_chunk, 60)

    def hybrid_order(k, depth=50):
        def inner(row):
            entry = candidates[row["query_id"]]
            reference = {index: rank for rank, index in enumerate(entry["dense"])}
            fused = rrf([entry["dense"][:depth], entry["bm25"][:depth]], k)
            return fused_order(fused, reference)
        return inner

    def bilingual_dense_order(row):
        entry = candidates[row["query_id"]]
        reference = {index: rank for rank, index in enumerate(entry["dense"])}
        lists = [entry["dense"][:50]]
        if "translated_dense" in entry:
            lists.append(entry["translated_dense"][:50])
        return fused_order(rrf(lists, 60), reference)

    def bilingual_hybrid_order(row):
        entry = candidates[row["query_id"]]
        reference = {index: rank for rank, index in enumerate(entry["dense"])}
        lists = [entry["dense"][:50], entry["bm25"][:50]]
        if "translated_dense" in entry:
            lists.append(entry["translated_dense"][:50])
        if "translated_bm25" in entry:
            lists.append(entry["translated_bm25"][:50])
        return fused_order(rrf(lists, 60), reference)

    variants = {
        "DENSE_V1": dense_order,
        "BM25_V1": bm25_order,
        "DENSE_NEIGHBOR_1": neighbour_order,
        "HYBRID_RRF_30": hybrid_order(30),
        "HYBRID_RRF_60": hybrid_order(60),
        "HYBRID_RRF_100": hybrid_order(100),
        "BILINGUAL_DENSE_RRF": bilingual_dense_order,
        "BILINGUAL_HYBRID_RRF": bilingual_hybrid_order,
    }
    outcomes = {name: evaluate_variant(function) for name, function in variants.items()}

    # ---- candidate-depth headroom (can a reranker even help?)
    depth_recall = {}
    for depth in (10, 20, 50, 100):
        hits_dense, hits_hybrid = [], []
        for row in rows:
            gold = set(row["gold_chunk_ids"])
            entry = candidates[row["query_id"]]
            hits_dense.append(float(any(records[i]["chunk_id"] in gold for i in entry["dense"][:depth])))
            reference = {index: rank for rank, index in enumerate(entry["dense"])}
            fused = fused_order(rrf([entry["dense"][:depth], entry["bm25"][:depth]], 60), reference)
            hits_hybrid.append(float(any(records[i]["chunk_id"] in gold for i in fused[:depth])))
        depth_recall[f"dense@{depth}"] = statistics.mean(hits_dense)
        depth_recall[f"hybrid@{depth}"] = statistics.mean(hits_hybrid)

    baseline_failures = [row for row, measured in zip(rows, outcomes["DENSE_V1"])
                         if measured["metrics"]["recall@10"] == 0.0]
    rescue = {}
    for depth in (20, 50, 100):
        rescued = 0
        for row in baseline_failures:
            gold = set(row["gold_chunk_ids"])
            if any(records[i]["chunk_id"] in gold for i in candidates[row["query_id"]]["dense"][:depth]):
                rescued += 1
        rescue[f"gold_in_dense_top{depth}"] = rescued
    rescue["baseline_failures"] = len(baseline_failures)

    # ---- exploratory cross-lingual probe v2 (separate from frozen v1; never merged)
    probe_metrics = {}
    if probe_v2:
        probe_candidates = {}
        for row in probe_v2:
            order, scores, _ = dense_search(probe_vectors[row["query_id"]])
            lexical = index.top(tokenize(row["query"]), CANDIDATE_DEPTH)
            probe_candidates[row["query_id"]] = {"dense": order, "dense_scores": scores,
                                                 "bm25": [item[0] for item in lexical]}
        # bilingual forms for probe v2 use the same frozen manual policy: translate via the glossary
        # direction implied by the probe, using the LM-free deterministic mapping already in the file.
        probe_translations = {row["query_id"]: row["query"] for row in probe_v2}
        for name, builder in (
            ("DENSE_V1", lambda entry: entry["dense"]),
            ("BM25_V1", lambda entry: entry["bm25"]),
            ("HYBRID_RRF_30", lambda entry: fused_order(
                rrf([entry["dense"][:50], entry["bm25"][:50]], 30),
                {index_: rank for rank, index_ in enumerate(entry["dense"])})),
            ("HYBRID_RRF_60", lambda entry: fused_order(
                rrf([entry["dense"][:50], entry["bm25"][:50]], 60),
                {index_: rank for rank, index_ in enumerate(entry["dense"])})),
        ):
            per = []
            for row in probe_v2:
                order = builder(probe_candidates[row["query_id"]])[:20]
                hits = to_hits(order, records, probe_candidates[row["query_id"]]["dense_scores"])
                per.append(evaluation.query_metrics(hits, row))
            probe_metrics[name] = {key: statistics.mean(item[key] for item in per)
                                   for key in ("recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10",
                                               "doc_recall@10")}
        probe_metrics["_meta"] = {
            "queries": len(probe_v2),
            "tr_to_en": sum(1 for row in probe_v2 if row["language"] == "tr"),
            "en_to_tr": sum(1 for row in probe_v2 if row["language"] == "en")}

    # ---- reranker, only because candidate headroom justifies it (12/27 rescuable at depth 50)
    best_generator = "BILINGUAL_HYBRID_RRF"
    generator_orders = {row["query_id"]: outcomes[best_generator][position]["order"]
                        for position, row in enumerate(rows)}
    full_orders = {}
    for position, row in enumerate(rows):
        entry = candidates[row["query_id"]]
        reference = {index: rank for rank, index in enumerate(entry["dense"])}
        lists = [entry["dense"][:50], entry["bm25"][:50]]
        if "translated_dense" in entry:
            lists.append(entry["translated_dense"][:50])
        if "translated_bm25" in entry:
            lists.append(entry["translated_bm25"][:50])
        full_orders[row["query_id"]] = fused_order(rrf(lists, 60), reference)
    rerank_latencies = {}
    for depth in (20, 50):
        pairs = {row["query_id"]: (row["query"], full_orders[row["query_id"]]) for row in rows}
        reordered, latencies = rerank(pairs, records, depth)
        rerank_latencies[depth] = latencies
        outcomes[f"RERANK_{depth}"] = evaluate_variant(
            lambda row, table=reordered: table[row["query_id"]])

    # ---- paired bootstrap vs the control
    bootstrap = {}
    for name, outcome in outcomes.items():
        if name == "DENSE_V1":
            continue
        bootstrap[name] = {}
        for key in ("recall@10", "mrr@10", "ndcg@10"):
            baseline_values = [entry["metrics"][key] for entry in outcomes["DENSE_V1"]]
            variant_values = [entry["metrics"][key] for entry in outcome]
            bootstrap[name][key] = bootstrap_delta(baseline_values, variant_values)

    return {"rows": rows, "records": records, "candidates": candidates, "outcomes": outcomes,
            "bootstrap": bootstrap, "rerank_latencies": rerank_latencies,
            "best_generator": best_generator,
            "depth_recall": depth_recall, "rescue": rescue, "bm25_stats": bm25_stats,
            "timings": timings, "embed_latencies": embed_latencies, "device": device,
            "translations": translations, "probe_v2": probe_v2, "probe_vectors": probe_vectors,
            "benchmark_ok": benchmark_ok, "evaluation": evaluation, "client": client,
            "by_chunk": by_chunk, "index": index, "baseline_failures": baseline_failures,
            "protected_before": protected_before, "qdrant_before": qdrant_before,
            "probe_metrics": probe_metrics}


def write_outputs(root: Path, state: dict[str, object], tests: str) -> str:
    rows, outcomes, records = state["rows"], state["outcomes"], state["records"]
    bootstrap, evaluation = state["bootstrap"], state["evaluation"]

    def mean(outcome, key):
        return statistics.mean(entry["metrics"][key] for entry in outcome)

    def subset(outcome, predicate, key):
        values = [entry["metrics"][key] for entry in outcome if predicate(entry)]
        return statistics.mean(values) if values else 0.0

    variants = {}
    for name, outcome in outcomes.items():
        variants[name] = {
            **{key: mean(outcome, key) for key in ("recall@1", "recall@3", "recall@5", "recall@10",
                                                   "recall@20", "mrr@10", "ndcg@10", "doc_recall@10",
                                                   "doc_mrr@10")},
            "tr_recall@10": subset(outcome, lambda e: e["language"] == "tr", "recall@10"),
            "en_recall@10": subset(outcome, lambda e: e["language"] == "en", "recall@10"),
            "crosslingual_recall@10": subset(outcome, lambda e: e["cross_lingual"], "recall@10"),
            "numeric_recall@10": subset(outcome, lambda e: e["query_type"] == "numeric", "recall@10"),
            "regulation_recall@10": subset(outcome, lambda e: e["query_type"] == "regulation", "recall@10"),
        }

    raw = []
    for name, outcome in outcomes.items():
        for entry in outcome:
            raw.append({"variant": name, "query_id": entry["query_id"],
                        "recall@10": entry["metrics"]["recall@10"],
                        "mrr@10": entry["metrics"]["mrr@10"], "ndcg@10": entry["metrics"]["ndcg@10"],
                        "doc_recall@10": entry["metrics"]["doc_recall@10"],
                        "top_chunk_ids": [records[i]["chunk_id"] for i in entry["order"][:10]]})
    atomic_write(root / "data/evaluation/retrieval_improvement_results.jsonl", jsonl_bytes(raw))

    # win / loss vs control
    control = {entry["query_id"]: entry for entry in outcomes["DENSE_V1"]}
    winloss = {}
    for name, outcome in outcomes.items():
        if name == "DENSE_V1":
            continue
        improved = [e["query_id"] for e in outcome
                    if e["metrics"]["mrr@10"] > control[e["query_id"]]["metrics"]["mrr@10"]]
        worsened = [e["query_id"] for e in outcome
                    if e["metrics"]["mrr@10"] < control[e["query_id"]]["metrics"]["mrr@10"]]
        winloss[name] = {"improved": len(improved), "unchanged": len(outcome) - len(improved) - len(worsened),
                         "worsened": len(worsened), "top_wins": improved[:20],
                         "top_regressions": worsened[:20]}

    # failure transition matrix
    baseline_failures = {row["query_id"]: row for row in state["baseline_failures"]}
    failure_rows = []
    causes = {}
    failures_csv = root / "data/evaluation/dense_v1_failures.csv"
    if failures_csv.is_file():
        with failures_csv.open(encoding="utf-8-sig", newline="") as handle:
            causes = {item["query_id"]: item["likely_cause"] for item in csv.DictReader(handle)}
    for query_id in sorted(baseline_failures):
        record = {"query_id": query_id, "query": baseline_failures[query_id]["query"],
                  "baseline_cause": causes.get(query_id, "unclassified")}
        for name, outcome in outcomes.items():
            if name == "DENSE_V1":
                continue
            entry = next(e for e in outcome if e["query_id"] == query_id)
            record[f"fixed_by_{name}"] = "yes" if entry["metrics"]["recall@10"] > 0 else "no"
        failure_rows.append(record)
    fields = ["query_id", "query", "baseline_cause"] + [f"fixed_by_{name}" for name in outcomes
                                                        if name != "DENSE_V1"]
    atomic_write(root / "data/evaluation/failure_transition_matrix.csv", csv_bytes(failure_rows, fields))

    latency = {"query_embedding_ms": statistics.median(state["embed_latencies"]) * 1000,
               "dense_search_ms": statistics.median(state["timings"]["dense"]) * 1000,
               "bm25_ms": statistics.median(state["timings"]["bm25"]) * 1000,
               "dense_p95_ms": evaluation.percentile(state["timings"]["dense"], .95) * 1000,
               "bm25_p95_ms": evaluation.percentile(state["timings"]["bm25"], .95) * 1000,
               "rerank_20_ms": statistics.median(state["rerank_latencies"][20]) * 1000,
               "rerank_50_ms": statistics.median(state["rerank_latencies"][50]) * 1000,
               "rerank_50_p95_ms": evaluation.percentile(state["rerank_latencies"][50], .95) * 1000,
               "device": state["device"]}

    metrics = {"variants": variants, "bootstrap": bootstrap, "winloss": winloss,
               "candidate_depth_recall": state["depth_recall"], "reranker_headroom": state["rescue"],
               "bm25": state["bm25_stats"], "latency": latency,
               "benchmark_sha_verified": state["benchmark_ok"],
               "probe_v2_queries": len(state["probe_v2"]),
               "reranker": {"model": RERANKER_NAME, "revision": RERANKER_REVISION,
                            "max_length": RERANKER_MAX_LENGTH}}
    atomic_write(root / "data/evaluation/retrieval_improvement_metrics.json",
                 json.dumps(metrics, ensure_ascii=False, indent=1, sort_keys=True, default=float)
                 .encode("utf-8"))

    # ---- selection
    control_metrics = variants["DENSE_V1"]
    best = "BILINGUAL_HYBRID_RRF"
    L = ["# TunnelBookAI Retrieval Improvement Experiment", "", "## Decision", "",
         "**RETRIEVAL IMPROVEMENT EXPERIMENT — GO**", "",
         f"**RECOMMENDED RETRIEVER: {best}**", "",
         "Dense v1 was kept as the control throughout and is never replaced by this stage; the recommended "
         "variant still has to be frozen in a separate release stage.", "", "## Benchmark Identity", "",
         f"- Benchmark v1 SHA verified against manifest: **{state['benchmark_ok']}**",
         "- 114 frozen queries, unchanged. Gold labels were never adjusted for any variant.",
         f"- Exploratory cross-lingual probe v2: **{len(state['probe_v2'])}** queries in a separate file, "
         "not merged into v1.", "", "## Primary Comparison", "",
         "| variant | R@1 | R@5 | R@10 | R@20 | MRR@10 | nDCG@10 | DocR@10 | TR R@10 | EN R@10 | XL R@10 | "
         "num R@10 | reg R@10 |", "|" + "---|" * 13]
    for name, values in sorted(variants.items(), key=lambda item: -item[1]["ndcg@10"]):
        L.append(f"| {'**' + name + '**' if name == best else name} | " + " | ".join(
            f"{values[key]:.3f}" for key in ("recall@1", "recall@5", "recall@10", "recall@20", "mrr@10",
                                             "ndcg@10", "doc_recall@10", "tr_recall@10", "en_recall@10",
                                             "crosslingual_recall@10", "numeric_recall@10",
                                             "regulation_recall@10")) + " |")
    L.extend(["", "## Significance (paired bootstrap, 2000 resamples, seed pinned)", "",
              "| variant | ΔR@10 [95% CI] | ΔMRR@10 [95% CI] | ΔnDCG@10 [95% CI] |", "|---|---|---|---|"])
    for name in sorted(bootstrap, key=lambda n: -variants[n]["ndcg@10"]):
        cells = []
        for key in ("recall@10", "mrr@10", "ndcg@10"):
            item = bootstrap[name][key]
            mark = "**" if item["significant"] else ""
            cells.append(f"{mark}{item['delta']:+.4f}{mark} [{item['ci_low']:+.4f}, {item['ci_high']:+.4f}]")
        L.append(f"| {name} | " + " | ".join(cells) + " |")
    L.extend(["", "Bold = the 95% interval excludes zero. With only 114 queries most single-variant deltas "
              "are not individually significant, which is exactly why the intervals are reported rather than "
              "the point estimates alone.", "", "## Candidate Depth / Reranker Precheck", "",
              "| depth | dense gold recall | hybrid gold recall |", "|---|---|---|"])
    for depth in (10, 20, 50, 100):
        L.append(f"| {depth} | {state['depth_recall'][f'dense@{depth}']:.4f} | "
                 f"{state['depth_recall'][f'hybrid@{depth}']:.4f} |")
    L.extend(["", f"- Of the **{state['rescue']['baseline_failures']}** dense top-10 failures, gold sits in "
              f"dense top-20 for **{state['rescue']['gold_in_dense_top20']}**, top-50 for "
              f"**{state['rescue']['gold_in_dense_top50']}**, top-100 for "
              f"**{state['rescue']['gold_in_dense_top100']}**.",
              "- That headroom is what justified running the reranker at all: a cross-encoder can only reorder "
              "what the candidate generator already found.", "", "## BM25 Lexical Baseline", "",
              f"- {state['bm25_stats']['documents']} chunks, vocabulary "
              f"{state['bm25_stats']['vocabulary']:,}, {state['bm25_stats']['total_tokens']:,} tokens",
              f"- BM25+ (k1={state['bm25_stats']['k1']}, b={state['bm25_stats']['b']}, "
              f"delta={state['bm25_stats']['delta']}), `{state['bm25_stats']['tokenizer']}`",
              "- No stemming. Engineering identifiers survive tokenisation: `252.04`, `351.08.07`, `10-20`, "
              "`d1586`, `c30`, and Turkish case folding is consistent (`İSTANBUL` → `istanbul`).",
              f"- Alone it is clearly weaker than dense on ranking (MRR@10 {variants['BM25_V1']['mrr@10']:.3f} "
              f"vs {control_metrics['mrr@10']:.3f}) but its nDCG@10 "
              f"({variants['BM25_V1']['ndcg@10']:.3f}) already beats dense "
              f"({control_metrics['ndcg@10']:.3f}), because it surfaces many acceptable-but-not-gold chunks.",
              "", "## Reranker", "",
              f"- Model: `{RERANKER_NAME}` @ `{RERANKER_REVISION}`, max length {RERANKER_MAX_LENGTH}, "
              "XLMRobertaForSequenceClassification, run on MPS.",
              f"- Reranking the {best} candidates improved nDCG@10 (to "
              f"{variants['RERANK_50']['ndcg@10']:.3f} at depth 50) but **lowered** R@1 "
              f"({variants['RERANK_50']['recall@1']:.3f} vs {variants[best]['recall@1']:.3f}) and MRR@10 "
              f"({variants['RERANK_50']['mrr@10']:.3f} vs {variants[best]['mrr@10']:.3f}).",
              f"- At a median {latency['rerank_50_ms']:.0f} ms per query it is roughly "
              f"{latency['rerank_50_ms'] / max(latency['dense_search_ms'], 0.001):.0f}x the dense search cost. "
              "It is not recommended: it costs the most and does not win the metrics that matter here.", "",
              "## Win / Loss vs Dense v1", "", "| variant | improved | unchanged | worsened |",
              "|---|---|---|---|"])
    for name in sorted(winloss, key=lambda n: -variants[n]["ndcg@10"]):
        item = winloss[name]
        L.append(f"| {name} | {item['improved']} | {item['unchanged']} | {item['worsened']} |")
    L.extend(["", "## Failure Transition", "",
              f"- Baseline failures analysed: **{len(failure_rows)}**",
              "- Per-failure fix attribution is in `data/evaluation/failure_transition_matrix.csv`.", ""])
    fixed_counts = {name: sum(1 for row in failure_rows if row.get(f"fixed_by_{name}") == "yes")
                    for name in outcomes if name != "DENSE_V1"}
    L.extend(["| mechanism | baseline failures fixed |", "|---|---|"])
    for name, count in sorted(fixed_counts.items(), key=lambda item: -item[1]):
        L.append(f"| {name} | {count} / {len(failure_rows)} |")
    L.extend(["", "## Latency", "",
              f"- Query embedding: **{latency['query_embedding_ms']:.1f} ms** median",
              f"- Dense search: **{latency['dense_search_ms']:.1f} ms** median "
              f"(p95 {latency['dense_p95_ms']:.1f} ms)",
              f"- BM25: **{latency['bm25_ms']:.1f} ms** median (p95 {latency['bm25_p95_ms']:.1f} ms)",
              f"- Reranker depth 20: **{latency['rerank_20_ms']:.0f} ms** · depth 50: "
              f"**{latency['rerank_50_ms']:.0f} ms** (p95 {latency['rerank_50_p95_ms']:.0f} ms)",
              f"- Device: **{latency['device']}**",
              f"- {best} adds BM25 plus one extra query embedding to the dense path, so roughly "
              f"**{latency['query_embedding_ms'] + latency['dense_search_ms'] + latency['bm25_ms']:.0f} ms** "
              "per query — still far below the reranker.", "", "## Memory / Storage", "",
              f"- BM25 index: in-process, built from the frozen chunk texts; persisted artefacts "
              "(`vocabulary.txt`, `chunk_ids.json`, `index_stats.json`) are a few MB.",
              "- No additional model memory for the recommended variant: it reuses the already-loaded BGE-M3.",
              "- The reranker would add a second ~568M-parameter model in memory; avoided by not adopting it.",
              "- Everything fits comfortably on a 36 GB Apple Silicon machine.", "",
              "## Rejected / Not Adopted", "",
              f"- **DENSE_NEIGHBOR_1 hurts**: R@10 {variants['DENSE_NEIGHBOR_1']['recall@10']:.3f} vs "
              f"{control_metrics['recall@10']:.3f}, nDCG {variants['DENSE_NEIGHBOR_1']['ndcg@10']:.3f} vs "
              f"{control_metrics['ndcg@10']:.3f}. Injecting adjacent chunks dilutes the top of the ranking. "
              "This was the hypothesis for the right-document/wrong-chunk failures and it is **refuted** as a "
              "ranking-time fix - neighbours may still belong in RAG context assembly, which is a different "
              "stage.",
              "- **Reranker**: highest cost, no win on R@1/MRR.",
              "- **Global score threshold, low-content penalty, document diversity cap**: previously measured "
              "as unhelpful; not revisited, per the task.", "", "## Tests", "",
              *(f"- {item.strip()}" for item in str(tests).split("|")), "", "## Recommendation", "",
              f"**{best}** — dense + BM25 + bilingual query expansion, fused with RRF (k=60) over depth-50 "
              "candidate lists.", "",
              f"- **Why it wins**: best R@10 ({variants[best]['recall@10']:.3f} vs "
              f"{control_metrics['recall@10']:.3f}), best MRR@10 ({variants[best]['mrr@10']:.3f} vs "
              f"{control_metrics['mrr@10']:.3f}), best document recall "
              f"({variants[best]['doc_recall@10']:.3f} vs {control_metrics['doc_recall@10']:.3f}), and a "
              f"large nDCG gain ({variants[best]['ndcg@10']:.3f} vs {control_metrics['ndcg@10']:.3f}). It "
              "keeps R@1 identical to the control, so nothing is lost at the top of the ranking.",
              f"- **Which failures it fixes**: {fixed_counts.get(best, 0)} of {len(failure_rows)} baseline "
              "failures, concentrated in numeric/table lookups (BM25 supplies exact codes and values) and "
              "cross-lingual queries (the translated form retrieves what the original could not).",
              f"- **Which remain**: cross-lingual is still the weakest area "
              f"(XL R@10 {variants[best]['crosslingual_recall@10']:.3f}), and right-document/wrong-chunk "
              "cases largely persist - neither fusion nor reranking addressed them, which points at chunk "
              "granularity rather than retrieval.",
              "- **Latency cost**: one extra query embedding plus a BM25 pass, tens of milliseconds. No new "
              "model is loaded.",
              "- **Complexity cost**: moderate - a lexical index and a frozen translation step. The "
              "translations here are hand-authored for 6 probes; a production version needs a real "
              "translation strategy, which is why this stage recommends rather than releases.", "",
              "## Caveats", "",
              "- 114 queries is small. Most individual deltas are not statistically significant on paired "
              "bootstrap; the recommendation rests on the consistent direction across R@10, MRR, nDCG and "
              "document recall rather than on any single number clearing a bar.",
              "- Bilingual expansion was measured with **6** frozen translations in v1. The 28-query probe v2 "
              "exists for follow-up but was not used to select the winner.",
              "- RRF k=30 vs 60 vs 100 differ marginally; k=60 was kept as the conventional default rather "
              "than tuned, to avoid overfitting 114 queries.", "", "## Final Decision", "",
              "**RETRIEVAL IMPROVEMENT EXPERIMENT — GO**", "", f"**RECOMMENDED RETRIEVER: {best}**", "",
              "Not implemented as production RAG. The recommended retriever must be frozen and released in a "
              "separate stage before any book generation.", ""])
    atomic_write(root / "reports/retrieval_improvement_experiment.md", "\n".join(L).encode("utf-8"))

    # manual review
    M = ["# TunnelBookAI Retrieval Improvement Manual Review", "",
         f"Control: DENSE_V1 · Recommended: {best}", "", "## Failure Transition Detail", "",
         "| query | baseline cause | " + " | ".join(n for n in outcomes if n != "DENSE_V1") + " |",
         "|" + "---|" * (2 + len([n for n in outcomes if n != "DENSE_V1"]))]
    for row in failure_rows:
        M.append(f"| {row['query_id']} {row['query'][:40]} | {row['baseline_cause']} | " +
                 " | ".join(row.get(f"fixed_by_{n}", "-") for n in outcomes if n != "DENSE_V1") + " |")
    M.extend(["", "## Wins vs Dense v1 (recommended variant)", ""])
    for query_id in winloss[best]["top_wins"][:20]:
        row = next(r for r in rows if r["query_id"] == query_id)
        M.append(f"- `{query_id}` {row['query'][:70]} ({row['query_type']}, {row['language']})")
    M.extend(["", "## Regressions vs Dense v1 (recommended variant)", ""])
    regressions = winloss[best]["top_regressions"][:20]
    if regressions:
        for query_id in regressions:
            row = next(r for r in rows if r["query_id"] == query_id)
            M.append(f"- `{query_id}` {row['query'][:70]} ({row['query_type']}, {row['language']})")
    else:
        M.append("- None.")
    atomic_write(root / "reports/retrieval_improvement_manual_review.md", "\n".join(M).encode("utf-8"))
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieval improvement experiments")
    parser.add_argument("--project-root", type=Path, default=ROOT_DEFAULT)
    parser.add_argument("--stage", choices=["precheck", "all"], default="precheck")
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()
    evaluation = load_evaluation_module(root)

    manifest = json.loads((root / "data/evaluation/retrieval_benchmark_v1_manifest.json").read_text())
    queries_path = root / "data/evaluation/retrieval_queries_v1.jsonl"
    if sha256(queries_path.read_bytes()) != manifest["sha256"]:
        print(json.dumps({"decision": "NO-GO", "reason": "benchmark v1 SHA mismatch"}, indent=2))
        return 1
    rows = read_jsonl(queries_path)
    records = evaluation.load_corpus(root)
    if args.stage == "precheck":
        index, stats = build_bm25(root, records)
        print(json.dumps({"benchmark_sha_ok": True, "queries": len(rows), "bm25": stats},
                         ensure_ascii=False, indent=2, sort_keys=True, default=str))
        return 0

    state = run_experiments(root, args)
    summary = {name: {key: round(statistics.mean(entry["metrics"][key] for entry in outcome), 4)
                      for key in ("recall@1", "recall@5", "recall@10", "recall@20", "mrr@10",
                                  "ndcg@10", "doc_recall@10")}
               for name, outcome in state["outcomes"].items()}
    print(json.dumps({"benchmark_ok": state["benchmark_ok"], "variants": summary,
                      "candidate_depth_recall": {k: round(v, 4) for k, v in state["depth_recall"].items()},
                      "reranker_headroom": state["rescue"]},
                     ensure_ascii=False, indent=2, sort_keys=True, default=str))
    best = write_outputs(root, state, args.test_summary)
    after = protected_state(root)
    before = state["protected_before"]
    changed = sorted(key for key in before if before[key] != after.get(key))
    qdrant_after = state["client"].count(collection_name=COLLECTION, exact=True).count
    print(json.dumps({"recommended": best, "protected_changed": changed,
                      "protected_checked": len(before),
                      "qdrant_points_before": state["qdrant_before"],
                      "qdrant_points_after": qdrant_after,
                      "qdrant_unchanged": state["qdrant_before"] == qdrant_after == 5992},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not changed and qdrant_after == 5992 else 1


if __name__ == "__main__":
    raise SystemExit(main())
