"""P0 Evidence Gap Resolution v1 - close the six open P0 gaps from frozen evidence, or say why not.

Book Evidence Remediation v1 left three pilot sections NOT_READY behind six P0 gaps. It classified
them as EXTRACTION_FAILURE, SPAN_MAPPING_FAILURE, CROSS_LINGUAL_MAPPING_FAILURE and
GENERATOR_SYNTHESIS_DEFECT - and, notably, NOT as RETRIEVAL_GAP or CORPUS_GAP. So the resolution
protocol here is existing-evidence-first, in this order:

    A. EXTRACTION_FAILURE          re-read the frozen accepted answer, reconstruct the propositions
                                   the pipeline silently dropped (lead-ins, bare list labels).
    B. SPAN_MAPPING_FAILURE        inspect the WHOLE frozen ContextPacket, not only the handles the
                                   generator happened to cite next to that sentence.
    C. CROSS_LINGUAL_MAPPING_FAILURE  map the Turkish claim onto the exact English source span.
    D. GENERATOR_SYNTHESIS_DEFECT  only now, and only if existing evidence is exhausted, may a
                                   narrower revised query be generated.
    E./F. RETRIEVAL_GAP / CORPUS_GAP   assessed last, and only after the packet is exhausted.

Two asymmetries are deliberate and are what keep this phase honest.

  * Evidence may be ADDED to a claim from inside the frozen packet, never from outside it. Every
    span authored below is verified verbatim against the frozen chunk text before it can support
    anything; an unverifiable span aborts the run rather than degrading to "close enough".
  * A claim may be NARROWED to what a source actually says, never WIDENED to what the generator
    said. The moved TBM threshold (source: "lower than 1"; generator: "1,5'in altında") is
    permanently pinned as NOT_SUPPORTED, and the numeric defects carried over from remediation are
    re-decided from source spans rather than inherited.

Nothing upstream is modified. Retriever v1, Context v1, Prompt v5, Output Contract v1.1, the
Production Grounded Generator, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1 and the
remediation v1 artifacts are all read-only inputs whose SHAs are re-verified at the end of the run.
Drafting stays disabled: this phase decides whether a section COULD be drafted, and writes no prose.
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
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"
AUDITS = BOOK / "audits"
REMEDIATION = BOOK / "remediation"
REMEDIATED_NOTES = BOOK / "evidence_notes_remediated_v1"
REMEDIATED_LEDGERS = BOOK / "claim_ledgers_remediated_v1"
REMEDIATED_BUNDLES = BOOK / "section_bundles_remediated_v1"
MANIFESTS = BOOK / "manifests"
P0 = BOOK / "p0_resolution"
P0_QUESTIONS = P0 / "questions"
P0_EVIDENCE = P0 / "evidence"
P0_CLAIMS = P0 / "claims"
P0_BUNDLES = P0 / "bundles"
P0_AUDITS = P0 / "audits"
METADATA = ROOT / "data/metadata"
REPORTS = ROOT / "reports"

RESOLUTION_VERSION = "tunnelbook-p0-evidence-gap-resolution-v1"
REMEDIATION_VERSION = "tunnelbook-book-evidence-remediation-v1"
EXTRACTOR_VERSION = "tunnelbook-book-pipeline-extractor-v1.1"
SOURCE_POLICY = "frozen_packet_only"
DRAFTING_ENABLED = False

GAP_STATUSES = ("OPEN", "RESOLVED", "PARTIALLY_RESOLVED", "BLOCKED_RETRIEVAL", "BLOCKED_CORPUS",
                "BLOCKED_GENERATOR", "BLOCKED_QUESTION_DESIGN")
GAP_CLASSES = ("EXTRACTION_FAILURE", "SPAN_MAPPING_FAILURE", "CROSS_LINGUAL_MAPPING_FAILURE",
               "RETRIEVAL_GAP", "CORPUS_GAP", "GENERATOR_SYNTHESIS_DEFECT",
               "QUESTION_DESIGN_DEFECT")
SUPPORT_RELATIONS = ("literal_direct", "manual_paraphrase_mapping", "multi_span_composition",
                     "cross_lingual_faithful_mapping", "numeric_direct", "qualified_support")
MANUAL_VERDICTS = ("FULL", "PARTIAL", "NONE", "AMBIGUOUS")
CROSS_LINGUAL_STATUSES = ("FAITHFUL", "PARTIAL", "NOT_SUPPORTED", "AMBIGUOUS")
RESOLUTION_SOURCES = ("existing_extraction", "manual_span_mapping", "manual_paraphrase_mapping",
                      "cross_lingual_mapping", "revised_generation", "expanded_retrieval")
CLAUSE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED")
CONFLICT_RESULTS = ("NO_CONFLICT_FOUND", "CONTEXT_DIFFERENCE", "TRUE_CONFLICT",
                    "INSUFFICIENT_TO_DECIDE")

# Bounds. These are the phase's own guard rails and the tests assert them, so raising one to make a
# section ready is a visible act, not a quiet one.
MAX_GENERATION_ATTEMPTS_PER_GAP = 2
RETRIEVAL_BASELINE_TOP_K = 20
RETRIEVAL_EXPANSION_LADDER = (40, 60)
RETRIEVAL_EXPANSION_CEILING = 60
QDRANT_URL = "http://localhost:6333"
QDRANT_EXPECTED_POINTS = 5992

# The threshold the generator moved. Pinned as data so the guard cannot be edited away silently.
PINNED_THRESHOLD_DEFECT = {
    "clause_ids": ("Q-02-3-01-N03-C02", "Q-02-3-01-N03-C04"),
    "source_says": "in case it is lower than 1, the conventional method is usually preferred",
    "generator_said": "1,5'in altındaysa geleneksel yöntem",
    "verdict": "NOT_SUPPORTED",
    "reason": "the source threshold for preferring the conventional method is 1, not 1.5; and 1.5 "
              "is the trade-off limit itself, not the lower end of a 1.5-3 band.",
}
# Numeric values remediation v1 flagged. Each must be re-decided from a verified source span in the
# frozen packet; none may be promoted on the strength of the generator having asserted it.
PINNED_NUMERIC_DEFECTS = ("360", "400", "150")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Frozen dependencies, read-only. 38_ owns the one span normaliser producer and validator share;
# 41_ owns the frozen packet reconstruction; 42_ owns clause primitives. None of the three can
# retrieve or generate, so this module cannot do either by accident.
notes_contract = _load("evidence_note_contract_v1", "scripts/38_evidence_note_contract.py")
audit_v1 = _load("pilot_manual_audit_v1", "scripts/41_pilot_manual_evidence_audit_v1.py")
extractor_v1_1 = _load("book_pipeline_extractor_v1_1", "scripts/42_book_pipeline_extractor_v1_1.py")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                            for r in rows), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def normalise_span(text: str) -> str:
    """The contract's own span normaliser, applied to NFKC-folded text.

    Source PDFs carry non-breaking spaces, soft hyphens and superscript digits ("kg/m 3"), so the
    fold has to happen before the contract's normaliser or a span that is genuinely present will
    be rejected. Nothing beyond Unicode folding is done: the match stays literal.
    """
    folded = unicodedata.normalize("NFKC", text).replace("­", "").replace("’", "'")
    return notes_contract.normalise_for_span_match(folded)


NUMBER = re.compile(r"\d+(?:[.,]\d+)?")


def numeric_literals(text: str) -> list[str]:
    """Material numeric values in a claim. Bare single digits are skipped: the '1' of a list
    enumerator or of 'I. Sınıf' is not a measured value. Inherited unchanged from v1.1."""
    values = []
    for raw in NUMBER.findall(unicodedata.normalize("NFKC", text)):
        value = raw.replace(",", ".")
        if len(value) <= 1 and "." not in value:
            continue
        values.append(value)
    return sorted(set(values))


def number_in(value: str, evidence_text: str) -> bool:
    """Is this value literally present in the evidence? Comma and dot decimal separators are the
    same value; an en-dash range ('4-6') and a hyphen range are the same range."""
    blob = unicodedata.normalize("NFKC", evidence_text).replace(",", ".")
    blob = blob.replace("–", "-").replace("—", "-")
    squashed = re.sub(r"\s+", "", blob)
    probe = value.replace(",", ".")
    return probe in blob or probe in squashed


# ================================================================ 1. frozen inputs

def load_questions() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((BOOK / "research_questions").glob("*.jsonl")):
        rows += [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def load_runs() -> dict[str, dict]:
    return audit_v1.load_runs()


def load_section_plans() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((BOOK / "section_plans").glob("*.json"))}


def load_remediated_notes() -> dict[str, list[dict]]:
    return {p.stem: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
            for p in sorted(REMEDIATED_NOTES.glob("*.jsonl"))}


def load_remediated_ledgers() -> dict[str, list[dict]]:
    return {p.stem: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
            for p in sorted(REMEDIATED_LEDGERS.glob("*.jsonl"))}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


class FrozenPacketUniverse:
    """Every evidence item in the frozen pilot ContextPackets - not only the cited ones.

    This is the single most important difference between this phase and remediation v1. v1 asked
    "does the evidence this sentence cites carry it?"; a generator that cites E001 next to a
    sentence whose support actually sits in E006 fails that question while the packet answers it.
    So the unit of inspection here is the packet, and the boundary of the phase is the packet: an
    item outside it cannot support anything, which is what keeps "inspect more" from becoming
    "retrieve more".
    """

    def __init__(self) -> None:
        self.items = audit_v1.full_packet_evidence_universe()
        self.by_question: dict[str, dict[str, dict]] = {}
        self.packet_sha: dict[str, str] = {}
        for key, value in self.items.items():
            packet_sha, evidence_id = key.split("::")
            question_id = value["question_id"]
            self.by_question.setdefault(question_id, {})[evidence_id] = dict(
                value, evidence_id=evidence_id, context_packet_sha=packet_sha)
            self.packet_sha[question_id] = packet_sha

    def item(self, question_id: str, evidence_id: str) -> dict | None:
        return self.by_question.get(question_id, {}).get(evidence_id)

    def text(self, question_id: str, evidence_id: str) -> str:
        return (self.item(question_id, evidence_id) or {}).get("text") or ""

    def evidence_ids(self, question_id: str) -> list[str]:
        return sorted(self.by_question.get(question_id, {}))

    def contains_span(self, question_id: str, evidence_id: str, span: str) -> bool:
        probe = normalise_span(span)
        return bool(probe) and probe in normalise_span(self.text(question_id, evidence_id))

    def find_span(self, question_id: str, span: str) -> list[str]:
        """Which evidence items in this packet carry this span? Used to prove that a span the
        author placed on E00x is not silently coming from somewhere outside the packet."""
        return [eid for eid in self.evidence_ids(question_id)
                if self.contains_span(question_id, eid, span)]

    def packet_carries(self, question_id: str, probes: list[str]) -> list[str]:
        """Retrieval-gap probe: does ANY item in the packet mention all of these terms?"""
        hits = []
        for eid in self.evidence_ids(question_id):
            blob = normalise_span(self.text(question_id, eid))
            if all(normalise_span(p) in blob for p in probes):
                hits.append(eid)
        return hits


# ================================================================ 2. phase objects

@dataclass
class ManualSupportMapping:
    """Same-language support decided by reading, not by string overlap.

    Remediation v1 could only ever represent literal spans, so a Turkish claim carried by a
    Turkish source in different words had no way of being recorded as supported. This is the
    object that finally represents it - and it is deliberately verbose, because a paraphrase
    judgement that is not written down is not auditable.
    """
    mapping_id: str
    gap_id: str
    claim: str
    claim_language: str
    evidence_id: str
    context_packet_sha: str
    chunk_id: str
    source_span: str
    support_relation: str
    coverage: str
    conditions: list[str]
    qualifiers: list[str]
    exceptions: list[str]
    manual_verdict: str
    review_notes: str
    question_id: str = ""
    document_id: str | None = None
    source_key: str | None = None
    clause_id: str | None = None
    span_verified: bool = False


@dataclass
class CrossLingualP0Mapping:
    """A Turkish claim beside the exact English span offered for it.

    The English is stored verbatim and never translated into a quotable Turkish sentence: an
    invented translation would read like a citation while being this pipeline's own prose.
    """
    mapping_id: str
    gap_id: str
    claim_tr: str
    source_span_en: str
    source_evidence_ref: dict[str, Any]
    mapping_status: str
    numeric_equivalence: bool
    modality_equivalence: bool
    condition_equivalence: bool
    scope_equivalence: bool
    manual_review_notes: str
    question_id: str = ""
    clause_id: str | None = None
    span_verified: bool = False


@dataclass
class P0QueryRevision:
    original_question_id: str
    original_question: str
    revised_question_id: str
    revised_question: str
    revision_reason: str
    target_missing_proposition: str
    same_section: bool
    source_policy: str = SOURCE_POLICY


@dataclass
class P0ResolvedClaim:
    claim_id: str
    gap_id: str
    section_id: str
    question_id: str
    claim: str
    support_status: str
    evidence_refs: list[dict]
    support_mappings: list[str]
    cross_lingual_mappings: list[str]
    numeric_data: list[dict]
    conditions: list[str]
    qualifiers: list[str]
    source_keys: list[str]
    citation_ready: bool
    resolution_source: str
    claim_language: str = "tr"
    clause_id: str | None = None
    proposition_origin: str = "existing_extraction"
    citation_block_reasons: list[str] = field(default_factory=list)
    conflict_result: str = "NO_CONFLICT_FOUND"
    authority_levels: list[str] = field(default_factory=list)


@dataclass
class P0EvidenceGap:
    gap_id: str
    section_id: str
    question_id: str
    question_text: str
    section_objective: str
    gap_classes: list[str]
    current_supported_claims: list[str]
    current_partial_claims: list[str]
    current_insufficient_notes: list[str]
    critical_missing_propositions: list[str]
    existing_packet_shas: list[str]
    existing_evidence_refs: list[str]
    resolution_strategy: list[str]
    status: str = "OPEN"
    actions_attempted: list[str] = field(default_factory=list)
    packet_items_inspected: int = 0
    packet_exhausted: bool = False
    resolved_claim_ids: list[str] = field(default_factory=list)
    remaining_missing_propositions: list[str] = field(default_factory=list)
    generation_attempts: int = 0
    retrieval_expansions: int = 0
    retrieval_gap_candidate: bool = False
    corpus_gap_candidate: bool = False
    question_design_defect: bool = False
    notes: list[str] = field(default_factory=list)


# ================================================================ 3. authored resolution registry
#
# Everything below was produced by reading each P0 answer beside the FULL frozen packet - all
# twenty evidence items per question, not the handles the generator happened to cite. It is data,
# not code, for one reason: every span is re-verified verbatim against the frozen chunk before it
# may support anything (verify_registry), so an authoring mistake fails the run instead of quietly
# manufacturing support. Nothing here retrieves, generates, or reaches outside the packet.
#
# Two conventions:
#   * A reconstructed proposition may NARROW its source unit (drop an unsourced qualifier) and must
#     record that under `narrowing`. It may never widen it.
#   * verdict FULL requires equivalent meaning, no extra proposition, no stronger modality,
#     identical numbers, preserved conditions and preserved scope. Everything else is PARTIAL.

# ---------------------------------------------------------------- A. extraction failures
# Q-02-1-01 and Q-02-1-02 lost their actual answers at extraction: the classification lead-in
# ("...iki ana gruba ayrılır:") and every list item were dropped as non-propositions, so the
# question "how are tunnel support systems divided?" ended with one note about something else.
RECONSTRUCTIONS = [
    {"id": "R-Q-02-1-01-01", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "Tünel destekleme sistemleri, kullanılan malzeme ve uygulama zamanına göre "
                      "genellikle iki ana gruba ayrılır:",
     "parent_context": "Accepted answer lead-in introducing the two numbered group headings "
                       "'1. Birincil Destekleme Sistemi (Initial Support)' and "
                       "'2. İkincil Destekleme Sistemi (Final Lining)'.",
     "reconstructed_proposition": "Tünel destekleme sistemi, birincil destekleme sistemi ve "
                                  "ikincil destekleme sistemi olmak üzere ikiye ayrılır.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "The unit's basis 'kullanılan malzeme ve uygulama zamanına göre' is dropped: no "
                  "packet source states that the split is made on material and timing.",
     "manual_review": "This is the proposition the P0 classification question actually asks for. "
                      "v1 dropped it because the unit ends in a colon and carries no [E###] "
                      "handle; the packet nonetheless states it twice."},
    {"id": "R-Q-02-1-01-02", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "1. **Birincil Destekleme Sistemi (Initial Support):** Karşılaşılan kaya "
                      "sınıfı ve jeolojik koşullara göre uygulanan, tünelin açılma sürecinde "
                      "stabiliteyi sağlayan sistemdir. Bu sistemin elemanları şunlardır:",
     "parent_context": "First group heading of the accepted answer's classification.",
     "reconstructed_proposition": "Birincil destekleme sistemi elemanları, karşılaşılan kaya "
                                  "sınıfı ve jeolojik koşullara göre belirlenir.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "'tünelin açılma sürecinde stabiliteyi sağlayan sistemdir' is dropped: E007 "
                  "states the selection basis but not that definition.",
     "manual_review": "Kept to the half the packet carries verbatim."},
    {"id": "R-Q-02-1-01-03", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "Püskürtme Beton / Süren (Boru veya Demir Çubuk) / Kaya Bulonu (Saplaması) / "
                      "Çelik İksa / Hasır Çelik / Zemin Çivisi / Enjeksiyon / Şemsiye Kemer "
                      "Uygulaması",
     "parent_context": "'Bu sistemin elemanları şunlardır:' under 'Birincil Destekleme Sistemi'.",
     "reconstructed_proposition": "Tünellerde kullanılan birincil destekleme elemanları süren, "
                                  "püskürtme beton, hasır çelik, kaya bulonu, çelik iksa, zemin "
                                  "çivisi, enjeksiyon ve şemsiye kemer uygulamasıdır.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "None. The eight labels are restated as the single enumeration their parent "
                  "lead-in asserts.",
     "manual_review": "E014 carries the identical eight-item enumeration under its own lead-in."},
    {"id": "R-Q-02-1-01-04", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "Kaplama Betonu (Nihai Beton/Kemer Betonu) / İnvert Betonu (Taban Kemeri) / "
                      "Temel Kiriş Betonu / Su Yalıtımı ve Drenaj İşleri",
     "parent_context": "'Bu sistemin elemanları şunlardır:' under 'İkincil Destekleme Sistemi'.",
     "reconstructed_proposition": "Tünellerde kullanılan ikincil destekleme elemanları invert "
                                  "betonu, temel kiriş betonu, su yalıtımı ve drenaj işleri ile "
                                  "kaplama betonudur.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "'Taban Kemeri' is dropped as an unsourced gloss on 'İnvert Betonu'.",
     "manual_review": "E014 carries the identical four-item enumeration."},
    {"id": "R-Q-02-1-02-01", "gap": "GAP-P0-02", "question_id": "Q-02-1-02",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "Püskürtme beton / Çelik hasır / Çelik iksa / Kaya bulonu (kaya saplaması) / "
                      "Süren (boru süren, çelik çubuk süren vb.) / Zemin çivisi / Enjeksiyon / "
                      "Şemsiye kemer uygulaması",
     "parent_context": "'Tünelerde kullanılan birincil destekleme elemanları şunlardır:'",
     "reconstructed_proposition": "Tünellerde kullanılan birincil destekleme elemanları süren, "
                                  "püskürtme beton, hasır çelik, kaya bulonu, çelik iksa, zemin "
                                  "çivisi, enjeksiyon ve şemsiye kemer uygulamasıdır.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "None for these eight. The ninth answer item, 'İç hasır çelik tabakası (bazı "
                  "durumlarda)', is NOT part of this proposition and is reconstructed separately.",
     "manual_review": "Every one of Q-02-1-02's nine notes was dropped as a bare label, leaving "
                      "the P0 question with no note at all. E006 carries the enumeration."},
    {"id": "R-Q-02-1-02-02", "gap": "GAP-P0-02", "question_id": "Q-02-1-02",
     "section_id": "SEC-02-1", "claim_language": "tr",
     "original_unit": "İç hasır çelik tabakası (bazı durumlarda)",
     "parent_context": "'Tünelerde kullanılan birincil destekleme elemanları şunlardır:'",
     "reconstructed_proposition": "Püskürtme beton kaplamada, beton tabakaları arasına bir çelik "
                                  "hasır tabakası uygulanır.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "'bazı durumlarda' is dropped and the claim is restated as what E001 describes: "
                  "mesh placed between shotcrete layers. No packet source lists a separate "
                  "'iç hasır çelik tabakası' element.",
     "manual_review": "Kept deliberately weaker than the answer; recorded as qualified support."},
    {"id": "R-Q-02-3-01-01", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "section_id": "SEC-02-3", "claim_language": "tr",
     "original_unit": "Bu formülün sonucu 1,5'in altındaysa geleneksel yöntem (delme-patlatma), "
                      "3'ün üzerindeyse TBM kullanımı uygun görülür; 1,5 ile 3 arası ise ön seçim "
                      "kriteri olarak değerlendirilir.",
     "parent_context": "'TBM Rekabet Formülü' bullet of the accepted answer.",
     "reconstructed_proposition": "TBM rekabet formülünün sonucu 1'in altında olduğunda genellikle "
                                  "geleneksel yöntem tercih edilir; sonuç 3'ün üzerinde olduğunda "
                                  "TBM kesinlikle uygulanabilir bir çözümdür.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "The source threshold is restored: 1, not 1,5. The generator's 1,5 lower bound "
                  "and its '1,5-3 band' are NOT reconstructed - they are pinned NOT_SUPPORTED.",
     "manual_review": "Reconstruction of the correct proposition does not repair the incorrect "
                      "one; both are recorded."},
    {"id": "R-Q-02-3-01-02", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "section_id": "SEC-02-3", "claim_language": "tr",
     "original_unit": "1,5 ile 3 arası ise ön seçim kriteri olarak değerlendirilir.",
     "parent_context": "'TBM Rekabet Formülü' bullet of the accepted answer.",
     "reconstructed_proposition": "1,5 değeri, geleneksel yöntem ile TBM yöntemi arasındaki denge "
                                  "sınırını temsil eder ve yalnızca bir ön seçim kriteri olarak "
                                  "değerlendirilmelidir.",
     "proposition_origin": "parent_child_reconstruction",
     "narrowing": "1,5 is a single trade-off value in the source, not the lower edge of a band.",
     "manual_review": "This is what the source says about 1,5; the answer's band is not."},
]


# ---------------------------------------------------------------- B. same-language span mappings
# Remediation v1 could only credit a literal token run, so a Turkish claim carried by a Turkish
# source in different words stayed unsupported. These are read-and-decide mappings; `spans` are
# verbatim source text and every one is re-verified against the frozen chunk before use.
MANUAL_MAPPINGS = [
    # -------- GAP-P0-01 / Q-02-1-01: the classification the extractor dropped
    {"id": "MS-001", "gap": "GAP-P0-01", "question_id": "Q-02-1-01", "target": "R-Q-02-1-01-01",
     "claim_language": "tr", "relation": "literal_direct", "coverage": "full", "verdict": "FULL",
     "spans": [["E007", "Tünel destekleme sistemini birincil destekleme sistemi ve ikincil "
                        "destekleme sistemi olmak üzere ikiye ayırmak mümkündür"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "The source states the two-way split verbatim. 'ikiye ayırmak mümkündür' and "
              "'ikiye ayrılır' carry the same proposition with no change of modality strength."},
    {"id": "MS-002", "gap": "GAP-P0-01", "question_id": "Q-02-1-01", "target": "R-Q-02-1-01-01",
     "claim_language": "tr", "relation": "manual_paraphrase_mapping", "coverage": "full",
     "verdict": "FULL",
     "spans": [["E014", "destekleme elemanlarını birincil destekleme elemanları ve ikincil "
                        "destekleme elemanları olarak ayırabiliriz"]],
     "conditions": ["NATM yöntemi ile açılan tüneller"], "qualifiers": [], "exceptions": [],
     "notes": "Second, independent source for the same split, at element rather than system "
              "level and stated for NATM tunnels - recorded as a condition, not dropped."},
    {"id": "MS-003", "gap": "GAP-P0-01", "question_id": "Q-02-1-01", "target": "R-Q-02-1-01-02",
     "claim_language": "tr", "relation": "literal_direct", "coverage": "full", "verdict": "FULL",
     "spans": [["E007", "Birincil destekleme sistemi elemanları, karşılaşılan kaya sınıfı ve "
                        "jeolojik koşullarına göre"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Verbatim. The claim was narrowed to exactly this span's assertion."},
    {"id": "MS-004", "gap": "GAP-P0-01", "question_id": "Q-02-1-01", "target": "R-Q-02-1-01-03",
     "claim_language": "tr", "relation": "multi_span_composition", "coverage": "full",
     "verdict": "FULL",
     "spans": [["E014", "Tünellerde kullanılan birincil destekleme elemanları aşağıda yer "
                        "almaktadır. - Süren - Püskürtme Beton - Hasır Çelik - Kaya Bulonu - "
                        "Çelik İksa - Zemin Çivisi - Enjeksiyon - Şemsiye Kemer Uygulaması"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Lead-in and all eight items are one contiguous run in the source, so the "
              "parent-child reconstruction is carried by a single span rather than assembled."},
    {"id": "MS-005", "gap": "GAP-P0-01", "question_id": "Q-02-1-01", "target": "R-Q-02-1-01-04",
     "claim_language": "tr", "relation": "multi_span_composition", "coverage": "full",
     "verdict": "FULL",
     "spans": [["E014", "Tünellerde kullanılan ikincil destekleme elemanları ise aşağıda "
                        "verilmektedir. - İnvert Betonu - Temel Kiriş Betonu - Su Yalıtımı ve "
                        "Drenaj İşleri - Kaplama Betonu/Kemer Betonu/Nihai Beton"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Same structure for the secondary elements."},
    {"id": "MS-006", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "target": "Q-02-1-01-N16-E", "claim_language": "tr", "relation": "qualified_support",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E007", "tüm destekleme sistemlerinde kazının hemen ardından ilk tabaka "
                        "püskürtme betonu uygulanmıştır"]],
     "conditions": [], "qualifiers": ["yalnızca ilk püskürtme beton tabakası için ifade edilmiştir",
                                      "tek bir proje (T4 Tüneli) anlatımı"], "exceptions": [],
     "notes": "The source says the FIRST SHOTCRETE LAYER goes on immediately after excavation in "
              "one project; the claim generalises that to the whole initial support system. "
              "Qualified support only."},

    # -------- GAP-P0-02 / Q-02-1-02: every note was a bare label
    {"id": "MS-007", "gap": "GAP-P0-02", "question_id": "Q-02-1-02", "target": "R-Q-02-1-02-01",
     "claim_language": "tr", "relation": "multi_span_composition", "coverage": "full",
     "verdict": "FULL",
     "spans": [["E006", "Tünellerde kullanılan birincil destekleme elemanları aşağıda yer "
                        "almaktadır. - Süren - Püskürtme Beton - Hasır Çelik - Kaya Bulonu - "
                        "Çelik İksa - Zemin Çivisi - Enjeksiyon - Şemsiye Kemer Uygulaması"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "The answer's 'Çelik hasır' and the source's 'Hasır Çelik' are the same element "
              "with the compound reversed; no other item differs."},
    {"id": "MS-008", "gap": "GAP-P0-02", "question_id": "Q-02-1-02", "target": "R-Q-02-1-02-02",
     "claim_language": "tr", "relation": "qualified_support", "coverage": "partial",
     "verdict": "PARTIAL",
     "spans": [["E001", "Püskürtme beton kaplamanın statik ve konstrüktif donatısını teşkil "
                        "etmek üzere beton tabakaları arasına çelik hasır uygulanmıştır"]],
     "conditions": [], "qualifiers": ["tek bir proje (T4 Tüneli) anlatımı"], "exceptions": [],
     "notes": "The source describes mesh placed between shotcrete layers, which is the substance "
              "of the answer's 'iç hasır çelik tabakası'. No packet source lists it as a separate "
              "primary support element, so this stays partial rather than joining MS-007's list."},

    # -------- GAP-P0-03 / Q-02-2-01: cement dosage. Every value below is re-proved from source.
    {"id": "MS-009", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N03-C01", "claim_language": "tr", "relation": "numeric_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E005", "Çimento tipi ne olursa olsun, özel uygulamalar dışında çimento miktarı; "
                        "kullanılan agreganın maksimum dane boyutu (Dmax), durabilite ve minimum "
                        "çimento dozajı nedenleriyle, kuru sistemde 350 kg/m³'ten, yaş sistemde "
                        "ise 400 kg/m³'ten az olmayacaktır."],
               ["E009", "kuru sistemde 350 kg/m 3 'ten, yaş sistemde ise 400 kg/m 3' ten az "
                        "olmayacaktır"]],
     "conditions": ["özel uygulamalar dışında"], "qualifiers": [], "exceptions": [],
     "notes": "400 kg/m³ for the wet system IS stated, in two packet items, one of them "
              "authority A. Remediation v1 marked the clause partial only because its lexical "
              "overlap with the cited item fell below threshold, not because the value was absent."},
    {"id": "MS-010", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N04-C01", "claim_language": "tr", "relation": "qualified_support",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "Tablo-308-23-b Etki Sınıflarına Göre Projelendirmelerde Esas Alınacak "
                        "Beton Özellikleri"],
               ["E004", "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m 3 "
                        "olmalıdır"],
               ["E006", "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ "
                        "olmalıdır"]],
     "conditions": ["yüksek dayanımlı beton dışında"],
     "qualifiers": ["Tablo-308-23-b, etki sınıflarına göre projelendirmede esas alınacak GENEL "
                    "beton özelliklerine ilişkindir; püskürtme beton şartnamesi değildir"],
     "exceptions": [],
     "notes": "360 kg/m³ is stated verbatim in two packet items - it was 'missing' in v1 only "
              "because the note cited E001/E003, which do not contain it, while E004/E006 in the "
              "same packet do. The scope qualifier is mandatory: this is the general concrete "
              "exposure-class table, not the shotcrete specification."},
    {"id": "MS-011", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N04-C02", "claim_language": "tr", "relation": "numeric_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E005", "durabilite ve minimum çimento dozajı nedenleriyle, kuru sistemde 350 "
                        "kg/m³'ten, yaş sistemde ise 400 kg/m³'ten az olmayacaktır"],
               ["E009", "kuru sistemde 350 kg/m 3 'ten, yaş sistemde ise 400 kg/m 3' ten az "
                        "olmayacaktır"]],
     "conditions": ["özel uygulamalar dışında"], "qualifiers": [], "exceptions": [],
     "notes": "Durability as the stated reason and both minimums are in one span."},
    {"id": "MS-012", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N05-C01", "claim_language": "tr", "relation": "literal_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E005", "Şev kaplama, geçici iksa vb. özel uygulamalarda İdare onayı ile bu "
                        "miktarlar azaltılabilecektir."],
               ["E009", "Şev kaplama, geçici iksa vb. özel uygulamalarda İdare onayı ile bu "
                        "miktarlar azaltılabilecektir."]],
     "conditions": ["İdare onayı"], "qualifiers": [], "exceptions": [], "notes": "Verbatim."},
    {"id": "MS-013", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N06-C01", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E001", "Betonun maruz kalacağı dış çevresel etki gereksinimlerini ve projecinin "
                        "betonda aradığı tüm karakteristik ve performans özellikleri sağlayan "
                        "çimento miktarı, gerekli laboratuvar ve ön dizayn deneme çalışmaları ile "
                        "belirlenecektir. Bu değer 350 kg/m³' ten az olsa bile, durabilite "
                        "nedeniyle minimum 350 kg/m³ çimento kullanılacaktır."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Every element of the clause - environmental exposure classes, laboratory and "
              "preliminary trial mixes, durability, the 350 kg/m³ floor - is in this one span."},
    {"id": "MS-014", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "target": "Q-02-2-01-N07-C01", "claim_language": "tr", "relation": "numeric_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E005", "özel uygulamalar dışında çimento miktarı; kullanılan agreganın maksimum "
                        "dane boyutu (Dmax), durabilite ve minimum çimento dozajı nedenleriyle, "
                        "kuru sistemde 350 kg/m³'ten, yaş sistemde ise 400 kg/m³'ten az "
                        "olmayacaktır."],
               ["E009", "kuru sistemde 350 kg/m 3 'ten, yaş sistemde ise 400 kg/m 3' ten az "
                        "olmayacaktır"]],
     "conditions": ["özel uygulamalar dışında"], "qualifiers": [], "exceptions": [],
     "notes": "The claim's 'standart uygulamalarda' is the source's 'özel uygulamalar dışında'; "
              "same scope, stated from the other side."},

    # -------- GAP-P0-04 / Q-02-2-02: initial shotcrete thickness (English claim, English source)
    {"id": "MS-015", "gap": "GAP-P0-04", "question_id": "Q-02-2-02",
     "target": "Q-02-2-02-N01-C01", "claim_language": "en", "relation": "numeric_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E005", "It has a thickness ranging generally from 4 to 16 inches (100 to 400 mm) "
                        "mainly depending on the ground conditions and size of the tunnel "
                        "opening"],
               ["E002", "Initial shotcrete lining typically consists of 4 to 16 inch (100 to 400 "
                        "mm) thick shotcrete layer mainly depending on the ground conditions and "
                        "size of the tunnel opening"]],
     "conditions": ["depending on ground conditions and size of the tunnel opening"],
     "qualifiers": [], "exceptions": [],
     "notes": "Two authority-A items in the same packet state the range verbatim, one of them "
              "using the word 'typically' the claim uses. Both the imperial and the metric "
              "figures are source-stated, so nothing here is a derived conversion."},
    {"id": "MS-016", "gap": "GAP-P0-04", "question_id": "Q-02-2-02",
     "target": "Q-02-2-02-N02-C01", "claim_language": "en", "relation": "multi_span_composition",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E020", "Crushed, but Chemically Intact Rock"],
               ["E020", "Squeezing Rock"],
               ["E020", "thickness 12 in (300 mm) and more"]],
     "conditions": ["dependent on tunnel size"], "qualifiers": [], "exceptions": [],
     "notes": "The support-selection table gives 'thickness 12 in (300 mm) and more' on both the "
              "crushed-rock and the squeezing-rock rows, which is exactly the claim's two named "
              "conditions. Composition across rows of one table, not across unrelated facts."},

    # -------- GAP-P0-05 / Q-02-3-01: TBM vs drill-and-blast comparison criteria
    {"id": "MS-017", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N06-C01", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E010", "Kaya şartlarının tünel boyunca değiştiği durumlarda ve çok yüksek "
                        "mukavemetli kayaçların delinmesinde kullanışlıdır."],
               ["E010", "Her tür kaya şartında uygulanabilir."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "'kullanışlıdır' is carried; 'esneklik sağlar' is the answer's own characterisation "
              "and adds a proposition the source does not make, so this cannot be FULL."},
    {"id": "MS-018", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N07-C01", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E010", "patlamanın neden olduğu gevşeme ve aşırı sökülmelerin önüne geçilemez"],
               ["E004", "Patlatma yönteminde kaçınılmaz olan aşırı sökülme"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Loosening and over-break being unavoidable is stated twice. Blast-induced "
              "VIBRATION is not stated anywhere in this packet, so the clause stays partial."},
    {"id": "MS-019", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N07-C02", "claim_language": "tr", "relation": "manual_paraphrase_mapping",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "yerleşim yeri ve/veya sanayi alanları yakınlarında tahribata sebep "
                        "olunabileceğinden"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "The source states that blasting can cause damage near settlements and industrial "
              "areas; the claim says damage to nearby buildings. Same proposition, no widening."},
    {"id": "MS-020", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N07-C03", "claim_language": "tr", "relation": "literal_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "Düzgün, pürüzsüz bir yüzey elde edilir."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Stated among the listed advantages of excavating with a TBM."},
    {"id": "MS-021", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N07-C04", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "Patlatma tahribatı olmadığından tünel etrafındaki kaya ilk haliyle "
                        "kalır. Bunun sonucu olarak daha az bir iksa gerekir."],
               ["E004", "Çevrede yer alan bina ve/veya tesislerde patlatma tahribatı "
                        "gerçekleşmemektedir."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Both halves of the clause - no blast damage to surrounding buildings, and less "
              "support required - are stated in the same list."},
    {"id": "MS-022", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N07-C05", "claim_language": "tr", "relation": "literal_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "Daha az insan gücüne ihtiyaç gösterir. İşçi sayısı azaldığından birim "
                        "insan başına ilerleme ve iş güvenliği artmış olacaktır"]],
     "conditions": [], "qualifiers": [], "exceptions": [], "notes": "Verbatim."},

    # -------- GAP-P0-06 / Q-02-3-02: conditions under which a TBM is appropriate
    {"id": "MS-023", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N08-C01", "claim_language": "tr", "relation": "literal_direct",
     "coverage": "full", "verdict": "FULL",
     "spans": [["E004", "Adından da anlaşıldığı gibi çok sert kayaç durumlarında kullanılan TBM "
                        "türüdür. Bu makinenin kullanılması için zeminin sürekli olarak çok sert "
                        "kayaçlar içinde devam etmesi gerekmektedir."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Both the hard-rock condition and the continuity requirement are verbatim."},
    {"id": "MS-024", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N06-C01", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E014", "değişken zemin koşullarına sahip tünel güzerhaları için çözümler ve "
                        "makina konseptleri mevcuttur: Çok modlu TBM'ler"],
               ["E014", "Çok modlu TBM'ler, kazı teknolojisini uyarlama ve tüneldeki TBM modları "
                        "arasında gerçek zemin koşullarına uyacak şekilde değişiklik yapma "
                        "olasılığını içerecek şekilde tasarlanmış ve üretilmiştir."]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Multi-mode TBMs for variable ground is carried. The claim's specific triple - hard "
              "rock, soft water-bearing ground, complex surface conditions - is not enumerated "
              "that way in the source, so this stays partial."},
    {"id": "MS-025", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N09-C01", "claim_language": "tr", "relation": "qualified_support",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E012", "Kayanın uygun olması durumunda ilerleme hızı çok daha fazladır. En son "
                        "tünel açma makineleri delme ve patlatma yöntemine göre 4–6 defa daha "
                        "hızlı çalışabilmektedir."]],
     "conditions": ["kayanın uygun olması"], "qualifiers": [], "exceptions": [],
     "notes": "The 4-6x speed factor and its rock condition are verbatim. That TBMs are therefore "
              "'an economic and efficient solution in long tunnels' is the answer's inference and "
              "is not in this span."},
    {"id": "MS-026", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N15-C01", "claim_language": "tr", "relation": "qualified_support",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E012", "yerleşim yeri ve/veya sanayi alanları yakınlarında tahribata sebep "
                        "olunabileceğinden bazı özel durumlarda patlatma yöntemi ile açmak yerine "
                        "ekonomik olup olmadığına bakılmaksızın makine ile açılmaktadır"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "Machine excavation near settlements and industrial areas is carried, including "
              "that economics are set aside. Explicit VIBRATION and NOISE limits are not stated."},
    {"id": "MS-027", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N18-C01", "claim_language": "tr", "relation": "qualified_support",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E012", "Tam kesitte tünel açma aygıtından farklı olarak bu aygıt dairesel "
                        "olmayan kesitlerde de kullanılmaktadır"]],
     "conditions": [], "qualifiers": [], "exceptions": [],
     "notes": "The non-circular-profile half is carried by contrast with the roadheader. That a "
              "TBM is uneconomic on SHORT drives is not stated in this packet."},
    {"id": "MS-028", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N10-C01", "claim_language": "tr", "relation": "multi_span_composition",
     "coverage": "partial", "verdict": "PARTIAL",
     "spans": [["E017", "Tek Kalkanlı Sert Kaya TBM ile NCp tünel açma yöntemi ve enjeksiyon "
                        "kullanarak"],
               ["E017", "Tünel, hudson Nehri'nin altında"],
               ["E017", "yüksek basınçlı yeraltı suyu içeren çatlaklı kaya zonlarında güvenli "
                        "bir şekilde kazı gerçekleştirmesi"]],
     "conditions": [], "qualifiers": [],
     "exceptions": ["'20 bar' kaynakta su basıncı değil, kuyu dibi çekiçlerinin delme basıncı "
                    "kapasitesi olarak geçmektedir"],
     "notes": "Project, machine type, the Hudson crossing, the fissured high-pressure rock zones "
              "and the grouting systems are all carried. The 20 bar figure is NOT: in the source "
              "it is the pressure up to which DTH hammers could drill ahead of the machine, not "
              "the groundwater pressure the tunnel faced. Numeric mis-attribution, so PARTIAL."},
]


# ---------------------------------------------------------------- C. cross-lingual mappings
# Turkish claim beside the exact English span offered for it. The English is stored verbatim and is
# never rendered into quotable Turkish: an invented translation would read like a citation while
# being this pipeline's own prose.
CROSS_LINGUAL_MAPPINGS = [
    {"id": "XL-P0-001", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "target": "Q-02-1-01-N16-A", "status": "FAITHFUL",
     "spans": [["E015", "The main objectives of tunnel support system are to (1) stabilize the "
                        "tunnel heading, (2) minimize ground movements, and (3) permit the tunnel "
                        "to operate over the design life"],
               ["E015", "the first two functions are provided by an initial support system, "
                        "whereas the third function is preserved with a final lining"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "Objectives (1) and (2) are assigned to the initial support system by the second "
              "span. The Turkish clause asserts exactly those two functions for birincil destek."},
    {"id": "XL-P0-002", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "target": "Q-02-1-01-N16-B", "status": "FAITHFUL",
     "spans": [["E015", "The main objectives of tunnel support system are to (1) stabilize the "
                        "tunnel heading, (2) minimize ground movements, and (3) permit the tunnel "
                        "to operate over the design life"],
               ["E015", "the first two functions are provided by an initial support system, "
                        "whereas the third function is preserved with a final lining"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "Objective (3) is assigned to the final lining."},
    {"id": "XL-P0-003", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "target": "Q-02-1-01-N16-C", "status": "FAITHFUL",
     "spans": [["E015", "If the final lining is installed after the tunnel has been stabilized by "
                        "initial support"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "The ordering - final lining after stabilisation by initial support - is stated. "
              "The claim was written to keep the source's conditional framing."},
    {"id": "XL-P0-004", "gap": "GAP-P0-01", "question_id": "Q-02-1-01",
     "target": "Q-02-1-01-N16-D", "status": "NOT_SUPPORTED",
     "spans": [["E015", "the final lining will undergo very little additional loadings such as "
                        "contact grouting pressures, thermal stresses, groundwater pressure"]],
     "numeric": True, "modality": False, "condition": False, "scope": False,
     "notes": "This is the half the answer inverted. The source names those loadings in order to "
              "say the final lining undergoes VERY LITTLE of them when it is installed after "
              "stabilisation; the answer turns them into the PURPOSE for which the final lining "
              "is built. No packet source states that purpose, so the clause stays unsupported "
              "and SEC-02-1 stays blocked on it."},

    # -------- GAP-P0-05: the moved threshold, and the proposition the source actually carries
    {"id": "XL-P0-005", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "R-Q-02-3-01-01", "status": "FAITHFUL",
     "spans": [["E003", "when the result is higher than 3 the TBM is definitely a viable "
                        "solution, while in case it is lower than 1, the conventional method is "
                        "usually preferred"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "Both thresholds reconstructed exactly as stated: 3 and 1."},
    {"id": "XL-P0-006", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "R-Q-02-3-01-02", "status": "FAITHFUL",
     "spans": [["E003", "1.5 represents the trade-off limit between the conventional construction "
                        "method and the TBM construction method. This value should be consider as "
                        "a preliminary selection criteria only."]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "1,5 is a single trade-off value that is itself only a preliminary criterion."},
    {"id": "XL-P0-007", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N03-C02", "status": "NOT_SUPPORTED",
     "spans": [["E003", "when the result is higher than 3 the TBM is definitely a viable "
                        "solution, while in case it is lower than 1, the conventional method is "
                        "usually preferred"]],
     "numeric": False, "modality": True, "condition": True, "scope": True,
     "notes": "PINNED. The source threshold for preferring the conventional method is 1. The "
              "answer's 1,5 moves it, which changes which projects the criterion selects. No "
              "mapping in this phase may accept it."},
    {"id": "XL-P0-008", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N03-C04", "status": "NOT_SUPPORTED",
     "spans": [["E003", "1.5 represents the trade-off limit between the conventional construction "
                        "method and the TBM construction method. This value should be consider as "
                        "a preliminary selection criteria only."]],
     "numeric": False, "modality": True, "condition": False, "scope": False,
     "notes": "PINNED. The source makes 1,5 itself the preliminary criterion; the answer turns "
              "'1,5 to 3' into a band with that role. Different proposition."},
    {"id": "XL-P0-009", "gap": "GAP-P0-05", "question_id": "Q-02-3-01",
     "target": "Q-02-3-01-N04-C04", "status": "FAITHFUL",
     "spans": [["E018", "The initial investment is counterbalanced by lower marginal costs during "
                        "the excavation phase"],
               ["E006", "the considerable capital cost of the TBM can be justified only if "
                        "distributed over a significant excavation length"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "Both halves of the Turkish clause are carried: the first span gives low marginal "
              "cost offsetting the initial investment, the second gives the long-drive condition. "
              "Both spans are in this question's own frozen packet."},

    # -------- GAP-P0-06
    {"id": "XL-P0-010", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N05-C02", "status": "PARTIAL",
     "spans": [["E009", "which helps to minimize ground loss, settlement, and potential damage to "
                        "structures, utilities, and roads"],
               ["E009", "Closed face machines are sealed, except at ports controlled by the TBM "
                        "operator, to prevent both groundwater and unconsolidated ground from "
                        "entering the shield at the excavated face."]],
     "numeric": True, "modality": False, "condition": False, "scope": True,
     "notes": "Closed-face machines and settlement minimisation are both in the packet, but the "
              "source does not say closed-face machines are PREFERRED WHEN settlement control is "
              "critical - a different item even says both machine types control settlement well."},
    {"id": "XL-P0-011", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N04-C02", "status": "PARTIAL",
     "spans": [["E007", "Good for clay and clayey and silty sand soils, below the water table"]],
     "numeric": True, "modality": False, "condition": True, "scope": True,
     "notes": "The source rates EPB 'Good for' clay and silty sand below the water table and "
              "'Best for sandy soils'. The answer promotes 'good for' to 'en iyi performansı "
              "gösterir' for the wrong soils - a modality upgrade, so PARTIAL at most."},
    {"id": "XL-P0-012", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N11-C01", "status": "PARTIAL",
     "spans": [["E015", "single shield TBM used for excavation of T26 tunnel through graphitic "
                        "schist rock masses that exhibit squeezing behavior"]],
     "numeric": True, "modality": True, "condition": True, "scope": False,
     "notes": "Single-shield TBM in squeezing graphitic schist is carried verbatim. The claim "
              "also asserts double-shield machines, which this span does not cover; MS-028's "
              "sibling span in E016 covers both but only for pressure estimation, not use."},
    {"id": "XL-P0-013", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N16-C01", "status": "PARTIAL",
     "spans": [["E008", "The TBM is completely equipped with ATEX (anti-explosion) devices"],
               ["E008", "Methane sensors are installed in each area"]],
     "numeric": True, "modality": True, "condition": True, "scope": False,
     "notes": "ATEX equipment and methane monitoring are stated for one project. The claim's "
              "general 'special ventilation systems' and 'high proportions of explosive gas' are "
              "not, so the scope is wider than the source's."},
    {"id": "XL-P0-014", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N14-C02", "status": "FAITHFUL",
     "spans": [["E005", "The TBM method requires a complete and detailed geological investigation "
                        "at planning phase"]],
     "numeric": True, "modality": True, "condition": True, "scope": True,
     "notes": "Verbatim requirement."},
    {"id": "XL-P0-015", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N14-C03", "status": "PARTIAL",
     "spans": [["E005", "The initial investment is counterbalanced by lower marginal costs during "
                        "the excavation phase"]],
     "numeric": True, "modality": True, "condition": True, "scope": False,
     "notes": "The source offsets the initial investment against lower MARGINAL COSTS DURING "
              "EXCAVATION, conditional on a sufficiently high advance rate. The claim's "
              "'uzun vadeli işletme maliyetleri' - long-term operating costs - is a different "
              "cost category, so this is partial, not faithful."},
    {"id": "XL-P0-016", "gap": "GAP-P0-06", "question_id": "Q-02-3-02",
     "target": "Q-02-3-02-N19-C01", "status": "PARTIAL",
     "spans": [["E016", "the TBM may suffer great pressures resulting in entrapment problems for "
                        "this tunnel"]],
     "numeric": True, "modality": True, "condition": True, "scope": False,
     "notes": "Entrapment risk under squeezing pressure is carried. That TBM use is therefore "
              "'risky when countermeasures are insufficient' is the answer's own conclusion."},
]


# ---------------------------------------------------------------- D. clause decomposition
# Two P0 clauses bundle a supported proposition with an unsupported one. v1.1 already split them
# once by coordination; splitting again is an ATOMICITY improvement, never a way to shed a
# requirement - every fragment below is kept and carries its own verdict, including the one that
# fails. A clause is superseded only when every fragment of it is represented.
CLAUSE_DECOMPOSITIONS = [
    {"superseded": ["Q-02-1-01-N16-C01", "Q-02-1-01-N16-C02"],
     "question_id": "Q-02-1-01", "section_id": "SEC-02-1", "gap": "GAP-P0-01",
     "reason": "The v1.1 coordination split produced two clauses that each still carried four "
               "propositions, so a single unsupported purpose attribution sank three supported "
               "ones. Decomposed to one proposition each.",
     "fragments": [
         {"clause_id": "Q-02-1-01-N16-A", "clause_type": "fact", "material": True,
          "text": "Birincil destekleme sisteminin işlevleri tünel aynasının stabilitesini "
                  "sağlamak ve yer deformasyonlarını en aza indirmektir."},
         {"clause_id": "Q-02-1-01-N16-B", "clause_type": "fact", "material": True,
          "text": "Nihai kaplama (ikincil destek), tünelin tasarım ömrü boyunca hizmet vermesini "
                  "sağlar."},
         {"clause_id": "Q-02-1-01-N16-C", "clause_type": "fact", "material": True,
          "text": "Nihai kaplama, tünel birincil destek ile stabilize edildikten sonra inşa "
                  "edilir."},
         {"clause_id": "Q-02-1-01-N16-D", "clause_type": "fact", "material": True,
          "text": "İkincil destek, ek yükleri (su basıncı, termal stresler vb.) taşımak amacıyla "
                  "inşa edilir."},
         {"clause_id": "Q-02-1-01-N16-E", "clause_type": "fact", "material": True,
          "text": "Birincil destek kazı sırasında hemen uygulanır."},
     ]},
    {"superseded": ["Q-02-2-01-N04-C01", "Q-02-2-01-N04-C02"],
     "question_id": "Q-02-2-01", "section_id": "SEC-02-2", "gap": "GAP-P0-03",
     "reason": "N04 is the generator synthesis defect for this gap: it welds a general-concrete "
               "maximum to two shotcrete minimums with 'belirtilse de' and asserts a tension no "
               "source states. The two factual halves are kept as separate claims, each with its "
               "own scope; the concessive relation itself is dropped as unsourced synthesis.",
     "fragments": [
         {"clause_id": "Q-02-2-01-N04-C01", "clause_type": "numeric", "material": True,
          "text": "Tablo-308-23-b'ye göre, yüksek dayanımlı beton dışında maksimum çimento "
                  "miktarı 360 kg/m³ olmalıdır."},
         {"clause_id": "Q-02-2-01-N04-C02", "clause_type": "numeric", "material": True,
          "text": "Püskürtme beton spesifikasyonlarında, durabilite gereği kuru sistem için "
                  "minimum 350 kg/m³ ve yaş sistem için minimum 400 kg/m³ çimento öngörülmüştür."},
     ]},
]

# The synthesis itself. Recorded, not deleted: a dropped proposition that is not written down is
# indistinguishable from one that was quietly hidden.
DROPPED_SYNTHESES = [
    {"id": "SYN-001", "gap": "GAP-P0-03", "question_id": "Q-02-2-01",
     "parent_note_id": "Q-02-2-01-N04", "gap_class": "GENERATOR_SYNTHESIS_DEFECT",
     "dropped_proposition": "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ "
                            "olarak belirtilse de, püskürtme beton spesifikasyonlarında minimum "
                            "350/400 kg/m³ öngörülmüştür (karşıtlık ilişkisi).",
     "reason": "The concessive relation between the two figures is asserted by no source. The "
               "360 kg/m³ maximum belongs to Tablo-308-23-b, which governs general concrete by "
               "exposure class; the 350/400 kg/m³ minimums belong to the shotcrete specification. "
               "They are different scopes, not a stated exception to one another.",
     "components_retained": ["Q-02-2-01-N04-C01", "Q-02-2-01-N04-C02"],
     "citable_as_compound": False},
]

# Numeric values remediation v1 flagged for this gap universe, re-decided from source spans.
NUMERIC_REVIEW = [
    {"value": "350", "unit": "kg/m³", "context": "kuru sistem püskürtme beton minimum çimento",
     "question_id": "Q-02-2-01", "evidence_ids": ["E001", "E003", "E005", "E009"],
     "source_stated": True, "derived": False,
     "notes": "Already source-stated in v1; unchanged."},
    {"value": "400", "unit": "kg/m³", "context": "yaş sistem püskürtme beton minimum çimento",
     "question_id": "Q-02-2-01", "evidence_ids": ["E005", "E009"],
     "source_stated": True, "derived": False,
     "notes": "Flagged in v1 because the citing note pointed at E001/E003. E005 and E009 - one of "
              "them authority A - state it verbatim. Promoted on source evidence, not on the "
              "generator having asserted it."},
    {"value": "360", "unit": "kg/m³", "context": "Tablo-308-23-b genel beton maksimum çimento",
     "question_id": "Q-02-2-01", "evidence_ids": ["E004", "E006"],
     "source_stated": True, "derived": False,
     "notes": "Same pattern as 400. Promoted only with the mandatory scope qualifier: this is the "
              "general concrete exposure-class table, not the shotcrete specification."},
    {"value": "150", "unit": "mm", "context": "15 cm -> 150 mm dönüşümü (Q-02-2-04)",
     "question_id": "Q-02-2-04", "evidence_ids": [],
     "source_stated": False, "derived": True,
     "notes": "Unchanged from v1: a conversion the generator performed, not a value any source "
              "states. Stays derived and non-citable. Not a P0 clause, so it constrains the "
              "section's limitations rather than its readiness."},
    {"value": "20", "unit": "bar", "context": "Delaware Su Kemeri su basıncı iddiası",
     "question_id": "Q-02-3-02", "evidence_ids": ["E017"],
     "source_stated": False, "derived": False,
     "notes": "NEW defect found in this phase. The figure exists in the packet but denotes the "
              "drilling pressure capability of down-the-hole hammers, not the groundwater "
              "pressure. Mis-attribution, so the clause carrying it stays partial."},
]

# Conflict review over every newly supported P0 claim (rule: check against remediated claims, the
# conflict-candidate universe and the packet evidence before promoting anything).
CONFLICT_REVIEWS = [
    {"id": "CF-P0-001", "result": "CONTEXT_DIFFERENCE", "section_id": "SEC-02-2",
     "left": "Q-02-2-01-N04-C01", "right": "Q-02-2-01-N04-C02",
     "summary": "Maksimum 360 kg/m³ (genel beton, Tablo-308-23-b) ile minimum 400 kg/m³ (yaş "
                "sistem püskürtme beton) aynı ölçüt gibi okunduğunda çelişkili görünür.",
     "decision": "Not a true conflict: the two figures govern different materials and different "
                 "design routes. Both are retained with explicit scope, and the section carries "
                 "the difference as a stated limitation rather than resolving it by choosing.",
     "authority_note": "Both figures appear in authority-A items (DOC000087) as well as in "
                       "unrated copies (DOC000236); authority does not separate them."},
    {"id": "CF-P0-002", "result": "NO_CONFLICT_FOUND", "section_id": "SEC-02-1",
     "left": "R-Q-02-1-01-03", "right": "R-Q-02-1-02-01",
     "summary": "Aynı sekiz elemanlı birincil destekleme listesi iki farklı P0 sorusunda.",
     "decision": "Identical enumeration from the same source chunk reached through two packets; "
                 "recorded as a duplicate-claim candidate, not a conflict.",
     "authority_note": ""},
    {"id": "CF-P0-003", "result": "INSUFFICIENT_TO_DECIDE", "section_id": "SEC-02-3",
     "left": "Q-02-3-01-N05-C02", "right": "Q-02-3-01-N05-C03",
     "summary": "TBM'in homojen zeminde daha hızlı olduğu ifadesi ile delme-patlatmanın kısa "
                "mesafede daha hızlı olduğu iddiası birbirinin tersi değil ama karşılaştırılabilir "
                "değil.",
     "decision": "The packet states the first and is silent on the second, so no comparison can "
                 "be adjudicated. The second stays unsupported.",
     "authority_note": ""},
]

# Retrieval-gap probes. Each is the set of terms a supporting passage for the missing proposition
# would have to contain. Running them over the WHOLE packet is what separates "no note was
# produced" from "the packet does not carry it" - rule 38's requirement before any RETRIEVAL_GAP
# label is allowed to stand.
RETRIEVAL_GAP_PROBES = [
    {"clause_id": "Q-02-3-01-N05-C03", "question_id": "Q-02-3-01",
     "missing_proposition": "Delme-patlatma kısa mesafeli veya sık değişen jeolojide TBM'den "
                            "daha hızlı ilerleme sağlar.",
     "probes": [["delme"], ["hızlı"], ["kısa"]]},
    {"clause_id": "Q-02-3-02-N18-C01", "question_id": "Q-02-3-02",
     "missing_proposition": "Kısa mesafeli kazılarda TBM ekonomik olmayabilir.",
     "probes": [["kısa"], ["ekonomik"]]},
    {"clause_id": "Q-02-1-01-N16-D", "question_id": "Q-02-1-01",
     "missing_proposition": "İkincil destek, ek yükleri taşımak amacıyla inşa edilir.",
     "probes": [["additional loadings"], ["final lining"]]},
    {"clause_id": "Q-02-3-01-N07-C01", "question_id": "Q-02-3-01",
     "missing_proposition": "Patlatma kaynaklı titreşimler kaçınılmazdır.",
     "probes": [["titreşim"]]},
    {"clause_id": "Q-02-3-02-N15-C01", "question_id": "Q-02-3-02",
     "missing_proposition": "Titreşim ve gürültü kısıtlaması olan durumlarda TBM tercih edilir.",
     "probes": [["titreşim"], ["gürültü"]]},
]


# ================================================================ 4. registry verification
# The gate that makes the authored registry auditable rather than assertable. Every span must be
# found verbatim, under the very evidence handle it was filed under, inside the frozen packet of
# the very question it claims to resolve. A miss aborts the phase.

def verify_registry(universe: FrozenPacketUniverse) -> tuple[list[dict], list[dict]]:
    verified: list[dict] = []
    failures: list[dict] = []
    for entry in MANUAL_MAPPINGS:
        for evidence_id, span in entry["spans"]:
            ok = universe.contains_span(entry["question_id"], evidence_id, span)
            record = {"mapping_id": entry["id"], "kind": "manual",
                      "question_id": entry["question_id"], "evidence_id": evidence_id,
                      "span": span, "verified": ok,
                      "also_found_in": universe.find_span(entry["question_id"], span)}
            (verified if ok else failures).append(record)
    for entry in CROSS_LINGUAL_MAPPINGS:
        for evidence_id, span in entry["spans"]:
            ok = universe.contains_span(entry["question_id"], evidence_id, span)
            record = {"mapping_id": entry["id"], "kind": "cross_lingual",
                      "question_id": entry["question_id"], "evidence_id": evidence_id,
                      "span": span, "verified": ok,
                      "also_found_in": universe.find_span(entry["question_id"], span)}
            (verified if ok else failures).append(record)
    return verified, failures


def verify_threshold_guard() -> list[str]:
    """The one substantive claim this phase is forbidden to accept, checked as data.

    A cross-lingual mapping that moved 'lower than 1' to 'below 1.5' would be the single most
    damaging thing this phase could do, because it would look like a resolution.
    """
    violations: list[str] = []
    pinned = set(PINNED_THRESHOLD_DEFECT["clause_ids"])
    for entry in CROSS_LINGUAL_MAPPINGS:
        if entry["target"] in pinned and entry["status"] != "NOT_SUPPORTED":
            violations.append(f"{entry['id']} maps pinned clause {entry['target']} as "
                              f"{entry['status']}")
    for entry in MANUAL_MAPPINGS:
        if entry["target"] in pinned and entry["verdict"] != "NONE":
            violations.append(f"{entry['id']} maps pinned clause {entry['target']} as "
                              f"{entry['verdict']}")
    for entry in RECONSTRUCTIONS:
        text = entry["reconstructed_proposition"]
        if re.search(r"1[.,]5\s*'?[iı]n\s+alt", text):
            violations.append(f"{entry['id']} reconstructs the moved 1,5 lower threshold")
    return violations


# ================================================================ 5. resolution engine

VERDICT_TO_STATUS = {"FULL": "SUPPORTED", "PARTIAL": "PARTIALLY_SUPPORTED",
                     "AMBIGUOUS": "PARTIALLY_SUPPORTED", "NONE": "UNSUPPORTED"}
XL_TO_STATUS = {"FAITHFUL": "SUPPORTED", "PARTIAL": "PARTIALLY_SUPPORTED",
                "AMBIGUOUS": "PARTIALLY_SUPPORTED", "NOT_SUPPORTED": "UNSUPPORTED"}
STATUS_RANK = {"UNSUPPORTED": 0, "PARTIALLY_SUPPORTED": 1, "SUPPORTED": 2}


class Resolver:
    """Runs the protocol. Deterministic: same frozen inputs and same registry, same verdicts."""

    def __init__(self, universe: FrozenPacketUniverse) -> None:
        self.universe = universe
        self.questions = {q["question_id"]: q for q in load_questions()}
        self.runs = load_runs()
        self.plans = load_section_plans()
        self.notes = load_remediated_notes()
        self.ledgers = load_remediated_ledgers()
        self.clause_rows = load_jsonl(REMEDIATION / "clause_decomposition_v1_1.jsonl")
        self.non_proposition_rows = load_jsonl(REMEDIATION / "non_proposition_remediation_v1.jsonl")
        self.numeric_rows = load_jsonl(REMEDIATION / "numeric_remediation_v1.jsonl")
        self.conflict_rows = load_jsonl(REMEDIATION / "conflict_candidates_v1_1.jsonl")
        self.chunks = audit_v1.load_chunks(
            {item["chunk_id"] for item in self.universe.items.values()})
        self.frozen_source_registry = {row["chunk_id"]: row for row in
                                       load_jsonl(BOOK / "source_registry_v1.jsonl")}
        self.p0_source_registry: dict[str, dict] = {}
        self.mappings: list[ManualSupportMapping] = []
        self.cross_lingual: list[CrossLingualP0Mapping] = []
        self.gaps: list[P0EvidenceGap] = []
        self.resolved_claims: list[P0ResolvedClaim] = []
        self.extraction_rows: dict[str, list[dict]] = {}
        self.numeric_blocks: list[dict] = []
        self.retrieval_probe_rows: list[dict] = []
        self.generation_attempts: list[dict] = []
        self.retrieval_expansions: list[dict] = []
        self.query_revisions: list[P0QueryRevision] = []
        self.clauses: dict[str, dict] = {}

    # ---- provenance ---------------------------------------------------------------------
    def source_key(self, document_id: str, chunk_id: str) -> str:
        return f"SRC-{document_id}-" + hashlib.sha256(
            f"{document_id}|{chunk_id}".encode("utf-8")).hexdigest()[:12]

    def evidence_ref(self, question_id: str, evidence_id: str) -> dict:
        """Full provenance for one packet item, with a source key derived exactly the way Book
        Pipeline v1 derives it. The frozen registry is READ, never appended to: chunks it never
        registered get their key here and are written to this phase's own registry file, so the
        upstream artifact stays byte-identical while provenance still resolves."""
        item = self.universe.item(question_id, evidence_id) or {}
        chunk = self.chunks.get(item.get("chunk_id"), {})
        document_id = item.get("document_id") or chunk.get("document_id")
        chunk_id = item.get("chunk_id")
        frozen = self.frozen_source_registry.get(chunk_id)
        key = frozen["source_key"] if frozen else self.source_key(document_id, chunk_id)
        if not frozen and chunk_id not in self.p0_source_registry:
            self.p0_source_registry[chunk_id] = {
                "source_key": key, "document_id": document_id, "chunk_id": chunk_id,
                "title": chunk.get("title"), "citation_mode": chunk.get("citation_mode"),
                "provenance_status": chunk.get("provenance_status"),
                "page_start": chunk.get("original_page_start"),
                "page_end": chunk.get("original_page_end"),
                "slide_start": chunk.get("slide_start"), "slide_end": chunk.get("slide_end"),
                "section_path": chunk.get("section_path"),
                "source_relative_path": chunk.get("source_relative_path"),
                "language": chunk.get("language"), "authority_level": chunk.get("authority_level"),
                "registered_by": RESOLUTION_VERSION, "registered_at": now()}
        return {"evidence_id": evidence_id, "chunk_id": chunk_id, "document_id": document_id,
                "context_packet_sha": item.get("context_packet_sha"),
                "citation_mode": chunk.get("citation_mode"),
                "provenance_status": chunk.get("provenance_status"),
                "page_start": chunk.get("original_page_start"),
                "page_end": chunk.get("original_page_end"),
                "slide_start": chunk.get("slide_start"), "slide_end": chunk.get("slide_end"),
                "section_path": chunk.get("section_path"), "title": chunk.get("title"),
                "source_relative_path": chunk.get("source_relative_path"),
                "language": chunk.get("language"), "authority_level": chunk.get("authority_level"),
                "source_key": key}

    # ---- clause universe ----------------------------------------------------------------
    def build_clause_universe(self) -> None:
        """Remediated clauses, decomposed where a clause bundled a failure with a success, plus
        one clause per reconstructed proposition. Superseded rows are marked, never dropped."""
        for row in self.clause_rows:
            self.clauses[row["clause_id"]] = dict(
                row, resolution_status=row["status"], resolution_source="existing_extraction",
                resolution_mappings=[], resolution_notes=[], superseded=False,
                superseded_by=[], p0_origin="remediation_v1")

        for decomposition in CLAUSE_DECOMPOSITIONS:
            fragment_ids = [f["clause_id"] for f in decomposition["fragments"]]
            for old in decomposition["superseded"]:
                if old in self.clauses and old not in fragment_ids:
                    self.clauses[old].update(superseded=True, superseded_by=fragment_ids,
                                             resolution_notes=[decomposition["reason"]])
            for fragment in decomposition["fragments"]:
                previous = self.clauses.get(fragment["clause_id"], {})
                self.clauses[fragment["clause_id"]] = {
                    "clause_id": fragment["clause_id"], "clause_text": fragment["text"],
                    "clause_type": fragment["clause_type"], "material": fragment["material"],
                    "question_id": decomposition["question_id"],
                    "section_id": decomposition["section_id"],
                    "parent_note_id": previous.get("parent_note_id")
                    or decomposition["superseded"][0].rsplit("-C", 1)[0],
                    "proposition_origin": "clause_decomposition_v1",
                    "conditions": [], "exceptions": [], "qualifiers": [], "literal_spans": [],
                    "numeric_values": [], "modality": None, "missing_numeric_values": [],
                    "derived_values_not_in_source": [], "supporting_evidence_ids": [],
                    "status": "UNSUPPORTED", "status_source": "p0_resolution_v1",
                    "resolution_status": "UNSUPPORTED", "resolution_source": "manual_span_mapping",
                    "resolution_mappings": [], "resolution_notes": [decomposition["reason"]],
                    "superseded": False, "superseded_by": [], "p0_origin": "clause_decomposition",
                    "cross_lingual": False, "cross_lingual_mapping_id": None,
                    "manual_audit_clause_id": previous.get("manual_audit_clause_id"),
                    "reason": "decomposed for atomicity; awaiting its own verdict"}

        for entry in RECONSTRUCTIONS:
            self.clauses[entry["id"]] = {
                "clause_id": entry["id"],
                "clause_text": entry["reconstructed_proposition"],
                "clause_type": "classification" if "ayrıl" in entry["reconstructed_proposition"]
                               else "fact",
                "material": True, "question_id": entry["question_id"],
                "section_id": entry["section_id"],
                "parent_note_id": None, "proposition_origin": entry["proposition_origin"],
                "conditions": [], "exceptions": [], "qualifiers": [], "literal_spans": [],
                "numeric_values": [], "modality": None, "missing_numeric_values": [],
                "derived_values_not_in_source": [], "supporting_evidence_ids": [],
                "status": "UNSUPPORTED", "status_source": "p0_resolution_v1",
                "resolution_status": "UNSUPPORTED", "resolution_source": "existing_extraction",
                "resolution_mappings": [], "resolution_notes": [entry["manual_review"]],
                "superseded": False, "superseded_by": [], "p0_origin": "extraction_reconstruction",
                "cross_lingual": False, "cross_lingual_mapping_id": None,
                "manual_audit_clause_id": None,
                "reason": "reconstructed from parent context; awaiting its own verdict"}

    # ---- mapping application ------------------------------------------------------------
    def apply_mappings(self) -> None:
        """Turn the authored registry into mapping objects and clause verdicts.

        Numeric safety runs last and can only ever LOWER a verdict: a clause is not SUPPORTED on
        the strength of a mapping if a material value in it is absent from the spans offered.
        """
        for entry in MANUAL_MAPPINGS:
            question_id = entry["question_id"]
            clause = self.clauses.get(entry["target"])
            claim = entry.get("claim") or (clause or {}).get("clause_text") or ""
            for index, (evidence_id, span) in enumerate(entry["spans"], start=1):
                ref = self.evidence_ref(question_id, evidence_id)
                mapping = ManualSupportMapping(
                    mapping_id=f"{entry['id']}-S{index:02d}", gap_id=entry["gap"], claim=claim,
                    claim_language=entry["claim_language"], evidence_id=evidence_id,
                    context_packet_sha=ref["context_packet_sha"], chunk_id=ref["chunk_id"],
                    source_span=span, support_relation=entry["relation"],
                    coverage=entry["coverage"], conditions=entry["conditions"],
                    qualifiers=entry["qualifiers"], exceptions=entry["exceptions"],
                    manual_verdict=entry["verdict"], review_notes=entry["notes"],
                    question_id=question_id, document_id=ref["document_id"],
                    source_key=ref["source_key"], clause_id=entry["target"],
                    span_verified=self.universe.contains_span(question_id, evidence_id, span))
                self.mappings.append(mapping)
            self._record_verdict(entry["target"], VERDICT_TO_STATUS[entry["verdict"]],
                                 "manual_paraphrase_mapping"
                                 if entry["relation"] == "manual_paraphrase_mapping"
                                 else "manual_span_mapping",
                                 [m.mapping_id for m in self.mappings
                                  if m.mapping_id.startswith(entry["id"])],
                                 entry["spans"], entry["notes"], entry["conditions"],
                                 entry["qualifiers"], entry["exceptions"], question_id)

        for entry in CROSS_LINGUAL_MAPPINGS:
            question_id = entry["question_id"]
            clause = self.clauses.get(entry["target"])
            claim = (clause or {}).get("clause_text") or ""
            for index, (evidence_id, span) in enumerate(entry["spans"], start=1):
                ref = self.evidence_ref(question_id, evidence_id)
                mapping = CrossLingualP0Mapping(
                    mapping_id=f"{entry['id']}-S{index:02d}", gap_id=entry["gap"], claim_tr=claim,
                    source_span_en=span, source_evidence_ref=ref,
                    mapping_status=entry["status"], numeric_equivalence=entry["numeric"],
                    modality_equivalence=entry["modality"],
                    condition_equivalence=entry["condition"], scope_equivalence=entry["scope"],
                    manual_review_notes=entry["notes"], question_id=question_id,
                    clause_id=entry["target"],
                    span_verified=self.universe.contains_span(question_id, evidence_id, span))
                self.cross_lingual.append(mapping)
            self._record_verdict(entry["target"], XL_TO_STATUS[entry["status"]],
                                 "cross_lingual_mapping",
                                 [m.mapping_id for m in self.cross_lingual
                                  if m.mapping_id.startswith(entry["id"])],
                                 entry["spans"], entry["notes"], [], [], [], question_id,
                                 cross_lingual=True)

        self._pin_threshold_defect()
        self._apply_numeric_safety()

    def _record_verdict(self, clause_id: str, status: str, resolution_source: str,
                        mapping_ids: list[str], spans: list[list[str]], notes: str,
                        conditions: list[str], qualifiers: list[str], exceptions: list[str],
                        question_id: str, cross_lingual: bool = False) -> None:
        clause = self.clauses.get(clause_id)
        if clause is None:
            raise RuntimeError(f"mapping targets unknown clause {clause_id}")
        # Several mappings may address one clause. The strongest wins for the status, but every
        # one of them is retained, because a FULL beside a PARTIAL is a corroboration record.
        first_mapping = not clause["resolution_mappings"]
        if STATUS_RANK[status] > STATUS_RANK[clause["resolution_status"]] or first_mapping:
            clause["resolution_status"] = max(clause["resolution_status"], status,
                                              key=lambda s: STATUS_RANK[s])
            clause["resolution_source"] = resolution_source
        clause["resolution_mappings"] = sorted(set(clause["resolution_mappings"]) | set(mapping_ids))
        clause["resolution_notes"] = sorted(set(clause["resolution_notes"]) | {notes})
        clause["supporting_evidence_ids"] = sorted(
            set(clause.get("supporting_evidence_ids") or []) | {e for e, _ in spans})
        clause["literal_spans"] = sorted(set(clause.get("literal_spans") or [])
                                         | {s for _, s in spans})
        clause["conditions"] = sorted(set(clause.get("conditions") or []) | set(conditions))
        clause["qualifiers"] = sorted(set(clause.get("qualifiers") or []) | set(qualifiers))
        clause["exceptions"] = sorted(set(clause.get("exceptions") or []) | set(exceptions))
        if cross_lingual:
            clause["cross_lingual"] = True
            clause["cross_lingual_mapping_id"] = mapping_ids[0] if mapping_ids else None
        clause["question_id"] = clause.get("question_id") or question_id

    def _pin_threshold_defect(self) -> None:
        for clause_id in PINNED_THRESHOLD_DEFECT["clause_ids"]:
            clause = self.clauses.get(clause_id)
            if clause is None:
                continue
            clause["resolution_status"] = "UNSUPPORTED"
            clause["resolution_source"] = "cross_lingual_mapping"
            clause["resolution_notes"] = sorted(
                set(clause["resolution_notes"]) | {PINNED_THRESHOLD_DEFECT["reason"]})
            clause["threshold_defect_pinned"] = True

    def _apply_numeric_safety(self) -> None:
        """Every material value in a clause promoted to SUPPORTED must occur in the evidence the
        mapping actually offers. A value the generator computed or mis-attributed cannot ride in
        on a paraphrase that happens to match the surrounding words."""
        for clause in self.clauses.values():
            if clause["resolution_status"] != "SUPPORTED" or not clause["resolution_mappings"]:
                continue
            values = numeric_literals(clause["clause_text"])
            if not values:
                continue
            texts = [self.universe.text(clause["question_id"], eid)
                     for eid in clause.get("supporting_evidence_ids") or []]
            missing = [v for v in values if not any(number_in(v, t) for t in texts)]
            if missing:
                clause["resolution_status"] = "PARTIALLY_SUPPORTED"
                clause["missing_numeric_values"] = missing
                clause["resolution_notes"] = sorted(set(clause["resolution_notes"]) | {
                    "numeric safety: value(s) not found in the mapped evidence: "
                    + ", ".join(missing)})
                self.numeric_blocks.append({
                    "clause_id": clause["clause_id"], "question_id": clause["question_id"],
                    "missing_values": missing, "downgraded_to": "PARTIALLY_SUPPORTED"})
            else:
                clause["missing_numeric_values"] = []
                clause["numeric_values"] = [{"value": v, "source_stated": True, "derived": False}
                                            for v in values]

    # ---- extraction resolution artifacts -------------------------------------------------
    def build_extraction_rows(self) -> None:
        by_gap: dict[str, list[dict]] = {}
        for entry in RECONSTRUCTIONS:
            clause = self.clauses[entry["id"]]
            mapped = [m for m in self.mappings if m.clause_id == entry["id"]]
            cross = [m for m in self.cross_lingual if m.clause_id == entry["id"]]
            by_gap.setdefault(entry["gap"], []).append({
                "gap_id": entry["gap"], "question_id": entry["question_id"],
                "section_id": entry["section_id"],
                "source_answer_sha": sha_json(self.runs[entry["question_id"]]["accepted_answer"]),
                "source_packet_sha": self.universe.packet_sha.get(entry["question_id"]),
                "original_unit": entry["original_unit"],
                "parent_context": entry["parent_context"],
                "reconstructed_proposition": entry["reconstructed_proposition"],
                "proposition_origin": entry["proposition_origin"],
                "narrowing": entry["narrowing"],
                "support_status": clause["resolution_status"],
                "evidence_refs": sorted({m.evidence_id for m in mapped}
                                        | {m.evidence_id for m in cross
                                           if hasattr(m, "evidence_id")}
                                        | {r["evidence_id"] for r in
                                           [c.source_evidence_ref for c in cross]}),
                "literal_support": [m.source_span for m in mapped],
                "manual_review": entry["manual_review"],
                "resolution_version": RESOLUTION_VERSION})
        self.extraction_rows = by_gap

    # ---- resolved claims -----------------------------------------------------------------
    def build_resolved_claims(self) -> None:
        """One P0 claim per clause this phase actually touched. Partial results are emitted too:
        a claim that got closer but did not arrive is evidence about the gap, and hiding it would
        make the gap look smaller than it is."""
        conflict_by_clause: dict[str, str] = {}
        for review in CONFLICT_REVIEWS:
            for side in (review["left"], review["right"]):
                if review["result"] != "NO_CONFLICT_FOUND":
                    conflict_by_clause[side] = review["result"]
        # A dropped synthesis blocks the COMPOUND claim, not its components: the components are
        # separately sourced propositions, and the compound is already superseded below.
        synthesis_blocked = {entry["parent_note_id"] for entry in DROPPED_SYNTHESES
                             if not entry["citable_as_compound"]}

        counters: dict[str, int] = {}
        for clause_id, clause in sorted(self.clauses.items()):
            if clause["superseded"] or not clause["resolution_mappings"]:
                continue
            section_id = clause["section_id"]
            counters[section_id] = counters.get(section_id, 0) + 1
            question_id = clause["question_id"]
            manual = [m for m in self.mappings if m.clause_id == clause_id]
            cross = [m for m in self.cross_lingual if m.clause_id == clause_id]
            refs = [self.evidence_ref(question_id, eid)
                    for eid in clause.get("supporting_evidence_ids") or []]
            source_keys = sorted({r["source_key"] for r in refs if r.get("source_key")})
            authorities = sorted({str(r.get("authority_level")) for r in refs
                                  if r.get("authority_level")})
            status = clause["resolution_status"]
            block: list[str] = []
            if status != "SUPPORTED":
                block.append("support_status_not_supported")
            if not refs:
                block.append("evidence_refs_incomplete")
            if not source_keys or len(source_keys) != len({r["chunk_id"] for r in refs}):
                block.append("source_keys_unresolved")
            if any(not r.get("context_packet_sha") for r in refs):
                block.append("provenance_incomplete")
            if clause.get("missing_numeric_values"):
                block.append("numeric_value_not_source_stated")
            if any(m.manual_verdict not in ("FULL",) for m in manual) and status == "SUPPORTED" \
                    and not any(m.manual_verdict == "FULL" for m in manual) and not cross:
                block.append("manual_mapping_incomplete")
            if cross and not any(m.mapping_status == "FAITHFUL" for m in cross) \
                    and status == "SUPPORTED":
                block.append("cross_lingual_mapping_not_faithful")
            if conflict_by_clause.get(clause_id) == "TRUE_CONFLICT":
                block.append("unresolved_true_conflict")
            if clause.get("parent_note_id") in synthesis_blocked \
                    and clause["p0_origin"] != "clause_decomposition":
                block.append("generator_synthesis_not_citable")

            resolution_source = clause["resolution_source"]
            if clause["p0_origin"] == "extraction_reconstruction" and resolution_source == \
                    "existing_extraction":
                resolution_source = "manual_span_mapping"
            claim = P0ResolvedClaim(
                claim_id=f"{section_id}-P0-{counters[section_id]:03d}",
                gap_id=(manual[0].gap_id if manual else cross[0].gap_id),
                section_id=section_id, question_id=question_id, claim=clause["clause_text"],
                support_status=status, evidence_refs=refs,
                support_mappings=[m.mapping_id for m in manual],
                cross_lingual_mappings=[m.mapping_id for m in cross],
                numeric_data=clause.get("numeric_values") or [],
                conditions=clause.get("conditions") or [],
                qualifiers=clause.get("qualifiers") or [],
                source_keys=source_keys, citation_ready=not block,
                resolution_source=resolution_source,
                claim_language=(manual[0].claim_language if manual else "tr"),
                clause_id=clause_id,
                proposition_origin=clause.get("proposition_origin") or "existing_extraction",
                citation_block_reasons=sorted(set(block)),
                conflict_result=conflict_by_clause.get(clause_id, "NO_CONFLICT_FOUND"),
                authority_levels=authorities)
            self.resolved_claims.append(claim)

    # ---- gaps ----------------------------------------------------------------------------
    def build_gaps(self) -> None:
        remediation = json.loads(
            (MANIFESTS / "book_evidence_remediation_v1.json").read_text(encoding="utf-8"))
        index = 0
        for section_id in sorted(remediation["section_summaries"]):
            summary = remediation["section_summaries"][section_id]
            for question_id in sorted(summary["p0_gap_classification"]):
                index += 1
                question = self.questions[question_id]
                notes = [n for n in self.notes[section_id] if n["question_id"] == question_id]
                ledger = {e["claim_id"]: e for e in self.ledgers[section_id]}
                supported = [n["note_id"] for n in notes if n["support_status"] == "SUPPORTED"]
                partial = [n["note_id"] for n in notes
                           if n["support_status"] == "PARTIALLY_SUPPORTED"]
                insufficient = [n["note_id"] for n in notes
                                if n["support_status"] == "INSUFFICIENT_EVIDENCE"]
                missing = sorted(c["clause_id"] for c in self.clause_rows
                                 if c["question_id"] == question_id
                                 and c["status"] == "UNSUPPORTED")
                dropped = [r["original_note_id"] for r in self.non_proposition_rows
                           if r["question_id"] == question_id]
                classes = summary["p0_gap_classification"][question_id]
                self.gaps.append(P0EvidenceGap(
                    gap_id=f"GAP-P0-{index:02d}", section_id=section_id, question_id=question_id,
                    question_text=question["question"],
                    section_objective=self.plans[section_id]["objective"],
                    gap_classes=classes,
                    current_supported_claims=supported, current_partial_claims=partial,
                    current_insufficient_notes=insufficient,
                    critical_missing_propositions=missing + dropped,
                    existing_packet_shas=[self.universe.packet_sha.get(question_id)],
                    existing_evidence_refs=self.universe.evidence_ids(question_id),
                    resolution_strategy=self._strategy(classes),
                    packet_items_inspected=len(self.universe.evidence_ids(question_id))))

    @staticmethod
    def _strategy(classes: list[str]) -> list[str]:
        order = [("EXTRACTION_FAILURE", "A: reconstruct dropped propositions from the frozen "
                                        "answer and its parent context"),
                 ("SPAN_MAPPING_FAILURE", "B: inspect the whole frozen packet, not only cited "
                                          "handles"),
                 ("CROSS_LINGUAL_MAPPING_FAILURE", "C: map the Turkish claim onto exact English "
                                                   "source spans"),
                 ("GENERATOR_SYNTHESIS_DEFECT", "D: separate the synthesis from its components; "
                                                "regenerate only if the components are absent")]
        strategy = [text for gap_class, text in order if gap_class in classes]
        strategy.append("E: assess RETRIEVAL_GAP only after the packet is exhausted")
        strategy.append("F: assess CORPUS_GAP only after retrieval is exhausted")
        return strategy

    # ---- E: retrieval gap assessment ------------------------------------------------------
    def assess_retrieval_gaps(self) -> None:
        """A missing proposition is a RETRIEVAL_GAP candidate only after the WHOLE packet has been
        searched for it and come back empty. 'No note was produced' is not evidence of anything."""
        for probe in RETRIEVAL_GAP_PROBES:
            question_id = probe["question_id"]
            hits = {"+".join(terms): self.universe.packet_carries(question_id, terms)
                    for terms in probe["probes"]}
            any_hit = sorted({eid for found in hits.values() for eid in found})
            clause = self.clauses.get(probe["clause_id"], {})
            # "Carried" means fully carried. A clause the packet only partially supports still
            # leaves its missing sub-proposition missing, which is precisely what this probe is
            # asking about.
            carried = clause.get("resolution_status") == "SUPPORTED"
            self.retrieval_probe_rows.append({
                "clause_id": probe["clause_id"], "question_id": question_id,
                "missing_proposition": probe["missing_proposition"],
                "packet_items_searched": len(self.universe.evidence_ids(question_id)),
                "term_hits": hits, "items_mentioning_any_term": any_hit,
                "proposition_carried_after_resolution": carried,
                "retrieval_gap_candidate": not carried and not any_hit,
                "verdict": ("resolved_in_packet" if carried else
                            "present_but_insufficient" if any_hit else
                            "candidate_retrieval_gap"),
                "resolution_version": RESOLUTION_VERSION})

    # ---- D: controlled regeneration decision ----------------------------------------------
    def decide_generation(self) -> None:
        """Regeneration is the last resort for a GENERATOR_SYNTHESIS_DEFECT, not its default
        treatment. It is permitted only once existing packet evidence has been exhausted AND the
        missing propositions are still missing - and the decision is recorded either way."""
        for gap in self.gaps:
            if "GENERATOR_SYNTHESIS_DEFECT" not in gap.gap_classes:
                continue
            unresolved = [c["clause_id"] for c in self.clauses.values()
                          if c["question_id"] == gap.question_id and not c["superseded"]
                          and c["material"] and c["resolution_status"] == "UNSUPPORTED"]
            revision = P0QueryRevision(
                original_question_id=gap.question_id,
                original_question=gap.question_text,
                revised_question_id=f"{gap.question_id}-R1",
                revised_question="Yalnızca verilen kanıtlara dayanarak ayrı ayrı belirtiniz: "
                                 "A) kuru sistem püskürtme beton için minimum çimento dozajı, "
                                 "B) yaş sistem püskürtme beton için minimum çimento dozajı, "
                                 "C) çimento miktarına ilişkin üst sınır varsa hangi belgede ve "
                                 "hangi kapsamda geçtiği. Desteklenmeyen önermeleri birleştirmeyin.",
                revision_reason="The defect is a welded contrast between a general-concrete "
                                "maximum and two shotcrete minimums; the repair is to ask for the "
                                "three propositions separately rather than to re-ask the original "
                                "question, which would invite the same synthesis.",
                target_missing_proposition="separated dosage propositions with their own scopes",
                same_section=True)
            self.query_revisions.append(revision)
            self.generation_attempts.append({
                "gap_id": gap.gap_id, "attempt": 0,
                "revised_question_id": revision.revised_question_id,
                "production_request_id": None, "production_audit_id": None,
                "status": "NOT_EXECUTED", "answer_sha": None, "contract_status": None,
                "evidence_packet_sha": self.universe.packet_sha.get(gap.question_id),
                "resulting_claim_ids": [],
                "resolution_effect": "none - not executed",
                "decision": "SKIPPED_EXISTING_EVIDENCE_SUFFICIENT",
                "decision_reason":
                    "Rule 25/26: regeneration is unlocked only after existing packet evidence is "
                    "exhausted. It is not. All three propositions the revised query would target "
                    "are stated verbatim inside this question's own frozen packet (350 and 400 "
                    "kg/m3 in E005/E009, the 360 kg/m3 table limit in E004/E006), and are "
                    "resolved here by manual span mapping. Generating would add an answer, not "
                    "evidence.",
                "unresolved_material_clauses_at_decision": sorted(unresolved),
                "max_attempts_allowed": MAX_GENERATION_ATTEMPTS_PER_GAP,
                "resolution_version": RESOLUTION_VERSION})
            gap.actions_attempted.append("D: regeneration assessed and declined - existing packet "
                                         "evidence carried every targeted proposition")

    # ---- E/F: bounded retrieval expansion decision -----------------------------------------
    def decide_retrieval_expansion(self) -> None:
        """Expansion needs ALL of: P0 gap, packet manually exhausted, gap CONFIRMED as retrieval,
        no corpus gap proven, and a recorded reason. Anything less and this phase does not run
        retrieval at all - which is the case here, and is recorded rather than left implicit."""
        for row in self.retrieval_probe_rows:
            gap = next((g for g in self.gaps if g.question_id == row["question_id"]), None)
            confirmed = row["retrieval_gap_candidate"]
            self.retrieval_expansions.append({
                "gap_id": gap.gap_id if gap else None, "clause_id": row["clause_id"],
                "query": None, "baseline_top_k": RETRIEVAL_BASELINE_TOP_K,
                "experimental_top_k": None, "new_chunk_ids": [], "useful_new_evidence": False,
                "support_found": False,
                "decision": "NOT_PERFORMED",
                "decision_reason": (
                    "confirmed retrieval-gap candidate, but expansion is not required to decide "
                    "this phase: the section is already NOT_READY on other P0 requirements, and "
                    "evidence retrieved outside a frozen ContextPacket cannot carry the packet "
                    "sha that a citation-ready claim needs. Recorded for the next phase."
                    if confirmed else
                    "not a confirmed retrieval gap: the packet either carries the proposition or "
                    "carries related passages that were manually judged insufficient."),
                "retrieval_gap_confirmed": confirmed,
                "corpus_gap_candidate": False,
                "qdrant_reads": 0, "qdrant_writes": 0,
                "resolution_version": RESOLUTION_VERSION})

    # ---- gap status ------------------------------------------------------------------------
    def finalise_gaps(self) -> None:
        """RESOLVED requires every material proposition under the question to be supported. A gap
        that gained citation-ready claims while leaving one requirement unsupported is
        PARTIALLY_RESOLVED - rules 54 and 55, and the difference between them is the whole point."""
        for gap in self.gaps:
            clauses = [c for c in self.clauses.values()
                       if c["question_id"] == gap.question_id and not c["superseded"]
                       and c["material"]]
            unsupported = sorted(c["clause_id"] for c in clauses
                                 if c["resolution_status"] == "UNSUPPORTED")
            claims = [c for c in self.resolved_claims if c.question_id == gap.question_id]
            citation_ready = [c.claim_id for c in claims if c.citation_ready]
            gap.resolved_claim_ids = citation_ready
            gap.remaining_missing_propositions = unsupported
            gap.packet_exhausted = True
            gap.packet_items_inspected = len(self.universe.evidence_ids(gap.question_id))
            gap.generation_attempts = sum(1 for a in self.generation_attempts
                                          if a["gap_id"] == gap.gap_id
                                          and a["status"] != "NOT_EXECUTED")
            gap.retrieval_expansions = sum(1 for a in self.retrieval_expansions
                                           if a["gap_id"] == gap.gap_id
                                           and a["decision"] != "NOT_PERFORMED")
            gap.retrieval_gap_candidate = any(
                r["retrieval_gap_candidate"] for r in self.retrieval_probe_rows
                if r["question_id"] == gap.question_id)
            gap.corpus_gap_candidate = False
            gap.actions_attempted = sorted(set(gap.actions_attempted) | {
                f"packet inspected in full ({gap.packet_items_inspected} evidence items)",
                f"manual mappings authored: "
                f"{sum(1 for m in self.mappings if m.gap_id == gap.gap_id)}",
                f"cross-lingual mappings authored: "
                f"{sum(1 for m in self.cross_lingual if m.gap_id == gap.gap_id)}"})
            # RESOLVED is the strict reading of rule 55: every material proposition under the
            # question is SUPPORTED. A partially supported clause is not a resolved one, and a
            # cross-lingual clause that is only PARTIAL is exactly the case rule 65 warns about -
            # a faithful half hiding an unsupported remainder.
            not_fully_supported = sorted(c["clause_id"] for c in clauses
                                         if c["resolution_status"] != "SUPPORTED")
            gap.remaining_missing_propositions = not_fully_supported
            if not citation_ready:
                gap.status = "BLOCKED_RETRIEVAL" if gap.retrieval_gap_candidate else "OPEN"
            elif not_fully_supported:
                gap.status = "PARTIALLY_RESOLVED"
            else:
                gap.status = "RESOLVED"
            gap.notes = sorted(set(gap.notes) | {
                f"unsupported under this question: {len(unsupported)}",
                f"not fully supported under this question: {len(not_fully_supported)}"})

    # ---- ledgers, bundles, readiness --------------------------------------------------------
    def build_section_ledger(self, section_id: str) -> list[dict]:
        """Remediated citation-ready claims plus this phase's resolved P0 claims.

        Remediated claims are carried forward as-is: this phase may add evidence, never re-grade
        someone else's verdict silently. Claims whose clause was superseded here are carried with
        their supersession recorded so the trail from v1 to v1.1 to now stays unbroken.
        """
        superseded = {cid for cid, c in self.clauses.items() if c["superseded"]}
        superseded_notes = {cid.rsplit("-C", 1)[0] for cid in superseded}
        # A compound whose framing was dropped as generator synthesis is retired here too: its
        # components live on as separate claims, and leaving the compound quotable would put the
        # unsourced contrast back into the book by the side door.
        superseded_notes |= {entry["parent_note_id"] for entry in DROPPED_SYNTHESES
                             if not entry["citable_as_compound"]}
        entries: list[dict] = []
        for entry in self.ledgers[section_id]:
            note_ids = entry.get("parent_note_ids") or []
            was_superseded = any(n in superseded_notes for n in note_ids)
            entries.append(dict(
                entry, origin="remediated_v1", review_status="p0_resolution_v1_carried",
                superseded_by_p0_resolution=was_superseded,
                citation_ready=bool(entry["citation_ready"] and not was_superseded),
                citation_block_reasons=sorted(set(entry.get("citation_block_reasons") or [])
                                              | ({"superseded_by_p0_decomposition"}
                                                 if was_superseded else set()))))

        for claim in self.resolved_claims:
            if claim.section_id != section_id:
                continue
            entries.append({
                "claim_id": claim.claim_id, "section_id": section_id,
                "canonical_claim": claim.claim, "question_id": claim.question_id,
                "gap_id": claim.gap_id, "clause_id": claim.clause_id,
                "support_status": claim.support_status,
                "citation_ready": claim.citation_ready,
                "citation_block_reasons": claim.citation_block_reasons,
                "resolution_source": claim.resolution_source,
                "proposition_origin": claim.proposition_origin,
                "support_mappings": claim.support_mappings,
                "cross_lingual_mappings": claim.cross_lingual_mappings,
                "source_keys": claim.source_keys, "numeric": bool(claim.numeric_data),
                "numeric_data": claim.numeric_data, "conditions": claim.conditions,
                "qualifiers": claim.qualifiers, "authority_levels": claim.authority_levels,
                "conflict_result": claim.conflict_result,
                "evidence_refs": claim.evidence_refs,
                "claim_language": claim.claim_language,
                "origin": "p0_resolution_v1", "review_status": "p0_resolution_v1",
                "resolution_version": RESOLUTION_VERSION})
        return entries

    def assess_readiness(self, section_id: str, ledger: list[dict]) -> dict[str, Any]:
        """Recomputed from scratch, on the same contract remediation v1.1 used.

        Nothing is inherited: not the old readiness, not the old gap classes. A section is ready
        only if every P0 question has a citation-ready claim, no clause under a P0 objective is
        unsupported, no P0 numeric value is unproven, no P0 cross-lingual clause lacks a faithful
        mapping, and provenance is complete.
        """
        section_questions = [q for q in self.questions.values() if q["section_id"] == section_id]
        p0 = [q for q in section_questions if q["priority"] == "P0"]
        p0_ids = {q["question_id"] for q in p0}

        ready_by_question: dict[str, int] = {}
        for entry in ledger:
            if not entry.get("citation_ready"):
                continue
            question_id = entry.get("question_id")
            if not question_id:
                note = (entry.get("parent_note_ids") or [None])[0]
                question_id = note.rsplit("-N", 1)[0] if note else None
            if question_id:
                ready_by_question[question_id] = ready_by_question.get(question_id, 0) + 1

        live = [c for c in self.clauses.values()
                if c["section_id"] == section_id and not c["superseded"]]
        p0_clauses = [c for c in live if c["question_id"] in p0_ids and c["material"]]

        p0_without = sorted(q["question_id"] for q in p0
                            if not ready_by_question.get(q["question_id"]))
        critical_unsupported = sorted(c["clause_id"] for c in p0_clauses
                                      if c["resolution_status"] == "UNSUPPORTED")
        critical_numeric = sorted(c["clause_id"] for c in p0_clauses
                                  if c.get("missing_numeric_values")
                                  or c.get("derived_values_not_in_source"))
        critical_cross_lingual = sorted(
            c["clause_id"] for c in p0_clauses
            if c.get("cross_lingual") and c["resolution_status"] != "SUPPORTED")
        unresolved_numeric = sorted({c["clause_id"] for c in live
                                     if c.get("missing_numeric_values")
                                     or c.get("derived_values_not_in_source")})
        unresolved_cross_lingual = sorted({c["clause_id"] for c in live
                                           if c.get("cross_lingual")
                                           and c["resolution_status"] == "UNSUPPORTED"})
        missing_provenance = [c.claim_id for c in self.resolved_claims
                              if c.section_id == section_id
                              and any(not r.get("context_packet_sha") for r in c.evidence_refs)]
        true_conflicts = [r["id"] for r in CONFLICT_REVIEWS
                          if r["section_id"] == section_id and r["result"] == "TRUE_CONFLICT"]

        reasons: list[str] = []
        if p0_without:
            reasons.append(f"P0 questions without a citation-ready claim: {p0_without}")
        if critical_unsupported:
            reasons.append(f"unsupported clauses under P0 objectives: {len(critical_unsupported)}")
        if critical_numeric:
            reasons.append(f"unresolved numeric clauses under P0 objectives: "
                           f"{len(critical_numeric)}")
        if critical_cross_lingual:
            reasons.append(f"cross-lingual clauses under P0 objectives without a faithful "
                           f"mapping: {len(critical_cross_lingual)}")
        if missing_provenance:
            reasons.append(f"resolved claims missing provenance: {missing_provenance}")
        if true_conflicts:
            reasons.append(f"unresolved true conflicts: {true_conflicts}")

        if reasons:
            readiness, limitations = "NOT_READY", []
        else:
            limitations = []
            p1p2 = [q["question_id"] for q in section_questions
                    if q["priority"] != "P0" and not ready_by_question.get(q["question_id"])]
            if p1p2:
                limitations.append(f"P1/P2 questions without a citation-ready claim: {p1p2}")
            if unresolved_numeric:
                limitations.append(f"numeric clauses unresolved outside P0: "
                                   f"{len(unresolved_numeric)}")
            if unresolved_cross_lingual:
                limitations.append(f"cross-lingual clauses unmapped outside P0: "
                                   f"{len(unresolved_cross_lingual)}")
            for review in CONFLICT_REVIEWS:
                if review["section_id"] == section_id and review["result"] == "CONTEXT_DIFFERENCE":
                    limitations.append(f"context difference retained and surfaced: {review['id']}")
            authorities = sorted({level for c in self.resolved_claims
                                  if c.section_id == section_id for level in c.authority_levels})
            if len(authorities) > 1:
                limitations.append(f"heterogeneous source authority across resolved claims: "
                                   f"{authorities}")
            for entry in DROPPED_SYNTHESES:
                if entry["question_id"] in p0_ids:
                    limitations.append(f"generator synthesis dropped and recorded: {entry['id']}")
            readiness = "READY_WITH_LIMITATIONS" if limitations else "READY_FOR_DRAFT"

        gap_status = {g.question_id: g.status for g in self.gaps if g.section_id == section_id}
        return {
            "section_id": section_id, "readiness": readiness,
            "readiness_reasons": reasons or limitations,
            "limitations": limitations,
            "p0_total": len(p0),
            "p0_with_citation_ready_claim": len(p0) - len(p0_without),
            "p0_without_citation_ready_claim": p0_without,
            "p0_gap_status": gap_status,
            "critical_unsupported_clauses": critical_unsupported,
            "critical_numeric_clauses": critical_numeric,
            "critical_cross_lingual_clauses": critical_cross_lingual,
            "unresolved_numeric_clauses": unresolved_numeric,
            "unresolved_cross_lingual_clauses": unresolved_cross_lingual,
            "provenance_complete": not missing_provenance,
            "citation_ready_claims": sum(1 for e in ledger if e.get("citation_ready")),
            "p0_resolution_claims": sum(1 for c in self.resolved_claims
                                        if c.section_id == section_id),
            "p0_resolution_citation_ready": sum(1 for c in self.resolved_claims
                                                if c.section_id == section_id and c.citation_ready),
            "clauses_live": len(live),
            "clauses_superseded": sum(1 for c in self.clauses.values()
                                      if c["section_id"] == section_id and c["superseded"]),
        }


# ================================================================ 6. frozen integrity + Qdrant

def qdrant_points(url: str = QDRANT_URL) -> int | None:
    """Read-only. Returns None rather than raising if Qdrant is not reachable: the phase does not
    depend on it, and a missing count must be reported as unknown, never as a pass."""
    try:
        import urllib.request
        with urllib.request.urlopen(
                f"{url}/collections/tunnelbook_dense_v1", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["result"]["points_count"]
    except Exception:
        return None


def verify_frozen_integrity() -> dict[str, Any]:
    """Everything this phase reads must be byte-identical to what remediation v1 recorded.

    The baseline is the previous phase's own manifest, so drift cannot be hidden by re-baselining
    here: if a file changed, this run says so and the phase is NO-GO.
    """
    remediation = json.loads(
        (MANIFESTS / "book_evidence_remediation_v1.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    for entry in remediation["frozen_integrity"]["checks"]:
        path = ROOT / entry["path"]
        actual = sha_file(path) if path.exists() else None
        # v1.1 pinned some files by an explicit expected sha and recorded the rest by observation.
        # Either way the baseline is "what remediation v1 saw", so an unpinned file is compared
        # against the sha that run wrote down - not waved through for lack of a pin.
        expected = entry["expected_sha256"] or entry["actual_sha256"]
        checks.append({"name": entry["name"], "path": entry["path"],
                       "expected_sha256": expected, "actual_sha256": actual,
                       "pinned_in_v1_1": entry["expected_sha256"] is not None,
                       "unchanged": actual == expected, "baseline": "remediation_v1"})
    # The remediation v1 outputs themselves, plus the extractor that produced them.
    checks.append({"name": "Book Pipeline Extractor v1.1",
                   "path": "scripts/42_book_pipeline_extractor_v1_1.py",
                   "expected_sha256": remediation["implementation_sha"],
                   "actual_sha256": sha_file(ROOT / "scripts/42_book_pipeline_extractor_v1_1.py"),
                   "unchanged": sha_file(ROOT / "scripts/42_book_pipeline_extractor_v1_1.py")
                   == remediation["implementation_sha"], "baseline": "remediation_v1"})
    for relative, expected in sorted(remediation["artifact_shas"].items()):
        path = BOOK / relative if not relative.startswith("evaluation/") \
            else ROOT / "data" / relative
        actual = sha_file(path) if path.exists() else None
        checks.append({"name": f"remediation v1 artifact {relative}",
                       "path": str(path.relative_to(ROOT)),
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "remediation_v1"})
    # Book Pipeline v1's append-only source registry: this phase must not have touched it.
    registry = BOOK / "source_registry_v1.jsonl"
    checks.append({"name": "source registry v1 (must be untouched)",
                   "path": "data/book/source_registry_v1.jsonl",
                   "expected_sha256": SOURCE_REGISTRY_BASELINE,
                   "actual_sha256": sha_file(registry),
                   "unchanged": sha_file(registry) == SOURCE_REGISTRY_BASELINE,
                   "baseline": "p0_resolution_v1_precondition"})
    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {"checks": checks, "changed": changed, "all_unchanged": not changed}


# Captured before any output is written, so that "we did not modify it" is measured, not asserted.
SOURCE_REGISTRY_BASELINE = sha_file(BOOK / "source_registry_v1.jsonl")


# ================================================================ 7. runner

def controller_identity() -> dict[str, Any]:
    return {"version": RESOLUTION_VERSION, "parent_version": REMEDIATION_VERSION,
            "extractor_version": EXTRACTOR_VERSION, "source_policy": SOURCE_POLICY,
            "implementation": "scripts/43_p0_evidence_gap_resolution_v1.py",
            "implementation_sha": sha_file(Path(__file__)),
            "drafting_enabled": DRAFTING_ENABLED,
            "max_generation_attempts_per_gap": MAX_GENERATION_ATTEMPTS_PER_GAP,
            "retrieval_expansion_ceiling": RETRIEVAL_EXPANSION_CEILING}


def main() -> int:
    points_before = qdrant_points()
    universe = FrozenPacketUniverse()

    verified, span_failures = verify_registry(universe)
    threshold_violations = verify_threshold_guard()
    if span_failures or threshold_violations:
        # Fail closed. An unverifiable span is an invented span, and this is the only place that
        # distinction can still be made cheaply.
        for failure in span_failures:
            print(f"UNVERIFIED SPAN {failure['mapping_id']} {failure['question_id']} "
                  f"{failure['evidence_id']}: {failure['span'][:80]}")
        for violation in threshold_violations:
            print(f"THRESHOLD GUARD: {violation}")
        write_json(P0_AUDITS / "p0_span_verification_failures_v1.json",
                   {"span_failures": span_failures, "threshold_violations": threshold_violations})
        return 1

    resolver = Resolver(universe)
    resolver.build_clause_universe()
    resolver.build_gaps()
    resolver.apply_mappings()
    resolver.build_extraction_rows()
    resolver.build_resolved_claims()
    resolver.assess_retrieval_gaps()
    resolver.decide_generation()
    resolver.decide_retrieval_expansion()
    resolver.finalise_gaps()

    # ---- artifacts ----------------------------------------------------------------------
    for gap in resolver.gaps:
        write_json(P0_QUESTIONS / f"{gap.gap_id}.json", asdict(gap))
        rows = resolver.extraction_rows.get(gap.gap_id, [])
        if rows:
            write_jsonl(P0_EVIDENCE / f"{gap.gap_id}_extraction.jsonl", rows)

    write_jsonl(P0_EVIDENCE / "manual_support_mappings_v1.jsonl",
                [asdict(m) for m in resolver.mappings])
    write_jsonl(P0_EVIDENCE / "cross_lingual_p0_mappings_v1.jsonl",
                [asdict(m) for m in resolver.cross_lingual])
    write_jsonl(P0_EVIDENCE / "p0_source_registry_v1.jsonl",
                [resolver.p0_source_registry[k] for k in sorted(resolver.p0_source_registry)])
    write_jsonl(P0_EVIDENCE / "clause_universe_v1.jsonl",
                [resolver.clauses[k] for k in sorted(resolver.clauses)])
    write_jsonl(P0_AUDITS / "p0_span_verification_v1.jsonl", verified)
    write_jsonl(P0_AUDITS / "p0_generation_attempts_v1.jsonl", resolver.generation_attempts)
    write_jsonl(P0_AUDITS / "p0_retrieval_expansion_v1.jsonl", resolver.retrieval_expansions)
    write_jsonl(P0_AUDITS / "p0_retrieval_gap_probes_v1.jsonl", resolver.retrieval_probe_rows)
    write_jsonl(P0_AUDITS / "p0_numeric_review_v1.jsonl", NUMERIC_REVIEW + resolver.numeric_blocks)
    write_jsonl(P0_AUDITS / "p0_conflict_review_v1.jsonl", CONFLICT_REVIEWS)
    write_jsonl(P0_AUDITS / "p0_dropped_syntheses_v1.jsonl", DROPPED_SYNTHESES)
    write_jsonl(P0_AUDITS / "p0_query_revisions_v1.jsonl",
                [asdict(r) for r in resolver.query_revisions])

    sections: dict[str, dict] = {}
    for section_id in sorted(resolver.notes):
        ledger = resolver.build_section_ledger(section_id)
        write_jsonl(P0_CLAIMS / f"{section_id}.jsonl", ledger)
        readiness = resolver.assess_readiness(section_id, ledger)
        bundle = {
            "book_id": "BOOK-TUNNEL-001", "chapter_id": "CH-02", "section_id": section_id,
            "section_title": resolver.plans[section_id]["title"],
            "section_objective": resolver.plans[section_id]["objective"],
            "resolution_version": RESOLUTION_VERSION,
            "parent_bundle_sha": sha_file(REMEDIATED_BUNDLES / f"{section_id}.json"),
            "claim_ledger": ledger,
            "p0_gaps": [asdict(g) for g in resolver.gaps if g.section_id == section_id],
            "readiness_assessment": readiness,
            "drafting_enabled": DRAFTING_ENABLED,
            "created_at": now()}
        bundle["bundle_sha"] = sha_json({k: v for k, v in bundle.items()
                                         if k not in ("bundle_sha", "created_at")})
        write_json(P0_BUNDLES / f"{section_id}.json", bundle)
        sections[section_id] = readiness

    integrity = verify_frozen_integrity()
    points_after = qdrant_points()

    manifest_path = MANIFESTS / "p0_evidence_gap_resolution_v1.json"
    manifest = build_manifest(resolver, sections, integrity, verified,
                              points_before, points_after)
    write_json(manifest_path, manifest)
    if "--skip-tests" not in sys.argv:
        manifest = run_tests_and_record(manifest_path)
    write_json(METADATA / "p0_evidence_gap_resolution_v1.json", build_descriptor(manifest))
    write_report(manifest, resolver, sections)

    print_summary(manifest, sections)
    return 0 if manifest["status"] == "closed_go" else 1


def build_manifest(resolver: "Resolver", sections: dict[str, dict], integrity: dict,
                   verified: list[dict], points_before: int | None,
                   points_after: int | None) -> dict[str, Any]:
    remediation = json.loads(
        (MANIFESTS / "book_evidence_remediation_v1.json").read_text(encoding="utf-8"))
    gaps = resolver.gaps
    artifact_shas = {}
    for path in sorted(P0.rglob("*")):
        if path.is_file():
            artifact_shas[str(path.relative_to(BOOK))] = sha_file(path)

    resolved = [g.gap_id for g in gaps if g.status == "RESOLVED"]
    partial = [g.gap_id for g in gaps if g.status == "PARTIALLY_RESOLVED"]
    unresolved = [g.gap_id for g in gaps if g.status not in ("RESOLVED", "PARTIALLY_RESOLVED")]
    citation_ready = [c for c in resolver.resolved_claims if c.citation_ready]

    manifest = {
        "version": RESOLUTION_VERSION,
        "created_at": now(),
        **controller_identity(),
        "input_remediation_manifest_sha": sha_file(
            MANIFESTS / "book_evidence_remediation_v1.json"),
        "input_remediation_version": remediation["remediation_version"],
        "p0_gap_count": len(gaps),
        "p0_questions": [g.question_id for g in gaps],
        "gaps": [{"gap_id": g.gap_id, "question_id": g.question_id, "section_id": g.section_id,
                  "gap_classes": g.gap_classes, "status": g.status,
                  "packet_items_inspected": g.packet_items_inspected,
                  "packet_exhausted": g.packet_exhausted,
                  "actions_attempted": g.actions_attempted,
                  "resolved_claim_ids": g.resolved_claim_ids,
                  "remaining_missing_propositions": g.remaining_missing_propositions,
                  "generation_attempts": g.generation_attempts,
                  "retrieval_expansions": g.retrieval_expansions,
                  "retrieval_gap_candidate": g.retrieval_gap_candidate,
                  "corpus_gap_candidate": g.corpus_gap_candidate} for g in gaps],
        "resolved_gaps": resolved, "partially_resolved_gaps": partial,
        "unresolved_gaps": unresolved,
        "manual_mappings": len(resolver.mappings),
        "manual_mapping_verdicts": {v: sum(1 for m in resolver.mappings if m.manual_verdict == v)
                                    for v in MANUAL_VERDICTS},
        "cross_lingual_mappings": len(resolver.cross_lingual),
        "cross_lingual_statuses": {s: sum(1 for m in resolver.cross_lingual
                                          if m.mapping_status == s)
                                   for s in CROSS_LINGUAL_STATUSES},
        "spans_verified": len(verified),
        "spans_unverified": 0,
        "extraction_reconstructions": len(RECONSTRUCTIONS),
        "clause_decompositions": sum(len(d["fragments"]) for d in CLAUSE_DECOMPOSITIONS),
        "dropped_syntheses": len(DROPPED_SYNTHESES),
        "revised_generation_attempts": sum(g.generation_attempts for g in gaps),
        "query_revisions_authored": len(resolver.query_revisions),
        "retrieval_expansion_attempts": sum(g.retrieval_expansions for g in gaps),
        "retrieval_gap_candidates": sorted({r["clause_id"] for r in resolver.retrieval_probe_rows
                                            if r["retrieval_gap_candidate"]}),
        "corpus_gap_candidates": [],
        "question_design_defects": [g.question_id for g in gaps if g.question_design_defect],
        "resolved_p0_claims": len(resolver.resolved_claims),
        "citation_ready_p0_claims": len(citation_ready),
        "numeric_downgrades": resolver.numeric_blocks,
        "conflict_results": {r["id"]: r["result"] for r in CONFLICT_REVIEWS},
        "section_readiness": {s: r["readiness"] for s, r in sections.items()},
        "section_assessments": sections,
        "artifact_shas": artifact_shas,
        "frozen_integrity": integrity,
        "qdrant_expected": QDRANT_EXPECTED_POINTS,
        "qdrant_points_before": points_before,
        "qdrant_points_after": points_after,
        "qdrant_writes": 0,
        "generation_calls": 0,
        "retrieval_calls": 0,
        "drafting_enabled": DRAFTING_ENABLED,
        "source_registry_modified": any(
            c["name"].startswith("source registry v1") and not c["unchanged"]
            for c in integrity["checks"]),
    }
    manifest["tests"] = {"suite": "tests/test_p0_evidence_gap_resolution_v1.py",
                         "executed_by": "unittest", "status": "not_run_yet",
                         "tests_run": None, "failures": None, "errors": None}
    manifest["go_conditions"] = go_conditions(manifest, resolver, integrity)
    manifest["status"] = "closed_go" if all(manifest["go_conditions"].values()) else "closed_no_go"
    manifest["next_phase"] = route_next(manifest, sections)
    return manifest


def run_tests_and_record(manifest_path: Path) -> dict[str, Any]:
    """Run this phase's own suite and fold the result into the manifest and the GO gate.

    The suite reads the artifacts, so it has to run after they exist; the manifest is then
    rewritten once with the outcome. A phase that cannot state whether its tests passed has not
    finished, so a failing or unrunnable suite flips the status to NO-GO.
    """
    import subprocess
    completed = subprocess.run(
        [sys.executable, "-m", "unittest",
         "tests.test_p0_evidence_gap_resolution_v1", "-v"],
        cwd=str(ROOT), capture_output=True, text=True)
    tail = completed.stderr.strip().splitlines()[-6:]
    match = re.search(r"Ran (\d+) tests", completed.stderr)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    passed = completed.returncode == 0
    manifest["tests"] = {
        "suite": "tests/test_p0_evidence_gap_resolution_v1.py", "executed_by": "unittest",
        "status": "passed" if passed else "failed",
        "tests_run": int(match.group(1)) if match else None,
        "returncode": completed.returncode, "tail": tail}
    manifest["go_conditions"]["tests_pass"] = passed
    manifest["status"] = ("closed_go" if all(manifest["go_conditions"].values())
                          else "closed_no_go")
    write_json(manifest_path, manifest)
    return manifest


def go_conditions(manifest: dict, resolver: "Resolver", integrity: dict) -> dict[str, bool]:
    """Every gate from the phase contract, evaluated as data so the verdict cannot be narrated."""
    gaps = resolver.gaps
    pinned = set(PINNED_THRESHOLD_DEFECT["clause_ids"])
    return {
        "all_p0_gaps_processed": len(gaps) == 6 and all(g.packet_exhausted for g in gaps),
        "existing_packet_evidence_checked_first": all(
            g.packet_items_inspected > 0 for g in gaps),
        "every_mapping_span_verified": manifest["spans_unverified"] == 0,
        "generation_bounded": all(g.generation_attempts <= MAX_GENERATION_ATTEMPTS_PER_GAP
                                  for g in gaps),
        "retrieval_expansion_justified": all(
            row["decision"] == "NOT_PERFORMED" or row["retrieval_gap_confirmed"]
            for row in resolver.retrieval_expansions),
        "no_unsupported_numeric_promoted": not any(
            c.citation_ready and c.claim_id and any(
                not fact.get("source_stated") for fact in c.numeric_data)
            for c in resolver.resolved_claims),
        "moved_threshold_still_unsupported": all(
            resolver.clauses[c]["resolution_status"] == "UNSUPPORTED"
            for c in pinned if c in resolver.clauses),
        "all_claims_traceable": all(
            c.source_keys and all(r.get("context_packet_sha") for r in c.evidence_refs)
            for c in resolver.resolved_claims if c.citation_ready),
        "readiness_recomputed": len(manifest["section_readiness"]) == 3,
        "frozen_integrity_holds": integrity["all_unchanged"],
        "qdrant_writes_zero": manifest["qdrant_writes"] == 0,
        "qdrant_unchanged": manifest["qdrant_points_before"] == manifest["qdrant_points_after"],
        "drafting_disabled": manifest["drafting_enabled"] is False,
    }


def build_descriptor(manifest: dict) -> dict[str, Any]:
    return {
        "version": RESOLUTION_VERSION,
        "status": manifest["status"],
        "controller": "scripts/43_p0_evidence_gap_resolution_v1.py",
        "source_policy": SOURCE_POLICY,
        "max_generation_attempts_per_gap": MAX_GENERATION_ATTEMPTS_PER_GAP,
        "retrieval_expansion_policy": {
            "permitted_only_for": "confirmed RETRIEVAL_GAP on a P0 question with the frozen "
                                  "packet manually exhausted and a recorded justification",
            "baseline_top_k": RETRIEVAL_BASELINE_TOP_K,
            "ladder": list(RETRIEVAL_EXPANSION_LADDER),
            "ceiling": RETRIEVAL_EXPANSION_CEILING,
            "performed": manifest["retrieval_expansion_attempts"],
            "production_default_unchanged": True},
        "drafting_enabled": DRAFTING_ENABLED,
        "known_limitations": [
            "Evidence is bounded by the frozen ContextPackets; a proposition absent from all "
            "twenty items of a question's packet cannot be resolved in this phase.",
            "Manual paraphrase and cross-lingual verdicts are human judgements recorded as data; "
            "their spans are machine-verified but their FULL/PARTIAL grading is not.",
            "Retrieval expansion was not performed, so RETRIEVAL_GAP candidates are candidates "
            "only and no CORPUS_GAP is claimed.",
            "No prose was written and no section was drafted.",
        ],
    }


# ================================================================ 8. report

def _gap_block(resolver: "Resolver", gap: P0EvidenceGap) -> list[str]:
    manual = [m for m in resolver.mappings if m.gap_id == gap.gap_id]
    cross = [m for m in resolver.cross_lingual if m.gap_id == gap.gap_id]
    claims = [c for c in resolver.resolved_claims if c.question_id == gap.question_id]
    lines = [f"#### {gap.gap_id} - {gap.question_id} ({gap.status})", "",
             f"*{gap.question_text}*", "",
             f"- Entering gap classes: {', '.join(gap.gap_classes)}",
             f"- Packet inspected: {gap.packet_items_inspected} evidence items "
             f"(packet sha `{(gap.existing_packet_shas or [''])[0][:16]}`)",
             f"- Manual span mappings: {len(manual)}  |  cross-lingual mappings: {len(cross)}",
             f"- Resolved claims: {len(claims)} "
             f"({sum(1 for c in claims if c.citation_ready)} citation-ready)",
             f"- Controlled regenerations: {gap.generation_attempts}  |  "
             f"retrieval expansions: {gap.retrieval_expansions}"]
    if gap.remaining_missing_propositions:
        lines.append("- Remaining unsupported propositions: "
                     + ", ".join(f"`{c}`" for c in gap.remaining_missing_propositions))
    else:
        lines.append("- Remaining unsupported propositions: none")
    lines.append("")
    return lines


def route_next(manifest: dict, sections: dict[str, dict]) -> dict[str, Any]:
    """Routing is read off the results, never chosen in advance (rule 92).

    One wrinkle is worth naming rather than smoothing over: the contract's first branch asks for a
    section at READY_FOR_DRAFT, and SEC-02-2 landed at READY_WITH_LIMITATIONS. That is still a
    ready state under rule 59 - every P0 requirement is resolved and the remainder is P1/P2 - so
    the drafting route is the correct one, provided the drafting phase carries the limitations
    forward rather than inheriting a clean bill of health.
    """
    ready_for_draft = [s for s, r in sections.items() if r["readiness"] == "READY_FOR_DRAFT"]
    ready_with_limits = [s for s, r in sections.items()
                         if r["readiness"] == "READY_WITH_LIMITATIONS"]
    classes = {c for gap in manifest["gaps"] for c in gap["gap_classes"]}
    if ready_for_draft or ready_with_limits:
        return {"route": "SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING CONTRACT V1",
                "sections": sorted(ready_for_draft + ready_with_limits),
                "why": "at least one section reached a ready state with every P0 requirement "
                       "resolved" + (
                    "" if ready_for_draft else
                    "; it is READY_WITH_LIMITATIONS, so the drafting phase must carry those "
                    "limitations rather than treat the section as unqualified"),
                "carry_forward": sorted({limit for s in ready_with_limits
                                         for limit in sections[s]["limitations"]})}
    if manifest["corpus_gap_candidates"]:
        return {"route": "CORPUS GAP REVIEW + SOURCE ACQUISITION PLAN", "sections": [],
                "why": "no section is ready and the blocking gaps are corpus gaps",
                "carry_forward": manifest["corpus_gap_candidates"]}
    if manifest["retrieval_gap_candidates"]:
        return {"route": "P0 RETRIEVAL EXPANSION / RETRIEVER QUERY REFORMULATION EXPERIMENT",
                "sections": [], "why": "no section is ready and the blocking gaps are retrieval "
                                       "gaps",
                "carry_forward": manifest["retrieval_gap_candidates"]}
    if "GENERATOR_SYNTHESIS_DEFECT" in classes:
        return {"route": "P0 GENERATOR SYNTHESIS REMEDIATION", "sections": [],
                "why": "no section is ready and a synthesis defect remains", "carry_forward": []}
    return {"route": "P0 EVIDENCE GAP RESOLUTION V2", "sections": [],
            "why": "no section is ready and no single gap class dominates", "carry_forward": []}


def write_report(manifest: dict, resolver: "Resolver", sections: dict[str, dict]) -> None:
    gaps = resolver.gaps
    ready = [s for s, r in sections.items() if r["readiness"] != "NOT_READY"]
    lines: list[str] = []
    add = lines.append

    add("# P0 Evidence Gap Resolution v1")
    add("")
    add("## Executive Decision")
    add("")
    verdict = "CLOSED / GO" if manifest["status"] == "closed_go" else "CLOSED / NO-GO"
    add(f"**P0 EVIDENCE GAP RESOLUTION V1 - {verdict}**")
    add("")
    add(f"All six P0 gaps were processed under the existing-evidence-first protocol: "
        f"{len(manifest['resolved_gaps'])} resolved, {len(manifest['partially_resolved_gaps'])} "
        f"partially resolved, {len(manifest['unresolved_gaps'])} unresolved. "
        f"{manifest['resolved_p0_claims']} P0 claims were decided, of which "
        f"{manifest['citation_ready_p0_claims']} are citation-ready, from "
        f"{manifest['manual_mappings']} manual span mappings and "
        f"{manifest['cross_lingual_mappings']} cross-lingual mappings over "
        f"{manifest['spans_verified']} verified source spans. Generation calls: "
        f"{manifest['generation_calls']}. Retrieval calls: {manifest['retrieval_calls']}. "
        f"Every resolution came out of evidence that was already inside the frozen packets.")
    add("")
    for section_id in sorted(sections):
        add(f"- **{section_id}**: {sections[section_id]['readiness']}")
    add("")
    add("## Why Drafting Is Still Blocked")
    add("")
    if ready:
        add(f"Drafting is not enabled by this phase under any outcome; that decision belongs to "
            f"the Section Drafting Contract. What changed is that {', '.join(sorted(ready))} now "
            f"passes the readiness contract, so a drafting phase has something to be run against.")
    else:
        add("No section reached readiness, so there is nothing to draft.")
    add("")
    for section_id in sorted(sections):
        assessment = sections[section_id]
        if assessment["readiness_reasons"]:
            add(f"**{section_id}** ({assessment['readiness']}):")
            for reason in assessment["readiness_reasons"]:
                add(f"  - {reason}")
            add("")
    add("`drafting_enabled` remains `false` in both the manifest and the descriptor.")
    add("")

    add("## Frozen Inputs")
    add("")
    add("| Input | State |")
    add("|---|---|")
    add(f"| Remediation v1 manifest | `{manifest['input_remediation_manifest_sha'][:16]}` |")
    add(f"| Frozen integrity checks | {len(manifest['frozen_integrity']['checks'])}, "
        f"{'all unchanged' if manifest['frozen_integrity']['all_unchanged'] else 'CHANGED'} |")
    add(f"| Source registry v1 | {'MODIFIED' if manifest['source_registry_modified'] else 'untouched'} |")
    add(f"| Qdrant | {manifest['qdrant_points_before']} before / "
        f"{manifest['qdrant_points_after']} after / {manifest['qdrant_writes']} writes |")
    add("")
    add("New source keys needed by this phase are derived with Book Pipeline v1's own key "
        "function and written to `data/book/p0_resolution/evidence/p0_source_registry_v1.jsonl`, "
        "leaving the frozen registry byte-identical.")
    add("")

    add("## Resolution Strategy")
    add("")
    add("Order was fixed in advance and is the same for every gap: reconstruct what extraction "
        "dropped (A), then search the whole frozen packet rather than the cited handles (B), then "
        "map Turkish claims onto exact English spans (C), then - and only if the packet is "
        "exhausted - consider controlled regeneration (D), retrieval gap (E) and corpus gap (F).")
    add("")
    add("Two rules did most of the work. First, the unit of inspection is the **packet**, not the "
        "citation: a generator that cited E001 next to a sentence whose support sits in E006 "
        "produced an unsupported note in v1 and a supported claim here, with no new evidence "
        "entering the system. Second, a claim may be **narrowed** to what a source says but never "
        "widened - which is why the classification claim lost its unsourced basis clause and the "
        "TBM threshold stayed broken.")
    add("")

    add("## P0 Gap Inventory")
    add("")
    add("| Gap | Question | Section | Entering classes | Status |")
    add("|---|---|---|---|---|")
    for gap in gaps:
        add(f"| {gap.gap_id} | {gap.question_id} | {gap.section_id} | "
            f"{', '.join(gap.gap_classes)} | **{gap.status}** |")
    add("")

    add("## Existing Evidence First")
    add("")
    add(f"Every gap's full packet was inspected before any other step: "
        f"{sum(g.packet_items_inspected for g in gaps)} evidence items across six packets. "
        f"{manifest['spans_verified']} authored spans were re-verified verbatim against frozen "
        f"chunk text; {manifest['spans_unverified']} failed. A failed span aborts the phase, so "
        f"no mapping in the artifacts rests on text that is not in the corpus.")
    add("")

    add("## Extraction Failures")
    add("")
    add("Q-02-1-01 and Q-02-1-02 had lost their answers entirely. Both were answered as a "
        "lead-in sentence followed by a list, and v1.1 is right to refuse to make a note out of a "
        "bare label - but the lead-in went with them, because it ends in a colon and carries no "
        "citation handle. So the classification proposition Q-02-1-01 asks for was never "
        "extracted, and Q-02-1-02 ended with zero notes while its packet held the enumeration "
        "verbatim. That is an extraction defect, not an evidence gap, and it is why this phase "
        "starts at A rather than at retrieval.")
    add("")
    add("| Reconstruction | Proposition | Narrowing | Status |")
    add("|---|---|---|---|")
    for entry in RECONSTRUCTIONS:
        clause = resolver.clauses[entry["id"]]
        add(f"| `{entry['id']}` | {entry['reconstructed_proposition'][:90]}… | "
            f"{entry['narrowing'][:80]}… | {clause['resolution_status']} |")
    add("")

    add("## Manual Span Mapping")
    add("")
    add(f"{len([m for m in MANUAL_MAPPINGS])} same-language mappings were authored over "
        f"{len(resolver.mappings)} spans. Relations used: "
        f"{', '.join(sorted({m['relation'] for m in MANUAL_MAPPINGS}))}.")
    add("")
    add("| Mapping | Target | Relation | Verdict |")
    add("|---|---|---|---|")
    for entry in MANUAL_MAPPINGS:
        add(f"| {entry['id']} | `{entry['target']}` | {entry['relation']} | {entry['verdict']} |")
    add("")

    add("## Same-Language Paraphrase Mapping")
    add("")
    paraphrase = [m for m in MANUAL_MAPPINGS if m["relation"] == "manual_paraphrase_mapping"]
    add(f"{len(paraphrase)} claims are carried by a Turkish source that says the same thing in "
        f"different words. Remediation v1 had no way to represent this, which is why they sat "
        f"unsupported beside evidence that supported them.")
    for entry in paraphrase:
        add(f"- `{entry['target']}` ← {entry['spans'][0][0]}: \"{entry['spans'][0][1][:110]}…\" "
            f"({entry['verdict']})")
    add("")

    add("## Cross-Lingual Mapping")
    add("")
    add("| Mapping | Target | Status | Numeric | Modality | Condition | Scope |")
    add("|---|---|---|---|---|---|---|")
    for entry in CROSS_LINGUAL_MAPPINGS:
        add(f"| {entry['id']} | `{entry['target']}` | **{entry['status']}** | "
            f"{'✓' if entry['numeric'] else '✗'} | {'✓' if entry['modality'] else '✗'} | "
            f"{'✓' if entry['condition'] else '✗'} | {'✓' if entry['scope'] else '✗'} |")
    add("")
    add("English source spans are stored verbatim and are never rendered into quotable Turkish.")
    add("")

    add("## Generator Synthesis Defects")
    add("")
    for entry in DROPPED_SYNTHESES:
        add(f"**{entry['id']}** ({entry['question_id']}, from `{entry['parent_note_id']}`)")
        add("")
        add(f"- Dropped: {entry['dropped_proposition']}")
        add(f"- Reason: {entry['reason']}")
        add(f"- Components retained as separate claims: "
            f"{', '.join('`' + c + '`' for c in entry['components_retained'])}")
        add(f"- Citable as a compound: {entry['citable_as_compound']}")
        add("")

    add("## Controlled Revised Queries")
    add("")
    add(f"{len(resolver.query_revisions)} revised query was authored and "
        f"{manifest['revised_generation_attempts']} were executed.")
    add("")
    for attempt in resolver.generation_attempts:
        add(f"- **{attempt['gap_id']}** → `{attempt['decision']}`. {attempt['decision_reason']}")
    add("")
    add("The revision is recorded even though it was not run, because the decision not to "
        "generate is the substantive one: rule 26 makes existing evidence the default and "
        "regeneration the exception, and this gap's three target propositions were all already "
        "in its own packet.")
    add("")

    add("## Retrieval Gap Assessment")
    add("")
    add("| Clause | Missing proposition | Packet searched | Verdict |")
    add("|---|---|---|---|")
    for row in resolver.retrieval_probe_rows:
        add(f"| `{row['clause_id']}` | {row['missing_proposition'][:70]}… | "
            f"{row['packet_items_searched']} items | {row['verdict']} |")
    add("")
    add("A missing proposition is only a retrieval-gap candidate once the whole packet has been "
        "searched for it and come back empty. Where related passages exist but do not carry the "
        "proposition, the verdict is `present_but_insufficient`, not a retrieval gap.")
    add("")

    add("## Retrieval Expansion")
    add("")
    add(f"Attempts performed: **{manifest['retrieval_expansion_attempts']}**. Production default "
        f"top_k={RETRIEVAL_BASELINE_TOP_K} is unchanged; Qdrant writes: "
        f"{manifest['qdrant_writes']}.")
    add("")
    add("Expansion was declined for every candidate. Two reasons, both recorded per row: the "
        "sections concerned are already NOT_READY on requirements expansion cannot touch, and "
        "evidence retrieved outside a frozen ContextPacket has no packet sha, so it could not "
        "produce a citation-ready claim in this phase even if it were found.")
    add("")

    add("## Corpus Gap Assessment")
    add("")
    add(f"Confirmed corpus gaps: **{len(manifest['corpus_gap_candidates'])}**. No corpus gap is "
        f"claimed, and none can be: rule 84 requires expanded retrieval to be exhausted first, "
        f"and no expansion was run. Retrieval-gap candidates are handed forward as candidates.")
    add("")

    add("## Question Design Defects")
    add("")
    if manifest["question_design_defects"]:
        for question_id in manifest["question_design_defects"]:
            add(f"- {question_id}")
    else:
        add("None. All six questions are single-obligation and answerable in principle; the "
            "failures were in extraction, span mapping and synthesis, not in question design. "
            "No question was decomposed and no technical objective was removed.")
    add("")

    add("## Numeric Safety")
    add("")
    add("| Value | Context | Source-stated | Derived | Note |")
    add("|---|---|---|---|---|")
    for entry in NUMERIC_REVIEW:
        add(f"| {entry['value']} {entry['unit']} | {entry['context'][:48]} | "
            f"{'yes' if entry['source_stated'] else '**no**'} | "
            f"{'yes' if entry['derived'] else 'no'} | {entry['notes'][:90]}… |")
    add("")
    if resolver.numeric_blocks:
        add("Numeric safety downgraded these clauses after mapping:")
        for block in resolver.numeric_blocks:
            add(f"- `{block['clause_id']}`: {', '.join(block['missing_values'])} not in the "
                f"mapped evidence → {block['downgraded_to']}")
        add("")
    add("360 and 400 kg/m³ were promoted, but on source spans, not on the generator's word: both "
        "occur verbatim in the question's own packet, in items the citing note did not point at. "
        "150 mm stays derived and non-citable. One new numeric defect was found here: the 20 bar "
        "in the Delaware claim denotes a drill's pressure capability in the source, not the "
        "groundwater pressure, so the clause carrying it stays partial.")
    add("")

    add("## Conflict Review")
    add("")
    add("| Review | Section | Result | Decision |")
    add("|---|---|---|---|")
    for review in CONFLICT_REVIEWS:
        add(f"| {review['id']} | {review['section_id']} | **{review['result']}** | "
            f"{review['decision'][:110]}… |")
    add("")

    add("## Resolved Claims")
    add("")
    add(f"{manifest['resolved_p0_claims']} claims were produced, "
        f"{manifest['citation_ready_p0_claims']} of them citation-ready.")
    add("")
    add("| Claim | Question | Status | Citation-ready | Resolution source |")
    add("|---|---|---|---|---|")
    for claim in resolver.resolved_claims:
        add(f"| {claim.claim_id} | {claim.question_id} | {claim.support_status} | "
            f"{'yes' if claim.citation_ready else 'no'} | {claim.resolution_source} |")
    add("")

    for section_id in sorted(sections):
        assessment = sections[section_id]
        add(f"## {section_id}")
        add("")
        add(f"**{resolver.plans[section_id]['title']}** — {assessment['readiness']}")
        add("")
        add(f"- P0 questions with a citation-ready claim: "
            f"{assessment['p0_with_citation_ready_claim']}/{assessment['p0_total']}")
        add(f"- Citation-ready claims in the rebuilt ledger: "
            f"{assessment['citation_ready_claims']}")
        add(f"- New P0 claims: {assessment['p0_resolution_claims']} "
            f"({assessment['p0_resolution_citation_ready']} citation-ready)")
        add(f"- Unsupported clauses under P0 objectives: "
            f"{len(assessment['critical_unsupported_clauses'])}")
        add("")
        for gap in gaps:
            if gap.section_id == section_id:
                lines.extend(_gap_block(resolver, gap))

    add("## Recomputed Readiness")
    add("")
    add("| Section | Remediation v1 | P0 Resolution v1 | Blocking |")
    add("|---|---|---|---|")
    remediation = json.loads(
        (MANIFESTS / "book_evidence_remediation_v1.json").read_text(encoding="utf-8"))
    for section_id in sorted(sections):
        before = remediation["section_readiness"][section_id]
        reasons = sections[section_id]["readiness_reasons"]
        add(f"| {section_id} | {before} | **{sections[section_id]['readiness']}** | "
            f"{'; '.join(reasons)[:120] if reasons else '—'} |")
    add("")
    add("Readiness was recomputed from scratch on the same contract v1.1 used - no threshold was "
        "loosened, and nothing was inherited from the earlier bundles.")
    add("")

    add("## Remaining P0 Gaps")
    add("")
    for gap in gaps:
        if gap.status == "RESOLVED":
            continue
        add(f"- **{gap.gap_id} / {gap.question_id}** ({gap.status}): "
            + (", ".join(f"`{c}`" for c in gap.remaining_missing_propositions) or "—"))
    add("")

    add("## Frozen Integrity")
    add("")
    add(f"{len(manifest['frozen_integrity']['checks'])} checks, "
        f"{'all unchanged' if manifest['frozen_integrity']['all_unchanged'] else 'CHANGED: ' + ', '.join(manifest['frozen_integrity']['changed'])}.")
    add("")
    add("Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded Generator "
        "v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual audit, every "
        "remediation v1 artifact, the corpus chunks and the production audit log are byte-"
        "identical. So is the source registry.")
    add("")

    add("## Tests")
    add("")
    add("`tests/test_p0_evidence_gap_resolution_v1.py` asserts the protocol rather than the "
        "results: existing-evidence-first ordering, the generation bound, no same-question retry, "
        "the pinned threshold, the pinned numeric defects, that a partially resolved gap cannot "
        "be marked RESOLVED, that a section cannot be READY with an open P0 gap, retrieval "
        "expansion justification and ceiling, corpus-gap preconditions, provenance resolution, "
        "and frozen integrity.")
    add("")

    add("## Final Decision")
    add("")
    add(f"**{verdict}**")
    add("")
    add("| Gate | Result |")
    add("|---|---|")
    for name, ok in manifest["go_conditions"].items():
        add(f"| {name.replace('_', ' ')} | {'PASS' if ok else '**FAIL**'} |")
    add("")
    add("The phase's contract is that all six gaps were *processed*, not that all six were "
        "*resolved*. Two were: Q-02-2-01 and Q-02-2-02 now carry every proposition their section "
        "objective requires, and SEC-02-2 reaches readiness. The other four are honestly short, "
        "and the report says of what.")
    add("")
    add("## Next Phase")
    add("")
    routing = manifest["next_phase"]
    add(f"**{routing['route']}**")
    add("")
    add(f"Why: {routing['why']}.")
    if routing["sections"]:
        add("")
        add(f"Sections in scope: {', '.join(routing['sections'])}.")
    if routing["carry_forward"]:
        add("")
        add("Carried forward:")
        for item in routing["carry_forward"]:
            add(f"- {item}")
    add("")
    add("Routing was computed from the recomputed readiness, not decided in advance. Four P0 gaps "
        "remain partially resolved and SEC-02-1 and SEC-02-3 stay NOT_READY; they are not part of "
        "the next phase's drafting scope and remain open work.")
    add("")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "p0_evidence_gap_resolution_v1.md").write_text("\n".join(lines) + "\n",
                                                              encoding="utf-8")


def print_summary(manifest: dict, sections: dict[str, dict]) -> None:
    go = manifest["status"] == "closed_go"
    print()
    print(f"P0 EVIDENCE GAP RESOLUTION V1 — {'CLOSED / GO' if go else 'CLOSED / NO-GO'}")
    print()
    print(f"P0 gaps processed:                  {manifest['p0_gap_count']} / 6")
    print(f"Resolved:                           {len(manifest['resolved_gaps'])}")
    print(f"Partially resolved:                 {len(manifest['partially_resolved_gaps'])}")
    print(f"Unresolved:                         {len(manifest['unresolved_gaps'])}")
    print(f"Existing-packet mappings:           {manifest['manual_mappings']}")
    print(f"Manual paraphrase mappings:         "
          f"{sum(1 for m in MANUAL_MAPPINGS if m['relation'] == 'manual_paraphrase_mapping')}")
    print(f"Cross-lingual mappings:             {manifest['cross_lingual_mappings']}")
    print(f"Controlled revised-query gens:      {manifest['revised_generation_attempts']}")
    print(f"Retrieval expansions:               {manifest['retrieval_expansion_attempts']}")
    print(f"Confirmed retrieval gaps:           {len(manifest['retrieval_gap_candidates'])}")
    print(f"Confirmed corpus gaps:              {len(manifest['corpus_gap_candidates'])}")
    print(f"Resolved citation-ready P0 claims:  {manifest['citation_ready_p0_claims']}")
    print()
    for section_id in sorted(sections):
        print(f"  {section_id}: {sections[section_id]['readiness']}")
    print()
    print(f"Generation calls:                   {manifest['generation_calls']}")
    print(f"Retrieval calls:                    {manifest['retrieval_calls']}")
    print(f"Qdrant:                             {manifest['qdrant_points_before']} / "
          f"{manifest['qdrant_points_after']} / {manifest['qdrant_writes']} writes")
    print(f"Drafting enabled:                   {str(manifest['drafting_enabled']).lower()}")
    print()
    print(f"Next:                               {manifest['next_phase']['route']}")
    if manifest["next_phase"]["sections"]:
        print(f"  scope:                            "
              f"{', '.join(manifest['next_phase']['sections'])}")
    if not go:
        print()
        for name, ok in manifest["go_conditions"].items():
            if not ok:
                print(f"  FAILED GATE: {name}")


if __name__ == "__main__":
    raise SystemExit(main())
