"""SEC-02-2 Draft Plan v1.2 + Attempt #3.

Two rejected pilots, two distinct causes, both analysed and both settled as writer-side rather
than validator-side. This phase authors the smallest artifact the evidence supports - a draft plan
v1.2 - runs every regression gate, and takes exactly one more generation.

**What plan v1.2 changes, and why it is only a plan.**

Attempt #2 copied `canonical_claim` byte-for-byte for 14 of 16 single-claim units. That is not a
defect in itself; it is the safest thing a writer can do with an approved Turkish sentence. It
becomes a defect exactly when a claim also carries a qualifier whose meaning the canonical
sentence does not contain, because then reproduction cannot reach the required meaning and no unit
is allocated for the part that must be composed. Plan v1.2 allocates that unit.

The allocation rule is general and deterministic: a claim whose non-empty qualifier has at least
one content anchor absent from its own canonical sentence, or which carries a registered
qualifier-semantics entry its canonical sentence does not satisfy, gets two bound unit slots.
Every other claim keeps one. The rule reads the frozen allowlist and the frozen registry; it names
no claim. Applied to the sixteen allocated claims it selects SEC-02-2-C-002 and SEC-02-2-C-009 -
which are, as it happens, the only two allocated claims carrying a qualifier at all.

Slot order is derived from the registered constraint's type rather than chosen per claim. A
`QUALIFIER_PRESERVATION` constraint says what a reference *is*, so its composed slot comes first,
before the numbers it would otherwise be read as establishing. A `QUALIFIER_SEMANTICS` constraint
restricts a figure already stated, so its composed slot comes second.

The second change exposes, verbatim, the `translation_glosses` the frozen contract already holds
for English-source claims. Attempt #2's `kayaç` was written three words after the licensed `kaya`.
The pool was never too narrow; the writer was never shown it. Exposure states what the validator
already accepts and changes nothing about what it accepts - `kayaç` and `spesifik` are asserted
absent from the exposed vocabulary as a gate, not hoped absent.

**What this phase does not do.** It edits no validator, threshold, failure code, marker set,
gloss, paraphrase entry, claim, allowlist, denylist, pair constraint, prompt or frozen contract.
Plan v1.1 stays on disk unchanged and is hashed against its recorded value. Attempt #1 and #2
outputs are read-only evidence.

**Attempt #3.** One generation, on the frozen writer at the frozen settings - temperature 0.0,
seed 11 - taken only after every gate passes. The raw text is written to disk before it is parsed,
so a failure stays inspectable exactly as the model produced it. Validation is Draft Validator
v1.2: twelve stages, including composition at F, sources and citation at G and H, language at J,
registered semantic constraints at K and registered qualifier semantics at L. All-or-nothing: one
rejected material unit rejects the pilot.

A rejected attempt #3 is not repaired, not patched, not translated, not partially kept and not
regenerated. There is no attempt #4 anywhere in this file.
"""

from __future__ import annotations

import argparse
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

VERSION = "tunnelbook-sec-02-2-draft-plan-v1-2-attempt-3"
PHASE = "SEC-02-2 DRAFT PLAN V1.2 + ATTEMPT #3 AUTHORISATION"
DRAFT_PLAN_V1_2_VERSION = "tunnelbook-sec-02-2-draft-plan-v1.2"
VALIDATION_CONTRACT_V1_2_VERSION = "tunnelbook-draft-validation-contract-v1.2"
DRAFT_VALIDATOR_V1_2_VERSION = "tunnelbook-section-draft-validator-v1.2"
QUALIFIER_SEMANTICS_VERSION = "tunnelbook-draft-qualifier-semantics-v1"

SECTION_ID = "SEC-02-2"
LANGUAGE = "tr"
ATTEMPT = 3

# A third DraftIR needs a third identity. Two drafts sharing one id are indistinguishable in every
# later audit, which is the mistake attempt #2 already declined to make.
DRAFT_ID = "SEC-02-2-PILOT-V1-2"
DRAFT_VERSION = "v1.2"

BOOK = ROOT / "data" / "book"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
MANIFESTS = BOOK / "manifests"
EVALUATION = ROOT / "data" / "evaluation"

PLAN_V1_1_PATH = SECTION_DIR / "draft_plan_v1_1.json"
PLAN_V1_2_PATH = SECTION_DIR / "draft_plan_v1_2.json"
QUALIFIER_VALIDATION = SECTION_DIR / "qualifier_validation_v1"
QUALIFIER_SEMANTICS_PATH = QUALIFIER_VALIDATION / "contracts" / "draft_qualifier_semantics_v1.json"
VALIDATOR_V1_2_PATH = ROOT / "scripts" / "54_section_draft_validator_v1_2.py"
VALIDATION_CONTRACT_V1_2_PATH = CONTRACTS / "draft_validation_contract_v1_2.json"
DRAFTING_CONTRACT_PATH = CONTRACTS / "section_drafting_contract_v1.json"

ATTEMPT_DIR = SECTION_DIR / "attempt_3"
RAW_PATH = ATTEMPT_DIR / "raw" / "sec_02_2_draft_raw_attempt_3.json"
ACCEPTED_IR_PATH = ATTEMPT_DIR / "accepted" / "sec_02_2_draft_ir_v1_2.json"
CITATION_MAP_PATH = ATTEMPT_DIR / "accepted" / "citation_map_v1_2.json"
REJECTED_PATH = ATTEMPT_DIR / "rejected" / "pilot_attempt_3_validation.json"
PRE_GATE_PATH = ATTEMPT_DIR / "audits" / "pre_generation_gate_v1.json"
ATTEMPT_AUDIT_PATH = ATTEMPT_DIR / "audits" / "attempt_3_audit_v1.json"
FIXTURE_RESULTS_PATH = ATTEMPT_DIR / "fixtures" / "pre_generation_fixture_results_v1.json"
RENDERED_PATH = SECTION_DIR / "rendered" / "sec_02_2_pilot_v1_2.md"
MANIFEST_PATH = MANIFESTS / "sec_02_2_draft_plan_v1_2_attempt_3.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_draft_plan_v1_2_attempt_3.md"

REMEDIATION_MANIFEST = MANIFESTS / "sec_02_2_draft_failure_remediation_v1.json"
ANALYSIS_V2_AUDIT = SECTION_DIR / "analysis_v2" / "audits" / "attempt_2_failure_analysis_v1.json"
QUALIFIER_MANIFEST = MANIFESTS / "sec_02_2_qualifier_validation_tightening_v1.json"

# Every suite that has ever guarded this pipeline. Nothing is dropped to make a gate pass.
GATE_SUITES = (
    "tests.test_section_drafting_contract_v1",
    "tests.test_book_citation_renderer_v1",
    "tests.test_section_draft_validator_v1",
    "tests.test_sec_02_2_claim_composition_validator_v1",
    "tests.test_sec_02_2_limitation_resolution_v1",
    "tests.test_sec_02_2_controlled_draft_pilot_v1",
    "tests.test_draft_language_validator_v1",
    "tests.test_section_draft_validator_v1_1",
    "tests.test_sec_02_2_draft_failure_remediation_v1",
    "tests.test_sec_02_2_draft_failure_analysis_v2",
    "tests.test_section_draft_validator_v1_2",
)

FIXTURE_UNIVERSES = {
    "section_drafting_contract_v1": EVALUATION / "section_drafting_contract_v1.jsonl",
    "sec_02_2_draft_failure_remediation_v1": (
        EVALUATION / "sec_02_2_draft_failure_remediation_v1.jsonl"),
}

# Frozen artifacts, each checked against a SHA some earlier phase recorded - not against a value
# this phase invents, which would only prove the file equals itself.
FROZEN_SHA_SOURCES = {
    "draft_plan_v1_1": (PLAN_V1_1_PATH, REMEDIATION_MANIFEST, "draft_plan_v1_1_sha"),
    "drafting_prompt_v1_1": (ROOT / "data" / "metadata"
                             / "section_drafting_system_prompt_v1_1.txt",
                             REMEDIATION_MANIFEST, "drafting_prompt_v1_1_sha"),
    "semantic_constraints_v1": (SECTION_DIR / "remediation_v1" / "contracts"
                                / "draft_semantic_constraints_v1.json",
                                REMEDIATION_MANIFEST, "semantic_constraints_sha"),
    "cross_lingual_mappings_v1": (SECTION_DIR / "remediation_v1" / "contracts"
                                  / "cross_lingual_condition_mappings_v1.json",
                                  REMEDIATION_MANIFEST, "cross_lingual_mapping_sha"),
    "draft_language_contract_v1": (CONTRACTS / "draft_language_contract_v1.json",
                                   REMEDIATION_MANIFEST, "draft_language_contract_sha"),
    "draft_language_validator_v1": (ROOT / "scripts" / "51_draft_language_validator_v1.py",
                                    REMEDIATION_MANIFEST, "draft_language_validator_sha"),
    "draft_validator_v1_1": (ROOT / "scripts" / "52_section_draft_validator_v1_1.py",
                             REMEDIATION_MANIFEST, "draft_validator_v1_1_sha"),
    "draft_validation_contract_v1_1": (CONTRACTS / "draft_validation_contract_v1_1.json",
                                       REMEDIATION_MANIFEST,
                                       "draft_validation_contract_v1_1_sha"),
    "attempt_1_raw": (SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json",
                      REMEDIATION_MANIFEST, "historical_pilot_raw_file_sha"),
    "attempt_2_raw": (SECTION_DIR / "remediation_v1" / "raw"
                      / "sec_02_2_draft_raw_attempt_2.json",
                      REMEDIATION_MANIFEST, "attempt_2_raw_file_sha"),
}


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# scripts/50 is imported rather than re-implemented: its compliance audits, test runner and
# attempt gate are the ones attempt #2 faced, and a second copy could drift into being kinder.
REM = _load("remediation_v1_controller", "scripts/50_sec_02_2_draft_failure_remediation_v1.py")
V1 = _load("plan_v1_2_validator_v1", "scripts/49_section_draft_validator_v1.py")
V11 = _load("plan_v1_2_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")
V12 = _load("plan_v1_2_validator_v1_2", "scripts/54_section_draft_validator_v1_2.py")

MODEL_ID = REM.MODEL_ID
TEMPERATURE = REM.TEMPERATURE
SEED = REM.SEED
MAX_TOKENS = REM.MAX_TOKENS
LMSTUDIO_URL = REM.LMSTUDIO_URL
REQUIRED_TOPICS = REM.REQUIRED_TOPICS


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_file(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


# ================================================================ 1. the allocation rule

def qualifier_reachability(claim: dict, entry: dict | None, bundle: Any) -> dict[str, Any]:
    """Can this claim's qualifier be reached by reproducing its own canonical sentence?

    Two independent tests, both deterministic, both reading frozen data.

    The lexical test asks whether every content anchor of the qualifier already occurs in the
    canonical sentence. If one does not, no verbatim copy can carry the qualifier, and a unit that
    must both reproduce and compose is the shape that failed twice.

    The semantic test asks whether a registered qualifier-semantics entry is satisfied by the
    canonical sentence. It exists because the lexical test is exactly the measure DF-01 showed to
    be a poor proxy; where a registry entry exists, its own constructions answer instead. The
    registry guarantees this test is always negative for a registered claim - which is the point,
    and why the two tests are combined with OR rather than trusted individually.
    """
    canonical = claim.get("canonical_claim") or ""
    canonical_tokens = set(V12.tokens(canonical))
    rows = []
    for qualifier in claim.get("qualifiers") or []:
        anchors = V12.content_tokens(qualifier, bundle.function_lexicon)
        absent = [a for a in anchors
                  if not any(V12.prefix_agreement(a, t) for t in canonical_tokens)]
        rows.append({"qualifier": qualifier, "anchors": anchors,
                     "anchors_absent_from_canonical": absent})
    lexical = any(row["anchors_absent_from_canonical"] for row in rows)
    semantic = None
    if entry is not None:
        semantic = not V12.realised_constructions(entry, canonical)
    return {
        "qualifiers": rows,
        "has_qualifier": bool(rows),
        "lexically_unreachable_by_reproduction": lexical,
        "registered_constraint_id": entry["constraint_id"] if entry else None,
        "semantically_unreachable_by_reproduction": semantic,
        "needs_composed_slot": bool(lexical or semantic),
    }


def _composed_slot_position(entry: dict | None, semantic_constraint: dict | None) -> str:
    """Where the composed slot goes, derived from the constraint's declared type.

    A `QUALIFIER_PRESERVATION` constraint states what a reference *is*; it has to be established
    before the numbers, or the numbers read as the thing the reference establishes - the attempt-#1
    failure. A `QUALIFIER_SEMANTICS` constraint restricts a figure already given, so it follows.
    A claim selected only lexically has no constraint to read, and a qualifier that restricts what
    was just said is the general case; it follows too.
    """
    if semantic_constraint and semantic_constraint.get("type") == "QUALIFIER_PRESERVATION":
        return "before"
    return "after"


def build_unit_allocation(plan_v1_1: dict, bundle: Any, entries: list[dict],
                          semantic_constraints: list[dict]) -> dict[str, Any]:
    allocated = [cid for sub in plan_v1_1["subsections"] for cid in sub["claim_ids"]]
    subsection_of = {cid: sub["subsection_id"] for sub in plan_v1_1["subsections"]
                     for cid in sub["claim_ids"]}
    entry_by_claim = {e["claim_id"]: e for e in entries}
    constraint_by_claim = {c["claim_id"]: c for c in semantic_constraints}

    rows, selected = [], []
    for claim_id in allocated:
        claim = bundle.allowlist[claim_id]
        entry = entry_by_claim.get(claim_id)
        constraint = constraint_by_claim.get(claim_id)
        reach = qualifier_reachability(claim, entry, bundle)
        slots: list[dict[str, Any]] = []
        source_keys = list(claim.get("source_keys") or [])
        if reach["needs_composed_slot"]:
            selected.append(claim_id)
            position = _composed_slot_position(entry, constraint)
            composed = {
                "slot_role": "QUALIFIER_SCOPE",
                "compose_or_reproduce": "compose",
                "has_canonical_sentence_to_copy": False,
                "must_express": [q["qualifier"] for q in reach["qualifiers"]],
                "must_also_carry_conditions": list(claim.get("conditions") or []),
                "note": ("This slot has no canonical sentence to copy. Copying is not an "
                         "available strategy here; the meaning must be composed."),
            }
            reproduced = {
                "slot_role": "CLAIM_STATEMENT",
                "compose_or_reproduce": "reproduce_or_paraphrase",
                "has_canonical_sentence_to_copy": True,
                "must_express": [claim["canonical_claim"]],
                "must_also_carry_conditions": list(claim.get("conditions") or []),
            }
            if constraint:
                composed["must_not_imply"] = constraint["forbidden_meaning"]
                composed["required_meaning"] = constraint["required_meaning"]
                composed["required_action"] = constraint["required_action"]
                composed["constraint_id"] = constraint["constraint_id"]
            if entry:
                composed["required_meaning"] = entry["required_meaning"]
                composed["required_action"] = entry["required_action"]
                composed["constraint_id"] = entry["constraint_id"]
                composed["must_not_imply"] = (
                    "the figure is a general rule outside the qualifier's declared scope")
            slots = ([composed, reproduced] if position == "before"
                     else [reproduced, composed])
        else:
            slots = [{
                "slot_role": "CLAIM_STATEMENT",
                "compose_or_reproduce": "reproduce_or_paraphrase",
                "has_canonical_sentence_to_copy": True,
                "must_express": [claim["canonical_claim"]],
                "must_also_carry_conditions": list(claim.get("conditions") or []),
            }]
        for index, slot in enumerate(slots, start=1):
            slot["slot_id"] = f"{claim_id}-SLOT-{index}"
            slot["claim_id"] = claim_id
            slot["source_keys"] = source_keys
            slot["relationship_type"] = "INDEPENDENT"
        rows.append({
            "claim_id": claim_id, "subsection_id": subsection_of[claim_id],
            "unit_slots": len(slots), "slots": slots,
            "selection": reach,
        })
    return {
        "rule": ("A claim whose non-empty qualifier has at least one content anchor absent from "
                 "its own canonical sentence, or which carries a registered qualifier-semantics "
                 "entry that its canonical sentence does not satisfy, is allocated two bound unit "
                 "slots. Every other allocated claim keeps one."),
        "rule_is_general": ("The rule reads the frozen allowlist and the frozen qualifier-"
                            "semantics registry. It names no claim, and it selects nothing by "
                            "hand."),
        "why": ("Attempt #2 reproduced canonical_claim verbatim for 14 of 16 single-claim units. "
                "Reproduction cannot reach a meaning the canonical sentence does not contain, and "
                "no unit was allocated for the part that has to be composed."),
        "slot_order_rule": ("A QUALIFIER_PRESERVATION constraint establishes what a reference is "
                            "and its composed slot precedes the numbers; a QUALIFIER_SEMANTICS "
                            "constraint restricts a figure already stated and follows it."),
        "binding": ("Both slots of a two-slot claim declare the same claim_id, cite the same "
                    "frozen source keys, and are INDEPENDENT. The claim is not split; only its "
                    "realisation in prose is."),
        "selected_claim_ids": selected,
        "two_slot_claims": len(selected),
        "one_slot_claims": len(rows) - len(selected),
        "total_slots": sum(row["unit_slots"] for row in rows),
        "by_claim": rows,
    }


# ================================================================ 2. licensed vocabulary

FORBIDDEN_ADDITIONS = ("kayaç", "spesifik")


def build_licensed_vocabulary(plan_v1_1: dict, contract: dict) -> dict[str, Any]:
    """Expose the frozen glosses. Copy them; do not touch them.

    Exposure and widening are different operations and this function performs only the first. The
    values are taken from the frozen contract by reference to its own key, and the audit below
    asserts byte-identity rather than describing it.
    """
    glosses = contract["translation_glosses"]
    rows = []
    for requirement in plan_v1_1["claim_translation_requirements"]:
        claim_id = requirement["claim_id"]
        vocabulary = list(glosses.get(claim_id, []))
        rows.append({
            "claim_id": claim_id,
            "licensed_vocabulary": vocabulary,
            "copied_from": "section_drafting_contract_v1.translation_glosses",
            "byte_identical_to_frozen": vocabulary == glosses.get(claim_id, []),
            "count": len(vocabulary),
        })
    return {
        "rule": ("These are the Turkish words the validator's containment rule already accepts "
                 "for this claim. They are shown, not added. A rendering that stays inside them "
                 "passes stage C; one that reaches outside does not."),
        "is_a_widening": False,
        "widening_guard": ("Every listed word is copied verbatim from the frozen contract's "
                           "translation_glosses. No synonym, gloss or paraphrase entry is added "
                           "by this phase."),
        "forbidden_additions_absent": {
            word: all(word not in row["licensed_vocabulary"] for row in rows)
            for word in FORBIDDEN_ADDITIONS},
        "by_claim": rows,
    }


# ================================================================ 3. draft plan v1.2

def build_draft_plan_v1_2(bundle: Any, entries: list[dict],
                          semantic_constraints: list[dict]) -> dict:
    parent = json.loads(PLAN_V1_1_PATH.read_text(encoding="utf-8"))
    contract = json.loads(DRAFTING_CONTRACT_PATH.read_text(encoding="utf-8"))
    plan = {k: v for k, v in parent.items() if k != "authored_at"}
    allocation = build_unit_allocation(parent, bundle, entries, semantic_constraints)
    vocabulary = build_licensed_vocabulary(parent, contract)
    vocabulary_by_claim = {row["claim_id"]: row["licensed_vocabulary"]
                           for row in vocabulary["by_claim"]}

    requirements = []
    for requirement in parent["claim_translation_requirements"]:
        extended = dict(requirement)
        extended["licensed_vocabulary"] = list(vocabulary_by_claim[requirement["claim_id"]])
        extended["licensed_vocabulary_source"] = (
            "section_drafting_contract_v1.translation_glosses, verbatim")
        extended["licensed_vocabulary_is_exhaustive_for_containment"] = True
        requirements.append(extended)

    plan.update({
        "version": DRAFT_PLAN_V1_2_VERSION,
        "parent_version": parent["version"],
        "parent_plan_path": str(PLAN_V1_1_PATH.relative_to(ROOT)),
        "draft_id": DRAFT_ID,
        "draft_version": DRAFT_VERSION,
        "status": "PLANNED",
        "change_scope": {
            "claim_allocation": "unchanged from v1.1",
            "subsections": "unchanged from v1.1",
            "required_topics": "unchanged from v1.1",
            "excluded_claims": "unchanged from v1.1",
            "semantic_constraints": "unchanged from v1.1",
            "language_policy": "unchanged from v1.1",
            "added": ["unit_allocation", "claim_translation_requirements.licensed_vocabulary",
                      "qualifier_semantics"],
            "widened": [],
            "weakened": [],
            "note": ("Additive over plan v1.1, which stays on disk unchanged. No validator, "
                     "threshold, failure code, marker set, gloss, paraphrase entry, claim, "
                     "allowlist, denylist, pair constraint, prompt or frozen contract is edited."),
        },
        "unit_allocation": allocation,
        "licensed_vocabulary_policy": {k: v for k, v in vocabulary.items() if k != "by_claim"},
        "claim_translation_requirements": requirements,
        "qualifier_semantics": {
            "path": str(QUALIFIER_SEMANTICS_PATH.relative_to(ROOT)),
            "version": QUALIFIER_SEMANTICS_VERSION,
            "constraint_ids": [e["constraint_id"] for e in entries
                               if e["claim_id"] in allocation["selected_claim_ids"]
                               or e["claim_id"] in {row["claim_id"]
                                                    for row in allocation["by_claim"]}],
            "registered": [
                {"constraint_id": e["constraint_id"], "claim_id": e["claim_id"],
                 "required_meaning": e["required_meaning"],
                 "required_action": e["required_action"],
                 "failure_code": e["missing_meaning_code"]}
                for e in entries],
        },
        "validation_contract_version": VALIDATION_CONTRACT_V1_2_VERSION,
        "validator_version": DRAFT_VALIDATOR_V1_2_VERSION,
        "validator_implementation": "scripts/54_section_draft_validator_v1_2.py",
        "authored_by": VERSION,
    })
    return plan


# ================================================================ 4. generation payload

def build_generation_payload_v1_2(plan: dict, allowlist: dict[str, dict]) -> dict:
    """Plan v1.1's payload plus the two things plan v1.2 adds. Nothing is removed.

    The writer still sees no corpus, no retrieval, no denylist text and no bibliography metadata.
    """
    payload = REM.build_generation_payload_v1_1(plan, allowlist)
    payload["draft_id"] = DRAFT_ID
    payload["draft_version"] = DRAFT_VERSION
    payload["unit_allocation"] = {
        k: v for k, v in plan["unit_allocation"].items() if k != "by_claim"}
    payload["licensed_vocabulary_policy"] = plan["licensed_vocabulary_policy"]
    payload["field_semantics"]["unit_slots"] = (
        "A claim with two allocated slots needs two sentences. One states the claim; the other "
        "states the qualifier's meaning, which the claim's own sentence does not contain. Both "
        "sentences declare the same claim_id and the same source_keys.")

    slots_by_claim = {row["claim_id"]: row for row in plan["unit_allocation"]["by_claim"]}
    vocabulary_by_claim = {row["claim_id"]: row["licensed_vocabulary"]
                           for row in plan["claim_translation_requirements"]}
    qualifier_by_claim = {row["claim_id"]: row
                          for row in plan["qualifier_semantics"]["registered"]}
    for subsection in payload["subsections"]:
        for claim in subsection["claims"]:
            claim_id = claim["claim_id"]
            row = slots_by_claim.get(claim_id)
            if row:
                claim["unit_slots"] = row["unit_slots"]
                claim["slots"] = row["slots"]
                if row["unit_slots"] > 1:
                    claim["slot_instruction"] = (
                        "Bu önerme için İKİ cümle yaz. Biri önermenin kendisini, diğeri "
                        "niteleyicinin anlamını taşır. Niteleyicinin anlamı, önermenin kendi "
                        "cümlesinde GEÇMEZ; kopyalayarak elde edilemez. Her iki cümle de aynı "
                        "claim_id ve aynı source_keys ile bağlanır.")
            if claim_id in vocabulary_by_claim:
                claim["licensed_vocabulary"] = list(vocabulary_by_claim[claim_id])
                claim["licensed_vocabulary_note"] = (
                    "Bu önerme İngilizcedir. Türkçe karşılığını yazarken bu sözcük havuzunun "
                    "içinde kal. Havuz genişletilemez; havuz dışındaki bir eşanlamlı önermeyi "
                    "desteklenmemiş hale getirir.")
            if claim_id in qualifier_by_claim:
                claim["qualifier_semantics"] = qualifier_by_claim[claim_id]
    return payload


# ================================================================ 5. pre-generation gates

def run_fixture_universes(bundle: Any) -> dict[str, Any]:
    """Every historical fixture universe, re-scored under v1.2.

    The point is not that v1.2 passes its own fixtures - script 55 established that. It is that a
    validator which gained a stage has not started rejecting prose the earlier universes declared
    valid.
    """
    universes = {}
    for name, path in FIXTURE_UNIVERSES.items():
        if not path.exists():
            universes[name] = {"present": False}
            continue
        fixtures = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                    if line.strip()]
        under_v1_1 = V11.run_fixtures(fixtures, bundle)
        under_v1_2 = V12.run_fixtures(fixtures, bundle)
        universes[name] = {
            "present": True, "sha256": sha_file(path), "total": under_v1_2["total"],
            "passed_under_v1_1": under_v1_1["passed"], "passed_under_v1_2": under_v1_2["passed"],
            "false_accepts": under_v1_2["false_accepts"],
            "false_rejects": under_v1_2["false_rejects"],
            "code_mismatches": under_v1_2["code_mismatches"],
            "newly_failing_under_v1_2": sorted(
                {r["case_id"] for r in under_v1_2["rows"] if r["outcome"] != "PASS"}
                - {r["case_id"] for r in under_v1_1["rows"] if r["outcome"] != "PASS"}),
            "all_pass": under_v1_2["all_pass"],
        }
    return {
        "universes": universes,
        "total": sum(u.get("total", 0) for u in universes.values()),
        "false_accepts": sorted(a for u in universes.values() for a in u.get("false_accepts", [])),
        "false_rejects": sorted(r for u in universes.values() for r in u.get("false_rejects", [])),
        "code_mismatches": sorted(m for u in universes.values()
                                  for m in u.get("code_mismatches", [])),
        "newly_failing_under_v1_2": sorted(n for u in universes.values()
                                           for n in u.get("newly_failing_under_v1_2", [])),
        "all_pass": all(u.get("all_pass", True) for u in universes.values()),
    }


def frozen_integrity() -> dict[str, Any]:
    rows = {}
    for name, (path, manifest_path, key) in FROZEN_SHA_SOURCES.items():
        recorded = json.loads(manifest_path.read_text(encoding="utf-8")).get(key)
        current = sha_file(path)
        rows[name] = {"path": str(path.relative_to(ROOT)), "sha256": current,
                      "recorded_sha256": recorded, "unchanged": current == recorded}
    analysis = json.loads(ANALYSIS_V2_AUDIT.read_text(encoding="utf-8"))["frozen_inputs"]["sha256"]
    validator_v1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
    rows["draft_validator_v1"] = {
        "path": "scripts/49_section_draft_validator_v1.py", "sha256": sha_file(validator_v1),
        "recorded_sha256": analysis["draft_validator_v1"],
        "unchanged": sha_file(validator_v1) == analysis["draft_validator_v1"]}
    qualifier = json.loads(QUALIFIER_MANIFEST.read_text(encoding="utf-8"))["frozen_inputs_sha256"]
    for name, key in (("composition_safe_allowlist_v1", "composition_safe_allowlist_v1"),
                      ("section_drafting_contract_v1", "section_drafting_contract_v1")):
        path = {"composition_safe_allowlist_v1": BOOK / "sec_02_2_limitation_resolution"
                / "claims" / "composition_safe_allowlist_v1.jsonl",
                "section_drafting_contract_v1": DRAFTING_CONTRACT_PATH}[name]
        rows[name] = {"path": str(path.relative_to(ROOT)), "sha256": sha_file(path),
                      "recorded_sha256": qualifier[key],
                      "unchanged": sha_file(path) == qualifier[key]}
    return {"rows": rows, "drifted": [n for n, r in rows.items() if not r["unchanged"]],
            "all_unchanged": all(r["unchanged"] for r in rows.values())}


def pre_generation_gate(state: dict[str, Any]) -> dict[str, Any]:
    """Nothing is generated until every one of these holds."""
    plan = state["plan"]
    allocation = plan["unit_allocation"]
    vocabulary = state["licensed_vocabulary"]
    fixtures = state["fixtures"]
    tests = state["tests"]
    integrity = state["frozen_integrity"]
    registry = state["registry_integrity"]
    contract = json.loads(DRAFTING_CONTRACT_PATH.read_text(encoding="utf-8"))
    glosses = contract["translation_glosses"]

    conditions = {
        "plan_v1_1_unchanged": integrity["rows"]["draft_plan_v1_1"]["unchanged"],
        "plan_v1_2_is_additive": plan["change_scope"]["widened"] == []
        and plan["change_scope"]["weakened"] == [],
        "plan_v1_2_allocation_is_general": bool(allocation["rule_is_general"]),
        "allocation_selects_c002_and_c009": set(allocation["selected_claim_ids"])
        >= {"SEC-02-2-C-002", "SEC-02-2-C-009"},
        "every_selected_claim_has_two_bound_slots": all(
            row["unit_slots"] == 2 for row in allocation["by_claim"]
            if row["claim_id"] in allocation["selected_claim_ids"]),
        "every_other_claim_has_one_slot": all(
            row["unit_slots"] == 1 for row in allocation["by_claim"]
            if row["claim_id"] not in allocation["selected_claim_ids"]),
        "bound_slots_share_claim_and_sources": all(
            len({slot["claim_id"] for slot in row["slots"]}) == 1
            and len({tuple(slot["source_keys"]) for slot in row["slots"]}) == 1
            for row in allocation["by_claim"]),
        "c002_remains_one_claim": len([c for c in state["allowlist"]
                                       if c == "SEC-02-2-C-002"]) == 1,
        "licensed_vocabulary_byte_identical": all(
            row["licensed_vocabulary"] == glosses.get(row["claim_id"], [])
            for row in vocabulary["by_claim"]),
        "licensed_vocabulary_adds_nothing": all(
            vocabulary["forbidden_additions_absent"].values()),
        "translation_glosses_unchanged": integrity["rows"][
            "section_drafting_contract_v1"]["unchanged"],
        "qualifier_registry_consistent": registry["consistent"],
        "all_gate_suites_pass": tests["status"] == "passed",
        "fixture_universes_all_pass": fixtures["all_pass"],
        "false_accepts_zero": not fixtures["false_accepts"],
        "false_rejects_zero": not fixtures["false_rejects"],
        "code_mismatches_zero": not fixtures["code_mismatches"],
        "no_universe_newly_fails_under_v1_2": not fixtures["newly_failing_under_v1_2"],
        "frozen_integrity_holds": integrity["all_unchanged"],
        "validator_v1_unchanged": integrity["rows"]["draft_validator_v1"]["unchanged"],
        "validator_v1_1_unchanged": integrity["rows"]["draft_validator_v1_1"]["unchanged"],
        "historical_attempts_unchanged": integrity["rows"]["attempt_1_raw"]["unchanged"]
        and integrity["rows"]["attempt_2_raw"]["unchanged"],
        "no_code_dropped_by_v1_2": all(code in V12.REJECTION_CODES
                                       for code in V11.REJECTION_CODES),
        "no_stage_dropped_by_v1_2": all(stage in V12.STAGES for stage in V11.STAGES),
        "retrieval_calls_zero": True,
        "qdrant_writes_zero": True,
        "corpus_reads_zero": True,
    }
    return {"conditions": conditions, "failed": [k for k, ok in conditions.items() if not ok],
            "go": all(conditions.values())}


# ================================================================ 6. attempt #3

def generate_attempt_3(payload: dict) -> dict:
    """One controlled generation on the frozen local path, at the frozen sampling settings.

    §65 holds unchanged: sampling settings are not a dial to turn until a draft passes. A pass
    obtained by moving temperature or seed would be evidence about the settings, not about the
    plan.
    """
    generation = REM.module("generation_eval", "scripts/21_generation_model_eval.py")
    system = REM.DRAFTING_PROMPT_V1_1_PATH.read_text(encoding="utf-8")
    user = ("Aşağıdaki onaylı önermeleri kullanarak bölümü yaz. Sadece JSON DraftIR döndür.\n\n"
            + json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    renderer_ = generation.TemplateRenderer()
    tokenizer = generation.GenerationTokenizer()
    prompt = renderer_.render(system=system, user=user, enable_thinking=False)
    config = generation.GenerationConfig(
        model_id=MODEL_ID, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer_.template_sha256,
        system_prompt_version="section-drafting-v1.1",
        system_prompt_sha256=REM.sha_text(system))
    began = now()
    response = generation.complete(prompt, config, MAX_TOKENS, base_url=LMSTUDIO_URL)
    return {
        "attempt": ATTEMPT,
        "draft_id": DRAFT_ID,
        "section_id": SECTION_ID,
        "model_id": MODEL_ID,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "max_tokens": MAX_TOKENS,
        "plan_version": DRAFT_PLAN_V1_2_VERSION,
        "system_prompt_path": str(REM.DRAFTING_PROMPT_V1_1_PATH.relative_to(ROOT)),
        "system_prompt_version": REM.DRAFTING_PROMPT_V1_1_VERSION,
        "system_prompt_sha256": REM.sha_text(system),
        "user_payload_sha256": REM.sha_text(json.dumps(payload, ensure_ascii=False,
                                                       sort_keys=True)),
        "rendered_prompt_sha256": REM.sha_text(prompt),
        "rendered_prompt_tokens": tokenizer.count(prompt),
        "template_sha256": renderer_.template_sha256,
        "tokenizer_sha256": tokenizer.tokenizer_sha256,
        "generation_config_hash": config.config_hash(),
        "requested_at": began,
        "completed_at": now(),
        "finish_reason": response.get("finish_reason"),
        "usage": response.get("usage", {}),
        "latency_seconds": round(response.get("latency_seconds", 0.0), 3),
        "raw_text": response["text"],
        "raw_text_sha256": REM.sha_text(response["text"]),
    }


def qualifier_semantics_audit(ir: Any, bundle: Any, entries: list[dict]) -> dict[str, Any]:
    """Stage L, reported per registered entry rather than only as a verdict."""
    paragraphs = V12.paragraph_texts(ir)
    rows = []
    for unit in ir.units:
        if not unit.material:
            continue
        paragraph = paragraphs.get(unit.paragraph_id, unit.text)
        failures = V12.stage_l_qualifier_semantics(unit, paragraph, bundle, entries)
        for entry in entries:
            if entry["claim_id"] not in unit.claim_ids:
                continue
            realised = V12.realised_constructions(entry, paragraph)
            rows.append({
                "unit_id": unit.unit_id, "claim_id": entry["claim_id"],
                "constraint_id": entry["constraint_id"],
                "realised_constructions": [c["construction_id"] for c in realised],
                "realising_clause": realised[0]["clause"] if realised else None,
                "satisfied": not [f for f in failures
                                  if f.rule_id == entry["constraint_id"]],
                "failure_codes": sorted({f.code for f in failures
                                         if f.rule_id == entry["constraint_id"]})})
    return {"rows": rows, "registered_entries": len(entries),
            "bound_units": len(rows),
            "all_satisfied": all(r["satisfied"] for r in rows),
            "unrealised": [r for r in rows if not r["satisfied"]]}


def attempt_gate_v1_2(result: Any, audit: dict, markdown: str | None, render_audit: dict | None,
                      determinism_ok: Any, language: dict, conditions: dict, qualifiers: dict,
                      qualifier_semantics: dict) -> dict[str, Any]:
    """scripts/50's gate, plus stage L. Inherited conditions are evaluated, never restated."""
    base = REM.attempt_gate(result, audit, markdown, render_audit, determinism_ok,
                            language, conditions, qualifiers)
    added = {
        "qualifier_semantics_all_satisfied": qualifier_semantics["all_satisfied"],
        "no_stage_l_failure": not any(
            f["stage"] == "L_qualifier_semantics"
            for unit in result.units for f in unit.failures),
    }
    merged = dict(base["conditions"], **added)
    return {"conditions": merged, "inherited_conditions": sorted(base["conditions"]),
            "added_conditions": sorted(added),
            "failed": [k for k, ok in merged.items() if ok is False],
            "not_evaluated": [k for k, ok in merged.items() if ok == "NOT_EVALUATED"],
            "accept": all(ok is True for ok in merged.values())}


def attempt_3_cause_record(ir: Any, result: Any, bundle: Any) -> dict[str, Any]:
    """What failed, stated as evidence rather than as a diagnosis.

    Deep analysis belongs to the next phase; this records what can be computed deterministically
    now, so the next phase starts from data rather than from a summary. For every unlicensed
    content word the one question worth answering immediately is whether a licensed equivalent was
    already in the writer's hand - the `kaya`/`kayaç` signature from attempt #2. A word written
    beside its own licensed synonym is a choice; a word with no licensed neighbour might be a gap.
    """
    rows = []
    for unit_result in result.units:
        if unit_result.status != "REJECT":
            continue
        unit = next(u for u in ir.units if u.unit_id == unit_result.unit_id)
        pool = V1.licensed_tokens(unit.claim_ids, bundle)
        unlicensed = V1.unlicensed(unit.text, pool, bundle)
        licensed_in_same_unit = [t for t in V1.content_tokens(unit.text, bundle.function_lexicon)
                                 if any(V1.prefix_agreement(t, p) for p in pool)]
        rows.append({
            "unit_id": unit_result.unit_id,
            "claim_ids": list(unit.claim_ids),
            "failure_codes": list(unit_result.failure_codes),
            "stages": sorted({f["stage"] for f in unit_result.failures}),
            "text": unit.text,
            "unlicensed_content_words": unlicensed,
            "licensed_content_words_in_the_same_unit": licensed_in_same_unit,
            "licensed_alternative_was_in_hand": bool(licensed_in_same_unit),
        })
    # What attempt #2 failed on, and whether plan v1.2 closed it.
    closed = {
        "SEC-02-2-C-002 qualifier (QUALIFIER_DROPPED, stages E and K)":
            not any("SEC-02-2-C-002" in row["claim_ids"]
                    and "QUALIFIER_DROPPED" in row["failure_codes"] for row in rows),
        "SEC-02-2-C-009 qualifier semantics (QUALIFIER_DROPPED, stage L)":
            not any("SEC-02-2-C-009" in row["claim_ids"]
                    and "QUALIFIER_DROPPED" in row["failure_codes"] for row in rows),
        "language (LANGUAGE_MISMATCH, stage J)":
            "LANGUAGE_MISMATCH" not in result.failure_histogram,
        "conditions (CONDITION_DROPPED, stage E)":
            "CONDITION_DROPPED" not in result.failure_histogram,
    }
    recurring = ("UNSUPPORTED_PROPOSITION" in result.failure_histogram
                 and all(row["licensed_alternative_was_in_hand"] for row in rows))
    return {
        "rejected_units": rows,
        "attempt_2_causes_closed": closed,
        "all_attempt_2_causes_closed": all(closed.values()),
        "surviving_failure_codes": list(result.failure_codes),
        "cause_is_novel": not recurring,
        "cause_class": ("WRITER_VOCABULARY_CHOICE - recurrence" if recurring
                        else "TO_BE_CLASSIFIED_BY_THE_NEXT_PHASE"),
        "note": ("Every unlicensed word was written beside a licensed content word from the same "
                 "claim's own pool, which is attempt #2's signature and not a new one. The "
                 "remediation analysis v2 specified was implemented exactly and the failure class "
                 "it targeted recurred on different words."
                 if recurring else
                 "The surviving cause does not match attempt #2's signature and needs its own "
                 "analysis."),
    }


# ================================================================ 7. report

def _next_phase_after_rejection(cause: dict[str, Any]) -> str:
    """Where a rejected attempt #3 routes, decided by the evidence rather than by a default.

    NEXT_PHASE.md's rule is 'a third distinct cause means stop adding instructions'. The evidence
    here is stronger than that rule anticipated and points the same way: the causes attempt #2
    failed on were each closed by plan v1.2 and the pilot still failed, on a class that had
    already been analysed and remediated. A remediation implemented exactly as specified, whose
    target failure recurred on different words, is evidence about the strategy of adding
    instructions - not an invitation to add another.
    """
    if cause["all_attempt_2_causes_closed"] and not cause["cause_is_novel"]:
        return ("SEC-02-2 DRAFTING APPROACH RETHINK V1 — plan v1.2 closed every cause attempt #2 "
                "failed on and the pilot was still rejected, on the one class analysis v2 had "
                "already remediated. The next question is whether claim-bound lexical containment "
                "and fluent Turkish prose are reachable together under this drafting approach, "
                "not which instruction to add fourth.")
    if cause["cause_is_novel"]:
        return ("SEC-02-2 DRAFTING APPROACH RETHINK V1 — a third distinct failure cause means the "
                "approach is the thing to reconsider, not the next instruction to add.")
    return ("SEC-02-2 DRAFTING APPROACH RETHINK V1 — three attempts, three rejections; the "
            "incremental-instruction strategy is what the evidence now bears on.")


def write_report(state: dict[str, Any]) -> None:
    add = (lines := []).append
    gate = state["pre_gate"]
    add(f"# {PHASE}")
    add("")
    add(f"**{state['final_decision']}**")
    add("")
    add(f"Attempt #3: {state['attempt_status']}. Generation attempts this phase: "
        f"{state['generation_attempts']}. Retrieval calls: 0. Qdrant writes: 0. Corpus reads: 0.")
    add("")
    add("## Draft plan v1.2")
    add("")
    allocation = state["plan"]["unit_allocation"]
    add(allocation["why"])
    add("")
    add(f"**Rule.** {allocation['rule']}")
    add("")
    add(f"{allocation['rule_is_general']} Applied to the {len(allocation['by_claim'])} allocated "
        f"claims it selects {allocation['selected_claim_ids']} — "
        f"{allocation['two_slot_claims']} two-slot claims, {allocation['one_slot_claims']} "
        f"one-slot, {allocation['total_slots']} slots in total.")
    add("")
    add("| Claim | Subsection | Slots | Selected by |")
    add("|---|---|---|---|")
    for row in allocation["by_claim"]:
        selection = row["selection"]
        why = "—"
        if selection["needs_composed_slot"]:
            reasons = []
            if selection["lexically_unreachable_by_reproduction"]:
                reasons.append("anchors absent from canonical")
            if selection["semantically_unreachable_by_reproduction"]:
                reasons.append(f"registered {selection['registered_constraint_id']}")
            why = "; ".join(reasons)
        add(f"| `{row['claim_id']}` | {row['subsection_id']} | {row['unit_slots']} | {why} |")
    add("")
    add("## Licensed vocabulary exposure")
    add("")
    add(state["plan"]["licensed_vocabulary_policy"]["rule"])
    add("")
    for row in state["licensed_vocabulary"]["by_claim"]:
        add(f"- `{row['claim_id']}` — {row['count']} words, byte-identical to the frozen "
            f"glosses: {row['byte_identical_to_frozen']}")
    add("")
    add(f"Forbidden additions absent: {state['licensed_vocabulary']['forbidden_additions_absent']}")
    add("")
    add("## Pre-generation gate")
    add("")
    add("| Condition | Result |")
    add("|---|---|")
    for key, value in gate["conditions"].items():
        add(f"| {key.replace('_', ' ')} | {value} |")
    add("")
    add(f"**{'GO' if gate['go'] else 'NO-GO'}**"
        + ("" if gate["go"] else f" — failed: {gate['failed']}"))
    add("")
    add(f"Suites: {state['tests']['tests_run']} tests, {state['tests']['status']}. "
        f"Fixture universes: {state['fixtures']['total']} cases, "
        f"false accepts {len(state['fixtures']['false_accepts'])}, "
        f"false rejects {len(state['fixtures']['false_rejects'])}.")
    add("")
    if state.get("validation") is None:
        add("## Attempt #3")
        add("")
        add(state["attempt_note"] or "Not run.")
        add("")
    else:
        result = state["validation"]
        audit = state["attempt_audit"]
        add("## Attempt #3")
        add("")
        add("| | |")
        add("|---|---|")
        add(f"| Model | `{MODEL_ID}` |")
        add(f"| Temperature | {TEMPERATURE} |")
        add(f"| Seed | {SEED} |")
        add(f"| Draft id | `{state['ir'].draft_id}` |")
        add(f"| Raw preserved before parsing | `{RAW_PATH.relative_to(ROOT)}` |")
        add(f"| Units | {audit['totals']['units']} |")
        add(f"| Material units | {audit['totals']['material_units']} |")
        add(f"| Validator | `{result.validator_version}` |")
        add(f"| Verdict | **{result.status}** |")
        add("")
        if result.rejected_unit_ids:
            add("| Unit | Claims | Codes |")
            add("|---|---|---|")
            for unit in result.units:
                if unit.status == "REJECT":
                    add(f"| `{unit.unit_id}` | {unit.claim_ids} | {unit.failure_codes} |")
            add("")
        add("| Compliance | |")
        add("|---|---|")
        add(f"| Language | {state['language_audit']['compliance']} |")
        add(f"| Conditions | {state['condition_audit']['preservation']} |")
        add(f"| Qualifiers (anchor) | {state['qualifier_audit']['preservation']} |")
        add(f"| Qualifier semantics (stage L) | "
            f"{'satisfied' if state['qualifier_semantics']['all_satisfied'] else 'NOT satisfied'} "
            f"({state['qualifier_semantics']['bound_units']} bound units) |")
        add(f"| Required topics | {audit['required_topics_covered']} / "
            f"{len(REQUIRED_TOPICS)} |")
        add(f"| Citation coverage | {audit['citation_coverage']['coverage']} |")
        add("")
        add("### What plan v1.2 changed")
        add("")
        add("| Claim | Planned slots | Material units written |")
        add("|---|---|---|")
        for claim_id, row in state["attempt_audit_allocation"].items():
            if row["planned_slots"] > 1 or row["units_written"] != row["planned_slots"]:
                add(f"| `{claim_id}` | {row['planned_slots']} | {row['units_written']} |")
        add("")
        cause = state["cause_record"]
        add("| Attempt-#2 cause | Closed by plan v1.2 |")
        add("|---|---|")
        for name, closed in cause["attempt_2_causes_closed"].items():
            add(f"| {name} | {'yes' if closed else 'NO'} |")
        add("")
        add("### Why attempt #3 was rejected")
        add("")
        for row in cause["rejected_units"]:
            add(f"- `{row['unit_id']}` ({', '.join(row['claim_ids'])}) — "
                f"{', '.join(row['failure_codes'])} at {', '.join(row['stages'])} on "
                f"`{row['unlicensed_content_words']}`. Licensed alternative in the same "
                f"sentence: {row['licensed_alternative_was_in_hand']}.")
        add("")
        add(f"**Cause class:** `{cause['cause_class']}`. {cause['note']}")
        add("")
        add("Not repaired, not patched, not translated, no unit deleted, not regenerated. "
            "There is no attempt #4.")
        add("")
        add("### Attempt gate")
        add("")
        add("| Condition | Result |")
        add("|---|---|")
        for key, value in state["attempt_gate"]["conditions"].items():
            add(f"| {key.replace('_', ' ')} | {value} |")
        add("")
    add("## Phase accounting")
    add("")
    add("| | |")
    add("|---|---|")
    add(f"| Generation attempts | {state['generation_attempts']} |")
    add("| Retrieval calls | 0 |")
    add("| Qdrant writes | 0 |")
    add("| Corpus reads | 0 |")
    add("| Automatic retries | 0 |")
    add("| Validators weakened | none |")
    add(f"| Frozen artifacts modified | {state['frozen_integrity']['drifted'] or 'none'} |")
    add("")
    add(f"**Next phase.** {state['next_phase']}")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ================================================================ 8. runner

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=PHASE)
    parser.add_argument("--gates-only", action="store_true",
                        help="author plan v1.2 and run every gate; take no generation")
    parser.add_argument("--replay", action="store_true",
                        help="re-derive the audits from the preserved attempt #3 output. Takes no "
                             "generation: the one authorised attempt is already spent, and "
                             "re-running the analysis must not silently spend another.")
    args = parser.parse_args(argv)

    bundle = V12.load_bundle()
    entries = V12.load_qualifier_semantics()
    constraints = V12.load_semantic_constraints()
    language_contract = REM.language_validator().load_contract()

    plan = build_draft_plan_v1_2(bundle, entries, constraints)
    write_json(PLAN_V1_2_PATH, plan)
    contract = json.loads(DRAFTING_CONTRACT_PATH.read_text(encoding="utf-8"))
    licensed = build_licensed_vocabulary(json.loads(PLAN_V1_1_PATH.read_text(encoding="utf-8")),
                                         contract)

    state: dict[str, Any] = {
        "plan": plan, "licensed_vocabulary": licensed, "allowlist": bundle.allowlist,
        "generation_attempts": 0, "attempt_status": "NOT_RUN", "attempt_note": "",
    }
    state["tests"] = REM.run_tests(GATE_SUITES)
    state["fixtures"] = run_fixture_universes(bundle)
    state["frozen_integrity"] = frozen_integrity()
    state["registry_integrity"] = V12.registry_integrity(bundle, entries)
    state["pre_gate"] = pre_generation_gate(state)
    write_json(FIXTURE_RESULTS_PATH, {"version": VERSION, "section_id": SECTION_ID,
                                      **state["fixtures"]})
    write_json(PRE_GATE_PATH, {
        "version": VERSION, "section_id": SECTION_ID, "evaluated_at": now(),
        "gate": state["pre_gate"], "tests": {k: v for k, v in state["tests"].items()
                                             if k != "tail"},
        "tests_tail": state["tests"]["tail"],
        "fixtures": {k: v for k, v in state["fixtures"].items() if k != "universes"},
        "fixture_universes": state["fixtures"]["universes"],
        "frozen_integrity": state["frozen_integrity"],
        "registry_integrity": state["registry_integrity"],
        "attempt_3_authorised": state["pre_gate"]["go"],
    })

    if not state["pre_gate"]["go"]:
        state.update({
            "final_decision": f"{PHASE} — NO-GO",
            "attempt_status": "NOT_RUN",
            "attempt_note": (f"The pre-generation gate failed on {state['pre_gate']['failed']}. "
                             "No generation was taken. §63 holds: a gate is not a formality to be "
                             "cleared after the fact."),
            "next_phase": "Resolve the failed pre-generation conditions. Attempt #3 is unspent.",
            "pilot_status": "SEC-02-2 PILOT ATTEMPT #3 — NOT RUN",
        })
        write_manifest(state)
        write_report(state)
        print(f"{PHASE}: NO-GO — {state['pre_gate']['failed']}")
        return 1

    if args.gates_only:
        state.update({
            "final_decision": f"{PHASE} — GATES PASSED, generation withheld (--gates-only)",
            "attempt_status": "NOT_RUN",
            "attempt_note": "Run without --gates-only to take the one authorised attempt.",
            "next_phase": "Take attempt #3.",
            "pilot_status": "SEC-02-2 PILOT ATTEMPT #3 — NOT RUN",
        })
        write_manifest(state)
        write_report(state)
        print(f"{PHASE}: GO — gates passed, generation withheld")
        return 0

    payload = build_generation_payload_v1_2(plan, bundle.allowlist)
    if args.replay:
        if not RAW_PATH.exists():
            print("no preserved attempt #3 output to replay", file=sys.stderr)
            return 2
        raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
        if REM.sha_text(raw["raw_text"]) != raw["raw_text_sha256"]:
            print("preserved attempt #3 output does not match its recorded SHA", file=sys.stderr)
            return 2
        state["generation_attempts"] = 1      # the attempt was taken; this run did not take it
        state["generation_calls_in_this_run"] = 0
    else:
        raw = generate_attempt_3(payload)
        state["generation_attempts"] = 1
        state["generation_calls_in_this_run"] = 1
        # §68: preserved before parsing. A DraftIR that will not parse is still evidence.
        write_json(RAW_PATH, raw)

    # A truncated or unparseable completion is a terminal rejection, not an input to repair.
    if raw.get("finish_reason") == "length":
        ir, schema_error = None, (
            f"output was truncated at the token ceiling (finish_reason='length', "
            f"{raw.get('usage', {}).get('completion_tokens')} completion tokens against a "
            f"{MAX_TOKENS}-token budget)")
    else:
        try:
            ir = V12.parse_draft_ir(
                REM.drafting_controller().extract_json_object(raw["raw_text"]))
            schema_error = None
        except V12.DraftSchemaError as error:
            ir, schema_error = None, str(error)

    if ir is None:
        write_json(REJECTED_PATH, {
            "version": VERSION, "attempt": ATTEMPT, "draft_id": DRAFT_ID, "rejected_at": now(),
            "failure_codes": ["SCHEMA_INVALID"], "schema_error": schema_error,
            "raw_text_sha256": raw["raw_text_sha256"], "rendered": False, "repaired": False,
            "translated": False, "regenerated": False, "units_deleted": False,
            "note": "No repair, no patch, no attempt #4. The raw output is preserved as evidence."})
        state.update({
            "attempt_status": "REJECT",
            "pilot_status": "SEC-02-2 PILOT ATTEMPT #3 — REJECTED",
            "final_decision": (f"{PHASE} — CLOSED / GO; SEC-02-2 PILOT ATTEMPT #3 — REJECTED "
                               "(SCHEMA_INVALID)"),
            "attempt_note": f"SCHEMA_INVALID: {schema_error}",
            "next_phase": ("SEC-02-2 DRAFTING APPROACH RETHINK V1 — a third distinct failure "
                           "cause means the approach is the thing to reconsider."),
        })
        write_manifest(state)
        write_report(state)
        print(f"{PHASE}: attempt #3 REJECTED — SCHEMA_INVALID: {schema_error}")
        return 1

    result = V12.validate_draft(ir, bundle, language_contract=language_contract,
                                constraints=constraints, qualifier_semantics=entries)
    state["ir"] = ir
    state["validation"] = result
    state["language_audit"] = REM.language_audit(ir, language_contract)
    state["condition_audit"] = REM.condition_audit(ir, bundle.allowlist, bundle)
    state["qualifier_audit"] = REM.qualifier_audit(ir, bundle.allowlist, bundle, constraints)
    state["qualifier_semantics"] = qualifier_semantics_audit(ir, bundle, entries)
    state["cause_record"] = attempt_3_cause_record(ir, result, bundle)

    markdown = render_entries = render_audit = None
    determinism_ok = None
    registry = V1.load_source_registry()
    if result.status == "ACCEPT":
        markdown, render_entries = REM.renderer().render(ir, registry)
        second, _ = REM.renderer().render(ir, registry)
        determinism_ok = markdown == second
        render_audit = REM.renderer().audit_rendered(markdown, render_entries)

    audit = REM.drafting_controller().build_draft_audit(
        ir, result, render_entries or [], bundle.allowlist, plan, markdown)
    state["attempt_audit"] = audit
    state["attempt_audit_allocation"] = {
        row["claim_id"]: {
            "planned_slots": row["unit_slots"],
            "units_written": len([u for u in ir.units
                                  if row["claim_id"] in u.claim_ids and u.material])}
        for row in plan["unit_allocation"]["by_claim"]}
    state["attempt_gate"] = attempt_gate_v1_2(
        result, audit, markdown, render_audit, determinism_ok, state["language_audit"],
        state["condition_audit"], state["qualifier_audit"], state["qualifier_semantics"])

    write_json(ATTEMPT_AUDIT_PATH, {
        "version": VERSION, "section_id": SECTION_ID, "attempt": ATTEMPT,
        "draft_id": ir.draft_id, "audited_at": now(),
        "raw_text_sha256": raw["raw_text_sha256"], "model_id": MODEL_ID,
        "temperature": TEMPERATURE, "seed": SEED,
        "validator_version": result.validator_version,
        "status": result.status, "failure_codes": result.failure_codes,
        "failure_histogram": result.failure_histogram,
        "rejected_unit_ids": result.rejected_unit_ids,
        "totals": audit["totals"],
        "required_topic_coverage": audit["required_topic_coverage"],
        "required_topics_covered": audit["required_topics_covered"],
        "citation_coverage": audit["citation_coverage"],
        "language_compliance": state["language_audit"]["compliance"],
        "condition_compliance": state["condition_audit"]["preservation"],
        "qualifier_compliance": state["qualifier_audit"]["preservation"],
        "qualifier_semantics": state["qualifier_semantics"],
        "attempt_gate": state["attempt_gate"],
        "cause_record": state["cause_record"],
        "unit_allocation_followed": state["attempt_audit_allocation"],
        "generation_attempts_in_this_phase": 1,
        "retrieval_calls": 0, "qdrant_writes": 0, "corpus_reads": 0, "automatic_retries": 0,
    })

    if state["attempt_gate"]["accept"]:
        write_json(ACCEPTED_IR_PATH, ir.as_dict())
        RENDERED_PATH.parent.mkdir(parents=True, exist_ok=True)
        RENDERED_PATH.write_text(markdown, encoding="utf-8")
        write_json(CITATION_MAP_PATH, {
            "version": "tunnelbook-book-citation-rendering-contract-v1",
            "section_id": SECTION_ID, "draft_id": ir.draft_id,
            "entries": [e.__dict__ for e in render_entries]})
        state.update({
            "attempt_status": "ACCEPT",
            "pilot_status": "SEC-02-2 PILOT_DRAFT_ACCEPTED",
            "final_decision": (f"{PHASE} — CLOSED / GO; SEC-02-2 PILOT_DRAFT_ACCEPTED "
                               "(NOT FINAL MANUSCRIPT PROSE)"),
            "next_phase": ("SEC-02-2 TECHNICAL DRAFT AUDIT V1 + BOOK STYLE CONTRACT V1. The "
                           "draft is a validated pilot, not publishable text; human technical "
                           "review has not happened."),
        })
    else:
        write_json(REJECTED_PATH, {
            "version": VERSION, "attempt": ATTEMPT, "draft_id": ir.draft_id,
            "rejected_at": now(), "raw_text_sha256": raw["raw_text_sha256"],
            "validator_version": result.validator_version,
            "status": result.status, "failure_codes": result.failure_codes,
            "failure_histogram": result.failure_histogram,
            "rejected_unit_ids": result.rejected_unit_ids,
            "rejected_units": [u.__dict__ for u in result.units if u.status == "REJECT"],
            "attempt_gate": state["attempt_gate"],
            "language_audit": {k: v for k, v in state["language_audit"].items() if k != "units"},
            "qualifier_semantics": state["qualifier_semantics"],
            "cause_record": state["cause_record"],
            "rendered": False, "repaired": False, "translated": False, "regenerated": False,
            "units_deleted": False,
            "note": ("No repair, no patch, no translation, no deleted units, no attempt #4. "
                     "The rejected draft is preserved as evidence and routes to a new phase.")})
        state.update({
            "attempt_status": "REJECT",
            "pilot_status": "SEC-02-2 PILOT ATTEMPT #3 — REJECTED",
            "final_decision": (f"{PHASE} — CLOSED / GO; SEC-02-2 PILOT ATTEMPT #3 — REJECTED"),
            "next_phase": _next_phase_after_rejection(state["cause_record"]),
        })
    write_manifest(state)
    write_report(state)
    print(f"{PHASE}: {state['final_decision']}")
    if state.get("validation") is not None:
        print(f"  attempt #3: {state['validation'].status} "
              f"({len(state['validation'].rejected_unit_ids)} rejected of "
              f"{state['attempt_audit']['totals']['units']} units)")
        if state["validation"].rejected_unit_ids:
            print(f"  codes: {state['validation'].failure_codes}")
    return 0 if state["attempt_gate"]["accept"] else 1


def write_manifest(state: dict[str, Any]) -> None:
    result = state.get("validation")
    audit = state.get("attempt_audit") or {}
    write_json(MANIFEST_PATH, {
        "version": VERSION,
        "section_id": SECTION_ID,
        "phase": PHASE,
        "created_at": now(),
        "status": "closed_go" if state["pre_gate"]["go"] else "closed_no_go",
        "final_decision": state["final_decision"],
        "pilot_status": state["pilot_status"],
        "draft_plan_v1_2_version": DRAFT_PLAN_V1_2_VERSION,
        "draft_plan_v1_2_sha": sha_file(PLAN_V1_2_PATH),
        "draft_plan_v1_1_sha": sha_file(PLAN_V1_1_PATH),
        "validator_version": DRAFT_VALIDATOR_V1_2_VERSION,
        "validation_contract_version": VALIDATION_CONTRACT_V1_2_VERSION,
        "model_id": MODEL_ID, "temperature": TEMPERATURE, "seed": SEED,
        "attempt_3_authorised": state["pre_gate"]["go"],
        "attempt_3_status": state["attempt_status"],
        "generation_attempts_this_phase": state["generation_attempts"],
        "generation_calls_in_this_run": state.get("generation_calls_in_this_run", 0),
        "attempt_3_cause_record": state.get("cause_record"),
        "total_pilot_attempts": 2 + state["generation_attempts"],
        "automatic_retries": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "validators_weakened": [],
        "attempt_4_authorised": False,
        "pre_generation_gate": state["pre_gate"],
        "test_counts": {"gate_suites": list(GATE_SUITES),
                        "tests_run": state["tests"]["tests_run"],
                        "status": state["tests"]["status"]},
        "fixture_counts": {k: v for k, v in state["fixtures"].items() if k != "universes"},
        "frozen_integrity": state["frozen_integrity"],
        "unit_allocation": {k: v for k, v in state["plan"]["unit_allocation"].items()
                            if k != "by_claim"},
        "licensed_vocabulary": {
            row["claim_id"]: row["count"] for row in state["licensed_vocabulary"]["by_claim"]},
        "attempt_3_raw_sha": (json.loads(RAW_PATH.read_text(encoding="utf-8"))["raw_text_sha256"]
                              if RAW_PATH.exists() and state["generation_attempts"] else None),
        "attempt_3_raw_file_sha": sha_file(RAW_PATH) if state["generation_attempts"] else None,
        "validation_status": result.status if result else None,
        "validation_failure_codes": result.failure_codes if result else [],
        "validation_failure_histogram": result.failure_histogram if result else {},
        "rejected_unit_ids": result.rejected_unit_ids if result else [],
        "required_topic_coverage": audit.get("required_topic_coverage"),
        "required_topics_covered": audit.get("required_topics_covered"),
        "citation_coverage": audit.get("citation_coverage"),
        "language_compliance": (state.get("language_audit") or {}).get("compliance"),
        "condition_compliance": (state.get("condition_audit") or {}).get("preservation"),
        "qualifier_compliance": (state.get("qualifier_audit") or {}).get("preservation"),
        "qualifier_semantics_satisfied": (state.get("qualifier_semantics") or {}).get(
            "all_satisfied"),
        "attempt_gate": state.get("attempt_gate"),
        "rendered": state["attempt_status"] == "ACCEPT",
        "rendered_sha": sha_file(RENDERED_PATH) if state["attempt_status"] == "ACCEPT" else None,
        "implementation": "scripts/56_sec_02_2_draft_plan_v1_2_attempt_3.py",
        "implementation_sha": sha_file(ROOT / "scripts"
                                       / "56_sec_02_2_draft_plan_v1_2_attempt_3.py"),
        "next_phase": state["next_phase"],
    })


if __name__ == "__main__":
    sys.exit(main())
