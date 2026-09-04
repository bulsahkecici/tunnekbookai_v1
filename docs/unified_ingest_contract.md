# Unified Ingest Contract

Bu belge, `tunnelbookai/ingest` altındaki Unified Ingest Engine'in giriş sözleşmesini,
ürettiği paketi ve promosyon kurallarını tanımlar. Chunk şeması ayrı belgededir:
`docs/chunking_contract.md`.

Motorun **yapmadıkları** sözleşmenin parçasıdır: embedding hesaplamaz, Qdrant'a yazmaz,
soru bankası değerlendirmesi çalıştırmaz ve `corpus/canonical/` içine hiçbir koşulda yazmaz.

---

## 1. Giriş sözleşmesi

İki giriş yolu vardır ve ikisi de aynı hattı kullanır.

### 1.1 PaperCrawler handoff (`incoming/crawler/releases/<RELEASE>/`)

| Gereksinim | Kural |
|---|---|
| `00_registry/handoff_contract.json` | `schema_version` major = **2** (schema 1.x yalnız `--allow-legacy-1x` ile) |
| `producer` | `paper-crawler-agent` — başka üretici paketi bloklanır |
| `00_registry/handoff_manifest.jsonl` | Kayıt başına bir JSON nesnesi |
| Kayıt durumu | Yalnız `paper_crawler_status = READY_FOR_HANDOFF` işlenir |
| `sha256` | Manifest'teki değer diskteki dosyayla **birebir** eşleşmelidir; eşleşmezse kayıt `sha256_mismatch` ile atlanır |
| `local_path` | Release kökü içinde çözülmelidir |

Crawler'ın sınıflandırması **ipucudur**. `provisional_primary_section`,
`provisional_secondary_sections`, `provisional_section_confidence` ve
`crawler_evidence_level` provenance'ta korunur; nihai bölüm bu motorda yeniden hesaplanır
(§ 5). `crawler_evidence_level` nihai kanıt seviyesi olarak **kullanılmaz**.

### 1.2 Manuel gelen kutusu (`incoming/manual/inbox/`)

Handoff sözleşmesi aranmaz. Desteklenen uzantı yeterlidir. Manuel belgeler
`MANUAL_INTERNAL` kaynak türüyle işaretlenir ve **hiçbir ağ çağrısı yapılmadan** işlenir.

### 1.3 Desteklenen formatlar

| Grup | Formatlar | Not |
|---|---|---|
| Birincil | PDF, DOCX, PPTX, XLSX, PNG, JPG/JPEG | |
| Ek | TXT, MD, CSV, HTML/HTM | |
| Legacy | DOC, PPT, XLS, RTF | Yalnız LibreOffice kuruluysa kabul edilir |

Format tespiti önce OOXML ZIP magic sniff (yanlış uzantılı `.docx` yakalanır), sonra
uzantı, sonra mimetype ile yapılır. `UNKNOWN` format sessizce kabul edilmez:
`REJECT / UNSUPPORTED_FORMAT` olur.

---

## 2. Kimlik ve orijinal arşiv

Kimlik = içerik SHA256. `document_id = ING_<sha256[:20]>`.

```text
originals/<document_id>/
  source.<ext>     orijinalin bayt-birebir, salt-okunur kopyası
  original.json    document_id, original_filename, original_sha256, source_kind(s),
                   received_at, file_size, mime_type, format
```

Orijinal asla değiştirilmez, yeniden adlandırılmaz, dönüştürülmez. Yeniden işleme mevcut
arşivi kullanır; var olan arşivle SHA uyuşmazlığı sert hatadır (`ArchiveConflict`).

---

## 3. İşleme paketi (`processing/<document_id>/`)

```text
processing/<document_id>/
├── provenance.json           tüm kaynakların birleşimi (crawler + manuel)
├── original.json → originals/<id>/original.json ile eşleşir
├── extraction_report.json    motor sürümleri, uygulanan Docling seçenekleri, uyarılar
├── normalized/
│   ├── document.json         YAPISAL OTORİTE
│   ├── document.md           erişim / insan-okur temsil
│   └── document.txt          düz metin yedeği
├── pages/page_0001.png       PDF sayfa görüntüleri (görsel provenance)
├── slides/slide_0001.png     PPTX slayt görüntüleri (renderer varsa)
├── sheet_snapshots/          XLSX görselleri (opsiyonel, otorite değil)
├── figures/FIG0001.png       figürler + OCR + (varsa) yerel görsel açıklama
├── tables/TABLE0001.{json,csv,png}
├── sheets/<Sheet>.{json,csv}
├── charts/CHART0001.json     yalnız deterministik PPTX/XLSX chart üstverisi
├── metadata.json
├── metadata_provenance.json
├── classification.json
├── quality_gate.json
├── chunk_quality.json
└── chunks/
    ├── chunk_manifest.jsonl  YETKİLİ chunk konumu
    └── embedding_ready.jsonl
```

`document.json` yapısal otoritedir; `document.md` ondan türetilmiş erişim temsilidir.

### 3.1 Format başına otorite

| Format | Yapısal otorite | Not |
|---|---|---|
| PDF | Docling `DoclingDocument` | Metin katmanı pdfium ile ölçülür; boşsa OCR devreye girer ve bu kayda geçer |
| DOCX | **Orijinal DOCX** (Docling ile) | Render edilmiş PDF asla yapısal otorite değildir; yalnız görsel snapshot üretir |
| PPTX | **Orijinal PPTX** (python-pptx) | Slayt sırası, başlık, gövde, tablo, figür, chart üstverisi, konuşmacı notu |
| XLSX | **openpyxl çalışma kitabı modeli** | `data_only=False` (formüller) + `data_only=True` (önbellek değerleri) |
| PNG/JPG | Görselin kendisi | Tek başına geçerli bir kaynak belgedir |
| TXT/MD/CSV/HTML | Orijinal kaynak metin | HTML yapısal çıkarım ham işaretlemeden yapılır |

### 3.2 Asset şemaları

**Sayfa/slayt snapshot'ı** — *görsel provenance, metinsel kanıt değil*:

```json
{"asset_id": "PAGE0001", "asset_type": "PAGE", "page_number": 1,
 "path": "processing/<id>/pages/page_0001.png", "sha256": "...",
 "width": 1224, "height": 1584, "renderer": "pypdfium2", "role": "VISUAL_PROVENANCE"}
```

**Figür** — OCR metni ve görsel açıklama **ayrı alanlardır**, asla birleştirilmez:

```json
{"asset_id": "FIG0001", "asset_type": "FIGURE", "page": 14, "caption": null,
 "bbox": [l, t, r, b], "sha256": "...", "pixel_digest": "...",
 "ocr_status": "SUCCESS", "ocr_text": "...", "ocr_confidence": null,
 "visual_description_status": "NOT_RUN", "visual_description": null}
```

`bbox` ve `page` yalnız Docling provenance verdiyse doldurulur; yoksa `null` kalır.

**Tablo** — markdown içinde yaşamaz:

```json
{"table_id": "TABLE0001", "page": 12, "caption": null, "bbox": null,
 "rows": 4, "columns": 3, "rectangular": true,
 "structured_path": "processing/<id>/tables/TABLE0001.json",
 "csv_path": "processing/<id>/tables/TABLE0001.csv", "image_path": null}
```

`TABLE0001.json` grid + OTSL + HTML tutar (birleşik hücre sadakati). CSV **yalnız**
tablo güvenle dikdörtgen değerlere indirgenebiliyorsa yazılır.

**Sayfa (XLSX) hücre modeli** — formül asla kaybolmaz, değer asla uydurulmaz:

```json
{"sheet": "Maliyetler", "cell": "F22", "row": 22, "column": 6,
 "formula": "=SUM(F2:F21)", "value": null, "data_type": "f"}
```

`value` yalnız Excel'in yazdığı önbellek değeridir. Önbellek yoksa `null` kalır; formül
dizesi değer yerine sunulmaz. Bu bir durdurma koşuludur.

**Chart** — Docling 2.124.0'ın `do_chart_extraction`'ı **kapalıdır**: bir sondajda düz
renk geçişli bir görüntüden tamamen uydurma bir "Bar chart" seri tablosu üretti. Yalnız
PPTX/XLSX'in kendi paketinden okunan deterministik chart üstverisi kaydedilir.
Durumlar: `SUCCESS` / `DISABLED` / `NOT_SUPPORTED` / `FAILED_NONBLOCKING`.
Chart çıkarımı hiçbir koşulda belgeyi başarısız yapmaz.

---

## 4. Metadata ve provenance

`metadata.json` asgari şeması (`tunnelbookai/ingest/metadata/schema.py`):

```json
{
  "document_id": "...", "source_kind": "MANUAL_INTERNAL | EXTERNAL_DISCOVERY",
  "original_filename": "...", "original_sha256": "...",
  "format": "...", "mime_type": "...",
  "title": null, "authors": [], "organization": null, "department": null,
  "document_date": null, "revision": null, "language": null,
  "document_type": null, "topics": [],
  "source_url": null, "doi": null,
  "confidentiality": "PUBLIC | INTERNAL | RESTRICTED | UNKNOWN",
  "document_status": "FINAL | APPROVED | DRAFT | WORKING_DOCUMENT | UNKNOWN",
  "ingest_method": "manual_inbox | crawler_handoff",
  "final_primary_section": null, "final_secondary_sections": [],
  "final_section_confidence": null,
  "final_evidence_level": null, "content_capabilities": {},
  "schema_version": "1.0"
}
```

Kontrollü sözlükler (`document_type`, `topics`) `scripts/09_metadata_enrichment.py`
içinden **import edilir**, kopyalanmaz.

### 4.1 Uydurma yasağı

`metadata_provenance.json` her önemli alan için bir kayıt tutar:

```json
{"field": "title", "value": "...", "source": "document_heading",
 "confidence": 0.98, "inferred": false, "reason": null}
```

`source` ∈ `original_file | document_heading | document_content | ooxml_properties |
crawler_manifest | local_llm | not_found`.

- `inferred = true` ise `reason` **ve** `confidence` zorunludur (kod seviyesinde dayatılır).
- `organization` ve `department` dosya adından veya gövde metninden **asla** çıkarılmaz.
- Bilinmeyen alan `null` ya da `UNKNOWN` kalır.
- Opsiyonel loopback-LLM zenginleştirmesi yalnız *hâlâ boş* alanları doldurur ve önerdiği
  dize metinde **birebir** geçmiyorsa reddedilir (`METADATA_LLM_REJECTED_NOT_VERBATIM`).
- Başlık dosya adına düşerse `title_inferred_from_filename = true` işaretlenir; bu
  başlık dedup'ta kimlik kanıtı sayılmaz.

---

## 5. Global dedup

Öncelik sırası, ilk eşleşen karar verir:

| # | Kural | Güç | Sonuç |
|---|---|---|---|
| 1 | SHA256 | `EXACT` | Tek belge kimliği |
| 2 | Normalize DOI | `EXACT` | Tek belge kimliği |
| 3 | Normalize URL (tracking parametreleri atılır) | `EXACT` | Tek belge kimliği |
| 4 | Normalize tam başlık + aynı yıl | `STRONG` | Tek belge kimliği |
| 5 | Bulanık başlık + yıl + yazar/kurum | `PROBABLE` | **Otomatik birleştirilmez**, `DUPLICATE_CANDIDATE` |

Aynı SHA'nın crawler'dan **ve** manuel gelen kutusundan gelmesi = **bir belge, iki
provenance kaynağı**. Motor girişleri işlemeden önce kimliğe göre gruplar, böylece her
kaynak provenance'ına katkı verir ama çıkarım bir kez çalışır.

Türkçe normalizasyon notu: NFKD, noktasız `ı` (U+0131) harfini ayrıştırmaz. Ayrı bir
katlama tablosu olmadan "Bakımı" → "bak m" olur ve Türkçe başlık eşleştirmesi bozulur;
`normalize_title` bu katlamayı yapar.

Defter: `audit/source_registry.jsonl` (belge kimliği başına bir satır).

---

## 6. Nihai bölüm sınıflandırması

Tek kanonik taksonomi: **`book/scope/normalized/book_scope.json`** (66 bölüm, 59 soru
bankası bölümü). `crawler/config/taxonomy.yaml` yalnız *terim sözlüğü* olarak yüklenir;
orada olup kanonik kapsamda olmayan bir kimlik yok sayılır, asla benimsenmez.

Akış:

```text
belge → yapısal chunk'lar → aday bölüm getirimi (loopback embedding)
      → chunk oyları → kural sinyalleri → crawler ipucu
      → uzlaşma/çatışma mantığı → gerekirse yerel Qwen hakem → NİHAİ
```

Girdi olarak başlık, gerçek abstract, başlıklar, tam normalize metin, tablo ve figür
altyazıları, OCR metni, metadata ve crawler ipucu kullanılır.

Hakem **yalnız** şu durumlarda çağrılır: düşük füzyon skoru, iki adayın yakın olması,
kural/embedding çatışması, çok bölümlü belirsizlik, veya crawler/nihai uyuşmazlığı.
Güçlü deterministik uzlaşma modele gitmez. Hakem aday kümesi dışında bir kimlik
döndürürse reddedilir (`REJECTED_INVALID_SECTION`).

`classification.json`:

```json
{
  "final_primary_section": "5.5.2",
  "final_secondary_sections": ["5.4", "5.6"],
  "final_section_confidence": 0.92,
  "classification_methods": ["heading_rules", "chunk_vote", "embedding"],
  "crawler_provisional_section": "5.5.2",
  "crawler_final_agreement": true,
  "section_evidence": [{"section_id": "5.5.2",
                        "supporting_elements": ["PARA0012", "TABLE0003"]}],
  "candidates": [...], "decision_path": [...], "warnings": [...],
  "taxonomy_source": "book/scope/normalized/book_scope.json"
}
```

Bir belge tek bölüme zorlanmaz: bir birincil, sıfır veya daha fazla ikincil bölüm.
İkincil eşiği `config/classification.yaml → secondary_sections.min_score`.

---

## 7. Nihai kanıt modeli

TunnelBookAI'ın **kendi** kanıt seviyesi (`tunnelbookai/ingest/evidence.py`);
PaperCrawler'ın crawler-tarafı kanıtı burada yeniden kullanılmaz.

| Seviye | Anlamı |
|---|---|
| `FULL_TEXT` | Gerçek, sürekli metin katmanı belgeyi taşıyor |
| `STRUCTURED_DOCUMENT` | Yapı (başlık/slayt) taşıyor, metin katmanı daha ince |
| `STRUCTURED_TABULAR` | Çalışma kitabı; otorite hücre/formül modeli |
| `IMAGE_OCR` | Metin yalnız OCR ürettiği için var |
| `VISUAL_ONLY` | Geçerli görsel, kurtarılabilir metin yok |
| `PARTIAL` | Çıkarım başarılı ama belgenin bir kısmı kayıp |
| `UNUSABLE` | Güvenilir hiçbir şey çıkmadı |

`content_capabilities` her zaman tam anahtar kümesiyle yazılır:
`text, tables, figures, page_snapshots, ocr, vision, formulas, charts, slides, sheets`.

Taranmış bir PDF asla `FULL_TEXT` değildir: pdfium ile ölçülen yerel metin katmanı boşsa
ve metin OCR'dan geldiyse seviye `IMAGE_OCR` olur.

---

## 8. Belge kalite kapısı

`GO` için hepsi sağlanmalıdır: orijinal var, SHA geçerli, format destekli, yapısal
çıkarım başarılı, provenance var, metadata şeması geçerli, nihai bölüm kimliği
taksonomide, kritik çıkarım hatası yok, kanıt seviyesi `UNUSABLE` değil.

Format özel kurallar:

| Format | Kural |
|---|---|
| PDF | Sayfa sayısı tutarlı; snapshot oranı eşiğin altındaysa **REVIEW** |
| DOCX / PPTX | Renderer yokluğu tek başına **asla REJECT değildir** → `VISUAL_RENDERER_UNAVAILABLE` REVIEW nedeni |
| XLSX | Yapısal çalışma kitabı çıkarımı **zorunludur** |
| PNG / JPG | OCR metni olmayan geçerli görsel `VISUAL_ONLY` + REVIEW olabilir |

REVIEW nedenleri: `VISUAL_RENDERER_UNAVAILABLE`, `LOW_SECTION_CONFIDENCE`,
`OCR_EMPTY_TEXT_IMAGE`, `CRAWLER_FINAL_SECTION_DISAGREEMENT`,
`VISION_UNAVAILABLE_VISUAL_ASSET`, `PARTIAL_EVIDENCE`.

---

## 9. Staging ve promosyon

`corpus/staging/` altındaki **122 legacy düz paket korunur**; hiçbiri silinmez, taşınmaz
veya üzerine yazılmaz. Unified Ingest sürümlü bir alt ağaca yazar:

```text
corpus/staging/v2/<document_id>/
├── bundle.json          yetkili manifest (bundle_shape: unified_ingest_v1)
├── metadata.json  metadata_provenance.json
├── classification.json  quality_gate.json  provenance.json
├── extraction_report.json  chunk_quality.json
└── document.md
```

`bundle.json.chunks_authoritative_path` `processing/<id>/chunks/chunk_manifest.jsonl`
konumunu **referans eder**; chunk'ların ikinci bir kopyası tutulmaz.

`scripts/promote_staging.py` varsayılan olarak **dry-run**'dır. `--apply` zorunludur ve
hedef `corpus/canonical` ise komut çıkış kodu 2 ile **reddeder**. Kanonik promosyon bu
motorun işi değildir.

---

## 10. Yerel-yalnız güvenlik sınırı

- Docling `enable_remote_services` ve `allow_external_plugins` kod içinde `False`'a
  sabitlenir; config bunları açamaz.
- Vision, embedding ve LLM hakem uç noktaları yalnız `127.0.0.1 / localhost / ::1`
  olabilir. Başka bir host `RemoteEndpointRejected` fırlatır — sessiz geri düşüş yoktur.
- `vision.remote_allowed: true` veya loopback dışı `allowed_hosts` yapılandırması
  başlatmayı reddettirir.
- Manuel belge işleme yolunda hiç soket açılmaz (test ile dayatılır).
- Bulut embedding/LLM geri düşüşü yoktur; yerel sunucu yoksa ilgili adım
  `UNAVAILABLE` olarak kaydedilir ve motor kuralcı yola düşer.

---

## 11. CLI

```bash
.venv/bin/python scripts/ingest_incoming.py --source all --dry-run
.venv/bin/python scripts/ingest_incoming.py --source manual --resume
.venv/bin/python scripts/ingest_incoming.py --source crawler --resume
```

| Seçenek | Etki |
|---|---|
| `--source crawler\|manual\|all` | Giriş yolu seçimi |
| `--dry-run` | Yalnız envanter: arşiv yok, Docling yok, OCR yok, staging yok, chunk yok |
| `--resume` | Terminal durumdaki belgeleri atlar (provenance yine tazelenir) |
| `--force-reprocess` | Türetilmiş çıktıları yeniden üretir; orijinali asla |
| `--document-id` | Tek belgeye kısıtlar |
| `--max-documents` | Parti boyutu |
| `--no-ocr` / `--no-vision` | İlgili sağlayıcıyı kapatır (durum kaydedilir) |
| `--no-chunking` | Staging'de durur (normal koşuda chunk'lama dahildir) |
| `--no-arbiter` | Yerel LLM hakemi hiç çağırmaz |
| `--from-stage <STATE>` | O aşamaya ulaşmış belgeleri yeniden işler |
| `--allow-legacy-1x` | Migrasyonlu schema-1.1 crawler paketini kabul eder |

Durum makinesi (`audit/ingest_state.jsonl`):

```text
DISCOVERED → QUEUED → ORIGINAL_ARCHIVED → EXTRACTING → EXTRACTED → ASSETS_EXTRACTED
→ OCR_COMPLETED → METADATA_COMPLETED → DEDUP_COMPLETED → CLASSIFIED → QUALITY_GATED
→ STAGED → CHUNKING → CHUNKED → CHUNK_QUALITY_GATED → EMBEDDING_READY
```

`REVIEW` / `REJECTED` / `FAILED` dallanmaları korunur. Terminal durumlar:
`EMBEDDING_READY`, `REJECTED`, `ALREADY_PROCESSED`.

---

## 12. Denetim çıktıları

| Dosya | İçerik |
|---|---|
| `audit/ingest_state.jsonl` | Belge başına durum + geçmiş |
| `audit/ingest_manifest.jsonl` | Belge başına koşu özeti |
| `audit/source_registry.jsonl` | Dedup defteri: kimlik başına kaynaklar |
| `audit/document_id_map.jsonl` | SHA ↔ legacy/crawler kimlik eşlemesi |
| `audit/unified_ingest_quality.json` | Koşu özeti + ortam yetenekleri |
| `audit/embedding_ready_manifest.jsonl` | Chunk başına embedding uygunluğu |
| `audit/ingest_dry_run.json` | Dry-run envanteri |
