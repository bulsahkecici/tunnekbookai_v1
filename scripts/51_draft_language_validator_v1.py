"""Draft Language Validator v1.

The first SEC-02-2 pilot emitted two units of untranslated English into a DraftIR whose own
header declared `language: "tr"`. One of them - U-C-P01-S03 - was rejected, but for an unrelated
reason: the English text had also dropped the claim's tunnel-size condition. The other,
U-C-P01-S02, passed every one of the nine validation stages and would have been rendered into a
Turkish book as an English sentence.

That is the defect this module exists to close. A unit whose language does not match the draft's
declared language is a translation failure, and it must fail as one rather than being caught by
accident when some other rule happens to fire.

Three commitments:

**No LLM judge.** Language is decided by declared lexicons and orthography, both frozen in
data/book/drafting/contracts/draft_language_contract_v1.json. A model asked "is this Turkish?"
would be more accurate on edge cases and would have no auditable failure mode; this detector can
be read, disagreed with, and regression-tested case by case.

**Evidence language is not book language.** The corpus is bilingual and half the approved claims
for this section are English. An English *source* is not a licence for English *prose*: §109 of
the drafting contract requires a faithful Turkish paraphrase, and the citation still resolves to
the English original. So the detector never looks at the claim's language, only at the text.

**Domain terms are not language evidence.** 'shotcrete', 'flashcrete', 'MPa', 'C25/30', 'FHWA',
'TS 4559' are the vocabulary of the field, and a Turkish sentence that uses them is still Turkish.
They are declared neutral in the contract and score for neither side. A complete English clause is
a different thing entirely, and that distinction - term versus clause - is the whole design.

The orthographic signal deserves a note, because it is what makes the detector work on technical
prose where function words are sparse. Turkish has no q/w/x and none of the digraphs th, ck, ph,
gh, sh, wh, oo, ee, ea. English has them constantly - 'the', 'thickness', 'crushed', 'squeezing'.
Turkish carries its own: ç, ğ, ı, ö, ş, ü appear in nearly every content word of a technical
Turkish sentence. Neither signal needs a stemmer, a model, or a word list that grows per section.

Fail closed, asymmetrically: a *material* unit whose language cannot be determined with confidence
is rejected (LANGUAGE_AMBIGUOUS), because a material unit is an assertion the reader will act on.
A non-material unit - a heading, a transition - is rejected only on confident English, because
headings are short enough that demanding positive evidence would reject 'Çimento Dozajı' for
being two words long.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

LANGUAGE_VALIDATOR_VERSION = "tunnelbook-draft-language-validator-v1"
LANGUAGE_CONTRACT_VERSION = "tunnelbook-draft-language-contract-v1"
DETECTOR_VERSION = "tunnelbook-lexical-orthographic-detector-v1"
SECTION_ID = "SEC-02-2"

LANGUAGE_CONTRACT_PATH = (ROOT / "data" / "book" / "drafting" / "contracts"
                          / "draft_language_contract_v1.json")

FAILURE_CODES = ("LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS")


# ================================================================ 1. the frozen lexicons

# Function words carry language identity without carrying subject matter, which is exactly what is
# wanted: a list of technical nouns would have to grow with every new section, while 'için' and
# 'of' are the same in a shotcrete section and a grouting one.
TURKISH_FUNCTION_WORDS = [
    "ve", "ile", "için", "olarak", "olan", "olup", "olması", "olmak", "gibi", "göre", "kadar",
    "sonra", "önce", "arasında", "üzerine", "üzerinde", "altında", "daha", "çok", "az", "bazı",
    "veya", "ya", "ise", "ancak", "fakat", "ayrıca", "bunun", "bunlar", "şekilde", "biçimde",
    "durumda", "durumlarda", "durumunda", "halinde", "koşulda", "koşullarda", "bir", "bu", "şu",
    "her", "aynı", "farklı", "diğer", "yer", "yerine", "ila", "arası", "yani", "böylece",
    "burada", "aşağıda", "yukarıda", "ilgili", "ilişkin", "dair", "karşı", "doğru", "boyunca",
    "birlikte", "ayrı", "vardır", "yoktur", "değildir", "değil", "olmayan", "olmadan", "ilk",
    "son", "sonraki", "önceki", "hem", "de", "da", "ki", "en", "tüm", "bütün", "özel", "genel",
    "iki", "üç", "dört", "beş", "adet", "toplam", "eğer", "nedeniyle", "amacıyla", "tarafından",
]

# Deliberately function words and auxiliaries only. Adding English technical nouns would make the
# detector score 'thickness' as English evidence and then, one section later, score a Turkish
# sentence that names an English standard as English too.
ENGLISH_FUNCTION_WORDS = [
    "the", "a", "an", "of", "and", "or", "but", "in", "on", "at", "to", "from", "with", "without",
    "for", "by", "as", "such", "is", "are", "was", "were", "be", "been", "being", "has", "have",
    "had", "may", "can", "shall", "should", "must", "will", "would", "not", "no", "this", "that",
    "these", "those", "it", "its", "which", "when", "where", "while", "than", "then", "there",
    "here", "some", "any", "all", "more", "most", "less", "least", "up", "out", "into", "over",
    "under", "between", "about", "after", "before", "during", "if", "unless", "also", "both",
]

# Turkish has no q, w or x, and none of these digraphs. English is full of them. The signal is
# orthographic rather than lexical, so it does not need a word list and does not go stale.
ENGLISH_ORTHOGRAPHY = ["th", "ck", "ph", "gh", "sh", "wh", "oo", "ee", "ea"]
ENGLISH_ONLY_LETTERS = "qwx"
TURKISH_LETTERS = "çğıöşü"

# ASCII-only Turkish endings, kept short because most Turkish morphology already carries a Turkish
# letter and is caught by the orthographic rule. These exist for the residue - 'katmanlar',
# 'tabakalar' - and are guarded by a minimum length and by the English-digraph test.
TURKISH_SUFFIXES = [
    "lar", "ler", "dir", "dur", "tir", "tur", "nin", "nun", "leri", "lari", "inde", "unda",
    "acak", "ecek", "deki", "teki", "sinde", "sonra",
]
TURKISH_SUFFIX_MIN_LENGTH = 7

# English words whose tails collide with a Turkish suffix. Without this the orthography-free
# residue of an English clause ('smaller', 'similar') would score as Turkish evidence.
ENGLISH_SUFFIX_EXCEPTIONS = [
    "smaller", "larger", "similar", "particular", "regular", "circular", "angular", "cellular",
    "granular", "modular", "annular", "tubular", "dollar", "collar", "filler", "director",
    "structur", "consider", "further", "another", "however", "greater", "matter", "better",
]

# Field vocabulary and unit symbols. These are the terms §24 forbids the detector from reading as
# English, and §27 permits to stay in Turkish prose as domain terms.
NEUTRAL_DOMAIN_TERMS = [
    "shotcrete", "flashcrete", "gunite", "sprayed", "mpa", "kpa", "gpa", "kg", "m3", "mm", "cm",
    "dm", "km", "inch", "inches", "kn", "mpa'dır", "fhwa", "aashto", "astm", "aci", "iso", "din",
    "kgm", "kts", "ts", "nato", "natm", "rmr", "usa", "abd", "tbm", "pdf", "doc",
]

# Table numbers, clause numbers, standard designations and strength classes are addresses, not
# words. Masking them keeps 'C25/30' and 'Tablo-351-5' out of the token stream entirely.
REFERENCE_MASKS = [
    r"[Tt]ablo\s?-?\s?\d+(?:-\d+)*-?[A-Za-z]?",
    r"[Tt]able\s?-?\s?\d+(?:-\d+)*-?[A-Za-z]?",
    r"§?\s?\d+(?:\.\d+){2,4}",
    r"[Tt][Ss]\s?\d+",
    r"[Ee][Nn]\s?\d{3,}",
    r"C\s?\d{2}\s?/\s?\d{2}",
    r"\bDOC\d{6}\b",
    r"SRC-[A-Za-z0-9]+-[0-9a-f]{12}",
    r"SEC-\d{2}-\d-[A-Za-z0-9-]+",
]

# A clause shorter than this asserts too little to be scored. Below the threshold a fragment like
# 'Kuru Sistem:' would be judged on two tokens, and a two-token verdict is noise.
SUBSTANTIVE_CLAUSE_TOKENS = 4
# Two independent English function words, not one. 'can' is also a Turkish noun and 'de' is also
# an English fragment; one hit is a collision, two is a clause.
ENGLISH_CLAUSE_MIN_EVIDENCE = 2


def build_contract(section_language: str = "tr") -> dict:
    """The frozen language contract. Deterministic - no timestamp, so the SHA is stable.

    Every list the detector uses lives here rather than in the code, which is what makes the
    detector's behaviour auditable from an artifact rather than from a diff.
    """
    return {
        "contract_version": LANGUAGE_CONTRACT_VERSION,
        "parent_contract_version": "tunnelbook-section-drafting-contract-v1",
        "section_id": SECTION_ID,
        "section_language": section_language,
        "allowed_visible_languages": [section_language],
        "source_claim_languages": ["tr", "en"],
        "translation_policy": {
            "rule": "An English approved claim is rendered as a faithful Turkish paraphrase.",
            "forbidden": [
                "leaving an English source claim untranslated in visible prose",
                "strengthening the claim while translating",
                "dropping a condition while translating",
                "dropping a qualifier while translating",
                "changing a numeric value or its unit while translating",
                "adding interpretation not present in the source claim",
            ],
            "must_preserve": ["numeric values", "units", "conditions", "modalities",
                              "qualifiers", "material scope", "system scope",
                              "technical meaning"],
            "citation": "the Turkish paraphrase cites the English original's source key",
            "evidence_language_is_not_book_language": (
                "The corpus is bilingual. An English source is a licence to state the fact, not a "
                "licence to state it in English."),
        },
        "proper_noun_policy": {
            "rule": "Organisation names, standard designations, document titles and table numbers "
                    "are neither Turkish nor English evidence.",
            "masked_patterns": REFERENCE_MASKS,
            "rationale": "'Tablo-351-5' and 'TS 4559' are addresses. Scoring them would make a "
                         "correctly cited Turkish sentence look foreign.",
        },
        "technical_term_policy": {
            "rule": "A recognised English technical term may remain inside otherwise Turkish "
                    "prose. A complete English clause may not.",
            "permitted_examples": ["shotcrete", "flashcrete", "MPa", "C25/30", "FHWA", "TS 4559",
                                   "kg/m³", "mm", "cm"],
            "forbidden_examples": [
                "The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches.",
                "In some specific rock conditions the thickness may be 12 inches and more.",
            ],
            "boundary": "term, not clause",
        },
        "detector": {
            "detector_version": DETECTOR_VERSION,
            "method": "declared function-word lexicons plus orthographic signals",
            "llm_judge": False,
            "turkish_function_words": TURKISH_FUNCTION_WORDS,
            "english_function_words": ENGLISH_FUNCTION_WORDS,
            "turkish_letters": TURKISH_LETTERS,
            "turkish_suffixes": TURKISH_SUFFIXES,
            "turkish_suffix_min_length": TURKISH_SUFFIX_MIN_LENGTH,
            "english_orthography_digraphs": ENGLISH_ORTHOGRAPHY,
            "english_only_letters": ENGLISH_ONLY_LETTERS,
            "english_suffix_exceptions": ENGLISH_SUFFIX_EXCEPTIONS,
            "neutral_domain_terms": NEUTRAL_DOMAIN_TERMS,
            "substantive_clause_tokens": SUBSTANTIVE_CLAUSE_TOKENS,
            "english_clause_min_evidence": ENGLISH_CLAUSE_MIN_EVIDENCE,
        },
        "detector_version": DETECTOR_VERSION,
        "enforcement": {
            "material_units": "reject on mismatch and on ambiguity (fail closed)",
            "non_material_units": "reject only on confident English; ambiguity tolerated",
            "non_material_rationale": "A heading is too short to demand positive evidence from. "
                                      "'Çimento Dozajı' is two words and would fail an "
                                      "ambiguity gate that a material sentence passes easily.",
            "auto_translation_repair": False,
            "auto_translation_repair_rationale":
                "The validator rejects; it never translates. A validator that repaired its own "
                "input would launder a translation failure into a pass and record it as one.",
        },
        "failure_codes": {
            "LANGUAGE_MISMATCH": "visible prose is not in the section language",
            "LANGUAGE_AMBIGUOUS": "a material unit's language could not be determined with "
                                  "confidence; fail closed",
        },
        "validator_implementation": "scripts/51_draft_language_validator_v1.py",
        "validator_version": LANGUAGE_VALIDATOR_VERSION,
        "version": LANGUAGE_CONTRACT_VERSION,
    }


def load_contract(path: Path = LANGUAGE_CONTRACT_PATH) -> dict:
    if not path.exists():
        return build_contract()
    return json.loads(path.read_text(encoding="utf-8"))


# ================================================================ 2. text handling

def normalise(text: str) -> str:
    """Lowercase without the Turkish-I fold the draft validator uses.

    scripts/49 folds 'I' to 'ı' because it is comparing Turkish against Turkish. Here that would
    turn English 'In' into 'ın' and lose an English function word, so only the dotted capital is
    special-cased and everything else takes ordinary lowercasing.
    """
    text = text.replace("İ", "i")
    return unicodedata.normalize("NFKC", text).lower()


def mask_references(text: str, contract: dict) -> str:
    for pattern in contract["proper_noun_policy"]["masked_patterns"]:
        text = re.sub(pattern, " ", text)
    return text


TOKEN_RE = re.compile(r"[0-9a-zçğıöşü]+", re.UNICODE)


def tokenise(text: str, contract: dict) -> list[str]:
    """Words only. Apostrophes split, so 'mm'dir' yields 'mm' and 'dir'.

    That split is load-bearing rather than incidental: Turkish attaches its copula to a foreign
    unit symbol through an apostrophe, and keeping 'dir' visible is what lets a sentence made
    almost entirely of unit symbols still read as Turkish.
    """
    masked = mask_references(text, contract)
    return [t for t in TOKEN_RE.findall(normalise(masked)) if not t.isdigit()]


CLAUSE_SPLIT_RE = re.compile(r"[.;:!?\n]|,|\s[-–—]\s")


def clauses(text: str) -> list[str]:
    return [c.strip() for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]


# ================================================================ 3. scoring

@dataclass
class Score:
    turkish: int = 0
    english: int = 0
    neutral: int = 0
    unknown: int = 0
    turkish_evidence: list[str] = field(default_factory=list)
    english_evidence: list[str] = field(default_factory=list)

    @property
    def scored_tokens(self) -> int:
        return self.turkish + self.english + self.unknown


def _detector(contract: dict) -> dict:
    return contract["detector"]


def classify_token(token: str, detector: dict) -> str:
    """One token, one verdict: 'tr', 'en', 'neutral' or 'unknown'.

    Order is the design. Neutral first, so no domain term ever becomes evidence. English function
    words before the Turkish orthographic test, so an English word carrying no digraph is still
    seen. The Turkish suffix rule last and most guarded, because it is the only rule here that
    can fire on an English word.
    """
    if token in detector["neutral_domain_terms"]:
        return "neutral"
    if token in detector["english_function_words"]:
        return "en"
    if token in detector["turkish_function_words"]:
        return "tr"
    if any(letter in token for letter in detector["turkish_letters"]):
        return "tr"
    if any(letter in token for letter in detector["english_only_letters"]):
        return "en"
    if any(digraph in token for digraph in detector["english_orthography_digraphs"]):
        return "en"
    if any(token.startswith(stem) for stem in detector["english_suffix_exceptions"]):
        return "en"
    if len(token) >= detector["turkish_suffix_min_length"]:
        for suffix in detector["turkish_suffixes"]:
            if token.endswith(suffix):
                return "tr"
    return "unknown"


def score(text: str, contract: dict) -> Score:
    detector = _detector(contract)
    result = Score()
    for token in tokenise(text, contract):
        verdict = classify_token(token, detector)
        if verdict == "tr":
            result.turkish += 1
            result.turkish_evidence.append(token)
        elif verdict == "en":
            result.english += 1
            result.english_evidence.append(token)
        elif verdict == "neutral":
            result.neutral += 1
        else:
            result.unknown += 1
    return result


@dataclass
class Detection:
    language: str
    unit_score: dict
    english_clauses: list[str]
    clause_scores: list[dict]
    detector_version: str = DETECTOR_VERSION

    def as_dict(self) -> dict:
        return asdict(self)


def detect(text: str, contract: dict | None = None) -> Detection:
    """Whole-unit verdict, with a clause pass that the whole-unit pass cannot do.

    A paragraph that is nine-tenths Turkish and one-tenth an English clause scores Turkish
    overall. §26 says that is a mismatch, and the only way to see it is to look at the clauses -
    which is also why a single borrowed term never triggers it: one term is not a clause.
    """
    contract = contract or load_contract()
    detector = _detector(contract)
    unit = score(text, contract)

    english_clauses, clause_rows = [], []
    for clause in clauses(text):
        clause_score = score(clause, contract)
        substantive = clause_score.scored_tokens >= detector["substantive_clause_tokens"]
        is_english = (substantive
                      and clause_score.english >= detector["english_clause_min_evidence"]
                      and clause_score.english > clause_score.turkish)
        clause_rows.append({"clause": clause, "turkish": clause_score.turkish,
                            "english": clause_score.english, "neutral": clause_score.neutral,
                            "unknown": clause_score.unknown, "substantive": substantive,
                            "english_clause": is_english})
        if is_english:
            english_clauses.append(clause)

    if english_clauses:
        language = "mixed" if unit.turkish > 0 else "en"
    elif unit.turkish == 0 and unit.english == 0:
        language = "unknown"
    elif unit.english > unit.turkish:
        language = "en"
    elif unit.turkish > unit.english:
        language = "tr"
    else:
        language = "unknown"

    return Detection(language=language, unit_score=asdict(unit), english_clauses=english_clauses,
                     clause_scores=clause_rows)


# ================================================================ 4. unit validation

@dataclass
class LanguageFailure:
    code: str
    unit_id: str
    detail: str
    required_action: str
    stage: str = "J_language"
    claim_ids: list[str] = field(default_factory=list)
    rule_id: str | None = None
    evidence: str | None = None
    detected_language: str | None = None


def validate_unit(unit_id: str, unit_type: str, material: bool, section_language: str,
                  text: str, claim_ids: Iterable[str] | None = None,
                  contract: dict | None = None) -> list[LanguageFailure]:
    """§22-§29. Material units fail closed; non-material units fail only on confident English."""
    contract = contract or load_contract()
    claim_ids = list(claim_ids or [])
    allowed = contract["allowed_visible_languages"]
    detection = detect(text, contract)

    if detection.language in allowed:
        return []

    if detection.language == "unknown":
        if not material:
            return []
        return [LanguageFailure(
            code="LANGUAGE_AMBIGUOUS", unit_id=unit_id,
            detail=(f"the language of this material unit could not be determined: "
                    f"{detection.unit_score['turkish']} Turkish and "
                    f"{detection.unit_score['english']} English signals over "
                    f"{detection.unit_score['unknown']} unresolved tokens"),
            required_action=(f"rewrite the unit in {section_language} using ordinary "
                             f"{section_language} sentence structure; a unit made only of "
                             f"symbols and figures asserts nothing a reader can check"),
            claim_ids=claim_ids, rule_id="LANG-002", detected_language=detection.language)]

    evidence = (detection.english_clauses[0] if detection.english_clauses
                else " ".join(detection.unit_score["english_evidence"][:8]))
    if not material and detection.language not in ("en", "mixed"):
        return []
    detail = (f"the section language is {section_language!r} but this unit reads as "
              f"{detection.language!r}")
    if detection.english_clauses:
        detail += (f"; {len(detection.english_clauses)} substantive English clause(s) survive "
                   f"into visible prose")
    return [LanguageFailure(
        code="LANGUAGE_MISMATCH", unit_id=unit_id, detail=detail,
        required_action=(f"render this unit as a faithful {section_language} paraphrase of the "
                         f"claims it declares, preserving every figure, unit, condition, "
                         f"qualifier and modality; do not copy an English source claim verbatim"),
        claim_ids=claim_ids, rule_id="LANG-001", evidence=evidence,
        detected_language=detection.language)]


def validate_units(units: Iterable[Any], section_language: str,
                   contract: dict | None = None) -> list[LanguageFailure]:
    contract = contract or load_contract()
    failures: list[LanguageFailure] = []
    for unit in units:
        failures += validate_unit(
            unit_id=unit.unit_id, unit_type=unit.unit_type, material=unit.material,
            section_language=section_language, text=unit.text, claim_ids=unit.claim_ids,
            contract=contract)
    return failures


# ================================================================ 5. fixture harness

def run_fixtures(fixtures: list[dict], contract: dict | None = None) -> dict[str, Any]:
    """A language false accept is English prose the detector called Turkish. It must be zero."""
    contract = contract or load_contract()
    rows, false_accepts, false_rejects, mismatches = [], [], [], []
    for fixture in fixtures:
        failures = validate_unit(
            unit_id=fixture.get("unit_id", "U-X-P01-S01"),
            unit_type=fixture.get("unit_type", "PARAGRAPH_SENTENCE"),
            material=fixture.get("material", True),
            section_language=fixture.get("section_language", "tr"),
            text=fixture["text"], claim_ids=fixture.get("claim_ids", []), contract=contract)
        actual = sorted({f.code for f in failures})
        expected_valid = fixture["expected_valid"]
        detection = detect(fixture["text"], contract)
        row = {"case_id": fixture["case_id"], "expected_valid": expected_valid,
               "actual_valid": not failures,
               "expected_failure_codes": sorted(fixture.get("expected_failure_codes", [])),
               "actual_failure_codes": actual, "detected_language": detection.language,
               "polarity": "positive" if expected_valid else "negative",
               "detail": [f.detail for f in failures]}
        if expected_valid and failures:
            false_rejects.append(fixture["case_id"])
            row["outcome"] = "FALSE_REJECT"
        elif not expected_valid and not failures:
            false_accepts.append(fixture["case_id"])
            row["outcome"] = "FALSE_ACCEPT"
        else:
            expected = set(fixture.get("expected_failure_codes", []))
            if expected and not expected <= set(actual):
                mismatches.append(fixture["case_id"])
                row["outcome"] = "CODE_MISMATCH"
            else:
                row["outcome"] = "PASS"
        rows.append(row)
    passed = [r for r in rows if r["outcome"] == "PASS"]
    return {"total": len(rows), "passed": len(passed),
            "positive": sum(1 for r in rows if r["polarity"] == "positive"),
            "negative": sum(1 for r in rows if r["polarity"] == "negative"),
            "false_accepts": false_accepts, "false_rejects": false_rejects,
            "code_mismatches": mismatches, "rows": rows,
            "all_pass": len(passed) == len(rows)}


if __name__ == "__main__":
    print(f"{LANGUAGE_VALIDATOR_VERSION}\nThis module is a library. Run "
          f"scripts/50_sec_02_2_draft_failure_remediation_v1.py to author the language contract, "
          f"score the fixtures and run the remediation.")
