"""TunnelBookAI generation output contract v1.1 - proper-noun-aware body language guard.

v1 rejected GEV018, a correct English answer, because nine Turkish glyphs sitting inside proper
nouns (Yapı Merkezi, Avrasya Tüneli İşletme İnşaat ve Yatırım A.Ş., ATAŞ) outweighed a paragraph of
English function words. Glyphs were weighted 2.0 each; the only Turkish *word* in the answer was
"ve", and it was part of a company's legal name.

v1.1 changes the language detector and nothing else. Language is decided by grammatical prose -
function words and morphology - measured after named entities have been masked out. Glyph evidence
survives only as a tie-break that cannot decide a case on its own and never fires without
corroborating Turkish function-word evidence.

Every other enforcement decision is delegated to the frozen v1 implementation itself rather than
reimplemented here, so citation syntax, unknown handles, marker mapping, marker position, leak
rules, empty-answer handling and coverage telemetry cannot drift. The repair policy is unchanged:
none_fail_closed. v1.1 still never rewrites a marker, translates a body, normalises a citation or
inserts a handle.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_VERSION = "tunnelbook-generation-output-contract-v1.1"
PARENT_CONTRACT_VERSION = "tunnelbook-generation-output-contract-v1"
PARENT_CONTRACT_SHA = "670031d116056485155fc9d5c3d12b472d91f6b1e7a34ed9b169166f3727ce7d"
LANGUAGE_DETECTION_VERSION = "proper-noun-aware-lexical-v1.1"
REPAIR_POLICY = "none_fail_closed"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


v1 = _load("output_contract_v1", "scripts/26_generation_output_contract.py")
gen = v1.gen

# Inherited verbatim from v1. Listing them here documents what v1.1 deliberately does NOT redefine.
VALIDATOR_VERSION = v1.VALIDATOR_VERSION
SUPPORTED_LANGUAGES = v1.SUPPORTED_LANGUAGES
MARKER_FOR_LANGUAGE = v1.MARKER_FOR_LANGUAGE
ANY_MARKER = v1.ANY_MARKER
MARKER_AT_START = v1.MARKER_AT_START
THINKING_MARKERS = v1.THINKING_MARKERS
HANDLE = v1.HANDLE
MIN_BODY_TOKENS = v1.MIN_BODY_TOKENS
LANGUAGE_MARGIN = v1.LANGUAGE_MARGIN
TURKISH_CHARS = v1.TURKISH_CHARS
ContractConfigError = v1.ContractConfigError
coverage_telemetry = v1.coverage_telemetry

TURKISH_WORDS = v1.TURKISH_WORDS | {
    "de", "da", "ki", "çok", "en", "hem", "ya", "ne", "şu", "o", "bunun", "buna", "bazı", "diğer",
    "böyle", "şöyle", "yani", "ayrı", "üzerinde", "altında", "karşı", "doğru", "sırasında",
    "durumunda", "halinde", "amacıyla", "tarafından", "olduğu", "olması", "edilmesi", "yapılması",
}
ENGLISH_WORDS = v1.ENGLISH_WORDS | {
    "a", "an", "was", "were", "has", "have", "had", "been", "being", "will", "would", "could",
    "into", "through", "under", "over", "after", "before", "about", "within", "without", "there",
    "here", "who", "whom", "whose", "what", "how", "why", "all", "any", "some", "more", "most",
    "other", "than", "then", "if", "but", "so", "because", "however", "therefore", "typically",
    "generally", "usually", "often", "including", "based", "due",
}

# Turkish predicate / nominalisation morphology. Deliberately excludes the plural -lar/-ler, which
# collides with ordinary English words (later, member, water, under). Every pattern below either
# carries a Turkish-specific vowel or is a multi-character verbal ending with no English analogue.
TURKISH_MORPHOLOGY = re.compile(
    r"(?:maktadır|mektedir|acaktır|ecektir|malıdır|melidir|mıştır|miştir|muştur|müştür"
    r"|dır|dir|dur|dür|tır|tir|tur|tür|dığı|diği|duğu|düğü|ması|mesi|ında|inde|unda|ünde"
    r"|ları|leri|ıyla|iyle|arak|erek|ilir|ılır|ulur|ünür)$")
# English morphology with no Turkish analogue. Weighted like a single function word.
ENGLISH_MORPHOLOGY = re.compile(r"(?:tion|tions|ment|ments|ness|ance|ence|ing|ally|ised|ized)$")

MARKDOWN_EMPHASIS = re.compile(r"[*_`#]+")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?:;])\s+|\n+|\s+(?=[-*•]\s)|^\s*[-*•]\s*|\s*\d{1,2}[.)]\s+")
CAPITALISED = re.compile(r"^[A-ZÇĞİÖŞÜ]")
GLYPH_TIE_BREAK_CAP = 2.0
MIN_TURKISH_WORDS_FOR_GLYPH_SUPPORT = 1
# Turkish is agglutinative: it carries in suffixes the grammatical load English spreads across
# separate function words, so counting both at 1.0 systematically under-reads Turkish. The patterns
# above are predicate morphology (-mıştır, -mektedir, -malıdır), which is strong grammatical
# evidence. The English patterns are derivational endings on content words (-ing, -ness, -tion),
# which are weak by comparison - "lining" and "thickness" say far less about language than "the"
# does. These two weights encode that asymmetry; they were calibrated on the development set only.
TURKISH_MORPHOLOGY_WEIGHT = 2.0
ENGLISH_MORPHOLOGY_WEIGHT = 0.5
# A single scalar over the whole body cannot tell "English prose" from "half English, half Turkish":
# the two languages differ in how densely they spend function words, so one aggregate score always
# favours one of them. Sentences are classified individually and then counted, which makes genuinely
# bilingual text visible as bilingual instead of resolving to whichever language counts faster.
# Three, not four: Turkish says in three tokens ("Drenaj boruları yerleştirilmiştir") what English
# needs four for ("Drainage pipes were installed"), so a four-token floor discards Turkish sentences
# while keeping their English counterparts - the same density bias, one level down.
MIN_SENTENCE_TOKENS = 3
MIXED_MINORITY_RATIO = 0.35


def implementation_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def mask_named_entities(text: str) -> str:
    """Blank out proper nouns deterministically, with no name list and no NER model.

    A capitalised token that is not the first token of its sentence or list item is treated as a
    named entity and removed. Sentence-initial capitals are kept, because every sentence in both
    languages starts with one and removing them would delete ordinary prose. This generalises to
    any corpus: nothing here knows what a tunnel, a ministry or a contractor is called.
    """
    cleaned = MARKDOWN_EMPHASIS.sub(" ", text)
    cleaned = HANDLE.sub(" ", cleaned)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    kept: list[str] = []
    for segment in SENTENCE_SPLIT.split(cleaned):
        if not segment or not segment.strip():
            continue
        tokens = segment.split()
        for index, token in enumerate(tokens):
            core = token.strip("(),;:'\"[]{}")
            if index > 0 and CAPITALISED.match(core):
                continue          # named entity: contributes no language evidence
            kept.append(token)
    return " ".join(kept)


def _lexical_tokens(text: str) -> list[str]:
    return [t for t in v1._strip_non_lexical(text).lower().split() if t]


def _score_tokens(tokens: list[str]) -> tuple[float, float, dict]:
    """Function words plus weighted morphology. The only place language evidence is counted."""
    turkish_words = sum(1 for t in tokens if t in TURKISH_WORDS)
    english_words = sum(1 for t in tokens if t in ENGLISH_WORDS)
    turkish_morphology = sum(1 for t in tokens
                             if t not in TURKISH_WORDS and len(t) >= 5
                             and TURKISH_MORPHOLOGY.search(t))
    english_morphology = sum(1 for t in tokens
                             if t not in ENGLISH_WORDS and len(t) >= 5
                             and ENGLISH_MORPHOLOGY.search(t))
    turkish = turkish_words + TURKISH_MORPHOLOGY_WEIGHT * turkish_morphology
    english = english_words + ENGLISH_MORPHOLOGY_WEIGHT * english_morphology
    return turkish, english, {"turkish_function_words": turkish_words,
                              "english_function_words": english_words,
                              "turkish_morphology": turkish_morphology,
                              "english_morphology": english_morphology}


def _verdict(turkish: float, english: float) -> tuple[str | None, str]:
    if turkish == 0 and english == 0:
        return None, "ambiguous"
    if turkish >= english * LANGUAGE_MARGIN:
        return "tr", "confident"
    if english >= turkish * LANGUAGE_MARGIN:
        return "en", "confident"
    return None, "ambiguous"


def _sentences(masked: str) -> list[list[str]]:
    spans = [sp for sp in SENTENCE_SPLIT.split(masked) if sp and sp.strip()]
    out = []
    for span in spans:
        tokens = [t for t in v1._strip_non_lexical(span).lower().split() if t]
        if len(tokens) >= MIN_SENTENCE_TOKENS:
            out.append(tokens)
    return out


def detect_language(text: str) -> dict[str, Any]:
    """Deterministic tr/en identification driven by grammatical prose, not by named entities.

    Named entities are masked first, so a Turkish organisation name inside an English sentence
    contributes nothing. Sentences are then classified individually and counted: text where both
    languages hold a substantial share of the sentences is reported ambiguous rather than resolved,
    which is what a body-language guard needs in order to stay fail-closed on genuinely bilingual
    answers. Glyphs remain a capped tie-break that never fires without Turkish function-word
    support, so a stray Ş cannot flip an English verdict, while Turkish prose light on special
    characters is still carried by its function words and morphology.
    """
    raw_tokens = _lexical_tokens(text)
    base = {"detector_version": LANGUAGE_DETECTION_VERSION}
    if len(raw_tokens) < MIN_BODY_TOKENS:
        return {**base, "language": None, "status": "insufficient_text", "tokens": len(raw_tokens),
                "turkish_score": 0.0, "english_score": 0.0, "turkish_function_words": 0,
                "english_function_words": 0, "turkish_morphology": 0, "english_morphology": 0,
                "glyphs_after_masking": 0, "glyph_tie_break_applied": False,
                "turkish_sentences": 0, "english_sentences": 0, "mixed_language_detected": False}

    masked = mask_named_entities(text)
    masked_lexical = v1._strip_non_lexical(masked)
    tokens = [t for t in masked_lexical.lower().split() if t]
    turkish_score, english_score, counts = _score_tokens(tokens)
    glyphs = sum(1 for ch in masked_lexical if ch in TURKISH_CHARS)

    sentence_languages = [_verdict(*_score_tokens(s)[:2])[0] for s in _sentences(masked)]
    turkish_sentences = sum(1 for lang in sentence_languages if lang == "tr")
    english_sentences = sum(1 for lang in sentence_languages if lang == "en")

    mixed = False
    decided = turkish_sentences + english_sentences
    if turkish_sentences and english_sentences:
        minority = min(turkish_sentences, english_sentences)
        mixed = (minority / decided) >= MIXED_MINORITY_RATIO

    glyph_applied = False
    if mixed:
        language, status = None, "ambiguous"
    elif decided:
        # Sentence majority is the primary verdict; the aggregate score only breaks a genuine tie.
        if turkish_sentences != english_sentences:
            language = "tr" if turkish_sentences > english_sentences else "en"
            status = "confident"
        else:
            language, status = _verdict(turkish_score, english_score)
    else:
        language, status = _verdict(turkish_score, english_score)

    if status == "ambiguous" and not mixed and glyphs and \
            counts["turkish_function_words"] >= MIN_TURKISH_WORDS_FOR_GLYPH_SUPPORT:
        glyph_applied = True
        language, status = _verdict(turkish_score + min(float(glyphs), GLYPH_TIE_BREAK_CAP),
                                    english_score)

    return {**base, "language": language, "status": status, "tokens": len(tokens),
            "turkish_score": round(turkish_score, 2), "english_score": round(english_score, 2),
            **counts, "glyphs_after_masking": glyphs, "glyph_tie_break_applied": glyph_applied,
            "turkish_sentences": turkish_sentences, "english_sentences": english_sentences,
            "mixed_language_detected": mixed}


def _body_after_marker(answer: str) -> str:
    return v1._body_after_marker(answer)


@dataclass
class ContractResult:
    contract_version: str
    contract_sha256: str
    parent_contract_version: str
    parent_contract_sha256: str
    language_detection_version: str
    validator_version: str
    repair_policy: str
    raw_answer_sha: str
    query_language: str | None
    query_language_status: str
    abstention_detected: bool
    expected_abstention_marker: str | None
    actual_abstention_marker: str | None
    marker_at_start: bool | None
    marker_language_valid: bool | None
    answer_body_language: str | None
    answer_body_language_status: str
    body_language_valid: bool | None
    body_language_evidence: dict
    malformed_citations: list
    unknown_handles: list
    citation_syntax_valid: bool
    doc_leaks: list
    page_leaks: list
    slide_leaks: list
    path_leaks: list
    template_leaks: list
    thinking_marker_leaks: list
    material_claim_count: int
    claims_with_citation: int
    citation_coverage: float | None
    citation_coverage_status: str
    contract_valid: bool
    failure_reasons: list

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def enforce(answer: str, query_language: str | None, exposed_evidence_ids,
            answerability: str | None = None) -> ContractResult:
    """Validate one generated answer. Returns a verdict; never modifies the answer.

    Control flow mirrors v1 exactly. Every non-language check calls v1's own validator and
    constants, so those semantics are the same code, not a copy of it.
    """
    if query_language is not None and query_language not in SUPPORTED_LANGUAGES:
        raise ContractConfigError(f"unsupported query language {query_language!r}; "
                                  f"supported: {SUPPORTED_LANGUAGES}")
    reasons: list[str] = []

    if query_language is None:
        detected = detect_language(answer)
        query_language, query_language_status = detected["language"], f"inferred_{detected['status']}"
        if query_language is None:
            reasons.append("query_language_ambiguous")
    else:
        query_language_status = "provided"

    if not answer.strip():
        reasons.append("empty_answer")

    citations = gen.validate_citations(answer, set(exposed_evidence_ids))
    malformed, unknown = citations["malformed_citations"], citations["unknown_handles"]
    if malformed:
        reasons.append("malformed_citation")
    if unknown:
        reasons.append("unknown_citation")
    for field_name, reason in (("doc_leaks", "source_coordinate_leak"),
                               ("page_leaks", "source_coordinate_leak"),
                               ("slide_leaks", "source_coordinate_leak"),
                               ("path_leaks", "source_coordinate_leak"),
                               ("template_leaks", "template_leak")):
        if citations[field_name] and reason not in reasons:
            reasons.append(reason)
    leaks = [m for m in THINKING_MARKERS if m in answer]
    if leaks:
        reasons.append("thinking_marker_leak")

    found = ANY_MARKER.search(answer)
    actual_marker = None
    if found:
        actual_marker = ("YETERSİZ KANIT" if found.group(1).upper().startswith("YET")
                         else "INSUFFICIENT EVIDENCE")
    at_start = bool(MARKER_AT_START.match(answer.lstrip())) if found else None
    abstained = bool(at_start)
    expected_marker = MARKER_FOR_LANGUAGE.get(query_language) if query_language else None
    marker_valid = None
    if abstained:
        marker_valid = actual_marker == expected_marker
        if not marker_valid:
            reasons.append("wrong_abstention_marker_language")
    elif found and at_start is False:
        reasons.append("abstention_marker_not_at_start")

    body = _body_after_marker(answer)
    detected_body = detect_language(body)
    body_language, body_status = detected_body["language"], detected_body["status"]
    body_valid = None
    if body_status == "confident" and query_language:
        body_valid = body_language == query_language
        if not body_valid:
            reasons.append("answer_body_language_mismatch")
    elif body_status == "ambiguous" and query_language:
        reasons.append("answer_body_language_ambiguous")

    material, cited, coverage = coverage_telemetry(answer)

    return ContractResult(
        contract_version=CONTRACT_VERSION, contract_sha256=implementation_sha256(),
        parent_contract_version=PARENT_CONTRACT_VERSION,
        parent_contract_sha256=PARENT_CONTRACT_SHA,
        language_detection_version=LANGUAGE_DETECTION_VERSION,
        validator_version=VALIDATOR_VERSION, repair_policy=REPAIR_POLICY,
        raw_answer_sha=hashlib.sha256(answer.encode("utf-8")).hexdigest(),
        query_language=query_language, query_language_status=query_language_status,
        abstention_detected=abstained, expected_abstention_marker=expected_marker,
        actual_abstention_marker=actual_marker, marker_at_start=at_start,
        marker_language_valid=marker_valid, answer_body_language=body_language,
        answer_body_language_status=body_status, body_language_valid=body_valid,
        body_language_evidence=detected_body,
        malformed_citations=malformed, unknown_handles=unknown,
        citation_syntax_valid=not malformed and not unknown,
        doc_leaks=citations["doc_leaks"], page_leaks=citations["page_leaks"],
        slide_leaks=citations["slide_leaks"], path_leaks=citations["path_leaks"],
        template_leaks=citations["template_leaks"], thinking_marker_leaks=leaks,
        material_claim_count=material, claims_with_citation=cited, citation_coverage=coverage,
        citation_coverage_status="telemetry_only_not_enforced",
        contract_valid=not reasons, failure_reasons=reasons)


if __name__ == "__main__":
    print(json.dumps({"contract_version": CONTRACT_VERSION,
                      "parent_contract_version": PARENT_CONTRACT_VERSION,
                      "parent_contract_sha256": PARENT_CONTRACT_SHA,
                      "implementation_sha256": implementation_sha256(),
                      "language_detection_version": LANGUAGE_DETECTION_VERSION,
                      "validator_version": VALIDATOR_VERSION,
                      "repair_policy": REPAIR_POLICY,
                      "supported_languages": list(SUPPORTED_LANGUAGES),
                      "marker_mapping": MARKER_FOR_LANGUAGE}, indent=2, ensure_ascii=False))
