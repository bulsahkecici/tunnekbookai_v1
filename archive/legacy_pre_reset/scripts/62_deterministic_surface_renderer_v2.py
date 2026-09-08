"""M4 — Deterministic Surface Renderer v2. A validated plan and a frozen contract become prose.

The renderer is a pure function of two frozen inputs and holds no judgement of its own. It reads
a validated SemanticPlanIRV2 and the Claim Realization Contract v2, concatenates the segments the
contract froze for each claim and role, applies deterministic morphology where the contract asks
for it, and emits DraftIR-compatible units the unchanged Draft Validator v1.2 can check. There is
no model call, no retrieval, no network, no clock, no randomness, no seed and no temperature.
Same input bytes, same output bytes.

**The renderer chooses no words.** Every lexical element it emits comes from a contract entry,
and `_ownership_guard` proves it rather than trusting it: after assembling a unit, every content
token of the result is checked against the same licensed pool the frozen validator computes for
the declaring claim, plus the frozen function lexicon. A token outside both raises
`RenderRefusal`. This is the construction invariant made executable — the renderer cannot emit an
unlicensed word even if a contract entry were wrong, because the guard runs on the finished
string, after morphology, after joining, on exactly what the validator will see.

**The renderer asserts no relationships.** Slots are rendered independently and joined by nothing
but a space. There is no code path that emits `bu nedenle`, `dolayısıyla`, `böylece`, `ancak` or
any other connective between two slots: adjacency in a paragraph carries no claim about how two
propositions relate, and inventing one is exactly the synthesis the composition contract forbids.
A relation reaches prose only when a frozen relation constraint puts it there, and for SEC-02-2
every allowlisted claim permits INDEPENDENT and nothing else.

**One slot, one unit.** Each slot becomes its own unit with its own claim id, source keys and
citation intent. Merging two claims into one sentence would create a unit whose licensed pool is
the union of two claims' pools, which is how a sentence quietly acquires vocabulary it did not
earn. Keeping the mapping one-to-one keeps every unit's pool exactly the claim it declares.

Citation follows the existing contract: stable `source_keys` only, drawn from the declaring
claim's own registered set, and packet-local `[E###]` handles never appear because the renderer
has no access to a retrieval packet and no code that could write one.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RENDERER_VERSION = "tunnelbook-deterministic-surface-renderer-v2"
DRAFT_IR_VERSION = "tunnelbook-rendered-draft-ir-v2"
SECTION_ID = "SEC-02-2"

VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
PLAN_IR = ROOT / "scripts" / "59_semantic_plan_ir_contract_v2.py"
REALIZATION = ROOT / "scripts" / "60_claim_realization_contract_v2.py"
MORPHOLOGY = ROOT / "scripts" / "61_turkish_morphology_v2.py"


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


class RenderRefusal(Exception):
    """The renderer refuses rather than emitting something it cannot prove is licensed."""

    def __init__(self, code: str, detail: str, slot_id: str = ""):
        self.code = code
        self.detail = detail
        self.slot_id = slot_id
        super().__init__(f"{code} at {slot_id or '<plan>'}: {detail}")

    def as_dict(self) -> dict:
        return {"code": self.code, "detail": self.detail, "slot_id": self.slot_id}


# Subsection ids map to the unit-id grammar the frozen validator enforces. Deterministic and
# order-independent: the label comes from the id, never from a counter that could drift.
def _subsection_label(subsection_id: str) -> str:
    tail = subsection_id.rsplit("-", 1)[-1]
    label = "".join(ch for ch in tail if ch.isalnum())
    if not label:
        raise RenderRefusal("RENDER_BAD_SUBSECTION_ID",
                            f"{subsection_id!r} yields no unit-id label")
    return label.upper()


@dataclass(frozen=True)
class RenderedUnit:
    unit_id: str
    unit_type: str
    text: str
    material: bool
    claim_ids: tuple[str, ...]
    source_keys: tuple[str, ...]
    relationship_type: str
    citation_intents: tuple[dict, ...]
    slot_id: str
    realization_role: str

    def as_dict(self) -> dict:
        return {
            "unit_id": self.unit_id,
            "unit_type": self.unit_type,
            "text": self.text,
            "material": self.material,
            "claim_ids": list(self.claim_ids),
            "source_keys": list(self.source_keys),
            "relationship_type": self.relationship_type,
            "citation_intents": [dict(i) for i in self.citation_intents],
        }


# ================================================================ segment realization

def _segment_surface(segment: dict, slot_id: str) -> str:
    """One segment to its surface string. Every branch reads frozen data; none chooses a word."""
    kind = segment["kind"]
    if kind == "FROZEN_TEXT":
        return segment["value"]
    if kind in ("GLOSS", "SCAFFOLD"):
        return segment["token"]
    if kind == "LICENSED_NUMERIC":
        morph = module("morphology", MORPHOLOGY)
        rendered = f"{segment['value']} {segment['unit']}"
        if segment.get("copula"):
            # The only place morphology runs. The unit symbol carries no vowel, so harmony is
            # read off the frozen pronunciation table rather than inferred from the string.
            return morph.copula(rendered)
        return rendered
    raise RenderRefusal("RENDER_UNKNOWN_SEGMENT_KIND",
                        f"{kind!r} is not a segment kind this renderer implements", slot_id)


def _capitalise(text: str) -> str:
    """Turkish sentence case. 'i' uppercases to 'İ', which str.capitalize gets wrong."""
    if not text:
        return text
    first = text[0]
    upper = "İ" if first == "i" else ("I" if first == "ı" else first.upper())
    return upper + text[1:]


def render_slot(slot, realization, bundle, claims) -> tuple[str, dict]:
    """The text for one slot, plus the contract entry it came from. Refuses on anything else."""
    entry = realization.entry(slot.claim_id, slot.realization_role)
    if entry is None:
        raise RenderRefusal("RENDER_NO_REALIZATION",
                            f"no contract entry for {slot.claim_id} / {slot.realization_role}",
                            slot.slot_id)
    if entry["status"] != "REALIZABLE":
        raise RenderRefusal("RENDER_UNREALIZABLE",
                            f"{slot.claim_id} / {slot.realization_role} is UNREALIZABLE: "
                            f"{entry.get('reason')}", slot.slot_id)

    realization_module = module("realization", REALIZATION)
    parts = [_segment_surface(segment, slot.slot_id) for segment in entry["segments"]]
    text = realization_module.join_parts(parts)
    return _capitalise(text), entry


def _ownership_guard(text: str, claim_id: str, slot_id: str, bundle) -> None:
    """Every content token of the finished string must be owned by a contract. No exceptions.

    This runs on the assembled, morphologically inflected, joined string — exactly what the
    validator will tokenize — so it cannot be satisfied by a segment that was licensed before
    joining and is not after. It is the executable form of the construction invariant.
    """
    v1 = module("v1", VALIDATOR_V1)
    pool = v1.licensed_tokens([claim_id], bundle)
    stray = v1.unlicensed(text, pool, bundle)
    if stray:
        raise RenderRefusal(
            "RENDER_UNLICENSED_TOKEN",
            f"content words {stray} are owned by no contract for {claim_id}; the renderer emits "
            f"only frozen claim material, frozen scaffold and deterministic morphology", slot_id)


# ================================================================ the renderer

def render_plan(plan, realization, bundle) -> dict:
    """A validated plan to a RenderedDraftIRV2. Pure: no I/O, no clock, no randomness."""
    claims = bundle.allowlist
    units: list[RenderedUnit] = []

    for subsection in plan.subsections:
        label = _subsection_label(subsection.subsection_id)
        for paragraph_index, paragraph in enumerate(subsection.paragraph_groups, start=1):
            for slot_index, slot in enumerate(paragraph.slots, start=1):
                text, entry = render_slot(slot, realization, bundle, claims)
                _ownership_guard(text, slot.claim_id, slot.slot_id, bundle)

                registered = list(claims[slot.claim_id].get("source_keys") or [])
                source_keys = (list(slot.citation_source_keys)
                               if slot.citation_source_keys else registered)
                for key in source_keys:
                    if key not in registered:
                        raise RenderRefusal("RENDER_SOURCE_KEY_NOT_OWNED",
                                            f"{key} is not registered to {slot.claim_id}",
                                            slot.slot_id)

                units.append(RenderedUnit(
                    unit_id=f"U-{label}-P{paragraph_index:02d}-S{slot_index:02d}",
                    unit_type="PARAGRAPH_SENTENCE",
                    text=text,
                    material=True,
                    claim_ids=(slot.claim_id,),
                    source_keys=tuple(source_keys),
                    # Adjacency asserts nothing. There is no branch that produces any other
                    # value, because the renderer never establishes a relation.
                    relationship_type="INDEPENDENT",
                    citation_intents=({"claim_id": slot.claim_id,
                                       "source_keys": list(source_keys)},),
                    slot_id=slot.slot_id,
                    realization_role=slot.realization_role))

    payload = {
        "section_id": plan.section_id,
        "draft_id": plan.plan_id,
        "draft_version": DRAFT_IR_VERSION,
        "language": plan.language,
        "title": SECTION_ID,
        "units": [unit.as_dict() for unit in units],
    }
    return payload


def render_bytes(payload: dict) -> bytes:
    """The canonical serialisation. Byte equality of this is what determinism is measured on."""
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8")


def render_sha256(payload: dict) -> str:
    return hashlib.sha256(render_bytes(payload)).hexdigest()


def render_from_raw(raw_plan: Any, realization=None, bundle=None) -> dict:
    """Parse, validate, render. The three gates in the only order they may run.

    Rendering never happens on an unvalidated plan: `validate_plan` failing raises here rather
    than returning a partial draft, so there is no code path from an invalid plan to prose.
    """
    v1 = module("v1", VALIDATOR_V1)
    plan_ir = module("plan_ir", PLAN_IR)
    realization_module = module("realization", REALIZATION)
    bundle = bundle or v1.load_bundle()
    realization = realization or realization_module.RealizationContract.load()

    plan = plan_ir.parse_plan(raw_plan)
    validation = plan_ir.validate_plan(plan, bundle, realization)
    if not validation.valid:
        raise RenderRefusal("RENDER_PLAN_INVALID",
                            f"plan validation failed: {validation.failures}", plan.plan_id)
    return render_plan(plan, realization, bundle)


def main() -> int:
    print(f"{RENDERER_VERSION}: a module, not a pipeline stage.")
    print("It renders only a validated SemanticPlanIRV2 supplied by a caller.")
    print("No plan is generated here and no pilot is rendered here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
