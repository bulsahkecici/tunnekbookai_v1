

<!-- FILE: 00_README.md -->

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


<!-- FILE: 01_PROJECT_HISTORY.md -->

# TunnelBookAI – Project History

## 1. Projenin Amacı

TunnelBookAI’ın amacı tünel mühendisliğiyle ilgili PDF/DOCX/PPTX ve diğer kaynakları
kontrollü biçimde işleyerek aşağıdaki zinciri kurmaktır:

```text
source documents
→ conversion
→ canonical Markdown
→ metadata + provenance
→ quality / corpus audit
→ chunking + embeddings
→ evidence retrieval
→ evidence-grounded technical book production
```

Hedef sadece “LLM ile kitap yazdırmak” değildir. Her teknik iddianın kaynağına
izlenebilir olduğu, uydurma onarım yapılmadığı, tekrar üretilebilir ve denetlenebilir
bir kitap üretim sistemi kurulmaktadır.

## 2. Document Conversion ve Corpus

İlk büyük çalışma kaynak belgelerin Markdown’a dönüştürülmesiydi.

- PDF / Word / PowerPoint kaynakları işlendi.
- Colab tabanlı Docling pipeline geliştirildi.
- Preflight testleri ve kalite kapıları oluşturuldu.
- Pilot conversion kalite kapısı GO oldu.
- Final Corpus Audit GO oldu.
- Canonical belge sayısı 214 olarak kapandı.
- Eksik/boş, duplicate id/path, SHA/provenance kontrolleri kapatıldı.
- Tek final Markdown politikası benimsendi.
- Frozen upstream artifacts ilkesi getirildi.

Corpus artık kontrolsüz biçimde yeniden üretilmemeli veya “projeyi anlamak için”
LLM contextine topluca taşınmamalıdır.

## 3. Chunking, Embedding ve Retrieval

- Semantic chunks v1.1: 6039
- Embedding input: 5992
- canonical: 5980
- recovery: 12
- Embedding model: BGE-M3
- dimension: 1024
- Qdrant collection: `tunnelbook_dense_v1`
- distance: cosine

Retriever deneylerinde dense-only yaklaşımı tutuldu.
Hybrid/translation/reranker gibi yollar empirik olarak reddedildi.

Sonuç:
- Retriever V1 CLOSED / GO
- RAG Context V1 CLOSED / GO

## 4. Local Generation

Yerel generation modeli:

`qwen3.6-35b-a3b-mlx`

Prompt v5’e kadar gelindi.
Raw generator tek başına yeterli bulunmadı.

Alınan kararlar:
- Prompt v6 ayrı experiment olmadan açılmayacak.
- Validator pass almak için gevşetilmeyecek.
- Same-config retry yapılmayacak.
- Reject sonrası otomatik rewrite/translate/repair yapılmayacak.

Production Grounded Generator ayrı frozen bileşen olarak CLOSED / GO oldu.

## 5. Book Evidence Architecture

Kitap üretimi için katmanlar oluşturuldu:

- source registry
- evidence notes
- research questions / runs
- section bundles
- claim ledgers
- allow/deny lists
- citation allocation
- drafting contracts
- validators

Ana pilot bölüm:
`SEC-02-2 — Püskürtme Beton`

Yan bölümler:
- SEC-02-1 — destek sistemleri
- SEC-02-3 — kazı yöntemi / TBM / drill-blast

## 6. Architecture V1 ve Neden Bırakıldı

İlk yaklaşım daha serbest prose generation temelliydi.

Sorunlar:
- qualifier dropping
- condition dropping
- unsupported vocabulary
- `UNSUPPORTED_PROPOSITION`
- açık-set LLM yüzey üretimi ile kapalı-set validator çatışması

Örnekler:
- C-002 kabul kriteri anlamının bulanıklaşması
- P0-008’te `kayaç`, `spesifik` gibi izin dışı kelimeler
- qualifier/condition kaybı

Sonuç:
**Architecture V1 RETIRED**

## 7. Architecture D / V2

Yeni mimari:

**Structured Semantic Plan + Deterministic Surface Renderer**

LLM yalnız:
- claim selection / omission
- order
- grouping
- rhetorical role
- qualifier slot placement
- topic structure

seçer.

LLM görünür teknik metni özgürce yazmaz.

Deterministic renderer:
- factual words
- numbers
- units
- condition wording
- qualifier wording
- modality
- citations
- morphology

üzerinden kontrol sağlar.

Architecture V2 M1–M5:
- M1 Draft Plan IR Contract
- M2 Claim Realization Contract
- M3 deterministic Turkish morphology
- M4 deterministic renderer
- M5 static containment proof

Sonuç:
**Architecture V2 CLOSED / GO**

## 8. Pilot #1 Failure

Architecture V2 Pilot #1 reddedildi.

İlk izlenim model hatasıydı ancak failure analysis şunu buldu:

`AUTHORISATION_OPTION_UNIVERSE_DEFECT`

C-005 için condition zorunluydu fakat available role seti bunu sağlayamıyordu.
Planner universe ile feasibility universe tutarsızdı.

Ayrıca M2’de Türkçe tespit heuristiğinde false-negative bulundu.

Planner universe remediation sonrası:
`required ⊆ available ⊆ realizable`

invariantı sağlandı.

## 9. Pilot #2

Architecture V2 Pilot #2:

**ACCEPTED / CLOSED / GO**

- 1 model call
- semantic plan valid
- 19 slot / 16 claim
- 0 unrealizable
- validator histogram `{}`
- citation rendering PASS
- deterministic
- `PILOT_DRAFT_ACCEPTED`

Bu final manuscript değildi.

## 10. Technical Draft Audit V1

Pilot #2 teknik audit sonucu:

**CLOSED / NO-GO**

6 blocker:
1. C-004/C-005 wet-system scope eksik
2. C-012 repair-work scope eksik
3. P0-008 named rock classes eksik
4. 500 kg/m³ maximum cement bilgisi eksik
5. cement citation yanlış allocation
6. C-002 acceptance kriteri anlamı bulanık

Style sorunları:
- bare identifier title
- hierarchy eksik
- note-like fragments
- orphan qualifier
- redundancy
- `katman/tabaka` tutarsızlığı

Book Style Contract v1 bu aşamada oluşturuldu.

## 11. Technical Scope + Citation Remediation

TDA-001–006 için versioned remediation yapıldı.

Sonuç:
**CLOSED / GO**

Kapandı:
- wet-system scope
- repair-work scope
- P0-008 named rock classes
- C-018 500 kg/m³ maximum cement
- doğru citation allocation
- C-002’nin 22.5/25.5 MPa kabul kriteri anlamı

## 12. V2.2 İlk Integration NO-GO

Technical + Book Style integration ilk denemesi fail-closed oldu:

`V22_REQUIRED_ROLE_UNREALIZABLE`

P0-008 CASE_SCOPE içinde `Swelling Rock` için authoritative Turkish term yoktu.

## 13. Turkish Terminology Resolution

Authoritative Turkish equivalent arandı ancak bulunmadı.

Sonuç:
**CLOSED / NO-GO**

Tahmini çeviri yapılmadı.

## 14. Original-Language Fallback Policy

Genel editorial policy:

Authoritative Turkish equivalent yoksa teknik terim orijinal dilinde korunabilir.

Örnek:
- semantic value: `Swelling Rock`
- status: `ORIGINAL_TERM_UNRESOLVED`
- visible Markdown: `**Swelling Rock**`

Kurallar:
- Türkçe çeviri uydurulmaz.
- Açıklayıcı gloss eklenmez.
- Bold yalnız presentation layer’dır.
- Semantic ownership markup dışıdır.
- Gelecekte authoritative translation bulunursa merkezi/versioned mapping yapılır.

Fallback Contract V1:
**CLOSED / GO**

## 15. V2.2 Retry ve CONDITION_DROPPED

Fallback sonrası retry’de:

`CONDITION_DROPPED`

Affected:
- `SEC-02-2-P0-008`
- role `CASE_SCOPE`
- unit `U-C-P02-S02`

Failure analysis:
`MULTI_ROLE_CLAIM_CONDITION_ALLOCATION_DEFECT`

CASE_SCOPE condition yükümlülüğü taşıyordu ama:
- condition ona allocated değildi
- role bunu realize edemiyordu
- adjacent unit satisfaction kabul edilmemeliydi

Ayrıca latent dependency emission gap bulundu.

## 16. Claim-Role Condition Closure

Genel remediation:

Her claim×role için render öncesinde:
- lexical feasibility
- condition feasibility
- dependency feasibility
- explicit owner
- validator scope compatibility

kapanmak zorunda.

Sonuç:
**CLOSED / GO**

- 25/25 condition
- 20/20 allocated claim×role feasible
- 2/2 dependency closure
- eski invalid P0-008 allocation pre-prose reject

## 17. V2.2 Technical + Style Retry

Condition closure sonrası integration:

**CLOSED / GO**

- 16/16 acceptance
- 6/6 blockers
- topics 3/3
- citation PASS
- fallback PASS
- factual completeness PASS
- Book Style PASS
- histogram `{}`
- deterministic

Accepted draft üretildi ama release edilmedi.

## 18. Technical Draft Re-Audit V2

Sonuç:
**CLOSED / NO-GO**

Yeni yüzey problemleri:
1. TDA-006 reopened
2. Book Style fragment / note-label
3. `tabaka/katman` tutarsızlığı

Advisory:
`minimum C25/30 MPa sınıfında`

Failure analysis:
- TDA-006 → semantic-subject binding failure
- style → projection fragment
- terminology → preferred-term allocation kapanmamış
- advisory → inherited redundant wording

Validator çalışıyordu ancak coverage gap vardı.

## 19. General Realization / Style / Terminology Closure

Yeni genel closure:
- typed subject/predicate binding
- complete-sentence feasibility
- material note-label exclusion
- preferred-term allocation
- no free terminology variants
- post-render binding/fragment/label checks
- strength-class/unit duplication advisory lint

Sonuç:
**CLOSED / GO**

## 20. General Closure Rerun

Yeni accepted draft:

**GO**

- 6/6 blockers
- 25/25 conditions
- 2/2 dependencies
- citation PASS
- factual completeness PASS
- Book Style PASS
- terminology PASS
- unresolved Swelling Rock preserved
- histogram `{}`
- deterministic

Accepted draft SHA-256:

`b63a422850a8791452cd923f40a27901ffa82ca4d5b36d15776f8fb40ba05e12`

## 21. Technical Draft Re-Audit V3

Sonuç:

**GO — no new blocker**

- blocking findings: none
- six blockers 6/6 CLOSED
- citation/support 19/19 PASS
- conditions 25/25
- dependencies 2/2
- scope/terminology PASS
- release recommendation: RELEASE

Advisories:
- redundant `C25/30 MPa`
- adjacent 22.5/25.5 MPa repetition

## 22. State-Synchronization Sorunu

Tekrarlayan workflow sorunu:

Bazı phase scriptleri authoritative GO artifact üretmesine rağmen:
- `docs/ai/CURRENT_STATE.md`
- `docs/ai/NEXT_PHASE.md`

dosyalarını ilerletmiyor.

Bu yüzden mismatch guard doğru şekilde durdu:
`NOT EXECUTED — phase mismatch`

Bu, teknik draft hatası değil workflow/state-sync problemidir.

Mevcut durumda V3 GO olmasına rağmen NEXT_PHASE henüz release authorization’a taşınmadan önce
state reconciliation yapılmalıdır.


<!-- FILE: 02_WORKING_RULES_MODELS_AND_TOKEN_POLICY.md -->

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


<!-- FILE: 03_PROMPT_LIBRARY.md -->

# TunnelBookAI – Prompt Library

## Normal New Phase

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.
Execute NEXT_PHASE exactly.

Use targeted reads/tests only.
Do not commit or push.
```

## Phase Identity Guard

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<EXACT_PHASE_NAME>

If it matches, execute that phase exactly.
If not, STOP and report the mismatch.

Use targeted reads/tests only.
Do not scan the corpus.
Do not commit or push.
```

## Technical Audit

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<TECHNICAL_AUDIT_PHASE>

If it matches, execute that phase exactly.

Audit only the authorized accepted draft.
Do not regenerate or rewrite it.
Do not scan the corpus.
Do not modify frozen historical artifacts.
Do not commit or push.

Focus on:
- technical correctness
- factual completeness
- claim-to-citation support
- scope fidelity
- terminology consistency
- sentence and paragraph quality
- ambiguity and redundancy
- prior blocker preservation
- new blockers

Return only:
- status
- blocking findings
- advisory findings
- blocker status
- citation/support status
- scope/terminology status
- release recommendation
- tests/probes
- changed files
- next phase

Final <= 220 words.
```

## Failure Analysis

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
<FAILURE_ANALYSIS_PHASE>

If it matches, execute that phase exactly.

Analyze only preserved failure evidence.
Do not rewrite/regenerate.
Do not scan the corpus.
Do not weaken validators.
Do not commit or push.

Determine root cause per finding:
- realization contract
- style integration
- terminology allocation
- renderer
- validator coverage gap
- other evidenced cause

Specify the smallest general remediation.
No claim-specific patch.

Return only:
- status
- root cause per finding
- validator fault yes/no
- renderer fault yes/no
- style-contract fault yes/no
- smallest remediation
- tests/probes
- changed files
- next phase

Final <= 220 words.
```

## State Reconciliation Pattern

```text
Follow AGENTS.md.

This is state reconciliation only.

Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Then read only the authoritative artifacts for:
<COMPLETED_PHASE>

Verify the phase completed GO.

Do NOT rerun the phase.
Do NOT regenerate/render.
Do NOT scan the corpus.
Do NOT modify historical artifacts.
Do NOT commit or push.

If authoritative artifacts confirm GO:
Update only:
- docs/ai/CURRENT_STATE.md
- docs/ai/NEXT_PHASE.md

CURRENT_STATE must record the phase as CLOSED / GO.

NEXT_PHASE must become exactly:
<NEXT_PHASE>

If evidence does not support this:
make no changes and report mismatch.

Return only:
- status
- evidence checked
- state docs changed
- resulting NEXT_PHASE

Final <= 150 words.
```

## LAST PROMPT GIVEN — NOT YET RUN

Bu kullanıcı tarafından “aklında tut” denilen son prompttur.

```text
Follow AGENTS.md.

This is state reconciliation only.

Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Then read only the authoritative artifacts for:

SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3

Verify that V3 actually completed GO with:

- no blocking findings
- six blockers 6/6 CLOSED
- citation/support 19/19 PASS
- conditions 25/25
- dependencies 2/2
- unresolved Swelling Rock fallback preserved
- terminology/scope PASS
- validator histogram {}
- release recommendation = RELEASE
- accepted draft unchanged

Do NOT rerun V3.
Do NOT regenerate/render anything.
Do NOT scan the corpus.
Do NOT modify historical artifacts.
Do NOT commit or push.

If authoritative V3 artifacts confirm GO:

Update only:
- docs/ai/CURRENT_STATE.md
- docs/ai/NEXT_PHASE.md

CURRENT_STATE must record:

SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3 = CLOSED / GO

NEXT_PHASE must become exactly:

SEC-02-2 RELEASE AUTHORISATION V1

Preserve the two V3 advisories as non-blocking advisories.

If evidence does not support this transition:
make no changes and report the mismatch.

Return only:
- status
- evidence checked
- state docs changed
- resulting NEXT_PHASE

Final <= 150 words.
```

## Release Authorisation Template

State reconciliation başarıyla tamamlandıktan sonra:

```text
Read:
docs/ai/CURRENT_STATE.md
docs/ai/NEXT_PHASE.md

Follow AGENTS.md.

Confirm NEXT_PHASE is:
SEC-02-2 RELEASE AUTHORISATION V1

If it matches, execute that phase exactly.

Use only:
- accepted V2.2 general-closure rerun draft
- Technical Draft Re-Audit V3
- frozen release/citation/style/technical evidence required by NEXT_PHASE

Do not regenerate or rewrite the draft.
Do not scan the corpus.
Do not modify frozen historical artifacts.
Do not commit or push.

Release only if all required gates remain satisfied:
- V3 re-audit GO
- 6/6 blockers closed
- citation/support PASS
- factual completeness PASS
- scope/terminology PASS
- condition/dependency closure PASS
- unresolved-term fallback PASS
- Book Style PASS
- validator histogram {}
- accepted draft hash unchanged

Preserve advisory findings as advisories.

Return only:
- status
- release decision
- release gates
- draft/hash identity
- unresolved advisories
- frozen integrity
- changed files
- next phase

Final <= 200 words.
```


<!-- FILE: 04_CURRENT_STATE_AND_NEXT_ACTION.md -->

# TunnelBookAI – Current State and Next Action

## Last Confirmed Technical Result

`SEC-02-2 TECHNICAL DRAFT RE-AUDIT V3`

Result:
**GO — no new blocker**

### Results

- blocking findings: none
- six blockers: 6/6 CLOSED
- citation/support: 19/19 PASS
- conditions: 25/25
- dependencies: 2/2
- unresolved `Swelling Rock` fallback: preserved
- scope/terminology: PASS
- validator histogram: `{}`
- release recommendation: RELEASE

### Non-blocking Advisories

1. Redundant `C25/30 MPa` strength-class/unit wording
2. Repeated 22.5/25.5 MPa acceptance values in adjacent sentences

## Accepted Draft SHA-256

`b63a422850a8791452cd923f40a27901ffa82ca4d5b36d15776f8fb40ba05e12`

## Current Workflow Problem

V3 GO artifact exists, but `NEXT_PHASE.md` remained at V3.
This is a state-synchronization issue.

Codex’s phase mismatch guard correctly stopped release authorization.

The correct immediate action is NOT to rerun V3.

Run the exact state reconciliation prompt in:
`03_PROMPT_LIBRARY.md → LAST PROMPT GIVEN — NOT YET RUN`

Expected result:

`NEXT_PHASE = SEC-02-2 RELEASE AUTHORISATION V1`

## Do Not Do Yet

- Do not rerun V3.
- Do not release before state reconciliation.
- Do not silently rewrite advisories.
- Do not weaken validators.
- Do not scan the corpus.
- Do not modify historical artifacts.
- Do not commit or push unless explicitly requested.

## Model

State reconciliation:
**GPT-5.6 Sol — Low**

Release Authorization after reconciliation:
**GPT-5.6 Sol — Medium**


<!-- FILE: 05_ARCHITECTURE_AND_INVARIANTS.md -->

# TunnelBookAI – Architecture and Invariants

## Frozen Pipeline Snapshot

### Corpus
- canonical documents: 214
- semantic chunks v1.1: 6039
- embedding input: 5992
- canonical embedding rows: 5980
- recovery rows: 12

### Embeddings
- BGE-M3
- dimension 1024
- Qdrant `tunnelbook_dense_v1`
- cosine

### Retrieval
- dense-only
- hybrid/translation/reranker empirically rejected
- Retriever V1 CLOSED / GO
- RAG Context CLOSED / GO

### Generation
- local model: `qwen3.6-35b-a3b-mlx`
- Prompt v5 frozen
- no Prompt v6 without separate experiment
- production grounded generator frozen

## Book Architecture

Evidence:
- source registry
- evidence notes
- research questions/runs
- section bundles
- claim ledgers
- citation allocation

Drafting:
- semantic plan IR
- claim realization contract
- deterministic morphology
- deterministic renderer
- static containment proof
- Book Style Contract
- validators

General closures:
- condition ownership
- dependency ownership
- semantic subject/predicate binding
- complete-sentence feasibility
- preferred-term allocation
- no free variants
- material note-label exclusion
- unresolved original-language fallback

## Critical Invariants

1. Frozen upstream artifacts immutable.
2. Wrong metadata worse than blank.
3. Evidence-only; unresolved allowed.
4. Provenance/citations preserved.
5. No hallucinated repair.
6. No model-generated gold.
7. Dev/eval separated.
8. No self-judge as sole authority.
9. Never weaken validators just to pass.
10. Evidence is untrusted data.
11. Contract failure → reject.
12. No same-config retry.
13. No automatic rewrite/translate/repair.
14. Corrections create new versions; history preserved.
15. Qdrant read-only except explicit indexing.
16. Book source policy defaults to corpus_only.
17. Packet-local `[E###]` IDs are not stable public refs.
18. Acceptance criteria freeze before outcome.
19. Script slots collision-check.
20. Qdrant unreachable → unknown/unobserved.
21. AI review is not human/manual review.
22. Pilot prose ≠ final manuscript.
23. Citation support must prove claim→source association.

## Original-Language Technical Term Policy

States:
- `AUTHORITATIVE_TRANSLATION`
- `ORIGINAL_TERM_UNRESOLVED`

For unresolved terms:
- exact source term retained semantically
- authoritative translation = null
- presentation = bold
- example: `**Swelling Rock**`
- no invented Turkish translation
- no explanatory gloss
- markup excluded from semantic ownership
- future replacement centralized + versioned

## SEC-02-2 Position

Current accepted surface passed:
- 6/6 blocker closures
- 25/25 conditions
- 2/2 dependencies
- citation support
- factual completeness
- Book Style
- terminology consistency
- unresolved fallback
- deterministic rendering

Release Authorization is pending because of state synchronization, not because the draft failed.
