# TunnelBookAI Terminal Komutları Rehberi

Bu belge, TunnelBookAI V1'in güncel ve desteklenen terminal komutlarını, her komutun ne
yaptığını, hangi dosyaları etkilediğini ve önemli güvenlik notlarını tek yerde toplar.
Komutlar proje kökünden çalıştırılmalıdır:

```bash
cd /Users/bulsahkecici/Projects/tunnelbookai_v1
```

## 1. Kullanılan gösterimler

| Gösterim | Anlamı |
| --- | --- |
| `ING_...` | İçeriğin SHA-256 kimliğinden türetilmiş belge kimliği |
| `CPI_...json` | Population envanteri |
| `CPB_...json` | Deterministik ingest batch'i |
| `CPR_...json` | Population koşusu ve checkpoint kaydı |
| `CSA_...json` | Staging audit sonucu |
| `CPP_...json` | Canonical promotion için belge seçici |
| `CCP_...json` | Canonical dry-run planı |
| `<PID>` | Çalışan bir işletim sistemi sürecinin numarası |
| `<exact-id>` | Komut çıktısında gerçekten üretilen tam kimlik; metin aynen değiştirilir |

Komutların başındaki `PYTHONPATH=.` proje paketlerinin doğrudan bu çalışma ağacından
yüklenmesini sağlar. `.venv/bin/python` ise yanlış Python veya yanlış bağımlılık ortamının
kullanılmasını önler.

## 2. İlk kurulum ve bağımlılıklar

### Python sanal ortamını oluşturma

```bash
python3.12 -m venv .venv
```

Proje kökünde Python 3.12 tabanlı izole bir ortam oluşturur. Bu işlem normalde yalnızca ilk
kurulumda yapılır; mevcut `.venv` üzerine tekrar uygulanmaz.

### Python bağımlılıklarını kurma

```bash
.venv/bin/python -m pip install -r requirements-ingest.lock
```

Docling, OCR, Office belge işleme, vektör ve diğer Python bağımlılıklarını kilit dosyasındaki
sürümlerle kurar.

### Dashboard test bağımlılıklarını kurma

```bash
npm ci
npx playwright install chromium
```

`npm ci`, `package-lock.json` ile birebir Node bağımlılığı kurar. İkinci komut Playwright'ın
Chromium tarayıcısını kurar. Bunlar dashboard'u normal kullanmak için değil, E2E tarayıcı
testleri için gereklidir.

### Python ve Node sürümlerini kontrol etme

```bash
.venv/bin/python --version
node --version
npm --version
```

Kurulumun hangi yorumlayıcılarla çalıştığını gösterir; hiçbir proje verisini değiştirmez.

### LibreOffice erişimini kontrol etme

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --version
```

macOS'ta DOCX, PPT/PPTX ve XLS/XLSX sayfa görselleri için kullanılan LibreOffice'ın erişilir
olduğunu doğrular. LibreOffice yoksa yapısal çıkarım devam edebilir fakat görsel snapshot
üretimi uyarı verebilir.

## 3. Yerel model servisi

Model adlarının otoritesi `config/models.yaml` dosyasıdır. Güncel varsayılanlar:

- embedding: `text-embedding-baai-bge-m3-568m`;
- LLM: `qwen/qwen3.8-27b`;
- OpenAI uyumlu yerel endpoint: `http://127.0.0.1:1234/v1`.

LM Studio içinde iki modelin de yüklü ve yerel sunucunun başlatılmış olması gerekir. Sistem
uzak sunucuya veya başka modele otomatik geçmez.

### Model yeteneklerini doğrulama

```bash
PYTHONPATH=. .venv/bin/python scripts/probe_models.py
```

Embedding modeline gerçek bir vektör isteği, Qwen'e de yapılandırılmış yanıt isteği gönderir.
Her iki model doğruysa `AVAILABLE` ve sıfır çıkış kodu verir. Servis kapalıysa
`MODEL_SERVICE_UNAVAILABLE` ve çıkış kodu `2` üretir. Bu script'in `--help` seçeneği yoktur;
çalıştırıldığında doğrudan modeli test eder.

### LM Studio model listesini ham API üzerinden görme

```bash
curl -fsS http://127.0.0.1:1234/v1/models
```

Yerel OpenAI uyumlu servisin erişilebilirliğini ve yüklediği model adlarını gösterir. Sadece
okuma isteğidir.

## 4. Unified Ingest komutları

Unified Ingest'in aktif giriş noktası `scripts/ingest_incoming.py` dosyasıdır. Doğrudan
`python -m tunnelbookai.ingest` kullanılmaz; paketin bir `__main__` girişi yoktur.

### Yardım ekranı

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py --help
```

Desteklenen bütün ingest parametrelerini listeler ve veri değiştirmez.

### Manuel kaynakları yalnızca keşfetme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source manual --dry-run
```

Yalnızca `incoming/manual/inbox/` altındaki uygun dosyaları envanterler; extraction veya
staging yapmaz.

### PaperCrawler kaynaklarını yalnızca keşfetme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source papercrawler --dry-run
```

`incoming/papercrawler/releases/` altındaki şema-2.x release paketlerini doğrular ve adayları
gösterir; dosya işlemez.

### Her iki giriş kanalını işleme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source all --resume
```

Manuel ve PaperCrawler girdilerini immutable original, extraction, metadata, classification,
quality gate, chunking ve staging aşamalarından geçirir. `--resume`, terminal artifact'leri
tam olan belgeleri yeniden işlememeyi sağlar. Ingest doğrudan canonical corpus'a yazmaz.

### Tek bir belgeyi işleme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source all --document-id ING_... --resume
```

Koşuyu tek belge kimliğiyle sınırlar. Sorunlu bir belgeyi kontrollü yeniden denemek için
kullanılır.

### Tek bir PaperCrawler release'ini işleme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source papercrawler --release RELEASE_DIZINI --resume
```

Keşfi yalnızca verilen release klasörüyle sınırlar.

### Küçük pilot koşusu

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source manual --max-documents 5 --resume
```

En fazla beş belge işler. Yeni yapılandırma veya model değişikliğini corpus geneline
uygulamadan önce denemek için kullanılır.

### Kontrollü yeniden işleme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --document-id ING_... --force-reprocess --from-stage EXTRACTING
```

Belgenin türetilmiş çıktılarını belirtilen aşamadan başlayarak yeniden kurar. Immutable
original dosyayı değiştirmez. `--force-reprocess` pahalı olabilir ve eski staging auditleri
ile canonical planlarını geçersiz kılabilir; yalnızca belirli bir düzeltme sonrası kullanılır.

Extraction sonrasında Türkçe glyph aralığı onarımı otomatik çalışır: `TEKN İ K`,
`k ı salmas ı` gibi bozuk metin katmanları `config/turkish_lexicon.txt` ve belge içi
kanıtla onarılır; sonuç `extraction_report.json` içinde `text_repair` ve
`TURKISH_GLYPH_SPACING_REPAIRED:<sayı>` uyarısıyla kaydedilir. Bozuk olmayan belgelere
dokunulmaz. Onarım yalnızca yeniden işlenen belgelere uygulanır; canonical'daki mevcut
belgeler `--force-reprocess --from-stage EXTRACTING` ile yeniden işlenip yeniden promote
edilmeden değişmez.

### Canonical belgeleri immutable orijinalden yeniden işleme

```bash
PYTHONPATH=. .venv/bin/python scripts/ingest_incoming.py \
  --source manual --reprocess-canonical ING_... ING_... --resume
```

Inbox temizlenmiş olsa bile verilen belgeleri `originals/<id>/source.*` üzerinden yeniden
işler; kayıtlı provenance kaynağı yeni kaynak eklemeden tazelenir. `--force-reprocess`
ima edilir; canonical yalnızca sonraki onaylı `canonical plan/apply` ile (`REPLACE`
eylemi) değişir. Figür açıklamaları için LM Studio'da bir VLM yüklü olmalıdır; yüklü
değilse figür chunk'ları `NOT_RUN` ile yeniden üretilir (otomatik seçim artık VLM olmayan
bir modele düşmez).

### Ingest seçeneklerinin anlamı

| Seçenek | Etki |
| --- | --- |
| `--source manual\|papercrawler\|all` | Yetkili giriş kanalını seçer |
| `--dry-run` | Sadece keşif yapar |
| `--resume` | Tamamlanmış aşamaları ve belgeleri tekrar etmez |
| `--force-reprocess` | Türetilmiş çıktıları yeniden üretir |
| `--document-id ING_...` | Tek belgeye sınırlar |
| `--release NAME` | Tek PaperCrawler release'ine sınırlar |
| `--max-documents N` | İşlenecek belge sayısını sınırlar |
| `--no-ocr` | OCR'ı kapatır; native metin extraction devam eder |
| `--no-vision` | Figure görsel açıklamasını kapatır |
| `--no-chunking` | Staging sonrasında durur, chunk üretmez |
| `--no-arbiter` | Belirsiz bölüm eşlemesinde yerel Qwen arbiter'ını çağırmaz |
| `--embedding-server/--embedding-model` | Bu koşu için embedding endpoint/model override eder |
| `--llm-server/--llm-model` | Bu koşu için LLM endpoint/model override eder |
| `--from-stage STATE` | O aşamaya ulaşmış belgeleri yeniden işleme kapsamına alır |
| `--reprocess-canonical ING_...` | Canonical belgeleri immutable orijinalden yeniden işler (`--force-reprocess` ima eder) |

Model override seçenekleri yalnızca açık ve bilinçli testlerde kullanılmalıdır; normal
işletimde `config/models.yaml` otorite olarak bırakılır.

## 5. Corpus Population iş akışı

Population, iki giriş kanalının deterministik envanterini ve batch'lerini yönetir. Tek yazarlı
çalışır, her belge sonrasında atomik checkpoint yazar ve canonical apply çağırmaz.

### Komut listesini görme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population --help
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population run-batch --help
```

İlk komut alt komutları, ikinci komut ilgili seçenekleri gösterir.

### Dış bir klasörden güvenli manuel import planı oluşturma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population manual-import-plan \
  --from /MUTLAK/KAYNAK/KLASORU --json
```

Harici klasörü değiştirmeden tarar ve `CMI_...` import planı oluşturur. Sembolik bağları
izlemez; çakışan hedefleri otomatik yeniden adlandırmaz.

### Manuel import planını uygulama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population manual-import-apply \
  --from /MUTLAK/KAYNAK/KLASORU \
  --plan audit/corpus_population/manual_imports/CMI_....json \
  --approve CMI_... --json
```

Planı ve kaynak SHA-256 değerlerini yeniden doğrular, ardından dosyaları
`incoming/manual/inbox/` altına atomik olarak kopyalar. `--approve` değeri plan içindeki tam
kimlikle aynı olmalıdır. Aynı yolda farklı içerik varsa `PATH_COLLISION` ile durur.

### Giriş envanteri oluşturma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population inventory --json
```

Manual ve PaperCrawler kaynaklarını içerik kimliğine göre gruplar; `NEW`,
`ALREADY_CANONICAL`, `REUSABLE_COMPLETE`, `RECOVERY_REQUIRED` ve `UNSUPPORTED` durumlarını
hesaplar. Çıktı `audit/corpus_population/inventories/CPI_....json` altına yazılır.

### Batch planlarını oluşturma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population plan-batches \
  --inventory audit/corpus_population/inventories/CPI_....json --json
```

Tam envanter kimliğine bağlı, kaynak türü ve tahmini maliyete göre sıralanmış `CPB_...`
batch'leri ile bir `CPR_...` koşusu oluşturur. Henüz belge işlemez.

### Batch çalıştırma veya devam ettirme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population run-batch \
  --batch audit/corpus_population/batches/CPB_....json \
  --resume --json
```

Batch'i sırayla işler. `--resume`, tamamlanan belgeleri tekrar üretmez; kesilmiş veya eksik
artifact'li belgeyi güvenli noktadan yeniden başlatır.

### Batch'i kooperatif durdurma dosyasıyla çalıştırma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population run-batch \
  --batch audit/corpus_population/batches/CPB_....json \
  --resume --stop-file audit/dashboard/stop.request --json
```

Verilen stop dosyası mevcut olduğunda aktif belgeyi tamamlar, checkpoint yazar ve sonraki
belgeye geçmeden `PAUSED` olur. Dosyayı elle oluşturmak yerine normalde dashboard'daki
“Güvenli durdur” düğmesi kullanılmalıdır.

### Population koşu durumunu görme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population status \
  --run audit/corpus_population/runs/CPR_....json --json
```

Koşu, batch ve belge sayaçlarını salt okunur biçimde gösterir.

### Staging auditi üretme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population staging-audit \
  --run audit/corpus_population/runs/CPR_....json --json
```

Koşu `INGEST_ACCOUNTED` durumuna geldikten sonra bütün seçili girdilerin açıklanıp
açıklanmadığını, kaliteyi, chunkları ve canonical adaylarını yeniden denetler. `CSA_...`
audit'i ve en fazla 25 belgeli `CPP_...` promotion seçicileri oluşturabilir.

### Canonical sonrası readiness raporu

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population readiness \
  --run audit/corpus_population/runs/CPR_....json --json
```

Seçilen her kimliğin terminal disposition'a sahip olduğunu ve gerekli belgelerin doğrulanmış
canonical manifestte bulunduğunu kontrol eder.

### Bir belge için gerekçeli exclusion kaydetme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.population account-exclusion \
  --run audit/corpus_population/runs/CPR_....json \
  --document-id ING_... \
  --reason "İnsan incelemesi: desteklenmeyen format" --json
```

Çözülemeyen bir belge için operatör gerekçesi kaydeder. Belgenin kalite kararını değiştirmez
ve onu canonical'a uygun hale getirmez; yalnızca koşu muhasebesini açıklanabilir kılar.

### Population `run-batch` seçenekleri

| Seçenek | Etki |
| --- | --- |
| `--resume` | Tam artifact'li terminal belgeleri atlar |
| `--force-reprocess` | Seçili batch'te türetilmiş çıktıları yeniden kurar |
| `--no-vision` | Figure görsel açıklamalarını kapatır |
| `--no-ocr` | OCR'ı kapatır |
| `--no-arbiter` | Yerel Qwen bölüm arbiter'ını kapatır |
| `--stop-file PATH` | Belge sınırında güvenli pause sağlar |
| `--json` | Makine tarafından okunabilir JSON çıktı verir |

## 6. Dashboard'u çalıştırma

Dashboard yalnızca `127.0.0.1` loopback üzerinde çalışır; dış ağa açılmaz.

### En yeni population koşusuyla varsayılan portta başlatma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.dashboard
```

En yeni geçerli `CPR_...` koşusunu seçer ve `http://127.0.0.1:8765` adresinde foreground
olarak çalışır.

### Belirli koşu ve portla başlatma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.dashboard \
  --host 127.0.0.1 --port 18765 \
  --run audit/corpus_population/runs/CPR_....json
```

Dashboard'u bu projede daha önce kullanılan `18765` portunda ve belirtilen population
koşusuyla başlatır. Terminal açık kaldığı sürece süreç çalışır; `Ctrl+C` ile düzgün kapatılır.

### Arka planda başlatma

```bash
mkdir -p audit/dashboard
nohup env PYTHONPATH=. .venv/bin/python -m tunnelbookai.dashboard \
  --host 127.0.0.1 --port 18765 \
  > audit/dashboard/server.log 2>&1 &
```

Terminal kapansa da dashboard'u arka planda tutar. Standart çıktı ve hatalar
`audit/dashboard/server.log` dosyasına yazılır.

### Dashboard'u tarayıcıda açma

```bash
open http://127.0.0.1:18765
```

macOS varsayılan tarayıcısında yerel paneli açar.

### Sağlık kontrolü

```bash
curl -fsS http://127.0.0.1:18765/healthz
```

Sunucu çalışıyorsa `ok` döndürür; bağlantı yoksa sıfırdan farklı çıkış kodu verir.

### Portu hangi sürecin kullandığını görme

```bash
lsof -nP -iTCP:18765 -sTCP:LISTEN
```

Portu dinleyen süreci ve `<PID>` değerini gösterir. Veri değiştirmez.

### Dashboard'u düzgün sonlandırma

```bash
kill <PID>
```

Önce normal `TERM` sinyali gönderir. `kill -9` yalnızca normal kapanış kesin biçimde
başarısızsa son çare olarak kullanılmalıdır; checkpoint yazımını kesebilir.

### Log izleme

```bash
tail -f audit/dashboard/server.log
```

Arka plan dashboard logunu canlı izler. `Ctrl+C` yalnızca `tail` komutunu kapatır,
dashboard'u kapatmaz.

## 7. Canonical corpus yönetimi

Canonical değişiklik yetkisi yalnızca `tunnelbookai.canonical` komutundadır. `plan` salt
okunur/dry-run, `apply` ise açık onay gerektiren yazma işlemidir.

### Canonical durumunu görme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical status --json
```

Corpus'un `EMPTY`, `READY` veya `INVALID` durumunu ve temel sayaçlarını gösterir.

### Bütünlüğü bağımsız doğrulama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical verify --json
```

Manifest, dosya hashleri, provenance, classification, chunk kimlikleri, belge digestleri ve
corpus digestini diskten yeniden hesaplar. `READY` dışındaki sonuç retrieval'ı engeller.

### Tek veya birkaç belge için dry-run planı

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical plan \
  --document-id ING_... --document-id ING_... --json
```

Staging ve original artifact'lerini doğrular, `CCP_...` planı yazar fakat canonical corpus'u
değiştirmez. `--document-id` birden çok kez verilebilir.

### Population seçicisinden plan oluşturma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical plan \
  --document-id-file audit/corpus_population/promotion_batches/CPP_....json \
  --json
```

Population'ın ürettiği belge listesini kullanır; bütün uygunluk kontrollerini canonical
otoritesi yeniden yapar.

### Tam plan kimliğini açıkça uygulama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.canonical apply \
  --plan audit/canonical_promotions/plans/CCP_....json \
  --approve CCP_.... --json
```

Canonical corpus'u değiştiren kontrollü komuttur. `--approve` plan içindeki tam `CCP_`
kimliğiyle aynı olmalıdır. Aynı belge kimliği ve kaynak SHA ile yeniden türetilmiş bir
belge planda `REPLACE` eylemiyle görünür; apply yeni nesneyi yazar, eski nesne dizini
referanssız (inert) kalır ve corpus digest değişir. Apply öncesi plan diskten tekrar kurulur; stale veya değişmiş plan
reddedilir. Başarılı her apply sonrasında yeniden `canonical verify` çalıştırılmalıdır.

### Eski compatibility komutu

```bash
PYTHONPATH=. .venv/bin/python scripts/promote_staging.py \
  --document-id ING_... --json
```

Yalnızca yeni canonical `plan` komutuna yönlendiren compatibility girişidir. Eski
`--apply`/`--target` arayüzü bilinçli olarak engellenmiştir; yeni iş akışında doğrudan
`tunnelbookai.canonical plan` ve `apply` tercih edilir.

## 8. Retrieval ve arama

### Canonical metin ve bölüm yönlendirme smoke testi

```bash
PYTHONPATH=. .venv/bin/python scripts/corpus_search_smoke.py --top-k 5
```

Doğrulanmış canonical corpus üzerinde deterministik, bölüm filtreli lexical kabul testi
çalıştırır ve `audit/retrieval/corpus_search_smoke_....json` yazar. Bu test embedding veya
semantik arama değildir.

### Retrieval indexi oluşturma veya devam ettirme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book build-index --batch-size 32
```

Yalnızca doğrulanmış canonical `embedding_ready.jsonl` satırlarını BGE-M3 ile vektörler.
Kesilmiş build varsayılan olarak checkpoint'ten devam eder ve sonunda
`book/retrieval/index_manifest.json` dosyasını atomik yayımlar. Dense index hazır olduktan
sonra aynı satırlar üzerinde BM25 lexical indexini de (`book/retrieval/lexical/<BRI_id>/`)
kurar; dense index zaten güncelse yalnızca eksik lexical index üretilir (`LEXICAL_BUILT`).
Lexical index yoksa `search` ve `evidence-audit` fail-closed durur.

### Indexi baştan üretme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book build-index \
  --batch-size 32 --no-resume
```

Mevcut build checkpoint'lerini kullanmadan yeniden başlar. Zaman ve model kaynağı tüketir;
canonical veya model kimliği değiştiğinde bilinçli olarak kullanılır.

### Semantik arama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book search \
  --query "tünel yapım maliyeti" --section 6 --top-k 10
```

Hibrit arama: sorguyu BGE-M3 ile vektörler, aynı anda Türkçe katlamalı BM25 ile lexical
eşleştirir, iki sıralamayı reciprocal-rank fusion ile birleştirir, chunk türü ağırlığı
uygular (figür başlıkları 0,6; metin 1,0) ve 150 karakterden kısa ya da içindekiler
tablosu görünümlü chunk'ları eler. Her sonuçta `dense_rank`, `lexical_rank` ve uygulanan
`retrieval_policy` raporlanır. `--section` verilmezse bütün bölümler aranır.

### Sabit semantik benchmark

```bash
PYTHONPATH=. .venv/bin/python scripts/retrieval_benchmark.py --top-k 10
```

3, 4, 5 ve 6. bölüm için sabit sorguları çalıştırır; beklenen canonical belgelerin bulunup
bulunmadığını denetler ve `audit/retrieval/semantic_benchmark_....json` üretir.

### Çıktı yolunu açıkça belirleme

```bash
PYTHONPATH=. .venv/bin/python scripts/retrieval_benchmark.py \
  --top-k 10 --output audit/retrieval/manual_benchmark.json
```

Benchmark sonucunu verilen proje-içi yola yazar.

## 9. Kitap üretim komutları

### Kitap sözleşmesini doğrulama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book validate --json
```

Dondurulmuş outline, soru bankası, hash kimlikleri ve yayın kurallarını
`book/config/book_contract.json` karşısında doğrular. Sözleşme şema 1.0 (sabit 66/59/50
yapısı) ve şema 2.0 (incelenmiş v2 kapsamı; bölüm başına değişken soru sayısı, pasif
başlıklar, insan-analizi bölümleri) desteklenir.

### İncelenmiş kapsam ve soru bankası taslağını normalize etme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book normalize-inputs \
  --draft book/question_bank/drafts/question_bank_v2_draft.md
```

İnsan tarafından düzenlenen tek Markdown taslağını (`## <no> <başlık> {keep|new|inactive:
gerekçe|chapter}` başlıkları ve numaralı sorular) ayrıştırır; `book/scope/normalized/`,
`book/question_bank/normalized/`, `book/audits/question_bank_integrity.json` ve
`book/audits/source_manifest.json` dosyalarını yeniden üretir; `book_contract.json`
dosyasını türetilmiş yapı ve yeni hash'lerle şema 2.0 olarak yeniden mühürler. Yayın
eşiği `ceil(toplam_soru × 0,6)` olarak türetilir. Taslaktaki her tutarsızlık satır
numarasıyla fail-closed hata verir. Komut, mevcut prewriting/coverage audit kimliklerini
geçersiz kılar; sonrasında `evidence-audit` yeniden çalıştırılmalıdır.

### Kitap üretim durumunu görme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book status --json
```

Canonical, retrieval, evidence audit, hazırlık, draft, coverage ve yayın blocker'larını salt
okunur biçimde raporlar.

### Bütün sorular için yazım öncesi kanıt auditi

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-audit \
  --all --batch-size 8 --top-k 8
```

Soru bankasındaki her soru için hibrit canonical retrieval (bölüm başlığıyla
zenginleştirilmiş sorgu, top-k 8, chunk içinden sorguya en çok değen 1.000 karakterlik pencere, örtüşen chunk tekrarlarının elenmesi) yapar ve Qwen ile
`SUPPORTED`, `PARTIAL` veya `UNSUPPORTED` kararı verir. Bölüm hazırlığı sözleşmedeki
kapsama oranından türetilen hedefe göre (`ceil(soru × 0,6)`) hesaplanır; insan-analizi
bölümleri `HUMAN_ANALYSIS_ARTIFACT_REQUIRED` olarak işaretlenir. Checkpoint'lidir; tekrar
çalıştırma son geçerli bölümden devam eder. `--top-k` en fazla 20 olabilir; batch
büyüdükçe Qwen bağlamı büyür.

### Tek bölüm için kanıt auditi

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-audit \
  --section 1.1 --batch-size 8 --top-k 8
```

Audit kapsamını tek soru-bankası bölümüne indirir. Pilot ve hedefli tekrar için uygundur.

### Bütün bölümlerin kanıt paketlerini hazırlama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book prepare --all
```

Tamamlanan prewriting auditinden, canonical claim registry ve immutable evidence paketleri
üretir. `UNSUPPORTED` sorular yazım kanıtına alınmaz.

### Tek bölümün kanıt paketini hazırlama

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book prepare --section 1.1
```

Yalnızca belirtilen bölümün hazırlık artifact'lerini üretir veya doğrular.

### Qwen ile kanıta bağlı bölüm taslağı yazma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book write \
  --section 1.1 --batch-size 8
```

Yalnızca bölümün hazırlanmış claim registry'sini kullanır ve iki geçişli çalışır: önce
Qwen bölümü 2–8 tematik akışa böler (`batches/plan.json`; her temaya pasaj ve soru
numaraları atanır, konu dışı pasajlar dışarıda kalır), sonra her tema için yalnızca o
temanın pasajlarıyla bağlantılı paragraflar yazılır (`batches/theme_NNN.json`). Cümleler
soru-cevap sırasına değil, tema sırasına göre dizilir. Her cümle en az bir claim'e bağlıdır;
soru bağı Qwen'in açık etiketi ile cümlenin claim'lerinin kanıtladığı soruların birleşimi
olarak türetilir ve `sentence_map.json` içine yazılır. `--batch-size` bu sürümde yalnızca
uyumluluk için kabul edilir. Kesinti halinde plan ve tema checkpoint'lerinden devam eder.
Sonuç audit yapılmadan yayınlanabilir sayılmaz.

### Yazım sonrası cümle-kanıt incelemesi

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book evidence-review \
  --section 1.1 --batch-size 12
```

Her taslak cümlesini yalnızca bağlı canonical claim pasajlarına karşı bağımsız Qwen geçişiyle
`SUPPORTED`, `PARTIAL`, `UNSUPPORTED` veya `NON_FACTUAL_OR_EDITORIAL` olarak değerlendirir.
Kısmi/desteksiz cümleler bölümü `AUDIT_HOLD` durumuna getirir.

### Soru kapsam auditi

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book coverage-audit \
  --section 1.1 --batch-size 10
```

Bölümün dondurulmuş sorularını gerçek cümle spanları ve kabul edilen claim zinciriyle
`ANSWERED`, `PARTIAL` veya `NOT_ANSWERED` olarak denetler. Yalnızca `ANSWERED` yayın
kapsamına sayılır.

### Kanıt sorunlu taslağı sınırlı revize etme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book revise --section 1.1
```

Yalnız aktif taslağın tamamlanmış cümle-kanıt auditi `REVISION_REQUIRED` olduğunda çalışır.
`PARTIAL` ve `UNSUPPORTED` cümleleri çıkarır; yalnız ortak canonical claim taşıyan yüksek
benzerlikli tekrarları birleştirir. Yeni bilgi veya yedek kaynak üretmez. Önceki taslağı
değiştirmeden yeni content-addressed taslak oluşturur, en fazla iki revizyon sınırını uygular
ve yeni taslağı tekrar `evidence-review` ile `coverage-audit` çalıştırılana kadar unaudited
tutar.

### Editoryal audit

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book editorial-audit --section 1.1
```

Metni ve sentence map'i deterministik editoryal hard gate ile doğrular; ayrıca yerel Qwen'in
kronoloji, adlandırma, dil ve yapı bulgularını danışman kayıt olarak saklar. Qwen bulguları
harici bilgiyle düzeltme yapamaz ve tek başına freeze'i engelleyemez.

### Bölümü okuyup operatör onayı kaydetme

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book approve-section \
  --section 1.1 --note "Bölümü baştan sona okudum; akış ve dil kitap bölümü olarak kabul edilebilir."
```

Model kapıları kanıtı ve yapıyı doğrular; metnin okunabilir bir kitap bölümü olduğunu
yalnızca bir insan doğrulayabilir. Bu komut, aktif taslağın kimliğine, Markdown hash'ine ve
editoryal audit kimliğine bağlı bir onay kaydı (`book/production/approvals/`) yazar. Taslak
yeniden yazılır, revize edilir veya editoryal audit yenilenirse onay kendiliğinden geçersiz
olur ve `freeze` `OPERATOR_READ_APPROVAL_PASS` koşulunda `HOLD` verir. `--note` zorunludur.

### Bölümü dondurma

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book freeze --section 1.1
```

Kanıt, maddi iddia, kapsam, editoryal, citation provenance, analiz artifact ve operatör
okuma onayı kapılarının tamamını doğrular. Geçerse bölüm, bağlı artifactler ve onay
kaydının content-addressed, salt okunur snapshotını üretir. Frozen bölümde `write` ve
`revise` fail-closed engellenir.

### Henüz uygulanmamış komut

```bash
PYTHONPATH=. .venv/bin/python -m tunnelbookai.book assemble
```

`assemble` CLI'da gelecekteki sözleşme yeri olarak bulunur; güncel sürümde yapılandırılmış
`NOT_IMPLEMENTED` sonucu ve sıfırdan farklı çıkış kodu verir. Sahte kitap artifacti üretmez.

## 10. Mimari ve bootstrap kontrolleri

### Aktif mimarinin legacy sistemden izole olduğunu doğrulama

```bash
PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py --mode isolation
```

Aktif script listesini, legacy yolları ve eski runtime referanslarını kontrol eder. Canlı ve
dolu bir repository için kullanılacak doğru mimari kontroldür.

### Empty-reset kontrolü

```bash
PYTHONPATH=. .venv/bin/python shared/project_quality_gate.py --mode empty-reset
```

Yalnızca yeni/boş bootstrap düzeninin sıfır corpus şartlarını denetler. Meşru ingest ve
canonical verisi bulunan güncel projede `NO_GO` dönmesi beklenir; veri silme gerekçesi
değildir. Sonucu `audit/empty_corpus_reset_gate.json` dosyasına yazar.

### Legacy reset doğrulama wrapper'ı

```bash
PYTHONPATH=. .venv/bin/python scripts/reset_legacy_state.py
```

Gerekli `.gitkeep` işaretlerini oluşturur ve empty-reset gate'ini gerçekten çalıştırır.
`--help` seçeneği yoktur; `--help` yazılsa bile kontrol çalışır ve audit dosyası güncellenir.
Dolu production repository üzerinde günlük operasyon komutu olarak kullanılmamalıdır.

## 11. Test ve kalite komutları

### Tüm Python testleri

```bash
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests
```

Bütün Python testlerini tek süreçte çalıştırır. Docling/OCR nedeniyle yüksek bellek
kullanabilir ve Office render testleri LibreOffice erişimi ister.

### Testleri daha kararlı gruplar halinde çalıştırma

```bash
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/book
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/canonical -t .
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/dashboard
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/population
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests/ingest -t .
```

Her alt sistemi ayrı süreçte doğrular. `-t .`, relative import kullanan testlerin proje
kökünü doğru paket üst dizini olarak görmesini sağlar.

### Tek test modülü veya tek test çalıştırma

```bash
PYTHONPATH=. .venv/bin/python -m unittest tests.book.test_retrieval -v
PYTHONPATH=. .venv/bin/python -m unittest \
  tests.ingest.test_reset_architecture.ResetArchitectureTests.test_legacy_runtime_is_isolated_from_active_topology \
  -v
```

Hedefli hata teşhisi için kullanılır. `-v`, test adlarını ve ayrıntılı sonucu gösterir.

### Playwright dashboard E2E testleri

```bash
npm run test:e2e
```

Geçici dashboard test sunucusunu başlatır, Chromium ile kullanıcı akışlarını test eder ve
sunucuyu kapatır. Test sunucusunun loopback porta bağlanabilmesi gerekir.

### Değişikliklerde whitespace kontrolü

```bash
git diff --check
```

Elle değiştirilen dosyalarda trailing whitespace ve bozuk patch satırlarını bulur. Otomatik
üretilen corpus Markdown'ındaki kaynak-korumalı boşluklar ayrıca değerlendirilebilir.

### Python dosyalarını bytecode'a derleyerek sözdizimi kontrolü

```bash
PYTHONPATH=. .venv/bin/python -m compileall -q tunnelbookai shared scripts
```

Python kaynaklarında import öncesi sözdizimi hatalarını bulur. `__pycache__` dosyaları üretir;
bunlar Git tarafından izlenmemelidir.

## 12. Git sürümleme komutları

### Durumu görme

```bash
git status --short
git status -sb
```

İlki değişen dosyaları kısa biçimde, ikincisi ayrıca branch ve uzak dal farkını gösterir.

### Değişiklikleri inceleme

```bash
git diff
git diff --stat
git diff --cached
```

Sırasıyla sahnelenmemiş patch'i, özetini ve commit'e girecek sahnelenmiş patch'i gösterir.

### Tüm proje değişikliklerini sahneleme

```bash
git add -A
```

Yeni, değişmiş ve silinmiş bütün izlenebilir dosyaları bir sonraki commit'e hazırlar.
Çalıştırmadan önce `.gitignore` ve büyük dosyalar kontrol edilmelidir.

### Commit oluşturma

```bash
git commit -m "Kısa ve açıklayıcı değişiklik özeti"
```

Sahnedeki değişiklikleri yerel Git geçmişine kaydeder.

### Commit'i GitHub'a gönderme

```bash
git push origin main
```

Yerel `main` commitlerini yapılandırılmış `origin/main` dalına gönderir. Corpus/audit gibi
büyük veya hassas içerikler varsa hedef ve kapsam push öncesinde açıkça doğrulanmalıdır.

### Yerel ve uzak commit'i karşılaştırma

```bash
git rev-parse HEAD
git rev-parse origin/main
git log --oneline -n 10
```

İlk iki hash aynıysa yerel takip bilgisine göre push tamamdır. Son komut son on commit'i
gösterir.

### Uzak dal bilgisini güvenli biçimde yenileme

```bash
git fetch origin main
```

Çalışma dosyalarını değiştirmeden `origin/main` bilgisini günceller. Büyük push sonunda
uzak dal güncellenmiş fakat yerel tracking ref eski kalmışsa doğrulama için kullanılabilir.

Bu projede veri kaybı riski nedeniyle `git reset --hard`, geniş kapsamlı `git clean` ve
onaysız force-push kullanılmamalıdır.

## 13. Salt okunur teşhis komutları

### Son population koşularını listeleme

```bash
ls -lt audit/corpus_population/runs | head
```

En son değişen koşu dosyalarını gösterir.

### Belirli bir belgeye ait artifact'leri bulma

```bash
find processing/ING_... -maxdepth 3 -type f | sort
```

Belgenin normalized metin, metadata, figures, tables ve chunk dosyalarını listeler.

### Bir JSON dosyasını okunabilir gösterme

```bash
PYTHONPATH=. .venv/bin/python -m json.tool DOSYA.json
```

JSON'u parse eder ve biçimli yazdırır. Geçersiz JSON'da sıfırdan farklı çıkış kodu verir.

### Log içinde hata veya uyarı arama

```bash
rg -n "ERROR|FAILED|MODEL_SERVICE_UNAVAILABLE|RECOVERY_REQUIRED" audit reports
```

Audit ve raporlarda önemli durum kodlarını hızlıca bulur; dosyaları değiştirmez.

### Disk kullanımını görme

```bash
du -sh audit corpus processing originals book
df -h .
```

İlk komut proje veri alanlarının büyüklüğünü, ikinci komut disk bölümündeki boş alanı
gösterir. Population batch çalışması öncesinde boş alan kontrolü önemlidir.

## 14. Önerilen uçtan uca işletim sırası

1. `scripts/probe_models.py` ile BGE-M3 ve Qwen'i doğrula.
2. `tunnelbookai.canonical verify` ile mevcut canonical tabanı doğrula.
3. Yeni dış dosyalar varsa `manual-import-plan` ve tam kimlikle `manual-import-apply` yap.
4. `population inventory` ve `plan-batches` çalıştır.
5. Dashboard'u başlat veya `run-batch --resume` ile batch'leri sırayla işle.
6. `population staging-audit` ile bütün girdileri ve promotion seçicilerini doğrula.
7. Her `CPP_` için sırasıyla canonical `verify`, `plan`, açık kimlikle `apply`, tekrar
   `verify` çalıştır.
8. `population readiness` ile corpus aktarımının tamamlandığını doğrula.
9. Canonical digest değiştiyse `book build-index` çalıştır ve `retrieval_benchmark.py` ile
   aramayı test et.
10. Kitap aşamalarını `evidence-audit → prepare → write → evidence-review → gerekirse revise
    → evidence-review → coverage-audit → editorial-audit → approve-section → freeze`
    sırasıyla yürüt.
11. Her anlamlı işlemden sonra `reports/project_work_log.md` dosyasına sonucu, artifact'i,
    doğrulamayı ve bilinen sınırlamaları ekle.

## 15. Kritik güvenlik kuralları

- `incoming/`, `processing/` veya `corpus/staging/` kitap kanıtı değildir; yalnızca
  doğrulanmış `corpus/canonical/` kanıttır.
- Ingest ve population canonical apply yapamaz.
- Canonical `apply`, tam `CCP_` plan kimliği açıkça onaylanmadan çalıştırılmaz.
- `--force-reprocess` sonrası eski staging audit ve canonical planları yeniden üretilir.
- Canonical manifest veya content-addressed object dosyaları elle düzenlenmez.
- Dashboard dış ağa bağlanmaz; `--host 127.0.0.1` korunur.
- Qwen veya BGE-M3 kullanılamıyorsa başka modele sessiz geçiş yapılmaz.
- `reset_legacy_state.py`, dolu production repository'sini sıfırlamaz; yalnızca tarihsel
  empty-reset koşulunu doğrular ve normal işletimde çalıştırılmaz.
- `assemble` güncel sürümde tamamlanmış özellik değildir.
