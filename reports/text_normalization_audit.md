# TunnelBookAI Text Normalization Audit

## Sonuç

- Karar: **GO**
- Source documents: **214/214**
- Normalized documents: **214/214**
- Unique document_id: **214**
- Changed documents: **172**
- Source corpus değişti: **false**

## Status

- unchanged: **38**
- normalized: **147**
- normalized_with_warning: **29**
- manual_review_required: **0**
- failed: **0**

## Rule counts

- rule_unicode_normalization_count: **54**
- rule_whitespace_count: **27939**
- rule_ocr_spacing_count: **45**
- rule_linebreak_count: **790**
- rule_hyphenation_count: **0**
- rule_header_footer_count: **0**
- rule_replacement_character_count: **153**
- rule_encoding_cleanup_count: **0**
- rule_placeholder_count: **14991**

## Safety

- Manual review required: **29**
- Extra/stale target file: **0**
- Front matter, provenance comments, tables, numeric tokens, protected identifiers and engineering symbols audited per document.
- Header/footer candidates were not silently deleted; uncertain repeats were flagged.
- Replacement characters were converted only to visible `[UNRESOLVED_CHAR]` markers and flagged.

## Warnings / review

- Bunlar blocker değildir; belirsiz içerik tahmin edilmedi ve kaynakta kalıcı değişiklik yapılmadı.
- `DOC000003`: repeated_header_footer_candidate_not_removed:(continued on next page)
- `DOC000013`: replacement_character_marked_unresolved
- `DOC000047`: repeated_header_footer_candidate_not_removed:This page is intentionally left blank.
- `DOC000073`: repeated_header_footer_candidate_not_removed:[**www.kgm.gov.tr**](http://www.kgm.gov.tr/)
- `DOC000128`: repeated_header_footer_candidate_not_removed:www.vizyon2023turkiye.org
- `DOC000153`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org | www.tunnelturkey.org BUILDING TRUST
- `DOC000154`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000156`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000157`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000159`: repeated_header_footer_candidate_not_removed:12/4/2022
- `DOC000160`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000161`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000163`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000165`: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org
- `DOC000176`: replacement_character_marked_unresolved
- `DOC000177`: replacement_character_marked_unresolved
- `DOC000193`: replacement_character_marked_unresolved
- `DOC000194`: replacement_character_marked_unresolved
- `DOC000195`: replacement_character_marked_unresolved
- `DOC000196`: replacement_character_marked_unresolved
- `DOC000197`: repeated_header_footer_candidate_not_removed:www.tuneldergisi.com; replacement_character_marked_unresolved
- `DOC000198`: replacement_character_marked_unresolved
- `DOC000199`: replacement_character_marked_unresolved
- `DOC000200`: replacement_character_marked_unresolved
- `DOC000201`: replacement_character_marked_unresolved
- `DOC000202`: replacement_character_marked_unresolved
- `DOC000203`: replacement_character_marked_unresolved
- `DOC000204`: replacement_character_marked_unresolved
- `DOC000207`: replacement_character_marked_unresolved

## Testler

- idempotency test

## Sınırlar

- `data/corpus_final/` immutable source olarak korundu.
- Metadata inference, Docling conversion, chunking, embedding, Qdrant ve RAG çalıştırılmadı.

## Blockers

- Yok.

## Oluşturulan/değiştirilen çıktılar

- `data/corpus_normalized/`
- `data/metadata/text_normalization_manifest.csv`
- `reports/text_normalization_audit.md`
- `scripts/10_text_normalization.py`
- `tests/test_text_normalization.py`

## Nihai karar

**GO**
