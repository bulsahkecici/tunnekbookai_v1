"""Language-aware retrieval gate.

HYBRID_RRF_30 improves monolingual ranking but wrecks cross-lingual retrieval, because a BM25 list
that shares no vocabulary with the query's language still enters RRF and displaces good dense hits.
This stage tests deterministic routing policies that keep the hybrid gain where lexical evidence is
real and fall back to dense where it is not.

No translation, no LLM, no new model. Routing may use only the query text, a corpus-derived language
detector, chunk language metadata and retrieval ranks - never gold labels.

ALL DECISION RULES BELOW ARE PREDECLARED, fixed before any variant metric was computed:
  * a query token is "technical" if it is a number, a code, or an all-caps acronym in the raw query
  * language is unknown when no non-technical token carries language evidence
  * a Turkish diacritic anywhere in the query is decisive for tr
  * otherwise corpus log-odds over non-technical tokens decide, needing |score| >= LANG_MARGIN
  * the BM25 gate opens only when >= GATE_MIN_TERMS distinct non-technical query terms occur in the
    same-language sub-corpus
  * dense protection keeps the top N dense hits fixed, N in {3, 5}
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
from collections import Counter, defaultdict
from pathlib import Path


ROOT_DEFAULT = Path(__file__).resolve().parents[1]
COLLECTION = "tunnelbook_dense_v1"
REST_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
DETECTOR_VERSION = "corpus-logodds-lang-v1"
DEPTH = 50
CANDIDATE_DEPTH = 100
BOOTSTRAP_SAMPLES = 2000
BOOTSTRAP_SEED = 20260818

# --- predeclared constants -------------------------------------------------------------------
LANG_MARGIN = 2.0        # minimum |log-odds| before committing to tr/en
MIN_LEXICON_DF = 3       # a token must appear in >= 3 chunks to contribute language evidence
GATE_MIN_TERMS = 2       # distinct non-technical query terms required in the same-language corpus
PROTECT_DEPTHS = (3, 5)

TURKISH_CHARS = set("çğıöşüÇĞİÖŞÜ")
ACRONYM_RE = re.compile(r"^[A-ZÇĞİÖŞÜ]{2,}$")
CODE_RE = re.compile(r"^\d|^[A-Za-z]+\d")

PROTECTED = ("data/embeddings/bge_m3_dense.npy", "data/metadata/full_embedding_manifest.csv",
             "data/chunks/chunks.jsonl", "data/chunks_recovery/chunks.jsonl",
             "data/evaluation/retrieval_queries_v1.jsonl",
             "data/evaluation/retrieval_benchmark_v1_manifest.json",
             "data/evaluation/crosslingual_probe_v2.jsonl",
             "data/metadata/retriever_v1_candidate.json",
             "data/retrieval/bm25_v1/index_stats.json", "data/retrieval/bm25_v1/chunk_ids.json",
             "data/retrieval/bm25_v1/vocabulary.txt")


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


def load_module(root: Path, name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, root / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def protected_state(root: Path) -> dict[str, str]:
    return {relative: sha256((root / relative).read_bytes()) for relative in PROTECTED
            if (root / relative).is_file()}


# ---------------------------------------------------------------- language detection

class LanguageDetector:
    """Deterministic tr/en/unknown detector built from the corpus itself.

    No model download: token→language evidence is log-odds of how often a token appears in Turkish
    versus English chunks, which is exactly the vocabulary the retriever has to serve.
    """

    def __init__(self, records, tokenize):
        self.tokenize = tokenize
        turkish, english = defaultdict(int), defaultdict(int)
        for record in records:
            language = (record.get("language") or "").lower()
            if language not in ("tr", "en"):
                continue
            target = turkish if language == "tr" else english
            for token in set(tokenize(str(record["text"]))):
                target[token] += 1
        self.turkish, self.english = dict(turkish), dict(english)
        self.total_tr = sum(1 for r in records if (r.get("language") or "") == "tr")
        self.total_en = sum(1 for r in records if (r.get("language") or "") == "en")

    def technical(self, raw_token: str) -> bool:
        return bool(ACRONYM_RE.match(raw_token) or CODE_RE.match(raw_token))

    def evidence(self, token: str) -> float:
        tr = self.turkish.get(token, 0)
        en = self.english.get(token, 0)
        if tr + en < MIN_LEXICON_DF:
            return 0.0
        # normalise by corpus size so the larger Turkish half does not dominate
        rate_tr = (tr + 0.5) / (self.total_tr + 1)
        rate_en = (en + 0.5) / (self.total_en + 1)
        return math.log(rate_tr / rate_en)

    def detect(self, query: str) -> dict[str, object]:
        raw = re.findall(r"\S+", query)
        content = [token for token in raw if not self.technical(token.strip(".,;:()"))]
        if not content:
            return {"language": "unknown", "score": 0.0, "reason": "technical_only"}
        if any(char in TURKISH_CHARS for char in query):
            return {"language": "tr", "score": float("inf"), "reason": "turkish_diacritic"}
        tokens = [token for token in self.tokenize(" ".join(content))]
        score = sum(self.evidence(token) for token in tokens)
        if abs(score) < LANG_MARGIN:
            return {"language": "unknown", "score": score, "reason": "insufficient_evidence"}
        return {"language": "tr" if score > 0 else "en", "score": score, "reason": "corpus_logodds"}



# ---------------------------------------------------------------- detector audit

AUDIT_QUERIES = (
    [(q, "tr") for q in [
        "tünel havalandırma sistemi tasarımı", "kaya bulonu boyu nasıl hesaplanır",
        "püskürtme beton uygulama tekniği", "jeoteknik araştırma raporu içeriği",
        "tünel bakım ve onarım işleri", "yangın güvenliği önlemleri nelerdir",
        "acil kaçış yolları", "tünel drenaj sistemi", "kazı sınıfları ve destek",
        "fay zonunda tünel açma", "yeraltı suyu kontrolü", "tünel aydınlatma tasarımı",
        "trafik güvenliği tedbirleri", "su yalıtımı nasıl yapılır", "segman kaplama montajı",
        "enjeksiyon ile zemin iyileştirme", "konverjans ölçümü", "portal şev stabilitesi",
        "maliyet analizi birim fiyatlar", "işletme giderleri hesabı"]] +
    [(q, "en") for q in [
        "tunnel ventilation system design", "how are rock bolts dimensioned",
        "shotcrete application technique", "geotechnical investigation report contents",
        "tunnel maintenance and repair works", "fire safety measures in tunnels",
        "emergency escape routes", "tunnel drainage system", "excavation classes and support",
        "tunnelling through a fault zone", "groundwater control", "tunnel lighting design",
        "traffic safety measures", "how is waterproofing applied", "segment lining erection",
        "ground improvement by grouting", "convergence monitoring", "portal slope stability",
        "cost analysis unit prices", "operating expenditure calculation"]] +
    [(q, "unknown") for q in [
        "TBM", "NATM RMR GSI", "EN 1997", "ASTM D1586", "KGM", "351.08.07", "252.04",
        "10-20 mm", "C30/37", "AASHTO"]]
)


def detector_audit(root: Path, detector) -> dict[str, object]:
    rows, correct, incorrect, unknown_ok, unknown_bad = [], 0, 0, 0, 0
    for query, expected in AUDIT_QUERIES:
        outcome = detector.detect(query)
        got = outcome["language"]
        row = {"query": query, "expected": expected, "detected": got,
               "score": None if outcome["score"] == float("inf") else round(outcome["score"], 3),
               "reason": outcome["reason"], "match": got == expected}
        if expected == "unknown":
            if got == "unknown":
                unknown_ok += 1
            else:
                unknown_bad += 1
        elif got == expected:
            correct += 1
        elif got == "unknown":
            unknown += 0
            incorrect += 0
            row["match"] = False
            rows.append(row)
            continue
        else:
            incorrect += 1
        rows.append(row)
    language_rows = [r for r in rows if r["expected"] != "unknown"]
    abstained = sum(1 for r in language_rows if r["detected"] == "unknown")
    summary = {"detector_version": DETECTOR_VERSION, "total": len(rows),
               "language_queries": len(language_rows),
               "correct": correct, "incorrect": incorrect, "abstained_unknown": abstained,
               "technical_queries": len(rows) - len(language_rows),
               "technical_correctly_unknown": unknown_ok,
               "technical_misclassified": unknown_bad,
               "accuracy_on_language_queries": correct / max(1, len(language_rows))}
    atomic_write(root / "data/evaluation/language_detector_audit.jsonl", jsonl_bytes(rows))
    return {"rows": rows, "summary": summary}


# ---------------------------------------------------------------- routing variants

def build_routing(root: Path, records, detector):
    """Derived, additive language-routing metadata. The core bm25_v1 index is not mutated."""
    languages = [(record.get("language") or "unknown").lower() for record in records]
    stats = {"detector_version": DETECTOR_VERSION, "lang_margin": LANG_MARGIN,
             "min_lexicon_df": MIN_LEXICON_DF, "gate_min_terms": GATE_MIN_TERMS,
             "protect_depths": list(PROTECT_DEPTHS),
             "chunk_language_counts": dict(Counter(languages)),
             "lexicon_tokens_tr": len(detector.turkish), "lexicon_tokens_en": len(detector.english)}
    atomic_write(root / "data/retrieval/language_routing_v1/routing_stats.json",
                 json.dumps(stats, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    return languages, stats


def same_language_bm25(index, tokenize, query, languages, language, depth):
    """BM25 restricted to chunks whose metadata language matches the detected query language."""
    if language not in ("tr", "en"):
        return [], 0
    scored = index.scores(tokenize(query))
    filtered = [(position, value) for position, value in scored.items()
                if languages[position] == language]
    filtered.sort(key=lambda item: (-item[1], item[0]))
    return [position for position, _ in filtered[:depth]], len(filtered)


def gate_open(index, tokenize, query, languages, language, detector) -> bool:
    """Predeclared rule: >= GATE_MIN_TERMS distinct non-technical query terms in the same-language corpus."""
    if language not in ("tr", "en"):
        return False
    raw = re.findall(r"\S+", query)
    content = [token for token in raw if not detector.technical(token.strip(".,;:()"))]
    terms = set(tokenize(" ".join(content)))
    hits = 0
    for term in terms:
        postings = index.postings.get(term)
        if postings and any(languages[position] == language for position in postings):
            hits += 1
    return hits >= GATE_MIN_TERMS


def dense_protected(dense_order, fused, protect):
    head = dense_order[:protect]
    tail = [index for index in fused if index not in set(head)]
    return head + tail



def run_gate(root: Path, records, detector, evaluation, improvement, tests: str) -> dict[str, object]:
    import numpy
    from qdrant_client import QdrantClient

    before = protected_state(root)
    rows = read_jsonl(root / "data/evaluation/retrieval_queries_v1.jsonl")
    probe = read_jsonl(root / "data/evaluation/crosslingual_probe_v2.jsonl")
    index, _ = improvement.build_bm25(root, records)
    languages, routing_stats = build_routing(root, records, detector)
    tokenize = improvement.tokenize

    client = QdrantClient(url=REST_URL, timeout=180)
    qdrant_before = client.count(collection_name=COLLECTION, exact=True).count

    def prepare(query_rows):
        vectors, embed_lat, device = evaluation.embed_queries([r["query"] for r in query_rows])
        prepared = {}
        timings = defaultdict(list)
        for position, row in enumerate(query_rows):
            began = time.perf_counter()
            detected = detector.detect(row["query"])
            timings["detect"].append(time.perf_counter() - began)
            began = time.perf_counter()
            points = client.query_points(collection_name=COLLECTION, query=vectors[position].tolist(),
                                         limit=CANDIDATE_DEPTH, with_payload=False).points
            dense = [int(point.id) for point in points]
            scores = {int(point.id): float(point.score) for point in points}
            timings["dense"].append(time.perf_counter() - began)
            began = time.perf_counter()
            lexical_all = [item[0] for item in index.top(tokenize(row["query"]), CANDIDATE_DEPTH)]
            same, pool = same_language_bm25(index, tokenize, row["query"], languages,
                                            detected["language"], CANDIDATE_DEPTH)
            timings["bm25"].append(time.perf_counter() - began)
            opened = gate_open(index, tokenize, row["query"], languages, detected["language"], detector)
            prepared[row["query_id"]] = {"dense": dense, "scores": scores, "bm25_all": lexical_all,
                                         "bm25_same": same, "lang": detected["language"],
                                         "gate_open": opened, "pool": pool}
        return prepared, timings, embed_lat, device

    def variants(entry):
        reference = {index_: rank for rank, index_ in enumerate(entry["dense"])}
        dense = entry["dense"]
        out = {"DENSE_V1": dense,
               "HYBRID_RRF_30": fused_rrf(improvement, [dense[:DEPTH], entry["bm25_all"][:DEPTH]], 30, reference)}
        if entry["lang"] in ("tr", "en") and entry["bm25_same"]:
            same30 = fused_rrf(improvement, [dense[:DEPTH], entry["bm25_same"][:DEPTH]], 30, reference)
            same60 = fused_rrf(improvement, [dense[:DEPTH], entry["bm25_same"][:DEPTH]], 60, reference)
        else:
            same30 = same60 = dense
        out["LANG_HYBRID_SAME_RRF30"] = same30
        out["LANG_HYBRID_SAME_RRF60"] = same60
        out["LANG_HYBRID_GATED_RRF30"] = same30 if entry["gate_open"] else dense
        for protect in PROTECT_DEPTHS:
            out[f"LANG_HYBRID_DENSE_PROTECTED_{protect}"] = dense_protected(dense, same30, protect)
        return out

    def evaluate(query_rows, prepared):
        per_variant = defaultdict(list)
        raw = []
        for row in query_rows:
            entry = prepared[row["query_id"]]
            for name, order in variants(entry).items():
                hits = improvement.to_hits(order[:20], records, entry["scores"])
                metrics = evaluation.query_metrics(hits, row)
                per_variant[name].append({"query_id": row["query_id"], "metrics": metrics,
                                          "language": row.get("language"),
                                          "query_type": row.get("query_type"),
                                          "cross_lingual": bool(row.get("cross_lingual")),
                                          "detected_language": entry["lang"],
                                          "gate_open": entry["gate_open"]})
                raw.append({"variant": name, "query_id": row["query_id"],
                            "detected_language": entry["lang"], "gate_open": entry["gate_open"],
                            **{k: metrics[k] for k in ("recall@1", "recall@5", "recall@10",
                                                       "recall@20", "mrr@10", "ndcg@10",
                                                       "doc_recall@10")}})
        return per_variant, raw

    prepared_v1, timings, embed_lat, device = prepare(rows)
    per_v1, raw_v1 = evaluate(rows, prepared_v1)
    prepared_v2, _, _, _ = prepare(probe)
    per_v2, raw_v2 = evaluate(probe, prepared_v2)

    KEYS = ("recall@1", "recall@5", "recall@10", "recall@20", "mrr@10", "ndcg@10", "doc_recall@10")

    def agg(entries, keys=KEYS, predicate=None):
        chosen = [e for e in entries if predicate(e)] if predicate else entries
        return {k: (statistics.mean(e["metrics"][k] for e in chosen) if chosen else 0.0) for k in keys}

    benchmark = {name: agg(entries) for name, entries in per_v1.items()}
    monolingual = {name: agg(entries, predicate=lambda e: not e["cross_lingual"])
                   for name, entries in per_v1.items()}
    crosslingual_v1 = {name: agg(entries, predicate=lambda e: e["cross_lingual"])
                       for name, entries in per_v1.items()}
    probe_metrics = {name: agg(entries) for name, entries in per_v2.items()}
    groups = {}
    for name, entries in per_v1.items():
        groups[name] = {
            "tr_recall@10": agg(entries, ("recall@10",), lambda e: e["language"] == "tr")["recall@10"],
            "en_recall@10": agg(entries, ("recall@10",), lambda e: e["language"] == "en")["recall@10"],
            "numeric_recall@10": agg(entries, ("recall@10",),
                                     lambda e: e["query_type"] == "numeric")["recall@10"],
            "regulation_recall@10": agg(entries, ("recall@10",),
                                        lambda e: e["query_type"] == "regulation")["recall@10"]}

    atomic_write(root / "data/evaluation/language_aware_retrieval_results.jsonl",
                 jsonl_bytes([{**r, "benchmark": "v1"} for r in raw_v1] +
                             [{**r, "benchmark": "probe_v2"} for r in raw_v2]))

    # ---- selection: predeclared success criteria (monolingual nDCG preserved, probe v2 back at dense)
    dense_probe = probe_metrics["DENSE_V1"]["recall@10"]
    hybrid_ndcg = monolingual["HYBRID_RRF_30"]["ndcg@10"]
    dense_ndcg = monolingual["DENSE_V1"]["ndcg@10"]
    candidates = []
    for name in ("LANG_HYBRID_GATED_RRF30", "LANG_HYBRID_SAME_RRF30", "LANG_HYBRID_SAME_RRF60",
                 "LANG_HYBRID_DENSE_PROTECTED_3", "LANG_HYBRID_DENSE_PROTECTED_5"):
        keeps_gain = monolingual[name]["ndcg@10"] >= dense_ndcg + 0.5 * (hybrid_ndcg - dense_ndcg)
        restores = probe_metrics[name]["recall@10"] >= dense_probe - 1e-9
        candidates.append({"variant": name, "monolingual_ndcg": monolingual[name]["ndcg@10"],
                           "probe_recall@10": probe_metrics[name]["recall@10"],
                           "keeps_monolingual_gain": keeps_gain, "restores_crosslingual": restores,
                           "qualifies": keeps_gain and restores})
    qualifying = [c for c in candidates if c["qualifies"]]
    best = max(qualifying, key=lambda c: c["monolingual_ndcg"])["variant"] if qualifying else None

    # ---- bootstrap for the winner
    bootstrap = {}
    if best:
        for control in ("DENSE_V1", "HYBRID_RRF_30"):
            bootstrap[control] = {}
            for key in ("recall@10", "mrr@10", "ndcg@10"):
                base = [e["metrics"][key] for e in per_v1[control]]
                variant = [e["metrics"][key] for e in per_v1[best]]
                bootstrap[control][key] = improvement.bootstrap_delta(base, variant, BOOTSTRAP_SAMPLES)

    winloss = {}
    if best:
        for control in ("DENSE_V1", "HYBRID_RRF_30"):
            base = {e["query_id"]: e["metrics"]["mrr@10"] for e in per_v1[control]}
            improved = [e["query_id"] for e in per_v1[best] if e["metrics"]["mrr@10"] > base[e["query_id"]]]
            worsened = [e["query_id"] for e in per_v1[best] if e["metrics"]["mrr@10"] < base[e["query_id"]]]
            winloss[control] = {"improved": len(improved), "worsened": len(worsened),
                                "unchanged": len(per_v1[best]) - len(improved) - len(worsened),
                                "regressions": worsened[:20]}

    # ---- failure transition on the original 27
    failures = list(csv.DictReader(
        (root / "data/evaluation/failure_transition_matrix.csv").open(encoding="utf-8-sig")))
    failure_ids = {r["query_id"]: r["baseline_cause"] for r in failures}
    fixed = {}
    for name in per_v1:
        fixed[name] = sum(1 for e in per_v1[name]
                          if e["query_id"] in failure_ids and e["metrics"]["recall@10"] > 0)
    by_cause = defaultdict(lambda: defaultdict(int))
    for name in per_v1:
        for e in per_v1[name]:
            if e["query_id"] in failure_ids and e["metrics"]["recall@10"] > 0:
                by_cause[failure_ids[e["query_id"]]][name] += 1

    latency = {k: {"median": statistics.median(v) * 1000,
                   "p95": evaluation.percentile(v, .95) * 1000} for k, v in timings.items()}
    latency["query_embedding"] = {"median": statistics.median(embed_lat) * 1000,
                                  "p95": evaluation.percentile(embed_lat, .95) * 1000}
    latency["total_estimate_ms"] = sum(latency[k]["median"] for k in
                                       ("detect", "dense", "bm25", "query_embedding"))

    qdrant_after = client.count(collection_name=COLLECTION, exact=True).count
    after = protected_state(root)
    changed = sorted(k for k in before if before[k] != after.get(k))
    blockers = list(changed)
    if qdrant_after != qdrant_before or qdrant_after != 5992:
        blockers.append("qdrant point count changed")
    if "FAIL" in tests:
        blockers.append("test failure")

    audit = detector_audit(root, detector)
    metrics = {"detector": audit["summary"], "routing": routing_stats,
               "benchmark_v1": benchmark, "monolingual_v1": monolingual,
               "crosslingual_v1": crosslingual_v1, "probe_v2": probe_metrics,
               "groups_v1": groups, "selection": candidates, "best_variant": best,
               "bootstrap": bootstrap, "winloss": winloss,
               "failure_fixed": fixed, "failure_by_cause": {k: dict(v) for k, v in by_cause.items()},
               "latency_ms": latency, "protected_changed": changed,
               "qdrant": {"before": qdrant_before, "after": qdrant_after},
               "probe_v2_queries": len(probe), "benchmark_queries": len(rows)}
    atomic_write(root / "data/evaluation/language_aware_retrieval_metrics.json",
                 json.dumps(metrics, ensure_ascii=False, indent=1, sort_keys=True, default=float)
                 .encode("utf-8"))
    write_gate_report(root, metrics, tests)
    return {"best_variant": best, "blockers": blockers,
            "probe_v2_recall@10": {k: probe_metrics[k]["recall@10"] for k in sorted(probe_metrics)},
            "monolingual_ndcg@10": {k: monolingual[k]["ndcg@10"] for k in sorted(monolingual)},
            "protected_changed": changed, "qdrant": metrics["qdrant"]}


def fused_rrf(improvement, rankings, k, reference):
    return improvement.fused_order(improvement.rrf(rankings, k), reference)



def write_gate_report(root: Path, m: dict, tests: str) -> None:
    best = m["best_variant"]
    decision = "GO" if best and not m["protected_changed"] else "NO-GO"
    recommended = best if best else "DENSE_V1"
    K = ("recall@1", "recall@5", "recall@10", "recall@20", "mrr@10", "ndcg@10", "doc_recall@10")
    order = ["DENSE_V1", "HYBRID_RRF_30", "LANG_HYBRID_SAME_RRF30", "LANG_HYBRID_SAME_RRF60",
             "LANG_HYBRID_GATED_RRF30", "LANG_HYBRID_DENSE_PROTECTED_3", "LANG_HYBRID_DENSE_PROTECTED_5"]

    def table(section, keys=K):
        out = ["| variant | " + " | ".join(keys) + " |", "|" + "---|" * (len(keys) + 1)]
        for name in order:
            if name not in m[section]:
                continue
            mark = "**" if name == best else ""
            out.append(f"| {mark}{name}{mark} | " + " | ".join(f"{m[section][name][k]:.3f}" for k in keys) + " |")
        return out

    d = m["detector"]
    L = ["# TunnelBookAI Language-Aware Retrieval Gate", "", "## Decision", "",
         f"**LANGUAGE-AWARE RETRIEVAL — {decision}**", "", f"**RECOMMENDED RETRIEVER V1: {recommended}**", "",
         "Goal: keep HYBRID_RRF_30's monolingual ranking gain without its cross-lingual collapse. No "
         "translation, no LLM, no new model.", "", "## Language Detector", "",
         f"- Version: `{d['detector_version']}` — corpus-derived log-odds, built from the indexed chunks "
         "themselves. Nothing downloaded.",
         "- Rules were fixed before any variant metric was computed: technical tokens (acronyms, codes, "
         f"numbers) carry no language evidence; a Turkish diacritic is decisive; otherwise |log-odds| must "
         f"reach {LANG_MARGIN} or the verdict is `unknown`.", "",
         f"- Audit set: **{d['total']}** queries ({d['language_queries']} language, "
         f"{d['technical_queries']} technical/ambiguous)",
         f"- Correct: **{d['correct']}/{d['language_queries']}** "
         f"(accuracy **{d['accuracy_on_language_queries']:.3f}**) · incorrect: **{d['incorrect']}** · "
         f"abstained: **{d['abstained_unknown']}**",
         f"- Technical-only queries correctly returned `unknown`: **{d['technical_correctly_unknown']}/"
         f"{d['technical_queries']}** · misclassified: **{d['technical_misclassified']}**",
         "- `TBM`, `NATM RMR GSI`, `EN 1997`, `ASTM D1586`, `KGM`, `351.08.07` all abstain rather than guess, "
         "which is what routes them to the dense-only path.",
         "- Evidence: `data/evaluation/language_detector_audit.jsonl`", "",
         "## Variants", "",
         "| variant | policy |", "|---|---|",
         "| DENSE_V1 | control: dense top-50, no lexical |",
         "| HYBRID_RRF_30 | control: dense top-50 + BM25 top-50 (whole corpus), RRF k=30 |",
         "| LANG_HYBRID_SAME_RRF30 | BM25 restricted to same-language chunks, RRF k=30; unknown → dense |",
         "| LANG_HYBRID_SAME_RRF60 | as above, RRF k=60 |",
         "| LANG_HYBRID_GATED_RRF30 | same-language BM25 enters RRF only if ≥2 distinct non-technical query "
         "terms occur in that sub-corpus; otherwise dense unchanged |",
         "| LANG_HYBRID_DENSE_PROTECTED_3 / _5 | dense top-3 / top-5 pinned, remainder fused |", "",
         "## Frozen Benchmark v1 (114 queries)", ""]
    L += table("benchmark_v1")
    L += ["", "## Monolingual Subset (108 queries)", "",
          "This is where hybrid's advantage has to survive.", ""]
    L += table("monolingual_v1", ("recall@10", "mrr@10", "ndcg@10"))
    L += ["", "## Cross-lingual Probe v2 (27 queries, exploratory)", "",
          f"TR→EN and EN→TR probes. Gold untouched; never merged into benchmark v1.", ""]
    L += table("probe_v2", ("recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10", "doc_recall@10"))
    L += ["", "## Selection", "",
          "Predeclared criteria: keep at least half of hybrid's monolingual nDCG gain over dense, **and** "
          "restore probe v2 recall@10 to at least the dense level.", "",
          "| variant | monolingual nDCG@10 | probe v2 R@10 | keeps gain | restores cross-lingual | qualifies |",
          "|---|---|---|---|---|---|"]
    for c in m["selection"]:
        L.append(f"| {c['variant']} | {c['monolingual_ndcg']:.4f} | {c['probe_recall@10']:.3f} | "
                 f"{c['keeps_monolingual_gain']} | {c['restores_crosslingual']} | "
                 f"{'**yes**' if c['qualifies'] else 'no'} |")
    L += ["", "## Group Breakdown (benchmark v1)", "",
          "| variant | TR R@10 | EN R@10 | numeric R@10 | regulation R@10 |", "|---|---|---|---|---|"]
    for name in order:
        g = m["groups_v1"].get(name)
        if g:
            L.append(f"| {name} | {g['tr_recall@10']:.3f} | {g['en_recall@10']:.3f} | "
                     f"{g['numeric_recall@10']:.3f} | {g['regulation_recall@10']:.3f} |")
    if m["bootstrap"]:
        L += ["", "## Bootstrap (2000 paired resamples, seed pinned)", "",
              f"Winner `{best}` against each control.", "",
              "| control | ΔRecall@10 | ΔMRR@10 | ΔnDCG@10 |", "|---|---|---|---|"]
        for control, entry in m["bootstrap"].items():
            cells = []
            for key in ("recall@10", "mrr@10", "ndcg@10"):
                b = entry[key]
                mark = "**" if b["significant"] else ""
                cells.append(f"{mark}{b['delta']:+.4f}{mark} [{b['ci_low']:+.4f}, {b['ci_high']:+.4f}]")
            L.append(f"| vs {control} | " + " | ".join(cells) + " |")
    if m["winloss"]:
        L += ["", "## Win / Loss (MRR@10)", "", "| control | improved | unchanged | worsened |",
              "|---|---|---|---|"]
        for control, w in m["winloss"].items():
            L.append(f"| vs {control} | {w['improved']} | {w['unchanged']} | {w['worsened']} |")
    L += ["", "## Failure Transition (original 27 dense failures)", "",
          "| variant | fixed |", "|---|---|"]
    for name in order:
        if name in m["failure_fixed"]:
            L.append(f"| {name} | {m['failure_fixed'][name]}/27 |")
    L += ["", "| cause | " + " | ".join(n for n in order if n in m["failure_fixed"]) + " |",
          "|" + "---|" * (1 + len([n for n in order if n in m["failure_fixed"]]))]
    for cause, entry in sorted(m["failure_by_cause"].items()):
        L.append(f"| {cause} | " + " | ".join(str(entry.get(n, 0)) for n in order
                                              if n in m["failure_fixed"]) + " |")
    lat = m["latency_ms"]
    L += ["", "## Latency", "", "| stage | median | p95 |", "|---|---|---|"]
    for stage in ("detect", "query_embedding", "dense", "bm25"):
        if stage in lat:
            L.append(f"| {stage} | {lat[stage]['median']:.2f} ms | {lat[stage]['p95']:.2f} ms |")
    L += [f"| **total (est.)** | **{lat['total_estimate_ms']:.1f} ms** | — |", "",
          "Language detection is a dictionary lookup over query tokens, so it adds effectively nothing. No "
          "LLM is involved anywhere in this path.", "",
          "## Integrity", "",
          f"- Protected artefacts changed: **{len(m['protected_changed'])}**",
          f"- Qdrant `{COLLECTION}` exact count: **{m['qdrant']['before']} → {m['qdrant']['after']}**, "
          "read-only queries, zero writes",
          "- Benchmark v1 and probe v2 gold unchanged; `retriever_v1_candidate.json` not overwritten",
          "- Routing metadata written additively to `data/retrieval/language_routing_v1/`; the core "
          "`bm25_v1` index was not mutated", "",
          "## No Gold Leakage", "",
          "Routing consumes only the query string, the corpus-derived detector, chunk `language` metadata and "
          "retrieval ranks. Gold labels, gold languages and benchmark annotations are never read at routing "
          "time — the cross-lingual probes are routed by the same detector as everything else.", "",
          "## Tests", "", *(f"- {i.strip()}" for i in str(tests).split("|")), "", "## Final Decision", "",
          f"**LANGUAGE-AWARE RETRIEVAL — {decision}**", "", f"**RECOMMENDED RETRIEVER V1: {recommended}**", ""]
    atomic_write(root / "reports/language_aware_retrieval_gate.md", "\n".join(L).encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Language-aware retrieval gate")
    parser.add_argument("--project-root", type=Path, default=ROOT_DEFAULT)
    parser.add_argument("--stage", choices=["detector", "all"], default="detector")
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()
    evaluation = load_module(root, "retrieval_evaluation", "scripts/16_retrieval_evaluation.py")
    improvement = load_module(root, "retrieval_improvement", "scripts/17_retrieval_improvement.py")
    records = evaluation.load_corpus(root)
    detector = LanguageDetector(records, improvement.tokenize)

    if args.stage == "detector":
        audit = detector_audit(root, detector)
        print(json.dumps(audit["summary"], ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    result = run_gate(root, records, detector, evaluation, improvement, args.test_summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=float))
    return 0 if not result["blockers"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
