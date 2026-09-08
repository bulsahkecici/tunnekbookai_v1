# TunnelBookAI V1 Migration Audit

Tarih: 2026-09-01  
Karar: **PASS (migrasyon bütünlüğü)** / **CONDITIONAL_GO (corpus kullanıma hazırlık)**

## Kaynak envanteri

| Kaynak | Git durumu | Taşınan ana varlıklar | Arşiv kararı |
|---|---|---|---|
| `paper-crawler-agent` | `hardening`, `ebe597a...`, dirty | 24 Python modülü, 10 test modülü, config, 5.6 GB devam ettirilebilir crawler çıktısı | `SAFE_TO_ARCHIVE` |
| `tunnel/_TunnelBookAI` | `master`, `a5d5c0f...`, dirty | 214 kanonik Markdown, 576 metadata dosyası, 738 full-Docling sidecar ve test için gerekli türetilmiş veri | `KEEP` |
| Hazır `book` paketi | Git dışı | Scope, question bank, manifest ve checksum'lar | V1 içinde korundu |

Eski projelerde silme, commit veya push yapılmadı. İç içe `.git`, `.venv`, cache ve model cache taşınmadı. `_TunnelBookAI` için ham/arşiv/office dönüşüm depolarının tümü V1 kapsamına alınmadığından kaynak proje korunmalıdır. Crawler'ın kod, test, config ve dayanıklı çıktı kapsamı doğrulandığı için crawler kaynak projesi arşivlenebilir; silme önerilmez.

## Taşıma sonucu

- Migration manifest: 10.134 proje dosyası envanterlendi; 1.542 kritik kaynak-hedef dosyası byte/SHA256 eşitliğiyle doğrulandı.
- Eksik dosya: 0; hash uyumsuzluğu: 0.
- Hazır kitap paketi overwrite edilmeden root `book/` altına byte-identical kopyalandı.
- Kanonik corpus: 214 Markdown; manifest ile dosya sayısı eşleşiyor.
- Handoff: 122 kabul/staging kaydı; 890 manuel inceleme kaydı.
- Eski testlerin beklediği `data/...` görünümü, yetkili `corpus/...` yollarına bağlantılar ve seçili uyumluluk fixture'larıyla korundu.
- Eski iki stale staging kaydı silinmedi; `corpus/rejects/stale_handoff` altında ayrıştırıldı.

Makinece okunur kanıt: `audit/migration_manifest.json`.

## Çakışma kararları

1. Root README/config/tests ad çakışmaları crawler namespace'i (`crawler/`) ve birleşik root dizinleriyle çözüldü.
2. Hazır kitap paketi yetkili kitap girdisi seçildi; legacy `data/book` onun üzerine yazılmadı.
3. Kanonik corpus `corpus/canonical`, metadata `corpus/metadata`, crawler çalışma alanı `data/downloads` olarak ayrıldı.
4. Kullanıcıya özgü mutlak çalışma yolları kaldırıldı; yalnız migration validator içinde kaynak proje konumları proje kökünün parent'ından türetiliyor.

## Kitap QA

Deterministik bütünlük kapısı `PASS` verdi:

- Scope: 66 bölüm
- Question bank: 59 bölüm, 2.950 soru
- Duplicate question ID: 0
- Yetim bölüm: 0
- Başlık/parent/count/hash uyuşmazlığı: 0
- Taxonomy kapsam eksiği: 0
- Tam 2.950 soruluk LLM değerlendirmesi: **çalıştırılmadı**

Question coverage ile document coverage ayrı şemalarda tutulur. Bölüm üretiminde tam soru metni arama sorgusu yapılmaz; kısa teknik kavramlar çıkarılır. Prewriting, question coverage ve postwriting audit şemaları `book/audits/schemas/` altındadır.

## Testler

- Crawler regresyonu: **97/97 OK**.
- Yeni V1 migration/book/gate testleri: **18/18 OK**.
- Kontrollü küçük internet smoke testi: **PASS**; 2 sorgu, kaynak başına en çok 2 sonuç, toplam download budget 2, 7 metadata adayından 1 başarılı indirme ve 6 sınıflandırma. Production crawl değildi.
- Eski 1.395 testlik paketin ilk koşusu, legacy `data/...` görünümü yokken 15 failure ve 451 error üretti. Uyumluluk verisi eklendikten sonraki tam tekrar, koşul belirtmeden canlı `localhost:6333` Qdrant isteyen iki legacy test ve Qdrant client bağlantı beklemesi nedeniyle tamamlanmadı; süreç güvenli biçimde kesildi. Bu durum yeni 115 testlik deterministik kapıda hata üretmedi, fakat `_TunnelBookAI` için `KEEP` kararının nedenlerinden biridir.

## Son karar

Migrasyon kendi bütünlük sözleşmesinde `PASS` durumundadır. Birleşik corpus kapısı, açık manuel review kuyruğu ve geçmiş kanonik dokümanlarda kaynak URL/bölüm ataması üretilemediği açıkça kaydedilmiş provenance sınırlamaları nedeniyle `CONDITIONAL_GO` durumundadır. Yeni staging girdileri otomatik olarak kanonik corpus'a alınmamalıdır.
