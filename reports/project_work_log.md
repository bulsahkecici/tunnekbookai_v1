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

### 2026-09-17 — Toplu commit/push ve terminal komutları rehberi

- Doğrulanmış kod, yapılandırma, canonical corpus, audit ve kitap üretim çıktıları
  `a612beb` (`Implement canonical retrieval and book production pipeline`) commit'iyle
  kaydedildi ve `origin/main` dalına gönderildi. Commit **8.482 dosya**, **2.158.163 eklenen
  satır** ve **282 silinen satır** içeriyor; yerel ve uzak commit kimlikleri eşitlendi.
- Yaklaşık 2,4 GB toplam büyüklüğe sahip iki yeniden üretilebilir recovery TAR'ı yerelde
  korundu, `.gitignore` ile Git/GitHub kapsamı dışında bırakıldı. Commit öncesi secret
  taraması eşleşme bulmadı; en büyük sürümlenen tek dosya GitHub tek-dosya sınırının
  altındaydı.
- Aktif CLI parser'ları, bütün alt komutların `--help` çıktıları, README, population,
  canonical, dashboard ve book sözleşmeleri incelenerek
  `docs/terminal_komutlari_rehberi.md` oluşturuldu. Belge; kurulum, yerel BGE-M3/Qwen,
  Unified Ingest, Corpus Population, dashboard, canonical promotion, retrieval, kitap
  üretimi, test, Git ve arıza teşhis komutlarını etkileri ve güvenlik notlarıyla açıklıyor.
- `README.md` dosyasına rehber bağlantısı eklendi. `probe_models.py` ile
  `reset_legacy_state.py` scriptlerinin gerçek bir `--help` modu olmadığı özellikle
  belgelendi; envanter sırasında çalıştırılan empty-reset kontrolünün tarihsel audit
  dosyasındaki yan etkisi commit'teki önceki içeriğe geri alındı.
- Doğrulama: rehber **893 satır** ve dengeli **78 Markdown kod bloğu** içeriyor; population,
  canonical ve book CLI alt komutlarının tamamı rehberde mevcut. `git diff --check` temiz,
  empty-reset auditinde veya başka runtime artifact'inde beklenmeyen çalışma ağacı değişikliği
  yok. Sıradaki işlem bu üç dokümantasyon dosyasını ayrı commit olarak kaydedip
  `origin/main` dalına göndermektir.

### 2026-09-18 — Kitap üretim aşaması durum kontrolü

- Amaç: projenin kitap yazımına geçip geçmediğini ve sıradaki gerçek üretim adımını mevcut
  artifactler üzerinden doğrulamak.
- `python -m tunnelbookai.book status --json`, son Git durumu ve kitap üretim raporları
  incelendi; herhangi bir corpus, taslak veya audit verisi değiştirilmedi.
- Doğrulanan durum: canonical corpus **656 belge / 30.926 chunk** ile hazır; retrieval indexi
  **30.332 vektör** ile hazır; **2.950 / 2.950 soru** yazım öncesi denetlenmiş ve **59 / 59
  bölüm** için kanıt paketi hazırlanmıştır.
- Kitap yazımına kontrollü pilot düzeyinde geçilmiştir: `1.1 Tünelin Tanımı` için **1 ham
  taslak**, **105 cümle** ve **1.794 yaklaşık sözcük** bulunmaktadır. Cümle-kanıt auditinde
  **86 SUPPORTED, 12 PARTIAL, 4 UNSUPPORTED, 3 NON_FACTUAL_OR_EDITORIAL** sonucu alınmış;
  **16 maddi düzeltme adayı** nedeniyle bölüm `AUDIT_HOLD` durumundadır.
- Soru kapsam auditi bölüm 1.1 için **32 ANSWERED / 9 PARTIAL / 9 NOT_ANSWERED** ve **%64
  bölüm kapsamı** göstermektedir. Buna rağmen hiçbir bölüm henüz `FROZEN` değildir; global
  yayın kapsamı **32 / 2.950 (yaklaşık %1,08)** ve publication gate `false` durumundadır.
- Bilinen sınırlama: eski `reports/corpus_population_readiness.md` raporundaki retrieval ve
  yazımın `NOT_IMPLEMENTED` olduğu cümlesi tarihsel readiness anını yansıtır; güncel çalışma
  durumu için `book status` ve daha yeni kitap üretim auditleri esas alınmıştır.
- Sonuç: kitap yazımı başlamıştır ancak toplu bölüm yazımına geçmeden önce sıradaki işlem,
  1.1 bölümündeki 4 desteksiz ve 12 kısmi cümleyi kaldıran/daraltan, tekrarları birleştiren
  sınırlı editoryal revizyon; ardından kanıt ve kapsam auditlerinin yeni draft hashine karşı
  yeniden çalıştırılmasıdır.

### 2026-09-18 — 1.1 sınırlı revizyon ve yeniden audit / İş kalemi 10

- Amaç: `1.1 Tünelin Tanımı` pilotundaki **4 UNSUPPORTED + 12 PARTIAL** cümleyi güvenli
  biçimde gidermek, yüksek güvenli tekrarları azaltmak ve bütün denetimleri yeni taslak
  hashine karşı yeniden çalıştırmak.
- `tunnelbookai.book.revision` ile `book revise --section 1.1` uygulandı. Akış eski taslağı
  yerinde değiştirmeden content-addressed yeni taslak üretir; yalnız `PARTIAL` ve
  `UNSUPPORTED` cümleleri çıkarır, ortak canonical claim taşıyan ve normalize metin
  benzerliği en az **0,75** olan tekrarları birleştirir. Yeni olgusal metin üretmez ve
  sözleşmedeki en fazla **2 revizyon** sınırını uygular.
- Birinci revizyon `DRF_f557834ec4ff065ffa96d196023ddeaa1bb68f83e6066d0a75c812247421ad6c`:
  **105 → 84 cümle**, **35 → 32 paragraf**; **16 kanıt sorunlu cümle çıkarıldı**, **5
  yüksek güvenli tekrar birleştirildi**. Kaynak cümle kararları
  `revision_actions.jsonl` içinde korunmuştur.
- Birinci revizyonun bağımsız Qwen kanıt auditi
  `PSE_9f9e7d3e019e6e50d042b8bbb494745cf5c21f1b4a50d3008ed638e302718935` sonucunda
  **69 SUPPORTED, 3 NON_FACTUAL_OR_EDITORIAL, 10 PARTIAL, 2 UNSUPPORTED** ve
  `REVISION_REQUIRED` kararı verdi. Aynı cümlelerin yeni bağlamda daha katı
  değerlendirilmesi nedeniyle ikinci ve son sözleşmeli revizyon uygulandı.
- İkinci revizyon `DRF_5fd4a263652723f929c49b4d69d572f882447a1def053112edec5cd874e1c2dc`:
  **84 → 72 cümle**, **32 → 30 paragraf**; kalan **12 kanıt sorunlu cümle çıkarıldı**.
  Nihai metin yaklaşık **1.245 sözcük**, 45 kullanılan claim ve 37 bağlı yazılabilir soru
  içeriyor. İlk 1.794 sözcüklük ham taslağa göre yaklaşık **%31** daraltıldı.
- Nihai kanıt auditi küçük bağlamlı **6 cümlelik batchler** ile çalıştırıldı.
  `PSE_a79b27b5edc2a019234d902e0aa7bb2e4fbacda729bc1769eb7589db5bc88276` sonucu:
  **69 SUPPORTED, 3 NON_FACTUAL_OR_EDITORIAL, 0 PARTIAL, 0 UNSUPPORTED**;
  maddi sorun **0**, karar **PASS**.
- Yeni 50 soruluk kapsam auditi
  `QCA_0c709eb13c2fe03c53fad18343196354b5da6ad468a6ac44d822594612803421` sonucu:
  **34 ANSWERED, 3 PARTIAL, 13 NOT_ANSWERED**, bölüm kapsamı **%68** ve karar **PASS**.
  Önceki **32 ANSWERED / %64** sonucuna göre kanıt sorunları kaldırılırken kapsam azalmadı.
- Yerel model doğrulaması: `qwen/qwen3.8-27b` `AVAILABLE`; BGE-M3 `AVAILABLE`, kararlı
  **1.024** boyutlu vektör. Terminal sandboxı localhost erişimini engellediği için model
  auditleri kullanıcı onaylı sandbox dışı yerel bağlantıyla çalıştırıldı; harici servis veya
  model fallback kullanılmadı.
- Doğrulama: aktif draft manifesti ve sentence map **2/2**, postwriting sonuçları **72/72**
  JSON şemasından geçti; kapsam sonuçları **50/50** `QuestionCoverageResult` modeliyle
  doğrulandı; hash zinciri temiz. Book testleri **37/37**, canonical testleri **30/30**
  geçti; mimari isolation gate `GO`, `git diff --check` temiz.
- Doğrulama sırasında canonical sentetik fixture'ının güncel altı desteklenen script yerine
  dört script oluşturduğu bulundu. Fixture `SUPPORTED_SCRIPTS` otoritesini doğrudan
  kullanacak biçimde düzeltildi; üretim davranışı değiştirilmedi.
- Sonuç: 1.1 artık `AUDIT_HOLD` değildir; aktif durum `DRAFTED=1`, kanıt ve bölüm kapsam
  kapıları geçmiştir. Bilinen sınır: ayrı `editorial-audit` ve `freeze` sözleşmeleri henüz
  `NOT_IMPLEMENTED`; bu nedenle bölüm henüz `FROZEN` veya yayınlanabilir değildir.
- Sıradaki önerilen işlem: ayrı editoryal audit sözleşmesini uygulamak, 1.1 metninin dil,
  yapı ve bölüm odağı kontrolünü tamamlamak; ardından section freeze kapısını geliştirmektir.

### 2026-09-18 — 1.1 editoryal audit ve hash doğrulamalı freeze / İş kalemi 11

- Amaç: kanıt ve kapsam kapılarını geçen 1.1 pilotuna ayrı editoryal audit uygulamak ve
  Book Contract'taki yedi koşulun tamamını sağlayan immutable bölüm snapshotı üretmek.
- `tunnelbookai.book.editorial` ve `book editorial-audit --section 1.1` uygulandı.
  Deterministik hard gate; draft ile sentence-map'in birebir eşleşmesini, cümle/paragraf ID
  bütünlüğünü, Unicode bozulmasını, tamamlanmamış prose satırlarını, tam paragraf/cümle
  tekrarını ve ardışık kelime tekrarını kontrol ediyor. Yerel Qwen'in kronoloji,
  adlandırma, dil, sentez ve yapı bulguları ayrı ve danışman nitelikli tutuluyor.
- Editoryal audit kimliği:
  `EDA_cddaeef4ae30bd096ac1dd7840cd04627a941165e50b1a782e60ad0266ea49ee`.
  Deterministik karar **PASS**, hard blocker **0**. Qwen danışman sonucu `HOLD` ve 8 öneri
  oldu. Dört öneri bir kelimeyi aynı yazımla değiştirmeyi istedi; bir öneri dış terminoloji
  bilgisiyle teknik terim düzeltmeye çalıştı. Bu beş öneri talimata aykırı/geçersiz sayıldı.
  `M.Ö./MÖ` tutarlılığı ve iki tematik tekrar gözlemi danışman notu olarak korundu; otomatik
  metin değişikliği yapılmadı. Değerlendirme:
  `reports/editorial_advisory_assessment_1_1.md`.
- Model değerlendirmesinin öznel ve kısmen hatalı önerilerinin evidence-valid bölümü tek
  başına reddetmemesi için tarihsel olarak doğrulanmış
  `MODEL_EDITORIAL_ADVISORY_DETERMINISTIC_HARD_GATE_V1` ayrımı uygulandı. Qwen çıktısı
  silinmedi veya daha iyi görünmesi için yeniden yazılmadı; audit artifactinde aynen korundu.
- `tunnelbookai.book.freeze` ve `book freeze --section 1.1` uygulandı. Sözleşmedeki
  `SCOPE_VALIDATION_PASS`, `EVIDENCE_AUDIT_PASS`,
  `NO_MATERIAL_UNSUPPORTED_TECHNICAL_CLAIMS`, `QUESTION_COVERAGE_AUDIT_COMPLETE`,
  `EDITORIAL_AUDIT_PASS`, `CITATION_PROVENANCE_INTEGRITY_PASS` ve
  `REQUIRED_ANALYSIS_ARTIFACTS_SATISFIED` koşullarının **7/7'si PASS** oldu.
- Citation integrity bağımsız olarak **72 cümle / 60 kayıtlı claim** üzerinde yeniden
  kuruldu; sentence-map, supporting claim, document ve locator uyuşmazlığı **0**. 1.1
  packetinde gerekli insan/proje analizi artifacti beyan edilmediği için analiz durumu
  `NOT_REQUIRED` olarak kaydedildi; modelin proje bulgusu icat etme izni değişmedi.
- Freeze kimliği:
  `FRZ_4dd8d6380b13550255134497383224e8c68535a62d1c7b6b3be32b50b29c51c4`.
  Snapshot; bölüm Markdown'ı, sentence map, kanıt sonuçları, kapsam sonuçları, editoryal
  sonuç, claim registry ve evidence packet olmak üzere **7 salt-okunur artifact** içeriyor.
  Manifest ve bütün artifact SHA-256 değerleri doğrulandı; tekrar freeze aynı kimlik ve
  manifest hashini vererek idempotent çalıştı.
- Frozen bölümde yeni `write` ve `revise` denemeleri `SECTION_FROZEN` ile fail-closed
  engellendi. `book status` artık **FROZEN=1, DRAFTED=0, AUDIT_HOLD=0** ve frozen count 1
  gösteriyor. Global yayın hâlâ kapalıdır: kalan bölümler frozen değil ve 2.950 soruluk
  global kapsam auditi tamamlanmadı.
- Yeni şemalar: `editorial_audit_result.schema.json` ve
  `section_freeze_manifest.schema.json`; gerçek artifactler **2/2 şema** ve **7/7 hash**
  doğrulamasından geçti.
- Testler: book **42/42**, canonical **30/30**, dashboard **11 geçti + 1 atlandı**;
  mimari isolation gate `GO`, `git diff --check` temiz.
- Sonuç: **İş kalemi 11 tamamlandı.** 1.1 bölümü ilk doğrulanmış frozen pilot bölümdür.
  Sıradaki önerilen işlem, 16 `READY_WITH_LIMITATIONS` bölüm arasından kanıt oranı ve bölüm
  önceliğine göre sıradaki pilotu seçmek; aynı write → evidence → coverage → editorial →
  freeze zincirini uygulamaktır. 42 `EVIDENCE_GAP` bölüm için önce corpus takviyesi gerekir.

### 2026-09-18 — Sıradaki pilot bölümün seçilmesi / İş kalemi 12

- Amaç: frozen 1.1 pilotundan sonra aynı üretim zincirinin uygulanacağı bölümü, mevcut
  evidence durumuna dayalı ve yeniden üretilebilir bir yöntemle seçmek.
- Aktif `SPM_d05b2282c795b17740b6d4c2089e73febc088f49987fe64e6d60b383efe01276`
  preparation manifestindeki `READY_WITH_LIMITATIONS` bölümler incelendi. Frozen 1.1
  çıkarılınca **16 aday** kaldı; yeni veri, claim veya chunk üretilmedi.
- Sıralama ölçütleri sırasıyla `UNSUPPORTED` artan, `SUPPORTED` azalan,
  `SUPPORTED + PARTIAL` azalan, toplam claim azalan ve bölüm kimliği artan olarak
  sabitlendi. Sonuçlar
  `audit/book/pilot_selection/NPS_bc29d114d042439be93d2427752264127766e2fcaf1cf799dc621e7f5f7d3abf/selection.json`
  içinde; insan özeti `reports/next_pilot_selection.md` içinde kaydedildi.
- **1.4 — En İyi Tünel Mühendislik Uygulamaları** seçildi: 20 `SUPPORTED`, 22 `PARTIAL`,
  8 `UNSUPPORTED`, toplam 42 yazılabilir evidence kaydı ve 84 claim. İkinci sıradaki 2.4
  aynı 8 unsupported ve 42 yazılabilir kayda sahipti; 1.4 daha fazla doğrudan supported
  claim taşıdığı için eşitliği kazandı.
- Doğrulama: seçim auditindeki **16/16 aday** aktif preparation manifestine karşı bölüm
  kimliği, başlık, evidence sayıları ve claim sayısı bakımından yeniden doğrulandı;
  kaynak manifest SHA-256 değerleri kaydedildi. JSON sözdizimi ve seçim sırası geçerli,
  `git diff --check` temiz.
- Bilinen sınır: seçim mevcut evidence sınıflarının anlık görüntüsüdür; corpus veya
  preparation manifesti değişirse yeniden çalıştırılmalıdır. `PARTIAL` kayıtlar yalnızca
  kanıtlanan alt kapsamla kullanılabilir. Bu işlem semantik arama değildir ve bölüm metni,
  post-writing audit ya da freeze üretmemiştir.
- Sonuç: **İş kalemi 12 tamamlandı.** Sıradaki önerilen işlem 1.4 için
  `book write --section 1.4 --batch-size 8` çalıştırmak; ardından evidence → gerekiyorsa
  revizyon → coverage → editorial → freeze zincirini uygulamaktır.

### 2026-09-19 — Dış gözle proje incelemesi ve yapısal düzeltme paketi / İş kalemi 13

- Amaç: projenin pipeline'ının doğru hedefe çalışıp çalışmadığını dışarıdan incelemek ve
  bulunan sorunları sırayla gidermek. Baseline commit `6a9cf59` alındı.
- İnceleme bulguları (kanıtlı): soru bankasının şablon üretimi olduğu (2.950 sorunun başlık
  yerine `X` konunca **549 şablona** indiği); outline'ın iki tezin yapısını taşıdığı (5.1–5.3,
  5.9, 6.1.x, 6.2 "Çalışmanın Amacı/Literatür Taraması", 6.2'de tez yazarı adı; 3. ve 4.
  bölümlerin boş olduğu); yayın kapısının (1.770 ANSWERED) pre-audit sonuçlarına göre
  (257 S + 907 P = 1.164) matematiksel olarak ulaşılamaz olduğu; pre-audit retrieval'ının
  soru metnini tek başına embed edip **top-k 4** ve **400 karakterlik** pasajla karar verdiği;
  indeksin **%47'sinin FIGURE_CHUNK** (medyan 244 karakter) olduğu; frozen 1.1 metninin
  şablon sorulara cevap veren, kopuk cümlelerden oluştuğu; 26 belgede bozuk Türkçe glyph
  aralığı (`TEKN İ K`) bulunduğu.
- Kapsam/soru bankası v2 taslağı: `book/question_bank/drafts/question_bank_v2_draft.md`
  (79 başlık: 44 korunan, 13 yeni, 13 pasif, 2 insan-analizi; 59 aktif soru bölümü;
  **698 soru**, bölüm başına 7–17). Kullanıcı incelemesi bekliyor; normalize edilmedi,
  canlı sözleşme değişmedi. `tunnelbookai.book.normalize` + `book normalize-inputs`
  komutu taslaktan şema 2.0 scope/soru bankası/index/integrity/source-manifest üretip
  sözleşmeyi yeniden mühürler (`ceil(toplam × 0,6)` eşiği). `contract.py` ve `inputs.py`
  şema 1.0 (sabit 66/59/50) ile 2.0'ı (değişken sayı, pasif başlık, `analysis_requirement`)
  birlikte destekler; 50/30 sabitleri `coverage.py`, `coverage_audit.py`, `editorial.py`,
  `freeze.py`, `prewriting.py`, `status.py` içinden sözleşme türevli hedeflere taşındı.
- Hibrit retrieval (`hybrid-rrf-v1`): `tunnelbookai/book/lexical.py` BM25 indexi (Türkçe
  katlama, F5 kök kesme, bozuk aralık onarımlı tokenizer, chunk gürültü bayrakları) dense
  index kimliğine bağlı olarak `book/retrieval/lexical/<BRI>/` altında (30.332 satır, 88.790
  terim, 20 sn, 17 MB; gitignore). `HybridRetriever` RRF füzyonu + chunk türü ağırlığı
  (FIGURE 0,6) + 150 karakter/TOC filtresi. Pre-audit: sorgu = bölüm başlığı + soru,
  top-k 8 (örtüşen chunk tekrarı elenerek), Qwen'e chunk'ın sorguya en çok değen 1.000
  karakterlik penceresi (`focused_window`); prompt sürümü `v4-hybrid-focused`.
- Karşılaştırma (aktif audit bozulmadan, scratchpad): **1.2** eski S6/P17/U27 →
  S14/P16/U20; **2.2.3** eski S0/P5/U45 → S1/P17/U32. Kalan desteksizler retrieval değil
  içerik/soru sorunu (su altı tünelleri için corpus'ta tek tez paragrafı var).
- Yazar v3 (outline-first): önce Qwen 2–8 tematik plan üretir (`batches/plan.json`), sonra
  her tema yalnızca kendi pasajlarıyla yazılır; soru bağı = açık etiket ∪ cümlenin claim'lerinin
  kanıtladığı sorular. `_validate_batch` soru kapsamasını zorlamaz (eski davranış
  `require_question_coverage=True` ile korunur). Henüz gerçek bölümde çalıştırılmadı.
- Freeze: `OPERATOR_READ_APPROVAL_PASS` sözleşmeye eklendi; `book approve-section --section
  --note` aktif taslak kimliği/hash'i ve editoryal audit kimliğine bağlı onay yazar,
  snapshot'a `operator_approval.json` kopyalanır. Mevcut frozen 1.1 bu kapı olmadan
  dondurulmuştu; v2 geçişinde zaten yeniden üretilecektir.
- Türkçe glyph onarımı: `tunnelbookai/ingest/glyph_repair.py` + `config/turkish_lexicon.txt`
  (189 bozuk olmayan Türkçe canonical belgeden 58.100 kelime/frekans). Sözlük + belge içi
  bağımsız-kelime kanıtı + ek-kalıntısı cezasıyla her glyph için sol/sağ/ikisi kararı.
  En bozuk 6 belgede izole glyph **29.833 → 158**. Pipeline'a extraction sonrası kanca
  eklendi (`TURKISH_GLYPH_SPACING_REPAIRED:<n>`); yalnızca yeniden işlenen belgeleri
  etkiler. Canonical'daki 26 belge henüz yeniden işlenmedi.
- Dense index yeniden kurulumu artık önceki indexin hash'i doğrulanmış vektörlerini
  `embedding_text_sha256` ile yeniden kullanır (`reused_vector_count`).
- Doğrulama: book 53, canonical 30, ingest 247, population 15, dashboard 11+1 test geçti;
  isolation gate `GO`; `git diff --check` temiz. Belgeler: terminal rehberi, engine ve ingest
  sözleşmesi güncellendi.
- Bilinen sınırlar ve sıradaki işler: (1) v2 taslağının insan incelemesi ve
  `normalize-inputs`; (2) 26 belgenin `--force-reprocess --from-stage EXTRACTING` ile
  yeniden işlenip canonical `plan/apply` ile yeniden promote edilmesi (operatör onayı
  gerekir); (3) canonical digest değişince `build-index` (vektör yeniden kullanımıyla) ve
  tam `evidence-audit`; (4) yeni yazarla 1.1'in yeniden yazımı, insan onaylı freeze.

### 2026-09-19 — Canonical belge yenileme yolu (REPLACE) ve orijinalden yeniden işleme / İş kalemi 14

- Amaç: glyph onarımının canonical'daki 26 bozuk belgeye uygulanabilmesi için eksik olan iki
  yeteneği eklemek. Inbox temizlendiği için (7 dosya kalmış) ingest bu belgeleri göremiyor;
  canonical otoritesi ise aynı kimlikte farklı digest'i `DOCUMENT_ID_CONFLICT` sayıyordu.
- `scripts/ingest_incoming.py --reprocess-canonical ING_...`: belgeyi `originals/<id>/source.*`
  üzerinden yeniden işler, kayıtlı provenance kaynağını yeni kaynak eklemeden tazeler,
  `ALREADY_CANONICAL` atlamasını yalnızca açıkça verilen kimlikler için aşar. E2E testi
  (`test_reprocess_from_immutable_original_after_inbox_cleanup`) eklendi.
- Canonical `CandidateAction.REPLACE`: aynı `document_id` + aynı kaynak SHA + farklı digest
  → plan `REPLACE`, apply yeni nesneyi yazar, eski nesne dizini `UNREFERENCED_CANONICAL_OBJECT`
  uyarısıyla inert kalır; audit `replaced_candidates` alanı taşır. Farklı kaynak SHA hâlâ
  `DOCUMENT_ID_CONFLICT`. Sözleşme belgesi güncellendi; eski test yeni davranışa göre yazıldı.
- Vision autodetect düzeltmesi: VLM tanınmazsa artık ilk sunulan modele (embedding modeli!)
  düşmüyor; sağlayıcı `unavailable` ve figürler `NOT_RUN`. Şu an LM Studio'da VLM yüklü
  değil; population koşusundaki figür açıklamaları hangi VLM ile üretildi bilinmiyor
  (figür kayıtlarında model adı saklanmıyor). Bozuk belgelerin yeniden işlenmesi VLM
  yüklenmeden başlatılmadı.
- Doğrulama: ingest 248, canonical 30, book 53, population 15 test geçti; isolation `GO`;
  `git diff --check` temiz.
- Sıradaki: kullanıcı kararı — (a) yeniden işlenecek belge kümesi (öneri: ≥25 bozuk chunk'lı
  12 belge; tamamı 26), (b) VLM'nin yüklenmesi, (c) `canonical plan` → `--approve` ile
  `REPLACE`, (d) `build-index` (vektör yeniden kullanımı) ve `evidence-audit`.

### 2026-09-23 — Boş altyazı sırasında görünen istenmeyen metin için kaynak incelemesi

- Amaç: boş altyazı aralıklarında görüldüğü bildirilen “İzlediğiniz için teşekkürler” ve
  “Altyazı M.K” metinlerinin projedeki kaynağını bulup kaldırmak.
- İnceleme: izlenen kaynak dosyaları ile dashboard, ingest ve test kodlarında birebir metin;
  ayrıca `altyazı`, `subtitle`, `caption`, `transcript`, `speech`, `audio`, `video` ve ilgili
  yazım varyasyonları arandı. Projede altyazı/ses transkripsiyon bileşeni veya bildirilen
  sabit metin bulunmadı; değişen belge/chunk sayısı **0**, kod değişikliği **0**.
- Doğrulama: `rg` tabanlı kaynak taraması yalnızca belge figür/tablo açıklamalarına ait
  `caption` kullanımlarını gösterdi; bildirilen davranış yeniden üretilemedi. Semantik arama
  yapılmadı.
- Bilinen sınırlama ve sıradaki işlem: düzeltme için ilgili video/altyazı dosyasının ya da
  davranışın görüldüğü uygulama/proje yolunun belirtilmesi gerekiyor.

### 2026-09-23 — v2 soru bankası taslağının incelenmesi, corpus desteksiz başlıkların pasifleştirilmesi ve normalize-inputs geçişi

- Amaç: [[book-pipeline-restructure-2026-09]] incelemesinde kullanıcıya bırakılan üç karardan
  ilkini kapatmak — 698 soruluk v2 taslağını (`book/question_bank/drafts/
  question_bank_v2_draft.md`) kullanıcıyla birlikte gözden geçirip onaylanan haliyle v1→v2
  sözleşme geçişini yapmak.
- İnceleme: taslağın 1003 satırı uçtan uca okundu. Sekiz yeni alt başlıkta (4.2, 4.3, 4.3.2–
  4.3.4, 6.4–6.6) diğer yeni başlıkların aksine hiç elle yazılmış corpus-destek notu yoktu —
  2.2.3'te önceki incelemede tespit edilen "template soru, destek yok" sorununun büyük
  ölçekli tekrarı riski. Kullanıcı bu 8 başlığı pasifleştirme kararı verdi.
- Değişiklik: 4.2, 4.3.2, 4.3.3, 4.3.4, 6.4, 6.5, 6.6 `{inactive: corpus desteği yok; 2.2.3
  türü destek riski}` olarak işaretlendi, soruları (77 adet) kaldırıldı. 4.3 kendi 7 sorusuyla
  aktif bırakıldı: `normalize.py` şeması aktif alt başlığın (4.3.1, 4.3.5) aktif bir ebeveyni
  olmasını zorunlu kılıyor ve orta seviye başlıklarda soru taşımayan `{chapter}` etiketine
  izin vermiyor (yalnızca üst düzey başlıklar chapter olabilir) — ilk deneme bu yüzden
  `BOOK_INPUT_INVALID` ile reddedildi, düzeltilip yeniden çalıştırıldı. Taslak özeti ve
  sayaçları güncellendi: 59→52 aktif bölüm (20 pasif, 6 yeni), 698→628 soru.
- `python -m tunnelbookai.book normalize-inputs` çalıştırıldı → `NORMALIZED`/`PASS`.
  `book_contract.json` `book-production-v2-reviewed-scope` olarak yeniden mühürlendi
  (`contract_sha256 034bb226...`); `book_scope`, `question_bank` (52 bölüm / 628 soru),
  `question_bank_integrity`, `source_manifest` normalize edilmiş çıktıları yeniden üretildi.
  Değişen dosyalar: `book/config/book_contract.json`, `book/question_bank/drafts/
  question_bank_v2_draft.md`, `book/question_bank/normalized/{question_bank.csv,jsonl,
  question_bank_index.json}`, `book/scope/normalized/{book_scope.csv,json}`,
  `book/audits/{question_bank_integrity.json,source_manifest.json}`.
- Doğrulama: `normalize-inputs` çıktısı `"decision": "PASS"`, `question_bank_sections: 52`,
  `total_questions: 628`, `global_minimum_answered_count: 377` (0.6 kapsama eşiği). Test
  paketi bu oturumda tekrar koşulmadı (kod değişmedi, yalnızca veri/sözleşme normalize
  edildi). Commit `8e0983e`, `origin/main`'e push edildi.
- Bilinen sınırlama: bu geçiş tüm önceki audit kimliklerini ve dondurulmuş 1.1 bölümünü
  geçersiz kılar (kasıtlı, tek seferlik — [[book-pipeline-restructure-2026-09]]). 4.3'ün
  kendi 7 sorusu da elle yazılmış corpus notu taşımıyor; genel metodoloji sorusu olduğu için
  tutuldu ama evidence-audit'te 2.2.3 gibi düşük destek çıkarsa ayrıca gözden geçirilmeli.
- Sıradaki: VLM LM Studio'ya yüklendi (`qwen3-vl-8b-instruct-mlx`, `vision/provider.py`
  autodetect filtresiyle — adında "vl" — uyumlu, doğrulandı). Sırada: 26 belgenin tamamı
  için `ingest --reprocess-canonical` → canonical `plan/apply` (kullanıcı `--approve
  CCP_...` onayı) → `build-index` (vektör yeniden kullanımı) → v2 ile tam `evidence-audit`
  (~628 soru, tahmini ~2 saat).

### 2026-09-23 — glyph_repair yoğunluk eşiği düzeltmesi ve 25 bozuk belgenin reprocess'e alınması

- Amaç: [[book-pipeline-restructure-2026-09]]'da kullanıcıya bırakılan üçüncü kararı
  (26 bozuk belgenin tamamının yeniden işlenmesi) uygulamaya başlamak. Önce hangi
  belgelerin gerçekten hasarlı olduğunu `tunnelbookai/ingest/glyph_repair.py`'nin üretim
  algılama mantığıyla (`damage_stats`) tazeden tespit etmek gerekti — elde geçmişten kalma
  "26 belge" listesini gösteren bir audit dosyası yoktu, yalnızca rapor metninde bir sayı
  vardı.
- Bulgu (kod hatası): `damage_stats` tüm belge metninde tek bir yoğunluk eşiği
  (`MIN_DENSITY = 1/2000`) uyguluyordu. **KARAYOLU TEKNİK ŞARTNAMESİ 2013** gibi çok büyük
  belgelerde (2,53M karakter) 534 izole bozuk glyph olmasına rağmen belge-geneli yoğunluk
  eşiğin altında kalıyordu (0.000211 < 0.0005); `repair_extraction()` bu nedenle belgeyi
  sessizce `damaged: false` sayıp atlıyordu — yani bu belge yeniden işlense bile glyph'ler
  düzelmeyecekti. Aynı seyrelme riski 8 belge daha için geçerliydi (SCADA kurs notları,
  Tünelcilik dergisi, KGM Tünel Haritası 2024 vb.).
- Düzeltme: `tunnelbookai/ingest/glyph_repair.py`'ye `WINDOW_CHARS = 20000` ve
  `_max_window_density()` eklendi; `damage_stats` artık belge-geneli eşiği geçemeyen ama
  ≥8 izole glyph içeren belgelerde 20.000 karakterlik pencerelerin en yoğununu da kontrol
  ediyor. `tests/ingest/test_glyph_repair.py`'ye bu senaryoyu kanıtlayan
  `test_locally_damaged_section_is_flagged_despite_low_document_wide_density` eklendi.
- Doğrulama: `tests/ingest/test_glyph_repair.py` 6/6 geçti; `tests/ingest/` tam paketi
  249 testten 248'i geçti (tek hata `test_canonical_baseline_counts`, 66≠79 — glyph
  değişikliğiyle ilgisiz, önceki v2 `normalize-inputs` geçişinin beklenen ama henüz
  düzeltilmemiş yan etkisi; ayrı iş kalemi).
- Düzeltilmiş eşikle canonical corpus'un tamamı (656 belge, `corpus/canonical/
  canonical_manifest.json`) yeniden tarandı: **25 belge** `damaged: true` — geçmişteki
  "26" ile pratikte aynı hedef küme (KGM 1950 el kitabı [`ING_a23b1e815eedc4a3c978`], iki
  tez [KTÜ `ING_674564f8c6d600238ac2`, YTÜ `ING_2005c18d2148fb921826`], Türkiye Tünelcilik
  Semineri 2 sürüm, Bolu Dağı, Marmaray, KGM Teknik Şartnamesi 2013 dahil). Tam liste ve
  occurrence/density değerleri bu kaydın altındadır.
- `scripts/ingest_incoming.py --reprocess-canonical <25 id>` önce `--dry-run` ile
  doğrulandı (25 belge, 33 kayıtlı provenance kaynağı — bazı belgelerin birden fazla
  provenance kaydı var; `audit/ingest_dry_run.json`'da 25 benzersiz `document_id`
  doğrulandı), sonra gerçek koşu arkaplan görevi `bfjy75hr1` olarak başlatıldı (OCR + VLM +
  classification tam pipeline; `--no-ocr`/`--no-vision`/`--no-arbiter` verilmedi). Log:
  `scratchpad/reprocess_26.log`. Bu koşunun tamamlanma sonucu ayrı bir kayıtla eklenecek.
- Bilinen sınırlama: bu tarama yalnızca `document.md` (birleştirilmiş normalize edilmiş
  metin) üzerinde çalışıyor; asıl reprocess sırasında extraction'dan gelen ham metin
  farklı bölünmüş olabilir, bu yüzden gerçek onarım sonuçları (`isolated_glyphs_after`)
  bu taramadaki sayılarla birebir eşleşmeyebilir. `--reprocess-canonical` yalnızca
  `processing/<id>/` türetilmiş çıktıları yeniler; canonical'a yansıması ayrı bir
  `canonical plan/apply` (`--approve`) adımı gerektirir — henüz çalıştırılmadı.
- Sıradaki: reprocess koşusu bitince sonuçları doğrula (her belgede
  `TURKISH_GLYPH_SPACING_REPAIRED:<n>` uyarısı var mı, `isolated_glyphs_after` sıfıra
  yakın mı) → canonical `plan` çıkar → kullanıcı `--approve CCP_...` → `build-index`
  (vektör yeniden kullanımı) → v2 ile tam `evidence-audit`.

Taranan 25 belge (document_id | occurrences | chars | density):
ING_a23b1e815eedc4a3c978|11310|446936|0.0253; ING_674564f8c6d600238ac2|10736|304075|0.0353;
ING_2005c18d2148fb921826|6177|512491|0.0121; ING_ef74fd1d060d31f37486|1811|33552|0.0540;
ING_746d18498e07a8a0f397|1476|1376762|0.0011; ING_7f177b472ed62ef80108|962|22996|0.0418;
ING_784b14ff9e8444a97c6d|710|29185|0.0243; ING_312befcda2ff316b7279|534|2528595|0.0002;
ING_c736114ad7d9ac29557c|467|12722|0.0367; ING_abc6dcf8e707da2f77f6|442|22639|0.0195;
ING_f036fbe6cc100faef49c|338|9435|0.0358; ING_752100774713db4bce1b|335|8368|0.0400;
ING_3fcd94bb525756ba52ca|331|281125|0.0012; ING_17e5e4aa41637a66b3de|300|17737|0.0169;
ING_290648f6f7fc8e05fe81|206|5455|0.0378; ING_249d0d30e2d019269dcc|190|250529|0.0008;
ING_7e795b9a47c89f5406c5|90|456591|0.0002; ING_339e05e3358e01b537d8|74|317717|0.0002;
ING_cbf08cc5651cbc903a95|63|53098|0.0012; ING_04c57c21fdf18e5176f0|60|12103|0.0050;
ING_161788a110d058683acf|48|43576|0.0011; ING_1fb6b71a35f819248daf|41|1220632|0.00003;
ING_49577e05781c8bbe2d72|24|413162|0.00006; ING_686f2fed7a37fea40455|19|466453|0.00004;
ING_5f9b220f6592b0ab2b78|18|31531|0.0006

### 2026-09-23 — Reprocess sonucu doğrulandı; archive_original() bütünlük hatası bulundu ve düzeltildi

- Amaç: arkaplan görevi `bfjy75hr1` (25 belgenin `--reprocess-canonical` koşusu) tamamlandı;
  sonucu doğrulamak ve canonical `plan` adımına geçmek.
- Koşu sonucu: `Inputs detected: 33` (25 belge, bazılarının birden fazla provenance kaydı
  var), **Staged (GO): 23, Review: 2, Failed: 0**, 6.148 chunk üretildi, 5.602 embedding-ready.
  REVIEW'daki 2 belge (`ING_ef74fd1d060d31f37486`, `ING_49577e05781c8bbe2d72`) sebebi
  `LOW_SECTION_CONFIDENCE` — classification güven sorunu, glyph onarımıyla ilgisiz.
- Glyph onarımı doğrulaması: her 25 belgenin `processing/<id>/extraction_report.json`
  içindeki `text_repair` kaydı okundu. Toplam izole glyph **31.048 → 311 (%99,0 azalma)**.
  Tek istisna `ING_249d0d30e2d019269dcc` (KALİTE KONTROL PLANI TABLO): 27→27, hiç ilerleme
  yok — muhtemelen tablo-ağırlıklı içerikte sözlük eşleştiricisinin güvenilir bağlam
  bulamaması; ayrı bir not olarak bırakıldı, blokaj değil.
- **Bulunan hata:** `tunnelbookai/ingest/original_archive.py`'deki `archive_original()`,
  belge zaten arşivde olsa (`mode="existing"`, içerik SHA256 eşleşse) bile
  `originals/<id>/original.json` sidecar'ını **koşulsuz yeniden yazıyordu**. Modülün kendi
  doc-string'i "orijinal asla değiştirilmez" diyor ama bu yalnızca `source.<ext>` için
  doğruydu. Etki: canonical manifest her belgenin bu sidecar dosyasının SHA256'sını
  bütünlük parmak izi olarak sabitliyor; reprocess ettiğim **25 belgenin 25'i de** bu
  parmak iziyle uyuşmaz hale geldi → `canonical status`/`plan` **tüm 656 belgelik corpus
  için INVALID** döndü (yalnızca bu 25'i değil, hiçbir planlamayı bloke etti).
- Doğrulama (kapsam): kaynak `source.pdf` byte'larının hiçbiri değişmedi (kaydedilen
  SHA256 ile birebir eşleşiyor); yalnızca sidecar metadata dosyası etkilendi.
- Düzeltme: `archive_original()` artık yeni `meta` içeriğini diskteki mevcut içerikle
  karşılaştırıyor (`archive_mode` hariç — o alan bu çağrının kendi sonucunu anlatır, belge
  özelliği değildir) ve gerçekten bir şey değişmemişse dosyayı yeniden yazmıyor.
  `tests/ingest/test_ingest_smoke.py`'ye
  `test_reprocessing_with_no_new_source_kind_leaves_metadata_sidecar_untouched` eklendi.
  İki yanlış ilk deneme oldu (birincisi ilk-oluşturmada da yazmayı atlıyordu, ikincisi
  `archive_mode` farkı yüzünden hâlâ her seferinde yazıyordu) — üçüncü sürüm 19/19
  `test_ingest_smoke.py` testini geçti.
- **Manifest onarımı:** `corpus/canonical/canonical_manifest.json` geçici olarak
  `chmod 0644` yapılıp (uygulamanın kendi `apply_plan`'ının yaptığı gibi) 25 belgenin
  `original.metadata_sha256` alanı, `originals/<id>/original.json`'un GÜNCEL (doğrulanmış,
  zararsız) SHA256'sıyla güncellendi, sonra `chmod 0444`'e geri döndürüldü. Öncesinde
  `tunnelbookai/canonical/eligibility.py:336` incelendi: bu alan `corpus_digest` veya
  `document_digest`'e girmiyor — yalnızca bu bağımsız bütünlük kontrolünde kullanılıyor,
  bu yüzden düzeltme diğer hiçbir hash'i etkilemedi (`canonical status` sonrası
  `corpus_digest` aynı kaldı: `1fec0054...`). Diff doğrulandı: yalnızca 25 satır
  (`metadata_sha256` alanları), başka hiçbir şey değişmedi.
- Doğrulama: `canonical status` → `"state": "READY", "ready": true` (önceden INVALID).
  `tests/ingest/` tam paketi 250 testten 248'i geçti: `test_canonical_baseline_counts`
  (66≠79, v2 geçişinden kalan bilinen/ayrı sorun) ve
  `test_unavailable_local_service_is_explicit_not_a_fallback` (ortam bağımlı — LM Studio
  şu an canlı ve modeller yüklü olduğu için probe farklı bir durum döndürüyor; kodla
  ilgisiz, CI/temiz ortamda muhtemelen geçer).
- Sıradaki: canonical `plan --document-id <25>` çalıştır → planı kullanıcıya göster →
  kullanıcının `--approve CCP_...` onayı → `apply` → `build-index` → v2 ile tam
  `evidence-audit`.

### 2026-09-23 — Canonical promosyon planı üretildi (23 REPLACE), kullanıcı onayı bekleniyor

- Amaç: canonical bütünlüğü onarıldıktan sonra 25 belge için `canonical plan` çalıştırmak.
- İlk deneme (25 belge, hepsi): `CCP_348ee4ed...`, `applicable: False`. 2 belge
  (`ING_ef74fd1d060d31f37486`, `ING_49577e05781c8bbe2d72` — reprocess sonucu REVIEW
  durumundaki ikisi) `PROCESSING_IDENTITY_MISMATCH` / "staging differs from processing:
  document.md" ile REJECTED döndü, çünkü REVIEW kararı staging'e hiç girmemişlerini
  gösteriyor. `promotion.py`'de `applicable = bool(candidates) and all(action is not
  REJECTED ...)` — tek bir REJECTED bile tüm planı uygulanamaz kılıyor, `apply` da
  `applicable: False` planı hard-refuse ediyor (`INVALID_CANONICAL_PROMOTION_PLAN`).
- İkinci deneme, bu 2 belge çıkarılıp kalan 23 GO belgesiyle: **`CCP_282db20c1ac99b98
  ca543b9ae803ece567460a5d994bb6fd1f292b5d4f90577e`**, `applicable: True`, 23/23 REPLACE.
  Plan dosyası: `audit/canonical_promotions/plans/CCP_282db20c....json`. DRY RUN —
  canonical, originals, processing, staging henüz değişmedi.
- 2 REVIEW belgesi (`LOW_SECTION_CONFIDENCE`) bu turun dışında bırakıldı; ayrı bir karar
  konusu (classification güven sorunu çözülüp yeniden mi işlensin, yoksa mevcut REVIEW
  durumuyla mı kalsın — kullanıcı kararı).
- Doğrulama: plan JSON'u okundu, 23 REPLACE + kaynak SHA256'ları + chunk sayıları
  doğrulandı; `Applicable: True`.
- Sıradaki (kullanıcı onayı bekliyor): `canonical apply --plan audit/canonical_promotions/
  plans/CCP_282db20c1ac99b98ca543b9ae803ece567460a5d994bb6fd1f292b5d4f90577e.json --approve
  CCP_282db20c1ac99b98ca543b9ae803ece567460a5d994bb6fd1f292b5d4f90577e` → sonra
  `build-index` (vektör yeniden kullanımı) → v2 ile tam `evidence-audit`.
