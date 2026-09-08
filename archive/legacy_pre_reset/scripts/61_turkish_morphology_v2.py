"""M3 — deterministic Turkish morphology, bounded to what SEC-02-2 realization actually needs.

This is not a Turkish NLP library and must not grow into one. Every rule below exists because a
frozen SEC-02-2 surface form exhibits it, and each is fixtured against that form rather than
against a grammar textbook. The fixtures are in the contract artifact, so the claim "this rule is
required" is auditable rather than asserted.

What the frozen material forces:

  `100-150 mm'dir`   in SEC-02-2-C-009's canonical  → copula, front-vowel harmony over an
                                                       abbreviation read as *milimetre*
  `25,5 MPa'dır`     in SEC-02-2-C-002's canonical  → copula, back-vowel harmony over an
                                                       abbreviation read as *megapaskal*
  `uygulamasında`    in SEC-02-2-C-009's canonical  → possessive + locative with a buffer
                                                       consonant on a vowel-final stem
  `kalınlığı`        in the P0-008 glosses          → k → ğ before a vowel-initial suffix
  `kaplamanın`       in the P0-007 glosses          → genitive with a buffer consonant

Abbreviations are the reason this module cannot be a pure string transformation. Turkish suffixes
harmonise with the last vowel of the word as *pronounced*, and `mm` and `MPa` contain no vowel to
harmonise with. `mm` is read *milimetre* and takes a front vowel; `MPa` is read *megapaskal* and
takes a back one. That mapping is data, not inference, so it lives in a frozen table and an
abbreviation missing from it raises rather than guesses. Guessing here would produce `mm'dır`,
which is wrong, and wrong in a way no validator downstream would catch — support containment sees
the token `dır`, and `dır` is licensed by the claim that legitimately writes `MPa'dır`.

Every function is pure: same input, same output, no state, no clock, no randomness, no I/O.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MORPHOLOGY_VERSION = "tunnelbook-turkish-morphology-v2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
CONTRACT_PATH = ARCH_V2 / "contracts" / "turkish_morphology_v2.json"

BACK_VOWELS = "aıou"
FRONT_VOWELS = "eiöü"
ROUNDED = "ouöü"
VOWELS = BACK_VOWELS + FRONT_VOWELS

# A suffix beginning with a stop is devoiced after a voiceless consonant: 'MPa'dır' but
# 'kat'tır'. These are the Turkish voiceless set, "fıstıkçı şahap".
VOICELESS = set("fstkçşhp")

# Word-final stops soften before a vowel-initial suffix. 'kalınlık' + possessive is
# 'kalınlığı', which is the form the frozen P0-008 glosses carry.
SOFTENING = {"k": "ğ", "p": "b", "ç": "c", "t": "d"}

# Abbreviations carry no vowel, so harmony has nothing to read. How each is pronounced is data.
# An abbreviation absent from this table raises; it is never guessed.
ABBREVIATION_PRONUNCIATION = {
    "mm": "milimetre",
    "cm": "santimetre",
    "m": "metre",
    "mpa": "megapaskal",
    "kg/m3": "kilogram bölü metreküp",
    "kg/m³": "kilogram bölü metreküp",
    "°c": "santigrat derece",
    "gün": "gün",
    "saat": "saat",
    "adet": "adet",
}


class MorphologyError(ValueError):
    """Raised rather than guessed. A wrong suffix is not visible to any downstream validator."""


# ================================================================ primitives

def last_vowel(word: str) -> str:
    """The last vowel of a word, which is what every Turkish suffix harmonises with."""
    for character in reversed(word.lower()):
        if character in VOWELS:
            return character
    raise MorphologyError(f"{word!r} contains no vowel to harmonise with")


def pronounce(token: str) -> str:
    """The spoken form of an abbreviation, or the token itself when it already has a vowel."""
    key = token.lower()
    if key in ABBREVIATION_PRONUNCIATION:
        return ABBREVIATION_PRONUNCIATION[key]
    if any(character in VOWELS for character in key):
        return token
    raise MorphologyError(
        f"{token!r} has no vowel and no frozen pronunciation; harmony cannot be inferred")


def harmony_two(word: str) -> str:
    """Two-way harmony: the -A archiphoneme, realised as 'a' or 'e'."""
    return "a" if last_vowel(pronounce(word)) in BACK_VOWELS else "e"


def harmony_four(word: str) -> str:
    """Four-way harmony: the -I archiphoneme, realised as 'ı', 'i', 'u' or 'ü'."""
    vowel = last_vowel(pronounce(word))
    back = vowel in BACK_VOWELS
    rounded = vowel in ROUNDED
    if back:
        return "u" if rounded else "ı"
    return "ü" if rounded else "i"


def ends_with_vowel(word: str) -> bool:
    stripped = word.rstrip(".")
    return bool(stripped) and stripped[-1].lower() in VOWELS


def is_voiceless_final(word: str) -> bool:
    """Whether a suffix-initial stop devoices after this word, judged on the spoken form."""
    spoken = pronounce(word).rstrip(".")
    return bool(spoken) and spoken[-1].lower() in VOICELESS


def soften_final(word: str) -> str:
    """k → ğ, p → b, ç → c, t → d before a vowel-initial suffix. 'kalınlık' → 'kalınlığ'."""
    if not word:
        return word
    final = word[-1].lower()
    if final in SOFTENING and len(word) > 2:
        return word[:-1] + SOFTENING[final]
    return word


def _attach(stem: str, suffix: str, apostrophe: bool) -> str:
    return f"{stem}'{suffix}" if apostrophe else f"{stem}{suffix}"


def _needs_apostrophe(stem: str) -> bool:
    """Abbreviations and figures take their suffix after an apostrophe: 'MPa'dır', '150 mm'dir'."""
    tail = stem.split()[-1] if stem.split() else stem
    return tail.lower() in ABBREVIATION_PRONUNCIATION and not tail.isalpha() or (
        tail.lower() in ABBREVIATION_PRONUNCIATION)


# ================================================================ suffixes

def copula(stem: str) -> str:
    """The -dIr copula. 'mm' → \"mm'dir\", 'MPa' → \"MPa'dır\", both frozen SEC-02-2 forms."""
    tail = stem.split()[-1] if stem.split() else stem
    consonant = "t" if is_voiceless_final(tail) else "d"
    return _attach(stem, f"{consonant}{harmony_four(tail)}r", _needs_apostrophe(tail))


def plural(stem: str) -> str:
    """The -lAr plural."""
    return f"{stem}l{harmony_two(stem)}r"


def possessive_third(stem: str) -> str:
    """The -(s)I third-person possessive. 'kalınlık' → 'kalınlığı'."""
    if ends_with_vowel(stem):
        return f"{stem}s{harmony_four(stem)}"
    return f"{soften_final(stem)}{harmony_four(stem)}"


def locative(stem: str, after_possessive: bool = False) -> str:
    """The -DA locative. After a possessive it takes the -n buffer: 'uygulaması' → 'uygulamasında'."""
    consonant = "t" if is_voiceless_final(stem) else "d"
    buffer = "n" if after_possessive else ""
    return f"{stem}{buffer}{consonant}{harmony_two(stem)}"


def dative(stem: str, after_possessive: bool = False) -> str:
    """The -A dative, with the -y buffer after a vowel."""
    buffer = "n" if after_possessive else ("y" if ends_with_vowel(stem) else "")
    return f"{soften_final(stem) if not buffer else stem}{buffer}{harmony_two(stem)}"


def genitive(stem: str) -> str:
    """The -In genitive, with the -n buffer after a vowel. 'kaplama' → 'kaplamanın'."""
    if ends_with_vowel(stem):
        return f"{stem}n{harmony_four(stem)}n"
    return f"{soften_final(stem)}{harmony_four(stem)}n"


def accusative(stem: str) -> str:
    """The -I accusative, with the -y buffer after a vowel."""
    if ends_with_vowel(stem):
        return f"{stem}y{harmony_four(stem)}"
    return f"{soften_final(stem)}{harmony_four(stem)}"


SUFFIXES = {
    "copula": copula,
    "plural": plural,
    "possessive_third": possessive_third,
    "locative": locative,
    "dative": dative,
    "genitive": genitive,
    "accusative": accusative,
}


# ================================================================ fixtures

# Each fixture names the frozen SEC-02-2 surface form that forces the rule. A rule with no
# frozen witness does not belong in this module.
FIXTURES = [
    {"operation": "copula", "stem": "mm", "expected": "mm'dir",
     "witness": "SEC-02-2-C-009 canonical: \"100-150 mm'dir\"",
     "phenomenon": "front harmony over an abbreviation read as milimetre"},
    {"operation": "copula", "stem": "MPa", "expected": "MPa'dır",
     "witness": "SEC-02-2-C-002 canonical: \"25,5 MPa'dır\"",
     "phenomenon": "back harmony over an abbreviation read as megapaskal"},
    {"operation": "copula", "stem": "cm", "expected": "cm'dir",
     "witness": "SEC-02-2-C-003 registers cm; santimetre takes a front vowel",
     "phenomenon": "front harmony, distinct from the MPa case"},
    {"operation": "possessive_third", "stem": "kalınlık", "expected": "kalınlığı",
     "witness": "SEC-02-2-P0-008 translation_glosses carry both 'kalınlık' and 'kalınlığı'",
     "phenomenon": "k → ğ before a vowel-initial suffix"},
    {"operation": "genitive", "stem": "kaplama", "expected": "kaplamanın",
     "witness": "SEC-02-2-P0-007 translation_glosses carry both 'kaplama' and 'kaplamanın'",
     "phenomenon": "genitive with the -n buffer after a vowel"},
    {"operation": "locative", "stem": "uygulaması", "expected": "uygulamasında",
     "witness": "SEC-02-2-C-009 canonical: \"uygulamasında\"",
     "phenomenon": "locative after a possessive, with the -n buffer",
     "kwargs": {"after_possessive": True}},
    {"operation": "plural", "stem": "tabaka", "expected": "tabakalar",
     "witness": "SEC-02-2-C-009 canonical: \"tabakalar\"",
     "phenomenon": "back harmony on the -lAr plural"},
    {"operation": "plural", "stem": "numune", "expected": "numuneler",
     "witness": "SEC-02-2-C-002 canonical carries 'numune' forms",
     "phenomenon": "front harmony on the -lAr plural"},
    {"operation": "accusative", "stem": "kriter", "expected": "kriteri",
     "witness": "SEC-02-2-C-002 qualifier: \"kabul kriteridir\"",
     "phenomenon": "four-way harmony on a front unrounded stem"},
    {"operation": "dative", "stem": "tabakalar", "expected": "tabakalara",
     "witness": "SEC-02-2-C-009 qualifier: \"kil zonlu tabakalara özgüdür\"",
     "phenomenon": "dative with the -y/-∅ choice on a consonant-final stem"},
]

NOT_IMPLEMENTED = [
    "verbal inflection, tense, aspect, person agreement",
    "compounding and derivational morphology",
    "the ablative, instrumental and equative cases",
    "possessives other than third-person singular",
    "vowel epenthesis and consonant deletion in loanwords",
    "irregular stems such as su, ne and the -yor exceptions",
]


def run_fixtures() -> list[dict]:
    results = []
    for fixture in FIXTURES:
        function = SUFFIXES[fixture["operation"]]
        actual = function(fixture["stem"], **fixture.get("kwargs", {}))
        results.append({**{k: v for k, v in fixture.items() if k != "kwargs"},
                        "actual": actual, "passed": actual == fixture["expected"]})
    return results


def determinism_probe() -> dict:
    """Same input, same output — asserted over repeated calls rather than assumed of the code."""
    repeats = []
    for _ in range(5):
        repeats.append(tuple(
            SUFFIXES[f["operation"]](f["stem"], **f.get("kwargs", {})) for f in FIXTURES))
    return {"runs": len(repeats), "identical": len(set(repeats)) == 1}


def build_contract() -> dict:
    fixtures = run_fixtures()
    determinism = determinism_probe()
    return {
        "version": MORPHOLOGY_VERSION,
        "scope": ("bounded to the phenomena SEC-02-2 realization requires. This is not a general "
                  "Turkish morphology library and may not become one."),
        "purity": ("every function is pure: no state, no clock, no randomness, no I/O, no model "
                   "call"),
        "implemented_phenomena": [
            "two-way vowel harmony (-A)",
            "four-way vowel harmony (-I), including rounding",
            "voicing assimilation on suffix-initial stops (d / t)",
            "word-final softening k → ğ, p → b, ç → c, t → d before a vowel-initial suffix",
            "buffer consonants -y, -n, -s",
            "plural -lAr",
            "third-person possessive -(s)I",
            "locative, dative, genitive and accusative cases",
            "copula -dIr, with apostrophe attachment after an abbreviation",
        ],
        "not_implemented": NOT_IMPLEMENTED,
        "abbreviation_pronunciation": ABBREVIATION_PRONUNCIATION,
        "abbreviation_policy": ("an abbreviation carries no vowel, so harmony has nothing to "
                                "read. The spoken form is frozen data; an abbreviation absent "
                                "from the table raises MorphologyError and is never guessed, "
                                "because 'mm'dır' would be wrong and support containment cannot "
                                "see it — 'dır' is licensed by the claim that writes 'MPa'dır'."),
        "fixtures": fixtures,
        "fixtures_passed": sum(1 for f in fixtures if f["passed"]),
        "fixtures_total": len(fixtures),
        "determinism": determinism,
    }


def main() -> int:
    contract = build_contract()
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"morphology contract written: {CONTRACT_PATH.relative_to(ROOT)}")
    print(f"fixtures {contract['fixtures_passed']}/{contract['fixtures_total']}, "
          f"deterministic: {contract['determinism']['identical']}")
    for fixture in contract["fixtures"]:
        if not fixture["passed"]:
            print(f"  FAIL {fixture['operation']}({fixture['stem']!r}) -> "
                  f"{fixture['actual']!r}, expected {fixture['expected']!r}")
    return 0 if contract["fixtures_passed"] == contract["fixtures_total"] else 1


if __name__ == "__main__":
    sys.exit(main())
