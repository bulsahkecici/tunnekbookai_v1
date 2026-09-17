from __future__ import annotations

import unittest

from tunnelbookai.book.evidence_review import _audit_with_split, _validate_results


class PostwritingEvidenceReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sentences = [{
            "sentence_id": "1.1-S001",
            "paragraph_id": "1.1-P001",
            "text": "Tünel yeraltında oluşturulan bir mühendislik yapısıdır.",
            "claim_ids": ["CLM_1"],
            "question_ids": ["1.1-Q01"],
        }]
        self.claims = [{
            "claim_id": "CLM_1",
            "document_id": "ING_1",
            "locator": "ING_1:CH_1:pages=1",
        }]

    def test_supported_result_projects_only_mapped_provenance(self):
        rows = _validate_results({"results": [{
            "i": 1, "s": "S", "e": [1], "r": "D", "c": 91,
        }]}, self.sentences, self.claims)
        self.assertEqual(rows[0]["status"], "SUPPORTED")
        self.assertEqual(rows[0]["supporting_claim_ids"], ["CLM_1"])
        self.assertEqual(rows[0]["confidence"], 0.91)

    def test_supported_without_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "without evidence"):
            _validate_results({"results": [{
                "i": 1, "s": "S", "e": [], "r": "D", "c": 80,
            }]}, self.sentences, self.claims)

    def test_unmapped_evidence_is_rejected(self):
        claims = [*self.claims, {"claim_id": "CLM_2", "document_id": "ING_2", "locator": "x"}]
        with self.assertRaisesRegex(ValueError, "not mapped"):
            _validate_results({"results": [{
                "i": 1, "s": "S", "e": [2], "r": "D", "c": 80,
            }]}, self.sentences, claims)

    def test_cross_sentence_claim_error_splits_until_references_are_local(self):
        sentences = [
            self.sentences[0],
            {
                **self.sentences[0],
                "sentence_id": "1.1-S002",
                "text": "İkinci ve yeterince uzun teknik cümledir.",
                "claim_ids": ["CLM_2"],
            },
        ]
        claims = {
            "CLM_1": {**self.claims[0], "claim_text": "Passage one."},
            "CLM_2": {"claim_id": "CLM_2", "document_id": "ING_2", "locator": "x", "claim_text": "Passage two."},
        }

        class Client:
            calls = 0

            def chat_json(self, *args, **kwargs):
                self.calls += 1
                count = kwargs["response_schema"]["properties"]["results"]["minItems"]
                if count == 2:
                    return {"results": [
                        {"i": 1, "s": "S", "e": [2], "r": "D", "c": 80},
                        {"i": 2, "s": "S", "e": [2], "r": "D", "c": 80},
                    ]}
                return {"results": [{"i": 1, "s": "S", "e": [1], "r": "D", "c": 80}]}

        client = Client()
        rows = _audit_with_split(client, "qwen", sentences, claims)
        self.assertEqual(client.calls, 3)
        self.assertEqual([row["sentence_id"] for row in rows], ["1.1-S001", "1.1-S002"])


if __name__ == "__main__":
    unittest.main()
