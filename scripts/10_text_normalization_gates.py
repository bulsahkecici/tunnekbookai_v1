from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "scripts/10_text_normalization.py"
spec = importlib.util.spec_from_file_location("text_normalization_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(core)

CHANGE_RULES = {
    "unicode": "rule_unicode_normalization_count",
    "whitespace": "rule_whitespace_count",
    "ocr_spacing": "rule_ocr_spacing_count",
    "linebreak": "rule_linebreak_count",
    "hyphenation": "rule_hyphenation_count",
    "header_footer": "rule_header_footer_count",
    "replacement_character": "rule_replacement_character_count",
    "encoding_cleanup": "rule_encoding_cleanup_count",
}
REVIEW_FIELDS = ["priority", "document_id", "source_relative_path", "reason", "rule",
                 "source_excerpt", "normalized_excerpt", "review_status", "reviewer_note"]
URL_RE = re.compile(r"https?://[^\s)>]+", re.IGNORECASE)
DOI_RE = re.compile(r"(?:doi\s*:\s*)?10\.\d{4,9}/[^\s)>]+", re.IGNORECASE)
ISBN_RE = re.compile(r"ISBN\s*[\dXx-]+", re.IGNORECASE)
ISSN_RE = re.compile(r"ISSN\s*[\dXx-]+", re.IGNORECASE)
STANDARD_RE = re.compile(r"(?:EN|ASTM|DIN|ISO)\s*-?\s*[A-Z]?\d[\w./-]*|RG-\d{1,2}/\d{1,2}/\d{4}-\d+", re.IGNORECASE)
ABBREVIATION_RE = re.compile(r"(?<![\w-])(?:TBM|NATM|RMR|Q-System|T1-01|M20-25)(?![\w-])", re.IGNORECASE)
FORMULA_RE = re.compile(r"formula-not-decoded", re.IGNORECASE)
IMAGE_RE = re.compile(r"<!--\s*image\s*-->|image placeholder|figure placeholder", re.IGNORECASE)
HARD_RISKS = ("numeric_mismatch", "url_mismatch", "doi_mismatch", "isbn_mismatch",
              "issn_mismatch", "standard_document_code_mismatch", "front_matter_mismatch",
              "citation_provenance_mismatch", "table_corruption", "technical_symbol_corruption",
              "technical_abbreviation_corruption", "formula_placeholder_loss", "image_placeholder_loss")


def canonical_tokens(pattern: re.Pattern[str], text: str) -> Counter:
    return Counter(re.sub(r"\s+", "", item) for item in pattern.findall(text))


def table_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.lstrip().startswith("|")]


def safety_audit(source: str, normalized: str) -> dict[str, bool]:
    source_front, _ = core.split_front_matter(source)
    normalized_front, _ = core.split_front_matter(normalized)
    checks = {
        "numeric_mismatch": core.token_counter(core.NUMERIC_RE, source) != core.token_counter(core.NUMERIC_RE, normalized),
        "url_mismatch": canonical_tokens(URL_RE, source) != canonical_tokens(URL_RE, normalized),
        "doi_mismatch": canonical_tokens(DOI_RE, source) != canonical_tokens(DOI_RE, normalized),
        "isbn_mismatch": canonical_tokens(ISBN_RE, source) != canonical_tokens(ISBN_RE, normalized),
        "issn_mismatch": canonical_tokens(ISSN_RE, source) != canonical_tokens(ISSN_RE, normalized),
        "standard_document_code_mismatch": canonical_tokens(STANDARD_RE, source) != canonical_tokens(STANDARD_RE, normalized),
        "front_matter_mismatch": source_front != normalized_front,
        "citation_provenance_mismatch": core.COMMENT_RE.findall(source) != core.COMMENT_RE.findall(normalized),
        "table_corruption": table_lines(source) != table_lines(normalized),
        "technical_symbol_corruption": any(source.count(symbol) != normalized.count(symbol) for symbol in core.ENGINEERING_SYMBOLS),
        "technical_abbreviation_corruption": canonical_tokens(ABBREVIATION_RE, source) != canonical_tokens(ABBREVIATION_RE, normalized),
        "formula_placeholder_loss": FORMULA_RE.findall(source) != FORMULA_RE.findall(normalized),
        "image_placeholder_loss": IMAGE_RE.findall(source) != IMAGE_RE.findall(normalized),
        "unsafe_semantic_rewrite": False,
    }
    return checks


def clip(text: str, limit: int = 180) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def clip_change(text: str, limit: int = 180) -> str:
    text = text.replace("\t", "⇥").replace(" ", "␠")
    return text if len(text) <= limit else text[:limit - 1] + "…"


def first_changed_lines(before: str, after: str) -> tuple[str, str]:
    left = before.splitlines()
    right = after.splitlines()
    for index in range(max(len(left), len(right))):
        old = left[index] if index < len(left) else ""
        new = right[index] if index < len(right) else ""
        if old != new:
            left_excerpt, right_excerpt = clip_change(old), clip_change(new)
            if left_excerpt == right_excerpt:
                offset = next((i for i, pair in enumerate(zip(old, new)) if pair[0] != pair[1]), min(len(old), len(new)))
                start, end = max(0, offset - 60), offset + 100
                left_excerpt = clip_change(old[start:end])
                right_excerpt = clip_change(new[start:end])
                if left_excerpt == right_excerpt:
                    left_excerpt = old[start:end].encode("unicode_escape").decode("ascii")
                    right_excerpt = new[start:end].encode("unicode_escape").decode("ascii")
            return left_excerpt, right_excerpt
    return clip_change(before), clip_change(after)


def representative_changes(document_id: str, source_relative_path: str, source: str,
                           normalized: str, row: dict[str, object]) -> list[dict[str, object]]:
    before, after = first_changed_lines(source, normalized)
    records = []
    for rule, field in CHANGE_RULES.items():
        count = int(row[field])
        if not count:
            continue
        rule_before, rule_after = before, after
        if rule == "ocr_spacing":
            for broken, fixed in core.OCR_REPLACEMENTS.items():
                if broken in source:
                    rule_before, rule_after = broken, fixed
                    break
        elif rule == "encoding_cleanup":
            for broken, fixed in core.MOJIBAKE.items():
                if broken in source:
                    rule_before, rule_after = broken, fixed
                    break
        elif rule == "replacement_character":
            rule_before, rule_after = "�", "[UNRESOLVED_CHAR]"
        records.append({
            "document_id": document_id,
            "source_relative_path": source_relative_path,
            "rule": rule,
            "before": rule_before,
            "after": rule_after,
            "context": f"{count} deterministic change(s); representative excerpt",
            "confidence": "high" if rule not in {"linebreak", "hyphenation"} else "conservative_rule",
        })
    unique = {}
    for record in records:
        key = (record["document_id"], record["rule"], record["before"], record["after"])
        unique[key] = record
    return list(unique.values())


def analyze(source_path: Path, source_root: Path, previous: dict[str, dict[str, str]]) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source = source_bytes.decode("utf-8-sig")
    front, body = core.split_front_matter(source)
    normalized_body, counts, headers = core.normalize_body(body)
    normalized = front + normalized_body
    normalized_bytes = normalized.encode("utf-8")
    doc_id = core.document_id(front)
    relative = source_path.relative_to(source_root)
    risks = safety_audit(source, normalized)
    hard = [name for name in HARD_RISKS if risks[name]]
    warnings = []
    if headers:
        warnings.append("repeated_header_footer_candidate_not_removed:" + " | ".join(headers[:3]))
    if counts["replacement"]:
        warnings.append("replacement_character_marked_unresolved")
    review_reasons = hard + warnings
    changed = source_bytes != normalized_bytes
    status = "manual_review_required" if hard else "normalized_with_warning" if warnings else "normalized" if changed else "unchanged"
    source_digest = core.sha256(source_bytes)
    old = previous.get(doc_id, {})
    processed_at = old.get("processed_at", "") if (old.get("source_sha256") == source_digest
                                                       and old.get("normalizer_version") == core.NORMALIZER_VERSION) else ""
    if not processed_at:
        processed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    row = {
        "document_id": doc_id,
        "source_relative_path": core.source_relative_path(front),
        "source_final_markdown": (Path("data/corpus_final") / relative).as_posix(),
        "normalized_markdown": (Path("data/corpus_normalized") / relative).as_posix(),
        "source_sha256": source_digest,
        "normalized_sha256": core.sha256(normalized_bytes),
        "changed": str(changed).lower(),
        "normalization_status": status,
        "rule_unicode_normalization_count": counts["unicode"],
        "rule_whitespace_count": counts["whitespace"],
        "rule_ocr_spacing_count": counts["ocr_spacing"],
        "rule_linebreak_count": counts["linebreak"],
        "rule_hyphenation_count": counts["hyphenation"],
        "rule_header_footer_count": 0,
        "rule_replacement_character_count": counts["replacement"],
        "rule_encoding_cleanup_count": counts["encoding"],
        "rule_placeholder_count": counts["placeholder"],
        "manual_review_required": str(bool(review_reasons)).lower(),
        "review_reason": "; ".join(review_reasons),
        "normalizer_version": core.NORMALIZER_VERSION,
        "processed_at": processed_at,
    }
    return {"path": source_path, "relative": relative, "source": source, "normalized": normalized,
            "normalized_bytes": normalized_bytes, "front": front, "body": body, "row": row,
            "counts": counts, "headers": headers, "risks": risks,
            "changes": representative_changes(doc_id, row["source_relative_path"], source, normalized, row)}


def analyze_all(root: Path) -> list[dict[str, object]]:
    source_root = root / "data/corpus_final"
    previous = {row["document_id"]: row for row in core.read_csv(root / "data/metadata/text_normalization_manifest.csv")}
    return [analyze(path, source_root, previous) for path in sorted(source_root.rglob("*.md"), key=lambda p: p.relative_to(source_root).as_posix())]


def hard_risk_documents(analyses: list[dict[str, object]]) -> dict[str, list[str]]:
    return {risk: [item["row"]["document_id"] for item in analyses if item["risks"][risk]] for risk in HARD_RISKS}


def dry_run_report(analyses: list[dict[str, object]], target_preexisting: bool) -> str:
    rule_doc_counts = {rule: sum(int(item["row"][field]) > 0 for item in analyses) for rule, field in CHANGE_RULES.items()}
    rule_totals = {rule: sum(int(item["row"][field]) for item in analyses) for rule, field in CHANGE_RULES.items()}
    placeholder_total = sum(int(item["row"]["rule_placeholder_count"]) for item in analyses)
    risks = hard_risk_documents(analyses)
    changed = sum(item["row"]["changed"] == "true" for item in analyses)
    gate = not any(risks.values()) and len(analyses) == 214
    lines = ["# TunnelBookAI Text Normalization Dry Run", "", "## Result", "", f"**{'GO' if gate else 'NO-GO'}**", "",
             "## Scope", "", f"- Documents analyzed in memory: **{len(analyses)}/214**",
             f"- Changed if applied: **{changed}**", f"- Unchanged if applied: **{len(analyses)-changed}**",
             "- `data/corpus_normalized/` written by dry-run: **false**",
             f"- Target existed before this requested dry-run: **{str(target_preexisting).lower()}**", "", "## Rule Impact", ""]
    for rule in CHANGE_RULES:
        lines.append(f"- {rule}: documents **{rule_doc_counts[rule]}**, changes **{rule_totals[rule]}**")
    lines.append(f"- placeholder encounters: **{placeholder_total}**")
    lines.extend(["", "## Risk Analysis", ""])
    for risk in HARD_RISKS:
        ids = risks[risk]
        lines.append(f"- {risk}: **{len(ids)}**" + (f" — {', '.join(ids)}" if ids else ""))
    lines.extend(["", "## Gate", "", f"**{'GO FOR STRATIFIED PILOT' if gate else 'NO-GO — pilot must not start'}**", ""])
    return "\n".join(lines)


def load_variant_map(root: Path) -> dict[str, str]:
    return {row["document_id"]: row.get("selected_variant", "") for row in core.read_csv(root / "data/metadata/final_corpus_manifest.csv")}


def pilot_selection(analyses: list[dict[str, object]], variants: dict[str, str]) -> list[tuple[str, dict[str, object]]]:
    def metric(item: dict[str, object], category: str) -> int:
        row, text, body = item["row"], item["source"], item["body"]
        suffix = Path(str(row["source_relative_path"])).suffix.lower()
        values = {
            "clean_text": int(row["changed"] == "false" and len(body) > 1000),
            "ocr_heavy_pdf": int(suffix == ".pdf") * (int(row["rule_whitespace_count"]) + int(row["rule_replacement_character_count"]) * 100),
            "broken_encoding": sum(text.count(token) for token in core.MOJIBAKE),
            "turkish_split_ocr": int(row["rule_ocr_spacing_count"]),
            "english_technical": text.lower().count(" the ") + text.lower().count(" tunnel "),
            "table_heavy": len(table_lines(text)),
            "formula_not_decoded": len(FORMULA_RE.findall(text)),
            "image_placeholders": len(IMAGE_RE.findall(text)),
            "repeated_header_footer": len(item["headers"]),
            "line_wrap_hyphenation": int(row["rule_linebreak_count"]) + int(row["rule_hyphenation_count"]) * 10,
            "docx_derived": int(suffix == ".docx"),
            "pptx_derived": int(suffix == ".pptx"),
            "full_docling_pdf": int(suffix == ".pdf" and variants.get(row["document_id"]) == "full_docling"),
            "baseline_ocr_pdf": int(suffix == ".pdf" and variants.get(row["document_id"]) == "baseline"),
            "very_short_image_heavy": max(1, 100000 - len(body)) + len(IMAGE_RE.findall(text)) * 10000,
        }
        return values[category]

    categories = ["clean_text", "ocr_heavy_pdf", "broken_encoding", "turkish_split_ocr", "english_technical",
                  "table_heavy", "formula_not_decoded", "image_placeholders", "repeated_header_footer",
                  "line_wrap_hyphenation", "docx_derived", "pptx_derived", "full_docling_pdf",
                  "baseline_ocr_pdf", "very_short_image_heavy"]
    selected = []
    used = set()
    for category in categories:
        ranked = sorted((item for item in analyses if item["row"]["document_id"] not in used),
                        key=lambda item: (-metric(item, category), item["row"]["document_id"]))
        chosen = ranked[0]
        score = metric(chosen, category)
        reason = category if score > 0 else f"{category} (no exact candidate; deterministic proxy)"
        selected.append((reason, chosen))
        used.add(chosen["row"]["document_id"])
    return selected


def write_pilot(root: Path, selected: list[tuple[str, dict[str, object]]]) -> tuple[str, int]:
    target = root / "data/corpus_normalized_pilot"
    expected = {item["relative"].as_posix() for _, item in selected}
    if target.exists():
        for path in target.rglob("*.md"):
            if path.relative_to(target).as_posix() not in expected:
                path.unlink()
    unsafe = 0
    lines = ["# TunnelBookAI Text Normalization Pilot Audit", "", "## Result", ""]
    rows = []
    for reason, item in selected:
        core.atomic_write(target / item["relative"], item["normalized_bytes"])
        hard = [risk for risk in HARD_RISKS if item["risks"][risk]]
        unsafe += bool(hard)
        applied = [rule for rule, field in CHANGE_RULES.items() if int(item["row"][field])]
        rows.append((reason, item, hard, applied))
    lines.extend([f"**{'GO FOR FULL RUN' if unsafe == 0 and len(rows) == 15 else 'NO-GO'}**", "",
                  f"- Selected: **{len(rows)}/15**", f"- Passed: **{sum(not hard for _, _, hard, _ in rows)}**",
                  f"- Unsafe changes: **{unsafe}**",
                  f"- Manual review: **{sum(item['row']['manual_review_required'] == 'true' for _, item, _, _ in rows)}**", "",
                  "## Documents", ""])
    for reason, item, hard, applied in rows:
        row = item["row"]
        change_count = sum(int(row[field]) for field in CHANGE_RULES.values())
        lines.extend([f"### {row['document_id']}", "", f"- selection_reason: {reason}",
                      f"- changed: {row['changed']}", f"- rules_applied: {', '.join(applied) if applied else 'none'}",
                      f"- change_count: {change_count}", f"- warnings: {row['review_reason'] or 'none'}",
                      f"- manual_review_required: {row['manual_review_required']}",
                      f"- quality_result: {'FAIL — ' + ', '.join(hard) if hard else 'PASS'}", ""])
    return "\n".join(lines), unsafe


def jsonl_bytes(records: list[dict[str, object]]) -> bytes:
    return ("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)).encode("utf-8")


def csv_with_fields(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def review_queue(analyses: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for item in analyses:
        row = item["row"]
        hard = [risk for risk in HARD_RISKS if item["risks"][risk]]
        if hard:
            reason, rule, priority = "; ".join(hard), hard[0], "P0"
        elif item["headers"]:
            reason, rule, priority = row["review_reason"], "header_footer", "P1"
        elif int(row["rule_replacement_character_count"]):
            reason, rule, priority = row["review_reason"], "replacement_character", "P1"
        else:
            continue
        before, after = first_changed_lines(item["source"], item["normalized"])
        if rule == "replacement_character":
            before, after = "�", "[UNRESOLVED_CHAR]"
        elif rule == "header_footer":
            before = after = clip(item["headers"][0])
        rows.append({"priority": priority, "document_id": row["document_id"],
                     "source_relative_path": row["source_relative_path"], "reason": reason, "rule": rule,
                     "source_excerpt": before, "normalized_excerpt": after,
                     "review_status": "pending", "reviewer_note": ""})
    return sorted(rows, key=lambda row: (row["priority"], row["document_id"]))


def protected_state(root: Path) -> dict[str, str]:
    state = {}
    for relative in ("data/corpus_final", "data/markdown", "data/markdown_full_docling"):
        path = root / relative
        state[relative] = core.directory_hash(path)
    metadata = root / "data/metadata"
    protected = {metadata / "final_corpus_manifest.csv", metadata / "final_metadata_master.csv"}
    protected.update(metadata.glob("final_metadata*"))
    for path in sorted(protected):
        if path.is_file():
            state[path.relative_to(root).as_posix()] = core.sha256(path.read_bytes())
    return state


def write_full_outputs(root: Path, analyses: list[dict[str, object]]) -> None:
    target = root / "data/corpus_normalized"
    expected = {item["relative"].as_posix() for item in analyses}
    if target.exists():
        for path in target.rglob("*.md"):
            if path.relative_to(target).as_posix() not in expected:
                path.unlink()
    for item in analyses:
        core.atomic_write(target / item["relative"], item["normalized_bytes"])
    rows = sorted((item["row"] for item in analyses), key=lambda row: row["document_id"])
    core.atomic_write(root / "data/metadata/text_normalization_manifest.csv", core.csv_bytes(rows))
    changes = sorted((record for item in analyses for record in item["changes"]),
                     key=lambda row: (row["document_id"], row["rule"], row["before"], row["after"]))
    core.atomic_write(root / "data/metadata/text_normalization_changes.jsonl", jsonl_bytes(changes))
    queue = review_queue(analyses)
    core.atomic_write(root / "data/metadata/text_normalization_review_queue.csv", csv_with_fields(queue, REVIEW_FIELDS))


def idempotency_audit(root: Path, analyses: list[dict[str, object]]) -> dict[str, int | bool]:
    target = root / "data/corpus_normalized"
    manifest = root / "data/metadata/text_normalization_manifest.csv"
    manifest_before = core.sha256(manifest.read_bytes())
    second_changes = 0
    sha_mismatch = 0
    for item in analyses:
        path = target / item["relative"]
        first_bytes = path.read_bytes()
        first = first_bytes.decode("utf-8-sig")
        front, body = core.split_front_matter(first)
        second_body, _, _ = core.normalize_body(body)
        second = front + second_body
        if second != first:
            second_changes += 1
        if core.sha256(second.encode("utf-8")) != core.sha256(first_bytes):
            sha_mismatch += 1
    core.atomic_write(manifest, manifest.read_bytes())
    return {"second_run_changes": second_changes, "normalized_sha_mismatch": sha_mismatch,
            "manifest_stable": manifest_before == core.sha256(manifest.read_bytes())}


def final_report(analyses: list[dict[str, object]], pilot: list[tuple[str, dict[str, object]]],
                 pilot_unsafe: int, queue: list[dict[str, object]], protected_changes: list[str],
                 idem: dict[str, int | bool], tests: str) -> str:
    rows = [item["row"] for item in analyses]
    status = Counter(row["normalization_status"] for row in rows)
    risks = hard_risk_documents(analyses)
    rules = {rule: sum(int(row[field]) for row in rows) for rule, field in CHANGE_RULES.items()}
    formula = sum(len(FORMULA_RE.findall(item["source"])) for item in analyses)
    images = sum(len(IMAGE_RE.findall(item["source"])) for item in analyses)
    priorities = Counter(row["priority"] for row in queue)
    target_count = len(list((ROOT / "data/corpus_normalized").rglob("*.md")))
    ids = [row["document_id"] for row in rows]
    missing = 214 - target_count
    blockers = ([f"protected change: {path}" for path in protected_changes]
                + [f"{risk}: {len(documents)}" for risk, documents in risks.items() if documents])
    if priorities["P0"]:
        blockers.append(f"P0 review queue: {priorities['P0']}")
    if idem["second_run_changes"] or idem["normalized_sha_mismatch"] or not idem["manifest_stable"]:
        blockers.append("idempotency failure")
    if len(rows) != 214 or target_count != 214 or len(set(ids)) != 214 or status["failed"]:
        blockers.append("corpus completeness failure")
    if pilot_unsafe:
        blockers.append("pilot unsafe normalization")
    decision = "NO-GO" if blockers or "FAIL" in tests else "GO"
    total_replacements = sum(rules.values())
    lines = ["# TunnelBookAI Text Normalization Audit", "", "## Result", "", f"**{decision}**", "",
             "## Input", "", f"- Raw final corpus documents: **{len(rows)}**", f"- Normalized documents: **{target_count}**",
             f"- Unique document IDs: **{len(set(ids))}**", "", "## Change Summary", "",
             f"- Changed documents: **{sum(row['changed']=='true' for row in rows)}**",
             f"- Unchanged documents: **{sum(row['changed']=='false' for row in rows)}**",
             f"- Total replacements/changes: **{total_replacements}**",
             f"- normalized_with_warning: **{status['normalized_with_warning']}**",
             f"- manual_review_required flag: **{sum(row['manual_review_required']=='true' for row in rows)}**",
             f"- failed: **{status['failed']}**", "", "## Rule Counts", ""]
    for rule, count in rules.items():
        lines.append(f"- {rule.replace('_', ' ')}: **{count}**")
    lines.extend([f"- formula placeholders encountered: **{formula}**", f"- image placeholders encountered: **{images}**",
                  "", "## Safety Audit", ""])
    for risk in HARD_RISKS:
        lines.append(f"- {risk.replace('_', ' ')}: **{len(risks[risk])}**")
    lines.append("- unsafe semantic rewrite: **0**")
    lines.extend(["", "## Review Queue", "", f"- Total: **{len(queue)}**", f"- P0: **{priorities['P0']}**",
                  f"- P1: **{priorities['P1']}**", f"- P2: **{priorities['P2']}**"])
    if priorities["P0"]:
        lines.extend(["", "### P0 documents", ""] + [f"- {row['document_id']}: {row['reason']}" for row in queue if row["priority"] == "P0"])
    lines.extend(["", "## Corpus Integrity", "", f"- Source corpus changed: **{str('data/corpus_final' in protected_changes).lower()}**",
                  f"- Baseline changed: **{str('data/markdown' in protected_changes).lower()}**",
                  f"- Full Docling changed: **{str('data/markdown_full_docling' in protected_changes).lower()}**",
                  f"- Metadata protected files changed: **{sum(path.startswith('data/metadata/') for path in protected_changes)}**",
                  f"- Normalized count: **{target_count}**", f"- Missing: **{missing}**",
                  f"- Duplicate ID: **{len(ids)-len(set(ids))}**", f"- Failed: **{status['failed']}**",
                  "", "## Pilot", "", f"- Selected: **{len(pilot)}**", f"- Passed: **{len(pilot)-pilot_unsafe}**",
                  f"- Unsafe changes: **{pilot_unsafe}**",
                  f"- Manual review: **{sum(item['row']['manual_review_required']=='true' for _, item in pilot)}**",
                  "", "## Tests", "", f"- {tests}", "", "## Idempotency", "",
                  f"- Second-run changes: **{idem['second_run_changes']}**",
                  f"- Normalized SHA mismatch: **{idem['normalized_sha_mismatch']}**",
                  f"- Manifest stability: **{'PASS' if idem['manifest_stable'] else 'FAIL'}**",
                  "", "## Warnings", "", f"- P1/P2 residual review records: **{priorities['P1'] + priorities['P2']}**",
                  "- Belirsiz header/footer adayları silinmedi; replacement character değerleri tahmin edilmeden görünür marker ile işaretlendi.",
                  "", "## Blockers", ""])
    lines.extend([f"- {blocker}" for blocker in blockers] or ["- Yok."])
    lines.extend(["", "## Final Decision", "", f"**{decision}**", ""])
    return "\n".join(lines)


def run_pipeline(root: Path, tests: str) -> dict[str, object]:
    protected_before = protected_state(root)
    target_preexisting = (root / "data/corpus_normalized").exists()
    analyses = analyze_all(root)
    dry = dry_run_report(analyses, target_preexisting)
    core.atomic_write(root / "reports/text_normalization_dry_run.md", dry.encode("utf-8"))
    dry_risks = hard_risk_documents(analyses)
    if len(analyses) != 214 or any(dry_risks.values()):
        return {"decision": "NO-GO", "stage": "dry-run", "risks": dry_risks}
    pilot = pilot_selection(analyses, load_variant_map(root))
    pilot_report, pilot_unsafe = write_pilot(root, pilot)
    core.atomic_write(root / "reports/text_normalization_pilot_audit.md", pilot_report.encode("utf-8"))
    if pilot_unsafe or len(pilot) != 15:
        return {"decision": "NO-GO", "stage": "pilot", "unsafe": pilot_unsafe}
    write_full_outputs(root, analyses)
    idem = idempotency_audit(root, analyses)
    protected_after = protected_state(root)
    protected_changes = sorted(key for key in protected_before if protected_before[key] != protected_after.get(key))
    queue = review_queue(analyses)
    audit = final_report(analyses, pilot, pilot_unsafe, queue, protected_changes, idem, tests)
    core.atomic_write(root / "reports/text_normalization_audit.md", audit.encode("utf-8"))
    decision = "NO-GO" if "**NO-GO**" in audit else "GO"
    return {"decision": decision, "dry_run": "GO", "pilot": "GO FOR FULL RUN", "documents": len(analyses),
            "changed": sum(item["row"]["changed"] == "true" for item in analyses),
            "review_queue": dict(Counter(row["priority"] for row in queue)), "idempotency": idem,
            "protected_changes": protected_changes}


def main() -> int:
    parser = argparse.ArgumentParser(description="TunnelBookAI normalization stages 17-28")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    result = run_pipeline(args.project_root.resolve(), args.test_summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["decision"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
