from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


FIELDS = ("title", "organization", "year", "language", "document_type", "authority_level", "topics")
ADJUDICATION_FIELDS = [
    "document_id", "field", "current_value", "deterministic_suggestion", "llm_suggestion",
    "selected_candidate", "evidence", "confidence", "agreement_status", "adjudication_status",
    "adjudication_reason", "review_priority", "source_sha256",
]
QUEUE_FIELDS = [
    "priority", "document_id", "source_relative_path", "field", "current_value",
    "deterministic_suggestion", "llm_suggestion", "selected_candidate", "evidence", "confidence",
    "agreement_status", "adjudication_reason", "reviewer_value", "reviewer_note", "review_status", "reviewed_at",
]
IDENTITY_FIELDS = ["document_id", "source_relative_path", "source_filename", "source_extension", "source_sha256"]


def load_llm_module(root: Path):
    path = root / "scripts/05_metadata_llm_review.py"
    spec = importlib.util.spec_from_file_location("metadata_llm_review", path)
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


def normalize(text: object) -> str:
    import unicodedata
    value = unicodedata.normalize("NFKD", str(text or "").casefold())
    value = "".join(character for character in value if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def meaningful(value: object) -> bool:
    return normalize(value) not in {"", "unknown", "unclassified", "null", "none"}


def guard_clean(row: dict[str, str], package: dict[str, object], llm) -> bool:
    evidence = row["llm_evidence"].strip()
    return bool(evidence) and "[" not in evidence and llm.evidence_grounded(evidence, package)


def identity_zone(package: dict[str, object]) -> str:
    return " ".join(package.get("headings", [])) + " " + str(package.get("first_excerpt", ""))[:3500]


def looks_referenced(evidence: str) -> bool:
    text = normalize(evidence)
    return bool(re.search(
        r"according to|as cited|references?|bibliograph|report .* (states?|contains?|notes?|says?)|"
        r"manual .* (states?|contains?)|article .* (states?|contains?)",
        text,
    ))


TYPE_PATTERNS = {
    "academic_article": r"journal|volume|issue|doi|academic article|research article|abstract",
    "thesis": r"thesis|dissertation|yuksek lisans tezi|doktora tezi|doctoral thesis|master s thesis",
    "conference_paper": r"proceedings|conference|symposium|presented at|kongre|sempozyum",
    "conference_proceedings": r"proceedings|conference|symposium|kongre|sempozyum",
    "manual": r"manual|el kitabi|kilavuz|guidebook",
    "handbook": r"handbook|el kitabi",
    "regulation": r"yonetmelik|regulation|resmi gazete",
    "technical_specification": r"technical specification|teknik sartname",
    "presentation": r"presentation|seminar|sunum|seminer|workshop",
    "training_material": r"training|course|seminar|presentation|egitim|kurs|seminer|sunum",
    "web_article": r"website|web page|blog|copyright .* website|wikipedia",
}


def strong_document_type(row: dict[str, str], package: dict[str, object]) -> bool:
    value = row["llm_suggestion"]
    pattern = TYPE_PATTERNS.get(value)
    if not pattern or looks_referenced(row["llm_evidence"]):
        return False
    evidence = normalize(row["llm_evidence"])
    zone = normalize(identity_zone(package))
    if value == "academic_article":
        strong_identity = r"journal|dergi|volume|issue|doi|academic article|research article"
        return bool(re.search(strong_identity, evidence) and re.search(strong_identity, zone))
    return bool(re.search(pattern, evidence) and re.search(pattern, zone))


def strong_year(row: dict[str, str], package: dict[str, object], document_rows: dict[str, dict[str, str]]) -> bool:
    year = row["llm_suggestion"]
    evidence = normalize(row["llm_evidence"])
    if not re.fullmatch(r"(?:18|19|20)\d{2}", year) or year not in evidence:
        return False
    direct = re.search(
        rf"published\s+(?:in\s+)?{year}|publication date\D{{0,30}}{year}|copyright\D{{0,10}}{year}|"
        rf"report date\D{{0,30}}{year}|resmi gazete.*{year}|(?:volume|vol|issue).{{0,80}}{year}|"
        rf"{year}.{{0,80}}(?:volume|vol|issue)",
        evidence,
    )
    if direct:
        return True
    doc_type = document_rows.get("document_type", {}).get("llm_suggestion", "")
    if doc_type == "thesis" and re.search(rf"(?:submitted|submission|accepted|approved|thesis|dissertation).{{0,50}}{year}|{year}.{{0,50}}(?:thesis|dissertation)", evidence):
        return True
    if doc_type in {"conference_paper", "conference_proceedings"} and re.search(rf"(?:conference|proceedings|symposium).{{0,80}}{year}|{year}.{{0,80}}(?:conference|proceedings|symposium)", evidence):
        return True
    return False


def strong_title(row: dict[str, str], package: dict[str, object]) -> bool:
    value = normalize(row["llm_suggestion"])
    evidence = normalize(row["llm_evidence"])
    headings = [normalize(item) for item in package.get("headings", [])]
    if not value or value not in evidence or re.match(r"^(chapter|section|part|bolum)\b", value):
        return False
    return any(value == heading or (len(value) >= 20 and value in heading) for heading in headings[:5])


def strong_organization(row: dict[str, str], package: dict[str, object]) -> bool:
    value = normalize(row["llm_suggestion"])
    evidence = normalize(row["llm_evidence"])
    zone = normalize(identity_zone(package))
    if not value or value not in evidence or value not in zone or looks_referenced(row["llm_evidence"]):
        return False
    ownership = r"published by|prepared by|issued by|authoring|publisher|ministry|general directorate|universit|department|survey team|official"
    return bool(re.search(ownership, evidence) or re.search(rf"(?:{ownership}).{{0,100}}{re.escape(value)}|{re.escape(value)}.{{0,100}}(?:{ownership})", zone))


def detected_language(package: dict[str, object]) -> str:
    raw = str(package.get("first_excerpt", ""))[:12000].casefold()
    text = f" {normalize(raw)} "
    scores = {
        "tr": 3 * sum(raw.count(ch) for ch in "çğıöşü") + sum(text.count(f" {word} ") for word in ("ve", "bir", "icin", "ile", "olarak", "tunel", "bu")),
        "en": sum(text.count(f" {word} ") for word in ("the", "and", "of", "to", "in", "for", "with", "tunnel")),
        "de": sum(text.count(f" {word} ") for word in ("der", "die", "das", "und", "von", "mit", "fur", "tunnel")),
    }
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return ordered[0][0] if ordered[0][1] >= 5 and ordered[0][1] >= 2 * max(1, ordered[1][1]) else "mixed"


def strong_language(row: dict[str, str], package: dict[str, object]) -> bool:
    value = row["llm_suggestion"]
    detected = detected_language(package)
    return value in {"tr", "en", "de"} and value == detected or value == "mixed" and detected == "mixed"


AUTHORITY_PATTERNS = {
    "A": r"karayollari genel mudurlugu|(?:^| )kgm(?: |$)|resmi gazete|federal highway administration|(?:^| )fhwa(?: |$)|world road association|(?:^| )piarc(?: |$)|teknik sartname|technical specification",
    "B": r"journal|academic|university|universit|thesis|dissertation|conference paper|proceedings|peer reviewed|elsevier|doi",
    "C": r"professional|industry|training|course|seminar|presentation|workshop|egitim|kurs|seminer|sunum",
    "D": r"wikipedia|website|web article|blog|secondary source|general web",
}


def strong_authority(row: dict[str, str], package: dict[str, object], document_rows: dict[str, dict[str, str]]) -> bool:
    value = row["llm_suggestion"]
    pattern = AUTHORITY_PATTERNS.get(value)
    if not pattern or looks_referenced(row["llm_evidence"]):
        return False
    evidence = normalize(row["llm_evidence"])
    zone = normalize(identity_zone(package))
    if not re.search(pattern, evidence) or not re.search(pattern, zone):
        return False
    doc_type = document_rows.get("document_type", {}).get("llm_suggestion", "")
    if value == "A":
        institution = re.search(r"karayollari genel mudurlugu|(?:^| )kgm(?: |$)|resmi gazete|federal highway administration|(?:^| )fhwa(?: |$)|world road association|(?:^| )piarc(?: |$)", evidence)
        ownership = re.search(r"official|published by|issued by|general directorate|baskanligi|ministry|department|manual|technical specification|teknik sartname", evidence)
        return bool(institution and ownership)
    if value == "B":
        doc_type_row = document_rows.get("document_type")
        corroborated_type = bool(doc_type_row and strong_document_type(doc_type_row, package))
        direct_class = re.search(r"journal article|academic paper|thesis|dissertation|conference paper|peer reviewed|doi", evidence)
        return bool(corroborated_type or direct_class)
    if value == "C":
        return doc_type in {"presentation", "training_material"} or bool(re.search(AUTHORITY_PATTERNS["C"], evidence))
    return doc_type == "web_article" or bool(re.search(AUTHORITY_PATTERNS["D"], evidence))


def field_auto_safe(row: dict[str, str], package: dict[str, object], document_rows: dict[str, dict[str, str]], llm) -> bool:
    if row["llm_confidence"] != "high" or not meaningful(row["llm_suggestion"]) or not guard_clean(row, package, llm):
        return False
    if row["agreement_status"] == "deterministic_llm_agree" and meaningful(row["deterministic_suggestion"]):
        return True
    if row["agreement_status"] != "llm_only":
        return False
    field = row["field"]
    if field == "language":
        return strong_language(row, package)
    if field == "document_type":
        return strong_document_type(row, package)
    if field == "year":
        return strong_year(row, package, document_rows)
    if field == "title":
        return strong_title(row, package)
    if field == "organization":
        return strong_organization(row, package)
    if field == "authority_level":
        return strong_authority(row, package, document_rows)
    return False


def human_priority(row: dict[str, str], clean: bool) -> str:
    if row["agreement_status"] == "deterministic_llm_conflict" and row["llm_confidence"] == "high" and clean and meaningful(row["deterministic_suggestion"]):
        return "P0"
    return "P2" if row["field"] in {"language", "topics"} else "P1"


def adjudicate_row(row: dict[str, str], package: dict[str, object], document_rows: dict[str, dict[str, str]], llm) -> dict[str, str]:
    current = row["current_value"]
    suggestion = row["llm_suggestion"]
    clean = guard_clean(row, package, llm)
    if meaningful(current):
        status, selected, reason, priority = "verified_existing", current, "current_verified_value_preserved", "NONBLOCKING"
    elif not meaningful(suggestion):
        status, selected, reason, priority = "unresolved_nonblocking", "", "no_grounded_value_found", "NONBLOCKING"
    elif not clean or row["llm_confidence"] == "low":
        status, selected, reason, priority = "rejected_suggestion", "", "evidence_or_validation_guard_failed", "NONBLOCKING"
    elif field_auto_safe(row, package, document_rows, llm):
        source = "deterministic_llm_agreement" if row["agreement_status"] == "deterministic_llm_agree" else "llm_grounded_auto_safe"
        status, selected, reason, priority = "auto_safe_candidate", suggestion, source, "NONBLOCKING"
    else:
        priority = human_priority(row, clean)
        status, selected = "human_review_required", ""
        reason = "strong_deterministic_llm_conflict" if priority == "P0" else f"field_specific_{row['field']}_identity_or_publication_check_required"
    return {
        "document_id": row["document_id"], "field": row["field"], "current_value": current,
        "deterministic_suggestion": row["deterministic_suggestion"], "llm_suggestion": suggestion,
        "selected_candidate": selected, "evidence": row["llm_evidence"], "confidence": row["llm_confidence"],
        "agreement_status": row["agreement_status"], "adjudication_status": status,
        "adjudication_reason": reason, "review_priority": priority, "source_sha256": row["source_sha256"],
    }


def build_candidate_master(master: list[dict[str, str]], adjudication: list[dict[str, str]], llm) -> tuple[list[dict[str, str]], list[str]]:
    by_key = {(row["document_id"], row["field"]): row for row in adjudication}
    columns = list(IDENTITY_FIELDS)
    for field in FIELDS:
        columns.extend([f"{field}_value", f"{field}_source", f"{field}_confidence", f"{field}_verification_status"])
    output = []
    for document in master:
        candidate = {key: document[key] for key in IDENTITY_FIELDS}
        for field in FIELDS:
            current = llm.current_value(document, field)
            deterministic = llm.deterministic_value(document, field)
            confidence_column = llm.CONFIDENCE_COLUMN[field]
            deterministic_confidence = document.get(confidence_column, "") if confidence_column else ""
            decision = by_key.get((document["document_id"], field))
            if meaningful(current):
                value, source, confidence, status = current, "existing_verified", "high", "verified_existing"
            elif decision and decision["adjudication_status"] == "auto_safe_candidate":
                value = decision["selected_candidate"]
                source = decision["adjudication_reason"]
                confidence = decision["confidence"]
                status = "auto_safe_candidate"
            elif decision and decision["adjudication_status"] == "human_review_required":
                value, source, confidence, status = "", "human_review_pending", decision["confidence"], "human_review_required"
            elif decision:
                value, source, confidence, status = "", "unresolved", decision["confidence"], decision["adjudication_status"]
            elif meaningful(deterministic):
                value, source, confidence, status = deterministic, "deterministic_existing", deterministic_confidence, "deterministic_candidate"
            else:
                value, source, confidence, status = "", "unresolved", deterministic_confidence, "unresolved_nonblocking"
            candidate[f"{field}_value"] = value
            candidate[f"{field}_source"] = source
            candidate[f"{field}_confidence"] = confidence
            candidate[f"{field}_verification_status"] = status
        output.append(candidate)
    return output, columns


def queue_rows(adjudication: list[dict[str, str]], master_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    output = []
    for row in adjudication:
        if row["adjudication_status"] != "human_review_required":
            continue
        output.append({
            "priority": row["review_priority"], "document_id": row["document_id"],
            "source_relative_path": master_by_id[row["document_id"]]["source_relative_path"], "field": row["field"],
            "current_value": row["current_value"], "deterministic_suggestion": row["deterministic_suggestion"],
            "llm_suggestion": row["llm_suggestion"], "selected_candidate": row["selected_candidate"],
            "evidence": row["evidence"], "confidence": row["confidence"], "agreement_status": row["agreement_status"],
            "adjudication_reason": row["adjudication_reason"], "reviewer_value": "", "reviewer_note": "",
            "review_status": "pending", "reviewed_at": "",
        })
    order = {"P0": 0, "P1": 1, "P2": 2}
    return sorted(output, key=lambda row: (order[row["priority"]], row["document_id"], FIELDS.index(row["field"])))


def sample_audit(adjudication: list[dict[str, str]], packages: dict[str, dict[str, object]], rows_by_document: dict[str, dict[str, dict[str, str]]], llm) -> dict[str, object]:
    samples: dict[str, list[str]] = {}
    failures = []
    for field in FIELDS:
        candidates = sorted(
            (row for row in adjudication if row["field"] == field and row["adjudication_status"] == "auto_safe_candidate"),
            key=lambda row: hashlib.sha256(f"{field}\0{row['document_id']}".encode()).hexdigest(),
        )[:10]
        samples[field] = [row["document_id"] for row in candidates]
        for decision in candidates:
            source = rows_by_document[decision["document_id"]][field]
            if not field_auto_safe(source, packages[decision["document_id"]], rows_by_document[decision["document_id"]], llm):
                failures.append(f"{decision['document_id']}:{field}")
    return {"samples": samples, "sample_count": sum(map(len, samples.values())), "failures": failures}


def report_text(summary: dict[str, object]) -> str:
    status = summary["status_counts"]
    priorities = summary["priorities"]
    lines = [
        "# TunnelBookAI Metadata Adjudication Audit", "", "## Sonuç", "", f"- Karar: **{summary['decision']}**",
        f"- Giriş suggestion row: **{summary['input_rows']}**", f"- Eski queue V2: **{summary['v2_rows']}**",
        f"- verified_existing: **{status.get('verified_existing', 0)}**",
        f"- auto_safe_candidate: **{status.get('auto_safe_candidate', 0)}**",
        f"- human_review_required: **{status.get('human_review_required', 0)}**",
        f"- unresolved_nonblocking: **{status.get('unresolved_nonblocking', 0)}**",
        f"- rejected_suggestion: **{status.get('rejected_suggestion', 0)}**", "", "## Review Queue V3", "",
        f"- Toplam: **{summary['v3_rows']}**", f"- P0: **{priorities.get('P0', 0)}**",
        f"- P1: **{priorities.get('P1', 0)}**", f"- P2: **{priorities.get('P2', 0)}**", "",
        f"- V2 → V3 azalma: **{summary['queue_reduction']} satır (%{summary['queue_reduction_percent']})**", "",
        "### Field bazında review", "",
    ]
    lines.extend(f"- {field}: **{summary['review_by_field'].get(field, 0)}**" for field in FIELDS)
    lines.extend(["", "### Field bazında auto-safe", ""])
    lines.extend(f"- {field}: **{summary['auto_by_field'].get(field, 0)}**" for field in FIELDS)
    lines.extend([
        "", "## Stratified sample quality audit", "", f"- Örnek sayısı: **{summary['sample_count']}**",
        f"- Unsafe auto-safe örnek: **{len(summary['sample_failures'])}**",
        f"- Sonuç: **{'PASS' if not summary['sample_failures'] else 'FAIL'}**",
        "- İlk kalite incelemesinde abstract-only DOC000309 type adayı ve yalnız affiliation'a dayanan Authority B adayları yakalandı; kurallar sıkılaştırılıp çıktılar yeniden üretildi.",
    ])
    for field in FIELDS:
        ids = summary["sample_ids"].get(field, [])
        lines.append(f"- {field}: {', '.join(ids) if ids else '(auto-safe yok)'}")
    lines.extend([
        "", "## Candidate master ve bütünlük", "", f"- Candidate master: **{summary['candidate_rows']}/214**",
        f"- Unique document_id: **{summary['candidate_unique']}**",
        f"- Korunan existing_verified alan değeri: **{summary['candidate_existing_verified']}**",
        f"- Current/verified değişikliği: **{summary['current_changed']}**",
        f"- Corpus değişikliği: **{summary['corpus_changed']}**", "", "## Testler", "",
        f"- {summary['tests']}", "", "## Warnings", "",
        "- `unresolved_nonblocking` kayıtlar bilinçli olarak V3 queue dışında tutuldu.",
        "- Auto-safe değerler yalnız candidate master'a yazıldı; canonical metadata master'a uygulanmadı.", "", "## Blockers", "",
        f"- {'Yok.' if summary['decision'] == 'GO' else 'Adjudication güvenlik veya bütünlük kontrolü başarısız.'}", "", "## Nihai karar", "",
        f"**{summary['decision']}**", "",
    ])
    return "\n".join(lines)


def run(root: Path, tests: str = "Henüz çalıştırılmadı") -> dict[str, object]:
    llm = load_llm_module(root)
    master_path = root / "data/metadata/final_metadata_master.csv"
    suggestions_path = root / "data/metadata/metadata_llm_suggestions.csv"
    v2_path = root / "data/metadata/final_metadata_review_queue_v2.csv"
    protected_before = {path: path.read_bytes() for path in (master_path, suggestions_path, v2_path)}
    corpus_before = llm.directory_state(root / "data/corpus_final")
    master = read_csv(master_path)
    suggestions = read_csv(suggestions_path)
    master_by_id = {row["document_id"]: row for row in master}
    rows_by_document: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in suggestions:
        rows_by_document[row["document_id"]][row["field"]] = row
    corpus_index = llm.corpus_document_index(root / "data/corpus_final")
    packages = {}
    for document_id in sorted(rows_by_document):
        document = master_by_id[document_id]
        markdown = llm.resolve_markdown_path(root, document, corpus_index).read_text(encoding="utf-8-sig", errors="replace")
        packages[document_id] = llm.context_package(document, markdown)
    adjudication = []
    for row in suggestions:
        adjudication.append(adjudicate_row(row, packages[row["document_id"]], rows_by_document[row["document_id"]], llm))
    adjudication.sort(key=lambda row: (row["document_id"], FIELDS.index(row["field"])))
    audit = sample_audit(adjudication, packages, rows_by_document, llm)
    if audit["failures"]:
        failed = set(audit["failures"])
        for row in adjudication:
            if f"{row['document_id']}:{row['field']}" in failed:
                row.update(adjudication_status="human_review_required", selected_candidate="",
                           adjudication_reason="sample_audit_failed", review_priority=human_priority(row, True))
        audit = sample_audit(adjudication, packages, rows_by_document, llm)
    queue = queue_rows(adjudication, master_by_id)
    candidates, candidate_fields = build_candidate_master(master, adjudication, llm)
    llm.atomic_write(root / "data/metadata/metadata_adjudication.csv", csv_bytes(adjudication, ADJUDICATION_FIELDS))
    llm.atomic_write(root / "data/metadata/final_metadata_review_queue_v3.csv", csv_bytes(queue, QUEUE_FIELDS))
    llm.atomic_write(root / "data/metadata/final_metadata_candidate.csv", csv_bytes(candidates, candidate_fields))
    status_counts = Counter(row["adjudication_status"] for row in adjudication)
    candidate_source_counts = Counter(
        value for row in candidates for key, value in row.items() if key.endswith("_source")
    )
    summary: dict[str, object] = {
        "input_rows": len(suggestions), "v2_rows": len(read_csv(v2_path)), "status_counts": dict(status_counts),
        "v3_rows": len(queue), "priorities": dict(Counter(row["priority"] for row in queue)),
        "review_by_field": dict(Counter(row["field"] for row in queue)),
        "auto_by_field": dict(Counter(row["field"] for row in adjudication if row["adjudication_status"] == "auto_safe_candidate")),
        "sample_count": audit["sample_count"], "sample_failures": audit["failures"], "sample_ids": audit["samples"],
        "candidate_rows": len(candidates), "candidate_unique": len({row["document_id"] for row in candidates}),
        "candidate_existing_verified": candidate_source_counts["existing_verified"],
        "queue_reduction": len(read_csv(v2_path)) - len(queue),
        "queue_reduction_percent": round(100 * (len(read_csv(v2_path)) - len(queue)) / len(read_csv(v2_path)), 1),
        "current_changed": any(path.read_bytes() != payload for path, payload in protected_before.items()),
        "corpus_changed": llm.directory_state(root / "data/corpus_final") != corpus_before, "tests": tests,
    }
    summary["decision"] = "GO" if (
        len(suggestions) == 511 and len(candidates) == 214 and summary["candidate_unique"] == 214
        and not summary["current_changed"] and not summary["corpus_changed"] and not audit["failures"]
        and all(row["review_priority"] != "P0" for row in adjudication if row["adjudication_status"] == "unresolved_nonblocking")
    ) else "NO-GO"
    llm.atomic_write(root / "reports/metadata_adjudication_audit.md", report_text(summary).encode("utf-8"))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggestion-only metadata adjudication and V3 queue reduction")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--test-summary", default="Henüz çalıştırılmadı")
    args = parser.parse_args()
    summary = run(args.project_root.resolve(), args.test_summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
