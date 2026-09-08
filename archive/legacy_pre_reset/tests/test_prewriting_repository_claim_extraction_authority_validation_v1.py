import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/84_prewriting_repository_claim_extraction_authority_validation_v1.py"
SPEC = importlib.util.spec_from_file_location("claim_validation_v1", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def valid_claim(authority="PRIMARY_OFFICIAL"):
    return {
        "support_anchor": {"exact_text": "The lining shall resist the specified load."},
        "atomicity_status": "ATOMIC",
        "provenance": {"status": "page_resolved"},
        "scope_validation": {"section_and_rq_match": True},
        "authority_validation": {"claim_relative_class": authority},
        "freshness": {"status": "CURRENT_OR_NOT_TIME_SENSITIVE"},
    }


class ClaimValidationFixtures(unittest.TestCase):
    source = "The lining shall resist the specified load."

    def test_six_positive_fixtures(self):
        classes = [
            "PRIMARY_OFFICIAL", "STANDARD_SPECIFICATION", "SECONDARY_TECHNICAL",
            "EXPERT_INTERPRETIVE", "PRACTICE_BASED", "PRIMARY_OFFICIAL",
        ]
        for authority in classes:
            with self.subTest(authority=authority):
                self.assertEqual(MOD.validate_claim(valid_claim(authority), self.source), ("CLAIM_LEVEL_ADMISSIBLE", []))

    def test_thirteen_negative_fixtures(self):
        mutations = [
            ("missing_anchor", lambda c: c["support_anchor"].update(exact_text="Missing."), "CLAIM_EXTRACTION_UNRESOLVED"),
            ("duplicate_anchor", lambda c: None, "CLAIM_EXTRACTION_UNRESOLVED"),
            ("non_atomic", lambda c: c.update(atomicity_status="COMPOUND"), "CLAIM_EXTRACTION_UNRESOLVED"),
            ("source_only", lambda c: c["provenance"].update(status="source_only"), "PROVENANCE_INCOMPLETE"),
            ("missing_provenance", lambda c: c["provenance"].update(status=None), "PROVENANCE_INCOMPLETE"),
            ("scope_mismatch", lambda c: c["scope_validation"].update(section_and_rq_match=False), "SCOPE_MISMATCH"),
            ("scope_missing", lambda c: c.update(scope_validation={}), "SCOPE_MISMATCH"),
            ("unknown_authority", lambda c: c["authority_validation"].update(claim_relative_class="UNKNOWN_AUTHORITY"), "AUTHORITY_INSUFFICIENT"),
            ("authority_missing", lambda c: c.update(authority_validation={"claim_relative_class": "UNKNOWN_AUTHORITY"}), "AUTHORITY_INSUFFICIENT"),
            ("stale", lambda c: c["freshness"].update(status="STALE_OR_UNDATED"), "STALE_OR_UNDATED"),
            ("undated", lambda c: c["freshness"].update(status="STALE_OR_UNDATED"), "STALE_OR_UNDATED"),
            ("empty_anchor", lambda c: c.update(support_anchor={"exact_text": ""}), "CLAIM_EXTRACTION_UNRESOLVED"),
            ("bad_atomicity", lambda c: c.update(atomicity_status=None), "CLAIM_EXTRACTION_UNRESOLVED"),
        ]
        for name, mutate, expected in mutations:
            with self.subTest(name=name):
                claim = valid_claim()
                mutate(claim)
                source = self.source * 2 if name == "duplicate_anchor" else self.source
                self.assertEqual(MOD.validate_claim(claim, source)[0], expected)

    def test_contract_classes_and_states_are_complete(self):
        self.assertEqual(len(MOD.AUTHORITY_CLASSES), 6)
        self.assertEqual(len(MOD.FINAL_STATES), 8)


if __name__ == "__main__":
    unittest.main()
