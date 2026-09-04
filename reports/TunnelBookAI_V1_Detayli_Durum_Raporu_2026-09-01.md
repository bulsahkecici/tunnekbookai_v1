# TunnelBookAI V1 — Ayrıntılı Migrasyon, Stabilizasyon ve Kalan İşler Raporu

**Rapor tarihi:** 1 Eylül 2026  
**Proje kökü:** `/Users/bulsahkecici/Projects/tunnelbookai_v1`  
**Migration kararı:** `PASS`  
**Genel corpus/üretime hazırlık kararı:** `CONDITIONAL_GO`

---

## 1. Yönetici özeti

TunnelBookAI V1 için eski Paper Crawler ve eski TunnelBookAI varlıkları tek proje altında, kaynak projeler değiştirilmeden ve silinmeden birleştirildi. Crawler'ın resumable pipeline yapısı, coverage muhasebesi, gap arama bütçeleri, handoff sınırı, provenance kontrolleri ve kitap taxonomy/question-bank kalite kapıları güçlendirildi.

Migration bütünlüğü geçmiştir: doğrulanan kaynak-hedef dosyalarında eksik veya hash uyuşmazlığı yoktur. Crawler regresyon testlerinin 97'si ve yeni eklenen 18 V1 testi geçmiştir. Kitap girdileri 59 bölüm ve 2.950 soru düzeyinde eksiksizdir.

Sistem henüz koşulsuz `GO` değildir. Bunun iki temel nedeni vardır:

1. Handoff dışındaki **890 tekil kayıt manuel inceleme kuyruğundadır**.
2. Eski 214 dokümanlık kanonik corpus için kaynak URL ve bölüm eşlemesi gibi bazı provenance ayrıntıları geçmiş veriden güvenilir biçimde yeniden üretilememiştir. Bu bilgiler uydurulmamış, açık sınırlama olarak kaydedilmiştir.

Ayrıca yeni 122 staging kaydı full-text olarak doğrulanmış değildir. Bu kayıtlar Docling/full-text kalite sürecinden geçirilmeden canonical corpus'a alınmamalıdır.

---

## 2. Başlangıçta bulunan kaynaklar

### 2.1 Paper Crawler

- Kaynak: `/Users/bulsahkecici/Projects/paper-crawler-agent`
- Git branch: `hardening`
- Kaynak HEAD: `ebe597a69ba0808621b4a1c4a7a3aff387af3985`
- Kaynak çalışma ağacı: dirty
- Taşınanlar:
  - 24 Python modülü
  - 10 crawler test modülü
  - Crawler config dosyaları
  - Requirements ve crawler README
  - Devam ettirilebilir discovery, classification, audit ve download çıktıları
- Taşınmayanlar:
  - Kaynağın `.git` dizini
  - Kaynağın `.venv` dizini
  - Cache dosyaları

### 2.2 Eski TunnelBookAI

- Kaynak: `/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI`
- Git branch: `master`
- Kaynak HEAD: `a5d5c0f1feb0cd5896e7faeb010bbaa7a0a28c22`
- Remote adında mevcut bir yazım farklılığı vardır: `_TunnelBokkAI.git`
- Kaynak çalışma ağacı: dirty
- Taşınanlar:
  - 214 kanonik Markdown dokümanı
  - Metadata ve corpus manifestleri
  - Full-Docling sidecar/chunk varlıkları
  - Scriptler, testler, config, prompts, audit ve raporlar
  - Eski testlerin ihtiyaç duyduğu seçili chunks, embeddings, evaluation, retrieval ve Qdrant fixture/depolarının çalışma kopyası
- Bilinçli olarak tam taşınmayanlar:
  - `.git` ve `.venv`
  - Model cache
  - Arşiv ve office-conversion ara depolarının tamamı
  - Geçici/generated cache içerikleri

### 2.3 Hazır kitap paketi

- Kaynak: `tunnelbookai_v1_book_inputs/book`
- Yetkili hedef: `book/`
- Hazır kitap paketi legacy `data/book` tarafından overwrite edilmedi.
- Kaynak scope ve question-bank dosyalarının SHA256 değerleri korundu.
- İki açık sekmede görülen `question_bank_integrity.json` dosyaları aynı doğrulama sonucuna sahiptir.

---

## 3. Oluşturulan birleşik mimari

| Yol | Sorumluluk |
|---|---|
| `crawler/src` | Discovery, acquisition, sınıflandırma, coverage-gap ve handoff kodu |
| `crawler/config` | Taxonomy, coverage ve crawler politikaları |
| `crawler/tests` | Crawler regresyon testleri |
| `data/downloads` | Resumable crawler çalışma alanı ve dayanıklı audit çıktıları |
| `handoff/accepted` | Handoff exporter tarafından kabul edilen paket |
| `handoff/manifests` | Üst seviye handoff manifesti |
| `handoff/review` | Manuel inceleme kuyruğu |
| `corpus/staging` | Hash/provenance kontrolünden geçen yeni adaylar |
| `corpus/canonical` | Mevcut yetkili 214 dokümanlık corpus |
| `corpus/metadata` | Canonical manifest, metadata ve provenance |
| `corpus/sidecars` | Docling/chunk yan çıktıları |
| `corpus/rejects` | Silinmeyen, ayrıştırılmış eski veya geçersiz handoff girdileri |
| `book` | Scope, question bank, QA şemaları ve kitap çalışma alanı |
| `shared` | Project quality gate ve book QA kodu |
| `audit` | Makinece okunur V1 audit sonuçları |
| `reports` | İnsan tarafından okunabilir raporlar |

Eski testlerin `data/corpus_final`, `data/metadata` ve `data/temp/full_docling_chunks` beklentileri için yeni yetkili `corpus/...` yollarına uyumluluk bağlantıları oluşturuldu. Böylece yeni mimari korunurken legacy testlerin okuma sözleşmesi mümkün olduğunca sürdürüldü.

Projenin veri büyüklükleri yaklaşık olarak:

- `crawler`: 1,1 MB
- `corpus`: 3,1 GB
- `data`: 6,3 GB
- `book`: 2,2 MB
- `handoff`: 332 MB

---

## 4. Migration kapsamında tamamlanan işler

### 4.1 Non-destructive taşıma

- Kaynak projelerde hiçbir dosya silinmedi.
- Git reset, checkout, commit veya push yapılmadı.
- İç içe `.git` deposu taşınmadı.
- Sanal ortam taşınmadı.
- Hazır kitap paketi byte-preserving olarak korundu.
- Corpus, metadata ve sidecar kritik dosyaları kaynakla SHA256 bazında karşılaştırıldı.
- Stale iki eski handoff kaydı silinmek yerine `corpus/rejects/stale_handoff` altına ayrıştırıldı.

### 4.2 Migration validator

`scripts/validate_migration.py` oluşturuldu. Validator şunları kontrol eder:

- Kaynak ve hedef kritik dosya hash'leri
- Eksik dosyalar
- Crawler kodu, testleri ve config varlığı
- Canonical corpus ve metadata varlığı
- Sidecar koruması
- Hazır kitap paketinin korunması
- İç içe Git deposu bulunmaması
- Sanal ortam taşınmaması

Son sonuç:

| Metrik | Sonuç |
|---|---:|
| Migration kararı | `PASS` |
| Envanterlenen migration dosyası | 10.134 |
| Byte/hash doğrulanan kritik dosya | 1.542 |
| Hash uyuşmazlığı | 0 |
| Eksik dosya | 0 |
| Canonical Markdown | 214 |
| Metadata dosyası | 576 |
| Sidecar dosyası | 738 |
| Book dosyası | 19 |

Makinece okunur çıktı: `audit/migration_manifest.json`.

---

## 5. Crawler'da tamamlanan stabilizasyonlar

### 5.1 Merkezi ve taşınabilir yol yönetimi

`crawler/src/project_paths.py` eklendi. Çalışma yolları proje kökünden türetilir. Eski kayıtlardaki legacy yollar hedef V1 yollarına yönlendirilir. Normal runtime kodunda kullanıcıya özgü `/Users/...` bağımlılığı kaldırıldı.

Migration validator, kaynak projeleri doğrulayabilmek için eski proje adlarını proje kökünün parent dizininden kasıtlı olarak türetir; bu runtime crawler bağımlılığı değildir.

### 5.2 Coverage muhasebesi

Coverage artık aşağıdaki sayaçları ayrı ayrı üretir:

- `discovered_count`
- `classified_count`
- `accepted_count`
- `review_count`
- `corpus_eligible_count`

Alt bölüm kayıtları parent bölümlere deterministik olarak toplanır. Böylece örneğin `5.5.1` gibi bir alt bölüm kaydı yalnız leaf'te kalmaz; `5.5` ve `5` toplamlarında da görünür.

Önceki `current=0` sorununun nedeni, gap mantığının doğrudan handoff-candidate bölüm sayımını kullanması ve parent aggregation yapmamasıydı. Metadata-only, acquisition bekleyen ve gerçek corpus-eligible kayıtların semantiği de birbirine karışıyordu. Bu ayrım düzeltildi.

### 5.3 1.193 → 1.160 farkının açıklanması

Bu fark kayıp veri değildi. Eski merge davranışı aynı DOI'ye sahip **33 duplicate kaydı** deterministik olarak birleştirmişti. Yeni reconciliation ve audit çıktılarında dedup açık metrik olarak tutulmaktadır.

### 5.4 Relevance ve review davranışı

- Weak/borderline kaynaklar doğrudan `REJECT_IRRELEVANT` yapılmıyor.
- Bu kayıtlar uygun durumda `NEEDS_REVIEW` veya `PREFILTERED` rotasına alınır.
- Explicit `handoff_candidate=false` olan kayıtlar handoff exporter tarafından reddedilir.
- `FULL_TEXT`, `ABSTRACT` ve `TITLE_METADATA_ONLY` seviyeleri ayrı tutulur.

### 5.5 Resume ve yeniden başlatma

- `--resume`: tamamlanan stage'leri tekrar çalıştırmaz.
- `--fresh-run`: checkpoint'i yeniler, mevcut indirmeleri silmez.
- `--from-stage`: seçilen stage ve downstream stage'leri yeniden çalıştırılabilir hale getirir.
- Ctrl+C durumunda pipeline `PARTIAL` olarak checkpoint bırakabilir.
- Dayanıklı download ve audit çıktıları korunur.

Son pipeline state'te aşağıdaki sekiz stage `COMPLETED` durumundadır:

1. `free_discovery`
2. `institutional_discovery`
3. `pdf_enrichment`
4. `initial_classification`
5. `gap_discovery`
6. `reclassification`
7. `source_audit`
8. `handoff`

İlk dört stage, mevcut legacy çalışmanın çıktıları doğrulanarak bootstrap edilmiştir.

### 5.6 Gap discovery maliyet ve trafik kontrolü

- Bölüm başına maksimum aday sayısı
- Bölüm başına download budget
- Acquisition öncesi metadata prefilter
- Acquisition öncesi dedup
- Sonuç üretmeyen sorgular için diminishing returns
- Sorgu ve bölüm bazında yeni ilgili kayıt metriği
- Teknik terimlerle domain anchoring

eklenmiş veya etkinleştirilmiştir.

### 5.7 Provider dayanıklılığı

- OpenAlex için sınırlı retry
- `Retry-After` desteği
- Exponential backoff
- Jitter
- Kalıcı source-health kaydı
- Provider cooldown davranışı
- Robots kararlarının hostname, karar, kontrol zamanı ve TTL/expiry ile cache edilmesi

Son kayıtlı provider durumunda OpenAlex, Crossref, Europe PMC, DOAJ, arXiv ve OpenAIRE için 48'er başarı bulunur. CORE'da üç toplam hata ve iki ardışık timeout kaydedilmiş; provider geçici cooldown'a alınmıştır. Bu davranış fail-open veri kabulü değil, provider seviyesinde kontrollü ertelemedir.

### 5.8 Taxonomy düzeltmesi

Crawler taxonomy başlangıçta scope ile tam hizalı değildi. Eksik üst ve alt bölümler eklenerek taxonomy 66 scope ID'sinin tamamıyla hizalandı. Question bank'teki 59 bölümün tümü taxonomy'de bulunmaktadır.

---

## 6. Handoff, staging ve corpus kalite kapısı

### 6.1 Handoff üretimi

- Regenerated handoff kabul sayısı: 122
- Üst manifest satırı: 122
- Staging kayıt sayısı: 122
- Manuel review queue: 890 tekil kayıt
- Explicit veya kalite kuralıyla exporter tarafından dışarıda bırakılan kayıtlar ayrıca tutulur.

`scripts/materialize_handoff.py`:

- Handoff manifestini okur.
- Kabul edilen dosyaları canonical ID bazında staging'e materialize eder.
- SHA256 ve provenance bilgisini üst manifestte tutar.
- Review kuyruğunu CSV olarak üretir.
- Eski/stale kayıtları silmeden rejects alanına ayırır.

### 6.2 Canonical corpus

- Mevcut canonical doküman: 214
- Canonical corpus'a otomatik yeni doküman eklenmedi.
- Existing canonical corpus için 214 satırlık additive provenance manifesti oluşturuldu.
- Bulunamayan legacy kaynak URL veya bölüm eşleşmesi uydurulmadı.
- Canonical dosyalarda aynı SHA'ya sahip duplicate bulunmadı.

### 6.3 Kalite kapısı sonucu

| Metrik | Değer |
|---|---:|
| Toplam classification kaydı | 1.652 |
| Discovered | 1.625 |
| Classified | 1.652 |
| Accepted | 948 |
| Bölüm atamalarındaki review sinyali | 1.279 |
| Corpus-eligible | 122 |
| Handoff-eligible | 122 |
| Manuel review queue | 890 |
| Rejected | 640 |
| Dedup removed | 88 |
| Existing canonical | 214 |
| New staging | 122 |
| Full-text | 0 |
| Abstract-only | 607 |
| Title/metadata-only | 1.045 |

`review_count=1279`, kayıtların birden fazla bölüme atanabildiği coverage toplamıdır. `review_required=890` ise üst review kuyruğundaki tekil kayıt sayısıdır; bu iki sayı aynı şeyi ölçmez.

Quality gate sonucu:

- Karar: `CONDITIONAL_GO`
- Bloklayıcı sorun: yok
- Uyarılar:
  - `legacy_canonical_provenance_has_recorded_limitations`
  - `manual_review_queue_not_empty`

---

## 7. Kitap ve soru bankası tarafında tamamlanan işler

### 7.1 Değişmez girdi bütünlüğü

`book/audits/question_bank_integrity.json` sonucu `PASS` durumundadır:

- 59 question-bank bölümü
- Her bölümde tam 50 soru
- Toplam 2.950 soru
- Duplicate question ID: 0
- Soru numarası sıralama hatası: 0
- Scope dışı yetim soru: 0
- Kaynak başlık eşleme hatası: 0
- Soru metinleri yeniden yazılmadı
- Scope kaynağındaki ellipsis/eksik başlıklar tahmin edilmedi

Kaynak hash'leri:

- Scope RTF: `59e5e61a044e8985fcef1a0d8206de73e8c34ba49b680f5a9d7c2cc355141ac2`
- Question bank DOCX: `977b899bb2a25665b527eff46913219bd0de044930bff01d5ed394f57a648ab7`

### 7.2 Dinamik book QA

`shared/book_qa.py` sabit bölüm sayısına güvenmeden scope, taxonomy ve question bank'i dinamik olarak yükler ve şunları denetler:

- Unique question ID
- Orphan section
- Section title uyumu
- Parent section ilişkisi
- Question count/index uyumu
- Source manifest hash'leri
- Taxonomy-scope-question bank kapsaması

Son taxonomy integration audit sonucu:

- Karar: `PASS`
- Scope bölümü: 66
- Question-bank bölümü: 59
- Soru: 2.950
- Duplicate/orphan/title/parent/count/hash hatası: 0

### 7.3 Chapter-level QA tasarımı

- Document coverage ve question coverage ayrı raporlanır.
- Evidence durumları `SUPPORTED`, `PARTIALLY_SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `NO_EVIDENCE` ve `NOT_EVALUATED` olarak ayrılır.
- Chapter audit; answered, partially answered, not answered, unsupported claim ve not applicable durumlarını ayrı tutar.
- Arama sorgusu olarak tam soru metni kullanılmaz; kısa teknik kavramlar çıkarılır.
- Prewriting evidence, question coverage ve postwriting chapter audit JSON şemaları oluşturuldu.

---

## 8. Çalıştırılan testler

### 8.1 Başarılı testler

| Test grubu | Sonuç |
|---|---|
| Crawler regresyon paketi | 97/97 `OK` |
| Yeni V1 book QA, quality gate ve migration testleri | 18/18 `OK` |
| Migration validator | `PASS` |
| Book taxonomy/integrity gate | `PASS` |
| Controlled public-network smoke test | `PASS` |

Toplam yeni/final deterministik test kapısı: **115 test, 115 başarılı**.

### 8.2 Kontrollü smoke test ayrıntısı

- Production crawl: hayır
- Sorgular:
  - `NATM tunnel support`
  - `road tunnel maintenance cost`
- Kaynak başına maksimum sonuç: 2
- Toplam download budget: 2
- Metadata adayı: 7
- Başarılı indirme: 1
- Sınıflandırılan kayıt: 6
- Coverage parent aggregation: başarılı
- Provider error: 0

### 8.3 Tamamlanamayan legacy test koşusu

Eski TunnelBookAI paketinde 1.395 test bulunuyordu.

İlk koşuda yeni V1 `data/...` uyumluluk görünümü henüz oluşturulmadığı için:

- 15 failure
- 451 error
- 254 skip

görüldü. Hataların büyük bölümü eski testlerin `data/chunks`, `data/embeddings`, `data/evaluation`, `data/qdrant_*` ve benzeri legacy yolları beklemesinden kaynaklanıyordu.

Gerekli uyumluluk görünümü ve fixture'lar eklendikten sonra tam paket yeniden başlatıldı. Ancak bazı legacy testler live-test flag'i olmaksızın `localhost:6333` üzerindeki Qdrant'a doğrudan erişiyor; ayrıca Qdrant client sürüm/bağlantı kontrolü uzun süre bekliyordu. Aktif Qdrant servisi olmadan koşu deterministik sürede tamamlanmadığı için güvenli biçimde kesildi.

Bu nedenle şu ifade özellikle önemlidir:

> Eski 1.395 testin tamamının V1 üzerinde geçtiği iddia edilmemektedir.

Yeni V1 için yazılan ve crawler kapsamındaki 115 test geçmektedir. Fakat legacy paket, kontrollü bir Qdrant test ortamında ayrıca yeniden çalıştırılmalıdır.

---

## 9. Yapılmayan veya bilinçli olarak çalıştırılmayan işler

### 9.1 Production crawl

Tam production crawl çalıştırılmadı. Bu, görevin güvenlik/maliyet sınırı gereğiydi. Yalnız iki sorguluk ve iki indirmelik kontrollü smoke test yapıldı.

### 9.2 Tam 2.950 soruluk LLM değerlendirmesi

Çalıştırılmadı. Soru bankası yapısal ve deterministik olarak doğrulandı; ancak her sorunun corpus kanıtıyla LLM tarafından cevaplanması/değerlendirilmesi yapılmadı.

### 9.3 Staging → canonical ingest

122 yeni staging kaydı canonical corpus'a alınmadı. Bunun nedeni:

- Yeni kayıtlarda full-text evidence sayısının 0 olması
- Abstract-only/title-only ağırlığı
- Manuel review gereksinimi
- Docling/text-quality/citation gate ihtiyacı

### 9.4 890 kaydın manuel incelemesi

Yapılmadı. Queue oluşturuldu ve korunmaktadır; karar verilmiş gibi gösterilmedi.

### 9.5 Legacy provenance'ın eksiksizleştirilmesi

Eski 214 dokümanın elde bulunmayan URL, discovery query ve bölüm eşlemeleri tamamlanmadı. Kanıtı olmayan değerler üretilmedi. Eksikler `legacy_provenance_limitations` olarak açıkça kaydedildi.

### 9.6 Eski projenin silinmesi veya otomatik arşivlenmesi

Hiçbir kaynak proje silinmedi, taşınmadı veya sıkıştırılmadı. Yalnız karar üretildi.

### 9.7 Git işlemleri

Commit, push, tag veya release oluşturulmadı.

---

## 10. Yarım kalan ve teste kalan işler

### Öncelik P0 — canonical ingest öncesi zorunlu

1. **890 review kaydını karara bağla.**
   - Accept/reject nedeni kaydedilmeli.
   - Duplicate DOI/URL/SHA kontrolleri korunmalı.
   - Weak topical similarity tek başına kabul nedeni olmamalı.

2. **122 staging kaydı için full-text acquisition yap.**
   - Robots, lisans ve erişim koşulları korunmalı.
   - PDF veya güvenilir web full text elde edilmeli.
   - İndirilemeyen kaynak abstract-only olarak açıkça işaretlenmeli.

3. **Docling/text-quality gate çalıştır.**
   - Boş/bozuk extraction
   - Çok kısa metin
   - OCR ihtiyacı
   - Kaynak dili
   - Sayfa/başlık bütünlüğü
   - Citation/provenance bağları

4. **Staging manifestini yeniden üret ve quality gate'i tekrar çalıştır.**
   - Ancak `GO` olursa controlled canonical ingest yapılmalı.

### Öncelik P1 — test ve altyapı

5. **İzole Qdrant test servisi başlat.**
   - Beklenen collection: `tunnelbook_dense_v1`
   - Legacy testlerin beklediği point count ve fixture sürümü doğrulanmalı.
   - Testler production Qdrant üzerinde çalıştırılmamalı.

6. **1.395 legacy testi yeniden çalıştır.**
   - Qdrant bağımlı testler açıkça integration/live grubu olarak ayrılmalı.
   - Varsayılan unit test discovery'sinin dış servise koşulsuz bağlanması düzeltilmeli.
   - Sonuç raporunda pass/fail/error/skip sayıları kaydedilmeli.

7. **Temiz bir V1 sanal ortamında test et.**
   - Mevcut doğrulamada eski projelerin sanal ortamları yalnız test çalıştırıcısı olarak kullanıldı; V1 içine taşınmadı.
   - Root ve crawler requirements ile sıfırdan ortam kurulmalı.
   - README komutları bu ortamda tekrar doğrulanmalı.

### Öncelik P2 — kitap üretimi

8. **Bölüm bazlı question coverage üret.**
   - Her soruya evidence status atanmalı.
   - Belgesel coverage ile soru coverage karıştırılmamalı.
   - Tam soru metni retrieval query olarak kullanılmamalı.

9. **Öncelikli coverage boşluklarını ele al.**
   - `4.1` Maliyet Kavramı, Ulaşım Maliyetleri ve İlgili Tanımlar
   - `7.1` Tünel Bakım-İşletme Maliyetleri
   - `7.2` Tünel Yapım Maliyetleri
   - `1.3.2` Türkiye'de İlk Tünel
   - `2.3` Tünellerin Yapım Maliyetine Etki Eden Unsurlar

   `5.1`, `5.2`, `5.3`, `6.1.1`, `6.1.2` ve `6.1.3` gibi amaç/kapsam/yöntem bölümleri doğrudan crawler discovery hedefi olmaktan çok chapter synthesis/evidence mapping konusu olarak değerlendirilmelidir.

10. **Pilot bölüm üretimi ve postwriting audit yap.**
    - Önce tek bir bölümle başlanmalı.
    - Unsupported claim oranı sıfır olmalı.
    - Citation ve evidence mapping doğrulanmalı.
    - Pilot başarılı olmadan 2.950 soruluk tam çalışma başlatılmamalı.

---

## 11. Arşiv kararları

### Paper Crawler: `SAFE_TO_ARCHIVE`

Gerekçe:

- Kod, config, test ve devam ettirilebilir çalışma çıktıları V1'e kopyalandı.
- Migration hash kontrolleri geçti.
- Crawler regresyonu 97/97 geçti.
- Kaynak proje değiştirilmedi.

Buradaki `SAFE_TO_ARCHIVE`, silinebilir anlamına gelmez. Özellikle dirty çalışma ağacı nedeniyle arşiv alınmadan önce kaynak repo kendi içinde ayrıca paketlenmeli veya korunmalıdır.

### Eski TunnelBookAI: `KEEP`

Gerekçe:

- Bazı raw/derived/arşiv/model-cache varlıkları migration kapsamı dışında bırakıldı.
- Legacy provenance sınırlamaları devam ediyor.
- 1.395 testlik eski paket Qdrant bağımlılığı nedeniyle henüz tam yeşil değildir.
- Eski proje karşılaştırma ve kurtarma kaynağı olarak korunmalıdır.

---

## 12. Sonraki güvenli çalışma sırası

Önerilen sıra:

1. Temiz V1 Python ortamını kur ve 115 testi yeniden doğrula.
2. İzole Qdrant fixture'ını ayağa kaldır.
3. 1.395 legacy testin tamamını yeniden çalıştır ve dış-servis testlerini unit testlerden ayır.
4. 890 review kaydını bölüm ve evidence seviyesi bazında paketlere ayır.
5. Önce en yüksek değerli küçük review paketini manuel karara bağla.
6. Kabul edilen kayıtlar için sınırlı full-text acquisition yap.
7. Docling ve text-quality gate'i çalıştır.
8. Handoff/staging manifestini yeniden üret.
9. Corpus quality gate `GO` vermeden canonical ingest yapma.
10. Tek bölümde question coverage + draft + postwriting audit pilotu yap.
11. Pilot geçerse diğer bölümlere kademeli genişlet.

---

## 13. Önemli dosyalar

### Ana dokümantasyon

- `README.md`
- `docs/architecture.md`
- `reports/tunnelbookai_v1_migration_audit.md`
- `reports/paper_crawler_stabilization_audit.md`

### Makinece okunur auditler

- `audit/migration_manifest.json`
- `audit/corpus_quality_gate.json`
- `audit/controlled_smoke_test.json`
- `audit/pipeline_state.json`
- `book/audits/question_bank_integrity.json`
- `book/audits/taxonomy_integration.json`

### Handoff ve provenance

- `handoff/manifests/handoff_manifest.jsonl`
- `handoff/review/review_queue.csv`
- `corpus/metadata/canonical_provenance.jsonl`

### Yeni kontrol kodları

- `scripts/validate_migration.py`
- `scripts/recompute_crawler_audit.py`
- `scripts/materialize_handoff.py`
- `scripts/build_canonical_provenance.py`
- `scripts/controlled_smoke.py`
- `shared/project_quality_gate.py`
- `shared/book_qa.py`

---

## 14. Nihai sonuç

Proje migrasyon ve temel stabilizasyon açısından başarıyla tamamlanmıştır. Dosya bütünlüğü, taxonomy ve question-bank yapısı ile crawler'ın deterministik test kapısı geçmektedir. Sistem, mevcut 214 dokümanlık canonical corpus'u bozmadan 122 yeni kaydı staging'e kadar güvenli biçimde getirebilmektedir.

Ancak **production-ready canonical ingest ve tam kitap üretimi tamamlanmış değildir**. Açık işler; manuel review, full-text/Docling doğrulaması, izole Qdrant ile legacy test kapanışı ve bölüm bazlı evidence/question coverage çalışmasıdır. Bu nedenle doğru nihai etiket `CONDITIONAL_GO` olarak korunmuştur.

