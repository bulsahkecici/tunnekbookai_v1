import importlib.util
from pathlib import Path
import unittest

P=Path(__file__).resolve().parents[1]/"scripts/85_prewriting_repository_claim_defect_remediation_v1.py"
S=importlib.util.spec_from_file_location("remediation",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)

class RemediationGate(unittest.TestCase):
    def test_positive_01_verified_authority(self): self.assertEqual(M.classify_authority({"evidence_status":"VERIFIED","authority_class":"PRIMARY_OFFICIAL","applicable_claim_scopes":["own"],"supporting_metadata":{"publisher":"x"},"canonical_source_relation":"r"},"own"),"PRIMARY_OFFICIAL")
    def test_positive_02_unique_anchor(self): self.assertEqual(M.disambiguate_anchor("alpha beta","beta")["state"],"ANCHOR_RESOLVED")
    def test_positive_03_offset_duplicate(self): self.assertEqual(M.disambiguate_anchor("x x","x",{"start":2,"end":3})["state"],"ANCHOR_RESOLVED")
    def test_positive_04_admissible(self): self.assertEqual(M.disposition("PRIMARY_OFFICIAL",True,"ANCHOR_RESOLVED",True),"CLAIM_LEVEL_ADMISSIBLE")
    def test_positive_05_scope_precedence(self): self.assertEqual(M.disposition("PRIMARY_OFFICIAL",True,"ANCHOR_RESOLVED",False),"SCOPE_INSUFFICIENT")
    def test_positive_06_token_determinism(self): self.assertEqual(M.tokens("Tunnel tunnel scope"),M.tokens("Tunnel tunnel scope"))
    def test_negative_01_no_evidence(self): self.assertEqual(M.classify_authority(None,"own"),"UNKNOWN_AUTHORITY")
    def test_negative_02_unverified(self): self.assertEqual(M.classify_authority({"evidence_status":"C","authority_class":"PRIMARY_OFFICIAL"},"own"),"UNKNOWN_AUTHORITY")
    def test_negative_03_bad_class(self): self.assertEqual(M.classify_authority({"evidence_status":"VERIFIED","authority_class":"C","applicable_claim_scopes":["own"],"supporting_metadata":1,"canonical_source_relation":1},"own"),"UNKNOWN_AUTHORITY")
    def test_negative_04_scope(self): self.assertEqual(M.classify_authority({"evidence_status":"VERIFIED","authority_class":"PRIMARY_OFFICIAL","applicable_claim_scopes":["project"],"supporting_metadata":1,"canonical_source_relation":1},"universal"),"UNKNOWN_AUTHORITY")
    def test_negative_05_title_only(self): self.assertEqual(M.classify_authority({"evidence_status":"VERIFIED","authority_class":"PRIMARY_OFFICIAL","applicable_claim_scopes":["own"],"supporting_metadata":{},"canonical_source_relation":"r"},"own"),"UNKNOWN_AUTHORITY")
    def test_negative_06_duplicate(self): self.assertEqual(M.disambiguate_anchor("x x","x")["state"],"ANCHOR_AMBIGUOUS")
    def test_negative_07_missing(self): self.assertEqual(M.disambiguate_anchor("x","y")["state"],"SOURCE_LOCATION_INSUFFICIENT")
    def test_negative_08_anchor_blocks(self): self.assertEqual(M.disposition("PRIMARY_OFFICIAL",True,"ANCHOR_AMBIGUOUS",True),"ANCHOR_AMBIGUOUS")
    def test_negative_09_provenance_blocks(self): self.assertEqual(M.disposition("PRIMARY_OFFICIAL",False,"ANCHOR_RESOLVED",True),"PROVENANCE_BLOCKED")
    def test_negative_10_unknown_blocks(self): self.assertEqual(M.disposition("UNKNOWN_AUTHORITY",True,"ANCHOR_RESOLVED",True),"AUTHORITY_INSUFFICIENT")
    def test_negative_11_empty_anchor(self): self.assertEqual(M.disambiguate_anchor("x","")["state"],"SOURCE_LOCATION_INSUFFICIENT")
    def test_negative_12_universal_scope(self): self.assertEqual(M.classify_authority({"evidence_status":"VERIFIED","authority_class":"PROJECT_TECHNICAL","applicable_claim_scopes":["own"],"supporting_metadata":1,"canonical_source_relation":1},"universal"),"UNKNOWN_AUTHORITY")

if __name__=="__main__": unittest.main()
