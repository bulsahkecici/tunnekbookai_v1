"""Complete claim-level grounding audit for the output-contract-integrated re-evaluation.

Deterministic first pass, manual residual second. No LLM judges any claim. The deterministic rules
only ever CONFIRM support against literal packet evidence; they never invent it, and anything they
cannot justify is left unresolved for hand review rather than being labelled optimistically.

Phase B v2 labels are not trusted blindly. A prior manual label is reusable only when the new raw
answer is byte-identical to the Phase B v2 answer AND the claim text matches exactly - i.e. the
audited object is literally the same string. Every such carry is recorded with its provenance.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/evaluation/generation_output_contract_eval_raw_v1.jsonl"
PACKETS = ROOT / "data/evaluation/generation_eval_benchmark_v2_packets.jsonl"
PHASE_B_RESULTS = ROOT / "data/evaluation/generation_eval_results_v2.jsonl"
PHASE_B_CLAIMS = ROOT / "data/evaluation/generation_claim_audit_v2.jsonl"
OUT = ROOT / "data/evaluation/generation_output_contract_claim_audit_v1.jsonl"
OVERRIDES = ROOT / "data/evaluation/generation_output_contract_claim_manual_v1.json"

HANDLE = re.compile(r"\[E(\d{3})\]")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
MARKER = re.compile(r"^\s*(YETERSİZ\s+KANIT|INSUFFICIENT\s+EVIDENCE)", re.I)
STOPWORDS = {
    "ve", "ile", "bir", "bu", "için", "gibi", "olarak", "olan", "ise", "veya", "göre", "kadar",
    "her", "tüm", "değil", "üzere", "the", "and", "of", "to", "in", "for", "on", "with", "is",
    "are", "be", "as", "by", "from", "that", "this", "which", "such", "shall", "must", "should",
    "not", "than", "when", "where", "while", "their", "they", "it", "its", "at", "or", "can",
}


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = HANDLE.sub(" ", text)
    return re.sub(r"[^\w\s]", " ", text)


def content_tokens(text: str) -> list[str]:
    return [t for t in normalise(text).split() if len(t) > 2 and t not in STOPWORDS]


def ngrams(tokens: list[str], n: int = 4) -> set[tuple]:
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)} if len(tokens) >= n else set()


def numbers_in(text: str) -> list[str]:
    """Numeric tokens, comma/period normalised so 0,60 and 0.60 compare equal."""
    return [n.replace(",", ".").rstrip("0").rstrip(".") if "." in n.replace(",", ".") else n
            for n in NUMBER.findall(HANDLE.sub(" ", text))]


def segment(answer: str) -> list[str]:
    """Split into claim units: list items and sentences within paragraphs."""
    text = re.sub(r"\r", "", answer)
    blocks = [b.strip() for b in re.split(r"\n(?=\s*(?:[-*•]|\d{1,2}[.)]))|\n{2,}", text) if b.strip()]
    claims: list[str] = []
    for block in blocks:
        block = re.sub(r"\s+", " ", block).strip()
        if not block:
            continue
        if re.match(r"^\s*(?:[-*•]|\d{1,2}[.)])", block) or len(block) < 160:
            claims.append(block)
            continue
        # Sentence split only for long prose paragraphs; abbreviations keep their period.
        parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])", block)
        claims.extend(p.strip() for p in parts if p.strip())
    return [c for c in claims if c]


def is_material(claim: str) -> bool:
    """Headings, lead-ins and bare markers assert nothing."""
    stripped = claim.strip()
    if MARKER.match(stripped) and len(stripped.split()) < 8:
        return False
    if re.search(r":\s*$", stripped) and not HANDLE.search(stripped):
        return False
    body = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", stripped)
    body = re.sub(r"^\*\*.*?\*\*\s*:?\s*$", "", body).strip()
    if not body:
        return False
    return len(content_tokens(body)) >= 4 or bool(NUMBER.search(body))


def supports(claim: str, evidence_text: str) -> tuple[bool, list[str]]:
    """Literal support: shared 4-grams plus containment of every numeric value in the claim."""
    claim_tokens, ev_tokens = content_tokens(claim), content_tokens(evidence_text)
    shared = ngrams(claim_tokens) & ngrams(ev_tokens)
    ev_numbers = set(numbers_in(evidence_text))
    claim_numbers = [n for n in numbers_in(claim) if len(n) > 1 or int(float(n)) > 3]
    numbers_ok = all(n in ev_numbers for n in claim_numbers)
    if not numbers_ok:
        return False, []
    if shared:
        spans = [" ".join(g) for g in sorted(shared)[:3]]
        return True, spans
    # Short claims cannot form 4-grams; fall back to strict unigram containment.
    if 0 < len(claim_tokens) < 4:
        ev_set = set(ev_tokens)
        if all(t in ev_set for t in claim_tokens):
            return True, [" ".join(claim_tokens)]
    # High-precision lexical overlap for claims whose wording is reordered.
    if claim_tokens:
        ev_set = set(ev_tokens)
        overlap = sum(1 for t in claim_tokens if t in ev_set) / len(claim_tokens)
        if overlap >= 0.85 and claim_numbers:
            return True, [t for t in claim_tokens if t in ev_set][:3]
    return False, []


def build() -> dict:
    raw = {r["query_id"]: r for r in
           (json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip())}
    packets = {p["packet_sha"]: p for p in
               (json.loads(l) for l in PACKETS.read_text(encoding="utf-8").splitlines() if l.strip())}
    contract = {r["query_id"]: r for r in
                (json.loads(l) for l in (ROOT / "data/evaluation/"
                 "generation_output_contract_eval_results_v1.jsonl")
                 .read_text(encoding="utf-8").splitlines() if l.strip())}

    # Prior manual labels, keyed by the exact answer bytes they were made against.
    import hashlib
    prior_sha = {}
    if PHASE_B_RESULTS.exists():
        for line in PHASE_B_RESULTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                prior_sha[row["query_id"]] = hashlib.sha256(
                    row["raw_answer"].encode("utf-8")).hexdigest()
    prior_claims: dict[tuple, dict] = {}
    if PHASE_B_CLAIMS.exists():
        for line in PHASE_B_CLAIMS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                prior_claims[(row["query_id"], row["claim_text"].strip())] = row

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}

    rows, unresolved = [], []
    for query_id in sorted(raw):
        answer_row = raw[query_id]
        packet = packets[answer_row["context_packet_sha"]]
        evidence = {e["evidence_id"]: e["text"] for e in packet["evidence"]}
        whole_packet = "\n".join(evidence.values())
        identical = prior_sha.get(query_id) == answer_row["raw_answer_sha"]

        for index, claim in enumerate(segment(answer_row["raw_answer"]), start=1):
            claim_id = f"K{index}"
            cited = [f"E{m}" for m in HANDLE.findall(claim)]
            material = is_material(claim)
            row = {
                "query_id": query_id, "claim_id": claim_id, "claim_text": claim,
                "material": material, "citation_bearing": bool(cited),
                "numeric_claim": bool(numbers_in(claim)),
                "cited_evidence_ids": cited, "supporting_evidence_ids": [],
                "supporting_literal_spans": [], "partial_reason": None,
                "unsupported_reason": None, "claim_label": None, "label_method": None,
                "contract_valid_for_answer": contract[query_id]["contract_valid"],
                "answer_byte_identical_to_phase_b_v2": identical, "resolved": False,
            }

            if not material:
                row.update(claim_label="NON_FACTUAL", label_method="deterministic_verified",
                           resolved=True)
                rows.append(row)
                continue

            supporting, spans = [], []
            for evidence_id in cited:
                if evidence_id in evidence:
                    ok, matched = supports(claim, evidence[evidence_id])
                    if ok:
                        supporting.append(evidence_id)
                        spans.extend(matched)
            if not cited:
                ok, matched = supports(claim, whole_packet)
                if ok:
                    supporting, spans = ["<packet>"], matched
            row["supporting_evidence_ids"] = supporting
            row["supporting_literal_spans"] = spans[:3]

            key = (query_id, claim.strip())
            manual_key = f"{query_id}||{claim_id}"
            if supporting:
                row.update(claim_label="SUPPORTED", label_method="deterministic_verified",
                           resolved=True)
            elif manual_key in overrides:
                # Hand-adjudicated in this phase; the override file carries the written reason.
                row.update(overrides[manual_key])
                row["resolved"] = True
                row["label_method"] = "manual_evidence_verified"
            if not row["resolved"]:
                if identical and key in prior_claims:
                    prior = prior_claims[key]
                    row.update(claim_label=prior["claim_label"],
                               label_method="manual_evidence_verified_carried_identical_answer",
                               partial_reason=prior.get("partial_reason"),
                               unsupported_reason=prior.get("unsupported_reason"),
                               supporting_evidence_ids=prior.get("supporting_evidence_ids") or [],
                               supporting_literal_spans=prior.get("supporting_literal_spans") or [],
                               resolved=True)
                    row["carried_from"] = "generation_claim_audit_v2.jsonl"
                else:
                    unresolved.append(row)
            rows.append(row)

    # The adjudicated label is authoritative for materiality: a claim decided NON_FACTUAL asserts
    # nothing, whatever the segmentation heuristic guessed. This keeps every downstream denominator
    # consistent with the labels actually assigned.
    for row in rows:
        if row["claim_label"] == "NON_FACTUAL":
            row["material"] = False

    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return {"rows": rows, "unresolved": unresolved}


if __name__ == "__main__":
    result = build()
    rows, unresolved = result["rows"], result["unresolved"]
    material = [r for r in rows if r["material"]]
    import collections
    print(f"claims={len(rows)} material={len(material)} nonfactual={len(rows)-len(material)}")
    print(collections.Counter(r["claim_label"] for r in rows))
    print(collections.Counter(r["label_method"] for r in rows))
    print(f"UNRESOLVED requiring manual review: {len(unresolved)}")
    for r in unresolved:
        print(f"  {r['query_id']} {r['claim_id']} cited={r['cited_evidence_ids']} "
              f"{r['claim_text'][:100]}")
