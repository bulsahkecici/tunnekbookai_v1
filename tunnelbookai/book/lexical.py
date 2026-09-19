"""Manifest-bound BM25 lexical index over the same canonical rows as the dense index.

The dense BGE-M3 index alone pulled short figure captions and table-of-contents chunks to
the top of nearly every evidence query (47% of the canonical index is FIGURE_CHUNK rows with
a median length of ~240 characters).  This module adds the second retrieval signal for the
hybrid retriever: a deterministic, rebuildable BM25 index bound to the exact dense index id,
plus per-row noise metadata (character count, table-of-contents likeness, broken Turkish
letter spacing) that the retrieval policy uses to filter and weight candidates.

Tokenisation folds Turkish (ı/İ before NFKD, see ``tunnelbookai.ingest.textfold``), strips
combining marks, casefolds and truncates every alphabetic token to its first five characters
(the "F5" prefix rule, which behaves close to a lemmatiser for agglutinative Turkish and is
harmless for the English half of the corpus).
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
from scipy import sparse

from tunnelbookai.canonical.hashing import canonical_sha256, sha256_file
from tunnelbookai.ingest.textfold import fold_turkish

from .errors import BookEngineError


SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "book-lexical-v1"
TOKENIZER_VERSION = "turkish-fold-nfkd-f5-v1"
BM25_K1 = 1.5
BM25_B = 0.75
PREFIX_LENGTH = 5
MIN_TOKEN_LENGTH = 2

# Question words, connectives and copulas that carry no evidence signal.  Folded form.
STOPWORDS = frozenset("""
ve veya ile icin gibi kadar gore uzere olan olarak olup ise ama fakat ancak ya da de
bir bu su o bunlar sunlar onlar bunun sunun onun bunu sunu onu buna suna ona bunda
ne neden nasil nedir nelerdir hangi hangisi kac mi mu mi mu midir mudur
var yok her hem cok daha en pek az tum butun bazi diger ayni
the a an of in on at to for from by with and or is are was were be been being as that
this these those it its into than then which who whom whose what when where why how
""".split())

_COMBINING = re.compile("[\\u0300-\\u036f]")
_TOKEN = re.compile(r"[a-z0-9]+")
_BROKEN_LEFT = re.compile(r"(?<=\w) ([ışğüöçİŞĞÜÖÇ])(?= |$)")
_BROKEN_BOTH = re.compile(r"(?<=\w) ([ışğüöçİŞĞÜÖÇ]) (?=\w)")
_BROKEN_PROBE = re.compile(r"\w+ [ışğüöçİŞĞÜÖÇ] \w+")
_DOTTED_LEADER = re.compile(r"\.{6,}")
_TOC_LINE = re.compile(r"^\s*(\d+(\.\d+)*\.?|[IVXLC]+\.)\s+\S.*\s\d{1,4}\s*$")


def repair_broken_spacing(text: str, *, join_right: bool = True) -> str:
    """Rejoin ``k ı salmas ı`` style extraction damage.

    A lone Turkish special letter is never a standalone word, so joining it to the word on
    its left is always safe.  Whether it also belongs to the word on its right is ambiguous
    (``k ı salmas ı ve``: the first ``ı`` is mid-word, the second is word-final), so callers
    choose: ``join_right=True`` recovers mid-word damage, ``False`` keeps word boundaries.
    Applied iteratively because damage frequently occurs twice in one word.
    """

    pattern = _BROKEN_BOTH if join_right else _BROKEN_LEFT
    previous = None
    current = text
    while previous != current:
        previous = current
        current = pattern.sub(r"\1", current)
    return current


def _basic_tokens(text: str) -> list[str]:
    folded = fold_turkish(text)
    decomposed = unicodedata.normalize("NFKD", folded)
    ascii_text = _COMBINING.sub("", decomposed).casefold()
    tokens: list[str] = []
    for token in _TOKEN.findall(ascii_text):
        if len(token) < MIN_TOKEN_LENGTH or token in STOPWORDS:
            continue
        if not token.isdigit():
            token = token[:PREFIX_LENGTH]
        tokens.append(token)
    return tokens


def tokenize(text: str) -> list[str]:
    """Fold, strip marks, casefold, F5-truncate; repair broken letter spacing both ways.

    For damaged chunks the mid-word repair (join both sides) is the primary token stream and
    the word-boundary repair (join left only) contributes any tokens it alone produces, so
    ``salması`` survives even when ``kısalması ve`` was mis-joined as one word.
    """

    if len(_BROKEN_PROBE.findall(text)) >= 3:
        primary = _basic_tokens(repair_broken_spacing(text, join_right=True))
        seen = set(primary)
        extra = [token for token in _basic_tokens(repair_broken_spacing(text, join_right=False)) if token not in seen]
        return primary + extra
    return _basic_tokens(repair_broken_spacing(text, join_right=True))


def noise_flags(text: str) -> dict[str, Any]:
    """Deterministic per-chunk noise markers consumed by the retrieval policy."""

    lines = [line for line in text.splitlines() if line.strip()]
    toc_lines = sum(1 for line in lines if _TOC_LINE.match(line))
    leaders = len(_DOTTED_LEADER.findall(text))
    toc_like = leaders >= 3 or (len(lines) >= 4 and toc_lines * 2 >= len(lines))
    return {
        "chars": len(text),
        "toc_like": bool(toc_like),
        "broken_spacing": len(_BROKEN_PROBE.findall(text)) >= 3,
    }


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _atomic_bytes(path: Path, writer: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        writer(handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def lexical_root(project_root: Path, index_id: str) -> Path:
    return project_root / "book" / "retrieval" / "lexical" / index_id


def build_lexical_index(
    project_root: Path,
    *,
    index_id: str,
    rows: Sequence[Mapping[str, Any]],
    texts: Iterable[str],
) -> dict[str, Any]:
    """Build BM25 weights for ``rows`` (dense index order) and publish an atomic manifest."""

    root = Path(project_root).resolve()
    target = lexical_root(root, index_id)
    vocabulary: dict[str, int] = {}
    indptr = [0]
    indices: list[int] = []
    counts: list[float] = []
    lengths: list[int] = []
    flags: list[dict[str, Any]] = []
    chunk_ids: list[str] = []
    for row, text in zip(rows, texts, strict=True):
        tokens = tokenize(text)
        lengths.append(len(tokens))
        flags.append(noise_flags(text))
        chunk_ids.append(str(row["chunk_id"]))
        frequencies: dict[int, int] = {}
        for token in tokens:
            term_id = vocabulary.setdefault(token, len(vocabulary))
            frequencies[term_id] = frequencies.get(term_id, 0) + 1
        for term_id in sorted(frequencies):
            indices.append(term_id)
            counts.append(float(frequencies[term_id]))
        indptr.append(len(indices))
    if not chunk_ids:
        raise BookEngineError("RETRIEVAL_INDEX_INVALID", "lexical index has no rows")
    document_count = len(chunk_ids)
    term_frequency = sparse.csr_matrix(
        (np.asarray(counts, dtype=np.float32), np.asarray(indices, dtype=np.int32), np.asarray(indptr, dtype=np.int64)),
        shape=(document_count, len(vocabulary)),
    )
    document_frequency = np.diff(term_frequency.tocsc().indptr).astype(np.float64)
    idf = np.log(1.0 + (document_count - document_frequency + 0.5) / (document_frequency + 0.5))
    length_array = np.asarray(lengths, dtype=np.float64)
    average_length = float(length_array.mean()) if length_array.size else 0.0
    weighted = term_frequency.tocoo()
    normaliser = BM25_K1 * (1.0 - BM25_B + BM25_B * length_array[weighted.row] / max(average_length, 1e-9))
    data = weighted.data.astype(np.float64) * (BM25_K1 + 1.0) / (weighted.data + normaliser) * idf[weighted.col]
    matrix = sparse.csr_matrix((data.astype(np.float32), (weighted.row, weighted.col)), shape=term_frequency.shape)
    matrix.sort_indices()

    target.mkdir(parents=True, exist_ok=True)
    matrix_path = target / "bm25_matrix.npz"
    _atomic_bytes(matrix_path, lambda handle: sparse.save_npz(handle, matrix, compressed=True))
    vocabulary_path = target / "vocabulary.json"
    _atomic_json(vocabulary_path, {"terms": sorted(vocabulary, key=vocabulary.__getitem__)})
    rows_path = target / "row_metadata.jsonl"
    temporary = rows_path.with_name(rows_path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for chunk_id, length, flag in zip(chunk_ids, lengths, flags):
            handle.write(json.dumps({"chunk_id": chunk_id, "tokens": length, **flag}, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, rows_path)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "contract_version": CONTRACT_VERSION,
        "tokenizer_version": TOKENIZER_VERSION,
        "dense_index_id": index_id,
        "bm25_k1": BM25_K1,
        "bm25_b": BM25_B,
        "row_count": document_count,
        "vocabulary_size": len(vocabulary),
        "average_tokens": round(average_length, 6),
        "rows_sha256": canonical_sha256(chunk_ids),
        "files": {
            "bm25_matrix.npz": sha256_file(matrix_path),
            "vocabulary.json": sha256_file(vocabulary_path),
            "row_metadata.jsonl": sha256_file(rows_path),
        },
    }
    manifest["lexical_index_id"] = "BLI_" + canonical_sha256(manifest)
    _atomic_json(target / "manifest.json", manifest)
    return manifest


@dataclass(frozen=True)
class LexicalIndex:
    manifest: Mapping[str, Any]
    matrix: sparse.csr_matrix
    vocabulary: Mapping[str, int]
    metadata: tuple[Mapping[str, Any], ...]

    @classmethod
    def load(cls, project_root: Path, *, index_id: str, expected_chunk_ids: Sequence[str]) -> "LexicalIndex":
        root = Path(project_root).resolve()
        target = lexical_root(root, index_id)
        manifest_path = target / "manifest.json"
        if not manifest_path.is_file():
            raise BookEngineError("LEXICAL_INDEX_MISSING", f"lexical index is missing for {index_id}; run build-index")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("contract_version") != CONTRACT_VERSION or manifest.get("dense_index_id") != index_id:
            raise BookEngineError("LEXICAL_INDEX_STALE", "lexical index is bound to a different dense index")
        if manifest.get("tokenizer_version") != TOKENIZER_VERSION:
            raise BookEngineError("LEXICAL_INDEX_STALE", "lexical tokenizer version changed; rebuild the index")
        for name, digest in (manifest.get("files") or {}).items():
            if sha256_file(target / name) != digest:
                raise BookEngineError("LEXICAL_INDEX_INVALID", f"lexical index file changed: {name}")
        matrix = sparse.load_npz(target / "bm25_matrix.npz").tocsr()
        terms = json.loads((target / "vocabulary.json").read_text(encoding="utf-8"))["terms"]
        metadata = tuple(
            json.loads(line)
            for line in (target / "row_metadata.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        chunk_ids = [str(row["chunk_id"]) for row in metadata]
        if chunk_ids != [str(value) for value in expected_chunk_ids] or matrix.shape[0] != len(chunk_ids):
            raise BookEngineError("LEXICAL_INDEX_STALE", "lexical rows do not match the dense index rows")
        if matrix.shape[1] != len(terms):
            raise BookEngineError("LEXICAL_INDEX_INVALID", "lexical vocabulary does not match the matrix")
        return cls(manifest, matrix, {term: position for position, term in enumerate(terms)}, metadata)

    def score(self, query: str) -> np.ndarray:
        """BM25 scores for every row; zeros when no query term is in the vocabulary."""

        term_ids = [self.vocabulary[token] for token in tokenize(query) if token in self.vocabulary]
        if not term_ids:
            return np.zeros(self.matrix.shape[0], dtype=np.float32)
        weights = np.zeros(self.matrix.shape[1], dtype=np.float32)
        for term_id in term_ids:
            weights[term_id] += 1.0
        return np.asarray(self.matrix @ weights, dtype=np.float32).ravel()


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?:;])\s+|\n{2,}")


def focused_window(text: str, query: str, *, chars: int) -> str:
    """Return the ~``chars``-long sentence window of ``text`` that best covers ``query``.

    Canonical chunks routinely begin with the tail of the previous section (structure-aware
    overlap), so a fixed prefix often misses the passage that made the chunk rank.  Windows
    are scored by the number of distinct query tokens they contain, then by token density;
    ties keep the earliest window so the result is deterministic.
    """

    normalised = " ".join(text.split())
    if len(normalised) <= chars:
        return normalised
    wanted = set(tokenize(query))
    sentences = [piece for piece in _SENTENCE_SPLIT.split(normalised) if piece and piece.strip()]
    if not wanted or len(sentences) <= 1:
        return normalised[:chars]
    sentence_tokens = [set(tokenize(piece)) for piece in sentences]
    best_score: tuple[int, float] = (-1, 0.0)
    best_text = normalised[:chars]
    for start in range(len(sentences)):
        length = 0
        covered: set[str] = set()
        end = start
        while end < len(sentences) and length + len(sentences[end]) + 1 <= chars:
            covered |= sentence_tokens[end] & wanted
            length += len(sentences[end]) + 1
            end += 1
        if end == start:
            # A single sentence longer than the window: score it truncated.
            covered = sentence_tokens[start] & wanted
            candidate = sentences[start][:chars]
        else:
            candidate = " ".join(sentences[start:end])
        score = (len(covered), len(covered) / max(len(candidate), 1))
        if score > best_score:
            best_score, best_text = score, candidate
        if end >= len(sentences):
            break
    return best_text


def token_jaccard(left: str, right: str) -> float:
    a, b = set(tokenize(left)), set(tokenize(right))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


__all__ = [
    "LexicalIndex",
    "focused_window",
    "token_jaccard",
    "build_lexical_index",
    "lexical_root",
    "noise_flags",
    "repair_broken_spacing",
    "tokenize",
]
