import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_cache import AuditCache, AuditCacheError, compute_key


class AuditCacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        self.draft = self.root / "draft.md"
        self.packet = self.root / "packet.json"
        self.prompt = self.root / "prompt.txt"

        self.draft.write_text("draft text", encoding="utf-8")
        self.packet.write_text("{}", encoding="utf-8")
        self.prompt.write_text("prompt text", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_same_inputs_reuse_key(self):
        key_a = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
        )
        key_b = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
        )
        self.assertEqual(key_a, key_b)

    def test_changed_draft_changes_key(self):
        key_a = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
        )
        self.draft.write_text("different draft", encoding="utf-8")
        key_b = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
        )
        self.assertNotEqual(key_a, key_b)

    def test_changed_model_config_changes_key(self):
        key_a = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
            model_config={"api_base": "http://127.0.0.1:1234"},
        )
        key_b = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
            model_config={"api_base": "http://127.0.0.1:9999"},
        )
        self.assertNotEqual(key_a, key_b)

    def test_missing_model_config_matches_empty_dict(self):
        key_a = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
        )
        key_b = compute_key(
            draft_path=self.draft,
            packet_path=self.packet,
            prompt_path=self.prompt,
            model="m1",
            contract_version="v2",
            model_config={},
        )
        self.assertEqual(key_a, key_b)

    def test_get_put_roundtrip(self):
        cache = AuditCache(self.root / "cache")
        key = "abc123"

        self.assertIsNone(cache.get(key))

        cache.put(
            key,
            section_id="CH-A-S04",
            kind="evidence_audit",
            audit_json={"decision": "PASS"},
            gate_result={"decision": "PASS"},
        )

        entry = cache.get(key)
        self.assertEqual(entry["audit"], {"decision": "PASS"})

    def test_collision_on_different_audit_rejected(self):
        cache = AuditCache(self.root / "cache")
        key = "dupkey"

        cache.put(
            key,
            section_id="CH-A-S04",
            kind="evidence_audit",
            audit_json={"decision": "PASS", "n": 1},
            gate_result={},
        )

        with self.assertRaises(AuditCacheError):
            cache.put(
                key,
                section_id="CH-A-S04",
                kind="evidence_audit",
                audit_json={"decision": "PASS", "n": 2},
                gate_result={},
            )

    def test_identical_put_is_idempotent(self):
        cache = AuditCache(self.root / "cache")
        key = "samekey"
        audit = {"decision": "PASS", "n": 1}

        cache.put(
            key,
            section_id="CH-A-S04",
            kind="evidence_audit",
            audit_json=audit,
            gate_result={},
        )
        cache.put(
            key,
            section_id="CH-A-S04",
            kind="evidence_audit",
            audit_json=audit,
            gate_result={},
        )

        self.assertEqual(cache.get(key)["audit"], audit)

    def test_corrupt_cache_entry_raises(self):
        cache_dir = self.root / "cache"
        cache_dir.mkdir()
        (cache_dir / "badkey.json").write_text("{not json", encoding="utf-8")

        cache = AuditCache(cache_dir)

        with self.assertRaises(AuditCacheError):
            cache.get("badkey")


if __name__ == "__main__":
    unittest.main()
