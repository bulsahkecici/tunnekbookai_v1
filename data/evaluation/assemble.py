# -*- coding: utf-8 -*-
import sys,json,re,hashlib,collections,subprocess
sys.path.insert(0,'.')
from pathlib import Path
from builder import build_item, PACKETS
from spec_df import DF
from spec_dc_ms import DC,MS
from spec_nt_rs import NT,RS
from spec_cl_ma_ia import CL,MA,IA

ROOT=Path("/Users/bulsahkecici/Projects/tunnel/_TunnelBookAI")
ORDER=DF+DC+MS+NT+RS+CL+MA+IA
assert len(ORDER)==72, len(ORDER)
items=[build_item(i,s) for i,s in enumerate(ORDER,1)]

FAIL=[]
def check(cond,msg):
    if not cond: FAIL.append(msg)

# ---- structural ----
check(len(items)==72, f"item count {len(items)}")
ids=[it["query_id"] for it in items]
check(len(set(ids))==72,"duplicate query_id")
check(ids==[f"GEV{i:03d}" for i in range(1,73)],"query_id sequence broken")
REQUIRED=["benchmark_version","query_id","primary_query_type","secondary_tags","language","query",
 "answerability","must_abstain","retrieval_limited","retrieval_limited_reason","retriever_release",
 "retriever_config","context_contract","context_packet_sha","context_text_sha","context_token_count",
 "context_token_budget","evidence_ids","evidence_count","document_ids_or_source_keys","gold_claims",
 "gold_answer_summary","gold_support","numeric_gold","conflict_gold","injection_metadata","notes",
 "authoring_status"]
for it in items:
    for f in REQUIRED: check(f in it, f"{it['query_id']} missing field {f}")
    check(bool(it["query"].strip()), f"{it['query_id']} empty query")
    check(bool(it["context_packet_sha"]), f"{it['query_id']} missing packet sha")
    check("model_answer" not in it and "generated_answer" not in it, f"{it['query_id']} model output field")

# ---- distribution ----
dist=collections.Counter(it["primary_query_type"] for it in items)
EXPECT={"direct_factual_conceptual":18,"design_construction":10,"multi_source_synthesis":10,
        "numeric_table":8,"regulation_specification":6,"cross_lingual":6,"must_abstain":8,
        "injection_adversarial":6}
check(dict(dist)==EXPECT, f"category distribution {dict(dist)}")
langs=collections.Counter(it["language"] for it in items)
check(abs(langs["tr"]-36)<=2 and abs(langs["en"]-36)<=2, f"language balance {dict(langs)}")

# ---- gold integrity ----
for it in items:
    pk=PACKETS[[s for s in ORDER if True][items.index(it)]["cid"]]
    ev={e["evidence_id"]:e for e in pk["evidence"]}
    excluded={x["chunk_id"] for x in pk["excluded"]}
    for sup in it["gold_support"]:
        e=ev.get(sup["evidence_id"])
        check(e is not None, f"{it['query_id']} support cites unknown {sup['evidence_id']}")
        if e:
            check(e["text"][sup["span_start"]:sup["span_end"]]==sup["literal_span"],
                  f"{it['query_id']} span mismatch {sup['evidence_id']}")
            check(e["text_sha256"]==sup["evidence_text_sha256"], f"{it['query_id']} evidence sha drift")
            check(e["chunk_id"] not in excluded, f"{it['query_id']} cites excluded chunk")
    for c in it["gold_claims"]:
        for eid in c["supporting_evidence_ids"]:
            check(eid in ev, f"{it['query_id']} claim cites unknown {eid}")
        if c["support_status"]=="supported":
            check(c["supporting_evidence_ids"], f"{it['query_id']} {c['claim_id']} supported w/o evidence")
        if it["answerability"]=="answerable" and c["required"]:
            check(c["support_status"]=="supported",
                  f"{it['query_id']} required claim unsupported on answerable item")
    for n in (it["numeric_gold"] or []):
        e=ev[n["supporting_evidence_id"]]
        check(e["text"][n["span_start"]:n["span_end"]]==n["literal_span"], f"{it['query_id']} numeric span")
        check(bool(n["unit"]), f"{it['query_id']} numeric missing unit")
        digits=re.findall(r"[\d]+(?:[.,]\d+)?",n["value"])
        for d in digits:
            check(d in n["literal_span"], f"{it['query_id']} numeric value {d} not literal in span")
    if it["must_abstain"]:
        check(it["answerability"]=="unanswerable", f"{it['query_id']} must_abstain but answerable")
        types={c["claim_type"] for c in it["gold_claims"]}
        check(types=={"abstention"}, f"{it['query_id']} must_abstain has non-abstention claims {types}")
    if it["primary_query_type"]=="must_abstain":
        check(it["must_abstain"], f"{it['query_id']} must_abstain type without flag")
    if it["primary_query_type"]=="multi_source_synthesis":
        check(len(it["gold_evidence_ids"])>=2, f"{it['query_id']} multi-source <2 evidence")
        check(it["minimum_required_evidence_count"]>=2, f"{it['query_id']} min_evidence not set")
        docs={ev[e]["document_id"] for e in it["gold_evidence_ids"]}
        check(len(docs)>=2, f"{it['query_id']} multi-source single document {docs}")
    if it["primary_query_type"]=="cross_lingual":
        m=it["cross_lingual_metadata"]
        check(m is not None, f"{it['query_id']} cross-lingual metadata missing")
        check(m["query_language"]!=m["dominant_evidence_language"] or "en_query_tr" in m["cross_lingual_direction"]
              or "tr_query_en" in m["cross_lingual_direction"], f"{it['query_id']} cross-lingual not a mismatch")
    if it["primary_query_type"]=="injection_adversarial":
        m=it["injection_metadata"]
        check(m is not None, f"{it['query_id']} injection metadata missing")
        for k in ("injection_present","injection_type","technical_imperative_control","expected_behavior"):
            check(k in m, f"{it['query_id']} injection metadata missing {k}")
controls=[it for it in items if (it["injection_metadata"] or {}).get("technical_imperative_control")]
check(len(controls)>=2, f"benign imperative controls {len(controls)}")

# ---- leakage ----
for it in items:
    q=it["query"]
    check(not re.search(r"\bE\d{3}\b",q), f"{it['query_id']} query leaks evidence id")
    check(not re.search(r"DOC\d{6}",q), f"{it['query_id']} query leaks document id")
    check("ContextPacket" not in q and "packet" not in q.lower(), f"{it['query_id']} query mentions packet")
    for sup in it["gold_support"]:
        span=sup["literal_span"]
        if len(span)>40: check(span not in q, f"{it['query_id']} query contains gold span")

# ---- duplicates ----
qs=[it["query"].strip().lower() for it in items]
check(len(set(qs))==72,"duplicate query text")
sig=collections.Counter()
for it in items:
    for sup in it["gold_support"]:
        sig[(sup["evidence_text_sha256"],sup["span_start"],sup["span_end"])]+=1
dupspans={k:v for k,v in sig.items() if v>1}
check(not dupspans, f"{len(dupspans)} gold spans reused across items")

# ---- diversity ----
alldocs=collections.Counter()      # gold-evidence references per document
docitems=collections.Counter()     # distinct benchmark items drawing gold from a document
allchunks=collections.Counter()
for it,spec in zip(items,ORDER):
    pk=PACKETS[spec["cid"]]; ev={e["evidence_id"]:e for e in pk["evidence"]}
    seen=set()
    for eid in it["gold_evidence_ids"]:
        d=ev[eid]["document_id"]
        alldocs[d]+=1
        allchunks[ev[eid]["chunk_id"]]+=1
        if d not in seen: docitems[d]+=1; seen.add(d)
diff=collections.Counter(it["difficulty"] for it in items)
ans=collections.Counter(it["answerability"] for it in items)
rl=[it["query_id"] for it in items if it["retrieval_limited"]]

if FAIL:
    print("AUDIT FAILURES:"); [print("  -",f) for f in FAIL[:40]]; print(f"total {len(FAIL)}"); sys.exit(1)

out=ROOT/"data/evaluation/generation_eval_benchmark_v1.jsonl"
with out.open("w",encoding="utf-8") as f:
    for it in items: f.write(json.dumps(it,ensure_ascii=False,sort_keys=True)+"\n")
sha=hashlib.sha256(out.read_bytes()).hexdigest()
now=subprocess.run(["date","-Iseconds"],capture_output=True,text=True).stdout.strip()
man={"benchmark_version":"generation-eval-benchmark-v1","item_count":len(items),
 "category_distribution":dict(sorted(dist.items())),"language_distribution":dict(sorted(langs.items())),
 "answerability_distribution":dict(sorted(ans.items())),"difficulty_distribution":dict(sorted(diff.items())),
 "must_abstain_items":sum(1 for it in items if it["must_abstain"]),
 "retrieval_limited_items":rl,
 "unique_source_count":len(alldocs),"unique_evidence_count":len(allchunks),
 "top_10_documents_by_gold_reference":alldocs.most_common(10),
 "top_10_documents_by_item_count":docitems.most_common(10),
 "max_gold_references_from_single_document":alldocs.most_common(1)[0][1],
 "max_items_sourced_from_single_document":docitems.most_common(1)[0][1],
 "max_evidence_chunk_reuse":allchunks.most_common(1)[0][1],
 "retriever_release":"tunnelbook-retriever-v1",
 "retriever_sha":hashlib.sha256((ROOT/"scripts/19_retriever_v1.py").read_bytes()).hexdigest(),
 "context_contract_version":"tunnelbook-context-v1",
 "context_implementation_sha":hashlib.sha256((ROOT/"scripts/20_rag_context.py").read_bytes()).hexdigest(),
 "retrieval_top_k":PACKETS["DF01"]["top_k"],
 "citation_validator_version":"citation-validator-v1.2",
 "system_prompt_version":"generation-system-prompt-v3",
 "system_prompt_sha":hashlib.sha256((ROOT/"data/metadata/generation_system_prompt_v3.txt").read_bytes()).hexdigest(),
 "tokenizer_sha":"87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4",
 "template_sha":"e84f32a23fdda27689f868aa4a1a5621f41133e51a48d7f3efcbea2839574259",
 "runtime_loaded_context":71936,"authoring_rag_budget":64610,
 "benchmark_jsonl_sha256":sha,"created_at":now,"frozen_at":now,
 "generation_calls_during_authoring":0,"status":"frozen"}
(ROOT/"data/evaluation/generation_eval_benchmark_v1_manifest.json").write_text(
    json.dumps(man,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("AUDIT PASSED")
print(json.dumps({k:man[k] for k in ("item_count","category_distribution","language_distribution",
 "answerability_distribution","difficulty_distribution","must_abstain_items","unique_source_count",
 "unique_evidence_count","max_items_sourced_from_single_document","max_gold_references_from_single_document","max_evidence_chunk_reuse",
 "benchmark_jsonl_sha256")},indent=1,ensure_ascii=False))
print("retrieval_limited:",rl)
print("top docs by item:",man["top_10_documents_by_item_count"][:8])
