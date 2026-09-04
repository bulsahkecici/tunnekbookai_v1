# Chunking Contract

Yapı farkında, çok kipli (multimodal) chunk'lama sözleşmesi.
Motor: `tunnelbookai/ingest/chunking/`. Yapılandırma: `config/chunking.yaml`.

Bu katman **embedding hesaplamaz**. Yalnız chunk üretir, doğrular ve embedding'e uygunluk
kararı verir.

---

## 1. Yetkili konum

```text
processing/<document_id>/chunks/chunk_manifest.jsonl     ← YETKİLİ
processing/<document_id>/chunks/embedding_ready.jsonl
processing/<document_id>/chunk_quality.json
```

`corpus/staging/v2/<document_id>/bundle.json` bu yolu
`chunks_authoritative_path` alanıyla **referans eder**; staging'de ikinci bir chunk kopyası
tutulmaz. Tek yetkili kaynak olması, chunk'ların yeniden üretildiğinde staging'le
sessizce ayrışmasını engeller.

Koşu genelinde toplam: `audit/embedding_ready_manifest.jsonl`.

---

## 2. Chunk tipleri

Kipler düz metne **düzleştirilmez**. Her kip birinci sınıf bir chunk tipidir.

| Tip | Kaynak | Not |
|---|---|---|
| `TEXT_CHUNK` | Başlık/paragraf/liste eleman akışı | PDF, DOCX, HTML, MD, TXT |
| `TABLE_CHUNK` | `tables/TABLE####.json` | Yapılandırılmış dosya otoritedir |
| `FIGURE_CHUNK` | `figures/FIG####.png` + altyazı + OCR + görsel açıklama | Üç alan **ayrı** tutulur |
| `OCR_CHUNK` | Sayfa kapsamlı OCR | Figür chunk'ında zaten temsil edilen metin tekrarlanmaz |
| `SLIDE_CHUNK` | PPTX slaytı | Başlık, gövde, konuşmacı notu, tablo/figür referansları |
| `SHEET_CHUNK` | XLSX sayfası, satır bantları hâlinde | Çalışma kitabı tek dev chunk olmaz |

Bir çalışma kitabı `SHEET_CHUNK`'larla tam temsil edildiği için ayrıca `TEXT_CHUNK`
üretilmez; bir sunum için de aynısı `SLIDE_CHUNK` ile geçerlidir.

---

## 3. Yapı sınırları ve token politikası

Metin, körlemesine her N karakterde bölünmez. Sınır önceliği:

```text
heading → subheading → paragraph → list → section → page
```

Bir başlık, mevcut chunk zaten asgari boyuta ulaştıysa yeni chunk başlatır. Yalnızca tek
bir paragraf `hard_max`'ı aşarsa son çare olarak cümle sınırlarından bölünür.

`config/chunking.yaml → tokens`:

| Alan | Değer | Gerekçe |
|---|---|---|
| `tokenizer` | `unicode-lexical-v1` | `scripts/11_semantic_chunking.py` ile aynı tokenizer |
| `target` | 850 | Kanonik 214 belgelik corpus üzerinde doğrulanmış legacy politika |
| `min` | 250 | Altındaki bitişik parça, aynı başlık yolundaysa öncekiyle birleştirilir |
| `max` | 1200 | Normal üst sınır |
| `hard_max` | 1500 | Aşılamaz; chunk kalite kapısı bunu hata sayar |
| `overlap` | 80 | Bu motorda yeni |

Görev metni başlangıç önerisi olarak 700/1000/150 veriyordu; §51 "mevcut test edilmiş
değerleri yeniden kullan" dediği ve bu projede gerçek corpus üzerinde doğrulanmış bir
politika (`semantic-markdown-v1.1`) bulunduğu için o değerler taşındı, yeniden ayarlanmadı.

Tokenizer, model tokenizer'ı değil deterministik bir vekildir — çevrimdışı ve kararlı bir
chunk politikasının ihtiyacı tam olarak budur.

---

## 4. Chunk şeması

```json
{
  "chunk_id": "ING_ABC123_CH_4f2a9c1b03",
  "ordinal": 42,
  "document_id": "ING_ABC123",
  "chunk_type": "TEXT_CHUNK",

  "final_primary_section": "4.1",
  "final_secondary_sections": [],

  "heading_path": ["4. MALİYET KAVRAMI", "4.1 Maliyet Kavramı ve İlgili Tanımlar"],

  "page_start": 17,
  "page_end": 18,
  "slide_number": null,
  "sheet_name": null,
  "cell_range": null,

  "source_elements": ["PARA0032", "PARA0033"],

  "text": "...",
  "token_count": 684,

  "provenance": {
    "original_sha256": "...",
    "source_kind": "MANUAL_INTERNAL",
    "format": "PDF",
    "evidence_level": "FULL_TEXT"
  },

  "chunk_schema_version": "1.0",
  "chunk_policy_version": "structure-aware-v1",
  "tokenizer": "unicode-lexical-v1"
}
```

### Kip başına ek alanlar

`TABLE_CHUNK`: `table_id, caption, structured_path, csv_path, image_path, page, rows, columns`
— metin gövdesi erişim için kısa bir tablo dökümüdür; **otorite `structured_path`'tir**.

`FIGURE_CHUNK`: `figure_id, caption, ocr_text, ocr_status, visual_description,
visual_description_status, image_path, page`
— vision çalışmadıysa `visual_description: null` ve `visual_description_status: NOT_RUN`.
Açıklama asla uydurulmaz ve OCR metninden **türetilmez**.

`OCR_CHUNK`: `ocr_item_id, ocr_scope, ocr_status, ocr_engine, ocr_confidence, page`
— RapidOCR kalibre bir skor vermediği için `ocr_confidence` `null` kalır.

`SLIDE_CHUNK`: `slide_number, slide_title, speaker_notes, table_refs, figure_refs,
chart_refs, snapshot_path` — çok büyük bir slayt birden fazla chunk üretebilir.

`SHEET_CHUNK`: `sheet_name, sheet_hidden, cell_range, used_range, formula_present,
formula_count, excel_tables, structured_path, csv_path`.

---

## 5. Provenance

Her chunk `page_start`/`page_end` taşır (mevcutsa). Office kipleri için sırasıyla
`slide_number`, `sheet_name` ve `cell_range` doldurulur. `provenance.original_sha256` ve
`provenance.source_kind` **zorunludur**; eksikse chunk kalite kapısı hata verir.

`source_elements`, `normalized/document.json` içindeki eleman kimliklerine
(`PARA0032`, `HEAD0007`, `TABLE0003`, `FIG0008`, `SHEET0001`, `SLIDE0002`, `OCRPAGE0001`)
işaret eder ve kalite kapısında **doğrulanır** — çözülemeyen bir referans hatadır.

---

## 6. Kararlı chunk kimlikleri

```text
chunk_id = <document_id>_CH_<sha256(...)[:10]>
```

Hash girdisi: `document_id`, `chunk_type`, kaynak eleman sınırları, `chunk_policy_version`,
`chunk_schema_version` ve normalize edilmiş metin.

Yalnız sıra numarasına dayanan bir kimlik, içerik değiştiğinde aynı kimliği sessizce
yeniden kullanırdı; metin hash'e dahil olduğu için değişen bir chunk yeni kimlik alır.
Sıra bilgisi ayrı bir `ordinal` alanında tutulur. Boşluk farkları kimliği değiştirmez.

---

## 7. Belge içi tekrar bastırma

Aynı içerik hem yerel metin hem sayfa OCR'ı olarak gelebilir; ikisi de saklanırsa erişimde
çift kanıt oluşur. Chunk'lar 5-gram shingle Jaccard benzerliğiyle karşılaştırılır
(eşik 0.92) ve şu öncelikle korunur:

```text
TEXT_CHUNK > SLIDE_CHUNK = SHEET_CHUNK > TABLE_CHUNK > FIGURE_CHUNK > OCR_CHUNK
```

Yani yerel metin OCR'a tercih edilir. Elenen chunk'lar `chunk_quality.json →
deduplicated_chunks` içinde `duplicate_of` ile birlikte kaydedilir — sessizce atılmaz.

Ayrıca bir figür chunk'ında zaten yer alan OCR metni için ikinci bir `OCR_CHUNK`
üretilmez.

---

## 8. Chunk kalite kapısı

`processing/<document_id>/chunk_quality.json`, durum `PASS` / `WARN` / `FAIL`.

Hata (FAIL) sayılanlar:

- yinelenen `chunk_id`
- boş chunk
- `token_count` ile gerçek token sayısının uyuşmaması
- `hard_max` aşımı
- çözülemeyen `source_elements` referansı, veya hiç referans olmaması
- eksik `provenance` (`original_sha256` / `source_kind`)
- kanonik taksonomide olmayan birincil/ikincil bölüm kimliği
- eksik `chunk_schema_version` / `chunk_policy_version`
- `document_id` uyuşmazlığı
- birebir aynı metne sahip chunk'lar
- yakın-yineleme seli (chunk sayısının %25'inden fazlası)

Uyarı (WARN) sayılanlar: `max` (ama `hard_max` değil) aşımı, `min` altındaki metin
chunk'ları, sınırlı sayıda yakın-yineleme çifti.

Rapor ayrıca tip dağılımını, token istatistiklerini ve yürürlükteki politika sürümünü
kaydeder.

---

## 9. Embedding-ready manifest

`audit/embedding_ready_manifest.jsonl`, chunk başına bir satır:

```json
{
  "chunk_id": "...", "document_id": "...", "chunk_type": "TEXT_CHUNK",
  "section_id": "4.1", "secondary_section_ids": [], "ordinal": 42,
  "text_path": null,
  "embedding_text": "4. MALİYET KAVRAMI > 4.1 ...\n<gövde>",
  "token_count": 690,
  "page_start": 17, "page_end": 18, "slide_number": null, "sheet_name": null,
  "provenance": {...},
  "chunk_schema_version": "1.0", "chunk_policy_version": "structure-aware-v1",
  "eligible": true, "reason": "READY"
}
```

`embedding_text` = başlık yolu + kip bağlamı (tablo/şekil altyazısı, slayt başlığı, sayfa
adı) + gövde. Böylece erişimde chunk kendi bağlamını taşır.

Uygunsuzluk nedenleri: `DOCUMENT_NOT_STAGED`, `CHUNK_QUALITY_FAILED`, `TYPE_EXCLUDED`,
`TOO_SHORT` (`embedding_ready.min_tokens` altında), `NO_SECTION`.

Satırlarda **vektör yoktur ve hesaplanmaz**. Embedding ve Qdrant indeksleme ayrı,
kontrollü bir fazın işidir.
