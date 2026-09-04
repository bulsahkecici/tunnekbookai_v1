"""SEC-02-2 Claim Composition Validator v1.

Evidence correctness is not composition correctness. Every claim on SEC-02-2's allowlist is
individually supported, traceable and numerically safe - and a drafter holding all 27 of them can
still produce a proposition no source states, simply by putting two of them in one sentence. That
is not a hypothetical: it is what SYN-001 was. Both of its components were well-supported; the
defect was the connective between them.

So this validator does not check whether claims are true. It checks whether a candidate draft
unit *uses* them in a way the sources license:

  - a claim whose figure is meaningless without its scope must carry that scope (CF-P0-001);
  - two claims governing different materials must not be joined into one assertion (SYN-001);
  - a converted number must not be attributed to a source that never stated it (150 mm);
  - and nothing may cite a claim that is denylisted, superseded, partial or unknown.

Three design commitments, all of them deliberate:

**Deterministic, no LLM judge.** Every decision is a regex, a set membership or a sentence-window
comparison. The same input always produces the same failure codes.

**Fail closed.** There is no auto-repair, no qualifier injection, no rewriting. An invalid unit is
rejected and the required action is reported. A unit whose scope cannot be determined fails as
AMBIGUOUS_SCOPE rather than passing on the benefit of the doubt.

**Scoped to SEC-02-2.** This is not general natural-language inference. It knows about six figures
in two materials, and it says so. Widening it is a later phase's decision, not a side effect of
this one.

Two traps that shaped the implementation, both found by reading the artifacts rather than by
reasoning about them in the abstract:

  1. The mandatory qualifier that CF-P0-001 requires *contains the wrong-scope phrase*: it reads
     "...GENEL beton özelliklerine ilişkindir; püskürtme beton şartnamesi değildir". A naive
     wrong-scope detector would reject the exact form the contract mandates. So shotcrete
     mentions are checked for negation before being treated as a governing scope.

  2. SEC-02-2-C-009 states "100-150 mm" for clay-zone layers, and that 150 mm *is* source-stated.
     The derived-number guard therefore keys on the single-pass thickness context, not on the
     string "150 mm" wherever it appears.

Numeric detection is unit-scoped throughout. Matching on bare values would make the "400" in
"4 to 16 inches (100 to 400 mm)" collide with the 400 kg/m3 wet-system minimum - a different
quantity in a different material - which is precisely the class of error the previous phase found
in its own numeric backfill.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_VERSION = "tunnelbook-sec-02-2-claim-composition-validator-v1"
CONTRACT_VERSION = "tunnelbook-sec-02-2-claim-composition-contract-v1"
SECTION_ID = "SEC-02-2"

RESOLUTION = ROOT / "data" / "book" / "sec_02_2_limitation_resolution"
CONTRACTS = RESOLUTION / "contracts"
CLAIMS = RESOLUTION / "claims"

CONTRACT_PATH = CONTRACTS / "sec_02_2_claim_composition_contract_v1.json"
ALLOWLIST_PATH = CLAIMS / "composition_safe_allowlist_v1.jsonl"
DENYLIST_PATH = CLAIMS / "composition_denylist_v1.jsonl"
PAIRS_PATH = CLAIMS / "claim_pair_constraints_v1.jsonl"

FAILURE_CODES = (
    "UNQUALIFIED_SCOPE",
    "FORBIDDEN_SYNTHESIS",
    "UNSUPPORTED_RELATION",
    "DERIVED_VALUE_AS_SOURCE_STATED",
    "CLAIM_NOT_ALLOWLISTED",
    "CLAIM_SUPERSEDED",
    "CLAIM_PARTIAL",
    "CLAIM_UNSUPPORTED",
    "MISSING_SOURCE_KEY",
    "AMBIGUOUS_SCOPE",
)

RELATIONSHIP_TYPES = (
    "INDEPENDENT",
    "SAME_SCOPE_SUPPORT",
    "QUALIFIED_COMPARISON",
    "SOURCE_SUPPORTED_RELATION",
    "FORBIDDEN_SYNTHESIS",
    "UNKNOWN_RELATION",
)


# ================================================================ 1. text normalisation

def fold(text: str) -> str:
    """Case- and spacing-insensitive form used for every match in this module.

    'kg/m³', 'kg/m3', 'kg / m 3' and 'kg/m^3' all fold together; nothing else is repaired. OCR
    variants are NOT normalised away - a draft unit is a thing someone wrote, not a scanned page.
    """
    folded = unicodedata.normalize("NFKC", text).lower()
    folded = folded.replace("³", "3").replace("^3", "3").replace("²", "2")
    folded = re.sub(r"\s*/\s*", "/", folded)
    folded = re.sub(r"\s+", " ", folded)
    return folded.strip()


def sentences(text: str) -> list[str]:
    """Split a draft unit into sentences.

    A semicolon is NOT a boundary. That is a fail-closed choice with a reason: 'X is 360; Y is
    400' is one sentence that invites the reader to compare, and the whole point of the
    same-sentence prohibition is to stop exactly that juxtaposition. Treating ';' as a split
    would let the forbidden construction through on punctuation.

    List items ARE boundaries, because the contract permits restricted claims to coexist in one
    paragraph as separate list items.
    """
    masked = text
    placeholders: dict[str, str] = {}

    def mask(match: re.Match) -> str:
        token = f"\x00{len(placeholders)}\x00"
        placeholders[token] = match.group(0)
        return token

    masked = re.sub(r"\d+(?:[.,]\d+)+", mask, masked)
    masked = re.sub(r"§?\s?\d+(?:\.\d+){1,4}", mask, masked)
    masked = re.sub(r"[Tt]ablo-\d+(?:-\d+)*-?[A-Za-z]?", mask, masked)
    masked = re.sub(r"[Tt][Ss]\s?\d+", mask, masked)

    parts: list[str] = []
    for line in masked.replace("\r", "").split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        # A leading bullet or enumerator starts a new unit.
        stripped = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", stripped)
        for piece in re.split(r"(?<=[.!?])\s+", stripped):
            if piece.strip():
                parts.append(piece.strip())
    restored = []
    for part in parts:
        for token, original in placeholders.items():
            part = part.replace(token, original)
        restored.append(part)
    return restored


# ================================================================ 2. contract loading

def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


@dataclass
class CompositionContract:
    contract: dict
    allowlist: dict[str, dict]
    denylist: dict[str, dict]
    pairs: dict[tuple[str, str], dict]

    @property
    def scopes(self) -> dict[str, dict]:
        return {row["claim_id"]: row for row in self.contract["claim_scopes"]}

    @property
    def qualifier_rules(self) -> list[dict]:
        return self.contract["mandatory_qualifier_rules"]

    @property
    def synthesis_rules(self) -> list[dict]:
        return self.contract["forbidden_synthesis_rules"]

    @property
    def derived_rules(self) -> list[dict]:
        return self.contract["derived_numeric_rules"]

    @property
    def markers(self) -> dict[str, list[str]]:
        return self.contract["scope_markers"]

    @property
    def negations(self) -> list[str]:
        return self.contract["negation_markers"]

    @property
    def connectors(self) -> dict[str, list[str]]:
        return self.contract["relation_connectors"]

    def pair(self, left: str, right: str) -> dict | None:
        return self.pairs.get((left, right)) or self.pairs.get((right, left))


def load_contract(
        contract_path: Path = CONTRACT_PATH,
        allowlist_path: Path = ALLOWLIST_PATH,
        denylist_path: Path = DENYLIST_PATH,
        pairs_path: Path = PAIRS_PATH) -> CompositionContract:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    allowlist = {row["claim_id"]: row for row in _read_jsonl(allowlist_path)}
    denylist = {row["claim_id"]: row for row in _read_jsonl(denylist_path)}
    pairs = {(row["left_claim_id"], row["right_claim_id"]): row
             for row in _read_jsonl(pairs_path)}
    return CompositionContract(contract, allowlist, denylist, pairs)


# ================================================================ 3. figure detection

def figure_pattern(value: str, unit: str) -> re.Pattern:
    """Unit-scoped, digit-bounded.

    The digit boundary stops '150 mm' from matching inside '2150 mm'. The unit requirement stops
    '400 kg/m3' from matching the '400 mm' in an inch-to-millimetre thickness range - two
    different quantities in two different materials that happen to share a numeral.
    """
    number = re.escape(fold(value)).replace(r"\-", "-")
    unit_folded = fold(unit)
    if unit_folded == "kg/m3":
        unit_re = r"kg/m\s?3"
    elif unit_folded == "mpa":
        unit_re = r"mpa"
    else:
        unit_re = re.escape(unit_folded)
    return re.compile(rf"(?<![\d,.]){number}\s*{unit_re}")


def find_figures(text: str, contract: CompositionContract) -> dict[str, list[str]]:
    """Which restricted figures does this text mention, and in which sentences?

    Returns figure_id -> list of sentences carrying it.
    """
    hits: dict[str, list[str]] = {}
    units = sentences(text)
    for figure in contract.contract["restricted_figures"]:
        pattern = figure_pattern(figure["value"], figure["unit"])
        carrying = [unit for unit in units if pattern.search(fold(unit))]
        if carrying:
            hits[figure["figure_id"]] = carrying
    return hits


def scope_in_sentence(sentence: str, scope: str, contract: CompositionContract) -> bool:
    """Is this scope asserted - not merely mentioned - in this sentence?

    Negated mentions do not count. This is what lets the mandatory CF-P0-001 qualifier, whose own
    text ends '...püskürtme beton şartnamesi değildir', avoid being read as a shotcrete claim.
    """
    folded = fold(sentence)
    for marker in contract.markers.get(scope, []):
        marker_folded = fold(marker)
        for match in re.finditer(re.escape(marker_folded), folded):
            tail = folded[match.end():match.end() + 60]
            if any(fold(negation) in tail for negation in contract.negations):
                continue
            return True
    return False


# ================================================================ 4. the validator

@dataclass
class Failure:
    code: str
    claim_ids: list[str]
    detail: str
    required_action: str
    rule_id: str | None = None
    sentence: str | None = None


@dataclass
class ValidationResult:
    valid: bool
    failure_codes: list[str]
    affected_claim_ids: list[str]
    required_actions: list[str]
    failures: list[dict] = field(default_factory=list)
    validator_version: str = VALIDATOR_VERSION
    contract_version: str = CONTRACT_VERSION
    section_id: str = SECTION_ID

    def as_dict(self) -> dict:
        return asdict(self)


def validate(candidate_claim_ids: Iterable[str],
             candidate_text_units: Iterable[str],
             citation_keys: dict[str, list[str]] | None = None,
             contract: CompositionContract | None = None) -> ValidationResult:
    """Validate one candidate draft unit against the SEC-02-2 composition contract.

    `candidate_claim_ids` are the claims the drafter says the unit rests on. `candidate_text_units`
    are the paragraphs (never written by this phase - the fixtures are synthetic). `citation_keys`
    maps claim_id -> the source keys the unit actually cites.
    """
    contract = contract or load_contract()
    claim_ids = list(candidate_claim_ids)
    units = [unit for unit in candidate_text_units if unit and unit.strip()]
    citation_keys = citation_keys or {}
    failures: list[Failure] = []

    failures += _check_claim_admissibility(claim_ids, citation_keys, contract)
    for unit in units:
        failures += _check_forbidden_synthesis(unit, claim_ids, contract)
        failures += _check_qualifiers(unit, claim_ids, contract)
        failures += _check_pairs(unit, contract)
        failures += _check_derived_numbers(unit, claim_ids, contract)

    ordered: list[Failure] = []
    for code in FAILURE_CODES:
        ordered += [f for f in failures if f.code == code]
    return ValidationResult(
        valid=not ordered,
        failure_codes=sorted({f.code for f in ordered}, key=FAILURE_CODES.index),
        affected_claim_ids=sorted({cid for f in ordered for cid in f.claim_ids}),
        required_actions=list(dict.fromkeys(f.required_action for f in ordered)),
        failures=[asdict(f) for f in ordered])


def _check_claim_admissibility(claim_ids: list[str], citation_keys: dict[str, list[str]],
                               contract: CompositionContract) -> list[Failure]:
    failures: list[Failure] = []
    for claim_id in claim_ids:
        denied = contract.denylist.get(claim_id)
        if denied is not None:
            reasons = set(denied.get("deny_reasons", []))
            status = denied.get("support_status")
            # support_status is the authoritative field and is checked before the reason strings.
            # A claim can carry 'clause_not_fully_supported' while its status is
            # INSUFFICIENT_EVIDENCE - that is unsupported, not partial, and reporting it as
            # partial would overstate how close it is to being usable.
            if "superseded" in reasons or denied.get("superseded_by"):
                code = "CLAIM_SUPERSEDED"
            elif status == "PARTIALLY_SUPPORTED":
                code = "CLAIM_PARTIAL"
            elif status in ("INSUFFICIENT_EVIDENCE", "UNSUPPORTED", "DERIVED_ONLY",
                            "SUPPORTED_BUT_UNSAFE_AS_WRITTEN"):
                code = "CLAIM_UNSUPPORTED"
            elif "partial" in reasons:
                code = "CLAIM_PARTIAL"
            else:
                code = "CLAIM_UNSUPPORTED"
            failures.append(Failure(
                code=code, claim_ids=[claim_id],
                detail=f"{claim_id} is on the composition denylist: {sorted(reasons)}",
                required_action=f"remove {claim_id} from the draft unit; it is not draftable"))
            continue
        row = contract.allowlist.get(claim_id)
        if row is None:
            failures.append(Failure(
                code="CLAIM_NOT_ALLOWLISTED", claim_ids=[claim_id],
                detail=f"{claim_id} is on neither the composition-safe allowlist nor the "
                       f"denylist - it is not a known SEC-02-2 claim",
                required_action=f"remove {claim_id}; only allowlisted claims may be drafted"))
            continue
        if not row.get("composition_safe"):
            failures.append(Failure(
                code="CLAIM_NOT_ALLOWLISTED", claim_ids=[claim_id],
                detail=f"{claim_id} is allowlisted for evidence but not composition-safe",
                required_action=f"remove {claim_id} or use its narrowed replacement"))
            continue
        expected = set(row.get("source_keys") or [])
        if not expected:
            failures.append(Failure(
                code="MISSING_SOURCE_KEY", claim_ids=[claim_id],
                detail=f"{claim_id} resolves to no source key",
                required_action=f"do not draft {claim_id}: provenance is incomplete"))
            continue
        cited = set(citation_keys.get(claim_id) or [])
        if not cited:
            failures.append(Failure(
                code="MISSING_SOURCE_KEY", claim_ids=[claim_id],
                detail=f"the unit cites no source key for {claim_id} (expected one of "
                       f"{sorted(expected)})",
                required_action=f"cite at least one registered source key for {claim_id}"))
        elif not cited & expected:
            failures.append(Failure(
                code="MISSING_SOURCE_KEY", claim_ids=[claim_id],
                detail=f"the unit cites {sorted(cited)} for {claim_id}, none of which is one of "
                       f"its registered keys {sorted(expected)}",
                required_action=f"cite {claim_id} against its own registered source keys"))
    return failures


def _check_forbidden_synthesis(unit: str, claim_ids: list[str],
                               contract: CompositionContract) -> list[Failure]:
    """Historical wordings and same-sentence juxtaposition of mutually restricted figures.

    The same-sentence rule needs no connector analysis, which is the point: a prohibition that
    depends on spotting the right conjunction can be evaded by choosing a different one.
    """
    failures: list[Failure] = []
    folded_unit = fold(unit)
    for rule in contract.synthesis_rules:
        for pattern in rule["forbidden_patterns"]:
            if re.search(pattern, folded_unit):
                failures.append(Failure(
                    code="FORBIDDEN_SYNTHESIS",
                    claim_ids=list(rule["component_claim_ids"]),
                    detail=f"{rule['synthesis_id']}: the unit matches a forbidden pattern for "
                           f"{rule['forbidden_relationship']}",
                    required_action=rule["required_action"], rule_id=rule["rule_id"]))
                break
    figures = find_figures(unit, contract)
    by_figure = {f["figure_id"]: f for f in contract.contract["restricted_figures"]}
    for sentence in sentences(unit):
        present = [fid for fid, carrying in figures.items() if sentence in carrying]
        for index, left in enumerate(present):
            for right in present[index + 1:]:
                left_claim = by_figure[left]["claim_id"]
                right_claim = by_figure[right]["claim_id"]
                pair = contract.pair(left_claim, right_claim)
                if pair is None or pair.get("allowed_same_sentence"):
                    continue
                failures.append(Failure(
                    code="FORBIDDEN_SYNTHESIS", claim_ids=sorted({left_claim, right_claim}),
                    detail=f"{by_figure[left]['label']} and {by_figure[right]['label']} appear in "
                           f"one sentence. Their scopes differ "
                           f"({by_figure[left]['material_scope']} vs "
                           f"{by_figure[right]['material_scope']}), so any single sentence "
                           f"holding both asserts a relation no source states.",
                    required_action=pair["required_action"], sentence=sentence,
                    rule_id=pair.get("constraint_id")))
    return failures


def _check_qualifiers(unit: str, claim_ids: list[str],
                      contract: CompositionContract) -> list[Failure]:
    """A figure that is meaningless without its scope must carry that scope in its own sentence."""
    failures: list[Failure] = []
    by_figure = {f["figure_id"]: f for f in contract.contract["restricted_figures"]}
    figures = find_figures(unit, contract)
    for rule in contract.qualifier_rules:
        figure = by_figure[rule["figure_id"]]
        for sentence in figures.get(rule["figure_id"], []):
            has_required = scope_in_sentence(sentence, rule["required_scope"], contract)
            wrong = [scope for scope in rule["forbidden_scopes"]
                     if scope_in_sentence(sentence, scope, contract)]
            if wrong and not has_required:
                failures.append(Failure(
                    code="AMBIGUOUS_SCOPE", claim_ids=[rule["claim_id"]],
                    detail=f"{figure['label']} is presented under scope {wrong} but belongs to "
                           f"{rule['required_scope']}. {rule['misattribution_note']}",
                    required_action=rule["required_action"], sentence=sentence,
                    rule_id=rule["rule_id"]))
            elif not has_required and rule.get("enforce_unqualified", True):
                failures.append(Failure(
                    code="UNQUALIFIED_SCOPE", claim_ids=[rule["claim_id"]],
                    detail=f"{figure['label']} appears without the mandatory scope qualifier "
                           f"({rule['required_scope']}). Forbidden bare form: "
                           f"\"{rule['forbidden_unqualified_form']}\"",
                    required_action=rule["required_action"], sentence=sentence,
                    rule_id=rule["rule_id"]))
    # Same-scope families still need their distinguishing condition. 350 and 400 may share a
    # sentence, but only as dry-system vs wet-system: without both system markers the sentence
    # merges two different requirements into one figure or into an invented range.
    for family in contract.contract["scope_families"]:
        for sentence in sentences(unit):
            present = [fid for fid in family["figure_ids"]
                       if sentence in figures.get(fid, [])]
            if len(present) < 2:
                continue
            missing = [fid for fid in present
                       if not scope_in_sentence(sentence, by_figure[fid]["system_scope"],
                                                contract)]
            if missing:
                failures.append(Failure(
                    code="AMBIGUOUS_SCOPE",
                    claim_ids=sorted({by_figure[fid]["claim_id"] for fid in missing}),
                    detail=f"{[by_figure[fid]['label'] for fid in missing]} share a sentence "
                           f"without their distinguishing system scope. {family['note']}",
                    required_action=family["required_action"], sentence=sentence,
                    rule_id=family["family_id"]))
    return failures


def _check_pairs(unit: str, contract: CompositionContract) -> list[Failure]:
    """Cross-sentence relation assertion between claims whose only allowed relation is
    INDEPENDENT.

    Same-sentence co-occurrence is already handled as FORBIDDEN_SYNTHESIS. What is left is the
    paragraph case the contract permits: separate sentences, each scoped. It stops being permitted
    the moment one of those sentences opens with a connector that ties it to the other.
    """
    failures: list[Failure] = []
    by_figure = {f["figure_id"]: f for f in contract.contract["restricted_figures"]}
    figures = find_figures(unit, contract)
    units = sentences(unit)
    index_of = {sentence: position for position, sentence in enumerate(units)}
    for (left_claim, right_claim), pair in contract.pairs.items():
        if pair["relationship_policy"] != "INDEPENDENT":
            continue
        left_figures = [fid for fid, figure in by_figure.items()
                        if figure["claim_id"] == left_claim and fid in figures]
        right_figures = [fid for fid, figure in by_figure.items()
                         if figure["claim_id"] == right_claim and fid in figures]
        if not left_figures or not right_figures:
            continue
        left_positions = {index_of[s] for fid in left_figures for s in figures[fid]}
        right_positions = {index_of[s] for fid in right_figures for s in figures[fid]}
        for position in sorted(left_positions | right_positions):
            other = right_positions if position in left_positions else left_positions
            if not any(abs(position - candidate) == 1 for candidate in other):
                continue
            sentence = units[position]
            opener = fold(sentence)
            for connector in contract.connectors["relation_asserting"]:
                folded_connector = fold(connector)
                if re.match(rf"^{re.escape(folded_connector)}\b", opener) or \
                        re.search(rf"(?:^|[,;]\s*){re.escape(folded_connector)}\b", opener):
                    failures.append(Failure(
                        code="UNSUPPORTED_RELATION",
                        claim_ids=sorted({left_claim, right_claim}),
                        detail=f"the sentence carrying one of these claims is tied to the "
                               f"adjacent sentence carrying the other by \"{connector}\". Their "
                               f"only licensed relation is INDEPENDENT.",
                        required_action=pair["required_action"], sentence=sentence,
                        rule_id=pair["constraint_id"]))
                    break
    return failures


def _check_derived_numbers(unit: str, claim_ids: list[str],
                           contract: CompositionContract) -> list[Failure]:
    """A converted figure must not be attributed to a source that never stated it.

    Keyed on context, not on the string: SEC-02-2-C-009's clay-zone '100-150 mm' is source-stated
    and must keep passing.
    """
    failures: list[Failure] = []
    for rule in contract.derived_rules:
        pattern = figure_pattern(rule["derived_value"], rule["derived_unit"])
        for sentence in sentences(unit):
            folded = fold(sentence)
            if not pattern.search(folded):
                continue
            exempt = any(re.search(fold(marker), folded)
                         for marker in rule["exempt_context_markers"])
            if exempt:
                continue
            in_context = any(re.search(fold(marker), folded)
                             for marker in rule["context_markers"])
            declared = rule["claim_id"] in claim_ids
            if not (in_context or declared):
                continue
            failures.append(Failure(
                code="DERIVED_VALUE_AS_SOURCE_STATED", claim_ids=[rule["claim_id"]],
                detail=f"{rule['derived_value']} {rule['derived_unit']} is a conversion of "
                       f"{rule['source_value']} {rule['source_unit']} that no source states. "
                       f"Policy: {rule['drafting_policy']}.",
                required_action=rule["required_action"], sentence=sentence,
                rule_id=rule["rule_id"]))
    return failures


# ================================================================ 5. fixture harness

def run_fixtures(fixtures: list[dict],
                 contract: CompositionContract | None = None) -> dict[str, Any]:
    """Score the regression suite.

    A false accept is a case the contract says must fail that the validator passed - the dangerous
    direction. A false reject is a safe case the validator rejected. Both must be zero; a code
    mismatch is reported separately, because a case that fails for the wrong reason is a rule that
    is not doing the job it claims to.
    """
    contract = contract or load_contract()
    results = []
    false_accepts, false_rejects, code_mismatches = [], [], []
    for fixture in fixtures:
        result = validate(fixture.get("candidate_claim_ids", []),
                          fixture.get("candidate_text_units", []),
                          fixture.get("citation_keys", {}), contract)
        should_pass = fixture["expected_valid"]
        row = {"case_id": fixture["case_id"], "expected_valid": should_pass,
               "actual_valid": result.valid,
               "expected_failure_codes": sorted(fixture.get("expected_failure_codes", [])),
               "actual_failure_codes": result.failure_codes,
               "polarity": "positive" if should_pass else "negative",
               "detail": [f["detail"] for f in result.failures]}
        if should_pass and not result.valid:
            false_rejects.append(fixture["case_id"])
            row["outcome"] = "FALSE_REJECT"
        elif not should_pass and result.valid:
            false_accepts.append(fixture["case_id"])
            row["outcome"] = "FALSE_ACCEPT"
        else:
            expected_codes = set(fixture.get("expected_failure_codes", []))
            if expected_codes and not expected_codes <= set(result.failure_codes):
                code_mismatches.append(fixture["case_id"])
                row["outcome"] = "CODE_MISMATCH"
            else:
                row["outcome"] = "PASS"
        results.append(row)
    passed = [r for r in results if r["outcome"] == "PASS"]
    return {"total": len(results), "passed": len(passed),
            "positive": sum(1 for r in results if r["polarity"] == "positive"),
            "negative": sum(1 for r in results if r["polarity"] == "negative"),
            "false_accepts": false_accepts, "false_rejects": false_rejects,
            "code_mismatches": code_mismatches, "rows": results,
            "all_pass": len(passed) == len(results)}


if __name__ == "__main__":
    import sys
    print(f"{VALIDATOR_VERSION}\nThis module is a library. Run "
          f"scripts/45_sec_02_2_limitation_resolution_v1.py to author the contract and score the "
          f"regression suite.")
    sys.exit(0)
