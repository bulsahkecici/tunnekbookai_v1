"""Section Draft Validator v1.1.

Parent: scripts/49_section_draft_validator_v1.py, which is not modified and not re-implemented.
This module imports it and adds two stages. Everything v1 decided, v1.1 decides identically; the
only way a draft that passed v1 fails v1.1 is by tripping one of the two new rules.

Both rules come from the rejected first SEC-02-2 pilot, and neither is a loosening.

**Stage J - language.** The pilot put two untranslated English sentences into a DraftIR declaring
`language: "tr"`. One was rejected for an unrelated reason; the other passed all nine stages. v1
had no per-unit language rule at all - the gap was recorded as a limitation of the drafting
contract rather than papered over mid-flight - and closing it is this phase's job. The detector
lives in scripts/51 and its lexicons live in a frozen contract, so the rule is auditable rather
than a model's opinion.

**Stage K - registered semantic constraints.** The pilot wrote Tablo-351-5's core-sample
acceptance criteria without the qualifier that says they are acceptance criteria, which risks
presenting an acceptance table as the thing that establishes the C25/30 strength class. v1's
qualifier rule caught it - correctly, by anchor count - but by a heuristic that happens to fire
rather than by a rule that knows what the distinction is. Stage K encodes the distinction: a
claim whose scope is a design table may not be drafted as the source of the requirement the table
tests.

Stage K is keyed on scope fields and declared markers, never on the pilot's exact wording (§11).
It applies to every claim carrying a registered DraftSemanticConstraint, and the registry is a
frozen artifact - a claim acquires the rule by declaring `design_table` scope and being given a
constraint, not by being named in this file.

What v1.1 does NOT do: it does not translate, repair, soften, or re-order anything. It rejects.
The new failure codes are appended to v1's list; none is renamed and none is removed.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1.1"
PARENT_VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1"
VALIDATION_CONTRACT_VERSION = "tunnelbook-draft-validation-contract-v1.1"
SECTION_ID = "SEC-02-2"

REMEDIATION = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "remediation_v1"
SEMANTIC_CONSTRAINTS_PATH = REMEDIATION / "contracts" / "draft_semantic_constraints_v1.json"
CROSS_LINGUAL_PATH = REMEDIATION / "contracts" / "cross_lingual_condition_mappings_v1.json"
VALIDATION_CONTRACT_V1_1_PATH = (ROOT / "data" / "book" / "drafting" / "contracts"
                                 / "draft_validation_contract_v1_1.json")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")
language = _load("draft_language_validator_v1", "scripts/51_draft_language_validator_v1.py")

# Re-exported so callers can treat v1.1 as a drop-in. These are the same objects, not copies:
# a second definition of DraftUnit would compare unequal to the one the renderer parses.
DraftIR = base.DraftIR
DraftUnit = base.DraftUnit
DraftSchemaError = base.DraftSchemaError
DraftingBundle = base.DraftingBundle
UnitFailure = base.UnitFailure
parse_draft_ir = base.parse_draft_ir
load_bundle = base.load_bundle
load_source_registry = base.load_source_registry
paragraph_texts = base.paragraph_texts
fold = base.fold
tokens = base.tokens
content_tokens = base.content_tokens
prefix_agreement = base.prefix_agreement
PACKET_EID_RE = base.PACKET_EID_RE
CLAIM_ID_RE = base.CLAIM_ID_RE
SOURCE_KEY_RE = base.SOURCE_KEY_RE

# Appended, never reordered above the inherited entries: the codes are a contract with the
# remediation report, and renumbering them would silently rewrite older audits' meaning.
NEW_REJECTION_CODES = ("LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS", "SEMANTIC_SCOPE_MISMATCH")
REJECTION_CODES = base.REJECTION_CODES + NEW_REJECTION_CODES

# §33's order. Language runs before composition and before any ACCEPT is returned (§34); the
# verdict does not depend on the order because every stage always runs, but the reported failure
# order does, and a remediation report is read top-down.
STAGES = ("A_allowlist", "B_denylist", "C_support", "D_numeric", "E_conditions", "J_language",
          "K_semantic", "F_composition", "G_sources", "H_citation", "I_rendering")

_STAGE_RANK = {name: index for index, name in enumerate(STAGES)}


# ================================================================ 1. registered constraints

def load_semantic_constraints(path: Path = SEMANTIC_CONSTRAINTS_PATH) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("constraints", []))


def load_cross_lingual_mappings(path: Path = CROSS_LINGUAL_PATH) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("mappings", []))


def mapping_consistency(bundle: DraftingBundle,
                        mappings: Iterable[dict] | None = None) -> dict[str, Any]:
    """Every registered Turkish rendering must already be licensed by the frozen contract.

    This is the guard against §50's failure mode. A mapping file that could introduce anchors the
    frozen drafting contract does not carry would be a way to widen what counts as a surviving
    condition - a validator loosening wearing the costume of a translation table. So the mapping
    is required to be a *subset* of the frozen glosses: it makes the translation explicit and
    auditable without being able to license anything new.
    """
    mappings = list(mappings if mappings is not None else load_cross_lingual_mappings())
    glosses = bundle.contract.get("condition_glosses", {})
    rows, unlicensed = [], []
    for mapping in mappings:
        claim_id = mapping["claim_id"]
        condition = mapping["source_condition"]
        frozen = {fold(t) for t in glosses.get(claim_id, {}).get(condition, [])}
        frozen |= {fold(t) for t in content_tokens(condition, bundle.function_lexicon)}
        registered = {fold(t) for t in mapping.get("registered_anchors", [])}
        stray = sorted(a for a in registered
                       if not any(prefix_agreement(a, f) for f in frozen))
        rows.append({"mapping_id": mapping["mapping_id"], "claim_id": claim_id,
                     "source_condition": condition, "registered_anchors": sorted(registered),
                     "frozen_gloss_anchors": sorted(frozen), "unlicensed_anchors": stray,
                     "consistent": not stray})
        unlicensed += [f"{mapping['mapping_id']}:{a}" for a in stray]
    return {"rows": rows, "unlicensed_anchors": unlicensed, "consistent": not unlicensed,
            "mapping_count": len(rows)}


# ================================================================ 2. stage J - language

def stage_j_language(unit: DraftUnit, section_language: str,
                     language_contract: dict) -> list[UnitFailure]:
    """Delegate to the frozen detector; translate its failures into this module's vocabulary."""
    failures: list[UnitFailure] = []
    for failure in language.validate_unit(
            unit_id=unit.unit_id, unit_type=unit.unit_type, material=unit.material,
            section_language=section_language, text=unit.text, claim_ids=unit.claim_ids,
            contract=language_contract):
        failures.append(UnitFailure(
            code=failure.code, unit_id=failure.unit_id, detail=failure.detail,
            required_action=failure.required_action, stage="J_language",
            claim_ids=list(failure.claim_ids), rule_id=failure.rule_id,
            evidence=failure.evidence))
    return failures


# ================================================================ 3. stage K - semantics

def _clauses(text: str) -> list[str]:
    return [c.strip() for c in re.split(r"[.;:!?\n]|,", text) if c.strip()]


def _any_marker(markers: Iterable[str], folded: str) -> str | None:
    for marker in markers:
        if fold(marker) in folded:
            return marker
    return None


def _constraint_applies(constraint: dict, unit: DraftUnit, bundle: DraftingBundle) -> bool:
    """A constraint binds a unit when the unit declares its claim.

    The scope test is asserted rather than assumed: a constraint declaring `design_table` scope
    must actually be attached to a claim whose allowlist row says so, or the constraint is stale
    and silently protecting nothing.
    """
    if constraint["claim_id"] not in unit.claim_ids:
        return False
    required_scope = constraint.get("requirement_scope_marker")
    if not required_scope:
        return True
    claim = bundle.allowlist.get(constraint["claim_id"]) or {}
    scope = (claim.get("scope") or {}).get("requirement_scope") or []
    return required_scope in scope


def _forbidden_attribution(constraint: dict, text: str) -> tuple[bool, str | None]:
    """Does this text present the reference as the source of the requirement it merely tests?

    Three things must hold together, and the conjunction is what keeps the rule from firing on a
    faithful rendering. The reference must be named; it must be named *attributively* ('göre',
    'uyarınca', 'defines'); and some clause must put the requirement noun and the class
    designation in a predicate relation - the noun first, the designation after it.

    The claim's own canonical sentence satisfies the first two and not the third, which is the
    point: 'Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda ... 22,5 MPa' attributes a
    *measurement* to the table, and that is what the table states.
    """
    forbidden = constraint["forbidden_meaning_patterns"]
    folded = fold(text)
    reference = _any_marker(forbidden["reference_markers"], folded)
    if reference is None:
        return False, None
    attribution = _any_marker(forbidden["attribution_markers"], folded)
    if attribution is None:
        return False, None
    designation = re.compile(forbidden["class_designation_pattern"])
    for clause in _clauses(folded):
        for pattern in forbidden["requirement_noun_patterns"]:
            noun = re.search(pattern, clause)
            if not noun:
                continue
            after = designation.search(clause, noun.end())
            if after:
                return True, clause
    return False, None


def stage_k_semantic(unit: DraftUnit, paragraph_text: str, bundle: DraftingBundle,
                     constraints: Iterable[dict]) -> list[UnitFailure]:
    """Registered semantic boundaries. Qualifier presence at paragraph scope, meaning at unit scope.

    The two scopes are not an inconsistency. A qualifier by definition lives outside the claim's
    own sentence - that is why it is a qualifier and not part of the canonical text - so requiring
    it inside the unit would reject a faithful rendering of the claim, exactly the failure mode
    v1's condition rule was built to avoid. A forbidden *meaning*, by contrast, is asserted by one
    sentence, and a correct neighbouring sentence does not undo it.
    """
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    for constraint in constraints:
        if not _constraint_applies(constraint, unit, bundle):
            continue
        claim_id = constraint["claim_id"]
        required = constraint["required_meaning_markers"]
        haystack = fold(paragraph_text if required.get("scope", "paragraph") == "paragraph"
                        else unit.text)
        if _any_marker(required["any_of"], haystack) is None:
            failures.append(UnitFailure(
                code=constraint["missing_qualifier_code"], unit_id=unit.unit_id,
                detail=(f"{claim_id} may be stated only with its {constraint['type'].lower()} "
                        f"qualifier: {constraint['required_meaning']} No marker of that meaning "
                        f"({required['any_of']}) survives into the "
                        f"{required.get('scope', 'paragraph')}"),
                required_action=constraint["required_action"], stage="K_semantic",
                claim_ids=[claim_id], rule_id=constraint["constraint_id"],
                evidence=constraint["required_meaning"]))
        violated, clause = _forbidden_attribution(constraint, unit.text)
        if violated:
            failures.append(UnitFailure(
                code=constraint["forbidden_meaning_code"], unit_id=unit.unit_id,
                detail=(f"{claim_id} is drafted so as to assert the forbidden meaning: "
                        f"{constraint['forbidden_meaning']} The clause \"{clause}\" attributes "
                        f"the requirement itself to the reference"),
                required_action=constraint["required_action"], stage="K_semantic",
                claim_ids=[claim_id], rule_id=constraint["constraint_id"], evidence=clause))
    return failures


# ================================================================ 4. driver

def _sort_key(failure: UnitFailure) -> tuple[int, int]:
    return (_STAGE_RANK.get(failure.stage, len(STAGES)), REJECTION_CODES.index(failure.code))


def validate_unit(unit: DraftUnit, paragraph_text: str, bundle: DraftingBundle,
                  section_language: str = "tr", language_contract: dict | None = None,
                  constraints: Iterable[dict] | None = None) -> list[UnitFailure]:
    """v1's nine stages verbatim, plus J and K. No inherited stage is skipped or softened."""
    language_contract = language_contract or language.load_contract()
    constraints = list(constraints if constraints is not None else load_semantic_constraints())
    failures = list(base.validate_unit(unit, paragraph_text, bundle))
    admissible = not any(f.code in ("CLAIM_NOT_ALLOWLISTED", "CLAIM_DENYLISTED")
                         for f in failures)
    failures += stage_j_language(unit, section_language, language_contract)
    if admissible:
        failures += stage_k_semantic(unit, paragraph_text, bundle, constraints)
    return sorted(failures, key=_sort_key)


def validate_draft(ir: DraftIR, bundle: DraftingBundle | None = None,
                   language_contract: dict | None = None,
                   constraints: Iterable[dict] | None = None) -> base.DraftValidationResult:
    """All-or-nothing (§70): one rejected material unit rejects the pilot."""
    bundle = bundle or load_bundle()
    language_contract = language_contract or language.load_contract()
    constraints = list(constraints if constraints is not None else load_semantic_constraints())
    paragraphs = paragraph_texts(ir)
    results: list[base.UnitResult] = []
    histogram: dict[str, int] = {}
    for unit in ir.units:
        failures = validate_unit(unit, paragraphs.get(unit.paragraph_id, unit.text), bundle,
                                 section_language=ir.language,
                                 language_contract=language_contract, constraints=constraints)
        for failure in failures:
            histogram[failure.code] = histogram.get(failure.code, 0) + 1
        unit.validation_status = "REJECT" if failures else "ACCEPT"
        results.append(base.UnitResult(
            unit_id=unit.unit_id, status=unit.validation_status, material=unit.material,
            claim_ids=list(unit.claim_ids),
            failure_codes=sorted({f.code for f in failures}, key=REJECTION_CODES.index),
            failures=[asdict(f) for f in failures]))
    rejected = [r.unit_id for r in results if r.status == "REJECT"]
    return base.DraftValidationResult(
        status="ACCEPT" if not rejected else "REJECT", units=results,
        failure_codes=sorted(histogram, key=REJECTION_CODES.index),
        failure_histogram=dict(sorted(histogram.items())), rejected_unit_ids=rejected,
        validator_version=VALIDATOR_VERSION)


# ================================================================ 5. fixture harness

def _fixture_unit(fixture: dict) -> DraftUnit:
    return DraftUnit(
        unit_id=fixture.get("unit_id", "U-X-P01-S01"),
        unit_type=fixture.get("unit_type", "PARAGRAPH_SENTENCE"),
        text=fixture["text"], material=fixture.get("material", True),
        claim_ids=list(fixture.get("claim_ids", [])),
        source_keys=list(fixture.get("source_keys", [])),
        relationship_type=fixture.get("relationship_type", "INDEPENDENT"),
        citation_intents=list(fixture.get("citation_intents", [])))


def run_fixtures(fixtures: list[dict], bundle: DraftingBundle | None = None,
                 language_contract: dict | None = None,
                 constraints: Iterable[dict] | None = None) -> dict[str, Any]:
    """Score fixtures at whichever scope each declares.

    Three scopes, because a fixture tests one rule and the other rules must not answer for it.

    `"draft"` is the full eleven-stage pipeline and is the default.

    `"language"` runs the language detector alone. §45 asks for positive cases like 'Turkish prose
    containing FHWA' - prose whose *language* is under test and whose content no approved claim
    licenses. Running those through claim containment would reject them for a reason unrelated to
    what they check, and inventing a claim to license 'FHWA' would be inventing evidence.

    `"semantic"` runs language and the registered constraints. It exists for the C-002 boundary
    cases, whose point is what stage K decides. §53's sentence is a faithful, correctly scoped
    statement of the claim that happens to reach for two words - 'ait', 'verir' - that C-002's own
    wording does not license, so the full pipeline rejects it at stage C. That rejection is
    correct and inherited, and widening the frozen paraphrase lexicon to make a fixture pass would
    be exactly the kind of loosening this phase forbids. The fully pipeline-valid rendering of the
    same meaning is carried separately as a corrected-synthetic case.
    """
    bundle = bundle or load_bundle()
    language_contract = language_contract or language.load_contract()
    constraints = list(constraints if constraints is not None else load_semantic_constraints())
    rows, false_accepts, false_rejects, mismatches = [], [], [], []
    for fixture in fixtures:
        scope = fixture.get("fixture_scope", "draft")
        section_language = fixture.get("section_language", "tr")
        if scope == "semantic":
            unit = _fixture_unit(fixture)
            paragraph = fixture.get("paragraph_text") or unit.text
            failures = (stage_j_language(unit, section_language, language_contract)
                        + stage_k_semantic(unit, paragraph, bundle, constraints))
        elif scope == "language":
            failures = [UnitFailure(code=f.code, unit_id=f.unit_id, detail=f.detail,
                                    required_action=f.required_action, stage="J_language",
                                    claim_ids=list(f.claim_ids), rule_id=f.rule_id,
                                    evidence=f.evidence)
                        for f in language.validate_unit(
                            unit_id=fixture.get("unit_id", "U-X-P01-S01"),
                            unit_type=fixture.get("unit_type", "PARAGRAPH_SENTENCE"),
                            material=fixture.get("material", True),
                            section_language=section_language, text=fixture["text"],
                            claim_ids=fixture.get("claim_ids", []), contract=language_contract)]
        else:
            unit = _fixture_unit(fixture)
            paragraph = fixture.get("paragraph_text") or unit.text
            failures = validate_unit(unit, paragraph, bundle, section_language=section_language,
                                     language_contract=language_contract, constraints=constraints)
        actual = sorted({f.code for f in failures}, key=REJECTION_CODES.index)
        expected_valid = fixture["expected_valid"]
        row = {"case_id": fixture["case_id"], "fixture_scope": scope,
               "category": fixture.get("category"), "expected_valid": expected_valid,
               "actual_valid": not failures,
               "expected_failure_codes": sorted(fixture.get("expected_failure_codes", [])),
               "actual_failure_codes": actual,
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
    language_rows = [r for r in rows if r["fixture_scope"] == "language"]
    return {"total": len(rows), "passed": len(passed),
            "positive": sum(1 for r in rows if r["polarity"] == "positive"),
            "negative": sum(1 for r in rows if r["polarity"] == "negative"),
            "language_total": len(language_rows),
            "language_passed": sum(1 for r in language_rows if r["outcome"] == "PASS"),
            "language_false_accepts": [r["case_id"] for r in language_rows
                                       if r["outcome"] == "FALSE_ACCEPT"],
            "language_false_rejects": [r["case_id"] for r in language_rows
                                       if r["outcome"] == "FALSE_REJECT"],
            "false_accepts": false_accepts, "false_rejects": false_rejects,
            "code_mismatches": mismatches, "rows": rows,
            "all_pass": len(passed) == len(rows)}


if __name__ == "__main__":
    print(f"{VALIDATOR_VERSION}\nThis module is a library. Run "
          f"scripts/50_sec_02_2_draft_failure_remediation_v1.py to author the remediation "
          f"contracts, score the fixtures and run the one authorised pilot attempt.")
