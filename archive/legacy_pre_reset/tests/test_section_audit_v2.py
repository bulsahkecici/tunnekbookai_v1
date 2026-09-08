import json
import tempfile
import unittest
from pathlib import Path

from scripts.section_audit_v2 import (
    AuditContractError,
    apply_human_review,
    freeze_exact,
    split_sentences,
    validate_evidence_audit,
)


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class ValidateEvidenceAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.sentence_map_path = self.root / "sentence_map.json"
        self.audit_path = self.root / "evidence_audit.json"
        self.packet_path = self.root / "packet.json"

        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {"sentence_id": "S001"},
                    {"sentence_id": "S002"},
                ],
            },
        )

        write_json(
            self.packet_path,
            {
                "admitted_claims": [
                    {"claim_id": "C001"},
                    {"claim_id": "C002"},
                ],
            },
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _base_audit(self, rows, **extra):
        audit = {
            "section_id": "CH-A-S04",
            "sentence_audit": rows,
        }
        audit.update(extra)
        return audit

    def test_clean_supported_rows_pass_despite_summary_mismatch(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ],
                decision="PASS",
                summary={
                    "supported": 34,
                    "partially_supported": 0,
                    "unsupported": 0,
                    "scope_leakage": 0,
                },
            ),
        )

        gate = validate_evidence_audit(
            self.sentence_map_path, self.audit_path, self.packet_path
        )

        self.assertEqual(gate["decision"], "PASS")
        self.assertEqual(gate["supported"], 2)
        self.assertIn("supported", gate["model_summary_mismatch"])

    def test_missing_sentence_id_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_duplicate_sentence_id_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_extra_sentence_id_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                    {
                        "sentence_id": "S999",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_supported_without_claims_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": [],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_unknown_claim_id_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C999"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_partially_supported_row_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "PARTIALLY_SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_qualifier_issues_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ],
                qualifier_issues=["S001: hedging removed"],
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_required_actions_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ],
                required_actions=["rewrite S001"],
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_invalid_status_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "MOSTLY_TRUE",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_unsupported_source_identity_row_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "UNSUPPORTED_SOURCE_IDENTITY",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_redundancy_row_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S001",
                        "status": "REDUNDANCY",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_section_mismatch_fails(self):
        write_json(
            self.audit_path,
            {
                "section_id": "CH-A-S99",
                "sentence_audit": [],
            },
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )


class NarrativeSynthesisTests(unittest.TestCase):
    """Regression tests for the NARRATIVE_SYNTHESIS status, modeled on the
    CH-A-S04 S006/S024 narrative-transition sentences that triggered this
    policy."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.sentence_map_path = self.root / "sentence_map.json"
        self.audit_path = self.root / "evidence_audit.json"
        self.packet_path = self.root / "packet.json"

        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {
                        "sentence_id": "S006",
                        "text": (
                            "Bu iki gelismenin bir araya gelmesi tunel "
                            "insaatinda yeni bir donemi baslatmistir."
                        ),
                    },
                    {"sentence_id": "S002", "text": "Diger cumle."},
                ],
            },
        )

        write_json(
            self.packet_path,
            {
                "admitted_claims": [
                    {
                        "claim_id": "C001",
                        "claim_text": (
                            "Basincli hava yontemi tunel insaatinda "
                            "kullanilmistir."
                        ),
                    },
                    {
                        "claim_id": "C002",
                        "claim_text": (
                            "Dinamit kullanimi kazi hizini artirmistir."
                        ),
                    },
                ],
            },
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _base_audit(self, rows, **extra):
        audit = {
            "section_id": "CH-A-S04",
            "sentence_audit": rows,
        }
        audit.update(extra)
        return audit

    def test_valid_narrative_synthesis_passes(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C001", "C002"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        gate = validate_evidence_audit(
            self.sentence_map_path, self.audit_path, self.packet_path
        )

        self.assertEqual(gate["decision"], "PASS")
        self.assertEqual(gate["narrative_synthesis"], 1)

    def test_narrative_synthesis_without_claims_fails(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": [],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_narrative_synthesis_with_new_number_fails(self):
        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {
                        "sentence_id": "S024",
                        "text": (
                            "Bu gelismeler 1871 yilinda tunelin acilmasina "
                            "zemin hazirlamistir."
                        ),
                    },
                    {"sentence_id": "S002", "text": "Diger cumle."},
                ],
            },
        )
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S024",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C001", "C002"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_narrative_synthesis_with_new_proper_noun_fails(self):
        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {
                        "sentence_id": "S006",
                        "text": (
                            "Bu gelismeler Gotthard tunelinde yeni bir "
                            "donem baslatmistir."
                        ),
                    },
                    {"sentence_id": "S002", "text": "Diger cumle."},
                ],
            },
        )
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C001", "C002"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_narrative_synthesis_with_superlative_fails(self):
        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {
                        "sentence_id": "S006",
                        "text": (
                            "Bu gelismeler tunel insaatinda kullanilan "
                            "en önemli yontemi ortaya cikarmistir."
                        ),
                    },
                    {"sentence_id": "S002", "text": "Diger cumle."},
                ],
            },
        )
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C001", "C002"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_narrative_synthesis_with_causal_claim_fails(self):
        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentences": [
                    {
                        "sentence_id": "S006",
                        "text": (
                            "Bu sayede tunel insaatinda yeni bir donem "
                            "baslamistir."
                        ),
                    },
                    {"sentence_id": "S002", "text": "Diger cumle."},
                ],
            },
        )
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C001", "C002"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )

    def test_narrative_synthesis_cannot_rescue_unsupported_sentence(self):
        write_json(
            self.audit_path,
            self._base_audit(
                [
                    {
                        "sentence_id": "S006",
                        "status": "UNSUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                    {
                        "sentence_id": "S002",
                        "status": "NARRATIVE_SYNTHESIS",
                        "supporting_claim_ids": ["C002"],
                    },
                ]
            ),
        )

        with self.assertRaises(AuditContractError):
            validate_evidence_audit(
                self.sentence_map_path, self.audit_path, self.packet_path
            )


class FreezeExactManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.draft_path = self.root / "draft.md"
        self.evidence_audit_path = self.root / "evidence_audit.json"
        self.editorial_audit_path = self.root / "editorial_audit.json"
        self.sentence_map_path = self.root / "sentence_map.json"
        self.compact_packet_path = self.root / "packet.json"
        self.evidence_audit_input_path = self.root / "evidence_input.txt"
        self.editorial_input_path = self.root / "editorial_input.txt"
        self.final_dir = self.root / "final"

        self.draft_path.write_text(
            "# CH-A-S04\n\nBu paragraf yeterince uzun ve düzgün "
            "bir şekilde bitiyor.\n",
            encoding="utf-8",
        )

        write_json(
            self.sentence_map_path,
            {
                "section_id": "CH-A-S04",
                "sentence_count": 1,
                "sentences": [{"sentence_id": "S001"}],
            },
        )

        write_json(
            self.compact_packet_path,
            {"admitted_claims": [{"claim_id": "C001"}]},
        )

        write_json(
            self.evidence_audit_path,
            {
                "section_id": "CH-A-S04",
                "decision": "PASS",
                "sentence_audit": [
                    {
                        "sentence_id": "S001",
                        "status": "SUPPORTED",
                        "supporting_claim_ids": ["C001"],
                    },
                ],
            },
        )

        write_json(
            self.editorial_audit_path,
            {"decision": "PASS"},
        )

        self.evidence_audit_input_path.write_text("input", encoding="utf-8")
        self.editorial_input_path.write_text("input", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _freeze(self):
        return freeze_exact(
            section_id="CH-A-S04",
            section_title="Test Section",
            version="v1",
            draft_path=self.draft_path,
            evidence_audit_path=self.evidence_audit_path,
            editorial_audit_path=self.editorial_audit_path,
            sentence_map_path=self.sentence_map_path,
            compact_packet_path=self.compact_packet_path,
            final_dir=self.final_dir,
            model_id="qwen3.6-35b-a3b-mlx",
            model_config={"api_base": "http://127.0.0.1:1234"},
            evidence_audit_input_path=self.evidence_audit_input_path,
            editorial_input_path=self.editorial_input_path,
        )

    def test_manifest_includes_identity_and_version_fields(self):
        manifest_path = self._freeze()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["model_id"], "qwen3.6-35b-a3b-mlx")
        self.assertEqual(
            manifest["model_config"],
            {"api_base": "http://127.0.0.1:1234"},
        )
        self.assertTrue(manifest["audit_identity"])
        self.assertEqual(
            manifest["evidence_contract_version"], "SENTENCE_ID_V2"
        )
        self.assertEqual(
            manifest["editorial_policy_version"],
            "DETERMINISTIC_EDITORIAL_GATE_V1",
        )
        self.assertEqual(manifest["human_review_refs"], [])
        self.assertTrue(manifest["evidence_audit_input_sha256"])
        self.assertTrue(manifest["editorial_input_sha256"])

    def test_audit_identity_changes_with_model_id(self):
        manifest_a = json.loads(self._freeze().read_text(encoding="utf-8"))

        self.final_dir = self.root / "final_b"
        self.draft_path.write_text(
            self.draft_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

        manifest_b_path = freeze_exact(
            section_id="CH-A-S04",
            section_title="Test Section",
            version="v1",
            draft_path=self.draft_path,
            evidence_audit_path=self.evidence_audit_path,
            editorial_audit_path=self.editorial_audit_path,
            sentence_map_path=self.sentence_map_path,
            compact_packet_path=self.compact_packet_path,
            final_dir=self.final_dir,
            model_id="a-different-model",
        )
        manifest_b = json.loads(manifest_b_path.read_text(encoding="utf-8"))

        self.assertNotEqual(
            manifest_a["audit_identity"], manifest_b["audit_identity"]
        )


class HumanReviewOverrideTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.manifest_path = self.root / "manifest.json"

        write_json(
            self.manifest_path,
            {
                "section_id": "CH-A-S04",
                "status": "FROZEN",
                "human_review_refs": [],
            },
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_approved_review_keeps_frozen_status(self):
        manifest = apply_human_review(
            self.manifest_path,
            reviewer="editor@example.com",
            decision="APPROVED",
            note="looks correct",
        )

        self.assertEqual(manifest["status"], "FROZEN")
        self.assertEqual(len(manifest["human_review_refs"]), 1)
        self.assertEqual(
            manifest["human_review_refs"][0]["decision"], "APPROVED"
        )

    def test_rejected_review_marks_human_rejected_without_deleting_artifacts(
        self,
    ):
        manifest = apply_human_review(
            self.manifest_path,
            reviewer="editor@example.com",
            decision="REJECTED",
            note="chronology issue",
        )

        self.assertEqual(manifest["status"], "HUMAN_REJECTED")
        self.assertEqual(
            manifest["human_review_refs"][0]["decision"], "REJECTED"
        )

    def test_invalid_decision_rejected(self):
        with self.assertRaises(AuditContractError):
            apply_human_review(
                self.manifest_path,
                reviewer="editor@example.com",
                decision="MAYBE",
            )

    def test_missing_reviewer_rejected(self):
        with self.assertRaises(AuditContractError):
            apply_human_review(
                self.manifest_path,
                reviewer="",
                decision="APPROVED",
            )


class SplitSentencesTests(unittest.TestCase):
    def test_st_abbreviation_not_split(self):
        sentences = split_sentences(
            "St. Gotthard tüneli İsviçre'de yer alır. "
            "Uzunluğu on altı kilometreyi aşar."
        )
        self.assertEqual(len(sentences), 2)
        self.assertTrue(sentences[0].startswith("St. Gotthard"))

    def test_dr_prof_doc_sn_no_bkz_not_split(self):
        text = (
            "Dr. Aksoy raporu hazırladı. Prof. Yılmaz katkı sundu. "
            "Doç. Demir inceledi. Sn. Kaya onayladı. "
            "No. 4 tünel referans alındı. Bkz. Ek A bölümü."
        )
        sentences = split_sentences(text)
        self.assertEqual(len(sentences), 6)

    def test_mo_ms_not_split(self):
        sentences = split_sentences(
            "Yapı M.Ö. 300 yılına tarihlenir. Sonraki dönem M.S. 100 "
            "civarındadır."
        )
        self.assertEqual(len(sentences), 2)

    def test_decimal_not_split(self):
        sentences = split_sentences(
            "Eğim değeri 4.5 olarak ölçüldü. İkinci ölçüm farklıdır."
        )
        self.assertEqual(len(sentences), 2)
        self.assertIn("4.5", sentences[0])

    def test_ordinal_century_not_split(self):
        sentences = split_sentences(
            "19. yüzyılda demiryolu gelişimiyle uzun mesafe tünelleri "
            "öne çıkmıştır. Bu gelişim yirminci yüzyılda sürmüştür."
        )
        self.assertEqual(len(sentences), 2)
        self.assertTrue(sentences[0].startswith("19. yüzyılda"))

    def test_normal_sentence_boundaries_still_split(self):
        sentences = split_sentences(
            "Tünel 1980 yılında açıldı. İnşaat on yıl sürdü. "
            "Bakım çalışmaları devam etmektedir."
        )
        self.assertEqual(len(sentences), 3)


if __name__ == "__main__":
    unittest.main()
