# TunnelBookAI Text Normalization Pilot Audit

## Result

**GO FOR FULL RUN**

- Selected: **15/15**
- Passed: **15**
- Unsafe changes: **0**
- Manual review: **4**

## Documents

### DOC000001

- selection_reason: clean_text
- changed: false
- rules_applied: none
- change_count: 0
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000198

- selection_reason: ocr_heavy_pdf
- changed: true
- rules_applied: whitespace, replacement_character
- change_count: 626
- warnings: replacement_character_marked_unresolved
- manual_review_required: true
- quality_result: PASS

### DOC000002

- selection_reason: broken_encoding (no exact candidate; deterministic proxy)
- changed: true
- rules_applied: whitespace
- change_count: 322
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000125

- selection_reason: turkish_split_ocr
- changed: true
- rules_applied: whitespace, ocr_spacing
- change_count: 72
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000047

- selection_reason: english_technical
- changed: true
- rules_applied: whitespace
- change_count: 2260
- warnings: repeated_header_footer_candidate_not_removed:This page is intentionally left blank.
- manual_review_required: true
- quality_result: PASS

### DOC000049

- selection_reason: table_heavy
- changed: true
- rules_applied: whitespace
- change_count: 48
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000037

- selection_reason: formula_not_decoded
- changed: true
- rules_applied: whitespace
- change_count: 29
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000087

- selection_reason: image_placeholders
- changed: true
- rules_applied: whitespace, ocr_spacing
- change_count: 3019
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000153

- selection_reason: repeated_header_footer
- changed: false
- rules_applied: none
- change_count: 0
- warnings: repeated_header_footer_candidate_not_removed:www.tunnelturkey.org | www.tunnelturkey.org BUILDING TRUST
- manual_review_required: true
- quality_result: PASS

### DOC000063

- selection_reason: line_wrap_hyphenation
- changed: true
- rules_applied: whitespace, linebreak
- change_count: 1156
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000012

- selection_reason: docx_derived
- changed: false
- rules_applied: none
- change_count: 0
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000066

- selection_reason: pptx_derived
- changed: true
- rules_applied: whitespace
- change_count: 60
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000003

- selection_reason: full_docling_pdf
- changed: true
- rules_applied: whitespace
- change_count: 594
- warnings: repeated_header_footer_candidate_not_removed:(continued on next page)
- manual_review_required: true
- quality_result: PASS

### DOC000009

- selection_reason: baseline_ocr_pdf
- changed: true
- rules_applied: whitespace
- change_count: 16
- warnings: none
- manual_review_required: false
- quality_result: PASS

### DOC000236

- selection_reason: very_short_image_heavy
- changed: true
- rules_applied: whitespace
- change_count: 494
- warnings: none
- manual_review_required: false
- quality_result: PASS
