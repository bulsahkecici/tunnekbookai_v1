"""ARCHITECTURE V2 PLANNER OPTION UNIVERSE REMEDIATION V1 — phase suite.

These tests exist to make the remediation's claims falsifiable rather than asserted. The
substantive ones construct the defect deliberately — a mutated universe, a diverging SHA, an
English token offered as Turkish material, the SEC-02-2-C-005 contradiction rebuilt exactly — and
require the refusal. A suite that only walked the happy path would prove nothing about the class
of failure this phase closes.

Nothing here calls a model, renders a pilot, reads the corpus or touches Qdrant.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ARCH_V2 = ROOT / "data" / "book" / "drafting" / "sec_02_2" / "architecture_v2"
REM = ARCH_V2 / "remediation_v1"
ACCEPTANCE = REM / "contracts" / "planner_universe_remediation_acceptance_contract_v1.json"
MANIFEST = ROOT / "data/book/manifests/architecture_v2_planner_universe_remediation_v1.json"
IMPL_MANIFEST = ROOT / "data/book/manifests/architecture_v2_implementation_v1.json"

ACCEPTANCE_SHA = "117e9ea4b67e536d54bb0cd262e8860649f7415f600f66f4acc742ebca480560"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


V1 = _load("t_v1", "49_section_draft_validator_v1.py")
V1_2 = _load("t_v1_2", "54_section_draft_validator_v1_2.py")
PROOF = _load("t_proof", "63_static_containment_proof_v2.py")
M2_V2 = _load("t_m2_v2", "60_claim_realization_contract_v2.py")
M2_V2_1 = _load("t_m2_v2_1", "68_claim_realization_contract_v2_1.py")
UNIVERSE = _load("t_universe", "69_planner_option_universe_v2_1.py")
RENDER = _load("t_render", "62_deterministic_surface_renderer_v2.py")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.bundle = V1.load_bundle()
        cls.realization = M2_V2_1.load()
        cls.universe, cls.universe_sha = UNIVERSE.load_universe()
        cls.negatives = json.loads(
            (REM / "fixtures" / "negative_fixtures_remediation_v1.json")
            .read_text(encoding="utf-8"))

    def mutated(self, mutate) -> Path:
        payload = json.loads(json.dumps({"universe": self.universe}, ensure_ascii=False))
        mutate(payload["universe"])
        path = REM / "fixtures" / "_test_mutated.json"
        path.write_bytes(UNIVERSE.canonical_bytes(payload))
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path


# ================================================================ freeze


class TestAcceptanceContract(Base):
    def test_contract_frozen_at_recorded_sha(self):
        self.assertEqual(sha_file(ACCEPTANCE), ACCEPTANCE_SHA)
        self.assertEqual(self.manifest["acceptance_contract_sha256"], ACCEPTANCE_SHA)

    def test_contract_declares_it_was_authored_before_results(self):
        contract = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
        self.assertTrue(contract["authored_before_results"])
        self.assertGreaterEqual(len(contract["conditions"]), 20)

    def test_frozen_preflight_drift_zero(self):
        self.assertEqual(self.manifest["frozen_preflight"]["drift"], 0)

    def test_gate_verdict_is_go_with_no_unmet_conditions(self):
        self.assertEqual(self.manifest["gate"]["verdict"], "CLOSED / GO")
        self.assertEqual(self.manifest["gate"]["unmet"], [])


# ================================================================ RM-1


class TestCanonicalUniverse(Base):
    def test_exactly_one_universe_artifact_and_it_carries_its_own_sha(self):
        self.assertTrue(UNIVERSE.UNIVERSE_PATH.is_file())
        stored = json.loads(UNIVERSE.UNIVERSE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(stored["universe_sha256"], self.universe_sha)

    def test_subset_invariant_holds_for_every_exposed_claim(self):
        for option in self.universe["options"]:
            required = set(option["required_roles"])
            available = set(option["available_roles"])
            realizable = set(option["realizable_roles"])
            with self.subTest(claim=option["claim_id"]):
                self.assertLessEqual(required, available)
                self.assertLessEqual(available, realizable)

    def test_no_unrealizable_pair_is_offered(self):
        realizable = set(self.realization.realizable_pairs())
        for option in self.universe["options"]:
            for role in option["available_roles"]:
                with self.subTest(pair=f"{option['claim_id']}/{role}"):
                    self.assertIn((option["claim_id"], role), realizable)

    def test_required_role_absent_from_available_fails_closed_on_load(self):
        def mutate(u):
            option = u["options"][0]
            option["required_roles"] = sorted(set(option["required_roles"]) | {"CONDITION"})
            option["available_roles"] = [r for r in option["available_roles"] if r != "CONDITION"]
        with self.assertRaises(UNIVERSE.UniverseViolation):
            UNIVERSE.load_universe(self.mutated(mutate))

    def test_available_role_absent_from_realizable_fails_closed_on_load(self):
        def mutate(u):
            option = u["options"][0]
            option["available_roles"] = sorted(set(option["available_roles"]) | {"EXEMPLIFICATION"})
            option["realizable_roles"] = [r for r in option["realizable_roles"]
                                          if r != "EXEMPLIFICATION"]
        with self.assertRaises(UNIVERSE.UniverseViolation):
            UNIVERSE.load_universe(self.mutated(mutate))

    def test_injected_alternate_universe_is_refused(self):
        def mutate(u):
            u["options"].append({
                "claim_id": "INJECTED", "topic": None, "source_keys": [],
                "allowed_relationships": [], "statement_role": "CLAIM_STATEMENT",
                "required_roles": ["CLAIM_STATEMENT", "QUALIFIER_SCOPE"],
                "available_roles": ["CLAIM_STATEMENT"], "realizable_roles": ["CLAIM_STATEMENT"],
                "requires_condition_slot": False, "requires_qualifier_slot": True,
                "condition_obligation_basis": "injected"})
        with self.assertRaises(UNIVERSE.UniverseViolation):
            UNIVERSE.load_universe(self.mutated(mutate))

    def test_mandatory_claim_with_no_satisfiable_role_set_fails_the_build(self):
        core = sorted(self.universe["required_core_claim_ids"])[0]
        entries = []
        for entry in self.realization.payload["entries"]:
            if (entry["claim_id"] == core
                    and entry["realization_role"] in UNIVERSE.STATEMENT_ROLES):
                entries.append({**entry, "status": "UNREALIZABLE", "reason": "test",
                                "segments": []})
            else:
                entries.append(entry)
        crippled = M2_V2.RealizationContract({**self.realization.payload, "entries": entries})
        with self.assertRaises(UNIVERSE.UniverseViolation):
            UNIVERSE.build_universe(crippled, self.bundle)
        UNIVERSE.install_obligation_rule(
            {o["claim_id"]: {"registered_conditions":
                             self.bundle.allowlist[o["claim_id"]].get("conditions") or [],
                             "requires_condition_slot": o["requires_condition_slot"]}
             for o in self.universe["options"]})

    def test_no_claim_specific_branch_in_the_derivation_modules(self):
        pattern = re.compile(r"claim_id\s*==|SEC-02-2-(?:C|P0|R)-?\d+")
        for filename in ("68_claim_realization_contract_v2_1.py",
                         "69_planner_option_universe_v2_1.py"):
            source = (ROOT / "scripts" / filename).read_text(encoding="utf-8")
            code = "\n".join(line for line in source.splitlines()
                             if not line.lstrip().startswith("#"))
            code = re.sub(r'""".*?"""', "", code, flags=re.S)
            with self.subTest(module=filename):
                self.assertIsNone(pattern.search(code),
                                  f"claim-specific branch in {filename}")


# ================================================================ the historical contradiction


class TestPilotOneContradiction(Base):
    def option(self, claim_id: str) -> dict:
        return next(o for o in self.universe["options"] if o["claim_id"] == claim_id)

    def test_c005_no_longer_requires_a_condition_slot(self):
        self.assertFalse(self.option("SEC-02-2-C-005")["requires_condition_slot"])

    def test_c005_condition_is_available_and_realizable(self):
        option = self.option("SEC-02-2-C-005")
        self.assertIn("CONDITION", option["available_roles"])
        self.assertIn("CONDITION", option["realizable_roles"])

    def test_both_upstream_defects_are_closed_independently(self):
        # The failure analysis held that either fix alone would have prevented the pilot. Both
        # are in place, so neither is load-bearing on its own.
        option = self.option("SEC-02-2-C-005")
        self.assertFalse(option["requires_condition_slot"])
        self.assertIn("CONDITION", option["available_roles"])

    def test_the_contradiction_rebuilt_exactly_is_refused_at_load(self):
        def mutate(u):
            for option in u["options"]:
                if option["claim_id"] == "SEC-02-2-C-005":
                    option["requires_condition_slot"] = True
                    option["required_roles"] = sorted(set(option["required_roles"])
                                                      | {"CONDITION"})
                    option["available_roles"] = [r for r in option["available_roles"]
                                                 if r != "CONDITION"]
        with self.assertRaises(UNIVERSE.UniverseViolation):
            UNIVERSE.load_universe(self.mutated(mutate))


# ================================================================ RM-2


class TestObligationDerivation(Base):
    def test_withdrawn_obligations_are_backed_by_the_validator_itself(self):
        for option in self.universe["options"]:
            if option["requires_condition_slot"]:
                continue
            claim = self.bundle.allowlist[option["claim_id"]]
            if not (claim.get("conditions") or []):
                continue
            probe = UNIVERSE.probe_statement_alone(
                option["claim_id"], option["statement_role"], self.realization, self.bundle)
            with self.subTest(claim=option["claim_id"]):
                self.assertFalse(probe["condition_dropped"])
                self.assertEqual(probe["histogram"].get("CONDITION_DROPPED", 0), 0)
                # The statement alone may still be REJECTed on its qualifier: qualifier
                # obligations are deliberately not derived from stage E (DF-01). What must be
                # absent is any condition failure, and any other failure would mean the
                # obligation was withdrawn for the wrong reason.
                residual = {code for code in probe["histogram"]
                            if code not in ("QUALIFIER_DROPPED", "QUALIFIER_SEMANTICS_UNMET")}
                self.assertEqual(residual, set())
                if probe["status"] != "ACCEPT":
                    self.assertTrue(claim.get("qualifiers"))

    def test_asserted_obligations_are_backed_by_the_validator_itself(self):
        asserted = [o for o in self.universe["options"] if o["requires_condition_slot"]]
        self.assertTrue(asserted, "the rule must still assert obligations somewhere")
        for option in asserted:
            probe = UNIVERSE.probe_statement_alone(
                option["claim_id"], option["statement_role"], self.realization, self.bundle)
            with self.subTest(claim=option["claim_id"]):
                self.assertTrue(probe["condition_dropped"])

    def test_plan_paragraph_condition_missing_is_still_reachable(self):
        UNIVERSE.ensure_obligation_rule()
        option = next(o for o in self.universe["options"] if o["requires_condition_slot"])
        outcome, detail = PROOF._probe_plan(
            PROOF._plan("P-OBLIG", [PROOF._slot("O1", option["claim_id"],
                                                option["statement_role"])]),
            self.realization, self.bundle)
        self.assertEqual(outcome, "PLAN_VALIDATION_REJECTED")
        self.assertIn("PLAN_PARAGRAPH_CONDITION_MISSING", json.dumps(detail))

    def test_qualifier_obligation_is_unchanged_and_not_derived_from_stage_e(self):
        for option in self.universe["options"]:
            claim = self.bundle.allowlist[option["claim_id"]]
            with self.subTest(claim=option["claim_id"]):
                self.assertEqual(option["requires_qualifier_slot"],
                                 bool(claim.get("qualifiers")))

    def test_probe_failure_leaves_the_obligation_standing(self):
        obligation = UNIVERSE.derive_obligations(
            "SEC-02-2-C-005",
            {**self.bundle.allowlist["SEC-02-2-C-005"], "claim_id": "SEC-02-2-C-005"},
            M2_V2.RealizationContract({**self.realization.payload, "entries": []}),
            self.bundle)
        self.assertTrue(obligation["requires_condition_slot"])
        self.assertIn("fail closed", obligation["condition_obligation_basis"])


# ================================================================ RM-3


class TestRealizationContractV2_1(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index = M2_V2_1.SourceLanguageIndex(cls.bundle)
        cls.delta = cls.manifest["m2_v2_1"]["delta"]

    def test_language_metadata_is_corroborated_by_the_frozen_detector(self):
        corroboration = self.index.corroboration
        self.assertEqual(corroboration["mismatches"], [])
        self.assertEqual(corroboration["claims_checked"], 27)

    def test_a_metadata_detector_disagreement_fails_the_build(self):
        index = M2_V2_1.SourceLanguageIndex(self.bundle)
        index.corroboration = {**index.corroboration, "mismatches": ["SEC-02-2-C-001"]}
        with self.assertRaises(M2_V2_1.LanguageRuleViolation):
            index.require_corroborated()

    def test_diacritic_free_turkish_is_not_classified_as_english(self):
        for text in ("ilk tabaka", "takip eden tabakalar", "ilave tabakalar"):
            with self.subTest(text=text):
                self.assertIsNone(M2_V2.TURKISH_MARK.search(text),
                                  "fixture must be diacritic-free to be meaningful")
                self.assertTrue(self.index.is_admissible_turkish(text))

    def test_english_and_unattested_material_is_refused(self):
        for text in ("normally", "dependent on tunnel size", "In some",
                     "a string that is in no frozen field"):
            with self.subTest(text=text):
                self.assertFalse(self.index.is_admissible_turkish(text))

    def test_r025_normally_remains_unrealizable(self):
        entry = self.realization.entry("SEC-02-2-R025", "QUALIFIER_SCOPE")
        self.assertEqual(entry["status"], "UNREALIZABLE")

    def test_r025_qualifier_scope_is_never_offered_by_the_universe(self):
        for option in self.universe["options"]:
            if option["claim_id"] == "SEC-02-2-R025":
                self.assertNotIn("QUALIFIER_SCOPE", option["available_roles"])

    def test_r025_qualifier_scope_is_rejected_if_a_plan_selects_it(self):
        outcome, _ = PROOF._probe_plan(
            PROOF._plan("P-R025", [PROOF._slot("R1", "SEC-02-2-R025", "QUALIFIER_SCOPE")]),
            self.realization, self.bundle)
        self.assertNotEqual(outcome, "RENDERED")

    def test_the_change_only_widens_and_by_exactly_three_pairs(self):
        self.assertEqual(self.delta["v2_realizable"], 77)
        self.assertEqual(self.delta["v2_1_realizable"], 80)
        self.assertEqual(self.delta["newly_unrealizable"], [])
        self.assertEqual(
            sorted(f"{r['claim_id']}/{r['realization_role']}"
                   for r in self.delta["newly_realizable"]),
            ["SEC-02-2-C-004/CONDITION", "SEC-02-2-C-005/CONDITION",
             "SEC-02-2-C-007/CONDITION"])

    def test_every_newly_realizable_pair_passes_the_unchanged_validator(self):
        UNIVERSE.ensure_obligation_rule()
        for row in self.delta["newly_realizable"]:
            claim_id, role = row["claim_id"], row["realization_role"]
            statement = UNIVERSE._statement_role(claim_id, self.realization)
            payload = RENDER.render_from_raw(
                PROOF._plan(f"P-G-{claim_id}", [PROOF._slot("G1", claim_id, statement),
                                                PROOF._slot("G2", claim_id, role)]),
                self.realization, self.bundle)
            result = V1_2.validate_draft(V1.parse_draft_ir(payload), self.bundle)
            with self.subTest(pair=f"{claim_id}/{role}"):
                self.assertEqual(result.status, "ACCEPT")
                self.assertEqual(dict(result.failure_histogram), {})

    def test_v2_contract_and_module_are_untouched(self):
        impl = json.loads(IMPL_MANIFEST.read_text(encoding="utf-8"))
        recorded = impl["modules"]["M2_claim_realization_contract_v2"]
        self.assertEqual(sha_file(ROOT / recorded["path"]), recorded["sha256"])
        self.assertEqual(sha_file(ROOT / "scripts/60_claim_realization_contract_v2.py"),
                         self.manifest["frozen_code_sha256"]["M2_realization_v2"])

    def test_no_lexicon_or_gloss_widening(self):
        contract = json.loads(
            (ROOT / "data/book/drafting/contracts/section_drafting_contract_v1.json")
            .read_text(encoding="utf-8"))
        for key, recorded in self.manifest["lexicon_sha256"].items():
            current = hashlib.sha256(
                json.dumps(contract.get(key), ensure_ascii=False, sort_keys=True)
                .encode("utf-8")).hexdigest()
            with self.subTest(lexicon=key):
                self.assertEqual(current, recorded)


# ================================================================ proofs


class TestFeasibilityAndPayload(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.feasibility = json.loads(
            (REM / "audits" / "feasibility_proof_v2_1.json").read_text(encoding="utf-8"))
        cls.payload = json.loads(
            (REM / "audits" / "planner_payload_v2_1.json").read_text(encoding="utf-8"))

    def test_a_complete_feasible_plan_exists(self):
        self.assertTrue(self.feasibility["feasible"])
        self.assertEqual(self.feasibility["validation"]["status"], "ACCEPT")
        self.assertEqual(self.feasibility["validation"]["histogram"], {})

    def test_all_required_topics_are_covered(self):
        self.assertEqual(self.feasibility["topics"]["covered"],
                         self.feasibility["topics"]["required"])
        self.assertEqual(self.feasibility["required_core_claims_missing"], [])

    def test_conditions_qualifiers_numerics_and_keys_survive(self):
        self.assertEqual(self.feasibility["mandatory_conditions_dropped"], 0)
        self.assertEqual(self.feasibility["mandatory_qualifiers_dropped"], 0)
        self.assertEqual(self.feasibility["numeric_drift"], 0)
        self.assertTrue(self.feasibility["source_keys_valid"])
        self.assertTrue(self.feasibility["relations_supported"])
        self.assertEqual(self.feasibility["language_failures"], [])

    def test_no_unrealizable_pair_is_selected(self):
        self.assertEqual(self.feasibility["unrealizable_pairs_selected"], [])

    def test_the_pilot_1_omission_is_recovered(self):
        # Pilot #1's feasible plan omitted SEC-02-2-C-005, 15 of 16 allocated claims.
        self.assertIn("SEC-02-2-C-005", self.feasibility["claims_stated"])
        self.assertEqual(len(self.feasibility["claims_stated"]), 16)

    def test_both_consumers_read_the_same_universe_sha(self):
        self.assertEqual(self.feasibility["universe_sha256"],
                         self.payload["universe_sha256"])
        self.assertEqual(self.feasibility["universe_sha256"], self.universe_sha)

    def test_a_diverging_payload_universe_is_detectable_by_sha(self):
        divergent = json.loads(json.dumps(self.universe, ensure_ascii=False))
        divergent["options"] = divergent["options"][:-1]
        self.assertNotEqual(
            UNIVERSE.sha_bytes(UNIVERSE.canonical_bytes(divergent)), self.universe_sha)

    def test_the_payload_was_built_and_not_sent(self):
        self.assertFalse(self.payload["model_called"])
        self.assertEqual(self.payload["unrealizable_pairs_exposed"], 0)


class TestStaticProof(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.proof = json.loads(
            (REM / "audits" / "static_containment_proof_v2_1.json").read_text(encoding="utf-8"))

    def test_proof_passes_with_an_empty_histogram(self):
        self.assertEqual(self.proof["status"], "PASS")
        self.assertEqual(self.proof["failure_histogram"], {})
        self.assertEqual(self.proof["zero_tolerance_violations"], {})

    def test_no_false_accepts_and_no_false_rejects(self):
        self.assertEqual(self.proof["false_accepts"], [])
        self.assertEqual(self.proof["false_rejects"], [])

    def test_every_unrealizable_pair_is_refused_and_none_leak(self):
        refusals = self.proof["unrealizable_refusals"]
        self.assertEqual(refusals["refused"], refusals["checked"])
        self.assertEqual(refusals["leaked"], [])

    def test_rendering_is_deterministic_across_processes(self):
        self.assertTrue(self.proof["determinism"]["in_process_identical"])
        self.assertTrue(self.proof["determinism"]["cross_process_identical"])

    def test_the_validator_is_unchanged(self):
        self.assertFalse(self.proof["validator_changed"])
        self.assertEqual(self.proof["validator_version"], V1_2.VALIDATOR_VERSION)

    def test_the_m5_artifacts_were_not_overwritten(self):
        for key in ("M5_negative_fixtures_v2", "M5_realization_universe_v2",
                    "M5_static_containment_proof_v2_as_found"):
            with self.subTest(artifact=key):
                self.assertIn(key, self.manifest["historical_sha256"])
        self.assertNotIn(key, self.manifest["historical_regression"]["artifact_drift"])


# ================================================================ regression and accounting


class TestNegativeFixtures(Base):
    def test_every_declared_negative_fixture_rejects(self):
        self.assertTrue(self.negatives["all_rejected"])
        self.assertEqual(self.negatives["not_rejected"], [])

    def test_the_required_defect_classes_are_all_covered(self):
        ids = {f["fixture_id"] for f in self.negatives["fixtures"]}
        self.assertLessEqual(
            {"NEG-U01", "NEG-U02", "NEG-U03", "NEG-U04", "NEG-U05", "NEG-U06",
             "NEG-U07", "NEG-U08", "NEG-U09", "NEG-U10", "NEG-U11"}, ids)


class TestHistoricalRegression(Base):
    def test_frozen_artifacts_are_byte_identical(self):
        for key, recorded in self.manifest["historical_sha256"].items():
            path = ROOT / _historical_path(key)
            with self.subTest(artifact=key):
                self.assertEqual(sha_file(path), recorded)

    def test_frozen_modules_are_byte_identical(self):
        driver = _load("t_driver", "70_architecture_v2_planner_universe_remediation_v1.py")
        for key, recorded in self.manifest["frozen_code_sha256"].items():
            with self.subTest(module=key):
                self.assertEqual(sha_file(ROOT / "scripts" / driver.FROZEN_CODE[key]), recorded)

    def test_pilot_1_artifacts_and_verdict_are_untouched(self):
        validation = json.loads(
            (ARCH_V2 / "pilot_1/validation/pilot_1_validation.json").read_text(encoding="utf-8"))
        self.assertIn("PLAN_ROLE_UNREALIZABLE", json.dumps(validation))
        self.assertEqual(self.manifest["historical_regression"]["artifact_drift"], [])

    def test_no_generation_render_retrieval_qdrant_or_corpus_access(self):
        accounting = self.manifest["accounting"]
        for key in ("generation_calls", "renders_released", "retrieval_calls", "qdrant_writes",
                    "corpus_reads", "validators_weakened", "failure_codes_changed",
                    "lexicon_entries_added", "frozen_artifacts_modified",
                    "claim_specific_branches"):
            with self.subTest(counter=key):
                self.assertEqual(accounting[key], 0)
        self.assertFalse(accounting["pilot_2_authorised"])


def _historical_path(key: str) -> str:
    driver = _load("t_driver_paths", "70_architecture_v2_planner_universe_remediation_v1.py")
    return str(driver.HISTORICAL_ARTIFACTS[key].relative_to(ROOT))


if __name__ == "__main__":
    unittest.main()
