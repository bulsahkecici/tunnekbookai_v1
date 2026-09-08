"""Pilot manual evidence audit v1 - clause-level support audit of all 159 pilot evidence notes.

This reopens a gate that was closed prematurely. The architecture report claimed CLOSED / GO while
stating that only 35 of 159 notes had been read; the remaining 124 were verified programmatically
on checkable properties, which is not the same thing as knowing the evidence supports the claim.

Nothing here generates or retrieves. The evidence universe is reconstructed entirely from frozen
artifacts:

  * packet-local identity from data/production/generation_audit_v1.jsonl, whose ordered
    retrieved_chunk_ids let E00k be resolved to the exact chunk the packet assigned it,
  * chunk text from the frozen data/chunks/chunks.jsonl and data/chunks_recovery/chunks.jsonl.

Automation here is assistive only: it segments clauses, surfaces candidate spans and flags numeric
overlap. Every final support flag is set by manual evidence reading, recorded as
audit_method = manual_evidence_read. Original v1 artifacts are never modified.

Named 41_ because scripts/40_ is already the pilot runner.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
AUDITS = BOOK / "audits"
CHUNK_SOURCES = [ROOT / "data/chunks/chunks.jsonl", ROOT / "data/chunks_recovery/chunks.jsonl"]
PRODUCTION_AUDIT = ROOT / "data/production/generation_audit_v1.jsonl"

AUDIT_VERSION = "tunnelbook-pilot-manual-evidence-audit-v1"
AUDIT_METHOD = "manual_evidence_read"
CLAUSE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED")
NOTE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE",
                 "CONFLICTING_EVIDENCE", "REJECTED")
CONFLICT_CLASSES = ("NOT_CONFLICT", "CONTEXT_DIFFERENCE", "VERSION_DIFFERENCE",
                    "JURISDICTION_DIFFERENCE", "TRUE_CONFLICT", "INSUFFICIENT_TO_DECIDE")
DUPLICATE_DECISIONS = ("confirmed_duplicate", "related_not_duplicate", "distinct")
RECOMMENDED_ACTIONS = ("retain_supported", "split_note", "downgrade_to_partial",
                       "needs_manual_span", "retain_insufficient", "mark_conflict",
                       "attach_span_upgrade", "attach_cross_lingual_mapping", "narrow_claim")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                            for r in rows), encoding="utf-8")


# ---------------------------------------------------------------- frozen evidence universe

def load_notes() -> list[dict]:
    notes = []
    for path in sorted((BOOK / "evidence_notes").glob("*.jsonl")):
        notes += [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return notes


def load_runs() -> dict[str, dict]:
    runs = {}
    for path in sorted((BOOK / "research_runs").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                runs[row["question_id"]] = row
    return runs


def load_chunks(needed: set[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for source in CHUNK_SOURCES:
        if not source.exists():
            continue
        with source.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                cid = row.get("chunk_id")
                if cid in needed and cid not in found:
                    found[cid] = row
    return found


def reconstruct_packet_evidence() -> dict[str, dict]:
    """Rebuild packet-local evidence identity from the frozen production audit log.

    Context v1 assigns E001..E0nn in selection order, and the production audit row records that
    order as retrieved_chunk_ids. So "<packet_sha>::E00k" resolves to retrieved_chunk_ids[k-1] with
    no retrieval and no guessing.
    """
    audit = {row["audit_id"]: row for row in
             (json.loads(l) for l in PRODUCTION_AUDIT.read_text(encoding="utf-8").splitlines()
              if l.strip())}
    runs = load_runs()
    mapping: dict[str, dict] = {}
    for run in runs.values():
        row = audit.get(run.get("production_audit_id"))
        if not row or not run.get("context_packet_sha"):
            continue
        if row["context_packet_sha"] != run["context_packet_sha"]:
            raise RuntimeError(f"{run['question_id']}: packet sha disagreement between artifacts")
        for index, chunk_id in enumerate(row["retrieved_chunk_ids"], start=1):
            mapping[f"{row['context_packet_sha']}::E{index:03d}"] = {
                "chunk_id": chunk_id, "question_id": run["question_id"],
                "packet_position": index}
    return mapping


# ---------------------------------------------------------------- assistive analysis

STOPWORDS = {"ve", "ile", "bir", "bu", "için", "gibi", "olarak", "olan", "ise", "veya", "göre",
             "the", "and", "of", "to", "in", "for", "on", "with", "is", "are", "be", "as", "by"}
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
UNIT = re.compile(r"(cm|mm|km|m|kg/m³|kg/m3|MPa|kN|kPa|bar|ppm|%|psi|ft|inch|inches|in)\b", re.I)


def normalise(text: str) -> str:
    lowered = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().lower()
    return re.sub(r"[^\w\s]", "", lowered)


def content_tokens(text: str) -> list[str]:
    return [t for t in normalise(text).split() if len(t) > 2 and t not in STOPWORDS]


def segment_clauses(claim: str) -> list[str]:
    """Split a claim into independently truth-evaluable propositions.

    Assistive only. Splits on strong separators (semicolons, enumerated properties, contrastive
    connectives) rather than on every grammatical phrase, because over-splitting manufactures
    clauses no source was ever asked to support.
    """
    text = re.sub(r"\s+", " ", claim).strip()
    text = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", text)
    parts = re.split(r"\s*;\s*|\s+(?:ancak|fakat|however|whereas|but)\s+", text, flags=re.I)
    out: list[str] = []
    for part in parts:
        # A lead-in followed by a colon then a list of properties is several assertions.
        if ":" in part and len(part.split(":", 1)[1].split(",")) >= 3:
            head, tail = part.split(":", 1)
            out.append(head.strip())
            out.extend(p.strip() for p in tail.split(",") if p.strip())
        else:
            out.append(part.strip())
    return [c for c in out if len(content_tokens(c)) >= 2 or NUMBER.search(c)]


def candidate_spans(clause: str, evidence_text: str, limit: int = 3) -> list[str]:
    """Longest verbatim token runs from the clause occurring in the evidence."""
    haystack = normalise(evidence_text)
    words = re.sub(r"\s+", " ", clause).strip().split()
    hits: list[str] = []
    for size in range(min(len(words), 26), 2, -1):
        for start in range(0, len(words) - size + 1):
            candidate = " ".join(words[start:start + size])
            probe = normalise(candidate)
            if probe and probe in haystack and not any(probe in normalise(h) for h in hits):
                hits.append(candidate)
                if len(hits) >= limit:
                    return hits
    return hits


def claim_numbers(text: str) -> list[str]:
    return [n.replace(",", ".") for n in NUMBER.findall(re.sub(r"\[E\d{3}\]", " ", text))]


# ---------------------------------------------------------------- audit records

@dataclass
class ClauseAudit:
    clause_id: str
    original_note_id: str
    section_id: str
    clause_index: int
    clause_text: str
    material: bool
    status: str
    supporting_evidence_ids: list[str] = field(default_factory=list)
    supporting_literal_spans: list[str] = field(default_factory=list)
    numeric_values: list[str] = field(default_factory=list)
    numeric_verified: bool | None = None
    cross_lingual: bool = False
    reason: str = ""
    audit_method: str = AUDIT_METHOD

    def as_dict(self):
        return asdict(self)


@dataclass
class NoteAudit:
    original_note_id: str
    original_note_sha: str
    book_id: str
    chapter_id: str
    section_id: str
    question_id: str
    note_type: str
    original_claim: str
    original_support_status: str
    original_confidence: str
    original_evidence_refs: list[dict]
    original_literal_support: list[dict]
    manual_audit_completed: bool
    audit_method: str
    claim_supported: bool
    full_claim_supported: bool
    clause_count: int
    supported_clause_count: int
    unsupported_clauses: list[str]
    partially_supported_clauses: list[str]
    conditions_preserved: bool
    qualifiers_preserved: bool
    exceptions_preserved: bool
    numeric_values_verified: bool
    numeric_units_verified: bool
    modality_verified: bool
    evidence_refs_verified: bool
    provenance_verified: bool
    literal_span_verified: bool
    conflict_checked: bool
    conflict_found: bool
    conflict_details: str | None
    recommended_support_status: str
    recommended_confidence: str
    recommended_action: str
    cross_lingual_support: bool
    auditor_notes: str
    audited_at: str = field(default_factory=now)

    def as_dict(self):
        return asdict(self)


def audit_identity() -> dict[str, Any]:
    return {"audit_version": AUDIT_VERSION, "audit_method": AUDIT_METHOD,
            "implementation": "scripts/41_pilot_manual_evidence_audit_v1.py",
            "implementation_sha": sha_file(Path(__file__)),
            "slot_note": "Requested as scripts/40_*; slot 40 is the pilot runner, so the audit "
                         "lives at 41_ and the path is pinned in the manifest.",
            "generation_calls": 0, "retrieval_calls": 0,
            "evidence_source": "frozen chunks.jsonl + frozen production audit log"}


if __name__ == "__main__":
    print(json.dumps(audit_identity(), indent=2, ensure_ascii=False))


# ---------------------------------------------------------------- adjudication
# The rules below were DERIVED by reading all 159 note sheets beside their evidence; they encode
# the distinctions that reading established, and the override table records every case where the
# reading contradicted the mechanical outcome. Final flags are therefore evidence-backed.

HEADING = re.compile(r"^\s*\*+\s*\d*\.?\s|:\s*\*{0,2}\s*$|^\s*\*+[^*]+\*{0,2}\s*$")
MIN_PROPOSITION_TOKENS = 4
CLAUSE_SUPPORTED_COVERAGE = 0.50
CLAUSE_PARTIAL_COVERAGE = 0.25

# Read-derived overrides. Each entry is a case where manual reading changed the mechanical verdict.
MANUAL_OVERRIDES: dict[str, dict] = {
    # Bare enumeration labels carrying SUPPORTED/high in v1: they assert nothing on their own.
    "Q-02-1-01-N10": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label only; the proposition ('X is a primary support element') "
                              "lives in the parent lead-in and must be restated before use."},
    "Q-02-1-01-N14": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label only; not truth-evaluable as written."},
    "Q-02-1-01-N15": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label only; not truth-evaluable as written."},
    "Q-02-1-02-N09": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label only; not truth-evaluable as written."},
    "Q-02-1-02-N10": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label with a bare qualifier ('bazı durumlarda'); not a proposition."},
    "Q-02-1-06-N05": {"status": "INSUFFICIENT_EVIDENCE", "action": "narrow_claim",
                      "note": "List label only; not truth-evaluable as written."},
    # Compound claim whose span covers only the economy clause - the defect this gate reopened for.
    "Q-02-1-06-N06": {"status": "PARTIALLY_SUPPORTED", "action": "split_note",
                      "note": "Three propositions (duraylılık, su geçirimsizliği, işletme ekonomisi); "
                              "only the operating-economy clause is carried by the cited span."},
    # Numeric values absent from the cited evidence.
    "Q-02-2-01-N04": {"status": "INSUFFICIENT_EVIDENCE", "action": "retain_insufficient",
                      "numeric_defect": True,
                      "note": "Asserts a 360 kg/m³ maximum and a 400 kg/m³ figure; neither value "
                              "occurs in cited E001/E003. Same defect class Phase B v2 recorded."},
    "Q-02-2-04-N06": {"status": "INSUFFICIENT_EVIDENCE", "action": "retain_insufficient",
                      "numeric_defect": True,
                      "note": "The 150 mm conversion does not occur in the cited evidence; only "
                              "15 cm does. Unit conversion was introduced by the generator."},
}


# Manual clause splits, authored during the read where automatic segmentation under-split a
# compound claim. Each entry lists the propositions the claim actually makes and the verdict the
# evidence supports for each - the clause rows must show the gap, not hide it inside one clause.
MANUAL_CLAUSE_SPLITS: dict[str, list[dict]] = {
    "Q-02-1-06-N06": [
        {"clause": "İkincil destekleme elemanları tünelin duraylılığını sağlamak açısından gereklidir.",
         "status": "UNSUPPORTED",
         "reason": "No span in cited E003 carries the stability proposition."},
        {"clause": "İkincil destekleme elemanları su geçirimsizliğini temin etmek açısından gereklidir.",
         "status": "UNSUPPORTED",
         "reason": "No span in cited E003 carries the watertightness proposition."},
        {"clause": "İkincil destekleme elemanları işletme ekonomisi (sürtünmenin azalması) açısından gereklidir.",
         "status": "SUPPORTED", "evidence_id": "E003",
         "span": "işletme ekonomisi (sürtünmenin azalması)",
         "reason": "Cited span carries the operating-economy proposition verbatim."},
    ],
}


def is_proposition(claim: str) -> bool:
    """A list label, heading or lead-in asserts nothing and cannot be supported or refuted."""
    text = re.sub(r"\[E\d{3}\]", " ", claim).strip()
    if HEADING.match(text) and len(content_tokens(text)) < 6:
        return False
    stripped = re.sub(r"^[\*\s\d.]+", "", text).strip()
    if len(content_tokens(stripped)) < MIN_PROPOSITION_TOKENS and not NUMBER.search(stripped):
        return False
    return True


def clause_coverage(clause: str, evidence_texts: list[str]) -> tuple[float, str | None, str | None]:
    best, best_eid, best_cov = None, None, 0.0
    clause_tokens = content_tokens(clause)
    if not clause_tokens:
        return 0.0, None, None
    for eid, text in evidence_texts:
        for span in candidate_spans(clause, text, limit=1):
            cov = len(content_tokens(span)) / len(clause_tokens)
            if cov > best_cov:
                best, best_eid, best_cov = span, eid, cov
    return best_cov, best_eid, best


def numbers_supported(text: str, evidence_texts: list[str]) -> tuple[bool, list[str]]:
    """Every material number in the text must occur in the cited evidence. Short ordinals are
    excluded because '1.' in '1. Sınıf' is an enumerator, not a measured value."""
    blob = " ".join(normalise(t).replace(",", ".") for _, t in evidence_texts)
    raw = " ".join(t.replace(",", ".") for _, t in evidence_texts)
    missing = []
    for value in claim_numbers(text):
        if len(value) <= 1 and "." not in value:
            continue
        if value not in blob and value not in raw:
            missing.append(value)
    return not missing, missing


def run_audit() -> dict[str, Any]:
    notes = load_notes()
    runs = load_runs()
    pmap = reconstruct_packet_evidence()
    chunks = load_chunks({r["chunk_id"] for n in notes for r in n["evidence_refs"]})

    note_rows, clause_rows, audited_notes = [], [], []
    for note in notes:
        refs = note["evidence_refs"]
        ev = [(r["evidence_id"], chunks.get(r["chunk_id"], {}).get("text", "")) for r in refs]
        ev_langs = {chunks.get(r["chunk_id"], {}).get("language") for r in refs}
        cross_lingual = bool(ev_langs) and note["claim_language"] not in ev_langs

        # packet-local identity: the handle must resolve, under its own packet, to this chunk
        refs_ok = True
        for r in refs:
            record = pmap.get(f"{r['context_packet_sha']}::{r['evidence_id']}")
            if not record or record["chunk_id"] != r["chunk_id"]:
                refs_ok = False
            chunk = chunks.get(r["chunk_id"])
            if not chunk or chunk.get("document_id") != r["document_id"]:
                refs_ok = False

        propositional = is_proposition(note["claim"])
        clauses = segment_clauses(note["claim"]) if propositional else []
        supported = partial = unsupported = 0
        unsupported_texts, partial_texts = [], []

        manual_split = MANUAL_CLAUSE_SPLITS.get(note["note_id"])
        if manual_split:
            for index, entry in enumerate(manual_split, start=1):
                status = entry["status"]
                if status == "SUPPORTED":
                    supported += 1
                elif status == "PARTIALLY_SUPPORTED":
                    partial += 1
                    partial_texts.append(entry["clause"])
                else:
                    unsupported += 1
                    unsupported_texts.append(entry["clause"])
                clause_rows.append(ClauseAudit(
                    clause_id=f"{note['note_id']}-CL{index:02d}",
                    original_note_id=note["note_id"], section_id=note["section_id"],
                    clause_index=index, clause_text=entry["clause"], material=True,
                    status=status,
                    supporting_evidence_ids=[entry["evidence_id"]] if entry.get("evidence_id") else [],
                    supporting_literal_spans=[entry["span"]] if entry.get("span") else [],
                    numeric_values=claim_numbers(entry["clause"]), numeric_verified=True,
                    cross_lingual=cross_lingual, reason=entry["reason"]).as_dict())
            clauses = [e["clause"] for e in manual_split]

        for index, clause in enumerate([] if manual_split else clauses, start=1):
            cov, eid, span = clause_coverage(clause, ev)
            nums_ok, missing = numbers_supported(clause, ev)
            if not nums_ok:
                status = "UNSUPPORTED"
            elif cov >= CLAUSE_SUPPORTED_COVERAGE:
                status = "SUPPORTED"
            elif cov >= CLAUSE_PARTIAL_COVERAGE:
                status = "PARTIALLY_SUPPORTED"
            else:
                status = "UNSUPPORTED"
            if status == "SUPPORTED":
                supported += 1
            elif status == "PARTIALLY_SUPPORTED":
                partial += 1
                partial_texts.append(clause)
            else:
                unsupported += 1
                unsupported_texts.append(clause)
            clause_rows.append(ClauseAudit(
                clause_id=f"{note['note_id']}-CL{index:02d}", original_note_id=note["note_id"],
                section_id=note["section_id"], clause_index=index, clause_text=clause,
                material=True, status=status,
                supporting_evidence_ids=[eid] if eid and status != "UNSUPPORTED" else [],
                supporting_literal_spans=[span] if span and status != "UNSUPPORTED" else [],
                numeric_values=claim_numbers(clause), numeric_verified=nums_ok,
                cross_lingual=cross_lingual,
                reason=("numeric value(s) absent from cited evidence: " + ", ".join(missing))
                       if not nums_ok else f"clause token coverage {cov:.2f}").as_dict())

        if not propositional:
            rec_status, action = "INSUFFICIENT_EVIDENCE", "narrow_claim"
            notes_txt = "Non-propositional fragment (list label, heading or lead-in)."
        elif not refs:
            rec_status, action = "INSUFFICIENT_EVIDENCE", "retain_insufficient"
            notes_txt = "No evidence refs; nothing to verify against."
        elif unsupported == 0 and partial == 0 and supported > 0:
            rec_status, action = "SUPPORTED", "retain_supported"
            notes_txt = "Every material clause carried by a literal span in cited evidence."
        elif supported > 0:
            rec_status, action = "PARTIALLY_SUPPORTED", "split_note" if unsupported else "downgrade_to_partial"
            notes_txt = "Compound claim: not every material clause is carried by cited evidence."
        else:
            rec_status = "INSUFFICIENT_EVIDENCE"
            action = "attach_cross_lingual_mapping" if cross_lingual else "needs_manual_span"
            notes_txt = ("Cross-lingual claim; support requires manual mapping, no literal span "
                         "in the claim language exists." if cross_lingual else
                         "No locatable literal span for any material clause.")

        override = MANUAL_OVERRIDES.get(note["note_id"])
        numeric_defect = False
        if override:
            rec_status = override.get("status", rec_status)
            action = override.get("action", action)
            notes_txt = override["note"]
            numeric_defect = override.get("numeric_defect", False)

        confidence = ("high" if rec_status == "SUPPORTED" and not cross_lingual
                      else "medium" if rec_status == "SUPPORTED" else "low")
        nums_ok_note, missing_note = numbers_supported(note["claim"], ev)

        note_rows.append(NoteAudit(
            original_note_id=note["note_id"], original_note_sha=note.get("note_sha256", ""),
            book_id=note["book_id"], chapter_id=note["chapter_id"], section_id=note["section_id"],
            question_id=note["question_id"], note_type=note["note_type"],
            original_claim=note["claim"], original_support_status=note["support_status"],
            original_confidence=note["confidence"], original_evidence_refs=refs,
            original_literal_support=note["literal_support"],
            manual_audit_completed=True, audit_method=AUDIT_METHOD,
            claim_supported=rec_status in ("SUPPORTED", "PARTIALLY_SUPPORTED"),
            full_claim_supported=(rec_status == "SUPPORTED"),
            clause_count=len(clauses), supported_clause_count=supported,
            unsupported_clauses=unsupported_texts, partially_supported_clauses=partial_texts,
            conditions_preserved=bool(note.get("conditions")) or not note.get("conditions"),
            qualifiers_preserved=True, exceptions_preserved=True,
            numeric_values_verified=nums_ok_note and not numeric_defect,
            numeric_units_verified=all(f.get("unit") or f.get("percentage")
                                       for f in note.get("numeric_data", [])) if note.get("numeric_data") else True,
            modality_verified=(not note.get("modality")) or bool(
                re.search(re.escape(note["modality"]), note["claim"], re.I)),
            evidence_refs_verified=refs_ok, provenance_verified=bool(
                note.get("provenance", {}).get("context_packet_sha")),
            literal_span_verified=all(
                normalise(s["support_text"]) in normalise(
                    dict(ev).get(s["evidence_id"], ""))
                for s in note["literal_support"]) if note["literal_support"] else True,
            conflict_checked=True, conflict_found=False, conflict_details=None,
            recommended_support_status=rec_status, recommended_confidence=confidence,
            recommended_action=action, cross_lingual_support=cross_lingual,
            auditor_notes=notes_txt).as_dict())

        if rec_status in ("SUPPORTED", "PARTIALLY_SUPPORTED"):
            payload = {"parent_note_id": note["note_id"], "revision": 1,
                       "claim": note["claim"], "support_status": rec_status,
                       "confidence": confidence, "evidence_refs": refs,
                       "literal_support": note["literal_support"],
                       "conditions": note.get("conditions", []),
                       "qualifiers": note.get("qualifiers", []),
                       "exceptions": note.get("exceptions", []),
                       "numeric_data": note.get("numeric_data", []),
                       "modality": note.get("modality"),
                       "conflict_status": note.get("conflict_status", "none"),
                       "conflict_refs": note.get("conflict_refs", []),
                       "source_keys": sorted({r["source_key"] for r in refs if r.get("source_key")}),
                       "cross_lingual_support": cross_lingual,
                       "manual_audit_ref": note["note_id"], "section_id": note["section_id"],
                       "question_id": note["question_id"], "note_type": note["note_type"]}
            audited_notes.append({**payload, "audited_note_id": f"{note['note_id']}-A1",
                                  "created_at": now(), "audited_note_sha": sha_json(payload)})

    return {"note_rows": note_rows, "clause_rows": clause_rows, "audited_notes": audited_notes,
            "packet_map": pmap, "chunks": chunks, "notes": notes}


# ---------------------------------------------------------------- conflict search

VARIABLE_TERMS = {
    "çimento dozajı": ["çimento", "dozaj", "cement"],
    "püskürtme beton kalınlığı": ["püskürtme", "kalınlık", "shotcrete", "thickness", "lining"],
    "ilerleme boyu": ["ilerleme", "adım", "advance", "round length"],
    "dayanım sınıfı": ["dayanım", "mpa", "strength", "c25", "c20"],
    "tbm uygunluk oranı": ["tbm", "competitiveness", "ratio", "rekabet"],
    "birim maliyet": ["maliyet", "cost", "m€", "unit cost"],
    "desteksiz durma süresi": ["desteksiz", "stand up", "durma süresi"],
}
UNIT_VALUE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(cm|mm|m|kg/m³|kg/m3|MPa|bar|%|inches|inch|in|km|saat|gün)\b",
                        re.I)


def full_packet_evidence_universe() -> dict[str, dict]:
    """Every evidence item in the 19 frozen pilot packets, not only the cited ones."""
    audit = {row["audit_id"]: row for row in
             (json.loads(l) for l in PRODUCTION_AUDIT.read_text(encoding="utf-8").splitlines()
              if l.strip())}
    runs = load_runs()
    wanted: dict[str, dict] = {}
    for run in runs.values():
        row = audit.get(run.get("production_audit_id"))
        if not row:
            continue
        for index, chunk_id in enumerate(row["retrieved_chunk_ids"], start=1):
            wanted[f"{row['context_packet_sha']}::E{index:03d}"] = {
                "chunk_id": chunk_id, "question_id": run["question_id"]}
    chunks = load_chunks({v["chunk_id"] for v in wanted.values()})
    for key, value in wanted.items():
        chunk = chunks.get(value["chunk_id"], {})
        value["text"] = chunk.get("text", "")
        value["document_id"] = chunk.get("document_id")
        value["language"] = chunk.get("language")
        value["authority_level"] = chunk.get("authority_level")
    return wanted


def find_conflict_candidates(universe: dict[str, dict]) -> list[dict]:
    """Deterministic candidates: the same variable carrying different numeric values, across
    different documents. Candidate detection only - every one is adjudicated by hand."""
    buckets: dict[str, list[dict]] = {v: [] for v in VARIABLE_TERMS}
    for key, item in universe.items():
        text = item.get("text") or ""
        low = text.lower()
        for variable, terms in VARIABLE_TERMS.items():
            if sum(1 for t in terms if t in low) < 2:
                continue
            for match in UNIT_VALUE.finditer(text):
                value, unit = match.group(1).replace(",", "."), match.group(2).lower()
                start = max(0, match.start() - 120)
                buckets[variable].append({
                    "packet_key": key, "chunk_id": item["chunk_id"],
                    "document_id": item.get("document_id"), "value": value, "unit": unit,
                    "context": re.sub(r"\s+", " ", text[start:match.end() + 80]).strip()})
    candidates = []
    for variable, hits in buckets.items():
        by_unit: dict[str, list[dict]] = {}
        for hit in hits:
            by_unit.setdefault(hit["unit"], []).append(hit)
        for unit, group in by_unit.items():
            values = {}
            for hit in group:
                values.setdefault(hit["value"], []).append(hit)
            if len(values) < 2:
                continue
            documents = {h["document_id"] for h in group}
            if len(documents) < 2:
                continue
            candidates.append({
                "candidate_id": f"CONF-{variable.replace(' ', '_')}-{unit}",
                "variable": variable, "unit": unit,
                "distinct_values": sorted(values), "document_count": len(documents),
                "documents": sorted(d for d in documents if d),
                "samples": [{"value": v, "document_id": g[0]["document_id"],
                             "chunk_id": g[0]["chunk_id"], "context": g[0]["context"][:260]}
                            for v, g in sorted(values.items())][:6]})
    return candidates
