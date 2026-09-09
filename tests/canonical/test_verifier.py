from __future__ import annotations

import json
import unittest

from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.promotion import apply_plan, build_plan
from tunnelbookai.canonical.verifier import inspect_canonical

from .fixtures import SyntheticRepo


class VerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()
        self.context = CanonicalContext.load(self.repo.root)

    def tearDown(self) -> None:
        self.repo.close()

    def promote(self):
        plan = build_plan(context=self.context)
        return apply_plan(
            self.context.audit_root / "plans" / f"{plan.plan_id}.json",
            approve=plan.plan_id, context=self.context,
        )

    def test_empty(self):
        self.assertEqual(inspect_canonical(context=self.context).state.value, "EMPTY")

    def test_nonempty_without_manifest_invalid(self):
        (self.context.canonical_root / "unexpected").write_text("x", encoding="utf-8")
        inventory = inspect_canonical(context=self.context)
        self.assertEqual(inventory.state.value, "INVALID")
        self.assertIn("CANONICAL_NOT_EMPTY_WITHOUT_MANIFEST", inventory.reasons)

    def test_manifest_corruption_invalid(self):
        self.promote()
        self.context.manifest_path.chmod(0o644)
        self.context.manifest_path.write_text("{", encoding="utf-8")
        self.assertEqual(inspect_canonical(context=self.context).state.value, "INVALID")

    def test_canonical_file_tamper_invalid(self):
        self.promote()
        manifest = json.loads(self.context.manifest_path.read_text())
        path = self.repo.root / manifest["documents"][0]["document"]["path"]
        path.chmod(0o644)
        path.write_text("tampered", encoding="utf-8")
        self.assertEqual(inspect_canonical(context=self.context).state.value, "INVALID")

    def test_digest_tamper_invalid(self):
        self.promote()
        manifest = json.loads(self.context.manifest_path.read_text())
        manifest["canonical_corpus_digest"] = "0" * 64
        self.context.manifest_path.chmod(0o644)
        self.context.manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        inventory = inspect_canonical(context=self.context)
        self.assertEqual(inventory.state.value, "INVALID")
        self.assertIn("CANONICAL_DIGEST_MISMATCH", inventory.reasons)

    def test_unexpected_active_object_file_invalid(self):
        self.promote()
        manifest = json.loads(self.context.manifest_path.read_text())
        path = self.repo.root / manifest["documents"][0]["document"]["path"]
        unexpected = path.parent / "unexpected.txt"
        path.parent.chmod(0o755)
        unexpected.write_text("not admitted", encoding="utf-8")
        self.assertEqual(inspect_canonical(context=self.context).state.value, "INVALID")


if __name__ == "__main__":
    unittest.main()
