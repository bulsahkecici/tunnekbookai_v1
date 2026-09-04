"""Benchmark builder. Gold claims name a search key that the author copied from the frozen
evidence while reading it; the builder re-locates that key in the ORIGINAL evidence text
(whitespace-flexible) and records the exact original substring plus its offsets. The recorded
literal_span is therefore always an exact substring of the evidence item, never a paraphrase."""
import json,re,unicodedata
from pathlib import Path

BENCH=Path(__file__).parent
PACKETS={json.loads(l)["cid"]:json.loads(l) for l in (BENCH/"generation_eval_benchmark_v1_packets.jsonl").open()}

class SpanNotFound(Exception): pass

def locate(evidence_text: str, key: str):
    """Find `key` in evidence_text tolerating whitespace differences. Returns (span,start,end)."""
    parts=[re.escape(tok) for tok in key.split()]
    pattern=re.compile(r"\s+".join(parts))
    m=pattern.search(evidence_text)
    if not m:
        raise SpanNotFound(key)
    return evidence_text[m.start():m.end()], m.start(), m.end()

def build_item(idx, spec):
    cid=spec["cid"]; pk=PACKETS[cid]
    ev={e["evidence_id"]:e for e in pk["evidence"]}
    excluded_chunks={x["chunk_id"] for x in pk["excluded"]}
    qid=f"GEV{idx:03d}"
    claims=[]; support=[]
    for (claim_id,text,ctype,required,refs) in spec["claims"]:
        eids=[]
        for eid,key in refs:
            if eid not in ev:
                raise KeyError(f"{cid} {claim_id}: evidence {eid} not in packet")
            span,s,e=locate(ev[eid]["text"],key)
            support.append({"claim_id":claim_id,"evidence_id":eid,"literal_span":span,
                            "span_start":s,"span_end":e,"span_scope":"evidence_item",
                            "evidence_text_sha256":ev[eid]["text_sha256"]})
            eids.append(eid)
        status="supported" if eids else "unsupported"
        claims.append({"claim_id":claim_id,"claim_text":text,"claim_type":ctype,
                       "required":required,"supporting_evidence_ids":eids,"support_status":status})
    numeric=[]
    for n in spec.get("numeric",[]):
        span,s,e=locate(ev[n["evidence_id"]]["text"],n["key"])
        numeric.append({"value":n["value"],"unit":n["unit"],"tolerance":n.get("tolerance","exact_textual"),
                        "operation":n["operation"],"supporting_evidence_id":n["evidence_id"],
                        "literal_span":span,"span_start":s,"span_end":e,"span_scope":"evidence_item",
                        "unit_conversion_allowed":n.get("conversion",False)})
    conflict=spec.get("conflict")
    if conflict:
        for side in conflict["sides"]:
            for eid,key in side.pop("refs"):
                span,s,e=locate(ev[eid]["text"],key)
                side.setdefault("supporting_evidence_ids",[]).append(eid)
                side.setdefault("literal_spans",[]).append(
                    {"evidence_id":eid,"literal_span":span,"span_start":s,"span_end":e,
                     "span_scope":"evidence_item"})
    used=sorted({e for c in claims for e in c["supporting_evidence_ids"]})
    langs={}
    for e in pk["evidence"]: langs[e["language"]]=langs.get(e["language"],0)+1
    dominant=max(langs,key=langs.get) if langs else None
    cross=spec.get("cross")
    if cross:
        cross={"query_language":pk["lang"],"dominant_evidence_language":cross["dominant"],
               "cross_lingual_direction":cross["direction"],
               "evidence_language_counts":{str(k):v for k,v in langs.items()}}
    return {
      "benchmark_version":"generation-eval-benchmark-v1",
      "query_id":qid,"primary_query_type":spec["type"],
      "secondary_tags":spec.get("tags",[]),"language":pk["lang"],"query":pk["query"],
      "difficulty":spec["difficulty"],
      "answerability":spec["answerability"],"must_abstain":spec["must_abstain"],
      "retrieval_limited":spec["retrieval_limited"],
      "retrieval_limited_reason":spec.get("rl_reason"),
      "retriever_release":pk_meta("retriever_release"),"retriever_config":{
          "retriever":"DENSE_V1","retrieval_top_k":pk["top_k"],
          "context_max_tokens":pk["token_budget"],"filters":None},
      "context_contract":"tunnelbook-context-v1",
      "context_packet_sha":pk["packet_sha"],"context_text_sha":pk["context_text_sha"],
      "context_token_count":pk["token_count"],"context_token_budget":pk["token_budget"],
      "evidence_ids":[e["evidence_id"] for e in pk["evidence"]],
      "evidence_count":pk["selected_count"],
      "document_ids_or_source_keys":sorted({e["document_id"] for e in pk["evidence"]}),
      "gold_evidence_ids":used,
      "minimum_required_evidence_count":spec.get("min_evidence"),
      "gold_claims":claims,"gold_answer_summary":spec["summary"],"gold_support":support,
      "numeric_gold":numeric or None,"conflict_gold":conflict,
      "injection_metadata":spec.get("injection"),
      "cross_lingual_metadata":cross,
      "dominant_evidence_language_metadata":dominant,
      "excluded_chunk_count":len(excluded_chunks),
      "notes":spec.get("notes",""),"authoring_status":"human_authored_evidence_verified",
      "authoring_method":"manual_reading_of_frozen_packet_then_programmatic_span_location",
    }

_META={}
def pk_meta(k): return _META.get(k,"tunnelbook-retriever-v1")
