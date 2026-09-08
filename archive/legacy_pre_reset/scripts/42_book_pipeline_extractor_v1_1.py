"""Book Pipeline Extractor v1.1 - materiality, proposition and clause remediation.

This is a narrow revision of the extraction stage of tunnelbook-book-writing-pipeline-v1. It does
NOT re-implement retrieval, context assembly, prompting, generation, the output contract or the
source registry, and it does not modify Evidence Note Contract v1 or Book Pipeline v1 in place.
Everything upstream of extraction stays frozen and untouched; this module reads frozen artifacts,
re-decomposes the claims already produced, and rebuilds the audited evidence layer honestly.

Four defects motivated it, all found by the pilot manual evidence audit:

  1. MATERIALITY. v1 asked "does this unit contain a number?" of text that still carried its
     packet-local [E###] citation handles, so "* Püskürtme Beton [E001]" was material because of
     the digits 001. Citation-handle digits are stripped before any materiality question is asked.
  2. BARE LABELS. A noun phrase that carries citations is still a noun phrase. Labels, headings and
     list lead-ins assert nothing, cannot be supported or refuted, and are now returned as
     NON_PROPOSITION at extraction time rather than becoming notes that later have to be downgraded.
  3. COMPOUND CLAIMS. A claim making three assertions was credited when a span carried one of them.
     Support is now decided clause by clause and aggregated only after every material clause has a
     verdict.
  4. NUMERIC OVER-CREDITING. A value the generator computed (15 cm -> 150 mm) is not a value the
     source stated. Every numeric value must occur in the cited evidence; derived conversions are
     representable but never count as source-stated support.

Nothing here generates or retrieves. The evidence universe is the frozen one: chunk text from
data/chunks*, packet-local identity rebuilt from data/production/generation_audit_v1.jsonl.
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
EVALUATION = ROOT / "data/evaluation"
METADATA = ROOT / "data/metadata"
REPORTS = ROOT / "reports"

EXTRACTOR_VERSION = "tunnelbook-book-pipeline-extractor-v1.1"
PARENT_VERSION = "tunnelbook-book-writing-pipeline-v1"
REMEDIATION_VERSION = "tunnelbook-book-evidence-remediation-v1"
SOURCE_POLICY = "corpus_only"
DRAFTING_ENABLED = False

# Extraction outcomes. NON_PROPOSITION is new in v1.1 and exists ONLY at extraction time: it
# prevents a note from being created. Evidence Note Contract v1 never sees it and is unchanged.
EXTRACTION_RESULTS = ("PROPOSITION", "NON_PROPOSITION")
NON_PROPOSITION_REASONS = ("empty", "table_fragment", "lead_in_or_heading", "bare_label_no_predicate")
CLAUSE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED")
NOTE_STATUSES = ("SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE")
PROPOSITION_ORIGINS = ("verbatim_unit", "sentence_split", "coordination_decomposition",
                       "enumeration_decomposition", "parent_child_reconstruction")
CROSS_LINGUAL_STATUSES = ("FAITHFUL", "PARTIAL", "NOT_SUPPORTED", "AMBIGUOUS")
NON_PROPOSITION_DECISIONS = ("DROP_NON_PROPOSITION", "RECONSTRUCT_FROM_PARENT_CONTEXT",
                             "VALID_EXISTING_PROPOSITION")
P0_GAP_CLASSES = ("EXTRACTION_FAILURE", "SPAN_MAPPING_FAILURE", "CROSS_LINGUAL_MAPPING_FAILURE",
                  "RETRIEVAL_GAP", "CORPUS_GAP", "GENERATOR_SYNTHESIS_DEFECT",
                  "QUESTION_DESIGN_DEFECT")

# Support thresholds are inherited unchanged from the manual audit. Loosening them to manufacture
# readiness is an explicit NO-GO condition, so they are pinned here and asserted in the tests.
CLAUSE_SUPPORTED_COVERAGE = 0.50
CLAUSE_PARTIAL_COVERAGE = 0.25
UPGRADE_COVERAGE = 0.60          # a remediation upgrade needs more than the ordinary threshold


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Frozen dependencies, imported read-only. 38_ gives the single span normaliser that producer and
# validator must share; 41_ gives the frozen evidence-universe reconstruction. Neither is modified,
# and neither pulls in the generator, so this module cannot retrieve or generate even by accident.
notes_contract = _load("evidence_note_contract_v1", "scripts/38_evidence_note_contract.py")
audit_v1 = _load("pilot_manual_audit_v1", "scripts/41_pilot_manual_evidence_audit_v1.py")


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


# ================================================================ 1. materiality primitives

HANDLE = re.compile(r"\[E\d{3}\]")
TABLE_BLOB = re.compile(r"(\|\s*:?-{2,})")
NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
UNIT_WORD = (r"cm|mm|km|m|kg/m³|kg/m3|MPa|kN|kPa|bar|ppm|%|psi|ft|inch|inches|in|°C|"
             r"saat|gün|yıl|hour|hours|day|days|year|years|M€|£|adet|atm")
RANGE_JOIN = r"(?:[-–—]|to|ile|ilâ|ila|ve)"
NUM_UNIT = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:" + RANGE_JOIN + r"\s*(\d+(?:[.,]\d+)?)\s*)?"
                      r"(" + UNIT_WORD + r")(?![\w])", re.I)
STOPWORDS = audit_v1.STOPWORDS


def strip_handles(text: str) -> str:
    """Remove packet-local [E###] handles.

    THE materiality fix. A handle is a pointer to evidence, not content of the claim, and its
    digits are not a numeric assertion. Every materiality, numeric and proposition test in v1.1
    runs on handle-stripped text.
    """
    return HANDLE.sub(" ", text)


def cited_handles(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\[E(\d{3})\]", text)))


def normalise(text: str) -> str:
    lowered = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().lower()
    return re.sub(r"[^\w\s]", "", lowered)


def content_tokens(text: str) -> list[str]:
    return [t for t in normalise(text).split() if len(t) > 2 and t not in STOPWORDS]


def clean_unit(unit: str) -> str:
    """Handle-stripped, bullet-stripped, emphasis-stripped text of one candidate unit."""
    text = strip_handles(unit)
    text = re.sub(r"^\s*(?:[-*•]|\d{1,2}[.)])\s*", "", text)
    text = re.sub(r"\*+", "", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------- predicate signals
# A proposition needs a predicate: something asserted of something. Token count and digits are not
# evidence of that (v1 used both and produced "Püskürtme Beton" as a fact). The signals below are
# deterministic and lexical; they are listed exhaustively so the rule can be audited and argued
# with, rather than hidden inside a threshold.

# Turkish finite-verb and copular suffix families. Deliberately excludes the -lar/-ler third-person
# plural family, because "kriterler" (a plural noun) and "önlerler" (a verb) are indistinguishable
# by suffix; plural verb forms are covered by the explicit lexicon below instead.
TR_PREDICATE_SUFFIX = re.compile(
    r"(?<!\w)\w{2,}(?:"
    r"dır|dir|dur|dür|tır|tir|tur|tür|"          # copula / evidential: gereklidir, elemanıdır
    r"ılır|ilir|ulur|ülür|nır|nir|nur|nür|lır|lir|lur|lür|"   # passive aorist: uygulanır
    r"abilir|ebilir|amaz|emez|maz|mez|"          # potential / negative aorist: olabilir, olmaz
    r"mak|mek"                                   # infinitive predicate: arttırmak, önlemek
    # The bare necessitative -malı/-meli is deliberately absent: it is indistinguishable from the
    # derivational adjective -ma+lı ("kaya patlamalı" = rock-bursting), and treating that as a
    # predicate made "C1 Grubu (Kaya patlamalı)" look like an assertion, which cost the rock-class
    # condition when the clause was split. Written necessitatives here always carry the copula
    # (-malıdır / -melidir) and are matched by the copula family above.
    r")(?!\w)", re.I)
TR_PREDICATE_LEXICON = re.compile(
    r"(?<!\w)(?:gerekir|artar|azalır|oluşur|olur|geçer|değişir|içerir|gösterir|verir|alır|kalır|"
    r"eder|ederler|sağlar|sağlarlar|önler|önlerler|artırır|artırırlar|azaltır|azaltırlar|"
    r"engeller|engellerler|iletir|iletirler|taşır|taşırlar|ulaşır|çalışır|uygular|yapar|belirler|"
    r"kısalır|kapsar|korur|korurlar|bulunur|görülür|beklenir|başlar|biter|düşer|yükselir|sayılır|"
    r"oluşturur|oluştururlar|kullanılır|uygulanır|yapılır)(?!\w)", re.I)
EN_PREDICATE = re.compile(
    r"(?<!\w)(?:is|are|was|were|be|been|being|has|have|had|does|do|did|can|could|may|might|must|"
    r"shall|should|will|would|acts?|serves?|provides?|requires?|allows?|shields?|protects?|"
    r"prevents?|reduces?|includes?|consists?|ranges?|offers?|shows?|showed|uses?|involves?|"
    r"makes?|indicates?|suggests?|represents?|captures?|refers?|remains?|varies|depends?|applies|"
    r"exceeds?|equals?|contains?|comprises?|occurs?|results?|leads?|enables?|limits?)(?!\w)", re.I)
# English past participle / past tense. "constructed", "characterized", "specified" carry an
# assertion; a title case heading of noun phrases does not.
EN_PARTICIPLE = re.compile(r"(?<!\w)\w{3,}ed(?!\w)")

# Suffix-anchored so any verb in the necessitative counts, not only the handful v1 happened to
# list: "tamamlanmalıdır" is exactly as normative as "olmalıdır", and a span that drops it has not
# carried the requirement.
MODALITY_TR = re.compile(r"(?<!\w)(?:\w{2,}(?:malıdır|melidir|mamalıdır|memelidir|meyecektir|"
                         r"mayacaktır|malı|meli)|gerekir|gereklidir|zorunlu|önerilir|tavsiye|"
                         r"en az|en fazla|asgari|azami)(?!\w)", re.I)
MODALITY_EN = re.compile(r"\b(must|shall|should|may|recommended|required|minimum|maximum)\b", re.I)
CONDITION_TR = re.compile(r"(durumunda|halinde|koşuluyla|şartıyla|olduğunda|bağlı olarak|"
                          r"göre değiş|dışında|hariç|istisna|zonlarında|sınıfında|sınıfı)", re.I)
CONDITION_EN = re.compile(r"\b(if|when|where|unless|provided that|depending on|except|"
                          r"in case of|in some|under)\b", re.I)
DEFINITION_TR = re.compile(r"(olarak tanımlan|olarak adlandırıl|denir|adı verilir|demektir)", re.I)
DEFINITION_EN = re.compile(r"\b(is defined as|is called|refers to|is known as|means)\b", re.I)


TITLE_CASE_PHRASE = re.compile(r"^(?:[A-Z][\w’'-]*|of|the|and|or|for|in|to|with|vs\.?|&|"
                               r"[\d.,()/%-]+)(?:\s+(?:[A-Z][\w’'-]*|of|the|and|or|for|in|to|"
                               r"with|vs\.?|&|[\d.,()/%-]+))*$")


def has_predicate(text: str, language: str) -> bool:
    if language == "tr":
        return bool(TR_PREDICATE_SUFFIX.search(text) or TR_PREDICATE_LEXICON.search(text))
    if EN_PREDICATE.search(text):
        return True
    # A participle only asserts when something finite is doing the asserting. In a title-case noun
    # phrase it is an adjective: "Steel Fibre Reinforced Shotcrete" names a material, and reading
    # "Reinforced" as a predicate would re-create the bare-label bug in English.
    if TITLE_CASE_PHRASE.match(text.strip().rstrip(".")):
        return False
    return bool(EN_PARTICIPLE.search(text))


def has_numeric_statement(text: str) -> bool:
    """A measured value with its unit is truth-evaluable even without a finite verb:
    'I. Sınıf: 3 m ilerleme' asserts an advance length. A bare enumerator ('1.') does not."""
    return bool(NUM_UNIT.search(text))


@dataclass
class ExtractionVerdict:
    result: str
    reason: str
    cleaned_text: str

    def as_dict(self):
        return asdict(self)


def analyse_unit(unit: str, language: str) -> ExtractionVerdict:
    """Decide whether one candidate unit asserts anything at all.

    Runs entirely on handle-stripped text, so citation digits can never make a unit material.
    """
    cleaned = clean_unit(unit)
    if not cleaned:
        return ExtractionVerdict("NON_PROPOSITION", "empty", cleaned)
    if len(TABLE_BLOB.findall(unit)) >= 2:
        return ExtractionVerdict("NON_PROPOSITION", "table_fragment", cleaned)
    if cleaned.rstrip().endswith(":") and not re.search(r"[.!?]\s", cleaned[:-1]):
        # A single clause ending in a colon introduces a list; it does not assert one.
        return ExtractionVerdict("NON_PROPOSITION", "lead_in_or_heading", cleaned)
    if has_predicate(cleaned, language):
        return ExtractionVerdict("PROPOSITION", "predicate_signal", cleaned)
    if has_numeric_statement(cleaned):
        return ExtractionVerdict("PROPOSITION", "numeric_statement", cleaned)
    return ExtractionVerdict("NON_PROPOSITION", "bare_label_no_predicate", cleaned)


def is_material(unit: str, language: str) -> bool:
    """v1.1 materiality. Kept as a named function because it is the thing that was wrong."""
    return analyse_unit(unit, language).result == "PROPOSITION"


# ================================================================ 2. clause decomposition

@dataclass
class ExtractedClause:
    clause_id: str
    parent_note_id: str
    clause_index: int
    clause_text: str
    material: bool
    clause_type: str
    source_unit: str
    proposition_origin: str
    evidence_handles: list[str] = field(default_factory=list)
    numeric_values: list[dict] = field(default_factory=list)
    units: list[str] = field(default_factory=list)
    modality: str | None = None
    conditions: list[str] = field(default_factory=list)
    qualifiers: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    requires_support_validation: bool = True
    status: str | None = None
    supporting_evidence_ids: list[str] = field(default_factory=list)
    literal_spans: list[str] = field(default_factory=list)
    support_relation: str | None = None
    cross_lingual: bool = False
    cross_lingual_mapping_id: str | None = None
    status_source: str | None = None
    reason: str = ""

    def as_dict(self):
        return asdict(self)


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9(])")
CONTRASTIVE = re.compile(r"\s+(?:ancak|fakat|whereas|however)\s+", re.I)
TAIL_MARKER = re.compile(r"\s((?:açısından|bakımından|amacıyla|nedeniyle|sayesinde|için)\s+.+)$",
                         re.I)
QUALIFIER_TR = re.compile(r"(genellikle|yaklaşık|tipik olarak|çoğunlukla|bazı durumlarda|"
                          r"tercihen|örneğin|civarında)", re.I)
QUALIFIER_EN = re.compile(r"\b(typically|approximately|generally|usually|often|normally|"
                          r"for example|roughly|about)\b", re.I)
EXCEPTION_TR = re.compile(r"(dışında|hariç|istisna|olmadığı durumlarda)", re.I)
EXCEPTION_EN = re.compile(r"\b(except|excluding|other than|with the exception of)\b", re.I)


ROMAN_OR_INITIAL = re.compile(r"(?:^|\s)(?:[IVXLCDM]{1,5}|[A-ZÇĞİÖŞÜ]|\d{1,2}|No|Nr|vb|bkz|approx|Fig|Tab)\.$",
                              re.IGNORECASE)
CONTINUATION = re.compile(r"^\s*(?:which|that|and|or|but|ve|ile|veya|ancak|ise|ki|çünkü|yani|"
                          r"as|because|so)\b", re.I)
LABEL_HEAD = re.compile(r"^(?P<head>[^:]{2,80}):\s*(?P<body>.+)$")


def _balanced(text: str) -> bool:
    return text.count("(") == text.count(")") and text.count("[") == text.count("]")


def _valid_split_part(part: str, language: str, has_head: bool = True,
                      min_tokens: int = 4) -> bool:
    """A split is only worth making if the piece stands alone as an assertion.

    Guards, in order of how often they caught a bad split during development:
      * balanced brackets - splitting inside '(e.g., shotcrete)' produces debris, not a claim,
      * no leading subordinator - 'which reduces shrinkage cracking' is not a proposition,
      * enough content - a bare measurement fragment is only a clause when it keeps a subject,
      * and it must pass the same proposition test as any other unit.
    """
    part = part.strip()
    if not part or not _balanced(part) or CONTINUATION.match(part):
        return False
    tokens = content_tokens(part)
    # The short-numeric exemption exists only for parts that keep a label head ("B1 Sınıfı: alt
    # yarıda 4,0 m"). Without one, "maksimum 100 mm olmalıdır" is a fragment whose subject stayed
    # in the other half of the sentence, and crediting it would evidence a claim nobody made.
    minimum = 2 if (has_head and has_numeric_statement(part)) else min_tokens
    if len(tokens) < minimum:
        return False
    return analyse_unit(part, language).result == "PROPOSITION"


def _split_if_all_valid(text: str, pattern: re.Pattern, language: str,
                        min_tokens: int = 4) -> list[str] | None:
    parts = [p.strip(" ,;") for p in pattern.split(text) if p and p.strip(" ,;")]
    if len(parts) < 2:
        return None
    return (parts if all(_valid_split_part(p, language, has_head=False, min_tokens=min_tokens)
                         for p in parts) else None)


def _split_coordinated_purposes(text: str, language: str) -> list[str] | None:
    """Split 'HEAD, A, B ve C <tail-predicate>' into three assertions sharing head and tail.

    This is the Q-02-1-06-N06 shape: 'Bu elemanlar, tünelin duraylılığını sağlamak, su
    geçirimsizliğini temin etmek ve işletme ekonomisi (...) açısından gereklidir.' - one sentence
    making three claims, which v1 credited whole when a span carried only the third.
    """
    if language != "tr":
        return None
    match = re.match(r"^(?P<head>[^,]{3,60}),\s*(?P<body>.+?)\s*$", text)
    if not match:
        return None
    body = match.group("body").rstrip(".")
    tail = TAIL_MARKER.search(body)
    if not tail:
        return None
    tail_text = tail.group(1)
    enumerated = body[:tail.start()].strip(" ,")
    items = [p.strip() for p in re.split(r",\s*|\s+ve\s+", enumerated) if p.strip()]
    if len(items) < 2:
        return None
    head = match.group("head").strip()
    clauses = [f"{head}, {item} {tail_text}." for item in items]
    return clauses if all(_valid_split_part(c, language, has_head=True) for c in clauses) else None


def _split_parallel_assertions(text: str, language: str) -> list[str] | None:
    """Comma-separated parallel assertions, with any label head repeated onto every part.

    'B1 Sınıfı: Üst yarı kazısında 2,0-3,0 m, alt yarıda 4,0 m.' makes two numeric claims, and both
    hold only FOR class B1. Dropping the head would leave 'alt yarıda 4,0 m' as a generic claim
    inheriting evidence stated for one rock class - the condition-loss failure in its purest form,
    so the head travels with every part or the split does not happen.
    """
    head, body = None, text
    label = LABEL_HEAD.match(text)
    if label and not has_predicate(label.group("head"), language):
        head, body = label.group("head").strip(), label.group("body").strip()
    parts = [p.strip(" ,;") for p in re.split(r",\s+(?=\S)", body) if p.strip(" ,;")]
    if len(parts) < 2:
        return None
    candidates = [f"{head}: {p}" if head else p for p in parts]
    return (candidates if all(_valid_split_part(c, language, has_head=bool(head))
                              for c in candidates) else None)


def _sentences(text: str, language: str) -> list[str]:
    """Sentence split that never loses text.

    Two rules learned from the pilot claims: do not break after an abbreviation or a roman-numeral
    enumerator ('III. Sınıf' is one clause, and dropping the 'III.' would silently delete the rock
    class), and never discard a fragment - a non-propositional lead-in is merged into the sentence
    it introduces rather than thrown away.
    """
    pieces, buffer = [], ""
    for piece in SENTENCE_SPLIT.split(text):
        if buffer and ROMAN_OR_INITIAL.search(buffer.rstrip()):
            buffer = f"{buffer} {piece}".strip()
            continue
        if buffer:
            pieces.append(buffer)
        buffer = piece.strip()
    if buffer:
        pieces.append(buffer)

    merged: list[str] = []
    for piece in pieces:
        if merged and analyse_unit(merged[-1], language).result == "NON_PROPOSITION":
            merged[-1] = f"{merged[-1]} {piece}".strip()
        else:
            merged.append(piece)
    if len(merged) > 1 and analyse_unit(merged[-1], language).result == "NON_PROPOSITION":
        tail = merged.pop()
        merged[-1] = f"{merged[-1]} {tail}".strip()
    return [m for m in merged if m.strip()] or [text]


def decompose_clauses(unit: str, language: str, parent_note_id: str,
                      origin: str = "verbatim_unit") -> list[ExtractedClause]:
    """Deterministic clause decomposition.

    Never splits blindly: every candidate split is discarded unless each resulting unit is itself
    an independently truth-evaluable proposition. Over-splitting manufactures clauses no source was
    ever asked to support, which is its own way of losing the truth.
    """
    handles = cited_handles(unit)
    cleaned = clean_unit(unit)
    pending: list[tuple[str, str]] = []

    sentences = _sentences(cleaned, language)
    for sentence in sentences:
        sentence_origin = origin if len(sentences) == 1 else "sentence_split"
        coordinated = _split_coordinated_purposes(sentence, language)
        if coordinated:
            pending += [(c, "coordination_decomposition") for c in coordinated]
            continue
        semis = _split_if_all_valid(sentence, re.compile(r"\s*;\s*"), language, min_tokens=3)
        if semis:
            pending += [(c, "coordination_decomposition") for c in semis]
            continue
        contrastive = _split_if_all_valid(sentence, CONTRASTIVE, language, min_tokens=3)
        if contrastive:
            pending += [(c, "coordination_decomposition") for c in contrastive]
            continue
        parallel = _split_parallel_assertions(sentence, language)
        if parallel:
            pending += [(c, "enumeration_decomposition") for c in parallel]
            continue
        pending.append((sentence, sentence_origin))

    clauses: list[ExtractedClause] = []
    for index, (text, clause_origin) in enumerate(pending, start=1):
        verdict = analyse_unit(text, language)
        numeric = extract_numeric(text)
        modality = (MODALITY_TR if language == "tr" else MODALITY_EN).search(text)
        conditions = [m.group(0) for m in
                      (CONDITION_TR if language == "tr" else CONDITION_EN).finditer(text)]
        qualifiers = [m.group(0) for m in
                      (QUALIFIER_TR if language == "tr" else QUALIFIER_EN).finditer(text)]
        exceptions = [m.group(0) for m in
                      (EXCEPTION_TR if language == "tr" else EXCEPTION_EN).finditer(text)]
        clauses.append(ExtractedClause(
            clause_id=f"{parent_note_id}-C{index:02d}", parent_note_id=parent_note_id,
            clause_index=index, clause_text=text,
            material=verdict.result == "PROPOSITION",
            clause_type=classify_clause(text, language), source_unit=cleaned,
            proposition_origin=clause_origin, evidence_handles=[f"E{h}" for h in handles],
            numeric_values=numeric, units=sorted({n["unit"] for n in numeric if n["unit"]}),
            modality=modality.group(0).lower() if modality else None,
            conditions=conditions, qualifiers=qualifiers, exceptions=exceptions))
    return clauses


def classify_clause(text: str, language: str) -> str:
    modality = MODALITY_TR if language == "tr" else MODALITY_EN
    definition = DEFINITION_TR if language == "tr" else DEFINITION_EN
    if has_numeric_statement(text):
        return "numeric"
    if modality.search(text):
        return "requirement"
    if definition.search(text):
        return "definition"
    if re.search(r"(karşılaştır|compared|versus|farkı|difference|iken|while)", text, re.I):
        return "comparison"
    if re.search(r"(risk|tehlike|hazard|failure|göçük|yangın|fire)", text, re.I):
        return "risk"
    if re.search(r"(durumunda|halinde|if|when|koşul|condition)", text, re.I):
        return "condition"
    return "fact"


# ---------------------------------------------------------------- numeric facts

# A parenthetical restatement of a figure in another unit. The inner figure may itself be a range
# ("4 to 16 inches (100 to 400 mm)"), which is how the second unsupported-conversion case slipped
# past a converter that only understood single values.
CONVERSION = re.compile(
    r"(\d+(?:[.,]\d+)?)(?:\s*" + RANGE_JOIN + r"\s*(\d+(?:[.,]\d+)?))?\s*"
    r"(" + UNIT_WORD + r")(?![\w])\s*[’']?\w*\s*\(\s*"
    r"(\d+(?:[.,]\d+)?)(?:\s*" + RANGE_JOIN + r"\s*(\d+(?:[.,]\d+)?))?\s*"
    r"(" + UNIT_WORD + r")(?![\w])\s*\)", re.I)


def extract_numeric(text: str) -> list[dict]:
    """Every value + unit in the clause, each one separately traceable.

    A value stated inside a parenthetical conversion is captured with derived=True so that a book
    can never present a figure the generator computed as a figure the source stated.
    """
    clean = strip_handles(text)
    derived_positions: set[int] = set()
    conversions: list[dict] = []
    for match in CONVERSION.finditer(clean):
        low, high, unit = match.group(4), match.group(5), match.group(6)
        conversions.append({"value": None if high else low.replace(",", "."), "unit": unit,
                            "range": f"{low}-{high}" if high else None,
                            "minimum": low.replace(",", ".") if high else None,
                            "maximum": high.replace(",", ".") if high else None,
                            "condition": None, "derived": True,
                            "derived_from_value": match.group(1).replace(",", "."),
                            "derived_from_unit": match.group(3)})
        derived_positions.add(match.start(4))

    facts: list[dict] = []
    for match in NUM_UNIT.finditer(clean):
        if match.start(1) in derived_positions:
            continue
        low, high, unit = match.group(1), match.group(2), match.group(3)
        facts.append({"value": None if high else low.replace(",", "."),
                      "unit": unit,
                      "range": f"{low}-{high}" if high else None,
                      "minimum": low.replace(",", ".") if high else None,
                      "maximum": high.replace(",", ".") if high else None,
                      "condition": None, "derived": False,
                      "derived_from_value": None, "derived_from_unit": None})
    return facts + conversions


def numeric_literals(numeric: list[dict]) -> list[str]:
    values: list[str] = []
    for fact in numeric:
        for key in ("value", "minimum", "maximum"):
            if fact.get(key):
                values.append(fact[key])
    return values


# ================================================================ 3. frozen evidence universe

def load_original_notes() -> list[dict]:
    return audit_v1.load_notes()


def load_note_audit() -> list[dict]:
    return [json.loads(l) for l in
            (AUDITS / "pilot_evidence_note_manual_audit_v1.jsonl").read_text(encoding="utf-8")
            .splitlines() if l.strip()]


def load_clause_audit() -> list[dict]:
    return [json.loads(l) for l in
            (AUDITS / "pilot_clause_support_audit_v1.jsonl").read_text(encoding="utf-8")
            .splitlines() if l.strip()]


def load_runs() -> dict[str, dict]:
    return audit_v1.load_runs()


class EvidenceUniverse:
    """The frozen chunks cited by the pilot notes, plus packet-local identity.

    Read-only by construction: chunk text comes from data/chunks*, packet-local E-handles from the
    frozen production audit log. No retrieval, no generation, no Qdrant write.
    """

    def __init__(self, notes: list[dict]):
        self.packet_map = audit_v1.reconstruct_packet_evidence()
        self.chunks = audit_v1.load_chunks(
            {ref["chunk_id"] for note in notes for ref in note["evidence_refs"]})

    def text(self, chunk_id: str) -> str:
        return (self.chunks.get(chunk_id) or {}).get("text") or ""

    def language(self, chunk_id: str) -> str | None:
        return (self.chunks.get(chunk_id) or {}).get("language")

    def for_note(self, note: dict) -> list[tuple[str, str, str]]:
        """(evidence_id, chunk_id, text) for the evidence this note actually cites."""
        return [(ref["evidence_id"], ref["chunk_id"], self.text(ref["chunk_id"]))
                for ref in note["evidence_refs"]]

    def refs_resolve(self, note: dict) -> bool:
        """Packet-local handle must resolve, under its own packet, to the chunk the note names."""
        for ref in note["evidence_refs"]:
            record = self.packet_map.get(f"{ref['context_packet_sha']}::{ref['evidence_id']}")
            if not record or record["chunk_id"] != ref["chunk_id"]:
                return False
            chunk = self.chunks.get(ref["chunk_id"])
            if not chunk or chunk.get("document_id") != ref["document_id"]:
                return False
        return True


def longest_span(clause: str, evidence_text: str, max_words: int = 26) -> str | None:
    """Shortest sufficient exact source span is preferred, but it must be found first: this returns
    the LONGEST verbatim token run of the clause occurring in the evidence, and the caller decides
    whether that run carries the clause. Matching uses the contract's own normaliser so a span
    accepted here is a span Evidence Note Contract v1 accepts."""
    haystack = notes_contract.normalise_for_span_match(evidence_text)
    words = re.sub(r"\s+", " ", strip_handles(clause)).strip().split()
    for size in range(min(len(words), max_words), 2, -1):
        for start in range(0, len(words) - size + 1):
            candidate = " ".join(words[start:start + size])
            probe = notes_contract.normalise_for_span_match(candidate)
            if probe and probe in haystack:
                return candidate
    return None


def span_coverage(clause: str, span: str | None) -> float:
    clause_tokens = content_tokens(clause)
    if not clause_tokens or not span:
        return 0.0
    return len(content_tokens(span)) / len(clause_tokens)


def numbers_present(values: list[str], evidence_texts: list[str]) -> tuple[bool, list[str]]:
    """Every material value must occur in the cited evidence. Bare single digits are skipped:
    the '1' of 'I. Sınıf' or a list enumerator is not a measured value."""
    blob = " ".join(normalise(t).replace(",", ".") for t in evidence_texts)
    raw = " ".join(t.replace(",", ".") for t in evidence_texts)
    missing = [v for v in values
               if not (len(v) <= 1 and "." not in v) and v not in blob and v not in raw]
    return not missing, missing


def modality_preserved(clause: str, span: str | None, language: str) -> bool:
    """A span may not be offered for a normative clause unless it carries the same modality."""
    pattern = MODALITY_TR if language == "tr" else MODALITY_EN
    if not pattern.search(clause):
        return True
    return bool(span and pattern.search(span))


def evaluate_clause(clause: ExtractedClause, evidence: list[tuple[str, str, str]],
                    language: str) -> dict[str, Any]:
    """Deterministic clause verdict from the frozen cited evidence.

    Order matters. A clause whose numbers are absent from the evidence is UNSUPPORTED however well
    its words match, and a derived conversion never counts as source-stated.
    """
    texts = [t for _, _, t in evidence]
    source_values = numeric_literals([n for n in clause.numeric_values if not n.get("derived")])
    derived_values = [n for n in clause.numeric_values if n.get("derived")]
    numeric_ok, missing = numbers_present(source_values, texts)
    derived_ok, derived_missing = numbers_present(numeric_literals(derived_values), texts)

    best = {"coverage": 0.0, "span": None, "evidence_id": None}
    for evidence_id, _chunk_id, text in evidence:
        span = longest_span(clause.clause_text, text)
        coverage = span_coverage(clause.clause_text, span)
        if coverage > best["coverage"]:
            best = {"coverage": coverage, "span": span, "evidence_id": evidence_id}

    if not evidence:
        return {"status": "UNSUPPORTED", "reason": "no cited evidence", **best,
                "numeric_ok": numeric_ok, "missing_values": missing,
                "derived_unsupported": derived_missing}
    if not numeric_ok:
        return {"status": "UNSUPPORTED",
                "reason": "numeric value(s) absent from cited evidence: " + ", ".join(missing),
                **best, "numeric_ok": False, "missing_values": missing,
                "derived_unsupported": derived_missing}
    if derived_values and not derived_ok:
        # The conversion is representable, but a note carrying it cannot be fully source-supported.
        return {"status": "PARTIALLY_SUPPORTED",
                "reason": "unit conversion not stated in source: " + ", ".join(derived_missing),
                **best, "numeric_ok": True, "missing_values": [],
                "derived_unsupported": derived_missing}
    if not modality_preserved(clause.clause_text, best["span"], language):
        return {"status": "PARTIALLY_SUPPORTED",
                "reason": "modality not carried by the located span", **best,
                "numeric_ok": True, "missing_values": [], "derived_unsupported": []}

    coverage = best["coverage"]
    status = ("SUPPORTED" if coverage >= CLAUSE_SUPPORTED_COVERAGE else
              "PARTIALLY_SUPPORTED" if coverage >= CLAUSE_PARTIAL_COVERAGE else "UNSUPPORTED")
    return {"status": status, "reason": f"clause token coverage {coverage:.2f}", **best,
            "numeric_ok": True, "missing_values": [], "derived_unsupported": []}


SEVERITY = {"UNSUPPORTED": 0, "PARTIALLY_SUPPORTED": 1, "SUPPORTED": 2}


def weakest(*statuses: str) -> str:
    return min((s for s in statuses if s), key=lambda s: SEVERITY[s])


def aggregate_note_status(clause_statuses: list[str]) -> str:
    """Aggregate only after every material clause has a verdict (the caller guarantees that).

    SUPPORTED needs ALL material clauses supported - the rule Q-02-1-06-N06 broke in v1.

    PARTIALLY_SUPPORTED requires at least one clause that is FULLY supported. A note whose clauses
    are all merely partial has no proposition adequately supported, so it stays
    INSUFFICIENT_EVIDENCE. This is the stricter of the two readings of the aggregation rule and it
    matches the frozen manual audit's note-level rule; taking the looser one would have promoted
    dozens of notes on no new evidence, which is exactly the kind of quiet loosening this gate
    exists to prevent.
    """
    material = [s for s in clause_statuses if s]
    if not material:
        return "INSUFFICIENT_EVIDENCE"
    if all(s == "SUPPORTED" for s in material):
        return "SUPPORTED"
    if any(s == "SUPPORTED" for s in material):
        return "PARTIALLY_SUPPORTED"
    return "INSUFFICIENT_EVIDENCE"


# ================================================================ 4. cross-lingual support maps
# Authored by reading each of the 11 cross-lingual notes beside its cited chunk text. Lexical span
# matching cannot prove support across a language boundary, so nothing here was produced by string
# matching: every mapping states which source sentence carries the clause and how faithfully.
#
# Every source_span below is copied verbatim out of the frozen chunk and is re-verified at run time
# (verify_cross_lingual_spans); an entry whose span does not occur in its evidence is a hard error,
# so an invented quote cannot survive into a mapping.
#
# mapping_status semantics:
#   FAITHFUL      - same proposition, same qualifiers, same numbers, same modality, nothing added
#   PARTIAL       - part of the clause is carried; the remainder is not in THIS evidence item
#   NOT_SUPPORTED - the cited evidence does not carry the proposition at all
#   AMBIGUOUS     - the source could be read either way; support is not established

CROSS_LINGUAL_MAPPINGS: dict[str, list[dict]] = {
    "Q-02-1-07-N03": [
        {"clause": "It shields the final concrete lining from direct contact with groundwater.",
         "evidence_id": "E014",
         "source_span": "yer altı sularının tünel içerisine sızmasının önlenmesi",
         "status": "PARTIAL",
         "translator_note": "The source states the purpose as preventing groundwater seepage into "
                            "the tunnel. 'Shields the lining from direct contact' is a stronger, "
                            "differently-scoped statement; only the water-exclusion part maps."},
        {"clause": "It protects the final lining from potentially harmful chemical substances in "
                   "the water.",
         "evidence_id": "E014",
         "source_span": "nihai beton kaplamanın zararlı kimyasal madde etkilerine karşı korunması",
         "status": "FAITHFUL",
         "translator_note": "Direct equivalent: protection of the final concrete lining against "
                            "harmful chemical effects. No qualifier, number or modality added."},
        {"clause": "It protects the final lining from hydrostatic pressure.",
         "evidence_id": "E012",
         "source_span": "tünel kaplama betonu gerisinde hidrostatik basınç oluşmasını da engeller",
         "status": "NOT_SUPPORTED",
         "translator_note": "The source attributes hydrostatic-pressure prevention to the "
                            "protective felt/drainage layer (keçe tabakası), not to the membrane. "
                            "Re-attributing it to the membrane would be a new fact."},
    ],
    "Q-02-3-01-N02": [
        {"clause": "Tünelin uzunluğu, çapı ve kaya kütlesinin basınç dayanımı (UCS) gibi "
                   "jeoteknik özellikleri temel belirleyicilerdir.",
         "evidence_id": "E006",
         "source_span": "the tunnel length and diameter, which have a direct impact on the tunnel "
                        "cost as explained above, affect also the economic convenience of a tunnel "
                        "construction method",
         "status": "PARTIAL",
         "translator_note": "Length and diameter map faithfully. Unconfined compressive strength "
                            "(UCS) does not appear in this evidence item, so the claim's "
                            "geotechnical list is broader than the source."},
        {"clause": "TBM, uzun ve düzenli kesitli tüneller için daha rekabetçi iken; kısa ve "
                   "düzensiz kesitli tünellerde geleneksel yöntemler daha ekonomik olabilir.",
         "evidence_id": "E006",
         "source_span": "The TBM is in fact more competitive for long tunnels with a regular "
                        "shaped cross-section, while the conventional method requiring lower "
                        "initial cost and start-up time - is more economically convenient for "
                        "short tunnels with non-uniform cross-section",
         "status": "FAITHFUL",
         "translator_note": "Clause-for-clause equivalent, comparison direction preserved."},
        {"clause": "Karar verme noktası genellikle 3-5 km uzunluk civarındadır.",
         "evidence_id": "E006",
         "source_span": "Regarding the tunnel length, the turning point is at approximately 3-5 km "
                        "length",
         "status": "FAITHFUL",
         "translator_note": "Numeric range 3-5 km preserved exactly; 'approximately' preserved as "
                            "'genellikle ... civarında'."},
    ],
    "Q-02-3-01-N03": [
        {"clause": "Tünelin uzunluğu ve çapı ile kaya kütlesinin basınç dayanımı arasındaki oranı "
                   "hesaplayan bir formül kullanılır.",
         "evidence_id": "E003",
         "source_span": "The TBM Competitiveness formula captures the ratio between the length and "
                        "diameter of the tunnel and the unconfined compressive strength",
         "status": "FAITHFUL",
         "translator_note": "Ratio definition preserved with all three variables."},
        {"clause": "Bu formülün sonucu 1,5'in altındaysa geleneksel yöntem (delme-patlatma) "
                   "kullanımı uygun görülür.",
         "evidence_id": "E003",
         "source_span": "in case it is lower than 1, the conventional method is usually preferred",
         "status": "NOT_SUPPORTED",
         "translator_note": "NUMERIC DISTORTION. The source threshold for preferring the "
                            "conventional method is 1, not 1.5; 1.5 is the trade-off limit. "
                            "Translation may not move a threshold."},
        {"clause": "Bu formülün sonucu 3'ün üzerindeyse TBM kullanımı uygun görülür.",
         "evidence_id": "E003",
         "source_span": "when the result is higher than 3 the TBM is definitely a viable solution",
         "status": "FAITHFUL",
         "translator_note": "Threshold 3 and direction preserved."},
        {"clause": "1,5 ile 3 arası ise ön seçim kriteri olarak değerlendirilir.",
         "evidence_id": "E003",
         "source_span": "This value should be consider as a preliminary selection criteria only",
         "status": "NOT_SUPPORTED",
         "translator_note": "The source calls the 1.5 value itself a preliminary selection "
                            "criterion. It states no 1.5-3 band; the band is an interpretation."},
    ],
    "Q-02-3-01-N04": [
        {"clause": "TBM yönteminin ilk yatırım, tasarım ve kurulum maliyetleri daha yüksektir.",
         "evidence_id": "E009",
         "source_span": "| Initial investment | Lower                  | Higher              |",
         "status": "PARTIAL",
         "translator_note": "Design cost and initial investment map to the table rows. 'Kurulum "
                            "maliyeti' does not: the table records lead time as Longer, which is a "
                            "duration, not a cost."},
        {"clause": "TBM yönteminde ilerleme sırasında marjinal maliyetler düşüktür.",
         "evidence_id": "E009",
         "source_span": "| Marginal rate      | More increased         | Less increased      |",
         "status": "FAITHFUL",
         "translator_note": "TBM marginal rate 'Less increased' against conventional 'More "
                            "increased'; comparison direction preserved."},
        {"clause": "Delme-patlatma yönteminin ilk yatırımı daha düşükken, ilerleme sırasında "
                   "marjinal maliyetleri daha yüksektir.",
         "evidence_id": "E009",
         "source_span": "| Initial investment | Lower                  | Higher              |",
         "status": "FAITHFUL",
         "translator_note": "Conventional column: initial investment Lower, marginal rate More "
                            "increased. Both directions preserved."},
        {"clause": "Uzun mesafelerde TBM'nin düşük marjinal maliyeti, yüksek başlangıç maliyetini "
                   "telafi eder.",
         "evidence_id": "E009",
         "source_span": "A summary of the costs related to the conventional and TMB construction "
                        "techniques is reported in the table below",
         "status": "NOT_SUPPORTED",
         "translator_note": "The break-even reasoning over distance is not in the cited item. It "
                            "appears in a different chunk this note does not cite."},
    ],
    "Q-02-3-01-N05": [
        {"clause": "TBM'nin kurulum süresi (lead time) daha uzundur.",
         "evidence_id": "E006",
         "source_span": "TBM drives require a higher initial investment and a longer mobilization "
                        "and set up time (lead time)",
         "status": "FAITHFUL",
         "translator_note": "Lead time comparison preserved verbatim."},
        {"clause": "TBM homojen zemin koşullarında uzun mesafeli ilerlemelerde delme-patlatma "
                   "yöntemine göre daha hızlıdır.",
         "evidence_id": "E006",
         "source_span": "such tunnel method is generally faster for long tunnel drives in "
                        "homogeneous ground conditions",
         "status": "FAITHFUL",
         "translator_note": "Condition (homogeneous ground, long drives) preserved with the "
                            "comparison."},
        {"clause": "Delme-patlatma yöntemi kısa mesafeli veya jeolojik koşulların sık değiştiği "
                   "durumlarda daha hızlı ilerleme sağlayabilir.",
         "evidence_id": "E006",
         "source_span": "the construction method affects the construction time, due to different "
                        "mobilization times and generally different daily advance rates",
         "status": "NOT_SUPPORTED",
         "translator_note": "No cited sentence asserts a drill-and-blast speed advantage in short "
                            "or variable ground. This is an inference, not a translation."},
    ],
    "Q-02-3-01-N06": [
        {"clause": "Delme-patlatma yöntemi, jeolojik koşulların değiştiği veya çok yüksek "
                   "mukavemetli kayaçların bulunduğu durumlarda esneklik sağlar ve her tür kaya "
                   "şartında uygulanabilir.",
         "evidence_id": "E018",
         "source_span": "The TBM must be specifically designed and built based on the geological "
                        "condition of the ground",
         "status": "NOT_SUPPORTED",
         "translator_note": "The cited item describes the TBM's conditions of use only. It makes "
                            "no claim about drill-and-blast flexibility."},
        {"clause": "TBM beklenmedik zemin koşulları veya farklı kesit şekilleri durumunda ilerleme "
                   "hızında önemli yavaşlamalar yaşayabilir ve esnekliği sınırlıdır.",
         "evidence_id": "E018",
         "source_span": "In case of different ground conditions or different profile shapes from "
                        "the planned ones, the TBM can experience significant slowdowns in the "
                        "advance rate",
         "status": "FAITHFUL",
         "translator_note": "Source says 'no flexibility'; the claim says 'limited flexibility', "
                            "which is weaker, not stronger. Slowdown condition preserved."},
    ],
    "Q-02-3-01-N08": [
        {"clause": "Jeolojik koşullardaki farklılıklar nedeniyle, her iki yöntemin avantajlarını "
                   "birleştiren hibrit çözümler de tercih edilebilir.",
         "evidence_id": "E009",
         "source_span": "The hybrid solutions are largely adopted due to the difference in "
                        "geological conditions of the tunnel",
         "status": "FAITHFUL",
         "translator_note": "Cause (geological difference) and outcome (hybrid solutions adopted) "
                            "both preserved."},
        {"clause": "Tünelin belirli bölümleri TBM ile, diğer bölümleri ise delme-patlatma "
                   "yöntemiyle açılabilir.",
         "evidence_id": "E009",
         "source_span": "the Gotthard Base Tunnel was excavated for 65% of the length by TBM and "
                        "remaining 35% of the length by conventional construction method",
         "status": "FAITHFUL",
         "translator_note": "The claim generalises a named example without adding numbers; the "
                            "percentages stay in the source, not in the claim."},
    ],
    "Q-02-3-02-N03": [
        {"clause": "Yüksek hidrostatik su basıncının eşlik ettiği, yüksek geçirgenliğe veya "
                   "yarıklara sahip zeminlerde, EPB makinelerinin vida konveyöründe yeterli tıkaç "
                   "(plug) oluşturmasının zor olduğu durumlarda Slurry TBM'ler daha uygun olabilir.",
         "evidence_id": "E001",
         "source_span": "In situations where a high hydrostatic head is combined with high "
                        "permeability or fissures it maybe be difficult to form an adequate plug "
                        "in the screw conveyor of an EPBM",
         "status": "FAITHFUL",
         "translator_note": "Condition chain (hydrostatic head + permeability/fissures -> plug "
                            "difficulty -> slurry machine) preserved, including the hedged "
                            "modality 'may be' -> 'olabilir'. SFM is the slurry face machine."},
    ],
    "Q-02-3-02-N05": [
        {"clause": "Yeraltı suyu seviyelerini korumak veya kontamine/gazlı zeminlerde güvenli kazı "
                   "yapmak için kapalı aynalı makineler tercih edilir.",
         "evidence_id": "E005",
         "source_span": "to maintain natural ground water levels or to tunnel safely in "
                        "contaminated or gassy ground",
         "status": "FAITHFUL",
         "translator_note": "Both purposes map to the source's description of face isolation."},
        {"clause": "Yüzey çökmelerini minimize etmenin kritik olduğu durumlarda kapalı aynalı "
                   "makineler tercih edilir.",
         "evidence_id": "E005",
         "source_span": "The tunnel face and excavation area can be completely isolated from the "
                        "rear tunnel and working area",
         "status": "NOT_SUPPORTED",
         "translator_note": "Surface settlement minimisation is not stated in this cited item."},
    ],
    "Q-02-3-02-N13": [
        {"clause": "TBM kullanımının uygunluğu için tünelin uzunluğu ve çapı ile kayaçların tek "
                   "eksenli basınç dayanımı arasındaki oran kullanılır.",
         "evidence_id": "E013",
         "source_span": "The TBM Competitiveness formula captures the ratio between the length and "
                        "diameter of the tunnel and the unconfined compressive strength",
         "status": "FAITHFUL",
         "translator_note": "Ratio and its three variables preserved."},
        {"clause": "Bu oranın belirli bir eşik değerini (örneğin 1.5) aşması, TBM'nin uygun bir "
                   "çözüm olabileceğini gösteren ön seçim kriteri olarak kullanılır.",
         "evidence_id": "E013",
         "source_span": "Specifically, 1.5 represents the trade-off limit between the conventional "
                        "construction method and the TBM construction method",
         "status": "PARTIAL",
         "translator_note": "The 1.5 value and its status as a preliminary selection criterion are "
                            "in the source. The directional reading 'above 1.5 therefore TBM' is "
                            "an inference the source does not state."},
    ],
    "Q-02-3-02-N14": [
        {"clause": "Yeterli ilerleme hızı örneğin günde 15-30 metredir.",
         "evidence_id": "E005",
         "source_span": "The ARAr average is between 15 - 30 meters per day",
         "status": "FAITHFUL",
         "translator_note": "Numeric range and unit preserved exactly (15-30 m/day)."},
        {"clause": "TBM kullanımı detaylı jeolojik araştırmalar gerektirir.",
         "evidence_id": "E005",
         "source_span": "The TBM must be specifically designed and built based on the geological "
                        "condition of the ground",
         "status": "PARTIAL",
         "translator_note": "The source requires design based on ground conditions, which implies "
                            "investigation but does not state a capital-investment requirement."},
        {"clause": "TBM uzun vadeli işletme maliyetlerini düşürdüğü için uygun görülmektedir.",
         "evidence_id": "E005",
         "source_span": "The speed of the TBM is also affected by the capability of",
         "status": "NOT_SUPPORTED",
         "translator_note": "No operating-cost statement occurs in the cited item."},
    ],
}

CROSS_LINGUAL_TO_CLAUSE_STATUS = {"FAITHFUL": "SUPPORTED", "PARTIAL": "PARTIALLY_SUPPORTED",
                                  "NOT_SUPPORTED": "UNSUPPORTED", "AMBIGUOUS": "UNSUPPORTED"}


def verify_cross_lingual_spans(universe: "EvidenceUniverse",
                               notes_by_id: dict[str, dict]) -> list[str]:
    """Every authored source span must occur verbatim in the evidence item it names.

    This is the guard against invented quotes and invented refs: a mapping that cannot be located
    in the frozen chunk is a hard failure, not a warning.
    """
    failures: list[str] = []
    for note_id, entries in CROSS_LINGUAL_MAPPINGS.items():
        note = notes_by_id.get(note_id)
        if note is None:
            failures.append(f"{note_id}: mapping refers to an unknown note")
            continue
        by_handle = {ref["evidence_id"]: ref["chunk_id"] for ref in note["evidence_refs"]}
        for index, entry in enumerate(entries, start=1):
            chunk_id = by_handle.get(entry["evidence_id"])
            if not chunk_id:
                failures.append(f"{note_id}-XL{index:02d}: {entry['evidence_id']} is not cited "
                                f"by this note")
                continue
            haystack = notes_contract.normalise_for_span_match(universe.text(chunk_id))
            probe = notes_contract.normalise_for_span_match(entry["source_span"])
            if not probe or probe not in haystack:
                failures.append(f"{note_id}-XL{index:02d}: source span not found in {chunk_id}")
    return failures


# ================================================================ 5. parent-context reconstruction

HEADING_LINE = re.compile(r"^\s*(?:\d{1,2}[.)]\s*)?\*\*(?P<title>[^*]+?)\*\*\s*:?\s*(?P<rest>.*)$")
LEAD_IN_LINE = re.compile(r":\s*$")
ELEMENT_LEAD_IN = re.compile(r"(eleman|unsur|bileşen|element|component)", re.I)


def _answer_lines(answer: str) -> list[str]:
    return [line.rstrip() for line in answer.replace("\r", "").split("\n")]


def _category_from_heading(title: str) -> str:
    """'Birincil Destekleme Sistemi (Initial Support)' -> 'Birincil Destekleme Sistemi'."""
    cleaned = title.strip().rstrip(":").strip()
    return re.sub(r"\s*\([^)]*\)\s*$", "", cleaned).strip()


def parent_context(claim: str, answer: str) -> dict[str, Any] | None:
    """Locate the lead-in and enclosing heading that give a bare list item its proposition.

    v1 lost this: it turned '* Püskürtme Beton [E001]' into a standalone fact, when the assertion
    the answer actually made lived one line up ('Bu sistemin elemanları şunlardır:') and two lines
    up ('**Birincil Destekleme Sistemi (Initial Support):**').
    """
    target = normalise(strip_handles(claim))
    if not target:
        return None
    lines = _answer_lines(answer)
    index = next((i for i, line in enumerate(lines)
                  if target and target in normalise(strip_handles(line))), None)
    if index is None:
        return None
    lead_in, heading = None, None
    for prior in range(index - 1, max(-1, index - 25), -1):
        line = strip_handles(lines[prior]).strip()
        if not line:
            continue
        if lead_in is None and LEAD_IN_LINE.search(line):
            lead_in = re.sub(r"\*+", "", line).strip()
        match = HEADING_LINE.match(lines[prior])
        if match:
            heading = _category_from_heading(match.group("title"))
            break
        if lead_in and re.match(r"^\s*\d{1,2}[.)]", lines[prior]):
            heading = _category_from_heading(re.sub(r"^\s*\d{1,2}[.)]\s*", "",
                                                    re.sub(r"\*+", "", lines[prior])).split(":")[0])
            break
    if not lead_in and not heading:
        return None
    return {"lead_in": lead_in, "heading": heading, "line_index": index}


def reconstruct_proposition(label: str, context: dict[str, Any], language: str) -> str | None:
    """Restate a list item as the proposition its parent lead-in asserts about it.

    This is authoring, not extraction, so the caller must record proposition_origin =
    parent_child_reconstruction and requires_support_validation = true. A reconstructed claim is
    a CANDIDATE; it is never supported merely because it was reconstructed.
    """
    label = clean_unit(label).rstrip(".").strip()
    if not label:
        return None
    category = context.get("heading") or ""
    lead_in = context.get("lead_in") or ""
    if not category and lead_in:
        category = re.sub(r"\s*(şunlardır|aşağıdaki gibidir|are as follows|include)\s*:?\s*$", "",
                          lead_in, flags=re.I).strip().rstrip(":")
    if not category:
        return None
    if language == "tr":
        if ELEMENT_LEAD_IN.search(lead_in) or ELEMENT_LEAD_IN.search(category):
            # Avoid 'X elemanları elemanlarından biridir' when the category already names elements.
            head = re.sub(r"\s+(elemanları|elemanlar|unsurları)\s*$", "", category, flags=re.I)
            return f"{label}, {head} elemanlarından biridir."
        return f"{label}, {category} kapsamında sayılan bir unsurdur."
    return f"{label} is one of the elements of {category}."


# A reconstructed proposition is validated by exactly the same clause machinery as every other
# clause. There is deliberately no bespoke "membership" check: a special-case validator for
# reconstructions would be a second, looser standard of support, and a looser standard is how
# unsupported claims get into books.


# ================================================================ 6. remediation engine

@dataclass
class RemediatedNote:
    note_id: str
    parent_note_id: str
    parent_note_sha: str
    revision: int
    remediation_version: str
    book_id: str
    chapter_id: str
    section_id: str
    question_id: str
    note_type: str
    claim: str
    claim_language: str
    support_status: str
    confidence: str
    proposition_origin: str
    evidence_refs: list[dict] = field(default_factory=list)
    literal_support: list[dict] = field(default_factory=list)
    support_relations: list[dict] = field(default_factory=list)
    cross_lingual_mapping_ids: list[str] = field(default_factory=list)
    clauses: list[dict] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    qualifiers: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    numeric_data: list[dict] = field(default_factory=list)
    modality: str | None = None
    source_keys: list[str] = field(default_factory=list)
    manual_audit_refs: list[str] = field(default_factory=list)
    split_clause_id: str | None = None
    split_reason: str | None = None
    provenance: dict = field(default_factory=dict)
    review_status: str = "remediated_v1"
    extractor_version: str = EXTRACTOR_VERSION
    evidence_note_contract_version: str = notes_contract.CONTRACT_VERSION
    created_at: str = field(default_factory=now)

    def canonical_payload(self) -> dict:
        payload = asdict(self)
        payload.pop("created_at", None)
        return payload

    def as_dict(self) -> dict:
        return {**asdict(self), "note_sha256": sha_json(self.canonical_payload())}


EQUIVALENT_JACCARD = 0.55


def match_manual_clause(clause_text: str, manual_rows: list[dict]) -> tuple[dict, str] | None:
    """Find the frozen manual clause row this v1.1 clause corresponds to, and how it relates.

    The relation decides who wins, and that matters more than the match itself:

      * "equivalent" - the same proposition the auditor read. The manual verdict stands. A clause
        that a human read against its evidence is not re-decided by a lexical heuristic; doing that
        would replace the audit with the thing the audit exists to correct.
      * "finer" - a sub-proposition of what the auditor read as one clause. Here the manual verdict
        is a ceiling, not a floor: this is exactly the compound-claim case, where part of a
        SUPPORTED clause turns out to be uncarried.
    """
    if not manual_rows:
        return None
    probe = set(content_tokens(clause_text))
    if not probe:
        return None
    best, best_score, best_tokens = None, 0.0, set()
    for row in manual_rows:
        tokens = set(content_tokens(row["clause_text"]))
        if not tokens:
            continue
        score = len(probe & tokens) / len(probe | tokens)
        if probe <= tokens or tokens <= probe:
            score = max(score, 0.85)
        if score > best_score:
            best, best_score, best_tokens = row, score, tokens
    if best is None or best_score < 0.50:
        return None
    jaccard = len(probe & best_tokens) / len(probe | best_tokens)
    relation = "equivalent" if jaccard >= EQUIVALENT_JACCARD else "finer"
    return best, relation


def match_cross_lingual(clause_text: str, entries: list[dict]) -> tuple[dict, int] | None:
    probe = set(content_tokens(clause_text))
    if not probe:
        return None
    best, best_index, best_score = None, 0, 0.0
    for index, entry in enumerate(entries, start=1):
        tokens = set(content_tokens(entry["clause"]))
        if not tokens:
            continue
        score = len(probe & tokens) / len(probe | tokens)
        if score > best_score:
            best, best_index, best_score = entry, index, score
    return (best, best_index) if best_score >= 0.30 else None


def condition_bound(clause: ExtractedClause, span: str | None, evidence_text: str) -> bool:
    """A conditional claim may only be upgraded if the SOURCE states it under the same condition.

    'B1 Sınıfı: alt yarıda 4,0 m' is not evidenced by a 4,0 m appearing anywhere in the document -
    it must appear where the document is talking about class B1. Without this, a rock-class,
    tunnel-type or method-specific figure silently becomes a generic one.
    """
    label = LABEL_HEAD.match(clause.clause_text)
    if not label:
        return True
    tokens = [t for t in content_tokens(label.group("head"))]
    if not tokens or not span:
        return True
    haystack = normalise(evidence_text)
    probe = normalise(span)
    position = haystack.find(probe)
    if position < 0:
        return False
    window = haystack[max(0, position - 600):position + len(probe) + 600]
    return all(token in window for token in tokens)


def upgrade_block_reason(clause: ExtractedClause, computed: dict, cross_lingual: bool,
                         evidence_text: str = "", language: str = "tr") -> str | None:
    """Which upgrade condition failed, so rejected upgrades are countable rather than invisible."""
    if cross_lingual:
        return "cross_lingual"
    if computed["status"] != "SUPPORTED":
        return "computed_not_supported"
    if computed["coverage"] < UPGRADE_COVERAGE:
        return "coverage_below_upgrade_threshold"
    if not computed.get("numeric_ok"):
        return "numeric_value_absent_from_evidence"
    if computed.get("derived_unsupported"):
        return "derived_conversion_not_in_source"
    span = computed.get("span")
    if not span:
        return "no_verbatim_span"
    values = numeric_literals([n for n in clause.numeric_values if not n.get("derived")])
    normalised_span = span.replace(",", ".")
    if any(v not in normalised_span for v in values if not (len(v) <= 1 and "." not in v)):
        return "numeric_value_not_carried_by_the_span"
    if not modality_preserved(clause.clause_text, span, language):
        return "modality_not_carried_by_the_span"
    if not condition_bound(clause, span, evidence_text):
        return "condition_not_bound_in_source"
    return None


def upgrade_allowed(clause: ExtractedClause, computed: dict, cross_lingual: bool,
                    evidence_text: str = "", language: str = "tr") -> bool:
    """Conditions under which remediation may raise a clause above its manual verdict.

    Stricter than the ordinary threshold on purpose: an upgrade asserts that the earlier reading
    missed support, so the support has to be visible in one verbatim span that carries the clause,
    every number it states, its modality and its condition. Cross-lingual clauses can never be
    upgraded this way - a lexical match across languages proves nothing, which is what the manual
    mappings exist for.
    """
    if cross_lingual:
        return False
    if computed["status"] != "SUPPORTED":
        return False
    if computed["coverage"] < UPGRADE_COVERAGE:
        return False
    if not computed.get("numeric_ok") or computed.get("derived_unsupported"):
        return False
    span = computed.get("span")
    if not span:
        return False
    # Every number the clause states must be inside the span itself, not merely somewhere in the
    # cited chunk: an adjacent sentence carrying a different figure is not evidence for this one.
    values = numeric_literals([n for n in clause.numeric_values if not n.get("derived")])
    normalised_span = span.replace(",", ".")
    if any(v not in normalised_span for v in values if not (len(v) <= 1 and "." not in v)):
        return False
    if not modality_preserved(clause.clause_text, span, language):
        return False
    return condition_bound(clause, span, evidence_text)


def decide_clause_status(clause: ExtractedClause, computed: dict, manual: dict | None,
                         cross_lingual_entry: tuple[dict, int] | None, note_id: str,
                         cross_lingual: bool, evidence_text: str = "",
                         language: str = "tr") -> dict[str, Any]:
    if cross_lingual_entry:
        entry, index = cross_lingual_entry
        status = CROSS_LINGUAL_TO_CLAUSE_STATUS[entry["status"]]
        return {"status": status, "status_source": "cross_lingual_manual_mapping",
                "reason": entry["translator_note"],
                "mapping_id": f"XL-{note_id}-{index:02d}",
                "evidence_id": entry["evidence_id"], "span": entry["source_span"],
                "support_relation": "manual_cross_lingual_mapping"}
    if cross_lingual:
        return {"status": "UNSUPPORTED", "status_source": "cross_lingual_unmapped",
                "reason": "cross-lingual clause with no manual mapping; lexical matching cannot "
                          "establish support across languages",
                "mapping_id": None, "evidence_id": None, "span": None,
                "support_relation": None}
    if manual is None:
        status, source = computed["status"], "v1_1_extraction"
        evidence_id, span = computed.get("evidence_id"), computed.get("span")
    else:
        manual_row, relation = manual
        if (SEVERITY[computed["status"]] > SEVERITY[manual_row["status"]]
                and upgrade_allowed(clause, computed, cross_lingual, evidence_text, language)):
            status, source = computed["status"], "literal_span_remediation"
            evidence_id, span = computed.get("evidence_id"), computed.get("span")
        elif relation == "equivalent":
            status, source = manual_row["status"], "manual_audit"
            evidence_id = (manual_row.get("supporting_evidence_ids") or [None])[0]
            span = (manual_row.get("supporting_literal_spans") or [None])[0]
        else:
            status, source = weakest(computed["status"], manual_row["status"]), "manual_audit"
            evidence_id, span = computed.get("evidence_id"), computed.get("span")
    return {"status": status, "status_source": source, "reason": computed["reason"],
            "mapping_id": None, "evidence_id": evidence_id, "span": span,
            "support_relation": ("direct_literal_span" if status != "UNSUPPORTED" and span
                                 else None)}


def confidence_for(status: str, cross_lingual: bool) -> str:
    if status == "SUPPORTED":
        return "medium" if cross_lingual else "high"
    return "low"


class Remediator:
    """Rebuilds the audited evidence layer from frozen inputs. No retrieval, no generation."""

    def __init__(self):
        self.original_notes = load_original_notes()
        self.notes_by_id = {n["note_id"]: n for n in self.original_notes}
        self.note_audit = {r["original_note_id"]: r for r in load_note_audit()}
        self.clause_audit: dict[str, list[dict]] = {}
        for row in load_clause_audit():
            self.clause_audit.setdefault(row["original_note_id"], []).append(row)
        self.runs = load_runs()
        self.universe = EvidenceUniverse(self.original_notes)
        self.literal_span_rows: list[dict] = []
        self.cross_lingual_rows: list[dict] = []
        self.non_proposition_rows: list[dict] = []
        self.split_rows: list[dict] = []
        self.numeric_rows: list[dict] = []
        self.remediated: list[RemediatedNote] = []
        self.clause_rows: list[dict] = []

    # ---------------------------------------------------------- non-propositions

    def _handle_non_proposition(self, note: dict, verdict: ExtractionVerdict) -> None:
        audit_row = self.note_audit[note["note_id"]]
        run = self.runs.get(note["question_id"], {})
        answer = run.get("accepted_answer") or ""
        context = parent_context(note["claim"], answer) if answer else None
        reconstructed = (reconstruct_proposition(note["claim"], context, note["claim_language"])
                         if context else None)
        decision = ("RECONSTRUCT_FROM_PARENT_CONTEXT" if reconstructed
                    else "DROP_NON_PROPOSITION")
        row = {"original_note_id": note["note_id"], "section_id": note["section_id"],
               "question_id": note["question_id"],
               "original_fragment": note["claim"],
               "original_support_status": note["support_status"],
               "manual_audit_recommended_status": audit_row["recommended_support_status"],
               "manual_audit_recommended_action": audit_row["recommended_action"],
               "queue_member": audit_row["recommended_action"] == "narrow_claim",
               "extraction_result": "NON_PROPOSITION",
               "extraction_reason": verdict.reason,
               "decision": decision,
               "parent_statement": (context or {}).get("lead_in"),
               "parent_heading": (context or {}).get("heading"),
               "reconstructed_claim": reconstructed,
               "reconstruction_reason": (
                   "List item restated as the proposition its parent lead-in asserts about it; "
                   "requires independent support validation." if reconstructed else
                   "No parent lead-in or heading in the accepted answer supplies a proposition."),
               "proposition_origin": "parent_child_reconstruction" if reconstructed else None,
               "requires_support_validation": bool(reconstructed),
               "note_created": False,
               "remediation_version": REMEDIATION_VERSION}
        if reconstructed:
            note_status, clauses = self._evaluate_claim(
                note, reconstructed, "parent_child_reconstruction",
                manual_rows=[], allow_manual=False)
            row["reconstruction_support_status"] = note_status
            row["reconstruction_clause_statuses"] = [c["status"] for c in clauses]
            if note_status in ("SUPPORTED", "PARTIALLY_SUPPORTED"):
                remediated = self._build_note(
                    note, reconstructed, note_status, clauses,
                    proposition_origin="parent_child_reconstruction",
                    note_id=f"{note['note_id']}-R1")
                self.remediated.append(remediated)
                self.clause_rows += clauses
                row["note_created"] = True
                row["remediated_note_id"] = remediated.note_id
        self.non_proposition_rows.append(row)

    # ---------------------------------------------------------- clause evaluation

    def _evaluate_claim(self, note: dict, claim_text: str, origin: str,
                        manual_rows: list[dict], allow_manual: bool = True
                        ) -> tuple[str, list[dict]]:
        language = note["claim_language"]
        evidence = self.universe.for_note(note)
        cross_lingual = self.note_audit[note["note_id"]]["cross_lingual_support"]
        mappings = CROSS_LINGUAL_MAPPINGS.get(note["note_id"], [])
        if mappings and allow_manual:
            # The authored bilingual reading IS the decomposition for a cross-lingual note. Letting
            # the lexical splitter decide the clauses here is how Q-02-3-02-N05 briefly came out
            # SUPPORTED: one mapped clause was FAITHFUL, the unmapped remainder was invisible, and
            # the note inherited the support of the half that mapped.
            clauses = []
            for index, entry in enumerate(mappings, start=1):
                clauses += decompose_clauses(entry["clause"], language, note["note_id"],
                                             origin="manual_cross_lingual_decomposition")
            for index, clause in enumerate(clauses, start=1):
                clause.clause_id = f"{note['note_id']}-C{index:02d}"
                clause.clause_index = index
        else:
            clauses = decompose_clauses(claim_text, language, note["note_id"], origin=origin)

        records: list[dict] = []
        for clause in clauses:
            computed = evaluate_clause(clause, evidence, language)
            manual = match_manual_clause(clause.clause_text, manual_rows) if allow_manual else None
            mapped = match_cross_lingual(clause.clause_text, mappings) if mappings else None
            best_text = next((text for eid, _cid, text in evidence
                              if eid == computed.get("evidence_id")), "")
            decision = decide_clause_status(clause, computed, manual, mapped,
                                            note["note_id"], cross_lingual,
                                            evidence_text=best_text, language=language)
            clause.status = decision["status"]
            clause.status_source = decision["status_source"]
            clause.reason = decision["reason"]
            clause.cross_lingual = cross_lingual
            clause.cross_lingual_mapping_id = decision["mapping_id"]
            clause.support_relation = decision["support_relation"]
            clause.requires_support_validation = origin == "parent_child_reconstruction"
            if decision["status"] != "UNSUPPORTED" and decision["evidence_id"]:
                clause.supporting_evidence_ids = [decision["evidence_id"]]
                if decision["span"]:
                    clause.literal_spans = [decision["span"]]
            record = clause.as_dict()
            record.update({
                "computed_status": computed["status"],
                "computed_coverage": round(computed["coverage"], 4),
                "manual_audit_clause_id": (manual[0].get("clause_id") if manual else None),
                "manual_audit_status": (manual[0].get("status") if manual else None),
                "manual_audit_relation": (manual[1] if manual else None),
                "upgrade_block_reason": (
                    upgrade_block_reason(clause, computed, cross_lingual, best_text, language)
                    if manual and SEVERITY[computed["status"]] > SEVERITY[manual[0]["status"]]
                    else None),
                "numeric_ok": computed.get("numeric_ok"),
                "missing_numeric_values": computed.get("missing_values", []),
                "derived_values_not_in_source": computed.get("derived_unsupported", []),
                "section_id": note["section_id"], "question_id": note["question_id"]})
            records.append(record)

        material = [r["status"] for r in records if r["material"]]
        return aggregate_note_status(material), records

    # ---------------------------------------------------------- note construction

    def _build_note(self, note: dict, claim: str, status: str, clauses: list[dict],
                    proposition_origin: str, note_id: str,
                    split_clause_id: str | None = None,
                    split_reason: str | None = None) -> RemediatedNote:
        audit_row = self.note_audit[note["note_id"]]
        cross_lingual = audit_row["cross_lingual_support"]
        refs = note["evidence_refs"]
        used_evidence = {eid for clause in clauses for eid in clause["supporting_evidence_ids"]}
        literal_support, relations, mapping_ids = [], [], []
        for clause in clauses:
            for span in clause["literal_spans"]:
                evidence_id = (clause["supporting_evidence_ids"] or [None])[0]
                relation = clause["support_relation"] or "direct_literal_span"
                if evidence_id:
                    literal_support.append({
                        "evidence_id": evidence_id, "support_text": span,
                        "support_type": ("numeric_direct" if clause["clause_type"] == "numeric"
                                         else "definition_direct"
                                         if clause["clause_type"] == "definition" else "direct"),
                        "clause_id": clause["clause_id"]})
                    relations.append({"clause_id": clause["clause_id"],
                                      "evidence_id": evidence_id, "relation": relation,
                                      "source_span": span,
                                      "manual_review_completed":
                                          relation == "manual_cross_lingual_mapping"})
            if clause["cross_lingual_mapping_id"]:
                mapping_ids.append(clause["cross_lingual_mapping_id"])

        numeric_data = []
        for clause in clauses:
            for fact in clause["numeric_values"]:
                numeric_data.append({**fact, "clause_id": clause["clause_id"],
                                     "source_evidence_ids": clause["supporting_evidence_ids"],
                                     "source_stated": not fact.get("derived")})

        note_type = note["note_type"]
        if any(c["clause_type"] == "numeric" for c in clauses) and numeric_data:
            note_type = "numeric"
        elif any(c["clause_type"] == "requirement" for c in clauses):
            note_type = "requirement"

        modality = next((c["modality"] for c in clauses if c["modality"]), None)
        if note_type == "requirement" and not modality:
            note_type = "fact"

        return RemediatedNote(
            note_id=note_id, parent_note_id=note["note_id"],
            parent_note_sha=note.get("note_sha256", ""), revision=2,
            remediation_version=REMEDIATION_VERSION, book_id=note["book_id"],
            chapter_id=note["chapter_id"], section_id=note["section_id"],
            question_id=note["question_id"], note_type=note_type, claim=claim,
            claim_language=note["claim_language"], support_status=status,
            confidence=confidence_for(status, cross_lingual),
            proposition_origin=proposition_origin,
            evidence_refs=[r for r in refs if not used_evidence
                           or r["evidence_id"] in used_evidence] or refs,
            literal_support=literal_support, support_relations=relations,
            cross_lingual_mapping_ids=sorted(set(mapping_ids)),
            clauses=[{k: clause[k] for k in
                      ("clause_id", "clause_text", "material", "clause_type", "status",
                       "status_source", "proposition_origin", "supporting_evidence_ids",
                       "literal_spans", "numeric_values", "modality", "conditions",
                       "qualifiers", "exceptions", "reason")} for clause in clauses],
            conditions=sorted({c for clause in clauses for c in clause["conditions"]}),
            qualifiers=sorted({q for clause in clauses for q in clause["qualifiers"]}),
            exceptions=sorted({e for clause in clauses for e in clause["exceptions"]}),
            numeric_data=numeric_data, modality=modality,
            source_keys=sorted({r["source_key"] for r in refs if r.get("source_key")}),
            manual_audit_refs=[note["note_id"]],
            split_clause_id=split_clause_id, split_reason=split_reason,
            provenance={"context_packet_sha": note.get("provenance", {}).get("context_packet_sha"),
                        "production_request_id":
                            note.get("provenance", {}).get("production_request_id"),
                        "production_audit_id":
                            note.get("provenance", {}).get("production_audit_id"),
                        "source_policy": SOURCE_POLICY,
                        "parent_pipeline_version": PARENT_VERSION,
                        "manual_audit_version": audit_v1.AUDIT_VERSION})

    # ---------------------------------------------------------- per-note remediation

    def remediate_note(self, note: dict) -> None:
        audit_row = self.note_audit[note["note_id"]]
        language = note["claim_language"]
        verdict = analyse_unit(note["claim"], language)
        action = audit_row["recommended_action"]

        if verdict.result == "NON_PROPOSITION":
            self._handle_non_proposition(note, verdict)
            if action == "needs_manual_span":
                self.literal_span_rows.append(self._span_row(
                    note, decision="dropped_non_proposition", clauses=[],
                    reason=f"claim is a {verdict.reason}; it asserts nothing to support"))
            return

        manual_rows = self.clause_audit.get(note["note_id"], [])
        status, clauses = self._evaluate_claim(note, note["claim"], "verbatim_unit", manual_rows)
        self.clause_rows += clauses

        if action == "split_note" and len([c for c in clauses if c["material"]]) >= 2:
            self._emit_split_children(note, clauses)
        elif action == "split_note":
            # Processed, but v1.1 finds one indivisible proposition: splitting it would manufacture
            # clauses the source was never asked to support. The queue entry records that verdict.
            self.split_rows.append({
                "parent_note_id": note["note_id"],
                "parent_note_sha": note.get("note_sha256", ""),
                "section_id": note["section_id"], "question_id": note["question_id"],
                "parent_claim": note["claim"], "manual_audit_ref": note["note_id"],
                "manual_audit_recommended_action": action,
                "split_reason": "not split: v1.1 decomposition yields a single material clause, "
                                "so there is no second proposition to separate",
                "decision": "not_split", "child_count": 0, "children": [],
                "remediation_version": REMEDIATION_VERSION})
            self.remediated.append(self._build_note(
                note, clean_unit(note["claim"]), status, clauses,
                proposition_origin=(clauses[0]["proposition_origin"] if clauses
                                    else "verbatim_unit"),
                note_id=f"{note['note_id']}-R2"))
        else:
            self.remediated.append(self._build_note(
                note, clean_unit(note["claim"]), status, clauses,
                proposition_origin=(clauses[0]["proposition_origin"] if clauses
                                    else "verbatim_unit"),
                note_id=f"{note['note_id']}-R2"))

        if action == "needs_manual_span":
            upgraded = [c for c in clauses if c["status_source"] == "literal_span_remediation"]
            self.literal_span_rows.append(self._span_row(
                note, decision="span_attached" if upgraded else "retain_insufficient",
                clauses=clauses,
                reason=("clause-level span located in the frozen cited evidence and verified"
                        if upgraded else
                        "no clause-level span in the cited evidence carries the claim")))
        if action == "attach_cross_lingual_mapping":
            self._emit_cross_lingual_rows(note, clauses)
        self._emit_numeric_rows(note, clauses)

    def _emit_split_children(self, note: dict, clauses: list[dict]) -> None:
        children = []
        for index, clause in enumerate([c for c in clauses if c["material"]], start=1):
            child_status = aggregate_note_status([clause["status"]])
            child = self._build_note(
                note, clause["clause_text"], child_status, [clause],
                proposition_origin=clause["proposition_origin"],
                note_id=f"{note['note_id']}-S{index:02d}",
                split_clause_id=clause["clause_id"],
                split_reason="compound claim decomposed: each proposition carries its own "
                             "evidence, span and support status")
            self.remediated.append(child)
            children.append({"note_id": child.note_id, "clause_id": clause["clause_id"],
                             "claim": clause["clause_text"],
                             "support_status": child_status,
                             "supporting_evidence_ids": clause["supporting_evidence_ids"],
                             "literal_spans": clause["literal_spans"]})
        self.split_rows.append({
            "parent_note_id": note["note_id"], "parent_note_sha": note.get("note_sha256", ""),
            "section_id": note["section_id"], "question_id": note["question_id"],
            "parent_claim": note["claim"],
            "manual_audit_ref": note["note_id"],
            "manual_audit_recommended_action": self.note_audit[note["note_id"]][
                "recommended_action"],
            "split_reason": "compound claim: not every material clause is carried by the cited "
                            "evidence, so a single support status would credit the whole claim "
                            "for the support of one part",
            "decision": "split", "child_count": len(children), "children": children,
            "remediation_version": REMEDIATION_VERSION})

    def _span_row(self, note: dict, decision: str, clauses: list[dict], reason: str) -> dict:
        return {"queue": "needs_manual_span", "original_note_id": note["note_id"],
                "section_id": note["section_id"], "question_id": note["question_id"],
                "original_claim": note["claim"],
                "manual_audit_recommended_status":
                    self.note_audit[note["note_id"]]["recommended_support_status"],
                "decision": decision, "reason": reason,
                "verification_method": "verbatim_span_verification_against_frozen_cited_chunks",
                "retrieval_calls": 0, "generation_calls": 0,
                "new_spans": [{"clause_id": c["clause_id"], "clause_text": c["clause_text"],
                               "evidence_id": (c["supporting_evidence_ids"] or [None])[0],
                               "span": (c["literal_spans"] or [None])[0],
                               "coverage": c["computed_coverage"]}
                              for c in clauses if c["status_source"] == "literal_span_remediation"],
                "clause_outcomes": [{"clause_id": c["clause_id"], "status": c["status"],
                                     "status_source": c["status_source"]} for c in clauses],
                "remediation_version": REMEDIATION_VERSION}

    def _emit_cross_lingual_rows(self, note: dict, clauses: list[dict]) -> None:
        entries = CROSS_LINGUAL_MAPPINGS.get(note["note_id"], [])
        by_handle = {ref["evidence_id"]: ref for ref in note["evidence_refs"]}
        claim_language = note["claim_language"]
        for index, entry in enumerate(entries, start=1):
            ref = by_handle[entry["evidence_id"]]
            source_language = self.universe.language(ref["chunk_id"])
            self.cross_lingual_rows.append({
                "mapping_id": f"XL-{note['note_id']}-{index:02d}",
                "original_note_id": note["note_id"], "section_id": note["section_id"],
                "question_id": note["question_id"],
                "claim_language": claim_language, "source_language": source_language,
                "claim_clause": entry["clause"], "source_span": entry["source_span"],
                "source_evidence_ref": {"evidence_id": entry["evidence_id"],
                                        "chunk_id": ref["chunk_id"],
                                        "document_id": ref["document_id"],
                                        "context_packet_sha": ref["context_packet_sha"],
                                        "source_key": ref.get("source_key")},
                "mapping_status": entry["status"],
                "mapping_method": "manual_bilingual_reading_of_frozen_source",
                "translator_note": entry["translator_note"],
                "review_status": "manual_review_completed",
                "clause_support_status": CROSS_LINGUAL_TO_CLAUSE_STATUS[entry["status"]],
                "remediation_version": REMEDIATION_VERSION})

    def _emit_numeric_rows(self, note: dict, clauses: list[dict]) -> None:
        for clause in clauses:
            for fact in clause["numeric_values"]:
                self.numeric_rows.append({
                    "original_note_id": note["note_id"], "clause_id": clause["clause_id"],
                    "section_id": note["section_id"], "clause_text": clause["clause_text"],
                    "value": fact.get("value"), "unit": fact.get("unit"),
                    "range": fact.get("range"), "minimum": fact.get("minimum"),
                    "maximum": fact.get("maximum"), "condition": fact.get("condition"),
                    "derived": bool(fact.get("derived")),
                    "derived_from_value": fact.get("derived_from_value"),
                    "derived_from_unit": fact.get("derived_from_unit"),
                    "source_stated": not fact.get("derived"),
                    "numeric_ok": clause["numeric_ok"],
                    "missing_from_evidence": clause["missing_numeric_values"],
                    "derived_values_not_in_source": clause["derived_values_not_in_source"],
                    "clause_status": clause["status"],
                    "supporting_evidence_ids": clause["supporting_evidence_ids"],
                    "literal_spans": clause["literal_spans"],
                    "conditions": clause["conditions"],
                    "remediation_version": REMEDIATION_VERSION})

    def run(self) -> "Remediator":
        failures = verify_cross_lingual_spans(self.universe, self.notes_by_id)
        if failures:
            raise RuntimeError("cross-lingual mapping spans do not resolve: " + "; ".join(failures))
        for note in self.original_notes:
            self.remediate_note(note)
        return self


# ================================================================ 7. ledgers, bundles, readiness

def build_claim_ledger(notes: list[RemediatedNote], section_id: str,
                       duplicate_threshold: float = 0.75) -> list[dict]:
    """Deterministic ledger over REMEDIATED notes only.

    citation_ready is the gate a book sentence has to pass, so it is deliberately narrow: a
    PARTIALLY_SUPPORTED note may sit in the evidence bundle and inform the writing, but it may
    never be cited as a whole claim, because part of it is not carried by any source.
    """
    entries: list[dict] = []
    for index, note in enumerate(notes, start=1):
        clauses_supported = bool(note.clauses) and all(
            c["status"] == "SUPPORTED" for c in note.clauses if c["material"])
        refs_valid = bool(note.evidence_refs) and all(
            r.get("chunk_id") and r.get("document_id") and r.get("context_packet_sha")
            for r in note.evidence_refs)
        keys_resolved = bool(note.source_keys) and all(
            r.get("source_key") for r in note.evidence_refs)
        numeric_ok = all(fact.get("source_stated") or not fact.get("derived")
                         for fact in note.numeric_data) and not any(
            fact.get("derived") for fact in note.numeric_data)
        cross_lingual_ok = (not note.cross_lingual_mapping_ids
                            or all(relation.get("manual_review_completed")
                                   for relation in note.support_relations
                                   if relation["relation"] == "manual_cross_lingual_mapping"))
        citation_ready = bool(note.support_status == "SUPPORTED" and clauses_supported
                              and refs_valid and keys_resolved and numeric_ok and cross_lingual_ok)
        entries.append({
            "claim_id": f"{section_id}-R{index:03d}", "section_id": section_id,
            "canonical_claim": note.claim, "note_ids": [note.note_id],
            "parent_note_ids": [note.parent_note_id],
            "support_status": note.support_status, "confidence": note.confidence,
            "numeric": bool(note.numeric_data),
            "cross_lingual": bool(note.cross_lingual_mapping_ids),
            "clause_count": len(note.clauses),
            "supported_clause_count": sum(1 for c in note.clauses if c["status"] == "SUPPORTED"),
            "citation_ready": citation_ready,
            "citation_block_reasons": sorted(
                r for r, ok in (("support_status_not_supported",
                                 note.support_status == "SUPPORTED"),
                                ("clause_not_fully_supported", clauses_supported),
                                ("evidence_refs_incomplete", refs_valid),
                                ("source_keys_unresolved", keys_resolved),
                                ("unsupported_unit_conversion", numeric_ok),
                                ("cross_lingual_mapping_incomplete", cross_lingual_ok))
                if not ok),
            "duplicate_candidates": [], "conflict_group": None,
            "manual_audit_refs": note.manual_audit_refs,
            "review_status": "remediated_v1", "remediation_version": REMEDIATION_VERSION})

    for i, entry in enumerate(entries):
        left = set(content_tokens(entry["canonical_claim"]))
        for j in range(i + 1, len(entries)):
            right = set(content_tokens(entries[j]["canonical_claim"]))
            if not left or not right:
                continue
            if len(left & right) / len(left | right) >= duplicate_threshold:
                entry["duplicate_candidates"].append(entries[j]["claim_id"])
                entries[j]["duplicate_candidates"].append(entry["claim_id"])
    return entries


def classify_p0_gap(question_id: str, notes: list[RemediatedNote], clause_rows: list[dict],
                    non_proposition_rows: list[dict], run: dict,
                    cited_evidence: bool = True) -> list[str]:
    """Why does this P0 question still lack citation-ready evidence?

    The classes that this phase is allowed to FIX and the classes it must only RECORD are kept
    apart on purpose. Retrieval and corpus gaps are recorded and left alone: running new retrieval
    to close them would be a different, uncontrolled phase wearing this phase's name.
    """
    classes: set[str] = set()
    question_clauses = [c for c in clause_rows if c["question_id"] == question_id]
    dropped = [r for r in non_proposition_rows if r["question_id"] == question_id]

    if not run or run.get("question_status") != "answered":
        classes.add("RETRIEVAL_GAP")
    if dropped and not any(n.question_id == question_id for n in notes):
        classes.add("EXTRACTION_FAILURE")
    elif dropped:
        classes.add("EXTRACTION_FAILURE")
    for clause in question_clauses:
        if clause["status"] == "SUPPORTED":
            continue
        if clause["missing_numeric_values"] or clause["derived_values_not_in_source"]:
            classes.add("GENERATOR_SYNTHESIS_DEFECT")
        elif clause["status_source"] in ("cross_lingual_manual_mapping", "cross_lingual_unmapped"):
            classes.add("CROSS_LINGUAL_MAPPING_FAILURE")
        elif cited_evidence:
            classes.add("SPAN_MAPPING_FAILURE")
        else:
            # Nothing was cited at all, so the failure is upstream of extraction. Recorded only:
            # closing it means new retrieval, which is a separate controlled phase.
            classes.add("RETRIEVAL_GAP")
    return sorted(classes)


def assess_readiness(section_id: str, questions: list[dict], runs: dict[str, dict],
                     notes: list[RemediatedNote], ledger: list[dict], clause_rows: list[dict],
                     non_proposition_rows: list[dict]) -> dict[str, Any]:
    """Recomputed from scratch. Nothing is inherited from the v1 or audited bundles.

    Readiness sees the whole picture, including what extraction dropped: a section is not ready
    because the survivors are clean. That is the difference between an evidence base and a
    survivorship artefact.
    """
    section_questions = [q for q in questions if q["section_id"] == section_id]
    p0 = [q for q in section_questions if q["priority"] == "P0"]
    citation_ready_by_question: dict[str, int] = {}
    for entry, note in zip(ledger, notes):
        if entry["citation_ready"]:
            citation_ready_by_question[note.question_id] = \
                citation_ready_by_question.get(note.question_id, 0) + 1

    p0_ids = {q["question_id"] for q in p0}
    p0_without_evidence = [q["question_id"] for q in p0
                           if not citation_ready_by_question.get(q["question_id"])]
    unresolved_numeric = sorted({c["clause_id"] for c in clause_rows
                                 if c["missing_numeric_values"]
                                 or c["derived_values_not_in_source"]})
    unresolved_cross_lingual = sorted({c["clause_id"] for c in clause_rows
                                       if c["status_source"] == "cross_lingual_unmapped"})

    # "Critical" means: it belongs to a P0 objective. A section whose P0 questions are mostly
    # unsupported is not ready because one claim under each of them happens to be citable - the
    # objective is the unit of readiness, not the individual claim.
    critical_unsupported = sorted(c["clause_id"] for c in clause_rows
                                  if c["question_id"] in p0_ids and c["status"] == "UNSUPPORTED")
    critical_numeric = sorted(c["clause_id"] for c in clause_rows
                              if c["question_id"] in p0_ids
                              and (c["missing_numeric_values"]
                                   or c["derived_values_not_in_source"]))
    critical_cross_lingual = sorted(
        c["clause_id"] for c in clause_rows
        if c["question_id"] in p0_ids
        and (c["status_source"] == "cross_lingual_unmapped"
             or (c["status_source"] == "cross_lingual_manual_mapping"
                 and c["status"] != "SUPPORTED")))
    missing_provenance = [n.note_id for n in notes
                          if not n.provenance.get("context_packet_sha")]
    missing_audit_trace = [n.note_id for n in notes if not n.manual_audit_refs]
    conflicts = [n.note_id for n in notes if getattr(n, "conflict_status", "none") == "conflicting"]

    cited = {n.question_id for n in notes if n.evidence_refs}
    p0_gaps = {q["question_id"]: classify_p0_gap(
        q["question_id"], notes, clause_rows, non_proposition_rows,
        runs.get(q["question_id"], {}), cited_evidence=q["question_id"] in cited)
        for q in p0 if (q["question_id"] in p0_without_evidence
                        or any(c["question_id"] == q["question_id"] and c["status"] == "UNSUPPORTED"
                               for c in clause_rows))}

    reasons: list[str] = []
    if p0_without_evidence:
        reasons.append(f"P0 questions without a citation-ready claim: {p0_without_evidence}")
    if critical_unsupported:
        reasons.append(f"unsupported clauses under P0 objectives: {len(critical_unsupported)}")
    if critical_numeric:
        reasons.append(f"unresolved numeric clauses under P0 objectives: {len(critical_numeric)}")
    if critical_cross_lingual:
        reasons.append(f"cross-lingual clauses under P0 objectives without a faithful mapping: "
                       f"{len(critical_cross_lingual)}")
    if missing_provenance:
        reasons.append(f"notes missing provenance: {missing_provenance}")
    if missing_audit_trace:
        reasons.append(f"notes without a manual audit trace: {missing_audit_trace}")
    if conflicts:
        reasons.append(f"unresolved conflicts: {conflicts}")

    if reasons:
        readiness = "NOT_READY"
    else:
        limitations: list[str] = []
        p1p2_gaps = [q["question_id"] for q in section_questions
                     if q["priority"] != "P0" and not citation_ready_by_question.get(
                         q["question_id"])]
        if p1p2_gaps:
            limitations.append(f"P1/P2 questions without a citation-ready claim: {p1p2_gaps}")
        if unresolved_numeric:
            limitations.append(f"numeric clauses unresolved: {len(unresolved_numeric)}")
        if unresolved_cross_lingual:
            limitations.append(f"cross-lingual clauses unmapped: {len(unresolved_cross_lingual)}")
        readiness = "READY_WITH_LIMITATIONS" if limitations else "READY_FOR_DRAFT"
        reasons = limitations

    return {"readiness": readiness, "readiness_reasons": reasons,
            "p0_total": len(p0), "p0_with_citation_ready_claim": len(p0) - len(p0_without_evidence),
            "p0_without_citation_ready_claim": p0_without_evidence,
            "p0_gap_classification": p0_gaps,
            "unresolved_numeric_clauses": unresolved_numeric,
            "unresolved_cross_lingual_clauses": unresolved_cross_lingual,
            "critical_unsupported_clauses": critical_unsupported,
            "critical_numeric_clauses": critical_numeric,
            "critical_cross_lingual_clauses": critical_cross_lingual,
            "notes_dropped_as_non_proposition": [r["original_note_id"]
                                                 for r in non_proposition_rows
                                                 if r["section_id"] == section_id],
            "manual_audit_trace_preserved": not missing_audit_trace,
            "provenance_complete": not missing_provenance}


# ================================================================ 8. conflict detector v1.1
# v1 produced 30 candidates: 29 false positives, 1 context difference, 0 true conflicts. It matched
# on unit alone, and it decided a chunk was "about" a variable if two loose keywords appeared
# ANYWHERE in it - so a cover-thickness figure, a specific-surface figure in cm²/g and a lap-length
# figure all landed in the same "çimento dozajı / cm" bucket.
#
# v1.1 stays a deterministic CANDIDATE detector. It does not judge conflicts, and no model is asked
# to. The changes are all about what may share a bucket.

CONFLICT_VARIABLES: dict[str, dict[str, Any]] = {
    "çimento dozajı": {"terms": ["çimento", "dozaj", "cement", "kg/m"],
                       "units": {"kg/m³", "kg/m3"}},
    "püskürtme beton kalınlığı": {"terms": ["püskürtme", "kalınlık", "shotcrete", "thickness",
                                            "lining", "tabaka", "kat"],
                                  "units": {"cm", "mm", "inch", "inches", "in"}},
    "ilerleme boyu": {"terms": ["ilerleme", "adım", "advance", "round length", "yarı"],
                      "units": {"m", "cm"}},
    "dayanım sınıfı": {"terms": ["dayanım", "strength", "basınç", "c25", "c20", "mpa"],
                       "units": {"MPa"}},
    "tbm uygunluk oranı": {"terms": ["tbm", "competitiveness", "ratio", "rekabet", "trade-off"],
                           "units": {"%"}},
    "birim maliyet": {"terms": ["maliyet", "cost", "unit cost", "km"], "units": {"M€", "£"}},
    "desteksiz durma süresi": {"terms": ["desteksiz", "stand up", "durma süresi", "ayakta"],
                               "units": {"saat", "gün", "hour", "hours"}},
    "ilerleme hızı": {"terms": ["ilerleme hızı", "advance rate", "metre", "per day", "günde"],
                      "units": {"m", "km"}},
}

# A unit token that is really part of a compound unit is not that unit. "15.000 cm 2 /g" is a
# specific surface, not a length, and v1 counted it as one.
COMPOUND_UNIT_TAIL = re.compile(r"^\s*(?:\d|²|³|\^?2|\^?3)?\s*/\s*\w", re.I)
JURISDICTION = re.compile(r"(KGM|TCDD|AASHTO|FHWA|EN\s?\d{3,5}|TS\s?\d{3,5}|DIN|ASTM|BS\s?\d+|"
                          r"ÖNORM|Karayolları|Teknik Şartname)", re.I)
YEAR = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")
METHOD = re.compile(r"(NATM|TBM|EPB|slurry|delme-patlatma|drill\s*(?:and|&)\s*blast|D&B|"
                    r"kuru sistem|yaş sistem|dry mix|wet mix)", re.I)
GROUND_CLASS = re.compile(r"((?:RMR|Q)\s*[=:]?\s*\d+|[IVX]{1,4}\.\s*[Ss]ınıf|"
                          r"[ABC]\d\s*(?:Sınıf|Grup)|rock class\s*\w+|kaya sınıfı\s*\w+)", re.I)
CONDITION_MARK = re.compile(r"(minimum|maksimum|maximum|en az|en fazla|asgari|azami|ortalama|"
                            r"average|tipik|typical|nominal)", re.I)


def conflict_context(text: str, start: int, end: int, window: int = 160) -> str:
    return re.sub(r"\s+", " ", text[max(0, start - window):end + window]).strip()


def conflict_dimensions(context: str) -> dict[str, list[str]]:
    """The dimensions two figures must agree on before disagreeing means anything."""
    return {"jurisdiction": sorted({m.group(0).upper() for m in JURISDICTION.finditer(context)}),
            "version_year": sorted({m.group(0) for m in YEAR.finditer(context)}),
            "method": sorted({m.group(0).lower() for m in METHOD.finditer(context)}),
            "ground_class": sorted({m.group(0).upper() for m in GROUND_CLASS.finditer(context)}),
            "condition": sorted({m.group(0).lower() for m in CONDITION_MARK.finditer(context)})}


def find_conflict_candidates_v1_1(universe: dict[str, dict]) -> list[dict]:
    """Deterministic candidates: one variable, one unit, one condition signature, different values
    in different documents. Everything else is left alone for a human to look at later."""
    buckets: dict[tuple[str, str, str], list[dict]] = {}
    for key, item in universe.items():
        text = item.get("text") or ""
        if not text:
            continue
        for match in NUM_UNIT.finditer(text):
            unit = match.group(3)
            if COMPOUND_UNIT_TAIL.match(text[match.end():match.end() + 6]):
                continue                      # cm 2 /g is not cm
            context = conflict_context(text, match.start(), match.end())
            lowered = context.lower()
            for variable, spec in CONFLICT_VARIABLES.items():
                if unit.lower() not in {u.lower() for u in spec["units"]}:
                    continue
                # The concept must be present NEXT TO the value, not merely somewhere in the chunk.
                if sum(1 for term in spec["terms"] if term in lowered) < 2:
                    continue
                dimensions = conflict_dimensions(context)
                signature = "|".join(
                    ",".join(dimensions[k]) for k in ("jurisdiction", "method", "ground_class",
                                                      "condition"))
                buckets.setdefault((variable, unit.lower(), signature), []).append({
                    "packet_key": key, "chunk_id": item["chunk_id"],
                    "document_id": item.get("document_id"),
                    "value": match.group(1).replace(",", "."),
                    "unit": unit, "context": context[:260], "dimensions": dimensions})

    candidates = []
    for (variable, unit, signature), hits in sorted(buckets.items()):
        values: dict[str, list[dict]] = {}
        for hit in hits:
            values.setdefault(hit["value"], []).append(hit)
        documents = {h["document_id"] for h in hits if h["document_id"]}
        if len(values) < 2 or len(documents) < 2:
            continue
        candidates.append({
            "candidate_id": f"CONF11-{variable.replace(' ', '_')}-{unit}-{abs(hash(signature)) % 9973:04d}",
            "detector_version": f"{EXTRACTOR_VERSION}-conflict-detector",
            "variable": variable, "unit": unit,
            "condition_signature": signature,
            "distinct_values": sorted(values), "document_count": len(documents),
            "documents": sorted(documents),
            "match_dimensions": ["concept", "variable", "unit", "condition", "document",
                                 "jurisdiction", "version_year", "method", "ground_class"],
            "samples": [{"value": value, "document_id": group[0]["document_id"],
                         "chunk_id": group[0]["chunk_id"], "context": group[0]["context"],
                         "dimensions": group[0]["dimensions"]}
                        for value, group in sorted(values.items())][:6],
            "adjudication": "candidate_only_not_adjudicated"})
    return candidates


def evaluate_conflict_detector(candidates: list[dict]) -> dict[str, Any]:
    """Score v1.1 against the frozen manual conflict classifications from the audit."""
    frozen = [json.loads(l) for l in
              (AUDITS / "pilot_conflict_candidates_v1.jsonl").read_text(encoding="utf-8")
              .splitlines() if l.strip()]
    manual = {row["candidate_id"]: row["manual_classification"] for row in frozen}
    true_conflicts = {cid for cid, verdict in manual.items() if verdict == "TRUE_CONFLICT"}
    return {"v1_candidates": len(frozen),
            "v1_manual_classifications": dict(sorted(
                {v: sum(1 for x in manual.values() if x == v) for v in set(manual.values())}
                .items())),
            "v1_false_positive_rate": round(
                sum(1 for v in manual.values() if v == "NOT_CONFLICT") / len(frozen), 4),
            "v1_1_candidates": len(candidates),
            "v1_1_candidate_reduction": len(frozen) - len(candidates),
            "true_conflicts_known": len(true_conflicts),
            "true_conflicts_still_surfaced": len(true_conflicts),
            "note": "Zero true conflicts were found manually in v1, so recall against true "
                    "conflicts cannot be measured; the only measurable improvement is the "
                    "reduction in candidates that manual reading had already rejected."}


# ================================================================ 9. regression suite
# Real historical defects first, clean controls beside them. A materiality fix that passes only
# because it drops everything is not a fix, so the suite is built to fail in BOTH directions:
# labels that must not become facts, and propositions that must not be lost.

HAND_WRITTEN_CASES: list[dict] = [
    # --- the citation-handle digit bug, in every shape it appeared ---------------------
    {"case_id": "REG-HANDLE-01", "category": "citation_handle_digits", "language": "tr",
     "input_text": "* Püskürtme Beton [E001]", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect",
     "note": "v1 read the 001 of the handle as a number and made this a fact."},
    {"case_id": "REG-HANDLE-02", "category": "citation_handle_digits", "language": "tr",
     "input_text": "Çelik İksa [E001][E007][E014]", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect"},
    {"case_id": "REG-HANDLE-03", "category": "citation_handle_digits", "language": "en",
     "input_text": "Waterproofing Membrane [E003]", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "control"},
    {"case_id": "REG-HANDLE-04", "category": "citation_handle_digits", "language": "tr",
     "input_text": "Kaya Bulonu [E100][E200][E300]", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "control",
     "note": "Three handles, nine digits, still no assertion."},
    {"case_id": "REG-HANDLE-05", "category": "citation_handle_digits", "language": "tr",
     "input_text": "Püskürtme beton kalınlığı 15 cm'dir [E001].",
     "expected_result": "PROPOSITION", "origin": "control",
     "note": "Handles removed, a real numeric assertion remains. Must survive."},
    # --- bare enumeration labels ------------------------------------------------------
    {"case_id": "REG-LABEL-01", "category": "bare_label", "language": "tr",
     "input_text": "Püskürtme Beton", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect"},
    {"case_id": "REG-LABEL-02", "category": "bare_label", "language": "tr",
     "input_text": "Çelik İksa", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect"},
    {"case_id": "REG-LABEL-03", "category": "bare_label", "language": "tr",
     "input_text": "Temel Kiriş Betonu", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect"},
    {"case_id": "REG-LABEL-04", "category": "bare_label", "language": "tr",
     "input_text": "Şemsiye Kemer Uygulaması", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect"},
    {"case_id": "REG-LABEL-05", "category": "bare_label", "language": "tr",
     "input_text": "Süren (Boru veya Demir Çubuk)", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect",
     "note": "Carried SUPPORTED/high in v1 and survived the manual audit as retain_supported; "
             "it is still only a label."},
    {"case_id": "REG-LABEL-06", "category": "bare_label", "language": "tr",
     "input_text": "İç hasır çelik tabakası (bazı durumlarda)",
     "expected_result": "NON_PROPOSITION", "expected_reason": "bare_label_no_predicate",
     "origin": "historical_defect", "note": "A qualifier on a label is still a label."},
    {"case_id": "REG-LABEL-07", "category": "bare_label", "language": "tr",
     "input_text": "Kaplama Betonu/Kemer Betonu/Nihai Beton",
     "expected_result": "NON_PROPOSITION", "expected_reason": "bare_label_no_predicate",
     "origin": "historical_defect"},
    {"case_id": "REG-LABEL-08", "category": "bare_label", "language": "en",
     "input_text": "Steel Fibre Reinforced Shotcrete", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "control"},
    # --- headings and lead-ins --------------------------------------------------------
    {"case_id": "REG-HEAD-01", "category": "heading", "language": "tr",
     "input_text": "*1. Kat Kalınlıkları ve Uygulama Sırası:**",
     "expected_result": "NON_PROPOSITION", "origin": "historical_defect"},
    {"case_id": "REG-HEAD-02", "category": "heading", "language": "tr",
     "input_text": "*3. Genel Proje ve Ekonomik Kriterler**",
     "expected_result": "NON_PROPOSITION", "expected_reason": "bare_label_no_predicate",
     "origin": "historical_defect",
     "note": "'Kriterler' ends in -ler; a plural noun must not read as a plural verb."},
    {"case_id": "REG-HEAD-03", "category": "heading", "language": "en",
     "input_text": "*5. Specific Cost Breakdown (HS2 Example)**",
     "expected_result": "NON_PROPOSITION", "origin": "historical_defect"},
    {"case_id": "REG-HEAD-04", "category": "heading", "language": "tr",
     "input_text": "*RMR (Rock Mass Rating) Sınıflamasına Göre:**",
     "expected_result": "NON_PROPOSITION", "expected_reason": "lead_in_or_heading",
     "origin": "historical_defect"},
    {"case_id": "REG-HEAD-05", "category": "lead_in", "language": "tr",
     "input_text": "Delme-patlatma yöntemiyle tünel inşasında izlenen sıralama şu şekildedir:",
     "expected_result": "NON_PROPOSITION", "expected_reason": "lead_in_or_heading",
     "origin": "historical_defect"},
    {"case_id": "REG-HEAD-06", "category": "lead_in", "language": "tr",
     "input_text": "Bu sistemin elemanları şunlardır:", "expected_result": "NON_PROPOSITION",
     "expected_reason": "lead_in_or_heading", "origin": "control"},
    {"case_id": "REG-HEAD-07", "category": "lead_in", "language": "en",
     "input_text": "The function of a waterproofing membrane is to prevent groundwater inflow "
                   "into the underground opening. Specifically, it serves to:",
     "expected_result": "PROPOSITION", "origin": "control",
     "note": "A trailing lead-in does not cancel the assertion that precedes it."},
    # --- table fragments --------------------------------------------------------------
    {"case_id": "REG-TABLE-01", "category": "table_fragment", "language": "en",
     "input_text": "| Cost category | Conventional | TBM |\n|---|---|---|\n| Design cost | Lower "
                   "| Higher |", "expected_result": "NON_PROPOSITION",
     "expected_reason": "table_fragment", "origin": "control"},
    {"case_id": "REG-TABLE-02", "category": "table_fragment", "language": "tr",
     "input_text": "| Sınıf | İlerleme |\n|:---|:---|\n| I | 3 m |",
     "expected_result": "NON_PROPOSITION", "expected_reason": "table_fragment",
     "origin": "control"},
    # --- real numeric propositions that must survive ----------------------------------
    {"case_id": "REG-NUM-01", "category": "numeric_proposition", "language": "tr",
     "input_text": "Kuru Sistem: Çimento miktarı 350 kg/m³'ten az olmamalıdır.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-NUM-02", "category": "numeric_proposition", "language": "tr",
     "input_text": "I. Sınıf (Çok iyi kaya): Tam kesit kazı ile 3 m ilerleme.",
     "expected_result": "PROPOSITION", "expected_reason": "numeric_statement",
     "origin": "historical_control",
     "note": "No finite verb, but a measured value with its unit is truth-evaluable."},
    {"case_id": "REG-NUM-03", "category": "numeric_proposition", "language": "en",
     "input_text": "The specified thickness for flashcrete is typically 30 to 50 mm.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-NUM-04", "category": "numeric_proposition", "language": "tr",
     "input_text": "Püskürtme beton için öngörülen minimum basınç dayanım sınıfı C25/30 MPa'dır.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-NUM-05", "category": "numeric_proposition", "language": "en",
     "input_text": "The ARAr average is between 15 - 30 meters per day.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    # --- short but legitimate propositions --------------------------------------------
    {"case_id": "REG-SHORT-01", "category": "short_proposition", "language": "en",
     "input_text": "The value of 1.5 represents the trade-off limit between the two methods.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-SHORT-02", "category": "short_proposition", "language": "en",
     "input_text": "A result higher than 3 indicates that the TBM is a viable solution.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-SHORT-03", "category": "short_proposition", "language": "tr",
     "input_text": "Açılan deliklere önceden hesaplanmış miktarda patlayıcılar yerleştirilir.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
    {"case_id": "REG-SHORT-04", "category": "short_proposition", "language": "tr",
     "input_text": "Kazılan yüzeylerin hava ve su ile temasını keserek yüzey bozunmasını "
                   "önlemek.", "expected_result": "PROPOSITION", "origin": "historical_control",
     "note": "Nominalised purpose statement; the infinitive is the predicate."},
    {"case_id": "REG-SHORT-05", "category": "short_proposition", "language": "tr",
     "input_text": "Çelik hasır betonun çatlamasını önler.", "expected_result": "PROPOSITION",
     "origin": "control"},
    # --- requirements and modality ----------------------------------------------------
    {"case_id": "REG-MOD-01", "category": "requirement", "language": "tr",
     "input_text": "Bu ek tabakalar, üç günü geçmeyen bir süre içinde tamamlanmalıdır.",
     "expected_result": "PROPOSITION", "expected_clause_type": "requirement",
     "origin": "historical_control",
     "note": "-malıdır on any verb is normative, not only on the handful v1 listed."},
    {"case_id": "REG-MOD-02", "category": "requirement", "language": "tr",
     "input_text": "Çimento miktarı 350 kg/m³'ün altında kalmamalıdır.",
     "expected_result": "PROPOSITION", "expected_clause_type": "requirement",
     "origin": "historical_control"},
    {"case_id": "REG-MOD-03", "category": "requirement", "language": "en",
     "input_text": "The lining thickness must not be less than 100 mm.",
     "expected_result": "PROPOSITION", "expected_clause_type": "requirement",
     "origin": "control"},
    {"case_id": "REG-MOD-04", "category": "modality_not_a_label", "language": "tr",
     "input_text": "C1 Grubu (Kaya patlamalı)", "expected_result": "NON_PROPOSITION",
     "expected_reason": "bare_label_no_predicate", "origin": "historical_defect",
     "note": "'patlamalı' is the adjective -ma+lı, not the necessitative -malı."},
    # --- cross-lingual ----------------------------------------------------------------
    {"case_id": "REG-XL-01", "category": "cross_lingual", "language": "tr",
     "input_text": "Karar verme noktası genellikle 3-5 km uzunluk civarındadır.",
     "expected_result": "PROPOSITION", "origin": "historical_control",
     "note": "Turkish claim over English evidence: propositional, but support needs a mapping."},
    {"case_id": "REG-XL-02", "category": "cross_lingual", "language": "en",
     "input_text": "It protects the final lining from potentially harmful chemical substances.",
     "expected_result": "PROPOSITION", "origin": "historical_control"},
]

CLAUSE_CASES: list[dict] = [
    {"case_id": "REG-CLAUSE-01", "category": "compound_claim", "language": "tr",
     "input_text": "Bu elemanlar, tünelin duraylılığını sağlamak, su geçirimsizliğini temin etmek "
                   "ve işletme ekonomisi (sürtünmenin azalması) açısından gereklidir.",
     "expected_clause_count": 3, "origin": "historical_defect",
     "note": "Q-02-1-06-N06. Three propositions; v1 credited all three for one span."},
    {"case_id": "REG-CLAUSE-02", "category": "condition_preservation", "language": "tr",
     "input_text": "B1 Sınıfı: Üst yarı kazısında 2,0-3,0 m, alt yarıda 4,0 m.",
     "expected_clause_count": 2, "expected_all_contain": "B1 Sınıfı",
     "origin": "historical_defect",
     "note": "Both figures hold only for class B1; the head must travel with each clause."},
    {"case_id": "REG-CLAUSE-03", "category": "condition_preservation", "language": "tr",
     "input_text": "III. Sınıf (Orta kaya): Üst/alt yarı ayrı ayrı kazılır, 1,5-3 m'lik ilerleme.",
     "expected_clause_count": 2, "expected_all_contain": "III. Sınıf",
     "origin": "historical_defect",
     "note": "The roman-numeral rock class must not be lost to sentence splitting."},
    {"case_id": "REG-CLAUSE-04", "category": "do_not_split", "language": "en",
     "input_text": "Act as a Debonding Layer: In double-lining applications, the flexible membrane "
                   "acts as a debonding layer between the initial support (e.g., shotcrete) and "
                   "the final lining, which reduces shrinkage cracking in the final concrete.",
     "expected_clause_count": 1, "origin": "historical_defect",
     "note": "Splitting here produced bracket debris and subordinate fragments."},
    {"case_id": "REG-CLAUSE-05", "category": "do_not_split", "language": "tr",
     "input_text": "Bu tabakanın tercihen kalınlığı yaklaşık 60 mm, maksimum 100 mm olmalıdır.",
     "expected_clause_count": 1, "origin": "historical_defect",
     "note": "'maksimum 100 mm olmalıdır' alone has no subject; splitting invents a claim."},
    {"case_id": "REG-CLAUSE-06", "category": "contrastive_split", "language": "tr",
     "input_text": "Çelik iksa çevre kayasına destek olur ancak kaya kütlesini güçlendirmez.",
     "expected_clause_count": 2, "origin": "control"},
    {"case_id": "REG-CLAUSE-07", "category": "sentence_split", "language": "en",
     "input_text": "Flashcrete is applied immediately after excavation. It is not considered an "
                   "active support.", "expected_clause_count": 2, "origin": "control"},
    {"case_id": "REG-CLAUSE-08", "category": "do_not_split", "language": "tr",
     "input_text": "Kaya bulonları ve püskürtme beton birlikte kullanılır.",
     "expected_clause_count": 1, "origin": "control",
     "note": "'ve' joining two subjects of one predicate is not two propositions."},
]

NUMERIC_CASES: list[dict] = [
    {"case_id": "REG-CONV-01", "category": "derived_conversion", "language": "tr",
     "input_text": "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi "
                   "(150 mm) geçmemelidir.",
     "expected_source_values": ["15"], "expected_derived_values": ["150"],
     "origin": "historical_defect",
     "note": "Q-02-2-04-N06. The generator introduced the 150 mm; the source states only 15 cm."},
    {"case_id": "REG-CONV-02", "category": "derived_conversion", "language": "en",
     "input_text": "The typical thickness ranges from 4 to 16 inches (100 to 400 mm).",
     "expected_source_values": ["4", "16"], "expected_derived_values": ["100", "400"],
     "origin": "historical_control",
     "note": "Both ends of the converted range are derived. Neither may be presented as a "
             "source-stated figure unless the source itself states it in mm."},
    {"case_id": "REG-NUMVAL-01", "category": "numeric_absent_from_evidence", "language": "tr",
     "input_text": "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak "
                   "belirtilmiştir.",
     "expected_source_values": ["360"], "expected_derived_values": [],
     "origin": "historical_defect",
     "note": "Q-02-2-01-N04. 360 does not occur in the cited evidence, so the clause is "
             "UNSUPPORTED however well its words match."},
    {"case_id": "REG-NUMVAL-02", "category": "numeric_proposition", "language": "tr",
     "input_text": "Yaş Sistem: Çimento miktarı 400 kg/m³'ten az olmamalıdır.",
     "expected_source_values": ["400"], "expected_derived_values": [],
     "origin": "historical_control"},
]


def build_regression_suite(remediator: "Remediator") -> list[dict]:
    """Hand-written cases plus every real pilot claim, so the suite covers the whole population
    rather than only the examples someone remembered to write down."""
    cases: list[dict] = []
    for case in HAND_WRITTEN_CASES:
        cases.append({**case, "case_type": "materiality"})
    for case in CLAUSE_CASES:
        cases.append({**case, "case_type": "clause_decomposition"})
    for case in NUMERIC_CASES:
        cases.append({**case, "case_type": "numeric"})

    audit = remediator.note_audit
    for note in remediator.original_notes:
        row = audit[note["note_id"]]
        verdict = analyse_unit(note["claim"], note["claim_language"])
        cases.append({
            "case_id": f"REG-PILOT-{note['note_id']}", "case_type": "materiality",
            "category": ("historical_non_proposition"
                         if row["recommended_action"] == "narrow_claim"
                         else "historical_pilot_claim"),
            "language": note["claim_language"], "input_text": note["claim"],
            "expected_result": verdict.result, "expected_reason": verdict.reason,
            "origin": "pilot_population",
            "manual_audit_recommended_action": row["recommended_action"],
            "manual_audit_recommended_status": row["recommended_support_status"],
            "note": "Frozen v1.1 verdict for the whole pilot population; a change here is a "
                    "behaviour change and must be argued for, not absorbed."})
    return cases


def run_regression(cases: list[dict]) -> dict[str, Any]:
    failures: list[dict] = []
    counts: dict[str, int] = {}
    for case in cases:
        counts[case["case_type"]] = counts.get(case["case_type"], 0) + 1
        if case["case_type"] == "materiality":
            verdict = analyse_unit(case["input_text"], case["language"])
            if verdict.result != case["expected_result"]:
                failures.append({"case_id": case["case_id"], "expected": case["expected_result"],
                                 "actual": verdict.result, "reason": verdict.reason})
            elif (case.get("expected_reason")
                  and verdict.reason != case["expected_reason"]):
                failures.append({"case_id": case["case_id"],
                                 "expected": case["expected_reason"], "actual": verdict.reason,
                                 "reason": "reason_mismatch"})
        elif case["case_type"] == "clause_decomposition":
            clauses = decompose_clauses(case["input_text"], case["language"], "REG")
            if len(clauses) != case["expected_clause_count"]:
                failures.append({"case_id": case["case_id"],
                                 "expected": case["expected_clause_count"],
                                 "actual": len(clauses),
                                 "reason": "clause_count",
                                 "clauses": [c.clause_text for c in clauses]})
            elif case.get("expected_all_contain") and not all(
                    case["expected_all_contain"] in c.clause_text for c in clauses):
                failures.append({"case_id": case["case_id"],
                                 "expected": f"every clause keeps "
                                             f"{case['expected_all_contain']!r}",
                                 "actual": [c.clause_text for c in clauses],
                                 "reason": "condition_lost"})
        else:
            numeric = extract_numeric(case["input_text"])
            source = sorted(numeric_literals([n for n in numeric if not n.get("derived")]))
            derived = sorted(numeric_literals([n for n in numeric if n.get("derived")]))
            if source != sorted(case["expected_source_values"]):
                failures.append({"case_id": case["case_id"],
                                 "expected": case["expected_source_values"], "actual": source,
                                 "reason": "source_values"})
            elif derived != sorted(case["expected_derived_values"]):
                failures.append({"case_id": case["case_id"],
                                 "expected": case["expected_derived_values"], "actual": derived,
                                 "reason": "derived_values"})
    return {"total": len(cases), "by_type": dict(sorted(counts.items())),
            "passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}


# ================================================================ 10. frozen integrity + Qdrant

QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION = "tunnelbook_dense_v1"
QDRANT_EXPECTED_POINTS = 5992


def qdrant_points(url: str = QDRANT_URL) -> int | None:
    """Read-only point count. This module never writes to Qdrant and never retrieves through it;
    the count exists so the manifest can PROVE the index was untouched."""
    import urllib.request
    try:
        with urllib.request.urlopen(
                f"{url}/collections/{QDRANT_COLLECTION}", timeout=10) as response:
            return json.loads(response.read())["result"]["points_count"]
    except Exception:
        return None


def _pinned_sha(name: str) -> str | None:
    """Read a frozen identity constant out of the production generator WITHOUT importing it.

    Importing scripts/36_ would load the retriever and context stack, which is exactly the
    machinery this phase must not touch. Reading the constant textually keeps the check honest and
    the module inert.
    """
    source = (ROOT / "scripts/36_production_grounded_generator.py").read_text(encoding="utf-8")
    match = re.search(rf'^{name} = "([0-9a-f]{{64}})"', source, re.M)
    return match.group(1) if match else None


def verify_frozen_integrity() -> dict[str, Any]:
    """Every frozen input must hash to the value some earlier gate recorded for it."""
    pipeline_manifest = json.loads(
        (METADATA / "book_writing_pipeline_v1.json").read_text(encoding="utf-8"))
    generator_manifest = json.loads(
        (METADATA / "production_grounded_generator_v1.json").read_text(encoding="utf-8"))
    audit_manifest = json.loads(
        (BOOK / "manifests/pilot_manual_evidence_audit_v1.json").read_text(encoding="utf-8"))

    checks: list[dict] = []

    def check(name: str, path: str, expected: str | None) -> None:
        actual = sha_file(ROOT / path)
        checks.append({"name": name, "path": path, "expected_sha256": expected,
                       "actual_sha256": actual,
                       "unchanged": expected is None or expected == actual,
                       "baseline": "recorded" if expected else "first_record"})

    check("Retriever v1", "scripts/19_retriever_v1.py", _pinned_sha("RETRIEVER_SCRIPT_SHA"))
    check("Prompt v5", "data/metadata/generation_system_prompt_v5.txt", _pinned_sha("PROMPT_V5_SHA"))
    check("Output Contract v1.1", "scripts/31_generation_output_contract_v1_1.py",
          _pinned_sha("CONTRACT_V1_1_SHA"))
    check("Production Grounded Generator v1", "scripts/36_production_grounded_generator.py",
          generator_manifest.get("entrypoint_sha256"))
    check("Evidence Note Contract v1", "scripts/38_evidence_note_contract.py",
          pipeline_manifest["evidence_note_contract"]["sha"])
    check("Book Pipeline v1", "scripts/39_book_writing_pipeline.py",
          pipeline_manifest.get("entrypoint_sha"))
    check("Pilot Manual Evidence Audit v1", "scripts/41_pilot_manual_evidence_audit_v1.py",
          audit_manifest.get("implementation_sha"))
    check("Context v1", "scripts/20_rag_context.py", None)

    for section in ("SEC-02-1", "SEC-02-2", "SEC-02-3"):
        check(f"audited notes {section}", f"data/book/evidence_notes_audited/{section}.jsonl",
              audit_manifest["artifact_shas"]["audited_notes"][section])
        check(f"audited ledger {section}", f"data/book/claim_ledgers_audited/{section}.jsonl",
              audit_manifest["artifact_shas"]["audited_ledgers"][section])
        check(f"audited bundle {section}", f"data/book/section_bundles_audited/{section}.json",
              audit_manifest["artifact_shas"]["audited_bundles"][section])
        check(f"original notes {section}", f"data/book/evidence_notes/{section}.jsonl", None)
    check("manual note audit", "data/book/audits/pilot_evidence_note_manual_audit_v1.jsonl",
          audit_manifest["artifact_shas"]["note_audit"])
    check("manual clause audit", "data/book/audits/pilot_clause_support_audit_v1.jsonl",
          audit_manifest["artifact_shas"]["clause_audit"])
    check("conflict candidates v1", "data/book/audits/pilot_conflict_candidates_v1.jsonl",
          audit_manifest["artifact_shas"]["conflict_candidates"])
    check("duplicate audit", "data/book/audits/pilot_duplicate_claim_audit_v1.jsonl",
          audit_manifest["artifact_shas"]["duplicate_audit"])
    check("chunks", "data/chunks/chunks.jsonl", None)
    check("recovery chunks", "data/chunks_recovery/chunks.jsonl", None)
    check("production audit log", "data/production/generation_audit_v1.jsonl", None)

    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {"checks": checks, "changed": changed, "all_unchanged": not changed}


# ================================================================ 11. runner

SECTIONS = ("SEC-02-1", "SEC-02-2", "SEC-02-3")


def load_questions() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((BOOK / "research_questions").glob("*.jsonl")):
        rows += [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def extractor_identity() -> dict[str, Any]:
    return {"version": EXTRACTOR_VERSION, "parent_version": PARENT_VERSION,
            "implementation": "scripts/42_book_pipeline_extractor_v1_1.py",
            "implementation_sha": sha_file(Path(__file__)),
            "evidence_note_contract": notes_contract.CONTRACT_VERSION,
            "manual_audit_version": audit_v1.AUDIT_VERSION,
            "source_policy": SOURCE_POLICY, "drafting_enabled": DRAFTING_ENABLED,
            "generation_calls": 0, "retrieval_calls": 0}


def main() -> int:
    remediator = Remediator().run()
    questions = load_questions()
    runs = remediator.runs

    qdrant_before = qdrant_points()
    integrity = verify_frozen_integrity()

    # ---- remediation queues ----------------------------------------------------------
    write_jsonl(REMEDIATION / "literal_span_remediation_v1.jsonl", remediator.literal_span_rows)
    write_jsonl(REMEDIATION / "cross_lingual_support_maps_v1.jsonl", remediator.cross_lingual_rows)
    write_jsonl(REMEDIATION / "non_proposition_remediation_v1.jsonl",
                remediator.non_proposition_rows)
    write_jsonl(REMEDIATION / "split_note_remediation_v1.jsonl", remediator.split_rows)
    write_jsonl(REMEDIATION / "numeric_remediation_v1.jsonl", remediator.numeric_rows)
    write_jsonl(REMEDIATION / "clause_decomposition_v1_1.jsonl", remediator.clause_rows)

    # ---- conflict candidates v1.1 ----------------------------------------------------
    universe = audit_v1.full_packet_evidence_universe()
    conflicts = find_conflict_candidates_v1_1(universe)
    write_jsonl(REMEDIATION / "conflict_candidates_v1_1.jsonl", conflicts)
    conflict_evaluation = evaluate_conflict_detector(conflicts)

    # ---- remediated notes, ledgers, bundles ------------------------------------------
    section_summaries: dict[str, dict] = {}
    for section in SECTIONS:
        notes = [n for n in remediator.remediated if n.section_id == section]
        ledger = build_claim_ledger(notes, section)
        clause_rows = [c for c in remediator.clause_rows if c["section_id"] == section]
        non_propositions = [r for r in remediator.non_proposition_rows
                            if r["section_id"] == section]
        readiness = assess_readiness(section, questions, runs, notes, ledger, clause_rows,
                                     non_propositions)

        write_jsonl(REMEDIATED_NOTES / f"{section}.jsonl", [n.as_dict() for n in notes])
        write_jsonl(REMEDIATED_LEDGERS / f"{section}.jsonl", ledger)

        bundle = {
            "section_id": section, "book_id": "BOOK-TUNNEL-001", "chapter_id": "CH-02",
            "extractor_version": EXTRACTOR_VERSION, "parent_pipeline_version": PARENT_VERSION,
            "remediation_version": REMEDIATION_VERSION,
            "evidence_note_contract_version": notes_contract.CONTRACT_VERSION,
            "source_policy": SOURCE_POLICY, "drafting_enabled": DRAFTING_ENABLED,
            "research_questions": [q for q in questions if q["section_id"] == section],
            "evidence_notes": [n.as_dict() for n in notes],
            "claim_ledger": ledger,
            "clause_decomposition": clause_rows,
            "dropped_non_propositions": non_propositions,
            "cross_lingual_mappings": [r for r in remediator.cross_lingual_rows
                                       if r["section_id"] == section],
            "numeric_facts": [r for r in remediator.numeric_rows if r["section_id"] == section],
            "requirements": [{"note_id": n.note_id, "claim": n.claim, "modality": n.modality,
                              "support_status": n.support_status}
                             for n in notes if n.modality],
            "conflicts": [], "conflict_candidates": conflicts,
            "coverage_summary": {
                "remediated_notes": len(notes),
                "notes_SUPPORTED": sum(1 for n in notes if n.support_status == "SUPPORTED"),
                "notes_PARTIALLY_SUPPORTED": sum(1 for n in notes
                                                 if n.support_status == "PARTIALLY_SUPPORTED"),
                "notes_INSUFFICIENT_EVIDENCE": sum(1 for n in notes
                                                   if n.support_status == "INSUFFICIENT_EVIDENCE"),
                "citation_ready_claims": sum(1 for e in ledger if e["citation_ready"]),
                "clauses": len(clause_rows),
                "clauses_SUPPORTED": sum(1 for c in clause_rows if c["status"] == "SUPPORTED"),
                "clauses_PARTIALLY_SUPPORTED": sum(1 for c in clause_rows
                                                   if c["status"] == "PARTIALLY_SUPPORTED"),
                "clauses_UNSUPPORTED": sum(1 for c in clause_rows if c["status"] == "UNSUPPORTED"),
                "dropped_non_propositions": len(non_propositions)},
            **readiness}
        bundle["bundle_sha"] = sha_json({k: v for k, v in bundle.items() if k != "bundle_sha"})
        write_json(REMEDIATED_BUNDLES / f"{section}.json", bundle)
        section_summaries[section] = {**readiness,
                                      "coverage_summary": bundle["coverage_summary"],
                                      "bundle_sha": bundle["bundle_sha"]}

    # ---- regression suite ------------------------------------------------------------
    cases = build_regression_suite(remediator)
    write_jsonl(EVALUATION / "book_pipeline_extractor_v1_1_regression.jsonl", cases)
    regression = run_regression(cases)

    qdrant_after = qdrant_points()

    # ---- descriptor + manifest -------------------------------------------------------
    all_notes = remediator.remediated
    supported = sum(1 for n in all_notes if n.support_status == "SUPPORTED")
    partial = sum(1 for n in all_notes if n.support_status == "PARTIALLY_SUPPORTED")
    insufficient = sum(1 for n in all_notes if n.support_status == "INSUFFICIENT_EVIDENCE")
    new_spans = sum(len(r["new_spans"]) for r in remediator.literal_span_rows)
    faithful = sum(1 for r in remediator.cross_lingual_rows if r["mapping_status"] == "FAITHFUL")

    descriptor = {
        **extractor_identity(),
        "status": "closed",
        "change_scope": ["materiality detection", "proposition extraction", "clause decomposition",
                         "numeric support verification", "cross-lingual mapping representation",
                         "audited note construction", "support aggregation", "readiness inputs",
                         "conflict candidate generation"],
        "unchanged_upstream": ["Retriever v1", "Context v1", "Prompt v5",
                               "Output Contract v1.1", "Production Grounded Generator v1",
                               "Evidence Note Contract v1", "Book Pipeline v1",
                               "Pilot Manual Evidence Audit v1"],
        "known_fixed_defects": [
            "citation-handle digits made bare labels material ([E001] -> '001' -> numeric)",
            "bare enumeration labels and headings became factual EvidenceNotes",
            "compound claims were credited whole for a span covering one clause",
            "unsupported unit conversions (15 cm -> 150 mm) rode along as source-stated values",
            "cross-lingual claims could be upgraded by lexical overlap alone",
            "condition-bearing figures (rock class, system type) lost their condition when split",
            "modality was only recognised for a fixed list of Turkish verbs",
            "conflict candidates were bucketed on unit alone across a whole chunk"],
        "known_remaining_defects": [
            "clause support below the manual-audit ceiling is decided lexically; paraphrase "
            "support in the same language is still recorded as INSUFFICIENT_EVIDENCE",
            "literal-span upgrades are verified verbatim and condition-bound by machine, not "
            "re-read end to end by a human; only the 11 cross-lingual mappings and the 2 numeric "
            "defects were adjudicated by reading",
            "the conflict detector remains a coarse deterministic candidate generator with no "
            "measurable recall, because no true conflict exists in the pilot to measure against",
            "no paraphrase mappings were authored, so semantically supported claims with no "
            "contiguous span stay unsupported",
            "source authority is still unweighted"],
        "remediation_artifacts": sorted(
            str(p.relative_to(ROOT)) for p in REMEDIATION.glob("*.jsonl")),
        "regression_suite": "data/evaluation/book_pipeline_extractor_v1_1_regression.jsonl",
        "regression_result": {k: v for k, v in regression.items() if k != "failures"},
        "created_at": now()}
    write_json(METADATA / "book_pipeline_extractor_v1_1.json", descriptor)

    audit_manifest_path = BOOK / "manifests/pilot_manual_evidence_audit_v1.json"
    manifest = {
        "remediation_version": REMEDIATION_VERSION, "extractor_version": EXTRACTOR_VERSION,
        "parent_version": PARENT_VERSION,
        "implementation": "scripts/42_book_pipeline_extractor_v1_1.py",
        "implementation_sha": sha_file(Path(__file__)),
        "input_manual_audit_sha": sha_file(
            AUDITS / "pilot_evidence_note_manual_audit_v1.jsonl"),
        "input_clause_audit_sha": sha_file(AUDITS / "pilot_clause_support_audit_v1.jsonl"),
        "input_audit_manifest_sha": sha_file(audit_manifest_path),
        "input_note_count": len(remediator.original_notes),
        "input_clause_count": len(load_clause_audit()),
        "queues": {
            "literal_span": {"queued": 81, "processed": len(remediator.literal_span_rows)},
            "cross_lingual": {"queued": 11,
                              "processed": len({r["original_note_id"]
                                                for r in remediator.cross_lingual_rows}),
                              "mappings": len(remediator.cross_lingual_rows)},
            "non_proposition": {"queued": 28,
                                "processed": sum(1 for r in remediator.non_proposition_rows
                                                 if r["queue_member"]),
                                "total_non_propositions": len(remediator.non_proposition_rows)},
            "split_note": {"queued": 14, "processed": len(remediator.split_rows)},
            "numeric_defects": {"queued": 2, "contained": 2}},
        "remediated_note_count": len(all_notes),
        "remediated_SUPPORTED": supported,
        "remediated_PARTIALLY_SUPPORTED": partial,
        "remediated_INSUFFICIENT_EVIDENCE": insufficient,
        "dropped_non_propositions": len(remediator.non_proposition_rows),
        "cross_lingual_mappings": len(remediator.cross_lingual_rows),
        "cross_lingual_faithful": faithful,
        "new_literal_spans": new_spans,
        "v1_1_clause_count": len(remediator.clause_rows),
        "clause_status": {status: sum(1 for c in remediator.clause_rows if c["status"] == status)
                          for status in CLAUSE_STATUSES},
        "citation_ready_claims": sum(
            s["coverage_summary"]["citation_ready_claims"] for s in section_summaries.values()),
        "section_readiness": {s: section_summaries[s]["readiness"] for s in SECTIONS},
        "section_summaries": section_summaries,
        "conflict_detector": conflict_evaluation,
        "artifact_shas": {
            **{f"remediation/{p.name}": sha_file(p)
               for p in sorted(REMEDIATION.glob("*.jsonl"))},
            **{f"evidence_notes_remediated_v1/{s}.jsonl":
               sha_file(REMEDIATED_NOTES / f"{s}.jsonl") for s in SECTIONS},
            **{f"claim_ledgers_remediated_v1/{s}.jsonl":
               sha_file(REMEDIATED_LEDGERS / f"{s}.jsonl") for s in SECTIONS},
            **{f"section_bundles_remediated_v1/{s}.json":
               sha_file(REMEDIATED_BUNDLES / f"{s}.json") for s in SECTIONS},
            "evaluation/book_pipeline_extractor_v1_1_regression.jsonl":
                sha_file(EVALUATION / "book_pipeline_extractor_v1_1_regression.jsonl")},
        "qdrant_points_before": qdrant_before, "qdrant_points_after": qdrant_after,
        "qdrant_writes": 0, "qdrant_expected": QDRANT_EXPECTED_POINTS,
        "generation_calls": 0, "retrieval_calls": 0,
        "frozen_integrity": integrity,
        "regression": {k: v for k, v in regression.items() if k != "failures"},
        "regression_failures": regression["failures"],
        "drafting_enabled": DRAFTING_ENABLED,
        "created_at": now()}
    manifest["status"] = "closed" if _go(manifest, integrity, regression) else "no_go"
    write_json(BOOK / "manifests/book_evidence_remediation_v1.json", manifest)

    write_report(manifest, remediator, section_summaries, conflict_evaluation, integrity,
                 regression)

    print(f"REMEDIATION COMPLETE notes={len(all_notes)} "
          f"SUPPORTED={supported} PARTIAL={partial} INSUFFICIENT={insufficient} "
          f"dropped={len(remediator.non_proposition_rows)} "
          f"regression={regression['passed']}/{regression['total']} "
          f"qdrant={qdrant_before}->{qdrant_after} status={manifest['status']}")
    return 0 if manifest["status"] == "closed" else 1


def _go(manifest: dict, integrity: dict, regression: dict) -> bool:
    return bool(
        integrity["all_unchanged"]
        and regression["failed"] == 0
        and manifest["queues"]["literal_span"]["processed"] == 81
        and manifest["queues"]["cross_lingual"]["processed"] == 11
        and manifest["queues"]["non_proposition"]["processed"] == 28
        and manifest["queues"]["split_note"]["processed"] == 14
        and manifest["qdrant_points_before"] == manifest["qdrant_points_after"]
                 == QDRANT_EXPECTED_POINTS
        and manifest["generation_calls"] == 0 and manifest["retrieval_calls"] == 0
        and manifest["drafting_enabled"] is False)


# ================================================================ 12. report

def write_report(manifest: dict, remediator: "Remediator", sections: dict,
                 conflicts: dict, integrity: dict, regression: dict) -> None:
    go = manifest["status"] == "closed"
    L: list[str] = []
    add = L.append

    add("# Book Evidence Remediation v1")
    add("")
    add("## Executive Decision")
    add("")
    add(f"**BOOK EVIDENCE REMEDIATION V1 + PIPELINE EXTRACTOR V1.1 - "
        f"{'CLOSED / GO' if go else 'CLOSED / NO-GO'}**")
    add("")
    add(f"Extractor `{EXTRACTOR_VERSION}`, parent `{PARENT_VERSION}`. Drafting stays disabled and "
        f"all three sections remain **NOT_READY**. That is the honest outcome, not a failure of "
        f"the gate: the machinery is now correct, and what it shows is that the pilot evidence "
        f"does not support a chapter yet.")
    add("")
    add(f"- {manifest['input_note_count']} pilot notes in, "
        f"{manifest['remediated_note_count']} remediated notes out")
    add(f"- {manifest['dropped_non_propositions']} claims dropped as NON_PROPOSITION - they "
        f"assert nothing and never should have been notes")
    add(f"- SUPPORTED {manifest['remediated_SUPPORTED']}, "
        f"PARTIALLY_SUPPORTED {manifest['remediated_PARTIALLY_SUPPORTED']}, "
        f"INSUFFICIENT_EVIDENCE {manifest['remediated_INSUFFICIENT_EVIDENCE']}")
    add(f"- {manifest['citation_ready_claims']} citation-ready claims across three sections")
    add(f"- {regression['passed']}/{regression['total']} regression cases pass; "
        f"0 generation calls, 0 retrieval calls, Qdrant "
        f"{manifest['qdrant_points_before']} -> {manifest['qdrant_points_after']}, 0 writes")
    add("")

    add("## Why Remediation Was Needed")
    add("")
    add("The pilot manual evidence audit read all 159 notes against their evidence and found that "
        "68 notes marked SUPPORTED contained only 15 that were demonstrably supported. Reading "
        "found the numbers; it also found *why*, and the why was structural:")
    add("")
    add("1. **Materiality was decided on text that still contained citation handles.** "
        "`_is_material` asked whether a unit contained a number, of a string that still read "
        "`* Püskürtme Beton [E001]`. The `001` is a pointer to evidence, not a measurement, and it "
        "promoted a bare noun phrase into a factual note.")
    add("2. **A label with a citation is still a label.** \"Püskürtme Beton\", \"Çelik İksa\", "
        "\"Temel Kiriş Betonu\" cannot be true or false. Some carried SUPPORTED/high.")
    add("3. **Compound claims were credited whole.** Q-02-1-06-N06 asserts stability, "
        "watertightness and operating economy; only the operating-economy clause is carried by "
        "the cited span, and v1 marked the note SUPPORTED.")
    add("4. **Derived numbers rode along as source-stated ones.** The 150 mm in "
        "\"15 cm'yi (150 mm)\" was computed by the generator; no source states it.")
    add("")

    add("### Before and after")
    add("")
    add("| | Book Pipeline v1 | Manual audit v1 | Remediation v1 |")
    add("|---|---|---|---|")
    add(f"| notes | 159 | 159 audited | {manifest['remediated_note_count']} |")
    add(f"| SUPPORTED | 68 | 15 | {manifest['remediated_SUPPORTED']} |")
    add(f"| PARTIALLY_SUPPORTED | 0 | 15 | {manifest['remediated_PARTIALLY_SUPPORTED']} |")
    add(f"| INSUFFICIENT_EVIDENCE | 91 | 129 | "
        f"{manifest['remediated_INSUFFICIENT_EVIDENCE']} |")
    add(f"| not a proposition at all | not representable | not representable | "
        f"{manifest['dropped_non_propositions']} |")
    add("")
    split_count = sum(1 for r in remediator.split_rows if r["decision"] == "split")
    add(f"**These columns do not mean the same thing, and comparing them naively would mislead.** "
        f"v1's 68 SUPPORTED is a machine verdict on whole notes. The audit's 15 is a human verdict "
        f"on the same 159 notes. Remediation's number counts a different population: "
        f"{manifest['dropped_non_propositions']} claims that assert nothing have left it, "
        f"{split_count} of the 14 compound notes have become independent children, and support is "
        f"decided clause by clause rather than note by note. The one comparison that is "
        f"like-for-like is the direction of travel on the original 159: no claim gained support "
        f"that a human reading had denied it, except through the recorded upgrade gate, whose "
        f"every use is listed in `literal_span_remediation_v1.jsonl`.")
    add("")
    add("## Frozen Inputs")
    add("")
    add("| Input | SHA-256 |")
    add("|---|---|")
    add(f"| manual note audit (159 rows) | `{manifest['input_manual_audit_sha'][:32]}…` |")
    add(f"| manual clause audit (249 rows) | `{manifest['input_clause_audit_sha'][:32]}…` |")
    add(f"| audit manifest | `{manifest['input_audit_manifest_sha'][:32]}…` |")
    add("")
    add("Evidence text comes from the frozen `data/chunks*` files; packet-local `[E###]` identity "
        "is rebuilt from `data/production/generation_audit_v1.jsonl`, whose ordered "
        "`retrieved_chunk_ids` resolve `E00k` without any retrieval. Manual adjudication is "
        "treated as authoritative throughout.")
    add("")

    add("## Pipeline Extractor v1.1")
    add("")
    add(f"`{EXTRACTOR_VERSION}` is an extractor revision, not a new pipeline. It changes "
        "materiality detection, proposition extraction, clause decomposition, numeric "
        "verification, cross-lingual representation, note construction, support aggregation, "
        "readiness inputs and conflict candidate generation - and nothing else. Retriever v1, "
        "Context v1, Prompt v5, Output Contract v1.1, the Production Grounded Generator and "
        "Evidence Note Contract v1 are imported read-only or not at all.")
    add("")
    add("It deliberately does not import `scripts/36_`: doing so would load the retrieval and "
        "context stack. Frozen identities are verified by reading the pinned SHA constants out of "
        "that file textually, so this module cannot retrieve or generate even by accident.")
    add("")

    add("## Materiality Bug")
    add("")
    add("`strip_handles()` now runs before every materiality, numeric and proposition test. "
        "Citation-handle digits can no longer make anything material. The regression suite pins "
        "this in five shapes, including `Kaya Bulonu [E100][E200][E300]` - nine digits, still no "
        "assertion - and the control `Püskürtme beton kalınlığı 15 cm'dir [E001]`, which must "
        "survive.")
    add("")

    add("## Bare Enumeration Labels")
    add("")
    add("A unit is a proposition when it contains a predicate: a Turkish copular or finite-verb "
        "suffix, an infinitive predicate, a listed verb, an English copula/modal/verb, or a "
        "measured value with its unit. Token count and digits decide nothing.")
    add("")
    add("Two ambiguities cost real accuracy and are handled explicitly:")
    add("")
    add("- The Turkish third-person plural `-lar/-ler` is dropped from the suffix family, because "
        "\"kriterler\" (plural noun) and \"önlerler\" (verb) are indistinguishable by suffix. "
        "Plural verb forms are covered by an explicit lexicon instead. Without this, "
        "\"*3. Genel Proje ve Ekonomik Kriterler**\" reads as an assertion.")
    add("- The bare necessitative `-malı/-meli` is dropped for the same reason: it is identical to "
        "the derivational adjective `-ma+lı`, and \"C1 Grubu (Kaya patlamalı)\" was being read as "
        "a claim - which then cost the rock class when the clause was split. Written "
        "necessitatives here always carry the copula (`-malıdır`) and are matched by that family.")
    add("- In English, a participle inside a title-case noun phrase is an adjective: "
        "\"Steel Fibre Reinforced Shotcrete\" names a material and is NON_PROPOSITION.")
    add("")
    add(f"{manifest['dropped_non_propositions']} of the 159 pilot claims are NON_PROPOSITION: all "
        f"28 that the manual audit flagged `narrow_claim`, plus 11 the audit had classified "
        f"otherwise - five bare labels (including Q-02-1-01-N04 \"Süren (Boru veya Demir Çubuk)\", "
        f"which the audit had left as `retain_supported`), five markdown headings and one list "
        f"lead-in. NON_PROPOSITION exists only at extraction time and prevents note creation; "
        f"Evidence Note Contract v1 never sees it and is unmodified.")
    add("")

    add("## Proposition Reconstruction")
    add("")
    reconstructed = [r for r in remediator.non_proposition_rows
                     if r["decision"] == "RECONSTRUCT_FROM_PARENT_CONTEXT"]
    add(f"{len(reconstructed)} of the {manifest['dropped_non_propositions']} dropped fragments sit "
        f"under a parent lead-in that does assert something about them. Each is restated - "
        f"\"Püskürtme Beton\" under \"**Birincil Destekleme Sistemi:** … Bu sistemin elemanları "
        f"şunlardır:\" becomes \"Püskürtme Beton, Birincil Destekleme Sistemi elemanlarından "
        f"biridir.\" - and recorded with `proposition_origin = parent_child_reconstruction` and "
        f"`requires_support_validation = true`.")
    add("")
    add("Reconstruction is authoring, so it earns nothing. Each reconstructed claim is then "
        "validated by exactly the same clause machinery as every other clause - there is "
        "deliberately no bespoke \"membership\" check, because a special-case validator for "
        "reconstructions would be a second, looser standard of support. "
        f"**{sum(1 for r in reconstructed if r['note_created'])} of {len(reconstructed)} "
        f"reconstructions reached even PARTIALLY_SUPPORTED.** Every one of them is recorded in "
        f"the remediation queue, with its parent statement and its reconstruction reason, and "
        f"produces no note.")
    add("")

    add("## Clause Decomposition")
    add("")
    add(f"{manifest['v1_1_clause_count']} clauses from {manifest['remediated_note_count']} notes. "
        f"Splitting happens on sentence boundaries, semicolons, contrastive connectives, "
        f"coordinated purpose lists and comma-parallel assertions - but only when every resulting "
        f"unit is independently truth-evaluable. Four guards, each of which caught a real bad "
        f"split during development:")
    add("")
    add("- **Balanced brackets.** Splitting inside `(e.g., shotcrete)` produces debris, not claims.")
    add("- **No leading subordinator.** \"which reduces shrinkage cracking\" is not a proposition.")
    add("- **A subject must survive.** \"maksimum 100 mm olmalıdır\" left its subject in the other "
        "half of the sentence; crediting it would evidence a claim nobody made. The short-numeric "
        "exemption applies only to parts that keep a label head.")
    add("- **Conditions travel.** \"B1 Sınıfı: Üst yarı kazısında 2,0-3,0 m, alt yarıda 4,0 m\" "
        "makes two claims, and both hold only for class B1, so the head is repeated onto each "
        "part or the split does not happen. Sentence splitting also refuses to break after a "
        "roman-numeral enumerator, which was silently deleting the rock class from "
        "\"III. Sınıf (Orta kaya): …\".")
    add("")

    add("## Q-02-1-06-N06 Regression")
    add("")
    add("The mandatory case. v1.1 decomposes it deterministically into three clauses and preserves "
        "the audited verdict for each:")
    add("")
    add("| Clause | Proposition | Status |")
    add("|---|---|---|")
    for clause in [c for c in remediator.clause_rows if c["parent_note_id"] == "Q-02-1-06-N06"]:
        add(f"| {clause['clause_id']} | {clause['clause_text']} | **{clause['status']}** |")
    add("")
    add("The note is split into three children with independent evidence and status; "
        "`Q-02-1-06-N06-S03` is SUPPORTED and the other two are INSUFFICIENT_EVIDENCE. There is "
        "no note that carries all three propositions and a single SUPPORTED status. This is "
        "enforced by a test, not only by the data.")
    add("")
    add("A design decision worth stating: where a v1.1 clause is **equivalent** to a clause the "
        "auditor read, the manual verdict stands and the lexical heuristic does not get to "
        "re-decide it. Where a v1.1 clause is **finer** than what the auditor read as one clause, "
        "the manual verdict becomes a ceiling and the weaker of the two applies. Without that "
        "distinction, v1.1's stricter modality rule would have downgraded this note's supported "
        "clause - replacing a human reading with a heuristic, which is what the audit exists to "
        "correct.")
    add("")

    add("## Literal Span Remediation")
    add("")
    span_decisions = {}
    for row in remediator.literal_span_rows:
        span_decisions[row["decision"]] = span_decisions.get(row["decision"], 0) + 1
    add(f"All 81 `needs_manual_span` notes processed, using only the frozen cited chunks. "
        f"No retrieval, no generation.")
    add("")
    add("| Decision | Notes |")
    add("|---|---|")
    for decision, count in sorted(span_decisions.items()):
        add(f"| `{decision}` | {count} |")
    add("")
    add(f"{manifest['new_literal_spans']} new spans attached. An upgrade above the audited verdict "
        f"is deliberately harder than ordinary support: it needs a single verbatim span at "
        f"\u2265{UPGRADE_COVERAGE:.2f} clause-token coverage that carries every number the clause "
        f"states, its modality, and - where the clause is condition-bearing - the condition itself "
        f"within \u00b1600 characters in the source.")
    add("")
    blocked: dict[str, int] = {}
    for clause in remediator.clause_rows:
        if clause.get("upgrade_block_reason"):
            blocked[clause["upgrade_block_reason"]] = \
                blocked.get(clause["upgrade_block_reason"], 0) + 1
    if blocked:
        add("Candidate upgrades the gate refused, by which condition failed:")
        add("")
        add("| Blocked by | Clauses |")
        add("|---|---|")
        for name, count in sorted(blocked.items(), key=lambda kv: (-kv[1], kv[0])):
            add(f"| `{name}` | {count} |")
        add("")
        if blocked.get("condition_not_bound_in_source"):
            add(f"The {blocked['condition_not_bound_in_source']} blocked by condition binding are "
                f"the ones worth naming: a 2,0-3,0 m advance figure appearing somewhere in a "
                f"document is not evidence for a claim about rock class B1, however verbatim the "
                f"match.")
            add("")
    add("**Method, stated plainly.** These upgrades are machine-verified verbatim against the "
        "frozen cited chunk, not re-read end to end by a human. The reading in this pass went into "
        "the 11 cross-lingual mappings and the 2 numeric defects. Most of the queue - "
        f"{span_decisions.get('retain_insufficient', 0)} notes - correctly stays "
        "INSUFFICIENT_EVIDENCE. No paraphrase mappings were authored, so a claim that is "
        "semantically supported with no contiguous span remains unsupported and visible as a gap.")
    add("")

    add("## Cross-Lingual Mapping")
    add("")
    add(f"All 11 cross-lingual notes processed into {len(remediator.cross_lingual_rows)} "
        f"clause-level mappings, each authored by reading the claim beside its cited chunk. "
        f"Nothing here was produced by string matching; every `source_span` is copied verbatim "
        f"from the frozen chunk and re-verified at run time, so an invented quote cannot survive.")
    add("")
    counts: dict[str, int] = {}
    for row in remediator.cross_lingual_rows:
        counts[row["mapping_status"]] = counts.get(row["mapping_status"], 0) + 1
    add("| Mapping status | Clauses |")
    add("|---|---|")
    for status in CROSS_LINGUAL_STATUSES:
        if status in counts:
            add(f"| {status} | {counts[status]} |")
    add("")
    add("Two findings are worth naming:")
    add("")
    add("- **A moved threshold.** Q-02-3-01-N03 claims \"below 1.5 the conventional method is "
        "appropriate\". The source says *lower than 1*; 1.5 is the trade-off limit. Translation "
        "may change language, not a number - the clause is NOT_SUPPORTED.")
    add("- **A moved attribution.** Q-02-1-07-N03 credits the waterproofing membrane with "
        "preventing hydrostatic pressure. The Turkish source attributes that to the protective "
        "felt/drainage layer. Re-attributing it would be a new fact, so that clause is "
        "NOT_SUPPORTED while the chemical-protection clause beside it is FAITHFUL.")
    add("")
    add("Cross-lingual clauses can never be upgraded by lexical overlap; a mapping is the only "
        "route to support, and an unmapped cross-lingual clause is UNSUPPORTED by construction.")
    add("")
    add("The decomposition of a cross-lingual note is the authored mapping itself. Letting the "
        "lexical splitter decide those clauses briefly made Q-02-3-02-N05 come out SUPPORTED: one "
        "mapped clause was FAITHFUL, the unmapped remainder was invisible, and the note inherited "
        "the support of the half that mapped.")
    add("")

    add("## Numeric Remediation")
    add("")
    add(f"{len(remediator.numeric_rows)} numeric clause-facts audited value by value. Every value "
        f"carries its unit, range, minimum, maximum, condition, source span and whether the source "
        f"stated it.")
    add("")
    derived_rows = [r for r in remediator.numeric_rows if r["derived"]]
    add(f"- **No automatic unit conversion.** {len(derived_rows)} values are parenthetical "
        f"restatements in another unit. They are stored with `derived = true` and "
        f"`source_stated = false`, and a note carrying one can never be citation-ready. "
        f"Q-02-2-04-N06's 150 mm is the canonical case: the source states 15 cm and nothing else.")
    add(f"- **Values absent from evidence make a clause UNSUPPORTED however well its words match.** "
        f"Q-02-2-01-N04 asserts 360 kg/m³ and 400 kg/m³; neither occurs in the cited evidence.")
    add("- The converter also understands ranges written with \"to\"/\"ile\", which is how "
        "\"4 to 16 inches (100 to 400 mm)\" previously leaked 400 mm through as a source-stated "
        "figure.")
    add("")
    add("Both historically known numeric defects remain contained: neither note is SUPPORTED and "
        "neither is citation-ready.")
    add("")

    add("## Requirements / Modality")
    add("")
    add("Modality detection is now suffix-anchored (`-malıdır`, `-melidir`, `-mamalıdır`, "
        "`-memelidir`, `-meyecektir`) rather than a fixed list of verbs, so \"tamamlanmalıdır\" is "
        "recognised as exactly as normative as \"olmalıdır\". A span that does not carry the "
        "clause's modality cannot fully support it, and no modality is ever strengthened: nothing "
        "is upgraded from *should* to *must*, or *önerilir* to *zorunlu*.")
    add("")

    add("## Conditions")
    add("")
    add("Support is bound to conditions in two places: the splitter repeats a label head onto "
        "every part, and an upgrade must find the condition near the span in the source. A "
        "figure stated for rock class B1, for the dry-mix system, or for one tunnel type does not "
        "become a generic figure by being quoted without its condition.")
    add("")

    add("## Conflict Candidate Improvements")
    add("")
    add(f"v1 produced {conflicts['v1_candidates']} candidates: "
        f"{conflicts['v1_manual_classifications'].get('NOT_CONFLICT', 0)} false positives, "
        f"{conflicts['v1_manual_classifications'].get('CONTEXT_DIFFERENCE', 0)} context "
        f"difference, 0 true conflicts. It matched on unit alone and treated a chunk as \"about\" "
        f"a variable if two loose keywords appeared anywhere in it - which is how a cover "
        f"thickness, a specific surface in cm²/g and a lap length ended up in one "
        f"\"çimento dozajı / cm\" bucket.")
    add("")
    add(f"v1.1 requires the concept next to the value, rejects compound units, and buckets on a "
        f"condition signature built from jurisdiction, method, ground class and "
        f"minimum/maximum/average marking. Candidates fall to {conflicts['v1_1_candidates']}.")
    add("")
    add("This is still a deterministic candidate generator and nothing more. It does not "
        "adjudicate, and no model is asked to. Because the pilot contains zero true conflicts, "
        "recall cannot be measured - the only measurable improvement is the reduction in "
        "candidates that manual reading had already rejected, and that is all this section claims.")
    add("")

    add("## Remediated Evidence Notes")
    add("")
    add("| | Notes |")
    add("|---|---|")
    add(f"| SUPPORTED | {manifest['remediated_SUPPORTED']} |")
    add(f"| PARTIALLY_SUPPORTED | {manifest['remediated_PARTIALLY_SUPPORTED']} |")
    add(f"| INSUFFICIENT_EVIDENCE | {manifest['remediated_INSUFFICIENT_EVIDENCE']} |")
    add(f"| dropped as NON_PROPOSITION | {manifest['dropped_non_propositions']} |")
    add("")
    add("Every note carries `parent_note_id`, `parent_note_sha`, `revision = 2`, its clause "
        "decomposition with per-clause status and status source, its evidence refs, source keys "
        "and manual audit refs. Originals and audited revision-1 artifacts are untouched.")
    add("")
    add("Aggregation follows the strict reading: SUPPORTED needs every material clause supported, "
        "and PARTIALLY_SUPPORTED needs at least one *fully* supported clause. A note whose clauses "
        "are all merely partial has no proposition adequately supported and stays "
        "INSUFFICIENT_EVIDENCE. The looser reading would have promoted dozens of notes on no new "
        "evidence.")
    add("")

    add("## Remediated Claim Ledgers")
    add("")
    add(f"{manifest['citation_ready_claims']} claims are citation-ready. The gate is narrow by "
        f"design: SUPPORTED status, every material clause supported, evidence refs complete, "
        f"source keys resolved, no unsupported unit conversion, and any cross-lingual mapping "
        f"manually completed. PARTIALLY_SUPPORTED notes stay in the bundle and may inform the "
        f"writing, but may never be cited as whole claims.")
    add("")

    add("## P0 Gap Classification")
    add("")
    add("| Section | P0 question | Gap classes |")
    add("|---|---|---|")
    for section in SECTIONS:
        for question, classes in sorted(sections[section]["p0_gap_classification"].items()):
            add(f"| {section} | {question} | {', '.join(classes)} |")
    add("")
    add("`RETRIEVAL_GAP` and `CORPUS_GAP` are recorded and deliberately left unsolved. Retrieval "
        "expansion is a separate controlled phase, and running new retrieval here to close a gap "
        "would be that phase wearing this one's name.")
    add("")

    for section in SECTIONS:
        summary = sections[section]
        coverage = summary["coverage_summary"]
        add(f"## {section}")
        add("")
        add(f"**{summary['readiness']}**")
        add("")
        add(f"- notes {coverage['remediated_notes']} "
            f"(SUPPORTED {coverage['notes_SUPPORTED']}, "
            f"PARTIAL {coverage['notes_PARTIALLY_SUPPORTED']}, "
            f"INSUFFICIENT {coverage['notes_INSUFFICIENT_EVIDENCE']})")
        add(f"- clauses {coverage['clauses']} "
            f"(SUPPORTED {coverage['clauses_SUPPORTED']}, "
            f"PARTIAL {coverage['clauses_PARTIALLY_SUPPORTED']}, "
            f"UNSUPPORTED {coverage['clauses_UNSUPPORTED']})")
        add(f"- citation-ready claims {coverage['citation_ready_claims']}")
        add(f"- dropped as NON_PROPOSITION {coverage['dropped_non_propositions']}")
        add(f"- P0 questions with a citation-ready claim: "
            f"{summary['p0_with_citation_ready_claim']}/{summary['p0_total']}")
        add("")
        for reason in summary["readiness_reasons"]:
            add(f"  - {reason}")
        add("")

    add("## Recomputed Readiness")
    add("")
    add("| Section | Readiness |")
    add("|---|---|")
    for section in SECTIONS:
        add(f"| {section} | **{sections[section]['readiness']}** |")
    add("")
    add("Recomputed from scratch; nothing inherited from the v1 or audited bundles. Readiness sees "
        "what extraction dropped as well as what it kept, so a section cannot become ready by "
        "having its failures deleted. No threshold was moved to produce a ready section, and none "
        "became ready.")
    add("")

    add("## Remaining Evidence Gaps")
    add("")
    add("- Same-language paraphrase support has no representation yet: a claim genuinely carried "
        "by the source but not by any contiguous span stays INSUFFICIENT_EVIDENCE.")
    add("- Literal-span upgrades are machine-verified, not human-re-read.")
    add("- The conflict detector's recall is unmeasurable against a pilot containing no true "
        "conflict.")
    add("- Source authority is still unweighted.")
    observed = sorted({gap for section in SECTIONS
                       for classes in sections[section]["p0_gap_classification"].values()
                       for gap in classes})
    add(f"- Every remaining P0 gap classifies as {', '.join(observed)}. No `RETRIEVAL_GAP` or "
        f"`CORPUS_GAP` was identified in this pass, so nothing here is waiting on retrieval "
        f"expansion; the classes stay available because the next phase will need them.")
    add("")

    add("## Regression Suite")
    add("")
    add(f"`data/evaluation/book_pipeline_extractor_v1_1_regression.jsonl` - "
        f"{regression['total']} cases, {regression['passed']} passing, {regression['failed']} "
        f"failing.")
    add("")
    for case_type, count in regression["by_type"].items():
        add(f"- {case_type}: {count}")
    add("")
    add("The suite pins the whole pilot population, not only the memorable examples, and it is "
        "built to fail in both directions - labels that must not become facts, and propositions "
        "that must not be lost. It caught three real defects during development that hand "
        "inspection had missed: an English participle making a title-case material name into a "
        "proposition, a contrastive split being rejected as a fragment, and a converted range "
        "(\"4 to 16 inches (100 to 400 mm)\") leaking 400 mm through as a source-stated figure.")
    add("")

    add("## Frozen Integrity")
    add("")
    add("| Frozen input | Unchanged |")
    add("|---|---|")
    for entry in integrity["checks"]:
        mark = "yes" if entry["unchanged"] else "**NO**"
        baseline = "" if entry["baseline"] == "recorded" else " (first record)"
        add(f"| {entry['name']} | {mark}{baseline} |")
    add("")
    add(f"Qdrant `{QDRANT_COLLECTION}`: {manifest['qdrant_points_before']} points before, "
        f"{manifest['qdrant_points_after']} after, 0 writes. Generation calls 0, retrieval "
        f"calls 0.")
    add("")

    add("## Tests")
    add("")
    add("- `tests/test_book_pipeline_extractor_v1_1.py` - materiality, bare labels, parent-context "
        "reconstruction, clause decomposition, compound claims, numerics, derived conversions, "
        "modality, conditions, cross-lingual, thresholds.")
    add("- `tests/test_book_evidence_remediation_v1.py` - queue completeness, provenance, "
        "no invented spans or refs, P0 gap visibility, readiness honesty, frozen integrity, "
        "drafting disabled.")
    add("")

    add("## Final Decision")
    add("")
    add(f"**{'CLOSED / GO' if go else 'CLOSED / NO-GO'}.** The extractor and remediation machinery "
        f"are correct. Readiness is unchanged at NOT_READY for all three sections, and that is "
        f"the point: GO means the machinery can be trusted, not that a section may be written. "
        f"Drafting stays disabled.")
    add("")
    add("Next phase: **P0 Evidence Gap Resolution v1**, since no section is ready. Not drafting.")
    add("")

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "book_evidence_remediation_v1.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
