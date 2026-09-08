from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from _loader import load_script
from utils import find_libreoffice, is_excluded, load_config, sha256_file


inventory = load_script("01_inventory.py", "inventory_script")


class InventoryTests(unittest.TestCase):
    def test_sha256_is_real_content_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Türkçe belge.txt"
            content = "İstanbul tüneli".encode("utf-8")
            path.write_bytes(content)
            self.assertEqual(sha256_file(path), hashlib.sha256(content).hexdigest())

    def test_project_directory_is_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertTrue(is_excluded(root / "_TunnelBookAI" / "data" / "x.pdf", root, ["_TunnelBookAI"]))
            self.assertFalse(is_excluded(root / "Kaynak" / "x.pdf", root, ["_TunnelBookAI"]))

    def test_tunnel_root_environment_override(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = os.environ.get("TUNNEL_ROOT")
            os.environ["TUNNEL_ROOT"] = directory
            try:
                self.assertEqual(load_config()["source_root"], Path(directory))
            finally:
                if previous is None:
                    os.environ.pop("TUNNEL_ROOT", None)
                else:
                    os.environ["TUNNEL_ROOT"] = previous

    @unittest.skipIf(os.name == "nt", "non-Windows portability check")
    def test_windows_portable_libreoffice_is_not_selected_on_macos(self):
        executable = find_libreoffice()
        self.assertFalse(executable and executable.suffix.casefold() in {".com", ".exe"})

    def test_relative_path_and_turkish_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "Tünel Belgeleri"
            source.mkdir()
            (source / "Şartname.pdf").write_bytes(b"pdf")
            project = root / "_TunnelBookAI"
            (project / "ignored.txt").parent.mkdir(parents=True)
            (project / "ignored.txt").write_text("ignored")
            config = {
                "source_root": root, "project_root": project,
                "exclude_directories": ["_TunnelBookAI"],
                "extensions": {"documents": [".pdf"]},
            }
            rows = inventory.collect_inventory(config)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["relative_path"], "Tünel Belgeleri/Şartname.pdf")


if __name__ == "__main__":
    unittest.main()
