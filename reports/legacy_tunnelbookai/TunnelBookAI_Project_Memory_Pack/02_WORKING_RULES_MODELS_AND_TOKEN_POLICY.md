# TunnelBookAI – Working Rules, Models and Token Policy

## Ana İlke

> Corpus conversation context değildir. Corpus sorgulanabilir veri kaynağıdır.

Normal görev sırası:
1. `AGENTS.md`
2. `docs/ai/CURRENT_STATE.md`
3. `docs/ai/NEXT_PHASE.md`
4. targeted `rg`
5. sadece gerekli dosyalar
6. targeted tests
7. targeted diff
8. STOP

## Repository Exploration

Tercih:
- `rg`
- `rg --files`
- targeted `ls`
- line-range reads
- bounded terminal output

Kaçınılacak:
- `tree`
- `find .`
- `grep -R "" .`
- bütün Markdown’ları okumak
- full git history
- full diff
- long successful logs

Normal corpus read budget:
1–5 document.
>10 gerekiyorsa candidate set önce metadata/manifests/indexes ile küçültülür.

## Git Safety

- destructive command yok
- user changes korunur
- commit yalnız açık istekle
- push yalnız açık istekle
- büyük generated data Git’e girmez

Git’te tutulan ana yapı:
- AGENTS.md
- CLAUDE.md
- .codex/
- config/
- docs/
- scripts/
- tests/
- reports/
- rapor/
- data/book/

Ignore:
- `.venv/`
- `.claude/`
- `logs/`
- `tools/`
- `data/corpus_*`
- `data/chunks*`
- `data/embeddings*`
- `data/converted_office/`
- `data/archive/`

İlk local commit:
`fc5bec2 Initialize TunnelBookAI project repository`

## Codex Workspace

Codex CLI:
`0.148.0-alpha.21`

Model:
`gpt-5.6-sol`

Project config:
`.codex/config.toml`

Aktif:
- reasoning: low
- verbosity: low
- auto-compaction: 32,000
- tool output limit: 4,000
- Fast mode: off
- subagents: off
- apps default: disabled

Sandbox:
- workspace-write
- restricted network

Approval:
- on-request

## Model / Reasoning Seçimi

### GPT-5.6 Sol — Low
- file lookup
- SHA
- metadata/provenance
- state reconciliation
- küçük script edit
- targeted test
- Git/workspace setup

### GPT-5.6 Sol — Medium
- technical audit
- re-audit
- failure analysis
- architecture remediation
- integration rerun
- release authorization
- semantic/citation/scope analysis

### GPT-5.6 Sol — High
Yalnız Medium gerçekten yetmezse:
- zor architecture contradiction
- multi-layer semantic conflict
- kritik root-cause
- sistem seviyesi tasarım kararı

Kural:
> Low first. Audit/root-cause → Medium. High only if necessary.

## Claude Code ↔ Codex Geçişleri

### Claude Code
Codex hakkı bittiğinde devam için kullanıldı.

Sorunlar:
- >150k context
- 8+ saat session
- compaction overhead
- çok hızlı weekly token tüketimi

Claude kuralı:
- yeni faz/konu → `/clear`
- aynı faz → compact/continue
- broad repo scan yok
- uzun session kapat
- bounded output

### Codex
Kullanım hakkı açılınca ana execution agent oldu.

Avantaj:
- AGENTS.md
- project-local config
- explicit low reasoning
- 32k compaction
- 4k tool output
- Fast off
- subagents off
- short phase prompts

## Token Tüketiminden Öğrenilenler

En büyük tüketim:
1. uzun session
2. repo/corpus taraması
3. reread
4. full pytest
5. uzun logs
6. tree/find/full diff
7. proje tarihini her promptta tekrar etmek
8. finalde dosyaların tamamını tekrar basmak

Yeni strateji:
- AGENTS.md = çalışma kuralları
- CURRENT_STATE = güncel gerçek durum
- NEXT_PHASE = executable brief
- prompt = kısa tetikleyici
- bu memory pack = yalnız gerektiğinde historical context
