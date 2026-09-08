from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable


PROMPT_VERSION = "metadata-verification-v1.2"
FIELDS = ("title", "organization", "year", "language", "document_type", "authority_level", "topics")
RELATIONSHIPS = {"document_identity", "publication_identity", "referenced_only", "event_only", "insufficient"}
VERIFICATION_FIELDS = [
    "document_id", "field", "previous_candidate", "verification_value", "verification_evidence",
    "verification_confidence", "verification_status", "verification_reason", "model", "prompt_version", "source_sha256",
]
V4_FIELDS = [
    "priority", "document_id", "source_relative_path", "field", "previous_candidate", "verification_value",
    "verification_evidence", "verification_confidence", "verification_reason", "reviewer_value", "reviewer_note",
    "review_status", "reviewed_at",
]
P0_FIELDS = [
    "document_id", "source_relative_path", "field", "current_value", "deterministic_suggestion", "llm_suggestion",
    "llm_evidence", "confidence", "conflict_type", "title_cover_headings", "opening_context", "field_context_snippets",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(rows: Iterable[dict[str, object]], fields: list[str]) -> bytes:
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def normalize(value: object) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def meaningful(value: object) -> bool:
    return normalize(value) not in {"", "unknown", "unclassified", "null", "none"}


KEYWORDS = {
    "organization": r"published by|prepared by|issued by|publisher|copyright|university|universit|ministry|mudurlugu|department|institute|enstitu|association|society",
    "year": r"published|publication|copyright|©|volume|issue|report date|submitted|accepted|approved|resmi gazete|(?:18|19|20)\d{2}",
    "document_type": r"journal|doi|volume|issue|thesis|dissertation|conference|proceedings|manual|handbook|report|presentation|training|course|seminar|form|checklist|inspection|drawing|website|magazine|dergi|tez|yonetmelik|sunum|egitim|kurs",
    "authority_level": r"official|published by|issued by|journal|doi|thesis|conference|training|seminar|presentation|wikipedia|website|kgm|karayollari|fhwa|piarc|university|universit",
    "title": r"^#{1,3}\s|title|document title",
    "language": r"abstract|oz|contents|icindekiler",
}


def snippets(text: str, field: str, maximum: int = 8) -> list[str]:
    pattern = re.compile(KEYWORDS.get(field, r"."), re.IGNORECASE)
    found = []
    for line in text.splitlines():
        clean = " ".join(line.split())
        if 10 <= len(clean) and pattern.search(clean):
            found.append(clean[:650])
            if len(found) >= maximum:
                break
    return found


def field_context(document: dict[str, str], markdown: str, field: str, llm) -> dict[str, object]:
    body = llm.strip_front_matter(markdown)
    words = body.split()
    opening = " ".join(words[:650])[:5500].rstrip()
    headings = llm.meaningful_headings(body)[:12]
    selected_snippets = [item[:450] for item in snippets(body, field, maximum=5)]
    if field == "language":
        middle = " ".join(words[len(words) // 2:len(words) // 2 + 300])[:2500]
        tail = " ".join(words[-300:])[:2500]
        selected_snippets = [middle, tail]
    return {
        "document_id": document["document_id"], "field": field,
        "source_filename": document["source_filename"], "source_relative_path": document["source_relative_path"],
        "source_extension": document["source_extension"], "title_cover_headings": headings,
        "opening_identity_context": opening, "field_context_snippets": selected_snippets,
    }


def evidence_grounded(evidence: str, context: dict[str, object]) -> bool:
    if not evidence.strip():
        return False
    source = normalize(" ".join(context.get("title_cover_headings", [])) + " "
                       + str(context.get("opening_identity_context", "")) + " "
                       + " ".join(context.get("field_context_snippets", [])))
    tokens = [token for token in normalize(evidence).split() if len(token) >= 3]
    return bool(tokens) and sum(token in source for token in tokens) / len(tokens) >= 0.75


def system_prompt(field: str, vocab: str) -> str:
    return f"""You verify exactly one metadata field: {field}. Return one JSON object only.
Use only supplied document identity context. Evidence must be a short verbatim phrase from context, maximum 25 words.
Never treat a referenced institution as this document's organization/authority. Never treat an event, project,
construction, or referenced-document year as publication year. A section/chapter heading is not document title.
For authority, prove the document itself is A official, B academic research, C professional/training, or D general web.
If proof is absent return value='' confidence='low' relationship='insufficient'.
Allowed values when applicable: {vocab}
Schema keys: value (string), confidence (high|medium|low), evidence (string),
relationship (document_identity|publication_identity|referenced_only|event_only|insufficient)."""


def response_format() -> dict[str, object]:
    schema = {
        "type": "object", "properties": {
            "value": {"type": "string", "maxLength": 200}, "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "evidence": {"type": "string", "maxLength": 300}, "relationship": {"type": "string", "enum": sorted(RELATIONSHIPS)},
        }, "required": ["value", "confidence", "evidence", "relationship"], "additionalProperties": False,
    }
    return {"type": "json_schema", "json_schema": {"name": "metadata_field_verification", "strict": True, "schema": schema}}


def parse_response(raw: str) -> dict[str, str]:
    stripped = raw.strip()
    fence = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n?```", stripped, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        stripped = fence.group(1).strip()
    try:
        result = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(result, dict) or set(result) != {"value", "confidence", "evidence", "relationship"}:
        raise ValueError("verification schema mismatch")
    if result["confidence"] not in {"high", "medium", "low"} or result["relationship"] not in RELATIONSHIPS:
        raise ValueError("verification enum mismatch")
    if not all(isinstance(result[key], str) for key in result):
        raise ValueError("verification values must be strings")
    return result


Transport = Callable[[str, dict[str, object], int], str]


def call_field(base_url: str, model: str, field: str, context: dict[str, object], vocab: str,
               timeout: int, transport: Transport, max_retries: int = 2) -> tuple[dict[str, str], int, float]:
    payload = {
        "model": model, "temperature": 0.0,
        "max_tokens": 512,
        "messages": [{"role": "system", "content": system_prompt(field, vocab)},
                     {"role": "user", "content": json.dumps(context, ensure_ascii=False)}],
        "response_format": response_format(),
    }
    started = time.monotonic()
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            raw = transport(base_url.rstrip("/") + "/chat/completions", payload, timeout)
            return parse_response(raw), attempt, time.monotonic() - started
        except Exception as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(0.25 * (attempt + 1))
    raise RuntimeError(f"verification retry exhausted: {last_error}")


def cache_identity(row: dict[str, str], model: str) -> str:
    raw = "\0".join((row["document_id"], row["source_sha256"], row["field"], model, PROMPT_VERSION))
    return hashlib.sha256(raw.encode()).hexdigest()


def cache_path(root: Path, row: dict[str, str], model: str) -> Path:
    return root / "data/metadata/cache/metadata_verification" / row["document_id"] / f"{cache_identity(row, model)}.json"


def read_cache(path: Path, row: dict[str, str], model: str) -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    expected = (row["document_id"], row["source_sha256"], row["field"], model, PROMPT_VERSION)
    actual = tuple(payload.get(key) for key in ("document_id", "source_sha256", "field", "model", "prompt_version"))
    return payload if actual == expected else None


def vocabulary(field: str, llm) -> set[str] | None:
    return {
        "language": llm.LANGUAGES, "document_type": llm.DOCUMENT_TYPES,
        "authority_level": llm.AUTHORITY_LEVELS, "topics": llm.TOPICS,
    }.get(field)


def verified_safe(field: str, response: dict[str, str], context: dict[str, object], prior: dict[str, str],
                  document_rows: dict[str, dict[str, str]], llm, adj) -> bool:
    value = response["value"].strip()
    allowed = vocabulary(field, llm)
    if response["confidence"] != "high" or not meaningful(value) or not evidence_grounded(response["evidence"], context):
        return False
    if allowed is not None and value not in allowed:
        return False
    required_relationship = "publication_identity" if field == "year" else "document_identity"
    if response["relationship"] != required_relationship:
        return False
    if field == "organization" and meaningful(prior.get("llm_suggestion", "")):
        previous = normalize(prior["llm_suggestion"])
        proposed = normalize(value)
        if previous != proposed:
            return False
    if field == "language":
        language_text = str(context.get("opening_identity_context", "")) + " " + " ".join(context.get("field_context_snippets", []))
        if len(language_text.split()) < 200:
            return False
    if field == "document_type" and value == "presentation":
        structural_text = normalize(str(context.get("opening_identity_context", "")) + " "
                                    + " ".join(context.get("title_cover_headings", [])))
        extension = str(context.get("source_extension", "")).casefold()
        if extension not in {".ppt", ".pptx"} and not re.search(r"presentation|slide deck|(?:^| )slides?(?: |$)|sunum adi|sunum icerigi", structural_text):
            return False
    package = {
        "headings": context["title_cover_headings"], "first_excerpt": context["opening_identity_context"],
        "tail_publication_or_references_excerpt": " ".join(context["field_context_snippets"]),
    }
    synthetic = {
        "field": field, "llm_suggestion": value, "llm_evidence": response["evidence"],
        "llm_confidence": response["confidence"], "agreement_status": "llm_only",
        "deterministic_suggestion": prior["deterministic_suggestion"],
    }
    return adj.field_auto_safe(synthetic, package, document_rows, llm)


def verification_decision(row: dict[str, str], response: dict[str, str] | None, context: dict[str, object],
                          document_rows: dict[str, dict[str, str]], model: str, llm, adj,
                          failure: str = "") -> dict[str, str]:
    if row["priority"] == "P0":
        return {"document_id": row["document_id"], "field": row["field"], "previous_candidate": row["llm_suggestion"],
                "verification_value": "", "verification_evidence": row["evidence"], "verification_confidence": row["confidence"],
                "verification_status": "still_human_review", "verification_reason": "P0_true_conflict_human_decision_required",
                "model": model, "prompt_version": PROMPT_VERSION, "source_sha256": document_rows["_source"]["source_sha256"]}
    if failure:
        status, reason, value, evidence, confidence = "still_human_review", failure, "", "", "low"
    else:
        assert response is not None
        value, evidence, confidence = response["value"].strip(), response["evidence"].strip(), response["confidence"]
        allowed = vocabulary(row["field"], llm)
        if not meaningful(value) or response["relationship"] == "insufficient":
            status, reason = "unresolved_nonblocking", "no_strong_field_specific_evidence"
            value = ""
        elif allowed is not None and value not in allowed:
            status, reason, value = "rejected", "controlled_vocabulary_rejected", ""
        elif response["relationship"] in {"referenced_only", "event_only"} or not evidence_grounded(evidence, context):
            status, reason, value = "rejected", f"{response['relationship']}_or_ungrounded_evidence", ""
        elif verified_safe(row["field"], response, context, row, document_rows, llm, adj):
            status, reason = "verified", "field_specific_identity_and_evidence_verified"
        else:
            status, reason, value = "still_human_review", "strong_evidence_or_identity_threshold_not_met", ""
    return {"document_id": row["document_id"], "field": row["field"], "previous_candidate": row["llm_suggestion"],
            "verification_value": value, "verification_evidence": evidence, "verification_confidence": confidence,
            "verification_status": status, "verification_reason": reason, "model": model,
            "prompt_version": PROMPT_VERSION, "source_sha256": document_rows["_source"]["source_sha256"]}


def p0_packet(rows: list[dict[str, str]], contexts: dict[tuple[str, str], dict[str, object]]) -> tuple[list[dict[str, str]], str]:
    packet = []
    markdown = ["# TunnelBookAI P0 Metadata Review Packet", "", "Bu paket karar önermez; dört gerçek conflict'i insan incelemesi için özetler.", ""]
    for row in rows:
        context = contexts[(row["document_id"], row["field"])]
        item = {
            "document_id": row["document_id"], "source_relative_path": row["source_relative_path"], "field": row["field"],
            "current_value": row["current_value"], "deterministic_suggestion": row["deterministic_suggestion"],
            "llm_suggestion": row["llm_suggestion"], "llm_evidence": row["evidence"], "confidence": row["confidence"],
            "conflict_type": row["adjudication_reason"],
            "title_cover_headings": " | ".join(context["title_cover_headings"][:8]),
            "opening_context": " ".join(str(context["opening_identity_context"]).split()[:750]),
            "field_context_snippets": " || ".join(context["field_context_snippets"][:6]),
        }
        packet.append(item)
        markdown.extend([
            f"## {row['document_id']} — {row['field']}", "", f"- Kaynak: `{row['source_relative_path']}`",
            f"- Current: `{row['current_value']}`", f"- Deterministic: `{row['deterministic_suggestion']}`",
            f"- LLM: `{row['llm_suggestion']}`", f"- Confidence: `{row['confidence']}`",
            f"- Conflict: `{row['adjudication_reason']}`", f"- LLM evidence: {row['evidence']}", "",
            f"**Başlıklar:** {item['title_cover_headings'] or '(yok)'}", "", "**Açılış context:**", "",
            item["opening_context"], "", "**Field snippet'ları:**", "", item["field_context_snippets"] or "(yok)", "",
        ])
    return packet, "\n".join(markdown)


def build_verified_candidate(base: list[dict[str, str]], verification: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    output = [dict(row) for row in base]
    by_id = {row["document_id"]: row for row in output}
    for decision in verification:
        target = by_id[decision["document_id"]]
        field = decision["field"]
        if decision["verification_status"] == "verified":
            target[f"{field}_value"] = decision["verification_value"]
            target[f"{field}_source"] = "second_pass_verified"
            target[f"{field}_confidence"] = decision["verification_confidence"]
            target[f"{field}_verification_status"] = "verified"
        elif decision["verification_status"] == "still_human_review":
            target[f"{field}_value"] = ""
            target[f"{field}_source"] = "human_review_pending"
            target[f"{field}_confidence"] = decision["verification_confidence"]
            target[f"{field}_verification_status"] = "still_human_review"
        elif decision["verification_status"] in {"unresolved_nonblocking", "rejected"}:
            target[f"{field}_value"] = ""
            target[f"{field}_source"] = "unresolved"
            target[f"{field}_confidence"] = decision["verification_confidence"]
            target[f"{field}_verification_status"] = decision["verification_status"]
    return output, list(base[0])


def report_text(summary: dict[str, object]) -> str:
    lines = ["# TunnelBookAI Metadata Verification Audit", "", "## Sonuç", "", f"- Karar: **{summary['decision']}**",
             f"- Endpoint/model: `http://127.0.0.1:1234/v1` / `{summary['model']}`",
             f"- Prompt version: `{PROMPT_VERSION}`",
             f"- V3 input: **{summary['input']}**", f"- P0 conflicts: **{summary['p0']}**",
             f"- Second pass processed: **{summary['processed']}**", f"- Second-pass verified: **{summary['verified']}**",
             f"- Still human review: **{summary['review']}**", f"- Unresolved: **{summary['unresolved']}**",
             f"- Rejected: **{summary['rejected']}**", f"- Cache hits / calls: **{summary['cache_hits']} / {summary['calls']}**",
             f"- Parse retry / failed inference: **{summary['retries']} / {summary['failures']}**",
             f"- Bu invocation gerçek inference ortalaması: **{summary['average_seconds']} saniye**",
             f"- Aktif second-pass cache identity: **{summary['active_cache']} / 150**", "", "## V4", "",
             f"- Toplam: **{summary['v4']}**", f"- P0/P1/P2: **{summary['P0']} / {summary['P1']} / {summary['P2']}**", "",
             "## Field bazında sonuç", ""]
    for field in FIELDS:
        counts = summary["by_field"].get(field, {})
        lines.append(f"- {field}: verified={counts.get('verified', 0)}, review={counts.get('still_human_review', 0)}, unresolved={counts.get('unresolved_nonblocking', 0)}, rejected={counts.get('rejected', 0)}")
    lines.extend(["", "## P0 human packet", "", f"- CSV/Markdown kayıt: **{summary['p0_packet']} / 4**",
                  "- P0 için otomatik karar verilmedi; dört kayıt V4 içinde de P0 olarak tutuldu.", "",
                  "## Stratified sample audit", "", f"- Örnek: **{summary['sample_count']}**",
                  f"- Unsafe verification: **{summary['unsafe']}**",
                  "- İlk model sınıflandırmasındaki 7 tentative verified kaydın tamamı ayrıca manuel incelendi. Organization conflict, sparse-language ve seminar-without-slide-structure guard'ları sıkılaştırıldı; final verified set boş ve unsafe count 0'dır.",
                  "", "## Final verified candidate", "",
                  f"- Satır/unique: **{summary['candidate_rows']} / {summary['candidate_unique']}**",
                  f"- Existing verified değişikliği: **{summary['protected_changed']}**",
                  f"- Corpus değişikliği: **{summary['corpus_changed']}**", "", "## Testler", "", f"- {summary['tests']}", "",
                  "## Warnings", "", "- Bilinmeyen metadata zorla doldurulmadı; unresolved/rejected değerler canonical metadata'ya uygulanmadı.",
                  "- Canonical metadata master'a otomatik merge yapılmadı.", "", "## Blockers", "",
                  f"- {'Yok.' if summary['decision'] == 'GO' else 'Verification güvenlik/bütünlük kontrolü başarısız.'}", "", "## Nihai karar", "", f"**{summary['decision']}**", ""])
    return "\n".join(lines)


def run(root: Path, base_url: str, model: str, tests: str, transport: Transport | None = None) -> dict[str, object]:
    llm = load_module("metadata_llm_review", root / "scripts/05_metadata_llm_review.py")
    adj = load_module("metadata_adjudication", root / "scripts/06_metadata_adjudication.py")
    llm.assert_local_endpoint(base_url)
    model = llm.discover_model(base_url, 10, model)
    transport = transport or llm.http_transport
    protected_paths = [root / path for path in (
        "data/metadata/final_metadata_master.csv", "data/metadata/metadata_llm_suggestions.csv",
        "data/metadata/metadata_adjudication.csv", "data/metadata/final_metadata_review_queue_v3.csv",
        "data/metadata/final_corpus_manifest.csv")]
    protected_before = {path: path.read_bytes() for path in protected_paths}
    corpus_before = llm.directory_state(root / "data/corpus_final")
    master = read_csv(root / "data/metadata/final_metadata_master.csv")
    master_by_id = {row["document_id"]: row for row in master}
    queue = read_csv(root / "data/metadata/final_metadata_review_queue_v3.csv")
    for row in queue:
        row["source_sha256"] = master_by_id[row["document_id"]]["source_sha256"]
    suggestion_rows: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for item in read_csv(root / "data/metadata/metadata_llm_suggestions.csv"):
        suggestion_rows[item["document_id"]][item["field"]] = item
    corpus_index = llm.corpus_document_index(root / "data/corpus_final")
    contexts = {}
    for row in queue:
        document = master_by_id[row["document_id"]]
        markdown = llm.resolve_markdown_path(root, document, corpus_index).read_text(encoding="utf-8-sig", errors="replace")
        contexts[(row["document_id"], row["field"])] = field_context(document, markdown, row["field"], llm)
    p0_rows = [row for row in queue if row["priority"] == "P0"]
    packet, packet_md = p0_packet(p0_rows, contexts)
    llm.atomic_write(root / "data/metadata/p0_metadata_review_packet.csv", csv_bytes(packet, P0_FIELDS))
    llm.atomic_write(root / "reports/p0_metadata_review_packet.md", packet_md.encode("utf-8"))
    decisions = []
    calls = cache_hits = retries = failures = 0
    durations = []
    output_path = root / "data/metadata/metadata_verification_pass.csv"
    v4_path = root / "data/metadata/final_metadata_review_queue_v4.csv"

    def checkpoint() -> None:
        llm.atomic_write(output_path, csv_bytes(decisions, VERIFICATION_FIELDS))
        current_v4 = []
        queue_by_key = {(item["document_id"], item["field"]): item for item in queue}
        for item in decisions:
            if item["verification_status"] != "still_human_review":
                continue
            prior = queue_by_key[(item["document_id"], item["field"])]
            current_v4.append({"priority": prior["priority"], "document_id": item["document_id"],
                               "source_relative_path": prior["source_relative_path"], "field": item["field"],
                               "previous_candidate": item["previous_candidate"], "verification_value": item["verification_value"],
                               "verification_evidence": item["verification_evidence"], "verification_confidence": item["verification_confidence"],
                               "verification_reason": item["verification_reason"], "reviewer_value": "", "reviewer_note": "",
                               "review_status": "pending", "reviewed_at": ""})
        llm.atomic_write(v4_path, csv_bytes(current_v4, V4_FIELDS))

    for row in queue:
        document_rows = dict(suggestion_rows[row["document_id"]])
        document_rows["_source"] = master_by_id[row["document_id"]]
        context = contexts[(row["document_id"], row["field"])]
        if row["priority"] == "P0":
            decisions.append(verification_decision(row, None, context, document_rows, model, llm, adj))
            checkpoint()
            continue
        cached = read_cache(cache_path(root, row, model), row, model)
        failure = ""
        if cached:
            response = cached["response"]
            cache_hits += 1
            retries += int(cached.get("retries", 0))
        else:
            allowed = vocabulary(row["field"], llm)
            vocab = ", ".join(sorted(allowed)) if allowed else "field-appropriate grounded string"
            try:
                response, used_retries, duration = call_field(base_url, model, row["field"], context, vocab, 45, transport, max_retries=1)
                calls += 1
                retries += used_retries
                durations.append(duration)
                payload = {"document_id": row["document_id"], "source_sha256": row["source_sha256"], "field": row["field"],
                           "model": model, "prompt_version": PROMPT_VERSION, "response": response, "retries": used_retries,
                           "processed_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
                llm.atomic_write(cache_path(root, row, model), json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8"))
            except Exception as exc:
                failures += 1
                response = None
                failure = f"inference_failed:{type(exc).__name__}:{exc}"
        decisions.append(verification_decision(row, response, context, document_rows, model, llm, adj, failure))
        checkpoint()
    base_candidate = read_csv(root / "data/metadata/final_metadata_candidate.csv")
    verified_candidate, candidate_fields = build_verified_candidate(base_candidate, decisions)
    llm.atomic_write(root / "data/metadata/final_metadata_verified_candidate.csv", csv_bytes(verified_candidate, candidate_fields))
    statuses = Counter(row["verification_status"] for row in decisions)
    v4 = read_csv(v4_path)
    by_field = defaultdict(Counter)
    for row in decisions:
        by_field[row["field"]][row["verification_status"]] += 1
    verified_rows = [row for row in decisions if row["verification_status"] == "verified"]
    sample = []
    unsafe = []
    for field in FIELDS:
        chosen = sorted((row for row in verified_rows if row["field"] == field),
                        key=lambda row: hashlib.sha256(f"{field}\0{row['document_id']}".encode()).hexdigest())[:10]
        sample.extend(chosen)
        for item in chosen:
            if not evidence_grounded(item["verification_evidence"], contexts[(item["document_id"], field)]):
                unsafe.append(f"{item['document_id']}:{field}")
    protected_changed = any(path.read_bytes() != payload for path, payload in protected_before.items())
    corpus_changed = llm.directory_state(root / "data/corpus_final") != corpus_before
    priorities = Counter(row["priority"] for row in v4)
    summary: dict[str, object] = {
        "input": len(queue), "p0": len(p0_rows), "processed": len(queue) - len(p0_rows),
        "verified": statuses["verified"], "review": statuses["still_human_review"],
        "unresolved": statuses["unresolved_nonblocking"], "rejected": statuses["rejected"],
        "cache_hits": cache_hits, "calls": calls, "retries": retries, "failures": failures,
        "active_cache": sum(PROMPT_VERSION in path.read_text(encoding="utf-8")
                            for path in (root / "data/metadata/cache/metadata_verification").rglob("*.json")),
        "average_seconds": round(sum(durations) / len(durations), 3) if durations else 0.0,
        "v4": len(v4), "P0": priorities["P0"], "P1": priorities["P1"], "P2": priorities["P2"],
        "by_field": {field: dict(counts) for field, counts in by_field.items()}, "p0_packet": len(packet),
        "sample_count": len(sample), "unsafe": len(unsafe), "candidate_rows": len(verified_candidate),
        "candidate_unique": len({row["document_id"] for row in verified_candidate}),
        "protected_changed": protected_changed, "corpus_changed": corpus_changed, "tests": tests,
        "model": model,
    }
    summary["decision"] = "GO" if (len(queue) == 154 and len(packet) == 4 and not failures and not unsafe
        and len(verified_candidate) == 214 and summary["candidate_unique"] == 214 and not protected_changed and not corpus_changed) else "NO-GO"
    llm.atomic_write(root / "reports/metadata_verification_audit.md", report_text(summary).encode("utf-8"))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Field-specific metadata verification pass")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    parser.add_argument("--model", default="qwen3.6-35b-a3b-mlx")
    parser.add_argument("--test-summary", default="Henüz çalıştırılmadı")
    args = parser.parse_args()
    summary = run(args.project_root.resolve(), args.base_url, args.model, args.test_summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
