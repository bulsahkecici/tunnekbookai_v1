# TunnelBookAI Agent Rules

Bu dosya TunnelBookAI projesi için sürekli geçerli kuralları tanımlar.

Amaç:
Yerel, kanıta dayalı, izlenebilir ve fail-closed çalışan teknik kitap üretim sistemi.

---

## 1. DİL

Kullanıcı aksi yönde istemedikçe Türkçe cevap ver.

Kitap metni:
- profesyonel
- teknik
- doğal
- okunabilir Türkçe olmalıdır.

---

## 2. PRIVACY — LOCAL ONLY

TunnelBookAI private içerikleri LOCAL ONLY işlenmelidir.

Şunları hiçbir cloud LLM servisine gönderme:

- canonical corpus
- kaynak PDF/DOCX/PPTX içerikleri
- canonical Markdown
- chunks
- evidence packets
- claim kayıtları
- kitap taslakları
- provenance içeriği
- private metadata

LLM endpoint yalnızca loopback olmalıdır:

- 127.0.0.1
- localhost
- ::1

Şunlara private içerik gönderme:

- OpenAI cloud API
- Anthropic
- DashScope
- Alibaba cloud
- Gemini API
- başka remote LLM servisleri

Local model ulaşılamıyorsa:

FAIL CLOSED.

Cloud fallback kullanma.

---

## 3. WEB VE DIŞ API KULLANIMI

Private corpus işleme sırasında web kullanma.

Açık akademik kaynak keşfi için yalnızca kullanıcı açıkça izin verdiğinde şu servisler kullanılabilir:

- OpenAlex
- Crossref
- DOAJ
- Europe PMC
- Unpaywall

Private corpus içeriğini bu servislere gönderme.

---

## 4. SOURCE OF TRUTH

Canonical corpus ve orijinal kaynak belgeler source of truth'tur.

Şunlar tek başına evidence değildir:

- AI summary
- literature note
- model hafızası
- pretrained knowledge
- internetten hatırlanan bilgi
- inference

AI-generated literature notes yalnızca triage için kullanılabilir.

---

## 5. EVIDENCE FIRST

Her teknik iddia gerçek evidence ile desteklenmelidir.

Topical similarity evidence support değildir.

Bir claim için ayrı ayrı değerlendir:

- support
- scope
- provenance
- locator
- authority
- source type
- qualifier
- section applicability

Evidence yoksa bilgi uydurma.

Gerekirse şu statülerden birini kullan:

- EVIDENCE_NOT_READY
- UNRESOLVED
- TRUE_CORPUS_EVIDENCE_GAP

---

## 6. FROZEN PIPELINE

Kullanıcı açıkça istemedikçe şunları değiştirme:

- canonical corpus
- frozen chunks
- embeddings
- Qdrant collection
- frozen retriever
- frozen prompt
- validator criteria
- global book structure

Kitap yazımı sırasında Qdrant read-only kabul edilir.

Retriever ayarlarını sonucu iyileştirmek amacıyla sessizce değiştirme.

---

## 7. FAIL-CLOSED

Bir işlem doğrulanamıyorsa başarılıymış gibi davranma.

Şunları yapma:

- hallucinated repair
- unsupported rewrite
- invented citation
- invented source
- invented standard
- invented page number
- invented result
- invented test result

Validator veya acceptance kriterlerini sonucu geçirmek için zayıflatma.

Aynı hatalı config ile anlamsız retry döngüsüne girme.

---

## 8. CLAIM RULES

Claim'ler mümkün olduğunca atomic olmalıdır.

Her claim için mümkün olduğunda koru:

- document_id
- source path
- page / locator
- scope
- qualifier
- source type
- authority state
- support state
- section applicability

İki farklı cümleyi daha güçlü tek bir sentetik claim haline getirme.

Scope-invalid claim'i konu benzerliği nedeniyle kabul etme.

UNKNOWN authority tek başına otomatik ret sebebi değildir; proje admission politikasına göre LIMITED olarak değerlendirilebilir.

---

## 9. BOOK SECTION BOUNDARIES

Her bölüm yalnızca kendi scope'u içinde yazılmalıdır.

Sonraki bölümlere taşma.

Örneğin CH-A-S01 — Tünelin Tanımı bölümünde:

Yazılabilir:
- tünelin temel tanımı
- yeraltı / kapalı mühendislik niteliği
- temel işlev
- ulaşım / altyapı işlevi
- çevre zemin / yapı ilişkisine sınırlı giriş

Yazılmamalı:
- detaylı sınıflandırma
- tarihçe
- NATM
- TBM
- destek sistemleri
- detaylı jeoteknik
- maliyet
- bakım
- yangın
- kazalar

---

## 10. WRITING RULES

Kitap yazarı yeni bilgi üretmez.

Görev:

verified evidence
->
coherent Turkish technical prose

Kurallar:

- Evidence packet dışından factual bilgi ekleme.
- Kaynaktaki qualifier'ları koru.
- Teknik ifadeleri güçlendirme.
- Aynı claim'i farklı kelimelerle tekrar ederek metni uzatma.
- Evidence sınırlıysa metni kısa tut.
- Hedef kelime sayısı evidence'dan daha önemli değildir.
- Internal evidence ID'lerini public citation olarak kullanma.
- Citation yalnızca gerçekten desteklediği iddiaya bağlanmalıdır.

---

## 11. STYLE

Kitap metni:

- teknik kitap diliyle
- doğal paragraf akışıyla
- gereksiz madde listeleri olmadan
- akademik ama okunabilir biçimde
- tekrar etmeyen yapıda yazılmalıdır.

Aşağıdaki ifadeleri gereksiz tekrar etme:

- "kaynaklara göre"
- "eldeki verilere göre"
- "bu bölümde"
- "mevcut literatürde"

---

## 12. TOOL VE REPO DİSİPLİNİ

Gereksiz tüm-repo taraması yapma.

Önce hedefi belirle.

Sonra yalnızca gerekli dosyaları oku.

Kaçın:

- find .
- grep -R /
- gereksiz recursive ls
- tüm corpus'u modele yükleme

Kod değişikliğinde:

- önce ilgili dosyayı oku
- minimum değişiklik yap
- unrelated refactor yapma
- test çalıştırıldıysa sonucu bildir
- test çalıştırılmadıysa çalıştırılmış gibi davranma

Kullanıcı açıkça istemedikçe:

- commit yapma
- push yapma
- branch oluşturma
- remote değiştirme
- dosya silme

---

## 13. MODEL ROLLERİ

Qwen Coder Local:

Kullan:
- repo inceleme
- terminal
- retrieval scriptleri
- evidence pipeline
- claim extraction otomasyonu
- kod değişiklikleri
- testler

Qwen 3.6 Writer Local:

Kullan:
- evidence değerlendirme
- teknik metin üretimi
- section drafting
- prose audit
- coherence kontrolü

Qwen 3.5 Fast Local:

Kullan:
- kısa sorular
- hızlı açıklamalar
- düşük maliyetli günlük işler

Writer modeline gereksiz agent/tool görevi verme.

---

## 14. SECTION WRITING CONTRACT

Bir section yazılmadan önce şu durumlar mevcut olmalıdır:

- section scope
- research question
- evidence packet
- admitted claims
- citation mapping
- readiness state

Readiness:

- READY
- READY_WITH_LIMITATIONS

ise yazım yapılabilir.

Readiness:

- EVIDENCE_NOT_READY
- TRUE_CORPUS_EVIDENCE_GAP
- BLOCKED

ise prose yazma.

---

## 15. OUTPUT DISCIPLINE

İş sonunda kısa rapor ver:

- durum
- değişen dosyalar
- test sonucu
- blocker
- sonraki adım

Uzun corpus veya evidence içeriğini gereksiz yere terminale basma.

Bir section tamamlandıktan sonra otomatik olarak sonraki section'a geçme.
