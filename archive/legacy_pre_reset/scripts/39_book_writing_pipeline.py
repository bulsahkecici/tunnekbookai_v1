"""TunnelBookAI book-writing pipeline v1 - evidence preparation controller.

This is NOT the chapter writer. It builds the evidence and control layer that must exist before any
prose is drafted:

    BookProject -> ChapterPlan -> SectionPlan -> ResearchQuestion[]
                -> ProductionGroundedGenerator -> GroundedAnswer
                -> EvidenceNote[] -> ClaimLedger -> SectionEvidenceBundle

and then stops. `draft_section` exists as an interface and deliberately raises NotImplementedError.

Two rules shape the whole design:

  * The corpus is the only factual authority. Nothing here consults the web, an external source, or
    the model's own memory; every note must trace to a chunk.
  * An accepted grounded answer is INPUT, not a fact. It is decomposed deterministically into notes,
    each of which must carry literal spans from the evidence it cites. Copying an answer wholesale
    into a note is exactly the failure this layer exists to prevent.

Named 39_ because scripts/37_ is already the production orchestration smoke runner.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
SOURCE_REGISTRY = BOOK / "source_registry_v1.jsonl"

PIPELINE_VERSION = "tunnelbook-book-writing-pipeline-v1"
SOURCE_POLICY = "corpus_only"
DRAFTING_ENABLED = False

QUESTION_TYPES = ("definition", "conceptual", "mechanism", "design", "construction",
                  "classification", "comparison", "numeric", "formula",
                  "standard_or_specification", "risk", "failure_mode", "methodology",
                  "historical", "case_example", "multi_source_synthesis", "cross_lingual",
                  "uncertainty")
PRIORITIES = ("P0", "P1", "P2")
QUESTION_STATUSES = ("planned", "answered", "insufficient_evidence", "generator_rejected",
                     "request_rejected")
READINESS = ("READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


notes_contract = _load("evidence_note_contract", "scripts/38_evidence_note_contract.py")
production = _load("production_generator", "scripts/36_production_grounded_generator.py")

EvidenceNote = notes_contract.EvidenceNote
EvidenceRef = notes_contract.EvidenceRef
LiteralSupport = notes_contract.LiteralSupport
NumericFact = notes_contract.NumericFact


class DraftingDisabled(NotImplementedError):
    """Prose drafting is a later phase and is not implemented here."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                            for r in rows), encoding="utf-8")


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


# ---------------------------------------------------------------- plan schemas

@dataclass
class BookProject:
    book_id: str
    working_title: str
    language: str
    audience: str
    technical_level: str
    purpose: str
    chapter_ids: list[str] = field(default_factory=list)
    source_policy: str = SOURCE_POLICY
    citation_policy: str = "evidence_note_backed_only"
    status: str = "planning"
    created_at: str = field(default_factory=_now)

    def __post_init__(self):
        if self.source_policy != SOURCE_POLICY:
            raise ValueError(f"source_policy must be {SOURCE_POLICY!r} in v1")

    def as_dict(self):
        return asdict(self)


@dataclass
class ChapterPlan:
    chapter_id: str
    chapter_number: int
    title: str
    purpose: str
    scope_in: list[str] = field(default_factory=list)
    scope_out: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    section_ids: list[str] = field(default_factory=list)
    target_audience: str = ""
    technical_depth: str = ""
    status: str = "planned"

    def as_dict(self):
        return asdict(self)


@dataclass
class SectionPlan:
    section_id: str
    chapter_id: str
    section_number: str
    title: str
    objective: str
    questions: list[str] = field(default_factory=list)
    required_topics: list[str] = field(default_factory=list)
    optional_topics: list[str] = field(default_factory=list)
    excluded_topics: list[str] = field(default_factory=list)
    expected_claim_types: list[str] = field(default_factory=list)
    status: str = "planned"

    def as_dict(self):
        return asdict(self)


@dataclass
class ResearchQuestion:
    question_id: str
    section_id: str
    question: str
    question_language: str
    question_type: str
    priority: str
    required: bool
    expected_answer_type: str
    minimum_sources: int = 1
    notes: str = ""
    status: str = "planned"

    def __post_init__(self):
        if self.question_type not in QUESTION_TYPES:
            raise ValueError(f"invalid question_type {self.question_type!r}")
        if self.priority not in PRIORITIES:
            raise ValueError(f"invalid priority {self.priority!r}")
        if self.question_language not in ("tr", "en"):
            raise ValueError(f"invalid question_language {self.question_language!r}")
        if self.status not in QUESTION_STATUSES:
            raise ValueError(f"invalid status {self.status!r}")

    def as_dict(self):
        return asdict(self)


@dataclass
class ClaimLedgerEntry:
    claim_id: str
    section_id: str
    canonical_claim: str
    note_ids: list[str] = field(default_factory=list)
    support_status: str = "SUPPORTED"
    required_for_section: bool = False
    duplicate_of: str | None = None
    duplicate_candidates: list[str] = field(default_factory=list)
    conflict_group: str | None = None
    numeric: bool = False
    citation_ready: bool = False
    review_status: str = "unreviewed"

    def as_dict(self):
        return asdict(self)


@dataclass
class SectionEvidenceBundle:
    section_id: str
    book_id: str
    chapter_id: str
    research_questions: list[dict]
    research_results: list[dict]
    evidence_notes: list[dict]
    claim_ledger: list[dict]
    unanswered_questions: list[str]
    rejected_questions: list[str]
    conflicts: list[dict]
    numeric_facts: list[dict]
    requirements: list[dict]
    source_summary: dict
    coverage_summary: dict
    readiness: str
    readiness_reasons: list[str]
    pipeline_version: str = PIPELINE_VERSION
    evidence_note_contract_version: str = notes_contract.CONTRACT_VERSION
    source_policy: str = SOURCE_POLICY
    created_at: str = field(default_factory=_now)
    bundle_sha: str = ""

    def canonical_payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("created_at", None)
        payload.pop("bundle_sha", None)
        return payload

    def finalise(self) -> "SectionEvidenceBundle":
        self.bundle_sha = _sha_json(self.canonical_payload())
        return self

    def as_dict(self):
        return asdict(self)


# ---------------------------------------------------------------- source registry

def source_key(document_id: str, chunk_id: str) -> str:
    """Stable, deterministic book-level key. Packet-local [E###] handles never appear in a book."""
    digest = hashlib.sha256(f"{document_id}|{chunk_id}".encode("utf-8")).hexdigest()[:12]
    return f"SRC-{document_id}-{digest}"


def register_source(record: dict[str, Any]) -> str:
    """Append-only registry. The same document/chunk always maps to the same key."""
    key = source_key(record["document_id"], record["chunk_id"])
    existing = load_source_registry()
    if key in existing:
        return key
    _append_jsonl(SOURCE_REGISTRY, {
        "source_key": key, "document_id": record["document_id"], "chunk_id": record["chunk_id"],
        "title": record.get("title"), "citation_mode": record.get("citation_mode"),
        "provenance_status": record.get("provenance_status"),
        "page_start": record.get("page_start"), "page_end": record.get("page_end"),
        "slide_start": record.get("slide_start"), "slide_end": record.get("slide_end"),
        "section_path": record.get("section_path"),
        "source_relative_path": record.get("source_relative_path"),
        "language": record.get("language"), "authority_level": record.get("authority_level"),
        "registered_at": _now()})
    return key


def load_source_registry() -> dict[str, dict[str, Any]]:
    if not SOURCE_REGISTRY.exists():
        return {}
    return {row["source_key"]: row for row in
            (json.loads(l) for l in SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines()
             if l.strip())}


# ---------------------------------------------------------------- note extraction

STOPWORDS = {"ve", "ile", "bir", "bu", "için", "gibi", "olarak", "olan", "ise", "veya", "göre",
             "the", "and", "of", "to", "in", "for", "on", "with", "is", "are", "be", "as", "by"}
HANDLE = re.compile(r"\[E(\d{3})\]")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
UNIT = re.compile(r"(cm|mm|km|m|kg/m³|kg/m3|MPa|kN|kPa|bar|ppm|%|psi|ft|inch|inches|in)\b", re.I)
# Word-boundary anchored so "en az" does not fire inside "en aza indirmek" and "en fazla" does
# not fire inside "birden fazla" - both observed in the pilot before this was tightened.
MODALITY_TR = re.compile(r"(?<!\w)(olmalıdır|yapılmalıdır|gerekir|gereklidir|zorunlu|önerilir|"
                         r"tavsiye|en az|en fazla|asgari|azami)(?!\w)", re.I)
MODALITY_EN = re.compile(r"\b(must|shall|should|may|recommended|required|minimum|maximum)\b", re.I)
TABLE_BLOB = re.compile(r"(\|\s*:?-{2,})")
CONDITION_TR = re.compile(r"(durumunda|halinde|koşuluyla|şartıyla|olduğunda|bağlı olarak|"
                          r"göre değiş|dışında|hariç|istisna)", re.I)
CONDITION_EN = re.compile(r"\b(if|when|where|unless|provided that|depending on|except|"
                          r"in case of)\b", re.I)
DEFINITION_TR = re.compile(r"(olarak tanımlan|olarak adlandırıl|denir|adı verilir|demektir)", re.I)
DEFINITION_EN = re.compile(r"\b(is defined as|is called|refers to|is known as|means)\b", re.I)


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = HANDLE.sub(" ", text)
    return re.sub(r"[^\w\s]", " ", text)


def _content_tokens(text: str) -> list[str]:
    return [t for t in _normalise(text).split() if len(t) > 2 and t not in STOPWORDS]


def segment_answer(answer: str) -> list[str]:
    """Decompose an accepted answer into candidate propositions. Deterministic; no LLM."""
    text = re.sub(r"\r", "", answer)
    blocks = [b.strip() for b in re.split(r"\n(?=\s*(?:[-*•]|\d{1,2}[.)]))|\n{2,}", text)
              if b.strip()]
    units: list[str] = []
    for block in blocks:
        block = re.sub(r"\s+", " ", block).strip()
        if not block:
            continue
        if re.match(r"^\s*(?:[-*•]|\d{1,2}[.)])", block) or len(block) < 200:
            units.append(block)
        else:
            units.extend(p.strip() for p in
                         re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])", block) if p.strip())
    return [u for u in units if u]


def _is_material(unit: str) -> bool:
    if len(TABLE_BLOB.findall(unit)) >= 2:
        return False          # a whole table is not one proposition
    stripped = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", unit).strip()
    stripped = re.sub(r"^\*\*(.*?)\*\*\s*:?\s*$", "", stripped).strip()
    if not stripped:
        return False
    if re.search(r":\s*$", stripped) and not HANDLE.search(stripped):
        return False
    return len(_content_tokens(stripped)) >= 4 or bool(NUMBER.search(stripped))


def _find_literal_span(unit: str, evidence_text: str) -> str | None:
    """Longest contiguous token run from the claim that occurs verbatim in the evidence.

    Matching uses the contract's own normaliser, so a span this function accepts is a span the
    contract will accept. Producer and validator cannot drift apart.
    """
    haystack = notes_contract.normalise_for_span_match(evidence_text)
    words = re.sub(r"\s+", " ", re.sub(r"\[E\d{3}\]", " ", unit)).strip().split()
    for size in range(min(len(words), 24), 3, -1):
        for start in range(0, len(words) - size + 1):
            candidate = " ".join(words[start:start + size])
            probe = notes_contract.normalise_for_span_match(candidate)
            if probe and probe in haystack:
                return candidate
    return None


def _classify(unit: str, language: str) -> str:
    modality = MODALITY_TR if language == "tr" else MODALITY_EN
    definition = DEFINITION_TR if language == "tr" else DEFINITION_EN
    if NUMBER.search(re.sub(r"\[E\d{3}\]", " ", unit)) and UNIT.search(unit):
        return "numeric"
    if modality.search(unit):
        return "requirement"
    if definition.search(unit):
        return "definition"
    if re.search(r"(karşılaştır|compared|versus|farkı|difference)", unit, re.I):
        return "comparison"
    if re.search(r"(risk|tehlike|hazard|failure|göçük|yangın|fire)", unit, re.I):
        return "risk"
    return "fact"


def _extract_conditions(unit: str, language: str) -> list[str]:
    pattern = CONDITION_TR if language == "tr" else CONDITION_EN
    return [m.group(0) for m in pattern.finditer(unit)]


def _extract_numeric(unit: str, evidence_ids: list[str]) -> list[NumericFact]:
    facts = []
    clean = re.sub(r"\[E\d{3}\]", " ", unit)
    for match in re.finditer(r"(\d+(?:[.,]\d+)?)(?:\s*[-–]\s*(\d+(?:[.,]\d+)?))?\s*"
                             r"(cm|mm|km|m|kg/m³|kg/m3|MPa|kN|kPa|bar|ppm|%|psi|ft|inch|inches|in)\b",
                             clean, re.I):
        low, high, unit_text = match.group(1), match.group(2), match.group(3)
        facts.append(NumericFact(
            value=None if high else low, range=f"{low}-{high}" if high else None,
            minimum=low if high else None, maximum=high if high else None,
            unit=unit_text, source_evidence_ids=list(evidence_ids)))
    return facts


def extract_notes(answer: str, packet, question, book_id: str, chapter_id: str,
                  language: str, generation_trace: dict) -> list[EvidenceNote]:
    """Decompose one accepted answer into evidence notes.

    Deterministic throughout. Each note keeps only the handles its own sentence cites, and its
    support status is decided by whether a literal span can be located in that cited evidence -
    never by how confident the prose sounds.
    """
    packet_sha = generation_trace["context_packet_sha"]
    by_id = {item.evidence_id: item for item in packet.evidence_items}
    produced: list[EvidenceNote] = []

    for index, unit in enumerate(segment_answer(answer), start=1):
        if not _is_material(unit):
            continue
        cited = [f"E{m}" for m in HANDLE.findall(unit)]
        cited = [e for e in dict.fromkeys(cited) if e in by_id]
        note_type = _classify(unit, language)
        claim = re.sub(r"\s*\[E\d{3}\]", "", unit).strip()
        claim = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", claim)
        claim = re.sub(r"\*\*(.*?)\*\*", r"\1", claim).strip()

        refs, supports = [], []
        for evidence_id in cited:
            item = by_id[evidence_id]
            key = register_source({
                "document_id": item.document_id, "chunk_id": item.chunk_id, "title": item.title,
                "citation_mode": item.citation_mode, "provenance_status": item.provenance_status,
                "page_start": item.original_page_start, "page_end": item.original_page_end,
                "slide_start": item.slide_start, "slide_end": item.slide_end,
                "section_path": item.section_path,
                "source_relative_path": item.source_relative_path,
                "language": item.language, "authority_level": item.authority_level})
            refs.append(EvidenceRef(
                evidence_id=evidence_id, context_packet_sha=packet_sha, chunk_id=item.chunk_id,
                document_id=item.document_id, citation_mode=item.citation_mode,
                provenance_status=item.provenance_status, retrieval_rank=item.retrieval_rank,
                retrieval_score=item.retrieval_score, page_start=item.original_page_start,
                page_end=item.original_page_end, slide_start=item.slide_start,
                slide_end=item.slide_end, section_path=item.section_path, title=item.title,
                source_relative_path=item.source_relative_path, source_key=key))
            span = _find_literal_span(unit, item.text)
            if span:
                support_type = ("numeric_direct" if note_type == "numeric"
                                else "definition_direct" if note_type == "definition" else "direct")
                supports.append(LiteralSupport(evidence_id=evidence_id, support_text=span,
                                               support_type=support_type))

        conditions = _extract_conditions(unit, language)
        modality_match = (MODALITY_TR if language == "tr" else MODALITY_EN).search(unit)
        numeric_data = _extract_numeric(unit, [r.evidence_id for r in refs]) \
            if note_type == "numeric" else []

        review = "unreviewed"
        # EVERY numeric fact in the note must be carried by a literal span, not merely one of
        # them. A claim stating "2,0-3,0 m üst yarı, 4,0 m alt yarı" whose span only shows the
        # 4,0 m has not evidenced the first figure, and a book must not inherit the difference.
        if numeric_data and supports:
            carried = " ".join(sp.support_text for sp in supports).replace(",", ".")
            for fact in numeric_data:
                values = [v.replace(",", ".") for v in
                          (fact.value, fact.minimum, fact.maximum) if v]
                if values and not all(v in carried for v in values):
                    supports = []
                    break

        if not refs:
            status, confidence = "INSUFFICIENT_EVIDENCE", "low"
        elif supports:
            status, confidence = "SUPPORTED", "high"
        else:
            # Cited, but no literal span is locatable by deterministic matching. Support has NOT
            # been demonstrated, so it is not claimed. This is the normal outcome when the model
            # paraphrases, synthesises across items, or answers in Turkish from English evidence -
            # a human can attach the span and upgrade the note, but the pipeline never asserts
            # support it cannot show.
            status, confidence = "INSUFFICIENT_EVIDENCE", "low"
            review = "needs_manual_literal_span"

        if note_type == "numeric" and not numeric_data:
            note_type = "fact"
        if note_type == "requirement" and not modality_match:
            note_type = "fact"

        produced.append(EvidenceNote(
            note_id=f"{question.question_id}-N{index:02d}", book_id=book_id,
            chapter_id=chapter_id, section_id=question.section_id,
            question_id=question.question_id, note_type=note_type, claim=claim,
            claim_language=language, support_status=status, confidence=confidence,
            evidence_refs=refs, literal_support=supports, source_count=len(refs),
            source_diversity={"document_count": len({r.document_id for r in refs}),
                              "language_count": len({by_id[r.evidence_id].language
                                                     for r in refs if by_id[r.evidence_id].language}),
                              "independent_source_count": len({r.document_id for r in refs})},
            conditions=conditions,
            modality=modality_match.group(0).lower() if modality_match else None,
            numeric_data=numeric_data,
            provenance={"context_packet_sha": packet_sha,
                        "production_request_id": generation_trace.get("request_id"),
                        "production_audit_id": generation_trace.get("audit_id"),
                        "source_policy": SOURCE_POLICY},
            generation_trace=generation_trace, review_status=review, created_at=_now()))
    return produced


# ---------------------------------------------------------------- claim ledger

def _similarity(left: str, right: str) -> float:
    a, b = set(_content_tokens(left)), set(_content_tokens(right))
    return len(a & b) / len(a | b) if a and b else 0.0


def build_claim_ledger(notes: list[EvidenceNote], section_id: str,
                       duplicate_threshold: float = 0.75) -> list[ClaimLedgerEntry]:
    """Deterministic ledger. Duplicate detection is lexical; no model is asked to merge claims."""
    entries: list[ClaimLedgerEntry] = []
    for index, note in enumerate(notes, start=1):
        entry = ClaimLedgerEntry(
            claim_id=f"{section_id}-C{index:03d}", section_id=section_id,
            canonical_claim=note.claim, note_ids=[note.note_id],
            support_status=note.support_status,
            numeric=bool(note.numeric_data),
            citation_ready=(note.support_status in ("SUPPORTED", "PARTIALLY_SUPPORTED")
                            and bool(note.evidence_refs)
                            and all(r.source_key for r in note.evidence_refs)
                            and note.conflict_status != "conflicting"))
        entries.append(entry)

    for i, entry in enumerate(entries):
        for j in range(i + 1, len(entries)):
            if _similarity(entry.canonical_claim, entries[j].canonical_claim) >= duplicate_threshold:
                entry.duplicate_candidates.append(entries[j].claim_id)
                entries[j].duplicate_candidates.append(entry.claim_id)
    return entries


# ---------------------------------------------------------------- readiness

def assess_readiness(questions: list[ResearchQuestion], results: list[dict],
                     notes: list[EvidenceNote],
                     ledger: list[ClaimLedgerEntry],
                     invalid_note_ids: list[str] | None = None) -> tuple[str, list[str]]:
    """Readiness must see the whole picture, including notes the contract rejected.

    A section whose notes were mostly discarded is not ready merely because the survivors are
    clean - that would be writing around the gap. Invalid notes and unsupported P0 questions are
    therefore first-class readiness inputs, not silent losses.
    """
    reasons: list[str] = []
    invalid_note_ids = invalid_note_ids or []
    by_id = {q.question_id: q for q in questions}
    status = {r["question_id"]: r["question_status"] for r in results}

    p0 = [q for q in questions if q.priority == "P0"]
    p0_unresolved = [q.question_id for q in p0 if status.get(q.question_id) != "answered"]
    rejected = [qid for qid, s in status.items() if s == "generator_rejected"]
    insufficient = [qid for qid, s in status.items() if s == "insufficient_evidence"]
    conflicts = [n for n in notes if n.conflict_status == "conflicting"]
    required_unsupported = [e.claim_id for e in ledger
                            if e.required_for_section and e.support_status
                            not in ("SUPPORTED", "PARTIALLY_SUPPORTED")]
    missing_provenance = [n.note_id for n in notes if not n.provenance]

    # A P0 question that produced no demonstrably supported note has not been established,
    # whatever its generation status says.
    supported_by_question: dict[str, int] = {}
    for note in notes:
        if note.support_status == "SUPPORTED":
            supported_by_question[note.question_id] = supported_by_question.get(
                note.question_id, 0) + 1
    p0_unsupported = [q.question_id for q in p0 if not supported_by_question.get(q.question_id)]

    if p0_unresolved:
        reasons.append(f"P0 questions unresolved: {p0_unresolved}")
    if p0_unsupported:
        reasons.append(f"P0 questions without any SUPPORTED evidence note: {p0_unsupported}")
    if invalid_note_ids:
        reasons.append(f"contract-invalid evidence notes discarded: {len(invalid_note_ids)}")
    if any(by_id[q].priority == "P0" for q in rejected if q in by_id):
        reasons.append(f"P0 generator rejection: "
                       f"{[q for q in rejected if by_id.get(q) and by_id[q].priority == 'P0']}")
    if required_unsupported:
        reasons.append(f"required claims unsupported: {required_unsupported}")
    if missing_provenance:
        reasons.append(f"notes missing provenance: {missing_provenance}")
    if conflicts:
        reasons.append(f"unresolved conflicts: {[n.note_id for n in conflicts]}")

    if reasons:
        return "NOT_READY", reasons

    limitations: list[str] = []
    p1_unresolved = [q.question_id for q in questions
                     if q.priority == "P1" and status.get(q.question_id) != "answered"]
    p2_unresolved = [q.question_id for q in questions
                     if q.priority == "P2" and status.get(q.question_id) != "answered"]
    if p1_unresolved:
        limitations.append(f"P1 questions unresolved: {p1_unresolved}")
    if p2_unresolved:
        limitations.append(f"P2 questions unresolved: {p2_unresolved}")
    if insufficient:
        limitations.append(f"insufficient corpus evidence for: {insufficient}")
    if rejected:
        limitations.append(f"non-P0 generator rejections: {rejected}")
    partial = [n.note_id for n in notes if n.support_status == "PARTIALLY_SUPPORTED"]
    if partial:
        limitations.append(f"partially supported notes require review: {len(partial)}")
    needs_span = [n.note_id for n in notes
                  if n.review_status == "needs_manual_literal_span"]
    if needs_span:
        limitations.append(
            f"notes citing evidence with no auto-locatable literal span, awaiting manual "
            f"attachment: {len(needs_span)}")
    unsupported = [n.note_id for n in notes if n.support_status == "INSUFFICIENT_EVIDENCE"]
    if unsupported:
        limitations.append(f"notes without demonstrated support: {len(unsupported)}")

    if limitations:
        return "READY_WITH_LIMITATIONS", limitations
    return "READY_FOR_DRAFT", []


# ---------------------------------------------------------------- research execution

def run_section_research(book: BookProject, chapter: ChapterPlan, section: SectionPlan,
                         questions: list[ResearchQuestion],
                         runtime=None) -> dict[str, Any]:
    """Execute one section's research through the frozen production generator.

    The generator's internal chain is never duplicated. Its packet is observed by wrapping
    build_packet, so exactly one retrieval happens per question and the packet we record is
    provably the one it used - the recorded sha is compared against the result's.
    """
    runtime = runtime or production.ProductionGroundedGenerator()
    captured: dict[str, Any] = {}
    original_build = runtime.build_packet

    def observing_build(request):
        packet = original_build(request)
        captured["packet"] = packet
        return packet

    runtime.build_packet = observing_build
    results, all_notes = [], []
    packet_evidence: dict[str, dict[str, Any]] = {}
    try:
        for question in questions:
            captured.clear()
            request = production.ProductionGenerationRequest(
                query=question.question, query_language=question.question_language)
            try:
                outcome = runtime.generate(request)
            except production.RequestRejected as error:
                question.status = "request_rejected"
                results.append({"book_id": book.book_id, "chapter_id": chapter.chapter_id,
                                "section_id": section.section_id,
                                "question_id": question.question_id, "question": question.question,
                                "query_language": question.question_language,
                                "priority": question.priority, "question_status": "request_rejected",
                                "production_status": "request_rejected",
                                "failure_reasons": [str(error)], "accepted_answer": None,
                                "evidence_handles": [], "context_packet_sha": None,
                                "created_at": _now()})
                continue

            packet = captured.get("packet")
            row = {"book_id": book.book_id, "chapter_id": chapter.chapter_id,
                   "section_id": section.section_id, "question_id": question.question_id,
                   "question": question.question, "query_language": question.question_language,
                   "priority": question.priority,
                   "production_request_id": outcome.request_id,
                   "production_audit_id": outcome.audit_id,
                   "production_status": outcome.status,
                   "failure_reasons": outcome.failure_reasons,
                   "context_packet_sha": outcome.context_packet_sha,
                   "evidence_handles": outcome.evidence_handles,
                   "created_at": _now()}

            if outcome.status == "rejected":
                # Never fabricated, never silently dropped: the gap stays visible.
                question.status = "generator_rejected"
                row.update(question_status="generator_rejected", accepted_answer=None,
                           answerability_status="not_determined")
                results.append(row)
                continue

            assert packet is not None, "packet was not observed for an accepted generation"
            # Prove the observed packet is the one the orchestrator actually used, by recomputing
            # its sha exactly as the orchestrator does. Any mismatch means we captured the wrong
            # object and every evidence ref derived from it would be unsound.
            observed_sha = hashlib.sha256(
                packet.to_json(indent=None).encode("utf-8")).hexdigest()
            if observed_sha != outcome.context_packet_sha:
                raise RuntimeError(
                    f"{question.question_id}: observed packet sha {observed_sha} does not match "
                    f"the generation's {outcome.context_packet_sha}")

            answer = outcome.answer
            abstained = bool(re.match(r"^\s*(YETERSİZ KANIT|INSUFFICIENT EVIDENCE)", answer,
                                      re.IGNORECASE))
            trace = {"request_id": outcome.request_id, "audit_id": outcome.audit_id,
                     "context_packet_sha": outcome.context_packet_sha,
                     "production_generator": production.VERSION,
                     "output_contract": "tunnelbook-generation-output-contract-v1.1"}

            if abstained:
                question.status = "insufficient_evidence"
                row.update(question_status="insufficient_evidence",
                           answerability_status="insufficient_evidence",
                           accepted_answer=answer)
                results.append(row)
                continue

            question.status = "answered"
            # Retain the evidence this packet exposed, keyed packet-locally, so the note contract
            # can verify handles and literal spans against the real text rather than trusting them.
            for item in packet.evidence_items:
                packet_evidence[f"{outcome.context_packet_sha}::{item.evidence_id}"] = {
                    "chunk_id": item.chunk_id, "document_id": item.document_id,
                    "text": item.text, "language": item.language,
                    "authority_level": item.authority_level}
            notes = extract_notes(answer, packet, question, book.book_id, chapter.chapter_id,
                                  question.question_language, trace)
            all_notes.extend(notes)
            row.update(question_status="answered", answerability_status="answered",
                       accepted_answer=answer, note_ids=[n.note_id for n in notes])
            results.append(row)
    finally:
        runtime.build_packet = original_build

    return {"results": results, "notes": all_notes, "packet_evidence": packet_evidence}


def build_section_bundle(book: BookProject, chapter: ChapterPlan, section: SectionPlan,
                         questions: list[ResearchQuestion], research: dict[str, Any],
                         packet_evidence: dict[str, dict[str, Any]] | None = None,
                         known_chunks: set[str] | None = None) -> tuple[SectionEvidenceBundle, dict]:
    notes = research["notes"]
    if packet_evidence is None:
        # Default to the evidence actually observed during research; validating against nothing
        # would silently disable the handle and literal-span checks.
        packet_evidence = research.get("packet_evidence")
    validation = notes_contract.validate_notes(notes, packet_evidence, known_chunks)
    valid_notes = [n for n, r in zip(notes, validation["results"]) if r.valid]
    invalid_ids = [r.note_id for r in validation["results"] if not r.valid]
    # The ledger cites only demonstrably supported notes; readiness still sees everything.
    ledger = build_claim_ledger([n for n in valid_notes if n.support_status == "SUPPORTED"],
                                section.section_id)
    readiness, reasons = assess_readiness(questions, research["results"], valid_notes, ledger,
                                          invalid_note_ids=invalid_ids)

    bundle = SectionEvidenceBundle(
        section_id=section.section_id, book_id=book.book_id, chapter_id=chapter.chapter_id,
        research_questions=[q.as_dict() for q in questions],
        research_results=research["results"],
        evidence_notes=[n.as_dict() for n in valid_notes],
        claim_ledger=[e.as_dict() for e in ledger],
        unanswered_questions=[r["question_id"] for r in research["results"]
                              if r["question_status"] == "insufficient_evidence"],
        rejected_questions=[r["question_id"] for r in research["results"]
                            if r["question_status"] in ("generator_rejected", "request_rejected")],
        conflicts=[n.as_dict() for n in valid_notes if n.conflict_status == "conflicting"],
        numeric_facts=[{"note_id": n.note_id, "claim": n.claim,
                        "numeric": [f.as_dict() for f in n.numeric_data]}
                       for n in valid_notes if n.numeric_data],
        requirements=[{"note_id": n.note_id, "claim": n.claim, "modality": n.modality}
                      for n in valid_notes if n.note_type in ("requirement", "recommendation")],
        source_summary=_source_summary(valid_notes),
        coverage_summary={**_coverage_summary(questions, research["results"], valid_notes),
                          "notes_extracted": len(notes),
                          "notes_contract_valid": len(valid_notes),
                          "notes_contract_invalid": len(invalid_ids),
                          "note_validity_rate": (round(len(valid_notes) / len(notes), 4)
                                                 if notes else None),
                          "notes_needing_manual_span": sum(
                              1 for n in valid_notes
                              if n.review_status == "needs_manual_literal_span")},
        readiness=readiness, readiness_reasons=reasons).finalise()
    return bundle, validation


def _source_summary(notes: list[EvidenceNote]) -> dict[str, Any]:
    documents, chunks, keys = set(), set(), set()
    for note in notes:
        for ref in note.evidence_refs:
            documents.add(ref.document_id)
            chunks.add(ref.chunk_id)
            if ref.source_key:
                keys.add(ref.source_key)
    return {"document_count": len(documents), "chunk_count": len(chunks),
            "source_key_count": len(keys), "documents": sorted(documents)}


def _coverage_summary(questions, results, notes) -> dict[str, Any]:
    status = {r["question_id"]: r["question_status"] for r in results}
    summary = {}
    for priority in PRIORITIES:
        group = [q for q in questions if q.priority == priority]
        answered = [q for q in group if status.get(q.question_id) == "answered"]
        summary[f"{priority}_total"] = len(group)
        summary[f"{priority}_answered"] = len(answered)
        summary[f"{priority}_resolution_rate"] = (round(len(answered) / len(group), 4)
                                                  if group else None)
    summary["generator_rejected"] = sum(1 for s in status.values() if s == "generator_rejected")
    summary["insufficient_evidence"] = sum(1 for s in status.values()
                                           if s == "insufficient_evidence")
    summary["note_count"] = len(notes)
    for support in notes_contract.SUPPORT_STATUSES:
        summary[f"notes_{support}"] = sum(1 for n in notes if n.support_status == support)
    for confidence in notes_contract.CONFIDENCES:
        summary[f"confidence_{confidence}"] = sum(1 for n in notes if n.confidence == confidence)
    summary["single_source_notes"] = sum(1 for n in notes if n.source_count == 1)
    summary["multi_source_notes"] = sum(1 for n in notes if n.source_count > 1)
    return summary


# ---------------------------------------------------------------- drafting interface

def draft_section(section_plan: SectionPlan, section_evidence_bundle: SectionEvidenceBundle):
    """Prose drafting interface. Deliberately not implemented in this phase.

    Drafting may only ever consume an approved SectionEvidenceBundle - never the raw corpus,
    unscoped retrieval, or model memory. It stays unimplemented until the evidence layer is proven:
    research decomposition, note reliability, ledger completeness and readiness must be trustworthy
    before model prose is introduced.
    """
    raise DraftingDisabled(
        "section drafting is not implemented in tunnelbook-book-writing-pipeline-v1; "
        "drafting_enabled=false")


def pipeline_identity() -> dict[str, Any]:
    return {"pipeline_version": PIPELINE_VERSION,
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "evidence_note_contract": notes_contract.CONTRACT_VERSION,
            "production_generator": production.VERSION,
            "source_policy": SOURCE_POLICY, "drafting_enabled": DRAFTING_ENABLED}


if __name__ == "__main__":
    print(json.dumps(pipeline_identity(), indent=2, ensure_ascii=False))
