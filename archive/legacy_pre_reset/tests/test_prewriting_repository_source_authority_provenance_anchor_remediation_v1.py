import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/87_prewriting_repository_source_authority_provenance_anchor_remediation_v1.py"
OUT = ROOT / "data/book/prewriting_repository_source_authority_provenance_anchor_remediation_v1"
spec = importlib.util.spec_from_file_location("remediation87", SCRIPT)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class RemediationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)

    def test_unique_block_locator(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as td:
            p=Path(td)/"one.json"
            p.write_text(json.dumps({"docling_document":{"texts":[{"self_ref":"#/texts/1","text":"alpha beta","prov":[{"page_no":3}]}]}}))
            rows=mod.block_matches([p],"alpha beta")
            self.assertEqual(1,len(rows)); self.assertEqual(3,rows[0]["page_no"])

    def test_repeated_anchor_is_not_unique(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as td:
            p=Path(td)/"two.json"
            p.write_text(json.dumps({"docling_document":{"texts":[{"self_ref":"#/texts/1","text":"repeat"},{"self_ref":"#/texts/2","text":"repeat"}]}}))
            self.assertEqual(2,len(mod.block_matches([p],"repeat")))

    def test_authority_never_promoted_without_evidence(self):
        rows=json.loads((OUT/"registries/source_authority_registry_v2.json").read_text())["items"]
        self.assertEqual(34,len(rows)); self.assertTrue(all(x["authority_class"]=="UNKNOWN_AUTHORITY" for x in rows))

    def test_bounded_source_limit_and_no_false_validation(self):
        data=json.loads((OUT/"registries/bounded_source_verification_registry_v1.json").read_text())
        self.assertEqual(5,len(data["opened_document_ids"]))
        self.assertFalse(any(x["support_and_scope_verified"] for x in data["items"]))

    def test_claim_and_section_reconciliation(self):
        claims=json.loads((OUT/"registries/remediated_claim_registry_v2.json").read_text())
        sections=json.loads((OUT/"registries/section_claim_readiness_ledger_v3.json").read_text())
        self.assertEqual(602,claims["claim_count"]); self.assertEqual(60,sections["section_count"])
        self.assertFalse(any(x["state"]=="CLAIM_LEVEL_ADMISSIBLE" for x in claims["items"]))

    def test_propositions_unchanged(self):
        old=json.loads((ROOT/"data/book/prewriting_repository_claim_defect_remediation_v1/registries/remediated_claim_registry_v1.json").read_text())["items"]
        new=json.loads((OUT/"registries/remediated_claim_registry_v2.json").read_text())["items"]
        self.assertEqual([x["structured_normalized_semantic_proposition"] for x in old],[x["structured_normalized_semantic_proposition"] for x in new])

    def test_all_audits_pass(self):
        rows=[json.loads(p.read_text()) for p in sorted((OUT/"audits").glob("*.json"))]
        self.assertEqual(12,len(rows)); self.assertTrue(all(x["passed"] for x in rows))

if __name__ == "__main__": unittest.main()
