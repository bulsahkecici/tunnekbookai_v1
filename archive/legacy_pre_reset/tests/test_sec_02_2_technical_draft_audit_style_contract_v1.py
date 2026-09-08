from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/book/drafting/sec_02_2/technical_draft_audit_v1/audits/sec_02_2_technical_draft_audit_v1.json"
STYLE = ROOT / "data/book/drafting/contracts/book_style_contract_v1.json"
MANIFEST = ROOT / "data/book/manifests/sec_02_2_technical_draft_audit_style_contract_v1.json"
IR = ROOT / "data/book/drafting/sec_02_2/architecture_v2/pilot_2/rendered/rendered_draft_ir_v2.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestTechnicalDraftAuditV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load(AUDIT)
        cls.ir = load(IR)

    def test_target_is_exact_immutable_accepted_pilot(self):
        target = self.audit["audit_target"]
        path = ROOT / target["path"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), target["sha256"])
        self.assertEqual(target["status"], "PILOT_DRAFT_ACCEPTED")
        self.assertFalse(target["released"])

    def test_audit_is_source_bounded(self):
        ir_keys = {key for unit in self.ir["units"] for key in unit["source_keys"]}
        self.assertEqual(set(self.audit["audited_source_keys"]), ir_keys)
        self.assertEqual(set(self.audit["audited_documents"]),
                         {key.split("-")[1] for key in ir_keys})

    def test_no_go_is_backed_by_visible_findings(self):
        findings = self.audit["findings"]
        blocking = [f for f in findings if f["severity"].startswith("BLOCKING_")]
        advisory = [f for f in findings if f["severity"].startswith("ADVISORY_")]
        self.assertEqual(self.audit["verdict"], "NO_GO")
        self.assertFalse(self.audit["release_authorised"])
        self.assertEqual(len(blocking), self.audit["summary"]["blocking_findings"])
        self.assertEqual(len(advisory), self.audit["summary"]["advisory_findings"])
        self.assertEqual({f["finding_id"] for f in findings},
                         {f"TDA-{index:03d}" for index in range(1, 9)})

    def test_required_review_dimensions_are_explicit(self):
        dimensions = self.audit["dimension_results"]
        self.assertEqual(set(dimensions),
                         {"factual", "citation", "language", "condition", "qualifier"})
        self.assertEqual(dimensions["factual"]["result"], "FAIL")
        self.assertEqual(dimensions["citation"]["result"], "FAIL")
        self.assertEqual(dimensions["condition"]["result"], "FAIL")

    def test_findings_are_claim_and_source_traced(self):
        rendered_claims = {claim for unit in self.ir["units"] for claim in unit["claim_ids"]}
        rendered_sources = {key for unit in self.ir["units"] for key in unit["source_keys"]}
        for finding in self.audit["findings"]:
            with self.subTest(finding=finding["finding_id"]):
                self.assertTrue(set(finding["claim_ids"]) <= rendered_claims)
                self.assertTrue(set(finding["source_keys"]) <= rendered_sources)
                self.assertTrue(finding["source_location"])
                self.assertTrue(finding["required_remediation"])


class TestBookStyleContractV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.style = load(STYLE)

    def test_contract_is_deterministic_and_forbids_model_rewrite(self):
        self.assertEqual(self.style["status"], "CLOSED_GO")
        self.assertEqual(self.style["model_style_pass"], "FORBIDDEN")
        self.assertEqual(self.style["post_render_rewrite"], "FORBIDDEN")
        self.assertEqual(self.style["cohesion_rules"]["free_form_transition_generation"],
                         "FORBIDDEN")

    def test_contract_preserves_claim_bound_units(self):
        rules = self.style["unit_rules"]
        self.assertTrue(rules["one_claim_slot_one_material_unit"])
        self.assertFalse(rules["merge_claim_lexical_pools"])
        self.assertTrue(rules["citation_on_every_material_unit"])

    def test_contract_freezes_section_hierarchy(self):
        self.assertEqual(self.style["sec_02_2_heading_map"], {
            "A": "Püskürtme Betonun Malzeme ve Dayanım Gereklilikleri",
            "B": "Çimento Dozajı",
            "C": "Kaplama Kalınlığı ve Katman Düzeni",
            "D": "Uygulama Koşulları ve Özel Durumlar",
        })
        self.assertGreaterEqual(len(self.style["ordering_rules"]), 7)

    def test_current_pilot_is_not_released_by_style_contract(self):
        assessment = self.style["current_pilot_assessment"]
        self.assertEqual(assessment["result"], "NO_GO")
        self.assertEqual(assessment["release_status"], "NOT_RELEASED")


class TestPhaseManifest(unittest.TestCase):
    def test_accounting_and_frozen_integrity(self):
        manifest = load(MANIFEST)
        self.assertEqual(manifest["status"], "CLOSED_NO_GO")
        accounting = manifest["accounting"]
        for field in ("generation_calls", "post_render_model_calls", "retrieval_calls",
                      "qdrant_writes", "validators_changed", "thresholds_changed",
                      "failure_codes_changed", "frozen_artifacts_modified",
                      "pilot_artifacts_modified", "claims_modified",
                      "lexicons_or_glosses_modified", "drafts_released"):
            self.assertEqual(accounting[field], 0, field)
        self.assertEqual(accounting["corpus_documents_read"], 3)
        for relative, expected in manifest["frozen_integrity"].items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                                 expected)


if __name__ == "__main__":
    unittest.main()
