# TunnelBookAI Metadata Enrichment Audit

## Sonuç

- Karar: **GO**
- Toplam belge: **214**
- Language otomatik bulunan: **206**
- Year otomatik bulunan: **147**
- Document type otomatik bulunan: **133**
- Authority high confidence: **32**
- Authority medium confidence: **88**
- Authority low/unclassified: **94**
- Topics bulunan: **213**
- Human review gereken belge: **200**
- Human review queue satırı: **369**

## Citation mode dağılımı

- `document_section`: **53**
- `image`: **3**
- `pdf_page`: **88**
- `slide`: **38**
- `source_only`: **29**
- `table_or_sheet`: **3**

## Master integrity

- Metadata master duplicate document_id: **0**
- Metadata master eksik zorunlu kimlik/SHA: **0**
- Canonical 214 document_id tam temsil: **true**
- Mevcut metadata `*_current` alanlarında korundu; suggestion alanları verified metadata olarak uygulanmadı.
- Filesystem created/modified tarihleri publication year çıkarımında kullanılmadı.
- Harici API/ücretli model çağrısı yapılmadı; LLM varsayılan olarak kapalıdır.

## Text normalization pre-audit özeti

- Aşırı kısa belge (<100 kelime): **7 belge**
- Broken encoding marker: **6 belge**
- Formula not decoded: **26 belge**
- Image placeholder: **159 belge**
- JEOLOJ İ K tipi parçalanmış kelimeler: **11 belge**
- Line-break/hyphenation: **15 belge**
- OCR-confidence şüpheli içerik: **31 belge**
- Repeated whitespace: **164 belge**
- Türk İ YE benzeri OCR boşlukları: **12 belge**
- Unicode replacement character: **16 belge**
- Çok tekrarlanan header/footer: **49 belge**

## Test sonuçları

- 55/55 başarılı (39 pipeline/final/metadata + 16 Colab/pre-flight)
