"""SEC-02-2 Qualifier Preservation Validation Tightening v1 - closing DF-01.

Validator-tightening phase. This phase generates nothing, retrieves nothing, writes nothing to
Qdrant, reads no corpus, renders no prose and authorises no attempt #3. It reproduces one
false-pass against frozen evidence, adds one versioned rule that closes it, and proves the rule
rejects nothing else.

DF-01, in one line: stage E measures a qualifier's *vocabulary*, and a qualifier that reuses its
own claim's vocabulary is therefore scored preserved by a verbatim copy that states it nowhere.

The reproduction is deterministic and reads only immutable artifacts: the frozen allowlist row for
SEC-02-2-C-009, and attempt #2's preserved DraftIR. It asserts four things in order - that
SEC-02-2-C-002's qualifier really is missing and really was rejected, that SEC-02-2-C-009's really
is missing too, that stage E nevertheless scored it preserved, and that the score came from anchor
overlap with the canonical sentence rather than from anything the prose said.

The remedy is not a higher anchor percentage; scripts/54 says why at length. It is a registered
qualifier-semantics entry, following DSC-C002-001's principle, validated by a new stage L in a new
validator version. Draft Validator v1 and v1.1 are read and hashed here, never written.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "tunnelbook-sec-02-2-qualifier-validation-tightening-v1"
PHASE = "SEC-02-2 QUALIFIER PRESERVATION VALIDATION TIGHTENING V1"
SECTION_ID = "SEC-02-2"
FINDING_ID = "DF-01"
TARGET_CLAIM = "SEC-02-2-C-009"
TARGET_UNIT = "U-D-P01-S03"
CONTROL_CLAIM = "SEC-02-2-C-002"
CONTROL_UNIT = "U-A-P01-S02"

BOOK = ROOT / "data" / "book"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
REMEDIATION = SECTION_DIR / "remediation_v1"
ANALYSIS = SECTION_DIR / "analysis_v2"
PHASE_DIR = SECTION_DIR / "qualifier_validation_v1"
MANIFESTS = BOOK / "manifests"

# ---- immutable evidence. Read, hashed, never written.
RAW_ATTEMPT_2 = REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_2.json"
REJECTED_2 = REMEDIATION / "rejected" / "pilot_attempt_2_validation.json"
SEMANTIC_CONSTRAINTS = REMEDIATION / "contracts" / "draft_semantic_constraints_v1.json"
FAILURE_ANALYSIS_V2 = ANALYSIS / "audits" / "attempt_2_failure_analysis_v1.json"
DRAFTING_CONTRACT = CONTRACTS / "section_drafting_contract_v1.json"
VALIDATION_CONTRACT_V1 = CONTRACTS / "draft_validation_contract_v1.json"
VALIDATION_CONTRACT_V1_1 = CONTRACTS / "draft_validation_contract_v1_1.json"
VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
VALIDATOR_V1_1 = ROOT / "scripts" / "52_section_draft_validator_v1_1.py"
ALLOWLIST = (BOOK / "sec_02_2_limitation_resolution" / "claims"
             / "composition_safe_allowlist_v1.jsonl")

FROZEN_INPUTS = {
    "attempt_2_raw": RAW_ATTEMPT_2,
    "attempt_2_rejection": REJECTED_2,
    "semantic_constraints_v1": SEMANTIC_CONSTRAINTS,
    "failure_analysis_v2": FAILURE_ANALYSIS_V2,
    "section_drafting_contract_v1": DRAFTING_CONTRACT,
    "draft_validation_contract_v1": VALIDATION_CONTRACT_V1,
    "draft_validation_contract_v1_1": VALIDATION_CONTRACT_V1_1,
    "draft_validator_v1": VALIDATOR_V1,
    "draft_validator_v1_1": VALIDATOR_V1_1,
    "composition_safe_allowlist_v1": ALLOWLIST,
}

# ---- authored by this phase.
QUALIFIER_SEMANTICS = PHASE_DIR / "contracts" / "draft_qualifier_semantics_v1.json"
VALIDATION_CONTRACT_V1_2 = CONTRACTS / "draft_validation_contract_v1_2.json"
VALIDATOR_V1_2 = ROOT / "scripts" / "54_section_draft_validator_v1_2.py"
REPRODUCTION_PATH = PHASE_DIR / "audits" / "df_01_reproduction_v1.json"
FIXTURE_RESULTS_PATH = PHASE_DIR / "fixtures" / "qualifier_semantics_fixture_results_v1.json"
AUDIT_PATH = PHASE_DIR / "audits" / "qualifier_validation_tightening_audit_v1.json"
MANIFEST_PATH = MANIFESTS / "sec_02_2_qualifier_validation_tightening_v1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_qualifier_validation_tightening_v1.md"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("qvt_validator_v1", VALIDATOR_V1)
V11 = _load("qvt_validator_v1_1", VALIDATOR_V1_1)
V12 = _load("qvt_validator_v1_2", VALIDATOR_V1_2)


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


# ================================================================ probes
#
# Validator inputs, not draft prose. They exist to answer "does the rule separate realisation from
# reproduction", they are recorded as phase evidence, and nothing authorises reusing them as text.

C009_PROBES = {
    # The scope-limiting meaning, said. Both constructions, in one sentence.
    "C009_scope_unit":
        "Bu ilk katman kalınlığı kil zonlu tabakalara özgüdür; genel bir ilk püskürtme beton "
        "katmanı kalınlığı değildir.",
    # Exclusivity alone. The any_of match must accept this, or the rule is a false-reject machine.
    "C009_exclusivity_only":
        "Bu kalınlık kil zonlu tabakalar üzerine uygulamaya özgüdür.",
    # Non-generality alone, phrased without 'özgü'.
    "C009_non_generality_only":
        "Bu kalınlık genel bir ilk katman kalınlığı değildir.",
    # DF-01's shape: claim vocabulary, no scope-limiting meaning. Stage E scores this preserved.
    "C009_lexical_padding":
        "Kil zonlu tabakalarda ilk püskürtme beton katmanı kalınlığı 100-150 mm olarak "
        "uygulanır.",
    # The wrong scope, actively asserted.
    "C009_generalised":
        "Genel olarak ilk püskürtme beton katmanı 100-150 mm kalınlığındadır.",
}

# The attempt-#1 shape DSC-C002-001 was built for. Copied from the analysis-v2 regression RC-A5 so
# the two suites cannot drift apart.
C002_FORBIDDEN_ATTRIBUTION = (
    "Tablo-351-5'e göre püskürtme betonun basınç dayanım sınıfı C25/30'dur; "
    "28 günlük karot numunelerinde kabul kriteri sağlanır.")

BUNDLE = V12.load_bundle()
ENTRIES = V12.load_qualifier_semantics()
CONSTRAINTS = V12.load_semantic_constraints()
ANALYSIS_V2 = json.loads(FAILURE_ANALYSIS_V2.read_text(encoding="utf-8"))
C002_PROBES = {
    "C002_identity_unit":
        "Tablo-351-5, C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerinde kalite "
        "kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul kriteridir.",
    "C002_single_unit_combined":
        "Tablo-351-5, C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerinde kabul "
        "kriteridir: bireysel minimum dayanım 22,5 MPa ve üç adet numuneden oluşan grubun "
        "ortalama minimum dayanımı 25,5 MPa'dır.",
}


def attempt_2_ir():
    raw = json.loads(RAW_ATTEMPT_2.read_text(encoding="utf-8"))
    return V12.parse_draft_ir(json.loads(raw["raw_text"]))


# ================================================================ 1. DF-01 reproduction

def _qualifier_anchor_score(claim: dict, paragraph_text: str) -> dict[str, Any]:
    """Stage E's own arithmetic, recomputed here so the reproduction shows its working."""
    qualifier = (claim.get("qualifiers") or [""])[0]
    anchors = V1.content_tokens(qualifier, BUNDLE.function_lexicon)
    present = set(V1.tokens(paragraph_text))
    hits = [a for a in anchors if any(V1.prefix_agreement(a, h) for h in present)]
    return {"qualifier": qualifier, "anchors": anchors, "anchors_present": hits,
            "hits": len(hits), "total": len(anchors),
            "stage_e_preserved": len(hits) * 2 >= len(anchors)}


def reproduce_df_01() -> dict[str, Any]:
    ir = attempt_2_ir()
    paragraphs = V12.paragraph_texts(ir)
    units = {u.unit_id: u for u in ir.units}
    rejection = json.loads(REJECTED_2.read_text(encoding="utf-8"))
    rejected_ids = {u["unit_id"] for u in rejection["rejected_units"]}

    steps = []
    findings: dict[str, Any] = {}
    for name, claim_id, unit_id in (("control", CONTROL_CLAIM, CONTROL_UNIT),
                                    ("target", TARGET_CLAIM, TARGET_UNIT)):
        claim = BUNDLE.allowlist[claim_id]
        unit = units[unit_id]
        paragraph = paragraphs[unit.paragraph_id]
        score = _qualifier_anchor_score(claim, paragraph)
        v11_failures = sorted({(f.code, f.stage) for f in V11.validate_unit(
            unit, paragraph, BUNDLE, section_language=ir.language, constraints=CONSTRAINTS)})
        # Semantic realisation, judged by the registered constructions where one exists. For the
        # control claim the question is already settled by v1.1's own rejection.
        entry = next((e for e in ENTRIES if e["claim_id"] == claim_id), None)
        realised = V12.realised_constructions(entry, paragraph) if entry else None
        findings[name] = {
            "claim_id": claim_id, "unit_id": unit_id,
            "unit_is_verbatim_canonical": unit.text == claim["canonical_claim"],
            "canonical_claim": claim["canonical_claim"],
            "unit_text": unit.text,
            "paragraph_text": paragraph,
            "stage_e_anchor_score": score,
            "v1_1_failures": [{"code": c, "stage": s} for c, s in v11_failures],
            "v1_1_rejected": unit_id in rejected_ids,
            "semantic_realisation": ([c["construction_id"] for c in realised]
                                     if realised is not None else None),
            "qualifier_meaning_stated": bool(realised) if realised is not None else False,
        }

    control, target = findings["control"], findings["target"]

    steps.append({
        "step": 1,
        "assertion": f"{CONTROL_CLAIM}'s qualifier is actually missing and already rejected",
        "holds": (not control["qualifier_meaning_stated"]
                  and control["v1_1_rejected"]
                  and ("QUALIFIER_DROPPED", "E_conditions") in
                  {(f["code"], f["stage"]) for f in control["v1_1_failures"]}),
        "evidence": (f"stage E scored {control['stage_e_anchor_score']['hits']}/"
                     f"{control['stage_e_anchor_score']['total']} anchors, below half; "
                     f"{CONTROL_UNIT} is in attempt #2's rejected units"),
    })
    steps.append({
        "step": 2,
        "assertion": f"{TARGET_CLAIM}'s qualifier is actually missing",
        "holds": (target["unit_is_verbatim_canonical"]
                  and not target["qualifier_meaning_stated"]),
        "evidence": (f"{TARGET_UNIT} is byte-identical to canonical_claim, and no clause in its "
                     f"paragraph realises either registered construction"),
    })
    steps.append({
        "step": 3,
        "assertion": "existing stage E nevertheless scores it preserved",
        "holds": (target["stage_e_anchor_score"]["stage_e_preserved"]
                  and not target["v1_1_failures"]),
        "evidence": (f"stage E scored {target['stage_e_anchor_score']['hits']}/"
                     f"{target['stage_e_anchor_score']['total']} anchors, at or above half; "
                     f"validator v1.1 returns no failure for {TARGET_UNIT}"),
    })
    # The decisive test, and the strictest available form of it: score the qualifier against the
    # canonical sentence *on its own*. If that alone clears the half-anchor threshold, the pass is
    # manufactured by the claim's own vocabulary and nothing the prose said can have earned it.
    canonical_only = _qualifier_anchor_score(BUNDLE.allowlist[TARGET_CLAIM],
                                             target["canonical_claim"])
    canonical_tokens = set(V1.tokens(target["canonical_claim"]))
    from_canonical = sorted(a for a in target["stage_e_anchor_score"]["anchors_present"]
                            if any(V1.prefix_agreement(a, t) for t in canonical_tokens))
    steps.append({
        "step": 4,
        "assertion": "the apparent pass comes from anchor overlap with canonical claim vocabulary",
        "holds": canonical_only["stage_e_preserved"],
        "evidence": (f"the canonical sentence alone scores {canonical_only['hits']}/"
                     f"{canonical_only['total']} anchors — {canonical_only['anchors_present']} — "
                     f"which already clears the half-anchor threshold, so copying it is by itself "
                     f"sufficient to be scored preserved. The only anchor the copy misses, "
                     f"'özgüdür', is the one word carrying the scope limitation"),
        "canonical_claim_alone_score": canonical_only,
        "anchors_from_canonical": from_canonical,
        "anchors_from_neighbouring_units": sorted(
            set(target["stage_e_anchor_score"]["anchors_present"]) - set(from_canonical)),
    })

    return {
        "finding_id": FINDING_ID,
        "finding": ("Stage E scores a qualifier preserved when at least half of its lexical "
                    "anchors reach the paragraph. A qualifier phrased in its own claim's "
                    "vocabulary is therefore scored preserved by a verbatim copy of the canonical "
                    "sentence, which states the qualifier's meaning nowhere."),
        "reproduced": all(s["holds"] for s in steps),
        "steps": steps,
        "control": control,
        "target": target,
        "measured_vs_realised": {
            "measured_qualifier_preservation": "1/2",
            "realised_qualifier_preservation": "0/2",
            "agrees_with_analysis_v2": any(
                d["id"] == FINDING_ID for d in ANALYSIS_V2["deferred_findings"]),
        },
        "root_cause": ("lexical anchor overlap is used as a proxy for semantic realisation; the "
                       "proxy is vacuous whenever the qualifier's anchors are drawn from the "
                       "claim it qualifies"),
        "frozen_regression_case": "QV-A",
    }


# ================================================================ 2. fixtures

def build_fixtures() -> list[dict]:
    ir = attempt_2_ir()
    paragraphs = V12.paragraph_texts(ir)
    units = {u.unit_id: u for u in ir.units}
    c009 = BUNDLE.allowlist[TARGET_CLAIM]
    canonical = c009["canonical_claim"]
    c009_keys = list(c009["source_keys"])
    c002_keys = list(BUNDLE.allowlist[CONTROL_CLAIM]["source_keys"])
    attempt_2_paragraph = paragraphs[units[TARGET_UNIT].paragraph_id]

    def c009_case(case_id: str, category: str, text: str, paragraph: str, valid: bool,
                  codes: list[str] | None = None, scope: str = "qualifier",
                  unit_id: str = TARGET_UNIT) -> dict:
        return {"case_id": case_id, "category": category, "fixture_scope": scope,
                "unit_id": unit_id, "unit_type": "PARAGRAPH_SENTENCE", "material": True,
                "text": text, "paragraph_text": paragraph, "claim_ids": [TARGET_CLAIM],
                "source_keys": c009_keys, "relationship_type": "INDEPENDENT",
                "citation_intents": [{"claim_id": TARGET_CLAIM, "source_keys": c009_keys}],
                "expected_valid": valid, "expected_failure_codes": codes or []}

    def c002_case(case_id: str, category: str, text: str, paragraph: str, valid: bool,
                  codes: list[str] | None = None, unit_id: str = CONTROL_UNIT) -> dict:
        return {"case_id": case_id, "category": category, "fixture_scope": "draft",
                "unit_id": unit_id, "unit_type": "PARAGRAPH_SENTENCE", "material": True,
                "text": text, "paragraph_text": paragraph, "claim_ids": [CONTROL_CLAIM],
                "source_keys": c002_keys, "relationship_type": "INDEPENDENT",
                "citation_intents": [{"claim_id": CONTROL_CLAIM, "source_keys": c002_keys}],
                "expected_valid": valid, "expected_failure_codes": codes or []}

    c001 = BUNDLE.allowlist["SEC-02-2-C-001"]["canonical_claim"]
    c002_canonical = BUNDLE.allowlist[CONTROL_CLAIM]["canonical_claim"]
    scope_unit = C009_PROBES["C009_scope_unit"]

    fixtures = [
        # A. the frozen DF-01 regression case: attempt #2's actual C-009 wording and paragraph.
        c009_case("QV-A", "df_01_historical_false_pass", units[TARGET_UNIT].text,
                  attempt_2_paragraph, False, ["QUALIFIER_DROPPED"]),
        # B. the scope-limiting meaning actually stated. Full pipeline, both units.
        c009_case("QV-B1", "meaning_realised_canonical_unit", canonical,
                  f"{canonical} {scope_unit}", True, scope="draft"),
        c009_case("QV-B2", "meaning_realised_scope_unit", scope_unit,
                  f"{canonical} {scope_unit}", True, scope="draft",
                  unit_id="U-D-P01-S04"),
        c009_case("QV-B3", "meaning_realised_exclusivity_only",
                  C009_PROBES["C009_exclusivity_only"],
                  f"{canonical} {C009_PROBES['C009_exclusivity_only']}", True,
                  unit_id="U-D-P01-S04"),
        c009_case("QV-B4", "meaning_realised_non_generality_only",
                  C009_PROBES["C009_non_generality_only"],
                  f"{canonical} {C009_PROBES['C009_non_generality_only']}", True,
                  unit_id="U-D-P01-S04"),
        # C. the canonical sentence alone. Reproduction, not realisation.
        c009_case("QV-C", "canonical_alone", canonical, canonical, False,
                  ["QUALIFIER_DROPPED"]),
        # D. lexical padding out of claim vocabulary, with no scope-limiting meaning.
        c009_case("QV-D1", "lexical_padding", canonical,
                  f"{canonical} {C009_PROBES['C009_lexical_padding']}", False,
                  ["QUALIFIER_DROPPED"]),
        c009_case("QV-D2", "generalised_scope_asserted", C009_PROBES["C009_generalised"],
                  f"{canonical} {C009_PROBES['C009_generalised']}", False,
                  ["QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH"], unit_id="U-D-P01-S04"),
        # E. the C-002 boundary DSC-C002-001 owns. Untouched by stage L, still rejecting.
        c002_case("QV-E1", "c002_historical_bad_form", c002_canonical,
                  f"{c001} {c002_canonical}", False, ["QUALIFIER_DROPPED"]),
        c002_case("QV-E2", "c002_forbidden_attribution", C002_FORBIDDEN_ATTRIBUTION,
                  f"{c001} {C002_FORBIDDEN_ATTRIBUTION}", False, ["SEMANTIC_SCOPE_MISMATCH"]),
        # F. the corrected C-002 forms analysis v2 proved compliant. Still compliant.
        c002_case("QV-F1", "c002_two_bound_units_identity", C002_PROBES["C002_identity_unit"],
                  f"{c001} {C002_PROBES['C002_identity_unit']} {c002_canonical}", True),
        c002_case("QV-F2", "c002_two_bound_units_numeric", c002_canonical,
                  f"{c001} {C002_PROBES['C002_identity_unit']} {c002_canonical}", True,
                  unit_id="U-A-P01-S03"),
        c002_case("QV-F3", "c002_single_unit_combined", C002_PROBES["C002_single_unit_combined"],
                  f"{c001} {C002_PROBES['C002_single_unit_combined']}", True),
    ]
    # H. every other material unit attempt #2 accepted, scored again under v1.2. None declares a
    # registered claim, so none may acquire a new failure.
    rejected = {u["unit_id"] for u in
                json.loads(REJECTED_2.read_text(encoding="utf-8"))["rejected_units"]}
    for unit in ir.units:
        if not unit.material or unit.unit_id in rejected or unit.unit_id == TARGET_UNIT:
            continue
        fixtures.append({
            "case_id": f"QV-H-{unit.unit_id}", "category": "unrelated_unit_not_newly_rejected",
            "fixture_scope": "draft", "unit_id": unit.unit_id, "unit_type": unit.unit_type,
            "material": True, "text": unit.text,
            "paragraph_text": paragraphs[unit.paragraph_id],
            "claim_ids": list(unit.claim_ids), "source_keys": list(unit.source_keys),
            "relationship_type": unit.relationship_type,
            "citation_intents": list(unit.citation_intents),
            "expected_valid": True, "expected_failure_codes": []})
    return fixtures


# ================================================================ 3. inherited behaviour

def inherited_behaviour() -> dict[str, Any]:
    """Does v1.2 decide everything v1.1 decided, identically, apart from the intended tightening?"""
    ir_11, ir_12 = attempt_2_ir(), attempt_2_ir()
    r11 = V11.validate_draft(ir_11, BUNDLE)
    r12 = V12.validate_draft(ir_12, BUNDLE)
    rejected_11, rejected_12 = set(r11.rejected_unit_ids), set(r12.rejected_unit_ids)
    newly_rejected = sorted(rejected_12 - rejected_11)
    return {
        "attempt_2_rejected_under_v1_1": sorted(rejected_11),
        "attempt_2_rejected_under_v1_2": sorted(rejected_12),
        "newly_rejected": newly_rejected,
        "newly_accepted": sorted(rejected_11 - rejected_12),
        "newly_rejected_is_exactly_df_01": newly_rejected == [TARGET_UNIT],
        "no_unit_newly_accepted": rejected_11 <= rejected_12,
        "inherited_codes_unchanged": (
            list(V11.REJECTION_CODES) == list(V12.REJECTION_CODES[:len(V11.REJECTION_CODES)])),
        "new_rejection_codes": list(V12.NEW_REJECTION_CODES),
        "inherited_stages_unchanged": (
            [s for s in V12.STAGES if s != "L_qualifier_semantics"] == list(V11.STAGES)),
    }


def prior_versions_unchanged() -> dict[str, Any]:
    """v1 and v1.1 must be byte-identical to what analysis v2 hashed."""
    recorded = ANALYSIS_V2["frozen_inputs"]["sha256"]
    rows = {}
    for name, path in (("draft_validator_v1", VALIDATOR_V1),
                       ("draft_validator_v1_1", VALIDATOR_V1_1)):
        current = sha_file(path)
        rows[name] = {"sha256": current, "recorded_in_analysis_v2": recorded.get(name),
                      "unchanged": current == recorded.get(name)}
    return {"rows": rows, "all_unchanged": all(r["unchanged"] for r in rows.values())}


# ================================================================ 4. driver

def build_audit() -> dict[str, Any]:
    reproduction = reproduce_df_01()
    fixtures = build_fixtures()
    results = V12.run_fixtures(fixtures, BUNDLE, constraints=CONSTRAINTS,
                               qualifier_semantics=ENTRIES)
    integrity = V12.registry_integrity(BUNDLE, ENTRIES)
    inherited = inherited_behaviour()
    prior = prior_versions_unchanged()
    before_after = {
        "wording": reproduction["target"]["unit_text"],
        "before_v1_2": ("PASS - stage E scored "
                        f"{reproduction['target']['stage_e_anchor_score']['hits']}/"
                        f"{reproduction['target']['stage_e_anchor_score']['total']} anchors "
                        "preserved; validator v1.1 returned no failure"),
        "after_v1_2": "REJECT - QUALIFIER_DROPPED at stage L_qualifier_semantics",
        "false_pass_eliminated": (
            not reproduction["target"]["v1_1_failures"]
            and TARGET_UNIT in inherited["attempt_2_rejected_under_v1_2"]),
    }
    gate = {
        "df_01_reproduced": reproduction["reproduced"],
        "false_pass_eliminated": before_after["false_pass_eliminated"],
        "c009_semantic_qualifier_enforced": integrity["consistent"] and len(ENTRIES) == 1,
        "c002_behaviour_preserved": all(
            r["outcome"] == "PASS" for r in results["rows"]
            if str(r["case_id"]).startswith(("QV-E", "QV-F"))),
        "no_validator_weakened": (inherited["no_unit_newly_accepted"]
                                  and inherited["inherited_codes_unchanged"]
                                  and inherited["inherited_stages_unchanged"]),
        "prior_validator_versions_unchanged": prior["all_unchanged"],
        "all_targeted_tests_pass": results["all_pass"],
        "false_accepts": len(results["false_accepts"]),
        "false_rejects": len(results["false_rejects"]),
        "registry_integrity": integrity["consistent"],
    }
    gate["status"] = ("CLOSED / GO" if (all(v is True for k, v in gate.items()
                                            if isinstance(v, bool))
                                       and gate["false_accepts"] == 0
                                       and gate["false_rejects"] == 0) else "NO-GO")
    return {
        "version": VERSION,
        "phase": PHASE,
        "section_id": SECTION_ID,
        "analysed_at": datetime.now(timezone.utc).isoformat(),
        "df_01": reproduction,
        "remedy": {
            "design": ("registered qualifier semantics - explicit, deterministic required-meaning "
                       "constructions per registered qualifier, following DSC-C002-001"),
            "rejected_alternative": ("raising the half-anchor threshold to a higher percentage; "
                                     "it is the same lexical heuristic with a different constant, "
                                     "would create false rejects on faithful prose that renders "
                                     "the meaning in other words, and would still pass a verbatim "
                                     "copy whose anchor overlap happens to be total"),
            "validator_version": V12.VALIDATOR_VERSION,
            "contract_version": V12.VALIDATION_CONTRACT_VERSION,
            "registry_version": json.loads(
                QUALIFIER_SEMANTICS.read_text(encoding="utf-8"))["version"],
            "new_stage": "L_qualifier_semantics",
            "failure_codes_used": ["QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH"],
            "new_failure_codes_invented": list(V12.NEW_REJECTION_CODES),
            "registered_constraint_ids": [e["constraint_id"] for e in ENTRIES],
        },
        "registry_integrity": integrity,
        "fixtures": {"total": results["total"], "passed": results["passed"],
                     "positive": results["positive"], "negative": results["negative"],
                     "false_accepts": results["false_accepts"],
                     "false_rejects": results["false_rejects"],
                     "code_mismatches": results["code_mismatches"],
                     "all_pass": results["all_pass"]},
        "inherited_behaviour": inherited,
        "prior_validator_versions": prior,
        "c009_historical_wording": before_after,
        "gate": gate,
        "frozen_inputs": {
            "sha256": {name: sha_file(path) for name, path in FROZEN_INPUTS.items()},
            "all_present": all(path.exists() for path in FROZEN_INPUTS.values()),
            "modified_by_this_phase": [],
        },
        "generation_attempts_in_this_phase": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "validators_weakened": [],
        "attempt_3_authorised_here": False,
        "prose_rendered": False,
    }, results


def write_report(audit: dict, results: dict) -> None:
    df = audit["df_01"]
    target, control = df["target"], df["control"]
    add = (lines := []).append
    add("# SEC-02-2 Qualifier Preservation Validation Tightening v1")
    add("")
    add(f"**{audit['gate']['status']}.** Closes {FINDING_ID}. Validator-tightening phase: "
        "0 generation attempts, 0 retrieval calls, 0 Qdrant writes, 0 corpus reads, "
        "0 validators weakened, no prose rendered, attempt #3 not authorised here.")
    add("")
    add("## DF-01, reproduced")
    add("")
    add(df["finding"])
    add("")
    add("| # | Assertion | Holds |")
    add("|---|---|---|")
    for step in df["steps"]:
        add(f"| {step['step']} | {step['assertion']} | {'yes' if step['holds'] else 'NO'} |")
    add("")
    step4 = df["steps"][3]
    alone = step4["canonical_claim_alone_score"]
    add(f"`{TARGET_UNIT}` is byte-identical to `{TARGET_CLAIM}`'s canonical sentence: "
        f"{str(target['unit_is_verbatim_canonical']).lower()}. Stage E scored "
        f"{target['stage_e_anchor_score']['hits']}/{target['stage_e_anchor_score']['total']} "
        f"anchors present — {target['stage_e_anchor_score']['anchors_present']} — of which "
        f"{step4['anchors_from_canonical']} are tokens of the sentence the writer copied and "
        f"{step4['anchors_from_neighbouring_units']} came from neighbouring units. The copied "
        f"sentence alone already scores {alone['hits']}/{alone['total']}, clearing the threshold "
        "on its own, so nothing the prose said was needed to earn the pass. The one anchor the "
        "copy misses, `özgüdür`, is the single word carrying the scope limitation. The control "
        f"claim `{CONTROL_CLAIM}` scored {control['stage_e_anchor_score']['hits']}/"
        f"{control['stage_e_anchor_score']['total']} and was correctly rejected.")
    add("")
    add(f"**Root cause.** {df['root_cause']}.")
    add("")
    add("## The remedy, and the one that was rejected")
    add("")
    add(f"Rejected: {audit['remedy']['rejected_alternative']}.")
    add("")
    add(f"Adopted: {audit['remedy']['design']}. Stage `L_qualifier_semantics` scores a registered "
        "qualifier by whether some clause satisfies a declared construction — an operator and the "
        "thing it is applied to, in the same clause. Clause scope is what separates meaning from "
        "padding: a paragraph can contain `özgü` and it can contain `kil` without ever having "
        "said one about the other.")
    add("")
    add("Two registry integrity properties are enforced fail-closed before any verdict: the "
        "registered qualifier text must equal the frozen allowlist qualifier byte for byte, and "
        "the claim's own canonical sentence must **not** satisfy the constructions. The second is "
        "DF-01 restated as a general property — an entry a verbatim copy would satisfy cannot "
        "tell realisation from reproduction, and is refused.")
    add("")
    add(f"No new failure code. `QUALIFIER_DROPPED` for absent required meaning; "
        "`SEMANTIC_SCOPE_MISMATCH` only where prose actively states the generalised scope.")
    add("")
    add("## SEC-02-2-C-009's historical wording")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| Before | {audit['c009_historical_wording']['before_v1_2']} |")
    add(f"| After | {audit['c009_historical_wording']['after_v1_2']} |")
    add("")
    add("## Fixtures")
    add("")
    add("| Case | Category | Expected | Outcome | Codes |")
    add("|---|---|---|---|---|")
    for row in results["rows"]:
        expected = "valid" if row["expected_valid"] else "reject"
        codes = ", ".join(row["actual_failure_codes"]) or "—"
        add(f"| {row['case_id']} | {row['category']} | {expected} | {row['outcome']} | {codes} |")
    add("")
    add(f"{results['passed']}/{results['total']} pass. False accepts: "
        f"{len(results['false_accepts'])}. False rejects: {len(results['false_rejects'])}.")
    add("")
    add("## Inherited behaviour")
    add("")
    inherited = audit["inherited_behaviour"]
    add("| | |")
    add("|---|---|")
    add(f"| Attempt #2 rejected under v1.1 | {inherited['attempt_2_rejected_under_v1_1']} |")
    add(f"| Attempt #2 rejected under v1.2 | {inherited['attempt_2_rejected_under_v1_2']} |")
    add(f"| Newly rejected | {inherited['newly_rejected']} |")
    add(f"| Newly accepted | {inherited['newly_accepted'] or 'none'} |")
    add(f"| Inherited codes unchanged | {inherited['inherited_codes_unchanged']} |")
    add(f"| New codes invented | {inherited['new_rejection_codes'] or 'none'} |")
    add("")
    for name, row in audit["prior_validator_versions"]["rows"].items():
        add(f"- `{name}` sha256 `{row['sha256'][:16]}…` — unchanged: {row['unchanged']}")
    add("")
    add("## Gate")
    add("")
    add("| Condition | Result |")
    add("|---|---|")
    for key, value in audit["gate"].items():
        if key == "status":
            continue
        add(f"| {key.replace('_', ' ')} | {value} |")
    add("")
    add(f"**{audit['gate']['status']}**")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    audit, results = build_audit()
    write_json(REPRODUCTION_PATH, audit["df_01"])
    write_json(FIXTURE_RESULTS_PATH, {"version": VERSION, "section_id": SECTION_ID,
                                      "validator_version": V12.VALIDATOR_VERSION, **results})
    write_json(AUDIT_PATH, audit)
    write_json(MANIFEST_PATH, {
        "version": VERSION,
        "section_id": SECTION_ID,
        "phase": PHASE,
        "generated_at": audit["analysed_at"],
        "status": "closed_go" if audit["gate"]["status"] == "CLOSED / GO" else "no_go",
        "final_decision": f"{PHASE} — {audit['gate']['status']}",
        "finding_closed": FINDING_ID,
        "generation_attempts": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "validators_weakened": [],
        "attempt_3_authorised_here": False,
        "validator_version": V12.VALIDATOR_VERSION,
        "contract_version": V12.VALIDATION_CONTRACT_VERSION,
        "registry_version": audit["remedy"]["registry_version"],
        "frozen_inputs_sha256": audit["frozen_inputs"]["sha256"],
        "prior_validator_versions_unchanged": audit["prior_validator_versions"]["all_unchanged"],
        "artifacts": {
            "qualifier_semantics_registry": str(QUALIFIER_SEMANTICS.relative_to(ROOT)),
            "validation_contract_v1_2": str(VALIDATION_CONTRACT_V1_2.relative_to(ROOT)),
            "validator": "scripts/54_section_draft_validator_v1_2.py",
            "phase_controller": "scripts/55_sec_02_2_qualifier_validation_tightening_v1.py",
            "df_01_reproduction": str(REPRODUCTION_PATH.relative_to(ROOT)),
            "fixture_results": str(FIXTURE_RESULTS_PATH.relative_to(ROOT)),
            "audit": str(AUDIT_PATH.relative_to(ROOT)),
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "tests": "tests/test_section_draft_validator_v1_2.py",
        },
        "fixtures": audit["fixtures"],
        "gate": audit["gate"],
        "next_phase": "SEC-02-2 DRAFT PLAN V1.2 + ATTEMPT #3 AUTHORISATION",
    })
    write_report(audit, results)
    print(f"{PHASE}: {audit['gate']['status']}")
    print(f"  DF-01 reproduced: {audit['df_01']['reproduced']}")
    print(f"  fixtures: {results['passed']}/{results['total']} "
          f"(false accepts {len(results['false_accepts'])}, "
          f"false rejects {len(results['false_rejects'])})")
    print(f"  newly rejected: {audit['inherited_behaviour']['newly_rejected']}")
    return 0 if audit["gate"]["status"] == "CLOSED / GO" else 1


if __name__ == "__main__":
    sys.exit(main())
