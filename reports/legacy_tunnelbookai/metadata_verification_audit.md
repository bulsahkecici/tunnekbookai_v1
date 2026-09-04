# TunnelBookAI Metadata Verification Audit

## Sonuç

- Karar: **GO**
- Endpoint/model: `http://127.0.0.1:1234/v1` / `qwen3.6-35b-a3b-mlx`
- Prompt version: `metadata-verification-v1.2`
- V3 input: **154**
- P0 conflicts: **4**
- Second pass processed: **150**
- Second-pass verified: **0**
- Still human review: **132**
- Unresolved: **18**
- Rejected: **4**
- Cache hits / calls: **150 / 0**
- Parse retry / failed inference: **0 / 0**
- Bu invocation gerçek inference ortalaması: **0.0 saniye**
- Aktif second-pass cache identity: **150 / 150**

## V4

- Toplam: **132**
- P0/P1/P2: **4 / 122 / 6**

## Field bazında sonuç

- title: verified=0, review=3, unresolved=0, rejected=0
- organization: verified=0, review=45, unresolved=13, rejected=1
- year: verified=0, review=27, unresolved=1, rejected=0
- language: verified=0, review=6, unresolved=1, rejected=0
- document_type: verified=0, review=46, unresolved=3, rejected=3
- authority_level: verified=0, review=5, unresolved=0, rejected=0
- topics: verified=0, review=0, unresolved=0, rejected=0

## P0 human packet

- CSV/Markdown kayıt: **4 / 4**
- P0 için otomatik karar verilmedi; dört kayıt V4 içinde de P0 olarak tutuldu.

## Stratified sample audit

- Örnek: **0**
- Unsafe verification: **0**
- İlk model sınıflandırmasındaki 7 tentative verified kaydın tamamı ayrıca manuel incelendi. Organization conflict, sparse-language ve seminar-without-slide-structure guard'ları sıkılaştırıldı; final verified set boş ve unsafe count 0'dır.

## Final verified candidate

- Satır/unique: **214 / 214**
- Existing verified değişikliği: **False**
- Corpus değişikliği: **False**

## Testler

- Native macOS .venv: tests 96/96 PASS; rapor/tests 16/16 PASS; total 112/112 PASS

## Warnings

- Bilinmeyen metadata zorla doldurulmadı; unresolved/rejected değerler canonical metadata'ya uygulanmadı.
- Canonical metadata master'a otomatik merge yapılmadı.

## Blockers

- Yok.

## Nihai karar

**GO**
