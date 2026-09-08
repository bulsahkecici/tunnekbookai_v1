# TunnelBookAI Colab Full Docling Pre-flight Audit

**Audit tarihi:** 13 Ağustos 2026  
**Audit kapsamı:** Colab pilot güvenliği, path portability, belge kimliği, chunk/resume, özgün sayfa provenance, aday seçimi, GPU/version preflight ve Drive I/O  
**Tam Full Docling koşusu:** Başlatılmadı  
**Karar:** **GO — 10 belgeli Colab pilotu güvenle başlatılabilir.**

## PASS

### Colab path portability

- `rapor/colab_full_docling.py` ve `rapor/TunnelBookAI_Colab_Full_Docling.ipynb` içinde `C:\`, `C:\Users`, `bulsa`, `OneDrive` veya `Desktop\tunnel` absolute çalışma yolu bulunmadı.
- Colab kaynak kökü notebook'taki tek değişkenden geliyor:

```python
DRIVE_TUNNEL = Path('/content/drive/MyDrive/tunnel')
```

- Colab yürütme kodu `pathlib.Path` kullanıyor.
- Windows `config/config.yaml` ve eski manifestlerin Windows absolute path içermesi beklendik bir legacy durumdur. Colab kodu Windows config'i import etmiyor ve envanterdeki `absolute_path` alanını identity/resume için kullanmıyor.

### Portable document identity

- Candidate/resume kimliği `document_id`, `source_relative_path` ve `source_sha256` temellidir.
- Candidate oluşturulurken conversion manifest ile inventory arasında relative path ve SHA256 eşleşmesi zorunlu kontrol ediliyor.
- Windows absolute path'in değişmesi processed/not-processed kararını etkilemiyor.
- Sentetik testte Windows absolute path içeren envanter, aynı relative path ve SHA256 ile Colab adayı olarak doğru eşleşti.
- Sentetik SHA256 uyuşmazlığı beklendiği gibi işlem başlamadan reddedildi.

### PDF chunk ve özgün sayfa doğruluğu

- Varsayılan `CHUNK_PAGES = 25` korundu.
- Chunk manifesti şu alanları içeriyor:
  - `document_id`
  - `source_sha256`
  - `chunk_id`
  - `original_page_start`
  - `original_page_end`
  - `page_map_json`
  - `output_chunk_json`
- 101–125 sayfa parçası için local sayfa 1 → original 101, local sayfa 3 → original 103 ve local sayfa 25 → original 125 testi geçti.
- Her chunk için Docling JSON sidecar üretiliyor. Docling öğelerinin provenance kayıtlarında:
  - `page_no`: Docling'in değiştirilmemiş chunk-local sayfası
  - `chunk_local_page_no`: açık local sayfa
  - `original_page_no`: citation'da kullanılacak gerçek PDF sayfası
- Sentetik provenance testinde chunk-local sayfa 3, `original_page_no = 103` olarak doğrulandı.
- 30 sayfalık sentetik PDF'den özgün 11–20 aralığı bölündü ve sonuç PDF'nin 10 sayfa olduğu doğrulandı.

### Chunk merge ve resume

- Birleştirme dosya adının lexicographic sırasına bağlı değildir.
- Beklenen plan `original_page_start` üzerinden numeric sıralanıyor.
- Merge öncesi her beklenen chunk için şu kontroller yapılıyor:
  - Başarılı durum
  - Aynı kaynak SHA256
  - Markdown checkpoint mevcut
  - Citation-safe Docling JSON sidecar mevcut
- Eksik veya başarısız chunk varsa final Markdown üretilmiyor.
- Chunk kayıtları `chunk_id` anahtarlı sözlükte tutulduğu için resume aynı chunk'ı ikinci kez final metne eklemiyor.
- `chunk_1`, `chunk_2`, `chunk_10` sentetik sıralama/resume testi geçti.

### Candidate manifest

- `data/metadata/full_docling_candidates.csv` oluşturuldu.
- Satır: **155**
- `selected=true`: **155**
- Kimliği eksik satır: **0**
- Pilot seçimi: **10**
- Stress pilot seçimi: **5**
- Candidate manifestte istenen alanların tamamı ve ayrıca pilot/stress seçim açıklamaları bulunuyor.

Gerçek 155 seçim kuralı değiştirilmedi:

```text
conversion_manifest.status == success
AND source_extension IN (.pdf, .docx, .pptx, .pptm, .xlsx)
AND converter adı "docling" içermiyor
```

Dağılım:

- PDF: 102
- DOCX: 26
- PPTX: 26
- PPTM: 1
- `layout_quality_check`: 89
- `ocr_comparison`: 16
- `python_docx_fallback`: 23
- `python_pptx_fallback`: 27

### GPU preflight

Notebook işlem başlamadan şunları logluyor:

- `torch.cuda.is_available()`
- `torch.cuda.get_device_name(0)`
- `torch.__version__`
- `torch.version.cuda`

CUDA yoksa notebook pilot başlamadan duruyor. Docling converter oluşturulurken accelerator/device ayrıca `cuda` olarak loglanıyor.

### Version audit

Pilot başlangıcında aşağıdaki gerçek runtime sürümleri `_TunnelBookAI/reports/colab_runtime_versions.json` içine yazılacak:

- Python
- docling
- docling-core
- torch
- CUDA
- pypdfium2
- pypdf
- transformers
- CUDA availability ve gerçek GPU adı

Sürümler otomatik pinlenmedi; mevcut dependency çözümü gereksiz yere değiştirilmedi.

### Drive I/O

Kodun veri yolu şu şekilde doğrulandı:

```text
Drive source
  → /content/tunnelbook_work/input yerel kopya
  → SHA256 karşılaştırması
  → yerel chunk/Docling işlemi
  → atomik Drive checkpoint/output
```

Docling ağır işlemi mounted Drive kaynağı üzerinde doğrudan çalıştırmıyor. Drive → `/content` kopyasının SHA256 değeri inventory SHA256 ile eşleşmezse işlem duruyor.

### Pilot ve stress pilot

10 belgeli pilot yalnız boyut örneklemesi değildir. Mevcut arşivde şu roller temsil ediliyor:

- Normal PDF
- Akademik/çok sütunlu PDF
- Tablo yoğun PDF
- DOCX
- PPTX
- Türkçe karakterli dosya adı
- OCR/layout açısından zor belge
- Boyut dağılımı örnekleri

En büyük aday ilk pilotta dışarıda tutuluyor.

İsteğe bağlı 5 belgeli stress pilot şu rolleri seçiyor:

- En büyük PDF (`KTS_2013.pdf`)
- OCR gerektiren büyük PDF
- Tablo/layout PDF
- Akademik/çok sütunlu PDF
- Ek büyük PDF

Stress pilot tam koşu için zorunlu engel değildir ve varsayılan olarak kapalıdır.

### Baseline corpus koruması

- `data/markdown/` yalnız mevcut front matter'ı okumak için açılıyor.
- Full Docling yazma hedefi yalnızca `data/markdown_full_docling/`.
- Audit sonunda baseline Markdown sayısı: **214**.
- Baseline klasöründeki en yeni değişiklik: **13 Ağustos 2026 02:04:28**; pre-flight audit sırasında değişmedi.
- Full Docling çıktı sayısı: **0**.
- `full_docling_manifest.csv` ve chunk manifesti oluşmadı; yani pilot/tam koşu başlatılmadı.

## FIXED

1. Chunk manifestindeki genel `page_start/page_end` alanlarına ek olarak açık `original_page_start/original_page_end` ve local→original `page_map_json` eklendi.
2. Gelecekte gerçek sayfa citation üretilebilmesi için her chunk'a Docling JSON sidecar ve her provenance öğesine `original_page_no` eklendi.
3. Final merge numeric özgün sayfa planına bağlandı; eksik chunk, yanlış SHA, eksik Markdown veya eksik citation JSON varsa merge reddediliyor.
4. Resume skip sırasında legacy chunk kayıtlarının özgün sayfa metadata'sı normalize ediliyor. Citation JSON yoksa eski başarı kaydı atlanmıyor; chunk yeniden işleniyor.
5. 155 satırlık `full_docling_candidates.csv` ve açık seçim nedeni alanları oluşturuldu.
6. Pilot seçimi format/zorluk çeşitliliğini kapsayacak biçimde deterministik hale getirildi; en büyük aday ilk pilottan hariç tutuldu.
7. İsteğe bağlı 5 belgeli stress pilot eklendi.
8. GPU adı, CUDA durumu, torch/CUDA ve gerekli paket sürümü audit kaydı eklendi.
9. Colab notebook ve kullanım kılavuzu A100/H100/L4/T4 seçenekleri, stress pilot ve citation-safe sidecar davranışıyla güncellendi.

## WARNING

- Gerçek Google Colab runtime, Drive mount, A100/H100/T4 donanımı ve gerçek Docling model indirme/çalıştırma bu pre-flight kapsamında başlatılmadı. Dolayısıyla gerçek Colab paket sürümleri ve GPU adı henüz oluşmadı; pilot başında kaydedilecek.
- `page_count_if_known` alanı mevcut inventory'de sayfa sayısı bulunmadığı için çoğu adayda boştur. PDF sayısı pilot/tam koşuda kaynak yerel diske kopyalandıktan sonra güvenli biçimde belirlenir.
- Citation-safe JSON sidecar gelecekteki RAG aşamasının `original_page_no` alanını kullanmasını sağlar. İlerideki chunking/RAG kodu bu alanı görmezden gelirse doğru sayfa bilgisi kendiliğinden taşınmış olmaz; bu aşamada RAG kodu oluşturulmadı.
- Google Colab GPU ve oturum süresi Pro hesabında da kapasite ve compute unit durumuna bağlıdır. Checkpoint/resume bu nedenle zorunlu güvenlik olarak korunmuştur.

## BLOCKER

**Yok.**

Pilot başlamadan notebook'un kendi runtime kontrolleri şunları yine zorunlu olarak doğrulayacaktır:

1. `/content/drive/MyDrive/tunnel` mevcut.
2. `_TunnelBookAI/data/metadata/conversion_manifest.csv` mevcut.
3. `rapor/colab_full_docling.py` mevcut.
4. CUDA GPU gerçekten kullanılabilir.

Bu kontrollerden biri başarısızsa notebook `GO` kararına rağmen o runtime'da işlem başlatmaz.

## Test sonuçları

### Mevcut pipeline testleri

- Çalıştırılan: **19**
- Başarılı: **19**
- Başarısız: **0**

### Yeni Colab pre-flight testleri

- Çalıştırılan: **8**
- Başarılı: **8**
- Başarısız: **0**

Test edilenler:

- Windows path → Colab path portability
- Relative-path kimliği
- SHA256 kimliği ve mismatch reddi
- Özgün sayfa offset/page map
- Docling provenance `original_page_no`
- Sentetik PDF bölme
- Numeric chunk merge
- Resume sonrası duplicate önleme
- Candidate manifest alanları
- Pilot/stress seçimleri

Ek statik doğrulama:

- `colab_full_docling.py`: Python AST başarılı
- Notebook: JSON parse başarılı
- Notebook'taki Python hücreleri: AST başarılı
- Notebook hücresi: **14**

Test edilmemiş olanlar açıkça WARNING bölümünde belirtilmiştir.

## Nihai karar

# GO

**10 belgeli Colab pilotu güvenle başlatılabilir.** Tam 155 belgeli koşu bu audit sırasında başlatılmadı ve pilot sonucu görülmeden otomatik başlamayacaktır.
