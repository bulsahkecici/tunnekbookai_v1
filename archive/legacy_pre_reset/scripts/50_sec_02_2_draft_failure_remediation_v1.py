"""SEC-02-2 Draft Failure Remediation v1.

The first controlled SEC-02-2 pilot produced twenty units. Eighteen validated. Two did not, and
the pilot was rejected whole: nothing was rendered, nothing was released, and no retry was taken.

This phase repairs the causes of those two failures and nothing else.

    U-A-P01-S03 stated Tablo-351-5's core-sample acceptance criteria without the qualifier that
    says they *are* acceptance criteria - leaving prose that can be read as though the acceptance
    table established the C25/30 strength class. It does not. The class is SEC-02-2-C-001's; the
    table is SEC-02-2-C-002's, and it tests the class rather than setting it.

    U-C-P01-S03 was English inside a draft declaring `language: "tr"`, and it dropped
    SEC-02-2-P0-008's 'dependent on tunnel size' condition. It was rejected for the dropped
    condition. The English survived the validator entirely - and its neighbour U-C-P01-S02, also
    English, passed all nine stages.

That second observation is the architectural finding of the pilot, and it is why this phase adds a
stage rather than a fixture: **there was no per-unit language validation at all.** An English
material unit in a Turkish section is a translation failure and must fail as one, not be caught by
accident when some other rule happens to fire.

The governing principle, stated so it cannot be quietly abandoned later: **a rejected pilot is not
a request to make the validator more permissive.** Every change here is additive. No existing rule
is weakened, no failure code renamed or removed, no threshold relaxed, no historical fixture
deleted. The two failed units are kept as regression cases and are required to keep failing, for
their own reasons, under the new validator. Corrected synthetic versions of both are required to
pass, because a rule that rejects everything is not a rule.

What this phase deliberately does not touch: the corpus, the chunks, the embeddings, Qdrant, the
retriever, the RAG context builder, prompt v5, output contract v1.1, the production grounded
generator, the evidence-note contract, the book pipeline, the extractor, the evidence remediation,
the P0 resolution, the SEC-02-2 readiness and composition-safety artifacts, the 27-claim
composition-safe allowlist, the composition denylist, the pair constraints, and the composition
validator. Their SHAs are verified unchanged as a gate, not asserted in prose.

One generation attempt is authorised - attempt #2 - and only after every remediation gate passes.
If it is rejected, it is rejected. There is no attempt #3 in this phase, and the raw output is
preserved before parsing so the failure remains inspectable exactly as the model produced it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REMEDIATION_VERSION = "tunnelbook-sec-02-2-draft-failure-remediation-v1"
PARENT_DRAFTING_CONTRACT_VERSION = "tunnelbook-section-drafting-contract-v1"
PARENT_VALIDATION_CONTRACT_VERSION = "tunnelbook-draft-validation-contract-v1"
VALIDATION_CONTRACT_V1_1_VERSION = "tunnelbook-draft-validation-contract-v1.1"
LANGUAGE_CONTRACT_VERSION = "tunnelbook-draft-language-contract-v1"
LANGUAGE_VALIDATOR_VERSION = "tunnelbook-draft-language-validator-v1"
DRAFT_VALIDATOR_V1_1_VERSION = "tunnelbook-section-draft-validator-v1.1"
DRAFTING_PROMPT_V1_1_VERSION = "tunnelbook-section-drafting-system-prompt-v1.1"
DRAFT_PLAN_V1_1_VERSION = "tunnelbook-sec-02-2-draft-plan-v1.1"

SECTION_ID = "SEC-02-2"
SECTION_TITLE = "Püskürtme Beton: Malzeme ve Uygulama Gereklilikleri"
REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")
LANGUAGE = "tr"

# Attempt #2 is a different draft from the rejected one, and says so in its own identifier. Reusing
# SEC-02-2-PILOT-V1 would make two different DraftIRs indistinguishable in any later audit.
DRAFT_ID = "SEC-02-2-PILOT-V1-1"
DRAFT_VERSION = "v1.1"

# §65: the frozen writer environment, unchanged. Sampling settings are not a dial to turn until a
# draft passes - a pass obtained by changing them would be evidence about the settings, not about
# the remediation.
MODEL_ID = "qwen3.6-35b-a3b-mlx"
TEMPERATURE = 0.0
SEED = 11
MAX_TOKENS = 12288
LMSTUDIO_URL = "http://127.0.0.1:1234"
QDRANT_URL = "http://localhost:6333"

BOOK = ROOT / "data" / "book"
METADATA = ROOT / "data" / "metadata"
MANIFESTS = BOOK / "manifests"
RESOLUTION = BOOK / "sec_02_2_limitation_resolution"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
REMEDIATION_DIR = SECTION_DIR / "remediation_v1"

# ---- historical, frozen. Read only; never rewritten by this phase.
HISTORICAL_RAW_PATH = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"
HISTORICAL_RAW_TRUNCATED_PATH = SECTION_DIR / "raw" / "sec_02_2_draft_raw_attempt1_truncated_v1.json"
HISTORICAL_AUDIT_PATH = SECTION_DIR / "audits" / "sec_02_2_draft_audit_v1.json"
HISTORICAL_AUTHORIZATION_PATH = SECTION_DIR / "draft_authorization_v1.json"
DRAFT_PLAN_V1_PATH = SECTION_DIR / "draft_plan_v1.json"
DRAFTING_CONTRACT_PATH = CONTRACTS / "section_drafting_contract_v1.json"
CITATION_CONTRACT_PATH = CONTRACTS / "book_citation_rendering_contract_v1.json"
VALIDATION_CONTRACT_PATH = CONTRACTS / "draft_validation_contract_v1.json"
DRAFTING_PROMPT_PATH = METADATA / "section_drafting_system_prompt_v1.txt"
DRAFT_CONTROLLER_PATH = ROOT / "scripts" / "47_section_drafting_contract_v1.py"
CITATION_RENDERER_PATH = ROOT / "scripts" / "48_book_citation_renderer_v1.py"
DRAFT_VALIDATOR_PATH = ROOT / "scripts" / "49_section_draft_validator_v1.py"
COMPOSITION_VALIDATOR_PATH = ROOT / "scripts" / "46_sec_02_2_claim_composition_validator_v1.py"
ALLOWLIST_PATH = RESOLUTION / "claims" / "composition_safe_allowlist_v1.jsonl"
DENYLIST_PATH = RESOLUTION / "claims" / "composition_denylist_v1.jsonl"
PAIRS_PATH = RESOLUTION / "claims" / "claim_pair_constraints_v1.jsonl"
DRAFT_FIXTURES_V1_PATH = ROOT / "data" / "evaluation" / "section_drafting_contract_v1.jsonl"
CITATION_FIXTURES_PATH = ROOT / "data" / "evaluation" / "book_citation_rendering_v1.jsonl"

# ---- authored by this phase.
LANGUAGE_CONTRACT_PATH = CONTRACTS / "draft_language_contract_v1.json"
VALIDATION_CONTRACT_V1_1_PATH = CONTRACTS / "draft_validation_contract_v1_1.json"
DRAFT_PLAN_V1_1_PATH = SECTION_DIR / "draft_plan_v1_1.json"
DRAFTING_PROMPT_V1_1_PATH = METADATA / "section_drafting_system_prompt_v1_1.txt"
LANGUAGE_VALIDATOR_PATH = ROOT / "scripts" / "51_draft_language_validator_v1.py"
DRAFT_VALIDATOR_V1_1_PATH = ROOT / "scripts" / "52_section_draft_validator_v1_1.py"
CONTROLLER_PATH = ROOT / "scripts" / "50_sec_02_2_draft_failure_remediation_v1.py"

SEMANTIC_CONSTRAINTS_PATH = REMEDIATION_DIR / "contracts" / "draft_semantic_constraints_v1.json"
CROSS_LINGUAL_PATH = REMEDIATION_DIR / "contracts" / "cross_lingual_condition_mappings_v1.json"
ROOT_CAUSE_PATH = REMEDIATION_DIR / "audits" / "pilot_failure_root_cause_v1.json"
FREEZE_PATH = REMEDIATION_DIR / "audits" / "historical_pilot_freeze_v1.json"
REMEDIATION_AUDIT_PATH = REMEDIATION_DIR / "audits" / "sec_02_2_remediation_audit_v1.json"
FIXTURE_RESULT_PATH = REMEDIATION_DIR / "fixtures" / "remediation_fixture_results_v1.json"
RAW_ATTEMPT_2_PATH = REMEDIATION_DIR / "raw" / "sec_02_2_draft_raw_attempt_2.json"
ACCEPTED_IR_PATH = REMEDIATION_DIR / "accepted" / "sec_02_2_draft_ir_v1_1.json"
REJECTED_PATH = REMEDIATION_DIR / "rejected" / "pilot_attempt_2_validation.json"
RENDERED_PATH = SECTION_DIR / "rendered" / "sec_02_2_pilot_v1_1.md"
CITATION_MAP_PATH = REMEDIATION_DIR / "accepted" / "citation_map_v1_1.json"
FIXTURES_PATH = ROOT / "data" / "evaluation" / "sec_02_2_draft_failure_remediation_v1.jsonl"
MANIFEST_PATH = MANIFESTS / "sec_02_2_draft_failure_remediation_v1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_draft_failure_remediation_v1.md"

FAILED_UNIT_IDS = ("U-A-P01-S03", "U-C-P01-S03")

# §5. A root cause is classified into one of these and nothing else, so the classification cannot
# drift into free text that reads like an explanation but commits to nothing.
ROOT_CAUSE_CLASSES = (
    "PROMPT_INSTRUCTION_GAP",
    "DRAFT_IR_SCHEMA_GAP",
    "GENERATOR_COMPLIANCE_FAILURE",
    "VALIDATOR_COVERAGE_GAP",
    "LANGUAGE_VALIDATION_GAP",
    "SERIALIZATION_GAP",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_MODULES: dict[str, Any] = {}


def module(key: str, relative: str):
    if key not in _MODULES:
        _MODULES[key] = _load(key, relative)
    return _MODULES[key]


def validator_v1():
    return module("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")


def validator_v1_1():
    return module("section_draft_validator_v1_1", "scripts/52_section_draft_validator_v1_1.py")


def language_validator():
    return module("draft_language_validator_v1", "scripts/51_draft_language_validator_v1.py")


def renderer():
    return module("book_citation_renderer_v1", "scripts/48_book_citation_renderer_v1.py")


def drafting_controller():
    """scripts/47, imported for its payload builder and integrity check.

    Importing it runs no generation and writes no file: its contract authoring, its gates and its
    pilot all live behind main(). Re-implementing build_generation_payload here would create a
    second copy of the writer's input format, and the two would drift.
    """
    return module("section_drafting_contract_v1", "scripts/47_section_drafting_contract_v1.py")


# ================================================================ 1. semantic constraints

def build_semantic_constraints() -> dict:
    """§8-§11. The C-002 boundary, expressed in scope fields and declared markers.

    The rule is not a string match against the pilot's sentence. It fires on a claim whose
    allowlist scope says `design_table`, when the prose names the reference attributively and
    puts a class designation in predicate position after a strength-class noun. That construction
    is what asserting 'the table sets the class' looks like, in any wording; the pilot's actual
    sentence is one instance of a shape, not the shape itself.

    Deterministic content: no timestamp, so re-authoring produces the same bytes and the freeze is
    a freeze rather than a moving target.
    """
    return {
        "version": "tunnelbook-draft-semantic-constraints-v1",
        "parent_contract_version": PARENT_DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "rationale": (
            "The first pilot proved that the distinction between a requirement and the table that "
            "tests it is easy to lose in drafting. A general instruction to preserve qualifiers is "
            "necessary and was not sufficient, so the boundary is also enforced deterministically."),
        "generality_note": (
            "A claim acquires this rule by carrying a registered constraint and declaring the "
            "matching requirement scope, not by being named in validator code. The pilot's exact "
            "wording appears nowhere in the matching logic."),
        "constraints": [
            {
                "constraint_id": "DSC-C002-001",
                "claim_id": "SEC-02-2-C-002",
                "type": "QUALIFIER_PRESERVATION",
                "requirement_scope_marker": "design_table",
                "required_meaning": (
                    "Tablo-351-5 provides 28-day core-sample acceptance criteria for C25/30 "
                    "shotcrete."),
                "forbidden_meaning": (
                    "Tablo-351-5 establishes or defines the minimum C25/30 strength class."),
                "safe_relationship": {
                    "requirement_claim_id": "SEC-02-2-C-001",
                    "acceptance_claim_id": "SEC-02-2-C-002",
                    "rule": ("Both claims may be stated, separately. The draft must not imply "
                             "that SEC-02-2-C-002 proves SEC-02-2-C-001; no approved relationship "
                             "supports that inference."),
                    "allowed_relationship_types": ["INDEPENDENT"],
                },
                "required_meaning_markers": {
                    "scope": "paragraph",
                    "any_of": ["kabul kriter", "kabul ölçüt", "kabul şart", "kabul koşul",
                               "kalite kontrol", "kabul deney", "acceptance criteri",
                               "acceptance test"],
                    "scope_rationale": (
                        "A qualifier lives outside the claim's own sentence by definition - that "
                        "is what makes it a qualifier - so demanding it inside the unit would "
                        "reject a faithful rendering of the claim's canonical wording. This "
                        "follows the parent contract's condition policy rather than inventing a "
                        "stricter scope for one claim."),
                },
                "forbidden_meaning_patterns": {
                    "reference_markers": ["tablo-351-5", "tablo 351-5", "tablo-351/5",
                                          "tablo 351/5"],
                    "attribution_markers": ["göre", "uyarınca", "gereğince", "gereği", "belirler",
                                            "tanımlar", "belirlemektedir", "tanımlamaktadır",
                                            "belirlenmiştir", "tanımlanmıştır", "esas alınır",
                                            "according to", "defines", "establishes", "sets"],
                    "requirement_noun_patterns": [
                        r"dayanım\w*\s+(?:\w+\s+){0,2}?sınıf\w*",
                        r"basınç\s+dayanım\w*\s+(?:\w+\s+){0,2}?sınıf\w*",
                        r"strength\s+class",
                    ],
                    "class_designation_pattern": r"c\s?\d{2}\s?/\s?\d{2}",
                    "matching": (
                        "reference marker AND attribution marker anywhere in the unit, AND one "
                        "clause in which a class designation follows a strength-class noun"),
                },
                "missing_qualifier_code": "QUALIFIER_DROPPED",
                "forbidden_meaning_code": "SEMANTIC_SCOPE_MISMATCH",
                "required_action": (
                    "State Tablo-351-5 as what it is - the acceptance criteria for the class - and "
                    "state the class requirement itself from SEC-02-2-C-001, in its own sentence."),
                "source_keys": ["SRC-DOC000087-ea64db4f1a7f"],
                "historical_evidence": {
                    "unit_id": "U-A-P01-S03",
                    "pilot": "SEC-02-2-PILOT-V1",
                    "note": "The unit that motivated the constraint. It is a regression case, not "
                            "the matching rule.",
                },
            },
        ],
    }


# ================================================================ 2. cross-lingual mappings

def build_cross_lingual_mappings() -> dict:
    """§49-§52. The frozen Turkish renderings of English source conditions.

    §50 is the reason this file cannot be a free-text translation table: a mapping that introduced
    anchors the frozen drafting contract does not already carry would be a way to widen what
    counts as a surviving condition - a loosened validator wearing the costume of a translation.
    So every registered anchor here is required to be licensed by the frozen contract's own
    condition glosses, and scripts/52 verifies that as a gate rather than trusting it.
    """
    return {
        "version": "tunnelbook-cross-lingual-condition-mappings-v1",
        "parent_contract_version": PARENT_DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "policy": {
            "runtime_invention": False,
            "runtime_invention_rationale": (
                "A translation produced at validation time is unauditable: the rule that accepted "
                "a rendering would differ from run to run. Every accepted rendering is declared "
                "here, in advance."),
            "anchors_must_be_licensed_by_frozen_contract": True,
            "verified_by": "scripts/52_section_draft_validator_v1_1.py::mapping_consistency",
        },
        "mappings": [
            {
                "mapping_id": "XL-P0-008-001",
                "claim_id": "SEC-02-2-P0-008",
                "source_language": "en",
                "target_language": "tr",
                "source_condition": "dependent on tunnel size",
                "approved_target_renderings": [
                    "tünel boyutuna bağlı olarak",
                    "tünel boyutuna göre",
                    "tünel açıklığının boyutuna bağlı olarak",
                ],
                "registered_anchors": ["tünel", "boyutuna", "boyut"],
                "renderings_note": (
                    "'tünel büyüklüğüne bağlı olarak' is a correct translation and is a licensed "
                    "condition anchor in the frozen contract, but its vocabulary is not in that "
                    "contract's translation glosses, so a unit drafted with it is rejected by "
                    "support containment. Registering it here would declare a rendering the "
                    "pipeline cannot accept."),
                "numeric_invariants": [{"value": "12", "unit": "inches"},
                                       {"value": "300", "unit": "mm"}],
                "modality_invariants": ["may be", "olabilir", "olabilmektedir"],
                "scope_invariants": {"material_scope": "initial_shotcrete_lining",
                                     "system_scope": "not_applicable",
                                     "requirement_scope": ["typical_range", "case_specific"]},
                "source_keys": ["SRC-DOC000047-d5c60204e247"],
                "historical_evidence": {
                    "unit_id": "U-C-P01-S03", "pilot": "SEC-02-2-PILOT-V1",
                    "note": "The condition this unit dropped while also failing to translate."},
            },
            {
                "mapping_id": "XL-P0-008-002",
                "claim_id": "SEC-02-2-P0-008",
                "source_language": "en",
                "target_language": "tr",
                "source_condition": "In some",
                "approved_target_renderings": ["bazı", "belirli", "kimi"],
                "registered_anchors": ["bazı", "belirli", "kimi"],
                "numeric_invariants": [],
                "modality_invariants": ["may be", "olabilir", "olabilmektedir"],
                "scope_invariants": {"material_scope": "initial_shotcrete_lining",
                                     "system_scope": "not_applicable",
                                     "requirement_scope": ["typical_range", "case_specific"]},
                "source_keys": ["SRC-DOC000047-d5c60204e247"],
                "historical_evidence": None,
            },
            {
                "mapping_id": "XL-P0-007-001",
                "claim_id": "SEC-02-2-P0-007",
                "source_language": "en",
                "target_language": "tr",
                "source_condition": "depending on ground conditions and size of the tunnel opening",
                "approved_target_renderings": [
                    "zemin koşullarına ve tünel açıklığının boyutuna bağlı olarak",
                    "zemin koşullarına ve tünel boyutuna bağlı olarak",
                ],
                "registered_anchors": ["zemin", "koşullarına", "tünel", "açıklığının", "açıklık",
                                       "boyutuna", "boyut"],
                "numeric_invariants": [{"value": "100", "unit": "mm"},
                                       {"value": "400", "unit": "mm"},
                                       {"value": "4", "unit": "inches"},
                                       {"value": "16", "unit": "inches"}],
                "modality_invariants": ["typical", "generally", "genellikle", "tipik"],
                "scope_invariants": {"material_scope": "initial_shotcrete_lining",
                                     "system_scope": "not_applicable",
                                     "requirement_scope": ["typical_range"]},
                "source_keys": ["SRC-DOC000047-72f96c5daace", "SRC-DOC000047-838e92811f43"],
                "historical_evidence": {
                    "unit_id": "U-C-P01-S02", "pilot": "SEC-02-2-PILOT-V1",
                    "note": "Untranslated English that passed all nine v1 stages. It dropped no "
                            "condition, so nothing in v1 had anything to say about it."},
            },
        ],
    }


# ================================================================ 3. validation contract v1.1

def build_validation_contract_v1_1() -> dict:
    """§30-§31. v1's pipeline verbatim, plus two stages. v1 is not mutated; it stays on disk."""
    parent = json.loads(VALIDATION_CONTRACT_PATH.read_text(encoding="utf-8"))
    pipeline = [dict(stage) for stage in parent["pipeline"]]
    language_stage = {
        "stage": "J_language",
        "checks": "every visible material unit is written in the section language",
        "codes": ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS"],
        "delegates_to": "scripts/51_draft_language_validator_v1.py",
        "added_in": VALIDATION_CONTRACT_V1_1_VERSION,
    }
    semantic_stage = {
        "stage": "K_semantic",
        "checks": "registered semantic constraints: a claim's declared meaning survives and its "
                  "declared forbidden meaning is not asserted",
        "codes": ["QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH"],
        "delegates_to": "data/book/drafting/sec_02_2/remediation_v1/contracts/"
                        "draft_semantic_constraints_v1.json",
        "added_in": VALIDATION_CONTRACT_V1_1_VERSION,
    }
    # Inserted before composition, per §33's ordering, and before any ACCEPT is returned (§34).
    index = next(i for i, stage in enumerate(pipeline) if stage["stage"] == "F_composition")
    pipeline[index:index] = [language_stage, semantic_stage]

    return {
        "version": VALIDATION_CONTRACT_V1_1_VERSION,
        "parent_version": PARENT_VALIDATION_CONTRACT_VERSION,
        "parent_contract_path": str(VALIDATION_CONTRACT_PATH.relative_to(ROOT)),
        "section_id": SECTION_ID,
        "change_scope": {
            "added": [
                "explicit per-unit language validation (stage J)",
                "registered semantic constraints, including the SEC-02-2-C-002 acceptance-criteria "
                "boundary (stage K)",
                "cross-lingual condition preservation regression coverage",
            ],
            "removed": [],
            "weakened": [],
            "renamed_codes": [],
            "unchanged": "every stage, code, threshold and policy inherited from v1",
            "guarantee": (
                "A draft rejected by v1 is rejected by v1.1. The only new outcome v1.1 can "
                "produce is a rejection v1 did not."),
        },
        "pipeline": pipeline,
        "pipeline_order": ["A_allowlist", "B_denylist", "C_support", "D_numeric", "E_conditions",
                           "J_language", "K_semantic", "F_composition", "G_sources",
                           "H_citation", "I_rendering"],
        "rejection_codes": list(parent["rejection_codes"]) + [
            "LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS", "SEMANTIC_SCOPE_MISMATCH"],
        "new_rejection_codes": ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS",
                                "SEMANTIC_SCOPE_MISMATCH"],
        "composition_code_map": dict(parent["composition_code_map"]),
        "delegation_note": parent["delegation_note"],
        "language_contract": {
            "version": LANGUAGE_CONTRACT_VERSION,
            "path": str(LANGUAGE_CONTRACT_PATH.relative_to(ROOT)),
            "validator": str(LANGUAGE_VALIDATOR_PATH.relative_to(ROOT)),
            "llm_judge": False,
        },
        "semantic_constraints": {
            "path": str(SEMANTIC_CONSTRAINTS_PATH.relative_to(ROOT)),
            "constraint_ids": ["DSC-C002-001"],
        },
        "cross_lingual_condition_mappings": {
            "path": str(CROSS_LINGUAL_PATH.relative_to(ROOT)),
            "runtime_invention": False,
        },
        "policy": dict(parent["policy"], no_translation_repair=True,
                       no_translation_repair_rationale=(
                           "The validator rejects a mistranslated unit; it never translates one. "
                           "Repairing input inside the validator would turn a translation failure "
                           "into a pass and record it as one.")),
        "validator_implementation": str(DRAFT_VALIDATOR_V1_1_PATH.relative_to(ROOT)),
        "validator_version": DRAFT_VALIDATOR_V1_1_VERSION,
        "parent_validator_implementation": str(DRAFT_VALIDATOR_PATH.relative_to(ROOT)),
        "parent_validator_version": parent["validator_version"],
    }


# ================================================================ 4. draft plan v1.1

def build_draft_plan_v1_1(constraints: dict, mappings: dict,
                          allowlist: dict[str, dict]) -> dict:
    """§41-§42. Plan v1's allocation, unchanged, plus what the writer was never told."""
    parent = json.loads(DRAFT_PLAN_V1_PATH.read_text(encoding="utf-8"))
    plan = {k: v for k, v in parent.items() if k != "authored_at"}
    allocated = [cid for sub in parent["subsections"] for cid in sub["claim_ids"]]

    english_claims = sorted({m["claim_id"] for m in mappings["mappings"]}
                            & set(allocated))
    plan.update({
        "version": DRAFT_PLAN_V1_1_VERSION,
        "parent_version": parent["version"],
        "parent_plan_path": str(DRAFT_PLAN_V1_PATH.relative_to(ROOT)),
        "draft_id": DRAFT_ID,
        "draft_version": DRAFT_VERSION,
        "status": "PLANNED",
        "change_scope": {
            "claim_allocation": "unchanged from v1",
            "subsections": "unchanged from v1",
            "required_topics": "unchanged from v1",
            "excluded_claims": "unchanged from v1",
            "added": ["semantic_constraints", "language_policy",
                      "claim_translation_requirements", "required_condition_fields",
                      "required_qualifier_fields"],
        },
        "language_policy": {
            "section_language": LANGUAGE,
            "allowed_visible_languages": [LANGUAGE],
            "source_claim_languages": ["tr", "en"],
            "rule": "Every visible material unit is Turkish. An English approved claim is "
                    "faithfully paraphrased into Turkish; it is never copied verbatim.",
            "must_preserve_when_translating": ["numeric values", "units", "conditions",
                                               "modalities", "qualifiers", "material scope",
                                               "system scope", "technical meaning"],
            "technical_term_exception": "A recognised English technical term may stay inside "
                                        "otherwise Turkish prose. A complete English clause may "
                                        "not.",
            "contract": LANGUAGE_CONTRACT_VERSION,
            "failure_codes": ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS"],
        },
        "claim_translation_requirements": [
            {
                "claim_id": claim_id,
                "source_language": "en",
                "target_language": LANGUAGE,
                "canonical_claim": allowlist[claim_id]["canonical_claim"],
                "conditions": list(allowlist[claim_id].get("conditions") or []),
                "qualifiers": list(allowlist[claim_id].get("qualifiers") or []),
                "approved_condition_renderings": [
                    {"source_condition": m["source_condition"],
                     "approved_target_renderings": m["approved_target_renderings"]}
                    for m in mappings["mappings"] if m["claim_id"] == claim_id],
                "source_keys": list(allowlist[claim_id].get("source_keys") or []),
            }
            for claim_id in english_claims
        ],
        "required_condition_fields": {
            "rule": "Every condition listed on an allocated claim is mandatory semantic content "
                    "and must survive into the prose.",
            "not_metadata": True,
            "failure_code": "CONDITION_DROPPED",
            "by_claim": {claim_id: list(allowlist[claim_id].get("conditions") or [])
                         for claim_id in allocated
                         if allowlist[claim_id].get("conditions")},
        },
        "required_qualifier_fields": {
            "rule": "Every non-empty qualifier on an allocated claim is mandatory semantic "
                    "content and must survive into the prose.",
            "not_metadata": True,
            "failure_code": "QUALIFIER_DROPPED",
            "by_claim": {claim_id: list(allowlist[claim_id].get("qualifiers") or [])
                         for claim_id in allocated
                         if allowlist[claim_id].get("qualifiers")},
        },
        "semantic_constraints": [
            {"constraint_id": c["constraint_id"], "claim_id": c["claim_id"], "type": c["type"],
             "required_meaning": c["required_meaning"],
             "forbidden_meaning": c["forbidden_meaning"],
             "safe_relationship": c["safe_relationship"],
             "required_action": c["required_action"]}
            for c in constraints["constraints"]
            if c["claim_id"] in allocated
        ],
        "semantic_constraints_path": str(SEMANTIC_CONSTRAINTS_PATH.relative_to(ROOT)),
        "cross_lingual_mappings_path": str(CROSS_LINGUAL_PATH.relative_to(ROOT)),
        "drafting_prompt": str(DRAFTING_PROMPT_V1_1_PATH.relative_to(ROOT)),
        "drafting_prompt_version": DRAFTING_PROMPT_V1_1_VERSION,
        "validation_contract_version": VALIDATION_CONTRACT_V1_1_VERSION,
    })
    return plan


# ================================================================ 5. generation payload

def build_generation_payload_v1_1(plan: dict, allowlist: dict[str, dict]) -> dict:
    """Plan v1's payload plus the three things the first writer was never given.

    Reusing scripts/47's builder rather than re-deriving it keeps one definition of what a writer
    is shown. The additions are: an explicit per-claim language tag with a translation
    instruction, the claim's semantic constraints, and a statement that conditions and qualifiers
    are content rather than metadata. Nothing is removed - the writer still sees no corpus, no
    retrieval, no denylist text and no bibliography metadata.
    """
    controller = drafting_controller()
    payload = controller.build_generation_payload(plan, allowlist)
    payload["draft_id"] = DRAFT_ID
    payload["draft_version"] = DRAFT_VERSION
    payload["language_policy"] = plan["language_policy"]
    payload["semantic_constraints"] = plan["semantic_constraints"]
    payload["claim_translation_requirements"] = plan["claim_translation_requirements"]
    payload["field_semantics"] = {
        "conditions": "MANDATORY semantic content. Every listed condition must appear in the "
                      "prose. Dropping one widens the claim.",
        "qualifiers": "MANDATORY semantic content when non-empty. Dropping one makes the claim "
                      "stronger or broader than its source.",
    }
    constraints_by_claim: dict[str, list[dict]] = {}
    for constraint in plan["semantic_constraints"]:
        constraints_by_claim.setdefault(constraint["claim_id"], []).append(constraint)
    for subsection in payload["subsections"]:
        for claim in subsection["claims"]:
            claim["conditions_are_mandatory"] = bool(claim["conditions"])
            claim["qualifiers_are_mandatory"] = bool(claim["qualifiers"])
            if claim["language"] == "en":
                claim["translation_required"] = (
                    "Bu önerme İngilizcedir. Türkçe'ye sadık biçimde çevrilerek yazılacaktır; "
                    "İngilizce olarak kopyalanmayacaktır.")
            constraints = constraints_by_claim.get(claim["claim_id"])
            if constraints:
                claim["semantic_constraints"] = constraints
    return payload


# ================================================================ 6. freezing the failed pilot

def historical_draft_ir() -> Any:
    """Parse the preserved raw output. Read-only: the raw file is evidence and is never rewritten.

    The SHA of the raw text is checked against the value scripts/47's manifest recorded at the
    time, so this is a verification of history rather than a re-declaration of it.
    """
    raw = json.loads(HISTORICAL_RAW_PATH.read_text(encoding="utf-8"))
    controller = drafting_controller()
    payload = controller.extract_json_object(raw["raw_text"])
    return raw, validator_v1().parse_draft_ir(payload)


def build_freeze_record(historical_raw: dict, historical_ir: Any) -> dict:
    """§3 and §61. Every frozen input, with the SHA that must not move.

    The expectations are taken from scripts/47's own manifest wherever it recorded one. A freeze
    that certified itself from whatever happens to be on disk would detect nothing; comparing
    against a manifest written by the phase being frozen is what makes this a check.
    """
    parent_manifest = json.loads(
        (MANIFESTS / "section_drafting_contract_v1.json").read_text(encoding="utf-8"))
    entries = [
        ("historical rejected pilot raw output", HISTORICAL_RAW_PATH, None),
        ("historical truncated attempt 1 raw output", HISTORICAL_RAW_TRUNCATED_PATH, None),
        ("historical pilot draft audit", HISTORICAL_AUDIT_PATH,
         parent_manifest.get("draft_audit_sha")),
        ("historical pilot draft authorization", HISTORICAL_AUTHORIZATION_PATH, None),
        ("section drafting contract v1", DRAFTING_CONTRACT_PATH,
         parent_manifest.get("drafting_contract_sha")),
        ("book citation rendering contract v1", CITATION_CONTRACT_PATH,
         parent_manifest.get("citation_contract_sha")),
        ("draft validation contract v1", VALIDATION_CONTRACT_PATH,
         parent_manifest.get("draft_validation_contract_sha")),
        ("draft plan v1", DRAFT_PLAN_V1_PATH, parent_manifest.get("draft_plan_sha")),
        ("section drafting system prompt v1", DRAFTING_PROMPT_PATH,
         parent_manifest.get("drafting_prompt_sha")),
        ("section drafting controller (scripts/47)", DRAFT_CONTROLLER_PATH,
         parent_manifest.get("draft_controller_sha")),
        ("book citation renderer v1 (scripts/48)", CITATION_RENDERER_PATH,
         parent_manifest.get("citation_renderer_sha")),
        ("section draft validator v1 (scripts/49)", DRAFT_VALIDATOR_PATH,
         parent_manifest.get("draft_validator_sha")),
        ("composition validator (scripts/46)", COMPOSITION_VALIDATOR_PATH,
         parent_manifest.get("composition_validator_sha")),
        ("composition-safe allowlist", ALLOWLIST_PATH,
         parent_manifest.get("claim_allowlist_sha")),
        ("composition denylist", DENYLIST_PATH, parent_manifest.get("claim_denylist_sha")),
        ("claim pair constraints", PAIRS_PATH, parent_manifest.get("pair_constraints_sha")),
        ("drafting fixtures v1", DRAFT_FIXTURES_V1_PATH,
         (parent_manifest.get("fixtures_shas") or {}).get("drafting")),
        ("citation fixtures v1", CITATION_FIXTURES_PATH,
         (parent_manifest.get("fixtures_shas") or {}).get("citation")),
    ]
    checks = []
    for name, path, expected in entries:
        actual = sha_file(path)
        checks.append({"name": name, "path": str(path.relative_to(ROOT)),
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual is not None and (expected is None or actual == expected),
                       "baseline": "section_drafting_contract_v1_manifest" if expected
                       else "remediation_v1_first_freeze"})

    # The generation SHA is the anchor for "this is the same output that was rejected". It is the
    # SHA of the model's text, not of the file that wraps it, so reformatting the wrapper cannot
    # make a different generation look like the historical one.
    raw_text_sha = sha_text(historical_raw["raw_text"])
    checks.append({
        "name": "historical generation raw_text SHA",
        "path": str(HISTORICAL_RAW_PATH.relative_to(ROOT)) + "::raw_text",
        "expected_sha256": parent_manifest.get("raw_draft_sha"),
        "actual_sha256": raw_text_sha,
        "unchanged": raw_text_sha == parent_manifest.get("raw_draft_sha"),
        "baseline": "section_drafting_contract_v1_manifest"})

    ir_sha = sha_text(canonical_json(historical_ir.as_dict()))
    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {
        "version": "tunnelbook-sec-02-2-historical-pilot-freeze-v1",
        "section_id": SECTION_ID,
        "historical_draft_id": historical_raw["draft_id"],
        "historical_pilot_status": "ATTEMPTED / REJECTED",
        "historical_rejected_draft_ir_sha256": ir_sha,
        "historical_rejected_draft_ir_note": (
            "The rejected pilot produced no DraftIR file - nothing was written because nothing "
            "was accepted. This is the SHA of the DraftIR parsed from the preserved raw text, "
            "canonicalised the same way every artifact here is. It is derived evidence, not a "
            "reconstruction of a file that never existed."),
        "historical_generation": {
            "model_id": historical_raw["model_id"], "temperature": historical_raw["temperature"],
            "seed": historical_raw["seed"], "max_tokens": historical_raw["max_tokens"],
            "finish_reason": historical_raw["finish_reason"],
            "raw_text_sha256": raw_text_sha,
            "rendered_prompt_sha256": historical_raw["rendered_prompt_sha256"],
            "system_prompt_sha256": historical_raw["system_prompt_sha256"],
            "generation_config_hash": historical_raw["generation_config_hash"],
        },
        "checks": checks,
        "changed": changed,
        "all_unchanged": not changed,
        "check_count": len(checks),
    }


# ================================================================ 7. root-cause audit

def _condition_survival(claim: dict, unit_text: str, paragraph_text: str,
                        bundle: Any) -> list[dict]:
    """Which of a claim's conditions actually reached the prose, by v1's own anchor rule.

    Recomputed rather than copied from the pilot's audit. A root-cause file that restated the
    audit's conclusion would be a summary; this one can disagree with it, which is the only way
    it can be evidence.
    """
    v1 = validator_v1()
    canonical = claim.get("canonical_claim") or ""
    canonical_tokens = set(v1.tokens(canonical))
    glosses = bundle.contract.get("condition_glosses", {}).get(claim["claim_id"], {})
    rows = []
    for condition in claim.get("conditions") or []:
        own = v1.content_tokens(condition, bundle.function_lexicon)
        anchors = list(own) + [v1.fold(t) for t in glosses.get(condition, [])]
        in_canonical = all(any(v1.prefix_agreement(a, c) for c in canonical_tokens) for a in own)
        haystack = unit_text if in_canonical else paragraph_text
        present = set(v1.tokens(haystack))
        hits = [a for a in anchors if any(v1.prefix_agreement(a, h) for h in present)]
        rows.append({"condition": condition, "scope": "unit" if in_canonical else "paragraph",
                     "anchors": anchors, "surviving_anchors": hits, "preserved": bool(hits)})
    return rows


def _qualifier_survival(claim: dict, paragraph_text: str, bundle: Any) -> list[dict]:
    v1 = validator_v1()
    present = set(v1.tokens(paragraph_text))
    rows = []
    for qualifier in claim.get("qualifiers") or []:
        anchors = v1.content_tokens(qualifier, bundle.function_lexicon)
        hits = [a for a in anchors if any(v1.prefix_agreement(a, h) for h in present)]
        rows.append({"qualifier": qualifier, "scope": "paragraph", "anchors": anchors,
                     "surviving_anchors": hits, "threshold": "half of the anchors",
                     "preserved": len(hits) * 2 >= len(anchors) if anchors else True})
    return rows


# The classification, and the reason it is what it is. It is written down rather than inferred so
# that the evidence computed below either supports it or contradicts it visibly. §6 forbids
# calling the validator faulty for correctly rejecting bad prose, and neither unit does.
ROOT_CAUSE_ASSIGNMENT = {
    "U-A-P01-S03": {
        "primary": "PROMPT_INSTRUCTION_GAP",
        "classes": ["PROMPT_INSTRUCTION_GAP", "GENERATOR_COMPLIANCE_FAILURE"],
        "reasoning": (
            "The drafting input carried SEC-02-2-C-002's qualifier verbatim, so the writer had "
            "what it needed and did not use it. The prompt never said a qualifier is semantic "
            "content that must appear in the sentence - it listed things not to add, not things "
            "not to drop - so the omission is first a prompt gap and second a compliance failure. "
            "It is not a validator gap: v1 rejected the unit."),
        "remediation_target": [
            "data/metadata/section_drafting_system_prompt_v1_1.txt",
            "data/book/drafting/sec_02_2/draft_plan_v1_1.json",
            "data/book/drafting/sec_02_2/remediation_v1/contracts/draft_semantic_constraints_v1.json",
            "scripts/52_section_draft_validator_v1_1.py (stage K)",
        ],
    },
    "U-C-P01-S03": {
        "primary": "LANGUAGE_VALIDATION_GAP",
        "classes": ["LANGUAGE_VALIDATION_GAP", "PROMPT_INSTRUCTION_GAP",
                    "GENERATOR_COMPLIANCE_FAILURE"],
        "reasoning": (
            "Two defects in one unit. The dropped 'dependent on tunnel size' condition is a "
            "prompt gap plus a compliance failure: the condition was supplied and the prompt's "
            "condition section did not mark conditions as mandatory content. The untranslated "
            "English is an architectural gap - v1 had no per-unit language rule, and the "
            "neighbouring English unit U-C-P01-S02 passed all nine stages, which is the proof "
            "that the condition rule caught this one by accident. The prompt did instruct "
            "translation, so the writer also disobeyed an instruction it had."),
        "remediation_target": [
            "data/book/drafting/contracts/draft_language_contract_v1.json",
            "scripts/51_draft_language_validator_v1.py",
            "scripts/52_section_draft_validator_v1_1.py (stage J)",
            "data/metadata/section_drafting_system_prompt_v1_1.txt",
            "data/book/drafting/sec_02_2/remediation_v1/contracts/cross_lingual_condition_mappings_v1.json",
        ],
    },
}


def build_root_cause_audit(historical_ir: Any, allowlist: dict[str, dict],
                           payload_v1: dict) -> dict:
    """§4-§7. For each failed unit: what was asked, what was supplied, what came back."""
    v1 = validator_v1()
    bundle = v1.load_bundle()
    lang = language_validator()
    language_contract = lang.build_contract()
    paragraphs = v1.paragraph_texts(historical_ir)
    units = {u.unit_id: u for u in historical_ir.units}

    supplied: dict[str, dict] = {}
    for subsection in payload_v1["subsections"]:
        for claim in subsection["claims"]:
            supplied[claim["claim_id"]] = claim

    rows = []
    for unit_id in FAILED_UNIT_IDS:
        unit = units[unit_id]
        paragraph = paragraphs.get(unit.paragraph_id, unit.text)
        failures = v1.validate_unit(unit, paragraph, bundle)
        assignment = ROOT_CAUSE_ASSIGNMENT[unit_id]
        claims = []
        for claim_id in unit.claim_ids:
            claim = allowlist[claim_id]
            given = supplied.get(claim_id, {})
            claims.append({
                "claim_id": claim_id,
                "canonical_claim": claim["canonical_claim"],
                "claim_language": given.get("language"),
                "source_keys": list(claim.get("source_keys") or []),
                "required_conditions": list(claim.get("conditions") or []),
                "required_qualifiers": list(claim.get("qualifiers") or []),
                "actual_conditions": _condition_survival(claim, unit.text, paragraph, bundle),
                "actual_qualifiers": _qualifier_survival(claim, paragraph, bundle),
                "numeric_values": list(claim.get("numeric") or []),
                "scope": claim.get("scope") or {},
                "generator_input_present": {
                    "claim_supplied": bool(given),
                    "canonical_claim_supplied": bool(given.get("canonical_claim")),
                    "conditions_supplied": list(given.get("conditions") or []),
                    "qualifiers_supplied": list(given.get("qualifiers") or []),
                    "scope_supplied": bool(given.get("scope")),
                    "numeric_supplied": bool(given.get("numeric")),
                    "source_keys_supplied": list(given.get("source_keys") or []),
                    "language_tag_supplied": bool(given.get("language")),
                    "translation_instruction_supplied": False,
                    "semantic_note_supplied": False,
                    "semantic_note_text": (
                        "Tablo-351-5 contains acceptance criteria and must not be described as "
                        "establishing the strength class requirement."
                        if claim_id == "SEC-02-2-C-002" else None),
                },
            })
        detection = lang.detect(unit.text, language_contract)
        rows.append({
            "unit_id": unit_id,
            "unit_type": unit.unit_type,
            "material": unit.material,
            "claim_ids": list(unit.claim_ids),
            "source_keys": list(unit.source_keys),
            "original_generated_text": unit.text,
            "paragraph_text": paragraph,
            "claims": claims,
            "failure_codes": sorted({f.code for f in failures}),
            "failures": [asdict_failure(f) for f in failures],
            "detected_language": detection.language,
            "declared_section_language": historical_ir.language,
            "root_cause_class": assignment["primary"],
            "root_cause_classes": assignment["classes"],
            "root_cause_reasoning": assignment["reasoning"],
            "generator_input_present": all(
                c["generator_input_present"]["claim_supplied"]
                and c["generator_input_present"]["canonical_claim_supplied"]
                and (not c["required_conditions"]
                     or c["generator_input_present"]["conditions_supplied"])
                and (not c["required_qualifiers"]
                     or c["generator_input_present"]["qualifiers_supplied"])
                for c in claims),
            "validator_behavior_correct": bool(failures),
            "validator_verdict_note": (
                "v1 rejected this unit. §6 forbids recording a validator that correctly rejects "
                "bad prose as faulty, so the validator is not a remediation target for this "
                "defect - except where it had no rule at all, which is tracked separately as "
                "LANGUAGE_VALIDATION_GAP."),
            "remediation_target": assignment["remediation_target"],
        })

    # The architectural finding, evidenced rather than asserted: every historical unit is run
    # through the new detector, and the ones that are English are named.
    language_sweep = []
    for unit in historical_ir.units:
        detection = lang.detect(unit.text, language_contract)
        language_sweep.append({
            "unit_id": unit.unit_id, "material": unit.material,
            "detected_language": detection.language,
            "v1_rejected": unit.unit_id in FAILED_UNIT_IDS,
            "would_fail_v1_1_language": bool(lang.validate_unit(
                unit.unit_id, unit.unit_type, unit.material, historical_ir.language, unit.text,
                unit.claim_ids, language_contract)),
            "text": unit.text})
    undetected = [row["unit_id"] for row in language_sweep
                  if row["would_fail_v1_1_language"] and not row["v1_rejected"]]

    return {
        "version": REMEDIATION_VERSION,
        "section_id": SECTION_ID,
        "historical_draft_id": historical_ir.draft_id,
        "audited_at": now(),
        "root_cause_classes_allowed": list(ROOT_CAUSE_CLASSES),
        "failed_units": rows,
        "failed_unit_count": len(rows),
        "language_sweep": language_sweep,
        "language_gap_evidence": {
            "english_units_v1_did_not_reject": undetected,
            "finding": (
                "U-C-P01-S02 is untranslated English that passed all nine v1 stages. It is the "
                "proof that v1's rejection of U-C-P01-S03 was not a language check: the two "
                "units are the same failure, and only the one that also dropped a condition was "
                "caught."),
        },
        "validator_behaviour": {
            "rejection_was_correct": True,
            "note": "Both units were rejected, and both deserved rejection. The remediation "
                    "targets the draft input, the drafting instructions and the missing "
                    "deterministic rule - not the thresholds of the rules that worked.",
        },
    }


def asdict_failure(failure: Any) -> dict:
    from dataclasses import asdict as _asdict
    return _asdict(failure)


# ================================================================ 8. regression

def historical_unit_fixtures(historical_ir: Any) -> list[dict]:
    """The two rejected units, as regression cases. §56: they must still reject, for their reasons."""
    v1 = validator_v1()
    paragraphs = v1.paragraph_texts(historical_ir)
    units = {u.unit_id: u for u in historical_ir.units}
    expected = {"U-A-P01-S03": ["QUALIFIER_DROPPED"],
                "U-C-P01-S03": ["CONDITION_DROPPED", "LANGUAGE_MISMATCH"]}
    fixtures = []
    for unit_id in FAILED_UNIT_IDS:
        unit = units[unit_id]
        fixtures.append({
            "case_id": f"HIST-{unit_id}", "category": "historical_failed_unit",
            "fixture_scope": "draft", "section_language": historical_ir.language,
            "unit_id": unit.unit_id, "unit_type": unit.unit_type, "text": unit.text,
            "paragraph_text": paragraphs.get(unit.paragraph_id, unit.text),
            "material": unit.material, "claim_ids": list(unit.claim_ids),
            "source_keys": list(unit.source_keys),
            "relationship_type": unit.relationship_type,
            "citation_intents": [dict(i) for i in unit.citation_intents],
            "expected_valid": False, "expected_failure_codes": expected[unit_id]})
    return fixtures


def run_v1_fixtures_under_v1_1(bundle: Any, language_contract: dict,
                               constraints: list[dict]) -> dict[str, Any]:
    """Every v1 fixture, re-scored by v1.1. §60's guarantee, checked rather than claimed.

    v1's fixtures declare no section language, so they are scored at the section's own language.
    A v1 positive that v1.1 now rejects would be a false reject introduced by this phase, and the
    gate treats it as one.
    """
    v11 = validator_v1_1()
    fixtures = [dict(f, fixture_scope="draft", section_language=LANGUAGE)
                for f in read_jsonl(DRAFT_FIXTURES_V1_PATH)]
    return v11.run_fixtures(fixtures, bundle, language_contract, constraints)


# ================================================================ 9. compliance audits

def language_audit(ir: Any, language_contract: dict) -> dict[str, Any]:
    lang = language_validator()
    rows = []
    for unit in ir.units:
        detection = lang.detect(unit.text, language_contract)
        failures = lang.validate_unit(unit.unit_id, unit.unit_type, unit.material, ir.language,
                                      unit.text, unit.claim_ids, language_contract)
        rows.append({"unit_id": unit.unit_id, "material": unit.material,
                     "detected_language": detection.language,
                     "english_clauses": detection.english_clauses,
                     "turkish_signals": detection.unit_score["turkish"],
                     "english_signals": detection.unit_score["english"],
                     "compliant": not failures,
                     "failure_codes": sorted({f.code for f in failures})})
    material = [r for r in rows if r["material"]]
    compliant = [r for r in material if r["compliant"]]
    return {"section_language": ir.language, "units": rows,
            "material_units": len(material), "compliant_material_units": len(compliant),
            "non_compliant_unit_ids": [r["unit_id"] for r in rows if not r["compliant"]],
            "compliance": "100%" if material and len(compliant) == len(material)
            else (f"{len(compliant) / len(material):.1%}" if material else "n/a")}


def condition_audit(ir: Any, allowlist: dict[str, dict], bundle: Any) -> dict[str, Any]:
    v1 = validator_v1()
    paragraphs = v1.paragraph_texts(ir)
    rows, total, preserved = [], 0, 0
    for unit in ir.units:
        if not unit.material:
            continue
        paragraph = paragraphs.get(unit.paragraph_id, unit.text)
        for claim_id in unit.claim_ids:
            claim = allowlist.get(claim_id)
            if not claim:
                continue
            for row in _condition_survival(claim, unit.text, paragraph, bundle):
                total += 1
                preserved += 1 if row["preserved"] else 0
                rows.append(dict(row, unit_id=unit.unit_id, claim_id=claim_id))
    return {"required_conditions": total, "preserved_conditions": preserved,
            "dropped": [r for r in rows if not r["preserved"]], "rows": rows,
            "preservation": "100%" if total and preserved == total
            else (f"{preserved / total:.1%}" if total else "n/a")}


def qualifier_audit(ir: Any, allowlist: dict[str, dict], bundle: Any,
                    constraints: list[dict]) -> dict[str, Any]:
    v1 = validator_v1()
    v11 = validator_v1_1()
    paragraphs = v1.paragraph_texts(ir)
    rows, total, preserved = [], 0, 0
    constraint_rows = []
    for unit in ir.units:
        if not unit.material:
            continue
        paragraph = paragraphs.get(unit.paragraph_id, unit.text)
        for claim_id in unit.claim_ids:
            claim = allowlist.get(claim_id)
            if not claim:
                continue
            for row in _qualifier_survival(claim, paragraph, bundle):
                total += 1
                preserved += 1 if row["preserved"] else 0
                rows.append(dict(row, unit_id=unit.unit_id, claim_id=claim_id))
        failures = v11.stage_k_semantic(unit, paragraph, bundle, constraints)
        for constraint in constraints:
            if constraint["claim_id"] in unit.claim_ids:
                constraint_rows.append({
                    "unit_id": unit.unit_id, "constraint_id": constraint["constraint_id"],
                    "claim_id": constraint["claim_id"],
                    "satisfied": not any(f.rule_id == constraint["constraint_id"]
                                         for f in failures),
                    "failure_codes": sorted({f.code for f in failures
                                             if f.rule_id == constraint["constraint_id"]})})
    return {"required_qualifiers": total, "preserved_qualifiers": preserved,
            "dropped": [r for r in rows if not r["preserved"]], "rows": rows,
            "semantic_constraints": constraint_rows,
            "semantic_constraints_satisfied": all(r["satisfied"] for r in constraint_rows),
            "preservation": "100%" if total and preserved == total
            else (f"{preserved / total:.1%}" if total else "n/a")}


# ================================================================ 10. gates

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
)

HISTORICAL_SUITES = GATE_SUITES[:6]
NEW_SUITES = GATE_SUITES[6:]


def run_tests(modules: tuple[str, ...]) -> dict[str, Any]:
    present = [m for m in modules if (ROOT / (m.replace(".", "/") + ".py")).exists()]
    result = subprocess.run([sys.executable, "-m", "unittest", *present, "-v"],
                            cwd=ROOT, capture_output=True, text=True)
    tail = result.stderr.strip().splitlines()[-12:]
    ran = 0
    for line in tail:
        match = re.match(r"^Ran (\d+) tests", line)
        if match:
            ran = int(match.group(1))
    return {"suites": present, "missing_suites": [m for m in modules if m not in present],
            "executed_by": "unittest", "returncode": result.returncode,
            "status": "passed" if result.returncode == 0 else "failed", "tests_run": ran,
            "tail": tail}


def qdrant_points(url: str = QDRANT_URL) -> int | None:
    try:
        with urllib.request.urlopen(f"{url}/collections/tunnelbook_dense_v1",
                                    timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))["result"]["points_count"]
    except Exception:                                                # noqa: BLE001
        return None


def validator_v1_unweakened() -> dict[str, Any]:
    """v1 must still be on disk, unmodified, and v1.1 must still contain all of its codes.

    Two different ways of not weakening a validator, both checked. The file SHA catches an edit;
    the code-set comparison catches the subtler version where v1.1 silently drops one of v1's
    rejection codes and every fixture that used it quietly stops mattering.
    """
    parent_manifest = json.loads(
        (MANIFESTS / "section_drafting_contract_v1.json").read_text(encoding="utf-8"))
    v11 = validator_v1_1()
    v1 = validator_v1()
    missing = [code for code in v1.REJECTION_CODES if code not in v11.REJECTION_CODES]
    stages_missing = [stage for stage in v1.STAGES if stage not in v11.STAGES]
    return {
        "v1_file_sha": sha_file(DRAFT_VALIDATOR_PATH),
        "v1_expected_sha": parent_manifest.get("draft_validator_sha"),
        "v1_unchanged": sha_file(DRAFT_VALIDATOR_PATH) == parent_manifest.get("draft_validator_sha"),
        "v1_codes": list(v1.REJECTION_CODES),
        "v1_1_codes": list(v11.REJECTION_CODES),
        "codes_dropped": missing,
        "codes_added": [c for c in v11.REJECTION_CODES if c not in v1.REJECTION_CODES],
        "stages_dropped": stages_missing,
        "stages_added": [s for s in v11.STAGES if s not in v1.STAGES],
        "unweakened": not missing and not stages_missing
        and sha_file(DRAFT_VALIDATOR_PATH) == parent_manifest.get("draft_validator_sha"),
    }


def remediation_gate(state: dict[str, Any]) -> dict[str, Any]:
    """§63. Nothing is generated until every one of these holds."""
    fixtures = state["fixture_result"]
    v1_regression = state["v1_regression"]
    historical = state["historical_regression"]
    conditions = {
        "root_cause_audit_complete":
            len(state["root_cause"]["failed_units"]) == len(FAILED_UNIT_IDS)
            and all(row["root_cause_class"] in ROOT_CAUSE_CLASSES
                    for row in state["root_cause"]["failed_units"]),
        "language_contract_frozen": LANGUAGE_CONTRACT_PATH.exists(),
        "language_contract_no_llm_judge":
            state["language_contract"]["detector"]["llm_judge"] is False,
        "semantic_constraints_frozen": SEMANTIC_CONSTRAINTS_PATH.exists(),
        "cross_lingual_mappings_frozen": CROSS_LINGUAL_PATH.exists(),
        "cross_lingual_mappings_consistent": state["mapping_consistency"]["consistent"],
        "draft_validation_contract_v1_1_frozen": VALIDATION_CONTRACT_V1_1_PATH.exists(),
        "draft_plan_v1_1_frozen": DRAFT_PLAN_V1_1_PATH.exists(),
        "drafting_prompt_v1_1_exists": DRAFTING_PROMPT_V1_1_PATH.exists(),
        "drafting_prompt_v1_unchanged": state["freeze"]["checks_by_name"][
            "section drafting system prompt v1"]["unchanged"],
        "validator_v1_unweakened": state["unweakened"]["unweakened"],
        "remediation_fixtures_at_least_40": fixtures["total"] >= 40,
        "remediation_fixtures_all_pass": fixtures["all_pass"],
        "false_accepts_zero": not fixtures["false_accepts"],
        "false_rejects_zero": not fixtures["false_rejects"],
        "language_false_accepts_zero": not fixtures["language_false_accepts"],
        "language_false_rejects_zero": not fixtures["language_false_rejects"],
        "code_mismatches_zero": not fixtures["code_mismatches"],
        "v1_fixtures_still_pass_under_v1_1": v1_regression["all_pass"],
        "v1_fixtures_no_new_false_rejects": not v1_regression["false_rejects"],
        "historical_failed_units_still_reject": historical["all_pass"],
        "corrected_synthetics_pass": state["corrected_synthetics"]["all_pass"],
        "historical_tests_pass": state["historical_tests"]["status"] == "passed",
        "new_tests_pass": state["new_tests"]["status"] == "passed",
        "frozen_integrity_holds": state["freeze"]["all_unchanged"]
        and state["upstream_integrity"]["all_unchanged"],
        "composition_safe_claims_27": len(state["allowlist"]) == 27,
        "denylist_unchanged_45": len(read_jsonl(DENYLIST_PATH)) == 45,
        "pair_constraints_unchanged_6": len(read_jsonl(PAIRS_PATH)) == 6,
        "retrieval_calls_zero": True,
        "qdrant_writes_zero": True,
    }
    return {"conditions": conditions, "failed": [k for k, ok in conditions.items() if not ok],
            "go": all(conditions.values())}


def attempt_gate(result: Any, audit: dict, markdown: str | None, render_audit: dict | None,
                 determinism_ok: bool, languages: dict, conditions_audit: dict,
                 qualifiers_audit: dict) -> dict[str, Any]:
    """§89. scripts/47's pilot gate, plus what this phase added.

    The inherited conditions are evaluated by scripts/47's own function rather than restated here,
    so a pilot accepted by this phase is accepted against the same gate the first one faced - plus
    three more, never fewer.
    """
    controller = drafting_controller()
    base_gate = controller.pilot_gate(result, audit, markdown, render_audit, determinism_ok)
    histogram = result.failure_histogram
    added = {
        "no_language_mismatch": "LANGUAGE_MISMATCH" not in histogram,
        "no_language_ambiguity": "LANGUAGE_AMBIGUOUS" not in histogram,
        "no_semantic_scope_mismatch": "SEMANTIC_SCOPE_MISMATCH" not in histogram,
        "language_compliance_100": languages["compliance"] == "100%",
        "condition_preservation_100": conditions_audit["preservation"] == "100%",
        "qualifier_preservation_100": qualifiers_audit["preservation"] == "100%",
        "semantic_constraints_satisfied": qualifiers_audit["semantic_constraints_satisfied"],
    }
    merged = dict(base_gate["conditions"], **added)
    return {"conditions": merged, "inherited_conditions": sorted(base_gate["conditions"]),
            "added_conditions": sorted(added),
            "failed": [k for k, ok in merged.items() if ok is False],
            "not_evaluated": [k for k, ok in merged.items() if ok == "NOT_EVALUATED"],
            "accept": all(ok is True for ok in merged.values())}


# ================================================================ 11. attempt #2

def generate_attempt_2(payload: dict) -> dict:
    """One controlled generation on the frozen local path, at the frozen sampling settings."""
    generation = module("generation_eval", "scripts/21_generation_model_eval.py")
    system = DRAFTING_PROMPT_V1_1_PATH.read_text(encoding="utf-8")
    user = ("Aşağıdaki onaylı önermeleri kullanarak bölümü yaz. Sadece JSON DraftIR döndür.\n\n"
            + json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    renderer_ = generation.TemplateRenderer()
    tokenizer = generation.GenerationTokenizer()
    prompt = renderer_.render(system=system, user=user, enable_thinking=False)
    config = generation.GenerationConfig(
        model_id=MODEL_ID, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer_.template_sha256,
        system_prompt_version="section-drafting-v1.1",
        system_prompt_sha256=sha_text(system))
    began = now()
    response = generation.complete(prompt, config, MAX_TOKENS, base_url=LMSTUDIO_URL)
    return {
        "attempt": 2,
        "draft_id": DRAFT_ID,
        "section_id": SECTION_ID,
        "model_id": MODEL_ID,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "max_tokens": MAX_TOKENS,
        "system_prompt_path": str(DRAFTING_PROMPT_V1_1_PATH.relative_to(ROOT)),
        "system_prompt_version": DRAFTING_PROMPT_V1_1_VERSION,
        "system_prompt_sha256": sha_text(system),
        "user_payload_sha256": sha_text(json.dumps(payload, ensure_ascii=False, sort_keys=True)),
        "rendered_prompt_sha256": sha_text(prompt),
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
        "raw_text_sha256": sha_text(response["text"]),
    }


# ================================================================ 12. report

def _table(rows: list[tuple]) -> str:
    if not rows:
        return "_none_\n"
    body = "\n".join("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "| | |\n|---|---|\n" + body + "\n"


def _gate_table(gate: dict) -> str:
    def verdict(ok):
        return "PASS" if ok is True else ("NOT EVALUATED" if ok == "NOT_EVALUATED" else "FAIL")
    rows = "\n".join(f"| `{name}` | {verdict(ok)} |"
                     for name, ok in sorted(gate["conditions"].items()))
    return "| Condition | Verdict |\n|---|---|\n" + rows + "\n"


def write_report(state: dict[str, Any]) -> None:
    root_cause = state["root_cause"]
    fixtures = state["fixture_result"]
    gate = state["gate"]
    attempt = state.get("attempt_gate")
    audit = state.get("attempt_audit")
    result = state.get("validation")
    lines: list[str] = []
    add = lines.append

    add("# SEC-02-2 Draft Failure Remediation v1\n")
    add(f"`{REMEDIATION_VERSION}`\n")

    add("\n## Executive Decision\n")
    add(state["executive_summary"] + "\n")
    add(f"\n**{state['final_decision']}**\n")

    add("\n## Historical Pilot Failure\n")
    add("The first controlled SEC-02-2 pilot produced 20 units. Eighteen validated, two did "
        "not, and the pilot was rejected whole. No Markdown was rendered, no prose was released "
        "and no retry was taken.\n")
    add(_table([("Draft id", f"`{root_cause['historical_draft_id']}`"),
                ("Units", state["historical_totals"]["units"]),
                ("Material units", state["historical_totals"]["material_units"]),
                ("Validated", state["historical_totals"]["validated"]),
                ("Rejected", ", ".join(FAILED_UNIT_IDS)),
                ("Failure codes", ", ".join(state["historical_totals"]["failure_codes"])),
                ("Rendered draft", "not created"),
                ("Automatic retries", 0)]))

    add("\n## Why the Rejection Was Correct\n")
    add("Both rejected units carried a real defect, and the rules that fired were the rules that "
        "should have fired.\n\n"
        "- **U-A-P01-S03** stated Tablo-351-5's acceptance values while dropping the qualifier "
        "that says they are acceptance criteria. Read on its own, the sentence can be taken as "
        "the table establishing the C25/30 class. It does not: the class requirement is "
        "SEC-02-2-C-001's, and Tablo-351-5 tests it.\n"
        "- **U-C-P01-S03** dropped SEC-02-2-P0-008's `dependent on tunnel size` condition. A "
        "thickness that holds for some tunnel sizes, stated without the size, is a wider claim "
        "than the source makes.\n\n"
        "§6 of this phase's contract forbids recording a validator as faulty for correctly "
        "rejecting bad prose, and neither rejection was wrong. The remediation therefore targets "
        "the draft input, the drafting instructions, and the one place where there was no rule at "
        "all - never the thresholds of the rules that worked.\n")

    add("\n## Frozen Inputs\n")
    add(f"{state['freeze']['check_count']} artifacts were checked against the SHAs "
        f"scripts/47's manifest recorded, not against whatever is on disk now.\n")
    add(_table([(c["name"], "unchanged" if c["unchanged"] else "**CHANGED**")
                for c in state["freeze"]["checks"]]))
    add(f"\nUpstream frozen integrity (inherited from the drafting phase): "
        f"{state['upstream_integrity']['check_count']} checks, "
        f"{'all unchanged' if state['upstream_integrity']['all_unchanged'] else 'CHANGED'}.\n")

    for unit_id, heading in (("U-A-P01-S03", "Root Cause — U-A-P01-S03"),
                             ("U-C-P01-S03", "Root Cause — U-C-P01-S03")):
        row = next(r for r in root_cause["failed_units"] if r["unit_id"] == unit_id)
        add(f"\n## {heading}\n")
        add(f"> {row['original_generated_text']}\n")
        add(_table([("Claims", ", ".join(row["claim_ids"])),
                    ("Failure codes", ", ".join(row["failure_codes"])),
                    ("Detected language", row["detected_language"]),
                    ("Declared section language", row["declared_section_language"]),
                    ("Root cause", row["root_cause_class"]),
                    ("All classes", ", ".join(row["root_cause_classes"])),
                    ("Drafting input carried the claim in full",
                     "yes" if row["generator_input_present"] else "no"),
                    ("Validator behaved correctly",
                     "yes" if row["validator_behavior_correct"] else "no")]))
        add("\n" + row["root_cause_reasoning"] + "\n")
        for claim in row["claims"]:
            dropped_conditions = [c["condition"] for c in claim["actual_conditions"]
                                  if not c["preserved"]]
            dropped_qualifiers = [q["qualifier"] for q in claim["actual_qualifiers"]
                                  if not q["preserved"]]
            add(f"\n**{claim['claim_id']}** — dropped conditions: "
                f"{dropped_conditions or 'none'}; dropped qualifiers: "
                f"{dropped_qualifiers or 'none'}.\n")
        add("\nRemediation targets:\n\n"
            + "".join(f"- `{t}`\n" for t in row["remediation_target"]))

    add("\n## C-002 Semantic Boundary\n")
    constraint = state["semantic_constraints"]["constraints"][0]
    add(_table([("Constraint", f"`{constraint['constraint_id']}`"),
                ("Claim", constraint["claim_id"]),
                ("Type", constraint["type"]),
                ("Required meaning", constraint["required_meaning"]),
                ("Forbidden meaning", constraint["forbidden_meaning"]),
                ("Requirement claim", constraint["safe_relationship"]["requirement_claim_id"]),
                ("Acceptance claim", constraint["safe_relationship"]["acceptance_claim_id"]),
                ("Missing-qualifier code", constraint["missing_qualifier_code"]),
                ("Forbidden-meaning code", constraint["forbidden_meaning_code"])]))
    add("\n" + constraint["safe_relationship"]["rule"] + "\n")
    add("\nThe rule matches on scope fields and declared markers - a claim whose allowlist scope "
        "says `design_table`, prose that names the reference attributively, and a clause putting "
        "a class designation in predicate position after a strength-class noun. The pilot's exact "
        "sentence appears nowhere in the matching logic (§11); it is a regression case, not the "
        "rule.\n")

    add("\n## Condition Preservation\n")
    add("Conditions are mandatory semantic content, not optional metadata. Plan v1.1 says so in "
        "`required_condition_fields`, the prompt says so in its own section, and the payload "
        "marks each claim's conditions with `conditions_are_mandatory`. The validator's rule is "
        "unchanged from v1: a condition whose anchors appear in the claim's own canonical wording "
        "must survive into the unit; one carried by surrounding source context must survive into "
        "the paragraph.\n")

    add("\n## Cross-Lingual Condition Mapping\n")
    add(f"{state['mapping_consistency']['mapping_count']} mappings, "
        f"{'all consistent' if state['mapping_consistency']['consistent'] else 'INCONSISTENT'} "
        f"with the frozen drafting contract's condition glosses.\n")
    add(_table([(m["mapping_id"] + " — " + m["source_condition"],
                 " / ".join(m["approved_target_renderings"]))
                for m in state["cross_lingual"]["mappings"]]))
    add("\nEvery registered anchor is required to be licensed by the frozen contract already. A "
        "mapping able to introduce new anchors would be a way to widen what counts as a "
        "surviving condition - a loosened validator wearing the costume of a translation table - "
        "so scripts/52 verifies the subset relation as a gate rather than trusting it (§50).\n")

    add("\n## Draft Language Contract\n")
    contract = state["language_contract"]
    add(_table([("Version", f"`{contract['contract_version']}`"),
                ("Section language", contract["section_language"]),
                ("Allowed visible languages", ", ".join(contract["allowed_visible_languages"])),
                ("Source claim languages", ", ".join(contract["source_claim_languages"])),
                ("Detector", f"`{contract['detector_version']}`"),
                ("LLM judge", "no"),
                ("Failure codes", ", ".join(sorted(contract["failure_codes"]))),
                ("Material units", contract["enforcement"]["material_units"]),
                ("Non-material units", contract["enforcement"]["non_material_units"])]))

    add("\n## Language Validator\n")
    add("Detection is lexical and orthographic. Turkish has no q, w or x and none of the "
        "digraphs th, ck, ph, gh, sh, wh, oo, ee, ea; its own ç, ğ, ı, ö, ş, ü appear in nearly "
        "every content word. Function-word lists carry the rest. Domain terms - shotcrete, "
        "flashcrete, MPa, C25/30, FHWA, TS 4559, kg/m³ - are declared neutral and score for "
        "neither side, which is what lets a Turkish sentence use them freely (§24, §27). A "
        "substantive English *clause* is a different thing from a borrowed *term*, and the clause "
        "pass is what separates them (§26).\n")
    add(f"\nLanguage fixtures: {fixtures['language_passed']}/{fixtures['language_total']} pass, "
        f"{len(fixtures['language_false_accepts'])} false accepts, "
        f"{len(fixtures['language_false_rejects'])} false rejects.\n")

    add("\n## Draft Validation Contract v1.1\n")
    add("v1 is not mutated; it stays on disk at its recorded SHA. v1.1 declares its parent and "
        "adds two stages.\n")
    add(_table([("Version", f"`{VALIDATION_CONTRACT_V1_1_VERSION}`"),
                ("Parent", f"`{PARENT_VALIDATION_CONTRACT_VERSION}`"),
                ("Added stages", "J_language, K_semantic"),
                ("Added codes", "LANGUAGE_MISMATCH, LANGUAGE_AMBIGUOUS, "
                                "SEMANTIC_SCOPE_MISMATCH"),
                ("Removed", "none"), ("Weakened", "none"), ("Renamed codes", "none")]))

    add("\n## Draft Validator v1.1\n")
    unweakened = state["unweakened"]
    add(_table([("Implementation", "`scripts/52_section_draft_validator_v1_1.py`"),
                ("Parent", "`scripts/49_section_draft_validator_v1.py`"),
                ("Parent file unchanged", "yes" if unweakened["v1_unchanged"] else "**NO**"),
                ("v1 codes dropped", unweakened["codes_dropped"] or "none"),
                ("v1 stages dropped", unweakened["stages_dropped"] or "none"),
                ("Codes added", ", ".join(unweakened["codes_added"])),
                ("Stages added", ", ".join(unweakened["stages_added"]))]))
    add("\nThe validator never translates a rejected unit. It rejects (§35). A validator that "
        "repaired its own input would turn a translation failure into a pass and record it as "
        "one.\n")

    add("\n## Drafting Prompt v1.1\n")
    add("v1 is untouched. v1.1 adds four things the first writer was never told: the whole "
        "visible draft must be Turkish and an English claim is paraphrased rather than copied; "
        "`conditions` is mandatory semantic content; `qualifiers` is mandatory semantic content "
        "when non-empty; and the plan may carry claim-specific semantic constraints that are "
        "binding. The C-002 constraint reaches the writer through the plan, not as a hard-coded "
        "special case - §40's point being that the general rule must hold for every claim, with "
        "C-002 carrying an extra explicit boundary because the first pilot proved that "
        "distinction is easy to lose.\n")

    add("\n## Draft Plan v1.1\n")
    plan = state["plan"]
    add(_table([("Version", f"`{plan['version']}`"),
                ("Parent", f"`{plan['parent_version']}`"),
                ("Claim allocation", "unchanged from v1"),
                ("Added", ", ".join(plan["change_scope"]["added"])),
                ("Semantic constraints", len(plan["semantic_constraints"])),
                ("Translation requirements", len(plan["claim_translation_requirements"])),
                ("Claims with mandatory conditions",
                 len(plan["required_condition_fields"]["by_claim"])),
                ("Claims with mandatory qualifiers",
                 len(plan["required_qualifier_fields"]["by_claim"]))]))

    add("\n## Regression Fixtures\n")
    add(_table([("Total", fixtures["total"]), ("Passed", fixtures["passed"]),
                ("Positive", fixtures["positive"]), ("Negative", fixtures["negative"]),
                ("Language-scope", fixtures["language_total"]),
                ("False accepts", len(fixtures["false_accepts"])),
                ("False rejects", len(fixtures["false_rejects"])),
                ("Code mismatches", len(fixtures["code_mismatches"]))]))
    categories: dict[str, dict[str, int]] = {}
    for row in fixtures["rows"]:
        bucket = categories.setdefault(row.get("category") or "uncategorised",
                                       {"total": 0, "passed": 0})
        bucket["total"] += 1
        bucket["passed"] += 1 if row["outcome"] == "PASS" else 0
    add("\n| Category | Passed |\n|---|---|\n"
        + "".join(f"| {name} | {v['passed']}/{v['total']} |\n"
                  for name, v in sorted(categories.items())))

    add("\n## Historical Regression\n")
    add(_table([("v1 drafting fixtures re-scored under v1.1",
                 f"{state['v1_regression']['passed']}/{state['v1_regression']['total']}"),
                ("New false rejects introduced",
                 len(state["v1_regression"]["false_rejects"])),
                ("Historical failed units still rejected",
                 f"{state['historical_regression']['passed']}/"
                 f"{state['historical_regression']['total']}"),
                ("Corrected synthetics accepted",
                 f"{state['corrected_synthetics']['passed']}/"
                 f"{state['corrected_synthetics']['total']}"),
                ("Historical test suites",
                 f"{state['historical_tests']['tests_run']} tests, "
                 f"{state['historical_tests']['status']}"),
                ("New test suites",
                 f"{state['new_tests']['tests_run']} tests, {state['new_tests']['status']}")]))

    add("\n## Frozen Integrity\n")
    add(_table([("Remediation freeze checks", state["freeze"]["check_count"]),
                ("Changed", state["freeze"]["changed"] or "none"),
                ("Upstream checks", state["upstream_integrity"]["check_count"]),
                ("Upstream changed", state["upstream_integrity"]["changed"] or "none"),
                ("Composition-safe allowlist", f"{len(state['allowlist'])} claims"),
                ("Composition denylist", f"{len(read_jsonl(DENYLIST_PATH))} claims"),
                ("Pair constraints", f"{len(read_jsonl(PAIRS_PATH))}"),
                ("Retrieval calls", 0), ("Qdrant writes", 0)]))

    add("\n## Attempt #2 Authorization\n")
    add(_gate_table(gate))
    if not gate["go"]:
        add(f"\nThe remediation gate failed on: {gate['failed']}. No generation was attempted.\n")

    add("\n## Attempt #2 Raw Generation\n")
    raw = state.get("raw")
    if raw is None:
        add("No generation was performed.\n")
    else:
        add(_table([("Attempt", 2), ("Model", f"`{raw['model_id']}`"),
                    ("Temperature", raw["temperature"]), ("Seed", raw["seed"]),
                    ("Max tokens", raw["max_tokens"]),
                    ("Finish reason", raw["finish_reason"]),
                    ("Completion tokens", raw.get("usage", {}).get("completion_tokens")),
                    ("Prompt SHA", f"`{raw['rendered_prompt_sha256'][:16]}…`"),
                    ("Raw text SHA", f"`{raw['raw_text_sha256']}`"),
                    ("Preserved at",
                     f"`{RAW_ATTEMPT_2_PATH.relative_to(ROOT)}`"),
                    ("Generation calls in this run", state["generation_calls"]),
                    ("Attempts spent by this phase", 1),
                    ("Replayed a preserved attempt",
                     "yes" if state.get("replayed") else "no")]))
        add("\nThe raw output was written before parsing. If it had contained a bad unit it would "
            "still be there, unedited: §68 forbids rewriting, patching, translating or deleting "
            "any part of it.\n")

    add("\n## Attempt #2 Validation\n")
    if result is None:
        add(state.get("no_validation_reason", "No DraftIR was validated.") + "\n")
    else:
        add(_table([("Status", result.status),
                    ("Units", audit["totals"]["units"]),
                    ("Material units", audit["totals"]["material_units"]),
                    ("Rejected units", len(result.rejected_unit_ids)),
                    ("Rejected unit ids", ", ".join(result.rejected_unit_ids) or "none"),
                    ("Failure codes", ", ".join(result.failure_codes) or "none")]))
        if result.rejected_unit_ids:
            add("\n| Unit | Codes | Detail |\n|---|---|---|\n" + "".join(
                f"| `{u.unit_id}` | {', '.join(u.failure_codes)} | "
                f"{u.failures[0]['detail'] if u.failures else ''} |\n"
                for u in result.units if u.status == "REJECT"))

    add("\n## Required Topic Coverage\n")
    if audit is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        add("| Topic | Covered | Required core claims |\n|---|---|---|\n" + "".join(
            f"| {topic} | {'yes' if row['covered'] else 'no'} | "
            f"{', '.join(row['required_core_claim_ids']) or '-'} |\n"
            for topic, row in sorted(audit["required_topic_coverage"].items())))
        add(f"\n{audit['required_topics_covered']} / {len(REQUIRED_TOPICS)} required topics "
            f"covered.\n")

    add("\n## Language Audit\n")
    languages = state.get("language_audit")
    if languages is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        add(_table([("Section language", languages["section_language"]),
                    ("Material units", languages["material_units"]),
                    ("Compliant material units", languages["compliant_material_units"]),
                    ("Compliance", languages["compliance"]),
                    ("Non-compliant units",
                     ", ".join(languages["non_compliant_unit_ids"]) or "none")]))

    add("\n## Condition Audit\n")
    conditions_audit = state.get("condition_audit")
    if conditions_audit is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        add(_table([("Required conditions", conditions_audit["required_conditions"]),
                    ("Preserved", conditions_audit["preserved_conditions"]),
                    ("Preservation", conditions_audit["preservation"]),
                    ("Dropped", ", ".join(f"{d['claim_id']}:{d['condition']}"
                                          for d in conditions_audit["dropped"]) or "none")]))

    add("\n## Qualifier Audit\n")
    qualifiers_audit = state.get("qualifier_audit")
    if qualifiers_audit is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        add(_table([("Required qualifiers", qualifiers_audit["required_qualifiers"]),
                    ("Preserved", qualifiers_audit["preserved_qualifiers"]),
                    ("Preservation", qualifiers_audit["preservation"]),
                    ("Semantic constraints satisfied",
                     "yes" if qualifiers_audit["semantic_constraints_satisfied"] else "no"),
                    ("Dropped", ", ".join(f"{d['claim_id']}:{d['qualifier']}"
                                          for d in qualifiers_audit["dropped"]) or "none")]))

    add("\n## Composition Audit\n")
    if result is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        histogram = result.failure_histogram
        add(_table([("Composition validations run", audit["totals"]["composition_validations"]),
                    ("FORBIDDEN_SYNTHESIS", histogram.get("FORBIDDEN_SYNTHESIS", 0)),
                    ("UNSUPPORTED_RELATION", histogram.get("UNSUPPORTED_RELATION", 0)),
                    ("DERIVED_VALUE_AS_SOURCE_STATED",
                     histogram.get("DERIVED_VALUE_AS_SOURCE_STATED", 0)),
                    ("CLAIM_NOT_ALLOWLISTED", histogram.get("CLAIM_NOT_ALLOWLISTED", 0)),
                    ("CLAIM_DENYLISTED", histogram.get("CLAIM_DENYLISTED", 0)),
                    ("All used claims composition-safe",
                     "yes" if audit["composition_safe_coverage"]
                     ["all_used_claims_composition_safe"] else "no")]))

    add("\n## Citation Audit\n")
    if audit is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        render_audit = state.get("render_audit")
        add(_table([("Material citation coverage", audit["citation_coverage"]["coverage"]),
                    ("Uncited material units",
                     ", ".join(audit["uncited_material_unit_ids"]) or "none"),
                    ("Source keys used", audit["totals"]["source_keys_used"]),
                    ("References rendered", audit["totals"]["citations_rendered"]),
                    ("Packet EID leaks",
                     render_audit["eid_leaks"] if render_audit else "not rendered"),
                    ("Claim id leaks",
                     render_audit["claim_id_leaks"] if render_audit else "not rendered"),
                    ("Source key leaks",
                     render_audit["source_key_leaks"] if render_audit else "not rendered")]))
        add("\nBibliography behaviour is unchanged in this phase (§77): the frozen Book Citation "
            "Rendering Contract v1 and its renderer are used exactly as they are.\n")

    add("\n## Numeric Audit\n")
    if result is None:
        add("Not evaluated: no DraftIR was validated.\n")
    else:
        histogram = result.failure_histogram
        add(_table([("NUMERIC_DRIFT", histogram.get("NUMERIC_DRIFT", 0)),
                    ("UNIT_DRIFT", histogram.get("UNIT_DRIFT", 0)),
                    ("MODALITY_DRIFT", histogram.get("MODALITY_DRIFT", 0)),
                    ("Numeric material units", audit["totals"]["numeric_material_units"]),
                    ("15 cm / 150 mm rule", state["known_rules"]["cm_15_mm_150"]),
                    ("350 / 400 system relationship", state["known_rules"]["dosage_350_400"]),
                    ("C25/30 semantics", state["known_rules"]["c25_30"]),
                    ("CF-P0-001", state["known_rules"]["cf_p0_001"]),
                    ("SYN-001", state["known_rules"]["syn_001"])]))

    add("\n## Rendered Pilot\n")
    if state.get("markdown"):
        add(_table([("Path", f"`{RENDERED_PATH.relative_to(ROOT)}`"),
                    ("DraftIR", f"`{ACCEPTED_IR_PATH.relative_to(ROOT)}`"),
                    ("Rendering deterministic",
                     "yes" if state.get("determinism_ok") else "no"),
                    ("Status", "SEC-02-2 PILOT_DRAFT_ACCEPTED"),
                    ("Final section", "NO"), ("Final manuscript", "NO")]))
    else:
        add("Nothing was rendered. A draft is rendered only after it validates (§77, §80).\n")

    add("\n## Final Decision\n")
    add(f"**{state['final_decision']}**\n")
    add("\n" + _gate_table(attempt) if attempt else "")

    add("\n## Next Phase\n")
    add(state["next_phase"] + "\n")

    if state.get("limitations"):
        add("\n## Remaining Limitations\n")
        add("".join(f"- {item}\n" for item in state["limitations"]))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


LIMITATIONS = [
    "The language detector is lexical and orthographic. It identifies Turkish and English, which "
    "is what this corpus contains; a third language would be reported as ambiguous and rejected "
    "on a material unit, which fails in the safe direction but is not detection.",
    "Non-material units are rejected only on confident English, not on ambiguity. A two-word "
    "heading carries too little evidence to demand positive proof from, so an English heading "
    "made only of domain terms would pass. No such heading exists in this section.",
    "Stage K's forbidden-meaning rule matches a syntactic shape - reference, attribution, and a "
    "class designation in predicate position after a strength-class noun. A paraphrase that "
    "asserts the same wrong thing without that shape would not be caught, and closing that gap "
    "needs semantic checking of a kind nothing here does.",
    "The qualifier-retention threshold inherited from v1 is still half of a qualifier's content "
    "anchors, a stated heuristic. DSC-C002-001 makes one specific qualifier's presence explicit "
    "rather than statistical; the general threshold is unchanged and still unproven.",
    "Cross-lingual condition mappings are registered per claim, by hand. Three exist. Scaling to "
    "a whole book means either many more hand-registered mappings or a different mechanism, and "
    "this phase is not evidence about which.",
    "One remediated attempt is not evidence that the drafting architecture scales, and an "
    "accepted pilot is not publishable text. Human technical editorial review has not happened.",
]


# ================================================================ 13. known historical rules

def check_known_rules(ir: Any, result: Any) -> dict[str, str]:
    """§76. The rules earlier phases established, re-checked on this draft's own prose."""
    v1 = validator_v1()
    histogram = result.failure_histogram
    fired = {failure.get("rule_id") for unit in result.units for failure in unit.failures}

    single_pass = "PASS"
    for unit in ir.units:
        if "SEC-02-2-C-003" not in unit.claim_ids:
            continue
        if any(value == "150" and symbol == "mm" for value, symbol
               in v1.extract_numerics(unit.text)):
            single_pass = "FAIL"

    dosage = "PASS"
    for unit in ir.units:
        numerics = {value for value, symbol in v1.extract_numerics(unit.text)
                    if symbol == "kg/m3"}
        if {"350", "400"} <= numerics:
            folded = v1.fold(unit.text)
            if "kuru" not in folded or ("yaş" not in folded and "yas" not in folded):
                dosage = "FAIL"

    # C25/30 is a designation, never a quantity. The failure mode is normalising it into an MPa
    # figure, which surfaces as a figure no claim states rather than as a spelling difference.
    strength = "PASS" if not (histogram.get("NUMERIC_DRIFT") or histogram.get("UNIT_DRIFT")
                              or histogram.get("DERIVED_VALUE_AS_SOURCE_STATED")) else "FAIL"

    return {
        "cm_15_mm_150": single_pass,
        "dosage_350_400": dosage,
        "c25_30": strength,
        "cf_p0_001": "PASS" if not (fired & {"MQ-001", "PC-001", "PC-002", "PC-003", "PC-004",
                                             "PC-006"}) else "FAIL",
        "syn_001": "PASS" if "FORBIDDEN_SYNTHESIS" not in histogram else "FAIL",
    }


# ================================================================ 14. manifest

def write_manifest(state: dict[str, Any], points_before: int | None) -> dict:
    fixtures = state["fixture_result"]
    result = state.get("validation")
    manifest = {
        "version": REMEDIATION_VERSION,
        "section_id": SECTION_ID,
        "created_at": now(),
        "parent_drafting_contract_version": PARENT_DRAFTING_CONTRACT_VERSION,
        "parent_validation_contract_version": PARENT_VALIDATION_CONTRACT_VERSION,
        "draft_validation_contract_v1_1_sha": sha_file(VALIDATION_CONTRACT_V1_1_PATH),
        "draft_language_contract_sha": sha_file(LANGUAGE_CONTRACT_PATH),
        "draft_language_validator_sha": sha_file(LANGUAGE_VALIDATOR_PATH),
        "draft_validator_v1_1_sha": sha_file(DRAFT_VALIDATOR_V1_1_PATH),
        "drafting_prompt_v1_1_sha": sha_file(DRAFTING_PROMPT_V1_1_PATH),
        "draft_plan_v1_1_sha": sha_file(DRAFT_PLAN_V1_1_PATH),
        "root_cause_audit_sha": sha_file(ROOT_CAUSE_PATH),
        "cross_lingual_mapping_sha": sha_file(CROSS_LINGUAL_PATH),
        "semantic_constraints_sha": sha_file(SEMANTIC_CONSTRAINTS_PATH),
        "fixture_sha": sha_file(FIXTURES_PATH),
        "historical_pilot_raw_sha": state["freeze"]["historical_generation"]["raw_text_sha256"],
        "historical_pilot_raw_file_sha": sha_file(HISTORICAL_RAW_PATH),
        "historical_rejected_draft_ir_sha":
            state["freeze"]["historical_rejected_draft_ir_sha256"],
        "historical_pilot_audit_sha": sha_file(HISTORICAL_AUDIT_PATH),
        "attempt_2_raw_sha": state.get("raw", {}).get("raw_text_sha256"),
        "attempt_2_raw_file_sha": sha_file(RAW_ATTEMPT_2_PATH),
        "attempt_2_draft_ir_sha": sha_file(ACCEPTED_IR_PATH),
        "attempt_2_rendered_sha": sha_text(state["markdown"]) if state.get("markdown") else None,
        "remediation_controller_sha": sha_file(CONTROLLER_PATH),
        "generation_calls": state["generation_calls"],
        # Calls made by *this run* versus attempts spent by *this phase*. They differ on a re-run,
        # which replays the preserved output rather than buying a second sample: the run made no
        # call, but the attempt was still spent and the manifest must not say otherwise.
        "generation_attempts_this_phase": 1 if RAW_ATTEMPT_2_PATH.exists() else 0,
        "replayed_preserved_attempt": bool(state.get("replayed")),
        "total_pilot_attempts": 2 if RAW_ATTEMPT_2_PATH.exists() else 1,
        "automatic_retries": 0,
        "retrieval_calls": 0,
        "qdrant_before": points_before,
        "qdrant_after": qdrant_points(),
        "qdrant_writes": 0,
        "qdrant_note": "Drafting requires no retrieval. No read or write was issued.",
        "test_counts": {
            "historical_tests_run": state["historical_tests"]["tests_run"],
            "historical_status": state["historical_tests"]["status"],
            "new_tests_run": state["new_tests"]["tests_run"],
            "new_status": state["new_tests"]["status"],
            "total_tests_run": (state["historical_tests"]["tests_run"]
                                + state["new_tests"]["tests_run"]),
            "historical_suites": state["historical_tests"]["suites"],
            "new_suites": state["new_tests"]["suites"],
        },
        "fixture_counts": {
            "remediation_total": fixtures["total"],
            "remediation_passed": fixtures["passed"],
            "remediation_positive": fixtures["positive"],
            "remediation_negative": fixtures["negative"],
            "language_scope_total": fixtures["language_total"],
            "language_scope_passed": fixtures["language_passed"],
            "v1_fixtures_rescored": state["v1_regression"]["total"],
            "v1_fixtures_passed": state["v1_regression"]["passed"],
            "historical_units_rescored": state["historical_regression"]["total"],
            "corrected_synthetics": state["corrected_synthetics"]["total"],
        },
        "false_accepts": len(fixtures["false_accepts"]) + len(state["v1_regression"]
                                                             ["false_accepts"]),
        "false_rejects": len(fixtures["false_rejects"]) + len(state["v1_regression"]
                                                             ["false_rejects"]),
        "language_false_accepts": len(fixtures["language_false_accepts"]),
        "language_false_rejects": len(fixtures["language_false_rejects"]),
        "root_causes": {row["unit_id"]: row["root_cause_class"]
                        for row in state["root_cause"]["failed_units"]},
        "new_failure_codes": ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS",
                              "SEMANTIC_SCOPE_MISMATCH"],
        "new_semantic_constraints": [c["constraint_id"]
                                     for c in state["semantic_constraints"]["constraints"]],
        "cross_lingual_mapping_ids": [m["mapping_id"] for m in state["cross_lingual"]["mappings"]],
        "validator_unweakened": state["unweakened"],
        "remediation_gate": state["gate"],
        "attempt_gate": state.get("attempt_gate"),
        "frozen_integrity": {
            "remediation_freeze": {k: v for k, v in state["freeze"].items()
                                   if k != "checks_by_name"},
            "upstream": state["upstream_integrity"],
            "all_unchanged": state["freeze"]["all_unchanged"]
            and state["upstream_integrity"]["all_unchanged"],
        },
        "validation_failure_histogram": result.failure_histogram if result else None,
        "validation_failure_codes": result.failure_codes if result else None,
        "rejected_unit_ids": result.rejected_unit_ids if result else None,
        "attempt_2_units": state.get("attempt_audit", {}).get("totals", {}).get("units"),
        "attempt_2_material_units": state.get("attempt_audit", {})
        .get("totals", {}).get("material_units"),
        "attempt_2_failed_units": len(result.rejected_unit_ids) if result else None,
        "language_audit": state.get("language_audit"),
        "condition_audit": {k: v for k, v in (state.get("condition_audit") or {}).items()
                            if k != "rows"},
        "qualifier_audit": {k: v for k, v in (state.get("qualifier_audit") or {}).items()
                            if k != "rows"},
        "known_rules": state["known_rules"],
        "audit": state.get("attempt_audit"),
        "implementation": str(CONTROLLER_PATH.relative_to(ROOT)),
        "implementation_sha": sha_file(CONTROLLER_PATH),
        "remaining_limitations": state["limitations"],
        "pilot_status": state["pilot_status"],
        "status": state["status"],
        "final_decision": state["final_decision"],
        "next_phase": state["next_phase"],
    }
    write_json(MANIFEST_PATH, manifest)
    return manifest


# ================================================================ 15. runner

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gates-only", action="store_true",
                        help="author the remediation artifacts and run every gate, but never "
                             "generate. Use to inspect the gate before spending the one "
                             "authorised attempt.")
    args = parser.parse_args(argv)

    started = now()
    points_before = qdrant_points()
    for directory in ("audits", "contracts", "fixtures", "raw", "accepted", "rejected"):
        (REMEDIATION_DIR / directory).mkdir(parents=True, exist_ok=True)

    allowlist = {row["claim_id"]: row for row in read_jsonl(ALLOWLIST_PATH)}
    controller = drafting_controller()
    v1 = validator_v1()
    v11 = validator_v1_1()
    lang = language_validator()

    # ---- 1. freeze the failed pilot before touching anything
    historical_raw, historical_ir = historical_draft_ir()
    freeze = build_freeze_record(historical_raw, historical_ir)
    freeze["checks_by_name"] = {c["name"]: c for c in freeze["checks"]}
    write_json(FREEZE_PATH, {k: v for k, v in freeze.items() if k != "checks_by_name"})

    # ---- 2. root-cause audit, against the input the writer actually received
    plan_v1 = json.loads(DRAFT_PLAN_V1_PATH.read_text(encoding="utf-8"))
    payload_v1 = controller.build_generation_payload(plan_v1, allowlist)
    root_cause = build_root_cause_audit(historical_ir, allowlist, payload_v1)
    write_json(ROOT_CAUSE_PATH, root_cause)

    # ---- 3. author the remediation artifacts (deterministic; re-running rewrites identical bytes)
    constraints_doc = build_semantic_constraints()
    mappings_doc = build_cross_lingual_mappings()
    language_contract = lang.build_contract(LANGUAGE)
    write_json(SEMANTIC_CONSTRAINTS_PATH, constraints_doc)
    write_json(CROSS_LINGUAL_PATH, mappings_doc)
    write_json(LANGUAGE_CONTRACT_PATH, language_contract)
    write_json(VALIDATION_CONTRACT_V1_1_PATH, build_validation_contract_v1_1())
    plan = build_draft_plan_v1_1(constraints_doc, mappings_doc, allowlist)
    write_json(DRAFT_PLAN_V1_1_PATH, plan)

    bundle = v11.load_bundle()
    constraints = constraints_doc["constraints"]
    mapping_check = v11.mapping_consistency(bundle, mappings_doc["mappings"])

    # ---- 4. regression
    all_fixtures = read_jsonl(FIXTURES_PATH)
    historical_fixtures = historical_unit_fixtures(historical_ir)
    fixture_result = v11.run_fixtures(all_fixtures + historical_fixtures, bundle,
                                      language_contract, constraints)
    historical_regression = v11.run_fixtures(historical_fixtures, bundle, language_contract,
                                             constraints)
    corrected = [f for f in all_fixtures if f.get("category") == "corrected_synthetic"]
    corrected_synthetics = v11.run_fixtures(corrected, bundle, language_contract, constraints)
    v1_regression = run_v1_fixtures_under_v1_1(bundle, language_contract, constraints)
    citation_fixtures = renderer().run_fixtures(read_jsonl(CITATION_FIXTURES_PATH))
    write_json(FIXTURE_RESULT_PATH, {
        "version": REMEDIATION_VERSION,
        "remediation_fixtures": fixture_result,
        "historical_unit_regression": historical_regression,
        "corrected_synthetics": corrected_synthetics,
        "v1_fixtures_under_v1_1": v1_regression,
        "citation_fixtures": {k: v for k, v in citation_fixtures.items() if k != "rows"},
        "mapping_consistency": mapping_check,
    })

    historical_tests = run_tests(HISTORICAL_SUITES)
    new_tests = run_tests(NEW_SUITES)
    upstream_integrity = controller.verify_frozen_integrity()
    unweakened = validator_v1_unweakened()

    state: dict[str, Any] = {
        "started_at": started, "allowlist": allowlist, "freeze": freeze,
        "root_cause": root_cause, "semantic_constraints": constraints_doc,
        "cross_lingual": mappings_doc, "language_contract": language_contract, "plan": plan,
        "mapping_consistency": mapping_check, "fixture_result": fixture_result,
        "historical_regression": historical_regression,
        "corrected_synthetics": corrected_synthetics, "v1_regression": v1_regression,
        "citation_fixtures": citation_fixtures, "historical_tests": historical_tests,
        "new_tests": new_tests, "upstream_integrity": upstream_integrity,
        "unweakened": unweakened, "generation_calls": 0, "limitations": list(LIMITATIONS),
        "known_rules": {k: "NOT_EVALUATED" for k in
                        ("cm_15_mm_150", "dosage_350_400", "c25_30", "cf_p0_001", "syn_001")},
        "historical_totals": {
            "units": len(historical_ir.units),
            "material_units": sum(1 for u in historical_ir.units if u.material),
            "validated": len(historical_ir.units) - len(FAILED_UNIT_IDS),
            "failure_codes": sorted({code for row in root_cause["failed_units"]
                                     for code in row["failure_codes"]}),
        },
    }

    gate = remediation_gate(state)
    state["gate"] = gate

    if not gate["go"]:
        state.update({
            "pilot_status": "NOT_ATTEMPTED",
            "status": "closed_no_go",
            "final_decision": "SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / NO-GO",
            "executive_summary": (
                f"The remediation gate failed on: {gate['failed']}. No generation was attempted "
                f"and nothing was rendered (§63)."),
            "next_phase": (f"Repair the failed remediation gates ({', '.join(gate['failed'])}), "
                           f"then re-run this phase."),
        })
        write_manifest(state, points_before)
        write_report(state)
        _post_run(state, points_before)
        return 1

    if args.gates_only:
        state.update({
            "pilot_status": "NOT_ATTEMPTED",
            "status": "closed_go",
            "final_decision": ("SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO "
                               "(attempt #2 deferred)"),
            "executive_summary": ("Every remediation gate passed. Generation was skipped by "
                                  "request; the one authorised attempt is still available."),
            "next_phase": "Re-run without --gates-only to spend pilot attempt #2.",
        })
        write_manifest(state, points_before)
        write_report(state)
        _post_run(state, points_before)
        return 0

    # ---- 5. the one authorised generation
    payload = build_generation_payload_v1_1(plan, allowlist)
    if RAW_ATTEMPT_2_PATH.exists():
        # §81 across runs, not just within one. The attempt was spent; re-running this phase
        # replays it rather than quietly buying a second sample of the same configuration.
        raw = json.loads(RAW_ATTEMPT_2_PATH.read_text(encoding="utf-8"))
        if sha_text(raw["raw_text"]) != raw["raw_text_sha256"]:
            print("preserved attempt #2 output does not match its recorded SHA", file=sys.stderr)
            return 2
        state["replayed"] = True
        state["generation_calls"] = 0
    else:
        raw = generate_attempt_2(payload)
        write_json(RAW_ATTEMPT_2_PATH, raw)          # preserved before parsing, per §67
        state["generation_calls"] = 1
    state["raw"] = raw

    if raw.get("finish_reason") == "length":
        ir, schema_error = None, (
            f"output was truncated at the token ceiling (finish_reason='length', "
            f"{raw.get('usage', {}).get('completion_tokens')} completion tokens against a "
            f"{MAX_TOKENS}-token budget)")
    else:
        try:
            ir = v1.parse_draft_ir(controller.extract_json_object(raw["raw_text"]))
            schema_error = None
        except v1.DraftSchemaError as error:
            ir, schema_error = None, str(error)

    if ir is None:
        state.update({
            "no_validation_reason": f"SCHEMA_INVALID: {schema_error}",
            "pilot_status": "SEC-02-2 PILOT_DRAFT_REJECTED",
            "status": "closed_go",
            "final_decision": ("SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO; "
                               "SEC-02-2 PILOT ATTEMPT #2 — REJECTED"),
            "executive_summary": (
                f"Every remediation gate passed. The one authorised generation returned output "
                f"that is not a DraftIR: {schema_error}. There is no repair path and no retry."),
            "next_phase": "SEC-02-2 DRAFT FAILURE ANALYSIS V2 (failure code: SCHEMA_INVALID)",
        })
        write_json(REJECTED_PATH, {"version": REMEDIATION_VERSION, "attempt": 2,
                                   "draft_id": DRAFT_ID, "rejected_at": now(),
                                   "failure_codes": ["SCHEMA_INVALID"],
                                   "schema_error": schema_error,
                                   "raw_text_sha256": raw["raw_text_sha256"],
                                   "rendered": False, "regenerated": False})
        write_manifest(state, points_before)
        write_report(state)
        _post_run(state, points_before)
        return 1

    # ---- 6. validation: v1.1 (which runs v1 verbatim, language, semantics and composition)
    result = v11.validate_draft(ir, bundle, language_contract, constraints)
    state["validation"] = result
    state["language_audit"] = language_audit(ir, language_contract)
    state["condition_audit"] = condition_audit(ir, allowlist, bundle)
    state["qualifier_audit"] = qualifier_audit(ir, allowlist, bundle, constraints)
    state["known_rules"] = check_known_rules(ir, result)

    markdown = entries = render_audit = None
    determinism_ok = None
    registry = v1.load_source_registry()
    if result.status == "ACCEPT":
        markdown, entries = renderer().render(ir, registry)
        second, _ = renderer().render(ir, registry)
        determinism_ok = markdown == second
        render_audit = renderer().audit_rendered(markdown, entries)
        state.update({"markdown": markdown, "render_audit": render_audit,
                      "determinism_ok": determinism_ok})

    audit = controller.build_draft_audit(ir, result, entries or [], allowlist, plan, markdown)
    state["attempt_audit"] = audit
    attempt = attempt_gate(result, audit, markdown, render_audit, determinism_ok,
                           state["language_audit"], state["condition_audit"],
                           state["qualifier_audit"])
    state["attempt_gate"] = attempt

    remediation_audit = {
        "version": REMEDIATION_VERSION, "section_id": SECTION_ID, "audited_at": now(),
        "historical_failed_units": list(FAILED_UNIT_IDS),
        "root_causes": {row["unit_id"]: {"primary": row["root_cause_class"],
                                         "classes": row["root_cause_classes"]}
                        for row in root_cause["failed_units"]},
        "new_semantic_constraints": [c["constraint_id"] for c in constraints],
        "new_language_rules": ["LANG-001 section-language match", "LANG-002 fail closed on "
                                                                 "undetermined material unit"],
        "new_failure_codes": ["LANGUAGE_MISMATCH", "LANGUAGE_AMBIGUOUS",
                              "SEMANTIC_SCOPE_MISMATCH"],
        "new_fixtures": fixture_result["total"],
        "historical_tests_run": historical_tests["tests_run"],
        "new_tests_run": new_tests["tests_run"],
        "language_validation_results": state["language_audit"],
        "condition_validation_results": {k: v for k, v in state["condition_audit"].items()
                                         if k != "rows"},
        "qualifier_validation_results": {k: v for k, v in state["qualifier_audit"].items()
                                         if k != "rows"},
        "generation_attempts_in_this_phase": 1 if RAW_ATTEMPT_2_PATH.exists() else 0,
        "generation_calls_in_this_run": state["generation_calls"],
        "attempt_2_units": audit["totals"]["units"],
        "attempt_2_material_units": audit["totals"]["material_units"],
        "attempt_2_failed_units": len(result.rejected_unit_ids),
        "attempt_2_failed_unit_ids": result.rejected_unit_ids,
        "required_topic_coverage": audit["required_topic_coverage"],
        "required_topics_covered": audit["required_topics_covered"],
        "citation_coverage": audit["citation_coverage"],
        "language_compliance": state["language_audit"]["compliance"],
        "condition_compliance": state["condition_audit"]["preservation"],
        "qualifier_compliance": state["qualifier_audit"]["preservation"],
        "composition_failures": sum(result.failure_histogram.get(code, 0) for code in
                                    ("FORBIDDEN_SYNTHESIS", "UNSUPPORTED_RELATION",
                                     "DERIVED_VALUE_AS_SOURCE_STATED", "CLAIM_NOT_ALLOWLISTED",
                                     "CLAIM_DENYLISTED")),
        "numeric_failures": sum(result.failure_histogram.get(code, 0) for code in
                                ("NUMERIC_DRIFT", "UNIT_DRIFT")),
        "citation_failures": sum(result.failure_histogram.get(code, 0) for code in
                                 ("MISSING_CITATION", "MISSING_SOURCE_KEY", "UNKNOWN_SOURCE_KEY",
                                  "CITATION_SCOPE_MISMATCH")),
        "known_rules": state["known_rules"],
        "attempt_gate": attempt,
        "pilot_accepted": attempt["accept"],
    }
    write_json(REMEDIATION_AUDIT_PATH, remediation_audit)

    if attempt["accept"]:
        write_json(ACCEPTED_IR_PATH, ir.as_dict())
        RENDERED_PATH.parent.mkdir(parents=True, exist_ok=True)
        RENDERED_PATH.write_text(markdown, encoding="utf-8")
        write_json(CITATION_MAP_PATH, {
            "version": "tunnelbook-book-citation-rendering-contract-v1",
            "section_id": SECTION_ID, "draft_id": ir.draft_id,
            "entries": [e.__dict__ for e in entries]})
        state.update({
            "pilot_status": "SEC-02-2 PILOT_DRAFT_ACCEPTED",
            "status": "closed_go",
            "final_decision": ("SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO; "
                               "SEC-02-2 PILOT_DRAFT_ACCEPTED (NOT FINAL MANUSCRIPT)"),
            "executive_summary": (
                f"Both historical failures were root-caused, per-unit language validation was "
                f"added, and every gate passed without weakening a rule. The one authorised "
                f"generation produced a DraftIR whose {audit['totals']['material_units']} "
                f"material units all validated across eleven stages, in Turkish throughout, with "
                f"every condition and qualifier preserved. It rendered deterministically to "
                f"Markdown with {audit['totals']['citations_rendered']} registry-backed "
                f"references. It is a pilot draft, not publishable text."),
            "next_phase": ("SEC-02-2 TECHNICAL DRAFT AUDIT V1 + BOOK STYLE CONTRACT V1. Human "
                           "technical editorial review becomes reachable; it has not happened."),
        })
    else:
        write_json(REJECTED_PATH, {
            "version": REMEDIATION_VERSION, "attempt": 2, "draft_id": DRAFT_ID,
            "rejected_at": now(), "raw_text_sha256": raw["raw_text_sha256"],
            "status": result.status, "failure_codes": result.failure_codes,
            "failure_histogram": result.failure_histogram,
            "rejected_unit_ids": result.rejected_unit_ids,
            "rejected_units": [u.__dict__ for u in result.units if u.status == "REJECT"],
            "attempt_gate": attempt, "language_audit": state["language_audit"],
            "rendered": False, "regenerated": False,
            "note": "No repair, no translation, no deletion, no second attempt (§68, §80, §81)."})
        state.update({
            "pilot_status": "SEC-02-2 PILOT_DRAFT_REJECTED",
            "status": "closed_go",
            "final_decision": ("SEC-02-2 DRAFT FAILURE REMEDIATION V1 — CLOSED / GO; "
                               "SEC-02-2 PILOT ATTEMPT #2 — REJECTED"),
            "executive_summary": (
                f"Both historical failures were root-caused and every remediation gate passed. "
                f"The one authorised generation produced a schema-valid DraftIR whose prose did "
                f"not validate: {len(result.rejected_unit_ids)} of {audit['totals']['units']} "
                f"units were rejected with codes {result.failure_codes}. Nothing was rendered, "
                f"nothing was repaired and no second attempt was taken."),
            "next_phase": ("SEC-02-2 DRAFT FAILURE ANALYSIS V2, using the exact attempt #2 "
                           "failure codes recorded in the rejection artifact."),
        })

    write_manifest(state, points_before)
    write_report(state)
    _post_run(state, points_before)
    return 0 if attempt["accept"] else 1


def _post_run(state: dict[str, Any], points_before: int | None) -> None:
    """Re-run the suites now that this run's artifacts exist, and record what they say.

    This cannot be a pre-generation gate: it asserts the shape of files the run has not written
    yet, so gating on it would read a stale copy or fail forever on a first run. It runs after,
    and the manifest is rewritten with its result rather than left claiming a pass nobody checked.
    """
    post = run_tests(NEW_SUITES)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["post_run_tests"] = {k: v for k, v in post.items() if k != "tail"}
    manifest["post_run_tests_tail"] = post["tail"]
    manifest["test_counts"]["post_run_tests_run"] = post["tests_run"]
    manifest["test_counts"]["post_run_status"] = post["status"]
    if post["status"] != "passed":
        manifest["status"] = "closed_no_go"
        manifest["final_decision"] = (
            f"{manifest['final_decision']} — INVALIDATED: the post-run artifact audit failed "
            f"({post['tail'][-1] if post['tail'] else 'see suite output'})")
        state["final_decision"] = manifest["final_decision"]
        state["status"] = "closed_no_go"
    write_json(MANIFEST_PATH, manifest)
    state["post_run_tests"] = post
    write_report(state)


if __name__ == "__main__":
    sys.exit(main())
