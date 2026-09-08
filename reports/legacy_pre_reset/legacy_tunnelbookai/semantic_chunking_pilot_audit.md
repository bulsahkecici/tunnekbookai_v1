# TunnelBookAI Semantic Chunking Pilot Audit

## Result

**GO FOR FULL RUN**

- Selected: **15/15**
- Passed: **15**
- Unsafe documents (P0): **0**

P0 conditions gate this stage. P1/P2 findings are reported per document and do not block.

## Documents

### DOC000001

- selection_reason: clean_pdf
- chunks: 17
- token_range: 305–1165
- median_tokens: 786
- headings_attached: 17/17
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000087

- selection_reason: large_full_docling_pdf
- chunks: 485
- token_range: 21–4750
- median_tokens: 905
- headings_attached: 485/485
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 14 chunk(s) over hard limit (14 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000198

- selection_reason: ocr_heavy
- chunks: 87
- token_range: 127–3750
- median_tokens: 822
- headings_attached: 87/87
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 1 chunk(s) over hard limit (1 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000047

- selection_reason: regulation
- chunks: 434
- token_range: 7–5688
- median_tokens: 834
- headings_attached: 434/434
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 30 chunk(s) over hard limit (30 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000003

- selection_reason: academic_article
- chunks: 227
- token_range: 7–2197
- median_tokens: 816
- headings_attached: 227/227
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 4 chunk(s) over hard limit (4 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000012

- selection_reason: handbook_manual
- chunks: 3
- token_range: 174–1198
- median_tokens: 1180
- headings_attached: 0/3
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000236

- selection_reason: table_heavy
- chunks: 488
- token_range: 12–4172
- median_tokens: 901
- headings_attached: 488/488
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 11 chunk(s) over hard limit (11 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000075

- selection_reason: list_heavy
- chunks: 200
- token_range: 182–2222
- median_tokens: 1149
- headings_attached: 0/200
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 6 chunk(s) over hard limit (6 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000023

- selection_reason: docx
- chunks: 1
- token_range: 323–323
- median_tokens: 323
- headings_attached: 0/1
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000066

- selection_reason: pptx
- chunks: 6
- token_range: 74–1200
- median_tokens: 854
- headings_attached: 6/6
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000124

- selection_reason: source_only_provenance
- chunks: 94
- token_range: 14–2833
- median_tokens: 1160
- headings_attached: 0/94
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 4 chunk(s) over hard limit (4 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000037

- selection_reason: formula_placeholder
- chunks: 133
- token_range: 179–1278
- median_tokens: 815
- headings_attached: 133/133
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000170

- selection_reason: image_heavy
- chunks: 150
- token_range: 4–4319
- median_tokens: 906
- headings_attached: 150/150
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 8 chunk(s) over hard limit (8 atomic table, 0 indivisible block)
- quality_result: PASS

### DOC000242

- selection_reason: very_short
- chunks: 1
- token_range: 30–30
- median_tokens: 30
- headings_attached: 1/1
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: none
- quality_result: PASS

### DOC000049

- selection_reason: very_long
- chunks: 150
- token_range: 17–2759
- median_tokens: 941
- headings_attached: 150/150
- tables_intact: True
- lists_intact: True
- citation_provenance_preserved: True
- dropped_substantive_text: 0
- duplicate_chunk_ids: 0
- overlap_tokens: 0
- p0_failures: none
- p1_warnings: P1 justified_special_case: 9 chunk(s) over hard limit (9 atomic table, 0 indivisible block)
- quality_result: PASS
