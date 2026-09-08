# TunnelBookAI V1

PaperCrawler kaynakları keşfeder ve güvenli bir schema-2.x Source Pack üretir. TunnelBookAI,
kullanıcının sağladığı veya PaperCrawler’dan gelen kaynakları tek Unified Ingest hattından
geçirerek işler, sınıflandırır, parçalar, indeksler ve kitap üretiminde kullanılabilir
doğrulanmış bir corpus oluşturur.

PaperCrawler source-oriented’dır. TunnelBookAI book- and knowledge-oriented’dır.

## Authoritative input channels

- `incoming/manual/inbox/`
- `incoming/papercrawler/releases/`

Her iki kanal aynı hattı izler: immutable originals → structural extraction → metadata and
provenance → TunnelBookAI final classification → chunking → staging. Canonical promotion
ayrı bir komuttur ve varsayılanı dry-run’dır; ingest doğrudan canonical corpus’a yazmaz.

## Empty-corpus bootstrap

Yeni bir kurulumda corpus, chunks, embeddings ve vectors sıfır olabilir. Bu durum hata
değildir; önce kaynaklar iki yetkili input kanalından alınır. Model servisleri opsiyonel
olarak loopback’te çalışır. Servis kapalıysa sistem başka model seçmez ve
`MODEL_SERVICE_UNAVAILABLE` raporlar.

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py --source manual --dry-run
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py --source papercrawler --dry-run
PYTHONPATH=. .venv/bin/python scripts/probe_models.py
PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py
```

The repository-level `scripts/` directory contains only supported post-reset operator
commands. Historical pipeline scripts are isolated under `archive/legacy_pre_reset/` and
must not be used against the current layout.

Model adlarının tek otoritesi `config/models.yaml`’dır. CLI override sırası:
`--embedding-model` / `--llm-model` > `config/models.yaml` > açık hata veya unavailable.
Uzak endpoint, bulut fallback’i ve rastgele model seçimi kabul edilmez.

PDF, DOCX, PPTX, XLSX, image, OCR fallback, LibreOffice snapshots, table/figure extraction,
Turkish text folding, provenance, global dedup, quality gates ve structure-aware chunking
Unified Ingest’in korunan yetenekleridir. Docling AI chart extraction devre dışıdır.
