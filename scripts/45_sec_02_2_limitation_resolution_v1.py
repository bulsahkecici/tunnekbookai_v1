"""SEC-02-2 Limitation Resolution v1.

The previous phase closed SEC-02-2's evidence gaps and then declined to call the section
READY_FOR_DRAFT. Its reason was narrow and specific: every enumerated readiness condition passed,
but two limitations - CF-P0-001 and SYN-001 - were constraints on *composition* rather than on
claim selection, and nothing in the project could enforce them. The allowlist and denylist bound
which claims a drafter may use. Neither can express "these two claims may not share a sentence".

This phase builds that missing layer, and the reason it needs to exist is worth stating plainly:

    SYN-001 was not an evidence failure. Both of its components were individually well-supported,
    correctly scoped and properly cited. The defect was the word between them. A pipeline that
    validates claims one at a time cannot see it, because at the level of a single claim there is
    nothing wrong.

So the object of validation here is not the claim but the *combination*. Three things get encoded:

  1. **Scope binding.** Every allowlisted claim gets a material scope, a system scope, a document
     scope and a requirement scope, read off the evidence rather than inferred. The 360 kg/m3
     figure is a maximum for general concrete under an exposure-class design table. The 350 and
     400 kg/m3 figures are minimums for dry- and wet-system shotcrete. Those are four different
     axes of difference, and the whole CF-P0-001 problem is that dropping any one of them makes
     the numbers look like they contradict.

  2. **Mandatory qualifiers.** The 360 figure may never be rendered bare. A drafter who writes
     "maksimum çimento miktarı 360 kg/m³'tür" has written something false about shotcrete while
     citing a true statement about general concrete.

  3. **Forbidden combination.** The 360 figure may not share a sentence with 350 or 400 at all -
     not merely may not be joined by "ancak". A prohibition that depends on enumerating
     conjunctions is evaded by choosing a conjunction nobody enumerated; a prohibition on
     juxtaposition is not.

What this phase deliberately does NOT do:

  - It does not rewrite claim wording to make composition easier. Where a wording is itself
    unsafe it is denied, not softened.
  - It does not add technical content. Narrowing may only remove an unsupported relation or an
    over-broad scope.
  - It does not authorise drafting. `drafting_authorized` is false at the end of this phase under
    every outcome, because authorisation belongs to the Section Drafting Contract.
  - It writes no prose. Every fixture in the regression suite is synthetic, and several of them
    are deliberately wrong.

Two traps found by reading the artifacts rather than reasoning about them abstractly, both of
which would have produced a validator that looked correct and was not:

  - The qualifier CF-P0-001 *requires* contains the phrase "püskürtme beton şartnamesi değildir".
    A wrong-scope check that looks for shotcrete markers near the 360 figure would reject the one
    form the contract mandates. Negation handling is therefore load-bearing, not a nicety.

  - SEC-02-2-C-009 states "100-150 mm" for clay-zone layers and that 150 mm *is* source-stated.
    A derived-number guard keyed on the string "150 mm" would reject a true, cited claim. The
    guard is keyed on the single-pass-thickness context instead.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESOLUTION_VERSION = "tunnelbook-sec-02-2-limitation-resolution-v1"
CONTRACT_VERSION = "tunnelbook-sec-02-2-claim-composition-contract-v1"
VALIDATOR_VERSION = "tunnelbook-sec-02-2-claim-composition-validator-v1"
PARENT_VERSION = "tunnelbook-sec-02-2-draft-readiness-closure-v1"
SECTION_ID = "SEC-02-2"
SOURCE_POLICY = "frozen_packet_only"
AUDIT_METHOD = "manual_evidence_read"
DRAFTING_ENABLED = False
DRAFTING_AUTHORIZED = False
GENERATION_CALLS = 0
RETRIEVAL_CALLS = 0

QDRANT_URL = "http://localhost:6333"
QDRANT_EXPECTED_POINTS = 5992

BOOK = ROOT / "data" / "book"
METADATA = ROOT / "data" / "metadata"
MANIFESTS = BOOK / "manifests"
CLOSURE = BOOK / "sec_02_2_readiness_closure"
P0 = BOOK / "p0_resolution"
OUT = BOOK / "sec_02_2_limitation_resolution"
OUT_CONTRACTS = OUT / "contracts"
OUT_CLAIMS = OUT / "claims"
OUT_AUDITS = OUT / "audits"
OUT_BUNDLE = OUT / "bundle"
FIXTURES_PATH = ROOT / "data" / "evaluation" / "sec_02_2_claim_composition_v1.jsonl"
REPORT_PATH = ROOT / "reports" / "sec_02_2_limitation_resolution_v1.md"
MANIFEST_PATH = MANIFESTS / "sec_02_2_limitation_resolution_v1.json"

REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str | None:
    return sha_text(path.read_text(encoding="utf-8")) if path.exists() else None


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                            for r in rows), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ================================================================ 1. scope vocabulary

MATERIAL_SCOPES = ("general_concrete", "shotcrete", "dry_system_shotcrete",
                   "wet_system_shotcrete", "initial_shotcrete_lining", "steel_fibre_shotcrete",
                   "steel_mesh", "flashcrete")
REQUIREMENT_SCOPES = ("maximum", "minimum", "typical_range", "recommended", "mandatory",
                      "design_table", "project_specific", "case_specific")
SYSTEM_SCOPES = ("dry_system", "wet_system", "system_independent", "not_applicable")
SEVERITIES = ("BLOCKING", "WARNING")
RELATIONSHIP_TYPES = ("INDEPENDENT", "SAME_SCOPE_SUPPORT", "QUALIFIED_COMPARISON",
                      "SOURCE_SUPPORTED_RELATION", "FORBIDDEN_SYNTHESIS", "UNKNOWN_RELATION")

# Scope markers. These are the surface forms a draft may use to assert a scope; they are matched
# with negation handling, so a marker inside "... şartnamesi değildir" does not count as an
# assertion. Kept deliberately small and SEC-02-2 specific (rule 49) rather than attempting a
# general vocabulary of Turkish civil-engineering scope language.
SCOPE_MARKERS = {
    # Deliberately narrow. "etki sınıfları" / "exposure class" is NOT here, and its absence is
    # load-bearing: the phrase occurs in Tablo-308-23-b's own title AND in SEC-02-2-P0-005, a
    # shotcrete durability claim ("Dış çevresel etki sınıfları gereksinimlerine göre ... 350
    # kg/m³"). Exposure-class design spans both materials, so it cannot discriminate between
    # them; treating it as a general-concrete marker would make the shotcrete claim's own
    # canonical wording fail as a misattribution.
    "general_concrete": ["genel beton", "Tablo-308-23-b", "308-23-b", "normal beton",
                         "general concrete"],
    "shotcrete": ["püskürtme beton", "püskürtme betonu", "shotcrete", "sprayed concrete",
                  "püskürtme beton şartname", "püskürtme beton spesifikasyon"],
    "dry_system": ["kuru sistem", "kuru sistemde", "kuru karışım", "dry system", "dry-system",
                   "dry-mix", "dry mix"],
    "wet_system": ["yaş sistem", "yaş sistemde", "yaş karışım", "wet system", "wet-system",
                   "wet-mix", "wet mix"],
    "initial_shotcrete_lining": ["initial shotcrete lining", "ilk püskürtme beton kaplama",
                                 "birincil kaplama", "initial lining"],
    "steel_mesh": ["hasır çelik", "çelik hasır", "welded wire fabric", "steel mesh"],
    "flashcrete": ["flashcrete", "sealing shotcrete", "sızdırmazlık püskürtme beton"],
}

# A marker followed by one of these inside the next 60 characters is a denial of that scope, not
# an assertion of it. This is what makes the mandatory CF-P0-001 qualifier expressible.
NEGATION_MARKERS = ["değildir", "değil", "kapsamaz", "kapsamamaktadır", "ilişkin değildir",
                    "geçerli değildir", "söz konusu değildir", "is not", "does not",
                    "not the", "rather than"]

# Connectors that assert a relation between two propositions. Used only for the cross-sentence
# paragraph case: same-sentence juxtaposition of restricted figures is forbidden outright, which
# is what makes the rule robust against a connector nobody listed.
RELATION_CONNECTORS = {
    "relation_asserting": [
        # Turkish concessive / adversative / causal
        "ancak", "buna rağmen", "buna karşın", "bununla birlikte", "oysa", "oysaki", "halbuki",
        "fakat", "lakin", "ne var ki", "olmasına rağmen", "olmakla birlikte", "belirtilse de",
        "olsa da", "rağmen", "karşın", "dolayısıyla", "bu nedenle", "bu sebeple", "böylece",
        "sonuç olarak", "demek ki", "yani", "aksine", "tersine", "buna göre", "istisna olarak",
        "bir istisna", "çelişmektedir", "çelişki", "farklı olarak", "aynı şekilde",
        # English
        "although", "though", "even though", "despite", "in spite of", "however", "whereas",
        "therefore", "thus", "hence", "but", "in contrast", "by contrast", "nevertheless",
        "nonetheless", "conversely", "as an exception", "an exception to", "contradicts",
        "on the other hand", "consequently", "accordingly",
    ],
}


@dataclass
class ClaimScopeV1:
    claim_id: str
    topic: str | None
    material_scope: str
    system_scope: str
    document_scope: str
    requirement_scope: list[str]
    conditions: list[str]
    qualifiers: list[str]
    exceptions: list[str]
    numeric_values: list[dict]
    source_keys: list[str]
    authority_levels: list[str | None]
    scope_evidence: str = ""
    audit_method: str = AUDIT_METHOD


# Scope binding, authored from the evidence the closure phase verified. Each row records WHY the
# scope is what it is, because a scope assigned without a reason is exactly the kind of inference
# rule "do not infer scope if evidence does not establish it" forbids.
SCOPE_BINDING: list[tuple[str, str, str, str, list[str], str]] = [
    # claim_id, material_scope, system_scope, document_scope, requirement_scope, evidence
    ("SEC-02-2-P0-002", "general_concrete", "not_applicable", "Tablo-308-23-b (KGM/KTS 2013)",
     ["maximum", "design_table"],
     "The span is the heading and body of Tablo-308-23-b, 'Etki Sınıflarına Göre "
     "Projelendirmelerde Esas Alınacak Beton Özellikleri'. That table governs general concrete "
     "designed by exposure class. It is in a different chapter from the shotcrete specification "
     "and names no shotcrete system. The P0 phase recorded this scope as a mandatory qualifier."),
    ("SEC-02-2-R001", "dry_system_shotcrete", "dry_system", "püskürtme beton şartnamesi",
     ["minimum"],
     "Source states 'kuru sistemde 350 kg/m³'ten ... az olmayacaktır' inside the shotcrete "
     "specification. System scope is stated, not inferred."),
    ("SEC-02-2-P0-001", "wet_system_shotcrete", "wet_system", "püskürtme beton şartnamesi",
     ["minimum"],
     "Source states 'yaş sistemde ise 400 kg/m³'ten az olmayacaktır' in the same span. System "
     "scope is stated, not inferred."),
    ("SEC-02-2-P0-003", "shotcrete", "system_independent", "püskürtme beton şartnamesi",
     ["minimum"],
     "One span carries both system minimums together with durability as the stated reason. The "
     "claim is system-independent because it enumerates both systems explicitly; that "
     "enumeration is the source's own, which is why 350 and 400 may share a sentence here."),
    ("SEC-02-2-P0-006", "shotcrete", "system_independent", "püskürtme beton şartnamesi",
     ["minimum"],
     "Same span as P0-003, stated as a summary. Both systems named explicitly."),
    ("SEC-02-2-P0-005", "shotcrete", "system_independent", "püskürtme beton şartnamesi",
     ["minimum", "project_specific"],
     "Source conditions the figure on external exposure classes and laboratory / preliminary mix "
     "design work, so the requirement scope is project_specific as well as a minimum. No system "
     "is named, so system scope stays system_independent rather than being guessed."),
    ("SEC-02-2-P0-004", "shotcrete", "system_independent", "püskürtme beton şartnamesi",
     ["case_specific"],
     "A reduction permitted with the Administration's approval for slope cladding and temporary "
     "support. It states no figure of its own; it modifies the others."),
    ("SEC-02-2-P0-007", "initial_shotcrete_lining", "not_applicable",
     "FHWA Technical Manual (DOC000047) §9.3.3", ["typical_range"],
     "Source: 'It has a thickness ranging generally from 4 to 16 inches (100 to 400 mm)...'. "
     "'generally' and 'typically' make this a typical range, not a requirement. Both units are "
     "inside the source's own parentheses."),
    ("SEC-02-2-P0-008", "initial_shotcrete_lining", "not_applicable",
     "FHWA Technical Manual (DOC000047) support-class table", ["typical_range", "case_specific"],
     "Source: crushed and squeezing rock rows both give '12 in (300 mm) and more'. Conditioned on "
     "named rock conditions, so case_specific."),
    ("SEC-02-2-C-001", "shotcrete", "system_independent", "KTS 2013 §351.10.01",
     ["minimum", "mandatory"],
     "Source: 'Püskürtme betonun basınç dayanım sınıfi minimum C25/30 MPa sınıfında olacaktır'. "
     "'olacaktır' is binding, so mandatory as well as a minimum."),
    ("SEC-02-2-C-002", "shotcrete", "system_independent", "Tablo-351-5 (KGM 2013)",
     ["design_table"],
     "Tablo-351-5 gives core-sample acceptance criteria for shotcrete strength classes. It is an "
     "acceptance table, not the strength class itself - hence design_table and the qualifier "
     "already carried on the claim."),
    ("SEC-02-2-C-003", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.08",
     ["maximum", "mandatory"],
     "Source: 'Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi "
     "geçmeyecektir'. Binding modality, stated in centimetres."),
    ("SEC-02-2-C-004", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.08",
     ["recommended", "maximum"],
     "Source: 'tercihen yaklaşık 60 mm (maksimum 100 mm)'. 'tercihen' makes the 60 mm a "
     "preference; the 100 mm is a maximum."),
    ("SEC-02-2-C-005", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.08",
     ["typical_range"],
     "Source: 'Takip eden tabakalar, nihai kalınlığa (ve kullanılan priz hızlandırıcı katkı "
     "malzemesinin tipine) bağlı olarak 50-200 mm olmalıdır'. Both dependencies are stated, so "
     "the range is a typical_range rather than a fixed requirement."),
    ("SEC-02-2-C-006", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.08",
     ["mandatory"],
     "Source: 'müteakip tabaka(lar) ... yeterli mertebeye ulaşmadan uygulanmayacaktır'. The "
     "modality is a prohibition, so the requirement scope is mandatory and carries no figure of "
     "its own - it is the strength gate between layers."),
    ("SEC-02-2-C-007", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.08",
     ["maximum", "mandatory"],
     "Source: 'Bu ilave tabakalar, üç günü geçmeyen bir süre içersinde tamamlanmış olacaktır'. "
     "A binding upper bound on elapsed time, stated in days, in the same clause as the layering "
     "rule."),
    ("SEC-02-2-C-008", "steel_fibre_shotcrete", "system_independent",
     "KTS/KGM 2013 §351.08.09", ["typical_range"],
     "Section heading is 'Çelik Liflerle Püskürtme', so the material scope is steel-fibre "
     "shotcrete specifically and not shotcrete generally. The 50 mm first phase belongs to that "
     "narrower material and must not be read as a general first-layer thickness."),
    ("SEC-02-2-C-009", "shotcrete", "system_independent", "KTS 2013 §351.08.10.02",
     ["typical_range", "case_specific"],
     "Section heading scopes the figure to clay zones. 'genellikle' makes it typical. The 150 mm "
     "here is a source-stated range bound and is unrelated to the derived 150 mm in C-003."),
    ("SEC-02-2-C-010", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.11",
     ["recommended", "case_specific"],
     "Source heads the list 'Herhangi bir priz hızlandırıcı katkı malzemesi kullanılmaksızın, "
     "püskürtülen katmanlar için tavsiye edilen kalınlıklar'. 'tavsiye edilen' makes these "
     "recommendations rather than requirements, and the accelerator-free condition scopes them."),
    ("SEC-02-2-C-011", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.11",
     ["recommended", "case_specific"],
     "Same list, the no-reinforcement branch. Kept separate from C-010 because merging the two "
     "figure pairs would read as a contradiction."),
    ("SEC-02-2-C-012", "shotcrete", "system_independent", "KTS/KGM 2013 §351.08.11",
     ["typical_range", "case_specific"],
     "Source: 'Yaklaşık 20 °C sıcaklıkta ve herhangi bir priz hızlandırıcı katkı malzemesi "
     "kullanılmaz ise, bekleme süresi yaklaşık 3-5 saattir'. Both conditions and both hedges "
     "('yaklaşık' twice) are stated, so this is a typical range under named conditions."),
    ("SEC-02-2-C-013", "steel_mesh", "not_applicable", "DOC000215 'Çelik hasır montajı'",
     ["design_table"],
     "Source lists 'Hasır Çelik Tipleri' and under it '(R) Tipleri 15 adet boy, 20 adet en "
     "çubuklu'. The material scope is welded wire mesh, not shotcrete: the figures are bar "
     "counts for a reinforcement product and carry no cement or thickness meaning."),
    ("SEC-02-2-C-014", "steel_mesh", "not_applicable", "DOC000215 'Çelik hasır montajı'",
     ["design_table"],
     "Same enumeration, the (Q) row: '15 adet boy, 33 adet en çubukludur'. Recorded as a "
     "design_table because it is a product type listing rather than a project requirement."),
    ("SEC-02-2-C-015", "steel_mesh", "not_applicable", "DOC000124 / DOC000098",
     ["design_table"],
     "Two independent sources state the same pair of mesh construction types in one sentence "
     "each ('zincir şeklinde geçmeli' and 'kaynatılarak tutturulan'). The enumeration is the "
     "source's own, which is why both types may share a sentence."),
    ("SEC-02-2-C-016", "steel_mesh", "not_applicable", "DOC000215 'Çelik hasır montajı'",
     ["design_table"],
     "Source states 'Standart Çelik Hasır 5.00 x 2.15 m. ebadındadır' and 'Çelik Hasır ile "
     "ilgili TSE standardı TS 4559'dur'. Product dimensions and a standard reference, not a "
     "shotcrete requirement."),
    ("SEC-02-2-C-017", "steel_mesh", "not_applicable", "DOC000195",
     ["case_specific"],
     "Describes one named mine operation's practice. The scope qualifier already on the claim is "
     "mandatory: without it these figures read as a specification requirement."),
    ("SEC-02-2-R025", "flashcrete", "not_applicable", "FHWA Technical Manual (DOC000047)",
     ["typical_range"],
     "Source describes flashcrete as a sealing layer that is not considered active support and "
     "is normally followed by the initial shotcrete lining. Material scope is flashcrete "
     "specifically, which is why its figures never interact with the lining-thickness claims."),
]


# ================================================================ 2. restricted figures

# The figures whose composition is constrained. Every one is unit-scoped: matching on bare values
# would collide "400 kg/m3" (wet-system cement minimum) with the "400 mm" in an inch-to-millimetre
# thickness range - a different quantity, a different material, the same numeral.
RESTRICTED_FIGURES = [
    {"figure_id": "FIG-360-GENERAL-MAX", "claim_id": "SEC-02-2-P0-002",
     "value": "360", "unit": "kg/m³", "label": "360 kg/m³ general-concrete maximum",
     "material_scope": "general_concrete", "system_scope": "not_applicable",
     "requirement_scope": "maximum",
     "note": "Tablo-308-23-b. Meaningless and misleading without its scope."},
    {"figure_id": "FIG-350-DRY-MIN", "claim_id": "SEC-02-2-R001",
     "value": "350", "unit": "kg/m³", "label": "350 kg/m³ dry-system shotcrete minimum",
     "material_scope": "dry_system_shotcrete", "system_scope": "dry_system",
     "requirement_scope": "minimum",
     "note": "Shotcrete specification, dry system."},
    {"figure_id": "FIG-400-WET-MIN", "claim_id": "SEC-02-2-P0-001",
     "value": "400", "unit": "kg/m³", "label": "400 kg/m³ wet-system shotcrete minimum",
     "material_scope": "wet_system_shotcrete", "system_scope": "wet_system",
     "requirement_scope": "minimum",
     "note": "Shotcrete specification, wet system."},
]

# Same-material families whose members may share a sentence, but only with their distinguishing
# condition present. 350 and 400 are both shotcrete minimums and the source states them together;
# what is forbidden is merging them into one figure or inventing a 350-400 range.
SCOPE_FAMILIES = [
    {"family_id": "FAM-SHOTCRETE-CEMENT-MIN",
     "figure_ids": ["FIG-350-DRY-MIN", "FIG-400-WET-MIN"],
     "relationship": "SOURCE_SUPPORTED_RELATION",
     "note": "The source states both minimums in one span, distinguished by system. They may be "
             "compared as dry-system vs wet-system and in no other way: without both system "
             "markers the sentence either merges two requirements or invents a 350-400 range.",
     "required_action": "name both systems explicitly (kuru sistem / yaş sistem) in the sentence "
                        "carrying both figures, or split them into separate sentences"},
]


def build_claim_scopes(allowlist: list[dict]) -> list[ClaimScopeV1]:
    binding = {row[0]: row for row in SCOPE_BINDING}
    by_id = {row["claim_id"]: row for row in allowlist}
    missing = sorted(set(by_id) - set(binding))
    if missing:
        raise RuntimeError(f"allowlisted claims without an authored scope: {missing}")
    scopes: list[ClaimScopeV1] = []
    for claim_id, row in sorted(by_id.items()):
        _, material, system, document, requirement, evidence = binding[claim_id]
        assert material in MATERIAL_SCOPES, material
        assert system in SYSTEM_SCOPES, system
        assert all(r in REQUIREMENT_SCOPES for r in requirement), requirement
        scopes.append(ClaimScopeV1(
            claim_id=claim_id, topic=row["topic"], material_scope=material,
            system_scope=system, document_scope=document, requirement_scope=requirement,
            conditions=row["conditions"], qualifiers=row["qualifiers"], exceptions=[],
            numeric_values=row["numeric"], source_keys=row["source_keys"],
            authority_levels=[], scope_evidence=evidence))
    return scopes


# ================================================================ 3. the three rule families

@dataclass
class MandatoryQualifierRule:
    rule_id: str
    claim_id: str
    figure_id: str
    required_scope: str
    required_qualifier: str
    forbidden_unqualified_form: str
    forbidden_scopes: list[str]
    misattribution_note: str
    required_action: str
    severity: str
    origin_limitation: str
    # Whether a bare, scope-less rendering fails. True only where the bare form is actively
    # misleading rather than merely terse - see build_qualifier_rules for why that is asymmetric
    # between the 360 maximum and the 350/400 minimums.
    enforce_unqualified: bool = True
    audit_method: str = AUDIT_METHOD


@dataclass
class ForbiddenSynthesisRule:
    rule_id: str
    synthesis_id: str
    component_claim_ids: list[str]
    forbidden_relationship: str
    forbidden_patterns: list[str]
    pattern_intent: list[str]
    safe_representation: str
    required_action: str
    severity: str
    audit_method: str = AUDIT_METHOD


@dataclass
class DerivedNumericRule:
    rule_id: str
    claim_id: str
    source_value: str
    source_unit: str
    derived_value: str
    derived_unit: str
    derived: bool
    source_stated: bool
    drafting_policy: str
    context_markers: list[str]
    exempt_context_markers: list[str]
    exemption_reason: str
    required_action: str
    severity: str
    audit_method: str = AUDIT_METHOD


@dataclass
class ClaimPairConstraint:
    constraint_id: str
    left_claim_id: str
    right_claim_id: str
    relationship_policy: str
    required_qualifiers: list[str]
    allowed_same_sentence: bool
    allowed_same_paragraph: bool
    manual_review_required: bool
    reason: str
    required_action: str
    origin_limitation: str | None = None
    audit_method: str = AUDIT_METHOD


def build_qualifier_rules() -> list[MandatoryQualifierRule]:
    """CF-P0-001, expressed as an enforceable rule rather than as a note in an audit file.

    Enforcement is deliberately asymmetric, and the asymmetry has a reason.

    The 360 figure is enforced in BOTH directions - a bare rendering fails and a shotcrete
    attribution fails. A bare "maksimum çimento miktarı 360 kg/m³'tür" is not merely terse: it
    sits inside a section whose entire subject is shotcrete, so the reader supplies the missing
    scope and supplies the wrong one. The sentence is actively misleading, not incomplete.

    The 350 and 400 figures are enforced in ONE direction - misattribution fails, bareness does
    not. Both live in the shotcrete specification, which is also the section's subject, so a
    reader who supplies the missing scope supplies the right one. Requiring an explicit shotcrete
    marker on every mention would reject SEC-02-2-P0-005's own canonical wording and the
    source-supported dry/wet comparison in POS-350-400-01, neither of which is unsafe.

    What 350 and 400 additionally need is the system distinction, and that is handled as a scope
    family rather than a per-figure qualifier, because it only binds when both figures meet.
    """
    rules = [
        MandatoryQualifierRule(
            rule_id="MQ-001", claim_id="SEC-02-2-P0-002", figure_id="FIG-360-GENERAL-MAX",
            required_scope="general_concrete",
            required_qualifier="Tablo-308-23-b, etki sınıflarına göre projelendirmede esas "
                               "alınacak GENEL beton özelliklerine ilişkindir; püskürtme beton "
                               "şartnamesi değildir",
            forbidden_unqualified_form="Maksimum çimento miktarı 360 kg/m³'tür.",
            forbidden_scopes=["shotcrete", "dry_system", "wet_system"],
            misattribution_note="Presenting the general-concrete maximum as a shotcrete figure "
                                "states something false about shotcrete while citing a true "
                                "statement about general concrete - the citation would resolve "
                                "and the sentence would still be wrong.",
            required_action="render 360 kg/m³ only in a sentence that names its general-concrete "
                            "/ Tablo-308-23-b scope; never bare, never as a shotcrete figure",
            severity="BLOCKING", origin_limitation="CF-P0-001", enforce_unqualified=True),
        MandatoryQualifierRule(
            rule_id="MQ-002", claim_id="SEC-02-2-R001", figure_id="FIG-350-DRY-MIN",
            required_scope="shotcrete",
            required_qualifier="püskürtme beton (kuru sistem) şartname hükmüdür",
            forbidden_unqualified_form="(bare form permitted - the section's subject supplies "
                                       "the correct scope)",
            forbidden_scopes=["general_concrete"],
            misattribution_note="The mirror of MQ-001: a dry-system shotcrete minimum presented "
                                "as a general-concrete requirement. Tablo-308-23-b sets no "
                                "cement minimum at all, so this attributes to it a requirement "
                                "it does not contain.",
            required_action="do not attribute the 350 kg/m³ shotcrete minimum to general "
                            "concrete or to Tablo-308-23-b",
            severity="BLOCKING", origin_limitation="CF-P0-001", enforce_unqualified=False),
        MandatoryQualifierRule(
            rule_id="MQ-003", claim_id="SEC-02-2-P0-001", figure_id="FIG-400-WET-MIN",
            required_scope="shotcrete",
            required_qualifier="püskürtme beton (yaş sistem) şartname hükmüdür",
            forbidden_unqualified_form="(bare form permitted - the section's subject supplies "
                                       "the correct scope)",
            forbidden_scopes=["general_concrete"],
            misattribution_note="The mirror of MQ-001 for the wet-system minimum. Attributing it "
                                "to general concrete would also place a 400 kg/m³ minimum above "
                                "Tablo-308-23-b's 360 kg/m³ maximum, manufacturing the very "
                                "contradiction CF-P0-001 exists to prevent.",
            required_action="do not attribute the 400 kg/m³ shotcrete minimum to general "
                            "concrete or to Tablo-308-23-b",
            severity="BLOCKING", origin_limitation="CF-P0-001", enforce_unqualified=False),
    ]
    for rule in rules:
        assert rule.severity in SEVERITIES
        assert rule.required_scope in SCOPE_MARKERS
        assert all(scope in SCOPE_MARKERS for scope in rule.forbidden_scopes)
    return rules


def build_forbidden_synthesis_rules() -> list[ForbiddenSynthesisRule]:
    """SYN-001.

    Two layers, and the second is the one that matters. The first is a set of patterns matching
    the historical wording and its close variants - useful, but a pattern list is only ever as
    good as the imagination of whoever wrote it. The second layer is the same-sentence
    prohibition in the pair constraints, which needs no pattern at all: the 360 figure may not
    share a sentence with 350 or 400 under any phrasing whatsoever. That is what makes the rule
    hold against a connective nobody thought to enumerate.
    """
    concessive = ("ancak|buna rağmen|buna karşın|olmasına rağmen|olmakla birlikte|belirtilse de|"
                  "olsa da|rağmen|karşın|oysa|oysaki|halbuki|fakat|lakin|aksine|tersine|"
                  "although|though|despite|however|whereas|but|in contrast|nevertheless|"
                  "nonetheless|conversely")
    number_360 = r"360\s*kg/m\s?3"
    number_350 = r"350\s*kg/m\s?3"
    number_400 = r"400\s*kg/m\s?3"
    rules = [
        ForbiddenSynthesisRule(
            rule_id="FS-001", synthesis_id="SYN-001",
            component_claim_ids=["SEC-02-2-P0-002", "SEC-02-2-P0-003", "SEC-02-2-R001",
                                 "SEC-02-2-P0-001"],
            forbidden_relationship="concessive / exception relation between the general-concrete "
                                   "maximum and the shotcrete minimums",
            forbidden_patterns=[
                # The historical wording and near variants: 360 then a concessive then 350 or 400.
                rf"{number_360}.{{0,200}}?(?:{concessive}).{{0,200}}?(?:{number_350}|{number_400})",
                rf"(?:{number_350}|{number_400}).{{0,200}}?(?:{concessive}).{{0,200}}?{number_360}",
                # 350/400 written as a slash-pair against the 360 maximum, which is how the
                # dropped synthesis abbreviated itself.
                r"360\s*kg/m\s?3.{0,200}?350\s?/\s?400",
                r"350\s?/\s?400\s*kg/m\s?3.{0,200}?360",
                # An explicit exception claim in either direction.
                rf"{number_360}.{{0,160}}?(?:istisna|exception|exempt)",
                rf"(?:istisna|exception|exempt).{{0,160}}?{number_360}",
                # An explicit contradiction claim. CF-P0-001 is a CONTEXT_DIFFERENCE, not a
                # TRUE_CONFLICT, so asserting a contradiction is asserting something no
                # ConflictRecord supports.
                rf"{number_360}.{{0,200}}?(?:çelişmekte|çelişki|contradict|conflict)",
                rf"(?:çelişmekte|çelişki|contradict|conflict).{{0,200}}?{number_360}",
                # An invented range spanning the two materials, or the 360 read as a ceiling on
                # the shotcrete minimums.
                r"350\s*(?:ila|-|–|to)\s*400\s*kg/m\s?3",
                r"360\s*kg/m\s?3.{0,120}?(?:üst sınır|üst limit|tavan|ceiling|upper limit)",
            ],
            pattern_intent=[
                "historical SYN-001 wording: 360 joined to 350 or 400 by a concessive",
                "the same construction in reverse order (minimum first, maximum second)",
                "the 350/400 slash abbreviation placed after 360",
                "the 350/400 slash abbreviation placed before 360",
                "360 named as having an exception",
                "360 named as being an exception",
                "360 asserted to contradict the shotcrete minimums - no TRUE_CONFLICT record "
                "exists, CF-P0-001 is a CONTEXT_DIFFERENCE",
                "the same contradiction claim in reverse order",
                "a fabricated 350-400 interval collapsing the dry/wet system distinction",
                "360 recast as a ceiling or upper limit over the shotcrete minimums",
            ],
            safe_representation="SEPARATE_SUPPORTED_CLAIMS",
            required_action="state the general-concrete maximum and the shotcrete minimums as "
                            "separate, separately scoped claims in separate sentences; assert no "
                            "relation between them",
            severity="BLOCKING"),
    ]
    for rule in rules:
        assert rule.severity in SEVERITIES
        assert len(rule.forbidden_patterns) == len(rule.pattern_intent)
        for pattern in rule.forbidden_patterns:
            re.compile(pattern)
    return rules


def build_derived_numeric_rules() -> list[DerivedNumericRule]:
    """The 15 cm / 150 mm guard.

    The exemption list is the whole difficulty. SEC-02-2-C-009 states "100-150 mm" for clay-zone
    first layers and that 150 mm *is* source-stated - so a guard keyed on the string "150 mm"
    would reject a true, properly cited claim. The guard therefore fires on the single-pass
    thickness context and stands down in the clay-zone one.
    """
    rules = [
        DerivedNumericRule(
            rule_id="DN-001", claim_id="SEC-02-2-C-003",
            source_value="15", source_unit="cm", derived_value="150", derived_unit="mm",
            derived=True, source_stated=False,
            drafting_policy="SOURCE_STATED_ONLY",
            context_markers=["bir defada", "tek seferde", "tek geçişte", "bir kerede",
                             "maksimum kalınlık", "maksimum kalınlığı", "single pass",
                             "in one pass", "single application"],
            exempt_context_markers=["kil zonu", "kil zonlu", "clay zone", "351.08.10.02",
                                    "100-150", "100 - 150", "100–150"],
            exemption_reason="SEC-02-2-C-009 states 'İlk püskürtme beton katmanı genellikle "
                             "100-150 mm'dir' for clay-zone layers. That 150 mm is source-stated "
                             "and cited; it is a different clause with different provenance and "
                             "must keep passing.",
            required_action="state the single-pass maximum as 15 cm, the unit the source uses; do "
                            "not attribute 150 mm to the specification",
            severity="BLOCKING"),
    ]
    for rule in rules:
        assert rule.severity in SEVERITIES
        assert rule.drafting_policy == "SOURCE_STATED_ONLY"
    return rules


def build_pair_constraints() -> list[ClaimPairConstraint]:
    """Pairwise composition policy.

    The 360-vs-350 and 360-vs-400 rows are the enforcement of CF-P0-001 and the structural half
    of SYN-001: same paragraph permitted, same sentence forbidden. The 350-vs-400 row is the
    contrast - a source-supported comparison, permitted in one sentence, but only with both
    system scopes named.
    """
    cross_reason = (
        "Different material (general concrete vs shotcrete), different requirement direction "
        "(maximum vs minimum), different document scope (Tablo-308-23-b exposure-class design "
        "table vs the shotcrete specification) and different design route. No source relates "
        "them. A single sentence containing both invites the reader to read one as bounding the "
        "other, which is exactly the proposition SYN-001 asserted and no source supports.")
    cross_action = (
        "put the two figures in separate sentences, each naming its own scope, with no connector "
        "tying them; or drop one of them from the unit")
    rows = [
        ClaimPairConstraint(
            constraint_id="PC-001", left_claim_id="SEC-02-2-P0-002",
            right_claim_id="SEC-02-2-R001", relationship_policy="INDEPENDENT",
            required_qualifiers=["general_concrete scope on 360 kg/m³",
                                 "dry_system shotcrete scope on 350 kg/m³"],
            allowed_same_sentence=False, allowed_same_paragraph=True,
            manual_review_required=False, reason=cross_reason, required_action=cross_action,
            origin_limitation="CF-P0-001"),
        ClaimPairConstraint(
            constraint_id="PC-002", left_claim_id="SEC-02-2-P0-002",
            right_claim_id="SEC-02-2-P0-001", relationship_policy="INDEPENDENT",
            required_qualifiers=["general_concrete scope on 360 kg/m³",
                                 "wet_system shotcrete scope on 400 kg/m³"],
            allowed_same_sentence=False, allowed_same_paragraph=True,
            manual_review_required=False, reason=cross_reason, required_action=cross_action,
            origin_limitation="CF-P0-001"),
        ClaimPairConstraint(
            constraint_id="PC-003", left_claim_id="SEC-02-2-P0-002",
            right_claim_id="SEC-02-2-P0-003", relationship_policy="INDEPENDENT",
            required_qualifiers=["general_concrete scope on 360 kg/m³",
                                 "shotcrete scope with both systems named"],
            allowed_same_sentence=False, allowed_same_paragraph=True,
            manual_review_required=False,
            reason=cross_reason + " P0-003 carries both shotcrete minimums, so pairing it with "
                                  "the 360 figure in one sentence is the SYN-001 construction "
                                  "almost verbatim.",
            required_action=cross_action, origin_limitation="CF-P0-001"),
        ClaimPairConstraint(
            constraint_id="PC-004", left_claim_id="SEC-02-2-P0-002",
            right_claim_id="SEC-02-2-P0-006", relationship_policy="INDEPENDENT",
            required_qualifiers=["general_concrete scope on 360 kg/m³",
                                 "shotcrete scope with both systems named"],
            allowed_same_sentence=False, allowed_same_paragraph=True,
            manual_review_required=False, reason=cross_reason, required_action=cross_action,
            origin_limitation="CF-P0-001"),
        ClaimPairConstraint(
            constraint_id="PC-005", left_claim_id="SEC-02-2-R001",
            right_claim_id="SEC-02-2-P0-001", relationship_policy="SOURCE_SUPPORTED_RELATION",
            required_qualifiers=["kuru sistem named for 350 kg/m³",
                                 "yaş sistem named for 400 kg/m³"],
            allowed_same_sentence=True, allowed_same_paragraph=True,
            manual_review_required=False,
            reason="Both are shotcrete cement minimums and one source span states them together, "
                   "distinguished by system: 'kuru sistemde 350 kg/m³'ten, yaş sistemde ise 400 "
                   "kg/m³'ten az olmayacaktır'. The comparison is the source's own, so it may be "
                   "drafted - but only as dry-system vs wet-system. Merging them into a single "
                   "figure or a 350-400 range is not what the source says.",
            required_action="name both systems in the sentence carrying both figures",
            origin_limitation=None),
        ClaimPairConstraint(
            constraint_id="PC-006", left_claim_id="SEC-02-2-P0-002",
            right_claim_id="SEC-02-2-P0-005", relationship_policy="INDEPENDENT",
            required_qualifiers=["general_concrete scope on 360 kg/m³",
                                 "shotcrete durability scope on 350 kg/m³"],
            allowed_same_sentence=False, allowed_same_paragraph=True,
            manual_review_required=False,
            reason=cross_reason + " P0-005's 350 kg/m³ floor is a shotcrete durability minimum "
                                  "set by exposure class and mix-design work; placing it beside "
                                  "the general-concrete maximum implies a single governing rule.",
            required_action=cross_action, origin_limitation="CF-P0-001"),
    ]
    for row in rows:
        assert row.relationship_policy in RELATIONSHIP_TYPES
    return rows


# ================================================================ 4. contract assembly

def build_composition_contract(scopes: list[ClaimScopeV1],
                               qualifier_rules: list[MandatoryQualifierRule],
                               synthesis_rules: list[ForbiddenSynthesisRule],
                               derived_rules: list[DerivedNumericRule],
                               pairs: list[ClaimPairConstraint]) -> dict[str, Any]:
    return {
        "version": CONTRACT_VERSION,
        "authored_by": RESOLUTION_VERSION,
        "authored_at": now(),
        "section_id": SECTION_ID,
        "scope": "SEC-02-2 only. This contract is not a general natural-language inference "
                 "system and must not be applied to other sections without their own scope "
                 "binding and their own regression suite.",
        "purpose": (
            "Decide whether a set of individually supported claims may appear in the same future "
            "draft unit, and under what qualifiers. Evidence correctness is checked upstream; "
            "what is checked here is composition - because two supported claims can be combined "
            "into a proposition no source states, which is what SYN-001 was."),
        "core_principle": (
            "supported claim A + supported claim B does NOT imply 'A therefore B', 'A although "
            "B', 'A contradicts B' or 'A is an exception to B' unless that relationship is "
            "itself supported by a source or an approved synthesis contract."),
        "determinism": "All decisions are regex, set membership or sentence-window comparisons. "
                       "No LLM judge is used at any point.",
        "failure_mode": "fail_closed - no auto-rewrite, no auto-repair, no automatic qualifier "
                        "insertion. An invalid draft unit is rejected with required actions.",
        "vocabularies": {
            "material_scopes": list(MATERIAL_SCOPES),
            "requirement_scopes": list(REQUIREMENT_SCOPES),
            "system_scopes": list(SYSTEM_SCOPES),
            "relationship_types": list(RELATIONSHIP_TYPES),
            "severities": list(SEVERITIES),
        },
        "claim_scopes": [asdict(s) for s in scopes],
        "restricted_figures": RESTRICTED_FIGURES,
        "scope_families": SCOPE_FAMILIES,
        "scope_markers": SCOPE_MARKERS,
        "negation_markers": NEGATION_MARKERS,
        "negation_rationale": (
            "The qualifier CF-P0-001 mandates contains the phrase 'püskürtme beton şartnamesi "
            "değildir'. Without negation handling, a wrong-scope check would reject the exact "
            "form the contract requires. Negation is therefore load-bearing, not cosmetic."),
        "relation_connectors": RELATION_CONNECTORS,
        "connector_policy": (
            "Connector matching is used only for the cross-sentence paragraph case. Same-sentence "
            "juxtaposition of restricted figures is forbidden outright, with no connector "
            "analysis, because a prohibition that depends on enumerating conjunctions can be "
            "evaded by choosing one nobody enumerated."),
        "mandatory_qualifier_rules": [asdict(r) for r in qualifier_rules],
        "forbidden_synthesis_rules": [asdict(r) for r in synthesis_rules],
        "derived_numeric_rules": [asdict(r) for r in derived_rules],
        "claim_pair_constraints": [asdict(p) for p in pairs],
        "derived_numeric_default_policy": "SOURCE_STATED_ONLY",
        "derived_numeric_policy_note": (
            "A later drafting contract may choose to render '15 cm (150 mm)' with the conversion "
            "explicitly marked as calculated and the citation making clear that 150 mm is not "
            "source-stated. That is not the default here. For SEC-02-2 Drafting Contract v1 the "
            "policy is SOURCE_STATED_ONLY, so 150 mm stays out of the draft allowlist entirely."),
        "prohibitions": [
            "no section or chapter prose", "no manuscript drafting",
            "drafting stays disabled and drafting_authorized stays false",
            "no invented relationships, exceptions, conversions, source scope or citation "
            "relationships",
            "no claim wording rewritten merely to make composition easier",
            "narrowing may remove an unsupported relation or an over-broad scope and may never "
            "add technical content",
            "no auto-repair of an invalid draft unit",
        ],
    }


# ================================================================ 5. composition-safe lists

@dataclass
class CompositionSafeClaim:
    claim_id: str
    canonical_claim: str
    topic: str | None
    scope: dict
    conditions: list[str]
    qualifiers: list[str]
    source_keys: list[str]
    citation_ready: bool
    composition_safe: bool
    mandatory_qualifier_rule_ids: list[str]
    forbidden_synthesis_rule_ids: list[str]
    derived_numeric_rule_ids: list[str]
    allowed_relationships: list[str]
    forbidden_relationships: list[str]
    numeric: list[dict] = field(default_factory=list)
    readiness_use: str = ""
    restricted_figure_ids: list[str] = field(default_factory=list)
    parent_claim_id: str | None = None
    narrowing_reason: str | None = None
    scope_preserved: bool = True
    support_preserved: bool = True
    composition_notes: str = ""
    section_id: str = SECTION_ID
    contract_version: str = CONTRACT_VERSION
    audit_method: str = AUDIT_METHOD


def build_composition_safe_allowlist(
        allowlist: list[dict], scopes: list[ClaimScopeV1],
        qualifier_rules: list[MandatoryQualifierRule],
        synthesis_rules: list[ForbiddenSynthesisRule],
        derived_rules: list[DerivedNumericRule],
        pairs: list[ClaimPairConstraint]) -> list[CompositionSafeClaim]:
    """Every evidence-allowlisted claim, annotated with the rules that bind it.

    No claim is dropped for being *constrained* - a claim with a mandatory qualifier is still
    draftable, it just cannot be drafted bare. A claim would only fail composition safety if its
    own canonical wording asserted an unsupported relation, and none does: the closure phase
    already denied the compounds.
    """
    scope_by_id = {s.claim_id: s for s in scopes}
    rows: list[CompositionSafeClaim] = []
    for claim in sorted(allowlist, key=lambda c: c["claim_id"]):
        claim_id = claim["claim_id"]
        scope = scope_by_id[claim_id]
        my_qualifier_rules = [r.rule_id for r in qualifier_rules if r.claim_id == claim_id]
        my_synthesis_rules = [r.rule_id for r in synthesis_rules
                              if claim_id in r.component_claim_ids]
        my_derived_rules = [r.rule_id for r in derived_rules if r.claim_id == claim_id]
        my_figures = [f["figure_id"] for f in RESTRICTED_FIGURES if f["claim_id"] == claim_id]
        allowed, forbidden = set(), set()
        for pair in pairs:
            if claim_id not in (pair.left_claim_id, pair.right_claim_id):
                continue
            allowed.add(pair.relationship_policy)
            if not pair.allowed_same_sentence:
                forbidden.add("FORBIDDEN_SYNTHESIS")
        if not allowed:
            allowed.add("INDEPENDENT")
        # A claim whose own wording asserts a relation across scopes would be unsafe. The closure
        # phase's denylist already removed those, so this is a guard rather than a filter - if it
        # ever fires, the upstream allowlist has regressed.
        unsafe_wording = _wording_asserts_cross_scope_relation(
            claim["canonical_claim"], synthesis_rules)
        rows.append(CompositionSafeClaim(
            claim_id=claim_id, canonical_claim=claim["canonical_claim"], topic=claim["topic"],
            scope={"material_scope": scope.material_scope, "system_scope": scope.system_scope,
                   "document_scope": scope.document_scope,
                   "requirement_scope": scope.requirement_scope,
                   "scope_evidence": scope.scope_evidence},
            conditions=claim["conditions"], qualifiers=claim["qualifiers"],
            source_keys=claim["source_keys"], citation_ready=claim["citation_ready"],
            composition_safe=not unsafe_wording,
            mandatory_qualifier_rule_ids=my_qualifier_rules,
            forbidden_synthesis_rule_ids=my_synthesis_rules,
            derived_numeric_rule_ids=my_derived_rules,
            allowed_relationships=sorted(allowed), forbidden_relationships=sorted(forbidden),
            numeric=claim["numeric"], readiness_use=claim["readiness_use"],
            restricted_figure_ids=my_figures,
            composition_notes=(
                "Bound by a BLOCKING mandatory-qualifier rule; may never be rendered bare."
                if my_qualifier_rules else
                "Bound by a BLOCKING derived-numeric rule; the converted value may not be "
                "attributed to the source." if my_derived_rules else
                "May share a sentence only with claims its pair constraints permit."
                if my_figures else "No composition restriction beyond allowlist membership.")))
    return rows


def _wording_asserts_cross_scope_relation(
        wording: str, synthesis_rules: list[ForbiddenSynthesisRule]) -> bool:
    validator = load_validator()
    folded = validator.fold(wording)
    return any(re.search(pattern, folded)
               for rule in synthesis_rules for pattern in rule.forbidden_patterns)


def build_composition_denylist(closure_denylist: list[dict],
                               qualifier_rules: list[MandatoryQualifierRule],
                               synthesis_rules: list[ForbiddenSynthesisRule],
                               derived_rules: list[DerivedNumericRule]) -> list[dict]:
    """The closure denylist, carried forward, plus the composition-level forms.

    Carrying the evidence denylist forward matters: a drafter that consults only the composition
    denylist must still be stopped from citing a superseded or partial claim, so both layers live
    in one file rather than requiring the consumer to read two.
    """
    rows: list[dict] = []
    for row in closure_denylist:
        rows.append(dict(row, carried_from=PARENT_VERSION,
                         deny_layer="evidence",
                         contract_version=CONTRACT_VERSION))
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-360-UNQUALIFIED",
        "canonical_claim": "Maksimum çimento miktarı 360 kg/m³'tür.",
        "question_id": "Q-02-2-01", "support_status": "SUPPORTED_BUT_UNSAFE_AS_WRITTEN",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["unqualified_scope", "cross_scope_misattribution_risk"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-P0-002"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["MQ-001"],
        "note": "The figure is true and cited; the sentence is not draftable because it drops the "
                "scope that makes the figure mean anything. SEC-02-2-P0-002 with its mandatory "
                "qualifier is the draftable form."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-360-AS-SHOTCRETE",
        "canonical_claim": "Püskürtme beton için maksimum çimento miktarı 360 kg/m³'tür.",
        "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["scope_misattribution", "material_scope_violation"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-P0-002"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["MQ-001"],
        "note": "States something false about shotcrete while citing a true statement about "
                "general concrete. The citation would resolve and the sentence would still be "
                "wrong, which is why scope binding cannot be left to citation checking."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-350-AS-GENERAL",
        "canonical_claim": "Genel beton için minimum çimento miktarı 350 kg/m³'tür.",
        "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["scope_misattribution", "material_scope_violation"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-R001"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["MQ-001"],
        "note": "The mirror error: a shotcrete dry-system minimum presented as a general-concrete "
                "requirement."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-SYN-001-COMPOUND",
        "canonical_claim": "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ "
                           "olarak belirtilse de, püskürtme beton spesifikasyonlarında minimum "
                           "350/400 kg/m³ öngörülmüştür.",
        "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["unsafe_synthesis", "concessive_relation_asserted_by_no_source",
                         "different_material_scope"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["FS-001", "PC-001", "PC-002", "PC-003", "PC-004"],
        "note": "The historical SYN-001 wording. Both components are separately draftable; this "
                "sentence is not, and no restatement of it becomes so."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-360-400-CONTRAST",
        "canonical_claim": "Maksimum 360 kg/m³ sınırına karşın yaş sistemde minimum 400 kg/m³ "
                           "istenmektedir.",
        "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["unsafe_synthesis", "cross_scope_comparison"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["FS-001", "PC-002"],
        "note": "A shorter paraphrase of the same construction, showing that the prohibition is "
                "on the juxtaposition and not on any particular set of words."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-CEMENT-RANGE",
        "canonical_claim": "Püskürtme betonda çimento dozajı 350 ila 400 kg/m³ arasındadır.",
        "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["invented_range", "system_scope_collapsed"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-P0-003"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["FS-001", "FAM-SHOTCRETE-CEMENT-MIN"],
        "note": "Two separate system minimums collapsed into one range. The source states a floor "
                "of 350 for dry and a floor of 400 for wet; it states no interval, and reading "
                "one licenses 360 kg/m³ wet-system shotcrete, which the source forbids."})
    rows.append({
        "claim_id": "SEC-02-2-DENY-COMP-150MM-SOURCE-STATED",
        "canonical_claim": "Kaynak, bir defada uygulanacak maksimum kalınlığı 150 mm olarak "
                           "vermektedir.",
        "question_id": "Q-02-2-04", "support_status": "DERIVED_ONLY",
        "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
        "deny_reasons": ["derived_numeric_presented_as_source_stated",
                         "unsupported_unit_conversion"],
        "deny_layer": "composition", "superseded_by": ["SEC-02-2-C-003"],
        "section_id": SECTION_ID, "contract_version": CONTRACT_VERSION,
        "enforced_by": ["DN-001"],
        "note": "The requirement is draftable as 15 cm. Attributing 150 mm to the specification "
                "attributes a conversion nobody performed in the source."})
    return sorted(rows, key=lambda r: r["claim_id"])


def load_validator():
    return _load("composition_validator_v1",
                 "scripts/46_sec_02_2_claim_composition_validator_v1.py")


# ================================================================ 6. regression fixtures

# Synthetic candidate draft units. None of this is SEC-02-2 prose and none of it is destined for
# the manuscript: several cases are deliberately wrong, and the correct ones are single sentences
# built to exercise one rule each. Fields: case_id, expected_valid, claim_ids, text, expected
# failure codes, and what the case is actually testing.
FIXTURES: list[tuple[str, bool, list[str], str, list[str], str]] = [

    # ---------- CF-P0-001: the 360 figure, qualified ----------
    ("POS-360-01", True, ["SEC-02-2-P0-002"],
     "Tablo-308-23-b kapsamındaki genel beton için, yüksek dayanımlı beton dışında maksimum "
     "çimento miktarı 360 kg/m³'tür.",
     [], "The canonical qualified form: table named and general concrete named."),
    ("POS-360-02", True, ["SEC-02-2-P0-002"],
     "Etki sınıflarına göre projelendirmede esas alınacak genel beton özellikleri için maksimum "
     "çimento miktarı 360 kg/m³ olmalıdır.",
     [], "Qualified through the exposure-class design route rather than the table number."),
    ("POS-360-03", True, ["SEC-02-2-P0-002"],
     "Tablo-308-23-b, etki sınıflarına göre projelendirmede esas alınacak GENEL beton "
     "özelliklerine ilişkindir ve püskürtme beton şartnamesi değildir; bu tabloya göre maksimum "
     "çimento miktarı 360 kg/m³'tür.",
     [], "The mandatory qualifier verbatim. This is the trap case: the qualifier itself contains "
         "'püskürtme beton', and negation handling must stop that reading as a shotcrete scope."),
    ("POS-360-04", True, ["SEC-02-2-P0-002"],
     "General concrete designed by exposure class has a maximum cement content of 360 kg/m³ "
     "under Tablo-308-23-b.",
     [], "English qualified form."),
    ("NEG-360-01", False, ["SEC-02-2-P0-002"],
     "Maksimum çimento miktarı 360 kg/m³'tür.",
     ["UNQUALIFIED_SCOPE"], "The bare form named in the qualifier rule."),
    ("NEG-360-02", False, ["SEC-02-2-P0-002"],
     "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olmalıdır.",
     ["UNQUALIFIED_SCOPE"],
     "Carries the claim's condition but not its scope. A condition is not a scope: this still "
     "reads as a rule about the material under discussion, which is shotcrete."),
    ("NEG-360-03", False, ["SEC-02-2-P0-002"],
     "Püskürtme beton için maksimum çimento miktarı 360 kg/m³'tür.",
     ["AMBIGUOUS_SCOPE"],
     "Misattribution: a true general-concrete figure asserted about shotcrete. The citation "
     "would resolve and the sentence would still be false."),
    ("NEG-360-04", False, ["SEC-02-2-P0-002"],
     "Kuru sistem püskürtme betonda maksimum çimento miktarı 360 kg/m³ olarak sınırlanmıştır.",
     ["AMBIGUOUS_SCOPE"], "Misattribution into a system scope the figure never had."),
    ("NEG-360-05", False, ["SEC-02-2-P0-002"],
     "The maximum cement content is 360 kg/m³.",
     ["UNQUALIFIED_SCOPE"], "English bare form."),
    ("NEG-360-06", False, ["SEC-02-2-P0-002"],
     "For shotcrete the maximum cement content is 360 kg/m³.",
     ["AMBIGUOUS_SCOPE"], "English misattribution."),

    # ---------- the shotcrete minimums, alone ----------
    ("POS-350-01", True, ["SEC-02-2-R001"],
     "Kuru sistem püskürtme betonda çimento miktarı 350 kg/m³'ten az olmamalıdır.",
     [], "Dry-system minimum alone, system named."),
    ("POS-350-02", True, ["SEC-02-2-R001"],
     "Püskürtme beton şartnamesine göre kuru sistemde minimum çimento dozajı 350 kg/m³'tür.",
     [], "Same figure through the specification scope."),
    ("POS-400-01", True, ["SEC-02-2-P0-001"],
     "Yaş sistem püskürtme betonda çimento miktarı 400 kg/m³'ten az olmamalıdır.",
     [], "Wet-system minimum alone."),
    ("POS-400-02", True, ["SEC-02-2-P0-001"],
     "Yaş sistemde minimum çimento dozajı 400 kg/m³ olarak öngörülmüştür.",
     [], "Wet-system minimum, shorter form."),
    ("NEG-350-01", False, ["SEC-02-2-R001"],
     "Genel beton için minimum çimento miktarı 350 kg/m³'tür.",
     ["AMBIGUOUS_SCOPE"],
     "The mirror of NEG-360-03: a shotcrete minimum asserted about general concrete."),

    # ---------- 350 vs 400: a source-supported comparison ----------
    ("POS-350-400-01", True, ["SEC-02-2-R001", "SEC-02-2-P0-001"],
     "Kuru sistem için minimum 350 kg/m³, yaş sistem için minimum 400 kg/m³ çimento dozajı "
     "aranmaktadır.",
     [], "The comparison the source itself makes, with both systems named. Must PASS - this is "
         "the case that proves the contract does not simply forbid figures from meeting."),
    ("POS-350-400-02", True, ["SEC-02-2-P0-003"],
     "Püskürtme beton spesifikasyonlarında, durabilite gereği kuru sistem için minimum "
     "350 kg/m³ ve yaş sistem için minimum 400 kg/m³ çimento öngörülmüştür.",
     [], "The P0-003 canonical claim itself, drafted as written."),
    ("POS-350-400-03", True, ["SEC-02-2-P0-006"],
     "Özetle, standart uygulamalarda kuru sistemde minimum 350 kg/m³, yaş sistemde ise minimum "
     "400 kg/m³ çimento dozajı aranmaktadır.",
     [], "The summary claim, both systems named."),
    ("POS-350-400-04", True, ["SEC-02-2-R001", "SEC-02-2-P0-001"],
     "Kuru sistemde minimum 350 kg/m³ çimento aranır. Yaş sistemde minimum 400 kg/m³ çimento "
     "aranır.",
     [], "Same pair split into two sentences."),
    ("NEG-350-400-01", False, ["SEC-02-2-R001", "SEC-02-2-P0-001"],
     "Püskürtme betonda minimum çimento dozajı 350 kg/m³ ile 400 kg/m³ arasında değişmektedir.",
     ["AMBIGUOUS_SCOPE"],
     "The system distinction collapsed into an invented range. Reading it licenses 360 kg/m³ "
     "wet-system shotcrete, which the source forbids."),
    ("NEG-350-400-02", False, ["SEC-02-2-P0-003"],
     "Püskürtme betonda çimento dozajı 350 ila 400 kg/m³ arasındadır.",
     ["FORBIDDEN_SYNTHESIS"], "The same fabricated interval in the form the denylist records."),
    ("NEG-350-400-03", False, ["SEC-02-2-R001", "SEC-02-2-P0-001"],
     "Minimum çimento dozajı 350 kg/m³, bazı hallerde 400 kg/m³'tür.",
     ["AMBIGUOUS_SCOPE"],
     "Both figures present, neither system named: 'bazı hallerde' replaces a stated system "
     "distinction with a vague one the source does not make."),

    # ---------- SYN-001: the forbidden synthesis ----------
    ("NEG-SYN-01", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
     "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse de, "
     "püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür.",
     ["FORBIDDEN_SYNTHESIS"], "The historical SYN-001 wording, verbatim."),
    ("NEG-SYN-02", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Tablo-308-23-b genel betonda maksimum 360 kg/m³ öngörmesine rağmen, yaş sistem püskürtme "
     "betonda minimum 400 kg/m³ istenmektedir.",
     ["FORBIDDEN_SYNTHESIS"],
     "Both scopes correctly named and still forbidden: the concession between them is the "
     "unsupported part, not the scoping."),
    ("NEG-SYN-03", False, ["SEC-02-2-P0-002", "SEC-02-2-R001"],
     "Genel betonda maksimum çimento 360 kg/m³'tür; buna rağmen kuru sistem püskürtme betonda "
     "minimum 350 kg/m³ aranır.",
     ["FORBIDDEN_SYNTHESIS"],
     "Semicolon joint. This is why ';' is not treated as a sentence boundary - the juxtaposition "
     "is the defect and punctuation must not launder it."),
    ("NEG-SYN-04", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Genel beton için 360 kg/m³ maksimum belirlenmiş olmakla birlikte yaş sistemde 400 kg/m³ "
     "minimum geçerlidir.",
     ["FORBIDDEN_SYNTHESIS"], "A different concessive connective; same construction."),
    ("NEG-SYN-05", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Genel betonda maksimum 360 kg/m³ iken yaş sistemde minimum 400 kg/m³ gerekmektedir.",
     ["FORBIDDEN_SYNTHESIS"],
     "No connective from any enumerated list - just 'iken'. Caught by the same-sentence rule, "
     "which is the point of having it: the prohibition does not depend on the word chosen."),
    ("NEG-SYN-06", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Maksimum 360 kg/m³ sınırına karşın yaş sistemde minimum 400 kg/m³ istenmektedir.",
     ["FORBIDDEN_SYNTHESIS", "AMBIGUOUS_SCOPE"],
     "The short paraphrase on the denylist. Also a misattribution rather than a bare form: the "
     "only scope in the sentence is 'yaş sistem', so the 360 maximum is read into the wet "
     "system."),
    ("NEG-SYN-07", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
     "Genel beton için 360 kg/m³ üst sınırı, püskürtme beton minimumları için bir istisna "
     "oluşturmaktadır.",
     ["FORBIDDEN_SYNTHESIS"], "An explicit exception relation, which no source states."),
    ("NEG-SYN-08", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Tablo-308-23-b'deki 360 kg/m³ değeri ile yaş sistem için verilen 400 kg/m³ değeri "
     "çelişmektedir.",
     ["FORBIDDEN_SYNTHESIS"],
     "An asserted contradiction. CF-P0-001 is a CONTEXT_DIFFERENCE, not a TRUE_CONFLICT, so no "
     "ConflictRecord licenses this."),
    ("NEG-SYN-09", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Although the general maximum is 360 kg/m³, the wet-system shotcrete minimum is 400 kg/m³.",
     ["FORBIDDEN_SYNTHESIS"], "English concessive."),
    ("NEG-SYN-10", False, ["SEC-02-2-P0-002", "SEC-02-2-R001"],
     "The maximum is 360 kg/m³, whereas the dry-system minimum is 350 kg/m³.",
     ["FORBIDDEN_SYNTHESIS", "AMBIGUOUS_SCOPE"],
     "English adversative. The only scope present is the dry system, so the 360 maximum is "
     "misattributed to it."),
    ("NEG-SYN-11", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
     "Genel beton için maksimum 360 kg/m³ öngörülmüştür. Buna rağmen, püskürtme beton "
     "spesifikasyonlarında kuru sistem için minimum 350 kg/m³ ve yaş sistem için minimum "
     "400 kg/m³ öngörülmüştür.",
     ["UNSUPPORTED_RELATION"],
     "Separate sentences, each correctly scoped - and the second opens with 'Buna rağmen', which "
     "ties them back together. This is the cross-sentence case the paragraph allowance must not "
     "let through."),
    ("NEG-SYN-12", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Tablo-308-23-b kapsamındaki genel betonda maksimum çimento 360 kg/m³'tür. Dolayısıyla yaş "
     "sistem püskürtme betonda minimum 400 kg/m³ aranır.",
     ["UNSUPPORTED_RELATION"],
     "A causal connective across sentences, which invents a derivation between two independent "
     "specifications."),
    ("NEG-SYN-13", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Tablo-308-23-b kapsamındaki genel betonda maksimum çimento 360 kg/m³'tür. However, the "
     "wet-system shotcrete minimum is 400 kg/m³.",
     ["UNSUPPORTED_RELATION"], "English cross-sentence connective in a mixed-language unit."),

    # ---------- the permitted paragraph arrangement ----------
    ("POS-PARA-01", True, ["SEC-02-2-P0-002", "SEC-02-2-P0-001"],
     "Tablo-308-23-b kapsamındaki genel beton için maksimum çimento miktarı 360 kg/m³'tür. "
     "Yaş sistem püskürtme betonda çimento miktarı 400 kg/m³'ten az olmamalıdır.",
     [], "Both claims in one paragraph, separate sentences, each scoped, no connector. This is "
         "the arrangement CF-P0-001 permits and the reason the pair policy is INDEPENDENT rather "
         "than a ban."),
    ("POS-PARA-02", True, ["SEC-02-2-P0-002", "SEC-02-2-R001", "SEC-02-2-P0-001"],
     "Tablo-308-23-b kapsamındaki genel beton için maksimum çimento miktarı 360 kg/m³'tür.\n"
     "- Kuru sistem püskürtme betonda minimum çimento miktarı 350 kg/m³'tür.\n"
     "- Yaş sistem püskürtme betonda minimum çimento miktarı 400 kg/m³'tür.",
     [], "All three figures as separate list items, each scoped. The safe representation SYN-001 "
         "prescribes."),
    ("POS-PARA-03", True, ["SEC-02-2-P0-002", "SEC-02-2-P0-003"],
     "Püskürtme beton spesifikasyonlarında kuru sistem için minimum 350 kg/m³ ve yaş sistem için "
     "minimum 400 kg/m³ çimento öngörülmüştür. Tablo-308-23-b ise etki sınıflarına göre "
     "projelendirilen genel beton için maksimum 360 kg/m³ vermektedir.",
     [], "Reverse order, both scoped, connected only by 'ise' as a topic shift rather than a "
         "relation claim."),

    # ---------- derived numeric: 15 cm / 150 mm ----------
    ("POS-15CM-01", True, ["SEC-02-2-C-003"],
     "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi geçmeyecektir.",
     [], "The source-stated form."),
    ("POS-15CM-02", True, ["SEC-02-2-C-003"],
     "Tek geçişte uygulanacak püskürtme beton kalınlığı en fazla 15 cm olacaktır.",
     [], "Paraphrase in the source's unit."),
    ("NEG-150MM-01", False, ["SEC-02-2-C-003"],
     "Kaynak, bir defada uygulanacak maksimum kalınlığı 150 mm olarak vermektedir.",
     ["DERIVED_VALUE_AS_SOURCE_STATED"], "Explicit source attribution of the conversion."),
    ("NEG-150MM-02", False, ["SEC-02-2-C-003"],
     "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 150 mm'yi geçmeyecektir.",
     ["DERIVED_VALUE_AS_SOURCE_STATED"],
     "The requirement restated in the derived unit. True by arithmetic, unstated by any source."),
    ("NEG-150MM-03", False, ["SEC-02-2-C-003"],
     "Şartnameye göre tek seferde maksimum 150 mm püskürtme beton uygulanabilir.",
     ["DERIVED_VALUE_AS_SOURCE_STATED"], "Attribution to 'şartname' in the derived unit."),
    ("POS-150MM-EXEMPT-01", True, ["SEC-02-2-C-009"],
     "Kil zonlu tabakalar üzerine püskürtme beton uygulamasında ilk katman genellikle "
     "100-150 mm'dir.",
     [], "The exemption that matters: this 150 mm IS source-stated, in a different clause with "
         "different provenance. A guard keyed on the string would reject a true, cited claim."),
    ("POS-150MM-EXEMPT-02", True, ["SEC-02-2-C-009"],
     "351.08.10.02 kapsamındaki kil zonlarında ilk püskürtme beton katmanı 150 mm kalınlığa "
     "kadar uygulanabilir ve lif takviyeli olması tercih edilir.",
     [], "Same exemption reached through the section number."),

    # ---------- other allowlisted claims, drafted plainly ----------
    ("POS-C25-01", True, ["SEC-02-2-C-001"],
     "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
     [], "The required topic 'dayanım sınıfı' core claim."),
    ("POS-C25-02", True, ["SEC-02-2-C-002"],
     "Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda 28 günlük karot numunelerde bireysel "
     "minimum dayanım 22,5 MPa'dır.",
     [], "The acceptance-criteria claim."),
    ("POS-LINING-01", True, ["SEC-02-2-P0-007"],
     "The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
     "(100 to 400 mm).",
     [], "Critical regression: this sentence contains '400 mm'. Unit-scoped figure detection "
         "must not read it as the 400 kg/m³ wet-system cement minimum."),
    ("POS-LINING-02", True, ["SEC-02-2-P0-008"],
     "In some specific rock conditions, such as crushed or squeezing rock, the thickness may be "
     "12 inches (300 mm) and more.",
     [], "Second lining-thickness claim."),
    ("POS-LINING-03", True, ["SEC-02-2-P0-007", "SEC-02-2-P0-008"],
     "The typical thickness of an initial shotcrete lining ranges from 4 to 16 inches "
     "(100 to 400 mm). In crushed or squeezing rock the thickness may be 12 inches (300 mm) and "
     "more.",
     [], "Both thickness claims together - same material, same requirement scope, no restriction."),
    ("POS-LAYER-01", True, ["SEC-02-2-C-004"],
     "İlk tabaka, taze betonun akmaması için ince olmalı; tercihen yaklaşık 60 mm, maksimum "
     "100 mm olmalıdır.",
     [], "First-layer thickness."),
    ("POS-LAYER-02", True, ["SEC-02-2-C-005"],
     "Takip eden tabakalar, nihai kalınlığa ve priz hızlandırıcı katkı tipine bağlı olarak "
     "50-200 mm olmalıdır.",
     [], "Subsequent-layer range."),
    ("POS-LAYER-03", True, ["SEC-02-2-C-006", "SEC-02-2-C-007"],
     "Kalınlığın artırılması gerektiğinde müteakip tabakalar, önceki tabakanın mukavemeti "
     "yeterli mertebeye ulaşmadan uygulanmayacaktır. İlave tabakalar, üç günü geçmeyen bir süre "
     "içerisinde tamamlanmış olacaktır.",
     [], "Two mandatory layering rules from the same section."),
    ("POS-MESH-01", True, ["SEC-02-2-C-013", "SEC-02-2-C-014"],
     "(R) tipi hasır çelik 15 adet boy ve 20 adet en çubuktan oluşur. (Q) tipi hasır çelik "
     "15 adet boy ve 33 adet en çubuktan oluşur.",
     [], "Mesh types. Contains '15 adet' and '20 adet' - unit-scoped detection must not confuse "
         "these with cement or thickness figures."),
    ("POS-MESH-02", True, ["SEC-02-2-C-017"],
     "Bir maden işletmesinde 7 mm kalınlığında ve 15 cm x 15 cm göz aralıklı çelik hasır "
     "kullanılmaktadır.",
     [], "Contains '15 cm' twice in a completely unrelated sense. Must not trip the thickness "
         "rules."),
    ("POS-REPAIR-01", True, ["SEC-02-2-C-010"],
     "Tamir işlerinde, priz hızlandırıcı katkı kullanılmaksızın tepe üstü aynalarda takviye "
     "donatılarını 10 mm geçecek şekilde uygulama tavsiye edilir.",
     [], "Repair-works recommendation with its conditions."),
    ("POS-REPAIR-02", True, ["SEC-02-2-C-011"],
     "Ek katman veya takviye donatısı bulunmayan durumda tepe üstü aynalarda maksimum 30 mm, "
     "dik aynalarda maksimum 50 mm kalınlık tavsiye edilir.",
     [], "The other repair branch, condition preserved."),
    ("POS-FIBRE-01", True, ["SEC-02-2-C-008"],
     "İstenilen nihai kalınlığa bağlı olarak çelik lifli püskürtme beton uygulaması iki fazda "
     "yapılır; ilk faz 50 mm'lik katmandır.",
     [], "Steel-fibre application."),
    ("POS-FLASH-01", True, ["SEC-02-2-R025"],
     "Flashcrete is not considered an active support and is normally followed by a systematically "
     "applied initial shotcrete lining.",
     [], "Flashcrete claim; contains 'is not', which the negation handler must not mis-scope."),
    ("POS-ENV-01", True, ["SEC-02-2-P0-005"],
     "Dış çevresel etki sınıfları gereksinimlerine göre püskürtme betonda belirlenen çimento "
     "miktarı, durabilite nedeniyle 350 kg/m³'ün altında kalmamalıdır.",
     [], "The environmental floor, shotcrete scope named."),
    ("POS-EXC-01", True, ["SEC-02-2-P0-004"],
     "Şev kaplama ve geçici iksa gibi özel durumlarda İdare onayı ile bu miktarlar "
     "azaltılabilmektedir.",
     [], "The reduction clause; states no figure of its own."),

    # ---------- admissibility ----------
    ("NEG-ADM-01", False, ["SEC-02-2-R003"],
     "Genel sınırlama olarak maksimum çimento miktarı 360 kg/m³ olarak belirtilmiştir.",
     ["CLAIM_SUPERSEDED"], "A claim superseded by the P0 decomposition."),
    ("NEG-ADM-02", False, ["SEC-02-2-R019"],
     "Çelik lifli püskürtme beton uygulaması genellikle iki fazda yapılır.",
     ["CLAIM_SUPERSEDED"],
     "SEC-02-2-R019 was PARTIALLY_SUPPORTED and is superseded by SEC-02-2-C-008."),
    ("NEG-ADM-03", False, ["SEC-02-2-R011"],
     "Kat sayısı ve kalınlıkları kullanılan sisteme ve donatı tipine bağlı olarak değişmektedir.",
     ["CLAIM_UNSUPPORTED"], "An unsupported generator framing claim."),
    ("NEG-ADM-04", False, ["SEC-02-2-C-999"],
     "Püskürtme betonda minimum çimento dozajı 300 kg/m³'tür.",
     ["CLAIM_NOT_ALLOWLISTED"], "An unknown claim id."),
    ("NEG-ADM-05", False, ["SEC-02-2-DENY-COMP-SYN-001-COMPOUND"],
     "Yüksek dayanımlı beton dışında maksimum çimento miktarı 360 kg/m³ olarak belirtilse de, "
     "püskürtme beton spesifikasyonlarında minimum 350/400 kg/m³ öngörülmüştür.",
     ["FORBIDDEN_SYNTHESIS"],
     "Citing the denylisted compound by id AND writing it. Both layers must fire."),
    ("NEG-ADM-06", False, ["SEC-02-2-DENY-NUM-150MM"],
     "Bir defada uygulanacak maksimum kalınlık 150 mm'dir.",
     ["DERIVED_VALUE_AS_SOURCE_STATED"], "Citing the denylisted 150 mm representation by id."),

    # ---------- citation / provenance ----------
    ("NEG-CIT-01", False, ["SEC-02-2-C-001"],
     "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
     ["MISSING_SOURCE_KEY"], "No citation key supplied for the claim."),
    ("NEG-CIT-02", False, ["SEC-02-2-C-001"],
     "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
     ["MISSING_SOURCE_KEY"],
     "A citation key that belongs to a different claim: the sentence would render with a "
     "footnote pointing at a source that does not say it."),

    # ---------- combined failures ----------
    ("NEG-MIX-01", False, ["SEC-02-2-P0-002", "SEC-02-2-C-003"],
     "Maksimum çimento miktarı 360 kg/m³'tür. Bir defada uygulanacak maksimum kalınlık "
     "150 mm'dir.",
     ["UNQUALIFIED_SCOPE", "DERIVED_VALUE_AS_SOURCE_STATED"],
     "Two independent defects in one unit; both must be reported, not just the first."),
    ("NEG-MIX-02", False, ["SEC-02-2-P0-002", "SEC-02-2-P0-001", "SEC-02-2-C-003"],
     "Genel betonda maksimum 360 kg/m³ iken yaş sistemde minimum 400 kg/m³ gerekir. Tek seferde "
     "150 mm uygulanabilir.",
     ["FORBIDDEN_SYNTHESIS", "DERIVED_VALUE_AS_SOURCE_STATED"],
     "Forbidden juxtaposition plus a derived attribution."),
]


def build_fixtures(allowlist: list[dict]) -> list[dict]:
    """Materialise the fixture table, resolving citation keys from the allowlist itself.

    Citation keys are looked up rather than hardcoded so that a fixture cannot drift out of
    agreement with the claim it cites. NEG-CIT-01 and NEG-CIT-02 are the deliberate exceptions:
    one supplies none, the other supplies a key belonging to a different claim.
    """
    keys = {row["claim_id"]: row["source_keys"] for row in allowlist}
    rows: list[dict] = []
    for case_id, expected_valid, claim_ids, text, codes, note in FIXTURES:
        if case_id == "NEG-CIT-01":
            citation_keys: dict[str, list[str]] = {}
        elif case_id == "NEG-CIT-02":
            citation_keys = {"SEC-02-2-C-001": keys["SEC-02-2-P0-007"][:1]}
        else:
            citation_keys = {cid: keys.get(cid, []) for cid in claim_ids if cid in keys}
        rows.append({
            "case_id": case_id, "section_id": SECTION_ID,
            "polarity": "positive" if expected_valid else "negative",
            "expected_valid": expected_valid,
            "expected_failure_codes": sorted(codes),
            "candidate_claim_ids": claim_ids,
            "candidate_text_units": [text],
            "citation_keys": citation_keys,
            "language": "en" if re.search(r"\b(the|is|and|shotcrete|thickness|although|however|"
                                          r"whereas)\b", text.lower()) and
                                not re.search(r"[çğıöşü]", text.lower()) else "tr",
            "tests": note, "synthetic": True,
            "contract_version": CONTRACT_VERSION, "fixture_version": RESOLUTION_VERSION,
        })
    return rows


# ================================================================ 7. readiness

def assess_final_readiness(topics: list[dict], parent_bundle: dict, allowlist: list[dict],
                           denylist: list[dict], fixture_result: dict,
                           qualifier_rules: list[MandatoryQualifierRule],
                           synthesis_rules: list[ForbiddenSynthesisRule],
                           derived_rules: list[DerivedNumericRule],
                           pairs: list[ClaimPairConstraint],
                           integrity: dict) -> dict[str, Any]:
    """Recompute SEC-02-2 readiness now that the composition layer exists.

    The previous phase held the section at READY_WITH_LIMITATIONS for one stated reason: CF-P0-001
    and SYN-001 were constraints nothing could enforce. That reason is what this function tests -
    not whether rules were written, but whether they are demonstrably enforced by a deterministic
    validator against a regression suite containing the historical defects themselves.
    """
    blocking: list[str] = []
    non_enforceable: list[str] = []
    resolved: list[str] = []

    covered = [t for t in topics
               if t["coverage_status"] in ("COMPLETE", "COMPLETE_WITH_QUALIFIER")]
    if len(covered) != len(REQUIRED_TOPICS):
        blocking.append(
            f"required topics no longer covered after composition constraints: "
            f"{[t['topic'] for t in topics if t not in covered]}")

    parent = parent_bundle["readiness_assessment"]
    for question_id, status in parent["p0_status"].items():
        if status != "RESOLVED":
            blocking.append(f"P0 regression: {question_id} is {status}")

    allowed_ids = {row["claim_id"] for row in allowlist}
    denied_ids = {row["claim_id"] for row in denylist}
    overlap = allowed_ids & denied_ids
    if overlap:
        blocking.append(f"allowlist and denylist are not disjoint: {sorted(overlap)}")

    unsafe = [row["claim_id"] for row in allowlist if not row["composition_safe"]]
    if unsafe:
        blocking.append(f"allowlisted claims that are not composition-safe: {unsafe}")

    missing_keys = [row["claim_id"] for row in allowlist if not row["source_keys"]]
    if missing_keys:
        blocking.append(f"allowlisted claims with unresolved provenance: {missing_keys}")

    # Enforcement is judged by the regression suite, not by the existence of a rule object.
    if fixture_result["false_accepts"]:
        blocking.append(f"validator accepts unsafe compositions: "
                        f"{fixture_result['false_accepts']}")
    if fixture_result["false_rejects"]:
        blocking.append(f"validator rejects safe compositions: "
                        f"{fixture_result['false_rejects']}")
    if fixture_result["code_mismatches"]:
        blocking.append(f"validator fails cases for the wrong reason: "
                        f"{fixture_result['code_mismatches']}")

    def historical_defect_caught(case_ids: list[str]) -> bool:
        rows = {row["case_id"]: row for row in fixture_result["rows"]}
        return all(case_id in rows and rows[case_id]["outcome"] == "PASS"
                   and not rows[case_id]["actual_valid"] for case_id in case_ids)

    cf_cases = ["NEG-360-01", "NEG-360-03", "NEG-360-05", "NEG-360-06"]
    syn_cases = ["NEG-SYN-01", "NEG-SYN-02", "NEG-SYN-05", "NEG-SYN-08", "NEG-SYN-11"]
    derived_cases = ["NEG-150MM-01", "NEG-150MM-02", "NEG-150MM-03"]

    if qualifier_rules and historical_defect_caught(cf_cases):
        resolved.append("CF-P0-001 - enforced by MQ-001 and pair constraints PC-001..PC-004, "
                        "PC-006; unqualified and misattributed forms are rejected")
    else:
        non_enforceable.append("CF-P0-001 - the qualifier rule does not demonstrably reject the "
                               "unqualified and misattributed forms")
    if synthesis_rules and historical_defect_caught(syn_cases):
        resolved.append("SYN-001 - enforced by FS-001 pattern rules plus the same-sentence "
                        "prohibition, which catches constructions no pattern lists")
    else:
        non_enforceable.append("SYN-001 - the forbidden-synthesis rule does not demonstrably "
                               "reject the historical compound and its paraphrases")
    if derived_rules and historical_defect_caught(derived_cases):
        resolved.append("15 cm / 150 mm guard - enforced by DN-001, with the source-stated "
                        "clay-zone 150 mm correctly exempted")
    else:
        non_enforceable.append("15 cm / 150 mm guard - the derived-numeric rule does not "
                               "demonstrably reject source attribution of the conversion")

    if not integrity["all_unchanged"]:
        blocking.append(f"frozen integrity failed: {integrity['changed']}")

    non_deterministic = [p.constraint_id for p in pairs if p.manual_review_required]
    if non_deterministic:
        non_enforceable.append(
            f"pair constraints requiring manual review rather than deterministic decision: "
            f"{non_deterministic}")

    if blocking:
        readiness = "NOT_READY"
    elif non_enforceable:
        readiness = "READY_WITH_LIMITATIONS"
    else:
        readiness = "READY_FOR_DRAFT"

    return {
        "section_id": SECTION_ID, "readiness": readiness,
        "blocking_reasons": blocking,
        "remaining_non_enforceable_limitations": non_enforceable,
        "resolved_composition_limitations": resolved,
        "required_topics_total": len(REQUIRED_TOPICS),
        "required_topics_covered": len(covered),
        "p0_status": parent["p0_status"],
        "composition_safe_allowlist": len(allowlist),
        "composition_denylist": len(denylist),
        "fixture_total": fixture_result["total"],
        "fixture_passed": fixture_result["passed"],
        "false_accepts": len(fixture_result["false_accepts"]),
        "false_rejects": len(fixture_result["false_rejects"]),
        "drafting_authorized": DRAFTING_AUTHORIZED,
        "drafting_enabled": DRAFTING_ENABLED,
        "assessed_at": now(),
    }


# ================================================================ 8. integrity

def verify_frozen_integrity() -> dict[str, Any]:
    """Baseline is the closure phase's manifest plus its own outputs and implementation."""
    closure_manifest = json.loads(
        (MANIFESTS / "sec_02_2_draft_readiness_closure_v1.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    for entry in closure_manifest["frozen_integrity"]["checks"]:
        path = ROOT / entry["path"]
        actual = sha_file(path) if path.exists() else None
        expected = entry["expected_sha256"] or entry["actual_sha256"]
        checks.append({"name": entry["name"], "path": entry["path"],
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "closure_v1"})
    checks.append({"name": "SEC-02-2 Draft Readiness Closure v1 (implementation)",
                   "path": closure_manifest["implementation"],
                   "expected_sha256": closure_manifest["implementation_sha"],
                   "actual_sha256": sha_file(ROOT / closure_manifest["implementation"]),
                   "unchanged": sha_file(ROOT / closure_manifest["implementation"])
                   == closure_manifest["implementation_sha"], "baseline": "closure_v1"})
    checks.append({"name": "SEC-02-2 draft readiness acceptance contract",
                   "path": closure_manifest["acceptance_contract"],
                   "expected_sha256": closure_manifest["acceptance_contract_sha256"],
                   "actual_sha256": sha_file(ROOT / closure_manifest["acceptance_contract"]),
                   "unchanged": sha_file(ROOT / closure_manifest["acceptance_contract"])
                   == closure_manifest["acceptance_contract_sha256"], "baseline": "closure_v1"})
    for relative, expected in sorted(closure_manifest["artifact_shas"].items()):
        path = CLOSURE / relative
        actual = sha_file(path) if path.exists() else None
        checks.append({"name": f"closure v1 artifact {relative}",
                       "path": str(path.relative_to(ROOT)),
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "closure_v1"})
    for name, relative, baseline in (
            ("source registry v1 (must be untouched)", "data/book/source_registry_v1.jsonl",
             SOURCE_REGISTRY_BASELINE),
            ("p0 source registry (must be untouched)",
             "data/book/p0_resolution/evidence/p0_source_registry_v1.jsonl", P0_REGISTRY_BASELINE),
            ("closure source registry (must be untouched)",
             "data/book/sec_02_2_readiness_closure/evidence/closure_source_registry_v1.jsonl",
             CLOSURE_REGISTRY_BASELINE),
            ("corpus chunks", "data/chunks/chunks.jsonl", CORPUS_BASELINE),
            ("production generation audit log", "data/production/generation_audit_v1.jsonl",
             AUDIT_LOG_BASELINE)):
        path = ROOT / relative
        checks.append({"name": name, "path": relative, "expected_sha256": baseline,
                       "actual_sha256": sha_file(path),
                       "unchanged": sha_file(path) == baseline,
                       "baseline": "limitation_resolution_v1_precondition"})
    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {"checks": checks, "changed": changed, "all_unchanged": not changed,
            "check_count": len(checks)}


def qdrant_points(url: str = QDRANT_URL) -> int | None:
    try:
        import urllib.request
        with urllib.request.urlopen(
                f"{url}/collections/tunnelbook_dense_v1", timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))["result"]["points_count"]
    except Exception:
        return None


SOURCE_REGISTRY_BASELINE = sha_file(BOOK / "source_registry_v1.jsonl")
P0_REGISTRY_BASELINE = sha_file(P0 / "evidence" / "p0_source_registry_v1.jsonl")
CLOSURE_REGISTRY_BASELINE = sha_file(CLOSURE / "evidence" / "closure_source_registry_v1.jsonl")
CORPUS_BASELINE = sha_file(ROOT / "data/chunks/chunks.jsonl")
AUDIT_LOG_BASELINE = sha_file(ROOT / "data/production/generation_audit_v1.jsonl")


# ================================================================ 9. runner

def main() -> int:
    points_before = qdrant_points()

    closure_allowlist = read_jsonl(CLOSURE / "claims" / "draft_claim_allowlist_v1.jsonl")
    closure_denylist = read_jsonl(CLOSURE / "claims" / "draft_claim_denylist_v1.jsonl")
    closure_topics = json.loads(
        (CLOSURE / "audits" / "required_topic_coverage_v1.json").read_text(encoding="utf-8"))
    closure_bundle = json.loads(
        (CLOSURE / "bundle" / "SEC-02-2.json").read_text(encoding="utf-8"))

    scopes = build_claim_scopes(closure_allowlist)
    qualifier_rules = build_qualifier_rules()
    synthesis_rules = build_forbidden_synthesis_rules()
    derived_rules = build_derived_numeric_rules()
    pairs = build_pair_constraints()

    contract = build_composition_contract(scopes, qualifier_rules, synthesis_rules,
                                          derived_rules, pairs)
    safe_allowlist = build_composition_safe_allowlist(
        closure_allowlist, scopes, qualifier_rules, synthesis_rules, derived_rules, pairs)
    composition_denylist = build_composition_denylist(
        closure_denylist, qualifier_rules, synthesis_rules, derived_rules)

    write_json(OUT_CONTRACTS / "sec_02_2_claim_composition_contract_v1.json", contract)
    write_jsonl(OUT_CLAIMS / "composition_safe_allowlist_v1.jsonl",
                [asdict(c) for c in safe_allowlist])
    write_jsonl(OUT_CLAIMS / "composition_denylist_v1.jsonl", composition_denylist)
    write_jsonl(OUT_CLAIMS / "claim_pair_constraints_v1.jsonl", [asdict(p) for p in pairs])

    validator = load_validator()
    loaded = validator.load_contract()
    fixtures = build_fixtures(closure_allowlist)
    write_jsonl(FIXTURES_PATH, fixtures)
    fixture_result = validator.run_fixtures(fixtures, loaded)
    write_json(OUT_AUDITS / "composition_regression_v1.json", fixture_result)

    topics = recompute_topic_coverage(closure_topics, safe_allowlist)
    write_json(OUT_AUDITS / "required_topic_coverage_after_constraints_v1.json", topics)

    consistency = carry_manifest_consistency()
    write_json(OUT_AUDITS / "p0_manifest_consistency_carried_v1.json", consistency)

    integrity = verify_frozen_integrity()
    verdict = assess_final_readiness(topics, closure_bundle, [asdict(c) for c in safe_allowlist],
                                     composition_denylist, fixture_result, qualifier_rules,
                                     synthesis_rules, derived_rules, pairs, integrity)
    points_after = qdrant_points()

    bundle = {
        "section_id": SECTION_ID,
        "parent_readiness_bundle_sha": closure_bundle["bundle_sha"],
        "composition_contract_version": CONTRACT_VERSION,
        "composition_validator_version": VALIDATOR_VERSION,
        "allowlist_sha": sha_file(OUT_CLAIMS / "composition_safe_allowlist_v1.jsonl"),
        "denylist_sha": sha_file(OUT_CLAIMS / "composition_denylist_v1.jsonl"),
        "pair_constraints_sha": sha_file(OUT_CLAIMS / "claim_pair_constraints_v1.jsonl"),
        "contract_sha": sha_file(OUT_CONTRACTS / "sec_02_2_claim_composition_contract_v1.json"),
        "qualifier_rules": [asdict(r) for r in qualifier_rules],
        "forbidden_synthesis_rules": [asdict(r) for r in synthesis_rules],
        "derived_numeric_rules": [asdict(r) for r in derived_rules],
        "claim_pair_constraints": [asdict(p) for p in pairs],
        "remaining_limitations": verdict["remaining_non_enforceable_limitations"],
        "resolved_limitations": verdict["resolved_composition_limitations"],
        "final_readiness": verdict["readiness"],
        "drafting_authorized": DRAFTING_AUTHORIZED,
        "drafting_enabled": DRAFTING_ENABLED,
        "created_at": now(), "resolution_version": RESOLUTION_VERSION,
    }
    bundle["bundle_sha"] = sha_text(json.dumps(bundle, ensure_ascii=False, sort_keys=True))
    write_json(OUT_BUNDLE / "sec_02_2_drafting_safety_bundle_v1.json", bundle)

    def emit(tests_result: dict) -> dict:
        built = build_manifest(contract, safe_allowlist, composition_denylist, pairs,
                               qualifier_rules, synthesis_rules, derived_rules, fixtures,
                               fixture_result, topics, verdict, integrity, consistency,
                               points_before, points_after, tests_result, bundle,
                               closure_allowlist)
        write_json(MANIFEST_PATH, built)
        write_report(built, contract, safe_allowlist, composition_denylist, pairs,
                     qualifier_rules, synthesis_rules, derived_rules, fixtures, fixture_result,
                     topics, verdict, integrity, consistency, closure_allowlist)
        return built

    emit({"suites": [], "status": "pending", "returncode": None, "tests_run": 0, "tail": []})
    tests = run_tests()
    manifest = emit(tests)

    print_summary(manifest, verdict, fixture_result, qualifier_rules, synthesis_rules,
                  derived_rules, pairs, safe_allowlist, composition_denylist)
    return 0 if manifest["status"] == "closed_go" else 1


def recompute_topic_coverage(closure_topics: list[dict],
                             safe_allowlist: list[CompositionSafeClaim]) -> list[dict]:
    """Composition safety must not silently remove a required topic's support.

    A claim bound by a mandatory qualifier still covers its topic - it is constrained, not
    removed. Only a claim that failed composition safety outright would drop out, and the check
    exists so that if one ever does, the topic goes INCOMPLETE rather than the loss going
    unnoticed.
    """
    safe_by_id = {c.claim_id: c for c in safe_allowlist}
    rows: list[dict] = []
    for topic in closure_topics:
        surviving = [cid for cid in topic["citation_ready_claim_ids"]
                     if cid in safe_by_id and safe_by_id[cid].composition_safe]
        core = [cid for cid in topic["required_core_claim_ids"] if cid in surviving]
        dropped = sorted(set(topic["citation_ready_claim_ids"]) - set(surviving))
        constrained = sorted(cid for cid in surviving
                             if safe_by_id[cid].mandatory_qualifier_rule_ids
                             or safe_by_id[cid].derived_numeric_rule_ids)
        if not core:
            status, blocking = "INCOMPLETE", (
                f"composition constraints removed every REQUIRED_CORE claim for "
                f"'{topic['topic']}'")
        elif constrained:
            status, blocking = "COMPLETE_WITH_QUALIFIER", None
        else:
            status, blocking = topic["coverage_status"], None
        rows.append({
            "topic": topic["topic"], "required": True,
            "coverage_status_before": topic["coverage_status"], "coverage_status": status,
            "citation_ready_claim_ids": topic["citation_ready_claim_ids"],
            "composition_safe_claim_ids": surviving,
            "required_core_claim_ids": core,
            "dropped_by_composition": dropped,
            "constrained_claim_ids": constrained,
            "blocking_reason": blocking, "audit_method": AUDIT_METHOD})
    return rows


def carry_manifest_consistency() -> dict:
    """Rule 56: carry the closure phase's retrieval-gap audit forward, unaltered."""
    carried = json.loads(
        (CLOSURE / "audits" / "p0_manifest_consistency_v1.json").read_text(encoding="utf-8"))
    return {
        "carried_from": PARENT_VERSION,
        "carried_at": now(),
        "canonical_value": carried["canonical_value"],
        "canonical_statement": carried["canonical_statement"],
        "canonical_clause_ids": carried["canonical_clause_ids"],
        "source_of_truth": carried["source_of_truth"],
        "inconsistency_found": carried["inconsistency_found"],
        "impact_on_sec_02_2": carried["impact_on_sec_02_2"],
        "historical_artifacts_modified": False,
        "note": "Carried verbatim from the closure phase's audit. This phase performed no "
                "retrieval, opened no new gap question and altered no historical artifact; the "
                "canonical count is restated here so a consumer of this bundle does not have to "
                "reach back two phases for it.",
    }


def run_tests() -> dict[str, Any]:
    suites = ["tests/test_sec_02_2_limitation_resolution_v1.py",
              "tests/test_sec_02_2_claim_composition_validator_v1.py"]
    present = [s for s in suites if (ROOT / s).exists()]
    if not present:
        return {"suites": suites, "status": "missing", "returncode": None, "tests_run": 0,
                "tail": []}
    modules = [s.replace("/", ".").removesuffix(".py") for s in present]
    result = subprocess.run([sys.executable, "-m", "unittest", *modules, "-v"],
                            cwd=ROOT, capture_output=True, text=True)
    output = result.stderr or result.stdout
    tail = output.strip().splitlines()[-8:]
    run_match = re.search(r"Ran (\d+) tests?", output)
    return {"suites": present, "executed_by": "unittest", "returncode": result.returncode,
            "status": "passed" if result.returncode == 0 else "failed",
            "tests_run": int(run_match.group(1)) if run_match else 0, "tail": tail}


def build_manifest(contract, safe_allowlist, denylist, pairs, qualifier_rules, synthesis_rules,
                   derived_rules, fixtures, fixture_result, topics, verdict, integrity,
                   consistency, points_before, points_after, tests, bundle,
                   closure_allowlist) -> dict[str, Any]:
    artifact_shas = {str(p.relative_to(OUT)): sha_file(p)
                     for p in sorted(OUT.rglob("*")) if p.is_file()}
    allowed_ids = {c.claim_id for c in safe_allowlist}
    denied_ids = {r["claim_id"] for r in denylist}
    go = {
        "composition_contract_authored": bool(contract["claim_scopes"]),
        "every_allowlisted_claim_scoped": len(contract["claim_scopes"]) == len(closure_allowlist),
        "cf_p0_001_has_blocking_qualifier_rule": any(
            r.severity == "BLOCKING" and r.origin_limitation == "CF-P0-001"
            for r in qualifier_rules),
        "syn_001_has_blocking_rule": any(
            r.severity == "BLOCKING" and r.synthesis_id == "SYN-001" for r in synthesis_rules),
        "derived_numeric_rule_present": any(
            r.severity == "BLOCKING" and r.derived_value == "150" for r in derived_rules),
        "pair_constraints_deterministic": all(not p.manual_review_required for p in pairs),
        "allowlist_denylist_disjoint": not (allowed_ids & denied_ids),
        "every_allowlisted_claim_composition_safe": all(
            c.composition_safe for c in safe_allowlist),
        "every_allowlisted_claim_has_source_keys": all(c.source_keys for c in safe_allowlist),
        "fixture_minimum_met": len(fixtures) >= 60,
        "zero_false_accepts": not fixture_result["false_accepts"],
        "zero_false_rejects": not fixture_result["false_rejects"],
        "zero_code_mismatches": not fixture_result["code_mismatches"],
        "required_topics_still_covered": verdict["required_topics_covered"] == len(
            REQUIRED_TOPICS),
        "manifest_consistency_carried": consistency["canonical_value"] is not None,
        "historical_artifacts_unmodified": not consistency["historical_artifacts_modified"],
        "frozen_integrity_holds": integrity["all_unchanged"],
        "generation_calls_zero": GENERATION_CALLS == 0,
        "retrieval_calls_zero": RETRIEVAL_CALLS == 0,
        "qdrant_unchanged": points_before == points_after,
        "qdrant_writes_zero": True,
        "drafting_disabled": DRAFTING_ENABLED is False,
        "drafting_not_authorized": DRAFTING_AUTHORIZED is False,
        "no_prose_written": not (BOOK / "manuscript").exists(),
        "tests_pass": tests["status"] == "passed",
    }
    return {
        "version": RESOLUTION_VERSION, "parent_version": PARENT_VERSION,
        "composition_contract_version": CONTRACT_VERSION,
        "composition_validator_version": VALIDATOR_VERSION,
        "section_id": SECTION_ID, "created_at": now(), "source_policy": SOURCE_POLICY,
        "audit_method": AUDIT_METHOD,
        "drafting_enabled": DRAFTING_ENABLED, "drafting_authorized": DRAFTING_AUTHORIZED,
        "implementation": "scripts/45_sec_02_2_limitation_resolution_v1.py",
        "implementation_sha": sha_file(Path(__file__)),
        "validator_implementation": "scripts/46_sec_02_2_claim_composition_validator_v1.py",
        "validator_implementation_sha": sha_file(
            ROOT / "scripts/46_sec_02_2_claim_composition_validator_v1.py"),
        "input_closure_manifest_sha": sha_file(
            MANIFESTS / "sec_02_2_draft_readiness_closure_v1.json"),
        "parent_readiness_bundle_sha": bundle["parent_readiness_bundle_sha"],
        "final_readiness": verdict["readiness"],
        "readiness_blocking_reasons": verdict["blocking_reasons"],
        "resolved_composition_limitations": verdict["resolved_composition_limitations"],
        "remaining_non_enforceable_limitations": verdict[
            "remaining_non_enforceable_limitations"],
        "required_topics": list(REQUIRED_TOPICS),
        "required_topics_covered": verdict["required_topics_covered"],
        "required_topic_status": {t["topic"]: t["coverage_status"] for t in topics},
        "input_allowlist_claims": len(closure_allowlist),
        "composition_safe_allowlist_claims": len(safe_allowlist),
        "composition_denylist_claims": len(denylist),
        "claim_scopes": len(contract["claim_scopes"]),
        "restricted_figures": len(contract["restricted_figures"]),
        "mandatory_qualifier_rules": len(qualifier_rules),
        "forbidden_synthesis_rules": len(synthesis_rules),
        "forbidden_synthesis_patterns": sum(len(r.forbidden_patterns) for r in synthesis_rules),
        "derived_numeric_rules": len(derived_rules),
        "claim_pair_constraints": len(pairs),
        "fixture_count": len(fixtures),
        "positive_fixtures": fixture_result["positive"],
        "negative_fixtures": fixture_result["negative"],
        "fixtures_passed": fixture_result["passed"],
        "false_accepts": len(fixture_result["false_accepts"]),
        "false_rejects": len(fixture_result["false_rejects"]),
        "code_mismatches": len(fixture_result["code_mismatches"]),
        "failure_codes": list(load_validator().FAILURE_CODES),
        "generation_calls": GENERATION_CALLS, "retrieval_calls": RETRIEVAL_CALLS,
        "p0_manifest_consistency_carried": consistency,
        "canonical_retrieval_gap_count": consistency["canonical_value"],
        "frozen_integrity": integrity,
        "qdrant_expected": QDRANT_EXPECTED_POINTS,
        "qdrant_points_before": points_before, "qdrant_points_after": points_after,
        "qdrant_writes": 0, "qdrant_reachable": points_before is not None,
        "qdrant_note": (
            f"Observed {points_before} before and {points_after} after."
            if points_before is not None else
            "Qdrant was not reachable at http://localhost:6333 during this run, so the point "
            "count could not be observed and is reported as unknown rather than as the expected "
            "5992. The phase performs no retrieval, opens no Qdrant client and holds no write "
            "path."),
        "safety_bundle_sha": bundle["bundle_sha"],
        "artifact_shas": artifact_shas,
        "fixtures_path": str(FIXTURES_PATH.relative_to(ROOT)),
        "fixtures_sha": sha_file(FIXTURES_PATH),
        "tests": tests, "go_conditions": go,
        "status": "closed_go" if all(go.values()) else "closed_no_go",
        "next_phase": next_phase(verdict),
    }


def next_phase(verdict: dict) -> dict[str, Any]:
    readiness = verdict["readiness"]
    if readiness == "READY_FOR_DRAFT":
        return {"route": "SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING CONTRACT V1",
                "sections": [SECTION_ID],
                "why": "the evidence layer was closed by the previous phase and the composition "
                       "layer is now enforced by a deterministic validator that rejects every "
                       "historical defect and accepts every safe arrangement. The drafting "
                       "contract inherits a bounded claim set plus the rules governing how those "
                       "claims may be combined.",
                "carry_forward": verdict["resolved_composition_limitations"],
                "note": "drafting_authorized is still false; authorisation is that phase's call"}
    if readiness == "READY_WITH_LIMITATIONS":
        return {"route": "smallest remediation for the remaining non-enforceable limitations",
                "sections": [SECTION_ID],
                "why": "evidence is sufficient but at least one composition limitation is not "
                       "deterministically enforceable.",
                "carry_forward": verdict["remaining_non_enforceable_limitations"]}
    return {"route": "route by blocking class - evidence, numeric or claim removal",
            "sections": [SECTION_ID],
            "why": "a composition constraint exposed an underlying defect.",
            "carry_forward": verdict["blocking_reasons"]}


# ================================================================ 10. report

def write_report(manifest, contract, safe_allowlist, denylist, pairs, qualifier_rules,
                 synthesis_rules, derived_rules, fixtures, fixture_result, topics, verdict,
                 integrity, consistency, closure_allowlist) -> None:
    lines: list[str] = []

    def add(text: str = "") -> None:
        lines.append(text)

    add("# SEC-02-2 Limitation Resolution v1")
    add()
    add("## Executive Decision")
    add()
    add(f"**SEC-02-2 LIMITATION RESOLUTION V1 - "
        f"{'CLOSED / GO' if manifest['status'] == 'closed_go' else 'CLOSED / NO-GO'}**")
    add()
    add(f"**SEC-02-2: {verdict['readiness']}**")
    add()
    add(f"The two composition limitations that held this section short of READY_FOR_DRAFT are now "
        f"enforced by a deterministic validator: {len(qualifier_rules)} mandatory qualifier "
        f"rule, {len(synthesis_rules)} forbidden-synthesis rule with "
        f"{manifest['forbidden_synthesis_patterns']} patterns, {len(derived_rules)} derived-numeric "
        f"rule and {len(pairs)} claim-pair constraints, scored against "
        f"{manifest['fixture_count']} regression fixtures "
        f"({manifest['positive_fixtures']} positive / {manifest['negative_fixtures']} negative) "
        f"with {manifest['false_accepts']} false accepts and {manifest['false_rejects']} false "
        f"rejects. Generation calls: {GENERATION_CALLS}. Retrieval calls: {RETRIEVAL_CALLS}. "
        f"`drafting_authorized` is **false**.")
    add()
    add("## Why Composition Needed Its Own Gate")
    add()
    add("SYN-001 is the whole argument, so it is worth being precise about what it was.")
    add()
    add("Its two components were individually well-supported. The 360 kg/m³ maximum is stated "
        "verbatim in Tablo-308-23-b, in an authority-A source, with a verified span and a "
        "resolvable citation key. The 350 and 400 kg/m³ minimums are stated verbatim in the "
        "shotcrete specification, likewise verified and citable. Every claim-level check the "
        "pipeline can run - support status, span verification, numeric source-statedness, "
        "provenance, citation readiness - passes on both.")
    add()
    add("The defect was the word *between* them. `belirtilse de` - \"although it is stated\" - "
        "asserts that the shotcrete minimums stand in a concessive relation to the general "
        "maximum, that one is an exception to or a tension with the other. No source says that. "
        "The figures govern different materials by different design routes in different chapters.")
    add()
    add("A pipeline that validates claims one at a time cannot see this, because **at the level "
        "of a single claim there is nothing wrong**. That is why the previous phase declined "
        "READY_FOR_DRAFT despite every enumerated condition passing: the allowlist and denylist "
        "bound which claims may be used, and neither can express \"these two may not share a "
        "sentence\". This phase builds the layer that can.")
    add()
    add("The core principle it encodes:")
    add()
    add("> " + contract["core_principle"])
    add()
    add("## Frozen Inputs")
    add()
    add("| Input | State |")
    add("|---|---|")
    add(f"| Closure v1 manifest | `{manifest['input_closure_manifest_sha'][:16]}` |")
    add(f"| Parent readiness bundle | `{manifest['parent_readiness_bundle_sha'][:16]}` |")
    add(f"| Input evidence allowlist | {len(closure_allowlist)} claims |")
    add(f"| Frozen integrity checks | {integrity['check_count']}, "
        f"{'all unchanged' if integrity['all_unchanged'] else 'CHANGED: ' + str(integrity['changed'])} |")
    add("| Source registries | untouched (book, P0, closure) |")
    if manifest["qdrant_reachable"]:
        add(f"| Qdrant | {manifest['qdrant_points_before']} before / "
            f"{manifest['qdrant_points_after']} after / 0 writes |")
    else:
        add("| Qdrant | **not reachable during this run** - count unobserved; 0 writes |")
    add(f"| Generation calls | {GENERATION_CALLS} |")
    add(f"| Retrieval calls | {RETRIEVAL_CALLS} |")
    add()
    if not manifest["qdrant_reachable"]:
        add(f"**On Qdrant.** {manifest['qdrant_note']} The expected count is "
            f"{QDRANT_EXPECTED_POINTS}; it is reported as unknown rather than restated from a "
            f"previous manifest, because a number nobody measured in this run is not an "
            f"observation.")
        add()
    add("## CF-P0-001")
    add()
    add("The apparent conflict and why it is not one:")
    add()
    add("| | 360 kg/m³ | 350 / 400 kg/m³ |")
    add("|---|---|---|")
    add("| Material | general concrete | shotcrete (dry / wet system) |")
    add("| Requirement direction | **maximum** | **minimum** |")
    add("| Document | Tablo-308-23-b, exposure-class design table | shotcrete specification |")
    add("| Design route | designed by exposure class | shotcrete mix specification |")
    add()
    add("Four independent axes of difference. Drop any one of them and the numbers look like they "
        "contradict - a 400 minimum above a 360 maximum. Keep all four and there is no tension at "
        "all, because the two figures never apply to the same concrete.")
    add()
    add("That is exactly why the qualifier is **mandatory rather than merely useful**: the bare "
        "figure is not incomplete, it is misleading in a way a reader cannot detect.")
    add()
    add("## Scope Binding")
    add()
    add(f"All {len(contract['claim_scopes'])} allowlisted claims carry an authored scope, each "
        f"with the evidence that establishes it. Scope is never inferred where the source does "
        f"not establish it.")
    add()
    add("| Claim | Material | System | Requirement | Document |")
    add("|---|---|---|---|---|")
    for scope in contract["claim_scopes"]:
        add(f"| `{scope['claim_id']}` | {scope['material_scope']} | {scope['system_scope']} | "
            f"{', '.join(scope['requirement_scope'])} | {scope['document_scope']} |")
    add()
    add("The three restricted figures - the only ones whose composition is constrained:")
    add()
    add("| Figure | Claim | Material | Direction |")
    add("|---|---|---|---|")
    for figure in contract["restricted_figures"]:
        add(f"| {figure['label']} | `{figure['claim_id']}` | {figure['material_scope']} | "
            f"{figure['requirement_scope']} |")
    add()
    add("Figure detection is **unit-scoped throughout**. Matching on bare values would make the "
        "`400` in \"4 to 16 inches (100 to 400 mm)\" collide with the 400 kg/m³ wet-system cement "
        "minimum - a different quantity in a different material sharing a numeral. Fixture "
        "`POS-LINING-01` pins that.")
    add()
    add("## Mandatory Qualifiers")
    add()
    for rule in qualifier_rules:
        add(f"**{rule.rule_id}** - `{rule.claim_id}` - severity **{rule.severity}** "
            f"(from {rule.origin_limitation})")
        add()
        add(f"- Required scope: `{rule.required_scope}`")
        add(f"- Required qualifier: *{rule.required_qualifier}*")
        add(f"- Forbidden bare form: *\"{rule.forbidden_unqualified_form}\"* → "
            f"`UNQUALIFIED_SCOPE`")
        add(f"- Forbidden scopes: {rule.forbidden_scopes} → `AMBIGUOUS_SCOPE`")
        add(f"- {rule.misattribution_note}")
        add()
    add("**The negation trap.** The qualifier this rule mandates ends "
        "\"...GENEL beton özelliklerine ilişkindir; **püskürtme beton şartnamesi değildir**\". A "
        "wrong-scope check that simply looked for shotcrete markers near the 360 figure would "
        "reject the one form the contract requires. Negation handling is therefore load-bearing, "
        "not a nicety: a marker followed by a denial within 60 characters is not an assertion of "
        "that scope. Fixture `POS-360-03` is the qualifier verbatim and must pass.")
    add()
    add("## SYN-001")
    add()
    for rule in synthesis_rules:
        add(f"**{rule.rule_id}** - severity **{rule.severity}** - safe representation: "
            f"`{rule.safe_representation}`")
        add()
        add(f"Forbidden relationship: {rule.forbidden_relationship}")
        add()
        add(f"Components (each individually supported and separately draftable): "
            f"{', '.join('`' + c + '`' for c in rule.component_claim_ids)}")
        add()
    add("## Forbidden Synthesis Rules")
    add()
    add("Two layers, and the second is the one that matters.")
    add()
    add(f"**Layer 1 - {manifest['forbidden_synthesis_patterns']} patterns** matching the "
        f"historical wording and its variants:")
    add()
    for rule in synthesis_rules:
        for intent in rule.pattern_intent:
            add(f"- {intent}")
    add()
    add("**Layer 2 - the same-sentence prohibition.** The 360 figure may not share a sentence "
        "with 350 or 400 under *any* phrasing. No connector analysis, no pattern.")
    add()
    add("This layering is deliberate. A pattern list is only ever as good as the imagination of "
        "whoever wrote it; a drafter who picks a conjunction nobody enumerated walks straight "
        "through it. Fixture `NEG-SYN-05` makes the point - it joins the two figures with "
        "`iken`, which appears in no connector list in this contract, and it is caught anyway "
        "because the juxtaposition itself is the defect.")
    add()
    add("A semicolon is deliberately **not** treated as a sentence boundary. "
        "\"X is 360; Y is 400\" is one sentence inviting the comparison the rule exists to "
        "prevent, and splitting on `;` would let it through on punctuation (`NEG-SYN-03`).")
    add()
    add("What remains permitted, and must: separate sentences, each scoped, no connector "
        "(`POS-PARA-01`), or separate list items (`POS-PARA-02`). And 350 vs 400 in one sentence "
        "**passes** (`POS-350-400-01`), because that comparison is the source's own - it states "
        "both minimums in one span, distinguished by system. The contract does not forbid figures "
        "from meeting; it forbids asserting relations no source states.")
    add()
    add("## Derived Numeric Rule")
    add()
    for rule in derived_rules:
        add(f"**{rule.rule_id}** - `{rule.claim_id}` - severity **{rule.severity}** - policy "
            f"`{rule.drafting_policy}`")
        add()
        add(f"- Source-stated: **{rule.source_value} {rule.source_unit}**")
        add(f"- Derived only: **{rule.derived_value} {rule.derived_unit}** "
            f"(derived={rule.derived}, source_stated={rule.source_stated})")
        add(f"- Fires in context: {rule.context_markers}")
        add(f"- Stands down in context: {rule.exempt_context_markers}")
        add()
        add(f"**The exemption is the difficulty.** {rule.exemption_reason}")
        add()
    add(f"{contract['derived_numeric_policy_note']}")
    add()
    add("## Composition-Safe Allowlist")
    add()
    add(f"{len(safe_allowlist)} claims, from {len(closure_allowlist)} on the evidence allowlist. "
        f"No claim was dropped: a claim bound by a mandatory qualifier is **constrained, not "
        f"removed**. It remains draftable; it simply cannot be drafted bare.")
    add()
    add("| Claim | Topic | Scope | Rules | Same-sentence restrictions |")
    add("|---|---|---|---|---|")
    for claim in safe_allowlist:
        rules = (claim.mandatory_qualifier_rule_ids + claim.forbidden_synthesis_rule_ids
                 + claim.derived_numeric_rule_ids)
        add(f"| `{claim.claim_id}` | {claim.topic or '-'} | {claim.scope['material_scope']} | "
            f"{', '.join(rules) or '-'} | "
            f"{'yes' if 'FORBIDDEN_SYNTHESIS' in claim.forbidden_relationships else 'no'} |")
    add()
    add("## Composition Denylist")
    add()
    add(f"{len(denylist)} entries, in two layers.")
    add()
    layers: dict[str, int] = {}
    for row in denylist:
        layers[row.get("deny_layer", "evidence")] = layers.get(row.get("deny_layer",
                                                                       "evidence"), 0) + 1
    add("| Layer | Entries |")
    add("|---|---|")
    for layer, count in sorted(layers.items()):
        add(f"| {layer} | {count} |")
    add()
    add("The evidence layer is carried forward from the closure phase unaltered, so a consumer "
        "reading only this file is still stopped from citing a superseded, partial or "
        "unsupported claim. The composition layer adds the forms that are unsafe *as written* "
        "even though their figures are true and cited:")
    add()
    for row in denylist:
        if row.get("deny_layer") != "composition":
            continue
        add(f"- `{row['claim_id']}` - *\"{row['canonical_claim']}\"* - enforced by "
            f"{row.get('enforced_by', [])}")
    add()
    add("`SEC-02-2-DENY-COMP-360-AS-SHOTCRETE` deserves particular note: its citation would "
        "resolve perfectly and the sentence would still be false. That is the case that shows "
        "why scope binding cannot be left to citation checking.")
    add()
    add("## Claim Pair Constraints")
    add()
    add("| Constraint | Pair | Policy | Same sentence | Same paragraph |")
    add("|---|---|---|---|---|")
    for pair in pairs:
        add(f"| `{pair.constraint_id}` | `{pair.left_claim_id}` / `{pair.right_claim_id}` | "
            f"{pair.relationship_policy} | "
            f"{'**forbidden**' if not pair.allowed_same_sentence else 'allowed'} | "
            f"{'allowed' if pair.allowed_same_paragraph else 'forbidden'} |")
    add()
    add("Every constraint is decided deterministically; none requires manual review, which is "
        "what lets the pair layer be enforced by a validator rather than by a reviewer.")
    add()
    add("## Composition Validator")
    add()
    add(f"`scripts/46_sec_02_2_claim_composition_validator_v1.py` "
        f"(`{manifest['validator_implementation_sha'][:16]}`)")
    add()
    add("It validates claim use, claim combination, scope qualifiers, derived numbers and "
        "forbidden synthesis. It is **not** a prose quality validator and does not attempt to be.")
    add()
    add("Three commitments:")
    add()
    add("- **Deterministic.** Every decision is a regex, a set membership or a sentence-window "
        "comparison. No LLM judge.")
    add("- **Fail closed.** No auto-rewrite, no auto-repair, no qualifier injection. An invalid "
        "unit is rejected with required actions. A unit whose scope cannot be determined fails "
        "as `AMBIGUOUS_SCOPE` rather than passing on the benefit of the doubt.")
    add("- **Scoped to SEC-02-2.** It knows about three figures in two materials and says so. "
        "Widening it is a later decision, not a side effect of this one.")
    add()
    add(f"Failure codes: {', '.join('`' + c + '`' for c in manifest['failure_codes'])}")
    add()
    add("## Regression Fixtures")
    add()
    add(f"`{manifest['fixtures_path']}` - **{manifest['fixture_count']} cases** "
        f"({manifest['positive_fixtures']} positive, {manifest['negative_fixtures']} negative), "
        f"all synthetic. Several are deliberately wrong. None is SEC-02-2 prose.")
    add()
    add("| Metric | Value |")
    add("|---|---|")
    add(f"| Cases | {manifest['fixture_count']} |")
    add(f"| Passed | {manifest['fixtures_passed']} |")
    add(f"| **False accepts** | **{manifest['false_accepts']}** |")
    add(f"| **False rejects** | **{manifest['false_rejects']}** |")
    add(f"| Code mismatches | {manifest['code_mismatches']} |")
    add()
    add("A false accept is a case the contract says must fail that the validator passed - the "
        "dangerous direction. A code mismatch is tracked separately because a case that fails "
        "for the wrong reason is a rule that is not doing the job it claims to.")
    add()
    add("The cases that carry the most weight:")
    add()
    add("| Case | What it pins |")
    add("|---|---|")
    for case_id in ("POS-360-03", "NEG-360-01", "NEG-360-03", "NEG-SYN-01", "NEG-SYN-05",
                    "NEG-SYN-11", "POS-350-400-01", "POS-PARA-01", "NEG-150MM-02",
                    "POS-150MM-EXEMPT-01", "POS-LINING-01", "POS-MESH-02"):
        row = next((f for f in fixtures if f["case_id"] == case_id), None)
        if row:
            add(f"| `{case_id}` ({'PASS' if row['expected_valid'] else 'FAIL'}) | "
                f"{row['tests']} |")
    add()
    add("## Required Topic Coverage After Constraints")
    add()
    add("| Topic | Before | After | Core claims | Constrained | Dropped |")
    add("|---|---|---|---|---|---|")
    for row in topics:
        add(f"| `{row['topic']}` | {row['coverage_status_before']} | "
            f"**{row['coverage_status']}** | {len(row['required_core_claim_ids'])} | "
            f"{len(row['constrained_claim_ids'])} | {len(row['dropped_by_composition'])} |")
    add()
    add("Composition safety removed support from no required topic. That check exists because "
        "the failure mode it guards against is silent: a constraint that quietly eliminated a "
        "topic's only core claim would leave the section looking safer and actually be "
        "incomplete.")
    add()
    add("## Remaining Limitations")
    add()
    if verdict["resolved_composition_limitations"]:
        add("Resolved by this phase:")
        add()
        for item in verdict["resolved_composition_limitations"]:
            add(f"- {item}")
        add()
    if verdict["remaining_non_enforceable_limitations"]:
        add("Still not deterministically enforceable:")
        add()
        for item in verdict["remaining_non_enforceable_limitations"]:
            add(f"- {item}")
        add()
    else:
        add("None. Every composition limitation carried into this phase is now enforced by a "
            "rule with a regression case proving it fires.")
        add()
    add("Carried forward unchanged, and out of scope here: the OPTIONAL limitations the closure "
        "phase registered (LIM-004's six unsupported Q-02-2-04 framing clauses, LIM-005's "
        "single-item provenance for the C25/30 sentence, LIM-006's flashcrete false-positive "
        "flag, LIM-007's mine-specific mesh scope). None is a composition constraint and none "
        "blocks drafting; LIM-007's scope qualifier travels on `SEC-02-2-C-017` as a claim field.")
    add()
    add("## Frozen Integrity")
    add()
    add(f"{integrity['check_count']} checks, "
        f"{'all unchanged' if integrity['all_unchanged'] else 'CHANGED: ' + str(integrity['changed'])}.")
    add()
    add("Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded "
        "Generator v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual "
        "audit, remediation v1, every P0 Evidence Gap Resolution v1 artifact, every SEC-02-2 "
        "Draft Readiness Closure v1 artifact, all three source registries, the corpus chunks and "
        "the production audit log are byte-identical.")
    add()
    add("### Manifest Consistency (carried)")
    add()
    add(f"{consistency['canonical_statement']} Source of truth: "
        f"`{consistency['source_of_truth']}`. Impact on SEC-02-2: "
        f"{consistency['impact_on_sec_02_2']}")
    add()
    add(f"{consistency['note']}")
    add()
    add("## Tests")
    add()
    tests = manifest["tests"]
    add(f"{', '.join('`' + s + '`' for s in tests.get('suites', []))} - {tests['status']}, "
        f"{tests['tests_run']} tests.")
    add()
    add("The suites assert the contract and the enforcement, not the wording: that every "
        "allowlisted claim has an authored scope, that CF-P0-001 and SYN-001 carry BLOCKING "
        "rules, that the qualified 360 form passes and the bare and misattributed forms fail, "
        "that the historical SYN-001 compound is rejected, that separate scoped claims are "
        "accepted, that 150 mm cannot be attributed to a source while the clay-zone 150 mm still "
        "passes, that 350 vs 400 remains comparable, that superseded / partial / unknown claims "
        "are rejected, that allowlist and denylist are disjoint, that all three required topics "
        "survive, and that no manuscript artifact exists.")
    add()
    add("## Final Readiness")
    add()
    add(f"**SEC-02-2: {verdict['readiness']}**")
    add()
    add("| Gate | Result |")
    add("|---|---|")
    for gate, result in sorted(manifest["go_conditions"].items()):
        add(f"| {gate.replace('_', ' ')} | {'PASS' if result else 'FAIL'} |")
    add()
    if verdict["blocking_reasons"]:
        add("Blocking reasons:")
        add()
        for reason in verdict["blocking_reasons"]:
            add(f"- {reason}")
        add()
    add(f"`drafting_enabled` is `false` and `drafting_authorized` is `false`. This phase does not "
        f"authorise drafting under any outcome - that decision belongs to the Section Drafting "
        f"Contract, which is the consumer of the bundle this phase produced, not its author.")
    add()
    add("## Next Phase")
    add()
    route = manifest["next_phase"]
    add(f"**{route['route']}**")
    add()
    add(f"Why: {route['why']}")
    add()
    add(f"Sections in scope: {', '.join(route['sections'])}.")
    add()
    if route.get("note"):
        add(f"Note: {route['note']}.")
        add()
    if route["carry_forward"]:
        add("Carried forward:")
        add()
        for item in route["carry_forward"]:
            add(f"- {item}")
        add()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def print_summary(manifest, verdict, fixture_result, qualifier_rules, synthesis_rules,
                  derived_rules, pairs, safe_allowlist, denylist) -> None:
    print()
    print(f"SEC-02-2 LIMITATION RESOLUTION V1 - "
          f"{'CLOSED / GO' if manifest['status'] == 'closed_go' else 'CLOSED / NO-GO'}")
    print()
    print(f"Section:                     {SECTION_ID}")
    print(f"Final readiness:             {verdict['readiness']}")
    print(f"Required topics:             {verdict['required_topics_covered']} / "
          f"{len(REQUIRED_TOPICS)}")
    print(f"Input allowlist:             {manifest['input_allowlist_claims']}")
    print(f"Composition-safe allowlist:  {len(safe_allowlist)}")
    print(f"Composition denylist:        {len(denylist)}")
    print(f"Mandatory qualifier rules:   {len(qualifier_rules)}")
    print(f"Forbidden synthesis rules:   {len(synthesis_rules)} "
          f"({manifest['forbidden_synthesis_patterns']} patterns)")
    print(f"Pair constraints:            {len(pairs)}")
    print(f"Derived numeric rules:       {len(derived_rules)}")
    print(f"Regression fixtures:         {fixture_result['passed']}/{fixture_result['total']} PASS")
    print(f"False accepts:               {len(fixture_result['false_accepts'])}")
    print(f"False rejects:               {len(fixture_result['false_rejects'])}")
    print(f"Code mismatches:             {len(fixture_result['code_mismatches'])}")
    print(f"Generation calls:            {GENERATION_CALLS}")
    print(f"Retrieval calls:             {RETRIEVAL_CALLS}")
    print(f"Qdrant:                      {manifest['qdrant_points_before']} / "
          f"{manifest['qdrant_points_after']} / {manifest['qdrant_writes']} writes")
    print(f"Drafting authorized:         {str(DRAFTING_AUTHORIZED).lower()}")
    print(f"Tests:                       {manifest['tests']['status']} "
          f"({manifest['tests']['tests_run']})")
    print(f"Next:                        {manifest['next_phase']['route']}")
    print()


if __name__ == "__main__":
    raise SystemExit(main())
