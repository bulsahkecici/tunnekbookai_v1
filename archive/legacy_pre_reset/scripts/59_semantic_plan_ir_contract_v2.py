"""M1 — Semantic Plan IR Contract v2. The symbolic structure the planner emits, and its gate.

Architecture V2 splits drafting at one line: the planner decides *which* claims are stated, in
*what order*, and in *what role*; the renderer decides every word. This module owns the line. A
plan is a tree of identifiers and enumerated roles, and the only free-form things in it are the
ids naming its own nodes.

Two mechanisms keep prose out, because one is not enough.

**Closed schema.** Every object declares its permitted keys and every key declares its type. An
unknown key is a rejection, not an ignored extra. A blocklist of suspicious names — `text`,
`prose`, `sentence` — would only catch a planner that names its smuggling honestly; requiring
each key to be known catches one that does not.

**Typed leaf values.** The leaves that survive are ids, and an id must match `ID_RE`: no spaces,
bounded length. A sentence cannot be spelled as an identifier, so there is nowhere left to put
one. `SLOT_LEAF_TYPES` is what makes this checkable rather than asserted.

The roles are closed and enumerated. There is deliberately no FREEFORM and no OTHER: a role that
means "something else" is a hole in a contract whose entire purpose is having no holes, and an
unknown role is rejected rather than degraded to a default. Each role names which part of a
frozen claim record gets realised, which is why the set is small and why extending it is a
contract change rather than a code change.

Plan validation proves what it can before the renderer runs — that the claim is allowlisted and
composition-safe, that it is not denylisted, that every source key, numeric, condition and
qualifier the slot asks for belongs to the claim that declares it, and that no relation is
asserted which the claim does not allow. None of that requires reading prose, because at this
layer there is none.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONTRACT_VERSION = "tunnelbook-semantic-plan-ir-contract-v2"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
CONTRACT_PATH = ARCH_V2 / "contracts" / "semantic_plan_ir_contract_v2.json"

# The closed role set. Each names which part of a frozen claim record is realised.
REALIZATION_ROLES: dict[str, str] = {
    "CLAIM_STATEMENT": "the claim's own proposition, from its approved canonical semantics",
    "REQUIREMENT": "the claim's proposition where the claim itself carries binding modality",
    "IDENTITY_SCOPE": "what a referenced table or clause *is*, where a frozen field states it",
    "QUALIFIER_SCOPE": "a registered qualifier's scope-limiting meaning",
    "CONDITION": "a condition the claim carries, in its approved realization",
    "EXEMPLIFICATION": "an exemplification the claim's own text carries",
    "NUMERIC_CRITERIA": "the claim's registered numeric records with their source-stated units",
}

FORBIDDEN_ROLE_NAMES = ("FREEFORM", "OTHER", "GENERIC", "CUSTOM", "FALLBACK", "DEFAULT")

# Names a plan must never carry. This is a tripwire, not the defence: the defence is that every
# key must be *known*, which catches smuggling under an innocent name too.
PROSE_FIELD_NAMES = (
    "free_text", "text", "prose", "sentence", "phrase", "wording", "draft", "content",
    "body", "narrative", "string", "语", "cumle", "cümle", "metin", "paragraph_text",
)

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/#-]{0,63}$")

# The schema. Keys are exact; anything else is a rejection.
SLOT_LEAF_TYPES: dict[str, str] = {
    "slot_id": "id",
    "claim_id": "id",
    "realization_role": "role",
    "condition_ids": "id_list",
    "qualifier_constraint_ids": "id_list",
    "relation_constraint_ids": "id_list",
    "numeric_fact_ids": "id_list",
    "citation_source_keys": "id_list",
}
SLOT_REQUIRED = ("slot_id", "claim_id", "realization_role")
PARAGRAPH_KEYS = {"paragraph_id": "id", "slots": "slot_list"}
SUBSECTION_KEYS = {"subsection_id": "id", "paragraph_groups": "paragraph_list"}
PLAN_KEYS = {"section_id": "id", "plan_id": "id", "plan_version": "id", "language": "id",
             "subsections": "subsection_list"}

PERMITTED_LANGUAGES = ("tr",)


class PlanRejection(Exception):
    """A plan that does not parse. Raised, never returned, so it cannot be ignored."""

    def __init__(self, code: str, detail: str, path: str = ""):
        self.code = code
        self.detail = detail
        self.path = path
        super().__init__(f"{code} at {path or '<plan>'}: {detail}")

    def as_dict(self) -> dict:
        return {"code": self.code, "detail": self.detail, "path": self.path}


@dataclass(frozen=True)
class PlanSlot:
    slot_id: str
    claim_id: str
    realization_role: str
    condition_ids: tuple[str, ...] = ()
    qualifier_constraint_ids: tuple[str, ...] = ()
    relation_constraint_ids: tuple[str, ...] = ()
    numeric_fact_ids: tuple[str, ...] = ()
    citation_source_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class PlanParagraph:
    paragraph_id: str
    slots: tuple[PlanSlot, ...]


@dataclass(frozen=True)
class PlanSubsection:
    subsection_id: str
    paragraph_groups: tuple[PlanParagraph, ...]


@dataclass(frozen=True)
class SemanticPlanIRV2:
    section_id: str
    plan_id: str
    plan_version: str
    language: str
    subsections: tuple[PlanSubsection, ...]

    def iter_slots(self):
        for subsection in self.subsections:
            for paragraph in subsection.paragraph_groups:
                for slot in paragraph.slots:
                    yield subsection, paragraph, slot


# ================================================================ parsing, fail-closed

def _require_mapping(value: Any, path: str) -> dict:
    if not isinstance(value, dict):
        raise PlanRejection("PLAN_MALFORMED", f"expected an object, got {type(value).__name__}",
                            path)
    return value


def _check_keys(obj: dict, permitted: dict[str, str], path: str) -> None:
    for key in obj:
        if not isinstance(key, str):
            raise PlanRejection("PLAN_MALFORMED", f"non-string key {key!r}", path)
        if key.lower() in PROSE_FIELD_NAMES:
            raise PlanRejection("PLAN_PROSE_FIELD",
                                f"{key!r} is a prose-bearing field name; the plan IR carries "
                                f"symbolic choices only", path)
        if key not in permitted:
            # The real defence. A planner smuggling prose under an unremarkable name is
            # rejected here, not by the name blocklist above.
            raise PlanRejection("PLAN_UNKNOWN_FIELD",
                                f"{key!r} is not declared by the plan IR contract; permitted "
                                f"keys are {sorted(permitted)}", path)


def _parse_id(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise PlanRejection("PLAN_MALFORMED", f"expected an id string, got "
                                              f"{type(value).__name__}", path)
    if not ID_RE.match(value):
        # An id cannot hold a sentence: no whitespace, bounded length. This is what closes the
        # last route for prose into the IR.
        raise PlanRejection("PLAN_PROSE_FIELD",
                            f"{value!r} is not a well-formed identifier; ids carry no whitespace "
                            f"and are at most 64 characters, so they cannot carry prose", path)
    return value


def _parse_id_list(value: Any, path: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PlanRejection("PLAN_MALFORMED", f"expected a list, got {type(value).__name__}",
                            path)
    return tuple(_parse_id(item, f"{path}[{i}]") for i, item in enumerate(value))


def _parse_role(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise PlanRejection("PLAN_MALFORMED", "realization_role must be a string", path)
    if value in FORBIDDEN_ROLE_NAMES:
        raise PlanRejection("PLAN_FORBIDDEN_ROLE",
                            f"{value!r} is an open-ended role; the role set is closed", path)
    if value not in REALIZATION_ROLES:
        raise PlanRejection("PLAN_UNKNOWN_ROLE",
                            f"{value!r} is not an enumerated realization role; permitted roles "
                            f"are {sorted(REALIZATION_ROLES)}", path)
    return value


def _parse_slot(raw: Any, path: str) -> PlanSlot:
    obj = _require_mapping(raw, path)
    _check_keys(obj, SLOT_LEAF_TYPES, path)
    for required in SLOT_REQUIRED:
        if required not in obj:
            raise PlanRejection("PLAN_MISSING_FIELD", f"{required!r} is required", path)
    parsed: dict[str, Any] = {}
    for key, kind in SLOT_LEAF_TYPES.items():
        if key not in obj:
            parsed[key] = () if kind == "id_list" else None
            continue
        if kind == "id":
            parsed[key] = _parse_id(obj[key], f"{path}.{key}")
        elif kind == "id_list":
            parsed[key] = _parse_id_list(obj[key], f"{path}.{key}")
        elif kind == "role":
            parsed[key] = _parse_role(obj[key], f"{path}.{key}")
    return PlanSlot(**parsed)


def _parse_paragraph(raw: Any, path: str) -> PlanParagraph:
    obj = _require_mapping(raw, path)
    _check_keys(obj, PARAGRAPH_KEYS, path)
    for required in PARAGRAPH_KEYS:
        if required not in obj:
            raise PlanRejection("PLAN_MISSING_FIELD", f"{required!r} is required", path)
    slots = obj["slots"]
    if not isinstance(slots, list) or not slots:
        raise PlanRejection("PLAN_MALFORMED", "a paragraph group needs a non-empty slot list",
                            path)
    return PlanParagraph(
        paragraph_id=_parse_id(obj["paragraph_id"], f"{path}.paragraph_id"),
        slots=tuple(_parse_slot(s, f"{path}.slots[{i}]") for i, s in enumerate(slots)))


def _parse_subsection(raw: Any, path: str) -> PlanSubsection:
    obj = _require_mapping(raw, path)
    _check_keys(obj, SUBSECTION_KEYS, path)
    for required in SUBSECTION_KEYS:
        if required not in obj:
            raise PlanRejection("PLAN_MISSING_FIELD", f"{required!r} is required", path)
    groups = obj["paragraph_groups"]
    if not isinstance(groups, list) or not groups:
        raise PlanRejection("PLAN_MALFORMED", "a subsection needs a non-empty paragraph list",
                            path)
    return PlanSubsection(
        subsection_id=_parse_id(obj["subsection_id"], f"{path}.subsection_id"),
        paragraph_groups=tuple(_parse_paragraph(p, f"{path}.paragraph_groups[{i}]")
                               for i, p in enumerate(groups)))


def parse_plan(raw: Any) -> SemanticPlanIRV2:
    """Parse a plan, or raise. There is no partial success and no repair."""
    obj = _require_mapping(raw, "<plan>")
    _check_keys(obj, PLAN_KEYS, "<plan>")
    for required in PLAN_KEYS:
        if required not in obj:
            raise PlanRejection("PLAN_MISSING_FIELD", f"{required!r} is required", "<plan>")
    language = _parse_id(obj["language"], "<plan>.language")
    if language not in PERMITTED_LANGUAGES:
        raise PlanRejection("PLAN_LANGUAGE_NOT_PERMITTED",
                            f"{language!r} is not a permitted section language", "<plan>.language")
    section_id = _parse_id(obj["section_id"], "<plan>.section_id")
    if section_id != SECTION_ID:
        raise PlanRejection("PLAN_SECTION_MISMATCH",
                            f"this contract governs {SECTION_ID}, not {section_id}",
                            "<plan>.section_id")
    subsections = obj["subsections"]
    if not isinstance(subsections, list) or not subsections:
        raise PlanRejection("PLAN_MALFORMED", "a plan needs a non-empty subsection list",
                            "<plan>.subsections")
    plan = SemanticPlanIRV2(
        section_id=section_id,
        plan_id=_parse_id(obj["plan_id"], "<plan>.plan_id"),
        plan_version=_parse_id(obj["plan_version"], "<plan>.plan_version"),
        language=language,
        subsections=tuple(_parse_subsection(s, f"<plan>.subsections[{i}]")
                          for i, s in enumerate(subsections)))
    seen: set[str] = set()
    for _, _, slot in plan.iter_slots():
        if slot.slot_id in seen:
            raise PlanRejection("PLAN_DUPLICATE_SLOT_ID", f"{slot.slot_id!r} appears twice",
                                "<plan>")
        seen.add(slot.slot_id)
    return plan


# ================================================================ semantic validation

@dataclass
class PlanValidation:
    plan_id: str
    failures: list[dict] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.failures

    def fail(self, code: str, detail: str, slot_id: str = "") -> None:
        self.failures.append({"code": code, "detail": detail, "slot_id": slot_id})


def validate_plan(plan: SemanticPlanIRV2, bundle, realization=None) -> PlanValidation:
    """Everything provable about a plan before a word is rendered.

    `bundle` is the frozen validator's DraftingBundle — the same allowlist, denylist and claim
    records the draft validator uses, so this stage cannot disagree with it about what a claim
    contains. `realization` is the M2 contract when available; without it the ownership checks
    below still run, and the realizability check is simply not one of them.
    """
    result = PlanValidation(plan_id=plan.plan_id)

    for _, _, slot in plan.iter_slots():
        claim = bundle.allowlist.get(slot.claim_id)

        if slot.claim_id in bundle.denylist:
            denied = bundle.denylist[slot.claim_id]
            result.fail("PLAN_CLAIM_DENYLISTED",
                        f"{slot.claim_id} is on the composition denylist "
                        f"({denied.get('support_status')})", slot.slot_id)
            continue
        if claim is None:
            result.fail("PLAN_CLAIM_NOT_ALLOWLISTED",
                        f"{slot.claim_id} is not on the {SECTION_ID} composition-safe allowlist",
                        slot.slot_id)
            continue
        if not claim.get("composition_safe"):
            result.fail("PLAN_CLAIM_NOT_COMPOSITION_SAFE",
                        f"{slot.claim_id} is allowlisted for evidence but not composition-safe",
                        slot.slot_id)
            continue
        if claim.get("section_id") != SECTION_ID:
            result.fail("PLAN_CLAIM_SECTION_MISMATCH",
                        f"{slot.claim_id} belongs to {claim.get('section_id')}", slot.slot_id)

        # Source laundering: a slot may cite only the keys its own claim registers.
        registered_keys = set(claim.get("source_keys") or [])
        for key in slot.citation_source_keys:
            if key not in registered_keys:
                result.fail("PLAN_SOURCE_KEY_NOT_OWNED",
                            f"{key} is not a source key of {slot.claim_id}; "
                            f"registered keys are {sorted(registered_keys)}", slot.slot_id)

        # Numerics are addressed by index into the claim's own frozen records.
        numerics = claim.get("numeric") or []
        for numeric_id in slot.numeric_fact_ids:
            index = _fact_index(numeric_id, slot.claim_id, "NUM")
            if index is None or not 0 <= index < len(numerics):
                result.fail("PLAN_NUMERIC_NOT_REGISTERED",
                            f"{numeric_id} does not address a registered numeric of "
                            f"{slot.claim_id} ({len(numerics)} registered)", slot.slot_id)
                continue
            if not numerics[index].get("source_stated"):
                result.fail("PLAN_NUMERIC_NOT_SOURCE_STATED",
                            f"{numeric_id} addresses a numeric {slot.claim_id} does not state "
                            f"as source-stated", slot.slot_id)

        conditions = claim.get("conditions") or []
        for condition_id in slot.condition_ids:
            index = _fact_index(condition_id, slot.claim_id, "COND")
            if index is None or not 0 <= index < len(conditions):
                result.fail("PLAN_CONDITION_NOT_OWNED",
                            f"{condition_id} does not address a condition of {slot.claim_id} "
                            f"({len(conditions)} registered)", slot.slot_id)

        qualifiers = claim.get("qualifiers") or []
        for qualifier_id in slot.qualifier_constraint_ids:
            index = _qualifier_index(qualifier_id, slot.claim_id, bundle)
            if index is None or not 0 <= index < len(qualifiers):
                result.fail("PLAN_QUALIFIER_NOT_OWNED",
                            f"{qualifier_id} does not address a registered qualifier of "
                            f"{slot.claim_id} ({len(qualifiers)} registered)", slot.slot_id)

        # A relation must be one the claim allows and none it forbids. The renderer emits a
        # connective only under one of these, which is what keeps adjacent claims independent.
        allowed = set(claim.get("allowed_relationships") or [])
        forbidden = set(claim.get("forbidden_relationships") or [])
        for relation_id in slot.relation_constraint_ids:
            if relation_id in forbidden:
                result.fail("PLAN_RELATION_FORBIDDEN",
                            f"{slot.claim_id} forbids {relation_id}", slot.slot_id)
            elif relation_id not in allowed:
                result.fail("PLAN_RELATION_NOT_ALLOWED",
                            f"{slot.claim_id} allows {sorted(allowed)}, not {relation_id}",
                            slot.slot_id)
            elif relation_id != "INDEPENDENT":
                result.fail("PLAN_RELATION_NOT_SOURCE_SUPPORTED",
                            f"{relation_id} asserts a relation between claims; only INDEPENDENT "
                            f"is renderable without a source that states the relation",
                            slot.slot_id)

        if realization is not None:
            entry = realization.entry(slot.claim_id, slot.realization_role)
            if entry is None:
                result.fail("PLAN_ROLE_NOT_REALIZABLE",
                            f"{slot.claim_id} has no frozen realization for role "
                            f"{slot.realization_role}", slot.slot_id)
            elif entry.get("status") == "UNREALIZABLE":
                result.fail("PLAN_ROLE_UNREALIZABLE",
                            f"{slot.claim_id} / {slot.realization_role} is UNREALIZABLE: "
                            f"{entry.get('reason')}", slot.slot_id)

    _validate_paragraph_scope(plan, bundle, result)
    return result


def _validate_paragraph_scope(plan: SemanticPlanIRV2, bundle, result: PlanValidation) -> None:
    """Paragraph-scoped meanings must be allocated a slot in the same paragraph.

    Two frozen stages score at paragraph scope: DSC-C002-001's required acceptance-criteria
    meaning and DQS-C009-001's scope limitation. A claim carrying one of those cannot be stated
    in a paragraph that does not also realise it — under architecture A that was a writer's
    omission, and it is the failure that rejected attempts #1 and #2. Here it is a plan defect,
    provable before a word is rendered, which is the whole point of moving the decision.
    """
    required = paragraph_scoped_claims(bundle)
    for subsection in plan.subsections:
        for paragraph in subsection.paragraph_groups:
            present = {s.claim_id for s in paragraph.slots}
            roles: dict[str, set[str]] = {}
            for slot in paragraph.slots:
                roles.setdefault(slot.claim_id, set()).add(slot.realization_role)
            for claim_id in sorted(present):
                first = next(s.slot_id for s in paragraph.slots if s.claim_id == claim_id)
                claim = bundle.allowlist.get(claim_id) or {}
                held = roles[claim_id]

                # A supporting role qualifies, scopes or quantifies a statement. Standing alone
                # it states a fragment whose conditions never reach the paragraph, which is what
                # stage E scores as CONDITION_DROPPED. There must be a statement to support.
                # Both statement roles realise the same proposition from the same frozen
                # canonical wording, so allocating both emits the sentence twice. REQUIREMENT is
                # the narrower of the two — it is admitted only where the claim's own modality is
                # binding — so holding both is a plan defect, not a stylistic one.
                if len(held & {"CLAIM_STATEMENT", "REQUIREMENT"}) > 1:
                    result.fail("PLAN_DUPLICATE_STATEMENT_ROLE",
                                f"{claim_id} holds both CLAIM_STATEMENT and REQUIREMENT in one "
                                f"paragraph; they realise the same proposition", first)

                if not held & {"CLAIM_STATEMENT", "REQUIREMENT"}:
                    result.fail("PLAN_SUPPORTING_ROLE_WITHOUT_STATEMENT",
                                f"{claim_id} appears only in supporting roles "
                                f"{sorted(held)}; a paragraph stating a claim must allocate a "
                                f"CLAIM_STATEMENT or REQUIREMENT slot for it", first)

                # A registered qualifier is mandatory wherever its claim is stated. Under
                # architecture A this was the writer's to remember, and it is what rejected
                # attempts #1 and #2. Here it is provable before a word is rendered.
                # A condition the claim's own sentence cannot carry — SEC-02-2-P0-001's
                # "özel uygulamalar dışında" lives in a neighbouring clause — is scored across
                # the paragraph, so the paragraph must allocate a slot that states it.
                if paragraph_scoped_conditions(claim, bundle) and "CONDITION" not in held:
                    result.fail("PLAN_PARAGRAPH_CONDITION_MISSING",
                                f"{claim_id} carries a condition its own sentence does not state "
                                f"({paragraph_scoped_conditions(claim, bundle)}); the paragraph "
                                f"must also allocate a CONDITION slot for it", first)

                if (claim.get("qualifiers") or []) and "QUALIFIER_SCOPE" not in held:
                    detail = (f" ({required[claim_id]} is scored at paragraph scope)"
                              if claim_id in required else "")
                    result.fail("PLAN_PARAGRAPH_QUALIFIER_MISSING",
                                f"{claim_id} registers a qualifier{detail}; the paragraph must "
                                f"also allocate a QUALIFIER_SCOPE slot for it", first)


def unit_scoped_conditions(claim: dict, bundle) -> list[str]:
    """Conditions stage E scores inside every unit that declares this claim.

    A condition whose anchors all appear in the claim's own canonical wording is checked at unit
    scope; one carried by neighbouring source context is checked across the paragraph. This
    mirrors stage E's own test rather than approximating it, and it lives here — in the contract
    layer — so the plan rules and the realization contract cannot come to disagree about which
    conditions are sentence-internal.
    """
    v1 = _validator_module("draft_validator_v1_plan", "49_section_draft_validator_v1.py")
    canonical_tokens = set(v1.tokens(claim.get("canonical_claim") or ""))
    scoped = []
    for condition in claim.get("conditions") or []:
        anchors = v1.content_tokens(condition, bundle.function_lexicon)
        if not anchors:
            continue
        if all(any(v1.prefix_agreement(a, c) for c in canonical_tokens) for a in anchors):
            scoped.append(condition)
    return scoped


def paragraph_scoped_conditions(claim: dict, bundle) -> list[str]:
    """Conditions the claim's own sentence cannot carry, so the paragraph must."""
    scoped = set(unit_scoped_conditions(claim, bundle))
    v1 = _validator_module("draft_validator_v1_plan", "49_section_draft_validator_v1.py")
    return [c for c in (claim.get("conditions") or [])
            if c not in scoped and v1.content_tokens(c, bundle.function_lexicon)]


def paragraph_scoped_claims(bundle=None) -> dict[str, str]:
    """Claims whose registered meaning is scored across the paragraph.

    Read from the frozen validators' own loaders rather than from the bundle, which does not
    carry them. Reading them from anywhere else would let this stage and stage K/L disagree
    about which claims are governed, which is the one thing it must not do.
    """
    v1_1 = _validator_module("draft_validator_v1_1_plan", "52_section_draft_validator_v1_1.py")
    v1_2 = _validator_module("draft_validator_v1_2_plan", "54_section_draft_validator_v1_2.py")
    required: dict[str, str] = {}
    for constraint in v1_1.load_semantic_constraints():
        markers = constraint.get("required_meaning_markers") or {}
        if markers.get("scope") == "paragraph":
            required[constraint["claim_id"]] = constraint["constraint_id"]
    for entry in v1_2.load_qualifier_semantics():
        if entry.get("required_meaning_scope") == "paragraph":
            required[entry["claim_id"]] = entry["constraint_id"]
    return required


_VALIDATOR_MODULES: dict[str, Any] = {}


def _validator_module(name: str, filename: str):
    if name not in _VALIDATOR_MODULES:
        import importlib.util
        path = ROOT / "scripts" / filename
        spec = importlib.util.spec_from_file_location(name, path)
        loaded = importlib.util.module_from_spec(spec)
        sys.modules[name] = loaded
        spec.loader.exec_module(loaded)
        _VALIDATOR_MODULES[name] = loaded
    return _VALIDATOR_MODULES[name]


def _fact_index(fact_id: str, claim_id: str, marker: str) -> int | None:
    """`SEC-02-2-C-002#NUM0` addresses the claim's own record, so an id cannot cross claims."""
    prefix = f"{claim_id}#{marker}"
    if not fact_id.startswith(prefix):
        return None
    tail = fact_id[len(prefix):]
    return int(tail) if tail.isdigit() else None


def _qualifier_index(qualifier_id: str, claim_id: str, bundle) -> int | None:
    """A qualifier is addressed by its registered constraint id, or by claim-local index."""
    index = _fact_index(qualifier_id, claim_id, "QUAL")
    if index is not None:
        return index
    for entry in getattr(bundle, "qualifier_semantics", []):
        if entry.get("constraint_id") == qualifier_id and entry.get("claim_id") == claim_id:
            return int(entry.get("qualifier_index", 0))
    return None


# ================================================================ contract artifact

def build_contract() -> dict:
    return {
        "version": CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "purpose": ("the symbolic structure a planner emits. It carries which claims are stated, "
                    "in what order and in what role, and no words."),
        "core_principle": ("The planner never emits a surface word. Every leaf of this structure "
                           "is an identifier or an enumerated role."),
        "realization_roles": REALIZATION_ROLES,
        "forbidden_role_names": list(FORBIDDEN_ROLE_NAMES),
        "unknown_role_policy": "reject; there is no default and no degradation",
        "prose_exclusion": {
            "mechanisms": [
                ("closed schema — every object declares its permitted keys and an undeclared key "
                 "is a rejection, so prose cannot enter under an innocent name"),
                ("prose-name blocklist — a tripwire for the obvious case, listed as "
                 "PROSE_FIELD_NAMES"),
                ("typed leaves — every surviving leaf is an id matching ID_RE, which admits no "
                 "whitespace and at most 64 characters, so a sentence cannot be spelled as one"),
            ],
            "forbidden_field_names": list(PROSE_FIELD_NAMES),
            "id_pattern": ID_RE.pattern,
        },
        "schema": {
            "plan": PLAN_KEYS,
            "subsection": SUBSECTION_KEYS,
            "paragraph_group": PARAGRAPH_KEYS,
            "slot": SLOT_LEAF_TYPES,
            "slot_required": list(SLOT_REQUIRED),
        },
        "permitted_languages": list(PERMITTED_LANGUAGES),
        "fact_addressing": {
            "numeric": "<claim_id>#NUM<index> into the claim's own frozen numeric records",
            "condition": "<claim_id>#COND<index> into the claim's own frozen conditions",
            "qualifier": ("<claim_id>#QUAL<index>, or a registered qualifier-semantics "
                          "constraint id whose declared claim matches"),
            "rationale": ("an id that embeds its own claim cannot address another claim's fact, "
                          "which is what closes cross-claim source laundering at parse time"),
        },
        "validation_proves_before_rendering": [
            "the claim is allowlisted and composition-safe",
            "the claim is not denylisted",
            "every cited source key is registered to the declaring claim",
            "every requested numeric is registered to the claim and source-stated",
            "every requested condition belongs to the claim",
            "every requested qualifier constraint belongs to the claim",
            "the relation is allowed by the claim and forbidden by none",
            "only INDEPENDENT is renderable without a source that states the relation",
            "the claim/role pair has a frozen realization and is not UNREALIZABLE",
            "a paragraph-scoped required meaning has a slot in its own paragraph",
            "a registered qualifier has a slot wherever its claim is stated",
            "a supporting role never stands without the statement it supports",
            "a claim holds at most one statement role per paragraph",
            "a paragraph-scoped condition has a slot in its own paragraph",
        ],
        "rejection_codes": [
            "PLAN_MALFORMED", "PLAN_MISSING_FIELD", "PLAN_UNKNOWN_FIELD", "PLAN_PROSE_FIELD",
            "PLAN_UNKNOWN_ROLE", "PLAN_FORBIDDEN_ROLE", "PLAN_DUPLICATE_SLOT_ID",
            "PLAN_LANGUAGE_NOT_PERMITTED", "PLAN_SECTION_MISMATCH", "PLAN_CLAIM_DENYLISTED",
            "PLAN_CLAIM_NOT_ALLOWLISTED", "PLAN_CLAIM_NOT_COMPOSITION_SAFE",
            "PLAN_CLAIM_SECTION_MISMATCH", "PLAN_SOURCE_KEY_NOT_OWNED",
            "PLAN_NUMERIC_NOT_REGISTERED", "PLAN_NUMERIC_NOT_SOURCE_STATED",
            "PLAN_CONDITION_NOT_OWNED", "PLAN_QUALIFIER_NOT_OWNED", "PLAN_RELATION_FORBIDDEN",
            "PLAN_RELATION_NOT_ALLOWED", "PLAN_RELATION_NOT_SOURCE_SUPPORTED",
            "PLAN_ROLE_NOT_REALIZABLE", "PLAN_ROLE_UNREALIZABLE",
            "PLAN_PARAGRAPH_QUALIFIER_MISSING", "PLAN_SUPPORTING_ROLE_WITHOUT_STATEMENT",
            "PLAN_PARAGRAPH_CONDITION_MISSING", "PLAN_DUPLICATE_STATEMENT_ROLE",
        ],
    }


def main() -> int:
    contract = build_contract()
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"plan IR contract written: {CONTRACT_PATH.relative_to(ROOT)}")
    print(f"roles: {len(REALIZATION_ROLES)}  rejection codes: "
          f"{len(contract['rejection_codes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
