from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "crawler" / "src"))

import project_paths


VENV_DIR_NAMES = {".venv", "venv"}
ALLOWED_VENV_RELATIVE_PATH = ".venv"
NEVER_DESCEND = {".git", "__pycache__", "node_modules"} | VENV_DIR_NAMES


def discover_virtual_environments(root: Path) -> list[str]:
    """Every directory that looks like a virtual environment, as a root-relative posix path.

    Never descends into a virtual environment (or .git/node_modules): the thousands of files
    inside the active .venv are irrelevant to migration integrity and walking them is slow.
    """
    found: list[str] = []

    def walk(directory: Path) -> None:
        try:
            entries = sorted(directory.iterdir())
        except (PermissionError, OSError):
            return
        for entry in entries:
            if entry.is_symlink() or not entry.is_dir():
                continue
            if entry.name in VENV_DIR_NAMES:
                found.append(entry.relative_to(root).as_posix())
                continue
            if entry.name in NEVER_DESCEND:
                continue
            walk(entry)

    walk(root)
    return sorted(found)


def gitignore_covers(root: Path, relative_directory: str) -> bool:
    """Is `relative_directory` excluded from version control?

    Uses git itself when a real repository is present; otherwise falls back to reading the
    `.gitignore` patterns directly, because this project is currently unversioned.
    """
    if (root / ".git").exists():
        probe = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", relative_directory],
            capture_output=True, check=False,
        )
        if probe.returncode in {0, 1}:
            return probe.returncode == 0
    ignore_file = root / ".gitignore"
    if not ignore_file.is_file():
        return False
    patterns = {
        line.strip().rstrip("/")
        for line in ignore_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    name = relative_directory.rstrip("/")
    return name in patterns or name.split("/")[-1] in patterns


def virtual_environment_violations(
    root: Path,
    *,
    discovered: list[str],
    tracked_paths: set[str],
) -> list[str]:
    """The migration-integrity rule for virtual environments.

    Tracked or migrated virtual environments stay forbidden. A root-level active `.venv` is
    allowed ONLY when it sits exactly at `<project_root>/.venv`, is covered by `.gitignore`,
    and appears in no manifest, hash list or corpus inventory. `tracked_paths` carries those
    migrated/verified/canonical entries.
    """
    violations: list[str] = []
    for relative in discovered:
        if relative != ALLOWED_VENV_RELATIVE_PATH:
            violations.append(f"non_root_or_nested_virtualenv:{relative}")
            continue
        if not gitignore_covers(root, relative):
            violations.append(f"root_virtualenv_not_gitignored:{relative}")
    prefix = ALLOWED_VENV_RELATIVE_PATH + "/"
    for path in sorted(tracked_paths):
        normalized = path.replace(chr(92), "/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized.lstrip("/")
        parts = normalized.split("/")
        if any(part in VENV_DIR_NAMES for part in parts):
            violations.append(f"virtualenv_artifact_is_tracked_or_migrated:{normalized}")
        elif normalized == ALLOWED_VENV_RELATIVE_PATH or normalized.startswith(prefix):
            violations.append(f"virtualenv_artifact_is_tracked_or_migrated:{normalized}")
    return violations


def manifest_tracked_paths(manifest: dict) -> set[str]:
    """Every repo-relative path the migration manifest, hash list or inventory records."""
    tracked: set[str] = set()
    for entry in manifest.get("verified_file_inventory", []) or []:
        value = entry.get("target_relative_path") or entry.get("relative_path") or entry.get("path") if isinstance(entry, dict) else entry
        if isinstance(value, str):
            tracked.add(value)
    for key in ("critical_hashes",):
        section = manifest.get(key) or {}
        if isinstance(section, dict):
            tracked.update(name for name in section if isinstance(name, str))
    for key in ("missing", "mismatches", "conflicts", "intentional_target_changes"):
        for entry in manifest.get(key, []) or []:
            if isinstance(entry, str):
                tracked.add(entry)
            elif isinstance(entry, dict):
                for field in ("target_relative_path", "relative_path", "path", "target"):
                    if isinstance(entry.get(field), str):
                        tracked.add(entry[field])
    return tracked


class MigrationIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "audit" / "migration_manifest.json").read_text(encoding="utf-8"))

    def test_target_project_valid(self):
        self.assertEqual(project_paths.PROJECT_ROOT, ROOT)

    def test_crawler_and_tests_migrated(self):
        self.assertTrue((ROOT / "crawler/src/tunnel_harvest.py").is_file())
        self.assertTrue(list((ROOT / "crawler/tests").glob("test_*.py")))

    def test_corpus_and_metadata_migrated(self):
        self.assertTrue(list((ROOT / "corpus/canonical").rglob("*.md")))
        self.assertTrue((ROOT / "corpus/metadata/final_metadata_master.csv").is_file())

    def test_critical_hashes_valid(self):
        self.assertEqual(self.manifest["hash_mismatches"], 0)
        self.assertEqual(self.manifest["missing_files"], 0)

    def test_no_nested_git_repository(self):
        nested = [path for path in ROOT.rglob(".git") if path != ROOT / ".git"]
        self.assertFalse(nested)

    def test_no_tracked_or_nested_virtual_environment(self):
        """The active root `.venv` is permitted; migrated/tracked virtualenvs are not.

        The original rule rejected every `.venv` outright, which predates this project
        standardising on a root-level Python 3.12 virtual environment. The intention it was
        protecting -- no virtual environment may enter the migrated/canonical data set --
        is preserved verbatim below.
        """
        discovered = discover_virtual_environments(ROOT)
        violations = virtual_environment_violations(
            ROOT, discovered=discovered, tracked_paths=manifest_tracked_paths(self.manifest))
        self.assertEqual(violations, [], f"virtual environment integrity violations: {violations}")

    def test_root_virtualenv_is_the_only_one_and_is_ignored(self):
        self.assertEqual(discover_virtual_environments(ROOT), [ALLOWED_VENV_RELATIVE_PATH])
        self.assertTrue(gitignore_covers(ROOT, ALLOWED_VENV_RELATIVE_PATH))

    def test_root_virtualenv_is_absent_from_corpus_and_manifests(self):
        tracked = manifest_tracked_paths(self.manifest)
        self.assertTrue(tracked, "migration manifest recorded no paths to check against")
        self.assertFalse([path for path in tracked if ".venv" in path or "/venv/" in path])
        self.assertFalse(list((ROOT / "corpus").rglob(".venv")))
        self.assertFalse(list((ROOT / "data/corpus_final").rglob(".venv")))


    def test_paths_are_project_relative_by_default(self):
        previous = os.environ.pop("TUNNEL_PAPERS_DIR", None)
        try:
            self.assertEqual(project_paths.crawler_output_root(), ROOT / "data/downloads")
        finally:
            if previous is not None:
                os.environ["TUNNEL_PAPERS_DIR"] = previous

    def test_legacy_output_path_resolves_to_target(self):
        old = next(key for key, value in project_paths.LEGACY_PATH_PREFIXES.items() if value == ROOT / "data/downloads") + "/catalog.json"
        self.assertEqual(project_paths.resolve_local_path(old), ROOT / "data/downloads/catalog.json")

    def test_book_package_preserved(self):
        self.assertTrue(self.manifest["integrity_gate"]["existing_book_package_preserved"])


class VirtualEnvironmentRuleTests(unittest.TestCase):
    """The four scenarios the narrowed rule must keep separating."""

    def scenario(self, build) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            tracked = build(root)
            return virtual_environment_violations(
                root, discovered=discover_virtual_environments(root), tracked_paths=tracked)

    def test_root_venv_that_is_gitignored_passes(self):
        def build(root: Path) -> set[str]:
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".gitignore").write_text(".venv/\n__pycache__/\n", encoding="utf-8")
            return {"scripts/utils.py", "corpus/canonical/DOC000001.md"}
        self.assertEqual(self.scenario(build), [])

    def test_root_venv_that_is_not_gitignored_fails(self):
        def build(root: Path) -> set[str]:
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
            return set()
        violations = self.scenario(build)
        self.assertEqual(violations, ["root_virtualenv_not_gitignored:.venv"])

    def test_nested_venv_inside_migrated_source_fails(self):
        def build(root: Path) -> set[str]:
            (root / "crawler" / "src" / ".venv").mkdir(parents=True)
            (root / ".gitignore").write_text(".venv/\nvenv/\n", encoding="utf-8")
            return set()
        self.assertEqual(self.scenario(build), ["non_root_or_nested_virtualenv:crawler/src/.venv"])

    def test_tracked_virtualenv_artifact_fails(self):
        def build(root: Path) -> set[str]:
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            return {"scripts/utils.py", ".venv/lib/python3.12/site-packages/x.py"}
        self.assertEqual(
            self.scenario(build),
            ["virtualenv_artifact_is_tracked_or_migrated:.venv/lib/python3.12/site-packages/x.py"])

    def test_legacy_named_venv_directory_still_fails(self):
        def build(root: Path) -> set[str]:
            (root / "venv").mkdir(parents=True)
            (root / ".gitignore").write_text(".venv/\nvenv/\n", encoding="utf-8")
            return set()
        self.assertEqual(self.scenario(build), ["non_root_or_nested_virtualenv:venv"])


if __name__ == "__main__":
    unittest.main()
