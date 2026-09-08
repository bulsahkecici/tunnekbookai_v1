import json
import tempfile
import unittest
from pathlib import Path

from scripts.editorial_hard_gate import (
    EditorialHardGateError,
    deterministic_editorial_gate,
)


class DeterministicEditorialGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.draft_path = self.root / "draft.md"
        self.audit_path = self.root / "editorial_audit.json"

    def tearDown(self):
        self.tmp.cleanup()

    def _write_audit(self, **fields):
        base = {"decision": "HOLD"}
        base.update(fields)
        self.audit_path.write_text(
            json.dumps(base, ensure_ascii=False), encoding="utf-8"
        )

    def test_clean_draft_passes_despite_model_hold_and_advisory_issues(self):
        self.draft_path.write_text(
            "# CH-A-S04\n\nBu paragraf yeterince uzun ve düzgün "
            "bir şekilde bitiyor.\n",
            encoding="utf-8",
        )
        self._write_audit(
            decision="HOLD",
            chronology_issues=["olaylar kronolojik değil"],
            structure_issues=["katalog gibi"],
            required_actions=["yeniden düzenle"],
        )

        result = deterministic_editorial_gate(self.draft_path, self.audit_path)

        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["hard_blockers"], [])
        self.assertEqual(
            result["model_editorial_review"]["model_decision"], "HOLD"
        )

    def test_empty_draft_fails(self):
        self.draft_path.write_text("# CH-A-S04\n\n", encoding="utf-8")
        self._write_audit(decision="PASS")

        with self.assertRaises(EditorialHardGateError):
            deterministic_editorial_gate(self.draft_path, self.audit_path)

    def test_unicode_replacement_character_fails(self):
        self.draft_path.write_text(
            "# CH-A-S04\n\nBozuk kar�akter iceren metin burada.\n",
            encoding="utf-8",
        )
        self._write_audit(decision="PASS")

        with self.assertRaises(EditorialHardGateError):
            deterministic_editorial_gate(self.draft_path, self.audit_path)

    def test_known_typo_pattern_fails(self):
        self.draft_path.write_text(
            "# CH-A-S04\n\nOn dokuzuncu yüzyıyıda inşa edilmiştir.\n",
            encoding="utf-8",
        )
        self._write_audit(decision="PASS")

        with self.assertRaises(EditorialHardGateError):
            deterministic_editorial_gate(self.draft_path, self.audit_path)

    def test_exact_duplicate_paragraph_fails(self):
        paragraph = (
            "Bu uzunca bir paragraf metnidir ve seksen karakterden "
            "fazla olacak sekilde tekrarlanacaktir boylece test gecerli olur."
        )
        self.draft_path.write_text(
            f"# CH-A-S04\n\n{paragraph}\n\n{paragraph}\n",
            encoding="utf-8",
        )
        self._write_audit(decision="PASS")

        with self.assertRaises(EditorialHardGateError):
            deterministic_editorial_gate(self.draft_path, self.audit_path)


if __name__ == "__main__":
    unittest.main()
