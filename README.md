# TunnelBookAI V1

TunnelBookAI V1; crawler hazırlama alanını, denetimli handoff'u, kanonik corpus'u ve kitap kalite araçlarını tek bir proje kökünde toplar. Kaynak projelerden kopyala-ilkesiyle taşınmıştır; eski projelerde silme, commit veya push yapılmamıştır.

## Dizinler

- `crawler/`: keşif, acquisition, sınıflandırma, coverage-gap ve handoff kodu
- `data/downloads/`: crawler'ın devam ettirilebilir çalışma çıktıları
- `handoff/`: kabul edilen paket, üst manifest ve manuel inceleme kuyruğu
- `tunnelbookai/ingest/`: Unified Ingest Engine (format adaptörleri, OCR/vision, metadata,
  dedup, sınıflandırma, kalite kapısı, chunk'lama)
- `incoming/`: motorun iki giriş yolu — `crawler/releases/` ve `manual/inbox/`
- `originals/`: değiştirilemez orijinal arşiv
- `processing/`: belge başına zengin çıkarım paketi ve yetkili chunk konumu
- `corpus/staging/`: kalite kapısından geçmeyi bekleyen yeni kaynaklar
  (`v2/` alt ağacı Unified Ingest paketleri içindir)
- `corpus/canonical/`: mevcut 214 dokümanlık kanonik corpus
- `corpus/metadata/`: kanonik metadata ve provenance
- `book/`: değişmez scope/question-bank paketi ve kitap QA çıktıları
- `shared/`: proje kalite kapısı ve kitap QA modülleri
- `audit/`, `reports/`: makinece okunur sonuçlar ve insan okunur denetimler

## Unified Ingest Engine

PaperCrawler `READY_FOR_HANDOFF` paketleri ve manuel belgeler (PDF, DOCX, PPTX, XLSX,
PNG, JPG, TXT, MD, CSV, HTML) **tek** bir motordan geçer.

**İki giriş yolu:**

- `incoming/crawler/releases/` — PaperCrawler'ın ürettiği schema-2.0 handoff paketleri.
  Sözleşme, üretici ve SHA256 doğrulanır; yalnız `READY_FOR_HANDOFF` kayıtlar işlenir.
- `incoming/manual/inbox/` — elle eklenen belgeler. Handoff sözleşmesi aranmaz; dosyayı
  bırakmak yeterlidir. Bu yolda hiçbir ağ çağrısı yapılmaz.

**Kullanım** (Python 3.12 `.venv` gerekir):

```bash
# 1) Ne işleneceğini gör — hiçbir şey yazılmaz
.venv/bin/python scripts/ingest_incoming.py --source all --dry-run

# 2) Manuel gelen kutusunu işle
.venv/bin/python scripts/ingest_incoming.py --source manual --resume

# 3) Crawler paketlerini işle
.venv/bin/python scripts/ingest_incoming.py --source crawler --resume
```

Başarılı bir koşu şunları yapar: orijinali arşivler → tam çıkarım (metin, tablo, figür,
sayfa/slayt görüntüsü, OCR, opsiyonel yerel vision) → metadata + provenance → global dedup
→ kanonik taksonomiye göre nihai bölüm sınıflandırması → belge kalite kapısı → staging →
yapı farkında çok kipli chunk'lama → chunk kalite kapısı → embedding-ready manifest.

Sık kullanılan seçenekler: `--document-id`, `--max-documents`, `--force-reprocess`,
`--from-stage <STATE>`, `--no-ocr`, `--no-vision`, `--no-chunking`, `--no-arbiter`,
`--allow-legacy-1x`.

**Motorun yapmadıkları:** embedding hesaplamaz, Qdrant'a yazmaz, soru bankası
değerlendirmesi çalıştırmaz ve `corpus/canonical/` içine hiçbir koşulda yazmaz.
Staging promosyonu ayrı ve varsayılan olarak dry-run'dır:

```bash
.venv/bin/python scripts/promote_staging.py          # dry run
```

Ayrıntılı sözleşmeler: `docs/unified_ingest_contract.md` ve `docs/chunking_contract.md`.
Yerel AI (embedding, VLM, LLM hakem) yalnız loopback üzerinde kabul edilir; loopback
dışı bir uç nokta yapılandırması motoru başlatmaz.

## Güvenli çalışma

Varsayılan crawler çıktısı `data/downloads` altındadır. Pipeline checkpoint'ten devam eder:

```bash
PYTHONPATH=. python crawler/src/prepare_tunnelbookai_handoff.py --resume
```

Belirli bir aşamadan yeniden başlatmak için:

```bash
PYTHONPATH=. python crawler/src/prepare_tunnelbookai_handoff.py --from-stage classify
```

`--fresh-run` checkpoint'i yeniler; mevcut indirilen dosyaları silmez. Cloud LLM fallback yoktur. Yerel model kullanılacaksa servis yalnız loopback üzerinde çalışmalıdır.

## Doğrulama

```bash
python scripts/validate_migration.py
PYTHONPATH=crawler/src python -m unittest discover -s crawler/tests -p 'test_*.py'
PYTHONPATH=.:scripts:tests python -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=. python shared/book_qa.py
PYTHONPATH=. python shared/project_quality_gate.py
```

Unified Ingest Engine testleri ve kanonik corpus doğrulaması:

```bash
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/ingest -p 'test_*.py'
.venv/bin/python scripts/verify_canonical_baseline.py
```

Tam üretim crawl'u ve 2950 soruluk tam LLM değerlendirmesi bu migrasyon kapsamında çalıştırılmamıştır. Güncel karar ve istisnalar için `audit/corpus_quality_gate.json` ile `reports/` altındaki V1 raporları esas alınır.
