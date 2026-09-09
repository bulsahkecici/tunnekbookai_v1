from __future__ import annotations

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock
from pathlib import Path

from tunnelbookai.canonical import cli
from tunnelbookai.canonical.paths import CanonicalContext

from .fixtures import SyntheticRepo
from tunnelbookai.population.models import atomic_json, identity


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SyntheticRepo()
        self.context = CanonicalContext.load(self.repo.root)

    def tearDown(self) -> None:
        self.repo.close()

    def test_status_and_plan_exit_zero(self):
        with mock.patch("tunnelbookai.canonical.cli.CanonicalContext.load", return_value=self.context):
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["status", "--json"]), 0)
                self.assertEqual(cli.main(["plan", "--document-id", self.repo.document_id, "--json"]), 0)

    def test_missing_candidate_plan_is_blocked(self):
        missing = "ING_" + "0" * 20
        with mock.patch("tunnelbookai.canonical.cli.CanonicalContext.load", return_value=self.context):
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["plan", "--document-id", missing, "--json"]), 2)

    def test_population_selector_file_is_validated(self):
        semantic = {
            "schema_version": "1.0",
            "contract_version": "corpus-population-v1",
            "staging_audit_id": "CSA_" + "1" * 64,
            "ordinal": 1,
            "document_ids": [self.repo.document_id],
        }
        selector = {
            "selector_id": identity("CPP_", semantic), **semantic,
            "materialized_bytes": 1, "generated_at": "2026-09-09T00:00:00+00:00",
        }
        path = self.repo.root / "audit/corpus_population/promotion_batches" / f"{selector['selector_id']}.json"
        atomic_json(path, selector)
        with mock.patch("tunnelbookai.canonical.cli.CanonicalContext.load", return_value=self.context):
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["plan", "--document-id-file", str(path), "--json"]), 0)

    def test_tampered_population_selector_is_blocked(self):
        path = self.repo.root / "audit/corpus_population/promotion_batches/CPP_bad.json"
        atomic_json(path, {
            "selector_id": "CPP_" + "0" * 64,
            "schema_version": "1.0",
            "contract_version": "corpus-population-v1",
            "staging_audit_id": "CSA_" + "1" * 64,
            "ordinal": 1,
            "document_ids": [self.repo.document_id],
        })
        with mock.patch("tunnelbookai.canonical.cli.CanonicalContext.load", return_value=self.context):
            with redirect_stdout(StringIO()):
                self.assertEqual(cli.main(["plan", "--document-id-file", str(path), "--json"]), 2)


if __name__ == "__main__":
    unittest.main()
