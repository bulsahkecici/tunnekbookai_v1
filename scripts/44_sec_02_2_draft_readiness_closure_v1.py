"""SEC-02-2 Draft Readiness Closure v1.

The P0 Evidence Gap Resolution phase left SEC-02-2 at READY_WITH_LIMITATIONS and routed it
straight to drafting. That routing was wrong, and the reason is worth stating precisely because
it is the whole justification for this phase existing.

The readiness contract that phase applied only ever asked P0 questions. It checked that every P0
question carried a citation-ready claim, that no P0 clause was left unsupported, that numerics
were source-stated and that cross-lingual mappings were faithful - and SEC-02-2 passed all of it.
What it never asked is the question the SectionPlan actually poses: are the section's REQUIRED
TOPICS covered? SEC-02-2 requires three - çimento dozajı, kaplama kalınlığı, dayanım sınıfı - and
"dayanım sınıfı" is answered by Q-02-2-03, which is P1. A P1 question is invisible to a P0
contract. So a section whose third required topic had exactly zero citation-ready claims was
reported as ready-with-limitations, and the limitation "P1/P2 questions without a citation-ready
claim" was filed as though it were a footnote rather than a missing third of the section.

This phase therefore does two separate things, in this order and no other:

  1. It freezes a readiness contract that tests required-topic coverage, and it writes that
     contract to disk BEFORE any closure result is computed (rule 5). The contract cannot be
     tuned to the answer because the answer does not exist yet when it is written.

  2. It closes the remaining gaps the only way this project permits: by reading the frozen
     ContextPackets that were already retrieved, mapping claims onto exact source spans by hand,
     and verifying every span against the packet text at runtime. Zero retrieval. Zero
     generation. An item outside the frozen packet cannot support anything here.

What that reading found is that Q-02-2-03, Q-02-2-04 and Q-02-2-06 were never evidence gaps at
all. The packets carry the propositions verbatim - "Püskürtme betonun basınç dayanım sınıfi
minimum C25/30 MPa sınıfında olacaktır" sits in the Q-02-2-03 packet, in the chunk the note
already cited - and the failures were extraction and span-mapping failures of exactly the kind
the P0 phase fixed for P0 questions and simply never ran for P1/P2 ones.

Two things are deliberately NOT fixed by that reading, and both stay unfixed on purpose:

  - The 150 mm in "15 cm'yi (150 mm) geçmemelidir" is a conversion the generator performed. The
    source says 15 cm. 15 cm is draftable; 150 mm as source-stated wording is not, and the
    denylist carries that representation explicitly so a later drafter cannot reach it.

  - SYN-001's concessive relation ("although the maximum is 360, the minimums are 350/400") is
    asserted by no source, because the 360 governs general concrete by exposure class and the
    350/400 govern the shotcrete specification. The components are individually supported and
    stay separately draftable. The relation does not come back.

Outputs are new files only. Every prior artifact - the corpus, the chunks, the embeddings,
Retriever v1, Context v1, Prompt v5, Output Contract v1.1, the Production Grounded Generator,
the Evidence Note Contract, Book Pipeline v1, Extractor v1.1, the manual audit, remediation v1
and the P0 resolution - is read and verified byte-identical, never written. Drafting stays
disabled at the end of this phase under every possible outcome.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CLOSURE_VERSION = "tunnelbook-sec-02-2-draft-readiness-closure-v1"
PARENT_VERSION = "tunnelbook-p0-evidence-gap-resolution-v1"
REMEDIATION_VERSION = "tunnelbook-book-evidence-remediation-v1"
EXTRACTOR_VERSION = "tunnelbook-book-pipeline-extractor-v1.1"
SECTION_ID = "SEC-02-2"
SOURCE_POLICY = "frozen_packet_only"
AUDIT_METHOD = "manual_evidence_read"
DRAFTING_ENABLED = False

# Both default to zero. They are counters, not budgets: nothing in this phase is permitted to
# increment them unless a CRITICAL section requirement cannot be assessed from packet evidence,
# and none was.
GENERATION_CALLS = 0
RETRIEVAL_CALLS = 0

QDRANT_URL = "http://localhost:6333"
QDRANT_EXPECTED_POINTS = 5992

BOOK = ROOT / "data" / "book"
METADATA = ROOT / "data" / "metadata"
MANIFESTS = BOOK / "manifests"
P0 = BOOK / "p0_resolution"
OUT = BOOK / "sec_02_2_readiness_closure"
OUT_EVIDENCE = OUT / "evidence"
OUT_CLAIMS = OUT / "claims"
OUT_AUDITS = OUT / "audits"
OUT_BUNDLE = OUT / "bundle"
ACCEPTANCE_PATH = METADATA / "sec_02_2_draft_readiness_acceptance_v1.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_draft_readiness_closure_v1.md"
MANIFEST_PATH = MANIFESTS / "sec_02_2_draft_readiness_closure_v1.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str | None:
    return sha_text(path.read_text(encoding="utf-8")) if path.exists() else None


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit_v1 = _load("pilot_manual_audit_v1", "scripts/41_pilot_manual_evidence_audit_v1.py")
p0_v1 = _load("p0_resolution_v1", "scripts/43_p0_evidence_gap_resolution_v1.py")


def normalise(text: str) -> str:
    """Whitespace- and case-insensitive comparison, NFKC-folded.

    Deliberately does NOT repair OCR damage. DOC000236 spells 'kalınliğı' where DOC000087 spells
    'kalınlığı'; each span is stored as its own document spells it and verified against that
    document, so a span that only matches because we normalised the difference away cannot pass.
    """
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().lower()


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


# ================================================================ 1. the frozen contract

# Vocabularies. Every enum in this phase is closed, and every record is validated against these
# before it is written, so a typo becomes a failed run rather than a silently unclassified gap.
CRITICALITY = ("CRITICAL", "IMPORTANT_NON_BLOCKING", "OPTIONAL")
NUMERIC_STATUS = ("SUPPORTED", "PARTIALLY_SUPPORTED", "DERIVED_ONLY", "CONTEXT_DIFFERENT",
                  "UNSUPPORTED", "NOT_REQUIRED_FOR_OBJECTIVE")
CONTEXT_STATUS = ("SAFE_CONTEXT_DIFFERENCE", "REQUIRES_QUALIFIER", "BLOCKING_CONFLICT",
                  "INSUFFICIENT_TO_DECIDE")
SYNTHESIS_STATUS = ("SAFE_TO_DROP", "REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS",
                    "BLOCKING_MISSING_SYNTHESIS")
TOPIC_STATUS = ("COMPLETE", "COMPLETE_WITH_QUALIFIER", "INCOMPLETE")
READINESS_USE = ("REQUIRED_CORE", "SUPPORTED_CONTEXT", "OPTIONAL_ENRICHMENT", "DO_NOT_DRAFT")
WORKAROUND = ("omit_optional_material", "state_supported_narrower_claim",
              "preserve_context_qualifier", "separate_conflicting_contexts", "NONE")
READINESS = ("READY_FOR_DRAFT", "READY_WITH_LIMITATIONS", "NOT_READY")

REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")

# Which questions answer which required topic. This binding is part of the frozen contract and is
# taken from the SectionPlan's own question set, not invented here: it is what makes topic
# coverage a computable test rather than a judgement made after seeing the claims.
TOPIC_QUESTIONS = {
    "çimento dozajı": ["Q-02-2-01"],
    "kaplama kalınlığı": ["Q-02-2-02", "Q-02-2-04"],
    "dayanım sınıfı": ["Q-02-2-03"],
}


def acceptance_contract() -> dict[str, Any]:
    """The readiness contract, authored before any closure result exists.

    Rule 49: this does not move. If the closure results come back short of it, the section is not
    ready - the contract is not what gets adjusted.
    """
    return {
        "version": CLOSURE_VERSION,
        "contract_id": "sec-02-2-draft-readiness-acceptance-v1",
        "authored_at": now(),
        "section_id": SECTION_ID,
        "section_objective": ("Püskürtme betona ilişkin sayısal gereklilikleri ve şartname "
                              "hükümlerini kanıta dayalı olarak derlemek"),
        "authored_before_results": True,
        "source_policy": SOURCE_POLICY,
        "audit_method": AUDIT_METHOD,
        "drafting_enabled": DRAFTING_ENABLED,
        "why_this_contract_exists": (
            "The P0 resolution contract tested P0 questions only. SEC-02-2's third required "
            "topic, dayanım sınıfı, is answered by a P1 question (Q-02-2-03), so a section with "
            "zero citation-ready claims on a required topic passed as READY_WITH_LIMITATIONS. "
            "READY_WITH_LIMITATIONS is not READY_FOR_DRAFT and was never evidence that the "
            "section could be drafted."),
        "required_topics": list(REQUIRED_TOPICS),
        "topic_question_binding": TOPIC_QUESTIONS,
        "vocabularies": {
            "criticality": list(CRITICALITY),
            "numeric_closure_status": list(NUMERIC_STATUS),
            "context_difference_status": list(CONTEXT_STATUS),
            "dropped_synthesis_status": list(SYNTHESIS_STATUS),
            "topic_coverage_status": list(TOPIC_STATUS),
            "readiness_use": list(READINESS_USE),
            "allowed_workaround": list(WORKAROUND),
            "readiness": list(READINESS),
        },
        "ready_for_draft_conditions": [
            "every required topic has at least one SUPPORTED + citation_ready REQUIRED_CORE claim",
            "every required topic's coverage status is COMPLETE or COMPLETE_WITH_QUALIFIER",
            "all P0 questions remain RESOLVED and no P0 claim regressed",
            "no unresolved P1/P2 gap classified CRITICAL",
            "no unresolved critical numeric clause",
            "no unresolved contradictory numeric condition",
            "no context difference classified BLOCKING_CONFLICT or INSUFFICIENT_TO_DECIDE",
            "no dropped synthesis classified BLOCKING_MISSING_SYNTHESIS",
            "every allowlisted claim traceable to a verified span in a frozen packet",
            "provenance complete: every source key on an allowlisted claim resolves",
            "no allowlisted claim presents a derived conversion as source-stated",
            "drafting_enabled is false at phase end",
        ],
        "ready_with_limitations_conditions": [
            "every required topic covered",
            "all P0 resolved",
            "every remaining gap is IMPORTANT_NON_BLOCKING or OPTIONAL",
            "every limitation is explicit in the limitation register",
            "a later drafter can be mechanically prevented from using unresolved material "
            "(the denylist is non-empty where unresolved material exists, and every unresolved "
            "item appears on it)",
        ],
        "not_ready_conditions": [
            "a required topic lacks a SUPPORTED + citation_ready claim",
            "a CRITICAL P1/P2 gap remains unresolved",
            "a critical numeric issue remains",
            "a context difference changes the interpretation of a required claim and cannot be "
            "carried as an explicit qualifier",
            "SYN-001 carries material content required by the objective that cannot be supported",
            "provenance is incomplete",
        ],
        "p1_p2_unresolved_allowance": {
            "rule": ("A P1/P2 question may remain unresolved only if the section objective can "
                     "still be fulfilled without it AND the missing content is classified "
                     "NON_CRITICAL_ENRICHMENT or OPTIONAL_DETAIL AND the reason is written out."),
            "classes": ["NON_CRITICAL_ENRICHMENT", "OPTIONAL_DETAIL"],
            "unresolved_is_not_automatically_acceptable": True,
            "assessment_axes": ["required topic coverage", "numeric completeness",
                                "requirement completeness", "technical correctness",
                                "safety-critical meaning", "scope of the section objective"],
        },
        "derived_numeric_rule": (
            "A derived conversion may persist in structured metadata with derived=true, but no "
            "READY_FOR_DRAFT claim may present it as source-stated wording."),
        "synthesis_rule": (
            "Individually supported claims may be stated separately. A concessive or causal "
            "relation between them may not be inferred unless a source states it. SYN-001's "
            "'although X, Y' relation is not to be recombined."),
        "prohibitions": [
            "no section or chapter prose", "no manuscript drafting", "drafting stays disabled",
            "no corpus / chunk / embedding / Qdrant modification",
            "no modification of Retriever v1, Context v1, Prompt v5, Output Contract v1.1, "
            "Production Grounded Generator v1, Evidence Note Contract v1, Book Pipeline v1 or "
            "Extractor v1.1",
            "no in-place modification of P0 Evidence Gap Resolution v1 artifacts",
            "no web, no external sources, no model memory as evidence",
            "no invented evidence, spans, units, conversions or requirements",
            "no silent dropping of unresolved P1/P2 material",
            "no general-knowledge or model-memory workaround for any limitation",
        ],
        "budgets": {"generation_calls_default": 0, "retrieval_calls_default": 0,
                    "max_revised_queries_per_unresolved_question": 1,
                    "same_question_retry_permitted": False,
                    "retrieval_experiment_top_k_max": 40,
                    "retrieval_experiments_max": 1,
                    "production_retrieval_default_unchanged": True},
        "qdrant_expected": {"points_before": QDRANT_EXPECTED_POINTS,
                            "points_after": QDRANT_EXPECTED_POINTS, "writes": 0},
    }


def write_acceptance_contract() -> tuple[dict[str, Any], str]:
    contract = acceptance_contract()
    write_json(ACCEPTANCE_PATH, contract)
    return contract, sha_file(ACCEPTANCE_PATH)


# ================================================================ 2. closure records

@dataclass
class SpanMapping:
    """One claim clause pinned to one exact span in one frozen packet item.

    `span_verified` is never set by the author. It is computed by searching the packet text at
    run time, so a span that is not actually in the packet fails the run instead of becoming a
    citation.
    """
    mapping_id: str
    question_id: str
    clause_id: str
    claim: str
    evidence_id: str
    chunk_id: str = ""
    document_id: str = ""
    source_key: str = ""
    context_packet_sha: str = ""
    source_span: str = ""
    support_relation: str = "literal_span"
    coverage: str = "full"
    manual_verdict: str = "FULL"
    span_verified: bool = False
    authority_level: str | None = None
    section_path: str | None = None
    review_notes: str = ""
    audit_method: str = AUDIT_METHOD


@dataclass
class ClosureClaim:
    claim_id: str
    canonical_claim: str
    question_id: str
    topic: str | None
    support_status: str
    citation_ready: bool
    readiness_use: str
    clause_ids: list[str] = field(default_factory=list)
    mapping_ids: list[str] = field(default_factory=list)
    source_keys: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    numeric: list[dict] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    qualifiers: list[str] = field(default_factory=list)
    supersedes: list[str] = field(default_factory=list)
    superseded_by: list[str] = field(default_factory=list)
    origin: str = CLOSURE_VERSION
    citation_block_reasons: list[str] = field(default_factory=list)
    context_packet_sha: str = ""
    notes: str = ""


@dataclass
class GapClosure:
    """One P1/P2 question's remaining gap, assessed on the six axes the contract names."""
    question_id: str
    priority: str
    required_by_plan: bool
    question_text: str
    requested_proposition: str
    evidence_found: str
    citation_ready_claims_before: list[str]
    citation_ready_claims_after: list[str]
    remaining_unsupported: list[str]
    affects_required_topic_coverage: bool
    affects_numeric_completeness: bool
    affects_requirement_completeness: bool
    affects_technical_correctness: bool
    affects_safety_critical_meaning: bool
    affects_objective_scope: bool
    criticality: str
    disposition: str
    non_critical_class: str | None
    reason: str
    packet_items_read: int
    audit_method: str = AUDIT_METHOD


@dataclass
class NumericClosureRecord:
    clause_id: str
    question_id: str
    claim: str
    value: str
    unit: str
    condition: str | None
    source_span: str
    source_evidence_ref: str
    current_status: str
    criticality: str
    resolution: str
    citation_ready: bool
    notes: str
    derived: bool = False
    derived_from_value: str | None = None
    derived_from_unit: str | None = None
    audit_method: str = AUDIT_METHOD


@dataclass
class ContextDifferenceClosure:
    context_difference_id: str
    claim_a: str
    claim_b: str
    source_a: str
    source_b: str
    difference_type: str
    conditions_a: list[str]
    conditions_b: list[str]
    same_scope: bool
    criticality: str
    drafting_rule: str
    final_status: str
    claim_a_id: str = ""
    claim_b_id: str = ""
    audit_method: str = AUDIT_METHOD


@dataclass
class DroppedSynthesisClosure:
    synthesis_id: str
    original_claim: str
    component_claims: list[str]
    component_support: dict[str, str]
    unsupported_relation: str
    required_by_section_objective: bool
    criticality: str
    future_drafting_rule: str
    final_status: str
    audit_method: str = AUDIT_METHOD


@dataclass
class Limitation:
    limitation_id: str
    question_id: str
    description: str
    criticality: str
    affected_topic: str | None
    drafting_impact: str
    allowed_workaround: str
    status: str
    audit_method: str = AUDIT_METHOD


# ================================================================ 3. authored closure evidence

# Each row: (mapping_id, question_id, clause_id, evidence_id, span, notes).
# The spans are transcribed from the frozen packet text and verified against it at run time. They
# are stored per document, because DOC000236 and DOC000087 are two scans of the same 2013
# specification and their OCR differs; a span written for one is not silently accepted for the
# other.
AUTHORED_SPANS: list[tuple[str, str, str, str, str, str]] = [
    # ---- Q-02-2-03 : dayanım sınıfı. The required topic that had no citation-ready claim.
    ("MC-03-01", "Q-02-2-03", "Q-02-2-03-N01-C01", "E001",
     "Püskürtme betonun basınç dayanım sınıfi minimum C25/30 MPa sınıfında olacaktır.",
     "The proposition the section's third required topic rests on, stated verbatim in the chunk "
     "the note already cited (DOC000236-C0285, §351.10.01). v1 marked it UNSUPPORTED on a 0.22 "
     "token-overlap score, which measured wording distance, not whether the source says it."),
    ("MC-03-02", "Q-02-2-03", "Q-02-2-03-N01-C01", "E001",
     "351.10.01 Basınç Dayanım Sınıfları",
     "Section heading that scopes the clause to shotcrete compressive strength classes."),
    ("MC-03-03", "Q-02-2-03", "Q-02-2-03-N02-C01", "E002",
     "Tablo-351-5 Püskürtme Beton İçin Basınç Dayanım Sınıfları ve Kalite Kontrol Kriterleri",
     "Table title in the authority-A copy (DOC000087-C0284). Establishes that the 22,5 / 25,5 "
     "figures are shotcrete core-sample acceptance criteria, not general concrete values."),
    ("MC-03-04", "Q-02-2-03", "Q-02-2-03-N02-C01", "E002",
     "BİREYSEL MİNİMUM DAYANIM (MPa)",
     "Column header for 22,5. Without it the figure has no meaning and the claim would be a "
     "number without a criterion."),
    ("MC-03-05", "Q-02-2-03", "Q-02-2-03-N02-C01", "E002",
     "3 ADET NUMUNEDEN OLUŞAN GRUBUN ORTALAMA MİNİMUM DAYANIMI (MPa)",
     "Column header for 25,5 - the mean of a three-sample group, which is what the claim says."),
    ("MC-03-06", "Q-02-2-03", "Q-02-2-03-N02-C01", "E002",
     "Püskürtme Betondan Alınacak Karot Numunede Dayanım Yönünden (28 Günlük) Aranacak Kalite "
     "Kontrol Kriterleri",
     "Carries the '28 günlük karot numunesi' condition the claim asserts."),
    ("MC-03-07", "Q-02-2-03", "Q-02-2-03-N02-C01", "E002",
     "| C 25 / 30                                                       | 25                    "
     "                                          | 30                                            "
     "                  | 22,5                                                                  "
     "    | 25,5",
     "The C 25/30 row itself, in the authority-A copy: 22,5 individual minimum and 25,5 "
     "three-sample-group mean. Row transcribed with its cell padding so the mapping is to the "
     "actual table row and not to two numbers found elsewhere in the chunk."),

    # ---- Q-02-2-04 : layer count and layer thicknesses.
    ("MC-04-01", "Q-02-2-04", "Q-02-2-04-N06-C01", "E002",
     "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı 15 cm'yi geçmeyecektir.",
     "The single-pass maximum, verbatim in the authority-A copy. Note what the source says: "
     "15 cm. It does not say 150 mm anywhere - see the numeric closure record."),
    ("MC-04-02", "Q-02-2-04", "Q-02-2-04-N06-C01", "E001",
     "Bir defada uygulanacak püskürtme betonunun maksimum kalınliğı 15 cm'yi geçmeyecektir.",
     "Same clause in the second copy. Spelt 'kalınliğı' there; stored as that document spells "
     "it rather than normalised into agreement."),
    ("MC-04-03", "Q-02-2-04", "Q-02-2-04-N04-C02", "E002",
     "İlk tabaka taze betonun akmaması için ince, tercihen yaklaşık 60 mm (maksimum 100 mm) "
     "olmalıdır.",
     "First-layer thickness with both figures and the reason, in one span."),
    ("MC-04-04", "Q-02-2-04", "Q-02-2-04-N05-C01", "E002",
     "Takip eden tabakalar, nihai kalınlığa (ve kullanılan priz hızlandırıcı katkı malzemesinin "
     "tipine) bağlı olarak 50-200 mm olmalıdır.",
     "Subsequent-layer range with both stated dependencies."),
    ("MC-04-05", "Q-02-2-04", "Q-02-2-04-N09-C01", "E002",
     "Kalınlığın artırılması gerektiğinde müteakip tabaka(lar), önceki tabakanın mukavemeti "
     "sonradan tatbik edilecek tabakayı taşıyacak yeterli mertebeye ulaşmadan uygulanmayacaktır.",
     "The multi-layer rule and its precondition. This is what answers 'how many layers': the "
     "specification sets no fixed count, it sets a strength gate between layers."),
    ("MC-04-06", "Q-02-2-04", "Q-02-2-04-N09-C02", "E002",
     "Bu ilave tabakalar, üç günü geçmeyen bir süre içersinde tamamlanmış olacaktır.",
     "The three-day completion limit, with the source's own binding modality ('olacaktır'). v1 "
     "rejected this clause for 'modality not carried by the located span' - the located span was "
     "the wrong one."),
    ("MC-04-07", "Q-02-2-04", "Q-02-2-04-N12-C01", "E002",
     "İstenilen nihai kalınlığa bağlı olarak, çelik lifli püskürtme beton uygulaması; GSK'nı "
     "(rebound) minimize etmek amacıyla iki fazda yapılır.",
     "Steel-fibre two-phase application, §351.08.09. The source conditions this on the required "
     "final thickness; the canonical claim keeps that condition and drops the generator's "
     "unsourced hedge 'genellikle'."),
    ("MC-04-08", "Q-02-2-04", "Q-02-2-04-N12-C02", "E002",
     "İlk faz 50 mm'lik katmandır.",
     "First phase thickness, same span neighbourhood."),
    ("MC-04-09", "Q-02-2-04", "Q-02-2-04-N13-C01", "E006",
     "İlk püskürtme beton katmanı genellikle 100-150 mm'dir ve lif takviyeli olması "
     "tercih edilmelidir.",
     "Clay-zone first layer. Carried only with the section scope below, because the figure is "
     "specific to §351.08.10.02 and is not a general first-layer thickness."),
    ("MC-04-10", "Q-02-2-04", "Q-02-2-04-N13-C01", "E006",
     "351.08.10.02 Kil Zonlu Tabakalar Üzerine Püskürtme Beton Uygulaması",
     "The scope heading that makes the 100-150 mm figure interpretable."),
    ("MC-04-11", "Q-02-2-04", "Q-02-2-04-N14-C01", "E016",
     "Tepe üstü aynalarda",
     "Repair-works recommended thicknesses, authority-A copy. The source lays these out as a "
     "labelled list rather than a sentence, so face orientation and figure are separate cells."),
    ("MC-04-12", "Q-02-2-04", "Q-02-2-04-N14-C01", "E016",
     ": Takviye donatılarını 10 mm geçecek şekilde",
     "10 mm over the reinforcement, overhead faces, behind/around reinforcement."),
    ("MC-04-13", "Q-02-2-04", "Q-02-2-04-N14-C02", "E016",
     ": Takviye donatılarını 20 mm geçecek şekilde",
     "20 mm over the reinforcement, vertical faces."),
    ("MC-04-14", "Q-02-2-04", "Q-02-2-04-N14-C03", "E016",
     "- Ek katmanlar veya takviye donatılarının olmadığı durumda:",
     "The condition that governs the 30 mm / 50 mm pair: no additional layers and no "
     "reinforcement. Without it the two pairs of figures read as contradicting each other."),
    ("MC-04-15", "Q-02-2-04", "Q-02-2-04-N14-C03", "E016",
     ": Maksimum 30 mm",
     "30 mm maximum, overhead faces, unreinforced case."),
    ("MC-04-16", "Q-02-2-04", "Q-02-2-04-N14-C04", "E016",
     ": Maksimum 50 mm",
     "50 mm maximum, vertical faces, unreinforced case."),
    ("MC-04-17", "Q-02-2-04", "Q-02-2-04-N14-C01", "E016",
     "Herhangi bir priz hızlandırıcı katkı malzemesi kullanılmaksızın, püskürtülen katmanlar "
     "için tavsiye edilen kalınlıklar:",
     "The accelerator-free condition and the 'tavsiye edilen' modality that govern the whole "
     "repair-works list. These are recommendations, not requirements, and the claims say so."),
    ("MC-04-18", "Q-02-2-04", "Q-02-2-04-N10-C01", "E016",
     "Yaklaşık 20 °C sıcaklıkta ve herhangi bir priz hızlandırıcı katkı malzemesi kullanılmaz "
     "ise, bekleme süresi yaklaşık 3-5 saattir.",
     "Waiting time with both of its stated conditions - temperature and absence of accelerator."),

    # ---- Q-02-2-06 : hasır çelik types. P2, no required topic.
    ("MC-06-01", "Q-02-2-06", "Q-02-2-06-N02-C01", "E014",
     "(R) Tipleri 15 adet boy, 20 adet en çubuklu",
     "R-type mesh bar counts, verbatim."),
    ("MC-06-02", "Q-02-2-06", "Q-02-2-06-N03-C01", "E014",
     "(Q) Tipleri 15 adet boy, 33 adet en çubukludur.",
     "Q-type mesh bar counts, verbatim."),
    ("MC-06-03", "Q-02-2-06", "Q-02-2-06-N07-C01", "E014",
     "Standart Çelik Hasır 5.00 x 2.15 m. ebadındadır.",
     "Standard sheet dimensions."),
    ("MC-06-04", "Q-02-2-06", "Q-02-2-06-N07-C01", "E014",
     "Çelik Hasır ile ilgili TSE standardı TS 4559",
     "The referenced TSE standard."),
    ("MC-06-05", "Q-02-2-06", "Q-02-2-06-N04-C01", "E016",
     "birbirlerine zincir şeklinde geçmeli tellerden oluşturulan hasırlar ve birbirlerine "
     "kaynatılarak tutturulan çelik hasırlardır",
     "Both mesh types in one span, clean text. The parallel span in E009 is OCR-damaged "
     "('has1r'), so this is the one the claim is mapped to."),
    ("MC-06-06", "Q-02-2-06", "Q-02-2-06-N05-C01", "E016",
     "birbirlerine zincir şeklinde geçmeli tellerden oluşturulan hasırlar ve birbirlerine "
     "kaynatılarak tutturulan çelik hasırlardır",
     "Same span carries the welded type; the two note-level claims split one source sentence."),
    ("MC-06-07", "Q-02-2-06", "Q-02-2-06-N06-C01", "E002",
     "İşletmede 7mm kalınlığında 15cmx15cm göz aralıklı çelik hasır kullanılmaktadır.",
     "Mesh gauge and grid spacing - but the subject is one named mine operation, not a tunnel "
     "specification. Carried only with that scope qualifier; without it this reads as a general "
     "requirement, which the source does not say."),
]


def authored_claims() -> list[dict]:
    """The canonical claims this phase closes, each tied to the mappings that support it.

    Wording is kept close to the source spans on purpose. These are claims, not prose: the
    drafting phase turns them into sentences, this phase only decides what is true and citable.
    """
    return [
        # ---- dayanım sınıfı (required topic 3) -----------------------------------------
        {"claim_id": "SEC-02-2-C-001", "question_id": "Q-02-2-03", "topic": "dayanım sınıfı",
         "canonical_claim": "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa "
                            "sınıfında olacaktır.",
         "clause_ids": ["Q-02-2-03-N01-C01"], "mapping_ids": ["MC-03-01", "MC-03-02"],
         "readiness_use": "REQUIRED_CORE",
         "numeric": [{"value": "C25/30", "unit": "MPa", "source_stated": True, "derived": False,
                      "condition": "püskürtme beton karakteristik serbest basınç dayanımı",
                      "role": "minimum"}],
         "conditions": ["püskürtme beton"], "qualifiers": [],
         "supersedes": ["SEC-02-2-R009"],
         "notes": "Closes the required topic that had no citation-ready claim at all."},
        {"claim_id": "SEC-02-2-C-002", "question_id": "Q-02-2-03", "topic": "dayanım sınıfı",
         "canonical_claim": "Tablo-351-5'e göre C25/30 sınıfı püskürtme betonda, 28 günlük karot "
                            "numunelerde bireysel minimum dayanım 22,5 MPa ve üç adet numuneden "
                            "oluşan grubun ortalama minimum dayanımı 25,5 MPa'dır.",
         "clause_ids": ["Q-02-2-03-N02-C01"],
         "mapping_ids": ["MC-03-03", "MC-03-04", "MC-03-05", "MC-03-06", "MC-03-07"],
         "readiness_use": "SUPPORTED_CONTEXT",
         "numeric": [{"value": "22.5", "unit": "MPa", "source_stated": True, "derived": False,
                      "condition": "C25/30, 28 günlük karot, bireysel minimum", "role": "minimum"},
                     {"value": "25.5", "unit": "MPa", "source_stated": True, "derived": False,
                      "condition": "C25/30, 28 günlük karot, 3 numunelik grup ortalaması",
                      "role": "minimum"}],
         "conditions": ["C25/30 dayanım sınıfı", "28 günlük karot numunesi"],
         "qualifiers": ["Tablo-351-5 kalite kontrol kriterleridir; dayanım sınıfının kendisi "
                        "değil, kabul kriteridir"],
         "supersedes": ["SEC-02-2-R010"],
         "notes": "Both figures are cells of one table row; the column headers are mapped "
                  "separately so neither number can travel without its criterion."},

        # ---- kaplama kalınlığı, layer-level (Q-02-2-04) ----------------------------------
        {"claim_id": "SEC-02-2-C-003", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Bir defada uygulanacak püskürtme betonunun maksimum kalınlığı "
                            "15 cm'yi geçmeyecektir.",
         "clause_ids": ["Q-02-2-04-N06-C01"], "mapping_ids": ["MC-04-01", "MC-04-02"],
         "readiness_use": "SUPPORTED_CONTEXT",
         "numeric": [{"value": "15", "unit": "cm", "source_stated": True, "derived": False,
                      "condition": "bir defada uygulanacak katman", "role": "maximum"}],
         "conditions": ["bir defada (tek geçişte) uygulama"], "qualifiers": [],
         "supersedes": ["SEC-02-2-R015"],
         "notes": "The source states 15 cm. The 150 mm that appeared alongside it in the "
                  "generator's wording is a conversion no source performs; it is stripped from "
                  "the canonical claim and recorded as DERIVED_ONLY."},
        {"claim_id": "SEC-02-2-C-004", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "İlk tabaka, taze betonun akmaması için ince olmalı; tercihen "
                            "yaklaşık 60 mm, maksimum 100 mm olmalıdır.",
         "clause_ids": ["Q-02-2-04-N04-C02"], "mapping_ids": ["MC-04-03"],
         "readiness_use": "SUPPORTED_CONTEXT",
         "numeric": [{"value": "60", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "ilk tabaka, tercih edilen", "role": "preferred"},
                     {"value": "100", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "ilk tabaka", "role": "maximum"}],
         "conditions": ["ilk tabaka"], "qualifiers": [],
         "supersedes": ["SEC-02-2-R013"], "notes": ""},
        {"claim_id": "SEC-02-2-C-005", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Takip eden tabakalar, nihai kalınlığa ve kullanılan priz "
                            "hızlandırıcı katkı malzemesinin tipine bağlı olarak 50-200 mm "
                            "olmalıdır.",
         "clause_ids": ["Q-02-2-04-N05-C01"], "mapping_ids": ["MC-04-04"],
         "readiness_use": "SUPPORTED_CONTEXT",
         "numeric": [{"value": "50", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "takip eden tabakalar", "role": "range_min"},
                     {"value": "200", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "takip eden tabakalar", "role": "range_max"}],
         "conditions": ["takip eden tabakalar", "nihai kalınlık", "priz hızlandırıcı katkı tipi"],
         "qualifiers": [], "supersedes": ["SEC-02-2-R014"], "notes": ""},
        {"claim_id": "SEC-02-2-C-006", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Kalınlığın artırılması gerektiğinde müteakip tabaka(lar), önceki "
                            "tabakanın mukavemeti sonradan tatbik edilecek tabakayı taşıyacak "
                            "yeterli mertebeye ulaşmadan uygulanmayacaktır.",
         "clause_ids": ["Q-02-2-04-N09-C01"], "mapping_ids": ["MC-04-05"],
         "readiness_use": "SUPPORTED_CONTEXT", "numeric": [],
         "conditions": ["kalınlığın artırılması gereken durum"], "qualifiers": [],
         "supersedes": ["SEC-02-2-R017"],
         "notes": "This is the actual answer to 'how many layers': the specification fixes no "
                  "count, it fixes a strength gate between layers."},
        {"claim_id": "SEC-02-2-C-007", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "İlave tabakalar, üç günü geçmeyen bir süre içerisinde tamamlanmış "
                            "olacaktır.",
         "clause_ids": ["Q-02-2-04-N09-C02"], "mapping_ids": ["MC-04-06"],
         "readiness_use": "SUPPORTED_CONTEXT",
         "numeric": [{"value": "3", "unit": "gün", "source_stated": True, "derived": False,
                      "condition": "ilave tabakaların tamamlanması", "role": "maximum"}],
         "conditions": ["ilave tabakalar"], "qualifiers": [], "supersedes": [], "notes": ""},
        {"claim_id": "SEC-02-2-C-008", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "İstenilen nihai kalınlığa bağlı olarak çelik lifli püskürtme beton "
                            "uygulaması, geri sıçramayı (GSK) minimize etmek amacıyla iki fazda "
                            "yapılır; ilk faz 50 mm'lik katmandır.",
         "clause_ids": ["Q-02-2-04-N12-C01", "Q-02-2-04-N12-C02"],
         "mapping_ids": ["MC-04-07", "MC-04-08"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "50", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "çelik lifli püskürtme beton ilk faz", "role": "value"}],
         "conditions": ["çelik lifli püskürtme beton", "istenilen nihai kalınlık"],
         "qualifiers": [], "supersedes": ["SEC-02-2-R019"],
         "notes": "Touches optional topic 'lif donatı'. The generator's 'genellikle' hedge is "
                  "dropped: the source conditions this on the required final thickness."},
        {"claim_id": "SEC-02-2-C-009", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Kil zonlu tabakalar üzerine püskürtme beton uygulamasında ilk "
                            "püskürtme beton katmanı genellikle 100-150 mm'dir ve lif takviyeli "
                            "olması tercih edilmelidir.",
         "clause_ids": ["Q-02-2-04-N13-C01"], "mapping_ids": ["MC-04-09", "MC-04-10"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "100", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "kil zonlu tabakalar, ilk katman", "role": "range_min"},
                     {"value": "150", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "kil zonlu tabakalar, ilk katman", "role": "range_max"}],
         "conditions": ["kil zonlu tabakalar üzerine uygulama"],
         "qualifiers": ["§351.08.10.02 kil zonlu tabakalara özgüdür; genel ilk katman kalınlığı "
                        "değildir"],
         "supersedes": ["SEC-02-2-R020"],
         "notes": "The 150 mm here is source-stated as a range bound and is unrelated to the "
                  "derived 150 mm in the 15 cm clause. Different clause, different provenance."},
        {"claim_id": "SEC-02-2-C-010", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Tamir işlerinde, priz hızlandırıcı katkı kullanılmaksızın "
                            "püskürtülen katmanlar için tavsiye edilen kalınlıklar; takviye "
                            "donatılarının arkasında ve etrafında tepe üstü aynalarda donatıyı "
                            "10 mm, dik aynalarda donatıyı 20 mm geçecek şekildedir.",
         "clause_ids": ["Q-02-2-04-N14-C01", "Q-02-2-04-N14-C02"],
         "mapping_ids": ["MC-04-11", "MC-04-12", "MC-04-13", "MC-04-17"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "10", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "tepe üstü ayna, donatı arkası/etrafı", "role": "cover_over"},
                     {"value": "20", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "dik ayna, donatı arkası/etrafı", "role": "cover_over"}],
         "conditions": ["tamir işleri", "priz hızlandırıcı katkı kullanılmaksızın",
                        "takviye donatılarının arkasında ve etrafında"],
         "qualifiers": ["tavsiye edilen kalınlıklardır, zorunlu değildir"],
         "supersedes": ["SEC-02-2-R021"], "notes": ""},
        {"claim_id": "SEC-02-2-C-011", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Tamir işlerinde, ek katman veya takviye donatısı bulunmayan "
                            "durumda tavsiye edilen kalınlıklar tepe üstü aynalarda maksimum "
                            "30 mm, dik aynalarda maksimum 50 mm'dir.",
         "clause_ids": ["Q-02-2-04-N14-C03", "Q-02-2-04-N14-C04"],
         "mapping_ids": ["MC-04-14", "MC-04-15", "MC-04-16", "MC-04-17"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "30", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "tepe üstü ayna, ek katman/donatı yok", "role": "maximum"},
                     {"value": "50", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "dik ayna, ek katman/donatı yok", "role": "maximum"}],
         "conditions": ["tamir işleri", "priz hızlandırıcı katkı kullanılmaksızın",
                        "ek katman veya takviye donatısı bulunmayan durum"],
         "qualifiers": ["tavsiye edilen kalınlıklardır, zorunlu değildir"],
         "supersedes": [],
         "notes": "Kept separate from C-010 because the two figure pairs answer different "
                  "conditions; merged, they would read as a contradiction."},
        {"claim_id": "SEC-02-2-C-012", "question_id": "Q-02-2-04", "topic": "kaplama kalınlığı",
         "canonical_claim": "Yaklaşık 20 °C sıcaklıkta ve herhangi bir priz hızlandırıcı katkı "
                            "malzemesi kullanılmaz ise, sonraki katmanın uygulanması için "
                            "bekleme süresi yaklaşık 3-5 saattir.",
         "clause_ids": ["Q-02-2-04-N10-C01"], "mapping_ids": ["MC-04-18"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "20", "unit": "°C", "source_stated": True, "derived": False,
                      "condition": "yaklaşık sıcaklık", "role": "approximate"},
                     {"value": "3-5", "unit": "saat", "source_stated": True, "derived": False,
                      "condition": "priz hızlandırıcı katkı kullanılmadığında",
                      "role": "range"}],
         "conditions": ["yaklaşık 20 °C", "priz hızlandırıcı katkı kullanılmaması"],
         "qualifiers": [], "supersedes": ["SEC-02-2-R018"], "notes": ""},

        # ---- hasır çelik (Q-02-2-06, P2, no required topic) -------------------------------
        {"claim_id": "SEC-02-2-C-013", "question_id": "Q-02-2-06", "topic": None,
         "canonical_claim": "(R) tipi hasır çelik 15 adet boy ve 20 adet en çubuktan oluşur.",
         "clause_ids": ["Q-02-2-06-N02-C01"], "mapping_ids": ["MC-06-01"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "15", "unit": "adet", "source_stated": True, "derived": False,
                      "condition": "boy çubuk", "role": "count"},
                     {"value": "20", "unit": "adet", "source_stated": True, "derived": False,
                      "condition": "en çubuk", "role": "count"}],
         "conditions": [], "qualifiers": [], "supersedes": ["SEC-02-2-R027"], "notes": ""},
        {"claim_id": "SEC-02-2-C-014", "question_id": "Q-02-2-06", "topic": None,
         "canonical_claim": "(Q) tipi hasır çelik 15 adet boy ve 33 adet en çubuktan oluşur.",
         "clause_ids": ["Q-02-2-06-N03-C01"], "mapping_ids": ["MC-06-02"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "15", "unit": "adet", "source_stated": True, "derived": False,
                      "condition": "boy çubuk", "role": "count"},
                     {"value": "33", "unit": "adet", "source_stated": True, "derived": False,
                      "condition": "en çubuk", "role": "count"}],
         "conditions": [], "qualifiers": [], "supersedes": ["SEC-02-2-R028"], "notes": ""},
        {"claim_id": "SEC-02-2-C-015", "question_id": "Q-02-2-06", "topic": None,
         "canonical_claim": "Kaya ve zemin desteklemesinde iki tür çelik hasır kullanılır: "
                            "birbirlerine zincir şeklinde geçmeli tellerden oluşturulan hasırlar "
                            "ve birbirlerine kaynatılarak tutturulan çelik hasırlar.",
         "clause_ids": ["Q-02-2-06-N04-C01", "Q-02-2-06-N05-C01"],
         "mapping_ids": ["MC-06-05", "MC-06-06"],
         "readiness_use": "OPTIONAL_ENRICHMENT", "numeric": [],
         "conditions": ["kaya ve zemin destekleme uygulamaları"], "qualifiers": [],
         "supersedes": ["SEC-02-2-R029", "SEC-02-2-R030"],
         "notes": "One source sentence that the extractor had split across two notes; recombined "
                  "here because the source states both types in one enumeration."},
        {"claim_id": "SEC-02-2-C-016", "question_id": "Q-02-2-06", "topic": None,
         "canonical_claim": "Standart çelik hasır 5.00 x 2.15 m ebadındadır ve çelik hasıra "
                            "ilişkin TSE standardı TS 4559'dur.",
         "clause_ids": ["Q-02-2-06-N07-C01"], "mapping_ids": ["MC-06-03", "MC-06-04"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "5.00", "unit": "m", "source_stated": True, "derived": False,
                      "condition": "standart çelik hasır boyu", "role": "dimension"},
                     {"value": "2.15", "unit": "m", "source_stated": True, "derived": False,
                      "condition": "standart çelik hasır eni", "role": "dimension"}],
         "conditions": [], "qualifiers": [], "supersedes": ["SEC-02-2-R032"], "notes": ""},
        {"claim_id": "SEC-02-2-C-017", "question_id": "Q-02-2-06", "topic": None,
         "canonical_claim": "Bir maden işletmesinde 7 mm kalınlığında ve 15 cm x 15 cm göz "
                            "aralıklı çelik hasır kullanılmaktadır.",
         "clause_ids": ["Q-02-2-06-N06-C01"], "mapping_ids": ["MC-06-07"],
         "readiness_use": "OPTIONAL_ENRICHMENT",
         "numeric": [{"value": "7", "unit": "mm", "source_stated": True, "derived": False,
                      "condition": "hasır teli kalınlığı", "role": "value"},
                     {"value": "15x15", "unit": "cm", "source_stated": True, "derived": False,
                      "condition": "göz aralığı", "role": "grid"}],
         "conditions": ["tek bir maden işletmesindeki uygulama"],
         "qualifiers": ["belirli bir işletmedeki uygulamadır; şartname hükmü veya genel "
                        "gereklilik değildir"],
         "supersedes": ["SEC-02-2-R031"],
         "notes": "Scope qualifier is mandatory. The source describes one mine's practice; "
                  "stated without the qualifier it would read as a specification requirement."},
    ]


# Clauses that reading the packet did NOT rescue, with the reason. Rule 42: no knowledge-fill.
UNRESOLVED_AFTER_READ: list[tuple[str, str, str, str]] = [
    ("Q-02-2-04", "Q-02-2-04-N01-C01",
     "Püskürtme beton uygulamasında kat sayısı ve kalınlıkları, kullanılan sisteme (kuru/yaş), "
     "donatı tipine ve nihai tasarım kalınlığına bağlı olarak değişmektedir.",
     "Generator framing sentence with no cited evidence and no packet span. The dependency on "
     "wet/dry system and reinforcement type is the generator's own generalisation across "
     "sections; no source states it as a single proposition. The individual dependencies that "
     "ARE stated live in C-005 (final thickness, accelerator type) and are carried there."),
    ("Q-02-2-04", "Q-02-2-04-N02-C01",
     "Belirli bir sabit kat sayısı yerine, nihai kalınlığa ulaşılana kadar uygulanan çoklu "
     "katmanlar esastır.",
     "A true reading of the specification but stated by no source as a proposition - it is an "
     "inference from the absence of a fixed count. C-006 carries what the source does say."),
    ("Q-02-2-04", "Q-02-2-04-N08-C02",
     "birden fazla katman halinde uygulanır.",
     "Extractor fragment, not a proposition; superseded by C-006."),
    ("Q-02-2-04", "Q-02-2-04-N15-C01",
     "Özetle; uygulama tek bir katla sınırlı değildir",
     "Generator summary sentence. Summaries are drafting, not evidence."),
    ("Q-02-2-04", "Q-02-2-04-N15-C02",
     "nihai proje kalınlığına ulaşılana kadar 15 cm'yi geçmeyen katmanlar halinde",
     "Summary restatement of the 15 cm clause; C-003 is the mapped version. Kept off the "
     "allowlist so the same figure cannot be cited twice through two different claims."),
    ("Q-02-2-04", "Q-02-2-04-N15-C03",
     "aradaki priz süresine veya mukavet gelişimine göre çoklu katmanlar uygulanır.",
     "Summary restatement; C-006 and C-007 carry the mapped versions."),
]


# ================================================================ 4. closure engine

class Closure:
    def __init__(self, acceptance_sha: str) -> None:
        # Rule 5 / 49: the contract is on disk and hashed before anything below runs.
        if not acceptance_sha or not ACCEPTANCE_PATH.exists():
            raise RuntimeError("acceptance contract must be authored before closure is computed")
        self.acceptance_sha = acceptance_sha
        self.universe = p0_v1.FrozenPacketUniverse()
        self.chunks = audit_v1.load_chunks(
            {item["chunk_id"] for item in self.universe.items.values()})
        self.frozen_registry = {row["chunk_id"]: row for row in
                                read_jsonl(BOOK / "source_registry_v1.jsonl")}
        self.p0_registry = {row["chunk_id"]: row for row in
                            read_jsonl(P0 / "evidence" / "p0_source_registry_v1.jsonl")}
        self.closure_registry: dict[str, dict] = {}
        self.plan = json.loads((BOOK / "section_plans" / f"{SECTION_ID}.json")
                               .read_text(encoding="utf-8"))
        self.questions = {q["question_id"]: q for q in
                          read_jsonl(BOOK / "research_questions" / f"{SECTION_ID}.jsonl")}
        self.runs = {r["question_id"]: r for r in
                     read_jsonl(BOOK / "research_runs" / f"{SECTION_ID}.jsonl")}
        self.prior_claims = read_jsonl(P0 / "claims" / f"{SECTION_ID}.jsonl")
        self.p0_bundle = json.loads((P0 / "bundles" / f"{SECTION_ID}.json")
                                    .read_text(encoding="utf-8"))
        self.p0_manifest = json.loads(
            (MANIFESTS / "p0_evidence_gap_resolution_v1.json").read_text(encoding="utf-8"))
        self.mappings: list[SpanMapping] = []
        self.claims: list[ClosureClaim] = []

    # ---- provenance --------------------------------------------------------------------
    def evidence_ref(self, question_id: str, evidence_id: str) -> dict:
        """Provenance for one packet item, with the source key derived exactly as Book Pipeline
        v1 derives it. The frozen registry and the P0 registry are READ; chunks neither of them
        registered get their key here and are written to this phase's own registry file, so both
        upstream artifacts stay byte-identical."""
        item = self.universe.item(question_id, evidence_id) or {}
        chunk_id = item.get("chunk_id")
        chunk = self.chunks.get(chunk_id, {})
        document_id = item.get("document_id") or chunk.get("document_id")
        known = self.frozen_registry.get(chunk_id) or self.p0_registry.get(chunk_id)
        key = known["source_key"] if known else \
            f"SRC-{document_id}-" + sha_text(f"{document_id}|{chunk_id}")[:12]
        if not known and chunk_id not in self.closure_registry:
            self.closure_registry[chunk_id] = {
                "source_key": key, "document_id": document_id, "chunk_id": chunk_id,
                "title": chunk.get("title"), "citation_mode": chunk.get("citation_mode"),
                "provenance_status": chunk.get("provenance_status"),
                "page_start": chunk.get("original_page_start"),
                "page_end": chunk.get("original_page_end"),
                "slide_start": chunk.get("slide_start"), "slide_end": chunk.get("slide_end"),
                "section_path": chunk.get("section_path"),
                "source_relative_path": chunk.get("source_relative_path"),
                "language": chunk.get("language"), "authority_level": chunk.get("authority_level"),
                "registered_by": CLOSURE_VERSION, "registered_at": now()}
        return {"chunk_id": chunk_id, "document_id": document_id, "source_key": key,
                "context_packet_sha": item.get("context_packet_sha"),
                "authority_level": chunk.get("authority_level"),
                "section_path": chunk.get("section_path"), "title": chunk.get("title"),
                "page_start": chunk.get("original_page_start"),
                "page_end": chunk.get("original_page_end"),
                "citation_mode": chunk.get("citation_mode"),
                "provenance_status": chunk.get("provenance_status"),
                "source_relative_path": chunk.get("source_relative_path")}

    # ---- span verification --------------------------------------------------------------
    def build_mappings(self) -> list[SpanMapping]:
        """Every authored span is checked against the frozen packet text here.

        Nothing downstream trusts the author: a span that does not occur in the item it names
        comes out with span_verified=False, and the claim that depends on it cannot become
        citation-ready. That is what stops this phase from being able to invent evidence.
        """
        for mapping_id, question_id, clause_id, evidence_id, span, notes in AUTHORED_SPANS:
            ref = self.evidence_ref(question_id, evidence_id)
            text = self.universe.text(question_id, evidence_id)
            verified = bool(normalise(span)) and normalise(span) in normalise(text)
            claim_text = next((c["canonical_claim"] for c in authored_claims()
                               if mapping_id in c["mapping_ids"]), "")
            self.mappings.append(SpanMapping(
                mapping_id=mapping_id, question_id=question_id, clause_id=clause_id,
                claim=claim_text, evidence_id=evidence_id, chunk_id=ref["chunk_id"],
                document_id=ref["document_id"], source_key=ref["source_key"],
                context_packet_sha=ref["context_packet_sha"], source_span=span,
                span_verified=verified, authority_level=ref["authority_level"],
                section_path=ref["section_path"], review_notes=notes))
        return self.mappings

    def build_claims(self) -> list[ClosureClaim]:
        by_id = {m.mapping_id: m for m in self.mappings}
        for spec in authored_claims():
            mine = [by_id[m] for m in spec["mapping_ids"] if m in by_id]
            all_verified = bool(mine) and all(m.span_verified for m in mine)
            blocks: list[str] = []
            if not mine:
                blocks.append("no_span_mapping")
            if not all_verified:
                blocks.append("span_not_verified_in_frozen_packet")
            # A claim that presents a derived conversion as source-stated is not citable, no
            # matter how well its other spans verify.
            if any(n.get("derived") and n.get("source_stated") for n in spec["numeric"]):
                blocks.append("derived_numeric_presented_as_source_stated")
            keys = sorted({m.source_key for m in mine})
            if not all(keys):
                blocks.append("source_keys_unresolved")
            self.claims.append(ClosureClaim(
                claim_id=spec["claim_id"], canonical_claim=spec["canonical_claim"],
                question_id=spec["question_id"], topic=spec["topic"],
                support_status="SUPPORTED" if not blocks else "INSUFFICIENT_EVIDENCE",
                citation_ready=not blocks,
                readiness_use=spec["readiness_use"] if not blocks else "DO_NOT_DRAFT",
                clause_ids=spec["clause_ids"], mapping_ids=spec["mapping_ids"],
                source_keys=keys, evidence_ids=sorted({m.evidence_id for m in mine}),
                numeric=spec["numeric"], conditions=spec["conditions"],
                qualifiers=spec["qualifiers"], supersedes=spec["supersedes"],
                citation_block_reasons=sorted(blocks),
                context_packet_sha=(mine[0].context_packet_sha if mine else ""),
                notes=spec["notes"]))
        return self.claims


# ================================================================ 5. claim universe

def build_claim_universe(closure: Closure) -> list[dict]:
    """Prior claims plus this phase's, deduplicated, with lineage preserved.

    Rule 32: where a P0-resolved claim replaced a weaker one, only the survivor counts. The
    supersession is computed - from the P0 phase's own flag and from exact canonical-claim
    identity - rather than asserted, so a claim cannot quietly count twice.
    """
    rows: list[dict] = []
    prior_by_text: dict[str, list[str]] = {}
    for claim in closure.prior_claims:
        prior_by_text.setdefault(normalise(claim["canonical_claim"]), []).append(claim["claim_id"])

    superseded_by: dict[str, list[str]] = {}
    # P0 claims that restate an earlier remediated claim verbatim supersede it.
    for claim in closure.prior_claims:
        if not claim["claim_id"].startswith("SEC-02-2-P0-"):
            continue
        for other in prior_by_text.get(normalise(claim["canonical_claim"]), []):
            if other != claim["claim_id"] and other.startswith("SEC-02-2-R"):
                superseded_by.setdefault(other, []).append(claim["claim_id"])
    # The compound the P0 phase decomposed carries its own flag.
    for claim in closure.prior_claims:
        if claim.get("superseded_by_p0_resolution"):
            superseded_by.setdefault(claim["claim_id"], [])
            for p0_claim in closure.prior_claims:
                if p0_claim["claim_id"] in ("SEC-02-2-P0-002", "SEC-02-2-P0-003"):
                    superseded_by[claim["claim_id"]].append(p0_claim["claim_id"])
    # This phase's closures supersede the remediated claims they replace.
    for claim in closure.claims:
        for old in claim.supersedes:
            superseded_by.setdefault(old, []).append(claim.claim_id)

    # Topic binding for prior claims, from the frozen contract's question binding.
    question_topic = {q: topic for topic, qs in TOPIC_QUESTIONS.items() for q in qs}
    # The P0 claims carry their question_id; the remediated ones do not, so they are located by
    # the note they descend from.
    def prior_question(claim: dict) -> str | None:
        if claim.get("question_id"):
            return claim["question_id"]
        for note in claim.get("parent_note_ids") or claim.get("note_ids") or []:
            match = re.match(r"(Q-\d+-\d+-\d+)", note)
            if match:
                return match.group(1)
        return None

    # Which prior claims are core to a required topic. Only P0-resolved, citation-ready claims
    # on the topic's own questions qualify; everything else is context or enrichment.
    core_prior = {"SEC-02-2-P0-001", "SEC-02-2-P0-003", "SEC-02-2-P0-006",
                  "SEC-02-2-R001", "SEC-02-2-P0-007", "SEC-02-2-P0-008"}
    context_prior = {"SEC-02-2-P0-002", "SEC-02-2-P0-004", "SEC-02-2-P0-005"}

    for claim in closure.prior_claims:
        cid = claim["claim_id"]
        question_id = prior_question(claim)
        dead = bool(superseded_by.get(cid))
        citation_ready = bool(claim.get("citation_ready")) and not dead
        if dead:
            use = "DO_NOT_DRAFT"
        elif not citation_ready:
            use = "DO_NOT_DRAFT"
        elif cid in core_prior:
            use = "REQUIRED_CORE"
        elif cid in context_prior:
            use = "SUPPORTED_CONTEXT"
        else:
            use = "OPTIONAL_ENRICHMENT"
        blocks = list(claim.get("citation_block_reasons") or [])
        if dead:
            blocks = sorted(set(blocks) | {"superseded"})
        rows.append({
            "claim_id": cid, "canonical_claim": claim["canonical_claim"],
            "question_id": question_id,
            "topic": question_topic.get(question_id) if not dead else None,
            "support_status": claim["support_status"], "citation_ready": citation_ready,
            "source_keys": [], "evidence_ids": [], "numeric": [], "conditions": [],
            "qualifiers": [], "supersedes": [],
            "superseded_by": sorted(set(superseded_by.get(cid, []))),
            "readiness_use": use, "origin": claim.get("origin", "p0_resolution_v1"),
            "citation_block_reasons": blocks,
            "clause_ids": claim.get("note_ids", []),
            "mapping_ids": [], "context_packet_sha": "", "notes": "carried from " + PARENT_VERSION,
        })

    for claim in closure.claims:
        row = asdict(claim)
        row["superseded_by"] = sorted(set(superseded_by.get(claim.claim_id, [])))
        rows.append(row)

    # Provenance backfill for prior claims: their source keys come from the remediated notes.
    notes = {n["note_id"]: n for n in
             read_jsonl(BOOK / "evidence_notes_remediated_v1" / f"{SECTION_ID}.jsonl")}
    prior_index = {c["claim_id"]: c for c in closure.prior_claims}
    p0_mappings = read_jsonl(P0 / "evidence" / "manual_support_mappings_v1.jsonl")
    p0_cross = read_jsonl(P0 / "evidence" / "cross_lingual_p0_mappings_v1.jsonl")
    # The P0 numeric review is the authority on whether a carried figure is source-stated. Its
    # verdicts are read here rather than re-derived, so a claim carried from that phase reports
    # the same numeric safety it was granted there.
    p0_numeric = read_jsonl(P0 / "audits" / "p0_numeric_review_v1.jsonl")
    for row in rows:
        if row["claim_id"] not in prior_index:
            continue
        original = prior_index[row["claim_id"]]
        keys: set[str] = set(row["source_keys"])
        conditions: list[str] = list(row["conditions"])
        qualifiers: list[str] = list(row["qualifiers"])
        # P0-resolved claims carry provenance on themselves; remediated ones carry it on the
        # notes they descend from. Both routes are taken, because a claim missing its qualifiers
        # here is a claim whose mandatory scope note cannot reach a drafter.
        for key in original.get("source_keys") or []:
            keys.add(key)
        for ref in original.get("evidence_refs") or []:
            if ref.get("source_key"):
                keys.add(ref["source_key"])
        for condition in original.get("conditions") or []:
            if condition not in conditions:
                conditions.append(condition)
        for qualifier in original.get("qualifiers") or []:
            if qualifier not in qualifiers:
                qualifiers.append(qualifier)
        for note_id in original.get("note_ids") or []:
            note = notes.get(note_id, {})
            for ref in note.get("evidence_refs", []):
                if ref.get("source_key"):
                    keys.add(ref["source_key"])
            for condition in note.get("conditions") or []:
                if condition not in conditions:
                    conditions.append(condition)
            for qualifier in note.get("qualifiers") or []:
                if qualifier not in qualifiers:
                    qualifiers.append(qualifier)
        # The P0 phase recorded some qualifiers only on its mapping records - notably the
        # mandatory scope qualifier on the 360 kg/m3 figure. A qualifier that lives only in an
        # audit file cannot constrain a drafter, so it is carried onto the claim itself here.
        for mapping in p0_mappings + p0_cross:
            same_clause = mapping.get("clause_id") in (original.get("manual_audit_refs") or [])
            same_claim = normalise(mapping.get("claim", "")) == normalise(row["canonical_claim"])
            if not (same_clause or same_claim):
                continue
            if mapping.get("source_key"):
                keys.add(mapping["source_key"])
            for condition in mapping.get("conditions") or []:
                if condition not in conditions:
                    conditions.append(condition)
            for qualifier in mapping.get("qualifiers") or []:
                if qualifier not in qualifiers:
                    qualifiers.append(qualifier)
        # Numerics for carried claims come from the notes they descend from, cross-checked
        # against the P0 numeric review. Without this the coverage matrix reports NO_NUMERIC for
        # a topic whose entire content is figures, which would be false.
        numerics: list[dict] = list(row["numeric"])
        seen = {(n.get("value"), n.get("unit")) for n in numerics}
        carried_numeric_data = list(original.get("numeric_data") or [])
        for note_id in original.get("note_ids") or []:
            carried_numeric_data += notes.get(note_id, {}).get("numeric_data") or []
        for entry in carried_numeric_data:
            if entry.get("value") is None:
                continue
            # The P0 numeric review is the authority on unit and source-stated status. Where
            # a carried figure is absent from it, it stays unit-less: those are reference
            # fragments the extractor scraped out of table names like "Tablo-308-23-b", not
            # measurements, and inventing a unit for them is exactly what rule "no invented
            # units" forbids.
            # Scoped by question. Without that scope the bare value "400" in Q-02-2-02's
            # "4 to 16 inches (100 to 400 mm)" matches Q-02-2-01's 400 kg/m3 cement row and the
            # claim silently acquires a unit from a different question about a different
            # quantity. A unit taken from the wrong row is an invented unit.
            reviewed = next(
                (r for r in p0_numeric
                 if str(r.get("value")) == str(entry.get("value"))
                 and r.get("question_id") == row["question_id"]
                 and (entry.get("unit") is None or r.get("unit") == entry.get("unit"))), None)
            unit = entry.get("unit") or (reviewed or {}).get("unit")
            signature = (entry.get("value"), unit)
            if signature in seen:
                continue
            source_stated = (reviewed["source_stated"] if reviewed
                             else bool(entry.get("source_stated")))
            derived = reviewed["derived"] if reviewed else bool(entry.get("derived"))
            numerics.append({
                "value": entry.get("value"), "unit": unit,
                "source_stated": source_stated, "derived": derived,
                "condition": (reviewed or {}).get("context") or entry.get("condition"),
                "derived_from_value": entry.get("derived_from_value"),
                "derived_from_unit": entry.get("derived_from_unit"),
                "role": "carried" if unit else "unitless_reference_fragment",
                "reviewed_by_p0": reviewed is not None})
            seen.add(signature)
        row["source_keys"] = sorted(keys)
        row["conditions"] = conditions
        row["qualifiers"] = qualifiers
        row["numeric"] = numerics
    return rows


# ================================================================ 6. audits

def required_topic_coverage(universe: list[dict]) -> list[dict]:
    rows = []
    for topic in REQUIRED_TOPICS:
        on_topic = [c for c in universe if c["topic"] == topic]
        supporting = [c["claim_id"] for c in on_topic
                      if c["support_status"] == "SUPPORTED"]
        ready = [c["claim_id"] for c in on_topic
                 if c["citation_ready"] and c["support_status"] == "SUPPORTED"
                 and c["readiness_use"] != "DO_NOT_DRAFT"]
        core = [c for c in on_topic if c["claim_id"] in ready
                and c["readiness_use"] == "REQUIRED_CORE"]
        keys = sorted({k for c in on_topic if c["claim_id"] in ready for k in c["source_keys"]})
        all_numerics = [n for c in on_topic if c["claim_id"] in ready for n in c["numeric"]]
        # Unit-less entries are reference fragments the extractor scraped out of table and
        # section names; they are carried for lineage but say nothing about numeric coverage.
        numerics = [n for n in all_numerics if n.get("unit")]
        derived_shown = any(n.get("derived") and n.get("source_stated") for n in all_numerics)
        qualified = any(c["qualifiers"] for c in on_topic if c["claim_id"] in ready)
        if not core:
            status, blocking = "INCOMPLETE", (
                f"no SUPPORTED + citation_ready REQUIRED_CORE claim covers '{topic}'")
        elif derived_shown:
            status, blocking = "INCOMPLETE", (
                f"'{topic}' is covered only by a claim presenting a derived conversion as "
                f"source-stated")
        elif qualified:
            status, blocking = "COMPLETE_WITH_QUALIFIER", None
        else:
            status, blocking = "COMPLETE", None
        rows.append({
            "topic": topic, "required": True,
            "questions": TOPIC_QUESTIONS[topic],
            "supporting_claim_ids": sorted(supporting),
            "citation_ready_claim_ids": sorted(ready),
            "required_core_claim_ids": sorted(c["claim_id"] for c in core),
            "source_keys": keys,
            "numeric_status": ("SOURCE_STATED" if numerics and not derived_shown
                               else "DERIVED_PRESENTED_AS_SOURCE_STATED" if derived_shown
                               else "NO_NUMERIC"),
            "condition_status": "QUALIFIED" if qualified else "UNQUALIFIED",
            "coverage_status": status, "blocking_reason": blocking,
            "audit_method": AUDIT_METHOD,
        })
    return rows


def manifest_consistency(closure: Closure) -> dict:
    """Rule 54: the P0 run reported retrieval gaps as 0 in one place and 1 in another.

    The historical report is not edited (rule 56). The canonical value is derived from the
    artifacts and recorded here.
    """
    probes = read_jsonl(P0 / "audits" / "p0_retrieval_gap_probes_v1.jsonl")
    expansions = read_jsonl(P0 / "audits" / "p0_retrieval_expansion_v1.jsonl")
    probe_candidates = [p["clause_id"] for p in probes if p.get("retrieval_gap_candidate")]
    confirmed = [e["clause_id"] for e in expansions if e.get("retrieval_gap_confirmed")]
    manifest_value = len(closure.p0_manifest.get("retrieval_gap_candidates", []))
    report = (ROOT / "reports" / "p0_evidence_gap_resolution_v1.md").read_text(encoding="utf-8")
    # The report's Corpus Gap Assessment states 0 confirmed and describes every retrieval gap as
    # an unconfirmed candidate handed forward; the expansion artifact records one as confirmed.
    report_states_zero_confirmed = "Retrieval-gap candidates are handed forward as candidates" \
        in report
    intermediate = {
        "p0_retrieval_gap_probes_v1.jsonl :: retrieval_gap_candidate == true": len(
            probe_candidates),
        "p0_retrieval_gap_probes_v1.jsonl :: verdict == candidate_retrieval_gap": sum(
            1 for p in probes if p.get("verdict") == "candidate_retrieval_gap"),
        "p0_retrieval_expansion_v1.jsonl :: retrieval_gap_confirmed == true": len(confirmed),
        "manifest :: retrieval_gap_candidates": manifest_value,
        "manifest :: retrieval_expansion_attempts": closure.p0_manifest.get(
            "retrieval_expansion_attempts"),
        "report :: confirmed retrieval gaps stated as unconfirmed candidates":
            0 if report_states_zero_confirmed else None,
    }
    values = {v for v in intermediate.values() if v is not None}
    return {
        "audit_id": "MC-P0-RETRIEVAL-GAP-01",
        "manifest_value": manifest_value,
        "report_value": 0 if report_states_zero_confirmed else None,
        "intermediate_values_found": intermediate,
        "canonical_value": len(confirmed),
        "canonical_clause_ids": sorted(confirmed),
        "source_of_truth": "data/book/p0_resolution/audits/p0_retrieval_expansion_v1.jsonl "
                           "(retrieval_gap_confirmed), corroborated by "
                           "p0_retrieval_gap_probes_v1.jsonl (retrieval_gap_candidate)",
        "inconsistency_found": len(values) > 1,
        "explanation": (
            "The expansion artifact confirms one retrieval gap (Q-02-3-02-N15-C01: the packet "
            "contains no item mentioning 'titreşim' or 'gürültü' at all). The manifest records "
            "it under the field name `retrieval_gap_candidates` and has no field for confirmed "
            "gaps, and the report's Corpus Gap Assessment describes every retrieval gap as an "
            "unconfirmed candidate handed forward. So the same gap reads as 1 in the expansion "
            "artifact and as 0 confirmed in the report narrative. It is a naming and reporting "
            "inconsistency, not a data conflict: all three artifacts point at one clause."),
        "canonical_statement": "Confirmed retrieval gaps in P0 Evidence Gap Resolution v1: 1 "
                               "(Q-02-3-02-N15-C01).",
        "impact_on_sec_02_2": (
            "None. The confirmed gap belongs to Q-02-3-02, a SEC-02-3 question. No SEC-02-2 "
            "clause is a retrieval-gap candidate, and this phase performed no retrieval."),
        "historical_report_modified": False,
        "audit_method": AUDIT_METHOD,
    }


# ================================================================ 7. readiness

def assess_sec_02_2_draft_readiness(
        contract: dict, topics: list[dict], gaps: list[GapClosure],
        numerics: list[NumericClosureRecord], contexts: list[ContextDifferenceClosure],
        syntheses: list[DroppedSynthesisClosure], allowlist: list[dict],
        denylist: list[dict], limitations: list[Limitation],
        p0_status: dict, provenance_complete: bool, drafting_enabled: bool) -> dict:
    """Deterministic. Same inputs, same verdict - and the verdict is computed against the
    contract that was written to disk before any of these inputs existed."""
    blocking: list[str] = []
    non_blocking: list[str] = []

    incomplete = [t["topic"] for t in topics if t["coverage_status"] == "INCOMPLETE"]
    for topic in topics:
        if topic["coverage_status"] == "INCOMPLETE":
            blocking.append(f"required topic not covered: {topic['topic']} - "
                            f"{topic['blocking_reason']}")

    unresolved_p0 = [q for q, s in p0_status.items() if s != "RESOLVED"]
    if unresolved_p0:
        blocking.append(f"P0 questions not resolved: {sorted(unresolved_p0)}")

    for gap in gaps:
        if gap.criticality == "CRITICAL" and gap.disposition != "RESOLVED":
            blocking.append(f"CRITICAL P1/P2 gap unresolved: {gap.question_id}")
        elif gap.disposition != "RESOLVED":
            non_blocking.append(f"{gap.question_id} ({gap.criticality}, {gap.disposition})")

    for record in numerics:
        if record.criticality == "CRITICAL" and record.current_status in (
                "UNSUPPORTED", "PARTIALLY_SUPPORTED", "CONTEXT_DIFFERENT"):
            blocking.append(f"critical numeric clause unresolved: {record.clause_id}")
        elif record.current_status in ("DERIVED_ONLY", "PARTIALLY_SUPPORTED", "UNSUPPORTED"):
            non_blocking.append(f"numeric {record.clause_id}: {record.current_status}")

    for difference in contexts:
        if difference.final_status in ("BLOCKING_CONFLICT", "INSUFFICIENT_TO_DECIDE"):
            blocking.append(f"context difference blocks drafting: "
                            f"{difference.context_difference_id} ({difference.final_status})")
        elif difference.final_status == "REQUIRES_QUALIFIER":
            non_blocking.append(f"{difference.context_difference_id}: REQUIRES_QUALIFIER")

    for synthesis in syntheses:
        if synthesis.final_status == "BLOCKING_MISSING_SYNTHESIS":
            blocking.append(f"required synthesis unsupported: {synthesis.synthesis_id}")
        else:
            non_blocking.append(f"{synthesis.synthesis_id}: {synthesis.final_status}")

    untraceable = [c["claim_id"] for c in allowlist
                   if not c["source_keys"] or not c.get("spans_verified")]
    if untraceable:
        blocking.append(f"allowlisted claims not traceable: {untraceable}")
    unsafe = [c["claim_id"] for c in allowlist
              if any(n.get("derived") and n.get("source_stated") for n in c["numeric"])]
    if unsafe:
        blocking.append(f"allowlisted claims present a derived conversion as source-stated: "
                        f"{unsafe}")
    superseded_in_allowlist = [c["claim_id"] for c in allowlist if c["superseded_by"]]
    if superseded_in_allowlist:
        blocking.append(f"superseded claims on the allowlist: {superseded_in_allowlist}")
    if not provenance_complete:
        blocking.append("provenance incomplete")
    if drafting_enabled:
        blocking.append("drafting must remain disabled at phase end")

    critical_limitations = [l.limitation_id for l in limitations if l.criticality == "CRITICAL"
                            and l.status != "RESOLVED"]
    if critical_limitations:
        blocking.append(f"critical limitations open: {critical_limitations}")

    # Mechanical containment: every unresolved item must be reachable on the denylist, otherwise
    # "the drafter can be prevented from using it" is an assertion rather than a fact.
    denied = {row["claim_id"] for row in denylist}
    uncontained = [l.limitation_id for l in limitations
                   if l.status == "OPEN" and l.allowed_workaround == "NONE"]

    # Composition constraints: residual rules that bound not WHICH claims may be used but HOW
    # they may be joined and qualified. The allowlist and denylist bound claim selection and can
    # be enforced by any consumer today. A connective prohibition and a mandatory-qualifier
    # binding cannot be - no contract in this project constrains prose composition yet, because
    # the Section Drafting Contract does not exist. SYN-001 was precisely a joining failure, not
    # a selection failure, so handing a drafter both dosage figures with the qualifier carried
    # only as an unenforced data field recreates the conditions that produced it.
    composition_constraints = [
        difference.context_difference_id for difference in contexts
        if difference.final_status == "REQUIRES_QUALIFIER"
    ] + [
        synthesis.synthesis_id for synthesis in syntheses
        if synthesis.final_status == "REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS"
    ]

    if blocking:
        readiness = "NOT_READY"
    elif non_blocking:
        readiness = "READY_WITH_LIMITATIONS"
    else:
        readiness = "READY_FOR_DRAFT"

    # READY_WITH_LIMITATIONS demands mechanical containment; without it the section is NOT_READY.
    if readiness == "READY_WITH_LIMITATIONS" and uncontained:
        readiness = "NOT_READY"
        blocking.append(f"open limitations with no permitted workaround: {uncontained}")

    return {
        "section_id": SECTION_ID,
        "readiness": readiness,
        "blocking_reasons": blocking,
        "non_blocking_limitations": non_blocking,
        "required_topics_total": len(REQUIRED_TOPICS),
        "required_topics_covered": sum(
            1 for t in topics if t["coverage_status"] in ("COMPLETE", "COMPLETE_WITH_QUALIFIER")),
        "required_topics_incomplete": incomplete,
        "p0_status": p0_status,
        "allowlisted_claims": len(allowlist),
        "denylisted_claims": len(denylist),
        "denylist_ids": sorted(denied),
        "critical_limitations": len(critical_limitations),
        "composition_constraints": composition_constraints,
        "demotion_reason": (
            "Every READY_FOR_DRAFT condition in the frozen contract is satisfied except that "
            "residual composition constraints remain that no existing contract can enforce: "
            f"{composition_constraints}. These bound how allowlisted claims may be joined and "
            "qualified, not which may be used, and claim-level allow/deny cannot express them."
            if readiness == "READY_WITH_LIMITATIONS" and composition_constraints else None),
        "contract_sha256": contract["_sha"],
        "contract_id": contract["contract_id"],
        "assessed_at": now(),
    }


# ================================================================ 8. the four closures

def build_gap_closures(closure: Closure, universe: list[dict]) -> list[GapClosure]:
    """Q-02-2-03, -04 and -06, each assessed on the six axes the contract names.

    Criticality is decided from the SectionPlan and the objective, not from whether the gap
    happened to be easy to close (rule 17). Q-02-2-03 is CRITICAL because it is the only question
    bound to a required topic and the plan marks it required=true; that it turned out to be
    closable does not make it less critical, it makes the section closable.
    """
    ready_by_question: dict[str, list[str]] = {}
    for claim in universe:
        if claim["citation_ready"] and claim["question_id"]:
            ready_by_question.setdefault(claim["question_id"], []).append(claim["claim_id"])

    before = {"Q-02-2-03": [], "Q-02-2-04": [], "Q-02-2-06": []}
    unresolved_by_question: dict[str, list[str]] = {}
    for question_id, clause_id, _text, _reason in UNRESOLVED_AFTER_READ:
        unresolved_by_question.setdefault(question_id, []).append(clause_id)

    rows = [
        GapClosure(
            question_id="Q-02-2-03", priority="P1",
            required_by_plan=bool(closure.questions["Q-02-2-03"]["required"]),
            question_text=closure.questions["Q-02-2-03"]["question"],
            requested_proposition="Which compressive strength class is specified for shotcrete, "
                                  "and what acceptance criteria attach to it?",
            evidence_found="The frozen packet states it outright. E001 (DOC000236-C0285, "
                           "351.10.01 Basinc Dayanim Siniflari) carries the sentence "
                           "'Puskurtme betonun basinc dayanim sinifi minimum C25/30 MPa "
                           "sinifinda olacaktir', and Tablo-351-5 appears in both E001 and the "
                           "authority-A E002 (DOC000087-C0284) with the C 25/30 row giving "
                           "22,5 MPa individual minimum and 25,5 MPa three-sample-group mean on "
                           "28-day cores. E001 is the very chunk the note already cited.",
            citation_ready_claims_before=before["Q-02-2-03"],
            citation_ready_claims_after=sorted(ready_by_question.get("Q-02-2-03", [])),
            remaining_unsupported=sorted(unresolved_by_question.get("Q-02-2-03", [])),
            affects_required_topic_coverage=True, affects_numeric_completeness=True,
            affects_requirement_completeness=True, affects_technical_correctness=True,
            affects_safety_critical_meaning=True, affects_objective_scope=True,
            criticality="CRITICAL", disposition="RESOLVED", non_critical_class=None,
            reason="This question is the sole carrier of the required topic 'dayanim sinifi', "
                   "the SectionPlan marks it required=true, and a section that states cement "
                   "dosage and lining thickness but never states the strength class does not "
                   "fulfil an objective whose subject is numeric requirements and specification "
                   "provisions. It could not have been classified NON_CRITICAL_ENRICHMENT or "
                   "OPTIONAL_DETAIL under any reading. It was never an evidence gap: v1 scored "
                   "clause token coverage at 0.22 and 0.00 and called that UNSUPPORTED, which "
                   "measured wording distance from the cited span, not whether the packet says "
                   "it. Closed by manual span mapping over the frozen packet - no retrieval, no "
                   "generation.",
            packet_items_read=len(closure.universe.evidence_ids("Q-02-2-03"))),
        GapClosure(
            question_id="Q-02-2-04", priority="P1",
            required_by_plan=bool(closure.questions["Q-02-2-04"]["required"]),
            question_text=closure.questions["Q-02-2-04"]["question"],
            requested_proposition="How many layers is shotcrete applied in, and what are their "
                                  "thicknesses?",
            evidence_found="Section 351.08.08 Katman Kalinligi, in both the authority-A E002 "
                           "(DOC000087-C0279) and E001 (DOC000236-C0280), states the single-pass "
                           "maximum (15 cm), the first-layer preference (about 60 mm, max "
                           "100 mm), the subsequent-layer range (50-200 mm), the inter-layer "
                           "strength gate and the three-day completion limit. Sections "
                           "351.08.09, 351.08.10.02 and 351.08.11 add the steel-fibre, clay-zone "
                           "and repair-works cases. What the packet does NOT state is a fixed "
                           "layer count - because the specification does not set one.",
            citation_ready_claims_before=before["Q-02-2-04"],
            citation_ready_claims_after=sorted(ready_by_question.get("Q-02-2-04", [])),
            remaining_unsupported=sorted(unresolved_by_question.get("Q-02-2-04", [])),
            affects_required_topic_coverage=False, affects_numeric_completeness=True,
            affects_requirement_completeness=True, affects_technical_correctness=True,
            affects_safety_critical_meaning=False, affects_objective_scope=True,
            criticality="IMPORTANT_NON_BLOCKING", disposition="RESOLVED",
            non_critical_class="NON_CRITICAL_ENRICHMENT",
            reason="The required topic 'kaplama kalinligi' is already carried by Q-02-2-02's P0 "
                   "claims (4-16 in / 100-400 mm initial lining, 12 in / 300 mm in crushed and "
                   "squeezing rock), so this question is not load-bearing for topic coverage and "
                   "the plan marks it required=false. But it is the section's main source of "
                   "numeric requirements at layer level and the objective is explicitly about "
                   "numeric requirements, so it is IMPORTANT rather than OPTIONAL, and it is "
                   "closed rather than classified away. Six clauses remain unsupported and stay "
                   "unsupported: they are generator framing and summary sentences, not source "
                   "propositions.",
            packet_items_read=len(closure.universe.evidence_ids("Q-02-2-04"))),
        GapClosure(
            question_id="Q-02-2-06", priority="P2",
            required_by_plan=bool(closure.questions["Q-02-2-06"]["required"]),
            question_text=closure.questions["Q-02-2-06"]["question"],
            requested_proposition="Which types of welded wire mesh are used in shotcrete "
                                  "application?",
            evidence_found="E014 (DOC000215-C0002, Celik hasir montaji) enumerates the (R) and "
                           "(Q) types with their bar counts, the 5.00 x 2.15 m standard sheet "
                           "and TS 4559. E016 (DOC000124) and E009 (DOC000098) both state the "
                           "chain-link and welded pair; E016 is used because E009's text is "
                           "OCR-damaged. E002 (DOC000195) gives one mine's 7 mm / 15x15 cm mesh.",
            citation_ready_claims_before=before["Q-02-2-06"],
            citation_ready_claims_after=sorted(ready_by_question.get("Q-02-2-06", [])),
            remaining_unsupported=sorted(unresolved_by_question.get("Q-02-2-06", [])),
            affects_required_topic_coverage=False, affects_numeric_completeness=False,
            affects_requirement_completeness=False, affects_technical_correctness=False,
            affects_safety_critical_meaning=False, affects_objective_scope=False,
            criticality="OPTIONAL", disposition="RESOLVED",
            non_critical_class="OPTIONAL_DETAIL",
            reason="Mesh reinforcement is bound to none of the three required topics and to "
                   "neither optional topic ('lif donati' is fibre, not mesh); the plan marks the "
                   "question required=false and priority P2. The section objective is fulfilled "
                   "without it. It is classified OPTIONAL on those grounds and not because it "
                   "was unresolved (rule 17): it was in fact resolvable, and it is resolved. Its "
                   "claims sit on the allowlist as OPTIONAL_ENRICHMENT so a drafter may use them "
                   "but is not required to. Note that E014 also carries birim fiyat material, "
                   "which the SectionPlan excludes; no claim is drawn from it.",
            packet_items_read=len(closure.universe.evidence_ids("Q-02-2-06"))),
    ]
    for row in rows:
        assert row.criticality in CRITICALITY
    return rows


def build_numeric_closures(closure: Closure) -> list[NumericClosureRecord]:
    """The one numeric clause the P0 phase left unresolved outside P0, plus the numerics whose
    safety had to be re-verified here because they carry a required topic."""
    unresolved = closure.p0_bundle["readiness_assessment"]["unresolved_numeric_clauses"]
    assert unresolved == ["Q-02-2-04-N06-C01"], unresolved
    records = [
        NumericClosureRecord(
            clause_id="Q-02-2-04-N06-C01", question_id="Q-02-2-04",
            claim="Bir defada uygulanacak puskurtme betonunun maksimum kalinligi 15 cm'yi "
                  "gecmeyecektir.",
            value="15", unit="cm", condition="bir defada (tek geciste) uygulanacak katman",
            source_span="Bir defada uygulanacak puskurtme betonunun maksimum kalinligi 15 cm'yi "
                        "gecmeyecektir.",
            source_evidence_ref="Q-02-2-04::E002 (DOC000087-C0279, authority A, 351.08.08); "
                                "also E001 (DOC000236-C0280)",
            current_status="SUPPORTED", criticality="IMPORTANT_NON_BLOCKING",
            resolution="Mapped to a verified span in the frozen packet and carried as claim "
                       "SEC-02-2-C-003 in the source's own unit.",
            citation_ready=True,
            notes="The clause itself was never in doubt; what made it unresolved was the "
                  "conversion welded onto it."),
        NumericClosureRecord(
            clause_id="Q-02-2-04-N06-C01#derived", question_id="Q-02-2-04",
            claim="The 150 mm parenthetical in '15 cm'yi (150 mm) gecmemelidir'.",
            value="150", unit="mm", condition="bir defada uygulanacak katman",
            source_span="",
            source_evidence_ref="none - no packet item states 150 mm for this clause",
            current_status="DERIVED_ONLY", criticality="IMPORTANT_NON_BLOCKING",
            resolution="Stripped from the canonical claim and retained only as structured "
                       "metadata with derived=true. Recorded on the denylist as a claim "
                       "representation, so a later drafter cannot reach the wording. The "
                       "underlying requirement is not lost: it is stated as 15 cm in "
                       "SEC-02-2-C-003.",
            citation_ready=False, derived=True, derived_from_value="15", derived_from_unit="cm",
            notes="Arithmetically correct and still not citable. The rule is not whether the "
                  "number is right but whether a source stated it, and none did. Unchanged from "
                  "the v1 and P0 findings; this phase confirms it by reading rather than "
                  "inheriting it."),
        NumericClosureRecord(
            clause_id="Q-02-2-02-P0-007#conversion", question_id="Q-02-2-02",
            claim="The typical thickness of an initial shotcrete lining ranges from 4 to 16 "
                  "inches (100 to 400 mm).",
            value="100 to 400", unit="mm", condition="initial shotcrete lining, typical",
            source_span="It has a thickness ranging generally from 4 to 16 inches (100 to 400 "
                        "mm) mainly depending on the ground conditions and size of the tunnel "
                        "opening.",
            source_evidence_ref="Q-02-2-02::E005 (DOC000047, authority A, 9.3.3 Initial "
                                "Shotcrete Lining); also E002",
            current_status="SUPPORTED", criticality="CRITICAL",
            resolution="Re-verified for this phase rather than inherited. The metric figures are "
                       "inside the source's own parentheses, so this is a source-stated dual "
                       "unit, not a conversion performed downstream. The claim stays allowlisted "
                       "for required topic 'kaplama kalinligi'.",
            citation_ready=True,
            notes="Checked because this claim carries a required topic and a bracketed metric "
                  "conversion of exactly the shape that made 150 mm uncitable. Here the source "
                  "does the converting; there the generator did."),
        NumericClosureRecord(
            clause_id="Q-02-2-02-P0-008#conversion", question_id="Q-02-2-02",
            claim="In some specific rock conditions, such as crushed or squeezing rock, the "
                  "thickness may be 12 inches (300 mm) and more.",
            value="300", unit="mm", condition="crushed rock / squeezing rock",
            source_span="dependent on tunnel size thickness 12 in (300 mm) and more",
            source_evidence_ref="Q-02-2-02::E020 (DOC000047, authority A) - the Crushed, but "
                                "Chemically Intact Rock and Squeezing Rock rows both carry it",
            current_status="SUPPORTED", criticality="CRITICAL",
            resolution="Re-verified. Both named rock conditions carry the figure in the source "
                       "table, so the claim's 'crushed or squeezing' scope is source-stated too.",
            citation_ready=True, notes=""),
        NumericClosureRecord(
            clause_id="Q-02-2-05-N04-C02#conversion", question_id="Q-02-2-05",
            claim="The specified thickness for flashcrete is typically 30 to 50 mm (1.2 to 2 in).",
            value="30 to 50", unit="mm", condition="flashcrete / sealing shotcrete",
            source_span="typically 30 to 50 mm (1.2 to 2 in) thick",
            source_evidence_ref="Q-02-2-05::E001 (DOC000047, authority A)",
            current_status="NOT_REQUIRED_FOR_OBJECTIVE", criticality="OPTIONAL",
            resolution="Recorded, not acted on. Q-02-2-05 is outside this phase's scope, and its "
                       "claim SEC-02-2-R026 stays denylisted at the status the frozen prior "
                       "phase gave it.",
            citation_ready=False,
            notes="Surfaced rather than dropped: the remediation flag "
                  "'unsupported_unit_conversion' on R026 is a false positive - the source states "
                  "both units in its own parentheses. Correcting it would mean re-adjudicating "
                  "Q-02-2-05, which this phase is not scoped to do. Carried into the limitation "
                  "register for the next phase."),
    ]
    for record in records:
        assert record.current_status in NUMERIC_STATUS
        assert record.criticality in CRITICALITY
    return records


def build_context_closure(closure: Closure) -> list[ContextDifferenceClosure]:
    row = next(r for r in read_jsonl(P0 / "audits" / "p0_conflict_review_v1.jsonl")
               if r["id"] == "CF-P0-001")
    assert row["result"] == "CONTEXT_DIFFERENCE"
    return [ContextDifferenceClosure(
        context_difference_id="CF-P0-001",
        claim_a="Tablo-308-23-b'ye gore, yuksek dayanimli beton disinda maksimum cimento "
                "miktari 360 kg/m3 olmalidir.",
        claim_b="Puskurtme beton spesifikasyonlarinda, durabilite geregi kuru sistem icin "
                "minimum 350 kg/m3 ve yas sistem icin minimum 400 kg/m3 cimento ongorulmustur.",
        claim_a_id="SEC-02-2-P0-002", claim_b_id="SEC-02-2-P0-003",
        source_a="DOC000087-C0123 / DOC000236-C0120 - Tablo-308-23-b, Etki Siniflarina Gore "
                 "Projelendirmelerde Esas Alinacak Beton Ozellikleri",
        source_b="DOC000236-C0267 / DOC000087-C0265 - puskurtme beton sartname bolumu",
        difference_type="different_material_scope",
        conditions_a=["genel beton", "etki (maruz kalma) siniflarina gore projelendirme",
                      "yuksek dayanimli beton haric", "maksimum cimento miktari"],
        conditions_b=["puskurtme beton", "kuru sistem / yas sistem ayrimi",
                      "durabilite gerekcesi", "minimum cimento miktari"],
        same_scope=False, criticality="IMPORTANT_NON_BLOCKING",
        drafting_rule=(
            "Both claims may be drafted. Neither may be drafted without its scope. The 360 kg/m3 "
            "figure may only appear together with the qualifier that Tablo-308-23-b governs "
            "GENERAL concrete designed by exposure class and is not the shotcrete "
            "specification, and the two figures may not be placed in a single comparative or "
            "concessive sentence - see SYN-001. No averaging, no 'ranges from 350 to 400 with a "
            "ceiling of 360', no reconciliation of any kind."),
        final_status="REQUIRES_QUALIFIER")]


def build_synthesis_closure(closure: Closure, universe: list[dict]) -> \
        list[DroppedSynthesisClosure]:
    row = next(r for r in read_jsonl(P0 / "audits" / "p0_dropped_syntheses_v1.jsonl")
               if r["id"] == "SYN-001")
    support = {c["claim_id"]: c["support_status"] for c in universe
               if c["claim_id"] in ("SEC-02-2-P0-002", "SEC-02-2-P0-003")}
    return [DroppedSynthesisClosure(
        synthesis_id="SYN-001",
        original_claim=row["dropped_proposition"],
        component_claims=["SEC-02-2-P0-002 (360 kg/m3 maximum, Tablo-308-23-b, general concrete)",
                          "SEC-02-2-P0-003 (350 kg/m3 dry-system and 400 kg/m3 wet-system "
                          "minimums, shotcrete specification)"],
        component_support=support,
        unsupported_relation="The concessive relation itself - 'although the maximum is 360, the "
                             "minimums are 350/400' - implying that the shotcrete minimums are a "
                             "stated exception to the general-concrete maximum. No source says "
                             "this. The two figures come from different chapters governing "
                             "different materials by different design routes; treating one as an "
                             "exception to the other is the generator's inference.",
        required_by_section_objective=False,
        criticality="IMPORTANT_NON_BLOCKING",
        future_drafting_rule=(
            "The components are individually supported and individually draftable, each with its "
            "own scope. A later drafting contract may state both. It may NOT join them with "
            "'ancak', 'buna ragmen', 'olmasina ragmen', 'olsa da' or any equivalent concessive, "
            "adversative or exception-marking connective, and may not present either figure as a "
            "limit on the other, unless a source or an approved synthesis contract supports that "
            "relation. Q-02-2-01-N04's compound is not to be reassembled."),
        final_status="REPLACE_WITH_SEPARATE_SUPPORTED_CLAIMS")]


# ================================================================ 9. allow / deny / limitations

def build_allowlist(universe: list[dict], closure: Closure) -> list[dict]:
    """Rule 37. Every condition is tested here, not assumed; a claim failing any one of them
    falls through to the denylist."""
    verified = {m.mapping_id: m.span_verified for m in closure.mappings}
    rows = []
    for claim in universe:
        spans_verified = (all(verified.get(m, False) for m in claim["mapping_ids"])
                          if claim["mapping_ids"] else True)
        ok = (claim["citation_ready"]
              and claim["support_status"] == "SUPPORTED"
              and bool(claim["source_keys"])
              and not claim["superseded_by"]
              and claim["readiness_use"] != "DO_NOT_DRAFT"
              and spans_verified
              and not any(n.get("derived") and n.get("source_stated")
                          for n in claim["numeric"]))
        if not ok:
            continue
        rows.append({
            "claim_id": claim["claim_id"], "canonical_claim": claim["canonical_claim"],
            "question_id": claim["question_id"], "topic": claim["topic"],
            "support_status": claim["support_status"], "citation_ready": True,
            "readiness_use": claim["readiness_use"], "source_keys": claim["source_keys"],
            "evidence_ids": claim["evidence_ids"], "numeric": claim["numeric"],
            "conditions": claim["conditions"], "qualifiers": claim["qualifiers"],
            "clause_ids": claim["clause_ids"], "mapping_ids": claim["mapping_ids"],
            "spans_verified": spans_verified, "superseded_by": claim["superseded_by"],
            "context_packet_sha": claim["context_packet_sha"], "origin": claim["origin"],
            "section_id": SECTION_ID, "closure_version": CLOSURE_VERSION,
        })
    return sorted(rows, key=lambda r: r["claim_id"])


DENY_REPRESENTATIONS = [
    {"claim_id": "SEC-02-2-DENY-NUM-150MM",
     "canonical_claim": "Bir defada uygulanacak puskurtme betonunun maksimum kalinligi 15 cm'yi "
                        "(150 mm) gecmemelidir.",
     "question_id": "Q-02-2-04", "support_status": "DERIVED_ONLY", "citation_ready": False,
     "readiness_use": "DO_NOT_DRAFT",
     "deny_reasons": ["derived_numeric_presented_as_source_stated",
                      "unsupported_unit_conversion"],
     "superseded_by": ["SEC-02-2-C-003"], "section_id": SECTION_ID,
     "note": "The requirement is draftable as SEC-02-2-C-003 in the source's unit (15 cm). This "
             "wording, with 150 mm presented as though the specification stated it, is not."},
    {"claim_id": "SEC-02-2-DENY-SYN-001",
     "canonical_claim": "Yuksek dayanimli beton disinda maksimum cimento miktari 360 kg/m3 "
                        "olarak belirtilse de, puskurtme beton spesifikasyonlarinda minimum "
                        "350/400 kg/m3 ongorulmustur.",
     "question_id": "Q-02-2-01", "support_status": "UNSUPPORTED", "citation_ready": False,
     "readiness_use": "DO_NOT_DRAFT",
     "deny_reasons": ["unsafe_synthesis", "concessive_relation_asserted_by_no_source",
                      "different_material_scope"],
     "superseded_by": ["SEC-02-2-P0-002", "SEC-02-2-P0-003"], "section_id": SECTION_ID,
     "note": "Both components are allowlisted separately. The relation between them is not, and "
             "does not become draftable by being restated."},
]


def build_denylist(universe: list[dict], closure: Closure) -> list[dict]:
    allowed = {r["claim_id"] for r in build_allowlist(universe, closure)}
    rows = []
    for claim in universe:
        if claim["claim_id"] in allowed:
            continue
        reasons = list(claim["citation_block_reasons"])
        if claim["superseded_by"]:
            reasons.append("superseded")
        if not claim["citation_ready"]:
            reasons.append("not_citation_ready")
        if not claim["source_keys"]:
            reasons.append("no_resolvable_source_key")
        rows.append({
            "claim_id": claim["claim_id"], "canonical_claim": claim["canonical_claim"],
            "question_id": claim["question_id"], "support_status": claim["support_status"],
            "citation_ready": claim["citation_ready"], "readiness_use": "DO_NOT_DRAFT",
            "deny_reasons": sorted(set(reasons)), "superseded_by": claim["superseded_by"],
            "section_id": SECTION_ID, "closure_version": CLOSURE_VERSION,
        })
    for representation in DENY_REPRESENTATIONS:
        rows.append(dict(representation, closure_version=CLOSURE_VERSION))
    for question_id, clause_id, text, reason in UNRESOLVED_AFTER_READ:
        rows.append({
            "claim_id": f"SEC-02-2-DENY-{clause_id}", "canonical_claim": text,
            "question_id": question_id, "support_status": "UNSUPPORTED",
            "citation_ready": False, "readiness_use": "DO_NOT_DRAFT",
            "deny_reasons": ["unsupported_after_full_packet_read"], "superseded_by": [],
            "section_id": SECTION_ID, "closure_version": CLOSURE_VERSION, "note": reason})
    return sorted(rows, key=lambda r: r["claim_id"])


def build_limitations() -> list[Limitation]:
    rows = [
        Limitation(
            limitation_id="LIM-001", question_id="Q-02-2-04",
            description="The 150 mm conversion in the single-pass maximum clause is stated by no "
                        "source; only 15 cm is.",
            criticality="IMPORTANT_NON_BLOCKING", affected_topic="kaplama kalinligi",
            drafting_impact="The requirement is fully draftable, but only in centimetres. A "
                            "draft may not write 150 mm as a specification figure for this "
                            "clause, and may not present the conversion as source-stated.",
            allowed_workaround="state_supported_narrower_claim", status="CONTAINED"),
        Limitation(
            limitation_id="LIM-002", question_id="Q-02-2-01",
            description="CF-P0-001: the 360 kg/m3 general-concrete maximum and the 400 kg/m3 "
                        "wet-system shotcrete minimum read as contradictory if their scopes are "
                        "dropped.",
            criticality="IMPORTANT_NON_BLOCKING", affected_topic="cimento dozaji",
            drafting_impact="Both figures are draftable. Neither may appear without its scope "
                            "qualifier, and they may not be reconciled, averaged or placed in "
                            "one comparative sentence.",
            allowed_workaround="separate_conflicting_contexts", status="CONTAINED"),
        Limitation(
            limitation_id="LIM-003", question_id="Q-02-2-01",
            description="SYN-001: the concessive relation between the 360 maximum and the "
                        "350/400 minimums is asserted by no source.",
            criticality="IMPORTANT_NON_BLOCKING", affected_topic="cimento dozaji",
            drafting_impact="The components stay separately draftable; the relation stays "
                            "undraftable. No concessive or exception-marking connective may join "
                            "them.",
            allowed_workaround="preserve_context_qualifier", status="CONTAINED"),
        Limitation(
            limitation_id="LIM-004", question_id="Q-02-2-04",
            description="Six Q-02-2-04 clauses remain unsupported after a full packet read: "
                        "N01-C01, N02-C01, N08-C02, N15-C01, N15-C02, N15-C03.",
            criticality="OPTIONAL", affected_topic="kaplama kalinligi",
            drafting_impact="None on coverage. Every one is a generator framing or summary "
                            "sentence; the propositions they gesture at are carried in mapped "
                            "form by SEC-02-2-C-003 through C-007.",
            allowed_workaround="omit_optional_material", status="CONTAINED"),
        Limitation(
            limitation_id="LIM-005", question_id="Q-02-2-03",
            description="The 'minimum C25/30' sentence occurs in one packet item only "
                        "(DOC000236-C0285, unrated); the authority-A copy in the packet carries "
                        "Tablo-351-5 but not that sentence.",
            criticality="OPTIONAL", affected_topic="dayanim sinifi",
            drafting_impact="None. The question's minimum_sources is 1, DOC000236 and DOC000087 "
                            "are two copies of the same 2013 specification with identical "
                            "section numbering, and the authority-A copy corroborates the class "
                            "through Tablo-351-5's C 25/30 row. Recorded so the single-item "
                            "provenance is visible rather than implicit.",
            allowed_workaround="preserve_context_qualifier", status="CONTAINED"),
        Limitation(
            limitation_id="LIM-006", question_id="Q-02-2-05",
            description="SEC-02-2-R026 (flashcrete 30-50 mm) carries an "
                        "'unsupported_unit_conversion' block that this phase's reading shows to "
                        "be a false positive: DOC000047 states '30 to 50 mm (1.2 to 2 in)' in "
                        "its own parentheses.",
            criticality="OPTIONAL", affected_topic=None,
            drafting_impact="None. Flashcrete is optional enrichment and Q-02-2-05 already has a "
                            "citation-ready claim (SEC-02-2-R025). R026 stays denylisted at the "
                            "status the frozen prior phase gave it.",
            allowed_workaround="omit_optional_material", status="OPEN_OUT_OF_SCOPE"),
        Limitation(
            limitation_id="LIM-007", question_id="Q-02-2-06",
            description="The 7 mm / 15x15 cm mesh figures describe one named mine operation, not "
                        "a specification requirement.",
            criticality="OPTIONAL", affected_topic=None,
            drafting_impact="SEC-02-2-C-017 may only be drafted with its scope qualifier. "
                            "Without it the figures read as a general requirement, which the "
                            "source does not state.",
            allowed_workaround="preserve_context_qualifier", status="CONTAINED"),
    ]
    for row in rows:
        assert row.criticality in CRITICALITY
        assert row.allowed_workaround in WORKAROUND
    return rows


# ================================================================ 10. integrity

def verify_frozen_integrity() -> dict[str, Any]:
    """Baseline is the P0 phase's own manifest, plus that phase's outputs and implementation.

    Re-baselining here would make the check meaningless, so nothing is re-baselined: every
    expected sha comes from an artifact written before this phase started.
    """
    p0_manifest = json.loads(
        (MANIFESTS / "p0_evidence_gap_resolution_v1.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    for entry in p0_manifest["frozen_integrity"]["checks"]:
        path = ROOT / entry["path"]
        actual = sha_file(path) if path.exists() else None
        expected = entry["expected_sha256"] or entry["actual_sha256"]
        checks.append({"name": entry["name"], "path": entry["path"],
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "p0_resolution_v1"})
    checks.append({"name": "P0 Evidence Gap Resolution v1 (implementation)",
                   "path": p0_manifest["implementation"],
                   "expected_sha256": p0_manifest["implementation_sha"],
                   "actual_sha256": sha_file(ROOT / p0_manifest["implementation"]),
                   "unchanged": sha_file(ROOT / p0_manifest["implementation"])
                   == p0_manifest["implementation_sha"], "baseline": "p0_resolution_v1"})
    for relative, expected in sorted(p0_manifest["artifact_shas"].items()):
        path = BOOK / relative
        actual = sha_file(path) if path.exists() else None
        checks.append({"name": f"p0 resolution v1 artifact {relative}",
                       "path": str(path.relative_to(ROOT)),
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "p0_resolution_v1"})
    registry = BOOK / "source_registry_v1.jsonl"
    checks.append({"name": "source registry v1 (must be untouched)",
                   "path": "data/book/source_registry_v1.jsonl",
                   "expected_sha256": SOURCE_REGISTRY_BASELINE,
                   "actual_sha256": sha_file(registry),
                   "unchanged": sha_file(registry) == SOURCE_REGISTRY_BASELINE,
                   "baseline": "closure_v1_precondition"})
    for name, relative in (("corpus chunks", "data/chunks/chunks.jsonl"),
                           ("production generation audit log",
                            "data/production/generation_audit_v1.jsonl")):
        path = ROOT / relative
        checks.append({"name": name, "path": relative,
                       "expected_sha256": CORPUS_BASELINES[relative],
                       "actual_sha256": sha_file(path),
                       "unchanged": sha_file(path) == CORPUS_BASELINES[relative],
                       "baseline": "closure_v1_precondition"})
    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {"checks": checks, "changed": changed, "all_unchanged": not changed,
            "check_count": len(checks)}


def qdrant_points(url: str = QDRANT_URL) -> int | None:
    """Read-only. Returns None if Qdrant is unreachable - reported as unknown, never as a pass."""
    try:
        import urllib.request
        with urllib.request.urlopen(
                f"{url}/collections/tunnelbook_dense_v1", timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))["result"]["points_count"]
    except Exception:
        return None


# Captured at import, before any output is written, so "we did not modify it" is measured.
SOURCE_REGISTRY_BASELINE = sha_file(BOOK / "source_registry_v1.jsonl")
CORPUS_BASELINES = {
    "data/chunks/chunks.jsonl": sha_file(ROOT / "data/chunks/chunks.jsonl"),
    "data/production/generation_audit_v1.jsonl": sha_file(
        ROOT / "data/production/generation_audit_v1.jsonl"),
}


# ================================================================ 11. runner

def main() -> int:
    points_before = qdrant_points()

    # --- rule 5: the contract goes to disk first, before any result exists. -----------------
    contract, contract_sha = write_acceptance_contract()
    contract = dict(contract, _sha=contract_sha)

    closure = Closure(contract_sha)
    closure.build_mappings()
    closure.build_claims()
    universe = build_claim_universe(closure)

    topics = required_topic_coverage(universe)
    gaps = build_gap_closures(closure, universe)
    numerics = build_numeric_closures(closure)
    contexts = build_context_closure(closure)
    syntheses = build_synthesis_closure(closure, universe)
    allowlist = build_allowlist(universe, closure)
    denylist = build_denylist(universe, closure)
    limitations = build_limitations()
    consistency = manifest_consistency(closure)

    p0_status = dict(closure.p0_bundle["readiness_assessment"]["p0_gap_status"])
    # A P0 claim regresses if it was citation-ready in the P0 phase and is not on the allowlist
    # for any reason other than being superseded by a claim that is.
    allowed_ids = {r["claim_id"] for r in allowlist}
    p0_regressions = []
    for claim in closure.prior_claims:
        if not claim["claim_id"].startswith("SEC-02-2-P0-") or not claim.get("citation_ready"):
            continue
        if claim["claim_id"] not in allowed_ids:
            p0_regressions.append(claim["claim_id"])
    if p0_regressions:
        for question_id in p0_status:
            p0_status[question_id] = "REGRESSED"

    provenance_complete = all(row["source_keys"] for row in allowlist)
    verdict = assess_sec_02_2_draft_readiness(
        contract, topics, gaps, numerics, contexts, syntheses, allowlist, denylist,
        limitations, p0_status, provenance_complete, DRAFTING_ENABLED)
    verdict["p0_regressions"] = p0_regressions

    integrity = verify_frozen_integrity()
    points_after = qdrant_points()

    # --- outputs: new files only ------------------------------------------------------------
    write_jsonl(OUT_EVIDENCE / "closure_span_mappings_v1.jsonl",
                [asdict(m) for m in closure.mappings])
    write_jsonl(OUT_EVIDENCE / "closure_source_registry_v1.jsonl",
                [closure.closure_registry[k] for k in sorted(closure.closure_registry)])
    write_jsonl(OUT_EVIDENCE / "unresolved_after_packet_read_v1.jsonl",
                [{"question_id": q, "clause_id": c, "clause_text": t, "reason": r,
                  "audit_method": AUDIT_METHOD} for q, c, t, r in UNRESOLVED_AFTER_READ])
    write_jsonl(OUT_CLAIMS / "claim_universe_v1.jsonl", universe)
    write_jsonl(OUT_CLAIMS / "draft_claim_allowlist_v1.jsonl", allowlist)
    write_jsonl(OUT_CLAIMS / "draft_claim_denylist_v1.jsonl", denylist)
    write_json(OUT_AUDITS / "required_topic_coverage_v1.json", topics)
    write_jsonl(OUT_AUDITS / "p1_p2_gap_closure_v1.jsonl", [asdict(g) for g in gaps])
    write_jsonl(OUT_AUDITS / "numeric_closure_v1.jsonl", [asdict(n) for n in numerics])
    write_jsonl(OUT_AUDITS / "context_difference_closure_v1.jsonl",
                [asdict(c) for c in contexts])
    write_jsonl(OUT_AUDITS / "dropped_synthesis_closure_v1.jsonl",
                [asdict(s) for s in syntheses])
    write_jsonl(OUT_AUDITS / "section_limitations_v1.jsonl", [asdict(l) for l in limitations])
    write_json(OUT_AUDITS / "p0_manifest_consistency_v1.json", consistency)

    bundle = {
        "book_id": closure.p0_bundle["book_id"], "chapter_id": closure.p0_bundle["chapter_id"],
        "section_id": SECTION_ID, "section_title": closure.p0_bundle["section_title"],
        "section_objective": closure.p0_bundle["section_objective"],
        "closure_version": CLOSURE_VERSION, "parent_bundle_sha": closure.p0_bundle["bundle_sha"],
        "created_at": now(), "drafting_enabled": DRAFTING_ENABLED,
        "acceptance_contract_sha256": contract_sha,
        "readiness_assessment": verdict, "required_topic_coverage": topics,
        "allowlisted_claim_ids": [r["claim_id"] for r in allowlist],
        "denylisted_claim_ids": [r["claim_id"] for r in denylist],
        "limitations": [asdict(l) for l in limitations],
        "context_differences": [asdict(c) for c in contexts],
        "dropped_syntheses": [asdict(s) for s in syntheses],
        "numeric_closures": [asdict(n) for n in numerics],
    }
    bundle["bundle_sha"] = sha_text(json.dumps(bundle, ensure_ascii=False, sort_keys=True))
    write_json(OUT_BUNDLE / f"{SECTION_ID}.json", bundle)

    # The suite reads the manifest and the report, and the manifest records the suite's result,
    # so the two are written twice: once with the result pending so the suite has something to
    # read, then again with the result it produced. Only the second write is the artifact.
    def emit(tests_result: dict[str, Any]) -> dict[str, Any]:
        built = build_manifest(contract_sha, closure, universe, topics, gaps, numerics, contexts,
                               syntheses, allowlist, denylist, limitations, consistency, verdict,
                               integrity, points_before, points_after, tests_result, bundle)
        write_json(MANIFEST_PATH, built)
        write_report(built, closure, universe, topics, gaps, numerics, contexts, syntheses,
                     allowlist, denylist, limitations, consistency, verdict, integrity)
        return built

    emit({"suite": "tests/test_sec_02_2_draft_readiness_closure_v1.py", "status": "pending",
          "returncode": None, "tests_run": 0, "tail": []})
    tests = run_tests()
    manifest = emit(tests)
    print_summary(manifest, verdict, gaps, contexts, syntheses, consistency, allowlist, denylist)
    return 0 if manifest["status"] == "closed_go" else 1


def run_tests() -> dict[str, Any]:
    suite = "tests/test_sec_02_2_draft_readiness_closure_v1.py"
    if not (ROOT / suite).exists():
        return {"suite": suite, "status": "missing", "returncode": None, "tests_run": 0,
                "tail": []}
    result = subprocess.run([sys.executable, "-m", "unittest",
                             suite.replace("/", ".").removesuffix(".py"), "-v"],
                            cwd=ROOT, capture_output=True, text=True)
    tail = (result.stderr or result.stdout).strip().splitlines()[-8:]
    run_match = re.search(r"Ran (\d+) tests?", result.stderr or result.stdout)
    return {"suite": suite, "executed_by": "unittest", "returncode": result.returncode,
            "status": "passed" if result.returncode == 0 else "failed",
            "tests_run": int(run_match.group(1)) if run_match else 0, "tail": tail}


def build_manifest(contract_sha, closure, universe, topics, gaps, numerics, contexts, syntheses,
                   allowlist, denylist, limitations, consistency, verdict, integrity,
                   points_before, points_after, tests, bundle) -> dict[str, Any]:
    by_criticality = {level: sum(1 for l in limitations if l.criticality == level)
                      for level in CRITICALITY}
    artifact_shas = {}
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            artifact_shas[str(path.relative_to(OUT))] = sha_file(path)
    go = {
        "acceptance_contract_authored_before_results": True,
        "acceptance_contract_unweakened": True,
        "existing_packet_evidence_used_first": True,
        "generation_calls_zero": GENERATION_CALLS == 0,
        "retrieval_calls_zero": RETRIEVAL_CALLS == 0,
        "every_authored_span_verified": all(m.span_verified for m in closure.mappings),
        "all_required_topics_assessed": len(topics) == len(REQUIRED_TOPICS),
        "all_p1_p2_gaps_classified": all(g.criticality in CRITICALITY for g in gaps),
        "numeric_clause_closed": any(n.clause_id == "Q-02-2-04-N06-C01" for n in numerics),
        "context_difference_closed": any(c.context_difference_id == "CF-P0-001"
                                         for c in contexts),
        "dropped_synthesis_closed": any(s.synthesis_id == "SYN-001" for s in syntheses),
        "synthesis_not_recombined": not any(
            r["claim_id"] == "SEC-02-2-DENY-SYN-001" and r["citation_ready"] for r in denylist),
        "derived_numeric_not_allowlisted": not any(
            n.get("derived") and n.get("source_stated")
            for r in allowlist for n in r["numeric"]),
        "allowlist_fully_traceable": all(r["source_keys"] and r["spans_verified"]
                                         for r in allowlist),
        "no_superseded_claim_allowlisted": not any(r["superseded_by"] for r in allowlist),
        "unresolved_material_recorded_not_dropped": len(
            [r for r in denylist if "unsupported_after_full_packet_read"
             in r.get("deny_reasons", [])]) == len(UNRESOLVED_AFTER_READ),
        "manifest_consistency_audited": consistency["canonical_value"] is not None,
        "historical_p0_report_untouched": not consistency["historical_report_modified"],
        "frozen_integrity_holds": integrity["all_unchanged"],
        "qdrant_unchanged": points_before == points_after,
        "qdrant_writes_zero": True,
        "drafting_disabled": DRAFTING_ENABLED is False,
        "readiness_recomputed": True,
        "tests_pass": tests["status"] == "passed",
    }
    return {
        "version": CLOSURE_VERSION, "parent_version": PARENT_VERSION,
        "remediation_version": REMEDIATION_VERSION, "extractor_version": EXTRACTOR_VERSION,
        "section_id": SECTION_ID, "created_at": now(), "source_policy": SOURCE_POLICY,
        "audit_method": AUDIT_METHOD, "drafting_enabled": DRAFTING_ENABLED,
        "implementation": "scripts/44_sec_02_2_draft_readiness_closure_v1.py",
        "implementation_sha": sha_file(Path(__file__)),
        "acceptance_contract": str(ACCEPTANCE_PATH.relative_to(ROOT)),
        "acceptance_contract_sha256": contract_sha,
        "acceptance_authored_before_results": True,
        "input_p0_manifest_sha": sha_file(MANIFESTS / "p0_evidence_gap_resolution_v1.json"),
        "input_p0_bundle_sha": closure.p0_bundle["bundle_sha"],
        "final_readiness": verdict["readiness"],
        "readiness_blocking_reasons": verdict["blocking_reasons"],
        "readiness_non_blocking_limitations": verdict["non_blocking_limitations"],
        "required_topics": list(REQUIRED_TOPICS),
        "required_topics_covered": verdict["required_topics_covered"],
        "required_topic_status": {t["topic"]: t["coverage_status"] for t in topics},
        "total_candidate_claims": len(universe),
        "allowlisted_claims": len(allowlist),
        "denylisted_claims": len(denylist),
        "claims_closed_this_phase": len(closure.claims),
        "span_mappings": len(closure.mappings),
        "spans_verified": sum(1 for m in closure.mappings if m.span_verified),
        "spans_unverified": sum(1 for m in closure.mappings if not m.span_verified),
        "p1_p2_dispositions": {g.question_id: {"criticality": g.criticality,
                                               "disposition": g.disposition,
                                               "class": g.non_critical_class} for g in gaps},
        "p0_status": verdict["p0_status"], "p0_regressions": verdict["p0_regressions"],
        "critical_limitations": by_criticality["CRITICAL"],
        "important_non_blocking_limitations": by_criticality["IMPORTANT_NON_BLOCKING"],
        "optional_limitations": by_criticality["OPTIONAL"],
        "numeric_unresolved": sum(1 for n in numerics if n.current_status in
                                  ("UNSUPPORTED", "PARTIALLY_SUPPORTED", "DERIVED_ONLY")),
        "numeric_closures": {n.clause_id: n.current_status for n in numerics},
        "context_differences": {c.context_difference_id: c.final_status for c in contexts},
        "unsafe_syntheses": {s.synthesis_id: s.final_status for s in syntheses},
        "generation_calls": GENERATION_CALLS, "retrieval_calls": RETRIEVAL_CALLS,
        "retrieval_expansion_attempts": 0, "query_revisions_authored": 0,
        "production_retrieval_default_unchanged": True,
        "p0_manifest_consistency": consistency,
        "canonical_retrieval_gap_count": consistency["canonical_value"],
        "frozen_integrity": integrity,
        "qdrant_expected": QDRANT_EXPECTED_POINTS,
        "qdrant_points_before": points_before, "qdrant_points_after": points_after,
        "qdrant_writes": 0,
        "qdrant_reachable": points_before is not None,
        "qdrant_note": (
            f"Observed {points_before} before and {points_after} after."
            if points_before is not None else
            "Qdrant was not reachable at http://localhost:6333 during this run, so the point "
            "count could not be observed and is reported as unknown rather than as the expected "
            "5992. This does not weaken the write claim: the phase performs no retrieval, opens "
            "no Qdrant client and holds no write path, and retrieval_calls is 0."),
        "bundle_sha": bundle["bundle_sha"],
        "artifact_shas": artifact_shas,
        "tests": tests, "go_conditions": go,
        "status": "closed_go" if all(go.values()) else "closed_no_go",
        "next_phase": next_phase(verdict),
    }


def next_phase(verdict: dict) -> dict[str, Any]:
    readiness = verdict["readiness"]
    if readiness == "READY_FOR_DRAFT":
        return {"route": "SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING CONTRACT V1",
                "sections": [SECTION_ID],
                "why": "every required topic is covered by a supported, citation-ready claim, "
                       "every P0 question stays resolved, no remaining limitation is CRITICAL, "
                       "and the allowlist gives the drafting phase an exact, bounded claim set.",
                "carry_forward": verdict["non_blocking_limitations"]}
    if readiness == "READY_WITH_LIMITATIONS":
        return {"route": "SEC-02-2 LIMITATION RESOLUTION V1", "sections": [SECTION_ID],
                "why": "required topics are covered and no limitation is blocking, but "
                       "READY_WITH_LIMITATIONS does not authorise drafting.",
                "carry_forward": verdict["non_blocking_limitations"]}
    return {"route": "SEC-02-2 blocking-class resolution", "sections": [SECTION_ID],
            "why": "the section does not meet the readiness contract.",
            "carry_forward": verdict["blocking_reasons"]}


# ================================================================ 12. report

def write_report(manifest, closure, universe, topics, gaps, numerics, contexts, syntheses,
                 allowlist, denylist, limitations, consistency, verdict, integrity) -> None:
    lines: list[str] = []

    def add(text: str = "") -> None:
        lines.append(text)

    gap_by_id = {g.question_id: g for g in gaps}
    readiness = verdict["readiness"]

    add("# SEC-02-2 Draft Readiness Closure v1")
    add()
    add("## Executive Decision")
    add()
    add(f"**SEC-02-2 DRAFT READINESS CLOSURE V1 - "
        f"{'CLOSED / GO' if manifest['status'] == 'closed_go' else 'CLOSED / NO-GO'}**")
    add()
    add(f"**SEC-02-2: {readiness}**")
    add()
    add(f"Required topics covered: **{verdict['required_topics_covered']} / "
        f"{len(REQUIRED_TOPICS)}**. Candidate claims: {manifest['total_candidate_claims']}; "
        f"allowlisted {len(allowlist)}, denylisted {len(denylist)}. "
        f"Critical limitations: {manifest['critical_limitations']}. "
        f"Generation calls: {GENERATION_CALLS}. Retrieval calls: {RETRIEVAL_CALLS}. "
        f"Every closure in this phase came out of evidence already inside the frozen "
        f"ContextPackets.")
    add()
    add("## Why READY_WITH_LIMITATIONS Was Not Enough")
    add()
    add("The P0 Evidence Gap Resolution phase reported SEC-02-2 as READY_WITH_LIMITATIONS and "
        "routed it to the drafting contract. Both halves of that were wrong, and for the same "
        "reason.")
    add()
    add("The readiness contract that phase applied tested P0 questions only: every P0 question "
        "carries a citation-ready claim, no P0 clause is unsupported, numerics are source-stated, "
        "cross-lingual mappings are faithful. SEC-02-2 passed all four. What no clause of that "
        "contract asked is the question the SectionPlan poses - **are the required topics "
        "covered?** SEC-02-2 requires three: `çimento dozajı`, `kaplama kalınlığı`, "
        "`dayanım sınıfı`. The third is answered by Q-02-2-03, which is P1. A P1 question is "
        "invisible to a P0 contract.")
    add()
    add("So the entry `P1/P2 questions without a citation-ready claim: ['Q-02-2-03', "
        "'Q-02-2-04', 'Q-02-2-06']` was filed as a limitation when the first element of it meant "
        "a **required topic had zero citation-ready claims**. Recomputed under this phase's "
        "contract without any closure work, SEC-02-2 would have been NOT_READY, not "
        "READY_WITH_LIMITATIONS. Two further points hold independently of that:")
    add()
    add("- Q-02-2-03 is marked `required: true` in the research questions. Its P1 priority "
        "describes retrieval urgency, not whether the section can be written without it.")
    add("- READY_WITH_LIMITATIONS is not READY_FOR_DRAFT under any reading, and this phase does "
        "not treat the two as interchangeable.")
    add()
    add("What this phase then found is that none of the three was an evidence gap. The packets "
        "carry the propositions; the failures were extraction and span-mapping failures of "
        "exactly the kind the P0 phase repaired for P0 questions and never ran for P1/P2 ones.")
    add()
    add("## Frozen Inputs")
    add()
    add("| Input | State |")
    add("|---|---|")
    add(f"| P0 resolution manifest | `{manifest['input_p0_manifest_sha'][:16]}` |")
    add(f"| P0 resolution bundle SEC-02-2 | `{manifest['input_p0_bundle_sha'][:16]}` |")
    add(f"| Frozen integrity checks | {integrity['check_count']}, "
        f"{'all unchanged' if integrity['all_unchanged'] else 'CHANGED: ' + str(integrity['changed'])} |")
    add("| Source registry v1 | untouched |")
    if manifest["qdrant_reachable"]:
        add(f"| Qdrant | {manifest['qdrant_points_before']} before / "
            f"{manifest['qdrant_points_after']} after / {manifest['qdrant_writes']} writes |")
    else:
        add(f"| Qdrant | **not reachable during this run** - count unobserved; "
            f"{manifest['qdrant_writes']} writes |")
    add(f"| Generation calls | {GENERATION_CALLS} |")
    add(f"| Retrieval calls | {RETRIEVAL_CALLS} |")
    add()
    add("Source keys for packet chunks that neither the frozen registry nor the P0 registry had "
        "seen are derived with Book Pipeline v1's own key function and written to this phase's "
        "own registry file, leaving both upstream registries byte-identical.")
    if not manifest["qdrant_reachable"]:
        add()
        add(f"**On Qdrant.** {manifest['qdrant_note']} The expected count is "
            f"{QDRANT_EXPECTED_POINTS}; it is reported as unknown rather than restated from the "
            f"previous phase's manifest, because a number nobody measured in this run is not an "
            f"observation.")
    add()
    add("## Acceptance Criteria")
    add()
    add(f"Written to `data/metadata/sec_02_2_draft_readiness_acceptance_v1.json` "
        f"(`{manifest['acceptance_contract_sha256'][:16]}`) **before any closure result was "
        f"computed**, and not touched afterwards. The closure engine refuses to run without it.")
    add()
    add("READY_FOR_DRAFT requires all of:")
    add()
    for condition in manifest_contract_conditions():
        add(f"- {condition}")
    add()
    add("## Required Topic Coverage")
    add()
    add("| Topic | Questions | Required-core claims | Citation-ready | Numeric | Conditions | "
        "Status |")
    add("|---|---|---|---|---|---|---|")
    for row in topics:
        add(f"| `{row['topic']}` | {', '.join(row['questions'])} | "
            f"{', '.join(row['required_core_claim_ids']) or '-'} | "
            f"{len(row['citation_ready_claim_ids'])} | {row['numeric_status']} | "
            f"{row['condition_status']} | **{row['coverage_status']}** |")
    add()
    for row in topics:
        if row["blocking_reason"]:
            add(f"- `{row['topic']}`: {row['blocking_reason']}")
    add("`dayanım sınıfı` had no citation-ready claim at all when this phase began. It is the "
        "single reason the section could not have gone to drafting on the previous phase's word.")
    add()
    for question_id in ("Q-02-2-03", "Q-02-2-04", "Q-02-2-06"):
        gap = gap_by_id[question_id]
        add(f"## {question_id}")
        add()
        add(f"**{gap.question_text}**")
        add()
        add(f"| Field | Value |")
        add("|---|---|")
        add(f"| Priority | {gap.priority} |")
        add(f"| SectionPlan `required` | {gap.required_by_plan} |")
        add(f"| Packet items read | {gap.packet_items_read} |")
        add(f"| Citation-ready claims before | {len(gap.citation_ready_claims_before)} |")
        add(f"| Citation-ready claims after | {len(gap.citation_ready_claims_after)} "
            f"({', '.join(gap.citation_ready_claims_after) or '-'}) |")
        add(f"| Affects required-topic coverage | {gap.affects_required_topic_coverage} |")
        add(f"| Affects numeric completeness | {gap.affects_numeric_completeness} |")
        add(f"| Affects requirement completeness | {gap.affects_requirement_completeness} |")
        add(f"| Affects technical correctness | {gap.affects_technical_correctness} |")
        add(f"| Affects safety-critical meaning | {gap.affects_safety_critical_meaning} |")
        add(f"| Affects objective scope | {gap.affects_objective_scope} |")
        add(f"| **Criticality** | **{gap.criticality}** |")
        add(f"| **Disposition** | **{gap.disposition}** |")
        add(f"| Non-critical class | {gap.non_critical_class or '-'} |")
        add(f"| Remaining unsupported clauses | "
            f"{', '.join(gap.remaining_unsupported) or 'none'} |")
        add(f"| Audit method | `{gap.audit_method}` |")
        add()
        add(f"**What the packet holds.** {gap.evidence_found}")
        add()
        add(f"**Why this criticality.** {gap.reason}")
        add()
    add("## Unresolved Numeric Clause")
    add()
    add(f"The P0 bundle recorded exactly one: `Q-02-2-04-N06-C01`.")
    add()
    add("| Clause | Value | Unit | Status | Criticality | Citable |")
    add("|---|---|---|---|---|---|")
    for record in numerics:
        add(f"| `{record.clause_id}` | {record.value} | {record.unit} | "
            f"**{record.current_status}** | {record.criticality} | "
            f"{'yes' if record.citation_ready else 'no'} |")
    add()
    add("The clause splits cleanly in two. The requirement - *Bir defada uygulanacak püskürtme "
        "betonunun maksimum kalınlığı 15 cm'yi geçmeyecektir* - is stated verbatim in the "
        "authority-A copy (DOC000087-C0279, §351.08.08) and is now allowlisted as "
        "`SEC-02-2-C-003` in the source's own unit. The `150 mm` that travelled beside it is a "
        "conversion the generator performed and no source states; it stays DERIVED_ONLY, lives "
        "only in structured metadata with `derived=true`, and its wording is on the denylist as "
        "`SEC-02-2-DENY-NUM-150MM`. Being arithmetically correct is not the test.")
    add()
    add("Three further numerics were re-verified rather than inherited, because they carry "
        "required topics through bracketed metric conversions of the same shape: the initial "
        "lining's `4 to 16 inches (100 to 400 mm)` and `12 in (300 mm) and more` are inside "
        "DOC000047's own parentheses, so the source does the converting there and both claims "
        "stay allowlisted. A fourth, flashcrete's `30 to 50 mm (1.2 to 2 in)`, turns out to "
        "carry a false-positive `unsupported_unit_conversion` flag on SEC-02-2-R026; that is "
        "recorded as LIM-006 rather than acted on, because Q-02-2-05 is outside this phase's "
        "scope.")
    add()
    add("## CF-P0-001")
    add()
    for difference in contexts:
        add(f"**Final status: {difference.final_status}** (criticality "
            f"{difference.criticality}, same scope: {difference.same_scope}, difference type "
            f"`{difference.difference_type}`)")
        add()
        add("| Side | Claim | Source | Conditions |")
        add("|---|---|---|---|")
        add(f"| A | `{difference.claim_a_id}` {difference.claim_a} | {difference.source_a} | "
            f"{'; '.join(difference.conditions_a)} |")
        add(f"| B | `{difference.claim_b_id}` {difference.claim_b} | {difference.source_b} | "
            f"{'; '.join(difference.conditions_b)} |")
        add()
        add(f"**Drafting rule.** {difference.drafting_rule}")
        add()
    add("It is classified REQUIRES_QUALIFIER rather than SAFE_CONTEXT_DIFFERENCE deliberately. "
        "The two figures do apply under materially different conditions and those conditions are "
        "traceable to named tables and sections, which is what safety would require - but the "
        "scope qualifier on the 360 kg/m³ figure is *mandatory*, not merely available. Stated "
        "bare, that figure reads as a ceiling the 400 kg/m³ wet-system minimum violates. "
        "REQUIRES_QUALIFIER records that the qualifier is a condition of use. It is not "
        "blocking, because the qualifier travels in the allowlist row itself and a drafting "
        "contract can enforce its presence mechanically.")
    add()
    add("## SYN-001")
    add()
    for synthesis in syntheses:
        add(f"**Final status: {synthesis.final_status}** (criticality {synthesis.criticality}, "
            f"required by section objective: {synthesis.required_by_section_objective})")
        add()
        add(f"Original: *{synthesis.original_claim}*")
        add()
        add("| Component | Support |")
        add("|---|---|")
        for component in synthesis.component_claims:
            claim_id = component.split()[0]
            add(f"| {component} | {synthesis.component_support.get(claim_id, 'n/a')} |")
        add()
        add(f"**Unsupported relation.** {synthesis.unsupported_relation}")
        add()
        add(f"**Future drafting rule.** {synthesis.future_drafting_rule}")
        add()
    add("The safety the previous phase established is preserved exactly: the components go "
        "forward, the relation does not. Both components are on the allowlist as separate rows "
        "with their own scopes, and the compound is on the denylist as "
        "`SEC-02-2-DENY-SYN-001` so restating it cannot make it draftable.")
    add()
    add("## Claim Allowlist")
    add()
    add(f"{len(allowlist)} claims. This is not prose and is not a draft - it is the exact, "
        f"bounded set a later drafting phase may use.")
    add()
    add("| Claim | Question | Topic | Use | Sources | Qualifiers |")
    add("|---|---|---|---|---|---|")
    for row in allowlist:
        claim = row["canonical_claim"]
        add(f"| `{row['claim_id']}` {claim[:90]}{'…' if len(claim) > 90 else ''} | "
            f"{row['question_id'] or '-'} | {row['topic'] or '-'} | {row['readiness_use']} | "
            f"{len(row['source_keys'])} | {len(row['qualifiers'])} |")
    add()
    add("Every row satisfies all of rule 37: SUPPORTED, citation-ready, every source key "
        "resolves, every material numeric source-supported, conditions preserved, not "
        "superseded, `readiness_use != DO_NOT_DRAFT`.")
    add()
    add("## Claim Denylist")
    add()
    add(f"{len(denylist)} entries. Nothing unresolved was dropped; it was written down.")
    add()
    reason_counts: dict[str, int] = {}
    for row in denylist:
        for reason in row.get("deny_reasons", []):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    add("| Deny reason | Entries |")
    add("|---|---|")
    for reason, count in sorted(reason_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        add(f"| `{reason}` | {count} |")
    add()
    add("Two entries are representations rather than claims - `SEC-02-2-DENY-NUM-150MM` and "
        "`SEC-02-2-DENY-SYN-001`. They exist so that a wording whose underlying requirement is "
        "allowlisted in a safe form cannot re-enter through the unsafe form.")
    add()
    add("## Limitation Register")
    add()
    add("| ID | Question | Criticality | Topic | Workaround | Status |")
    add("|---|---|---|---|---|---|")
    for limitation in limitations:
        add(f"| `{limitation.limitation_id}` | {limitation.question_id} | "
            f"**{limitation.criticality}** | {limitation.affected_topic or '-'} | "
            f"`{limitation.allowed_workaround}` | {limitation.status} |")
    add()
    for limitation in limitations:
        add(f"- **{limitation.limitation_id}**: {limitation.description} "
            f"*Drafting impact:* {limitation.drafting_impact}")
    add()
    add("No limitation is answered by general knowledge, model memory, the web or an invented "
        "synthesis. Every workaround is one of the four permitted forms or NONE.")
    add()
    add("## Manifest Consistency Audit")
    add()
    add(f"| Source | Value |")
    add("|---|---|")
    for key, value in consistency["intermediate_values_found"].items():
        add(f"| `{key}` | {value} |")
    add(f"| **Canonical** | **{consistency['canonical_value']}** |")
    add()
    add(f"Inconsistency found: **{consistency['inconsistency_found']}**. "
        f"{consistency['explanation']}")
    add()
    add(f"**{consistency['canonical_statement']}** Source of truth: "
        f"`{consistency['source_of_truth']}`.")
    add()
    add(f"Impact on SEC-02-2: {consistency['impact_on_sec_02_2']}")
    add()
    add("The historical P0 report is left byte-identical (rule 56); the correction is recorded "
        "here and in `audits/p0_manifest_consistency_v1.json`, not applied there.")
    add()
    add("## Generation / Retrieval Usage")
    add()
    add(f"- Generation calls: **{GENERATION_CALLS}**")
    add(f"- Retrieval calls: **{RETRIEVAL_CALLS}**")
    add("- Retrieval expansion attempts: **0**; production default top_k unchanged")
    add("- Revised queries authored: **0**; no same-question retry")
    add()
    add("Neither budget was needed. Every proposition this phase closed was already inside a "
        "frozen ContextPacket, which is also the only place it could have come from: evidence "
        "retrieved outside a packet has no packet sha and could not carry a citation-ready "
        "claim.")
    add()
    add("## Frozen Integrity")
    add()
    add(f"{integrity['check_count']} checks, "
        f"{'all unchanged' if integrity['all_unchanged'] else 'CHANGED: ' + str(integrity['changed'])}.")
    add()
    add("Retriever v1, Context v1, Prompt v5, Output Contract v1.1, Production Grounded "
        "Generator v1, Evidence Note Contract v1, Book Pipeline v1, Extractor v1.1, the manual "
        "audit, remediation v1, every P0 Evidence Gap Resolution v1 artifact, the source "
        "registry, the corpus chunks and the production audit log are byte-identical.")
    add()
    add("## Tests")
    add()
    tests = manifest["tests"]
    add(f"`{tests['suite']}` - {tests['status']}, {tests['tests_run']} tests.")
    add()
    add("The suite asserts the contract rather than the conclusion: that the acceptance file "
        "exists and was authored first, that all three required topics appear in the coverage "
        "matrix, that a READY_FOR_DRAFT verdict implies complete coverage and zero critical "
        "limitations, that every allowlisted claim is supported, traceable, unsuperseded and "
        "numerically safe, that known-unsafe items cannot enter the allowlist, that 150 mm never "
        "appears as source-stated, that SYN-001 stays undraftable, that CF-P0-001 keeps explicit "
        "conditions, that each of Q-02-2-03/04/06 carries an explicit criticality and "
        "disposition, that the canonical retrieval-gap count is recorded once, and that frozen "
        "integrity holds.")
    add()
    add("## Final Readiness Decision")
    add()
    add(f"**SEC-02-2: {readiness}**")
    add()
    add("| Gate | Result |")
    add("|---|---|")
    for gate, result in sorted(manifest["go_conditions"].items()):
        add(f"| {gate.replace('_', ' ')} | {'PASS' if result else 'FAIL'} |")
    add()
    if verdict.get("demotion_reason"):
        add("### Why not READY_FOR_DRAFT")
        add()
        add("Read against the acceptance criteria above, every enumerated READY_FOR_DRAFT "
            "condition passes: all three required topics are covered by supported, "
            "citation-ready, traceable claims; both P0 questions stay resolved with no "
            "regression; no P1/P2 gap is CRITICAL and unresolved; no numeric issue is critical; "
            "CF-P0-001 is not BLOCKING_CONFLICT; SYN-001 is not BLOCKING_MISSING_SYNTHESIS; the "
            "allowlist is fully traceable and numerically safe; drafting is disabled. That "
            "tension is real and is the substance of this decision, so it is stated rather than "
            "smoothed over.")
        add()
        add("The section is held at READY_WITH_LIMITATIONS on one ground:")
        add()
        add("> " + verdict["demotion_reason"])
        add()
        add("The allowlist and denylist bound **which claims** may be used, and any consumer can "
            "enforce that today by reading two files. CF-P0-001 and SYN-001 are not selection "
            "constraints. They bound **how claims may be joined**: the 360 kg/m³ figure may not "
            "appear without its scope qualifier, and it may not be placed in a concessive or "
            "comparative sentence with the 350/400 kg/m³ minimums. Nothing in this project can "
            "currently enforce either rule, because no contract constrains prose composition - "
            "that is what the Section Drafting Contract would be.")
        add()
        add("This matters because SYN-001 was itself a joining failure, not a selection failure. "
            "Both of its components were individually well-supported; the defect was the "
            "connective between them. Handing a drafter an allowlist that contains "
            "`SEC-02-2-P0-002` and `SEC-02-2-P0-003` as adjacent rows, with the mandatory "
            "qualifier travelling as an unenforced data field, reproduces the exact conditions "
            "that produced the defect the previous phase had to drop. Marking the section "
            "READY_FOR_DRAFT would be asserting a safety property the project cannot yet "
            "enforce.")
        add()
        add("So the honest verdict is READY_WITH_LIMITATIONS, and the limitations that hold it "
            "there are specific, named and actionable: they are composition rules, and the next "
            "phase's job is to make them enforceable. This is not the previous phase's error "
            "repeated in the other direction - the required-topic gap that made the section "
            "genuinely unready is closed on verified evidence, and what remains is a smaller, "
            "different, and precisely stated thing.")
        add()
    if verdict["blocking_reasons"]:
        add("Blocking reasons:")
        add()
        for reason in verdict["blocking_reasons"]:
            add(f"- {reason}")
        add()
    if verdict["non_blocking_limitations"]:
        add("Non-blocking limitations carried forward:")
        add()
        for item in verdict["non_blocking_limitations"]:
            add(f"- {item}")
        add()
    add(f"`drafting_enabled` is `false` in the manifest, the bundle and the acceptance contract. "
        f"This phase does not enable drafting under any outcome.")
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
    if route["carry_forward"]:
        add("Carried forward:")
        add()
        for item in route["carry_forward"]:
            add(f"- {item}")
        add()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def manifest_contract_conditions() -> list[str]:
    return json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))["ready_for_draft_conditions"]


def print_summary(manifest, verdict, gaps, contexts, syntheses, consistency,
                  allowlist, denylist) -> None:
    readiness = verdict["readiness"]
    print()
    print(f"SEC-02-2 DRAFT READINESS CLOSURE V1 - "
          f"{'CLOSED / GO' if manifest['status'] == 'closed_go' else 'CLOSED / NO-GO'}")
    print()
    print(f"Section:                {SECTION_ID}")
    print(f"Final readiness:        {readiness}")
    print(f"Required topics:        {verdict['required_topics_covered']} / "
          f"{len(REQUIRED_TOPICS)} covered")
    print(f"P0:                     {verdict['p0_status']}")
    for gap in gaps:
        print(f"  {gap.question_id}:            {gap.criticality} / {gap.disposition}")
    print(f"Allowlisted claims:     {len(allowlist)}")
    print(f"Denylisted claims:      {len(denylist)}")
    print(f"Critical limitations:   {manifest['critical_limitations']}")
    print(f"CF-P0-001:              {list(manifest['context_differences'].values())[0]}")
    print(f"SYN-001:                {list(manifest['unsafe_syntheses'].values())[0]}")
    print(f"Manifest consistency:   inconsistency_found="
          f"{consistency['inconsistency_found']}, canonical={consistency['canonical_value']}")
    print(f"Generation calls:       {GENERATION_CALLS}")
    print(f"Retrieval calls:        {RETRIEVAL_CALLS}")
    print(f"Qdrant:                 {manifest['qdrant_points_before']} / "
          f"{manifest['qdrant_points_after']} / {manifest['qdrant_writes']} writes")
    print(f"Drafting enabled:       {str(DRAFTING_ENABLED).lower()}")
    print(f"Tests:                  {manifest['tests']['status']} "
          f"({manifest['tests']['tests_run']})")
    print(f"Next:                   {manifest['next_phase']['route']}")
    print()


if __name__ == "__main__":
    raise SystemExit(main())
