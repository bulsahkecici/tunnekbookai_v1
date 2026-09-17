# TunnelBookAI Ana Çalışma Günlüğü

Son güncelleme: 2026-09-16

Bu dosya projenin aktif, insan tarafından okunabilir çalışma günlüğüdür. Aşağıdaki geçmiş,
mevcut raporlar, audit dosyaları, manifestler ve doğrulama sonuçlarından yeniden
oluşturulmuştur. Pre-reset ayrıntıları `reports/legacy_pre_reset/` altında değişmeden
korunmaktadır. Bundan sonraki her anlamlı işlem bu dosyaya yeni bir kayıt olarak eklenir.

## Güncel durum

- Canonical durum: `READY`
- Canonical belge: **656**
- Toplam chunk: **30.926**
- Aramaya uygun metin temsili: **30.332 chunk**
- Corpus digest: `1fec0054249e8350c1ff300d5669a1ad914b1cd1ec48f3d85b1cc6e22da60660`
- Seçili population girdisi: **890**
- Açıklanmamış girdi: **0**
- Gerçek embedding/vektör retrieval index: **henüz uygulanmadı**
- Yerel operasyon dashboard'u: **şu anda çalışmıyor**

Ana kanıtlar:

- `corpus/canonical/canonical_manifest.json`
- `audit/canonical_promotions/applies/CPA_20260916T040652Z_8105d117e1_4dbb0c67.json`
- `reports/corpus_population_readiness.md`

## Kronolojik çalışma özeti

### 2026-09-04 — Güvenli temizleme ve mimari sıfırlama

- Eski corpus, staging, processing, embedding, Qdrant ve üretim çıktıları silinmeden önce
  geri kazanılabilirlik kapısı çalıştırıldı.
- **350 kaynak referansı** incelendi; geri getirilemeyen özgün kaynak baytı bulunmadı.
- Eski çalışma yüzeyi aktif mimariden çıkarıldı; tarihsel dosyalar `archive/legacy_pre_reset/`,
  raporlar ve auditler kendi `legacy_pre_reset` alanlarına taşındı.
- PaperCrawler yalnızca Source Pack üreticisi, TunnelBookAI ise ingest, sınıflandırma,
  kalite, chunking ve canonical otoritesi olarak ayrıldı.
- Kanıt: `reports/master_cleanup_reset_report.md`, `reports/pre_reset_recoverability.md`.

### 2026-09-08 — Aktif depo hizalaması ve model doğrulaması

- Desteklenen aktif komutlar ve klasör sınırları sadeleştirildi.
- Kitap kapsamı ve **2.950 soruluk** soru bankası doğrulandı.
- Yerel embedding ve LLM servisleri kesin model kimlikleriyle test edildi; o tarihte
  kullanılabilir olduğu kaydedildi.
- Aktif ingest testleri ve mimari izolasyon kapısı geçti.
- Kanıt: `reports/post_reset_repository_alignment.md`.

### 2026-09-08 — Kontrollü canonical promotion katmanı

- `tunnelbookai.canonical` tek plan/apply/verify/status otoritesi olarak oluşturuldu.
- İçerik adresli canonical nesneler, deterministik manifest, stale-plan koruması, atomik
  commit ve bağımsız bütünlük doğrulaması eklendi.
- İlk kilometre taşında corpus bilinçli olarak boş bırakıldı; gerçek promotion daha sonra
  açık onayla yapıldı.
- Kanıt: `reports/canonical_promotion_milestone.md`.

### 2026-09-09–13 — Corpus population ve belge işleme

- Manuel ve PaperCrawler girdileri Unified Ingest hattında envanterlendi, çıkarıldı,
  normalize edildi, sınıflandırıldı, chunklandı ve staging'e alındı.
- PDF, Office, tablo, şekil, OCR fallback ve sayfa snapshot yolları kullanıldı.
- Son readiness kaydında **890 seçili girdi** ve **0 çözümsüz girdi** bulunuyor.
- Belge metinleri `processing/<BELGE_ID>/normalized/document.md`, sayfa görüntüleri
  `processing/<BELGE_ID>/pages/page_XXXX.png` olarak üretildi.
- 2026-09-16 sayımında processing altında **18.554 sayfa PNG'si** ve **889 normalize
  Markdown**, canonical altında **656 `document.md`** bulunuyordu.
- Kanıt: `reports/corpus_population_readiness.md`, `audit/corpus_population/`.

### 2026-09-13 — Uyarı güdümlü chunk iyileştirmeleri

- Dashboard uyarıları işlem yapılabilir ve bilgi amaçlı olarak ayrıldı.
- Audit kaydındaki **424 adayın 424'ü** işlendi; başarısız işlem olmadı.
- Fazla uzun chunklar giderildi; güvenle birleştirilemeyen kısa yapısal parçalar
  `CHUNK_SHORT_STRUCTURAL` bilgi notuna dönüştürüldü.
- Görsel/Office kaynağına özel durumlar otomatik ve kayıplı bir dönüşüm yapılmaması için
  ertelendi.
- Kanıt: `audit/dashboard/improvements.json`, `audit/dashboard/improvements.log`.

### 2026-09-14 — Bölüm 3, 4 ve 6 manuel tam-metin incelemesi

- **83 belge** başlık, tam metin, bölüm kanıtı, confidence ve retrieval temsili üzerinden
  manuel incelendi.
- **36 belge eşlemesi güncellendi**, **29 belge değişmeden doğrulandı**, **18 belge** konu
  dışı veya yetersiz kanıt nedeniyle geri kazanılabilir karantinaya alındı.
- Yanlış “TBM”, tunnel-form, özgeçmiş ve içeriksiz landing page kayıtları kitap kanıtından
  çıkarıldı.
- Kanıt: `audit/dashboard/section_reviews/MSR_section_3_4_6_full_text_v1.json`.

### 2026-09-14–15 — Hedefli tam-metin recovery

- İki eksik landing-page kaydı resmi tam metinlerle kurtarıldı.
- Biri tünel kaplama inceleme/bakım maliyetine, diğeri jeolojik risk kaynaklı kazı
  maliyetine eşlendi.
- Kanıt: `audit/dashboard/targeted_recovery_review.json`.

### 2026-09-15 — PaperCrawler ile Bölüm 3 derin araştırması

- **187 aday** tarandı, **3 yeni tam metin** sisteme alındı ve toplam **6 belge** Bölüm 3
  kanıtı için manuel eşlendi.
- Bölüm 3 birincil belge sayısı **2'den 4'e**, corpus belge sayısı **653'ten 656'ya**,
  chunk sayısı **30.873'ten 30.926'ya**, aramaya uygun chunk sayısı **30.280'den
  30.332'ye** çıktı.
- Ovit ve Zigana tarihçesi/kurumsal bağlamı ile KGM envanterleri corpus kapsamına alındı.
- Kanıt: `audit/dashboard/section_reviews/MSR_section_3_papercrawler_deep_research_v1.json`.

### 2026-09-16 — Canonical corpus promotion

- Güncel staging kümesi kontrollü plan ve açık onayla canonical corpusa aktarıldı.
- Plan: `CCP_1ddc3a37a1a8588517a6f1c6ca7f4a1333d5e2c1df706b014935168105d117e1`.
- Bağımsız doğrulama sonucu: `READY`; **656 belge**, **30.926 chunk**, **30.332
  retrieval-ready chunk**, hata ve uyarı yok.
- Her canonical belgede normalize `document.md`, metadata, provenance, sınıflandırma,
  kalite ve chunk kimlik kayıtları bulunuyor. Sayfa/figure PNG dosyaları processing
  alanında tutuluyor; canonical içine kopyalanmıyor.
- Kanıt: `corpus/canonical/canonical_manifest.json`,
  `audit/canonical_promotions/applies/CPA_20260916T040652Z_8105d117e1_4dbb0c67.json`.

### 2026-09-16 — Canonical arama kabul testi

- `scripts/corpus_search_smoke.py` eklendi. Script önce canonical bütünlüğünü doğruluyor,
  sonra yalnızca manifestin kabul ettiği `embedding_ready.jsonl` dosyalarında
  deterministik, bölüm filtreli lexical sıralama yapıyor.
- Bölüm 3, 4, 5 ve 6 için **4/4 test geçti**.
- Bölüm 3 sorgusunda Yeni Zigana ve Ovit/Zigana belgeleri; Bölüm 4'te yaşam döngüsü
  maliyeti; Bölüm 5'te bakım/işletme; Bölüm 6'da tünel birim fiyatı ve püskürtme beton
  kayıtları üst sonuçlarda bulundu.
- Bu test canonical metnin bulunabildiğini ve bölüm yönlendirmesini doğrular. Embedding,
  vector store veya semantik retrieval kalitesini doğrulamaz; Book Retrieval Layer hâlâ
  ayrı bir sonraki kilometre taşıdır.
- Sonuç: `audit/retrieval/corpus_search_smoke_20260916T073736Z.json`.

## Çalışma günlüğü protokolü

Yeni her kayıt aşağıdaki şablonla bu dosyanın sonuna eklenir:

```text
### YYYY-AA-GG — İşlem adı
- Amaç ve kapsam
- Yapılan değişiklik
- Sayısal önce/sonra sonucu
- Doğrulama ve audit/rapor bağlantısı
- Bilinen sınırlama
- Sıradaki önerilen işlem
```

Bu protokol kök `AGENTS.md` dosyasında proje çalışma kuralı olarak tanımlanmıştır.

## Sıradaki önerilen iş

Book Retrieval Layer V1 uygulanmalı: yalnızca doğrulanmış canonical snapshot üzerinden
yeniden üretilebilir embedding/index oluşturmalı, manifest digestine bağlanmalı ve bölüm
filtreli retrieval benchmark ile doğrulanmalıdır. Bu yapılana kadar
`scripts/corpus_search_smoke.py` yalnızca corpus erişilebilirlik ve yönlendirme kabul testi
olarak kullanılmalıdır.

### 2026-09-16 — Retrieval hazırlığı / İş kalemi 1: model servisleri

- Amaç: gerçek retrieval indexi oluşturulmadan önce yapılandırılmış kesin model
  kimliklerinin yerel serviste çalıştığını doğrulamak.
- Embedding modeli `text-embedding-baai-bge-m3-568m` ile iki başarılı istek yapıldı;
  kararlı ve boş olmayan **1.024 boyutlu** vektör alındı.
- LLM olarak kullanıcının seçtiği `qwen/qwen3.8-27b` ile yapılandırılmış yanıt isteği
  başarıyla tamamlandı.
- Her iki servis de `http://127.0.0.1:1234/v1` loopback sınırında `AVAILABLE` durumunda.
- İlk sandbox içi kontrol yerel servise erişemedi; gerçek makine bağlamındaki doğrulama
  başarılı oldu. Bulut fallback'i veya model ikamesi kullanılmadı.
- Audit: `audit/retrieval/model_capability_20260916.json`.
- Sonuç: **İş kalemi 1 tamamlandı.** Sıradaki işlem canonical digestine bağlı retrieval
  index sözleşmesi ve index üreticisidir.

### 2026-09-16 — Book Retrieval Layer V1 / İş kalemi 2: gerçek embedding indexi

- Amaç: doğrulanmış canonical corpusun bütün retrieval-ready chunklarını gerçek yerel
  embedding vektörleriyle aranabilir hâle getirmek.
- `tunnelbookai.book.retrieval` eklendi; yalnızca bağımsız doğrulamadan geçmiş canonical
  manifest ve onun kabul ettiği `embedding_ready.jsonl` kayıtlarını tüketiyor.
- `python -m tunnelbookai.book build-index` ve `search` komutları etkinleştirildi.
- Kesinti sonrası devam, atomik checkpoint, exact-model kontrolü, loopback sınırı,
  normalize cosine vektörleri, shard hashleri ve corpus-digest geçersizleştirmesi eklendi.
- `text-embedding-baai-bge-m3-568m` ile **30.332 / 30.332 chunk** için **1.024 boyutlu**
  gerçek embedding üretildi.
- Index: `BRI_283dad3544bd03b43c67e7c252464374e62762add63eadc7b9b10371238fe691`;
  **474 shard**, **948 dosya**, yaklaşık **137 MiB**.
- Aktif manifest: `book/retrieval/index_manifest.json`; canonical corpus digest
  `1fec0054249e8350c1ff300d5669a1ad914b1cd1ec48f3d85b1cc6e22da60660` ile bağlı.
- Bağımsız index doğrulaması ve Book status sonucu `READY`; 22 hedefli unit test geçti.
- Büyük, yeniden üretilebilir vektör shardları `.gitignore` kapsamındadır; küçük kimlik
  manifesti proje durumunda tutulur.
- Sonuç: **İş kalemi 2 tamamlandı.** Sıradaki işlem gerçek semantik sorgularla bölüm 3,
  4, 5 ve 6 retrieval benchmarkıdır.

### 2026-09-16 — Semantik retrieval kabul testi / İş kalemi 3

- Amaç: gerçek embedding indexinin Bölüm 3, 4, 5 ve 6 için beklenen canonical
  belgeleri bölüm filtresiyle bulduğunu ve sonuçların kaynak konumlarına geri
  izlenebildiğini doğrulamak.
- `scripts/retrieval_benchmark.py` eklendi; dört sabit sorgu, önceden belirlenmiş
  beklenen belge kimlikleri ve `top_k=10` kabul ölçütü kullanıldı.
- İlk koşu 4/4 geçti fakat NumPy 2.2.6 `matmul` işlemi finite float32 mmap dizilerinde
  yanıltıcı taşma uyarıları verdi. Indexin 474 shardının tamamı ayrıca kontrol edildi:
  dtype `float32`, non-finite değer sayısı **0**, L2 norm aralığı
  **0,99999988–1,00000012**.
- Skorlama eşdeğer ve bu ortamda kararlı `np.dot` işlemine geçirildi; index doğrulamasına
  finite-float32 ve L2-normalizasyon kapıları, aramaya da finite-skor kapısı eklendi.
- Temiz tekrar koşusunda **4/4 bölüm testi geçti**. Üst skorlar Bölüm 3: **0,657589**,
  Bölüm 4: **0,696736**, Bölüm 5: **0,691299**, Bölüm 6: **0,733575**. Her sonuç belge,
  chunk, bölüm ve varsa sayfa başlangıç/bitiş konumunu içeriyor.
- Nihai audit: `audit/retrieval/semantic_benchmark_20260916T083237Z.json`. İlk uyarılı
  tarihsel koşu: `audit/retrieval/semantic_benchmark_20260916T083043Z.json`.
- Doğrulama: 22 hedefli unit test, Python derleme kontrolü ve `git diff --check` geçti.
- Sınırlama: Bu küçük kabul seti retrieval hattını ve dört bölümde bilinen kanıtların
  bulunmasını doğrular; 2.950 sorunun tamamı için kanıt yeterliliğini henüz ölçmez.
- Sonuç: **İş kalemi 3 tamamlandı.** Sıradaki işlem semantik arama ve kaynak
  konumlarının operasyon dashboardunda görünür hâle getirilmesidir.

### 2026-09-16 — Dashboard semantik arama / İş kalemi 4

- Amaç: doğrulanmış Book Retrieval V1 indexini operatörün kullanabildiği, salt okunur bir
  dashboard yüzeyine taşımak.
- `GET /api/retrieval/status` ve `GET /api/retrieval/search` uçları eklendi. Arama ucu
  sorgu uzunluğu ve `top_k` sınırlarını denetliyor; stale/bozuk index veya model hatasında
  kapalı kalıyor.
- Dashboarda **Semantik arama** sekmesi eklendi. Tüm corpus veya Bölüm 3/4/5/6 filtresiyle
  arama yapılıyor; sonuçlarda benzerlik skoru, canonical belge/chunk kimliği, birincil
  bölüm, chunk türü, sayfa/slayt/sheet konumu ve canonical retrieval yolu gösteriliyor.
- Playwright test sunucusu canlı `18765` dashboarduyla çakışmaması için varsayılan olarak
  ayrı `18766` test portuna alındı.
- Doğrulama: **9/9 unit test** ve **8/8 Playwright E2E test** geçti; JavaScript/Python
  sözdizimi ve `git diff --check` temiz.
- Gerçek tarayıcı kabulünde aktif index `READY`, **30.332 vektör / 1.024 boyut** olarak
  göründü. Bölüm 6 gerçek sorgusunda 10 sonuç üretildi; ilk sonuç
  `ING_ecb7b50dece6c5a14085_CH_ee9942806e`, **%73,4** skor ve **sayfa 8–9** konumuyla
  görüntülendi. Tarayıcı konsolunda hata/uyarı yoktu.
- Eski `18765` dashboard süreci kontrollü sonlandırılıp güncel kodla aynı adreste yeniden
  başlatıldı; `http://127.0.0.1:18765/healthz` yanıtı `ok`.
- Değişen ana dosyalar: `tunnelbookai/dashboard/server.py`,
  `tunnelbookai/dashboard/static/{index.html,app.js,styles.css}`,
  `tests/dashboard/test_dashboard.py`, `tests/e2e/dashboard.spec.js`,
  `playwright.config.js`, `docs/operations_dashboard.md`.
- Sınırlama: Arama ilk kullanımda index bütünlüğünü baştan doğruladığı için birkaç saniye
  sürebilir; dashboard sonuçları kanıt bulur fakat henüz 2.950 sorunun kanıt yeterliliği
  değerlendirmesini yapmaz.
- Sonuç: **İş kalemi 4 tamamlandı.** Sıradaki işlem 2.950 soruluk soru bankasında Qwen ile
  kanıt yeterliliği ve boşluk auditidir.

### 2026-09-17 — Qwen yazım-öncesi kanıt auditi / İş kalemi 5

- Amaç: dondurulmuş 2.950 sorunun her biri için doğrulanmış canonical corpusta gerçekten
  cevaplayıcı kanıt bulunup bulunmadığını yazımdan önce ölçmek ve açıkları bölüm bazında
  görünür kılmak.
- `tunnelbookai.book.prewriting` ve `evidence-audit` komutu uygulandı. Audit yalnızca
  doğrulanmış Book Retrieval V1 indexinde global semantik arama yapıyor; her soru için ilk
  4 adayı yerel `qwen/qwen3.8-27b` modeline veriyor ve `SUPPORTED`, `PARTIAL` veya
  `UNSUPPORTED` kararı üretiyor. Bulunan adayların belge, chunk, kaynak konumu ve canonical
  yolu model kararından bağımsız olarak korunuyor.
- Kesinti güvenliği için bölüm başına atomik checkpoint ve aynı audit kimliğiyle devam
  mekanizması eklendi. Bilgisayar uykuya geçtikten sonra yapılan kontrolde auditin yarım
  kalmadığı, **59 / 59 bölüm** ve **2.950 / 2.950 benzersiz soru** ile tamamlandığı
  doğrulandı; geçici dosya yoktu ve her bölüm tam 50 kayıt içeriyordu.
- Sonuç: **257 SUPPORTED**, **907 PARTIAL**, **1.786 UNSUPPORTED**. Bölüm durumu
  **17 READY_WITH_LIMITATIONS**, **42 EVIDENCE_GAP**; hiçbir bölüm tercih edilen destek
  eşiğini henüz karşılamıyor. Bu sonuç mevcut corpusun gerçek yazım boşluklarını gösterir,
  nihai metin soru kapsamı sonucu değildir.
- Audit kimliği:
  `PEA_2f345af44628523a55abf2ac91f7385b1b819ffc21d7fbb7440565ca040584c9`.
  Aktif özet: `audit/book/prewriting_evidence_audit.json`; 2.950 satırlık sonuç:
  `audit/book/prewriting/PEA_2f345af44628523a55abf2ac91f7385b1b819ffc21d7fbb7440565ca040584c9/results.jsonl`;
  insan özeti: `reports/prewriting_evidence_audit.md`.
- Kimlik bağları doğrulandı: canonical digest
  `1fec0054249e8350c1ff300d5669a1ad914b1cd1ec48f3d85b1cc6e22da60660`, retrieval index
  `BRI_283dad3544bd03b43c67e7c252464374e62762add63eadc7b9b10371238fe691`, embedding modeli
  `text-embedding-baai-bge-m3-568m`, Qwen modeli `qwen/qwen3.8-27b`.
- Doğrulama: sonuç satırı/benzersiz soru/sayaç/provenance/canonical yol kontrolleri temiz;
  `tests.book.test_prewriting`, `tests.book.test_retrieval` ve
  `tests.book.test_foundation` toplam **20 / 20 test** geçti; `git diff --check` temiz.
- Dokümantasyon güncellendi: `README.md` ve `docs/book_production_engine.md` artık auditin
  gerçek komutunu, kesinti sonrası devam davranışını ve çıktı konumlarını gösteriyor.
- Sonuç: **İş kalemi 5 tamamlandı.** Sıradaki işlem, Qwen'e yalnızca izinli kanıtı veren
  bölüm kanıt paketleri ile iddia kayıt sözleşmesinin uygulanmasıdır.

### 2026-09-17 — Bölüm kanıt paketleri ve iddia kayıtları / İş kalemi 6

- Amaç: tamamlanan Qwen kanıt auditini yerel bölüm yazarının serbestçe kaynak veya bilgi
  uyduramayacağı, makinece doğrulanabilir bir yazım girdisine dönüştürmek.
- `tunnelbookai.book.preparation` ve `python -m tunnelbookai.book prepare --all|--section`
  uygulandı. Her bölüm için içerik-adresli `evidence_packet.json` ve
  `claim_registry.json` üretiliyor; aktif durum
  `book/production/preparation/manifest.json` üzerinden izleniyor.
- Paketler audit tarafından Qwen'in açıkça seçtiği canonical pasajları kabul ediyor.
  `SUPPORTED` sorular doğrudan-atıflı, `PARTIAL` sorular sınırlama ifadesi zorunlu,
  `UNSUPPORTED` sorular ise **NO_FACTUAL_ANSWER** olarak kilitli. Kayıt dışı olgusal iddia,
  canonical dışı kaynak ve modelin proje bulgusu icat etmesi makine kısıtlarında kapalı.
- **59 / 59 bölüm** ve **2.950 / 2.950 soru** hazırlandı. Bölümlere bağlı toplam
  **1.776 canonical pasaj/iddia kaydı** oluşturuldu. Her kayıt belge/chunk kimliği,
  canonical dosya/satır konumu, locator, metin SHA-256 özeti, kaynak sınıfı ve bağlı soru
  kimliklerini içeriyor.
- Bağımsız bütünlük kontrolünde 59 benzersiz paket, 59 benzersiz kayıt defteri ve 2.950
  benzersiz soru doğrulandı. **1.776 / 1.776** iddia kaydının metni ve özeti gerçek
  canonical satırla birebir eşleşti; kullanılmayan veya kayıtsız claim kimliği ve kaynak
  uyuşmazlığı sayısı **0**.
- Kanıtı hiç olmayan ve claim sayısı sıfır bölümler: `5.1`, `5.3`, `5.9`, `5.9.1`,
  `6.1`, `6.1.3`, `6.2.1`. Bu bölümlerde Qwen yazarı olgusal metin üretmemeli; corpus
  takviyesi veya insan analizi gerekir.
- Manifest kimliği:
  `SPM_d05b2282c795b17740b6d4c2089e73febc088f49987fe64e6d60b383efe01276`.
  İnsan özeti: `reports/section_preparation.md`. Şemalar:
  `book/audits/schemas/section_evidence_packet.schema.json` ve
  `book/audits/schemas/section_claim_registry.schema.json`.
- `book status` çıktısına `sections_prepared` ve geçerli preparation manifesti eklendi.
  Doğrulama: **59 paket + 59 kayıt defteri = 118 artifact** JSON şemalarından geçti;
  hazırlama/prewriting/retrieval/foundation testleri toplam **23 / 23 geçti**;
  `git diff --check` temiz. Status sonucu preparation için `COMPLETE` ve 59 bölüm gösteriyor.
- Sonuç: **İş kalemi 6 tamamlandı.** Sıradaki işlem, yalnızca paket claim kimliklerini
  kullanabilen ve her teknik cümle için sentence-to-claim haritası üreten yerel Qwen bölüm
  yazarıdır. Kanıtsız bölümler yazım yerine açık `EVIDENCE_GAP` sonucu vermelidir.

### 2026-09-17 — Yerel Qwen bölüm yazarı ve 1.1 pilotu / İş kalemi 7

- Amaç: hazırlanmış bölüm paketleri dışında bilgi kullanamayan, her cümleyi kayıtlı claim
  ve soru kimliklerine bağlayan, kesintiden sonra devam edebilen yerel bölüm yazarı kurmak.
- `tunnelbookai.book.writer` ve `python -m tunnelbookai.book write --section ...` uygulandı.
  Yazar yalnızca `SUPPORTED`/`PARTIAL` soruları ve bunların izinli claimlerini Qwen'e verir;
  `UNSUPPORTED` sorular modele yazım girdisi olarak verilmez. Kayıt dışı claim, eksik soru
  kapsaması ve boş kaynak eşlemesi fail-closed reddedilir.
- Qwen çağrıları bölüm başına küçük partilere ayrılıyor ve atomik checkpoint tutuluyor.
  Bilgisayar uyur veya servis kesilirse tamamlanan partiler yeniden üretilmeden devam eder.
- Yerel servis tekrar doğrulandı: `qwen/qwen3.8-27b` yapılandırılmış JSON için,
  `text-embedding-baai-bge-m3-568m` ise kararlı 1.024 boyutlu vektör için `AVAILABLE`.
- İlk pilot **1.1 Tünelin Tanımı** bölümünde tamamlandı. **42/42 yazılabilir soru** işlendi;
  8 `UNSUPPORTED` soru bilerek dışarıda bırakıldı. Sonuç **35 paragraf, 105 cümle,
  yaklaşık 1.794 sözcük ve 51 kullanılan claim**; 6/6 Qwen checkpoint partisi tamamlandı.
- 105 cümlenin tamamı claim ve soru kimliğine bağlıdır. Kayıt dışı claim, bilinmeyen soru,
  `UNSUPPORTED` soru referansı ve hash uyuşmazlığı sayısı **0**. Draft ve sentence-map 2/2
  JSON şemasından geçti; hedefli testler **27/27** geçti; `git diff --check` temiz.
- İlk pilotta LM Studio'nun şema motoru `uniqueItems` anahtarını desteklemediği için istek
  HTTP 400 ile kapandı; veri/checkpoint yazılmadı. Benzersizlik denetimi kod tarafında
  korunarak desteklenmeyen şema anahtarı kaldırıldı ve ikinci koşu başarıyla tamamlandı.
- Draft kimliği:
  `DRF_25a2b5c31856ff4a3e6d0a7edcf332df23794659e674bd0e978a84102ddbbcca`.
  İnsan özeti: `reports/section_writer_pilot_1_1.md`. `book status` artık bir aktif taslak
  ve `section_states.DRAFTED=1` gösteriyor.
- Manuel sınırlama: metin kanıta bağlıdır ancak soru bankasının genişliğini altı partide
  işlediği için tekrarlar ve 1.1 başlığına göre ikincil ayrıntılar içeriyor. Claim bağlantısı
  cümlenin tam olarak desteklendiğini tek başına kanıtlamaz; durum bu nedenle dürüstçe
  `DRAFTED_UNAUDITED` tutuldu.
- Sonuç: **İş kalemi 7 tamamlandı.** Sıradaki işlem 105 cümleyi claim metinlerine karşı
  yerel Qwen ile tek tek `SUPPORTED/PARTIAL/UNSUPPORTED` denetleyen post-writing evidence
  auditidir; ardından soru kapsam ve editoryal daraltma uygulanmalıdır.

### 2026-09-17 — Yazım sonrası cümle-kanıt auditi / İş kalemi 8

- Amaç: yazarın claim kimliği eklemesini yeterli saymadan, 1.1 ham taslağındaki her cümleyi
  bağlı gerçek canonical pasajlara karşı ikinci ve bağımsız bir Qwen geçişiyle denetlemek.
- `tunnelbookai.book.evidence_review` ve `evidence-review --section ...` uygulandı. Her
  cümle yalnızca kendi sentence-map claimleriyle değerlendirilir; destek veren belge,
  claim ve locator kimlikleri model yanıtından doğrulanarak projekte edilir.
- İlk denemede Qwen aynı partideki başka cümlenin claim numarasını seçti. Sistem eşlemeyi
  reddetti ve checkpoint yazmadı. Denetleyici hata halinde partiyi ikiye bölüp gerekirse tek
  cümleye kadar indiren fail-closed izolasyonla güncellendi; ikinci koşu tamamlandı.
- **105 / 105 cümle** denetlendi: **86 SUPPORTED**, **12 PARTIAL**, **4 UNSUPPORTED**,
  **3 NON_FACTUAL_OR_EDITORIAL**. Maddi sorun sayısı **16** ve nihai karar
  **REVISION_REQUIRED**. Bölüm status'u `DRAFTED` yerine `AUDIT_HOLD=1` gösteriyor.
- Dört desteksiz cümle: `1.1-S033`, `1.1-S034`, `1.1-S087`, `1.1-S089`. Kısmi
  cümlelerin çoğunda claim pasajını aşan genelleme, neden-sonuç veya tanıma bağlama sorunu
  bulundu. Bu sonuç manuel pilot gözlemindeki kapsam genişlemesi ve tekrar riskini doğruladı.
- Audit kimliği:
  `PSE_71c7993c2f3eee8678b11171cf121357cc9a27d5db3b33b44f8b923fb8d4c02e`.
  Sonuç: `audit/book/postwriting/PSE_71c7993c2f3eee8678b11171cf121357cc9a27d5db3b33b44f8b923fb8d4c02e/results.jsonl`;
  insan raporu: `reports/postwriting_evidence_review_1_1.md`.
- Bağımsız doğrulama: 105 benzersiz sentence ID, 105/105 JSON şema geçişi, destekleyici
  claimlerin mapped-claim altkümesi dışına çıkma sayısı **0**, destekli/kısmi olup kanıtsız
  sonuç sayısı **0**, sonuç SHA-256 ve sayaç uyuşmazlığı **0**. Hedefli testler **31/31**
  geçti; `git diff --check` temiz.
- Sonuç: **İş kalemi 8 tamamlandı.** Sıradaki işlem, 50 sorunun gerçek taslak spanları ve
  yalnızca evidence-review tarafından kabul edilen claimlerle `ANSWERED/PARTIAL/NOT_ANSWERED`
  kapsam auditidir. Sonrasında 16 maddi sorun ve editoryal tekrarlar kontrollü revizyona
  alınmalıdır.

### 2026-09-17 — 1.1 soru kapsam auditi / İş kalemi 9

- Amaç: 1.1 bölümündeki 50 dondurulmuş soruyu gerçek taslak cümle spanları ve yalnızca
  yazım-sonrası kanıt auditinde kabul edilen claim/document/locator zinciriyle ölçmek.
- `tunnelbookai.book.coverage_audit` ve `coverage-audit --section ...` uygulandı.
  `ANSWERED` yalnızca `SUPPORTED` cümlelerden verilebilir; `PARTIAL` yayın kapsamına
  eklenmez. Her `ANSWERED` sonucu gerçek section file, sentence ID, claim ID, belge ID ve
  source locator taşımak zorundadır.
- İlk koşuda Qwen `PARTIAL` denetimli spanı `ANSWERED` saymaya çalışınca sistem durdu.
  Sonraki koşuda bir `PARTIAL` kararı hiç span seçmediği için yine durdu. Güvenli ve yalnızca
  aşağı yönlü kurallar eklendi: zayıf spanlı `ANSWERED` → `PARTIAL`; spansız `PARTIAL` →
  `NOT_ANSWERED`. Sonuçları yukarı yükselten otomatik dönüşüm yoktur.
- Nihai sonuç: **32 ANSWERED**, **9 PARTIAL**, **9 NOT_ANSWERED**; bölüm kapsamı **%64**.
  Böylece 30/50 ve %60 tercih hedefi `PASS`. Ancak 16 maddi cümle-kanıt sorunu nedeniyle
  bölüm `AUDIT_HOLD` durumunda kalır; kapsam başarısı kanıt düzeltmesini geçersiz kılmaz.
- Audit kimliği:
  `QCA_567e9ff1709d3d573b69c79170576d0a65b84f5ee729950aaea394ac5de4be3e`.
  Sonuç: `audit/book/coverage/QCA_567e9ff1709d3d573b69c79170576d0a65b84f5ee729950aaea394ac5de4be3e/results.jsonl`;
  insan raporu: `reports/question_coverage_1_1.md`.
- Bağımsız doğrulama: 50 benzersiz soru, 50/50 mevcut postwriting coverage şemasından
  geçiş, 32/32 `ANSWERED` için tam traceability ve evidence-review zinciri, geçersiz
  span/claim/document/locator sayısı **0**, sayaç/hash uyuşmazlığı **0**. Hedefli testler
  **35/35** geçti; `git diff --check` temiz.
- `book status` artık bir section coverage auditi ve **50 final soru auditi** gösteriyor.
  Global yayın kapsamı doğal olarak henüz eksik: 32/2.950 = yaklaşık **%1,08**, complete
  audit `false`, publication gate `false`.
- Sonuç: **İş kalemi 9 tamamlandı.** Sıradaki işlem 1.1 bölümünde 4 desteksiz ve 12 kısmi
  cümleyi kaldıran/daraltan, tekrarları birleştiren ve bütün kanıt/kapsam auditlerini yeni
  draft hashine karşı yeniden çalıştıran sınırlı editoryal revizyondur.

### 2026-09-17 — Toplu sürümleme öncesi doğrulama

- Çalışma ağacındaki kod, yapılandırma, canonical corpus, audit ve kitap üretim çıktıları
  toplu commit öncesinde doğrulandı. Yerel geri dönüş amacıyla üretilmiş iki büyük
  `quality_failures_before_reprocess.tar` ve `upstream_before_apply.tar` arşivi toplam
  yaklaşık 2,4 GB olduğu ve yeniden üretilebildiği için silinmeden `.gitignore` kapsamına
  alındı; GitHub sürümüne dahil edilmedi.
- Tam testin tek süreçte yoğun Docling/OCR belleği biriktirmesi üzerine testler bağımsız
  paket ve modül süreçlerine ayrıldı. Book **35/35**, canonical **30/30**, dashboard
  **11 geçti + 1 atlandı**, population **15/15** ve tüm ingest modülleri ayrı ayrı geçti.
- Doğrulama sırasında yeni `corpus_search_smoke.py` ve `retrieval_benchmark.py`
  komutlarının reset mimarisi izin listesinde bulunmadığı saptandı. İki script
  `SUPPORTED_SCRIPTS` listesine, karşılıkları da sentetik reset test kurulumuna eklendi;
  hedefli mimari test **6/6** geçti.
- Dashboard Playwright uçtan uca testleri yerel port erişimiyle **8/8 geçti**.
  `git diff --check` temizdir.
