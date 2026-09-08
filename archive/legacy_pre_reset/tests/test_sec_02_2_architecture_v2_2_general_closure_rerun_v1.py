import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("general_closure_rerun", ROOT / "scripts/82_architecture_v2_2_general_closure_rerun_v1.py")
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


class GeneralClosureRerunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = runner.evaluate()

    def test_required_gates(self):
        self.assertEqual("GO", self.result["status"])
        self.assertEqual({"conditions": "25/25", "dependencies": "2/2", "unresolved_term_fallback": "PASS"}, self.result["closure_results"])
        self.assertEqual(6, self.result["six_blocker_status"]["closed"])
        self.assertEqual("ACCEPT", self.result["validation"]["status"])
        self.assertEqual({}, self.result["validation"]["failure_histogram"])
        self.assertEqual("ACCEPT", self.result["general_closure"]["status"])
        self.assertEqual({}, self.result["general_closure"]["failure_histogram"])
        self.assertEqual({"book_style": "PASS", "citation_support": "PASS", "factual_completeness": "PASS", "frozen_drift": 0}, self.result["gate_results"])

    def test_surface_closure(self):
        text = self.result["rendered_markdown"]
        body = text.split("\n## Kaynaklar\n", 1)[0]
        self.assertNotIn("katman", body.casefold())
        self.assertIn("**Swelling Rock**", text)
        for label in ("Kuru Sistem:", "Yaş Sistem:", "Çevresel Şartlar:", "Özel Uygulamalar:"):
            self.assertNotIn(label, text)

    def test_deterministic_in_process(self):
        self.assertEqual(runner.canonical_bytes(self.result), runner.canonical_bytes(runner.evaluate()))


if __name__ == "__main__":
    unittest.main()
