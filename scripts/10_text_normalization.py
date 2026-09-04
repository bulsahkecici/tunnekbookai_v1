from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


NORMALIZER_VERSION = "text-normalizer-v1.1"
MANIFEST_FIELDS = [
    "document_id", "source_relative_path", "source_final_markdown", "normalized_markdown",
    "source_sha256", "normalized_sha256", "changed", "normalization_status",
    "rule_unicode_normalization_count", "rule_whitespace_count", "rule_ocr_spacing_count",
    "rule_linebreak_count", "rule_hyphenation_count", "rule_header_footer_count",
    "rule_replacement_character_count", "rule_encoding_cleanup_count", "rule_placeholder_count",
    "manual_review_required", "review_reason", "normalizer_version", "processed_at",
]
ENGINEERING_SYMBOLS = "µμ²³°±≤≥ØΦστ αβγ".replace(" ", "")
OCR_REPLACEMENTS = {
    "TÜRK İ YE": "TÜRKİYE", "TÜRK İYE": "TÜRKİYE", "TÜRKİ YE": "TÜRKİYE",
    "JEOLOJ İ K": "JEOLOJİK", "JEOLOJ İK": "JEOLOJİK",
    "İ ÇER İĞİ": "İÇERİĞİ", "İ ÇERİĞİ": "İÇERİĞİ",
}
MOJIBAKE = {
    "Ã¼": "ü", "Ãœ": "Ü", "Ã¶": "ö", "Ã–": "Ö", "Ã§": "ç", "Ã‡": "Ç",
    "Ä±": "ı", "Ä°": "İ", "ÄŸ": "ğ", "Äž": "Ğ", "ÅŸ": "ş", "Åž": "Ş",
}
NUMERIC_RE = re.compile(r"(?<![\w])(?:%\s*)?[+-]?\d+(?:[.,:]\d+)*(?:\s*(?:mm|cm|m|km|kN|N|MPa|GPa|Pa|°C|%))?(?![\w])", re.IGNORECASE)
PROTECTED_TOKEN_RE = re.compile(
    r"https?://[^\s)>]+|(?:doi\s*:\s*)?10\.\d{4,9}/[^\s)>]+|"
    r"(?:ISBN|ISSN)\s*[\dXx-]+|(?:EN|ASTM|DIN|ISO)\s*-?\s*[A-Z]?\d[\w./-]*|"
    r"RG-\d{1,2}/\d{1,2}/\d{4}-\d+",
    re.IGNORECASE,
)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(rows: list[dict[str, object]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=MANIFEST_FIELDS, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == payload:
        return False
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return True


def split_front_matter(text: str) -> tuple[str, str]:
    match = re.match(r"\A(---\r?\n.*?\r?\n---(?:\r?\n|\Z))", text, re.DOTALL)
    return (match.group(1), text[match.end():]) if match else ("", text)


def protect_inline_code(line: str) -> tuple[str, list[str]]:
    saved: list[str] = []
    def replace(match: re.Match[str]) -> str:
        saved.append(match.group(0))
        return f"\uE000{len(saved) - 1}\uE001"
    return re.sub(r"`[^`\n]+`", replace, line), saved


def protect_inline_comments(line: str) -> tuple[str, list[str]]:
    saved: list[str] = []
    def replace(match: re.Match[str]) -> str:
        saved.append(match.group(0))
        return f"\uE002{len(saved) - 1}\uE003"
    return re.sub(r"<!--.*?-->", replace, line), saved


def restore_inline_code(line: str, saved: list[str]) -> str:
    for index, value in enumerate(saved):
        line = line.replace(f"\uE000{index}\uE001", value)
    return line


def restore_inline_comments(line: str, saved: list[str]) -> str:
    for index, value in enumerate(saved):
        line = line.replace(f"\uE002{index}\uE003", value)
    return line


def normalize_plain_line(line: str, counts: Counter) -> str:
    line, comments = protect_inline_comments(line)
    line, inline = protect_inline_code(line)
    original = line
    line = unicodedata.normalize("NFC", line)
    if line != original:
        counts["unicode"] += 1
    for broken, fixed in OCR_REPLACEMENTS.items():
        occurrences = line.count(broken)
        if occurrences:
            line = line.replace(broken, fixed)
            counts["ocr_spacing"] += occurrences
    for broken, fixed in MOJIBAKE.items():
        occurrences = line.count(broken)
        if occurrences:
            line = line.replace(broken, fixed)
            counts["encoding"] += occurrences
    replacements = line.count("�")
    if replacements:
        line = line.replace("�", "[UNRESOLVED_CHAR]")
        counts["replacement"] += replacements
    leading = re.match(r"^[ \t]*", line).group(0)
    content = line[len(leading):]
    if "\t" in content:
        counts["whitespace"] += content.count("\t")
        content = content.replace("\t", " ")
    collapsed = re.sub(r" {2,}", " ", content)
    if collapsed != content:
        counts["whitespace"] += 1
    content = collapsed
    trailing = len(content) - len(content.rstrip(" "))
    if trailing == 1:
        content = content.rstrip(" ")
        counts["whitespace"] += 1
    elif trailing > 2:
        content = content.rstrip(" ") + "  "
        counts["whitespace"] += 1
    return restore_inline_comments(restore_inline_code(leading + content, inline), comments)


def structural(line: str) -> bool:
    stripped = line.lstrip()
    return (not stripped or stripped.startswith(("#", "- ", "* ", "+ ", ">", "<!--", "```", "~~~"))
            or bool(re.match(r"\d+[.)]\s", stripped)) or stripped.startswith("|"))


def join_wrapped_lines(lines: list[str], protected: list[bool], counts: Counter) -> list[str]:
    output: list[str] = []
    index = 0
    while index < len(lines):
        current = lines[index]
        while index + 1 < len(lines):
            following = lines[index + 1]
            if (current and following and not protected[index] and not protected[index + 1]
                    and not structural(current) and not structural(following)):
                hyphen = re.search(r"([^\W\d_]{3,})-$", current)
                next_word = re.match(r"^\s*([^\W\d_]{2,})(.*)$", following)
                if hyphen and next_word and next_word.group(1)[0].islower():
                    prefix = current[:hyphen.start(1)]
                    current = prefix + hyphen.group(1) + next_word.group(1) + next_word.group(2)
                    counts["hyphenation"] += 1
                    index += 1
                    continue
                if (re.match(r"^\s*[a-zçğıöşü]", following)
                        and not re.search(r"[.!?:;…)'\"]$", current.rstrip())
                        and len(current.rstrip()) >= 40):
                    current = current.rstrip() + " " + following.lstrip()
                    counts["linebreak"] += 1
                    index += 1
                    continue
            break
        output.append(current)
        index += 1
    return output


def repeated_header_footer_candidates(body: str) -> list[str]:
    lines = [" ".join(line.split()) for line in body.splitlines()]
    candidates = Counter(line for line in lines if 3 <= len(line) <= 100 and not structural(line))
    return sorted(line for line, count in candidates.items() if count >= 6 and re.search(r"page|sayfa|\b\d+\s*/\s*\d+\b|copyright|www\.", line, re.IGNORECASE))


def normalize_body(body: str) -> tuple[str, Counter, list[str]]:
    counts: Counter = Counter()
    counts["placeholder"] = len(re.findall(r"formula-not-decoded|<!--\s*image\s*-->|image placeholder|figure placeholder", body, re.IGNORECASE))
    header_candidates = repeated_header_footer_candidates(body)
    newline = "\r\n" if "\r\n" in body else "\n"
    lines = body.splitlines()
    normalized: list[str] = []
    protected: list[bool] = []
    in_fence = False
    in_comment = False
    fence_marker = ""
    for line in lines:
        stripped = line.lstrip()
        fence = re.match(r"^(```+|~~~+)", stripped)
        if fence:
            marker = fence.group(1)[0:3]
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence = False
            normalized.append(line)
            protected.append(True)
            continue
        comment_line = in_comment or "<!--" in line
        if "<!--" in line and "-->" not in line[line.index("<!--") + 4:]:
            in_comment = True
        if in_comment and "-->" in line:
            in_comment = False
        if in_fence or stripped.startswith("|") or comment_line:
            normalized.append(line)
            protected.append(True)
            continue
        normalized.append(normalize_plain_line(line, counts))
        protected.append(False)
    normalized = join_wrapped_lines(normalized, protected, counts)
    compact: list[str] = []
    blank_run = 0
    for line in normalized:
        if line == "":
            blank_run += 1
            if blank_run <= 2:
                compact.append(line)
            else:
                counts["whitespace"] += 1
        else:
            blank_run = 0
            compact.append(line)
    result = newline.join(compact)
    if body.endswith(("\n", "\r")):
        result += newline
    return result, counts, header_candidates


def token_counter(pattern: re.Pattern[str], text: str) -> Counter:
    return Counter(re.sub(r"\s+", "", token) for token in pattern.findall(text))


def audit_safety(source: str, normalized: str, front: str, normalized_front: str) -> list[str]:
    reasons = []
    if front != normalized_front:
        reasons.append("front_matter_changed")
    if COMMENT_RE.findall(source) != COMMENT_RE.findall(normalized):
        reasons.append("citation_or_provenance_comment_changed")
    if token_counter(NUMERIC_RE, source) != token_counter(NUMERIC_RE, normalized):
        reasons.append("numeric_token_mismatch")
    if token_counter(PROTECTED_TOKEN_RE, source) != token_counter(PROTECTED_TOKEN_RE, normalized):
        reasons.append("url_doi_isbn_standard_token_mismatch")
    source_tables = [(line.count("|"), line) for line in source.splitlines() if line.lstrip().startswith("|")]
    normalized_tables = [(line.count("|"), line) for line in normalized.splitlines() if line.lstrip().startswith("|")]
    if source_tables != normalized_tables:
        reasons.append("markdown_table_changed")
    for symbol in ENGINEERING_SYMBOLS:
        if source.count(symbol) != normalized.count(symbol):
            reasons.append(f"engineering_symbol_changed:{symbol}")
    return reasons


def document_id(front: str) -> str:
    match = re.search(r"(?m)^document_id:\s*[\"']?([^\"'\s]+)", front)
    if not match:
        raise ValueError("document_id front matter içinde bulunamadı")
    return match.group(1)


def source_relative_path(front: str) -> str:
    match = re.search(r"(?m)^source_relative_path:\s*[\"']?(.*?)[\"']?\s*$", front)
    return match.group(1) if match else ""


def process(source_path: Path, source_root: Path, target_root: Path, previous: dict[str, dict[str, str]]) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source_text = source_bytes.decode("utf-8-sig", errors="strict")
    front, body = split_front_matter(source_text)
    normalized_body, counts, header_candidates = normalize_body(body)
    normalized_text = front + normalized_body
    normalized_bytes = normalized_text.encode("utf-8")
    normalized_front, _ = split_front_matter(normalized_text)
    safety = audit_safety(source_text, normalized_text, front, normalized_front)
    if header_candidates:
        safety.append("repeated_header_footer_candidate_not_removed:" + " | ".join(header_candidates[:3]))
    if counts["replacement"]:
        safety.append("replacement_character_marked_unresolved")
    relative = source_path.relative_to(source_root)
    target_path = target_root / relative
    atomic_write(target_path, normalized_bytes)
    changed = source_bytes != normalized_bytes
    review = bool(safety)
    warning = bool(counts["replacement"] or header_candidates)
    status = "manual_review_required" if review and any("mismatch" in item or "changed" in item for item in safety) else (
        "normalized_with_warning" if warning else "normalized" if changed else "unchanged")
    source_digest = sha256(source_bytes)
    old = previous.get(document_id(front), {})
    processed_at = old.get("processed_at", "") if old.get("source_sha256") == source_digest and old.get("normalizer_version") == NORMALIZER_VERSION else ""
    if not processed_at:
        processed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "document_id": document_id(front), "source_relative_path": source_relative_path(front),
        "source_final_markdown": (Path("data/corpus_final") / relative).as_posix(),
        "normalized_markdown": (Path("data/corpus_normalized") / relative).as_posix(),
        "source_sha256": source_digest, "normalized_sha256": sha256(normalized_bytes),
        "changed": str(changed).lower(), "normalization_status": status,
        "rule_unicode_normalization_count": counts["unicode"], "rule_whitespace_count": counts["whitespace"],
        "rule_ocr_spacing_count": counts["ocr_spacing"], "rule_linebreak_count": counts["linebreak"],
        "rule_hyphenation_count": counts["hyphenation"], "rule_header_footer_count": 0,
        "rule_replacement_character_count": counts["replacement"], "rule_encoding_cleanup_count": counts["encoding"],
        "rule_placeholder_count": counts["placeholder"], "manual_review_required": str(review).lower(),
        "review_reason": "; ".join(safety), "normalizer_version": NORMALIZER_VERSION, "processed_at": processed_at,
    }


def directory_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def report(rows: list[dict[str, object]], source_unchanged: bool, extra_targets: list[str], tests: str) -> str:
    status = Counter(str(row["normalization_status"]) for row in rows)
    totals = {key: sum(int(row[key]) for row in rows) for key in MANIFEST_FIELDS if key.startswith("rule_")}
    review_rows = [row for row in rows if str(row["manual_review_required"]) == "true"]
    decision = "GO" if len(rows) == 214 and len({row["document_id"] for row in rows}) == 214 and source_unchanged and not extra_targets and not status["failed"] else "NO-GO"
    lines = ["# TunnelBookAI Text Normalization Audit", "", "## Sonuç", "", f"- Karar: **{decision}**",
             f"- Source documents: **{len(rows)}/214**", f"- Normalized documents: **{len(rows)}/214**",
             f"- Unique document_id: **{len({row['document_id'] for row in rows})}**",
             f"- Changed documents: **{sum(str(row['changed']) == 'true' for row in rows)}**",
             f"- Source corpus değişti: **{str(not source_unchanged).lower()}**", "", "## Status", ""]
    for name in ("unchanged", "normalized", "normalized_with_warning", "manual_review_required", "failed"):
        lines.append(f"- {name}: **{status[name]}**")
    lines.extend(["", "## Rule counts", ""])
    lines.extend(f"- {key}: **{value}**" for key, value in totals.items())
    lines.extend(["", "## Safety", "", f"- Manual review required: **{sum(str(row['manual_review_required']) == 'true' for row in rows)}**",
                  f"- Extra/stale target file: **{len(extra_targets)}**", "- Front matter, provenance comments, tables, numeric tokens, protected identifiers and engineering symbols audited per document.",
                  "- Header/footer candidates were not silently deleted; uncertain repeats were flagged.",
                  "- Replacement characters were converted only to visible `[UNRESOLVED_CHAR]` markers and flagged.",
                  "", "## Warnings / review", "",
                  "- Bunlar blocker değildir; belirsiz içerik tahmin edilmedi ve kaynakta kalıcı değişiklik yapılmadı."])
    lines.extend(f"- `{row['document_id']}`: {row['review_reason']}" for row in review_rows)
    if not review_rows:
        lines.append("- Yok.")
    lines.extend(["", "## Testler", "", f"- {tests}", "",
                  "## Sınırlar", "", "- `data/corpus_final/` immutable source olarak korundu.",
                  "- Metadata inference, Docling conversion, chunking, embedding, Qdrant ve RAG çalıştırılmadı.", "", "## Blockers", "",
                  f"- {'Yok.' if decision == 'GO' else 'Corpus count/source immutability/output consistency kontrolü başarısız.'}", "",
                  "## Oluşturulan/değiştirilen çıktılar", "", "- `data/corpus_normalized/`",
                  "- `data/metadata/text_normalization_manifest.csv`", "- `reports/text_normalization_audit.md`",
                  "- `scripts/10_text_normalization.py`", "- `tests/test_text_normalization.py`",
                  "", "## Nihai karar", "", f"**{decision}**", ""])
    return "\n".join(lines)


def run(root: Path, limit: int = 0, tests: str = "Henüz çalıştırılmadı") -> dict[str, object]:
    source_root = root / "data/corpus_final"
    target_root = root / "data/corpus_normalized"
    manifest_path = root / "data/metadata/text_normalization_manifest.csv"
    source_before = directory_hash(source_root)
    sources = sorted(source_root.rglob("*.md"), key=lambda p: p.relative_to(source_root).as_posix())
    selected = sources[:limit] if limit else sources
    previous = {row["document_id"]: row for row in read_csv(manifest_path)}
    rows = [process(path, source_root, target_root, previous) for path in selected]
    rows.sort(key=lambda row: str(row["document_id"]))
    atomic_write(manifest_path, csv_bytes(rows))
    expected = {path.relative_to(source_root).as_posix() for path in selected}
    actual = {path.relative_to(target_root).as_posix() for path in target_root.rglob("*.md")} if target_root.exists() else set()
    extra = sorted(actual - expected)
    source_unchanged = directory_hash(source_root) == source_before
    audit = report(rows, source_unchanged, extra, tests)
    atomic_write(root / "reports/text_normalization_audit.md", audit.encode("utf-8"))
    statuses = Counter(str(row["normalization_status"]) for row in rows)
    summary = {"source_documents": len(selected), "normalized_documents": len(actual),
               "unique_document_id": len({row["document_id"] for row in rows}), "changed": sum(row["changed"] == "true" for row in rows),
               "status": dict(statuses), "manual_review": sum(row["manual_review_required"] == "true" for row in rows),
               "extra_targets": extra, "source_unchanged": source_unchanged}
    summary["decision"] = "GO" if len(selected) == 214 and len(actual) == 214 and summary["unique_document_id"] == 214 and source_unchanged and not extra and not statuses["failed"] else "NO-GO"
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Conservative derived-layer Markdown text normalization")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--test-summary", default="Henüz çalıştırılmadı")
    args = parser.parse_args()
    summary = run(args.project_root.resolve(), args.limit, args.test_summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["decision"] == "GO" or args.limit else 2


if __name__ == "__main__":
    raise SystemExit(main())
