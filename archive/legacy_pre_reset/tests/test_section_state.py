import tempfile
import unittest
from pathlib import Path

from scripts.section_state import (
    SectionStateError,
    checkpoint_revision,
    list_revisions,
    restore_revision,
)


class SectionStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.remediation_dir = Path(self.tmp.name)

        self.draft = self.remediation_dir / "draft.md"
        self.sentence_map = self.remediation_dir / "sentence_map.json"
        self.evidence_audit = self.remediation_dir / "evidence_audit.json"
        self.editorial_audit = self.remediation_dir / "editorial_audit.json"

        self.draft.write_text("R0 draft", encoding="utf-8")
        self.sentence_map.write_text("{}", encoding="utf-8")
        self.evidence_audit.write_text('{"decision": "PASS"}', encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_checkpoint_creates_revision_dir(self):
        checkpoint_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_path=self.evidence_audit,
            editorial_audit_path=None,
            status="EVIDENCE_VALID_PRE_REVISION",
        )

        self.assertEqual(list_revisions(self.remediation_dir), [0])

    def test_checkpoint_is_write_once(self):
        checkpoint_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_path=self.evidence_audit,
            editorial_audit_path=None,
            status="EVIDENCE_VALID_PRE_REVISION",
        )

        with self.assertRaises(SectionStateError):
            checkpoint_revision(
                remediation_dir=self.remediation_dir,
                revision=0,
                draft_path=self.draft,
                sentence_map_path=self.sentence_map,
                evidence_audit_path=self.evidence_audit,
                editorial_audit_path=None,
                status="EVIDENCE_VALID_PRE_REVISION",
            )

    def test_restore_brings_back_r0_after_r1_overwrite(self):
        checkpoint_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_path=self.evidence_audit,
            editorial_audit_path=None,
            status="EVIDENCE_VALID_PRE_REVISION",
        )

        # Simulate an R1 attempt that fails evidence and mutates
        # the working files in place.
        self.draft.write_text("R1 failed draft", encoding="utf-8")
        self.evidence_audit.write_text('{"decision": "HOLD"}', encoding="utf-8")

        result = restore_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_path=self.evidence_audit,
            editorial_audit_path=self.editorial_audit,
        )

        self.assertEqual(self.draft.read_text(encoding="utf-8"), "R0 draft")
        self.assertIn("draft.md", result["restored"])

    def test_checkpoint_and_restore_include_input_and_state_artifacts(self):
        evidence_input = self.remediation_dir / "evidence_audit_input.txt"
        editorial_input = self.remediation_dir / "editorial_input.txt"
        evidence_input.write_text("evidence prompt input", encoding="utf-8")
        editorial_input.write_text("editorial prompt input", encoding="utf-8")

        checkpoint_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_input_path=evidence_input,
            evidence_audit_path=self.evidence_audit,
            editorial_input_path=editorial_input,
            editorial_audit_path=None,
            status="EVIDENCE_VALID_PRE_REVISION",
            state={"section_id": "CH-Z-S99", "cycle": 0},
        )

        r0_dir = self.remediation_dir / "revisions" / "r0"
        self.assertTrue((r0_dir / "evidence_audit_input.txt").exists())
        self.assertTrue((r0_dir / "editorial_input.txt").exists())
        self.assertTrue((r0_dir / "state.json").exists())

        evidence_input.write_text("mutated after checkpoint", encoding="utf-8")
        editorial_input.write_text("mutated after checkpoint", encoding="utf-8")

        result = restore_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_input_path=evidence_input,
            evidence_audit_path=self.evidence_audit,
            editorial_input_path=editorial_input,
            editorial_audit_path=self.editorial_audit,
        )

        self.assertEqual(evidence_input.read_text(encoding="utf-8"), "evidence prompt input")
        self.assertEqual(editorial_input.read_text(encoding="utf-8"), "editorial prompt input")
        self.assertIn("evidence_audit_input.txt", result["restored"])
        self.assertIn("editorial_input.txt", result["restored"])

    def test_restore_missing_revision_fails(self):
        with self.assertRaises(SectionStateError):
            restore_revision(
                remediation_dir=self.remediation_dir,
                revision=5,
                draft_path=self.draft,
                sentence_map_path=self.sentence_map,
                evidence_audit_path=self.evidence_audit,
                editorial_audit_path=None,
            )

    def test_restore_detects_tampered_checkpoint(self):
        checkpoint_revision(
            remediation_dir=self.remediation_dir,
            revision=0,
            draft_path=self.draft,
            sentence_map_path=self.sentence_map,
            evidence_audit_path=self.evidence_audit,
            editorial_audit_path=None,
            status="EVIDENCE_VALID_PRE_REVISION",
        )

        tampered = self.remediation_dir / "revisions" / "r0" / "draft.md"
        tampered.write_text("tampered content", encoding="utf-8")

        with self.assertRaises(SectionStateError):
            restore_revision(
                remediation_dir=self.remediation_dir,
                revision=0,
                draft_path=self.draft,
                sentence_map_path=self.sentence_map,
                evidence_audit_path=self.evidence_audit,
                editorial_audit_path=None,
            )


if __name__ == "__main__":
    unittest.main()
