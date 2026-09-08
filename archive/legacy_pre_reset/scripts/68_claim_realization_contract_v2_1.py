"""M2 v2.1 — Claim Realization Contract v2.1. Additive: v2 is not edited and not overwritten.

v2 decided whether a frozen claim field could be emitted into Turkish prose by asking whether the
string contained one of `çğıöşü`. That is not a language test. `ilk tabaka`, `takip eden
tabakalar` and `ilave tabakalar` are Turkish and contain none of those letters, so their CONDITION
roles were marked UNREALIZABLE — three false negatives out of four, and the fourth, SEC-02-2-R025's
`normally`, was refused for the right reason by accident. One of those false negatives is what
broke ARCHITECTURE V2 PILOT #1: the planner was told SEC-02-2-C-005 needed a CONDITION slot beside
an option list that could not offer one.

The replacement is not another character rule. It reads language from frozen data:

**A frozen claim field carries the language of the claim it belongs to.** A claim's conditions and
qualifiers are excerpts of the same source sentence as its canonical claim, so they cannot be in a
different language from it. The claim's language is already recorded in the frozen drafting
contract, because a claim whose source is English is exactly a claim for which
`translation_glosses` and `condition_glosses` were authored. Presence of a frozen translation
mapping *is* the language metadata; nothing new is declared here.

That mapping is not taken on trust. At build time every claim's canonical sentence is put to the
frozen Draft Language Validator — stage J of Draft Validator v1.1, which already governs every
rendered unit — and its verdict must agree with the metadata for all 27 claims. A disagreement
fails the build. So the classification is metadata-driven and detector-corroborated, and neither
half can drift without the build stopping. No model is asked, no external detector is used, and no
new lexicon or gloss is introduced.

A string the frozen fields do not contain is UNATTESTED and refused. The rule fails closed in the
direction that withholds material, which is the same direction v2 failed in — but now it withholds
only what is genuinely unaccounted for.

**What this widens, precisely.** Three pairs, all of them CONDITION roles on Turkish claims whose
own frozen condition strings happen to lack diacritics. Nothing else moves. R025's `normally` stays
UNREALIZABLE because R025 is an English-source claim and no gloss frame exists for its qualifier.
Every newly REALIZABLE entry still passes the same guards v2 applied and did not reach: the numeric
licence check, the gloss-pool check, the deterministic-surface check and — the one that matters —
the containment guard against the pool the frozen Draft Validator computes for that claim. A pair
is realizable when it is deterministically constructible *and* valid, never when it merely looks
like Turkish.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONTRACT_VERSION = "tunnelbook-claim-realization-contract-v2-1"
LANGUAGE_RULE_VERSION = "tunnelbook-claim-source-language-rule-v2-1"
SECTION_ID = "SEC-02-2"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
CONTRACT_PATH = ARCH_V2 / "contracts" / "claim_realization_contract_v2_1.json"
V2_CONTRACT_PATH = ARCH_V2 / "contracts" / "claim_realization_contract_v2.json"

M2_V2 = ROOT / "scripts" / "60_claim_realization_contract_v2.py"
VALIDATOR_V1 = ROOT / "scripts" / "49_section_draft_validator_v1.py"
LANGUAGE_VALIDATOR = ROOT / "scripts" / "51_draft_language_validator_v1.py"

# The frozen field families a claim's surface material is drawn from. Each is an excerpt of the
# same source sentence, so each carries the claim's language.
LANGUAGE_BEARING_FIELDS = ("canonical_claim", "conditions", "qualifiers")


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


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ================================================================ the language rule


class LanguageRuleViolation(Exception):
    """The frozen language metadata and the frozen language detector disagree. Terminal."""


class SourceLanguageIndex:
    """Which frozen claim fields may be emitted as Turkish prose, decided from frozen data.

    Two independent frozen sources have to agree before anything is classified:

    1. **Metadata.** `translation_glosses[claim_id]` exists exactly for the claims whose source
       sentence is English — that is why the glosses were authored. It is read as the declaration
       it already is.
    2. **Corroboration.** The frozen Draft Language Validator's verdict on the same canonical
       sentence. It already decides this question for every rendered unit at stage J; asking it
       here means the realization contract and the draft validator cannot come to disagree about
       what Turkish is.

    A string is admissible Turkish material only if it is one of the frozen fields of a
    Turkish-source claim. Anything else — an English field, a paraphrase, an invented string —
    is refused.
    """

    def __init__(self, bundle):
        self.bundle = bundle
        v1 = module("v1", VALIDATOR_V1)
        self.claims = {cid: row for cid, row in bundle.allowlist.items()
                       if row.get("section_id") == SECTION_ID}
        self.translation_glosses = bundle.translation_glosses
        self.condition_glosses = bundle.contract.get("condition_glosses", {})

        self.claim_languages: dict[str, str] = {
            cid: ("ENGLISH" if self._has_translation_mapping(cid) else "TURKISH")
            for cid in sorted(self.claims)
        }

        self._field_language: dict[str, str] = {}
        self._field_owner: dict[str, str] = {}
        self.collisions: list[dict] = []
        for cid in sorted(self.claims):
            language = self.claim_languages[cid]
            for text in self._fields(self.claims[cid]):
                key = v1.fold(text)
                previous = self._field_language.get(key)
                if previous is not None and previous != language:
                    # The same string owned by claims of two languages. Nothing decides which is
                    # meant, so the string stops being admissible Turkish material.
                    self.collisions.append({"text": text, "owners": [self._field_owner[key], cid],
                                            "languages": [previous, language],
                                            "resolution": "ENGLISH — fail closed"})
                    self._field_language[key] = "ENGLISH"
                    continue
                self._field_language[key] = language
                self._field_owner.setdefault(key, cid)

        self.corroboration = self._corroborate()

    def _has_translation_mapping(self, claim_id: str) -> bool:
        return bool(self.translation_glosses.get(claim_id)
                    or self.condition_glosses.get(claim_id))

    @staticmethod
    def _fields(claim: dict) -> list[str]:
        out = []
        for name in LANGUAGE_BEARING_FIELDS:
            value = claim.get(name)
            if isinstance(value, str):
                candidates = [value]
            else:
                candidates = list(value or [])
            out.extend(text.strip() for text in candidates if (text or "").strip())
        return out

    def _corroborate(self) -> dict:
        """The frozen stage-J detector must agree with the metadata on every canonical sentence."""
        lang = module("language", LANGUAGE_VALIDATOR)
        contract = lang.load_contract()
        rows, mismatches = [], []
        for cid in sorted(self.claims):
            canonical = (self.claims[cid].get("canonical_claim") or "").strip()
            verdict = lang.detect(canonical, contract).as_dict().get("language")
            declared = self.claim_languages[cid]
            agrees = (verdict == "tr") if declared == "TURKISH" else (verdict != "tr")
            rows.append({"claim_id": cid, "declared_language": declared,
                         "frozen_detector_verdict": verdict, "agrees": agrees})
            if not agrees:
                mismatches.append(cid)
        return {"detector": lang.DETECTOR_VERSION, "claims_checked": len(rows),
                "mismatches": mismatches, "rows": rows}

    def require_corroborated(self) -> None:
        if self.corroboration["mismatches"]:
            raise LanguageRuleViolation(
                "frozen language metadata disagrees with the frozen Draft Language Validator on "
                f"{self.corroboration['mismatches']}; the realization contract will not be built "
                "on a classification the draft validator would contradict")

    def field_language(self, text: str) -> str:
        v1 = module("v1", VALIDATOR_V1)
        return self._field_language.get(v1.fold((text or "").strip()), "UNATTESTED")

    def is_admissible_turkish(self, text: str) -> bool:
        """Drop-in replacement for M2 v2's `is_turkish`. Same signature, frozen-data answer."""
        return self.field_language(text) == "TURKISH"

    def summary(self) -> dict:
        by_language: dict[str, list[str]] = {}
        for cid, language in self.claim_languages.items():
            by_language.setdefault(language, []).append(cid)
        return {
            "rule_version": LANGUAGE_RULE_VERSION,
            "principle": ("A frozen claim field carries the language of its claim. A claim is "
                          "English-source exactly when the frozen drafting contract holds a "
                          "translation or condition gloss mapping for it. Corroborated against "
                          "the frozen Draft Language Validator; a disagreement fails the build."),
            "inputs": ["section_drafting_contract_v1.translation_glosses",
                       "section_drafting_contract_v1.condition_glosses",
                       "composition_safe_allowlist_v1.canonical_claim/conditions/qualifiers",
                       "draft_language_contract_v1 (corroboration only)"],
            "not_used": ["diacritic or character heuristics", "LLM language judgement",
                         "external language detection libraries", "new lexicon or gloss entries"],
            "unattested_policy": "refused — a string outside the frozen fields is not material",
            "claims_by_language": {k: sorted(v) for k, v in sorted(by_language.items())},
            "distinct_fields_indexed": len(self._field_language),
            "cross_language_collisions": self.collisions,
            "corroboration": self.corroboration,
        }


# ================================================================ build


def build_contract_v2_1() -> tuple[dict, dict]:
    """Build v2.1 by running M2 v2's own builder under the corrected language rule.

    The segment construction, the numeric licence check, the gloss-pool check and the containment
    guard are v2's, unmodified and un-duplicated — this phase exists because two derivations of
    one thing is the defect it is closing, so it does not add a third. The only substitution is
    the language predicate, made on the imported module object; `60_claim_realization_contract_v2.py`
    is not written to and its SHA is recorded here to prove it.
    """
    m2 = module("m2_v2", M2_V2)
    v1 = module("v1", VALIDATOR_V1)
    bundle = v1.load_bundle()

    index = SourceLanguageIndex(bundle)
    index.require_corroborated()

    m2_sha_before = sha_file(M2_V2)
    original = m2.is_turkish
    try:
        m2.is_turkish = index.is_admissible_turkish
        payload = m2.build_contract()
    finally:
        m2.is_turkish = original
    if sha_file(M2_V2) != m2_sha_before:
        raise LanguageRuleViolation("M2 v2 source changed during the v2.1 build")

    payload["version"] = CONTRACT_VERSION
    payload["parent_contracts"] = sorted(set(payload["parent_contracts"])
                                         | {"tunnelbook-claim-realization-contract-v2"})
    payload["supersedes"] = "tunnelbook-claim-realization-contract-v2"
    payload["additive_to"] = str(V2_CONTRACT_PATH.relative_to(ROOT))
    payload["language_rule"] = index.summary()
    payload["derivation"] = {
        "builder": "60_claim_realization_contract_v2.build_contract",
        "builder_sha256": m2_sha_before,
        "substitution": "is_turkish -> SourceLanguageIndex.is_admissible_turkish",
        "note": ("v2's construction, guards and containment check are reused unmodified. Only the "
                 "language predicate is replaced, so no second realization derivation exists."),
    }
    return payload, index


def delta_against_v2(payload: dict) -> dict:
    """Old versus new realizable counts, pair by pair. Widening must be visible and small."""
    old = json.loads(V2_CONTRACT_PATH.read_text(encoding="utf-8"))
    old_status = {(e["claim_id"], e["realization_role"]): e["status"] for e in old["entries"]}
    new_status = {(e["claim_id"], e["realization_role"]): e["status"] for e in payload["entries"]}
    newly_realizable, newly_unrealizable = [], []
    for key in sorted(set(old_status) | set(new_status)):
        before, after = old_status.get(key), new_status.get(key)
        if before == after:
            continue
        row = {"claim_id": key[0], "realization_role": key[1], "from": before, "to": after}
        (newly_realizable if after == "REALIZABLE" else newly_unrealizable).append(row)
    return {
        "v2_realizable": old["totals"]["realizable"],
        "v2_unrealizable": old["totals"]["unrealizable"],
        "v2_1_realizable": payload["totals"]["realizable"],
        "v2_1_unrealizable": payload["totals"]["unrealizable"],
        "pairs": payload["totals"]["pairs"],
        "newly_realizable": newly_realizable,
        "newly_unrealizable": newly_unrealizable,
        "net_widening": payload["totals"]["realizable"] - old["totals"]["realizable"],
        "only_widens": not newly_unrealizable,
    }


def load(path: Path = CONTRACT_PATH):
    """The v2.1 contract as a lookup, using M2 v2's own RealizationContract class."""
    m2 = module("m2_v2", M2_V2)
    return m2.RealizationContract(json.loads(path.read_text(encoding="utf-8")))


def write(payload: dict, path: Path = CONTRACT_PATH) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    payload, index = build_contract_v2_1()
    sha = write(payload)
    delta = delta_against_v2(payload)
    print(f"claim realization contract v2.1: {CONTRACT_PATH.relative_to(ROOT)}")
    print(f"sha256 {sha}")
    print(f"language corroboration: {index.corroboration['claims_checked']} claims, "
          f"mismatches {index.corroboration['mismatches']}")
    print(f"realizable {delta['v2_realizable']} -> {delta['v2_1_realizable']} "
          f"(unrealizable {delta['v2_unrealizable']} -> {delta['v2_1_unrealizable']})")
    for row in delta["newly_realizable"]:
        print(f"  + {row['claim_id']} / {row['realization_role']}")
    for row in delta["newly_unrealizable"]:
        print(f"  - {row['claim_id']} / {row['realization_role']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
