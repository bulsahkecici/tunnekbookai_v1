# TunnelBookAI Native macOS Environment Test Audit

- Audit tarihi: **2026-08-16** (Europe/Istanbul)
- Proje: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`
- Kapsam: yalnız native environment test/preflight
- Karar: **GO**

## Native interpreter

- Python executable: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI/.venv/bin/python`
- Python version: **3.12.14**
- Architecture: **arm64**
- Platform: `macOS-26.5.2-arm64-arm-64bit`
- Virtualenv: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI/.venv`
- Native site-packages: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI/.venv/lib/python3.12/site-packages`
- Windows `Lib/site-packages` sys.path girdisi: **0**
- Windows absolute sys.path girdisi: **0**

Aktivasyon kontrolü:

```text
$ source .venv/bin/activate
$ which python
/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI/.venv/bin/python
$ python --version
Python 3.12.14
```

## Test commands and results

### Main suite

```bash
source .venv/bin/activate
python -m unittest discover -s tests -v
```

- Çalıştırılan: **51**
- PASS: **51**
- FAIL/ERROR/SKIP: **0/0/0**
- Sonuç: **PASS**

### Rapor / Colab preflight suite

```bash
source .venv/bin/activate
python -m unittest discover -s rapor/tests -v
```

- Çalıştırılan: **16**
- PASS: **16**
- FAIL/ERROR/SKIP: **0/0/0**
- Sonuç: **PASS**

Test çıktısındaki kasıtlı conversion failure/retry mesajları fixture senaryolarına aittir; unittest suite sonucu `OK` ve exit code `0`'dır. Ağır Docling conversion veya Colab runtime başlatılmadı.

### Toplam

- Test: **67**
- PASS: **67**
- FAIL/ERROR/SKIP: **0/0/0**
- Genel sonuç: **PASS**

## Additional test command discovery

- `pytest.ini`: bulunmadı
- `pyproject.toml`: bulunmadı
- `tox.ini`: bulunmadı
- `noxfile.py`: bulunmadı
- `setup.cfg`: bulunmadı
- Proje-local pytest command/config: bulunmadı
- Tanımlı test runner: Python standard-library `unittest`

Bu nedenle iki mevcut unittest discovery komutu gerekli ve uygun test kapsamıdır.

## Targeted portability and integrity preflight

### Runtime paths

- `source_root`: `/Users/bulsahkecici/Projects/tunnel`
- `project_root`: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`
- `TUNNEL_ROOT` override testi: **PASS**
- Relative/pathlib çözümleme testleri: **PASS**
- Colab identity'nin Windows absolute path'ten bağımsızlığı: **PASS**
- Aktif config/scripts/notebook içinde eski `C:\Users\bulsa\OneDrive\Desktop\tunnel` runtime root kullanımı: **0**

Historical inventory/manifest/report Windows path alanları provenance kabul edildi ve aktif runtime path sayılmadı.

### Windows process/executable isolation

- Non-Windows `active_office_processes()`: `[]`
- macOS'ta `tasklist` çağrısı: yapılmadı
- Windows Portable/`.exe` LibreOffice seçimi: yapılmadı
- Windows LibreOffice selection regresyon testi: **PASS**
- Windows `.venv/Lib/site-packages` injection: yapılmadı

### LibreOffice graceful handling

- Native LibreOffice discovery: `None`
- LibreOffice bulunmaması import/test akışını bozmadı.
- Recovery route testleri: **PASS**
- Seviye: **WARNING**, blocker değil.

### Final corpus integrity

- Final manifest rows: **214**
- Physical final Markdown: **214**
- Unique `document_id`: **214**
- Duplicate `document_id`: **0**
- Full Docling / baseline: **138 / 76**
- Final corpus unit/integrity tests: **PASS**

### Metadata master integrity

- Rows: **214**
- Unique `document_id`: **214**
- Missing source SHA: **0**
- Current metadata preservation tests: **PASS**
- Deterministic human-review queue test: **PASS**

### Full Docling manifest / sidecar integrity

- Citation sidecar references: **361**
- Missing sidecar: **0**
- Invalid sidecar JSON: **0**
- Original-page/page-map tests: **PASS**
- SHA identity mismatch rejection: **PASS**

### Snapshot / transient policy

- Historical snapshot rows: **309**
- Ignored transient rows: **10**
- Content source rows: **299**
- Missing content source: **0**
- Content SHA mismatch: **0**
- Snapshot digest tests: **PASS**
- macOS non-Windows Office process guard: **PASS**

Transient patterns: `desktop.ini`, `Thumbs.db`, `~$*`; Mac-only `.DS_Store` da non-content extra kabul edilir.

### DOC000239 canonical repair

- Literal canonical source path exists: **true**
- Canonical path: `TÜNEL MÜH.GELİŞTİRME KURSU - (24-28.02.2020)/DOKÜMANLAR/ROCKBİT-3.5''9m-ANALİZ.pdf`
- Source SHA equals manifest SHA: **true**
- Migrated-filename identity resolver regression test: **PASS**

## Dependency status

- Dependency fix during this test turn: **yok**
- Native venv dependency source: `requirements.txt`
- `pypdf` native venv içinde mevcut; Windows site-packages fallback gerekmedi.
- Missing test dependency: **0**
- `pip check`: **PASS**, broken requirement yok.

## Protected data

Değiştirilmedi:

- `data/corpus_final/`
- `data/markdown/`
- `data/markdown_full_docling/`
- `data/metadata/final_corpus_manifest.csv`
- `data/metadata/final_metadata_master.csv`
- citation sidecar içerikleri
- historical snapshot artefact'ları

Metadata LLM, LM Studio inference, GPU inference, Docling heavy conversion, normalization, chunking, embedding, Qdrant ve RAG çalıştırılmadı.

## Warnings

- Native LibreOffice bulunamadı; graceful handling doğrulandı ve testleri engellemedi.
- Project-local pytest konfigürasyonu yok; yalnız tanımlı unittest suite'leri çalıştırıldı.
- Rapor suite'indeki beklenen fixture failure mesajları test edilen retry/fallback davranışıdır; gerçek test hatası değildir.

## Blockers

**Yok.**

## Final decision

**GO**
