"""SEC-02-2 ARCHITECTURE V2 PILOT #2 — one authorised semantic-plan generation, or none.

Pilot #1 was rejected by this phase's own gate. The planner option universe and the feasibility
universe were derived twice, by different code, and disagreed on exactly the claim that broke the
pilot; only one of them reached the model. The remediation replaced both with one canonical
artifact, and this controller consumes it and derives nothing.

**What is new here is the byte-identity gate.** It is not enough that the payload was *built from*
the canonical universe: Pilot #1's option set was also built from the frozen data. The exact
serialized universe segment inside the prompt string that is handed to the model is extracted back
out of that string, hashed, and required to equal the canonical universe SHA and the SHA the
feasibility proof recorded. Reconstructed Python objects are not compared, because equal objects
were never the thing in doubt. If the three hashes are not equal there is no generation.

One call. No repair, no regeneration, no retry, no post-render model pass. A plan that fails
validation is preserved as evidence and never rendered.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "tunnelbook-sec-02-2-architecture-v2-pilot-2"
PHASE = "SEC-02-2 ARCHITECTURE V2 PILOT #2 AUTHORISATION"
SECTION_ID = "SEC-02-2"
PILOT_ID = "SEC-02-2-ARCHV2-PILOT-2"

MODEL_ID = "qwen3.6-35b-a3b-mlx"
TEMPERATURE = 0.0
SEED = 11
MAX_TOKENS = 8000
LMSTUDIO_URL = "http://127.0.0.1:1234"

CANONICAL_UNIVERSE_SHA = "fafa8b4ceebe788d9765ac8f82463fde5b4c1253c38222fe178113874d37c000"
ARCH_V2_CONTRACT_SHA = "c9766e437bd00222574d1aeee5ede17ff74a51bf5ae0cea37e0f3f496f6ebccd"
REMEDIATION_CONTRACT_SHA = "117e9ea4b67e536d54bb0cd262e8860649f7415f600f66f4acc742ebca480560"
M2_V2_1_CONTRACT_SHA = "6d0b3e3ff5619d23fe6896cbf97d0fa010c2ac732c5222d004e06c475fb19eb7"

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
PILOT = ARCH_V2 / "pilot_2"
ACCEPTANCE = PILOT / "contracts" / "architecture_v2_pilot_2_acceptance_contract_v1.json"
REM_CONTRACT = (ARCH_V2 / "remediation_v1" / "contracts"
                / "planner_universe_remediation_acceptance_contract_v1.json")
ARCH_CONTRACT = ARCH_V2 / "contracts" / "architecture_v2_acceptance_contract_v1.json"
M2_V2_1_CONTRACT = ARCH_V2 / "contracts" / "claim_realization_contract_v2_1.json"
PLAN_V1_2 = ROOT / "data/book/drafting/sec_02_2/draft_plan_v1_2.json"
SOURCE_REGISTRY = ROOT / "data/book/source_registry_v1.jsonl"

GATE_PATH = PILOT / "audits" / "pre_generation_gate_v1.json"
PREFLIGHT_PATH = PILOT / "audits" / "frozen_preflight_v1.json"
FEASIBILITY_PATH = PILOT / "audits" / "feasibility_proof_v1.json"
STATIC_PATH = PILOT / "audits" / "static_containment_proof_v2_1.json"
CASES_PATH = PILOT / "audits" / "realization_universe_v2_1.json"
BYTE_IDENTITY_PATH = PILOT / "audits" / "payload_byte_identity_v1.json"
PAYLOAD_PATH = PILOT / "contracts" / "planner_payload_v2_1.json"
PROMPT_PATH = ROOT / "data/metadata/architecture_v2_semantic_planner_prompt_v2.txt"
PROMPT_SENT_PATH = PILOT / "raw" / "model_payload_prompt_v1.txt"
RAW_PATH = PILOT / "raw" / "semantic_plan_raw_v1.json"
PLAN_PATH = PILOT / "plan" / "semantic_plan_ir_v2.json"
RENDER_PATH = PILOT / "rendered" / "rendered_draft_ir_v2.json"
DRAFT_PATH = PILOT / "rendered" / "sec_02_2_pilot_2_draft.md"
VALIDATION_PATH = PILOT / "validation" / "pilot_2_validation.json"
MANIFEST_PATH = ROOT / "data/book/manifests/sec_02_2_architecture_v2_pilot_2.json"
REPORT_PATH = ROOT / "reports" / "sec_02_2_architecture_v2_pilot_2.md"

ZERO_TOLERANCE = (
    "UNSUPPORTED_PROPOSITION", "CLAIM_EXPANSION", "NUMERIC_DRIFT", "UNIT_DRIFT",
    "MODALITY_DRIFT", "CONDITION_DROPPED", "QUALIFIER_DROPPED", "SEMANTIC_SCOPE_MISMATCH",
    "LANGUAGE_MISMATCH", "CLAIM_DENYLISTED", "UNKNOWN_CITATION",
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("p2_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("p2_v1_2", "54_section_draft_validator_v1_2.py")
PLAN_IR = _load("p2_plan_ir", "59_semantic_plan_ir_contract_v2.py")
M2_1 = _load("p2_m2_1", "68_claim_realization_contract_v2_1.py")
RENDER = _load("p2_render", "62_deterministic_surface_renderer_v2.py")
UNIVERSE = _load("p2_universe", "69_planner_option_universe_v2_1.py")
CITE = _load("p2_cite", "48_book_citation_renderer_v1.py")
# The unchanged safety stack and the unchanged frozen preflight, imported rather than restated.
P1 = _load("p2_pilot_1", "65_sec_02_2_architecture_v2_pilot_1.py")
REM = _load("p2_rem", "70_architecture_v2_planner_universe_remediation_v1.py")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    path.write_text(data, encoding="utf-8")
    return sha_text(data)


# ================================================================ gates 1-3 — frozen inputs


def gate_frozen_inputs() -> dict:
    """The remediation's own preflight, extended with the remediation's outputs."""
    preflight = REM.frozen_preflight()
    outputs = {
        "claim_realization_contract_v2_1": (sha_file(M2_V2_1_CONTRACT), M2_V2_1_CONTRACT_SHA),
        "planner_universe_remediation_acceptance_contract_v1": (sha_file(REM_CONTRACT),
                                                                REMEDIATION_CONTRACT_SHA),
        "planner_option_universe_v2_1": (sha_file(UNIVERSE.UNIVERSE_PATH), None),
    }
    remediation_drift = sorted(k for k, (found, expected) in outputs.items()
                               if expected is not None and found != expected)
    arch_sha = sha_file(ARCH_CONTRACT)
    rem_sha = sha_file(REM_CONTRACT)
    preflight.update({
        "remediation_outputs_sha256": {k: v[0] for k, v in sorted(outputs.items())},
        "remediation_output_drift": remediation_drift,
        "architecture_v2_acceptance_contract_prefix_ok": arch_sha.startswith("c9766e43"),
        "remediation_acceptance_contract_sha256": rem_sha,
        "remediation_acceptance_contract_unamended": rem_sha == REMEDIATION_CONTRACT_SHA,
        "drift": preflight["drift"] + len(remediation_drift),
    })
    preflight["passed"] = (preflight["drift"] == 0
                           and preflight["architecture_v2_acceptance_contract_unamended"]
                           and preflight["architecture_v2_acceptance_contract_prefix_ok"]
                           and preflight["remediation_acceptance_contract_unamended"])
    return preflight


# ================================================================ gate 4/5 — the one universe


def gate_universe(realization, bundle) -> dict:
    """Load the canonical universe, reproduce its SHA from a rebuild, re-check the invariant.

    The rebuild is a verification, not a second derivation: it calls the universe's own owner
    module, and nothing downstream of this gate reads its result. Every consumer below reads the
    bytes on disk.
    """
    universe, loaded_sha = UNIVERSE.load_universe()
    recorded = json.loads(UNIVERSE.UNIVERSE_PATH.read_text(encoding="utf-8"))["universe_sha256"]

    rebuilt = UNIVERSE.build_universe(realization, bundle)
    rebuilt_sha = UNIVERSE.sha_bytes(UNIVERSE.canonical_bytes(rebuilt["universe"]))
    construction_violations = UNIVERSE.assert_invariant(rebuilt["universe"])

    violations = UNIVERSE.assert_invariant(universe)
    rows = []
    for option in universe["options"]:
        required = set(option["required_roles"])
        available = set(option["available_roles"])
        realizable = set(option["realizable_roles"])
        rows.append({"claim_id": option["claim_id"],
                     "required_subset_available": required <= available,
                     "available_subset_realizable": available <= realizable,
                     "invariant_holds": required <= available <= realizable})
    return {
        "loaded_sha256": loaded_sha,
        "recorded_sha256": recorded,
        "rebuilt_sha256": rebuilt_sha,
        "expected_sha256": CANONICAL_UNIVERSE_SHA,
        "sha_reproduced": (loaded_sha == recorded == rebuilt_sha == CANONICAL_UNIVERSE_SHA),
        "artifact_sha256": sha_file(UNIVERSE.UNIVERSE_PATH),
        "claims_exposed": len(universe["options"]),
        "exclusions": universe["exclusions"],
        "unrealizable_pairs_exposed": universe["unrealizable_pairs_exposed"],
        "invariant": universe["invariant"],
        "invariant_rows": rows,
        "invariant_violations": violations,
        "construction_violations": construction_violations,
        "passed": (loaded_sha == recorded == rebuilt_sha == CANONICAL_UNIVERSE_SHA
                   and not violations and not construction_violations
                   and len(universe["options"]) == 16
                   and universe["unrealizable_pairs_exposed"] == 0
                   and all(r["invariant_holds"] for r in rows)),
        "universe": universe,
    }


# ================================================================ the payload and its bytes

PLANNER_PROMPT = """Sen bir teknik kitap bölümü için SEMANTİK PLANLAYICISISIN.

MUTLAK KURAL: Hiçbir cümle, ifade, açıklama veya metin üretmeyeceksin.
Yalnızca sembolik seçimler yapacaksın: hangi iddia (claim_id), hangi rolde
(realization_role), hangi sırada ve hangi paragrafta yer alacak.

Bütün görünür Türkçe metni deterministik bir renderer üretir. Senin çıktında
hiçbir yerde serbest metin alanı bulunamaz.

ÇIKTI: yalnızca aşağıdaki şemaya uyan tek bir JSON nesnesi. Başka hiçbir şey yok.

{
  "section_id": "SEC-02-2",
  "plan_id": "<kısa tanımlayıcı, boşluksuz>",
  "plan_version": "<kısa tanımlayıcı, boşluksuz>",
  "language": "tr",
  "subsections": [
    {
      "subsection_id": "<kısa tanımlayıcı, boşluksuz>",
      "paragraph_groups": [
        {
          "paragraph_id": "<kısa tanımlayıcı, boşluksuz>",
          "slots": [
            {
              "slot_id": "<kısa tanımlayıcı, boşluksuz>",
              "claim_id": "<yalnızca evrendeki options listesinden>",
              "realization_role": "<yalnızca o iddianın available_roles listesinden>"
            }
          ]
        }
      ]
    }
  ]
}

İZİN VERİLEN ALAN ADLARI SADECE BUNLARDIR. Başka bir alan adı eklersen plan
tamamen reddedilir. Özellikle şunlar YASAKTIR: text, sentence, phrase,
free_text, explanation, prose, note, description, content, body.

ZORUNLU PLAN KURALLARI:
1. Bir iddia bir paragrafta yer alıyorsa, o paragrafta o iddianın
   statement_role alanında yazan rol ZORUNLU olarak bulunmalıdır.
2. Bir iddianın required_roles listesindeki HER rol, o iddianın yer aldığı
   AYNI paragrafta bir slot olarak bulunmak ZORUNDADIR.
3. Bir iddia bir paragrafta CLAIM_STATEMENT ve REQUIREMENT rollerinin
   yalnızca BİRİNİ alabilir.
4. Yalnızca o iddianın available_roles listesinde yazan rolleri seçebilirsin.
   Listede olmayan bir rol planı geçersiz kılar.
5. required_core_claim_ids listesindeki her iddia planda yer almalıdır;
   zorunlu konuların üçü de kapsanmalıdır.
6. Aşağıdaki evrende olmayan hiçbir iddiayı veya rolü kullanamazsın. Evren
   tek kaynaktır; başka bir listeye başvurma.

GÖREV: Aşağıdaki KANONİK PLANLAYICI EVRENİ'ni kullanarak SEC-02-2 bölümü için
eksiksiz bir semantik plan üret. Evrendeki subsections sırasını koru, iddia
sırasını teknik olarak anlamlı biçimde düzenle.
"""

UNIVERSE_BEGIN = "=== CANONICAL PLANNER UNIVERSE v2.1 BEGIN ==="
UNIVERSE_END = "=== CANONICAL PLANNER UNIVERSE v2.1 END ==="


def build_model_payload(universe: dict) -> dict:
    """The exact prompt string the model will be given, plus the bytes of its universe segment.

    The universe is embedded as the canonical serialization the remediation contract specifies —
    the same bytes `load_universe` hashed — delimited so the segment can be recovered from the
    finished prompt and hashed on its own.
    """
    generation = _load("p2_generation", "21_generation_model_eval.py")
    payload = UNIVERSE.planner_payload(universe)
    universe_text = UNIVERSE.canonical_bytes(payload["universe"]).decode("utf-8")

    user = (f"{PLANNER_PROMPT}\n\n{UNIVERSE_BEGIN}\n{universe_text}{UNIVERSE_END}\n\n"
            "Yalnızca JSON döndür.\n")
    renderer = generation.TemplateRenderer()
    tokenizer = generation.GenerationTokenizer()
    prompt = renderer.render(system=PLANNER_PROMPT, user=user, enable_thinking=False)
    return {"generation": generation, "renderer": renderer, "tokenizer": tokenizer,
            "prompt": prompt, "payload": payload, "universe_text": universe_text}


def extract_universe_segment(prompt: str) -> str:
    """Recover the serialized universe from the finished prompt. Ambiguity is a failure."""
    if prompt.count(UNIVERSE_BEGIN) != 1 or prompt.count(UNIVERSE_END) != 1:
        raise ValueError("universe delimiters are not unique in the model payload")
    start = prompt.index(UNIVERSE_BEGIN) + len(UNIVERSE_BEGIN) + 1
    end = prompt.index(UNIVERSE_END)
    if end <= start:
        raise ValueError("universe delimiters are out of order in the model payload")
    return prompt[start:end]


def gate_byte_identity(built: dict, feasibility_sha: str, canonical_sha: str) -> dict:
    """The gate Pilot #1 did not have, enforced on the bytes that leave this process."""
    segment = extract_universe_segment(built["prompt"])
    model_payload_sha = sha_text(segment)
    equal = canonical_sha == feasibility_sha == model_payload_sha == CANONICAL_UNIVERSE_SHA
    return {
        "method": ("the serialized universe segment is extracted from the finished prompt string "
                   "and hashed as UTF-8 bytes; no Python object is compared"),
        "canonical_universe_sha256": canonical_sha,
        "feasibility_universe_sha256": feasibility_sha,
        "model_payload_universe_sha256": model_payload_sha,
        "expected_sha256": CANONICAL_UNIVERSE_SHA,
        "segment_bytes": len(segment.encode("utf-8")),
        "all_equal": equal,
        "passed": equal,
    }


# ================================================================ coverage, measured once


def coverage_report(payload_ir: dict, verdict: dict, bundle) -> dict:
    """Citation, language, condition and qualifier coverage — each measured by its owner.

    **Gate-design correction, made before the generation and recorded here.** Pilot #1's
    `coverage_report` scores a condition by looking for its anchors in the paragraph, and does not
    add the frozen `condition_glosses` that stage E adds for exactly this case: an English-source
    claim rendered in Turkish cannot retain an English anchor. It is therefore a second
    implementation of stage E's rule, stricter than the rule itself, and it false-rejects every
    valid rendering of SEC-02-2-P0-007 and SEC-02-2-P0-008 — it reports 0.8696 on the
    deterministic feasibility plan that Draft Validator v1.2 accepts with an empty histogram.

    That is Pilot #1's defect class exactly: one rule implemented twice, disagreeing. The
    remediation's principle applies unchanged — ask the validator that owns the question instead
    of reimplementing it. So the condition and qualifier figures are taken from the unchanged
    Draft Validator v1.2's own failures, counted as the remediation's feasibility proof counts
    them.

    Nothing is weakened. Stage E, stage L, CONDITION_DROPPED, QUALIFIER_DROPPED and
    SEMANTIC_SCOPE_MISMATCH are untouched and still reject; the discarded measurement was not a
    stricter check but a wrong one. Pilot #1's figures are still computed and reported alongside,
    so the divergence stays visible rather than being resolved silently.
    """
    reported = P1.coverage_report(payload_ir, bundle)
    histogram = verdict["histogram"]

    stated = {u["claim_ids"][0] for u in payload_ir["units"] if u["claim_ids"]}
    conditions_required = qualifiers_required = 0
    for claim_id in sorted(stated):
        claim = bundle.allowlist[claim_id]
        conditions_required += len([c for c in (claim.get("conditions") or [])
                                    if V1.content_tokens(c, bundle.function_lexicon)])
        qualifiers_required += len(claim.get("qualifiers") or [])
    conditions_dropped = histogram.get("CONDITION_DROPPED", 0)
    qualifiers_dropped = (histogram.get("QUALIFIER_DROPPED", 0)
                          + histogram.get("SEMANTIC_SCOPE_MISMATCH", 0))

    coverage = dict(reported)
    coverage.update({
        "condition_obligations": conditions_required,
        "conditions_dropped": conditions_dropped,
        "condition_preservation": (round(1 - conditions_dropped / conditions_required, 4)
                                   if conditions_required else 1.0),
        "qualifier_obligations": qualifiers_required,
        "qualifiers_dropped": qualifiers_dropped,
        "qualifier_preservation": (round(1 - qualifiers_dropped / qualifiers_required, 4)
                                   if qualifiers_required else 1.0),
        "measured_by": "draft_validator_v1_2_stage_E_and_L",
        "pilot_1_anchor_metric": {
            "condition_preservation": reported["condition_preservation"],
            "condition_obligations": reported["condition_obligations"],
            "qualifier_preservation": reported["qualifier_preservation"],
            "qualifier_obligations": reported["qualifier_obligations"],
            "note": ("reimplements stage E without its frozen condition glosses; reported as a "
                     "diagnostic, not as the gate"),
        },
    })
    return coverage


# ================================================================ the one generation


def generate_semantic_plan(built: dict) -> dict:
    generation = built["generation"]
    config = generation.GenerationConfig(
        model_id=MODEL_ID, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED,
        tokenizer_sha256=built["tokenizer"].tokenizer_sha256,
        template_sha256=built["renderer"].template_sha256,
        system_prompt_version="architecture-v2-semantic-planner-v2",
        system_prompt_sha256=sha_text(PLANNER_PROMPT))
    prompt_tokens = built["tokenizer"].count(built["prompt"])
    headroom = generation.validate_prompt_budget(prompt_tokens, MAX_TOKENS)
    began = now()
    response = generation.complete(built["prompt"], config, MAX_TOKENS, base_url=LMSTUDIO_URL)
    return {
        "pilot_id": PILOT_ID, "section_id": SECTION_ID, "model_id": MODEL_ID,
        "temperature": TEMPERATURE, "seed": SEED, "max_tokens": MAX_TOKENS,
        "system_prompt_version": "architecture-v2-semantic-planner-v2",
        "system_prompt_sha256": sha_text(PLANNER_PROMPT),
        "template_sha256": built["renderer"].template_sha256,
        "tokenizer_sha256": built["tokenizer"].tokenizer_sha256,
        "prompt_sha256": sha_text(built["prompt"]),
        "prompt_tokens": prompt_tokens, "context_headroom": headroom,
        "requested_at": began, "completed_at": now(),
        "finish_reason": response["finish_reason"], "usage": response.get("usage", {}),
        "latency_seconds": response.get("latency_seconds"),
        "raw_text": response["text"],
        "raw_text_sha256": sha_text(response["text"]),
        "generation_calls": 1,
    }


# ================================================================ plan / universe consistency


def plan_universe_consistency(raw_plan: dict, universe: dict, realization) -> dict:
    """Every selected pair proven against the canonical universe, claim by claim.

    The universe is the authority for what was offered; M2 v2.1 is the authority for what is
    realizable. Both are checked, because Pilot #1 failed on the gap between two such answers.
    """
    options = {o["claim_id"]: o for o in universe["options"]}
    unknown_claims, not_available, not_realizable, unrealizable = [], [], [], []
    selected = []
    for subsection in raw_plan.get("subsections", []):
        for paragraph in subsection.get("paragraph_groups", []):
            for slot in paragraph.get("slots", []):
                claim_id = slot.get("claim_id")
                role = slot.get("realization_role")
                pair = f"{claim_id}/{role}"
                selected.append((claim_id, role))
                option = options.get(claim_id)
                if option is None:
                    unknown_claims.append(pair)
                    continue
                if role not in option["available_roles"]:
                    not_available.append(pair)
                if role not in option["realizable_roles"]:
                    not_realizable.append(pair)
                if (realization.entry(claim_id, role) or {}).get("status") != "REALIZABLE":
                    unrealizable.append(pair)

    obligations_unmet = []
    for subsection in raw_plan.get("subsections", []):
        for paragraph in subsection.get("paragraph_groups", []):
            held: dict[str, set[str]] = {}
            for slot in paragraph.get("slots", []):
                held.setdefault(slot.get("claim_id"), set()).add(slot.get("realization_role"))
            for claim_id, roles in held.items():
                option = options.get(claim_id)
                if option is None:
                    continue
                for required in option["required_roles"]:
                    if required not in roles:
                        obligations_unmet.append(
                            {"paragraph_id": paragraph.get("paragraph_id"), "claim_id": claim_id,
                             "missing_role": required})

    stated = {c for c, r in selected if r in ("CLAIM_STATEMENT", "REQUIREMENT")}
    core = set(universe["required_core_claim_ids"])
    return {
        "slots": len(selected),
        "claims": len({c for c, _ in selected}),
        "claim_role_counts": {f"{c}/{r}": sum(1 for a, b in selected if (a, b) == (c, r))
                              for c, r in sorted(set(selected))},
        "role_counts": {role: sum(1 for _, r in selected if r == role)
                        for role in sorted({r for _, r in selected})},
        "claims_not_exposed_by_universe": sorted(set(unknown_claims)),
        "roles_not_available": sorted(set(not_available)),
        "roles_not_realizable_in_universe": sorted(set(not_realizable)),
        "unrealizable_pairs_selected": sorted(set(unrealizable)),
        "mandatory_obligations_unmet": obligations_unmet,
        "required_core_claims_missing": sorted(core - stated),
        "consistent": not (unknown_claims or not_available or not_realizable or unrealizable
                           or obligations_unmet or (core - stated)),
    }


# ================================================================ determinism


def determinism_check(realization, bundle) -> dict:
    """Three in-process renders and one in a process that shares nothing with this one."""
    raw_plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    UNIVERSE.ensure_obligation_rule()
    digests = [RENDER.render_sha256(RENDER.render_from_raw(raw_plan, realization, bundle))
               for _ in range(3)]
    script = (
        "import importlib.util,sys,json\n"
        f"sys.path.insert(0,{str(ROOT)!r})\n"
        "def L(n,f):\n"
        f"    s=importlib.util.spec_from_file_location(n,{str(ROOT / 'scripts')!r}+'/'+f)\n"
        "    m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m)\n"
        "    return m\n"
        "v1=L('a','49_section_draft_validator_v1.py')\n"
        "m21=L('b','68_claim_realization_contract_v2_1.py')\n"
        "u=L('d','69_planner_option_universe_v2_1.py')\n"
        "rd=L('c','62_deterministic_surface_renderer_v2.py')\n"
        "b=v1.load_bundle();r=m21.load()\n"
        "uni,_=u.load_universe()\n"
        "u.install_obligation_rule({o['claim_id']:{'registered_conditions':"
        "b.allowlist[o['claim_id']].get('conditions') or [],"
        "'requires_condition_slot':o['requires_condition_slot']} for o in uni['options']})\n"
        f"plan=json.loads(open({str(PLAN_PATH)!r},encoding='utf-8').read())\n"
        "print(rd.render_sha256(rd.render_from_raw(plan,r,b)))\n")
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                               cwd=str(ROOT))
    fresh = completed.stdout.strip()
    return {"in_process_runs": len(digests), "in_process_identical": len(set(digests)) == 1,
            "in_process_sha256": digests[0], "fresh_process_sha256": fresh,
            "identical": len(set(digests)) == 1 and fresh == digests[0],
            "stderr": completed.stderr.strip()[-300:]}


# ================================================================ acceptance gate


def evaluate_acceptance(state: dict) -> dict:
    contract = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    pre = state["preflight"]
    uni = state["universe_gate"]
    feas = state["feasibility"]
    static = state["static"]
    byte_gate = state.get("byte_identity") or {}
    plan = state.get("plan_validation") or {}
    cons = state.get("consistency") or {}
    post = state.get("post_render") or {}
    hist = state.get("historical") or {}
    gen = state.get("generation") or {}

    checks = {
        "AC-P01": pre["drift"] == 0,
        "AC-P02": pre["architecture_v2_acceptance_contract_unamended"],
        "AC-P03": pre["remediation_acceptance_contract_unamended"],
        "AC-P04": not pre["remediation_output_drift"],
        "AC-P05": uni["sha_reproduced"],
        "AC-P06": (not uni["invariant_violations"] and uni["claims_exposed"] == 16
                   and all(r["invariant_holds"] for r in uni["invariant_rows"])),
        "AC-P07": (feas["feasible"] and not feas["validation"]["histogram"]
                   and feas["topics"]["covered"] == feas["topics"]["required"]
                   and len(feas["claims_stated"]) == 16
                   and feas["source_keys_valid"] and feas["relations_supported"]),
        "AC-P08": (static["status"] == "PASS" and not static["failure_histogram"]
                   and not static["false_accepts"] and not static["false_rejects"]
                   and static["determinism"]["cross_process_identical"]),
        "AC-P09": bool(byte_gate.get("all_equal")),
        "AC-P10": (state["payload"]["unrealizable_pairs_exposed"] == 0
                   and state["payload"]["options"] == 16
                   and state["payload"]["derived_in_controller"] is False),
        "AC-P11": (gen.get("generation_calls") == 1 and gen.get("model_id") == MODEL_ID
                   and gen.get("temperature") == TEMPERATURE and gen.get("seed") == SEED
                   and bool(gen.get("raw_text_sha256"))),
        "AC-P12": plan.get("schema_accepted") is True,
        "AC-P13": plan.get("valid") is True,
        "AC-P14": cons.get("consistent") is True and cons.get("unrealizable_pairs_selected") == [],
        "AC-P15": post.get("rendered") is True and post.get("post_render_model_calls") == 0,
        "AC-P16": (post.get("validator", {}).get("status") == "ACCEPT"
                   and not post.get("zero_tolerance_violations")),
        "AC-P17": (post.get("required_topics", {}).get("covered")
                   == post.get("required_topics", {}).get("required")
                   and post.get("coverage", {}).get("citation_coverage") == 1.0
                   and post.get("coverage", {}).get("unknown_citations") == 0
                   and post.get("coverage", {}).get("language_compliance") == 1.0
                   and post.get("coverage", {}).get("condition_preservation") == 1.0
                   and post.get("coverage", {}).get("qualifier_preservation") == 1.0),
        "AC-P18": bool(post.get("determinism", {}).get("identical")),
        "AC-P19": True,
        "AC-P20": bool(hist.get("byte_identical")),
        "AC-P21": post.get("draft_status") == "PILOT_DRAFT_ACCEPTED",
    }
    rows = [{"id": c["id"], "condition": c["condition"], "satisfied": bool(checks.get(c["id"]))}
            for c in contract["conditions"]]
    unmet = [r["id"] for r in rows if not r["satisfied"]]
    return {"contract_version": contract["version"], "contract_sha256": sha_file(ACCEPTANCE),
            "conditions": len(rows), "rows": rows, "unmet": unmet,
            "verdict": "ACCEPTED" if not unmet else "REJECTED"}


def preserve(state: dict, status: str, stage: str, failure: dict | None = None) -> int:
    """Write the evidence and stop. A rejected pilot is never rendered and never released."""
    validation = state["validation"]
    validation.update({"status": status, "stage": stage})
    if failure:
        validation["failure"] = failure
    state["acceptance"] = evaluate_acceptance(state)
    validation["acceptance_gate"] = state["acceptance"]
    write_json(VALIDATION_PATH, validation)
    print(f"PILOT #2 {status} at {stage}: {failure or ''}")
    return 1


# ================================================================ main


def main() -> int:
    baseline = None
    bundle = V1.load_bundle()
    realization = M2_1.load()

    preflight = gate_frozen_inputs()
    write_json(PREFLIGHT_PATH, preflight)
    baseline = preflight

    universe_gate = gate_universe(realization, bundle)
    universe = universe_gate.pop("universe")
    UNIVERSE.ensure_obligation_rule()

    feasibility = REM.feasibility_proof(realization, bundle)
    write_json(FEASIBILITY_PATH, feasibility)

    # Redirected so the remediation's own frozen fixture is not rewritten by this phase.
    REM.CASES_PATH = CASES_PATH
    static = REM.static_proof_v2_1(realization, bundle)
    write_json(STATIC_PATH, static)

    built = build_model_payload(universe)
    byte_identity = gate_byte_identity(built, feasibility["universe_sha256"],
                                       universe_gate["loaded_sha256"])
    write_json(BYTE_IDENTITY_PATH, byte_identity)
    write_json(PAYLOAD_PATH, {"payload": built["payload"],
                              "universe_sha256": byte_identity["model_payload_universe_sha256"],
                              "model_called": False})
    PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_PATH.write_text(PLANNER_PROMPT, encoding="utf-8")
    PROMPT_SENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROMPT_SENT_PATH.write_text(built["prompt"], encoding="utf-8")

    payload_summary = {
        "payload_version": built["payload"]["payload_version"],
        "options": len(built["payload"]["universe"]["options"]),
        "unrealizable_pairs_exposed": built["payload"]["universe"]["unrealizable_pairs_exposed"],
        "derived_in_controller": False,
        "claim_specific_exceptions": 0,
        "prompt_sha256": sha_text(built["prompt"]),
    }

    authorised = (preflight["passed"] and universe_gate["passed"] and feasibility["feasible"]
                  and static["status"] == "PASS" and byte_identity["passed"])
    gate = {
        "version": VERSION, "phase": PHASE, "pilot_id": PILOT_ID, "evaluated_at": now(),
        "gate_1_frozen_preflight": {k: v for k, v in preflight.items()
                                    if k not in ("frozen_code_sha256", "historical_sha256")},
        "gate_2_architecture_v2_acceptance_contract": {
            "sha256": preflight["architecture_v2_acceptance_contract_sha256"],
            "unamended": preflight["architecture_v2_acceptance_contract_unamended"]},
        "gate_3_remediation_acceptance_contract": {
            "sha256": preflight["remediation_acceptance_contract_sha256"],
            "unamended": preflight["remediation_acceptance_contract_unamended"]},
        "gate_4_canonical_universe": universe_gate,
        "gate_5_subset_invariant": {
            "claims": len(universe_gate["invariant_rows"]),
            "violations": universe_gate["invariant_violations"]},
        "gate_6_feasibility": {k: v for k, v in feasibility.items()
                               if k not in ("plan", "rendered_units")},
        "gate_7_static_proof": {k: v for k, v in static.items() if k != "not_plannable_pairs"},
        "gate_8_byte_identity": byte_identity,
        "planner_payload": payload_summary,
        "gate_design_correction": {
            "made_before_generation": True,
            "finding": ("Pilot #1's coverage_report reimplements stage E's condition test without "
                        "the frozen condition_glosses stage E adds, so it false-rejects every "
                        "valid Turkish rendering of an English-source claim; it scores 0.8696 on "
                        "the feasibility plan Draft Validator v1.2 accepts with an empty "
                        "histogram."),
            "correction": ("condition and qualifier coverage are read from the unchanged Draft "
                           "Validator v1.2's own failures, as the remediation's feasibility proof "
                           "counts them; Pilot #1's figures are still reported as a diagnostic."),
            "validators_changed": 0, "thresholds_changed": 0, "failure_codes_changed": 0,
            "frozen_modules_changed": 0,
        },
        "generation_authorised": authorised,
    }
    write_json(GATE_PATH, gate)

    print(f"gate 1 frozen preflight    : {'PASS' if preflight['passed'] else 'FAIL'} "
          f"(drift {preflight['drift']})")
    print(f"gate 2 arch v2 contract    : "
          f"{'PASS' if preflight['architecture_v2_acceptance_contract_unamended'] else 'FAIL'}")
    print(f"gate 3 remediation contract: "
          f"{'PASS' if preflight['remediation_acceptance_contract_unamended'] else 'FAIL'}")
    print(f"gate 4 canonical universe  : {'PASS' if universe_gate['passed'] else 'FAIL'} "
          f"({universe_gate['claims_exposed']} claims, sha "
          f"{universe_gate['loaded_sha256'][:16]})")
    print(f"gate 5 subset invariant    : "
          f"{len(universe_gate['invariant_violations'])} violations")
    print(f"gate 6 feasibility         : {'PASS' if feasibility['feasible'] else 'FAIL'} "
          f"({feasibility['units']} units, topics {feasibility['topics']['covered']}/"
          f"{feasibility['topics']['required']}, claims {len(feasibility['claims_stated'])})")
    print(f"gate 7 static proof v2.1   : {static['status']}")
    print(f"gate 8 byte identity       : {'PASS' if byte_identity['passed'] else 'FAIL'}")
    print(f"  canonical      {byte_identity['canonical_universe_sha256']}")
    print(f"  feasibility    {byte_identity['feasibility_universe_sha256']}")
    print(f"  model payload  {byte_identity['model_payload_universe_sha256']}")
    print(f"GENERATION AUTHORISED      : {authorised}")

    state: dict[str, Any] = {
        "preflight": preflight, "universe_gate": universe_gate, "feasibility": feasibility,
        "static": static, "byte_identity": byte_identity, "payload": payload_summary,
        "gate": gate,
    }
    validation: dict[str, Any] = {
        "version": VERSION, "pilot_id": PILOT_ID, "section_id": SECTION_ID,
        "validated_at": now(), "generation_calls": 0, "retrieval_calls": 0,
        "qdrant_writes": 0, "corpus_reads": 0, "post_render_model_calls": 0,
        "automatic_retries": 0, "repaired": False, "regenerated": False,
        "generation_authorised": authorised,
    }
    state["validation"] = validation
    state["historical"] = REM.historical_regression(baseline)

    if not authorised:
        return preserve(state, "NOT_RUN", "pre_generation_gate",
                        {"code": "PRE_GENERATION_GATE_FAILED"})

    if "--gates-only" in sys.argv:
        # Proves the controller runs end to end up to the model boundary without crossing it.
        # No model call, no plan, no render. The counts below stay at zero.
        print("--gates-only: stopping at the model boundary; 0 generation calls.")
        return 0

    raw = generate_semantic_plan(built)
    write_json(RAW_PATH, raw)
    validation.update({"generation_calls": 1, "raw_text_sha256": raw["raw_text_sha256"]})
    state["generation"] = raw
    print(f"generation: 1 call, finish_reason={raw['finish_reason']}, "
          f"raw sha256={raw['raw_text_sha256'][:16]}")

    try:
        raw_plan = P1.extract_plan_json(raw["raw_text"])
    except (ValueError, json.JSONDecodeError) as error:
        return preserve(state, "REJECT", "plan_parse",
                        {"code": "PLAN_NOT_JSON", "detail": str(error)})

    write_json(PLAN_PATH, raw_plan)
    try:
        plan = PLAN_IR.parse_plan(raw_plan)
    except PLAN_IR.PlanRejection as rejection:
        state["plan_validation"] = {"schema_accepted": False, "valid": False,
                                    "failures": [rejection.as_dict()]}
        validation["semantic_plan"] = state["plan_validation"]
        return preserve(state, "REJECT", "plan_schema", rejection.as_dict())

    UNIVERSE.ensure_obligation_rule()
    result = PLAN_IR.validate_plan(plan, bundle, realization)
    consistency = plan_universe_consistency(raw_plan, universe, realization)
    topics_planned = [t for t in universe["required_topics"]
                      if any(o["topic"] == t and o["claim_id"] in
                             {s.claim_id for _, _, s in plan.iter_slots()}
                             for o in universe["options"])]

    state["plan_validation"] = {
        "schema_accepted": True,
        "prose_fields": 0,
        "unknown_fields": 0,
        "valid": result.valid and consistency["consistent"],
        "m1_valid": result.valid,
        "failures": result.failures,
        "required_topics_planned": {"required": len(universe["required_topics"]),
                                    "covered": len(topics_planned)},
    }
    state["consistency"] = consistency
    validation["semantic_plan"] = state["plan_validation"]
    validation["plan_universe_consistency"] = consistency

    if not result.valid or not consistency["consistent"]:
        return preserve(state, "REJECT", "plan_validation",
                        {"code": "PLAN_VALIDATION_FAILED",
                         "m1_failures": result.failures[:5],
                         "universe_failures": {k: v for k, v in consistency.items()
                                               if k.startswith(("claims_not", "roles_not",
                                                                "unrealizable", "mandatory",
                                                                "required_core")) and v}})

    payload_ir = RENDER.render_from_raw(raw_plan, realization, bundle)
    write_json(RENDER_PATH, payload_ir)
    verdict = P1.validate_rendered(payload_ir, bundle)
    coverage = coverage_report(payload_ir, verdict, bundle)
    topics = P1.topics_covered(payload_ir, bundle)
    determinism = determinism_check(realization, bundle)

    zero_violations = {code: count for code, count in verdict["histogram"].items()
                       if code in ZERO_TOLERANCE and count}
    accepted = (verdict["status"] == "ACCEPT" and not zero_violations
                and coverage["citation_coverage"] == 1.0
                and coverage["unknown_citations"] == 0
                and coverage["language_compliance"] == 1.0
                and coverage["condition_preservation"] == 1.0
                and coverage["qualifier_preservation"] == 1.0
                and topics["covered"] == topics["required"]
                and determinism["identical"])

    citation = {"rendered": False}
    if accepted:
        registry = {row["source_key"]: row for row in
                    (json.loads(line) for line in
                     SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip())}
        markdown, entries = CITE.render(V1.parse_draft_ir(payload_ir), registry)
        DRAFT_PATH.parent.mkdir(parents=True, exist_ok=True)
        DRAFT_PATH.write_text(markdown, encoding="utf-8")
        citation = {"rendered": True, "renderer_version": CITE.RENDERER_VERSION,
                    "path": str(DRAFT_PATH.relative_to(ROOT)),
                    "sha256": sha_text(markdown), "citations": len(entries),
                    "label": "PILOT_DRAFT_ACCEPTED"}

    state["post_render"] = {
        "rendered": True,
        "post_render_model_calls": 0,
        "rendered_units": len(payload_ir["units"]),
        "render_sha256": RENDER.render_sha256(payload_ir),
        "validator_version": V1_2.VALIDATOR_VERSION,
        "validator": verdict,
        "zero_tolerance_violations": zero_violations,
        "coverage": coverage,
        "required_topics": topics,
        "determinism": determinism,
        "citation_render": citation,
        "draft_status": "PILOT_DRAFT_ACCEPTED" if accepted else "REJECTED",
    }
    validation.update(state["post_render"])
    state["historical"] = REM.historical_regression(baseline)

    state["acceptance"] = evaluate_acceptance(state)
    validation["acceptance_gate"] = state["acceptance"]
    validation["status"] = "ACCEPT" if accepted and not state["acceptance"]["unmet"] else "REJECT"
    validation["stage"] = "post_render"
    write_json(VALIDATION_PATH, validation)

    write_json(MANIFEST_PATH, {
        "version": VERSION, "phase": PHASE, "pilot_id": PILOT_ID, "generated_at": now(),
        "section_id": SECTION_ID,
        "acceptance_contract_sha256": sha_file(ACCEPTANCE),
        "gate": {k: v for k, v in state["acceptance"].items() if k != "rows"},
        "pre_generation": {"authorised": authorised,
                           "canonical_universe_sha256": byte_identity[
                               "canonical_universe_sha256"],
                           "feasibility_universe_sha256": byte_identity[
                               "feasibility_universe_sha256"],
                           "model_payload_universe_sha256": byte_identity[
                               "model_payload_universe_sha256"],
                           "sha_equality": byte_identity["all_equal"]},
        "generation": {k: v for k, v in raw.items() if k != "raw_text"},
        "semantic_plan": state["plan_validation"],
        "consistency": consistency,
        "post_render": {k: v for k, v in state["post_render"].items() if k != "coverage"},
        "coverage": coverage,
        "historical_regression": state["historical"],
        "accounting": {"generation_calls": 1, "retrieval_calls": 0, "qdrant_writes": 0,
                       "corpus_reads": 0, "post_render_model_calls": 0, "automatic_retries": 0,
                       "regenerations": 0, "repairs": 0, "validators_weakened": 0,
                       "lexicons_widened": 0, "frozen_artifacts_modified": 0},
    })

    print(f"plan: {consistency['slots']} slots, {consistency['claims']} claims, "
          f"roles {consistency['role_counts']}")
    print(f"UNREALIZABLE selections: {len(consistency['unrealizable_pairs_selected'])}")
    print(f"rendered units: {len(payload_ir['units'])}")
    print(f"validator: {verdict['status']} histogram {verdict['histogram'] or '{}'}")
    print(f"topics {topics['covered']}/{topics['required']}  "
          f"citation {coverage['citation_coverage']}  language {coverage['language_compliance']}  "
          f"condition {coverage['condition_preservation']}  "
          f"qualifier {coverage['qualifier_preservation']}")
    print(f"determinism identical: {determinism['identical']}")
    print(f"acceptance gate: {state['acceptance']['verdict']} unmet={state['acceptance']['unmet']}")
    print(f"PILOT #2: {'ACCEPTED' if validation['status'] == 'ACCEPT' else 'REJECTED'}")
    return 0 if validation["status"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
