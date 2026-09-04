# TunnelBookAI V1 Architecture

## Sorumluluk sınırı

Crawler doğrudan kanonik corpus'a yazmaz. Keşif ve sınıflandırma sonuçları önce handoff paketine, ardından hash ve provenance kontrolüyle `corpus/staging` alanına alınır. `corpus/canonical` yalnız ayrı bir ingest/normalizasyon kararıyla değiştirilebilir.

```text
book taxonomy
  -> crawler discovery/acquisition
  -> classification + parent-aggregated coverage
  -> handoff/accepted + handoff/review
  -> Unified Ingest Engine            (tunnelbookai/ingest, bkz. aşağıdaki akış)
  -> corpus/staging/v2
  -> project quality gate
  -> controlled ingest
  -> corpus/canonical
  -> evidence retrieval
  -> prewriting/chapter/postwriting audits
```

## Unified Ingest Engine

Crawler paketleri ve manuel belgeler **tek** bir motordan geçer. Manuel belgeler
handoff sözleşmesinden bağımsızdır; ikisi de aynı orijinal-arşiv, çıkarım, sınıflandırma
ve kalite kapısı hattını kullanır.

```text
PaperCrawler (READY_FOR_HANDOFF)        Manuel belgeler
  incoming/crawler/releases/              incoming/manual/inbox/
            │                                    │
            └──────────────────┬─────────────────┘
                               ▼
                      ORİJİNAL ARŞİV (immutable)
                          originals/<document_id>/
                               ▼
                        FORMAT TESPİTİ
                               ▼
                        TAM ÇIKARIM (Docling + yerel ayrıştırıcılar)
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
      METİN                 TABLOLAR               FİGÜRLER
   normalized/            tables/*.json          figures/*.png
   {md,json,txt}          tables/*.csv           OCR / yerel vision
   pages/ slides/         sheets/*.json
   sheet_snapshots/
        └──────────────────────┼──────────────────────┘
                               ▼
                    METADATA + PROVENANCE (uydurma yok)
                               ▼
                        GLOBAL DEDUP (sha → doi → url → başlık)
                               ▼
                  NİHAİ BÖLÜM SINIFLANDIRMASI
              (kural + loopback embedding + chunk oyu
               + crawler ipucu → gerekirse yerel Qwen hakem)
                               ▼
                     NİHAİ KANIT MODELİ (evidence level)
                               ▼
                   BELGE KALİTE KAPISI (GO/REVIEW/REJECT)
                               ▼
                       corpus/staging/v2/<document_id>/
                               ▼
                YAPI FARKINDA CHUNK'LAMA (multimodal)
                  processing/<id>/chunks/chunk_manifest.jsonl
                               ▼
                       CHUNK KALİTE KAPISI
                               ▼
                  EMBEDDING-READY MANIFEST
              audit/embedding_ready_manifest.jsonl
```

Bu motor **embedding üretmez, Qdrant'a yazmaz ve kanonik promosyon yapmaz.**
Ayrıntılı sözleşmeler: `docs/unified_ingest_contract.md`, `docs/chunking_contract.md`.

## Veri katmanları

| Katman | Rol | Yazma kuralı |
|---|---|---|
| `data/downloads` | Devam ettirilebilir crawler çalışma alanı | Pipeline stage'leri |
| `handoff/accepted` | Crawler tarafından uygun görülen kaynak paketi | Handoff exporter |
| `handoff/review` | Belirsiz veya insan kararı isteyen kayıtlar | Otomatik kabul edilmez |
| `incoming/` | Crawler release'leri ve manuel gelen kutusu | Kullanıcı / crawler |
| `originals/` | Değiştirilemez orijinal arşiv (read-only kopya) | Unified Ingest, yalnız bir kez |
| `processing/` | Belge başına zengin çıkarım paketi (yetkili chunk konumu) | Unified Ingest |
| `corpus/staging` | Hash doğrulanmış yeni adaylar (122 legacy düz paket) | Materializer |
| `corpus/staging/v2` | Unified Ingest paketleri (`unified_ingest_v1` şekli) | Unified Ingest |
| `corpus/canonical` | Kitapta kullanılabilen kanonik corpus | Kontrollü ingest |
| `corpus/rejects` | Silinmeden ayrıştırılan eski/uygunsuz girdiler | Denetimli taşıma |

`data/corpus_final`, `data/metadata` ve `data/temp/full_docling_chunks` eski test/topoloji uyumluluğu için yeni kanonik konumlara yönlenen bağlantılardır; yetkili yollar `corpus/` altındadır.

## Kalite kapıları

1. Migration gate dosya varlığını, kaynak-hedef SHA256 eşitliğini, iç içe Git ve sanal ortam taşınmadığını doğrular.
2. Crawler gate checkpoint bütünlüğünü, coverage parent aggregation'ı, handoff uygunluğunu ve duplicate kayıtları denetler.
3. Corpus gate staging dosyalarının hash/provenance'ını ve kanonik corpus bütünlüğünü doğrular.
4. Book gate scope, taxonomy ve question bank ilişkilerini dinamik olarak denetler; sabit bölüm/soru sayısına dayanmaz.
5. Chapter gate yalnız ilgili bölümün soru/kavram kapsamını değerlendirir; tam soru bankasını her bölümde modele göndermez.

## Karar semantiği

- `PASS` / `GO`: bloklayıcı sorun yoktur.
- `CONDITIONAL_GO`: otomasyon bütünlüğü geçmiştir fakat açık manuel inceleme veya kayıtlı legacy sınırlaması vardır.
- `NO_GO`: eksik dosya, hash/provenance hatası, yetim taxonomy ilişkisi ya da tamamlanmamış zorunlu pipeline aşaması vardır.

Tüm yollar proje kökünden türetilir; kullanıcıya özgü mutlak yol çalışma zamanı sözleşmesinin parçası değildir. Robots kararları TTL'li cache'e, provider başarısızlıkları ise kalıcı source-health durumuna yazılır.
