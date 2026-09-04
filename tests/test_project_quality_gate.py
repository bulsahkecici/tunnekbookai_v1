from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

import project_quality_gate


class ProjectQualityGateTests(unittest.TestCase):
    def test_real_project_gate_has_no_blocking_issue(self):
        result = project_quality_gate.evaluate()
        self.assertNotEqual(result["decision"], "NO_GO", result["blocking_issues"])
        self.assertFalse(result["blocking_issues"])

    def test_manifest_paths_are_staging_and_exist(self):
        rows, ok = project_quality_gate.jsonl(ROOT / "handoff" / "manifests" / "handoff_manifest.jsonl")
        self.assertTrue(ok)
        self.assertTrue(rows)
        self.assertTrue(all(str(row["local_path"]).startswith("corpus/staging/") for row in rows))
        self.assertTrue(all((ROOT / row["local_path"]).is_file() for row in rows))


if __name__ == "__main__":
    unittest.main()
