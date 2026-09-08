"""SEC-02-2 Draft Failure Analysis v2 - why attempt #2's two units failed.

Analysis only. This phase generates nothing, retrieves nothing, writes nothing to Qdrant and
weakens no rule. It reads attempt #1 and attempt #2 as immutable evidence, reconstructs what the
writer was actually given, and decides - against the frozen validator, not against an opinion -
which of the candidate explanations the evidence supports.

The two questions, and the way each is settled:

  U-A-P01-S02 / SEC-02-2-C-002, QUALIFIER_DROPPED. Settled by reconstructing the attempt-#2
  generation payload from the frozen plan and allowlist. If the qualifier and DSC-C002-001 are
  in it, payload omission is out and the question becomes why data the writer held did not reach
  the prose. The census of verbatim canonical copies answers that.

  U-C-P01-S02 / SEC-02-2-P0-008, UNSUPPORTED_PROPOSITION. Settled by enumerating what the frozen
  glosses already license. If a natural Turkish rendering exists inside the current pool, the
  defect is the writer's vocabulary choice and the gloss set is not too narrow. Nothing here
  widens the pool; the probes only read it.

The probe strings below are validator inputs, not draft prose. They exist to answer "was a
compliant rendering reachable", they are recorded as analysis evidence, and nothing authorises
reusing them as text. Attempt #3 is not generated here and is not authorised here.
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

VERSION = "tunnelbook-sec-02-2-draft-failure-analysis-v2"
SECTION_ID = "SEC-02-2"
DRAFT_ID = "SEC-02-2-PILOT-V1-1"

BOOK = ROOT / "data" / "book"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
REMEDIATION = SECTION_DIR / "remediation_v1"
ANALYSIS = SECTION_DIR / "analysis_v2"
MANIFESTS = BOOK / "manifests"
METADATA = ROOT / "data" / "metadata"

# ---- immutable evidence. Read, hashed, never written.
RAW_ATTEMPT_1 = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"
RAW_ATTEMPT_2 = REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_2.json"
REJECTED_2 = REMEDIATION / "rejected" / "pilot_attempt_2_validation.json"
REMEDIATION_AUDIT = REMEDIATION / "audits" / "sec_02_2_remediation_audit_v1.json"
ROOT_CAUSE_V1 = REMEDIATION / "audits" / "pilot_failure_root_cause_v1.json"
SEMANTIC_CONSTRAINTS = REMEDIATION / "contracts" / "draft_semantic_constraints_v1.json"
CROSS_LINGUAL = REMEDIATION / "contracts" / "cross_lingual_condition_mappings_v1.json"
DRAFTING_CONTRACT = CONTRACTS / "section_drafting_contract_v1.json"
PLAN_V1_1 = SECTION_DIR / "draft_plan_v1_1.json"
PROMPT_V1_1 = METADATA / "section_drafting_system_prompt_v1_1.txt"
VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
VALIDATOR_V1_1 = ROOT / "scripts" / "52_section_draft_validator_v1_1.py"
REMEDIATION_CONTROLLER = ROOT / "scripts" / "50_sec_02_2_draft_failure_remediation_v1.py"
REMEDIATION_MANIFEST = MANIFESTS / "sec_02_2_draft_failure_remediation_v1.json"

FROZEN_INPUTS = {
    "attempt_1_raw": RAW_ATTEMPT_1,
    "attempt_2_raw": RAW_ATTEMPT_2,
    "attempt_2_rejection": REJECTED_2,
    "remediation_audit": REMEDIATION_AUDIT,
    "root_cause_v1": ROOT_CAUSE_V1,
    "semantic_constraints_v1": SEMANTIC_CONSTRAINTS,
    "cross_lingual_mappings_v1": CROSS_LINGUAL,
    "section_drafting_contract_v1": DRAFTING_CONTRACT,
    "draft_plan_v1_1": PLAN_V1_1,
    "drafting_prompt_v1_1": PROMPT_V1_1,
    "draft_validator_v1": VALIDATOR_V1,
    "draft_validator_v1_1": VALIDATOR_V1_1,
    "remediation_controller": REMEDIATION_CONTROLLER,
    "remediation_manifest_v1": REMEDIATION_MANIFEST,
}

# ---- authored by this phase.
FAILURE_ANALYSIS_PATH = ANALYSIS / "audits" / "attempt_2_failure_analysis_v1.json"
MANIFEST_PATH = MANIFESTS / "sec_02_2_draft_failure_analysis_v2.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_draft_failure_analysis_v2.md"

FAILED_UNITS = ("U-A-P01-S02", "U-C-P01-S02")

# A root cause is one of these. Free text explains; a class commits.
ROOT_CAUSE_CLASSES = (
    "CLAIM_QUALIFIER_REPRESENTATION_MISMATCH",   # (a)
    "GENERATION_PAYLOAD_OMISSION",               # (b)
    "PROMPT_COMPLIANCE_FAILURE",                 # (c)
    "VALIDATOR_SEMANTIC_BOUNDARY_DEFECT",        # (d)
    "WRITER_VOCABULARY_CHOICE",                  # (e), U-C
    "GLOSS_COVERAGE_DEFECT",                     # (e), U-C
    "PLAN_UNIT_ALLOCATION_DEFECT",               # (e), U-A
)

# Validator probes. Analysis inputs, not draft prose - see the module docstring.
PROBE_NOTE = ("Validator probe strings. They answer whether a compliant rendering was reachable "
              "under the frozen rules. They are not draft prose, they are not attempt #3, and "
              "nothing in this phase authorises reusing them as text.")

C002_PROBES = {
    # Does the qualifier's own meaning fit in one unit together with the numbers?
    "C002_single_unit_combined":
        "Tablo-351-5, C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerinde kabul "
        "kriteridir: bireysel minimum dayanım 22,5 MPa ve üç adet numuneden oluşan grubun "
        "ortalama minimum dayanımı 25,5 MPa'dır.",
    # Does a dedicated identity/scope unit fit, carrying C-002's own conditions?
    "C002_identity_unit":
        "Tablo-351-5, C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerinde kalite "
        "kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul kriteridir.",
    # The bare qualifier, to show what the split costs if the conditions are not carried with it.
    "C002_identity_unit_without_conditions":
        "Tablo-351-5 kalite kontrol kriterleridir; dayanım sınıfının kendisi değil, kabul "
        "kriteridir.",
}

P0_008_PROBES = {
    "P0008_attempt_2_actual":
        "Tünel boyutuna bağlı olarak, ezilmiş veya sıkışan kaya gibi bazı spesifik kayaç "
        "koşullarında kalınlık 12 inç (300 mm) ve daha fazla olabilir.",
    "P0008_kaya_for_kayac":
        "Tünel boyutuna bağlı olarak, ezilmiş veya sıkışan kaya gibi bazı kaya koşullarında "
        "kalınlık 12 inç (300 mm) ve daha fazla olabilir.",
    "P0008_belirli":
        "Tünel boyutuna bağlı olarak, ezilmiş veya sıkışan kaya gibi belirli kaya koşullarında "
        "kalınlık 12 inç (300 mm) ve daha fazla olabilir.",
    "P0008_bazi_belirli":
        "Tünel boyutuna bağlı olarak, ezilmiş veya sıkışan kaya gibi bazı belirli kaya "
        "koşullarında kalınlık 12 inç (300 mm) ve daha fazla olabilmektedir.",
}

# The words the rejection named, and the licensed neighbours they were chosen over.
CONTESTED_WORDS = ("kayaç", "spesifik")
LICENSED_NEIGHBOURS = ("kaya", "bazı", "belirli")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_file(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_MODULES: dict[str, Any] = {}


def module(key: str, path: Path):
    if key not in _MODULES:
        _MODULES[key] = _load(key, path)
    return _MODULES[key]


def v1():
    return module("analysis_v2_validator_v1", VALIDATOR_V1)


def v11():
    return module("analysis_v2_validator_v1_1", VALIDATOR_V1_1)


def controller():
    return module("analysis_v2_remediation", REMEDIATION_CONTROLLER)


# ================================================================ 1. evidence

def freeze_check() -> dict[str, Any]:
    """Every input this analysis rests on, hashed as read. Nothing here is written back."""
    rows = {name: sha_file(path) for name, path in FROZEN_INPUTS.items()}
    missing = sorted(name for name, sha in rows.items() if sha is None)
    return {"sha256": rows, "missing": missing, "all_present": not missing}


def attempt_2_ir() -> tuple[dict, dict]:
    raw = json.loads(RAW_ATTEMPT_2.read_text(encoding="utf-8"))
    return raw, json.loads(raw["raw_text"])


def paragraph_text(ir: dict, prefix: str) -> str:
    return " ".join(u["text"] for u in ir["units"] if u["unit_id"].startswith(prefix))


def verbatim_census(ir: dict, allowlist: dict[str, dict]) -> dict[str, Any]:
    """How much of attempt #2 is the canonical claim, copied.

    This is the load-bearing measurement of the phase. A writer that reproduces the claim's own
    sentence cannot add a qualifier the sentence does not contain, whatever the payload says
    about qualifiers being mandatory - so the copy rate decides whether U-A-P01-S02 is a
    compliance failure or a representation failure.
    """
    rows = []
    for unit in ir["units"]:
        if len(unit.get("claim_ids") or []) != 1:
            continue
        claim = allowlist.get(unit["claim_ids"][0])
        if claim is None:
            continue
        canonical = claim.get("canonical_claim") or ""
        rows.append({
            "unit_id": unit["unit_id"], "claim_id": unit["claim_ids"][0],
            "verbatim_canonical": unit["text"] == canonical,
            "claim_language": "en" if claim.get("canonical_claim_language") == "en"
            else ("en" if unit["claim_ids"][0] in
                  (v1().load_bundle().contract.get("translation_glosses") or {}) else "tr"),
        })
    verbatim = [r for r in rows if r["verbatim_canonical"]]
    composed = [r for r in rows if not r["verbatim_canonical"]]
    return {
        "single_claim_units": len(rows), "verbatim_units": len(verbatim),
        "composed_units": len(composed),
        "verbatim_rate": f"{len(verbatim) / len(rows):.0%}" if rows else "n/a",
        "verbatim_unit_ids": [r["unit_id"] for r in verbatim],
        "composed_unit_ids": [r["unit_id"] for r in composed],
        "composed_claim_languages": sorted({r["claim_language"] for r in composed}),
        "rows": rows,
        "finding": ("Every unit whose canonical claim was already Turkish is a byte-identical "
                    "copy of it. The only composed units are the two whose claims are English "
                    "and could not be copied. The writer composes when copying is impossible and "
                    "not otherwise."),
    }


def unit_to_claim_allocation(ir: dict, plan: dict) -> dict[str, Any]:
    allocated = [cid for sub in plan["subsections"] for cid in sub["claim_ids"]]
    material = [u for u in ir["units"] if u.get("material")]
    per_claim: dict[str, list[str]] = {}
    for unit in material:
        for claim_id in unit.get("claim_ids") or []:
            per_claim.setdefault(claim_id, []).append(unit["unit_id"])
    return {
        "allocated_claims": len(allocated), "material_units": len(material),
        "units_per_claim": {k: len(v) for k, v in sorted(per_claim.items())},
        "max_units_per_claim": max((len(v) for v in per_claim.values()), default=0),
        "plan_allocates_units": False,
        "finding": ("The plan allocates claims to subsections, never claims to units. The writer "
                    "resolved that freedom into a strict one-unit-per-claim section, which is "
                    "what the frozen prompt's CÜMLE YOĞUNLUĞU rule asks for. A claim whose "
                    "mandatory qualifier does not fit its own sentence therefore has nowhere to "
                    "put it."),
    }


def payload_reconstruction(plan: dict, allowlist: dict[str, dict]) -> dict[str, Any]:
    """What the writer was actually handed for SEC-02-2-C-002 and SEC-02-2-P0-008.

    Rebuilt from the frozen plan and allowlist through the frozen builder, so this is the payload
    attempt #2 saw unless the plan or allowlist changed - and the freeze check says they did not.
    """
    payload = controller().build_generation_payload_v1_1(plan, allowlist)
    claims = {c["claim_id"]: c for sub in payload["subsections"] for c in sub["claims"]}
    c002, p0008 = claims["SEC-02-2-C-002"], claims["SEC-02-2-P0-008"]
    return {
        "rebuilt_payload_sha256": sha_text(controller().canonical_json(payload)),
        "SEC-02-2-C-002": {
            "canonical_claim_supplied": bool(c002.get("canonical_claim")),
            "canonical_claim_is_a_complete_target_language_sentence": True,
            "conditions_supplied": list(c002.get("conditions") or []),
            "qualifiers_supplied": list(c002.get("qualifiers") or []),
            "qualifiers_are_mandatory_flag": c002.get("qualifiers_are_mandatory"),
            "semantic_constraint_ids": [c["constraint_id"]
                                        for c in c002.get("semantic_constraints") or []],
            "required_meaning_supplied": [c.get("required_meaning")
                                          for c in c002.get("semantic_constraints") or []],
            "required_action_supplied": [c.get("required_action")
                                         for c in c002.get("semantic_constraints") or []],
            "unit_slot_for_the_qualifier": False,
        },
        "SEC-02-2-P0-008": {
            "canonical_claim_supplied": bool(p0008.get("canonical_claim")),
            "canonical_claim_language": p0008.get("language"),
            "translation_required_instruction": bool(p0008.get("translation_required")),
            "approved_condition_renderings_supplied": True,
            "licensed_vocabulary_supplied": False,
            "note": ("The payload names approved renderings for the two conditions and says the "
                     "claim must be translated. It never states the vocabulary the support "
                     "validator will accept for the rest of the sentence, although that "
                     "vocabulary is already frozen in the contract's translation_glosses."),
        },
        "payload_omission_for_C_002": False,
        "payload_omission_for_P0_008": "partial: glosses exist but are not exposed to the writer",
    }


def qualifier_survival_evidence(ir: dict, allowlist: dict[str, dict], bundle: Any) -> dict:
    """Both qualifiers in the section, scored by stage E's own rule.

    Recomputed rather than quoted, because the interesting result is one the attempt-#2 audit
    reports as a pass.
    """
    rem, base = controller(), v1()
    rows = []
    for claim_id, prefix in (("SEC-02-2-C-002", "U-A-P01"), ("SEC-02-2-C-009", "U-D-P01")):
        claim = allowlist[claim_id]
        paragraph = paragraph_text(ir, prefix)
        present = set(base.tokens(paragraph))
        canonical = set(base.tokens(claim.get("canonical_claim") or ""))
        for row in rem._qualifier_survival(claim, paragraph, bundle):
            # An anchor the claim's own sentence already contains proves nothing: a verbatim copy
            # supplies it for free. Only the anchors that distinguish the qualifier from the
            # sentence can show the qualifier was actually stated.
            distinguishing = [a for a in row["anchors"]
                              if not any(base.prefix_agreement(a, c) for c in canonical)]
            surviving = [a for a in distinguishing
                         if any(base.prefix_agreement(a, h) for h in present)]
            rows.append({
                "claim_id": claim_id, "qualifier": row["qualifier"],
                "anchors": len(row["anchors"]), "surviving_anchors": len(row["surviving_anchors"]),
                "distinguishing_anchors": distinguishing,
                "surviving_distinguishing_anchors": surviving,
                "missing_distinguishing_anchors": [a for a in distinguishing
                                                   if a not in surviving],
                "stage_e_preserved": row["preserved"],
                # All of them, not any. A qualifier's meaning needs its distinguishing vocabulary
                # entire; one word of it surviving is as likely to be a neighbouring claim's word
                # as the qualifier's - 'kalınlığı' here comes from SEC-02-2-C-006's sentence.
                "qualifier_meaning_actually_stated": bool(distinguishing) and not [
                    a for a in distinguishing if a not in surviving],
            })
    return {
        "rows": rows,
        "stage_e_preservation": f"{sum(1 for r in rows if r['stage_e_preserved'])}/{len(rows)}",
        "meaning_realised": f"{sum(1 for r in rows if r['qualifier_meaning_actually_stated'])}/"
                            f"{len(rows)}",
        "finding": ("SEC-02-2-C-009's qualifier scores 5 of 6 anchors and passes stage E, but the "
                    "meaning it carries - that §351.08.10.02 is specific to clay zones and is not "
                    "the general first-layer thickness - is nowhere in the paragraph. It passes "
                    "because its anchors are the claim's own words, which a verbatim copy "
                    "supplies for free. Its one surviving distinguishing anchor, 'kalınlığı', "
                    "comes from SEC-02-2-C-006's sentence in the same paragraph, not from the "
                    "qualifier. Attempt #2 therefore realised 0 of 2 qualifiers, not 1 of 2. "
                    "This is a permissiveness gap in stage E's anchor-overlap test, not a "
                    "reason to loosen anything, and tightening it is a separate phase."),
        "recorded_but_not_actioned": True,
    }


# ================================================================ 2. probes

def probe_c002(bundle: Any) -> dict[str, Any]:
    """Was any compliant rendering of SEC-02-2-C-002 reachable under the frozen validator?"""
    base, val = v1(), v11()
    constraints = val.load_semantic_constraints()
    claim = bundle.allowlist["SEC-02-2-C-002"]
    canonical, source_keys = claim["canonical_claim"], list(claim["source_keys"])
    s01 = bundle.allowlist["SEC-02-2-C-001"]["canonical_claim"]

    def unit(unit_id: str, text: str):
        return base.DraftUnit(
            unit_id=unit_id, unit_type="PARAGRAPH_SENTENCE", text=text, material=True,
            claim_ids=["SEC-02-2-C-002"], source_keys=source_keys,
            relationship_type="INDEPENDENT",
            citation_intents=[{"claim_id": "SEC-02-2-C-002", "source_keys": source_keys}])

    def codes(unit_id: str, text: str, paragraph: str) -> list[dict]:
        return [{"code": f.code, "stage": f.stage, "rule_id": f.rule_id}
                for f in val.validate_unit(unit(unit_id, text), paragraph, bundle,
                                           constraints=constraints)]

    scenarios = {}
    # 1. attempt #2 as it stands.
    para_actual = f"{s01} {canonical}"
    scenarios["attempt_2_as_written"] = {
        "shape": "one unit, canonical claim copied verbatim",
        "units": {"U-A-P01-S02": codes("U-A-P01-S02", canonical, para_actual)},
    }
    # 2. one unit carrying identity and numbers together.
    combined = C002_PROBES["C002_single_unit_combined"]
    para_combined = f"{s01} {combined}"
    scenarios["single_unit_combined"] = {
        "shape": "one unit carrying the acceptance-table identity and the numeric criteria",
        "units": {"U-A-P01-S02": codes("U-A-P01-S02", combined, para_combined)},
    }
    # 3. two bound units: identity/scope, then the numbers.
    identity = C002_PROBES["C002_identity_unit"]
    para_split = f"{s01} {identity} {canonical}"
    scenarios["two_bound_units"] = {
        "shape": "identity/scope unit + numeric-criteria unit, both declaring SEC-02-2-C-002",
        "units": {"U-A-P01-S02": codes("U-A-P01-S02", identity, para_split),
                  "U-A-P01-S03": codes("U-A-P01-S03", canonical, para_split)},
    }
    # 4. the split done carelessly - the identity unit without the claim's own conditions.
    bare = C002_PROBES["C002_identity_unit_without_conditions"]
    para_bare = f"{s01} {bare} {canonical}"
    scenarios["two_units_identity_without_conditions"] = {
        "shape": "identity unit stripped of SEC-02-2-C-002's own conditions",
        "units": {"U-A-P01-S02": codes("U-A-P01-S02", bare, para_bare),
                  "U-A-P01-S03": codes("U-A-P01-S03", canonical, para_bare)},
    }
    for scenario in scenarios.values():
        scenario["accepts"] = all(not c for c in scenario["units"].values())
    return {
        "note": PROBE_NOTE, "probe_texts": C002_PROBES, "scenarios": scenarios,
        "finding": ("A compliant rendering was reachable in two different shapes, so the "
                    "validator is not demanding the impossible. It was not reachable by copying "
                    "the canonical sentence, which is the one thing the writer did for every "
                    "Turkish claim in the section. Splitting the claim across two units also "
                    "requires carrying its own conditions into the identity unit; done without "
                    "that, the split trades QUALIFIER_DROPPED for CONDITION_DROPPED."),
    }


def probe_p0_008(bundle: Any) -> dict[str, Any]:
    """Do the frozen glosses already license a natural Turkish rendering of SEC-02-2-P0-008?"""
    base = v1()
    pool = base.licensed_tokens(["SEC-02-2-P0-008"], bundle)
    probes = {name: {"unlicensed_content_words": base.unlicensed(text, pool, bundle)}
              for name, text in P0_008_PROBES.items()}
    for row in probes.values():
        row["licensed"] = not row["unlicensed_content_words"]
    words = {}
    for word in CONTESTED_WORDS + LICENSED_NEIGHBOURS:
        folded = base.fold(word)
        words[word] = {
            "licensed": any(base.prefix_agreement(folded, t) for t in pool),
            "in_function_lexicon": folded in bundle.function_lexicon,
        }
    glosses = bundle.contract["translation_glosses"]["SEC-02-2-P0-008"]
    return {
        "note": PROBE_NOTE, "probe_texts": P0_008_PROBES,
        "frozen_glosses": list(glosses), "pool_size": len(pool),
        "probes": probes, "words": words,
        "licensed_alternatives_that_existed": sorted(
            name for name, row in probes.items() if row["licensed"]),
        "finding": ("Three natural Turkish renderings are fully licensed by the glosses as they "
                    "stand. Each differs from what the writer produced only in using 'kaya' "
                    "where it wrote 'kayaç', and in dropping or replacing 'spesifik' with the "
                    "licensed 'belirli'. The rejected sentence itself contains the licensed "
                    "'kaya', three words from the unlicensed 'kayaç', so the writer had the "
                    "accepted form in hand and used both. 'kayaç' misses 'kaya' only because "
                    "prefix agreement needs five characters and 'kaya' has four; 'spesifik' "
                    "misses 'specific' because a borrowed cognate shares two leading characters "
                    "with its English source. Neither is evidence that the gloss set is too "
                    "narrow for a faithful rendering, because faithful renderings pass."),
    }


# ================================================================ 3. classification

def classify(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    payload = evidence["payload_reconstruction"]
    census = evidence["verbatim_census"]
    c002 = evidence["c002_probes"]
    p0008 = evidence["p0_008_probes"]
    alloc = evidence["unit_allocation"]

    u_a = {
        "unit_id": "U-A-P01-S02",
        "claim_ids": ["SEC-02-2-C-002"],
        "generated_text": evidence["failed_unit_texts"]["U-A-P01-S02"],
        "failure_codes": ["QUALIFIER_DROPPED"],
        "failing_stages": ["E_conditions", "K_semantic"],
        "rule_ids": [None, "DSC-C002-001"],
        "candidate_causes": {
            "a_canonical_claim_qualifier_representation_mismatch": "SUPPORTED - primary",
            "b_generation_payload_omission": "REFUTED",
            "c_prompt_compliance_failure": "CONTRIBUTING, not primary",
            "d_validator_semantic_boundary_design_issue": "REFUTED",
            "e_other": "SUPPORTED - plan allocates no unit slot for the qualifier",
        },
        "root_cause_class": "CLAIM_QUALIFIER_REPRESENTATION_MISMATCH",
        "secondary_class": "PLAN_UNIT_ALLOCATION_DEFECT",
        "root_cause": (
            "SEC-02-2-C-002's mandatory semantic content is split across two fields that share "
            "no vocabulary: a canonical_claim that is already a complete, copy-ready Turkish "
            "sentence, and a qualifier string whose meaning that sentence does not contain. The "
            "writer reproduced the canonical sentence byte-for-byte, as it did for "
            f"{census['verbatim_units']} of {census['single_claim_units']} single-claim units - "
            "every one whose claim was already Turkish. A mandatory-qualifier flag delivered "
            "beside a copy-ready sentence cannot change that output, because the compliant "
            "output is unreachable by reproduction and reachable only by composing past the "
            "canonical text. Nothing in the plan or the payload allocates a unit for the "
            "composed part, and the frozen prompt's one-proposition-per-sentence rule pushes "
            "against putting it in the claim's own sentence."),
        "evidence": {
            "payload_carried_qualifier_verbatim":
                payload["SEC-02-2-C-002"]["qualifiers_supplied"],
            "payload_carried_mandatory_flag":
                payload["SEC-02-2-C-002"]["qualifiers_are_mandatory_flag"],
            "payload_carried_constraint":
                payload["SEC-02-2-C-002"]["semantic_constraint_ids"],
            "payload_allocated_a_unit_for_it":
                payload["SEC-02-2-C-002"]["unit_slot_for_the_qualifier"],
            "verbatim_copy_rate": census["verbatim_rate"],
            "composed_units_were_only_the_untranslatable_ones":
                census["composed_unit_ids"],
            "units_per_claim_max": alloc["max_units_per_claim"],
            "qualifiers_actually_realised_in_attempt_2":
                evidence["qualifier_survival"]["meaning_realised"],
            "compliant_shapes_that_validate_today": sorted(
                name for name, s in c002["scenarios"].items() if s["accepts"]),
        },
        "validator_verdict_correct": True,
        "validator_verdict_reasoning": (
            "The paragraph states that Tablo-351-5 gives minimum strength values and never says "
            "the table is an acceptance criterion. A reader can take it as the table imposing "
            "the requirement, which is the meaning SEC-02-2-C-001 owns. Stage E and stage K "
            "fired independently on the same absence, and the probes show two compliant shapes "
            "the same rules accept, so the boundary is not drawn too tightly."),
        "smallest_safe_remediation": (
            "Plan change only. In a draft plan v1.2, allocate SEC-02-2-C-002 two bound unit "
            "slots in subsection A - (1) acceptance-table identity and scope, carrying the "
            "qualifier's meaning and the claim's own conditions, (2) the numeric acceptance "
            "criteria - both declaring SEC-02-2-C-002, both citing SRC-DOC000087-ea64db4f1a7f, "
            "both INDEPENDENT. Slot 1 has no canonical sentence to copy, so copying stops being "
            "an available strategy. No validator, threshold, failure code, claim, allowlist, "
            "gloss, prompt or frozen contract changes."),
        "remediation_is": "generic mechanism, SEC-02-2-specific instance",
        "remediation_generality": (
            "The mechanism - a claim carrying a non-empty qualifier whose anchors are absent "
            "from its canonical sentence gets an explicit qualifier unit slot - is general and "
            "applies to SEC-02-2-C-009 in the same section. Only the allocation itself is "
            "section-local."),
        "remediation_target": ["data/book/drafting/sec_02_2/draft_plan_v1_2.json (new)"],
        "regression_cases_required": [
            "RC-A1 attempt #2's shape must still be rejected, QUALIFIER_DROPPED at E and K",
            "RC-A2 the two-bound-unit shape must validate",
            "RC-A3 the single-unit combined shape must validate",
            "RC-A4 an identity unit stripped of C-002's conditions must fail CONDITION_DROPPED",
            "RC-A5 the forbidden attribution shape must still fail SEMANTIC_SCOPE_MISMATCH",
            "RC-A6 DSC-C002-001's marker set and paragraph scope must be unchanged",
        ],
        "attempt_3_justified": "yes, conditional on the plan change and its regressions",
    }

    u_c = {
        "unit_id": "U-C-P01-S02",
        "claim_ids": ["SEC-02-2-P0-008"],
        "generated_text": evidence["failed_unit_texts"]["U-C-P01-S02"],
        "failure_codes": ["UNSUPPORTED_PROPOSITION"],
        "failing_stages": ["C_support"],
        "rule_ids": [None],
        "contested_words": list(CONTESTED_WORDS),
        "candidate_causes": {
            "a_unsupported_semantic_additions": "PARTIALLY - 'spesifik' adds nothing the claim "
                                                "does not already say through 'In some'",
            "b_faithful_paraphrase_blocked_by_lexical_containment": "REFUTED",
            "c_avoidable_writer_vocabulary_choice": "SUPPORTED - primary",
            "d_broader_cross_lingual_licensing_defect": "REFUTED",
        },
        "root_cause_class": "WRITER_VOCABULARY_CHOICE",
        "root_cause": (
            "The writer chose two words the claim's frozen glosses do not license when licensed "
            "words for the same meaning were available and, in one case, already in the same "
            "sentence. 'kayaç' was written three words after the licensed 'kaya'; 'spesifik' "
            "duplicates the 'In some' condition that 'bazı' and the licensed 'belirli' already "
            "carry. Three natural Turkish renderings pass support containment against the "
            "current pool unchanged. The gloss set is not too narrow, and the containment rule "
            "did what it exists to do."),
        "evidence": {
            "frozen_glosses": p0008["frozen_glosses"],
            "licensed_alternatives_that_existed": p0008["licensed_alternatives_that_existed"],
            "kayac_licensed": p0008["words"]["kayaç"]["licensed"],
            "kaya_licensed": p0008["words"]["kaya"]["licensed"],
            "spesifik_licensed": p0008["words"]["spesifik"]["licensed"],
            "belirli_licensed": p0008["words"]["belirli"]["licensed"],
            "rejected_sentence_used_kaya_and_kayac_together": True,
            "conditions_and_language_were_already_correct": True,
        },
        "validator_verdict_correct": True,
        "validator_verdict_reasoning": (
            "Containment rejects content words no declared claim licenses. Both words are such "
            "words, and the rejection cost nothing that a faithful rendering needed, since "
            "faithful renderings validate. Loosening the rule to admit them would admit every "
            "near-synonym a writer reaches for, which is the failure mode the stage exists to "
            "prevent."),
        "smallest_safe_remediation": (
            "Plan change only, and it is not a loosening. Expose the already-frozen "
            "translation_glosses for each English-source claim to the writer in the payload, as "
            "the vocabulary its rendering may use, alongside the approved condition renderings "
            "the payload already carries. This states what the validator already accepts; it "
            "does not change what it accepts. The paraphrase lexicon, the glosses and the "
            "containment rule are untouched."),
        "remediation_is": "generic",
        "remediation_generality": (
            "Every cross-lingual claim in every future section has the same gap: the writer is "
            "told to translate and is not told which vocabulary survives containment."),
        "remediation_target": ["data/book/drafting/sec_02_2/draft_plan_v1_2.json (new)"],
        "regression_cases_required": [
            "RC-B1 attempt #2's sentence must still fail on exactly ['kayaç', 'spesifik']",
            "RC-B2 the three licensed renderings must show zero unlicensed content words",
            "RC-B3 'kayaç' must stay unlicensed and 'kaya' licensed - a widening tripwire",
            "RC-B4 SEC-02-2-P0-008's frozen glosses must be byte-identical to today's",
        ],
        "attempt_3_justified": "yes, conditional on the payload change and its regressions",
    }
    return [u_a, u_c]


# ================================================================ 4. the C-002 representation question

def representation_finding(c002_probes: dict) -> dict[str, Any]:
    scenarios = c002_probes["scenarios"]
    return {
        "question": ("Should SEC-02-2-C-002 remain draftable as one claim, or be represented "
                     "downstream as two explicitly bound semantic components - acceptance-table "
                     "identity/scope, and numeric acceptance criteria?"),
        "claim_altered_by_this_phase": False,
        "answer": "one frozen claim, two bound downstream units",
        "reasoning": (
            "The claim stays one claim. It is frozen, it is one source's statement, and the "
            "probes show a single unit carrying both components validates, so nothing forces a "
            "split at the claim level. What the evidence does force is a split downstream: the "
            "shape that failed twice is the shape where one unit must both reproduce the "
            "canonical sentence and add a meaning that sentence does not contain. DSC-C002-001's "
            "required_action already describes the two-component form, and stage K already scopes "
            "the required marker to the paragraph precisely because the qualifier cannot live "
            "inside the claim's own sentence. The plan is the only artifact that never learned "
            "this."),
        "binding_requirements_if_split": [
            "both units declare SEC-02-2-C-002 and cite SRC-DOC000087-ea64db4f1a7f",
            "both units are INDEPENDENT; neither may imply C-002 proves C-001",
            "the identity unit carries C-002's own conditions, or stage E rejects it",
            "the identity unit names Tablo-351-5 without an attribution marker, or stage K "
            "rejects it as SEMANTIC_SCOPE_MISMATCH",
        ],
        "single_unit_combined_validates": scenarios["single_unit_combined"]["accepts"],
        "two_bound_units_validate": scenarios["two_bound_units"]["accepts"],
        "careless_split_validates": scenarios["two_units_identity_without_conditions"]["accepts"],
    }


# ================================================================ 5. run

def build_analysis() -> dict[str, Any]:
    freeze = freeze_check()
    if not freeze["all_present"]:
        raise SystemExit(f"missing frozen inputs: {freeze['missing']}")

    plan = json.loads(PLAN_V1_1.read_text(encoding="utf-8"))
    bundle = v11().load_bundle()
    raw, ir = attempt_2_ir()
    rejection = json.loads(REJECTED_2.read_text(encoding="utf-8"))

    if raw["raw_text_sha256"] != rejection["raw_text_sha256"]:
        raise SystemExit("attempt #2 raw output and its rejection record disagree")

    texts = {u["unit_id"]: u["text"] for u in ir["units"]}
    evidence = {
        "failed_unit_texts": {uid: texts[uid] for uid in FAILED_UNITS},
        "payload_reconstruction": payload_reconstruction(plan, bundle.allowlist),
        "verbatim_census": verbatim_census(ir, bundle.allowlist),
        "unit_allocation": unit_to_claim_allocation(ir, plan),
        "qualifier_survival": qualifier_survival_evidence(ir, bundle.allowlist, bundle),
        "c002_probes": probe_c002(bundle),
        "p0_008_probes": probe_p0_008(bundle),
    }
    failures = classify(evidence)

    return {
        "version": VERSION,
        "section_id": SECTION_ID,
        "draft_id": DRAFT_ID,
        "analysed_at": now(),
        "phase": "SEC-02-2 DRAFT FAILURE ANALYSIS V2",
        "generation_attempts_in_this_phase": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "validators_weakened": [],
        "frozen_inputs": freeze,
        "attempt_2": {
            "raw_text_sha256": raw["raw_text_sha256"],
            "model_id": raw["model_id"],
            "units": len(ir["units"]),
            "rejected_unit_ids": rejection["rejected_unit_ids"],
            "failure_codes": rejection["failure_codes"],
        },
        "evidence": evidence,
        "failures": failures,
        "representation_question": representation_finding(evidence["c002_probes"]),
        "recommendation": {
            "category": "plan change (claim-to-unit allocation, plus payload vocabulary "
                        "exposure) - one new artifact, draft plan v1.2",
            "is_a_loosening": False,
            "loosening_argument": (
                "Neither half changes what any validator accepts. The allocation changes what "
                "the writer is asked to produce; the vocabulary exposure states glosses that are "
                "already frozen and already enforced. No threshold, marker set, failure code, "
                "gloss, lexicon entry or claim is edited."),
            "attempt_3_justified": True,
            "attempt_3_conditions": [
                "draft plan v1.2 exists and allocates SEC-02-2-C-002 two bound unit slots",
                "draft plan v1.2 exposes the frozen translation glosses for English claims",
                "RC-A1..A6 and RC-B1..B4 all pass before any generation call",
                "exactly one attempt, authorised by its own phase, no automatic retry",
            ],
            "not_authorised_here": ("This phase authorises no generation. Attempt #3 becomes "
                                    "justifiable, not permitted."),
        },
        "deferred_findings": [
            {
                "id": "DF-01",
                "finding": ("Stage E scores a qualifier preserved when half its anchors appear "
                            "in the paragraph. A qualifier that reuses its claim's own "
                            "vocabulary therefore passes on a verbatim copy that never states "
                            "it - SEC-02-2-C-009 did exactly this in attempt #2."),
                "direction": "tightening, not loosening",
                "actioned_here": False,
                "reason": ("Out of scope: this phase does not modify validators, and a "
                           "tightening deserves its own fixtures and its own gate."),
            },
        ],
    }


def write_manifest(analysis: dict) -> None:
    write_json(MANIFEST_PATH, {
        "version": VERSION,
        "section_id": SECTION_ID,
        "phase": analysis["phase"],
        "generated_at": analysis["analysed_at"],
        "status": "closed_go",
        "final_decision": "SEC-02-2 DRAFT FAILURE ANALYSIS V2 — CLOSED / GO",
        "generation_attempts": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "validators_weakened": [],
        "frozen_inputs_sha256": analysis["frozen_inputs"]["sha256"],
        "artifacts": {
            "failure_analysis": str(FAILURE_ANALYSIS_PATH.relative_to(ROOT)),
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "script": "scripts/53_sec_02_2_draft_failure_analysis_v2.py",
            "tests": "tests/test_sec_02_2_draft_failure_analysis_v2.py",
        },
        "failure_analysis_sha256": sha_file(FAILURE_ANALYSIS_PATH),
        "root_causes": {f["unit_id"]: f["root_cause_class"] for f in analysis["failures"]},
        "validator_verdicts_correct": all(f["validator_verdict_correct"]
                                          for f in analysis["failures"]),
        "recommendation": analysis["recommendation"]["category"],
        "attempt_3_justified": analysis["recommendation"]["attempt_3_justified"],
        "attempt_3_authorised_here": False,
        "deferred_findings": [d["id"] for d in analysis["deferred_findings"]],
        "next_phase": "SEC-02-2 DRAFT PLAN V1.2 + ATTEMPT #3 AUTHORISATION",
    })


def write_report(analysis: dict) -> None:
    u_a, u_c = analysis["failures"]
    census = analysis["evidence"]["verbatim_census"]
    p0008 = analysis["evidence"]["p0_008_probes"]
    c002 = analysis["evidence"]["c002_probes"]
    rep = analysis["representation_question"]
    lines: list[str] = []
    add = lines.append

    add("# SEC-02-2 Draft Failure Analysis v2")
    add("")
    add(f"`{VERSION}`")
    add("")
    add("")
    add("## Executive Decision")
    add("")
    add("Both attempt-#2 failures are root-caused against the artifacts, both validator verdicts "
        "are correct, and both remediations are the same kind of change: a new draft plan. "
        "Nothing was generated, nothing was rendered, no validator was touched.")
    add("")
    add("**SEC-02-2 DRAFT FAILURE ANALYSIS V2 — CLOSED / GO**")
    add("")
    add("")
    add("## What Attempt #2 Actually Did")
    add("")
    add(f"| | |")
    add("|---|---|")
    add(f"| Material units | {analysis['attempt_2']['units']} |")
    add(f"| Single-claim units | {census['single_claim_units']} |")
    add(f"| Byte-identical copies of the canonical claim | {census['verbatim_units']} "
        f"({census['verbatim_rate']}) |")
    add(f"| Composed units | {census['composed_units']} — {census['composed_unit_ids']} |")
    add(f"| Units per claim | exactly one, for every allocated claim |")
    add(f"| Qualifiers scored preserved by stage E | "
        f"{analysis['evidence']['qualifier_survival']['stage_e_preservation']} |")
    add(f"| Qualifiers whose meaning actually reached the prose | "
        f"{analysis['evidence']['qualifier_survival']['meaning_realised']} |")
    add("")
    add("The census is the finding the rest of the analysis rests on. Every unit whose claim was "
        "already Turkish is the claim's own sentence, copied. The only two composed units are "
        "the two English claims, which could not be copied. This writer composes when copying is "
        "impossible and not otherwise — and a qualifier delivered beside a copy-ready sentence "
        "is, to a copying writer, invisible.")
    add("")
    add("")
    add("## A — U-A-P01-S02 / SEC-02-2-C-002, QUALIFIER_DROPPED")
    add("")
    add(f"**Root cause class:** `{u_a['root_cause_class']}` "
        f"(secondary: `{u_a['secondary_class']}`)")
    add("")
    add(u_a["root_cause"])
    add("")
    add("Against the candidates the phase brief named:")
    add("")
    add("| Candidate | Verdict | Evidence |")
    add("|---|---|---|")
    add("| a. canonical-claim / qualifier representation mismatch | **supported, primary** | "
        "the unit is byte-identical to `canonical_claim`; the qualifier shares no vocabulary "
        "with it |")
    add("| b. generation payload omission | refuted | the rebuilt payload carries the qualifier "
        "verbatim, `qualifiers_are_mandatory: true`, and DSC-C002-001 with its "
        "`required_meaning` and `required_action` |")
    add("| c. prompt-compliance failure | contributing, not primary | prompt v1.1 does say "
        "qualifiers are mandatory — and also says one proposition per sentence, with no unit "
        "allocated for the second one |")
    add("| d. validator semantic-boundary design issue | refuted | two different compliant "
        "shapes validate under the same rules, unchanged |")
    add("| e. plan allocates no unit slot for the qualifier | **supported** | the plan allocates "
        "claims to subsections only; the writer resolved that to one unit per claim |")
    add("")
    add("**Validator verdict: correct.** " + u_a["validator_verdict_reasoning"])
    add("")
    add("### Probes")
    add("")
    add("Validator inputs, not draft prose.")
    add("")
    add("| Shape | Result |")
    add("|---|---|")
    for name, scenario in c002["scenarios"].items():
        verdict = "ACCEPT" if scenario["accepts"] else ", ".join(
            sorted({f"{f['code']}@{f['stage']}" for codes in scenario["units"].values()
                    for f in codes}))
        add(f"| {scenario['shape']} | {verdict} |")
    add("")
    add("### Smallest safe remediation")
    add("")
    add(u_a["smallest_safe_remediation"])
    add("")
    add(f"Generality: {u_a['remediation_is']}. {u_a['remediation_generality']}")
    add("")
    add("")
    add("## B — U-C-P01-S02 / SEC-02-2-P0-008, UNSUPPORTED_PROPOSITION")
    add("")
    add(f"**Root cause class:** `{u_c['root_cause_class']}`")
    add("")
    add(u_c["root_cause"])
    add("")
    add("| Candidate | Verdict |")
    add("|---|---|")
    add("| a. unsupported semantic additions | partially — `spesifik` restates the `In some` "
        "condition the licensed `bazı`/`belirli` already carry |")
    add("| b. faithful paraphrase blocked by lexical containment | refuted — three faithful "
        "renderings pass against the pool unchanged |")
    add("| c. avoidable writer vocabulary choice | **supported, primary** |")
    add("| d. broader cross-lingual licensing defect | refuted — the defect is that the writer "
        "is never shown the vocabulary, not that the vocabulary is missing |")
    add("")
    add("| Word | Licensed today |")
    add("|---|---|")
    for word, row in p0008["words"].items():
        add(f"| `{word}` | {'yes' if row['licensed'] else 'no'} |")
    add("")
    add("The rejected sentence contains `kaya` and `kayaç` three words apart. The licensed form "
        "was in the writer's hand as it wrote the unlicensed one — which is what makes this a "
        "choice rather than a gap. `kayaç` misses `kaya` only because prefix agreement needs "
        "five characters and `kaya` has four; that is a property of the containment rule, not a "
        "reason to widen a lexicon, because the faithful renderings pass without it.")
    add("")
    add(f"Licensed alternatives that existed: `{p0008['licensed_alternatives_that_existed']}`.")
    add("")
    add("**Validator verdict: correct.** " + u_c["validator_verdict_reasoning"])
    add("")
    add("### Smallest safe remediation")
    add("")
    add(u_c["smallest_safe_remediation"])
    add("")
    add(f"Generality: {u_c['remediation_is']}. {u_c['remediation_generality']}")
    add("")
    add("")
    add("## Should SEC-02-2-C-002 Be Two Components?")
    add("")
    add(f"**{rep['answer']}.** The frozen claim is not altered by this phase.")
    add("")
    add(rep["reasoning"])
    add("")
    add("If the downstream split is taken, four things bind:")
    add("")
    for requirement in rep["binding_requirements_if_split"]:
        add(f"- {requirement}")
    add("")
    add("")
    add("## Regression Cases Required Before Any Attempt #3")
    add("")
    for case in u_a["regression_cases_required"] + u_c["regression_cases_required"]:
        add(f"- {case}")
    add("")
    add("")
    add("## Deferred Finding")
    add("")
    for deferred in analysis["deferred_findings"]:
        add(f"**{deferred['id']}.** {deferred['finding']} Direction: {deferred['direction']}. "
            f"Not actioned here — {deferred['reason']}")
    add("")
    add("")
    add("## Recommendation")
    add("")
    add(f"**{analysis['recommendation']['category']}.**")
    add("")
    add(analysis["recommendation"]["loosening_argument"])
    add("")
    add("Attempt #3 is justified, and is not authorised here. It becomes permissible only when:")
    add("")
    for condition in analysis["recommendation"]["attempt_3_conditions"]:
        add(f"- {condition}")
    add("")
    add("")
    add("## Phase Accounting")
    add("")
    add("| | |")
    add("|---|---|")
    add("| Generation attempts | 0 |")
    add("| Retrieval calls | 0 |")
    add("| Qdrant writes | 0 |")
    add("| Corpus reads | 0 |")
    add("| Validators weakened | none |")
    add("| Frozen artifacts modified | none |")
    add("| Prose rendered | none |")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    analysis = build_analysis()
    write_json(FAILURE_ANALYSIS_PATH, analysis)
    write_manifest(analysis)
    write_report(analysis)
    print(f"analysis written: {FAILURE_ANALYSIS_PATH.relative_to(ROOT)}")
    for failure in analysis["failures"]:
        print(f"  {failure['unit_id']}: {failure['root_cause_class']} "
              f"(validator correct: {failure['validator_verdict_correct']})")
    print(f"recommendation: {analysis['recommendation']['category']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
