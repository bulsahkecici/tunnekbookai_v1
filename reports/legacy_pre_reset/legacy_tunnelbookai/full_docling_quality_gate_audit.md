# TunnelBookAI Full Docling Quality Gate Audit

**Tarih:** 13 Ağustos 2026  
**İncelenen gerçek pilot:** 10 belge, Google Colab A100  
**Tam 155 belge koşusu:** Başlatılmadı  
**Stress pilot:** Başlatılmadı  
**İkinci pilot kararı:** **GO**

## Değiştirilen dosyalar

- `rapor/colab_full_docling.py`
- `rapor/tests/test_colab_preflight.py`
- `data/metadata/full_docling_manifest.csv` — mevcut 10 pilotun quality-gate kararları ve runtime fingerprint'i işlendi
- `data/metadata/full_docling_quality_manifest.csv` — yeni
- `reports/full_docling_quality_gate_audit.md` — bu rapor

Notebook, baseline Markdown corpus, kaynak belgeler ve candidate seçim mimarisi değiştirilmedi.

## Yeni kalite kuralları

Docling'in yalnız dosya üretmesi artık `success` sayılmıyor. Final Full Docling Markdown aşağıdaki konservatif ölçülerle inceleniyor:

- Toplam karakter ve anlamlı içerik uzunluğu
- Doğal dil sözcük sayısı
- Printable karakter oranı
- Unicode replacement karakter oranı
- `G\d{1,3}` glyph/code örüntü sayısı ve doğal dile göre oranı
- Markdown image placeholder sayısı
- Yalnız image placeholder veya yetersiz metinden oluşma

Yoğun glyph bozulması ancak şu koşullar birlikte gerçekleşirse reddediliyor:

```text
glyph_pattern_count >= 20
glyph_pattern_ratio >= 0.65
natural_word_count <= max(20, glyph_pattern_count / 3)
```

Bu nedenle tekil `G20` gibi normal teknik ifadeler false positive üretmiyor.

Yeni terminal belge durumları:

- `success`: Docling çıktısı kalite kapısından geçti.
- `quality_reject_use_baseline`: Docling çıktı üretti fakat kalite kapısı reddetti; baseline önerildi.
- `no_improvement_use_baseline`: Docling anlamlı Markdown üretmedi ve başarılı baseline mevcut; baseline önerildi.
- `failed`: Gerçek runtime, I/O veya beklenmeyen Docling exception; yeniden denenebilir.

## Baseline güvenliği

`data/markdown/` yalnız okunuyor ve hiçbir durumda üzerine yazılmıyor. Full Docling çıktıları `data/markdown_full_docling/` altında ayrı kalıyor. Reddedilen Full Docling çıktısı inceleme amacıyla korunuyor; tercih kararı yalnız manifestte tutuluyor.

## Quality decision manifest

Yeni dosya:

`data/metadata/full_docling_quality_manifest.csv`

Alanlar:

- `document_id`
- `source_sha256`
- `runtime_fingerprint`
- `baseline_converter`
- `full_docling_status`
- `quality_status`
- `quality_reason`
- `full_docling_output`
- `baseline_output`
- `recommended_variant`
- `glyph_pattern_count`
- `glyph_pattern_ratio`
- `text_length`
- `image_placeholder_count`
- `review_required`

`recommended_variant` yalnız `full_docling`, `baseline` veya `human_review` değerlerini alıyor.

## Resume davranışı

`quality_reject_use_baseline` ve `no_improvement_use_baseline` terminal kararlardır; aynı koşullarda gereksiz yere tekrar işlenmez.

Yeniden deneme şu durumlarda açılır:

- Kaynak SHA256 değişirse
- Docling/Python/torch/CUDA/pypdf/runtime fingerprint değişirse
- Kullanıcı `force_retry=True` verirse

Gerçek runtime/I/O exception durumları `failed` kalır ve sonraki resume koşusunda yeniden denenir.

## Gerçek 10 pilotun post-flight sınıflandırması

Mevcut manifest ve sekiz gerçek Full Docling Markdown yeniden Docling çalıştırılmadan incelendi.

### Full Docling önerilen — 7

- `STANDART ÇELİK HASIRLAR-TS 4559-İMO.pdf`
- `GeoMon2013Paper644_revised_final_cost.pdf`
- `Dergipark_Kop T__neli Yap__m __al____malar__ ve Metodolojisi#367279-384775.docx`
- `Makro sentetik Fiber.pptx`
- `tunel37.pdf`
- `TÜNEL SAYI-33.pdf`
- `Portal Yerleşimi 24.02.2020.pptx`

Bu çıktıların tümü kalite kapısından `passed` olarak geçti.

### Baseline önerilen — 3

1. `Estimate of annual operating costs Highway Tunnel.pdf`
   - Durum: `quality_reject_use_baseline`
   - Neden: `dense_glyph_code_pattern`
   - Glyph pattern: **3.700**
   - Glyph oranı: **0,977285**
   - Metin uzunluğu: **12.114**
   - Baseline converter: `pypdf_fallback`

2. `B3 60 ÇELİK İKSA DETAYI-Model.pdf`
   - Durum: `no_improvement_use_baseline`
   - Neden: Docling anlamlı Markdown üretmedi; başarılı RapidOCR baseline mevcut.
   - Baseline converter: `pypdfium2+rapidocr_torch`

3. `Taban kemersiz tip kesit.pdf`
   - Durum: `no_improvement_use_baseline`
   - Neden: Docling anlamlı Markdown üretmedi; başarılı RapidOCR baseline mevcut.
   - Baseline converter: `pypdfium2+rapidocr_torch`

### Human review — 0

Quality gate sonrası zorunlu insan incelemesine bırakılan pilot belgesi yok.

### True runtime failure — 0

Pilotun önceki iki `failed` kaydı gerçek runtime failure değildi; başarılı OCR baseline bulunan deterministik Docling no-improvement durumlarıydı.

## Test sonuçları

### Mevcut pipeline testleri

- Çalıştırılan: **19**
- Başarılı: **19**
- Başarısız: **0**

### Colab pre-flight + quality-gate testleri

- Çalıştırılan: **15**
- Başarılı: **15**
- Başarısız: **0**

### Toplam

- **34/34 başarılı**

Yeni doğrulamalar:

- Yoğun gerçekçi `G49G72...` corruption detection
- Normal Türkçe/İngilizce teknik metinde false positive olmaması
- Tekil `G20` ifadesinin reddedilmemesi
- Image-placeholder-only içeriğin reddedilmesi
- Mevcut pilot artifact'lerinin post-flight kalite sınıflandırması
- Empty Docling + başarılı baseline → `no_improvement_use_baseline`
- Terminal baseline kararının resume'da tekrar denenmemesi
- Gerçek runtime exception'ın `failed` ve retry edilebilir kalması
- Kaynak SHA değişince yeniden deneme
- Runtime fingerprint değişince yeniden deneme
- `force_retry=True` ile zorunlu yeniden deneme

## Blocker

**Yok.**

## İkinci pilot kararı

# GO

Quality gate ve baseline fallback etkinleştirildikten sonra ikinci pilot başlatılabilir. Tam 155 belge koşusuna geçmeden önce ikinci pilotun `full_docling_quality_manifest.csv` dağılımı ve birkaç örnek çıktı yine kontrol edilmelidir.
