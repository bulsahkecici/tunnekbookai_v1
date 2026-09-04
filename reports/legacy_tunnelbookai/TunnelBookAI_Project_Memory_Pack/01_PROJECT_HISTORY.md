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
