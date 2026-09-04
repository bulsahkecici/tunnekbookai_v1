# Manuel / Kurum İçi Doküman Kutusu

Bu klasör, kendi eklediğiniz dokümanları TunnelBookAI'nin **Unified Ingest Engine**'ine
vermek içindir. PaperCrawler paketleri buraya değil, `incoming/crawler/releases/` altına gider.

## Nasıl kullanılır

Dosyalarınızı doğrudan bu klasöre veya `incoming/manual/inbox/` altına bırakın:

```text
incoming/manual/inbox/
    KGM_Tunel_Bakim_Raporu.pdf
    Tunel_Maliyetleri.xlsx
    Ovit_Tuneli.pptx
    NATM_Destek_Sistemi.docx
    Tunel_Enkesiti.png
    Saha_Fotografi.jpg
```

Sistem formatı otomatik algılar. Handoff sözleşmesi, manifest veya metadata dosyası
hazırlamanıza gerek yoktur — SHA256, MIME, format, boyut, zaman damgası ve kaynak türü
(`MANUAL_INTERNAL`) motor tarafından üretilir.

## Desteklenen formatlar

| Öncelikli | Ek | Eski (LibreOffice varsa) |
|---|---|---|
| PDF, DOCX, PPTX, XLSX, PNG, JPG, JPEG | TXT, MD, CSV, HTML | DOC, PPT, XLS |

## Sonra ne çalıştırılır

```bash
# Önce sadece envanter (hiçbir şey işlenmez, dosyalarınıza dokunulmaz):
.venv/bin/python scripts/ingest_incoming.py --source manual --dry-run

# Gerçek işleme (devam ettirilebilir):
.venv/bin/python scripts/ingest_incoming.py --source manual --resume
```

## Garantiler

- **Orijinal dosyanız hiçbir zaman değiştirilmez.** İlk işlem SHA256 + `originals/` arşividir.
- **Ağ kullanılmaz.** Manuel işleme sırasında hiçbir uzak servise (bulut OCR, bulut vision,
  bulut LLM) bağlanılmaz. Yerel yapay zekâ yalnız `127.0.0.1` üzerinde kabul edilir.
- Aynı dosyayı iki kez bıraksanız bile ikinci kez yeniden işlenmez (`ALREADY_PROCESSED`).
- Bu görev kapsamında hiçbir belge `corpus/canonical/`'e yazılmaz; yalnız kalite kapısından
  geçenler `corpus/staging/` için hazırlanır.

## Gizlilik

Manuel belgelere `confidentiality` alanı eklenir. Siz metadata vermezseniz varsayılan
`UNKNOWN`'dır; klasör adına bakılarak kesin bir hukuki sınıf (INTERNAL/RESTRICTED) atanmaz.
`source_kind = MANUAL_INTERNAL` ayrı bir kavramdır ve gizlilik sınıfı anlamına gelmez.
