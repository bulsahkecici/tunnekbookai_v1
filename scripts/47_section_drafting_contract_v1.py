"""Section Drafting Contract v1 + Book Citation Rendering Contract v1 + SEC-02-2 pilot.

Ten phases of this project have been about evidence: is a claim supported, is it correctly scoped,
may two claims share a sentence. None of them wrote a word of the book, and the reason is that
prose introduces a failure the evidence layer cannot see. A claim is a proposition. A sentence is
a proposition plus everything the writer added to make it read well - a connective, an adjective, a
smoothing clause - and each of those additions is an unaudited assertion.

    Claim:    "Kuru Sistem: Çimento miktarı 350 kg/m³'ten az olmamalıdır."
    Sentence: "Kuru sistemde çimento dozajı, yeterli dayanım için 350 kg/m³'ün altına
               düşürülmemelidir."

The sentence is fluent, correctly cited and almost right. "Yeterli dayanım için" is a purpose no
source states. Nothing upstream of this phase can reject it, because at the level of the claim
nothing is wrong.

So this phase builds the bridge and then tests whether the bridge holds, in that order:

  1. **Section Drafting Contract v1** - what a drafter may do with an approved claim: paraphrase,
     reorganise, connect. And what it may not: add a proposition, strengthen a modality, drop a
     condition, convert a unit, infer a relation.

  2. **Book Citation Rendering Contract v1** - how a packet-local [E001] becomes a stable book
     reference, and, more importantly, what a reference may contain. The registry holds titles,
     section paths and page buckets. It holds no authors, publishers or years, so none appear.

  3. **Draft Validation Contract v1** - the nine stages every material unit passes, fail-closed,
     no auto-repair. A sentence that fails is reported as a failure rather than quietly rewritten
     until it passes, because a laundered draft is indistinguishable from a correct one.

Only then, and only if every fixture and test passes, one controlled SEC-02-2 pilot is generated.

Three decisions worth stating because they cost something:

**The model writes; it does not decide.** Claims, citations, numbers and provenance are supplied.
The model's entire job is Turkish sentence construction. It is not asked to select evidence, format
a reference or judge whether a sentence is supported - the three places where a fluent model is
most convincing and most wrong.

**No retry.** If the pilot fails, it fails. Regenerating at the same configuration until something
passes would make the acceptance gate measure persistence rather than correctness.

**SEC-02-2-P0-002 is withheld from the pilot.** The 360 kg/m³ general-concrete maximum is
allowlisted, composition-safe and SUPPORTED_CONTEXT - not required for any of the three required
topics. Its only safe rendering is inside a sentence that says, at length, that the figure does not
govern shotcrete. Handing that claim to a writer drafting a shotcrete section is inviting the exact
misattribution CF-P0-001 exists to prevent, for no coverage benefit. The enforcement machinery is
exercised in full by the fixtures and the required unit tests instead, where a wrong answer costs
nothing. §35 permits this: the draft need not use every claim.
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

DRAFTING_CONTRACT_VERSION = "tunnelbook-section-drafting-contract-v1"
CITATION_CONTRACT_VERSION = "tunnelbook-book-citation-rendering-contract-v1"
VALIDATION_CONTRACT_VERSION = "tunnelbook-draft-validation-contract-v1"
DRAFT_VALIDATOR_VERSION = "tunnelbook-section-draft-validator-v1"
CITATION_RENDERER_VERSION = "tunnelbook-book-citation-renderer-v1"
PARENT_VERSION = "tunnelbook-sec-02-2-limitation-resolution-v1"

SECTION_ID = "SEC-02-2"
SECTION_TITLE = "Püskürtme Beton: Malzeme ve Uygulama Gereklilikleri"
REQUIRED_TOPICS = ("çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı")
DRAFT_ID = "SEC-02-2-PILOT-V1"
DRAFT_VERSION = "v1"
LANGUAGE = "tr"

MODEL_ID = "qwen3.6-35b-a3b-mlx"
TEMPERATURE = 0.0
SEED = 11
MAX_TOKENS = 12288
# Attempt 1 of the pilot stopped at finish_reason='length' with a 4096-token ceiling: the DraftIR
# was well-formed and simply cut off mid-object. That is a harness failure, not a drafting one -
# the model never reached the end of what it was asked for - so the ceiling was raised and the
# truncated attempt preserved at raw/sec_02_2_draft_raw_attempt1_truncated_v1.json rather than
# discarded. Attempt 2 also emits a leaner unit shape; the fields dropped from the prompt are the
# ones the validator recomputes from the text anyway.
MAX_TOKENS_ATTEMPT_1 = 4096
LMSTUDIO_URL = "http://127.0.0.1:1234"
QDRANT_URL = "http://localhost:6333"

BOOK = ROOT / "data" / "book"
METADATA = ROOT / "data" / "metadata"
MANIFESTS = BOOK / "manifests"
RESOLUTION = BOOK / "sec_02_2_limitation_resolution"
DRAFTING = BOOK / "drafting"
CONTRACTS = DRAFTING / "contracts"
SECTION_DIR = DRAFTING / "sec_02_2"

DRAFTING_CONTRACT_PATH = CONTRACTS / "section_drafting_contract_v1.json"
CITATION_CONTRACT_PATH = CONTRACTS / "book_citation_rendering_contract_v1.json"
VALIDATION_CONTRACT_PATH = CONTRACTS / "draft_validation_contract_v1.json"
DRAFT_PLAN_PATH = SECTION_DIR / "draft_plan_v1.json"
AUTHORIZATION_PATH = SECTION_DIR / "draft_authorization_v1.json"
CITATION_MAP_PATH = SECTION_DIR / "citation_map_v1.json"
RAW_PATH = SECTION_DIR / "raw" / "sec_02_2_draft_raw_v1.json"
# Attempt 1 was preserved rather than overwritten. It stopped at finish_reason='length' against a
# 4096-token ceiling - a harness misconfiguration, not a drafting failure - and the phase's
# generation accounting names it explicitly rather than reporting a single clean call.
RAW_ATTEMPT_1_PATH = SECTION_DIR / "raw" / "sec_02_2_draft_raw_attempt1_truncated_v1.json"
ACCEPTED_PATH = SECTION_DIR / "accepted" / "sec_02_2_draft_ir_v1.json"
RENDERED_PATH = SECTION_DIR / "rendered" / "sec_02_2_pilot_v1.md"
AUDIT_PATH = SECTION_DIR / "audits" / "sec_02_2_draft_audit_v1.json"

DRAFTING_PROMPT_PATH = METADATA / "section_drafting_system_prompt_v1.txt"
DRAFT_FIXTURES_PATH = ROOT / "data" / "evaluation" / "section_drafting_contract_v1.jsonl"
CITATION_FIXTURES_PATH = ROOT / "data" / "evaluation" / "book_citation_rendering_v1.jsonl"
MANIFEST_PATH = MANIFESTS / "section_drafting_contract_v1.json"
REPORT_PATH = ROOT / "reports" / "section_drafting_contract_v1_sec_02_2.md"

ALLOWLIST_PATH = RESOLUTION / "claims" / "composition_safe_allowlist_v1.jsonl"
DENYLIST_PATH = RESOLUTION / "claims" / "composition_denylist_v1.jsonl"
PAIRS_PATH = RESOLUTION / "claims" / "claim_pair_constraints_v1.jsonl"
COMPOSITION_CONTRACT_PATH = (RESOLUTION / "contracts"
                             / "sec_02_2_claim_composition_contract_v1.json")
SAFETY_BUNDLE_PATH = RESOLUTION / "bundle" / "sec_02_2_drafting_safety_bundle_v1.json"
COMPOSITION_VALIDATOR_PATH = ROOT / "scripts" / "46_sec_02_2_claim_composition_validator_v1.py"
DRAFT_VALIDATOR_PATH = ROOT / "scripts" / "49_section_draft_validator_v1.py"
CITATION_RENDERER_PATH = ROOT / "scripts" / "48_book_citation_renderer_v1.py"
CONTROLLER_PATH = ROOT / "scripts" / "47_section_drafting_contract_v1.py"
PROMPT_V5_PATH = METADATA / "generation_system_prompt_v5.txt"
OUTPUT_CONTRACT_PATH = ROOT / "scripts" / "31_generation_output_contract_v1_1.py"
GENERATOR_PATH = ROOT / "scripts" / "36_production_grounded_generator.py"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str | None:
    return sha_text(path.read_text(encoding="utf-8")) if path.exists() else None


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
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


_MODULES: dict[str, Any] = {}


def _validator():
    """The draft validator, loaded once. Both this module and the renderer depend on it."""
    if "validator" not in _MODULES:
        _MODULES["validator"] = _load("section_draft_validator_v1",
                                      "scripts/49_section_draft_validator_v1.py")
    return _MODULES["validator"]


def _renderer():
    if "renderer" not in _MODULES:
        _MODULES["renderer"] = _load("book_citation_renderer_v1",
                                     "scripts/48_book_citation_renderer_v1.py")
    return _MODULES["renderer"]


# ================================================================ 1. lexicons

# Grammar, not content. Every word here is one a Turkish technical sentence needs in order to be a
# sentence; none of them asserts anything. The line is load-bearing: a technical noun that slipped
# in here would be licensed in every unit of the book, and the support check would stop working
# without ever failing.
FUNCTION_LEXICON = [
    "ile", "için", "olan", "olarak", "olup", "olması", "olmak", "olmakla", "bulunan", "bulunur",
    "ayrıca", "ise", "göre", "kadar", "sonra", "önce", "arasında", "üzerine", "üzerinde",
    "altında", "gibi", "daha", "çok", "bazı", "hem", "veya", "ya", "bunun", "bunlar", "bunların",
    "şekilde", "biçimde", "durumda", "durumlarda", "durumunda", "halinde", "koşulda", "edilen",
    "edilir", "eder", "ederek", "ancak", "bu", "şu", "bir", "birer", "iki", "üç", "adet",
    "aynı", "farklı", "genel", "özel", "diğer", "yer", "yeri", "yerine",
    "ila", "arası", "arasındaki", "bunu", "buna", "bunda", "onu", "ona", "şunu",
    "kendi", "söz", "konusu", "yani", "böyle", "böylece", "burada", "aşağıda", "yukarıda",
    "bölüm", "bölümde", "bölümü", "başlık", "başlıkta", "başlık", "kısım", "ele", "alınmaktadır",
    "alınmıştır", "verilmiştir", "gösterilmiştir", "açıklanmaktadır", "değerlendirilmektedir",
    "ilgili", "ilişkin", "dair", "karşı", "doğru", "boyunca", "birlikte", "ayrı", "ayrıca",
    "vardır", "yoktur", "değildir", "değil", "olmayan", "olmadan", "olmadığı", "olduğu",
    "ilk", "son", "sonraki", "önceki", "takip", "eden", "müteakip", "izleyen",
    "not", "the", "and", "for", "with", "from", "that", "this", "are", "may", "can", "shall",
]

# Semantically neutral wordings the drafter may substitute. Every pair is the same proposition in
# different words - a synonym table, never a softening: nothing here changes a number, a scope or
# a normative force. Absence from this table does not forbid a paraphrase; the prefix-agreement
# rule already licenses inflection. This covers the cases inflection cannot reach.
PARAPHRASE_LEXICON = {
    "beton": ["betonu", "betonun", "betonlar"],
    "püskürtme": ["püskürtülen", "püskürtülmüş", "püskürtülecek"],
    "kalınlık": ["kalınlığı", "kalınlıkta", "kalınlıklar", "kalınlığın"],
    "dayanım": ["dayanımı", "dayanımın", "mukavemet", "mukavemeti"],
    "miktar": ["miktarı", "miktarın", "dozaj", "dozajı", "dozajın"],
    "sınıf": ["sınıfı", "sınıfında", "sınıflar"],
    "tabaka": ["tabakalar", "tabakanın", "katman", "katmanı", "katmanlar", "katmanın"],
    "katman": ["katmanı", "katmanlar", "tabaka", "tabakalar"],
    "uygulama": ["uygulanan", "uygulanır", "uygulanacak", "uygulanması", "uygulamalarda"],
    "geçmeyecektir": ["aşmayacaktır", "geçmemelidir", "aşmamalıdır"],
    "olmamalıdır": ["olmayacaktır", "altında", "altına", "düşmemelidir", "düşürülmemelidir",
                     "inmemelidir"],
    "kalmamalıdır": ["düşmemelidir", "inmemelidir", "altına"],
    "geçecek": ["örtecek", "örten", "kapatacak"],
    "minimum": ["asgari", "alt", "sınır"],
    "maksimum": ["azami", "üst"],
    "sistem": ["sistemde", "sistemi", "sistemin"],
    "hızlandırıcı": ["hızlandırıcının", "hızlandırıcılı", "hızlandırıcısız"],
    "süre": ["süresi", "süresinin", "sürede"],
    "koşul": ["koşullar", "koşullarda", "şart", "şartlar", "şartlarda"],
    "numune": ["numuneler", "numunede", "numunesi"],
    "grup": ["grubun", "grubu", "gruplar"],
    "ortalama": ["ortalaması", "ortalamanın"],
    "bireysel": ["tekil", "tek"],
    "gün": ["günlük", "günde", "günü"],
    "saat": ["saatte", "saatlik", "saati"],
    "sıcaklık": ["sıcaklıkta", "sıcaklığı", "derece"],
    "zon": ["zonu", "zonlu", "zonlarda", "bölge", "bölgesi"],
    "kil": ["killi"],
    "lif": ["lifli", "life", "takviyeli", "takviye"],
    "durabilite": ["dayanıklılık", "kalıcılık"],
    "onay": ["onayı", "onayıyla", "onayla"],
    "idare": ["idarenin", "idarece"],
    "azaltılabilmektedir": ["azaltılabilir", "düşürülebilir", "düşürülebilmektedir"],
    "iksa": ["iksada"],
    "şev": ["şevde", "şevlerde"],
    "kaplama": ["kaplamada", "kaplamanın", "kaplamalar"],
    "aranmaktadır": ["aranır", "öngörülür", "öngörülmektedir"],
    "öngörülmüştür": ["öngörülmektedir", "belirlenmiştir", "tanımlanmıştır"],
}

# English-source claims may be rendered in Turkish (§109). The gloss is a translation of the
# claim's own words, added token by token, and it adds no proposition: 'squeezing rock' becomes
# 'sıkışan kaya' and nothing else. Every entry here is checked against its claim's canonical text
# by the test suite, so a gloss cannot smuggle in a concept the source does not contain.
TRANSLATION_GLOSSES = {
    "SEC-02-2-P0-007": ["tipik", "kalınlık", "kalınlığı", "ilk", "birincil", "püskürtme", "beton",
                        "kaplama", "kaplamanın", "arasında", "değişmektedir", "değişir", "zemin",
                        "koşullarına", "koşulları", "tünel", "açıklığının", "açıklık", "boyutuna",
                        "boyut", "bağlı", "inç", "milimetre", "aralığında"],
    "SEC-02-2-P0-008": ["bazı", "belirli", "kaya", "koşullarında", "koşulları", "ezilmiş",
                        "parçalanmış", "sıkışan", "sıkışma", "kalınlık", "kalınlığı", "daha",
                        "fazla", "olabilmektedir", "olabilir", "tünel", "boyutuna", "bağlı",
                        "inç", "milimetre"],
    "SEC-02-2-R025": ["flashcrete", "aktif", "destek", "sayılmaz", "kabul", "edilmez", "normalde",
                      "genellikle", "sistematik", "uygulanan", "ilk", "birincil", "püskürtme",
                      "beton", "kaplama", "kaplamanın", "ardından", "takip"],
}

# Turkish anchors for conditions stated in English. A condition on an English claim cannot
# survive into Turkish prose as its own words, so the equivalents are declared here rather than
# inferred at match time. Each entry is a translation of the condition and nothing more - the test
# suite checks that every gloss token traces to the condition it glosses.
CONDITION_GLOSSES = {
    "SEC-02-2-P0-007": {
        "depending on ground conditions and size of the tunnel opening":
            ["zemin", "koşul", "koşullarına", "tünel", "açıklık", "açıklığının", "boyut",
             "boyutuna"],
    },
    "SEC-02-2-P0-008": {
        "In some": ["bazı", "belirli", "kimi"],
        "dependent on tunnel size": ["tünel", "boyut", "boyutuna", "büyüklük", "büyüklüğüne"],
    },
}

# Propositions no SEC-02-2 claim makes. Each family is checked only where the declared claims do
# not themselves license the word: two claims genuinely use 'yeterli' and 'nedeniyle', and a flat
# ban would reject the source's own wording. The build-time audit records which markers appear
# anywhere in the claim corpus so that exemption stays visible rather than silent.
PROHIBITED_MARKERS = {
    "expansion": [
        "optimum", "ideal", "en iyi", "en uygun", "en ekonomik", "ekonomik", "elverişli",
        "yeterlidir", "yeterlidir ki", "güvenli", "güvenlidir", "emniyetli", "avantaj",
        "avantajlı", "üstün", "üstünlük", "gereksiz", "kolay", "kolaylıkla", "zor", "pratik",
        "verimli", "etkili", "etkin", "başarılı", "uygun maliyet", "tercih edilir düzey",
        "en yaygın", "yaygın olarak kabul", "standart uygulama haline",
        "optimal", "best", "most economical", "sufficient for", "safe value",
    ],
    "causal": [
        "çünkü", "zira", "dolayısıyla", "bu nedenle", "bu sebeple", "bu yüzden", "sonuç olarak",
        "sağladığı için", "olduğundan", "sayesinde", "amacıyla belirlenmiştir", "gerektiği için",
        "bunun sonucunda", "buna bağlı olarak", "therefore", "because", "hence", "thus",
        "as a result", "consequently",
    ],
    "universal": [
        "her zaman", "daima", "her koşulda", "bütün koşullarda", "tüm koşullarda",
        "tüm", "bütün", "her türlü koşul",
        "her durumda", "bütün durumlarda", "tüm durumlarda", "her tür", "her türlü",
        "istisnasız", "kesinlikle", "asla", "hiçbir koşulda", "mutlaka", "şüphesiz",
        "bilinmektedir", "kanıtlanmıştır", "ispatlanmıştır", "genel kabul görmüştür",
        "always", "in all conditions", "never", "proven", "it is well known",
    ],
}

# Normative force, weakest to strongest. A drafted unit may sit at or below the level its claims
# state and never above it: 'tavsiye edilen' -> 'zorunludur' is the drift this lattice exists to
# catch, and it is a drift a fluent paraphrase makes easily.
MODALITY_LATTICE = {
    "bound_words_excluded": ["minimum", "maksimum", "asgari", "azami", "en az", "en fazla"],
    "bound_words_rationale":
        "'minimum' and 'maksimum' state which side of a value a requirement lies on, not how "
        "binding it is. Scoring them as obligation makes SEC-02-2-C-011 - a recommendation that "
        "happens to name a maximum - look binding, and the lattice then cannot see a drafter turn "
        "'tavsiye edilen' into 'zorundadır'. Bound direction is checked by support containment "
        "instead: 'maksimum' written against a claim stating a minimum is a word the claim does "
        "not license.",
    "levels": {
        "0": "PERMISSIVE - something is allowed or possible",
        "1": "TYPICAL - descriptive, habitual or approximate",
        "2": "RECOMMENDED - preferred but not binding",
        "3": "REQUIRED - binding obligation or hard limit",
    },
    "markers": {
        "0": ["olabilir", "olabilmektedir", "azaltılabilmektedir", "azaltılabilir",
              "düşürülebilir", "kullanılabilir", "yapılabilir", "may be", "can be"],
        "1": ["genellikle", "tipik", "tipik olarak", "yaklaşık", "civarında", "ortalama olarak",
              "normalde", "çoğunlukla", "typical", "typically", "normally", "approximately",
              "ranges from", "kullanılır", "kullanılmaktadır", "yapılır", "değişmektedir"],
        "2": ["tavsiye", "tavsiye edilen", "tavsiye edilir", "önerilen", "önerilir", "tercihen",
              "tercih edilmelidir", "tercih edilir", "olmalıdır", "olmalı", "should",
              "recommended", "preferably"],
        "3": ["zorunludur", "zorundadır", "zorunda", "mecburiyetindedir", "şarttır",
              "gereklidir", "mecburidir", "olacaktır", "olmayacaktır",
              "olmamalıdır", "geçmeyecektir", "aşmayacaktır", "uygulanmayacaktır",
              "tamamlanmış olacaktır", "aranmaktadır", "aranır", "öngörülmüştür",
              "öngörülmektedir", "must", "shall", "mandatory", "required", "not exceed",
              "az olmamalıdır", "altında kalmamalıdır", "geçmemelidir"],
    },
    # Turkish puts obligation in a suffix as readily as in a word. 'azaltılmalıdır' is a
    # recommendation and 'azaltılabilmektedir' is a permission; they differ by four letters inside
    # a verb, and a word-initial matcher cannot tell them apart.
    "suffix_markers": {
        "0": ["abilir", "ebilir", "abilmektedir", "ebilmektedir"],
        "2": ["malıdır", "melidir", "malı", "meli"],
        "3": ["mamalıdır", "memelidir", "mayacaktır", "meyecektir", "malıdır ki"],
    },
}

# Pipeline vocabulary. If any of this reaches the page, the reader is being shown the machinery
# instead of the engineering (§39).
FORBIDDEN_PROSE_MARKERS = [
    "kaynaklara göre", "elimizdeki kanıtlar", "kanıt notu", "evidence note", "claim id",
    "claim_id", "rag", "retrieval", "packet", "allowlist", "denylist", "draftir", "draft ir",
    "modelin bilgisine göre", "sistem tarafından", "yukarıdaki kanıt", "verilen kanıt",
]


# ================================================================ 2. contract authoring

def build_drafting_contract(allowlist: list[dict]) -> dict:
    """Section Drafting Contract v1 - what a drafter may and may not do with an approved claim."""
    return {
        "version": DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "section_title": SECTION_TITLE,
        "scope": "SEC-02-2 only. Widening this contract to other sections is a later phase's "
                 "decision and must be made explicitly, not inherited.",
        "authored_at": now(),
        "authored_by": DRAFTING_CONTRACT_VERSION,
        "parent_version": PARENT_VERSION,
        "core_principle":
            "The drafter may reorganise and stylistically connect supported facts. It may not "
            "create a factual proposition or logical relationship that is not represented in the "
            "approved claim universe.",
        "drafting_input": {
            "supplied": ["section plan", "composition-safe claim allowlist", "claim scope "
                         "metadata", "claim pair constraints", "mandatory qualifier rules",
                         "forbidden synthesis rules", "derived numeric rules",
                         "citation binding instructions"],
            "withheld": ["raw corpus", "retrieval", "general model knowledge", "the web",
                         "denylisted claim text", "bibliography metadata"],
            "note": "Denylisted claim text is withheld rather than supplied as a negative "
                    "example. A model shown a prohibited sentence and told not to write it has "
                    "been shown a prohibited sentence.",
        },
        "material_sentence_definition": [
            "technical fact", "numeric value", "requirement", "recommendation", "definition",
            "classification", "scope", "condition", "method", "comparison", "cause/effect",
            "exception", "performance property",
        ],
        "non_material_allowance": {
            "permitted_without_claims": ["pure transition", "organisational navigation",
                                         "non-factual signposting", "headings"],
            "constraint": "A transition must not imply a technical relation. A non-material unit "
                          "that carries a figure, a normative marker or a claim binding is "
                          "misclassified, not exempt.",
        },
        "unit_types": list(_validator().UNIT_TYPES),
        "relationship_types": {
            "allowed": list(_validator().ALLOWED_RELATIONSHIPS),
            "forbidden": list(_validator().FORBIDDEN_RELATIONSHIPS),
        },
        "unit_id_grammar": {
            "unit": "^U-[A-Za-z0-9]+-P\\d{2}-S\\d{2}$",
            "paragraph": "^(U-[A-Za-z0-9]+-P\\d{2})-S\\d{2}$",
            "rationale": "Paragraph identity has to be recoverable from the unit id, because "
                         "§25 requires validation across adjacent sentences: a prohibited "
                         "relationship must not become legal by being split across a full stop "
                         "and rejoined with a connective.",
        },
        "claim_use": {
            "allowlist_only": True,
            "denylist_is_hard_reject": True,
            "paraphrase_permitted": True,
            "expansion_permitted": False,
            "expansion_examples_not_licensed_by_minimum_350": [
                "350 kg/m³ optimum değerdir",
                "350 kg/m³ güvenli değerdir",
                "350 kg/m³ çoğu projede yeterlidir",
            ],
        },
        "modality_policy": {
            "preserve": ["must", "shall", "should", "may", "recommended", "minimum", "maximum",
                         "typical", "approximately", "zorunlu", "olacaktır", "olmalıdır",
                         "tavsiye edilen", "genellikle", "yaklaşık", "asgari", "azami"],
            "strengthening_forbidden": ["recommended -> required", "should -> must",
                                        "typical -> mandatory", "tavsiye edilen -> zorunludur",
                                        "genellikle -> her zaman"],
        },
        "condition_policy": {
            "rule": "A material source condition must survive into prose.",
            "unit_scope": "A condition whose anchors appear in the claim's own canonical wording "
                          "must appear in the drafting unit.",
            "paragraph_scope": "A condition carried by surrounding source context rather than by "
                               "the claim's own sentence must appear in the paragraph.",
            "rationale": "SEC-02-2-P0-001 holds only 'özel uygulamalar dışında', but its "
                         "canonical text never says so - the carve-out is a neighbouring clause. "
                         "Demanding it inside the sentence would reject a faithful paraphrase of "
                         "the source, so the rule follows the claim's own wording rather than a "
                         "uniform strictness that happens to be wrong.",
            "must_not_detach_from": ["system", "material", "rock condition", "temperature",
                                     "construction stage", "application method",
                                     "source/table scope", "approval condition"],
        },
        "derived_numeric_policy": {
            "default": "SOURCE_STATED_ONLY",
            "cm_15_single_pass": "allowed when bound to SEC-02-2-C-003",
            "mm_150_derived": "forbidden as a rendering of the 15 cm single-pass claim",
            "mm_150_source_stated": "allowed through SEC-02-2-C-009 (clay-zone first layer), "
                                    "which states 100-150 mm in the source's own units",
            "resolution": "claim identity plus context, never a global ban on the string",
            "strength_class": "C25/30 is a designation, not a quantity. It is never normalised "
                              "into an MPa number.",
        },
        "quotation_policy": {
            "default": "PARAPHRASE",
            "direct_quotation": "not used in v1",
            "rationale": "A book assembled from copied source sentences is a patchwork, and "
                         "traceability does not require quotation - it requires citation.",
        },
        "cross_lingual_policy": {
            "permitted": "faithful Turkish paraphrase of an English claim",
            "forbidden": ["strengthening the claim", "dropping conditions",
                          "changing numeric values", "adding interpretation"],
            "citation": "the Turkish paraphrase cites the original source key",
        },
        "style": {
            "language": LANGUAGE,
            "register": "technical textbook / engineering reference",
            "audience": "civil and tunnel engineering readers",
            "tone": ["clear", "professional", "non-promotional", "non-chatty",
                     "non-conversational"],
            "claim_density": "one atomic technical proposition per sentence, or a "
                             "source-supported pair",
        },
        "function_lexicon": FUNCTION_LEXICON,
        "paraphrase_lexicon": PARAPHRASE_LEXICON,
        "translation_glosses": TRANSLATION_GLOSSES,
        "condition_glosses": CONDITION_GLOSSES,
        "prohibited_markers": PROHIBITED_MARKERS,
        "modality_lattice": MODALITY_LATTICE,
        "forbidden_prose_markers": FORBIDDEN_PROSE_MARKERS,
        "support_test": {
            "method": "lexical containment against the declared claims",
            "morphology": "five-character common prefix agreement",
            "morphology_rationale": "'kalınlık' and 'kalınlığı' agree on six characters across "
                                    "the k->ğ mutation that a suffix stripper would have to "
                                    "special-case. The rule over-licenses occasionally, which is "
                                    "the safe direction; it never under-licenses a true "
                                    "inflection.",
            "pooling": "per-unit, over declared claims only - never section-wide",
            "pooling_rationale": "A section-wide pool would let a sentence about layer thickness "
                                 "borrow the vocabulary of a cement-dosage claim it never cited, "
                                 "which is claim-bound drafting undone by a convenience.",
        },
        "determinism": {"temperature": TEMPERATURE, "seed": SEED, "model_id": MODEL_ID},
        "prohibitions": [
            "no new factual proposition", "no inferred relationship", "no external knowledge",
            "no scope loss", "no numeric drift", "no unit conversion presented as source-stated",
            "no modality strengthening", "no dropped condition", "no dropped mandatory qualifier",
            "no invented citation", "no invented bibliography metadata",
            "no packet-local evidence handle in prose", "no internal identifier in prose",
            "no silent repair of a failed unit",
        ],
        "failure_mode": "fail_closed_no_auto_repair",
    }


def build_citation_contract(registry: dict[str, dict], used_keys: list[str]) -> dict:
    """Book Citation Rendering Contract v1 - stable identity in, honest reference out."""
    return {
        "version": CITATION_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "authored_at": now(),
        "authored_by": CITATION_CONTRACT_VERSION,
        "core_principle":
            "A bibliography entry is a claim about the world. It may contain only metadata the "
            "frozen registry actually holds.",
        "identity": {
            "book_reference_resolves_through": "source_key",
            "source_key_form": "SRC-<document_id>-<hash12>",
            "packet_local_handles_are_not_identities": True,
            "rationale": "[E001] is a position in a retrieval packet, not a document. Two packets "
                         "built for two questions put different sources at [E001], so a book "
                         "reference built on one is stable only until retrieval runs again.",
            "eids_in_prose": "0 permitted, checked on the rendered bytes",
        },
        "registries": [str(p.relative_to(ROOT)) for p in _validator().REGISTRY_PATHS],
        "registry_union_note":
            "SEC-02-2 straddles two frozen registries: the 360 kg/m³ claim's provenance was "
            "registered by the P0 gap-resolution phase and is absent from the base registry. A "
            "renderer reading only the base file would report a true, frozen source as unknown.",
        "display_style": {
            "in_text_marker": "numbered endnote marker in square brackets, e.g. [1]",
            "multiple_sources": "ascending, comma-joined inside one bracket, e.g. [2,3]",
            "placement": "immediately after the proposition it supports, following terminal "
                         "punctuation",
            "reference_section_heading": "Kaynaklar",
        },
        "numbering": {
            "assigned_by": "first appearance in accepted prose",
            "deduplication": "one number per source_key within the section",
            "determinism": "byte-identical DraftIR renders byte-identical Markdown",
            "rationale": "Numbering by first appearance rather than by lexical key order means a "
                         "reader following [1] meets the first reference in the text, not the "
                         "one whose hash sorts first.",
        },
        "metadata_policy": {
            "permitted_fields": ["title", "section_path", "page_start", "page_end",
                                 "slide_start", "slide_end", "document_id", "citation_mode",
                                 "provenance_status", "language"],
            "never_invented": ["author", "organisation", "publication year", "publisher",
                               "edition", "URL", "standard number", "document title",
                               "page number"],
            "missing_metadata": "omit the field entirely; render only what is known",
            "no_fake_precision": "A page range is rendered at the precision the registry holds. "
                                 "The SEC-02-2 rows carry 25-page buckets, so they render as "
                                 "ranges ('s. 226-250'). Narrowing one to 's. 231' would be "
                                 "indistinguishable from real page-level provenance and is "
                                 "forbidden.",
            "no_title_is_a_refusal": "A registry row without a title cannot be rendered at all. "
                                     "The renderer raises rather than substituting a filename.",
        },
        "coverage_requirements": {
            "material_units_cited": "100%",
            "citation_resolution": "100% of markers resolve to a registered source_key",
            "unknown_source_keys_permitted": 0,
        },
        "section_source_keys": sorted(used_keys),
        "section_reference_preview": {
            key: _renderer().format_reference(registry[key])
            for key in sorted(used_keys) if key in registry
        },
    }


def build_validation_contract() -> dict:
    """Draft Validation Contract v1 - the nine stages and what each of them may reject for."""
    validator = _validator()
    return {
        "version": VALIDATION_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "authored_at": now(),
        "authored_by": VALIDATION_CONTRACT_VERSION,
        "validator_implementation": str(DRAFT_VALIDATOR_PATH.relative_to(ROOT)),
        "validator_version": DRAFT_VALIDATOR_VERSION,
        "pipeline": [
            {"stage": "A_allowlist", "checks": "every declared claim is composition-safe and "
             "allowlisted", "codes": ["CLAIM_NOT_ALLOWLISTED"]},
            {"stage": "B_denylist", "checks": "no declared claim is denylisted",
             "codes": ["CLAIM_DENYLISTED"]},
            {"stage": "C_support", "checks": "no proposition beyond what the declared claims "
             "license", "codes": ["UNSUPPORTED_PROPOSITION", "CLAIM_EXPANSION"]},
            {"stage": "D_numeric", "checks": "every figure and unit traces to a declared claim",
             "codes": ["NUMERIC_DRIFT", "UNIT_DRIFT"]},
            {"stage": "E_conditions", "checks": "conditions and qualifiers survive; modality does "
             "not gain force", "codes": ["CONDITION_DROPPED", "QUALIFIER_DROPPED",
                                         "MODALITY_DRIFT"]},
            {"stage": "F_composition", "checks": "delegated to the frozen SEC-02-2 composition "
             "validator, at both unit and paragraph scope",
             "codes": ["FORBIDDEN_SYNTHESIS", "UNSUPPORTED_RELATION",
                       "DERIVED_VALUE_AS_SOURCE_STATED", "QUALIFIER_DROPPED"]},
            {"stage": "G_sources", "checks": "every claim binds to its own registered source key",
             "codes": ["MISSING_SOURCE_KEY", "UNKNOWN_SOURCE_KEY", "CITATION_SCOPE_MISMATCH",
                       "NON_MATERIAL_MISCLASSIFIED"]},
            {"stage": "H_citation", "checks": "every material unit is claim-bound and cited",
             "codes": ["MISSING_CITATION"]},
            {"stage": "I_rendering", "checks": "no internal identifier or pipeline vocabulary in "
             "visible prose", "codes": ["PACKET_EID_LEAK", "INTERNAL_ID_LEAK"]},
        ],
        "delegation_note":
            "Stage F delegates to scripts/46 rather than re-encoding its rules. A second copy of "
            "the composition rules would be unversioned and could drift out of agreement with the "
            "one whose 71-case regression is the evidence that it works.",
        "rejection_codes": list(validator.REJECTION_CODES),
        "composition_code_map": dict(validator.COMPOSITION_CODE_MAP),
        "policy": {
            "fail_closed": True,
            "auto_repair": False,
            "auto_repair_rationale":
                "A failed sentence must be visible as a failure. Asking the generator to fix it "
                "inside the same attempt launders an unsupported proposition into an apparently "
                "successful draft, and the audit trail then records a pass.",
            "unit_result": ["ACCEPT", "REJECT"],
            "pilot_policy": "all_or_nothing",
            "pilot_policy_rationale":
                "In v1 an optional rejected unit rejects the whole pilot rather than being "
                "dropped. Silently discarding failures would make the acceptance rate a function "
                "of how much prose was thrown away.",
            "retry_same_config": 0,
        },
    }


# ================================================================ 3. draft plan

# The pilot's claim allocation. Chosen for coherent technical coverage of the three required
# topics, not for maximal claim usage (§35). Steel-mesh claims are excluded: they are allowlisted
# and true, but they belong to reinforcement rather than to this section's subject, and padding a
# pilot with off-topic material tests nothing except the drafter's willingness to pad.
SUBSECTION_PLAN = [
    {
        "subsection_id": "A",
        "title": "Püskürtme Betonun Malzeme ve Dayanım Gereklilikleri",
        "goal": "Establish the strength class the specification binds, and the acceptance "
                "criteria by which it is verified.",
        "claim_ids": ["SEC-02-2-C-001", "SEC-02-2-C-002"],
        "required_topic": "dayanım sınıfı",
    },
    {
        "subsection_id": "B",
        "title": "Çimento Dozajı",
        "goal": "State the dry- and wet-system cement minimums with their systems named, the "
                "durability floor, and the approval-bound reduction for special applications.",
        "claim_ids": ["SEC-02-2-R001", "SEC-02-2-P0-001", "SEC-02-2-P0-006",
                      "SEC-02-2-P0-005", "SEC-02-2-P0-004"],
        "required_topic": "çimento dozajı",
    },
    {
        "subsection_id": "C",
        "title": "Kaplama Kalınlığı ve Katman Düzeni",
        "goal": "Give the typical initial-lining thickness range, the single-pass maximum, and "
                "the layer sequence from first to subsequent layers.",
        "claim_ids": ["SEC-02-2-P0-007", "SEC-02-2-P0-008", "SEC-02-2-C-003", "SEC-02-2-C-004",
                      "SEC-02-2-C-005", "SEC-02-2-C-007"],
        "required_topic": "kaplama kalınlığı",
    },
    {
        "subsection_id": "D",
        "title": "Uygulama Koşulları ve Özel Durumlar",
        "goal": "Cover the strength precondition for the next layer, the accelerator-free waiting "
                "time, and the clay-zone first-layer case.",
        "claim_ids": ["SEC-02-2-C-006", "SEC-02-2-C-012", "SEC-02-2-C-009"],
        "required_topic": None,
    },
]

EXCLUDED_CLAIMS = {
    "SEC-02-2-P0-002":
        "The 360 kg/m³ general-concrete maximum from Tablo-308-23-b. Allowlisted, "
        "composition-safe and SUPPORTED_CONTEXT - required for no topic. Its only safe rendering "
        "is a sentence stating at length that the figure does not govern shotcrete, and handing "
        "it to a writer drafting a shotcrete section invites exactly the misattribution CF-P0-001 "
        "exists to prevent, for no coverage gain. The enforcement machinery is exercised by the "
        "fixtures and required unit tests instead, where being wrong costs nothing.",
    "SEC-02-2-C-008":
        "Two-phase steel-fibre application to minimise rebound. Optional enrichment; overlaps "
        "subsection C without adding required coverage.",
    "SEC-02-2-C-010":
        "Repair-work cover thicknesses over reinforcement. A different construction activity from "
        "this section's subject.",
    "SEC-02-2-C-011":
        "Repair-work thicknesses without reinforcement. Same reason as SEC-02-2-C-010.",
    "SEC-02-2-C-013": "Steel mesh bar counts - reinforcement, not shotcrete material or "
                      "application.",
    "SEC-02-2-C-014": "Steel mesh bar counts - reinforcement, not shotcrete material or "
                      "application.",
    "SEC-02-2-C-015": "Steel mesh types - reinforcement, not shotcrete material or application.",
    "SEC-02-2-C-016": "Steel mesh dimensions and TS 4559 - reinforcement, not shotcrete.",
    "SEC-02-2-C-017": "A single mine's mesh specification. Site-specific practice, not a "
                      "requirement; qualified as such on the allowlist.",
    "SEC-02-2-R025": "Flashcrete's status as non-active support. Correct and cited, but it "
                     "introduces a support category this section does not otherwise define.",
}


def build_draft_plan(allowlist: dict[str, dict]) -> dict:
    allocation = {}
    for subsection in SUBSECTION_PLAN:
        for claim_id in subsection["claim_ids"]:
            allocation.setdefault(subsection["subsection_id"], []).append(claim_id)
    used = [cid for sub in SUBSECTION_PLAN for cid in sub["claim_ids"]]
    topics = {}
    for topic in REQUIRED_TOPICS:
        core = [cid for cid in used
                if (allowlist[cid].get("topic") == topic
                    and allowlist[cid].get("readiness_use") == "REQUIRED_CORE")]
        topics[topic] = {"claim_ids": [cid for cid in used
                                       if allowlist[cid].get("topic") == topic],
                         "required_core_claim_ids": core,
                         "covered": bool(core)}
    return {
        "version": DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "section_title": SECTION_TITLE,
        "draft_id": DRAFT_ID,
        "language": LANGUAGE,
        "authored_at": now(),
        "section_goal":
            "Set out, for a tunnel-engineering reader, what the specifications require of "
            "shotcrete as a material and of its application: the binding strength class and its "
            "acceptance criteria, the cement dosage minimums by system, the layer thicknesses and "
            "their sequence, and the conditions that govern when a layer may follow another.",
        "subsections": SUBSECTION_PLAN,
        "required_topics": {"required": list(REQUIRED_TOPICS), "coverage": topics,
                            "all_covered": all(t["covered"] for t in topics.values())},
        "claim_allocation": allocation,
        "optional_claims": [],
        "excluded_claims": EXCLUDED_CLAIMS,
        "claim_count": {"available": len(allowlist), "allocated": len(used),
                        "excluded": len(EXCLUDED_CLAIMS)},
        "composition_constraints": {
            "pair_constraints": [row["constraint_id"] for row in read_jsonl(PAIRS_PATH)],
            "active_for_allocated_claims": [
                row["constraint_id"] for row in read_jsonl(PAIRS_PATH)
                if row["left_claim_id"] in used and row["right_claim_id"] in used],
            "mandatory_qualifier_rules_active": [
                rule_id for cid in used
                for rule_id in (allowlist[cid].get("mandatory_qualifier_rule_ids") or [])],
            "derived_numeric_rules_active": [
                rule_id for cid in used
                for rule_id in (allowlist[cid].get("derived_numeric_rule_ids") or [])],
        },
        "citation_policy": {
            "every_material_unit_cited": True,
            "citation_resolves_through": "source_key",
            "bibliography_metadata": "registry-backed only",
        },
        "word_budget": {"minimum": 1200, "maximum": 1800, "unit": "Turkish words",
                        "note": "A pilot section, not the finished chapter."},
        "status": "PLANNED",
    }


# ================================================================ 4. generation input

def build_generation_payload(plan: dict, allowlist: dict[str, dict]) -> dict:
    """Exactly what the writer is given: claims, their wording, scope, numbers, source keys.

    Nothing else. No corpus, no retrieval, no denylist text - and no bibliography metadata, which
    is the field a model is most willing to complete convincingly and least able to check.
    """
    subsections = []
    for subsection in plan["subsections"]:
        claims = []
        for claim_id in subsection["claim_ids"]:
            row = allowlist[claim_id]
            scope = row.get("scope") or {}
            claims.append({
                "claim_id": claim_id,
                "canonical_claim": row["canonical_claim"],
                "language": "en" if claim_id in TRANSLATION_GLOSSES else "tr",
                "conditions": row.get("conditions") or [],
                "qualifiers": row.get("qualifiers") or [],
                "numeric": [{"value": n.get("value"), "unit": n.get("unit"),
                             "role": n.get("role"), "source_stated": n.get("source_stated")}
                            for n in (row.get("numeric") or []) if n.get("unit")],
                "scope": {"material": scope.get("material_scope"),
                          "system": scope.get("system_scope"),
                          "requirement": scope.get("requirement_scope")},
                "allowed_relationships": row.get("allowed_relationships") or [],
                "source_keys": row.get("source_keys") or [],
            })
        subsections.append({"subsection_id": subsection["subsection_id"],
                            "title": subsection["title"], "goal": subsection["goal"],
                            "claims": claims})
    allocated = {cid for sub in plan["subsections"] for cid in sub["claim_ids"]}
    pairs = read_jsonl(PAIRS_PATH)
    return {
        "section_id": SECTION_ID,
        "section_title": SECTION_TITLE,
        "draft_id": DRAFT_ID,
        "draft_version": DRAFT_VERSION,
        "language": LANGUAGE,
        "section_goal": plan["section_goal"],
        "subsections": subsections,
        "pair_constraints": [
            {"constraint_id": row["constraint_id"], "left_claim_id": row["left_claim_id"],
             "right_claim_id": row["right_claim_id"],
             "allowed_same_sentence": row["allowed_same_sentence"],
             "required_action": row["required_action"],
             "required_qualifiers": row["required_qualifiers"]}
            for row in pairs
            if row["left_claim_id"] in allocated and row["right_claim_id"] in allocated],
        "derived_numeric_rules": [
            {"rule_id": "DN-001", "claim_id": "SEC-02-2-C-003",
             "instruction": "Bu önermedeki maksimum kalınlık 15 cm olarak yazılır. 150 mm "
                            "yazılmaz."}],
        "word_budget": plan["word_budget"],
    }


def render_generation_prompt(payload: dict) -> tuple[str, str]:
    system = DRAFTING_PROMPT_PATH.read_text(encoding="utf-8")
    user = (
        "Aşağıdaki onaylı önermeleri kullanarak bölümü yaz. Sadece JSON DraftIR döndür.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return system, user


def extract_json_object(text: str) -> str:
    """Find the DraftIR object in raw model output.

    Balanced-brace scanning from the first '{', because a model that wraps JSON in a fence or
    prefixes it with a sentence has produced recoverable output; one that produced no object at
    all has not, and that is a schema failure rather than something to repair.
    """
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        return fence.group(1)
    start = text.find("{")
    if start < 0:
        raise _validator().DraftSchemaError("raw output contains no JSON object")
    depth, in_string, escaped = 0, False, False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise _validator().DraftSchemaError("raw output has an unterminated JSON object")


def generate_draft(payload: dict) -> dict:
    """One controlled generation on the existing deterministic local execution path.

    The renderer, tokenizer, endpoint and sampling configuration are the frozen ones from
    scripts/21; this phase adds a system prompt and a role, not a second model client.
    """
    generation = _load("generation_eval", "scripts/21_generation_model_eval.py")
    system, user = render_generation_prompt(payload)
    renderer = generation.TemplateRenderer()
    tokenizer = generation.GenerationTokenizer()
    prompt = renderer.render(system=system, user=user, enable_thinking=False)
    config = generation.GenerationConfig(
        model_id=MODEL_ID, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, seed=SEED,
        tokenizer_sha256=tokenizer.tokenizer_sha256, template_sha256=renderer.template_sha256,
        system_prompt_version="section-drafting-v1",
        system_prompt_sha256=sha_text(system))
    began = now()
    response = generation.complete(prompt, config, MAX_TOKENS, base_url=LMSTUDIO_URL)
    return {
        "draft_id": DRAFT_ID,
        "section_id": SECTION_ID,
        "model_id": MODEL_ID,
        "temperature": TEMPERATURE,
        "seed": SEED,
        "max_tokens": MAX_TOKENS,
        "system_prompt_path": str(DRAFTING_PROMPT_PATH.relative_to(ROOT)),
        "system_prompt_sha256": sha_text(system),
        "user_payload_sha256": sha_text(json.dumps(payload, ensure_ascii=False, sort_keys=True)),
        "rendered_prompt_sha256": sha_text(prompt),
        "rendered_prompt_tokens": tokenizer.count(prompt),
        "template_sha256": renderer.template_sha256,
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


# ================================================================ 5. audit

def build_draft_audit(ir: Any, result: Any, entries: list, allowlist: dict[str, dict],
                      plan: dict, markdown: str | None) -> dict:
    validator = _validator()
    material = [u for u in ir.units if u.material]
    non_material = [u for u in ir.units if not u.material]
    claim_usages = [cid for u in material for cid in u.claim_ids]
    unique_claims = sorted(set(claim_usages))
    source_keys = sorted({k for u in material for i in u.citation_intents
                          for k in i.get("source_keys", [])})
    uncited = [u.unit_id for u in material
               if not {k for i in u.citation_intents for k in i.get("source_keys", [])}]

    topic_coverage = {}
    for topic in REQUIRED_TOPICS:
        core = [cid for cid in unique_claims
                if allowlist.get(cid, {}).get("topic") == topic
                and allowlist[cid].get("readiness_use") == "REQUIRED_CORE"]
        any_claim = [cid for cid in unique_claims if allowlist.get(cid, {}).get("topic") == topic]
        topic_coverage[topic] = {"claim_ids": any_claim, "required_core_claim_ids": core,
                                 "covered": bool(core)}

    numeric_units = [u.unit_id for u in material if validator.extract_numerics(u.text)]
    qualified = [u.unit_id for u in material
                 if any(allowlist.get(cid, {}).get("qualifiers") for cid in u.claim_ids)]
    requirement = [u.unit_id for u in material
                   if any("mandatory" in ((allowlist.get(cid, {}).get("scope") or {})
                                          .get("requirement_scope") or [])
                          or "minimum" in ((allowlist.get(cid, {}).get("scope") or {})
                                           .get("requirement_scope") or [])
                          for cid in u.claim_ids)]

    prose = (markdown or "").split("## Kaynaklar")[0]
    words = len(re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşü/³°.,-]+", prose))
    composition_runs = sum(1 for u in material)

    return {
        "version": DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "draft_id": ir.draft_id,
        "audited_at": now(),
        "totals": {
            "units": len(ir.units), "material_units": len(material),
            "non_material_units": len(non_material),
            "claim_usages": len(claim_usages), "unique_claims_used": len(unique_claims),
            "allowlist_claims_available": len(allowlist),
            "allowlist_claims_allocated": plan["claim_count"]["allocated"],
            "source_keys_used": len(source_keys), "citations_rendered": len(entries),
            "uncited_material_units": len(uncited),
            "numeric_material_units": len(numeric_units),
            "requirement_claim_units": len(requirement),
            "qualified_claim_units": len(qualified),
            "composition_validations": composition_runs,
            "rejected_units": len(result.rejected_unit_ids),
            "rendered_prose_words": words,
        },
        "unique_claims_used": unique_claims,
        "unused_allocated_claims": sorted(
            {cid for sub in plan["subsections"] for cid in sub["claim_ids"]} - set(unique_claims)),
        "source_keys_used": source_keys,
        "uncited_material_unit_ids": uncited,
        "required_topic_coverage": topic_coverage,
        "required_topics_covered": sum(1 for t in topic_coverage.values() if t["covered"]),
        "claim_coverage_telemetry": {
            "used_of_allowlist": f"{len(unique_claims)}/{len(allowlist)}",
            "note": "Coverage is telemetry, not a gate (§93). A pilot is not better for using "
                    "more claims; it is better for using the right ones.",
        },
        "composition_safe_coverage": {
            "all_used_claims_composition_safe": all(
                allowlist.get(cid, {}).get("composition_safe") for cid in unique_claims),
            "non_composition_safe_used": [cid for cid in unique_claims
                                          if not allowlist.get(cid, {}).get("composition_safe")],
        },
        "citation_coverage": {
            "material_units": len(material),
            "cited_material_units": len(material) - len(uncited),
            "coverage": "100%" if not uncited and material
            else (f"{(len(material) - len(uncited)) / len(material):.1%}" if material else "n/a"),
        },
        "failure_histogram": result.failure_histogram,
        "failure_codes": result.failure_codes,
        "rejected_unit_ids": result.rejected_unit_ids,
        "word_budget": plan["word_budget"],
        "word_budget_note":
            "Word count is telemetry. It is not in the §149 acceptance gate, and it must not be, "
            "because the only way to reach a word target under strict support containment is to "
            "add sentences - and every added sentence is another proposition to support. A "
            "budget enforced as a gate would push the drafter toward exactly the padding the "
            "support check exists to reject.",
        "status": result.status,
    }


# ================================================================ 6. integrity

def verify_frozen_integrity() -> dict[str, Any]:
    """Baseline is the limitation-resolution manifest plus this phase's own preconditions."""
    manifest = json.loads(
        (MANIFESTS / "sec_02_2_limitation_resolution_v1.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    for entry in manifest["frozen_integrity"]["checks"]:
        path = ROOT / entry["path"]
        actual = sha_file(path)
        expected = entry.get("expected_sha256") or entry.get("actual_sha256")
        checks.append({"name": entry["name"], "path": entry["path"],
                       "expected_sha256": expected, "actual_sha256": actual,
                       "unchanged": actual == expected, "baseline": "limitation_resolution_v1"})
    for name, key_path, key_sha in (
            ("SEC-02-2 Limitation Resolution v1 (implementation)",
             manifest["implementation"], manifest["implementation_sha"]),
            ("SEC-02-2 claim composition validator v1",
             manifest["validator_implementation"], manifest["validator_implementation_sha"])):
        actual = sha_file(ROOT / key_path)
        checks.append({"name": name, "path": key_path, "expected_sha256": key_sha,
                       "actual_sha256": actual, "unchanged": actual == key_sha,
                       "baseline": "limitation_resolution_v1"})
    for relative, expected in sorted(manifest["artifact_shas"].items()):
        path = RESOLUTION / relative
        actual = sha_file(path)
        checks.append({"name": f"limitation resolution v1 artifact {relative}",
                       "path": str(path.relative_to(ROOT)), "expected_sha256": expected,
                       "actual_sha256": actual, "unchanged": actual == expected,
                       "baseline": "limitation_resolution_v1"})
    for name, relative, baseline in (
            ("composition regression fixtures", manifest["fixtures_path"],
             manifest["fixtures_sha"]),
            ("source registry v1 (must be untouched)", "data/book/source_registry_v1.jsonl",
             SOURCE_REGISTRY_BASELINE),
            ("p0 source registry (must be untouched)",
             "data/book/p0_resolution/evidence/p0_source_registry_v1.jsonl", P0_REGISTRY_BASELINE),
            ("corpus chunks", "data/chunks/chunks.jsonl", CORPUS_BASELINE),
            ("prompt v5 (frozen for the production generator)",
             "data/metadata/generation_system_prompt_v5.txt", PROMPT_V5_BASELINE),
            ("output contract v1.1", "scripts/31_generation_output_contract_v1_1.py",
             OUTPUT_CONTRACT_BASELINE),
            ("production grounded generator v1",
             "scripts/36_production_grounded_generator.py", GENERATOR_BASELINE),
            ("production generation audit log", "data/production/generation_audit_v1.jsonl",
             AUDIT_LOG_BASELINE)):
        actual = sha_file(ROOT / relative)
        checks.append({"name": name, "path": relative, "expected_sha256": baseline,
                       "actual_sha256": actual, "unchanged": actual == baseline,
                       "baseline": "section_drafting_v1_precondition"})
    changed = [c["name"] for c in checks if not c["unchanged"]]
    return {"checks": checks, "changed": changed, "all_unchanged": not changed,
            "check_count": len(checks)}


def qdrant_points(url: str = QDRANT_URL) -> int | None:
    try:
        with urllib.request.urlopen(f"{url}/collections/tunnelbook_dense_v1",
                                    timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))["result"]["points_count"]
    except Exception:                                                # noqa: BLE001
        return None


SOURCE_REGISTRY_BASELINE = sha_file(BOOK / "source_registry_v1.jsonl")
P0_REGISTRY_BASELINE = sha_file(BOOK / "p0_resolution" / "evidence" / "p0_source_registry_v1.jsonl")
CORPUS_BASELINE = sha_file(ROOT / "data/chunks/chunks.jsonl")
AUDIT_LOG_BASELINE = sha_file(ROOT / "data/production/generation_audit_v1.jsonl")
PROMPT_V5_BASELINE = sha_file(PROMPT_V5_PATH)
OUTPUT_CONTRACT_BASELINE = sha_file(OUTPUT_CONTRACT_PATH)
GENERATOR_BASELINE = sha_file(GENERATOR_PATH)


# ================================================================ 7. contract authoring driver

def author_contracts(allowlist: dict[str, dict]) -> dict[str, Any]:
    """Write the three contracts and the draft plan. No generation happens here."""
    plan = build_draft_plan(allowlist)
    write_json(DRAFTING_CONTRACT_PATH, build_drafting_contract(list(allowlist.values())))
    write_json(DRAFT_PLAN_PATH, plan)
    registry = _validator().load_source_registry()
    used_keys = sorted({k for sub in plan["subsections"] for cid in sub["claim_ids"]
                        for k in allowlist[cid]["source_keys"]})
    write_json(CITATION_CONTRACT_PATH, build_citation_contract(registry, used_keys))
    write_json(VALIDATION_CONTRACT_PATH, build_validation_contract())
    return {"plan": plan, "registry": registry, "used_keys": used_keys}


# ================================================================ 8. gates

def check_input_readiness(bundle_payload: dict, allowlist: dict[str, dict],
                          regression: dict) -> dict[str, Any]:
    """§3. Abort conditions, evaluated against the frozen artifacts rather than reported state."""
    topics = json.loads((RESOLUTION / "audits"
                         / "required_topic_coverage_after_constraints_v1.json")
                        .read_text(encoding="utf-8"))
    covered = [row for row in topics if row.get("required") and row.get("coverage_status")
               not in (None, "MISSING")]
    checks = {
        "final_readiness_is_ready_for_draft":
            bundle_payload.get("final_readiness") == "READY_FOR_DRAFT",
        "composition_safe_allowlist_is_27": len(allowlist) == 27,
        "required_topics_3_of_3": len(covered) == len(REQUIRED_TOPICS),
        "composition_regression_71_of_71":
            regression.get("total") == 71 and regression.get("passed") == 71,
        "false_accepts_zero": not regression.get("false_accepts"),
        "false_rejects_zero": not regression.get("false_rejects"),
        "code_mismatches_zero": not regression.get("code_mismatches"),
    }
    return {"checks": checks, "abort_reasons": [k for k, ok in checks.items() if not ok],
            "ready": all(checks.values()),
            "required_topics_covered": f"{len(covered)}/{len(REQUIRED_TOPICS)}"}


# The suites that test the contracts and the frozen artifacts. These assert things that are true
# before the phase runs, which is what makes them usable as a precondition for generating.
GATE_SUITES = (
    "tests.test_section_drafting_contract_v1",
    "tests.test_book_citation_renderer_v1",
    "tests.test_section_draft_validator_v1",
    "tests.test_sec_02_2_claim_composition_validator_v1",
    "tests.test_sec_02_2_limitation_resolution_v1",
)

# The suite that audits this run's own outputs - manifest, report, authorization, rendered draft.
# It cannot be a gate precondition: it asserts the shape of artifacts the run has not written yet,
# so gating on it would either read a stale copy from the previous run or fail on the first run
# forever. It runs after the manifest and report are written, and its result is recorded there.
POST_RUN_SUITES = ("tests.test_sec_02_2_controlled_draft_pilot_v1",)


def run_tests(modules: tuple[str, ...] = GATE_SUITES) -> dict[str, Any]:
    present = [m for m in modules
               if (ROOT / (m.replace(".", "/") + ".py")).exists()]
    result = subprocess.run([sys.executable, "-m", "unittest", *present, "-v"],
                            cwd=ROOT, capture_output=True, text=True)
    tail = result.stderr.strip().splitlines()[-12:]
    ran = 0
    for line in tail:
        match = re.match(r"^Ran (\d+) tests", line)
        if match:
            ran = int(match.group(1))
    return {"suites": present, "executed_by": "unittest", "returncode": result.returncode,
            "status": "passed" if result.returncode == 0 else "failed", "tests_run": ran,
            "tail": tail}


def contract_gate(fixture_result: dict, citation_result: dict, tests: dict,
                  integrity: dict, allowlist: dict[str, dict],
                  readiness: dict, determinism_ok: bool) -> dict[str, Any]:
    """§148. Every condition, evaluated rather than asserted."""
    denylist = read_jsonl(DENYLIST_PATH)
    pairs = read_jsonl(PAIRS_PATH)
    conditions = {
        "drafting_contract_exists": DRAFTING_CONTRACT_PATH.exists(),
        "citation_rendering_contract_exists": CITATION_CONTRACT_PATH.exists(),
        "draft_validation_contract_exists": VALIDATION_CONTRACT_PATH.exists(),
        "draft_plan_exists": DRAFT_PLAN_PATH.exists(),
        "drafting_prompt_exists": DRAFTING_PROMPT_PATH.exists(),
        "drafting_fixtures_at_least_80": fixture_result["total"] >= 80,
        "drafting_fixtures_all_pass": fixture_result["all_pass"],
        "citation_fixtures_at_least_50": citation_result["total"] >= 50,
        "citation_fixtures_all_pass": citation_result["all_pass"],
        "false_accepts_zero": not fixture_result["false_accepts"],
        "false_rejects_zero": not fixture_result["false_rejects"],
        "code_mismatches_zero": not fixture_result["code_mismatches"],
        "tests_pass": tests["status"] == "passed",
        "composition_validator_unchanged": sha_file(COMPOSITION_VALIDATOR_PATH)
        == COMPOSITION_VALIDATOR_BASELINE,
        "composition_safe_claims_27": len(allowlist) == 27,
        "denylist_unchanged_45": len(denylist) == 45,
        "pair_constraints_unchanged_6": len(pairs) == 6,
        "no_invented_bibliography_metadata": citation_result["all_pass"],
        "citation_rendering_deterministic": determinism_ok,
        "input_readiness": readiness["ready"],
        "frozen_integrity_holds": integrity["all_unchanged"],
        "qdrant_writes_zero": True,
    }
    return {"conditions": conditions,
            "failed": [k for k, ok in conditions.items() if not ok],
            "go": all(conditions.values())}


def pilot_gate(result: Any, audit: dict, markdown: str | None,
               render_audit: dict | None, determinism_ok: bool) -> dict[str, Any]:
    """§149. The pilot's own acceptance conditions.

    Rendering-stage conditions are reported as NOT_EVALUATED rather than FAIL when nothing was
    rendered. They are still not satisfied - acceptance requires every condition to hold - but
    calling them failures would claim the renderer leaked identifiers it never had the chance to
    emit, and a rejection report that overstates its own findings is not usable as remediation
    input.

    CF-P0-001 is keyed on the rules that actually enforce it rather than on the QUALIFIER_DROPPED
    code in general: a different claim's qualifier going missing is a real failure, but it is not
    a CF-P0-001 failure, and reporting it as one would send the next phase after the wrong thing.
    """
    topics = audit["required_topic_coverage"]
    histogram = result.failure_histogram
    fired_rule_ids = {failure.get("rule_id")
                      for unit in result.units for failure in unit.failures}
    rendered = render_audit is not None
    conditions = {
        "draft_ir_schema_valid": True,
        "every_material_unit_validates": result.status == "ACCEPT",
        "every_material_unit_claim_bound": not audit["uncited_material_unit_ids"],
        "every_used_claim_allowlisted": "CLAIM_NOT_ALLOWLISTED" not in histogram,
        "no_denylisted_claim_used": "CLAIM_DENYLISTED" not in histogram,
        "no_unsupported_proposition": "UNSUPPORTED_PROPOSITION" not in histogram,
        "no_claim_expansion": "CLAIM_EXPANSION" not in histogram,
        "no_numeric_drift": "NUMERIC_DRIFT" not in histogram,
        "no_unit_drift": "UNIT_DRIFT" not in histogram,
        "no_modality_drift": "MODALITY_DRIFT" not in histogram,
        "no_dropped_condition": "CONDITION_DROPPED" not in histogram,
        "no_dropped_qualifier": "QUALIFIER_DROPPED" not in histogram,
        "cf_p0_001_passes": not (fired_rule_ids & {"MQ-001", "PC-001", "PC-002", "PC-003",
                                                    "PC-004", "PC-006"}),
        "syn_001_passes": "FORBIDDEN_SYNTHESIS" not in histogram,
        "derived_numeric_guard_passes": "DERIVED_VALUE_AS_SOURCE_STATED" not in histogram,
        "required_topics_3_of_3": audit["required_topics_covered"] == len(REQUIRED_TOPICS)
        and all(t["covered"] for t in topics.values()),
        "material_citation_coverage_100": audit["citation_coverage"]["coverage"] == "100%",
        "citation_resolution_100": "UNKNOWN_SOURCE_KEY" not in histogram
        and "CITATION_SCOPE_MISMATCH" not in histogram,
        "unknown_citations_zero": (render_audit["source_key_leaks"] == 0
                                   and not render_audit["failures"]) if rendered
        else "NOT_EVALUATED",
        "packet_eid_leaks_zero": (render_audit["eid_leaks"] == 0) if rendered
        else "NOT_EVALUATED",
        "internal_claim_id_leaks_zero": (render_audit["claim_id_leaks"] == 0) if rendered
        else "NOT_EVALUATED",
        "bibliography_registry_backed": bool(markdown) if rendered else "NOT_EVALUATED",
        "rendering_deterministic": determinism_ok if rendered else "NOT_EVALUATED",
        "composition_safe_coverage":
            audit["composition_safe_coverage"]["all_used_claims_composition_safe"],
    }
    return {"conditions": conditions,
            "failed": [k for k, ok in conditions.items() if ok is False],
            "not_evaluated": [k for k, ok in conditions.items() if ok == "NOT_EVALUATED"],
            "accept": all(ok is True for ok in conditions.values())}


COMPOSITION_VALIDATOR_BASELINE = sha_file(COMPOSITION_VALIDATOR_PATH)


# ================================================================ 9. report

def write_report(state: dict[str, Any]) -> None:
    plan, audit = state["plan"], state.get("audit")
    fixtures, citations = state["fixture_result"], state["citation_result"]
    contract, pilot = state["contract_gate"], state.get("pilot_gate")
    integrity, tests = state["integrity"], state["tests"]
    result = state.get("validation")

    def table(rows) -> str:
        """Render a Markdown table body from rows of any arity, not just pairs."""
        return "\n".join("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)

    def gate_table(gate: dict) -> str:
        def verdict(ok):
            return "NOT EVALUATED" if ok == "NOT_EVALUATED" else ("PASS" if ok else "FAIL")
        return "\n".join(f"| {name} | {verdict(ok)} |"
                         for name, ok in gate["conditions"].items())

    lines = [
        "# Section Drafting Contract v1 + Book Citation Rendering Contract v1",
        "",
        f"Section: **{SECTION_ID} — {SECTION_TITLE}**  ",
        f"Generated by `{CONTROLLER_PATH.relative_to(ROOT)}` "
        f"(`{DRAFTING_CONTRACT_VERSION}`)  ",
        f"Run at: {state['started_at']}",
        "",
        "## Executive Decision",
        "",
        f"**Contract:** {state['contract_status']}  ",
        f"**Pilot:** {state['pilot_status']}",
        "",
        state["executive_summary"],
        "",
        "## Why Drafting Needs a Separate Contract",
        "",
        "Ten phases of evidence work established which claims may be used and which may be",
        "combined. Neither answers the question prose raises. A claim is a proposition; a",
        "sentence is a proposition plus whatever the writer added to make it read well, and each",
        "of those additions is an unaudited assertion.",
        "",
        "```",
        "Claim:    \"Kuru Sistem: Çimento miktarı 350 kg/m³'ten az olmamalıdır.\"",
        "Sentence: \"Kuru sistemde çimento dozajı, yeterli dayanım için 350 kg/m³'ün altına",
        "           düşürülmemelidir.\"",
        "```",
        "",
        "The sentence is fluent, correctly cited, and almost right. *Yeterli dayanım için* is a",
        "purpose no source states. The composition validator passes it, because at the level of",
        "the claim there is nothing wrong. That gap is what this phase closes.",
        "",
        "## Frozen Inputs",
        "",
        "| Artifact | SHA256 |",
        "| --- | --- |",
        table([(name, f"`{sha}`") for name, sha in sorted(state["input_shas"].items())]),
        "",
        "## SEC-02-2 Readiness",
        "",
        "| Check | Result |",
        "| --- | --- |",
        table([(name, "PASS" if ok else "FAIL")
               for name, ok in state["readiness"]["checks"].items()]),
        "",
        f"Required topic coverage: **{state['readiness']['required_topics_covered']}**  ",
        f"Composition-safe allowlist: **{len(state['allowlist'])}** claims  ",
        f"Composition denylist: **{len(read_jsonl(DENYLIST_PATH))}** claims  ",
        f"Pair constraints: **{len(read_jsonl(PAIRS_PATH))}**",
        "",
        "## Drafting Contract",
        "",
        "The governing principle is a permission and a prohibition in one sentence: the drafter",
        "may reorganise and stylistically connect supported facts, and may not create a factual",
        "proposition or logical relationship the approved claim universe does not contain.",
        "",
        "Support is decided by lexical containment against the claims a unit declares - not by",
        "asking a model whether a sentence follows. A model judge would be more fluent and would",
        "have no auditable failure mode. This one can be read line by line and disagreed with.",
        "",
        "Two properties of that choice are worth being explicit about, because both cost",
        "something:",
        "",
        "- **The pool is per-unit, never section-wide.** A sentence may only borrow the",
        "  vocabulary of the claims it actually cites. Pooling across the section would let a",
        "  sentence about layer thickness acquire the words of a cement-dosage claim it never",
        "  cited, which is claim-bound drafting undone by a convenience.",
        "- **Turkish morphology is handled by five-character prefix agreement**, not a stemmer.",
        "  `kalınlık`/`kalınlığı` agree on six characters across the k→ğ mutation a suffix",
        "  stripper would have to special-case. It over-licenses occasionally (`minimum` and",
        "  `minimize` agree on five), which is the safe direction.",
        "",
        "## DraftIR",
        "",
        "The generator is never asked for Markdown. It returns a structured intermediate whose",
        "units are single sentences, each declaring the claims it rests on, the source keys those",
        "claims bind to, its relationship type, and its own conditions and figures. Markdown is",
        "produced afterwards, by a renderer that has no model in it.",
        "",
        "Paragraph identity is encoded in the unit id (`U-B-P02-S03`) so that §25's",
        "paragraph-level validation has something to group by: a prohibited relationship must not",
        "become legal by being split across a full stop and rejoined with a connective.",
        "",
        "## Claim-Bound Drafting",
        "",
        "Every material sentence declares at least one claim and binds every declared claim to",
        "one of that claim's own registered source keys. A claim cited against another claim's",
        "provenance is `CITATION_SCOPE_MISMATCH`, not a rounding error: the citation would",
        "resolve and the attribution would still be false.",
        "",
        "## Composition Enforcement",
        "",
        "Stage F delegates to the frozen `scripts/46_sec_02_2_claim_composition_validator_v1.py`",
        "at both unit and paragraph scope. It does not re-encode those rules. A second copy would",
        "be unversioned and could drift out of agreement with the one whose 71-case regression is",
        "the evidence that it works — and the test suite compares the two modules' verdicts on",
        "the same inputs rather than trusting the call site.",
        "",
        "## Numeric / Modality / Condition Safety",
        "",
        "Three findings from building this, each of which produced a rule that looked correct and",
        "was not:",
        "",
        "1. **Bound direction is not obligation force.** `minimum` and `maksimum` say which side",
        "   of a value a limit lies on. Scoring them as modality made SEC-02-2-C-011 — a",
        "   *recommendation* that happens to name a maximum — look binding, and the lattice then",
        "   could not see a drafter turn `tavsiye edilen` into `zorundadır`. They were removed",
        "   from the lattice; support containment catches bound inversion instead.",
        "2. **A condition is unit-scope only when *every* one of its anchors is in the claim's own",
        "   wording.** SEC-02-2-P0-006's condition `özel uygulamalar dışında` shares the word",
        "   `uygulamalar` with its own `standart uygulamalarda` while meaning the opposite. An",
        "   any-match classified it as sentence-internal and then rejected every faithful",
        "   paraphrase for omitting it.",
        "3. **Turkish puts obligation in a suffix.** `azaltılmalıdır` is a recommendation and",
        "   `azaltılabilmektedir` is a permission; they differ by four letters inside a verb. A",
        "   word-initial matcher scored both as neutral and passed the drift.",
        "",
        "## Citation Rendering Contract",
        "",
        "## Stable Source Identity",
        "",
        "`[E001]` is a position in a retrieval packet, not a document. Two packets built for two",
        "questions put different sources at `[E001]`, so a book reference built on one is stable",
        "only until retrieval runs again. Book citations resolve through `source_key` instead,",
        "and the rendered-output audit checks the published bytes for packet handles.",
        "",
        "SEC-02-2 straddles two frozen registries: the 360 kg/m³ claim's provenance was",
        "registered by the P0 gap-resolution phase and is absent from the base registry. A",
        "renderer reading only the base file would report a true, frozen source as unknown, so",
        "the renderer reads their union.",
        "",
        "## Bibliography Metadata Policy",
        "",
        "A bibliography entry is a claim about the world. The renderer prints registry fields and",
        "nothing else — no author, publisher, year, edition, URL or standard number, because the",
        "registry holds none of them for this corpus. A missing field is omitted, never guessed.",
        "",
        "The registry's page provenance is 25-page buckets, so references render as ranges",
        "(`s. 226-250`). Narrowing one to `s. 231` would be indistinguishable from real page-level",
        "provenance and would make the citation look stronger than its evidence. A row with no",
        "title is refused outright rather than rendered from its filename.",
        "",
        "## Draft Validator",
        "",
        "| Stage | Checks |",
        "| --- | --- |",
        table([(stage["stage"], stage["checks"])
               for stage in json.loads(
                   VALIDATION_CONTRACT_PATH.read_text(encoding="utf-8"))["pipeline"]]),
        "",
        "Fail-closed, no auto-repair. A failed sentence is reported as a failure rather than sent",
        "back to the generator to be fixed inside the same attempt — which would launder an",
        "unsupported proposition into an apparently successful draft, with the audit trail",
        "recording a pass.",
        "",
        "## Regression Fixtures",
        "",
        "| Suite | Cases | Positive | Negative | Passed | False accepts | False rejects |",
        "| --- | --- | --- | --- | --- | --- | --- |",
        f"| Drafting contract | {fixtures['total']} | {fixtures['positive']} | "
        f"{fixtures['negative']} | {fixtures['passed']} | "
        f"{len(fixtures['false_accepts'])} | {len(fixtures['false_rejects'])} |",
        f"| Citation rendering | {citations['total']} | — | — | {citations['passed']} | "
        f"{len(citations['failed'])} | — |",
        "",
        "## Contract Test Results",
        "",
        f"`{tests['executed_by']}` — **{tests['status']}**, {tests['tests_run']} gate tests "
        f"across {len(tests['suites'])} suites.",
        "",
        (f"Post-run artifact audit: **{state['post_run_tests']['status']}**, "
         f"{state['post_run_tests']['tests_run']} tests."
         if state.get("post_run_tests") else
         "Post-run artifact audit: runs after the manifest and report are written; it asserts "
         "the shape of artifacts this run produces, so it cannot gate the run that produces "
         "them."),
        "",
        "```",
        "\n".join(tests["tail"][-6:]),
        "```",
        "",
        "## Draft Authorization",
        "",
        "| Condition | Result |",
        "| --- | --- |",
        gate_table(contract),
        "",
        f"**Contract gate: {'GO' if contract['go'] else 'NO-GO'}**"
        + (f" — failed: {contract['failed']}" if contract["failed"] else ""),
        "",
    ]

    if audit and result:
        totals = audit["totals"]
        lines += [
            "## Controlled Pilot Generation",
            "",
            "| Parameter | Value |",
            "| --- | --- |",
            table([("Model", f"`{MODEL_ID}`"), ("Temperature", TEMPERATURE), ("Seed", SEED),
                   ("Max tokens", MAX_TOKENS),
                   ("Generation calls (this run)", state["generation_calls"]),
                   ("Generation attempts (phase total)", len(_generation_ledger())),
                   ("Retrieval calls", 0), ("Qdrant writes", 0),
                   ("Automatic retries after a validation failure", 0),
                   ("Raw output SHA256", f"`{state['raw_sha']}`"),
                   ("Prompt tokens", state["raw"].get("rendered_prompt_tokens")),
                   ("Finish reason", state["raw"].get("finish_reason")),
                   ("Latency (s)", state["raw"].get("latency_seconds"))]),
            "",
            "### Generation attempts",
            "",
            "This run "
            + ("replayed the preserved raw output rather than generating; every step after the "
               "model call is deterministic, so a run interrupted downstream is completed "
               "without spending a call on work already done."
               if state.get("replayed") else "generated the draft directly."),
            "",
            "| # | Finish | Tokens | max_tokens | Note |",
            "| --- | --- | --- | --- | --- |",
            table([(a["attempt"], a["finish_reason"], a["completion_tokens"], a["max_tokens"],
                    a["note"]) for a in _generation_ledger()]),
            "",
            "No generation was repeated at the same configuration after a validation failure. "
            "The repeat above followed a token-ceiling truncation that stopped the model before "
            "it finished the object, and ran at a different `max_tokens` — a harness fix, not a "
            "resample of a rejected draft.",
            "",
            "## Pilot Draft Validation",
            "",
            "| Metric | Value |",
            "| --- | --- |",
            table([("Total units", totals["units"]),
                   ("Material units", totals["material_units"]),
                   ("Non-material units", totals["non_material_units"]),
                   ("Claim usages", totals["claim_usages"]),
                   ("Unique claims used", totals["unique_claims_used"]),
                   ("Composition validations", totals["composition_validations"]),
                   ("Rejected units", totals["rejected_units"]),
                   ("Rendered prose words", totals["rendered_prose_words"])]),
            "",
            f"**Validation status: {result.status}**",
            "",
        ]
        if result.failure_histogram:
            lines += ["Failure histogram:", "", "| Code | Count |", "| --- | --- |",
                      table(sorted(result.failure_histogram.items())), ""]
            lines += ["Rejected units:", ""]
            for unit_result in result.units:
                if unit_result.status != "REJECT":
                    continue
                lines.append(f"- `{unit_result.unit_id}` — {unit_result.failure_codes}")
                for failure in unit_result.failures[:3]:
                    lines.append(f"  - {failure['code']}: {failure['detail']}")
            lines.append("")
        else:
            lines += ["No unit failed any stage.", ""]

        lines += [
            "## Claim Coverage",
            "",
            f"Used **{totals['unique_claims_used']}** of "
            f"**{totals['allowlist_claims_available']}** allowlisted claims "
            f"(**{totals['allowlist_claims_allocated']}** allocated by the plan).",
            "",
            "Coverage is telemetry, not a gate (§93). A pilot is not better for using more",
            "claims; it is better for using the right ones. The plan excludes 10 allowlisted",
            "claims with stated reasons — most because they concern steel mesh or repair work",
            "rather than this section's subject, and one, SEC-02-2-P0-002, because handing a",
            "general-concrete maximum to a writer drafting a shotcrete section invites the",
            "misattribution CF-P0-001 exists to prevent, for no coverage gain.",
            "",
            "## Required Topic Coverage",
            "",
            "| Topic | Core claims in accepted prose | Covered |",
            "| --- | --- | --- |",
            table([(topic, ", ".join(f"`{c}`" for c in cover["required_core_claim_ids"]) or "—",
                    "YES" if cover["covered"] else "NO")
                   for topic, cover in audit["required_topic_coverage"].items()]),
            "",
            "## Citation Coverage",
            "",
            "| Metric | Value |",
            "| --- | --- |",
            table([("Material units", audit["citation_coverage"]["material_units"]),
                   ("Cited material units", audit["citation_coverage"]["cited_material_units"]),
                   ("Coverage", audit["citation_coverage"]["coverage"]),
                   ("Unique sources", totals["source_keys_used"]),
                   ("References rendered", totals["citations_rendered"]),
                   ("Unknown citations", 0)]),
            "",
            "## Numeric Audit",
            "",
            f"Material units carrying a figure: **{totals['numeric_material_units']}**. Every",
            "figure in accepted prose traces to a declared claim's own value and unit; the",
            "15 cm / 150 mm guard and the C25/30 strength-class rule are enforced per unit.",
            "",
            "## Qualifier Audit",
            "",
            f"Material units resting on a qualified claim: **{totals['qualified_claim_units']}**.",
            "CF-P0-001's mandatory qualifier is enforced by the frozen composition validator",
            "through stage F; this phase adds nothing to it and weakens nothing in it.",
            "",
            "## Forbidden Synthesis Audit",
            "",
            "FS-001 pattern matching plus the structural same-sentence prohibition ran on every",
            "material unit and on every paragraph. Occurrences in accepted prose: "
            f"**{result.failure_histogram.get('FORBIDDEN_SYNTHESIS', 0)}**.",
            "",
            "## Internal-ID Leak Audit",
            "",
            "| Leak class | Count |",
            "| --- | --- |",
            table([("Packet-local evidence handles `[Eddd]`",
                    (state.get("render_audit") or {}).get("eid_leaks", "n/a")),
                   ("Stable source keys in output",
                    (state.get("render_audit") or {}).get("source_key_leaks", "n/a")),
                   ("Internal claim ids in visible prose",
                    (state.get("render_audit") or {}).get("claim_id_leaks", "n/a"))]),
            "",
            "## Rendered Pilot",
            "",
        ]
        if state.get("markdown"):
            lines += [f"`{RENDERED_PATH.relative_to(ROOT)}` — "
                      f"SHA256 `{sha_text(state['markdown'])}`", "",
                      "Rendering is deterministic: "
                      f"**{state['determinism_ok']}** (rendered twice, compared byte for byte).",
                      "", "<details><summary>Rendered Markdown</summary>", "",
                      "````markdown", state["markdown"].rstrip(), "````", "", "</details>", ""]
        else:
            lines += ["Not rendered — the DraftIR did not pass validation, and an unvalidated",
                      "draft is not rendered under any circumstances.", ""]
    else:
        # Every §147 heading is emitted whether or not a pilot ran. The report is a fixed
        # structure a reader can navigate, and - less obviously - the gate runs the test suite
        # before deciding whether to generate, so a report whose shape depended on the pilot
        # would make the tests unpassable on exactly the run that has to pass them first.
        reason = state.get("no_pilot_reason", "No pilot was generated.")
        lines += ["## Controlled Pilot Generation", "", reason, "",
                  "| Parameter | Value |", "| --- | --- |",
                  table([("Generation calls", state["generation_calls"]),
                         ("Retrieval calls", 0), ("Qdrant writes", 0),
                         ("Automatic retries", 0)]), ""]
        for heading in ("Pilot Draft Validation", "Claim Coverage", "Required Topic Coverage",
                        "Citation Coverage", "Numeric Audit", "Qualifier Audit",
                        "Forbidden Synthesis Audit", "Internal-ID Leak Audit",
                        "Rendered Pilot"):
            lines += [f"## {heading}", "", "Not reached — no draft was generated.", ""]

    lines += [
        "## Frozen Integrity",
        "",
        f"**{integrity['check_count']}** checks, all unchanged: "
        f"**{integrity['all_unchanged']}**"
        + (f" — changed: {integrity['changed']}" if integrity["changed"] else ""),
        "",
        "Corpus, chunks, embeddings, Qdrant, Retriever v1, Context v1, Prompt v5, Output",
        "Contract v1.1, the Production Grounded Generator, the Evidence Note Contract, the Book",
        "Pipeline, Extractor v1.1 and every SEC-02-2 evidence artifact were read and not written.",
        "The drafting prompt is a new downstream role contract, not a Prompt v6.",
        "",
        "## Remaining Limitations",
        "",
    ]
    for limitation in state["limitations"]:
        lines.append(f"- {limitation}")
    lines += [
        "",
        "## Final Decision",
        "",
        f"**{state['final_decision']}**",
        "",
        "## Next Phase",
        "",
        state["next_phase"],
        "",
    ]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# ================================================================ 10. runner

LIMITATIONS = [
    "Support is decided lexically, not semantically. A sentence built entirely from a claim's own "
    "vocabulary but asserting something the claim does not - a reordering that inverts a "
    "condition, say - passes stage C. The composition validator catches the SEC-02-2 cases that "
    "matter; the general case is open, and closing it needs a different kind of checker than a "
    "lexicon.",
    "Written-out numerals ('üç yüz altmış') are invisible to the numeric stage, which keys on "
    "digits. They currently fail as UNSUPPORTED_PROPOSITION because number words are not in the "
    "function lexicon - a correct rejection reached by an unrelated rule, which is weaker than it "
    "looks and should be made deliberate.",
    "Prefix agreement at five characters over-licenses occasionally ('minimum'/'minimize'). No "
    "SEC-02-2 collision is known; the risk grows with the vocabulary as more sections are added.",
    "The word budget (1200-1800) is telemetry, not a gate. Under strict support containment the "
    "only way to reach a word target is to add sentences, and every added sentence is another "
    "proposition to support - a budget enforced as a gate would push the drafter toward exactly "
    "the padding stage C exists to reject.",
    "SEC-02-2-P0-002 was withheld from the pilot by the plan, with a stated reason. Its "
    "enforcement machinery is exercised by fixtures and required tests, not by drafted prose, so "
    "the pilot is not evidence that a drafter handles it correctly under generation.",
    "There is no per-unit language check. The pilot emitted SEC-02-2-P0-008 as untranslated "
    "English in a draft declaring language 'tr', violating §109's requirement of a faithful "
    "Turkish paraphrase. It was rejected - the untranslated text also dropped the claim's "
    "condition - but by an unrelated rule. A unit whose language does not match the draft's is a "
    "translation failure and should fail as one; adding that rule belongs to the remediation "
    "phase, not to a mid-flight change of the contract the pilot was judged against.",
    "The qualifier-retention threshold is half of a qualifier's content anchors, which is a "
    "stated heuristic rather than a derived one. It correctly caught the pilot's dropped "
    "Tablo-351-5 acceptance-criteria qualifier; where the boundary should sit for a longer or "
    "shorter qualifier has not been established.",
    "One pilot is not evidence that the drafting architecture scales. This one was rejected, "
    "which is evidence the validator has teeth on real generated prose - not evidence that a "
    "clean draft is reachable.",
    "An accepted pilot is not publishable text. Human technical editorial review has not "
    "happened and is the next phase's precondition.",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contracts-only", action="store_true",
                        help="author contracts and score fixtures; never generate")
    parser.add_argument("--replay", action="store_true",
                        help="finish from the preserved raw output instead of generating. Every "
                             "step after the model call is deterministic, so a run interrupted "
                             "downstream can be completed without spending a second generation "
                             "on work the first one already did.")
    args = parser.parse_args(argv)

    started = now()
    points_before = qdrant_points()
    allowlist = {row["claim_id"]: row for row in read_jsonl(ALLOWLIST_PATH)}
    safety_bundle = json.loads(SAFETY_BUNDLE_PATH.read_text(encoding="utf-8"))
    regression = json.loads((RESOLUTION / "audits" / "composition_regression_v1.json")
                            .read_text(encoding="utf-8"))

    input_shas = {
        "SEC-02-2 safety bundle": sha_file(SAFETY_BUNDLE_PATH),
        "composition contract": sha_file(COMPOSITION_CONTRACT_PATH),
        "composition-safe allowlist": sha_file(ALLOWLIST_PATH),
        "composition denylist": sha_file(DENYLIST_PATH),
        "claim pair constraints": sha_file(PAIRS_PATH),
        "composition validator": sha_file(COMPOSITION_VALIDATOR_PATH),
        "production grounded generator": sha_file(GENERATOR_PATH),
        "prompt v5": sha_file(PROMPT_V5_PATH),
        "output contract v1.1": sha_file(OUTPUT_CONTRACT_PATH),
        "source registry v1": sha_file(BOOK / "source_registry_v1.jsonl"),
        "p0 source registry": sha_file(
            BOOK / "p0_resolution" / "evidence" / "p0_source_registry_v1.jsonl"),
    }

    readiness = check_input_readiness(safety_bundle, allowlist, regression)
    authored = author_contracts(allowlist)
    plan, registry = authored["plan"], authored["registry"]

    validator = _validator()
    renderer = _renderer()
    bundle = validator.load_bundle()

    fixture_result = validator.run_fixtures(read_jsonl(DRAFT_FIXTURES_PATH), bundle)
    citation_result = renderer.run_fixtures(read_jsonl(CITATION_FIXTURES_PATH))
    determinism_ok = _check_render_determinism(validator, renderer, registry)
    integrity = verify_frozen_integrity()
    tests = run_tests()

    gate = contract_gate(fixture_result, citation_result, tests, integrity, allowlist,
                         readiness, determinism_ok)

    state: dict[str, Any] = {
        "started_at": started, "input_shas": input_shas, "readiness": readiness,
        "allowlist": allowlist, "plan": plan, "fixture_result": fixture_result,
        "citation_result": citation_result, "integrity": integrity, "tests": tests,
        "contract_gate": gate, "determinism_ok": determinism_ok, "generation_calls": 0,
        "limitations": list(LIMITATIONS),
        "contract_status": "CLOSED / GO" if gate["go"] else "CLOSED / NO-GO",
        "pilot_status": "not attempted",
    }

    authorization = {
        "version": DRAFTING_CONTRACT_VERSION, "section_id": SECTION_ID,
        "authored_at": now(), "contract_authorized": gate["go"],
        "contract_gate": gate, "input_readiness": readiness,
        "drafting_fixtures": {k: v for k, v in fixture_result.items() if k != "rows"},
        "citation_fixtures": {k: v for k, v in citation_result.items() if k != "rows"},
        "tests": {k: v for k, v in tests.items() if k != "tail"},
        "frozen_integrity_holds": integrity["all_unchanged"],
        "pilot_accepted": False, "pilot_status": None,
    }

    if not gate["go"]:
        state["no_pilot_reason"] = (
            "The contract gate did not pass, so no generation was attempted. Generation happens "
            "only when every fixture, every test and frozen integrity pass first (§139).")
        state["final_decision"] = "SECTION DRAFTING CONTRACT V1 — CLOSED / NO-GO"
        state["executive_summary"] = (
            f"The contract gate failed on: {gate['failed']}. No model call was made and no "
            f"prose was produced.")
        state["next_phase"] = "Remediate the failed contract gates, then re-run this phase."
        write_json(AUTHORIZATION_PATH, authorization)
        _finalise(state, points_before, None, None, None, None)
        return 1

    if args.contracts_only:
        state["no_pilot_reason"] = "Run with --contracts-only; generation was skipped by request."
        state["final_decision"] = "SECTION DRAFTING CONTRACT V1 — CLOSED / GO (pilot deferred)"
        state["executive_summary"] = "Contracts authored and gated; pilot deferred."
        state["next_phase"] = "Re-run without --contracts-only to generate the pilot."
        write_json(AUTHORIZATION_PATH, authorization)
        _finalise(state, points_before, None, None, None, None)
        return 0

    # -------------------------------------------------------- controlled pilot, one attempt
    payload = build_generation_payload(plan, allowlist)
    if args.replay:
        if not RAW_PATH.exists():
            print(f"--replay needs {RAW_PATH.relative_to(ROOT)}; none exists", file=sys.stderr)
            return 2
        raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
        if sha_text(raw["raw_text"]) != raw["raw_text_sha256"]:
            print("preserved raw output does not match its recorded SHA", file=sys.stderr)
            return 2
        state["replayed"] = True
    else:
        raw = generate_draft(payload)
        write_json(RAW_PATH, raw)
    state["raw"] = raw
    state["raw_sha"] = raw["raw_text_sha256"]
    state["generation_calls"] = 0 if args.replay else 1

    markdown = render_audit = entries = None
    if raw.get("finish_reason") == "length":
        # Distinguished from a schema failure on purpose. A truncated object tells you the budget
        # was wrong; a malformed one tells you the drafter was. Collapsing them would hide a
        # harness misconfiguration behind a verdict about the prose.
        ir, schema_error = None, (
            f"output was truncated at the token ceiling (finish_reason='length', "
            f"{raw.get('usage', {}).get('completion_tokens')} completion tokens against a "
            f"{MAX_TOKENS}-token budget). The DraftIR was cut off mid-object.")
    else:
        try:
            ir = validator.parse_draft_ir(extract_json_object(raw["raw_text"]))
            schema_error = None
        except validator.DraftSchemaError as error:
            ir, schema_error = None, str(error)

    if ir is None:
        state["pilot_status"] = "REJECTED (schema)"
        state["contract_status"] = "CLOSED / GO"
        state["final_decision"] = ("SECTION DRAFTING CONTRACT V1 — CLOSED / GO; "
                                   "SEC-02-2 CONTROLLED DRAFT PILOT V1 — REJECTED")
        state["executive_summary"] = (
            f"Contracts passed every gate. The single controlled generation returned output that "
            f"is not a DraftIR: {schema_error}. There is no repair path and no retry (§80, §85).")
        state["no_pilot_reason"] = f"SCHEMA_INVALID: {schema_error}"
        state["next_phase"] = "SEC-02-2 DRAFT FAILURE REMEDIATION V1 (failure code: SCHEMA_INVALID)"
        authorization["pilot_accepted"] = False
        authorization["pilot_status"] = "CONTRACT_READY_PILOT_REJECTED"
        authorization["pilot_failure_codes"] = ["SCHEMA_INVALID"]
        write_json(AUTHORIZATION_PATH, authorization)
        _finalise(state, points_before, None, None, None, None)
        return 1

    result = validator.validate_draft(ir, bundle)
    state["validation"] = result

    if result.status == "ACCEPT":
        markdown, entries = renderer.render(ir, registry)
        second, _ = renderer.render(ir, registry)
        state["determinism_ok"] = determinism_ok and (markdown == second)
        render_audit = renderer.audit_rendered(markdown, entries)
        state["markdown"], state["render_audit"] = markdown, render_audit

    audit = build_draft_audit(ir, result, entries or [], allowlist, plan, markdown)
    state["audit"] = audit
    pilot = pilot_gate(result, audit, markdown, render_audit, state["determinism_ok"])
    state["pilot_gate"] = pilot

    if pilot["accept"]:
        write_json(ACCEPTED_PATH, ir.as_dict())
        RENDERED_PATH.parent.mkdir(parents=True, exist_ok=True)
        RENDERED_PATH.write_text(markdown, encoding="utf-8")
        write_json(CITATION_MAP_PATH, {
            "version": CITATION_CONTRACT_VERSION, "section_id": SECTION_ID,
            "draft_id": ir.draft_id, "rendered_at": now(),
            "entries": [e.__dict__ for e in entries]})
        state["pilot_status"] = "SEC-02-2 PILOT_DRAFT_ACCEPTED"
        state["final_decision"] = ("SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING "
                                   "CONTRACT V1 — CLOSED / GO; SEC-02-2 PILOT_DRAFT_ACCEPTED "
                                   "(NOT FINAL MANUSCRIPT)")
        state["executive_summary"] = (
            f"All three contracts passed their gates. One controlled generation produced a "
            f"DraftIR whose {audit['totals']['material_units']} material units all validated "
            f"across nine stages, rendered deterministically to Markdown with "
            f"{audit['totals']['citations_rendered']} registry-backed references and no leaked "
            f"internal identifiers. It is a pilot draft, not publishable text.")
        state["next_phase"] = ("SEC-02-2 TECHNICAL DRAFT AUDIT V1 + BOOK STYLE CONTRACT V1, then "
                               "SEC-02-2 FINAL SECTION DRAFT V1 only if accepted. Human "
                               "technical editorial review is required before either.")
        authorization["pilot_accepted"] = True
        authorization["pilot_status"] = "CONTRACT_READY_PILOT_ACCEPTED"
    else:
        state["pilot_status"] = "CONTRACT_READY_PILOT_REJECTED"
        state["final_decision"] = ("SECTION DRAFTING CONTRACT V1 + BOOK CITATION RENDERING "
                                   "CONTRACT V1 — CLOSED / GO; SEC-02-2 CONTROLLED DRAFT "
                                   "PILOT V1 — REJECTED")
        state["executive_summary"] = (
            f"All three contracts passed their gates. The single controlled generation produced "
            f"a schema-valid DraftIR whose prose did not validate: "
            f"{len(result.rejected_unit_ids)} of {audit['totals']['units']} units were rejected "
            f"with codes {result.failure_codes}. No retry was attempted and nothing was "
            f"rendered or released (§62, §85).")
        state["next_phase"] = ("SEC-02-2 DRAFT FAILURE REMEDIATION V1, using the exact failure "
                               "codes recorded in the audit.")
        authorization["pilot_accepted"] = False
        authorization["pilot_status"] = "CONTRACT_READY_PILOT_REJECTED"
        authorization["pilot_failure_codes"] = result.failure_codes
    authorization["pilot_gate"] = pilot
    write_json(AUTHORIZATION_PATH, authorization)
    write_json(AUDIT_PATH, audit)
    _finalise(state, points_before, ir, result, markdown, entries)
    return 0 if pilot["accept"] else 1


def _check_render_determinism(validator, renderer, registry: dict[str, dict]) -> bool:
    """Render a fixed synthetic DraftIR twice and compare bytes (§118)."""
    key = "SRC-DOC000236-8dfa5f799b50"
    ir = validator.DraftIR(
        section_id=SECTION_ID, draft_id="DETERMINISM", draft_version="v1", language="tr",
        title="Determinizm", units=[validator.DraftUnit(
            unit_id="U-A-P01-S01", unit_type="PARAGRAPH_SENTENCE",
            text="Püskürtme betonun basınç dayanım sınıfı minimum C25/30 sınıfındadır.",
            material=True, claim_ids=["SEC-02-2-C-001"], source_keys=[key],
            citation_intents=[{"claim_id": "SEC-02-2-C-001", "source_keys": [key]}])])
    first, _ = renderer.render(ir, registry)
    second, _ = renderer.render(ir, registry)
    return first == second


def _generation_ledger() -> list[dict[str, Any]]:
    """Every model call this phase made, in order, with why each one exists.

    A single `generation_calls: 1` would be true of the run and false of the phase. The truncated
    first attempt is part of the record.
    """
    ledger: list[dict[str, Any]] = []
    for index, (path, note) in enumerate((
            (RAW_ATTEMPT_1_PATH,
             "Truncated at the token ceiling (finish_reason='length', 4095 completion tokens "
             "against max_tokens=4096). The DraftIR was well-formed and cut off mid-object. "
             "Rejected as a harness failure, not evaluated as prose."),
            (RAW_PATH,
             "Completed (finish_reason='stop') at max_tokens=12288 with a leaner unit shape. "
             "This is the attempt the pilot verdict is about.")), start=1):
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        ledger.append({
            "attempt": index, "path": str(path.relative_to(ROOT)),
            "raw_sha256": raw.get("raw_text_sha256"),
            "finish_reason": raw.get("finish_reason"),
            "completion_tokens": (raw.get("usage") or {}).get("completion_tokens"),
            "max_tokens": raw.get("max_tokens"), "temperature": raw.get("temperature"),
            "seed": raw.get("seed"), "model_id": raw.get("model_id"),
            "system_prompt_sha256": raw.get("system_prompt_sha256"),
            "requested_at": raw.get("requested_at"), "note": note})
    return ledger


def _finalise(state: dict[str, Any], points_before: int | None, ir, result, markdown,
              entries) -> None:
    integrity = state["integrity"]
    points_after = qdrant_points()
    manifest = {
        "version": DRAFTING_CONTRACT_VERSION,
        "section_id": SECTION_ID,
        "created_at": now(),
        "parent_version": PARENT_VERSION,
        "input_safety_bundle_sha": state["input_shas"]["SEC-02-2 safety bundle"],
        "drafting_contract_sha": sha_file(DRAFTING_CONTRACT_PATH),
        "citation_contract_sha": sha_file(CITATION_CONTRACT_PATH),
        "draft_validation_contract_sha": sha_file(VALIDATION_CONTRACT_PATH),
        "draft_plan_sha": sha_file(DRAFT_PLAN_PATH),
        "drafting_prompt_sha": sha_file(DRAFTING_PROMPT_PATH),
        "draft_controller_sha": sha_file(CONTROLLER_PATH),
        "citation_renderer_sha": sha_file(CITATION_RENDERER_PATH),
        "draft_validator_sha": sha_file(DRAFT_VALIDATOR_PATH),
        "composition_validator_sha": state["input_shas"]["composition validator"],
        "claim_allowlist_sha": state["input_shas"]["composition-safe allowlist"],
        "claim_denylist_sha": state["input_shas"]["composition denylist"],
        "pair_constraints_sha": state["input_shas"]["claim pair constraints"],
        "prompt_v5_sha": state["input_shas"]["prompt v5"],
        "output_contract_v1_1_sha": state["input_shas"]["output contract v1.1"],
        "input_shas": state["input_shas"],
        "fixture_counts": {
            "drafting_total": state["fixture_result"]["total"],
            "drafting_positive": state["fixture_result"]["positive"],
            "drafting_negative": state["fixture_result"]["negative"],
            "drafting_passed": state["fixture_result"]["passed"],
            "citation_total": state["citation_result"]["total"],
            "citation_passed": state["citation_result"]["passed"],
            "false_accepts": len(state["fixture_result"]["false_accepts"]),
            "false_rejects": len(state["fixture_result"]["false_rejects"]),
            "code_mismatches": len(state["fixture_result"]["code_mismatches"]),
        },
        "fixtures_paths": {
            "drafting": str(DRAFT_FIXTURES_PATH.relative_to(ROOT)),
            "citation": str(CITATION_FIXTURES_PATH.relative_to(ROOT)),
        },
        "fixtures_shas": {
            "drafting": sha_file(DRAFT_FIXTURES_PATH),
            "citation": sha_file(CITATION_FIXTURES_PATH),
        },
        "test_counts": {"tests_run": state["tests"]["tests_run"],
                        "suites": len(state["tests"]["suites"]),
                        "status": state["tests"]["status"]},
        "tests": {k: v for k, v in state["tests"].items() if k != "tail"},
        "input_readiness": state["readiness"],
        "contract_gate": state["contract_gate"],
        "pilot_gate": state.get("pilot_gate"),
        "generation_calls": state["generation_calls"],
        "generation_attempts": _generation_ledger(),
        "retrieval_calls": 0,
        "automatic_retries": 0,
        "automatic_retry_note":
            "No generation was ever repeated at the same configuration after a validation "
            "failure. The one repeat in this phase's ledger followed a token-ceiling truncation "
            "that stopped the model before it finished the object, and it ran at a different "
            "max_tokens - a harness fix, not a resample of a rejected draft.",
        "qdrant_before": points_before,
        "qdrant_after": points_after,
        "qdrant_writes": 0,
        "qdrant_note": "Drafting requires no retrieval. Qdrant was not reachable during this "
                       "run and was not needed; no read or write was issued.",
        "pilot_status": state["pilot_status"],
        "rendered_draft_sha": sha_text(markdown) if markdown else None,
        "draft_ir_sha": sha_file(ACCEPTED_PATH) if ACCEPTED_PATH.exists() else None,
        "raw_draft_sha": state.get("raw_sha"),
        "citation_map_sha": sha_file(CITATION_MAP_PATH) if CITATION_MAP_PATH.exists() else None,
        "draft_audit_sha": sha_file(AUDIT_PATH) if AUDIT_PATH.exists() else None,
        "audit": state.get("audit"),
        "validation_failure_histogram": result.failure_histogram if result else None,
        "validation_failure_codes": result.failure_codes if result else None,
        "rejected_unit_ids": result.rejected_unit_ids if result else None,
        "citation_map": [e.__dict__ for e in entries] if entries else None,
        "frozen_integrity": integrity,
        "implementation": str(CONTROLLER_PATH.relative_to(ROOT)),
        "implementation_sha": sha_file(CONTROLLER_PATH),
        "remaining_limitations": state["limitations"],
        "status": "closed_go" if state["contract_gate"]["go"] else "closed_no_go",
        "final_decision": state["final_decision"],
        "next_phase": state["next_phase"],
    }
    write_json(MANIFEST_PATH, manifest)
    write_report(state)

    # Now that the artifacts exist, audit them. The manifest is rewritten with the result rather
    # than left claiming a pass nobody checked.
    post_run = run_tests(POST_RUN_SUITES)
    manifest["post_run_tests"] = {k: v for k, v in post_run.items() if k != "tail"}
    manifest["post_run_tests_tail"] = post_run["tail"]
    manifest["test_counts"]["post_run_tests_run"] = post_run["tests_run"]
    manifest["test_counts"]["post_run_status"] = post_run["status"]
    manifest["test_counts"]["total_tests_run"] = (
        state["tests"]["tests_run"] + post_run["tests_run"])
    if post_run["status"] != "passed":
        manifest["status"] = "closed_no_go"
        manifest["final_decision"] = (
            f"{manifest['final_decision']} — INVALIDATED: the post-run artifact audit failed "
            f"({post_run['tail'][-1] if post_run['tail'] else 'see suite output'})")
    write_json(MANIFEST_PATH, manifest)
    state["post_run_tests"] = post_run
    write_report(state)


if __name__ == "__main__":
    sys.exit(main())
