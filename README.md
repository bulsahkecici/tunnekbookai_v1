# TunnelBookAI V1

PaperCrawler kaynakları keşfeder ve güvenli bir schema-2.x Source Pack üretir. TunnelBookAI,
kullanıcının sağladığı veya PaperCrawler’dan gelen kaynakları tek Unified Ingest hattından
geçirerek işler, sınıflandırır, parçalar ve kitap üretiminde kullanılabilir
doğrulanmış bir corpus oluşturur.

PaperCrawler source-oriented’dır. TunnelBookAI book- and knowledge-oriented’dır.

## Authoritative input channels

- `incoming/manual/inbox/`
- `incoming/papercrawler/releases/`

Her iki kanal aynı hattı izler: immutable originals → structural extraction → metadata and
provenance → TunnelBookAI final classification → chunking → staging. Canonical promotion
ayrı bir komuttur ve varsayılanı dry-run’dır; ingest doğrudan canonical corpus’a yazmaz.

Manuel keşfin tek varsayılan kökü tam olarak `incoming/manual/inbox/` dizinidir. Bunun
üstündeki veya yanındaki dosyalar, gizli yollar, sembolik bağlar ve geçici Office dosyaları
işleme adayı değildir.

## Corpus Population V1

`tunnelbookai.population`, iki giriş kanalının deterministik envanterini çıkarır, tek-yazarlı
ingest batch'leri üretir, her belge sonrasında koşu durumunu atomik olarak kaydeder ve ancak
bütün seçili girdiler açıklanmışsa staging audit oluşturur. Bu kontrol katmanı mevcut
extractor, classifier, chunker veya canonical otoritesinin yerini almaz.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population inventory --json
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population plan-batches \
  --inventory audit/corpus_population/inventories/CPI_<exact-id>.json --json
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population run-batch \
  --batch audit/corpus_population/batches/CPB_<exact-id>.json --resume --json
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population staging-audit \
  --run audit/corpus_population/runs/CPR_<exact-id>.json --json
```

Population hiçbir zaman canonical apply çağırmaz. Audit'in ürettiği `CPP_` seçici yalnızca
belge kimliklerini taşır; `tunnelbookai.canonical` bütün uygunluk kontrollerini yeniden yapar
ve her `CCP_` planı için operatörün aynı kimlikle açık onayını ister. Normatif sözleşme:
`docs/corpus_population_contract.md`.

## Empty-corpus bootstrap

Yeni bir kurulumda corpus, chunks, embeddings ve vectors sıfır olabilir. Bu durum hata
değildir; önce kaynaklar iki yetkili input kanalından alınır. Model servisleri opsiyonel
olarak loopback’te çalışır. Servis kapalıysa sistem başka model seçmez ve
`MODEL_SERVICE_UNAVAILABLE` raporlar.

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py --source manual --dry-run
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py --source papercrawler --dry-run
PYTHONPATH=. .venv/bin/python scripts/probe_models.py
PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py --mode isolation
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

## Book Production Engine V1 foundation

TunnelBookAI bir sohbet uygulaması değil, kaynak-temelli teknik kitap üretim sistemidir.
`book/config/book_contract.json`; dondurulmuş kapsamı, 2.950 soruluk kalite sözleşmesini,
kanıt sınırını ve yayın kapılarını tek yerde tanımlar. `config/models.yaml` kesin model
adları için tek otorite olmaya devam eder.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book validate
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book status
```

Yayın için 2.950 sorunun tamamı denetlenmeli; yalnızca `ANSWERED` sayılır ve hem en az
1.770 cevap hem de en az `%60` global kapsama ulaşılmalıdır. `PARTIAL` kapsama eklenmez.
Canonical dışındaki ingest, processing, staging, archive veya internet içeriği kitap
kanıtı değildir. Foundation sonrasındaki üretim aşamaları henüz `NOT_IMPLEMENTED`
döndürür; boş canonical corpus üzerinden metin üretilmez. Ayrıntılar için
`docs/book_production_engine.md` belgesine bakın.

## Controlled canonical promotion

Canonical admission is owned only by `tunnelbookai.canonical`. Planning verifies the
immutable original, processing/staging agreement, metadata, provenance, final
classification, quality decisions, ingest ledgers and every chunk identity. It writes a
deterministic audit plan but does not change canonical evidence.

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical status
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical plan --document-id ING_...
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical apply \
  --plan audit/canonical_promotions/plans/CCP_....json --approve CCP_...
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical verify
```

Apply is bound to the exact plan identity and rejects stale inputs. It copies verified
book evidence into content-addressed canonical objects, retains staging, processing and
originals, and commits the complete document set through one atomic manifest replacement.
See `docs/canonical_promotion_contract.md`.

The empty-reset gate is historical/bootstrap validation and is expected to return
`NO_GO` after legitimate ingest data exists. Use `--mode isolation` for active repository
architecture checks and canonical `verify` for the production evidence gate.
