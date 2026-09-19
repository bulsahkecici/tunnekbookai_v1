from __future__ import annotations

import json
import unittest
from unittest import mock

from tunnelbookai.canonical.errors import CanonicalError
from tunnelbookai.canonical.paths import CanonicalContext
from tunnelbookai.canonical.promotion import apply_plan, build_plan
from tunnelbookai.canonical.verifier import inspect_canonical

from .fixtures import SyntheticRepo


class PromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()
        self.context = CanonicalContext.load(self.repo.root)

    def tearDown(self) -> None:
        self.repo.close()

    def test_plan_is_deterministic_and_does_not_mutate_canonical(self):
        first = build_plan(context=self.context)
        second = build_plan(context=self.context)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertTrue(first.applicable)
        self.assertEqual(first.candidates[0].action.value, "PROMOTE")
        self.assertEqual(list(self.context.canonical_root.glob("objects/**/*")), [])

    def test_valid_apply_and_verify(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        result = apply_plan(path, approve=plan.plan_id, context=self.context)
        self.assertEqual(result["status"], "APPLIED")
        inventory = inspect_canonical(context=self.context)
        self.assertTrue(inventory.ready)
        self.assertEqual((inventory.document_count, inventory.chunk_count), (1, 1))

    def test_missing_and_mismatched_approval_do_not_mutate_canonical(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        for approval, code in ((None, "PROMOTION_APPROVAL_REQUIRED"), ("CCP_wrong", "PROMOTION_APPROVAL_MISMATCH")):
            with self.subTest(code=code), self.assertRaises(CanonicalError) as raised:
                apply_plan(path, approve=approval, context=self.context)
            self.assertEqual(raised.exception.code, code)
        self.assertEqual(inspect_canonical(context=self.context).state.value, "EMPTY")

    def test_stale_plan_fails_closed(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        staged = self.repo.root / f"corpus/staging/v2/{self.repo.document_id}/document.md"
        staged.write_text(staged.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
        with self.assertRaises(CanonicalError) as raised:
            apply_plan(path, approve=plan.plan_id, context=self.context)
        self.assertEqual(raised.exception.code, "STALE_CANONICAL_PROMOTION_PLAN")
        self.assertEqual(inspect_canonical(context=self.context).state.value, "EMPTY")

    def test_fresh_plan_after_apply_is_idempotent(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        apply_plan(path, approve=plan.plan_id, context=self.context)
        before = self.context.manifest_path.read_bytes()
        fresh = build_plan(context=self.context)
        self.assertEqual(fresh.candidates[0].action.value, "IDEMPOTENT_NO_CHANGE")
        fresh_path = self.context.audit_root / "plans" / f"{fresh.plan_id}.json"
        result = apply_plan(fresh_path, approve=fresh.plan_id, context=self.context)
        self.assertEqual(result["status"], "IDEMPOTENT_NO_CHANGE")
        self.assertEqual(before, self.context.manifest_path.read_bytes())

    def test_old_plan_is_stale_after_success(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        apply_plan(path, approve=plan.plan_id, context=self.context)
        with self.assertRaises(CanonicalError) as raised:
            apply_plan(path, approve=plan.plan_id, context=self.context)
        self.assertEqual(raised.exception.code, "STALE_CANONICAL_PROMOTION_PLAN")

    def test_changed_semantic_record_conflicts_after_promotion(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        apply_plan(path, approve=plan.plan_id, context=self.context)
        for relative in ("processing", "corpus/staging/v2"):
            metadata = self.repo.root / relative / self.repo.document_id / "metadata.json"
            value = json.loads(metadata.read_text())
            value["title"] = "Changed title"
            metadata.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        fresh = build_plan(context=self.context)
        # Same source bytes, re-derived record: replaceable only through an explicit,
        # approved apply; never silently.
        self.assertEqual(fresh.candidates[0].action.value, "REPLACE")
        before_digest = plan.expected_after["canonical_corpus_digest"]
        self.assertNotEqual(fresh.expected_after["canonical_corpus_digest"], before_digest)
        result = apply_plan(self.context.audit_root / "plans" / f"{fresh.plan_id}.json", approve=fresh.plan_id, context=self.context)
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(result["canonical"]["document_count"], 1)
        audit = json.loads((self.repo.root / result["audit_path"]).read_text(encoding="utf-8"))
        self.assertEqual(audit["replaced_candidates"], [self.repo.document_id])
        inventory = inspect_canonical(context=self.context)
        self.assertTrue(inventory.ready)
        self.assertTrue(any(w.startswith("UNREFERENCED_CANONICAL_OBJECT") for w in inventory.warnings))
        # A re-plan is now idempotent.
        self.assertEqual(build_plan(context=self.context).candidates[0].action.value, "IDEMPOTENT_NO_CHANGE")

    def test_atomic_manifest_failure_restores_empty_state(self):
        plan = build_plan(context=self.context)
        path = self.context.audit_root / "plans" / f"{plan.plan_id}.json"
        from tunnelbookai.canonical import promotion
        original = promotion._atomic_json
        def fail_manifest(target, value):
            if target == self.context.manifest_path:
                raise OSError("injected manifest failure")
            return original(target, value)
        with mock.patch("tunnelbookai.canonical.promotion._atomic_json", side_effect=fail_manifest):
            with self.assertRaises(CanonicalError) as raised:
                apply_plan(path, approve=plan.plan_id, context=self.context)
        self.assertEqual(raised.exception.code, "ATOMIC_PROMOTION_FAILED")
        self.assertEqual(inspect_canonical(context=self.context).state.value, "EMPTY")
        objects = self.context.canonical_root / "objects"
        self.assertFalse(objects.exists() and any(path.is_file() for path in objects.rglob("*")))


if __name__ == "__main__":
    unittest.main()
