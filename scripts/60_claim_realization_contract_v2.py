"""M2 — Claim Realization Contract v2. Frozen surface material, one entry per claim and role.

This is not a new evidence layer and it must not become one. Every factual element it stores is
copied from an already-approved frozen field — a claim's canonical sentence, its conditions, its
qualifiers, its registered numerics, its translation glosses. Nothing here paraphrases, and
nothing here invents a synonym.

The build is a constructive search with a guard, and the guard is what makes the contract
trustworthy rather than merely careful. For each claim and role it assembles candidate segments
out of frozen material, then checks every content token of the result against the same licensed
pool the frozen Draft Validator computes for that claim. A token outside the pool does not get
patched, whitelisted or excused: the whole entry is marked UNREALIZABLE and the offending tokens
are recorded. That is why the contract can be small and still honest — what could not be built
from approved semantics is visible as a gap rather than filled from model knowledge.

The rule caught real cases, and they are worth naming because they are the contract working.
SEC-02-2-C-002 has two registered numerics whose own condition strings distinguish the individual
sample minimum from the three-sample group average. Those strings are not part of the claim's
licensed pool — `grup` shares only three characters with the pooled `grubun` — so
NUMERIC_CRITERIA for that claim is UNREALIZABLE, and its figures reach prose through the
canonical sentence, which states them precisely and is licensed by construction. Rendering the
two numbers without the labels that distinguish them would have been the alternative, and it
would have been worse.

Three claims carry English canonical sentences. Their Turkish material is the frozen
`translation_glosses` and `condition_glosses`, which are token lists, not sentences. For those a
gloss frame orders frozen tokens against the frozen grammatical scaffold. Ordering approved
tokens is a transformation of approved semantics; choosing a token those lists do not contain
would not be, and the guard is what enforces the difference.

The scaffold itself is closed and self-checking. Every scaffold token is either shorter than the
support test's minimum content-word length — Turkish grammar lives in those — or present in the
frozen function lexicon. No scaffold token may appear in the prohibited causal, expansion or
universal marker sets, and none may be an attribution marker from DSC-C002-001. The check runs at
build time, so a scaffold that drifted out of the lexicon would fail the build rather than the
pilot.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONTRACT_VERSION = "tunnelbook-claim-realization-contract-v2"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
CONTRACT_PATH = ARCH_V2 / "contracts" / "claim_realization_contract_v2.json"
VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
PLAN_IR = ROOT / "scripts" / "59_semantic_plan_ir_contract_v2.py"
MORPHOLOGY = ROOT / "scripts" / "61_turkish_morphology_v2.py"
SEMANTIC_CONSTRAINTS = (ROOT / "data" / "book" / "drafting" / "sec_02_2" / "remediation_v1"
                        / "contracts" / "draft_semantic_constraints_v1.json")

TURKISH_MARK = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


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


# ================================================================ frozen scaffold

# Punctuation the renderer may emit. It carries no lexical content and the support test's
# tokenizer does not see it at all.
SCAFFOLD_PUNCTUATION = (",", ";", ":", ".", "(", ")", "-")

# Grammatical connectives. Every one is checked at build time against the frozen function
# lexicon, or is shorter than the support test's content-word minimum.
SCAFFOLD_TOKENS = (
    "ve", "veya", "ile", "gibi", "olarak", "için", "ise", "daha", "bu", "en",
)

# Never scaffold, whatever the lexicon says: these assert relations or attribute authorship.
SCAFFOLD_FORBIDDEN = (
    "bu nedenle", "dolayısıyla", "bunun sonucunda", "sayesinde", "böylece", "ancak",
    "buna karşın", "göre", "uyarınca", "gereğince", "gereği", "esas alınır",
)

ROLES = ("CLAIM_STATEMENT", "REQUIREMENT", "IDENTITY_SCOPE", "QUALIFIER_SCOPE",
         "CONDITION", "EXEMPLIFICATION", "NUMERIC_CRITERIA")

# ---- gloss frames for the three claims whose canonical sentence is English.
# Each entry is an ordered list of segments. Every GLOSS token below is copied from the frozen
# translation_glosses or condition_glosses of that same claim; the build asserts it.
GLOSS_FRAMES: dict[str, dict[str, list[dict]]] = {
    "SEC-02-2-P0-007": {
        "CLAIM_STATEMENT": [
            {"kind": "GLOSS", "token": "tipik"}, {"kind": "GLOSS", "token": "ilk"},
            {"kind": "GLOSS", "token": "püskürtme"}, {"kind": "GLOSS", "token": "beton"},
            {"kind": "GLOSS", "token": "kaplama"}, {"kind": "GLOSS", "token": "kalınlığı"},
            {"kind": "GLOSS", "token": "zemin"}, {"kind": "GLOSS", "token": "koşullarına"},
            {"kind": "SCAFFOLD", "token": "ve"}, {"kind": "GLOSS", "token": "tünel"},
            {"kind": "GLOSS", "token": "açıklığının"}, {"kind": "GLOSS", "token": "boyutuna"},
            {"kind": "GLOSS", "token": "bağlı"}, {"kind": "SCAFFOLD", "token": "olarak"},
            {"kind": "LICENSED_NUMERIC", "value": "100-400", "unit": "mm"},
            {"kind": "GLOSS", "token": "aralığında"},
            {"kind": "GLOSS", "token": "değişmektedir"},
            {"kind": "SCAFFOLD", "token": "."},
        ],
        "CONDITION": [
            {"kind": "GLOSS", "token": "zemin"}, {"kind": "GLOSS", "token": "koşullarına"},
            {"kind": "SCAFFOLD", "token": "ve"}, {"kind": "GLOSS", "token": "tünel"},
            {"kind": "GLOSS", "token": "açıklığının"}, {"kind": "GLOSS", "token": "boyutuna"},
            {"kind": "GLOSS", "token": "bağlı"}, {"kind": "SCAFFOLD", "token": "olarak"},
            {"kind": "GLOSS", "token": "değişir"}, {"kind": "SCAFFOLD", "token": "."},
        ],
    },
    "SEC-02-2-P0-008": {
        "CLAIM_STATEMENT": [
            {"kind": "GLOSS", "token": "belirli"}, {"kind": "GLOSS", "token": "kaya"},
            {"kind": "GLOSS", "token": "koşullarında"}, {"kind": "SCAFFOLD", "token": ","},
            {"kind": "GLOSS", "token": "tünel"}, {"kind": "GLOSS", "token": "boyutuna"},
            {"kind": "GLOSS", "token": "bağlı"}, {"kind": "SCAFFOLD", "token": "olarak"},
            {"kind": "SCAFFOLD", "token": ","}, {"kind": "GLOSS", "token": "kalınlık"},
            {"kind": "LICENSED_NUMERIC", "value": "300", "unit": "mm"},
            {"kind": "SCAFFOLD", "token": "ve"}, {"kind": "GLOSS", "token": "daha"},
            {"kind": "GLOSS", "token": "fazla"}, {"kind": "GLOSS", "token": "olabilir"},
            {"kind": "SCAFFOLD", "token": "."},
        ],
        "EXEMPLIFICATION": [
            {"kind": "GLOSS", "token": "ezilmiş"}, {"kind": "SCAFFOLD", "token": "veya"},
            {"kind": "GLOSS", "token": "sıkışan"}, {"kind": "GLOSS", "token": "kaya"},
            {"kind": "SCAFFOLD", "token": "gibi"}, {"kind": "GLOSS", "token": "belirli"},
            {"kind": "GLOSS", "token": "kaya"}, {"kind": "GLOSS", "token": "koşullarında"},
            {"kind": "GLOSS", "token": "kalınlık"}, {"kind": "GLOSS", "token": "daha"},
            {"kind": "GLOSS", "token": "fazla"}, {"kind": "GLOSS", "token": "olabilir"},
            {"kind": "SCAFFOLD", "token": "."},
        ],
        "CONDITION": [
            {"kind": "GLOSS", "token": "bazı"}, {"kind": "GLOSS", "token": "belirli"},
            {"kind": "GLOSS", "token": "kaya"}, {"kind": "GLOSS", "token": "koşullarında"},
            {"kind": "SCAFFOLD", "token": "ve"}, {"kind": "GLOSS", "token": "tünel"},
            {"kind": "GLOSS", "token": "boyutuna"}, {"kind": "GLOSS", "token": "bağlı"},
            {"kind": "SCAFFOLD", "token": "olarak"}, {"kind": "GLOSS", "token": "kalınlık"},
            {"kind": "GLOSS", "token": "olabilir"}, {"kind": "SCAFFOLD", "token": "."},
        ],
    },
    "SEC-02-2-R025": {
        "CLAIM_STATEMENT": [
            {"kind": "GLOSS", "token": "flashcrete"}, {"kind": "SCAFFOLD", "token": ","},
            {"kind": "GLOSS", "token": "sistematik"}, {"kind": "GLOSS", "token": "uygulanan"},
            {"kind": "GLOSS", "token": "ilk"}, {"kind": "GLOSS", "token": "püskürtme"},
            {"kind": "GLOSS", "token": "beton"}, {"kind": "GLOSS", "token": "kaplama"},
            {"kind": "SCAFFOLD", "token": ","}, {"kind": "GLOSS", "token": "normalde"},
            {"kind": "GLOSS", "token": "aktif"}, {"kind": "GLOSS", "token": "destek"},
            {"kind": "GLOSS", "token": "sayılmaz"}, {"kind": "SCAFFOLD", "token": "."},
        ],
    },
}


# ================================================================ helpers

def load_claims(bundle) -> dict[str, dict]:
    return {cid: row for cid, row in bundle.allowlist.items()
            if row.get("section_id") == SECTION_ID}


def is_turkish(text: str) -> bool:
    return bool(TURKISH_MARK.search(text))


def scaffold_audit(bundle) -> dict:
    """The scaffold must be grammar the support test already ignores. Checked, not assumed."""
    v1 = module("v1", VALIDATOR_V1)
    prohibited = {v1.fold(m) for family in bundle.prohibited.values() for m in family}
    constraints = json.loads(SEMANTIC_CONSTRAINTS.read_text(encoding="utf-8"))
    attribution = {v1.fold(m) for c in constraints["constraints"]
                   for m in c["forbidden_meaning_patterns"].get("attribution_markers", [])}
    rows = []
    for token in SCAFFOLD_TOKENS:
        folded = v1.fold(token)
        below_min = len(folded) < 3
        in_lexicon = folded in bundle.function_lexicon
        ok = (below_min or in_lexicon) and folded not in prohibited and folded not in attribution
        rows.append({"token": token, "below_content_minimum": below_min,
                     "in_function_lexicon": in_lexicon,
                     "is_prohibited_marker": folded in prohibited,
                     "is_attribution_marker": folded in attribution, "admissible": ok})
    for phrase in SCAFFOLD_FORBIDDEN:
        if any(v1.fold(phrase) == v1.fold(t) for t in SCAFFOLD_TOKENS):
            rows.append({"token": phrase, "admissible": False,
                         "is_relation_or_attribution": True})
    return {"tokens": rows, "punctuation": list(SCAFFOLD_PUNCTUATION),
            "all_admissible": all(r["admissible"] for r in rows)}


def frozen_glosses(bundle, claim_id: str) -> set[str]:
    v1 = module("v1", VALIDATOR_V1)
    tokens = {v1.fold(t) for t in bundle.translation_glosses.get(claim_id, [])}
    for gloss_list in (bundle.contract.get("condition_glosses", {})
                       .get(claim_id, {}).values()):
        tokens |= {v1.fold(t) for t in gloss_list}
    return tokens


# ================================================================ segment construction

class UnrenderableSegment(Exception):
    """A segment whose surface cannot be produced deterministically from frozen data."""


def _text_segment(origin: str, value: str) -> dict:
    return {"kind": "FROZEN_TEXT", "origin": origin, "value": value}


def build_segments(claim_id: str, claim: dict, role: str, bundle) -> tuple[list[dict], str]:
    """Candidate segments for a claim and role, or a reason the pair cannot be built."""
    canonical = (claim.get("canonical_claim") or "").strip()
    conditions = list(claim.get("conditions") or [])
    qualifiers = list(claim.get("qualifiers") or [])
    numerics = list(claim.get("numeric") or [])
    frames = GLOSS_FRAMES.get(claim_id, {})

    if role in ("CLAIM_STATEMENT", "REQUIREMENT"):
        if role == "REQUIREMENT" and modality_level(canonical, bundle) < 2:
            return [], ("the claim's own wording carries no binding or recommended modality, so "
                        "REQUIREMENT would strengthen it")
        if is_turkish(canonical):
            return [_text_segment("canonical_claim", canonical)], ""
        if role in frames:
            return list(frames[role]), ""
        return [], ("the canonical sentence is not Turkish and no frozen gloss frame exists for "
                    "this claim")

    if role == "QUALIFIER_SCOPE":
        if not qualifiers:
            return [], "the claim registers no qualifier"
        if not is_turkish(qualifiers[0]):
            return [], "the registered qualifier is not Turkish and has no frozen gloss frame"
        return (_condition_prefix(claim, bundle)
                + [_text_segment("qualifiers[0]", qualifiers[0]),
                   {"kind": "SCAFFOLD", "token": "."}]), ""

    if role == "IDENTITY_SCOPE":
        # What a referenced table or clause *is*. Only where a frozen qualifier's leading clause
        # already says so; splitting frozen text at its own semicolon is deterministic and
        # removes nothing.
        document_scope = (claim.get("scope") or {}).get("document_scope") or ""
        if not qualifiers or not document_scope:
            return [], "no registered qualifier or no document scope to state an identity for"
        lead = qualifiers[0].split(";")[0].strip()
        reference = document_scope.split("(")[0].strip()
        if not lead or not reference or reference.lower() not in lead.lower():
            return [], ("the registered qualifier's leading clause does not state what the "
                        "referenced document is")
        return (_condition_prefix(claim, bundle)
                + [_text_segment("qualifiers[0].clause[0]", lead),
                   {"kind": "SCAFFOLD", "token": "."}]), ""

    if role == "CONDITION":
        if role in frames:
            return list(frames[role]), ""
        if not conditions:
            return [], "the claim registers no condition"
        if not all(is_turkish(c) for c in conditions):
            return [], "a registered condition is not Turkish and has no frozen gloss frame"
        segments: list[dict] = []
        for index, condition in enumerate(conditions):
            if index:
                segments.append({"kind": "SCAFFOLD", "token": ","})
            segments.append(_text_segment(f"conditions[{index}]", condition))
        segments.append({"kind": "SCAFFOLD", "token": "."})
        return segments, ""

    if role == "EXEMPLIFICATION":
        if role in frames:
            return _condition_prefix(claim, bundle) + list(frames[role]), ""
        return [], ("the claim carries no frozen exemplification material; an example not stated "
                    "by the source may not be supplied")

    if role == "NUMERIC_CRITERIA":
        if not numerics:
            return [], "the claim registers no numeric"
        if not all(n.get("source_stated") for n in numerics):
            return [], "a registered numeric is not source-stated"
        if any(n.get("derived") for n in numerics):
            return [], "a registered numeric is derived; only source-stated figures render"
        if not all(n.get("unit") for n in numerics):
            return [], ("a registered numeric carries no unit, so it cannot be rendered as a "
                        "criterion without inventing one")
        labels = [n.get("condition") for n in numerics]
        if not all(labels):
            return [], ("a registered numeric carries no condition label, so two figures could "
                        "not be told apart in prose")
        segments = _condition_prefix(claim, bundle)
        for index, numeric in enumerate(numerics):
            if index:
                segments.append({"kind": "SCAFFOLD", "token": ";"})
            segments.append(_text_segment(f"numeric[{index}].condition", numeric["condition"]))
            segments.append({"kind": "SCAFFOLD", "token": ":"})
            segments.append({"kind": "LICENSED_NUMERIC", "value": str(numeric["value"]),
                             "unit": str(numeric["unit"]),
                             "copula": (index == len(numerics) - 1
                                        and _claim_writes_copula(claim_id, str(numeric["unit"]),
                                                                 bundle))})
        segments.append({"kind": "SCAFFOLD", "token": "."})
        return segments, ""

    return [], f"role {role} has no construction rule"


def unit_scoped_conditions(claim: dict, bundle) -> list[str]:
    """Delegated to the plan IR contract, which owns this computation.

    Two implementations of "which conditions are sentence-internal" would be two chances to
    disagree with stage E. There is one, and it lives in the contract layer.
    """
    return module("plan_ir", PLAN_IR).unit_scoped_conditions(claim, bundle)


def _condition_prefix(claim: dict, bundle) -> list[dict]:
    """Frozen condition text, ahead of a supporting role, joined by the scaffold's 'için'."""
    scoped = unit_scoped_conditions(claim, bundle)
    if not scoped:
        return []
    segments: list[dict] = []
    for index, condition in enumerate(scoped):
        if index:
            segments.append({"kind": "SCAFFOLD", "token": ","})
        segments.append(_text_segment(f"conditions[{index}]", condition))
    segments.append({"kind": "SCAFFOLD", "token": "için"})
    return segments


def _claim_writes_copula(claim_id: str, unit_symbol: str, bundle) -> bool:
    """Does this claim's own approved wording attach the copula to this unit symbol?

    SEC-02-2-C-009's canonical sentence writes "100-150 mm'dir", so a numeric-criteria sentence
    for that claim may write it too. SEC-02-2-C-004 registers mm and never inflects it, so its
    criteria render the bare figure. The rule is the source's own wording, not what the validator
    would tolerate — the containment guard below is a backstop for this decision, not its reason.
    """
    v1 = module("v1", VALIDATOR_V1)
    morph = module("morphology", MORPHOLOGY)
    try:
        inflected = morph.copula(unit_symbol)
    except morph.MorphologyError:
        return False
    pool = v1.licensed_tokens([claim_id], bundle)
    return all(any(v1.prefix_agreement(token, licensed) for licensed in pool)
               for token in v1.content_tokens(inflected, bundle.function_lexicon))


def modality_level(text: str, bundle) -> int:
    """Highest modality level the claim's own wording carries, from the frozen lattice."""
    v1 = module("v1", VALIDATOR_V1)
    folded = v1.fold(text)
    lattice = bundle.contract["modality_lattice"]["markers"]
    excluded = {v1.fold(w) for w in bundle.contract["modality_lattice"]["bound_words_excluded"]}
    best = 0
    for level, markers in lattice.items():
        for marker in markers:
            folded_marker = v1.fold(marker)
            if folded_marker in excluded:
                continue
            if re.search(rf"(?<![a-zçğıöşü]){re.escape(folded_marker)}", folded):
                best = max(best, int(level))
    return best


# ================================================================ the guard

def preview_text(segments: list[dict], claim: dict, bundle) -> str:
    """Assemble segments the way the renderer will, so the guard checks the real string.

    This mirrors M4 rather than duplicating its judgement: M4 imports this contract and follows
    the same segment kinds, and the static containment proof renders through M4, not through
    here. This exists so an entry that would fail containment never reaches the contract.
    """
    parts: list[str] = []
    for segment in segments:
        kind = segment["kind"]
        if kind == "FROZEN_TEXT":
            parts.append(segment["value"])
        elif kind == "GLOSS":
            parts.append(segment["token"])
        elif kind == "SCAFFOLD":
            parts.append(segment["token"])
        elif kind == "LICENSED_NUMERIC":
            rendered = f"{segment['value']} {segment['unit']}"
            if segment.get("copula"):
                morph = module("morphology", MORPHOLOGY)
                try:
                    rendered = morph.copula(rendered)
                except morph.MorphologyError as error:
                    # No frozen pronunciation for the unit symbol, so harmony cannot be read.
                    # Refusing here makes the entry UNREALIZABLE rather than guessing a suffix.
                    raise UnrenderableSegment(str(error)) from error
            parts.append(rendered)
    return join_parts(parts)


def join_parts(parts: list[str]) -> str:
    """Spacing rules. Deterministic, and shared with the renderer so previews cannot diverge."""
    out = ""
    for part in parts:
        if not out:
            out = part
        elif part in (",", ";", ":", ".", ")"):
            out += part
        elif out.endswith("(") or out.endswith("-"):
            out += part
        elif part in ("(",):
            out += " " + part
        else:
            out += " " + part
    return out


def containment_check(text: str, claim_id: str, bundle) -> list[str]:
    """Every content token against the same pool the frozen validator computes. No exceptions."""
    v1 = module("v1", VALIDATOR_V1)
    pool = v1.licensed_tokens([claim_id], bundle)
    return v1.unlicensed(text, pool, bundle)


# ================================================================ build

def build_contract() -> dict:
    v1 = module("v1", VALIDATOR_V1)
    bundle = v1.load_bundle()
    claims = load_claims(bundle)
    scaffold = scaffold_audit(bundle)
    if not scaffold["all_admissible"]:
        raise SystemExit("scaffold audit failed: a scaffold token is not grammar the support "
                         "test ignores")

    entries: list[dict] = []
    for claim_id in sorted(claims):
        claim = claims[claim_id]
        gloss_pool = frozen_glosses(bundle, claim_id)
        for role in ROLES:
            segments, reason = build_segments(claim_id, claim, role, bundle)
            entry: dict[str, Any] = {
                "claim_id": claim_id,
                "realization_role": role,
                "source_keys": sorted(claim.get("source_keys") or []),
                "allowed_relationships": sorted(claim.get("allowed_relationships") or []),
            }
            if not segments:
                entry.update({"status": "UNREALIZABLE", "reason": reason, "segments": []})
                entries.append(entry)
                continue

            allowed_numerics = v1.licensed_numerics([claim_id], bundle)
            stray_numeric = [
                f"{s['value']} {s['unit']}" for s in segments
                if s["kind"] == "LICENSED_NUMERIC"
                and (v1._normalise_value(s["value"]),
                     v1.fold(s["unit"]).replace("³", "3")) not in allowed_numerics]
            if stray_numeric:
                entry.update({"status": "UNREALIZABLE", "segments": [],
                              "reason": f"numeric the frozen validator does not license for this "
                                        f"claim: {sorted(set(stray_numeric))}"})
                entries.append(entry)
                continue

            stray_gloss = [s["token"] for s in segments
                           if s["kind"] == "GLOSS" and v1.fold(s["token"]) not in gloss_pool]
            if stray_gloss:
                entry.update({"status": "UNREALIZABLE", "segments": [],
                              "reason": f"gloss frame uses tokens the frozen glosses do not "
                                        f"license: {sorted(set(stray_gloss))}"})
                entries.append(entry)
                continue

            try:
                text = preview_text(segments, claim, bundle)
            except UnrenderableSegment as error:
                entry.update({"status": "UNREALIZABLE", "segments": [],
                              "reason": f"surface cannot be produced deterministically: {error}"})
                entries.append(entry)
                continue
            stray = containment_check(text, claim_id, bundle)
            if stray:
                entry.update({"status": "UNREALIZABLE", "segments": [],
                              "reason": f"assembled surface leaves the claim's licensed pool: "
                                        f"{stray}"})
                entries.append(entry)
                continue

            entry.update({
                "status": "REALIZABLE",
                "segments": segments,
                "frame_id": f"{claim_id}/{role}",
                "modality_level": modality_level(claim.get("canonical_claim") or "", bundle),
                "numeric_fact_ids": [f"{claim_id}#NUM{i}"
                                     for i in range(len(claim.get("numeric") or []))],
                "condition_ids": [f"{claim_id}#COND{i}"
                                  for i in range(len(claim.get("conditions") or []))],
                "qualifier_ids": [f"{claim_id}#QUAL{i}"
                                  for i in range(len(claim.get("qualifiers") or []))],
                "preview_sha256": __import__("hashlib").sha256(text.encode("utf-8")).hexdigest(),
            })
            entries.append(entry)

    realizable = [e for e in entries if e["status"] == "REALIZABLE"]
    return {
        "version": CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "parent_contracts": [
            "tunnelbook-section-drafting-contract-v1",
            "tunnelbook-semantic-plan-ir-contract-v2",
            "tunnelbook-draft-qualifier-semantics-v1",
        ],
        "principle": ("Every factual lexical element is copied from a frozen approved claim "
                      "field. Nothing is paraphrased and no synonym is invented. An entry whose "
                      "assembled surface leaves the claim's licensed pool is UNREALIZABLE."),
        "frozen_material_sources": [
            "canonical_claim", "conditions", "qualifiers", "numeric",
            "scope.document_scope", "translation_glosses", "condition_glosses",
        ],
        "segment_kinds": {
            "FROZEN_TEXT": "a frozen claim field, copied verbatim",
            "GLOSS": "a token from the claim's own frozen translation or condition glosses",
            "SCAFFOLD": "a grammatical connector from the frozen closed scaffold",
            "LICENSED_NUMERIC": ("a value/unit pair the frozen validator already licenses for "
                                 "this claim, checked against licensed_numerics at build time"),
        },
        "scaffold": scaffold,
        "scaffold_forbidden": list(SCAFFOLD_FORBIDDEN),
        "roles": list(ROLES),
        "entries": entries,
        "totals": {
            "claims": len(claims),
            "roles": len(ROLES),
            "pairs": len(entries),
            "realizable": len(realizable),
            "unrealizable": len(entries) - len(realizable),
        },
    }


class RealizationContract:
    """Lookup over the built contract, used by plan validation and by the renderer."""

    def __init__(self, payload: dict):
        self.payload = payload
        self._by_key = {(e["claim_id"], e["realization_role"]): e for e in payload["entries"]}

    @classmethod
    def load(cls, path: Path = CONTRACT_PATH) -> "RealizationContract":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def entry(self, claim_id: str, role: str) -> dict | None:
        return self._by_key.get((claim_id, role))

    def realizable_pairs(self) -> list[tuple[str, str]]:
        return sorted(key for key, entry in self._by_key.items()
                      if entry["status"] == "REALIZABLE")


def main() -> int:
    contract = build_contract()
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    totals = contract["totals"]
    print(f"realization contract written: {CONTRACT_PATH.relative_to(ROOT)}")
    print(f"pairs {totals['pairs']} = realizable {totals['realizable']} + "
          f"unrealizable {totals['unrealizable']}")
    by_role: dict[str, int] = {}
    for entry in contract["entries"]:
        if entry["status"] == "REALIZABLE":
            by_role[entry["realization_role"]] = by_role.get(entry["realization_role"], 0) + 1
    for role in ROLES:
        print(f"  {role:20} {by_role.get(role, 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
