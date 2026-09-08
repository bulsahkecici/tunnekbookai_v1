"""Section Draft Validator v1.

The composition validator asks whether a set of claims may be *combined*. This one asks the
question one layer further down: whether a sentence someone actually wrote is licensed by the
claims it declares. Those are different failures. A drafter can satisfy every composition rule -
correct claims, correct scopes, no forbidden pair - and still write a sentence containing a fact
no source states, because the defect is inside the sentence rather than between two of them.

    "Kuru sistemde çimento miktarı 350 kg/m³'ten az olmamalıdır, çünkü bu miktar stabilite için
     optimum değerdir."

Every claim here is allowlisted, correctly scoped and correctly cited. The first half is exactly
what the source says. The second half is a proposition about optimality that appears in no
document in the corpus. Composition validation passes it. This module does not.

Four commitments, each with a cost that was accepted deliberately:

**Deterministic, no LLM judge.** Support is decided by lexical containment against the declared
claims, not by asking a model whether a sentence "follows". A model judge would be more fluent and
would have no auditable failure mode; this one can be read line by line and disagreed with.

**Fail closed, and strict about it.** A content word that no declared claim licenses is an
UNSUPPORTED_PROPOSITION even when it is harmless. The alternative - a permissive default - fails in
the direction that puts unsupported technical prose in a book, which is the only direction that
matters here.

**Self-consistency is enforced, not assumed.** Every rule in this module must pass the canonical
wording of the claim it governs. A condition-retention rule that rejects the source's own sentence
is not strict, it is broken, and the test suite asserts the difference. This is what forces the
split between unit-scope and paragraph-scope conditions below: SEC-02-2-P0-001 carries the
condition "özel uygulamalar dışında" while its own canonical text never says so - the carve-out
lives in a neighbouring clause - so demanding it inside the sentence would reject a faithful
paraphrase of the source.

**Turkish morphology is handled by prefix agreement, not by a stemmer.** 'kalınlık' and
'kalınlığı' share six leading characters across the k->ğ mutation; 'beton' and 'betonun' share
five. A five-character common prefix is the licensing test. It over-licenses occasionally
('minimum'/'minimize' agree on five) and that is the safe direction: the words that matter here -
ekonomik, optimum, yeterli, güvenli - share no root with anything on the allowlist, which the
fixtures assert directly rather than take on trust.

The rejection codes are the phase's contract with the next one. A pilot that fails must fail with
a code specific enough to act on, so nothing here reports a generic error.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1"
DRAFTING_CONTRACT_VERSION = "tunnelbook-section-drafting-contract-v1"
SECTION_ID = "SEC-02-2"

DRAFTING = ROOT / "data" / "book" / "drafting"
DRAFT_CONTRACTS = DRAFTING / "contracts"
DRAFTING_CONTRACT_PATH = DRAFT_CONTRACTS / "section_drafting_contract_v1.json"
VALIDATION_CONTRACT_PATH = DRAFT_CONTRACTS / "draft_validation_contract_v1.json"

RESOLUTION = ROOT / "data" / "book" / "sec_02_2_limitation_resolution"
ALLOWLIST_PATH = RESOLUTION / "claims" / "composition_safe_allowlist_v1.jsonl"
DENYLIST_PATH = RESOLUTION / "claims" / "composition_denylist_v1.jsonl"

REGISTRY_PATHS = (
    ROOT / "data" / "book" / "source_registry_v1.jsonl",
    ROOT / "data" / "book" / "p0_resolution" / "evidence" / "p0_source_registry_v1.jsonl",
    ROOT / "data" / "book" / "sec_02_2_readiness_closure" / "evidence"
    / "closure_source_registry_v1.jsonl",
)


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


composition = _load("composition_validator_v1",
                    "scripts/46_sec_02_2_claim_composition_validator_v1.py")


REJECTION_CODES = (
    "CLAIM_NOT_ALLOWLISTED",
    "CLAIM_DENYLISTED",
    "UNSUPPORTED_PROPOSITION",
    "CLAIM_EXPANSION",
    "NUMERIC_DRIFT",
    "UNIT_DRIFT",
    "MODALITY_DRIFT",
    "CONDITION_DROPPED",
    "QUALIFIER_DROPPED",
    "FORBIDDEN_SYNTHESIS",
    "UNSUPPORTED_RELATION",
    "DERIVED_VALUE_AS_SOURCE_STATED",
    "MISSING_SOURCE_KEY",
    "MISSING_CITATION",
    "UNKNOWN_SOURCE_KEY",
    "CITATION_SCOPE_MISMATCH",
    "NON_MATERIAL_MISCLASSIFIED",
    "PACKET_EID_LEAK",
    "INTERNAL_ID_LEAK",
    "SCHEMA_INVALID",
)

# How the composition validator's vocabulary maps into this one's. The mapping is deliberate
# rather than mechanical: UNQUALIFIED_SCOPE and AMBIGUOUS_SCOPE are both, from the drafter's
# point of view, a qualifier that failed to survive into prose.
COMPOSITION_CODE_MAP = {
    "UNQUALIFIED_SCOPE": "QUALIFIER_DROPPED",
    "AMBIGUOUS_SCOPE": "QUALIFIER_DROPPED",
    "FORBIDDEN_SYNTHESIS": "FORBIDDEN_SYNTHESIS",
    "UNSUPPORTED_RELATION": "UNSUPPORTED_RELATION",
    "DERIVED_VALUE_AS_SOURCE_STATED": "DERIVED_VALUE_AS_SOURCE_STATED",
    "CLAIM_NOT_ALLOWLISTED": "CLAIM_NOT_ALLOWLISTED",
    "CLAIM_SUPERSEDED": "CLAIM_DENYLISTED",
    "CLAIM_PARTIAL": "CLAIM_DENYLISTED",
    "CLAIM_UNSUPPORTED": "CLAIM_DENYLISTED",
    "MISSING_SOURCE_KEY": "MISSING_SOURCE_KEY",
}

UNIT_TYPES = ("HEADING", "PARAGRAPH_SENTENCE", "LIST_ITEM", "TABLE_CELL", "TRANSITION")
ALLOWED_RELATIONSHIPS = ("INDEPENDENT", "SAME_SCOPE_SUPPORT", "QUALIFIED_COMPARISON",
                         "SOURCE_SUPPORTED_RELATION", "NONE")
FORBIDDEN_RELATIONSHIPS = ("FORBIDDEN_SYNTHESIS", "UNKNOWN_RELATION")

PACKET_EID_RE = re.compile(r"\[\s*E\s*\d{3}\s*\]|(?<![A-Za-z])E\d{3}(?![A-Za-z])")
CLAIM_ID_RE = re.compile(r"SEC-\d{2}-\d(?:-[A-Z0-9]+)*-\w+|SEC-02-2-[A-Za-z0-9-]+")
SOURCE_KEY_RE = re.compile(r"SRC-[A-Za-z0-9]+-[0-9a-f]{12}")


# ================================================================ 1. text handling

def fold(text: str) -> str:
    """Case- and spacing-insensitive form. Turkish dotted-I is folded before lowercasing.

    Python's str.lower() maps 'İ' to 'i̇' (i plus combining dot), which then fails to compare
    equal to a plain 'i'. Folding it first is not cosmetic: 'İlk tabaka' is a condition anchor.
    """
    text = text.replace("İ", "i").replace("I", "ı")
    folded = unicodedata.normalize("NFKC", text).lower()
    folded = folded.replace("³", "3").replace("^3", "3").replace("²", "2")
    folded = re.sub(r"\s+", " ", folded)
    return folded.strip()


TOKEN_RE = re.compile(r"[0-9a-zçğıöşü]+(?:[./,][0-9a-zçğıöşü]+)*", re.UNICODE)


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(fold(text))


def content_tokens(text: str, function_lexicon: set[str], min_length: int = 3) -> list[str]:
    """Tokens that carry technical content, in the sense that matters for support checking.

    Short tokens are dropped because Turkish grammar lives in them ('ve', 'ile', 'bu', 'en') and a
    superlative marker on its own asserts nothing - 'en ekonomik' is caught on 'ekonomik'. Pure
    numerals are dropped because the numeric stage owns them and owns them better: it knows units.
    """
    out = []
    for token in tokens(text):
        if len(token) < min_length or token in function_lexicon:
            continue
        if re.fullmatch(r"[0-9]+(?:[.,/][0-9]+)*", token):
            continue
        out.append(token)
    return out


def prefix_agreement(left: str, right: str, minimum: int = 5) -> bool:
    """Do these two tokens share a root, judged by leading characters?

    Exact equality settles short tokens. Longer ones agree when their common prefix reaches
    `minimum`, which is what carries 'kalınlık'/'kalınlığı' across the k->ğ mutation that a
    suffix-stripping stemmer would have to encode as a special case.
    """
    if left == right:
        return True
    if len(left) < minimum or len(right) < minimum:
        return False
    shared = 0
    for a, b in zip(left, right):
        if a != b:
            break
        shared += 1
    return shared >= minimum


# ================================================================ 2. contracts and inputs

def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def load_source_registry(paths: Iterable[Path] = REGISTRY_PATHS) -> dict[str, dict]:
    """The union of every frozen registry, first writer wins.

    SEC-02-2 straddles two of them: the 360 kg/m³ claim's provenance was registered by the P0
    gap-resolution phase and is not in the base registry. A validator reading only the base file
    would report a true, frozen source key as unknown.
    """
    registry: dict[str, dict] = {}
    for path in paths:
        for row in _read_jsonl(path):
            registry.setdefault(row["source_key"], row)
    return registry


@dataclass
class DraftingBundle:
    contract: dict
    allowlist: dict[str, dict]
    denylist: dict[str, dict]
    registry: dict[str, dict]
    composition_contract: Any

    @property
    def function_lexicon(self) -> set[str]:
        return set(self.contract["function_lexicon"])

    @property
    def paraphrase_lexicon(self) -> dict[str, list[str]]:
        return self.contract["paraphrase_lexicon"]

    @property
    def translation_glosses(self) -> dict[str, list[str]]:
        return self.contract["translation_glosses"]

    @property
    def prohibited(self) -> dict[str, list[str]]:
        return self.contract["prohibited_markers"]

    @property
    def modality(self) -> dict[str, Any]:
        return self.contract["modality_lattice"]


def load_bundle(contract_path: Path = DRAFTING_CONTRACT_PATH,
                allowlist_path: Path = ALLOWLIST_PATH,
                denylist_path: Path = DENYLIST_PATH,
                registry_paths: Iterable[Path] = REGISTRY_PATHS) -> DraftingBundle:
    return DraftingBundle(
        contract=json.loads(contract_path.read_text(encoding="utf-8")),
        allowlist={row["claim_id"]: row for row in _read_jsonl(allowlist_path)},
        denylist={row["claim_id"]: row for row in _read_jsonl(denylist_path)},
        registry=load_source_registry(registry_paths),
        composition_contract=composition.load_contract())


# ================================================================ 3. DraftIR schema

class DraftSchemaError(ValueError):
    """The raw model output is not a DraftIR. There is no repair path; this is terminal."""


@dataclass
class DraftUnit:
    unit_id: str
    unit_type: str
    text: str
    material: bool
    claim_ids: list[str] = field(default_factory=list)
    source_keys: list[str] = field(default_factory=list)
    relationship_type: str = "NONE"
    qualifier_rule_ids: list[str] = field(default_factory=list)
    pair_constraint_ids: list[str] = field(default_factory=list)
    citation_intents: list[dict] = field(default_factory=list)
    numeric_values: list[dict] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    validation_status: str = "PENDING"

    @property
    def paragraph_id(self) -> str:
        match = re.match(r"^(U-[A-Za-z0-9]+-P\d{2})-S\d{2}$", self.unit_id)
        return match.group(1) if match else self.unit_id

    def citation_map(self) -> dict[str, list[str]]:
        mapping: dict[str, list[str]] = {}
        for intent in self.citation_intents:
            mapping.setdefault(intent["claim_id"], []).extend(intent.get("source_keys", []))
        return mapping


@dataclass
class DraftIR:
    section_id: str
    draft_id: str
    draft_version: str
    language: str
    title: str
    units: list[DraftUnit]

    def as_dict(self) -> dict:
        return {"section_id": self.section_id, "draft_id": self.draft_id,
                "draft_version": self.draft_version, "language": self.language,
                "title": self.title, "units": [asdict(u) for u in self.units]}


UNIT_ID_RE = re.compile(r"^U-[A-Za-z0-9]+-P\d{2}-S\d{2}$")


def parse_draft_ir(payload: Any, section_id: str = SECTION_ID) -> DraftIR:
    """Strict parse. Anything unexpected raises; nothing is defaulted into place.

    Silent defaulting is how a model that omitted `material` ends up with prose that was never
    support-checked, so a missing field is an error rather than a False.
    """
    if isinstance(payload, (str, bytes)):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as error:
            raise DraftSchemaError(f"output is not valid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise DraftSchemaError(f"DraftIR must be an object, got {type(payload).__name__}")

    for key in ("section_id", "draft_id", "draft_version", "language", "title", "units"):
        if key not in payload:
            raise DraftSchemaError(f"DraftIR is missing required field '{key}'")
    if payload["section_id"] != section_id:
        raise DraftSchemaError(
            f"DraftIR section_id is {payload['section_id']!r}, expected {section_id!r}")
    if not isinstance(payload["units"], list) or not payload["units"]:
        raise DraftSchemaError("DraftIR.units must be a non-empty list")

    units: list[DraftUnit] = []
    seen: set[str] = set()
    for index, raw in enumerate(payload["units"]):
        if not isinstance(raw, dict):
            raise DraftSchemaError(f"unit {index} is not an object")
        for key in ("unit_id", "unit_type", "text", "material", "claim_ids"):
            if key not in raw:
                raise DraftSchemaError(f"unit {index} is missing required field '{key}'")
        unit_id = raw["unit_id"]
        if not isinstance(unit_id, str) or not UNIT_ID_RE.match(unit_id):
            raise DraftSchemaError(
                f"unit {index} has unit_id {unit_id!r}; expected the form U-<sub>-P00-S00")
        if unit_id in seen:
            raise DraftSchemaError(f"duplicate unit_id {unit_id!r}")
        seen.add(unit_id)
        if raw["unit_type"] not in UNIT_TYPES:
            raise DraftSchemaError(f"{unit_id}: unit_type {raw['unit_type']!r} is not one of "
                                   f"{list(UNIT_TYPES)}")
        if not isinstance(raw["material"], bool):
            raise DraftSchemaError(f"{unit_id}: 'material' must be a boolean")
        if not isinstance(raw["text"], str) or not raw["text"].strip():
            raise DraftSchemaError(f"{unit_id}: 'text' must be a non-empty string")
        if not isinstance(raw["claim_ids"], list) or \
                any(not isinstance(c, str) for c in raw["claim_ids"]):
            raise DraftSchemaError(f"{unit_id}: 'claim_ids' must be a list of strings")
        relationship = raw.get("relationship_type", "NONE")
        if relationship in FORBIDDEN_RELATIONSHIPS:
            raise DraftSchemaError(
                f"{unit_id}: relationship_type {relationship!r} is forbidden by contract")
        if relationship not in ALLOWED_RELATIONSHIPS:
            raise DraftSchemaError(f"{unit_id}: relationship_type {relationship!r} is not one of "
                                   f"{list(ALLOWED_RELATIONSHIPS)}")
        intents = raw.get("citation_intents", [])
        if not isinstance(intents, list) or any(
                not isinstance(i, dict) or "claim_id" not in i for i in intents):
            raise DraftSchemaError(
                f"{unit_id}: 'citation_intents' must be a list of {{claim_id, source_keys}}")
        units.append(DraftUnit(
            unit_id=unit_id, unit_type=raw["unit_type"], text=raw["text"].strip(),
            material=raw["material"], claim_ids=list(raw["claim_ids"]),
            source_keys=list(raw.get("source_keys", [])), relationship_type=relationship,
            qualifier_rule_ids=list(raw.get("qualifier_rule_ids", [])),
            pair_constraint_ids=list(raw.get("pair_constraint_ids", [])),
            citation_intents=[dict(i) for i in intents],
            numeric_values=list(raw.get("numeric_values", [])),
            conditions=list(raw.get("conditions", []))))
    return DraftIR(section_id=payload["section_id"], draft_id=payload["draft_id"],
                   draft_version=payload["draft_version"], language=payload["language"],
                   title=payload["title"], units=units)


# ================================================================ 4. licensing pools

def claim_text_pool(claim: dict, bundle: DraftingBundle) -> list[str]:
    """Everything the drafter is licensed to say about one claim, as raw strings."""
    scope = claim.get("scope") or {}
    pieces = [claim.get("canonical_claim") or ""]
    pieces += list(claim.get("conditions") or [])
    pieces += list(claim.get("qualifiers") or [])
    pieces += [scope.get("scope_evidence") or "", scope.get("document_scope") or "",
               claim.get("topic") or ""]
    return [p for p in pieces if p]


def licensed_tokens(claim_ids: Iterable[str], bundle: DraftingBundle) -> set[str]:
    """The token pool a unit's declared claims license.

    Deliberately NOT pooled across the section: a unit may only borrow the vocabulary of the
    claims it actually declares. Pooling section-wide would let a sentence about layer thickness
    quietly acquire the words of a cement-dosage claim it never cited, which is the whole point of
    claim-bound drafting undone by a convenience.
    """
    pool: set[str] = set()
    for claim_id in claim_ids:
        claim = bundle.allowlist.get(claim_id)
        if claim is None:
            continue
        for piece in claim_text_pool(claim, bundle):
            pool.update(tokens(piece))
        pool.update(fold(t) for t in bundle.translation_glosses.get(claim_id, []))
    for token in list(pool):
        pool.update(fold(t) for t in bundle.paraphrase_lexicon.get(token, []))
    return pool


def unlicensed(text: str, pool: set[str], bundle: DraftingBundle) -> list[str]:
    unlicensed_tokens = []
    for token in content_tokens(text, bundle.function_lexicon):
        if not any(prefix_agreement(token, licensed) for licensed in pool):
            unlicensed_tokens.append(token)
    return sorted(dict.fromkeys(unlicensed_tokens))


# ================================================================ 5. numeric handling

REFERENCE_MASKS = (
    r"[Tt]ablo\s?-?\s?\d+(?:-\d+)*-?[A-Za-z]?",
    r"§?\s?\d+(?:\.\d+){2,4}",
    r"[Tt][Ss]\s?\d+",
    r"C\s?\d{2}\s?/\s?\d{2}",
)

# Ranges are written four ways in this corpus - '3-5', '100-150', '4 to 16', '4 ila 16' - and a
# pattern that reads only the hyphen form silently ignores half of them. Turkish suffixes attach
# directly to the unit ('saattir', "mm'dir"), so the unit may not be closed with \b either; it is
# closed against a following digit instead, which is what actually distinguishes '15 cm' from a
# longer number.
RANGE_SEPARATOR = r"(?:\s?[-–]\s?|\s+(?:to|ila|ile|–)\s+)"
NUMERIC_RE = re.compile(
    rf"(?<![\d,.])(\d+(?:[.,]\d+)?(?:{RANGE_SEPARATOR}\d+(?:[.,]\d+)?)?)\s*"
    r"(kg/m\s?3|mpa|mm|cm|°c|gün|saat|adet|inches|inch|inç|m)(?![0-9])")

# Two spellings of one unit. The Turkish rendering of an English claim writes 'inç' where the
# source wrote 'inches'; treating those as different units would report unit drift on a faithful
# translation, which is the opposite of what the unit check is for.
UNIT_EQUIVALENCE = {"inç": "inches", "inch": "inches"}


def _normalise_value(value: str) -> str:
    value = value.replace(",", ".").strip()
    if re.fullmatch(r"\d+\.0+", value):
        value = value.split(".")[0]
    return value


def mask_references(text: str) -> str:
    """Table numbers, clause numbers, standard numbers and strength classes are not measurements.

    'Tablo-351-5' holds a 5 and a 351; 'C25/30' holds a 25 and a 30. Reading either as a quantity
    manufactures numeric drift out of a correct citation, and - worse for §107 - normalising
    C25/30 into an MPa value is precisely the error the contract forbids the drafter from making.
    """
    for pattern in REFERENCE_MASKS:
        text = re.sub(pattern, " ", text)
    return text


def extract_numerics(text: str) -> list[tuple[str, str]]:
    """Every quantity the prose asserts, ranges expanded into their endpoints.

    A range is reported as the range AND as each endpoint, because both are things the sentence
    claims: writing '3-6 saat' against a source that says '3-5 saat' drifts on the endpoint, not
    on the range string, and matching only the whole string would miss it.
    """
    folded = fold(mask_references(text))
    found: list[tuple[str, str]] = []
    for match in NUMERIC_RE.finditer(folded):
        raw = re.sub(RANGE_SEPARATOR, "-", match.group(1)).replace(",", ".")
        unit = re.sub(r"\s+", "", match.group(2))
        unit = "kg/m3" if unit.startswith("kg/m") else UNIT_EQUIVALENCE.get(unit, unit)
        found.append((_normalise_value(raw), unit))
        if "-" in raw:
            for part in raw.split("-"):
                if part.strip():
                    found.append((_normalise_value(part.strip()), unit))
    return list(dict.fromkeys(found))


def licensed_numerics(claim_ids: Iterable[str], bundle: DraftingBundle) -> set[tuple[str, str]]:
    """Value/unit pairs the declared claims state, plus those readable off their own wording.

    Both sources are needed. The structured `numeric` field misses figures the extractor recorded
    as unitless reference fragments - SEC-02-2-P0-007's '100 to 400 mm' arrives with unit None -
    while the canonical text carries them correctly. Neither alone covers the claim set.
    """
    allowed: set[tuple[str, str]] = set()
    for claim_id in claim_ids:
        claim = bundle.allowlist.get(claim_id)
        if claim is None:
            continue
        for entry in claim.get("numeric") or []:
            value, unit = entry.get("value"), entry.get("unit")
            if value is None:
                continue
            value = _normalise_value(str(value))
            if unit:
                symbol = fold(unit).replace("³", "3")
                symbol = UNIT_EQUIVALENCE.get(symbol, symbol)
                allowed.add((value, symbol))
                for part in re.split(r"[-–x]", value):
                    if part.strip():
                        allowed.add((_normalise_value(part.strip()), symbol))
        for piece in claim_text_pool(claim, bundle):
            allowed.update(extract_numerics(piece))
    return allowed


# ================================================================ 6. modality

def modality_level(text: str, bundle: DraftingBundle) -> tuple[int, str | None]:
    """Highest normative force asserted anywhere in the text, with the marker that carried it.

    Turkish carries obligation in a suffix as often as in a word: 'azaltılmalıdır' is a
    recommendation and 'azaltılabilmektedir' is a permission, and the two differ by four letters
    in the middle of a verb. Word-initial matching alone cannot see that, so the lattice carries
    a second set of markers matched as suffixes.
    """
    folded = fold(text)
    best, marker = -1, None
    for level, markers in sorted(bundle.modality["markers"].items(), key=lambda kv: int(kv[0])):
        for candidate in markers:
            if re.search(rf"(?<![a-zçğıöşü]){re.escape(fold(candidate))}", folded):
                if int(level) > best:
                    best, marker = int(level), candidate
    for level, markers in sorted(bundle.modality.get("suffix_markers", {}).items(),
                                 key=lambda kv: int(kv[0])):
        for candidate in markers:
            if re.search(rf"[a-zçğıöşü]{re.escape(fold(candidate))}(?![a-zçğıöşü])", folded):
                if int(level) > best:
                    best, marker = int(level), f"-{candidate}"
    return best, marker


# ================================================================ 7. the stages

@dataclass
class UnitFailure:
    code: str
    unit_id: str
    detail: str
    required_action: str
    stage: str
    claim_ids: list[str] = field(default_factory=list)
    rule_id: str | None = None
    evidence: str | None = None


def _fail(code: str, unit: DraftUnit, detail: str, action: str, stage: str,
          claim_ids: list[str] | None = None, rule_id: str | None = None,
          evidence: str | None = None) -> UnitFailure:
    return UnitFailure(code=code, unit_id=unit.unit_id, detail=detail, required_action=action,
                       stage=stage, claim_ids=claim_ids or [], rule_id=rule_id, evidence=evidence)


def stage_a_allowlist(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    failures = []
    for claim_id in unit.claim_ids:
        if claim_id in bundle.denylist:
            continue                        # stage B owns this, and reports it more precisely
        if claim_id not in bundle.allowlist:
            failures.append(_fail(
                "CLAIM_NOT_ALLOWLISTED", unit,
                f"{claim_id} is not on the SEC-02-2 composition-safe allowlist",
                f"remove {claim_id}; only the 27 allowlisted claims may be drafted",
                "A_allowlist", [claim_id]))
        elif not bundle.allowlist[claim_id].get("composition_safe"):
            failures.append(_fail(
                "CLAIM_NOT_ALLOWLISTED", unit,
                f"{claim_id} is allowlisted for evidence but is not composition-safe",
                f"remove {claim_id} or draft its narrowed replacement",
                "A_allowlist", [claim_id]))
    return failures


def stage_b_denylist(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    failures = []
    for claim_id in unit.claim_ids:
        denied = bundle.denylist.get(claim_id)
        if denied is None:
            continue
        failures.append(_fail(
            "CLAIM_DENYLISTED", unit,
            f"{claim_id} is on the composition denylist "
            f"({denied.get('support_status')}; {sorted(denied.get('deny_reasons', []))})",
            f"remove {claim_id}; it is not draftable in any wording",
            "B_denylist", [claim_id]))
    return failures


def _marker_present(marker: str, folded_text: str) -> bool:
    """Match a marker as a word, allowing Turkish suffixes only on markers long enough to bear one.

    'ekonomik' should match 'ekonomiktir'; 'zor' must not match 'olmak zorundadır', which is a
    modality, not an evaluation. Five characters is the line: below it a marker is too short for
    a suffix allowance to be anything but a substring collision.
    """
    folded_marker = fold(marker)
    tail = "" if len(folded_marker) >= 5 else r"(?![a-zçğıöşü])"
    return bool(re.search(rf"(?<![a-zçğıöşü]){re.escape(folded_marker)}{tail}", folded_text))


def _licensed_marker(marker: str, pool: set[str], bundle: DraftingBundle) -> bool:
    """Is every content word of this marker already licensed by the declared claims?"""
    parts = content_tokens(marker, bundle.function_lexicon)
    if not parts:
        return False
    return all(any(prefix_agreement(part, licensed) for licensed in pool) for part in parts)


def stage_c_support(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    """Containment: does the sentence say anything its declared claims do not license?"""
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    folded = fold(unit.text)
    pool = licensed_tokens(unit.claim_ids, bundle)

    for family in ("expansion", "causal", "universal"):
        for marker in bundle.prohibited.get(family, []):
            if not _marker_present(marker, folded):
                continue
            # A marker the declared claims themselves use is not an addition. Two allowlisted
            # claims genuinely say "yeterli" (C-006, of a layer's load-bearing strength) and
            # "durabilite nedeniyle" (P0-005) - a flat prohibition would reject the source's own
            # wording, which is the failure mode this module is built to avoid.
            if _licensed_marker(marker, pool, bundle):
                continue
            if family == "causal" and unit.relationship_type == "SOURCE_SUPPORTED_RELATION":
                # A causal connective is licensed only when a source states the relation, and the
                # composition validator - not this stage - decides whether it actually does.
                continue
            code = "CLAIM_EXPANSION" if family == "expansion" else "UNSUPPORTED_PROPOSITION"
            failures.append(_fail(
                code, unit,
                f"the unit asserts a {family} proposition via \"{marker}\", which appears in no "
                f"claim it declares",
                "state only what the declared claims state; drop the added proposition",
                "C_support", list(unit.claim_ids), evidence=marker))

    if not pool and unit.claim_ids:
        return failures
    stray = unlicensed(unit.text, pool, bundle)
    if stray:
        failures.append(_fail(
            "UNSUPPORTED_PROPOSITION", unit,
            f"content words {stray} are licensed by none of the declared claims "
            f"{sorted(unit.claim_ids)}",
            "either cite a claim that supports these words or remove them",
            "C_support", list(unit.claim_ids), evidence=", ".join(stray)))
    return failures


def stage_d_numeric(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    allowed = licensed_numerics(unit.claim_ids, bundle)
    allowed_values = {value for value, _ in allowed}
    for value, unit_symbol in extract_numerics(unit.text):
        value = _normalise_value(value)
        if (value, unit_symbol) in allowed:
            continue
        if value in allowed_values:
            others = sorted({u for v, u in allowed if v == value})
            failures.append(_fail(
                "UNIT_DRIFT", unit,
                f"{value} is stated by a declared claim in {others}, not in {unit_symbol!r}",
                "render the figure in the unit its source uses",
                "D_numeric", list(unit.claim_ids), evidence=f"{value} {unit_symbol}"))
        else:
            failures.append(_fail(
                "NUMERIC_DRIFT", unit,
                f"the figure {value} {unit_symbol} is stated by none of the declared claims "
                f"{sorted(unit.claim_ids)}",
                "remove the figure or cite the claim that states it",
                "D_numeric", list(unit.claim_ids), evidence=f"{value} {unit_symbol}"))
    return failures


def stage_e_conditions(unit: DraftUnit, paragraph_text: str,
                       bundle: DraftingBundle) -> list[UnitFailure]:
    """Conditions and qualifiers must survive; modality must not gain force.

    A condition is checked in the sentence when the claim's own canonical wording carries it, and
    in the paragraph when it does not. That distinction is not a softening - it is what keeps the
    rule honest. SEC-02-2-P0-001's condition 'özel uygulamalar dışında' is real and comes from the
    surrounding clause, so demanding it inside a faithful paraphrase of the claim's own sentence
    would reject the source.
    """
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    for claim_id in unit.claim_ids:
        claim = bundle.allowlist.get(claim_id)
        if claim is None:
            continue
        canonical = claim.get("canonical_claim") or ""
        canonical_tokens = set(tokens(canonical))
        glosses = bundle.contract.get("condition_glosses", {}).get(claim_id, {})
        for condition in claim.get("conditions") or []:
            anchors = list(content_tokens(condition, bundle.function_lexicon))
            # An English claim rendered in Turkish cannot retain an English anchor. The Turkish
            # equivalents are declared in the contract rather than inferred, so a gloss is
            # auditable and cannot quietly widen what the condition means.
            gloss = [fold(t) for t in glosses.get(condition, [])]
            if gloss:
                anchors = anchors + gloss
            if not anchors:
                continue
            # ALL anchors, not any. 'özel uygulamalar dışında' shares 'uygulamalar' with
            # SEC-02-2-P0-006's own 'standart uygulamalarda' while meaning the opposite; an
            # any-match would classify a neighbouring-clause condition as sentence-internal and
            # then reject every faithful paraphrase of the claim for omitting it.
            in_canonical = all(any(prefix_agreement(a, c) for c in canonical_tokens)
                               for a in content_tokens(condition, bundle.function_lexicon))
            haystack = unit.text if in_canonical else paragraph_text
            scope = "unit" if in_canonical else "paragraph"
            present = set(tokens(haystack))
            if any(any(prefix_agreement(a, h) for h in present) for a in anchors):
                continue
            failures.append(_fail(
                "CONDITION_DROPPED", unit,
                f"{claim_id} holds only under \"{condition}\", and no anchor for it "
                f"({anchors}) survives into the {scope}",
                f"state the condition \"{condition}\" alongside the claim, or drop the claim",
                "E_conditions", [claim_id], evidence=condition))

        for qualifier in claim.get("qualifiers") or []:
            anchors = content_tokens(qualifier, bundle.function_lexicon)
            if not anchors:
                continue
            present = set(tokens(paragraph_text))
            hits = sum(1 for a in anchors if any(prefix_agreement(a, h) for h in present))
            if hits * 2 >= len(anchors):
                continue
            failures.append(_fail(
                "QUALIFIER_DROPPED", unit,
                f"{claim_id} carries the qualifier \"{qualifier}\"; only {hits} of "
                f"{len(anchors)} of its anchors survive into the paragraph",
                f"carry the qualifier \"{qualifier}\" into the prose, or drop the claim",
                "E_conditions", [claim_id], evidence=qualifier))

    # Modality is compared against the strongest force any declared claim carries, not against
    # each claim in turn. A sentence resting on a binding minimum and a descriptive typical value
    # legitimately reads as binding; scoring it against the descriptive claim alone would reject
    # a faithful rendering of the binding one.
    licensed_level = -1
    strongest: str | None = None
    for claim_id in unit.claim_ids:
        claim = bundle.allowlist.get(claim_id)
        if claim is None:
            continue
        level, _ = modality_level(claim.get("canonical_claim") or "", bundle)
        if level > licensed_level:
            licensed_level, strongest = level, claim_id
    draft_level, draft_marker = modality_level(unit.text, bundle)
    if unit.claim_ids and draft_level > licensed_level:
        failures.append(_fail(
            "MODALITY_DRIFT", unit,
            f"the unit asserts modality level {draft_level} (\"{draft_marker}\") while the "
            f"strongest force its claims state is level {licensed_level}"
            + (f" ({strongest})" if strongest else ""),
            "preserve the source's normative force; do not strengthen it",
            "E_conditions", list(unit.claim_ids), evidence=draft_marker))
    return failures


def stage_f_composition(unit: DraftUnit, paragraph_text: str,
                        bundle: DraftingBundle) -> list[UnitFailure]:
    """Delegate, never re-implement.

    The composition validator is frozen and its 71-case regression is the evidence that it works.
    Re-encoding its rules here would create a second, unversioned copy that can drift out of
    agreement with the one the previous phase actually tested.
    """
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    texts = [unit.text] if unit.text.strip() == paragraph_text.strip() else \
        [unit.text, paragraph_text]
    seen: set[tuple[str, str]] = set()
    for text in texts:
        result = composition.validate(unit.claim_ids, [text], unit.citation_map(),
                                      bundle.composition_contract)
        for failure in result.failures:
            code = COMPOSITION_CODE_MAP.get(failure["code"], failure["code"])
            key = (code, failure["detail"])
            if key in seen:
                continue
            seen.add(key)
            failures.append(_fail(
                code, unit, failure["detail"], failure["required_action"], "F_composition",
                list(failure["claim_ids"]), rule_id=failure.get("rule_id"),
                evidence=failure.get("sentence")))
    return failures


def stage_g_sources(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    failures: list[UnitFailure] = []
    if not unit.material:
        if unit.source_keys or unit.claim_ids:
            failures.append(_fail(
                "NON_MATERIAL_MISCLASSIFIED", unit,
                "a non-material unit declares claims or source keys; if it asserts something it "
                "must be marked material",
                "mark the unit material, or remove its claim and citation bindings",
                "G_sources", list(unit.claim_ids)))
        return failures
    declared = unit.citation_map()
    for claim_id in unit.claim_ids:
        keys = declared.get(claim_id) or []
        if not keys:
            failures.append(_fail(
                "MISSING_SOURCE_KEY", unit,
                f"the unit declares {claim_id} but binds no source key to it",
                f"bind {claim_id} to one of its registered source keys",
                "G_sources", [claim_id]))
            continue
        registered = set((bundle.allowlist.get(claim_id) or {}).get("source_keys") or [])
        for key in keys:
            if key not in bundle.registry:
                failures.append(_fail(
                    "UNKNOWN_SOURCE_KEY", unit,
                    f"{key} resolves against no frozen source registry",
                    "cite only source keys present in the frozen registries",
                    "G_sources", [claim_id], evidence=key))
            elif key not in registered:
                failures.append(_fail(
                    "CITATION_SCOPE_MISMATCH", unit,
                    f"{key} is a registered source but is not one of {claim_id}'s own keys "
                    f"{sorted(registered)}",
                    f"cite {claim_id} against its own provenance",
                    "G_sources", [claim_id], evidence=key))
    stray = set(unit.source_keys) - {k for keys in declared.values() for k in keys}
    for key in sorted(stray):
        failures.append(_fail(
            "CITATION_SCOPE_MISMATCH", unit,
            f"{key} is listed on the unit but is bound to no declared claim",
            "bind every cited source key to the claim it supports",
            "G_sources", list(unit.claim_ids), evidence=key))
    return failures


def stage_h_citation(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    if not unit.claim_ids:
        failures.append(_fail(
            "MISSING_CITATION", unit,
            "a material unit declares no claim; every material sentence must be claim-bound",
            "declare the claim ids the sentence rests on, or mark the unit non-material",
            "H_citation"))
        return failures
    if not {k for keys in unit.citation_map().values() for k in keys}:
        failures.append(_fail(
            "MISSING_CITATION", unit,
            "a material unit carries no resolvable citation",
            "cite at least one registered source key",
            "H_citation", list(unit.claim_ids)))
    return failures


def stage_i_rendering(unit: DraftUnit, bundle: DraftingBundle) -> list[UnitFailure]:
    """Internal machinery must be invisible. The check runs on visible prose only."""
    failures: list[UnitFailure] = []
    leak = PACKET_EID_RE.search(unit.text)
    if leak:
        failures.append(_fail(
            "PACKET_EID_LEAK", unit,
            f"visible prose contains the packet-local evidence handle {leak.group(0)!r}; these "
            f"are retrieval-packet addresses and are not stable book references",
            "remove the handle; citations are rendered from source keys",
            "I_rendering", list(unit.claim_ids), evidence=leak.group(0)))
    for pattern, label in ((CLAIM_ID_RE, "claim id"), (SOURCE_KEY_RE, "source key")):
        found = pattern.search(unit.text)
        if found:
            failures.append(_fail(
                "INTERNAL_ID_LEAK", unit,
                f"visible prose contains an internal {label} {found.group(0)!r}",
                "keep internal identifiers in machine metadata, never in book prose",
                "I_rendering", list(unit.claim_ids), evidence=found.group(0)))
    for marker in bundle.contract["forbidden_prose_markers"]:
        if re.search(rf"(?<![a-zçğıöşü]){re.escape(fold(marker))}", fold(unit.text)):
            failures.append(_fail(
                "INTERNAL_ID_LEAK", unit,
                f"visible prose exposes pipeline machinery via \"{marker}\"",
                "write as a textbook; the evidence pipeline must be invisible to the reader",
                "I_rendering", list(unit.claim_ids), evidence=marker))
    return failures


STAGES = ("A_allowlist", "B_denylist", "C_support", "D_numeric", "E_conditions",
          "F_composition", "G_sources", "H_citation", "I_rendering")


# ================================================================ 8. driver

@dataclass
class UnitResult:
    unit_id: str
    status: str
    material: bool
    claim_ids: list[str]
    failure_codes: list[str]
    failures: list[dict]


@dataclass
class DraftValidationResult:
    status: str
    units: list[UnitResult]
    failure_codes: list[str]
    failure_histogram: dict[str, int]
    rejected_unit_ids: list[str]
    validator_version: str = VALIDATOR_VERSION
    contract_version: str = DRAFTING_CONTRACT_VERSION
    section_id: str = SECTION_ID

    def as_dict(self) -> dict:
        return asdict(self)


def paragraph_texts(ir: DraftIR) -> dict[str, str]:
    grouped: dict[str, list[str]] = {}
    for unit in ir.units:
        if unit.material or unit.unit_type in ("PARAGRAPH_SENTENCE", "LIST_ITEM", "TRANSITION"):
            grouped.setdefault(unit.paragraph_id, []).append(unit.text)
    return {pid: " ".join(parts) for pid, parts in grouped.items()}


def validate_unit(unit: DraftUnit, paragraph_text: str,
                  bundle: DraftingBundle) -> list[UnitFailure]:
    failures: list[UnitFailure] = []
    failures += stage_a_allowlist(unit, bundle)
    failures += stage_b_denylist(unit, bundle)
    # A unit resting on an inadmissible claim is already rejected; running support containment
    # against a claim that does not exist would only add noise about a sentence nobody may write.
    admissible = not any(f.code in ("CLAIM_NOT_ALLOWLISTED", "CLAIM_DENYLISTED")
                         for f in failures)
    if admissible:
        failures += stage_c_support(unit, bundle)
        failures += stage_d_numeric(unit, bundle)
        failures += stage_e_conditions(unit, paragraph_text, bundle)
        failures += stage_f_composition(unit, paragraph_text, bundle)
    failures += stage_g_sources(unit, bundle)
    failures += stage_h_citation(unit, bundle)
    failures += stage_i_rendering(unit, bundle)
    return sorted(failures, key=lambda f: REJECTION_CODES.index(f.code))


def validate_draft(ir: DraftIR, bundle: DraftingBundle | None = None) -> DraftValidationResult:
    """All-or-nothing, per §84: one rejected material unit rejects the pilot."""
    bundle = bundle or load_bundle()
    paragraphs = paragraph_texts(ir)
    results: list[UnitResult] = []
    histogram: dict[str, int] = {}
    for unit in ir.units:
        failures = validate_unit(unit, paragraphs.get(unit.paragraph_id, unit.text), bundle)
        for failure in failures:
            histogram[failure.code] = histogram.get(failure.code, 0) + 1
        unit.validation_status = "REJECT" if failures else "ACCEPT"
        results.append(UnitResult(
            unit_id=unit.unit_id, status=unit.validation_status, material=unit.material,
            claim_ids=list(unit.claim_ids),
            failure_codes=sorted({f.code for f in failures}, key=REJECTION_CODES.index),
            failures=[asdict(f) for f in failures]))
    rejected = [r.unit_id for r in results if r.status == "REJECT"]
    return DraftValidationResult(
        status="ACCEPT" if not rejected else "REJECT", units=results,
        failure_codes=sorted(histogram, key=REJECTION_CODES.index),
        failure_histogram=dict(sorted(histogram.items())), rejected_unit_ids=rejected)


# ================================================================ 9. fixture harness

def run_fixtures(fixtures: list[dict], bundle: DraftingBundle | None = None) -> dict[str, Any]:
    """A false accept is a case the contract says must fail that passed. It must be zero."""
    bundle = bundle or load_bundle()
    rows, false_accepts, false_rejects, mismatches = [], [], [], []
    for fixture in fixtures:
        unit = DraftUnit(
            unit_id=fixture.get("unit_id", "U-X-P01-S01"),
            unit_type=fixture.get("unit_type", "PARAGRAPH_SENTENCE"),
            text=fixture["text"], material=fixture.get("material", True),
            claim_ids=list(fixture.get("claim_ids", [])),
            source_keys=list(fixture.get("source_keys", [])),
            relationship_type=fixture.get("relationship_type", "INDEPENDENT"),
            citation_intents=list(fixture.get("citation_intents", [])))
        paragraph = fixture.get("paragraph_text") or unit.text
        failures = validate_unit(unit, paragraph, bundle)
        actual_codes = sorted({f.code for f in failures}, key=REJECTION_CODES.index)
        expected_valid = fixture["expected_valid"]
        row = {"case_id": fixture["case_id"], "expected_valid": expected_valid,
               "actual_valid": not failures,
               "expected_failure_codes": sorted(fixture.get("expected_failure_codes", [])),
               "actual_failure_codes": actual_codes,
               "polarity": "positive" if expected_valid else "negative",
               "detail": [f.detail for f in failures]}
        if expected_valid and failures:
            false_rejects.append(fixture["case_id"])
            row["outcome"] = "FALSE_REJECT"
        elif not expected_valid and not failures:
            false_accepts.append(fixture["case_id"])
            row["outcome"] = "FALSE_ACCEPT"
        else:
            expected_codes = set(fixture.get("expected_failure_codes", []))
            if expected_codes and not expected_codes <= set(actual_codes):
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
    print(f"{VALIDATOR_VERSION}\nThis module is a library. Run "
          f"scripts/47_section_drafting_contract_v1.py to author the contracts, score the "
          f"fixtures and run the controlled pilot.")
