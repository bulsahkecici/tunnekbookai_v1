# TunnelBookAI Text Normalization Audit

## Result

**GO**

## Input

- Raw final corpus documents: **214**
- Normalized documents: **214**
- Unique document IDs: **214**

## Change Summary

- Changed documents: **172**
- Unchanged documents: **42**
- Total replacements/changes: **28981**
- normalized_with_warning: **29**
- manual_review_required flag: **29**
- failed: **0**

## Rule Counts

- unicode: **54**
- whitespace: **27939**
- ocr spacing: **45**
- linebreak: **790**
- hyphenation: **0**
- header footer: **0**
- replacement character: **153**
- encoding cleanup: **0**
- formula placeholders encountered: **421**
- image placeholders encountered: **14570**

## Safety Audit

- numeric mismatch: **0**
- url mismatch: **0**
- doi mismatch: **0**
- isbn mismatch: **0**
- issn mismatch: **0**
- standard document code mismatch: **0**
- front matter mismatch: **0**
- citation provenance mismatch: **0**
- table corruption: **0**
- technical symbol corruption: **0**
- technical abbreviation corruption: **0**
- formula placeholder loss: **0**
- image placeholder loss: **0**
- unsafe semantic rewrite: **0**

## Review Queue

- Total: **29**
- P0: **0**
- P1: **29**
- P2: **0**

## Corpus Integrity

- Source corpus changed: **false**
- Baseline changed: **false**
- Full Docling changed: **false**
- Metadata protected files changed: **0**
- Normalized count: **214**
- Missing: **0**
- Duplicate ID: **0**
- Failed: **0**

## Pilot

- Selected: **15**
- Passed: **15**
- Unsafe changes: **0**
- Manual review: **4**

## Tests

- Previous/non-normalization tests: 96/96 PASS; new normalization tests: 27/27 PASS; rapor/tests: 16/16 PASS; total: 139/139 PASS

## Idempotency

- Second-run changes: **0**
- Normalized SHA mismatch: **0**
- Manifest stability: **PASS**

## Warnings

- P1/P2 residual review records: **29**
- Belirsiz header/footer adayları silinmedi; replacement character değerleri tahmin edilmeden görünür marker ile işaretlendi.

## Blockers

- Yok.

## Final Decision

**GO**
