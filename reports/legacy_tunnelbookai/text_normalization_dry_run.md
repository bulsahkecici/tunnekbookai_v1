# TunnelBookAI Text Normalization Dry Run

## Result

**GO**

## Scope

- Documents analyzed in memory: **214/214**
- Changed if applied: **172**
- Unchanged if applied: **42**
- `data/corpus_normalized/` written by dry-run: **false**
- Target existed before this requested dry-run: **true**

## Rule Impact

- unicode: documents **3**, changes **54**
- whitespace: documents **171**, changes **27939**
- ocr_spacing: documents **5**, changes **45**
- linebreak: documents **12**, changes **790**
- hyphenation: documents **0**, changes **0**
- header_footer: documents **0**, changes **0**
- replacement_character: documents **16**, changes **153**
- encoding_cleanup: documents **0**, changes **0**
- placeholder encounters: **14991**

## Risk Analysis

- numeric_mismatch: **0**
- url_mismatch: **0**
- doi_mismatch: **0**
- isbn_mismatch: **0**
- issn_mismatch: **0**
- standard_document_code_mismatch: **0**
- front_matter_mismatch: **0**
- citation_provenance_mismatch: **0**
- table_corruption: **0**
- technical_symbol_corruption: **0**
- technical_abbreviation_corruption: **0**
- formula_placeholder_loss: **0**
- image_placeholder_loss: **0**

## Gate

**GO FOR STRATIFIED PILOT**
