# TunnelBookAI – Project Memory Pack

Bu paket, TunnelBookAI projesinde bugüne kadar alınan kararları, yaşanan sorunları,
Codex/Claude çalışma düzenini, token tasarrufu politikasını ve tekrar kullanılabilir
promptları tek yerde toplar.

## Dosyalar

- `00_README.md` — İndeks ve kullanım notu.
- `01_PROJECT_HISTORY.md` — Projenin başlangıcından bugüne teknik yolculuk.
- `02_WORKING_RULES_MODELS_AND_TOKEN_POLICY.md` — Codex/Claude çalışma koşulları, model/reasoning seçimi ve token politikası.
- `03_PROMPT_LIBRARY.md` — Tekrar kullanılabilir kısa promptlar ve kritik prompt şablonları.
- `04_CURRENT_STATE_AND_NEXT_ACTION.md` — Bugünkü gerçek durum, açık problem ve çalıştırılmamış son prompt.
- `05_ARCHITECTURE_AND_INVARIANTS.md` — Projenin değişmez teknik kuralları ve üretim mimarisi.

## Kullanım

Yeni Codex/Claude oturumunda bu paketin tamamını okutma.

Normalde sadece:

1. `AGENTS.md`
2. `docs/ai/CURRENT_STATE.md`
3. `docs/ai/NEXT_PHASE.md`

kullanılmalıdır.

Bu paket yalnız bağlam kaybolduğunda, model değiştirildiğinde, uzun vadeli proje devri
gerektiğinde veya karar geçmişi aranırken referans olarak kullanılmalıdır.

Ana ilke:

> Corpus conversation context değildir. Corpus sorgulanabilir bir veri kaynağıdır.
