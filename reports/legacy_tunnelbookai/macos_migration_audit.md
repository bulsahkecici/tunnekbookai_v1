# TunnelBookAI macOS Migration Integrity / Preflight Audit

- Audit tarihi: **2026-08-16** (Europe/Istanbul)
- Runtime root: `/Users/bulsahkecici/Projects/tunnel`
- Proje: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`
- Kapsam: migration integrity, path portability, runtime ve test preflight
- Çalıştırılmayan işlemler: metadata LLM, normalization, chunking, embedding, Qdrant, RAG, inference ve ağır Docling

## Sonuç

**GO**

Transient Windows artefact'ları içerik kaynağı sayılmadan yapılan karşılaştırmada gerçek source corpus Windows snapshot ile tam eşleşiyor. Canonical 214 kaynak literal path ve SHA düzeyinde doğrulandı. Final corpus, variant seçimi, provenance, metadata master ve tüm testler geçti.

## Gate özeti

| Kontrol | Sonuç | Durum |
|---|---:|---|
| Historical snapshot total | 309 | INFO |
| Content source total | 299 | PASS |
| Missing content source | 0 | PASS |
| Content source SHA mismatch | 0 | PASS |
| Extra content source | 0 | PASS |
| Canonical source literal path | 214/214 | PASS |
| Canonical source SHA | 214/214 | PASS |
| Final Markdown | 214/214 | PASS |
| Unique `document_id` | 214 | PASS |
| Empty final output | 0 | PASS |
| Duplicate final path | 0 | PASS |
| Full Docling / baseline | 138 / 76 | PASS |
| Selected variant content match | 214/214 | PASS |
| Sidecar missing / invalid | 0 / 0 | PASS |
| Metadata master | 214 | PASS |
| Tests | 67/67 | PASS |

## Transient exclusion policy

Migration source-integrity karşılaştırması aşağıdaki filename pattern'larını non-content, OS/temporary artefact olarak sınıflandırır:

- `desktop.ini` — Windows Explorer metadata
- `Thumbs.db` — Windows thumbnail cache
- `~$*` — Microsoft Office temporary/lock files
- `.DS_Store` — macOS Finder metadata; yalnız Mac tarafındaki extra-file karşılaştırmasından çıkarılır

Policy yalnız filename bazlıdır. Bu pattern'lara uymayan her gerçek kaynak için relative path ve SHA256 eşleşmesi zorunludur; gerçek belge farkı hâlâ blocker üretir.

- `historical_snapshot_total`: **309**
- `ignored_transient_count`: **10**
- `content_source_total`: **299**
- Mac source total (`_TunnelBookAI` hariç, transient dahil): **311**
- Mac ignored transient: **12** (`7 .DS_Store` + snapshot'ta da bulunan `5 Thumbs.db`)
- Mac content source total: **299**
- Missing content source: **0**
- Content source SHA mismatch: **0**
- Extra content source: **0**

### ignored_transient_paths

Historical snapshot'tan çıkarılan 10 kayıt:

1. `Mehmet/Kitap 2.Bolum/~$neller Bolum2_9_7_2025.docx`
2. `Mehmet/Literatur/Thumbs.db`
3. `Mehmet/Literatur/YTMK Tunelcilik Semineri/2013/Thumbs.db`
4. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/TAKİP FORMU/desktop.ini`
5. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/Tünelde Özel Çözümler/Thumbs.db`
6. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/yapim_isleri_ihaleleri_uygulama_yonetmeligi_degisiklikler_islenmis/~$ Yapım Genel Partname.docx`
7. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/~$rim Fiyat Tarifleri (Genel Müdürlük)-TÜNEL (2).doc`
8. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/~$rim Fiyat Tarifleri (Genel Müdürlük)-TÜNEL.doc`
9. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/Thumbs.db`
10. `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/Tünelde Özel Çözümler/Thumbs.db`

Snapshot'ta bulunup Mac'te bulunmayan transient kayıt sayısı **5**: dört `~$*` Office lock dosyası ve bir `desktop.ini`. Bunların eksikliği INFO/WARNING'dir, source-integrity failure değildir. Beş `Thumbs.db` iki tarafta da mevcuttur fakat policy gereği content source sayılmaz.

Historical `data/inventory/source_snapshot.json` ve snapshot CSV/JSONL dosyaları değiştirilmedi; yeni snapshot üretilmedi.

## DOC000239 canonical path repair

Manifest canonical source yolu:

`TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/ROCKBİT-3.5''9m-ANALİZ.pdf`

Migration sonrası eski Mac adı:

`TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/ROCKBİT-3.5_9m-ANALİZ.pdf`

Kaynak dosya `pathlib`/`os.rename` ile exact canonical filename'e yeniden adlandırıldı. Rename önkoşulları:

- Canonical hedef mevcut değildi.
- Manifest SHA ile eşleşen kaynak adayı tam bir taneydi.
- Boyut: **46111 byte**.

SHA kanıtı:

- `SHA_before`: `07c7ec20474708b9db495ec7cb6ac067587cf421cfc6347555cdefd4ced57044`
- `SHA_after`: `07c7ec20474708b9db495ec7cb6ac067587cf421cfc6347555cdefd4ced57044`
- Manifest `source_sha256`: `07c7ec20474708b9db495ec7cb6ac067587cf421cfc6347555cdefd4ced57044`
- `SHA_before == SHA_after == manifest source_sha256`: **true**
- `DOC000239` canonical literal source path match: **true**

Dosya içeriği değiştirilmedi. `final_corpus_manifest.csv` ve diğer manifestler değiştirilmedi.

Protected `data/markdown/` ve `data/corpus_final/` ağaçlarındaki migration-sanitized Markdown adı değiştirilmedi. Bu artefact benzersiz front-matter `document_id=DOC000239` ile güvenli biçimde çözülüyor; baseline ve final SHA256 değeri aynıdır: `4d3eb9e8043029254140abfafc3f08d03a54df34d69b05d33908a3b7b4d8837b`.

## Source integrity

Transient exclusion sonrası historical ve Mac content source kümeleri:

- Path eşleşmesi: **299/299**
- SHA256 eşleşmesi: **299/299**
- Missing content source: **0**
- Extra content source: **0**
- Hash error: **0**
- Canonical source literal path: **214/214**
- Canonical source SHA: **214/214**
- Canonical source SHA relation problemi: **0**

Mac filesystem `ctime`/`mtime` değerleri publication metadata olarak kullanılmadı.

## Final corpus integrity

`data/corpus_final/`:

- Markdown: **214**
- Non-Markdown: **0**
- Unique `document_id`: **214**
- Duplicate `document_id`: **0**
- Empty output: **0**
- Duplicate final path: **0**
- Duplicate canonical source SHA: **0**
- Duplicate final content SHA: **0**
- Unresolved final output: **0**
- Selected variant ile byte-for-byte eşleşme: **214/214**

Final corpus içeriği değiştirilmedi.

## Variant integrity

`data/metadata/final_corpus_manifest.csv`:

- Satır: **214**
- `full_docling`: **138**
- `baseline`: **76**
- Toplam: **214**
- Selected variant content match: **214/214**
- Source snapshot / conversion / metadata master SHA relation problemi: **0**

## Docling sidecar / provenance

- Full Docling seçilmiş belge: **138**
- Citation sidecar referansı bulunan belge: **138**
- Toplam sidecar referansı: **361**
- Missing sidecar: **0**
- Invalid sidecar JSON: **0**
- Windows absolute sidecar referansı: **0**
- `original_page_provenance_available=true`: **88**
- `original_page_provenance_available=false`: **50**

88/50 dağılımı historical final audit ile aynıdır. Citation sidecar içerikleri değiştirilmedi veya yeniden üretilmedi.

## Metadata master

`data/metadata/final_metadata_master.csv`:

- Satır: **214**
- Unique `document_id`: **214**
- Duplicate `document_id`: **0**
- Missing `source_sha256`: **0**
- Final manifest ile `document_id` kümesi eşit: **true**
- Final manifest SHA uyuşmazlığı: **0**

Current/suggested metadata değiştirilmedi. Metadata LLM çalıştırılmadı.

## Path portability

Aktif runtime:

- `source_root`: `/Users/bulsahkecici/Projects/tunnel`
- `project_root`: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`
- `TUNNEL_ROOT=~/Projects/tunnel` destekleniyor.
- Config'te aktif Windows absolute runtime root yok.
- Relative yollar `pathlib.Path` ile çözülüyor.
- Windows LibreOffice `.exe`/Portable adayları yalnız Windows dalında değerlendiriliyor.
- `tasklist` tabanlı Office process kontrolü yalnız Windows'ta çalışıyor.
- Colab Python/notebook kodunda Windows absolute çalışma root'u yok.
- Windows path test fixture'ları aktif filesystem erişimi değildir.
- Historical inventory/manifest/report absolute path alanları provenance olarak korundu.

## Mac runtime

- OS: **macOS 26.5.2**, build `25F84`
- Architecture: **arm64**
- CPU: **Apple M5 Max**
- Apple Silicon: **doğrulandı**
- System Python: **3.14.6**
- pip: **26.1.2**, Homebrew Python 3.14
- Project venv: `.venv/bin/python` yok; taşınmış venv Windows Python 3.12.13 artefact'ıdır ve macOS'ta çalışmaz.
- Native LibreOffice: **bulunamadı**.
- Taşınmış Windows LibreOffice Portable macOS executable olarak seçilmiyor.
- Ağır Docling çalıştırılmadı.

## LM Studio connectivity

- Endpoint: `http://127.0.0.1:1234/v1/models`
- Sonuç: bağlantı kurulamadı (`curl` exit 7, HTTP 000).
- Model adı raporlanamadı.
- Seviye: **WARNING**, blocker değil.
- Inference çağrısı yapılmadı.

## Tests

- `python3 -m unittest discover -s tests -v`: **51/51 PASS**
- `PYTHONPATH=.venv/Lib/site-packages python3 -m unittest discover -s rapor/tests -v`: **16/16 PASS**
- Toplam: **67/67 PASS**

İkinci komutta yalnız taşınmış saf-Python `pypdf` paketi test sürecine eklendi. Bu, Windows venv'i geçerli macOS venv'i yapmaz ve hiçbir Docling/inference işlemi başlatmaz.

## Changed files / operations

Bu blocker-resolution turu:

- Kaynak `DOC000239` dosyası canonical filename'e yeniden adlandırıldı; içerik SHA değişmedi.
- `reports/macos_migration_audit.md` güncellendi.

Audit kapsamında daha önce yapılmış portability düzeltmeleri:

- `config/config.yaml`
- `scripts/utils.py`
- `scripts/07_snapshot.py`
- `scripts/09_metadata_enrichment.py`
- `tests/test_inventory.py`
- `tests/test_snapshot.py`
- `tests/test_metadata_enrichment.py`

Değiştirilmeyen korumalı artefact'lar:

- `data/corpus_final/`
- `data/markdown/`
- `data/markdown_full_docling/`
- `data/metadata/final_corpus_manifest.csv`
- `data/metadata/final_metadata_master.csv`
- citation sidecar içerikleri
- historical `data/inventory/source_snapshot.json` ve diğer snapshot artefact'ları

Yeni snapshot üretilmedi.

## Warnings / info

- Historical snapshot'taki dört Office lock dosyası ve bir `desktop.ini` Mac'te yok; transient policy kapsamında non-content INFO'dur.
- Yedi Mac `.DS_Store` dosyası non-content extra olarak yok sayıldı.
- LM Studio server erişilemiyor; blocker değil.
- Native macOS LibreOffice bulunamadı.
- Project `.venv` Windows'a ait; ileride gerçek macOS venv oluşturulmalı.
- 50 Full Docling belgede original-page provenance yok; historical durumla aynı ve sidecar kaybı bulunmuyor.

## Blockers

**Yok.**

## Gate

**GO**
