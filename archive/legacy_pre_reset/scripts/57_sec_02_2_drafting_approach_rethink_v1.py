"""SEC-02-2 Drafting Approach Rethink v1 — is free prose + lexical containment an architecture?

Three attempts, three rejections. The previous phases each asked why a particular unit failed.
This one asks whether the drafting approach can succeed at all, and answers it with a census
rather than an opinion.

The census is the whole phase. Every material unit of every preserved attempt is classified by
how it was produced — reproduced (it contains its claim's canonical sentence verbatim) or
composed (it does not) — and the containment outcome is counted separately for each mode. The
result does not vary between attempts and does not respond to remediation:

    reproduced units:  516 content tokens across three attempts,  0 unlicensed
    composed units:     79 content tokens across two attempts,    6 unlicensed

Plan v1.2 changed the fidelity outcomes completely — qualifier realisation went 0/2 to 2/2,
conditions and language to 100% — and moved the composed-token containment rate from 0.077 to
0.075. Instructions govern what the writer chooses to say. They do not govern which surface forms
it reaches for while saying it, because nothing in the architecture makes the licensed pool a
constraint on generation; it is a filter applied afterwards.

Worse, the two requirements are in direct tension. Every fidelity fix must be composed — a
qualifier whose vocabulary its canonical sentence lacks is unreachable by reproduction, which is
what analysis v2 established. So closing fidelity causes raises the composed-unit count: 0, then
2, then 4. The architecture pays for each fidelity fix in containment exposure at a fixed rate.

Two things this phase refuses to do:

**It does not treat `licensed_alternative_was_in_hand` as proof of semantic harmlessness.** That
inference is recorded here as insufficient. A licensed string existing nearby says nothing about
whether the unlicensed string means the same thing. `durumlarında` and the exempt `durumlarda`
differ by one morpheme; `ifade eder` and the qualifier's categorical `-dir` differ in modality.
The same evidence flag was attached to both, and it cannot bear that weight.

**It does not widen a lexicon.** Two of the four attempt-#3 words are relationship-bearing —
`sağlar` asserts provision, `ifade eder` substitutes a metalinguistic predicate for a copula the
qualifier states flatly. Exempting them globally would let stage C accept an unsupported
performance assertion in any unit of any section. That is a loosening, in the one direction the
stage exists to block, and it is named as such below.

Analysis only. No generation, no retrieval, no Qdrant write, no corpus read, no rendering, no
attempt #4. Every probe reads preserved artifacts and calls the frozen validator's own pure
functions; none of them constructs prose.
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

VERSION = "tunnelbook-sec-02-2-drafting-approach-rethink-v1"
PHASE = "SEC-02-2 DRAFTING APPROACH RETHINK V1"
SECTION_ID = "SEC-02-2"

BOOK = ROOT / "data" / "book"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"
REMEDIATION = SECTION_DIR / "remediation_v1"
ANALYSIS_V2 = SECTION_DIR / "analysis_v2"
ATTEMPT_3 = SECTION_DIR / "attempt_3"
QUALIFIER_V1 = SECTION_DIR / "qualifier_validation_v1"
RETHINK = SECTION_DIR / "rethink_v1"
MANIFESTS = BOOK / "manifests"

# ---- immutable evidence. Read and hashed, never written.
RAW_ATTEMPT_1 = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"
RAW_ATTEMPT_2 = REMEDIATION / "raw" / "sec_02_2_draft_raw_attempt_2.json"
RAW_ATTEMPT_3 = ATTEMPT_3 / "raw" / "sec_02_2_draft_raw_attempt_3.json"
AUDIT_ATTEMPT_1 = SECTION_DIR / "audits" / "sec_02_2_draft_audit_v1.json"
REJECTED_2 = REMEDIATION / "rejected" / "pilot_attempt_2_validation.json"
REJECTED_3 = ATTEMPT_3 / "rejected" / "pilot_attempt_3_validation.json"
FAILURE_ANALYSIS_V2 = ANALYSIS_V2 / "audits" / "attempt_2_failure_analysis_v1.json"
DRAFTING_CONTRACT = CONTRACTS / "section_drafting_contract_v1.json"
QUALIFIER_SEMANTICS = QUALIFIER_V1 / "contracts" / "draft_qualifier_semantics_v1.json"
PLAN_V1 = SECTION_DIR / "draft_plan_v1.json"
PLAN_V1_1 = SECTION_DIR / "draft_plan_v1_1.json"
PLAN_V1_2 = SECTION_DIR / "draft_plan_v1_2.json"
VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
VALIDATOR_V1_1 = ROOT / "scripts" / "52_section_draft_validator_v1_1.py"
VALIDATOR_V1_2 = ROOT / "scripts" / "54_section_draft_validator_v1_2.py"

FROZEN_INPUTS = {
    "attempt_1_raw": RAW_ATTEMPT_1,
    "attempt_1_audit": AUDIT_ATTEMPT_1,
    "attempt_2_raw": RAW_ATTEMPT_2,
    "attempt_2_rejection": REJECTED_2,
    "attempt_2_failure_analysis_v2": FAILURE_ANALYSIS_V2,
    "attempt_3_raw": RAW_ATTEMPT_3,
    "attempt_3_rejection": REJECTED_3,
    "section_drafting_contract_v1": DRAFTING_CONTRACT,
    "draft_qualifier_semantics_v1": QUALIFIER_SEMANTICS,
    "draft_plan_v1": PLAN_V1,
    "draft_plan_v1_1": PLAN_V1_1,
    "draft_plan_v1_2": PLAN_V1_2,
    "draft_validator_v1": VALIDATOR_V1,
    "draft_validator_v1_1": VALIDATOR_V1_1,
    "draft_validator_v1_2": VALIDATOR_V1_2,
}

# ---- outputs. All phase-local.
ANALYSIS_PATH = RETHINK / "audits" / "drafting_approach_analysis_v1.json"
CENSUS_PATH = RETHINK / "probes" / "realization_mode_census_v1.json"
PROBES_PATH = RETHINK / "probes" / "containment_boundary_probes_v1.json"
MATRIX_PATH = RETHINK / "audits" / "architecture_comparison_matrix_v1.json"
ADR_PATH = RETHINK / "decisions" / "adr_001_drafting_architecture_v2.json"
MIGRATION_PATH = RETHINK / "audits" / "migration_plan_v1.json"
MANIFEST_PATH = MANIFESTS / "sec_02_2_drafting_approach_rethink_v1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_drafting_approach_rethink_v1.md"


# ================================================================ 1. io

def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


_V1 = None


def validator():
    """The frozen validator, imported for its pure functions only.

    Nothing here runs a validation pass or writes anything the validator owns. `content_tokens`,
    `licensed_tokens`, `unlicensed`, `prefix_agreement` and `fold` are read-only and are the only
    honest way to state what containment does — restating their behaviour in this file would be a
    second implementation to disagree with the first.
    """
    global _V1
    if _V1 is None:
        _V1 = _load("draft_validator_v1_rethink", VALIDATOR_V1)
    return _V1


def draft_ir(raw_path: Path) -> dict:
    return json.loads(json.loads(raw_path.read_text(encoding="utf-8"))["raw_text"])


def writer_config(raw_path: Path) -> dict:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    return {k: raw.get(k) for k in
            ("model_id", "temperature", "seed", "finish_reason", "system_prompt_version")}


# ================================================================ 2. probe P1 — realization mode

def realization_mode(unit: dict, bundle) -> str:
    """Reproduced or composed, decided by whether the canonical sentence survives in the text.

    This is the distinction the whole phase turns on, so it is drawn mechanically: a unit is
    reproduced when the folded canonical sentence of one of its declared claims occurs as a
    substring of the folded unit text. Everything else is composed. The test is deliberately
    generous to 'reproduced' — a unit that copies and then adds is still counted as reproduced,
    which understates rather than overstates the composed-mode failure rate.
    """
    v1 = validator()
    folded_text = v1.fold(unit.get("text", ""))
    for claim_id in unit.get("claim_ids") or []:
        claim = bundle.allowlist.get(claim_id) or {}
        canonical = (claim.get("canonical_claim") or "").strip()
        if canonical and v1.fold(canonical) in folded_text:
            return "reproduced"
    return "composed"


def census_attempt(label: str, raw_path: Path) -> dict:
    v1 = validator()
    bundle = v1.load_bundle()
    units = draft_ir(raw_path)["units"]
    modes: dict[str, dict] = {
        "reproduced": {"units": [], "content_tokens": 0, "unlicensed_tokens": []},
        "composed": {"units": [], "content_tokens": 0, "unlicensed_tokens": []},
    }
    for unit in units:
        if not unit.get("material"):
            continue
        text = unit.get("text", "")
        claim_ids = unit.get("claim_ids") or []
        mode = realization_mode(unit, bundle)
        content = v1.content_tokens(text, bundle.function_lexicon)
        pool = v1.licensed_tokens(claim_ids, bundle)
        stray = v1.unlicensed(text, pool, bundle) if pool else []
        modes[mode]["units"].append({
            "unit_id": unit["unit_id"],
            "claim_ids": sorted(claim_ids),
            "content_token_count": len(content),
            "unlicensed": stray,
        })
        modes[mode]["content_tokens"] += len(content)
        modes[mode]["unlicensed_tokens"] += stray

    for mode in modes.values():
        mode["unit_count"] = len(mode["units"])
        mode["unlicensed_token_count"] = len(mode["unlicensed_tokens"])
        mode["failing_unit_count"] = sum(1 for u in mode["units"] if u["unlicensed"])
        mode["containment_failure_rate_per_content_token"] = (
            round(mode["unlicensed_token_count"] / mode["content_tokens"], 4)
            if mode["content_tokens"] else None)
        mode["unit_pass_rate"] = (
            round(1 - mode["failing_unit_count"] / mode["unit_count"], 4)
            if mode["unit_count"] else None)

    return {
        "attempt": label,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "raw_sha256": sha_file(raw_path),
        "writer_config": writer_config(raw_path),
        "material_units": modes["reproduced"]["unit_count"] + modes["composed"]["unit_count"],
        "modes": modes,
    }


def build_census() -> dict:
    attempts = [
        census_attempt("attempt_1", RAW_ATTEMPT_1),
        census_attempt("attempt_2", RAW_ATTEMPT_2),
        census_attempt("attempt_3", RAW_ATTEMPT_3),
    ]
    totals = {"reproduced": {"content_tokens": 0, "unlicensed": 0, "units": 0, "failing": 0},
              "composed": {"content_tokens": 0, "unlicensed": 0, "units": 0, "failing": 0}}
    for attempt in attempts:
        for mode, data in attempt["modes"].items():
            totals[mode]["content_tokens"] += data["content_tokens"]
            totals[mode]["unlicensed"] += data["unlicensed_token_count"]
            totals[mode]["units"] += data["unit_count"]
            totals[mode]["failing"] += data["failing_unit_count"]
    for mode in totals.values():
        mode["failure_rate_per_content_token"] = (
            round(mode["unlicensed"] / mode["content_tokens"], 4)
            if mode["content_tokens"] else None)
        mode["unit_pass_rate"] = (
            round(1 - mode["failing"] / mode["units"], 4) if mode["units"] else None)

    composed_trend = [a["modes"]["composed"]["unit_count"] for a in attempts]
    rate_trend = [a["modes"]["composed"]["containment_failure_rate_per_content_token"]
                  for a in attempts]

    # A section's containment outcome is the joint outcome over its composed units, so the
    # per-token rate compounds. This is the scaling statement, computed rather than asserted.
    p = totals["composed"]["failure_rate_per_content_token"] or 0.0
    mean_tokens = (round(totals["composed"]["content_tokens"] / totals["composed"]["units"], 2)
                   if totals["composed"]["units"] else 0)
    projection = []
    for composed_units in (2, 4, 8, 16, 32):
        clean_unit = (1 - p) ** mean_tokens
        projection.append({
            "composed_units": composed_units,
            "expected_clean_section_probability": round(clean_unit ** composed_units, 6),
        })

    return {
        "version": VERSION,
        "probe_id": "P1_realization_mode_census",
        "question": "does containment failure depend on how a unit was produced?",
        "method": ("classify every material unit of every preserved attempt as reproduced or "
                   "composed, then count containment outcomes separately for each mode using the "
                   "frozen validator's own pure functions"),
        "attempts": attempts,
        "totals": totals,
        "findings": {
            "reproduced_mode_never_fails_containment": totals["reproduced"]["unlicensed"] == 0,
            "composed_mode_fails_at_a_stable_rate": rate_trend,
            "composed_unit_count_trend": composed_trend,
            "composed_unit_count_rose_under_remediation":
                composed_trend == sorted(composed_trend) and composed_trend[0] < composed_trend[-1],
            "mean_content_tokens_per_composed_unit": mean_tokens,
            "scaling_projection": projection,
        },
        "interpretation": (
            "Containment failure is a property of the composed mode, not of the writer's "
            "diligence in a given attempt. Three attempts produced "
            f"{totals['reproduced']['content_tokens']} content tokens by reproduction with "
            f"{totals['reproduced']['unlicensed']} unlicensed, and "
            f"{totals['composed']['content_tokens']} by composition with "
            f"{totals['composed']['unlicensed']} unlicensed. Plan v1.2 closed every fidelity "
            "cause and moved the composed-mode rate from "
            f"{rate_trend[1]} to {rate_trend[2]}. Because a qualifier whose vocabulary its "
            "canonical sentence lacks is unreachable by reproduction, each fidelity fix converts "
            "reproduced units into composed ones: the composed-unit count went "
            f"{composed_trend}. Fidelity and containment are not two independent defects being "
            "fixed in turn; under this architecture one is paid for with the other."),
    }


# ================================================================ 3. probe P2/P3 — the boundary

FOUR_WORDS = ("ifade", "sağlar", "durumlarında", "örneğin")

CLASSIFICATION_CATEGORIES = {
    "1": "grammatical/discourse surface vocabulary",
    "2": "semantic paraphrase",
    "3": "relationship-bearing vocabulary",
    "4": "proposition-changing vocabulary",
}


def classify_words() -> dict:
    """Classify attempt #3's four unlicensed words, with the machine-checkable part checked.

    The categories are a judgement; the evidence each judgement rests on is not. Whether a word
    is exempt as a function word, whether a morphological sibling of it is exempt, and whether a
    same-meaning token sits in the claim's own pool are all decided here by calling the frozen
    validator, so a reader who disagrees with a category can still see exactly what was true.
    """
    v1 = validator()
    bundle = v1.load_bundle()
    lexicon = bundle.function_lexicon
    pools = {"SEC-02-2-C-002": v1.licensed_tokens(["SEC-02-2-C-002"], bundle),
             "SEC-02-2-P0-008": v1.licensed_tokens(["SEC-02-2-P0-008"], bundle)}

    def in_pool(token: str, claim_id: str) -> list[str]:
        folded = v1.fold(token)
        return sorted(t for t in pools[claim_id] if v1.prefix_agreement(folded, t))

    def exempt_siblings(*forms: str) -> dict[str, bool]:
        return {form: v1.fold(form) in lexicon for form in forms}

    words = [
        {
            "word": "ifade",
            "unit_id": "U-A-P01-S03",
            "claim_id": "SEC-02-2-C-002",
            "gloss": "'expression'; the construction written was `ifade eder`, 'expresses'",
            "categories": ["2", "3"],
            "primary": "2",
            "category_4_excluded": False,
            "category_4_note": (
                "Cannot be excluded. SEC-02-2-C-002's qualifier states the identity flatly — "
                "'kabul kriteridir', it *is* the acceptance criterion. `ifade eder` substitutes a "
                "metalinguistic predicate for that copula: the table *expresses* the criterion. "
                "DSC-C002-001 exists precisely because what this table is, versus what it is "
                "taken to establish, is the distinction the claim is fragile on. A modality shift "
                "on that exact copula is the one place in the sentence where it could matter."),
            "evidence": {
                "exempt_as_function_word": v1.fold("ifade") in lexicon,
                "light_verb_partner_eder_is_exempt": v1.fold("eder") in lexicon,
                "pool_tokens_agreeing": in_pool("ifade", "SEC-02-2-C-002"),
                "copula_it_replaces_is_licensed": sorted(
                    t for t in pools["SEC-02-2-C-002"] if t in {"kriteridir", "kriterleridir"}),
            },
            "rationale": (
                "A paraphrase of a licensed copula, and it bears the relation it paraphrases. It "
                "is not grammar: `eder` is exempt as a function word and `ifade` is the lexical "
                "half that carries the meaning, which is why only one of the pair was flagged."),
        },
        {
            "word": "sağlar",
            "unit_id": "U-A-P01-S03",
            "claim_id": "SEC-02-2-C-002",
            "gloss": "'provides/gives'; third-person present of sağlamak",
            "categories": ["3", "2"],
            "primary": "3",
            "category_4_excluded": True,
            "category_4_note": (
                "Excluded in this slot only. The claim's own English canonical uses `gives` for "
                "the same relation, so the proposition asserted is the source's. The exclusion "
                "does not travel: `sağlamak` also means 'to ensure/to satisfy', and "
                "'... gerekli dayanımı sağlar' is a performance assertion no source states. Same "
                "surface form, different proposition, decided by the slot it fills."),
            "evidence": {
                "exempt_as_function_word": v1.fold("sağlar") in lexicon,
                "pool_tokens_agreeing": in_pool("sağlar", "SEC-02-2-C-002"),
                "source_relation_verb_in_pool": sorted(
                    t for t in pools["SEC-02-2-C-002"] if t in {"gives", "give"}),
            },
            "rationale": (
                "A light verb by form, a relation by function: it asserts that the table stands "
                "in a providing relation to the criteria. That the relation happens to be the "
                "licensed one here is a fact about this sentence, not about the word."),
        },
        {
            "word": "durumlarında",
            "unit_id": "U-C-P01-S03",
            "claim_id": "SEC-02-2-P0-008",
            "gloss": "'in the cases/situations of'; durum + plural + possessive + locative",
            "categories": ["1", "2"],
            "primary": "1",
            "category_4_excluded": True,
            "category_4_note": (
                "Excluded, and demonstrably so. The function lexicon already exempts three "
                "inflections of the same lexeme. The fourth was rejected because the exemption "
                "test is exact string membership while the licensing test is five-character "
                "prefix agreement — two different matching regimes over an agglutinative "
                "language. Had the writer produced `durumlarda`, one morpheme away and equally "
                "grammatical, stage C would have said nothing."),
            "evidence": {
                "exempt_as_function_word": v1.fold("durumlarında") in lexicon,
                "exempt_siblings_of_the_same_lexeme": exempt_siblings(
                    "durumda", "durumlarda", "durumunda", "durumlarında"),
                "pool_tokens_agreeing": in_pool("durumlarında", "SEC-02-2-P0-008"),
                "licensed_same_meaning_token_in_pool": sorted(
                    t for t in pools["SEC-02-2-P0-008"]
                    if t in {"koşullarında", "koşulları", "conditions", "case"}),
            },
            "rationale": (
                "Discourse surface vocabulary that the containment boundary already treats as "
                "such in three of its four forms. It also restates the licensed `koşullarında` "
                "three words later, which makes it a paraphrase as well as grammar."),
        },
        {
            "word": "örneğin",
            "unit_id": "U-C-P01-S03",
            "claim_id": "SEC-02-2-P0-008",
            "gloss": "'for example'",
            "categories": ["1", "3"],
            "primary": "1",
            "category_4_excluded": True,
            "category_4_note": (
                "Excluded. It marks an exemplification relation, and that relation is stated by "
                "the source: the claim's English canonical reads 'such as crushed or squeezing "
                "rock', and both `such` and `as` are in the pool. The Turkish marker asserts "
                "nothing the English one did not."),
            "evidence": {
                "exempt_as_function_word": v1.fold("örneğin") in lexicon,
                "comparable_marker_gibi_is_exempt": v1.fold("gibi") in lexicon,
                "pool_tokens_agreeing": in_pool("örneğin", "SEC-02-2-P0-008"),
                "source_exemplification_markers_in_pool": sorted(
                    t for t in pools["SEC-02-2-P0-008"] if t in {"such", "as"}),
            },
            "rationale": (
                "A discourse marker, and the closest analogue already exempt: `gibi` — the word "
                "attempt #2 used for this same relation in this same claim — is in the function "
                "lexicon. It does bear a relation, which is why category 3 is listed, but the "
                "relation is the claim's own."),
        },
    ]
    assert [w["word"] for w in words] == list(FOUR_WORDS)
    return {
        "probe_id": "P4_attempt_3_word_classification",
        "categories": CLASSIFICATION_CATEGORIES,
        "words": words,
        "finding": (
            "The four words are not one class. Two are discourse surface vocabulary the "
            "containment boundary arguably never meant to catch; one bears a relation that "
            "happens to be licensed here and would not be elsewhere; one shifts the modality of "
            "the exact copula its claim is fragile on. Attempt #3's cause record described them "
            "collectively as connectives and light verbs carrying no technical content. That is "
            "true of two of them."),
        "consequence": (
            "No single remedy addresses the set. A lexicon entry that admits `durumlarında` "
            "correctly admits `sağlar` incorrectly, because the exemption mechanism cannot see "
            "which slot a word fills."),
    }


def boundary_probes() -> dict:
    """What the containment boundary actually licenses, as opposed to what it is described as.

    Stage C is documented as testing content words against the declaring claim's pool. The pool is
    built from every field of the claim record, so it also contains the record's English metadata.
    That is not a defect anyone chose; it is what pooling every field produces. It matters here
    because it sets the boundary in a place no one designed: `specific` is licensed and `spesifik`
    is not, and neither outcome was a decision about meaning.
    """
    v1 = validator()
    bundle = v1.load_bundle()
    lexicon = bundle.function_lexicon
    pools = {c: v1.licensed_tokens([c], bundle)
             for c in ("SEC-02-2-C-002", "SEC-02-2-P0-008")}

    metadata_tokens = sorted(
        t for t in pools["SEC-02-2-C-002"] | pools["SEC-02-2-P0-008"]
        if t in {"claim", "qualifier", "carried", "hence", "already", "source", "named", "rows",
                 "technical", "table", "class", "classes", "design", "manual", "support"})

    # Only cases where the English surface form of the same meaning is licensed and the Turkish
    # one is not. `kayaç` is deliberately excluded: the licensed `kaya` is Turkish, so that
    # substitution is a technical synonym shift and not a cross-lingual artifact.
    cross_lingual = []
    for turkish, english, claim_id, turkish_alternatives in (
            ("spesifik", "specific", "SEC-02-2-P0-008", ["belirli", "bazı"]),
            ("durumlarında", "conditions", "SEC-02-2-P0-008", ["koşullarında", "koşulları"]),
            ("sağlar", "gives", "SEC-02-2-C-002", [])):
        pool = pools[claim_id]
        licensed_alternatives = sorted(a for a in turkish_alternatives if v1.fold(a) in pool)
        cross_lingual.append({
            "claim_id": claim_id,
            "turkish_form": turkish,
            "english_form": english,
            "english_form_is_licensed": v1.fold(english) in pool,
            "turkish_form_is_licensed": any(
                v1.prefix_agreement(v1.fold(turkish), t) for t in pool),
            "licensed_turkish_alternatives_in_pool": licensed_alternatives,
        })

    durum_forms = {f: v1.fold(f) in lexicon for f in
                   ("durum", "durumda", "durumlarda", "durumunda", "durumlarında",
                    "durumların", "durumu", "durumları", "durumundaki")}

    return {
        "probe_id": "P2_P3_containment_boundary",
        "question": "where does the containment boundary actually fall, and was it placed there?",
        "matching_regimes": {
            "content_word_licensing": "five-character prefix agreement against the claim pool",
            "function_word_exemption": "exact string membership in a 126-entry list",
            "consequence": (
                "Turkish inflection defeats the exemption test and is absorbed by the licensing "
                "test. A grammatical word is exempt only in the forms someone happened to "
                "enumerate."),
        },
        "function_lexicon_size": len(lexicon),
        "durum_lexeme_coverage": {
            "forms_tested": durum_forms,
            "exempt": sum(1 for v in durum_forms.values() if v),
            "tested": len(durum_forms),
            "finding": ("The exemption list covers the forms of this lexeme that were written "
                        "down, not the lexeme. `durumlarda` is exempt and `durumlarında` is not, "
                        "which is the entire reason U-C-P01-S03 carries that word in its "
                        "rejection."),
        },
        "pool_contains_record_metadata": {
            "tokens": metadata_tokens,
            "finding": ("The licensed pool is built from every field of the claim record, "
                        "including English scope evidence and topic prose. It licenses the "
                        "vocabulary of the record as well as the vocabulary of the claim."),
        },
        "cross_lingual_asymmetry": {
            "cases": cross_lingual,
            "finding": ("For an English-source claim the pool licenses the English surface form "
                        "and not its Turkish realisation, so the writer is licensed to use words "
                        "the section's language policy forbids and unlicensed to use the words "
                        "that policy requires. `sağlar` is the case with no licensed Turkish "
                        "alternative at all: SEC-02-2-C-002's canonical states the relation with "
                        "`gives`, and the pool offers no Turkish lexical verb for it — only the "
                        "copula. The writer's licensed options there were to restructure the "
                        "sentence around `-dir` or to leave the pool, which is precisely what "
                        "`licensed_alternative_was_in_hand = true` does not record."),
        },
        "conclusion": (
            "Stage C's verdicts on the composed mode are correct as specified and are not, at the "
            "margin, decisions about meaning. Some of the boundary is principled — `kayaç` for "
            "`kaya` is a real technical synonym substitution. Some of it is an artifact of which "
            "inflections were enumerated and which fields were pooled. Neither the principled nor "
            "the accidental part is something a free-form writer can see."),
    }


# ================================================================ 4. refined cause

def refined_cause(census: dict, classification: dict, probes: dict) -> dict:
    reproduced = census["totals"]["reproduced"]
    composed = census["totals"]["composed"]
    return {
        "supersedes": "WRITER_VOCABULARY_CHOICE (attempt #2 analysis v2, attempt #3 cause record)",
        "superseded_inference": {
            "inference": ("`licensed_alternative_was_in_hand = true` was taken to show the writer "
                          "made an avoidable choice, and therefore that the unlicensed word was "
                          "semantically harmless and the defect was the writer's diligence."),
            "status": "INSUFFICIENT",
            "why_insufficient": [
                ("It conflates the existence of a licensed string with semantic equivalence "
                 "between it and the unlicensed one. `durumlarında` and the exempt `durumlarda` "
                 "are one morpheme apart and mean the same thing. `ifade eder` and the "
                 "qualifier's `-dir` are a modality apart and do not. The same flag was attached "
                 "to both, so the flag distinguishes nothing."),
                ("It reasons from availability to reachability. The pool was exposed to the "
                 "writer verbatim, as analysis v2 specified, and nothing in free-form generation "
                 "makes an exposed vocabulary a constraint on the next token. Showing a writer "
                 "the licensed words does not remove the unlicensed ones from its output space."),
                ("It made a testable prediction — better instructions would close the class — "
                 "and plan v1.2 tested it. The remediation was implemented exactly, every "
                 "fidelity cause closed, and the composed-mode containment rate moved from "
                 f"{census['attempts'][1]['modes']['composed']['containment_failure_rate_per_content_token']} "
                 f"to {census['attempts'][2]['modes']['composed']['containment_failure_rate_per_content_token']}. "
                 "The prediction failed."),
                ("For one of the four words it is not even true. `sağlar` renders the relation "
                 "SEC-02-2-C-002's own canonical states as `gives`, and that claim's pool "
                 "contains no Turkish lexical verb for it — only the copula. The licensed "
                 "options were to restructure the sentence around `-dir` or to leave the pool. "
                 "The flag records neither, because it asks whether some licensed token existed "
                 "and not whether a licensed way to say this thing existed."),
                ("It is a description of the symptom. Every containment failure is by definition "
                 "a word the writer chose; naming that as the cause cannot be wrong and cannot "
                 "be acted on."),
            ],
        },
        "refined_cause_class": "ARCHITECTURAL — UNCONSTRAINED_SURFACE_REALIZATION",
        "statement": (
            "Claim-bound lexical containment is a closed-set membership test applied to the "
            "output of an open-set generator. The licensed pool is a filter downstream of "
            "generation, never a constraint on it, so the containment outcome of any composed "
            "sentence is a sample from the writer's surface-form distribution rather than a "
            "property the architecture establishes. The three attempts measure that sample: "
            f"{composed['unlicensed']} unlicensed tokens in {composed['content_tokens']} composed "
            f"content tokens, against {reproduced['unlicensed']} in "
            f"{reproduced['content_tokens']} reproduced ones. Reproduction succeeds because it is "
            "not sampling — the tokens come from the pool by construction. That is the whole "
            "difference between the two modes, and it is a difference in architecture."),
        "contributing_causes": [
            {
                "id": "RC-01",
                "class": "GENERATOR_UNCONSTRAINED",
                "weight": "primary",
                "accounts_for": "all 6 unlicensed tokens across attempts #2 and #3",
                "detail": ("Free-form generation has no mechanism by which an exposed vocabulary "
                           "becomes a restriction. Prompting raises the probability of licensed "
                           "forms; it does not bound the output alphabet."),
            },
            {
                "id": "RC-02",
                "class": "CONTAINMENT_BOUNDARY_MORPHOLOGY",
                "weight": "contributory",
                "accounts_for": "`durumlarında` specifically; 1 of 6 observed tokens",
                "detail": ("Function-word exemption is exact string membership over an "
                           "agglutinative language, so a grammatical word is exempt only in "
                           "enumerated forms. Provable: `durumlarda` is exempt, `durumlarında` "
                           "is not, and they are the same lexeme."),
                "note": ("A real defect, and not the cause of the rejections. Fixing it alone "
                         "leaves 5 of 6 tokens unaddressed."),
            },
            {
                "id": "RC-03",
                "class": "STRUCTURAL_TENSION_FIDELITY_VS_CONTAINMENT",
                "weight": "aggravating",
                "accounts_for": "the trend across attempts",
                "detail": ("A qualifier whose vocabulary its canonical sentence lacks is "
                           "unreachable by reproduction, so every fidelity fix converts a "
                           "reproduced unit into a composed one. Composed units went "
                           f"{census['findings']['composed_unit_count_trend']}. The architecture "
                           "charges for fidelity in containment exposure."),
            },
        ],
        "confound_recorded": {
            "id": "CF-01",
            "finding": ("All three attempts used the same writer: "
                        f"{census['attempts'][2]['writer_config']['model_id']}, temperature "
                        f"{census['attempts'][2]['writer_config']['temperature']}, seed "
                        f"{census['attempts'][2]['writer_config']['seed']}. The three attempts "
                        "varied the instructions, never the writer."),
            "consequence": ("Reading 4 of the phase brief — the approach is sound and the writer "
                            "is not — is UNTESTED by this evidence, not refuted. Nothing here "
                            "shows a stronger writer would fail."),
            "why_it_does_not_change_the_decision": (
                "The architectural argument does not require reading 4 to be false. A better "
                "writer lowers the per-token rate; it does not make the rate zero, and the "
                "section-level outcome compounds over every composed token. Nor does a better "
                "writer see the boundary: the `durumlarda` / `durumlarında` line is invisible to "
                "any writer, however strong, because it is an artifact of which forms were "
                "enumerated. Selecting on 'a better model might be enough' is an unbounded bet "
                "whose cost is one generation per test."),
        },
        "classification_consequence": classification["consequence"],
        "boundary_consequence": probes["conclusion"],
    }


# ================================================================ 5. A/B/C/D

def comparison_matrix(census: dict, probes: dict) -> dict:
    composed = census["totals"]["composed"]
    reproduced = census["totals"]["reproduced"]
    durum = probes["durum_lexeme_coverage"]
    projection = {p["composed_units"]: p["expected_clean_section_probability"]
                  for p in census["findings"]["scaling_projection"]}

    options = [
        {
            "id": "A",
            "name": "current — free-form Turkish prose + strict claim-bound lexical containment",
            "containment_guarantee": "none; filter after the fact",
            "measured_composed_failure_rate": composed["failure_rate_per_content_token"],
            "responds_to_instruction": ("no — rate moved "
                                        f"{census['attempts'][1]['modes']['composed']['containment_failure_rate_per_content_token']} "
                                        f"to {census['attempts'][2]['modes']['composed']['containment_failure_rate_per_content_token']} "
                                        "under a correctly implemented remediation"),
            "scaling": (f"P(clean section) ≈ {projection[4]} at 4 composed units, "
                        f"{projection[16]} at 16"),
            "cost_to_continue": "one generation per attempt, unbounded",
            "weakens_stage_c": False,
            "prose_quality": "high where composed",
            "verdict": "REJECTED — not scalable; the failure rate is invariant under the only "
                       "lever the architecture offers",
        },
        {
            "id": "B",
            "name": "expanded function / paraphrase lexicon",
            "containment_guarantee": "none; the same filter with a larger accept set",
            "measured_composed_failure_rate": "unchanged mechanism; lowers observed rate by "
                                              "moving the boundary",
            "responds_to_instruction": "not applicable",
            "scaling": ("unbounded. Six new words after two attempts with no saturation "
                        "evidence, and Turkish morphology multiplies every lemma: the exemption "
                        f"list covers {durum['exempt']} of {durum['tested']} tested forms of the "
                        "single lexeme `durum`, in a list of "
                        f"{probes['function_lexicon_size']} entries"),
            "cost_to_continue": "per-word adjudication forever",
            "weakens_stage_c": True,
            "weakening_stated_plainly": (
                "This option works by making stage C more permissive. `sağlar` and `ifade` are "
                "relationship-bearing; a global exemption for them makes stage C accept "
                "'püskürtme beton gerekli dayanımı sağlar' — an unsupported performance "
                "assertion — in any unit of any section, because the exemption mechanism cannot "
                "see which slot a word fills. That is a loosening in the direction the stage "
                "exists to block."),
            "prose_quality": "high",
            "verdict": "REJECTED — explicitly weakens the validator, and cannot be bounded",
        },
        {
            "id": "C",
            "name": "controlled claim-specific realization templates",
            "containment_guarantee": "yes, within a template; none for text outside one",
            "measured_composed_failure_rate": "0 for framed spans",
            "responds_to_instruction": "not applicable",
            "scaling": ("authoring cost is claims × rhetorical roles, per section. SEC-02-2 alone "
                        "allowlists 27 claims. Templates are section-local and do not compose."),
            "cost_to_continue": "hand-authored frames per claim, re-authored per section",
            "weakens_stage_c": False,
            "prose_quality": "formulaic and repetitive; no cohesion mechanism",
            "verdict": "VIABLE BUT SUBSUMED — this is D's renderer with a hand-written, "
                       "non-compositional grammar and no separation of concerns",
        },
        {
            "id": "D",
            "name": "structured semantic plan (LLM) + deterministic surface renderer",
            "containment_guarantee": ("by construction. The renderer's output alphabet is the "
                                      "licensed pool plus a frozen closed grammatical scaffold, "
                                      "which is a static property provable over all plans"),
            "measured_composed_failure_rate": ("0 by construction; the reproduced mode's "
                                               f"{reproduced['unlicensed']} / "
                                               f"{reproduced['content_tokens']} generalised to "
                                               "the composed slots"),
            "responds_to_instruction": "not applicable — containment stops being a behaviour",
            "scaling": ("realization data is per claim and reusable across sections; the renderer "
                        "and the morphology are written once"),
            "cost_to_continue": ("build cost: plan IR contract, per-claim realization contract, "
                                 "renderer, Turkish suffixation, static containment proof"),
            "weakens_stage_c": False,
            "stage_c_relationship": ("unchanged and still running, demoted to a regression check "
                                     "that should now be unfailable — which is the correct "
                                     "relationship between a construction guarantee and a filter"),
            "prose_quality": ("formulaic. Measured against the status quo the loss is small: "
                              f"{reproduced['units']} of "
                              f"{reproduced['units'] + composed['units']} material units across "
                              "the three attempts are already verbatim reproduction"),
            "verdict": "SELECTED",
        },
    ]
    return {
        "probe_id": "architecture_comparison_matrix_v1",
        "evaluated_against": [
            "containment guarantee — construction or filter",
            "measured failure rate on the three-attempt evidence",
            "response to the levers the architecture offers",
            "scaling to a section, a chapter, a book",
            "whether it weakens stage C, stated plainly",
            "prose quality, measured against what the current architecture actually produces",
        ],
        "options": options,
        "selected": "D",
    }


# ================================================================ 6. ADR

def adr(census: dict, cause: dict, matrix: dict) -> dict:
    reproduced = census["totals"]["reproduced"]
    composed = census["totals"]["composed"]
    return {
        "id": "ADR-001",
        "title": "SEC-02-2 drafting architecture v2 — structured plan plus deterministic renderer",
        "status": "ACCEPTED",
        "date": datetime.now(timezone.utc).isoformat(),
        "phase": PHASE,
        "context": (
            "Three controlled pilot attempts under free-form Turkish generation with claim-bound "
            "lexical containment were rejected. Attempt #3 closed every cause attempt #2 failed "
            "on — qualifiers 0/2 to 2/2 realised, conditions 100%, language 100%, required topics "
            "3/3, citation coverage 100% — and was rejected on containment alone."),
        "decision": (
            "Adopt architecture D. The LLM emits a structured semantic plan and no prose. A "
            "deterministic renderer produces every surface form."),
        "decided_on": {
            "primary_evidence": (
                f"Reproduced units: {reproduced['content_tokens']} content tokens, "
                f"{reproduced['unlicensed']} unlicensed, across all three attempts. Composed "
                f"units: {composed['content_tokens']} content tokens, {composed['unlicensed']} "
                "unlicensed. The containment outcome is determined by production mode, and "
                "reproduction's guarantee comes from the tokens being drawn from the pool by "
                "construction rather than sampled and filtered."),
            "invariance_evidence": (
                "The composed-mode rate did not respond to the one lever architecture A offers. "
                "Plan v1.2 was implemented exactly as analysis v2 specified and the rate went "
                f"{census['attempts'][1]['modes']['composed']['containment_failure_rate_per_content_token']} "
                f"to {census['attempts'][2]['modes']['composed']['containment_failure_rate_per_content_token']}."),
            "tension_evidence": (
                "Composed units rose "
                f"{census['findings']['composed_unit_count_trend']} across the attempts, because "
                "fidelity fixes are only reachable by composition. Under A, fidelity is bought "
                "with containment exposure."),
            "volume_evidence": (
                f"{reproduced['units']} of {reproduced['units'] + composed['units']} material "
                "units are already produced by verbatim reproduction. Free generation supplies a "
                "minority of the volume and all of the risk."),
        },
        "not_decided_on": [
            ("Not selected because a phase brief proposed it. The brief lists four readings and "
             "requires the evidence to choose; the census chooses, and it would have selected A "
             "had the composed and reproduced rates been comparable."),
            ("Not selected on a claim that the writer is inadequate. CF-01 records that all three "
             "attempts used one writer and that reading 4 is untested."),
            ("Not selected to make validation easier. Stage C is unchanged and every rejection "
             "code is retained; the renderer must pass the validator that rejected all three "
             "attempts."),
        ],
        "consequences": {
            "accepted": [
                "Prose becomes formulaic. For a technical standards book this is acceptable, and "
                "78% of current output is already verbatim source sentences.",
                "A renderer and Turkish suffixation must be built and tested before any prose.",
                "Realization data must be authored per claim, reusable across sections.",
            ],
            "gained": [
                "Containment becomes a static property provable without generating anything.",
                "A failed unit becomes a renderer bug with a deterministic repro, not a sample.",
                "Numerics, units, qualifiers, conditions, modality and citations stop being "
                "things a writer might drop.",
            ],
            "risks": [
                ("Expressiveness. If the plan IR cannot express a needed rhetorical move, the "
                 "renderer cannot produce it, and the failure is visible at contract time rather "
                 "than in prose. This is the intended direction of failure."),
                ("Morphology. Turkish suffixation with vowel harmony and consonant mutation must "
                 "be correct or the prose is ungrammatical. Bounded and unit-testable."),
                ("Renderer error becomes systematic rather than sporadic. Mitigated by the static "
                 "containment proof and by stage C still running unchanged."),
            ],
        },
        "rejected_alternatives": {
            option["id"]: option["verdict"] for option in matrix["options"]
            if option["id"] != "D"},
        "refined_cause_class": cause["refined_cause_class"],
        "supersedes_inference": cause["superseded_inference"]["inference"],
        "authorises": ("contracts, renderer and tests only. No prose generation is authorised by "
                       "this decision."),
        "does_not_authorise": [
            "attempt #4 — the identifier is retired; nothing may bear it",
            "any generation under architecture A",
            "rendering, retrieval, Qdrant writes or corpus reads",
            "modification of any validator, lexicon, gloss, allowlist, plan or preserved attempt",
        ],
    }


# ================================================================ 7. migration plan

def migration_plan() -> dict:
    return {
        "version": VERSION,
        "target_phase": "SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION",
        "principle": ("Contracts and renderer and tests first. The implementation phase produces "
                      "no prose, and the first prose under the new architecture is named "
                      "ARCHITECTURE V2 PILOT #1, never attempt #4."),
        "unchanged_and_frozen": [
            "corpus, normalized documents, chunks, embeddings",
            "Retriever v1, Context v1, Prompt v5, Output Contract v1.1",
            "Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1",
            "Extractor v1.1, P0 artifacts, SEC-02-2 readiness and composition-safety artifacts",
            "composition-safe allowlist, composition denylist, pair constraints",
            "function lexicon, paraphrase lexicon, translation glosses",
            "Section Drafting Contract v1, Book Citation Rendering Contract v1",
            "Draft Validator v1, v1.1, v1.2 — every stage, every rejection code",
            "draft plans v1, v1.1, v1.2",
            "preserved attempts #1, #2, #3 and every audit and rejection record",
            "DQS-C009-001 and the qualifier semantics registry",
        ],
        "new_artifacts": [
            {
                "id": "M1",
                "name": "draft_plan_ir_contract_v2",
                "kind": "contract",
                "purpose": ("the symbolic structure the LLM emits: an ordered list of typed "
                            "slots — claim id, rhetorical role, which conditions and qualifiers "
                            "to realise, citation intent, paragraph and subsection grouping"),
                "fail_closed_property": ("no free-text field anywhere in the IR. A plan carrying "
                                         "prose is rejected at parse, before rendering"),
            },
            {
                "id": "M2",
                "name": "claim_realization_contract_v2",
                "kind": "contract",
                "purpose": ("per-claim frozen realization data: canonical form, role-to-frame "
                            "bindings, approved condition renderings, registered qualifier "
                            "constructions, numeric and unit rendering, citation binding"),
                "reuses": ["translation_glosses", "draft_qualifier_semantics_v1",
                           "cross_lingual_condition_mappings_v1"],
            },
            {
                "id": "M3",
                "name": "turkish_morphology_v2",
                "kind": "module",
                "purpose": ("deterministic suffixation — vowel harmony, buffer consonants, "
                            "k/ğ and p/b mutation — so the renderer can inflect licensed stems "
                            "instead of selecting inflected surface forms"),
            },
            {
                "id": "M4",
                "name": "deterministic_surface_renderer_v2",
                "kind": "module",
                "purpose": "plan IR to Turkish prose. A pure function. No model call.",
                "invariant": ("output alphabet is a subset of the declared claims' licensed pool "
                              "plus a frozen closed grammatical scaffold"),
            },
            {
                "id": "M5",
                "name": "static_containment_proof_v2",
                "kind": "test harness",
                "purpose": ("enumerate every claim by every rhetorical role the contract admits, "
                            "render each, and assert zero failures from validator v1.2 stages A "
                            "through L — without generating anything"),
            },
        ],
        "sequence": [
            "M1 and M2 authored and frozen, with fixtures, before any renderer code",
            "M3 with morphology unit tests",
            "M4 against M1/M2, no model in the loop",
            "M5 as the gate: static containment proof over the full enumeration",
            "regression: the preserved attempts' accepted units must remain acceptable, and every "
            "rejected unit must remain rejected under the unchanged validator",
            "only then may a later phase authorise ARCHITECTURE V2 PILOT #1 on its own evidence",
        ],
        "llm_responsibility": [
            "which claims to draft and which to omit",
            "order of claims within a paragraph and of paragraphs within a subsection",
            "rhetorical role assignment per slot — identity, requirement, qualifier, condition, "
            "exemplification, scope limitation",
            "whether a qualifier gets its own unit or rides with its claim",
            "paragraph and subsection grouping, and topic coverage",
        ],
        "llm_explicitly_not_responsible_for": [
            "any surface word", "numeric rendering", "unit symbols", "qualifier wording",
            "condition wording", "modality", "citation strings", "morphology",
        ],
        "renderer_responsibility": [
            "factual surface realization from licensed stems",
            "numeric rendering with the unit its source uses",
            "qualifier realization against registered constructions",
            "condition realization against approved renderings",
            "modality — every requirement verb comes from a frozen scaffold",
            "citation binding through Book Citation Rendering Contract v1",
            "Turkish morphology",
        ],
        "out_of_scope": [
            "attempt #4 — retired identifier",
            "any prose generation in the implementation phase",
            "SEC-02-1, SEC-02-3, other sections, whole-book bibliography",
            "rendering or release of anything",
            "human technical review",
        ],
        "deferred_findings": [
            {
                "id": "DF-02",
                "finding": ("Function-word exemption is exact string membership over an "
                            "agglutinative language; `durumlarda` is exempt and `durumlarında` "
                            "is not."),
                "direction": ("a morphology-aware exemption test would place the boundary where "
                              "it was meant to be, without admitting relationship-bearing words"),
                "reason_not_actioned": ("this phase widens nothing, and under architecture D the "
                                        "renderer inflects licensed stems rather than selecting "
                                        "surface forms, so the defect stops being reachable. It "
                                        "remains a real defect in the validator and is recorded, "
                                        "not fixed"),
            },
            {
                "id": "DF-03",
                "finding": ("The licensed pool is built from every field of the claim record and "
                            "so contains English record metadata; it licenses `specific` and not "
                            "`spesifik` for a Turkish section."),
                "direction": "pool construction could be restricted to claim-bearing fields",
                "reason_not_actioned": ("narrowing the pool is a tightening, not a loosening, but "
                                        "it is still a validator change and this phase makes "
                                        "none"),
            },
            {
                "id": "CF-01",
                "finding": ("All three attempts used one writer at temperature 0.0, seed 11. "
                            "Reading 4 of the phase brief is untested, not refuted."),
                "direction": ("if architecture D's build ever stalls, a writer comparison under "
                              "architecture A is the cheapest remaining experiment"),
                "reason_not_actioned": ("it costs a generation, and the decision does not depend "
                                        "on it"),
            },
        ],
    }


# ================================================================ 8. assembly

def build_analysis() -> dict:
    census = build_census()
    classification = classify_words()
    probes = boundary_probes()
    cause = refined_cause(census, classification, probes)
    matrix = comparison_matrix(census, probes)
    decision = adr(census, cause, matrix)
    migration = migration_plan()

    attempts_prove = {
        "attempt_1": (
            "Reproduction alone satisfies containment and cannot satisfy fidelity. 16 material "
            "units, all reproduced, 0 unlicensed content tokens, and rejected for a dropped "
            "qualifier and a dropped condition — the two things reproduction cannot supply."),
        "attempt_2": (
            "Composition satisfies fidelity and breaks containment. The two units that could not "
            "be copied — the English-source claims — were the only composed ones, and one of "
            "them carried the section's first UNSUPPORTED_PROPOSITION."),
        "attempt_3": (
            "Instructions govern fidelity and do not govern containment. Every attempt-#2 cause "
            "closed, qualifier realisation 0/2 to 2/2, and the composed-mode rate stayed where it "
            "was. The remediation worked exactly as designed and the pilot was rejected anyway."),
        "the_series": (
            "The three attempts are not three failures of one kind. They are a demonstration that "
            "the architecture has two requirements it can satisfy one at a time. Attempt #1 "
            "bought containment with fidelity, attempt #2 bought fidelity with containment, "
            "attempt #3 bought more fidelity with more containment exposure at an unchanged "
            "rate."),
    }

    verdict = {
        "architecture_a_verdict": "NOT AN APPROPRIATE SCALABLE DRAFTING ARCHITECTURE",
        "grounds": [
            "its containment guarantee is a filter, so the outcome is sampled rather than "
            "established",
            "the sampled rate does not respond to the only lever it offers",
            "its two requirements trade against each other, and the trade worsens as fidelity "
            "improves",
            "the section-level outcome compounds over composed tokens, so it degrades as sections "
            "grow",
        ],
        "what_would_have_refuted_this": (
            "a composed-mode containment rate comparable to the reproduced mode's, or a rate that "
            "fell materially between attempt #2 and attempt #3. Neither is observed."),
    }

    return {
        "version": VERSION,
        "phase": PHASE,
        "section_id": SECTION_ID,
        "analysed_at": datetime.now(timezone.utc).isoformat(),
        "status": "CLOSED / GO",
        "what_the_attempts_prove": attempts_prove,
        "refined_cause": cause,
        "architecture_verdict": verdict,
        "word_classification": classification,
        "boundary_probes": probes,
        "comparison_matrix": matrix,
        "decision": decision,
        "migration_plan": migration,
        "accounting": {
            "generation_attempts": 0,
            "retrieval_calls": 0,
            "qdrant_writes": 0,
            "corpus_reads": 0,
            "prose_rendered": 0,
            "validators_weakened": [],
            "lexicons_widened": [],
            "frozen_artifacts_modified": [],
            "attempt_4_authorised": False,
        },
        "frozen_inputs": {
            "sha256": {name: sha_file(path) for name, path in sorted(FROZEN_INPUTS.items())},
        },
        "census": census,
    }


# ================================================================ 9. report

def write_report(analysis: dict) -> None:
    census = analysis["census"]
    lines: list[str] = []
    add = lines.append

    add(f"# {PHASE}")
    add("")
    add("**CLOSED / GO.** Architecture A rejected on three-attempt evidence. Architecture D "
        "selected. No generation, no attempt #4.")
    add("")
    add("")
    add("## The census")
    add("")
    add("Every material unit of every preserved attempt, classified by how it was produced and "
        "counted for containment separately.")
    add("")
    add("| Attempt | Reproduced units | Unlicensed / content tokens | Composed units | "
        "Unlicensed / content tokens | Composed rate |")
    add("|---|---|---|---|---|---|")
    for attempt in census["attempts"]:
        rep = attempt["modes"]["reproduced"]
        com = attempt["modes"]["composed"]
        add(f"| {attempt['attempt']} | {rep['unit_count']} | "
            f"{rep['unlicensed_token_count']} / {rep['content_tokens']} | "
            f"{com['unit_count']} | {com['unlicensed_token_count']} / {com['content_tokens']} | "
            f"{com['containment_failure_rate_per_content_token']} |")
    totals = census["totals"]
    add(f"| **total** | **{totals['reproduced']['units']}** | "
        f"**{totals['reproduced']['unlicensed']} / {totals['reproduced']['content_tokens']}** | "
        f"**{totals['composed']['units']}** | "
        f"**{totals['composed']['unlicensed']} / {totals['composed']['content_tokens']}** | "
        f"**{totals['composed']['failure_rate_per_content_token']}** |")
    add("")
    add(census["interpretation"])
    add("")
    add("Projected section-level outcome at the measured rate:")
    add("")
    add("| Composed units in a section | P(section clean) |")
    add("|---|---|")
    for row in census["findings"]["scaling_projection"]:
        add(f"| {row['composed_units']} | {row['expected_clean_section_probability']} |")
    add("")
    add("")
    add("## What attempts #1–#3 prove")
    add("")
    for key, text in analysis["what_the_attempts_prove"].items():
        add(f"**{key.replace('_', ' ')}.** {text}")
        add("")
    add("")
    add("## Refined attempt #3 root cause")
    add("")
    superseded = analysis["refined_cause"]["superseded_inference"]
    add(f"**Status: {superseded['status']}.**")
    add("")
    add(f"The previous inference: {superseded['inference']}")
    add("")
    for reason in superseded["why_insufficient"]:
        add(f"- {reason}")
    add("")
    add(f"**Refined cause class: {analysis['refined_cause']['refined_cause_class']}.**")
    add("")
    add(analysis["refined_cause"]["statement"])
    add("")
    add("| Cause | Weight | Accounts for |")
    add("|---|---|---|")
    for rc in analysis["refined_cause"]["contributing_causes"]:
        add(f"| {rc['id']} {rc['class']} | {rc['weight']} | {rc['accounts_for']} |")
    add("")
    confound = analysis["refined_cause"]["confound_recorded"]
    add(f"**{confound['id']}.** {confound['finding']} {confound['consequence']} "
        f"{confound['why_it_does_not_change_the_decision']}")
    add("")
    add("")
    add("## Attempt #3 word classification")
    add("")
    add("Categories: 1 grammatical/discourse surface · 2 semantic paraphrase · "
        "3 relationship-bearing · 4 proposition-changing.")
    add("")
    add("| Word | Categories | Primary | Category 4 excluded | Basis |")
    add("|---|---|---|---|---|")
    for word in analysis["word_classification"]["words"]:
        excluded = "yes" if word["category_4_excluded"] else "**no**"
        add(f"| `{word['word']}` | {', '.join(word['categories'])} | {word['primary']} | "
            f"{excluded} | {word['rationale']} |")
    add("")
    for word in analysis["word_classification"]["words"]:
        add(f"**`{word['word']}`** — {word['gloss']}. {word['category_4_note']}")
        add("")
    add(analysis["word_classification"]["finding"])
    add("")
    add(analysis["word_classification"]["consequence"])
    add("")
    add("")
    add("## Current architecture verdict")
    add("")
    add(f"**{analysis['architecture_verdict']['architecture_a_verdict']}.**")
    add("")
    for ground in analysis["architecture_verdict"]["grounds"]:
        add(f"- {ground}")
    add("")
    add(f"What would have refuted this: {analysis['architecture_verdict']['what_would_have_refuted_this']}")
    add("")
    add("")
    add("## A / B / C / D")
    add("")
    add("| | Containment guarantee | Weakens stage C | Scaling | Verdict |")
    add("|---|---|---|---|---|")
    for option in analysis["comparison_matrix"]["options"]:
        add(f"| **{option['id']}** {option['name']} | {option['containment_guarantee']} | "
            f"{'**yes**' if option['weakens_stage_c'] else 'no'} | {option['scaling']} | "
            f"{option['verdict']} |")
    add("")
    option_b = next(o for o in analysis["comparison_matrix"]["options"] if o["id"] == "B")
    add(f"**Why lexicon widening is rejected.** {option_b['weakening_stated_plainly']}")
    add("")
    add("")
    add("## Decision")
    add("")
    decision = analysis["decision"]
    add(f"**{decision['id']} — {decision['title']}. {decision['status']}.**")
    add("")
    add(decision["decision"])
    add("")
    add("Decided on:")
    add("")
    for key, text in decision["decided_on"].items():
        add(f"- *{key.replace('_', ' ')}* — {text}")
    add("")
    add("Not decided on:")
    add("")
    for text in decision["not_decided_on"]:
        add(f"- {text}")
    add("")
    add("")
    add("## Responsibility split")
    add("")
    migration = analysis["migration_plan"]
    add("| LLM | Deterministic renderer |")
    add("|---|---|")
    llm = migration["llm_responsibility"]
    renderer = migration["renderer_responsibility"]
    for i in range(max(len(llm), len(renderer))):
        add(f"| {llm[i] if i < len(llm) else ''} | {renderer[i] if i < len(renderer) else ''} |")
    add("")
    add("The LLM emits no surface word. It is explicitly not responsible for: "
        + ", ".join(migration["llm_explicitly_not_responsible_for"]) + ".")
    add("")
    add("")
    add("## Migration scope")
    add("")
    add("Unchanged and frozen:")
    add("")
    for item in migration["unchanged_and_frozen"]:
        add(f"- {item}")
    add("")
    add("New in the implementation phase:")
    add("")
    add("| | Artifact | Kind | Purpose |")
    add("|---|---|---|---|")
    for artifact in migration["new_artifacts"]:
        add(f"| {artifact['id']} | `{artifact['name']}` | {artifact['kind']} | "
            f"{artifact['purpose']} |")
    add("")
    add("Sequence:")
    add("")
    for step in migration["sequence"]:
        add(f"1. {step}")
    add("")
    add("")
    add("## Deferred findings")
    add("")
    for deferred in migration["deferred_findings"]:
        add(f"**{deferred['id']}.** {deferred['finding']} Direction: {deferred['direction']}. "
            f"Not actioned — {deferred['reason_not_actioned']}.")
        add("")
    add("")
    add("## Phase accounting")
    add("")
    add("| | |")
    add("|---|---|")
    for key, value in sorted(analysis["accounting"].items()):
        rendered = value if not isinstance(value, list) else (", ".join(value) or "none")
        add(f"| {key.replace('_', ' ')} | {rendered} |")
    add("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(analysis: dict) -> None:
    write_json(MANIFEST_PATH, {
        "version": VERSION,
        "section_id": SECTION_ID,
        "phase": PHASE,
        "generated_at": analysis["analysed_at"],
        "status": "closed_go",
        "final_decision": f"{PHASE} — CLOSED / GO",
        "architecture_selected": analysis["comparison_matrix"]["selected"],
        "architecture_a_verdict": analysis["architecture_verdict"]["architecture_a_verdict"],
        "refined_cause_class": analysis["refined_cause"]["refined_cause_class"],
        "superseded_inference_status": analysis["refined_cause"]["superseded_inference"]["status"],
        "lexicon_widening": "REJECTED",
        "generation_attempts": 0,
        "retrieval_calls": 0,
        "qdrant_writes": 0,
        "corpus_reads": 0,
        "prose_rendered": 0,
        "validators_weakened": [],
        "lexicons_widened": [],
        "frozen_artifacts_modified": [],
        "attempt_4_authorised": False,
        "frozen_inputs_sha256": analysis["frozen_inputs"]["sha256"],
        "artifacts": {
            "analysis": str(ANALYSIS_PATH.relative_to(ROOT)),
            "census": str(CENSUS_PATH.relative_to(ROOT)),
            "probes": str(PROBES_PATH.relative_to(ROOT)),
            "comparison_matrix": str(MATRIX_PATH.relative_to(ROOT)),
            "adr": str(ADR_PATH.relative_to(ROOT)),
            "migration_plan": str(MIGRATION_PATH.relative_to(ROOT)),
            "report": str(REPORT_PATH.relative_to(ROOT)),
            "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
            "script": "scripts/57_sec_02_2_drafting_approach_rethink_v1.py",
            "tests": "tests/test_sec_02_2_drafting_approach_rethink_v1.py",
        },
        "analysis_sha256": sha_file(ANALYSIS_PATH),
        "adr_sha256": sha_file(ADR_PATH),
        "next_phase": "SEC-02-2 DRAFTING ARCHITECTURE V2 IMPLEMENTATION",
        "first_pilot_identifier": "ARCHITECTURE V2 PILOT #1",
        "attempt_4_identifier": "retired",
        "deferred_findings": [d["id"] for d in analysis["migration_plan"]["deferred_findings"]],
    })


def main() -> int:
    analysis = build_analysis()
    write_json(CENSUS_PATH, analysis["census"])
    write_json(PROBES_PATH, {"boundary": analysis["boundary_probes"],
                             "classification": analysis["word_classification"]})
    write_json(MATRIX_PATH, analysis["comparison_matrix"])
    write_json(ADR_PATH, analysis["decision"])
    write_json(MIGRATION_PATH, analysis["migration_plan"])
    write_json(ANALYSIS_PATH, analysis)
    write_report(analysis)
    write_manifest(analysis)

    totals = analysis["census"]["totals"]
    print(f"reproduced: {totals['reproduced']['unlicensed']} unlicensed / "
          f"{totals['reproduced']['content_tokens']} content tokens")
    print(f"composed:   {totals['composed']['unlicensed']} unlicensed / "
          f"{totals['composed']['content_tokens']} content tokens "
          f"(p={totals['composed']['failure_rate_per_content_token']})")
    print(f"architecture A: {analysis['architecture_verdict']['architecture_a_verdict']}")
    print(f"selected: {analysis['comparison_matrix']['selected']}")
    print(f"refined cause: {analysis['refined_cause']['refined_cause_class']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
