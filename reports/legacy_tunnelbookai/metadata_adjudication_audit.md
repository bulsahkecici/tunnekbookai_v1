# TunnelBookAI Metadata Adjudication Audit

## Sonuç

- Karar: **GO**
- Giriş suggestion row: **511**
- Eski queue V2: **494**
- verified_existing: **0**
- auto_safe_candidate: **55**
- human_review_required: **154**
- unresolved_nonblocking: **270**
- rejected_suggestion: **32**

## Review Queue V3

- Toplam: **154**
- P0: **4**
- P1: **143**
- P2: **7**

- V2 → V3 azalma: **340 satır (%68.8)**

### Field bazında review

- title: **3**
- organization: **59**
- year: **28**
- language: **7**
- document_type: **52**
- authority_level: **5**
- topics: **0**

### Field bazında auto-safe

- title: **0**
- organization: **17**
- year: **3**
- language: **1**
- document_type: **10**
- authority_level: **24**
- topics: **0**

## Stratified sample quality audit

- Örnek sayısı: **34**
- Unsafe auto-safe örnek: **0**
- Sonuç: **PASS**
- İlk kalite incelemesinde abstract-only DOC000309 type adayı ve yalnız affiliation'a dayanan Authority B adayları yakalandı; kurallar sıkılaştırılıp çıktılar yeniden üretildi.
- title: (auto-safe yok)
- organization: DOC000193, DOC000018, DOC000098, DOC000145, DOC000024, DOC000072, DOC000121, DOC000116, DOC000113, DOC000117
- year: DOC000017, DOC000042, DOC000063
- language: DOC000307
- document_type: DOC000073, DOC000015, DOC000132, DOC000012, DOC000128, DOC000308, DOC000167, DOC000127, DOC000063, DOC000023
- authority_level: DOC000126, DOC000014, DOC000127, DOC000167, DOC000216, DOC000115, DOC000218, DOC000157, DOC000066, DOC000308
- topics: (auto-safe yok)

## Candidate master ve bütünlük

- Candidate master: **214/214**
- Unique document_id: **214**
- Korunan existing_verified alan değeri: **213**
- Current/verified değişikliği: **False**
- Corpus değişikliği: **False**

## Testler

- Native macOS .venv: tests 78/78 PASS; rapor/tests 16/16 PASS; total 94/94 PASS

## Warnings

- `unresolved_nonblocking` kayıtlar bilinçli olarak V3 queue dışında tutuldu.
- Auto-safe değerler yalnız candidate master'a yazıldı; canonical metadata master'a uygulanmadı.

## Blockers

- Yok.

## Nihai karar

**GO**
