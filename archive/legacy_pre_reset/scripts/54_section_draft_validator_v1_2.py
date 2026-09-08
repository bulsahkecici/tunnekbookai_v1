"""Section Draft Validator v1.2 - registered qualifier semantics (stage L).

Parent: scripts/52_section_draft_validator_v1_1.py, which is not modified and not re-implemented,
and through it scripts/49. This module imports both and adds one stage. Everything v1.1 decided,
v1.2 decides identically; the only way a draft that passed v1.1 fails v1.2 is by tripping stage L.

**Why stage L exists - DF-01.** Stage E scores a qualifier preserved when at least half of its
lexical anchors reach the paragraph. That is a reasonable proxy for a qualifier phrased in words
the claim does not use, and it is no proxy at all for one phrased in words the claim already uses.
SEC-02-2-C-009's qualifier - "§351.08.10.02 kil zonlu tabakalara özgüdür; genel ilk katman
kalınlığı değildir" - shares kil, zonlu, tabakalara, katman and kalınlığı with its own canonical
sentence. Attempt #2 copied that sentence verbatim, stated the qualifier's meaning nowhere, and
scored 5 of 6 anchors present. Stage E called it preserved. Realised preservation was zero.

**Why not a higher percentage.** Raising the half-anchor threshold to 75% or 100% would be the
same kind of rule with a different constant: it would reject faithful prose that renders the
meaning in other words, and it would still pass a verbatim copy whose overlap happens to be
total - which is exactly the DF-01 case, at 5/6 and climbing to 6/6 on any sentence that also
says "özgü". The percentage is not the defect. Measuring vocabulary instead of meaning is.

**What stage L does instead.** It follows DSC-C002-001's design principle: a qualifier with
material scope-changing meaning gets explicit, deterministic required-meaning constructions. A
construction is a set of pattern groups that must be satisfied *within one clause* - an operator,
and the thing the operator is applied to. Clause scope is what stops padding: a paragraph can
contain "özgü" and it can contain "kil", and neither the registry nor stage E can tell whether
they were said about each other, but a clause can.

Stage E is untouched and still runs. Stage L cannot accept anything; it can only add a failure.
A unit declaring no registered claim gets no failure from it, which is the guarantee that this
tightening cannot newly reject unrelated material.

The registry is a versioned artifact, not code: a claim acquires a rule by carrying an entry
whose declared scope matches its allowlist row. Two integrity properties are enforced fail-closed
before any verdict, because a registry that silently protects nothing is worse than no registry -
the qualifier text must still match the frozen allowlist byte for byte, and the claim's own
canonical sentence must NOT satisfy the entry's constructions. That second check is DF-01 stated
as a general property: an entry a verbatim copy would satisfy cannot distinguish realisation from
reproduction, and is refused.
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

VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1.2"
PARENT_VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1.1"
VALIDATION_CONTRACT_VERSION = "tunnelbook-draft-validation-contract-v1.2"
SECTION_ID = "SEC-02-2"

QUALIFIER_VALIDATION = (ROOT / "data" / "book" / "drafting" / "sec_02_2"
                        / "qualifier_validation_v1")
QUALIFIER_SEMANTICS_PATH = (QUALIFIER_VALIDATION / "contracts"
                            / "draft_qualifier_semantics_v1.json")
VALIDATION_CONTRACT_V1_2_PATH = (ROOT / "data" / "book" / "drafting" / "contracts"
                                 / "draft_validation_contract_v1_2.json")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


parent = _load("section_draft_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")
base = parent.base
language = parent.language

# Re-exported so callers can treat v1.2 as a drop-in. Same objects, not copies.
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
load_semantic_constraints = parent.load_semantic_constraints
load_cross_lingual_mappings = parent.load_cross_lingual_mappings
mapping_consistency = parent.mapping_consistency
stage_j_language = parent.stage_j_language
stage_k_semantic = parent.stage_k_semantic

# No new code. DF-01 is an absent required meaning, which is what QUALIFIER_DROPPED already means,
# and an actively generalised scope is what SEMANTIC_SCOPE_MISMATCH already means. Inventing a
# third code would split one concept across two audits' vocabularies for no gain.
NEW_REJECTION_CODES: tuple[str, ...] = ()
REJECTION_CODES = parent.REJECTION_CODES + NEW_REJECTION_CODES

# L sits immediately after K: both decide registered meaning, and a reader of a rejection report
# should meet them together. No inherited stage moves.
STAGES = ("A_allowlist", "B_denylist", "C_support", "D_numeric", "E_conditions", "J_language",
          "K_semantic", "L_qualifier_semantics", "F_composition", "G_sources", "H_citation",
          "I_rendering")

_STAGE_RANK = {name: index for index, name in enumerate(STAGES)}


class QualifierRegistryError(ValueError):
    """The registry does not describe the frozen claims it claims to describe. Terminal."""


# ================================================================ 1. registry

def load_qualifier_semantics(path: Path = QUALIFIER_SEMANTICS_PATH) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("qualifier_semantics", []))


def _clauses(folded: str) -> list[str]:
    """v1.1's clause split, applied to already-folded text.

    Shared with stage K deliberately: two different clause definitions in one validator would
    make 'in the same clause' mean two things depending on which rule was reading.
    """
    return [c.strip() for c in re.split(r"[.;:!?\n]|,", folded) if c.strip()]


def _clause_satisfies(construction: dict, clause: str) -> bool:
    for group in construction["clause_requires"]:
        if not any(re.search(pattern, clause) for pattern in group["any_of"]):
            return False
    return not any(re.search(pattern, clause)
                   for pattern in construction.get("clause_forbids", []))


def _matching_clause(construction: dict, text: str) -> str | None:
    for clause in _clauses(fold(text)):
        if _clause_satisfies(construction, clause):
            return clause
    return None


def realised_constructions(entry: dict, text: str) -> list[dict]:
    """Which required constructions this text actually realises, with the clause that did it."""
    found = []
    for construction in entry["required_constructions"]["items"]:
        clause = _matching_clause(construction, text)
        if clause is not None:
            found.append({"construction_id": construction["construction_id"], "clause": clause})
    return found


def _meaning_realised(entry: dict, text: str) -> list[dict]:
    realised = realised_constructions(entry, text)
    if entry["required_constructions"].get("match", "any_of") == "all_of":
        return realised if len(realised) == len(entry["required_constructions"]["items"]) else []
    return realised


def generalisation_violations(entry: dict, text: str) -> list[dict]:
    forbidden = entry.get("forbidden_generalisation")
    if not forbidden:
        return []
    out = []
    for construction in forbidden["items"]:
        clause = _matching_clause(construction, text)
        if clause is not None:
            out.append({"construction_id": construction["construction_id"], "clause": clause})
    return out


def registry_integrity(bundle: DraftingBundle,
                       entries: Iterable[dict] | None = None) -> dict[str, Any]:
    """Is every entry still describing the frozen claim it names?

    Three properties, all fail-closed. The claim must be allowlisted and carry the declared scope,
    so a stale entry cannot sit in the file protecting nothing. The qualifier text must equal the
    frozen one byte for byte, so the registry cannot become a second, editable copy of a frozen
    qualifier. And the canonical sentence must not satisfy the constructions - DF-01 as a general
    property rather than as a fact about one claim.
    """
    entries = list(entries if entries is not None else load_qualifier_semantics())
    rows, problems = [], []
    for entry in entries:
        constraint_id = entry["constraint_id"]
        claim_id = entry["claim_id"]
        claim = bundle.allowlist.get(claim_id)
        row: dict[str, Any] = {"constraint_id": constraint_id, "claim_id": claim_id,
                               "claim_allowlisted": claim is not None}
        if claim is None:
            problems.append(f"{constraint_id}: {claim_id} is not allowlisted")
            rows.append(row)
            continue
        frozen_qualifiers = list(claim.get("qualifiers") or [])
        index = entry.get("qualifier_index", 0)
        frozen = frozen_qualifiers[index] if index < len(frozen_qualifiers) else None
        row["qualifier_matches_frozen"] = frozen == entry["qualifier_text"]
        if not row["qualifier_matches_frozen"]:
            problems.append(f"{constraint_id}: qualifier_text does not match the frozen qualifier")

        markers = entry.get("claim_scope_markers")
        if markers:
            declared = (claim.get("scope") or {}).get(markers["field"]) or []
            row["scope_matches"] = any(m in declared for m in markers["any_of"])
            if not row["scope_matches"]:
                problems.append(f"{constraint_id}: {claim_id} declares no "
                                f"{markers['field']} in {markers['any_of']}")

        canonical = claim.get("canonical_claim") or ""
        satisfied_by_canonical = realised_constructions(entry, canonical)
        row["canonical_satisfies"] = [c["construction_id"] for c in satisfied_by_canonical]
        if entry.get("self_test", {}).get("canonical_claim_must_not_satisfy") \
                and satisfied_by_canonical:
            problems.append(f"{constraint_id}: the canonical claim itself satisfies "
                            f"{row['canonical_satisfies']} - the entry cannot tell semantic "
                            f"realisation from verbatim reproduction (DF-01)")
        row["consistent"] = not any(p.startswith(f"{constraint_id}:") for p in problems)
        rows.append(row)
    return {"rows": rows, "problems": problems, "consistent": not problems,
            "entry_count": len(rows)}


# ================================================================ 2. stage L

def stage_l_qualifier_semantics(unit: DraftUnit, paragraph_text: str, bundle: DraftingBundle,
                                entries: Iterable[dict]) -> list[UnitFailure]:
    """Registered qualifier semantics. Required meaning at paragraph scope, generalisation at unit.

    The scopes follow stage K for the same reason: a qualifier is by definition outside the
    claim's own sentence, so requiring it inside the unit would reject a faithful rendering of the
    claim - while an asserted generalisation is made by one sentence and a correct neighbour does
    not retract it.
    """
    failures: list[UnitFailure] = []
    if not unit.material:
        return failures
    for entry in entries:
        if entry["claim_id"] not in unit.claim_ids:
            continue
        claim_id = entry["claim_id"]
        scope = entry.get("required_meaning_scope", "paragraph")
        haystack = paragraph_text if scope == "paragraph" else unit.text
        if not _meaning_realised(entry, haystack):
            constructions = [c["construction_id"]
                             for c in entry["required_constructions"]["items"]]
            failures.append(UnitFailure(
                code=entry["missing_meaning_code"], unit_id=unit.unit_id,
                detail=(f"{claim_id} carries the registered qualifier "
                        f"\"{entry['qualifier_text']}\"; its required meaning "
                        f"({entry['required_meaning']}) is realised by no clause in the {scope}. "
                        f"None of {constructions} is present. Lexical overlap with the claim's "
                        f"own vocabulary does not discharge it"),
                required_action=entry["required_action"], stage="L_qualifier_semantics",
                claim_ids=[claim_id], rule_id=entry["constraint_id"],
                evidence=entry["qualifier_text"]))
        for violation in generalisation_violations(entry, unit.text):
            failures.append(UnitFailure(
                code=entry["forbidden_generalisation"]["code"], unit_id=unit.unit_id,
                detail=(f"{claim_id} is drafted so as to state the generalised scope its "
                        f"qualifier denies. The clause \"{violation['clause']}\" matches "
                        f"{violation['construction_id']}"),
                required_action=entry["required_action"], stage="L_qualifier_semantics",
                claim_ids=[claim_id], rule_id=entry["constraint_id"],
                evidence=violation["clause"]))
    return failures


# ================================================================ 3. driver

def _sort_key(failure: UnitFailure) -> tuple[int, int]:
    return (_STAGE_RANK.get(failure.stage, len(STAGES)), REJECTION_CODES.index(failure.code))


def validate_unit(unit: DraftUnit, paragraph_text: str, bundle: DraftingBundle,
                  section_language: str = "tr", language_contract: dict | None = None,
                  constraints: Iterable[dict] | None = None,
                  qualifier_semantics: Iterable[dict] | None = None) -> list[UnitFailure]:
    """v1.1's eleven stages verbatim, plus L. No inherited stage is skipped or softened."""
    entries = list(qualifier_semantics if qualifier_semantics is not None
                   else load_qualifier_semantics())
    failures = list(parent.validate_unit(unit, paragraph_text, bundle,
                                         section_language=section_language,
                                         language_contract=language_contract,
                                         constraints=constraints))
    admissible = not any(f.code in ("CLAIM_NOT_ALLOWLISTED", "CLAIM_DENYLISTED")
                         for f in failures)
    if admissible:
        failures += stage_l_qualifier_semantics(unit, paragraph_text, bundle, entries)
    return sorted(failures, key=_sort_key)


def validate_draft(ir: DraftIR, bundle: DraftingBundle | None = None,
                   language_contract: dict | None = None,
                   constraints: Iterable[dict] | None = None,
                   qualifier_semantics: Iterable[dict] | None = None
                   ) -> base.DraftValidationResult:
    """All-or-nothing (§70): one rejected material unit rejects the pilot."""
    bundle = bundle or load_bundle()
    language_contract = language_contract or language.load_contract()
    constraints = list(constraints if constraints is not None else load_semantic_constraints())
    entries = list(qualifier_semantics if qualifier_semantics is not None
                   else load_qualifier_semantics())
    integrity = registry_integrity(bundle, entries)
    if not integrity["consistent"]:
        raise QualifierRegistryError("; ".join(integrity["problems"]))
    paragraphs = paragraph_texts(ir)
    results: list[base.UnitResult] = []
    histogram: dict[str, int] = {}
    for unit in ir.units:
        failures = validate_unit(unit, paragraphs.get(unit.paragraph_id, unit.text), bundle,
                                 section_language=ir.language,
                                 language_contract=language_contract, constraints=constraints,
                                 qualifier_semantics=entries)
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


# ================================================================ 4. fixture harness

_fixture_unit = parent._fixture_unit


def run_fixtures(fixtures: list[dict], bundle: DraftingBundle | None = None,
                 language_contract: dict | None = None,
                 constraints: Iterable[dict] | None = None,
                 qualifier_semantics: Iterable[dict] | None = None) -> dict[str, Any]:
    """v1.1's three scopes, plus `"qualifier"` for cases whose point is what stage L decides.

    The extra scope exists for the same reason v1.1's `"semantic"` scope does: a fixture tests one
    rule, and the other rules must not answer for it. A padding probe deliberately built out of
    claim vocabulary is fully pipeline-valid - that is what makes it a probe - so scoring it
    through every stage would only confirm the stages it is not about.
    """
    bundle = bundle or load_bundle()
    language_contract = language_contract or language.load_contract()
    constraints = list(constraints if constraints is not None else load_semantic_constraints())
    entries = list(qualifier_semantics if qualifier_semantics is not None
                   else load_qualifier_semantics())
    inherited = [f for f in fixtures if f.get("fixture_scope") != "qualifier"]
    result = parent.run_fixtures(inherited, bundle, language_contract, constraints) if inherited \
        else {"total": 0, "passed": 0, "positive": 0, "negative": 0, "language_total": 0,
              "language_passed": 0, "language_false_accepts": [], "language_false_rejects": [],
              "false_accepts": [], "false_rejects": [], "code_mismatches": [], "rows": [],
              "all_pass": True}
    for fixture in fixtures:
        if fixture.get("fixture_scope") != "qualifier":
            continue
        unit = _fixture_unit(fixture)
        paragraph = fixture.get("paragraph_text") or unit.text
        failures = stage_l_qualifier_semantics(unit, paragraph, bundle, entries)
        actual = sorted({f.code for f in failures}, key=REJECTION_CODES.index)
        expected_valid = fixture["expected_valid"]
        row = {"case_id": fixture["case_id"], "fixture_scope": "qualifier",
               "category": fixture.get("category"), "expected_valid": expected_valid,
               "actual_valid": not failures,
               "expected_failure_codes": sorted(fixture.get("expected_failure_codes", [])),
               "actual_failure_codes": actual,
               "polarity": "positive" if expected_valid else "negative",
               "detail": [f.detail for f in failures]}
        if expected_valid and failures:
            result["false_rejects"].append(fixture["case_id"])
            row["outcome"] = "FALSE_REJECT"
        elif not expected_valid and not failures:
            result["false_accepts"].append(fixture["case_id"])
            row["outcome"] = "FALSE_ACCEPT"
        else:
            expected = set(fixture.get("expected_failure_codes", []))
            if expected and not expected <= set(actual):
                result["code_mismatches"].append(fixture["case_id"])
                row["outcome"] = "CODE_MISMATCH"
            else:
                row["outcome"] = "PASS"
                result["passed"] += 1
        result["total"] += 1
        result["positive" if expected_valid else "negative"] += 1
        result["rows"].append(row)
    result["all_pass"] = result["passed"] == result["total"]
    return result


if __name__ == "__main__":
    print(f"{VALIDATOR_VERSION}\nThis module is a library. Run "
          f"scripts/55_sec_02_2_qualifier_validation_tightening_v1.py to reproduce DF-01, score "
          f"the fixtures and write the phase audit.")
