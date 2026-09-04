# TunnelBookAI Final Corpus Audit

## Sonuç

- Karar: **GO**
- Ana baseline canonical belge sayısı: **214**
- Full Docling ile değiştirilen belge sayısı: **138**
- Baseline kalan belge sayısı: **76**
- Quality reject sayısı: **8**
- No improvement sayısı: **8**
- Persistent Docling failure sayısı: **1**
- Final corpus toplam belge sayısı: **214**

## Integrity kontrolleri

- Eksik final output: **0**
- Boş final output: **0**
- Duplicate document_id: **0**
- Duplicate final path: **0**
- Exact duplicate SHA tekrar dahil edilmiş: **0**
- SHA/provenance problemi: **0**
- Baseline kaynak ağacı değişti: **false**
- Full Docling kaynak ağacı değişti: **false**
- Her canonical document_id için tek final Markdown: **true**

## Metadata eksiklikleri

Bu aşamada metadata LLM ile doldurulmadı; aşağıdaki boşluklar mevcut canonical metadata'dan aynen taşındı:

- `document_id`: **0**
- `source_relative_path`: **0**
- `sha256`: **0**
- `authority_level`: **189**
- `document_type`: **193**
- `language`: **137**
- `year`: **186**
- `topics`: **152**

## Provenance

- Citation sidecar referansı bulunan Full Docling belge: **138**
- Original-page provenance mevcut Full Docling belge: **88**
- Citation-safe Docling JSON sidecar dosyaları yerinde bırakıldı; manifest yalnız referanslarını taşır.
- Final Markdown dosyaları seçilen kaynaktan byte-for-byte kopyalandı; front matter değiştirilmedi.

## Kapsam dışı

OCR normalization, LLM metadata tamamlama, chunking, embedding, Qdrant ve RAG çalıştırılmadı.
