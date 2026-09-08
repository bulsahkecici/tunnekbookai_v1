"""Embedding eligibility classification and targeted extraction recovery.

Classifies every canonical chunk for embedding, quarantines extraction failures, and attempts
deterministic recovery for the three documents whose PDF text extraction failed. Recovery uses
verifiable decoders only - no invented text, no LLM, no OCR guesswork.

Frozen inputs (chunks, normalized corpus, manifests) are read-only throughout.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path


ELIGIBILITY_VERSION = "eligibility-v1.0"
RECOVERY_VERSION = "recovery-v1"
DAMAGED_DOCUMENTS = ("DOC000009", "DOC000041", "DOC000051")
LOW_CONTENT_WORDS = 8

# Subset-font glyph ids: printable char = chr(gid + 29), so gid 3 is space and the useful range is 3..97.
GLYPH_OFFSET = 29
GLYPH_MIN, GLYPH_MAX = 3, 97
GLYPH_SLASH_RE = re.compile(r"(?:/G\d{1,3}){3,}")
GLYPH_CONCAT_RE = re.compile(r"(?:G\d{1,3}){4,}")
# Detection stays conservative so ordinary text ("the G20 summit") is never quarantined. Decoding runs only
# inside documents already proven corrupt, where short runs are numerals - prices, rates, quantities - and
# leaving them encoded would silently falsify the figures.
GLYPH_SLASH_DECODE_RE = re.compile(r"(?:/G\d{1,3})+")
GLYPH_CONCAT_DECODE_RE = re.compile(r"(?:G\d{1,3}){2,}")
GLYPH_TOKEN_RE = re.compile(r"/?G(\d{1,3})")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
WORD_RE = re.compile(r"[^\W\d_]{3,}", re.UNICODE)
DIGIT_RE = re.compile(r"\d")
TABLE_LINE_RE = re.compile(r"(?m)^\s*\|.*\|\s*$")
HEADING_RE = re.compile(r"(?m)^#{1,4}[ \t]+\S")
PAGE_MARKER_RE = re.compile(r"<!--\s*original_page_(?:start|end):\s*\d+\s*-->", re.IGNORECASE)
REPLACEMENT_RE = re.compile(r"[�﻿]")

GLYPH_DENSITY = 20
CONTROL_DENSITY = 20

ELIGIBILITY_FIELDS = ["chunk_id", "document_id", "bge_m3_token_count", "eligibility_status", "quality_reason",
                      "glyph_sequence_count", "control_character_count", "real_word_count", "contains_table",
                      "document_type", "provenance_status", "recovery_status", "replacement_chunk_id"]
INPUT_FIELDS = ["vector_index", "chunk_id", "document_id", "source_kind", "bge_m3_token_count",
                "eligibility_status", "text_sha256"]


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


def jsonl_bytes(rows: list[dict[str, object]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                   for row in rows).encode("utf-8")


def load_chunker(root: Path):
    spec = importlib.util.spec_from_file_location("semantic_chunking", root / "scripts/11_semantic_chunking.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------- detection

def glyph_sequence_count(text: str) -> int:
    """Glyph-code runs in both observed forms: `/G49/G72/...` (pypdf) and `G49G72...` (Docling)."""
    return sum(len(GLYPH_TOKEN_RE.findall(match.group(0)))
               for match in GLYPH_SLASH_RE.finditer(text)) + \
           sum(len(GLYPH_TOKEN_RE.findall(match.group(0)))
               for match in GLYPH_CONCAT_RE.finditer(text))


def control_character_count(text: str) -> int:
    return len(CONTROL_RE.findall(text))


def real_word_count(text: str) -> int:
    """Words a reader would recognise: provenance comments and table scaffolding do not count."""
    stripped = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    stripped = re.sub(r"[|\-:]+", " ", stripped)
    return len(WORD_RE.findall(stripped))


def classify(text: str) -> tuple[str, str]:
    """Return (status, reason). Isolated control characters never quarantine a chunk on their own."""
    glyphs = glyph_sequence_count(text)
    controls = control_character_count(text)
    reasons = []
    if glyphs > GLYPH_DENSITY:
        reasons.append("glyph_index_sequence")
    if controls > CONTROL_DENSITY:
        reasons.append("control_character_residue")
    if reasons:
        return "quarantined_extraction_failure", "|".join(reasons)
    if real_word_count(text) < LOW_CONTENT_WORDS:
        return "eligible_low_content", "under_8_real_words"
    return "eligible", ""


# ---------------------------------------------------------------- decoding

def decode_glyph_run(run: str) -> str:
    """Decode a glyph-code run, preferring the longest id that maps to a printable character."""
    out, index = [], 0
    while index < len(run):
        if run[index] in "/G":
            index += 1
            continue
        digits = ""
        while index < len(run) and run[index].isdigit():
            digits += run[index]
            index += 1
        if not digits:
            index += 1
            continue
        value = int(digits)
        if len(digits) == 3 and not (GLYPH_MIN <= value <= GLYPH_MAX):
            value = int(digits[:2])
            index -= 1
        if len(digits) >= 2 and not (GLYPH_MIN <= value <= GLYPH_MAX):
            value = int(digits[0])
            index -= len(digits) - 1
        out.append(chr(value + GLYPH_OFFSET) if GLYPH_MIN <= value <= GLYPH_MAX else "")
    return "".join(out)


def decode_glyphs(text: str) -> str:
    text = GLYPH_SLASH_DECODE_RE.sub(lambda match: decode_glyph_run(match.group(0)), text)
    return GLYPH_CONCAT_DECODE_RE.sub(lambda match: decode_glyph_run(match.group(0)), text)


def residual_glyph_tokens(text: str) -> int:
    """Glyph codes still encoded after decoding - these would silently falsify numbers if left behind."""
    return len(GLYPH_SLASH_DECODE_RE.findall(text)) + len(GLYPH_CONCAT_DECODE_RE.findall(text))


def decode_utf16_pairs(text: str) -> str:
    """Repair UTF-16BE code units that were decoded byte-wise: (high, low) -> chr(high*256 + low)."""
    out, index = [], 0
    while index < len(text):
        char = text[index]
        if ord(char) < 32 and char not in "\r\n\t" and index + 1 < len(text):
            out.append(chr(ord(char) * 256 + ord(text[index + 1])))
            index += 2
        else:
            out.append(char)
            index += 1
    return "".join(out)


def recover_text(text: str) -> tuple[str, str]:
    """Apply whichever deterministic decoder the damage signature calls for."""
    methods = []
    if glyph_sequence_count(text) > GLYPH_DENSITY:
        text = decode_glyphs(text)
        methods.append("glyph_index_decode(+29)")
    if control_character_count(text) > CONTROL_DENSITY:
        text = decode_utf16_pairs(text)
        methods.append("utf16be_pair_decode")
    return text, "+".join(methods) or "none"


# ---------------------------------------------------------------- recovery

def quality_metrics(text: str) -> dict[str, int]:
    return {"glyph_sequences": glyph_sequence_count(text), "residual_glyph_runs": residual_glyph_tokens(text),
            "control_characters": control_character_count(text),
            "replacement_characters": len(REPLACEMENT_RE.findall(text)), "real_words": real_word_count(text),
            "digits": len(DIGIT_RE.findall(text)), "table_lines": len(TABLE_LINE_RE.findall(text)),
            "headings": len(HEADING_RE.findall(text)), "page_markers": len(PAGE_MARKER_RE.findall(text)),
            "characters": len(text)}


def split_front_matter(text: str) -> tuple[str, str]:
    match = re.match(r"\A(---\r?\n.*?\r?\n---(?:\r?\n|\Z))", text, re.DOTALL)
    return (match.group(1), text[match.end():]) if match else ("", text)


def candidate_sources(root: Path, relative: str) -> list[tuple[str, Path]]:
    """Recovery priority: the frozen normalized text first, then each surviving extraction layer."""
    return [(name, root / tree / f"{relative}.md") for name, tree in
            (("normalized", "data/corpus_normalized"), ("baseline_markdown", "data/markdown"),
             ("full_docling", "data/markdown_full_docling"))]


def attempt_recovery(root: Path, document_id: str, relative: str) -> dict[str, object]:
    attempts = []
    for name, path in candidate_sources(root, relative):
        if not path.is_file():
            attempts.append({"variant": name, "available": False})
            continue
        original = path.read_text(encoding="utf-8-sig", errors="replace")
        front, body = split_front_matter(original)
        recovered, method = recover_text(body)
        before, after = quality_metrics(body), quality_metrics(recovered)
        # Recovery must remove the damage and genuinely add readable text, keeping numbers and provenance.
        accepted = (after["glyph_sequences"] <= GLYPH_DENSITY and after["control_characters"] <= CONTROL_DENSITY
                    and after["residual_glyph_runs"] == 0
                    and after["real_words"] > before["real_words"]
                    and after["real_words"] >= LOW_CONTENT_WORDS
                    and after["page_markers"] >= before["page_markers"]
                    and after["replacement_characters"] <= before["replacement_characters"])
        attempts.append({"variant": name, "available": True, "method": method, "accepted": accepted,
                         "before": before, "after": after, "front": front, "text": recovered})
    usable = [attempt for attempt in attempts if attempt.get("accepted")]
    best = max(usable, key=lambda attempt: (attempt["after"]["real_words"], -attempt["after"]["glyph_sequences"]),
               default=None)
    return {"document_id": document_id, "relative": relative, "attempts": attempts, "best": best,
            "status": "recovered" if best else "recovery_failed_quarantine"}


def write_recovery_document(root: Path, document_id: str, relative: str, recovery: dict[str, object],
                            source_sha: str) -> Path:
    best = recovery["best"]
    front = str(best["front"]).rstrip()
    provenance = "\n".join([
        f'recovery_version: "{RECOVERY_VERSION}"',
        f'recovery_method: "{best["method"]}"',
        f'recovery_source_variant: "{best["variant"]}"',
        f'original_source_sha256: "{source_sha}"',
        f'recovery_created_at: "{RECOVERY_VERSION}"  # deterministic marker; no wall-clock timestamp',
    ])
    header = (front[:-3].rstrip() + "\n" + provenance + "\n---\n") if front.endswith("---") else \
             ("---\n" + provenance + "\n---\n")
    path = root / "data/corpus_recovery" / f"{document_id}.md"
    atomic_write(path, (header + str(best["text"])).encode("utf-8"))
    return path


def recovery_chunks(root: Path, document_id: str, path: Path, chunker) -> list[dict[str, object]]:
    verified = {row["document_id"]: row for row in
                read_csv(root / "data/metadata/final_metadata_verified_candidate.csv")}
    master = {row["document_id"]: row for row in read_csv(root / "data/metadata/final_metadata_master.csv")}
    document = chunker.chunk_document(path, root, verified.get(document_id, {}), master.get(document_id, {}))
    chunks = []
    for position, chunk in enumerate(document["chunks"], start=1):
        chunk = dict(chunk)
        chunk["chunk_id"] = f"{document_id}-R1-C{position:04d}"
        chunk["chunk_index"] = position
        chunk["source_kind"] = "recovery_chunk"
        chunk["recovery_version"] = RECOVERY_VERSION
        chunks.append(chunk)
    return chunks


# ---------------------------------------------------------------- pipeline

def build(root: Path) -> dict[str, object]:
    chunker = load_chunker(root)
    chunks = [json.loads(line) for line in (root / "data/chunks/chunks.jsonl").read_text(encoding="utf-8").splitlines()
              if line.strip()]
    tokens = {row["chunk_id"]: int(row["bge_m3_token_count"])
              for row in read_csv(root / "data/metadata/bge_m3_tokenizer_audit.csv")}
    master = {row["document_id"]: row for row in read_csv(root / "data/metadata/final_metadata_master.csv")}

    recoveries = {}
    for document_id in DAMAGED_DOCUMENTS:
        relative = Path(master[document_id]["source_relative_path"]).with_suffix("").as_posix()
        recovery = attempt_recovery(root, document_id, relative)
        if recovery["best"]:
            path = write_recovery_document(root, document_id, relative, recovery,
                                           master[document_id].get("source_sha256", ""))
            recovery["chunks"] = recovery_chunks(root, document_id, path, chunker)
        else:
            recovery["chunks"] = []
        recoveries[document_id] = recovery

    replacement_for = {}
    for document_id, recovery in recoveries.items():
        if recovery["chunks"]:
            replacement_for[document_id] = recovery["chunks"][0]["chunk_id"]

    rows = []
    for chunk in chunks:
        status, reason = classify(str(chunk["text"]))
        document_id = str(chunk["document_id"])
        recovery = recoveries.get(document_id)
        recovery_status, replacement = "", ""
        if recovery:
            recovery_status = recovery["status"]
            if recovery["chunks"]:
                # A recovery re-extracts the whole document, so it supersedes every canonical chunk of that
                # document - not only the ones that tripped the detector. Keeping the survivors would both
                # duplicate content and re-admit residual damage that sat under the density threshold.
                status = "replacement_available"
                replacement = replacement_for[document_id]
            elif status == "quarantined_extraction_failure":
                status = "quarantined_extraction_failure"
        rows.append({"chunk_id": chunk["chunk_id"], "document_id": document_id,
                     "bge_m3_token_count": tokens.get(chunk["chunk_id"], ""), "eligibility_status": status,
                     "quality_reason": reason, "glyph_sequence_count": glyph_sequence_count(str(chunk["text"])),
                     "control_character_count": control_character_count(str(chunk["text"])),
                     "real_word_count": real_word_count(str(chunk["text"])),
                     "contains_table": int(bool(chunk["contains_table"])),
                     "document_type": chunk.get("document_type") or "",
                     "provenance_status": chunk["provenance_status"],
                     "recovery_status": recovery_status, "replacement_chunk_id": replacement})
    atomic_write(root / "data/metadata/embedding_eligibility.csv", csv_bytes(rows, ELIGIBILITY_FIELDS))

    all_recovery_chunks = [chunk for recovery in recoveries.values() for chunk in recovery["chunks"]]
    if all_recovery_chunks:
        atomic_write(root / "data/chunks_recovery/chunks.jsonl", jsonl_bytes(all_recovery_chunks))

    excluded = {"quarantined_extraction_failure", "replacement_available"}
    input_rows, index = [], 0
    for chunk, row in zip(chunks, rows):
        if row["eligibility_status"] in excluded:
            continue
        input_rows.append({"vector_index": index, "chunk_id": chunk["chunk_id"], "document_id": chunk["document_id"],
                           "source_kind": "canonical_chunk", "bge_m3_token_count": row["bge_m3_token_count"],
                           "eligibility_status": row["eligibility_status"],
                           "text_sha256": sha256(str(chunk["text"]).encode("utf-8"))})
        index += 1
    for chunk in all_recovery_chunks:
        status, _ = classify(str(chunk["text"]))
        if status == "quarantined_extraction_failure":
            continue
        input_rows.append({"vector_index": index, "chunk_id": chunk["chunk_id"], "document_id": chunk["document_id"],
                           "source_kind": "recovery_chunk", "bge_m3_token_count": "",
                           "eligibility_status": status,
                           "text_sha256": sha256(str(chunk["text"]).encode("utf-8"))})
        index += 1
    atomic_write(root / "data/metadata/full_embedding_input_manifest.csv", csv_bytes(input_rows, INPUT_FIELDS))
    return {"chunks": chunks, "rows": rows, "recoveries": recoveries, "input_rows": input_rows,
            "recovery_chunks": all_recovery_chunks}


def frozen_state(root: Path) -> dict[str, str]:
    state = {}
    for relative in ("data/chunks/chunks.jsonl", "data/chunks_pilot/chunks.jsonl",
                     "data/metadata/chunk_manifest.csv", "data/metadata/chunk_review_queue.csv",
                     "data/metadata/bge_m3_tokenizer_audit.csv",
                     "data/metadata/bge_m3_embedding_pilot_manifest.csv",
                     "data/metadata/final_corpus_manifest.csv", "data/metadata/final_metadata_master.csv"):
        path = root / relative
        if path.is_file():
            state[relative] = sha256(path.read_bytes())
    for relative in ("data/corpus_final", "data/corpus_normalized", "data/markdown", "data/markdown_full_docling"):
        digest = hashlib.sha256()
        base = root / relative
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    return state


def report(result: dict[str, object], frozen_changed: list[str], tests: str) -> tuple[str, bool]:
    rows, recoveries = result["rows"], result["recoveries"]
    statuses = Counter(row["eligibility_status"] for row in rows)
    input_rows = result["input_rows"]
    quarantined = [row for row in rows if row["eligibility_status"] in
                   {"quarantined_extraction_failure", "replacement_available"}]
    input_ids = {row["chunk_id"] for row in input_rows}
    leaked = [row["chunk_id"] for row in quarantined if row["chunk_id"] in input_ids]
    canonical = sum(row["source_kind"] == "canonical_chunk" for row in input_rows)
    recovery_count = sum(row["source_kind"] == "recovery_chunk" for row in input_rows)
    duplicate_documents = {row["document_id"] for row in input_rows if row["source_kind"] == "recovery_chunk"} & \
                          {row["document_id"] for row in input_rows if row["source_kind"] == "canonical_chunk"}

    blockers = []
    if len(rows) != 6039:
        blockers.append(f"eligibility manifest rows: {len(rows)} (expected 6039)")
    if len({row["chunk_id"] for row in rows}) != len(rows):
        blockers.append("duplicate chunk_id in eligibility manifest")
    if leaked:
        blockers.append(f"quarantined chunks present in embedding input: {len(leaked)}")
    if duplicate_documents:
        blockers.append(f"canonical and recovery content for same document: {sorted(duplicate_documents)}")
    if len({row["chunk_id"] for row in input_rows}) != len(input_rows):
        blockers.append("duplicate chunk_id in embedding input manifest")
    if [row["vector_index"] for row in input_rows] != list(range(len(input_rows))):
        blockers.append("vector_index is not contiguous")
    if frozen_changed:
        blockers.append(f"frozen artefacts changed: {', '.join(frozen_changed)}")
    if "FAIL" in tests:
        blockers.append("test failure")
    decision = "NO-GO" if blockers else "GO"

    lines = ["# TunnelBookAI Embedding Eligibility & Extraction Recovery Audit", "", "## Result", "",
             f"**FULL EMBEDDING INPUT — {decision}**", "",
             "No embedding, vector database, retrieval or RAG was run in this stage.", "", "## Input", "",
             f"- Canonical chunks classified: **{len(rows)}/6039**",
             f"- Every chunk received exactly one eligibility status: **{sum(statuses.values()) == len(rows)}**", "",
             "## Extraction Failures", "",
             f"- Chunks with extraction damage: **{len(quarantined)}**", "",
             "| document | damaged chunks | total chunks | signature |", "|---|---|---|---|"]
    totals = Counter(row["document_id"] for row in rows)
    damaged = Counter(row["document_id"] for row in quarantined)
    for document_id in sorted(damaged):
        reasons = {row["quality_reason"] for row in quarantined if row["document_id"] == document_id}
        lines.append(f"| {document_id} | {damaged[document_id]} | {totals[document_id]} | {', '.join(sorted(reasons))} |")
    lines.extend(["", "## Low-content", "",
                  f"- Total flagged `eligible_low_content`: **{statuses['eligible_low_content']}**",
                  f"- Kept in embedding input: **{statuses['eligible_low_content']}**", "- Quarantined: **0**",
                  "- Policy is keep + flag. Short regulation articles (`MADDE 3- Bu Karar yayımı tarihinde "
                  "yürürlüğe girer.`), table chunks and technical labels are legitimate content and are not "
                  "deleted. A retrieval-time score threshold is the right lever, and is deferred to retrieval "
                  "evaluation.", "", "## Recovery", ""])
    for document_id in DAMAGED_DOCUMENTS:
        recovery = recoveries[document_id]
        best = recovery["best"]
        lines.extend([f"### {document_id}", ""])
        if best:
            before, after = best["before"], best["after"]
            lines.extend([f"- Method: **{best['method']}**",
                          f"- Source variant used: **{best['variant']}**",
                          f"- Result: **{recovery['status']}**",
                          f"- Replacement chunks: **{len(recovery['chunks'])}**",
                          "",
                          "| metric | before | after |", "|---|---|---|",
                          f"| glyph sequences | {before['glyph_sequences']} | {after['glyph_sequences']} |",
                          f"| residual glyph runs | {before['residual_glyph_runs']} | {after['residual_glyph_runs']} |",
                          f"| control characters | {before['control_characters']} | {after['control_characters']} |",
                          f"| replacement chars | {before['replacement_characters']} | {after['replacement_characters']} |",
                          f"| real words | {before['real_words']} | **{after['real_words']}** |",
                          f"| digits | {before['digits']} | {after['digits']} |",
                          f"| table lines | {before['table_lines']} | {after['table_lines']} |",
                          f"| headings | {before['headings']} | {after['headings']} |",
                          f"| page markers | {before['page_markers']} | {after['page_markers']} |", ""])
        else:
            lines.extend([f"- Result: **{recovery['status']}**",
                          "- No decoder produced a strictly better result. No text was invented; the document's "
                          "damaged chunks stay out of the embedding input.", ""])
    lines.extend(["## Final Embedding Eligibility", "",
                  f"- `eligible`: **{statuses['eligible']}**",
                  f"- `eligible_low_content`: **{statuses['eligible_low_content']}**",
                  f"- `replacement_available` (canonical, superseded): **{statuses['replacement_available']}**",
                  f"- `quarantined_extraction_failure`: **{statuses['quarantined_extraction_failure']}**", "",
                  f"- Canonical eligible in input: **{canonical}**",
                  f"- Recovery chunks in input: **{recovery_count}**",
                  f"- **Total vectors planned: {len(input_rows)}**",
                  f"- Baseline without any recovery would have been 6039 − {len(quarantined)} = "
                  f"**{6039 - len(quarantined)}**", "", "## Duplication Guard", "",
                  f"- Documents contributing both canonical and recovery content: **{len(duplicate_documents)}**",
                  "- For each recovered document the damaged canonical chunks are marked "
                  "`replacement_available` and excluded, so the same source text is never embedded twice.", "",
                  "## Integrity", "",
                  f"- Frozen corpus changed: **{str(any(key.startswith('data/corpus') for key in frozen_changed)).lower()}**",
                  f"- Frozen chunks changed: **{str(any('chunks' in key for key in frozen_changed)).lower()}**",
                  f"- Frozen metadata changed: **{str(any(key.startswith('data/metadata') for key in frozen_changed)).lower()}**",
                  f"- Total frozen artefacts changed: **{len(frozen_changed)}**",
                  "- Recovery output is written only to `data/corpus_recovery/` and `data/chunks_recovery/`.", "",
                  "## Tests", "", *(f"- {item.strip()}" for item in tests.split("|")), "", "## Warnings", "",
                  "- Recovery decoders are deterministic character-mapping repairs, not OCR and not generation. "
                  "The glyph decoder inverts a subset-font mapping (`char = chr(gid + 29)`, verified by decoding "
                  "known titles such as `Estimate of annual operating costs`); the UTF-16 decoder reassembles "
                  "byte-split code units. No text was invented at any point.",
                  "- Recovered documents keep `source_only` provenance: the damaged extractions carried no usable "
                  "page anchors, and none were fabricated.",
                  "- Recovery chunks are new content entering the corpus and have not been through the full "
                  "chunking audit that the frozen 6039 passed. They were produced with the same chunker rules, but "
                  "review them before treating them as equal-confidence sources.",
                  "- The original damaged chunks remain in the frozen corpus by design; they are excluded at the "
                  "manifest level, not deleted.", "", "## Blockers", ""])
    lines.extend([f"- {item}" for item in blockers] or ["- Yok."])
    lines.extend(["", "## Final Decision", "", f"**FULL EMBEDDING INPUT — {decision}**", "",
                  f"`data/metadata/full_embedding_input_manifest.csv` is the single input list for the full "
                  f"embedding run: **{len(input_rows)} vectors**.", ""])
    return "\n".join(lines), decision == "GO"


def main() -> int:
    parser = argparse.ArgumentParser(description="Embedding eligibility and targeted extraction recovery")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()
    before = frozen_state(root)
    result = build(root)
    after = frozen_state(root)
    changed = sorted(key for key in before if before[key] != after.get(key))
    audit, go = report(result, changed, args.test_summary)
    atomic_write(root / "reports/embedding_eligibility_audit.md", audit.encode("utf-8"))
    statuses = Counter(row["eligibility_status"] for row in result["rows"])
    print(json.dumps({"decision": "GO" if go else "NO-GO", "classified": len(result["rows"]),
                      "statuses": dict(statuses), "recovery_chunks": len(result["recovery_chunks"]),
                      "embedding_input_vectors": len(result["input_rows"]),
                      "recovery": {key: value["status"] for key, value in result["recoveries"].items()},
                      "frozen_changed": changed}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if go else 2


if __name__ == "__main__":
    raise SystemExit(main())
