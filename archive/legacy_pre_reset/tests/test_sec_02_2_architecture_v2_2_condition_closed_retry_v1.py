from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1_rerun"
SCRIPT = ROOT / "scripts/78_architecture_v2_2_condition_closed_retry_v1.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


spec = importlib.util.spec_from_file_location("condition_closed_retry_test", SCRIPT)
retry = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = retry
spec.loader.exec_module(retry)


class TestFrozenAndClosureGates(unittest.TestCase):
    def test_acceptance_was_frozen_before_integration(self):
        freeze = load(BASE / "audits/acceptance_freeze_v1.json")
        self.assertTrue(freeze["frozen_before_integration_and_rendering"])
        self.assertEqual(sha256(ROOT / freeze["contract_path"]), freeze["contract_sha256"])

    def test_historical_preflight_has_zero_live_drift(self):
        baseline = load(ROOT / "data/book/drafting/sec_02_2/architecture_v2_2_retry_v1/audits/frozen_preflight_v1.json")
        self.assertEqual(len(baseline["artifacts"]), 49)
        for relative, expected in baseline["artifacts"].items():
            self.assertEqual(sha256(ROOT / relative), expected)

    def test_closure_gate_passes_before_renderer(self):
        proof = retry.closure_gate()
        self.assertEqual(proof["fully_feasible_instances"], 20)
        self.assertEqual(proof["condition_requirements_closed"], 25)
        self.assertEqual(proof["dependency_requirements_closed"], 2)

    def test_no_claim_specific_renderer_branch(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("Swelling Rock", source)
        self.assertNotIn("SEC-02-2-P0-008", source)


class TestIntegrationGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = retry.evaluate()
        cls.units = {row["unit_id"]: row for row in cls.result["draft_ir"]["units"]}

    def test_unchanged_validator_and_fallback_accept(self):
        validation = self.result["validation"]
        self.assertEqual(validation["validator_version"], "tunnelbook-section-draft-validator-v1.2")
        self.assertEqual(validation["status"], "ACCEPT")
        self.assertEqual(validation["failure_histogram"], {})
        self.assertEqual(validation["fallback_failures"], [])
        self.assertEqual(validation["rejected_unit_ids"], [])

    def test_p0_008_safe_allocation_is_visible(self):
        statement = self.units["U-C-P02-S01"]["text"]
        cases = self.units["U-C-P02-S02"]["text"]
        self.assertIn("Belirli", statement)
        self.assertIn("tünel boyutuna bağlı", statement)
        self.assertEqual(cases, "Belirli ezilmiş kaya, sıkışan kaya ve **Swelling Rock**.")

    def test_all_six_technical_blockers_pass(self):
        audit = load(BASE / "audits/integration_audit_v1.json")
        self.assertEqual(audit["technical_blockers_surface_validated"], "6/6")
        self.assertTrue(all(row["status"] == "PASS" for row in audit["technical_blockers"]))

    def test_citation_ownership_and_required_topics(self):
        registry = retry.integration._extended_bundle().registry
        for unit in self.result["draft_ir"]["units"]:
            self.assertEqual(unit["citation_intents"][0]["claim_id"], unit["claim_ids"][0])
            self.assertEqual(unit["citation_intents"][0]["source_keys"], unit["source_keys"])
            self.assertTrue(all(key in registry for key in unit["source_keys"]))
        markdown = self.result["markdown"]
        for topic in ("dayanım sınıfı", "Çimento Dozajı", "Kaplama Kalınlığı"):
            self.assertIn(topic, markdown)

    def test_book_style_projection(self):
        markdown = self.result["markdown"]
        headings = [line for line in markdown.splitlines() if line.startswith("#")]
        self.assertEqual(headings[-1], "## Kaynaklar")
        self.assertIn("### Yaş Sistem", headings)
        self.assertIn("### Tamir İşleri", headings)
        self.assertFalse(any(line.startswith(("- ", "* ", "|")) for line in markdown.splitlines()))

    def test_accounting_is_zero(self):
        self.assertEqual(set(self.result["accounting"].values()), {0})


class TestStorageAndDeterminism(unittest.TestCase):
    def test_exactly_one_additive_accepted_draft(self):
        drafts = list((BASE / "rendered").glob("*"))
        self.assertEqual([path.name for path in drafts], ["accepted_draft_v1.json"])
        stored = load(drafts[0])
        self.assertEqual(stored["artifact_status"], "V2_2_TECHNICAL_STYLE_DRAFT_ACCEPTED")
        self.assertFalse(stored["final_manuscript"])
        self.assertEqual(stored["draft_ir"], retry.evaluate()["draft_ir"])
        self.assertEqual(stored["rendered_markdown"], retry.evaluate()["markdown"])

    def test_three_in_process_and_one_fresh_process_are_identical(self):
        values = [retry.integration.canonical_bytes(retry.evaluate()) for _ in range(3)]
        fresh = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True).stdout
        self.assertEqual(len(set(values + [fresh])), 1)
        audit = load(BASE / "audits/determinism_v1.json")
        self.assertEqual(hashlib.sha256(fresh).hexdigest(), audit["canonical_evaluation_sha256"])

    def test_acceptance_is_closed_go(self):
        result = load(BASE / "audits/acceptance_results_v1.json")
        self.assertEqual(result["verdict"], "CLOSED_GO")
        self.assertEqual(result["summary"], {"total": 16, "passed": 16, "failed": 0})
        self.assertEqual(result["next_phase"], "SEC-02-2 TECHNICAL DRAFT RE-AUDIT V2")

    def test_manifest_hashes_and_accounting(self):
        manifest = load(ROOT / "data/book/manifests/sec_02_2_architecture_v2_2_technical_style_integration_retry_v1_rerun.json")
        self.assertEqual(manifest["status"], "CLOSED_GO")
        for artifact in manifest["artifacts"].values():
            self.assertEqual(sha256(ROOT / artifact["path"]), artifact["sha256"])
        self.assertEqual(manifest["accounting"]["stored_drafts"], 1)
        self.assertEqual(manifest["accounting"]["released_drafts"], 0)


if __name__ == "__main__":
    unittest.main()
