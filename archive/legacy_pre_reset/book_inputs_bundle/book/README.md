# TunnelBookAI V1 — Book Scope & Question Bank Package

Bu paket doğrudan `~/Projects/tunnelbookai_v1/` içine çıkarılmak üzere hazırlanmıştır. ZIP'in kökünde `book/` klasörü vardır.

## İçerik

- `book/scope/source/` — orijinal Çalışma Kapsamı Tasarısı (RTF)
- `book/scope/normalized/book_scope.json` — canonical bölüm/alt başlık yapısı
- `book/scope/normalized/book_scope.csv` — Excel/manuel kontrol için aynı kapsam
- `book/question_bank/source/` — orijinal 2.950 soruluk Word dosyası
- `book/question_bank/normalized/question_bank.jsonl` — pipeline için ana makine-okunur soru bankası
- `book/question_bank/normalized/question_bank.csv` — Excel/manuel kontrol sürümü
- `book/question_bank/normalized/question_bank_index.json` — bölüm ve soru indeksleri
- `book/audits/question_bank_integrity.json` — bütünlük kontrolü
- `book/audits/source_manifest.json` — kaynak SHA256 manifesti
- `book/tools/validate_book_inputs.py` — paketi sonradan hızlı doğrulama aracı

## Doğrulanan mevcut durum

- Canonical kapsam girdisi: **66 bölüm/başlık** (7 ana bölüm + 59 soru bankası alt başlığı)
- Soru bankası alt başlığı: **59**
- Toplam soru: **2950**
- Her soru bankası alt başlığında: **50 soru**
- Integrity kararı: **PASS**

## Tasarım kararı

DOCX ve RTF dosyaları insan tarafından okunabilir kaynak belgeler olarak korunur. Pipeline'ın ana çalışma formatı `question_bank.jsonl` ve `book_scope.json` olmalıdır. CSV dosyaları manuel denetim/Excel amacıyla üretilmiştir.

Kaynak kapsam dosyasındaki `…` ile gösterilen eksik/gizli başlıklar tahmin edilmemiştir. Soru bankası da aynı prensiple yalnızca açık başlıklara dayanır.

## Kurulum

ZIP'i şu dizinde aç:

```bash
cd ~/Projects/tunnelbookai_v1
unzip tunnelbookai_v1_book_inputs.zip
```

Sonrasında:

```bash
python book/tools/validate_book_inputs.py
```

beklenen çıktı:

```text
BOOK INPUT VALIDATION: PASS
59 question-bank sections / 2950 questions
```

## Pipeline'da kullanım

İleride her `section_id` için ilgili 50 soru JSONL'den seçilebilir. Aynı bankanın iki kalite kapısında kullanılması önerilir:

1. **Pre-writing evidence audit:** Corpus bu soruyu cevaplayacak yeterli kanıt içeriyor mu?
2. **Post-writing chapter audit:** Yazılan bölüm bu soruya gerçekten cevap veriyor mu?

Tam 2.950 soruluk LLM değerlendirmesi bu paket oluşturulurken çalıştırılmamıştır.
