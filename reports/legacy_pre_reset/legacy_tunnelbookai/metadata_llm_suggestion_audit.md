# TunnelBookAI Local LLM Metadata Suggestion Audit

## Sonuç

- Karar: **GO**
- Çalışma tarihi: 2026-08-16 (Europe/Istanbul)
- İşlem yalnız suggestion/evidence/confidence çıktıları üretti; current/verified metadata'ya uygulanmadı.
- `data/corpus_final/`, canonical manifest, metadata master ve historical snapshot değişmedi.

## Endpoint preflight ve model

- Endpoint: `http://127.0.0.1:1234/v1`
- `GET /models`: **PASS**
- Seçilen gerçek model kimliği: `qwen3.6-35b-a3b-mlx`
- Config/model eşleşmesi: **PASS**
- OpenAI-compatible `chat/completions`: **PASS**
- Metadata'ya yazmayan strict JSON Schema smoke: **PASS**
- Smoke parse retry: **0**
- Smoke gözlenen süre: **11.901 saniye**
- Harici/ücretli API: **kullanılmadı**; yalnız loopback HTTP kabul ediliyor.
- LM Studio bu reasoning modelinde schema-constrained JSON'u boş `content` yanında `reasoning_content` alanında döndürebiliyor. Uygulama bu alanı yalnız `content` boşsa ve baştan sona strict schema JSON ise kabul ediyor; prose/mixed text reddediliyor.

## Seçim ve context

- Metadata master belge sayısı: **214**
- LLM yardımı gerektiren seçilmiş belge: **201**
- High-confidence/current alanlar yeniden tahmin edilmedi.
- Seçilen alan sayısı: **511**
  - authority_level: 182
  - organization: 165
  - document_type: 81
  - year: 67
  - language: 10
  - title: 5
  - topics: 1
- Context deterministik olarak document identity, source bilgileri, current/deterministic metadata, headings, ilk yaklaşık 2.000 kelime ve son yaklaşık 750 kelimeden oluşturuldu.
- Yoğun OCR metninin model context limitini aşmasını önlemek için deterministik 12.000 karakter first-excerpt ve 4.000 karakter tail tavanı uygulandı.
- DOC000239 final Markdown, corpus içindeki benzersiz front-matter `document_id` ile güvenli biçimde çözüldü; corpus dosyası yeniden adlandırılmadı/değiştirilmedi.

## Pilot

- Pilot kapsamı: **5 belge**
- İşlenen: **5/5**
- Structured JSON parse: **5/5 PASS**
- Parse retry / failed inference: **0 / 0**
- Ortalama pilot inference süresi: **2.967 saniye/belge**
- Cache/resume tekrarında: **5 cache hit, 0 inference**
- Pilot kalite incelemesi sonucunda title/organization/year value-to-evidence bağı ve A/B/C/D authority evidence-class guard'ları sıkılaştırıldı.
- Guard sonrası unsupported title ve authority sınıfları low-confidence/review veya unclassified durumuna indirildi; full pass bundan sonra başlatıldı.

## Full suggestion pass

- Seçilen belge: **201**
- İşlenen belge: **201/201**
- Başarılı cache identity (`document_id + source_sha256 + model + prompt_version`): **201/201**
- Nihai idempotency turu: **201 cache hit, 0 inference**
- Nihai başarısız inference: **0**
- Nihai parse retry: **0**
- Başarılı gerçek inference'lar için gözlenen kümülatif ortalama süre: yaklaşık **5.80 saniye/belge**
- İlk full turda DOC000051 yoğun context nedeniyle LM Studio context-limit HTTP 400 verdi. Deterministik context tavanı sonrası resume turunda belge başarıyla işlendi; nihai çıktıda failure marker yok.

## Suggestion çıktısı

- Dosya: `data/metadata/metadata_llm_suggestions.csv`
- Satır: **511**
- Benzersiz belge: **201**
- Non-empty LLM suggestion: **396**
- High confidence: **208**
- Medium confidence: **22**
- Low confidence: **281**
- Deterministic + LLM agreement: **18**
- Deterministic + LLM conflict: **5**
- LLM only: **218**
- Unresolved: **270**
- Source SHA mismatch: **0**
- Out-of-vocabulary document type: **0**
- Failed inference marker: **0**
- SHA256: `430a0fc8654af4a53696b236ee2e3b1fa39108523f4c0b87709f194c6acfd711`

`unresolved` ve low-confidence kayıtlar güvenli/konservatif sonuçtur: uydurma değer üretmek yerine human review'a bırakılmıştır ve GO'yu engellemez.

## Review queue V2

- Dosya: `data/metadata/final_metadata_review_queue_v2.csv`
- Toplam satır: **494**
- P0: **283**
- P1: **202**
- P2: **9**
- SHA256: `744844815776c8abc70b00182454fe753a4395b525f9f20fcea1fbb3031e4b0e`
- Eski `final_metadata_review_queue.csv` değiştirilmedi; V2 ayrı üretildi.
- Hiçbir suggestion auto-accept edilmedi.

## Cache, resume ve atomiklik

- Aktif prompt version: `metadata-suggestion-v2.2`
- Aktif cache: **201 belge**
- Önceki pilot sürümlerinden kullanılmayan cache: v2.0 **5**, v2.1 **5**
- Eski cache'ler identity uyuşmadığı için okunmaz; aktif sonuçları etkilemez.
- Her belge sonrasında suggestion CSV ve V2 queue atomik checkpoint edilir.
- Son idempotency turunda suggestion ve queue SHA256 değerleri değişmedi.

## Bütünlük korumaları

- `final_metadata_master.csv` SHA256: `55fe1e44b57b705c8538690b2c0550e7c11fe8a8aed8618b3f1da04fada3d1e0` — **değişmedi**
- `final_corpus_manifest.csv` SHA256: `cf59e74f9435635a15f8446c20aa8d6fb5976c0434ee87022e067722cccf44c3` — **değişmedi**
- `source_snapshot.json` SHA256: `b4d78d3914aea2258a10b8549c5a4b2ecfa680d5048040b6255fbdafccf9ad6c` — **değişmedi**
- Final corpus dosya sayısı: **214**
- Her çalıştırmanın öncesi/sonrası corpus state kontrolü: **değişiklik yok**
- Normalization, chunking, embedding, Qdrant, RAG ve ağır Docling conversion: **çalıştırılmadı**

## Testler

- `.venv/bin/python -m unittest discover -s tests -v`: **61/61 PASS**
- `.venv/bin/python -m unittest discover -s rapor/tests -v`: **16/16 PASS**
- Toplam: **77/77 PASS**
- Yeni kapsama: disabled/unreachable endpoint, exact model discovery, strict ve fenced JSON, invalid JSON ve transient local HTTP retry, vocab guard, evidence grounding, A/B/C/D authority conservatism, overwrite protection, cache identity/resume, agreement/conflict, P0/P1/P2, context bound ve idempotency.

## Değişen/üretilen dosyalar

- `config/metadata_llm.yaml`
- `scripts/05_metadata_llm_review.py`
- `tests/test_metadata_llm_review.py`
- `data/metadata/metadata_llm_suggestions.csv`
- `data/metadata/final_metadata_review_queue_v2.csv`
- `data/metadata/cache/metadata_llm/` altındaki cache kayıtları
- `reports/metadata_llm_suggestion_audit.md`

## Warnings

- 270 alan evidence yetersizliği nedeniyle unresolved; bunlar P0/P1/P2 human review queue içinde tutuluyor.
- 10 eski pilot cache kaydı disk üzerinde duruyor ancak prompt-version identity nedeniyle aktif koşuda kullanılmıyor.
- LM Studio model context kapasitesi yükleme ayarına bağlıdır; yoğun OCR context'i için deterministik karakter tavanı zorunludur.

## Blockers

- **Yok.**

## Nihai karar

**GO**
