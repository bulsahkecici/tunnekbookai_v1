# Paper Crawler Stabilization Audit

Tarih: 2026-09-01  
Karar: **CONDITIONAL_GO**

## Kök neden

Önceki 1.193 → 1.160 mutabakatı veri kaybı değildi: legacy merge, aynı DOI'ye sahip 33 kaydı deterministik olarak birleştirmişti. Buna karşılık coverage'daki `current=0` görüntüsünün ana nedeni, gap kararının yalnız doğrudan `handoff_candidate_section_coverage` saymasıydı. Alt bölüm atamaları parent bölümlere toplanmıyor, metadata-only veya henüz acquisition yapılmamış kayıtlar farklı semantiklerle karıştırılıyordu.

## Uygulanan stabilizasyon

- Coverage artık bölüm başına `discovered_count`, `classified_count`, `accepted_count`, `review_count` ve `corpus_eligible_count` üretir; parent aggregation deterministiktir.
- Zayıf/borderline kaynaklar otomatik `REJECT_IRRELEVANT` yerine `NEEDS_REVIEW`/`PREFILTERED` akışına alınır.
- `--resume`, veri silmeyen `--fresh-run`, aşama bazlı `--from-stage` ve Ctrl+C sonrası `PARTIAL` checkpoint davranışı korunur/test edilir.
- Gap discovery'de bölüm başına aday ve indirme bütçesi, acquisition öncesi metadata prefilter/dedup ve sonuç üretmeyen sorgular için diminishing returns vardır.
- Robots cache hostname, karar, `checked_at` ve `expires_at` alanlarıyla kalıcıdır.
- OpenAlex retry `Retry-After`, sınırlı retry, exponential backoff ve jitter uygular. Provider health kalıcıdır; CORE son durumda 2 ardışık timeout nedeniyle geçici cooldown'a alınmış, diğer altı akademik provider 48'er başarı kaydetmiştir.
- Explicit `handoff_candidate=false` kayıtları exporter tarafından reddedilir.
- Taxonomy, scope'un 66 bölümünün tamamıyla hizalandı; question bank'teki 59 bölümün tümü kapsanıyor.

## Son sayımlar

| Metrik | Değer |
|---|---:|
| Birleşik sınıflandırma indeksi | 1.652 |
| Discovered | 1.625 |
| Classified | 1.652 |
| Accepted (classification) | 948 |
| Review sinyali (coverage, bölüm atamaları toplamı) | 1.279 |
| Corpus-eligible / handoff | 122 |
| Üst review queue (tekil kayıt) | 890 |
| Rejected (türetilmiş tekil kayıt) | 640 |
| Dedup removed | 88 |
| Mevcut kanonik corpus | 214 |
| Yeni staging | 122 |
| Full-text evidence | 0 |
| Abstract-only | 607 |
| Title/metadata-only | 1.045 |

Coverage toplamları kayıtların birden çok bölüme atanabilmesi nedeniyle tekil review queue sayısıyla aynı semantiğe sahip değildir.

## Başlıca coverage boşlukları

Corpus-eligible sayısı sıfır ve discovery sayısı da sıfır olan ilk 10 scope alanı:

1. `4.1` Maliyet Kavramı, Ulaşım Maliyetleri ve İlgili Tanımlar
2. `5.1` Çalışmanın Amacı ve Önemi
3. `5.2` Çalışmanın Kapsamı
4. `5.3` Çalışmanın Yöntemi ve Kullanılan Veriler
5. `6.1.1` Çalışmanın Amacı ve Önemi
6. `6.1.2` Çalışmanın Kapsamı
7. `6.1.3` Çalışmanın Yöntemi
8. `7` Araştırmanın Bulguları, Sonuçlar ve Öneriler
9. `7.1` Tünel Bakım-İşletme Maliyetleri
10. `7.2` Tünel Yapım Maliyetleri

Bunların bir kısmı kaynak keşif konusu değil, sentez/yöntem bölümü niteliğindedir. Bu nedenle bir sonraki gap turunda körlemesine download budget artırmak yerine, `4.1`, `7.1` ve `7.2` için teknik/ekonomik kaynak araması; yöntem ve sonuç başlıkları içinse chapter-level evidence mapping uygulanmalıdır.

## Handoff ve kalite kapısı

`handoff/manifests/handoff_manifest.jsonl` 122 tekil canonical ID ve tekil SHA içerir. Her kaydın staging dosyası, SHA256 değeri ve provenance alanı doğrulandı. Mevcut kanonik 214 dosyada hash duplicate yoktur; 214 satırlık additive provenance manifesti oluşturuldu. Legacy dokümanlarda bulunamayan URL ve bölüm ataması uydurulmadı, sınırlama olarak kaydedildi.

Bloklayıcı sorun yoktur. `CONDITIONAL_GO` koşulları:

- 890 kayıt manuel review bekliyor.
- 122 staging kaydı full-text değildir; 607 abstract-only ve 1.045 title/metadata-only kayıt bulunan sınıflandırma evreninden gelmektedir.
- Legacy canonical provenance sınırlamaları açık kalmaktadır.

Bu nedenle full-text acquisition/Docling doğrulaması ve manuel review tamamlanmadan staging → canonical ingest yapılmamalıdır. Tam production crawl ve tam soru bankası LLM değerlendirmesi çalıştırılmamıştır.
