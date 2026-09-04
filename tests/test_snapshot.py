from __future__ import annotations

import os
import unittest

from _loader import load_script


snapshot = load_script("07_snapshot.py", "snapshot_script")


class SnapshotTests(unittest.TestCase):
    @unittest.skipIf(os.name == "nt", "non-Windows portability check")
    def test_office_process_check_is_safe_off_windows(self):
        self.assertEqual(snapshot.active_office_processes(), [])

    def test_archive_digest_is_order_independent(self):
        rows = [
            {"relative_path": "B.pdf", "sha256": "b" * 64},
            {"relative_path": "A.pdf", "sha256": "a" * 64},
        ]
        self.assertEqual(snapshot.archive_digest(rows), snapshot.archive_digest(list(reversed(rows))))

    def test_archive_digest_changes_with_content_hash(self):
        first = [{"relative_path": "A.pdf", "sha256": "a" * 64}]
        second = [{"relative_path": "A.pdf", "sha256": "b" * 64}]
        self.assertNotEqual(snapshot.archive_digest(first), snapshot.archive_digest(second))


if __name__ == "__main__":
    unittest.main()
