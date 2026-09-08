"""Section Drafting Contract v1 - contract shape, lexicon discipline and the required cases.

The required tests (§120-§135) are the ones with names. The rest exist because a support checker
built on a lexicon has one specific way of failing silently: a technical word that slips into the
function lexicon is licensed everywhere in the book, forever, and nothing about the failure looks
like a failure. Several tests below check the lexicon against the claim corpus rather than
checking behaviour, for exactly that reason.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


controller = _load("section_drafting_contract_v1", "scripts/47_section_drafting_contract_v1.py")
validator = _load("section_draft_validator_v1", "scripts/49_section_draft_validator_v1.py")

ALLOWLIST = {row["claim_id"]: row for row in controller.read_jsonl(controller.ALLOWLIST_PATH)}
KEYS = {cid: row["source_keys"] for cid, row in ALLOWLIST.items()}


class DraftingTestCase(unittest.TestCase):
    """Shared harness: build one draft unit and run it through the full nine-stage validator."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = validator.load_bundle()

    def check(self, text, claim_ids, *, keys=None, material=True, paragraph=None,
              relationship="INDEPENDENT", unit_type="PARAGRAPH_SENTENCE"):
        binding = keys if keys is not None else {c: KEYS.get(c, []) for c in claim_ids}
        unit = validator.DraftUnit(
            unit_id="U-T-P01-S01", unit_type=unit_type, text=text, material=material,
            claim_ids=list(claim_ids),
            source_keys=sorted({k for v in binding.values() for k in v}),
            relationship_type=relationship,
            citation_intents=[{"claim_id": c, "source_keys": list(v)}
                              for c, v in binding.items()])
        failures = validator.validate_unit(unit, paragraph or text, self.bundle)
        return sorted({f.code for f in failures}), failures

    def assertRejects(self, code, text, claim_ids, **kwargs):
        codes, failures = self.check(text, claim_ids, **kwargs)
        self.assertIn(code, codes, f"expected {code}, got {codes}: "
                                   f"{[f.detail for f in failures]}")

    def assertAccepts(self, text, claim_ids, **kwargs):
        codes, failures = self.check(text, claim_ids, **kwargs)
        self.assertEqual(codes, [], [f.detail for f in failures])


class ContractShape(unittest.TestCase):
    def test_all_three_contracts_exist_and_are_versioned(self):
        for path, version in (
                (controller.DRAFTING_CONTRACT_PATH, controller.DRAFTING_CONTRACT_VERSION),
                (controller.CITATION_CONTRACT_PATH, controller.CITATION_CONTRACT_VERSION),
                (controller.VALIDATION_CONTRACT_PATH, controller.VALIDATION_CONTRACT_VERSION)):
            with self.subTest(contract=path.name):
                self.assertTrue(path.exists(), f"{path} was not authored")
                self.assertEqual(
                    json.loads(path.read_text(encoding="utf-8"))["version"], version)

    def test_contract_scope_is_sec_02_2_only(self):
        contract = json.loads(controller.DRAFTING_CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(contract["section_id"], "SEC-02-2")
        self.assertIn("SEC-02-2 only", contract["scope"])

    def test_validation_contract_covers_every_rejection_code(self):
        contract = json.loads(controller.VALIDATION_CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(set(contract["rejection_codes"]), set(validator.REJECTION_CODES))
        staged = {code for stage in contract["pipeline"] for code in stage["codes"]}
        unstaged = set(validator.REJECTION_CODES) - staged - {"SCHEMA_INVALID"}
        self.assertEqual(unstaged, set(), f"codes no stage can emit: {sorted(unstaged)}")

    def test_validation_contract_forbids_auto_repair(self):
        contract = json.loads(controller.VALIDATION_CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertIs(contract["policy"]["auto_repair"], False)
        self.assertEqual(contract["policy"]["retry_same_config"], 0)
        self.assertEqual(contract["policy"]["pilot_policy"], "all_or_nothing")

    def test_draft_plan_covers_every_required_topic_with_a_core_claim(self):
        plan = json.loads(controller.DRAFT_PLAN_PATH.read_text(encoding="utf-8"))
        for topic, coverage in plan["required_topics"]["coverage"].items():
            with self.subTest(topic=topic):
                self.assertTrue(coverage["required_core_claim_ids"],
                                f"{topic} has no REQUIRED_CORE claim allocated")

    def test_excluded_claims_each_carry_a_stated_reason(self):
        plan = json.loads(controller.DRAFT_PLAN_PATH.read_text(encoding="utf-8"))
        for claim_id, reason in plan["excluded_claims"].items():
            with self.subTest(claim=claim_id):
                self.assertIn(claim_id, ALLOWLIST)
                self.assertGreater(len(reason), 40, "an exclusion needs a real reason")

    def test_drafting_prompt_exists_and_forbids_bibliography_metadata(self):
        prompt = controller.DRAFTING_PROMPT_PATH.read_text(encoding="utf-8")
        for required in ("Kaynak künyesi", "birim dönüştürme", "DraftIR", "JSON",
                         "sayfa numarası"):
            with self.subTest(phrase=required):
                self.assertIn(required.lower(), prompt.lower())

    def test_prompt_v5_is_untouched(self):
        """The drafting prompt is a new downstream role, not Prompt v6 (§71)."""
        self.assertNotEqual(controller.DRAFTING_PROMPT_PATH, controller.PROMPT_V5_PATH)
        self.assertEqual(controller.sha_file(controller.PROMPT_V5_PATH),
                         controller.PROMPT_V5_BASELINE)


class LexiconDiscipline(unittest.TestCase):
    def test_function_lexicon_contains_no_technical_content_word(self):
        """A technical word here would be licensed in every unit of the book, silently."""
        technical = {"beton", "püskürtme", "çimento", "kalınlık", "dayanım", "kaya", "zemin",
                     "tabaka", "katman", "sistem", "kuru", "yaş", "sınıf", "dozaj", "minimum",
                     "maksimum", "tünel", "hasır", "lif", "durabilite", "sıcaklık",
                     "hızlandırıcı", "optimum", "ekonomik", "yeterli", "güvenli"}
        overlap = technical & set(controller.FUNCTION_LEXICON)
        self.assertEqual(overlap, set(), f"technical words in the function lexicon: {overlap}")

    def test_paraphrase_lexicon_never_changes_a_number_or_a_scope(self):
        for source, targets in controller.PARAPHRASE_LEXICON.items():
            for target in targets:
                with self.subTest(pair=(source, target)):
                    self.assertFalse(any(ch.isdigit() for ch in target))
                    self.assertNotIn(target.lower(), {"kuru", "yaş", "genel", "püskürtme"})

    def test_translation_glosses_only_cover_english_claims(self):
        for claim_id in controller.TRANSLATION_GLOSSES:
            with self.subTest(claim=claim_id):
                self.assertTrue(ALLOWLIST[claim_id]["canonical_claim"].isascii(),
                                f"{claim_id} has a gloss but its claim is not English")

    def test_condition_glosses_name_real_conditions(self):
        for claim_id, conditions in controller.CONDITION_GLOSSES.items():
            with self.subTest(claim=claim_id):
                actual = set(ALLOWLIST[claim_id]["conditions"])
                self.assertLessEqual(set(conditions), actual)

    def test_prohibited_markers_are_absent_from_the_claim_corpus(self):
        """A marker the sources use is not an addition.

        Two words come close: SEC-02-2-C-006 says a layer must reach 'yeterli mertebeye' and
        SEC-02-2-P0-005 sets a floor 'durabilite nedeniyle'. Neither bare word is on the list -
        the predicative 'yeterlidir' is - and the per-unit exemption in the validator covers the
        rest, so a claim that uses a word still licenses it.
        """
        corpus = validator.fold(" ".join(
            " ".join([row["canonical_claim"]] + row["conditions"] + row["qualifiers"])
            for row in ALLOWLIST.values()))
        # Matched the way the validator matches, not by substring. 'zor' occurs inside the
        # qualifier 'zorunlu değildir', and a substring test would report a collision the
        # validator's word-boundary rule does not have - failing on the checker's behalf.
        present = [(family, marker)
                   for family in ("expansion", "universal")
                   for marker in controller.PROHIBITED_MARKERS[family]
                   if validator._marker_present(marker, corpus)]
        self.assertEqual(present, [])

    def test_bound_words_are_not_obligation_markers(self):
        """minimum/maksimum say which side of a value a limit lies on, not how binding it is."""
        for markers in controller.MODALITY_LATTICE["markers"].values():
            for word in ("minimum", "maksimum", "asgari", "azami"):
                with self.subTest(word=word):
                    self.assertNotIn(word, markers)


class RequiredCases(DraftingTestCase):
    """§120-§135. Each is a sentence the contract names and a verdict it fixes in advance."""

    def test_120_unsupported_sentence_is_rejected(self):
        self.assertRejects(
            "UNSUPPORTED_PROPOSITION",
            "Püskürtme beton, bütün zemin koşullarında en ekonomik destek yöntemidir.",
            ["SEC-02-2-C-001"])

    def test_121_unqualified_360_is_rejected(self):
        self.assertRejects("QUALIFIER_DROPPED",
                           "Maksimum çimento miktarı 360 kg/m³'tür.", ["SEC-02-2-P0-002"])

    def test_122_correctly_scoped_360_passes(self):
        self.assertAccepts(
            "Tablo-308-23-b, etki sınıflarına göre projelendirmede esas alınacak genel beton "
            "özelliklerine ilişkindir ve yüksek dayanımlı beton dışında maksimum çimento "
            "miktarı 360 kg/m³ olmalıdır.",
            ["SEC-02-2-P0-002"])

    def test_123_syn_001_historical_synthesis_is_rejected(self):
        self.assertRejects(
            "FORBIDDEN_SYNTHESIS",
            "Tablo-308-23-b'ye göre genel betonda maksimum çimento miktarı 360 kg/m³ olmasına "
            "rağmen kuru sistemde minimum 350 kg/m³ çimento aranmaktadır.",
            ["SEC-02-2-P0-002", "SEC-02-2-R001"])

    def test_123b_syn_001_survives_a_sentence_split(self):
        """§25: splitting the construction across a full stop must not launder it."""
        paragraph = ("Tablo-308-23-b'ye göre genel betonda maksimum çimento miktarı 360 kg/m³ "
                     "olmalıdır. Ancak kuru sistem püskürtme betonda minimum 350 kg/m³ çimento "
                     "aranmaktadır.")
        self.assertRejects("FORBIDDEN_SYNTHESIS", paragraph,
                           ["SEC-02-2-P0-002", "SEC-02-2-R001"], paragraph=paragraph)

    def test_124_derived_150_mm_single_pass_is_rejected(self):
        self.assertRejects(
            "DERIVED_VALUE_AS_SOURCE_STATED",
            "Bir defada uygulanacak püskürtme betonun maksimum kalınlığı 150 mm'yi "
            "geçmeyecektir.", ["SEC-02-2-C-003"])

    def test_125_source_stated_clay_zone_150_mm_passes(self):
        self.assertAccepts(
            "Kil zonlu tabakalar üzerine püskürtme beton uygulamasında ilk püskürtme beton "
            "katmanı genellikle 100-150 mm'dir.", ["SEC-02-2-C-009"])

    def test_126_visible_packet_handle_is_rejected(self):
        self.assertRejects(
            "PACKET_EID_LEAK",
            "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır "
            "[E003].", ["SEC-02-2-C-001"])

    def test_127_unknown_source_key_is_rejected(self):
        self.assertRejects(
            "UNKNOWN_SOURCE_KEY",
            "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
            ["SEC-02-2-C-001"], keys={"SEC-02-2-C-001": ["SRC-UNKNOWN-000000000000"]})

    def test_131_every_material_unit_needs_a_source_key(self):
        self.assertRejects(
            "MISSING_SOURCE_KEY",
            "Püskürtme betonun basınç dayanım sınıfı minimum C25/30 MPa sınıfında olacaktır.",
            ["SEC-02-2-C-001"], keys={"SEC-02-2-C-001": []})

    def test_132_structural_transition_passes_without_a_source(self):
        self.assertAccepts("Bu bölüm dört başlık altında ele alınmaktadır.", [],
                           keys={}, material=False, unit_type="TRANSITION")

    def test_132b_a_transition_that_asserts_is_misclassified(self):
        self.assertRejects("NON_MATERIAL_MISCLASSIFIED",
                           "Bu bölümde 15 cm'lik maksimum kalınlık ele alınmaktadır.",
                           ["SEC-02-2-C-003"], material=False, unit_type="TRANSITION")

    def test_133_claim_expansion_is_rejected(self):
        self.assertRejects(
            "CLAIM_EXPANSION",
            "Kuru sistemde çimento miktarı 350 kg/m³'ten az olmamalıdır, çünkü bu miktar "
            "stabilite için optimum değerdir.", ["SEC-02-2-R001"])

    def test_134_modality_strengthening_is_rejected(self):
        """SEC-02-2-C-011 states 'tavsiye edilen kalınlıklar'; an obligation overstates it."""
        self.assertRejects(
            "MODALITY_DRIFT",
            "Tamir işlerinde priz hızlandırıcı katkı kullanılmaksızın, ek katman veya takviye "
            "donatısı bulunmayan durumda kalınlıklar tepe üstü aynalarda maksimum 30 mm, dik "
            "aynalarda maksimum 50 mm olmak zorundadır.", ["SEC-02-2-C-011"])

    def test_135_dropped_condition_is_rejected(self):
        """SEC-02-2-C-012 holds at ~20 °C without accelerator; unconditional prose drops both."""
        self.assertRejects("CONDITION_DROPPED",
                           "Sonraki katmanın uygulanması için bekleme süresi 3-5 saattir.",
                           ["SEC-02-2-C-012"])

    def test_107_strength_class_is_not_normalised_to_mpa(self):
        self.assertRejects("NUMERIC_DRIFT",
                           "Püskürtme betonun basınç dayanım sınıfı minimum 25 MPa olacaktır.",
                           ["SEC-02-2-C-001"])

    def test_denylisted_claim_is_a_hard_reject(self):
        denied = controller.read_jsonl(controller.DENYLIST_PATH)[0]["claim_id"]
        self.assertRejects("CLAIM_DENYLISTED",
                           "Püskürtme betona ilişkin bir gereklilik belirtilmiştir.",
                           [denied], keys={denied: ["SRC-DOC000236-8dfa5f799b50"]})


class SelfConsistency(DraftingTestCase):
    """A rule that rejects the source's own sentence is broken, not strict."""

    def test_every_claims_own_wording_passes_its_own_rules(self):
        for claim_id, claim in sorted(ALLOWLIST.items()):
            with self.subTest(claim=claim_id):
                paragraph = " ".join([claim["canonical_claim"]] + claim["conditions"]
                                     + claim["qualifiers"])
                self.assertAccepts(claim["canonical_claim"], [claim_id], paragraph=paragraph)


class FixtureSuite(DraftingTestCase):
    def test_fixture_suite_passes_with_no_false_accepts(self):
        fixtures = controller.read_jsonl(controller.DRAFT_FIXTURES_PATH)
        self.assertGreaterEqual(len(fixtures), 80,
                                f"§112 requires at least 80 cases, found {len(fixtures)}")
        result = validator.run_fixtures(fixtures, self.bundle)
        self.assertEqual(result["false_accepts"], [])
        self.assertEqual(result["false_rejects"], [])
        self.assertEqual(result["code_mismatches"], [])
        self.assertTrue(result["all_pass"])

    def test_fixture_suite_has_both_polarities(self):
        fixtures = controller.read_jsonl(controller.DRAFT_FIXTURES_PATH)
        positive = sum(1 for f in fixtures if f["expected_valid"])
        self.assertGreaterEqual(positive, 10)
        self.assertGreaterEqual(len(fixtures) - positive, 20)


if __name__ == "__main__":
    unittest.main()
