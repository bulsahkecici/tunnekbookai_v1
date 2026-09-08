from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


MASTER_FIELDS = [
    "document_id", "source_relative_path", "source_filename", "source_extension",
    "source_sha256", "selected_variant", "authority_level_current",
    "authority_level_suggested", "authority_evidence", "authority_confidence",
    "document_type_current", "document_type_suggested", "document_type_evidence",
    "document_type_confidence", "language_current", "language_suggested",
    "language_confidence", "year_current", "year_suggested", "year_evidence",
    "year_confidence", "topics_current", "topics_suggested", "topics_evidence",
    "topics_confidence", "organization_suggested", "title_suggested", "citation_mode",
    "citation_sidecar", "original_page_provenance_available", "requires_human_review",
    "review_status",
]
QUEUE_FIELDS = [
    "document_id", "source_relative_path", "field", "current_value", "suggested_value",
    "evidence", "confidence", "reviewer_value", "reviewer_note", "review_status", "reviewed_at",
]
LANGUAGES = {"tr", "en", "de", "mixed", "unknown"}
AUTHORITY_LEVELS = {"A", "B", "C", "D", "unclassified"}
CONFIDENCES = {"high", "medium", "low"}
DOCUMENT_TYPES = {
    "regulation", "technical_specification", "standard", "manual", "handbook",
    "academic_article", "thesis", "conference_paper", "conference_proceedings",
    "technical_report", "presentation", "training_material", "project_document",
    "inspection_form", "cost_analysis", "inventory", "web_article", "magazine",
    "book_or_book_chapter", "drawing", "spreadsheet", "other", "unknown",
}
TOPICS = {
    "tunnel_general", "natm", "tbm", "geotechnical_investigation", "geology",
    "rock_mechanics", "route_selection", "excavation", "blasting", "shotcrete",
    "steel_mesh", "steel_rib", "rock_bolt", "forepoling", "support_systems",
    "ground_improvement", "jet_grouting", "injection", "karst", "water", "gas",
    "drainage", "waterproofing", "final_lining", "fiber_reinforced_concrete", "portal",
    "monitoring", "instrumentation", "risk", "safety", "fire_safety", "ventilation",
    "traffic", "operations", "maintenance", "inspection", "regulation", "standards",
    "cost", "unit_price", "payment", "contracts", "construction_management",
    "quality_control", "accident", "collapse", "case_study", "history", "inventory",
}
CITATION_MODES = {"pdf_page", "slide", "document_section", "table_or_sheet", "image", "source_only"}
MISSING = {"", "unknown", "unclassified", "null", "none"}
TRUE_VALUES = {"1", "true", "yes"}

TOPIC_ALIASES = {
    "tunnel_history": "history", "geotechnics": "geotechnical_investigation",
    "drill_and_blast": "blasting", "operation": "operations", "fiber_reinforcement": "fiber_reinforced_concrete",
    "special_solutions": "support_systems",
}
TOPIC_RULES = {
    "natm": [r"\bnatm\b", r"new austrian tunnel"],
    "tbm": [r"\btbm\b", r"tunnel boring machine"],
    "geotechnical_investigation": [r"geoteknik", r"geotechnical", r"zemin araştır", r"site investigation", r"sondaj"],
    "geology": [r"jeoloji", r"geolog"],
    "rock_mechanics": [r"kaya mekani", r"rock mechanics", r"rock mass", r"ho ek", r"rqd\b"],
    "route_selection": [r"güzergah seç", r"güzergâh seç", r"route selection", r"alignment selection"],
    "excavation": [r"kazı", r"excavat"],
    "blasting": [r"patlatma", r"blasting", r"drill.{0,8}blast"],
    "shotcrete": [r"püskürtme beton", r"shotcrete"],
    "steel_mesh": [r"çelik hasır", r"steel mesh", r"welded wire mesh"],
    "steel_rib": [r"çelik iksa", r"steel rib", r"lattice girder"],
    "rock_bolt": [r"kaya bulonu", r"rock bolt", r"rockbolt"],
    "forepoling": [r"süren", r"forepol", r"umbrella arch"],
    "support_systems": [r"destek sistem", r"support system", r"tahkimat"],
    "ground_improvement": [r"zemin iyileşt", r"ground improvement"],
    "jet_grouting": [r"jet ?grout"],
    "injection": [r"enjeksiyon", r"grout injection", r"injection"],
    "karst": [r"karst"],
    "water": [r"yeraltı su", r"groundwater", r"water inflow", r"su geliri"],
    "gas": [r"metan", r"methane", r"tünel gaz", r"tunnel gas"],
    "drainage": [r"drenaj", r"drainage"],
    "waterproofing": [r"su yalıt", r"waterproof"],
    "final_lining": [r"nihai kaplama", r"final lining", r"kalıcı kaplama"],
    "fiber_reinforced_concrete": [r"fiber reinforced", r"lifli beton", r"lif takviy"],
    "portal": [r"\bportal\b"],
    "monitoring": [r"izleme", r"monitoring"],
    "instrumentation": [r"enstrüman", r"instrumentation"],
    "risk": [r"\brisk\b", r"risk anal"],
    "safety": [r"güvenlik", r"safety"],
    "fire_safety": [r"yangın", r"fire safety", r"tunnel fire"],
    "ventilation": [r"havalandırma", r"ventilation"],
    "traffic": [r"trafik", r"traffic"],
    "operations": [r"işletme", r"operat(?:ion|ing)"],
    "maintenance": [r"bakım", r"maintenance"],
    "inspection": [r"muayene", r"inspection", r"kontrol form"],
    "regulation": [r"yönetmelik", r"mevzuat", r"regulation"],
    "standards": [r"standart", r"standard", r"\bts \d", r"\ben \d", r"\biso \d"],
    "cost": [r"maliyet", r"\bcost"],
    "unit_price": [r"birim fiyat", r"unit price"],
    "payment": [r"hakediş", r"payment certificate"],
    "contracts": [r"sözleşme", r"contract"],
    "construction_management": [r"yapım yönet", r"construction management", r"proje yönet"],
    "quality_control": [r"kalite kontrol", r"quality control", r"kalite güvence"],
    "accident": [r"kaza", r"accident"],
    "collapse": [r"çökme", r"collapse"],
    "case_study": [r"vaka", r"case study", r"örnek olay"],
    "history": [r"tarihçe", r"tunnel history", r"tünel tarihi"],
    "inventory": [r"envanter", r"inventory"],
    "tunnel_general": [r"\btünel", r"\btunnel"],
}


class MetadataError(RuntimeError):
    pass


def as_bool(value: object) -> bool:
    return str(value).strip().casefold() in TRUE_VALUES


def missing(value: str) -> bool:
    return (value or "").strip().casefold() in MISSING


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise MetadataError(f"Manifest bulunamadı: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(rows: Iterable[dict[str, object]], fields: list[str]) -> bytes:
    import io
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
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


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text).translate(str.maketrans({"İ": "i", "I": "ı"})).casefold()
    return re.sub(r"\s+", " ", text)


def strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    match = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n?", text, flags=re.DOTALL)
    return text[match.end():] if match else text


def index_final_markdown_by_document_id(project_root: Path) -> dict[str, Path]:
    """Index migrated final files by stable front-matter identity, not platform-specific names."""
    index: dict[str, Path] = {}
    corpus_root = project_root / "data/corpus_final"
    for path in corpus_root.rglob("*.md"):
        with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
            header = handle.read(8192)
        match = re.search(r'(?m)^document_id:\s*["\']?([^"\'\s]+)', header)
        if not match:
            continue
        document_id = match.group(1)
        if document_id in index:
            raise MetadataError(f"Final corpus'ta duplicate front-matter document_id: {document_id}")
        index[document_id] = path
    return index


def resolve_final_markdown(
    project_root: Path,
    final_row: dict[str, str],
    identity_index: dict[str, Path] | None = None,
) -> Path:
    expected = project_root / Path(unicodedata.normalize("NFC", final_row["final_output"].replace("\\", "/")))
    if expected.is_file():
        return expected
    index = identity_index if identity_index is not None else index_final_markdown_by_document_id(project_root)
    resolved = index.get(final_row["document_id"])
    if resolved is None:
        raise MetadataError(f"Final Markdown bulunamadı: {final_row['document_id']}")
    return resolved


def first_heading(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+?)\s*$", line.strip())
        if match:
            return match.group(1).strip()
    return ""


def analysis_excerpt(text: str, max_words: int = 2500) -> str:
    body = strip_front_matter(text)
    words = body.split()
    return " ".join(words[:max_words])


def infer_language(text: str, current: str) -> tuple[str, str]:
    current = (current or "").strip().casefold()
    if current in {"tr", "en", "de", "mixed"}:
        return current, "high"
    sample = analysis_excerpt(text, 1800)
    words = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşüÄÖÜäöüß]+", sample)
    if len(words) < 60:
        return "unknown", "low"
    lowered = [normalize(word) for word in words]
    counts = {
        "tr": sum(word in {"ve", "bir", "bu", "için", "ile", "olarak", "olan", "tünel", "kaya", "yapı", "yer", "de", "da"} for word in lowered) + sum(bool(re.search(r"[çğıöşü]", word)) for word in lowered),
        "en": sum(word in {"the", "and", "of", "to", "in", "for", "with", "is", "are", "tunnel", "construction", "road"} for word in lowered),
        "de": sum(word in {"der", "die", "das", "und", "von", "zu", "mit", "für", "ist", "im", "tunnel", "bau"} for word in lowered) + sum("ß" in word for word in lowered),
    }
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    best, best_count = ordered[0]
    second_count = ordered[1][1]
    threshold = max(5, len(words) // 120)
    if best_count < threshold:
        return "unknown", "low"
    if second_count >= threshold and second_count >= best_count * 0.65:
        return "mixed", "medium"
    return best, "high" if best_count >= threshold * 2 else "medium"


def infer_year(path: str, title: str, text: str, current: str) -> tuple[str, str, str, bool]:
    current = (current or "").strip()
    if re.fullmatch(r"(?:19|20)\d{2}", current):
        return current, f"Mevcut canonical metadata yılı: {current}", "high", False
    path_title = f"{path}\n{title}"
    explicit = sorted(set(re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", path_title)))
    if len(explicit) == 1:
        return explicit[0], f"Dosya yolu/başlıkta açık yıl: {explicit[0]}", "high", False
    if len(explicit) > 1:
        return "", f"Dosya yolu/başlıkta çelişkili yıllar: {', '.join(explicit)}", "low", True
    excerpt = analysis_excerpt(text, 2500)
    contextual = []
    pattern = re.compile(r"(?:yayın(?:lanma)?|publication|published|copyright|©|baskı|edition|tarih|date).{0,45}?((?:19|20)\d{2})", re.IGNORECASE)
    contextual.extend(pattern.findall(excerpt))
    contextual = sorted(set(contextual))
    if len(contextual) == 1:
        return contextual[0], f"Belge metninde publication/date bağlamında açık yıl: {contextual[0]}", "medium", False
    if len(contextual) > 1:
        return "", f"Belge metninde çelişkili publication/date yılları: {', '.join(contextual)}", "low", True
    return "", "Publication year için güvenilir açık kanıt bulunamadı; filesystem tarihi kullanılmadı", "low", False


def infer_document_type(path: str, title: str, text: str, current: str, extension: str) -> tuple[str, str, str]:
    current = (current or "").strip()
    if current in DOCUMENT_TYPES - {"unknown"}:
        return current, f"Mevcut canonical metadata document_type={current}", "high"
    heading = first_heading(text)
    strong_evidence = normalize(f"{path} {title} {heading}")
    content_evidence = normalize(analysis_excerpt(text, 500))
    evidence = f"{strong_evidence} {content_evidence}"
    strong_rules = [
        ("regulation", r"resmi gazete|yönetmelik|mevzuat|regulation|directive", "high"),
        ("technical_specification", r"teknik şartname|technical specification|şartnamesi", "high"),
        ("standard", r"\b(?:ts|en|iso|din)\s*\d{3,}|standardı|standard specification", "high"),
        ("thesis", r"doktora tezi|yüksek lisans tezi|doctoral thesis|master.?s thesis|a thesis submitted", "high"),
        ("conference_proceedings", r"bildiriler kitabı|conference proceedings|sempozyum bildirileri", "high"),
        ("conference_paper", r"conference paper|sempozyumu? bildir|kongre bildir", "medium"),
        ("inspection_form", r"kontrol formu|muayene formu|inspection form|checklist", "high"),
        ("cost_analysis", r"maliyet analiz|cost analysis|cost estimate|birim fiyat analiz", "medium"),
        ("inventory", r"envanter|inventory list|stok list", "high"),
        ("training_material", r"eğitim|kursu|ders notu|training material|lecture notes", "medium"),
        ("manual", r"el kitabı|manual|guidebook|kılavuz", "medium"),
        ("handbook", r"handbook", "high"),
        ("technical_report", r"technical report|teknik rapor|araştırma raporu|final report", "medium"),
        ("project_document", r"projesi|project document|uygulama projesi|metraj|hakediş", "medium"),
        ("drawing", r"çizim|drawing|plan pafta|kesit|detay", "medium"),
        ("web_article", r"wikipedia|civil digital|web article", "high"),
        ("magazine", r"dergisi|magazine", "medium"),
        ("book_or_book_chapter", r"book chapter|chapter \d|kitabı", "medium"),
    ]
    for document_type, pattern, confidence in strong_rules:
        match = re.search(pattern, strong_evidence)
        if match:
            return document_type, f"Dosya yolu/başlık/ilk heading sinyali: {match.group(0)[:100]}", confidence
    content_rules = [
        ("academic_article", r"\bdoi\b|journal of|research article|abstract.{0,80}keywords", "medium"),
        ("thesis", r"doktora tezi|yüksek lisans tezi|doctoral thesis|master.?s thesis|a thesis submitted", "high"),
        ("web_article", r"wikipedia|civil digital|web article", "high"),
    ]
    for document_type, pattern, confidence in content_rules:
        match = re.search(pattern, content_evidence)
        if match:
            return document_type, f"İlk içerik bölümünde yayın türü sinyali: {match.group(0)[:100]}", confidence
    if extension in {".ppt", ".pptx", ".pptm"} and re.search(r"slayt|sunum|presentation", evidence):
        return "presentation", "PPT içeriğinde slayt/sunum yapısı", "high"
    if extension in {".xls", ".xlsx"} and re.search(r"sayfa|sheet|tablo", evidence):
        return "spreadsheet", "Çalışma kitabında sheet/tablo yapısı", "high"
    return "unknown", "Kontrollü document type vocabulary için yeterli içerik kanıtı bulunamadı", "low"


def infer_authority(path: str, title: str, text: str, current: str, document_type: str) -> tuple[str, str, str, str]:
    current = (current or "").strip()
    strong_evidence = normalize(f"{path} {title} {first_heading(text)}")
    content_evidence = normalize(analysis_excerpt(text, 900))
    evidence_text = f"{strong_evidence} {content_evidence}"
    organizations = [
        ("Karayolları Genel Müdürlüğü (KGM)", r"karayolları genel müdürlüğü|(?<![a-z0-9])kgm(?![a-z0-9])"),
        ("Resmî Gazete", r"resmi gazete|resmî gazete"),
        ("FHWA", r"federal highway administration|(?<![a-z0-9])fhwa(?![a-z0-9])"),
        ("PIARC", r"world road association|(?<![a-z0-9])piarc(?![a-z0-9])"),
        ("TSE", r"türk standartları enstitüsü|(?<![a-z0-9])tse(?![a-z0-9])"),
    ]
    organization = next((name for name, pattern in organizations if re.search(pattern, evidence_text)), "")
    if current in {"A", "B", "C", "D"}:
        return current, f"Mevcut canonical metadata authority_level={current}", "high", organization
    if re.search(r"wikipedia|civil digital|blog|web article", evidence_text):
        return "D", "Secondary web/Wikipedia kaynağı sinyali", "high", organization
    official_type = document_type in {"regulation", "technical_specification", "standard", "manual", "handbook", "technical_report"}
    official_pattern = r"resmi gazete|resmî gazete|mevzuat|yönetmelik|federal highway administration|(?<![a-z0-9])fhwa(?![a-z0-9])|world road association|(?<![a-z0-9])piarc(?![a-z0-9])|karayolları genel müdürlüğü|(?<![a-z0-9])kgm(?![a-z0-9])"
    official_signal = re.search(official_pattern, strong_evidence)
    if official_signal and official_type:
        return "A", f"Resmî kurum + authoritative belge türü: {official_signal.group(0)}; {document_type}", "high", organization
    if re.search(r"resmi gazete|resmî gazete|mevzuat|yönetmelik", strong_evidence):
        return "A", "Resmî mevzuat/yönetmelik kanıtı", "high", organization
    if document_type == "thesis" and re.search(r"üniversite|university|enstitü|institute", evidence_text):
        university = re.search(r"[\wçğıöşü .-]{0,60}(?:üniversitesi|university)", evidence_text)
        return "B", f"Üniversite tez/research kanıtı: {(university.group(0) if university else 'university thesis')[-100:]}", "high", organization
    if document_type in {"academic_article", "conference_paper", "conference_proceedings", "thesis"}:
        return "B", f"Akademik yayın türü sinyali: {document_type}", "medium", organization
    if document_type in {"presentation", "training_material"} or re.search(r"eğitim|kursu|teknik sunum|seminar", evidence_text):
        return "C", "Profesyonel eğitim/sunum/sektör dokümanı sinyali", "medium", organization
    if official_signal:
        return "unclassified", f"Başlık/yolda kurum adı var ancak authoritative belge türü doğrulanmadı: {official_signal.group(0)}", "low", organization
    cited_official = re.search(official_pattern, content_evidence)
    if cited_official:
        return "unclassified", f"İçerikte resmî kaynağa atıf var; belgenin kendisinin authority'si doğrulanmadı: {cited_official.group(0)}", "low", organization
    return "unclassified", "Authority sınıfı için güvenilir kurum/yayın türü kanıtı bulunamadı", "low", organization


def infer_topics(path: str, title: str, text: str, current: str) -> tuple[list[str], str, str]:
    selected = set()
    current_values = [part.strip() for part in (current or "").split("|") if part.strip()]
    for value in current_values:
        canonical = TOPIC_ALIASES.get(value, value)
        if canonical in TOPICS:
            selected.add(canonical)
    evidence_text = normalize(f"{path} {title} {first_heading(text)} {analysis_excerpt(text, 1200)}")
    matched = []
    for topic, patterns in TOPIC_RULES.items():
        for pattern in patterns:
            match = re.search(pattern, evidence_text)
            if match:
                selected.add(topic)
                matched.append(f"{topic}:{match.group(0)[:50]}")
                break
    if len(selected) > 1 and "tunnel_general" in selected:
        selected.remove("tunnel_general")
    values = sorted(selected)
    if not values:
        return [], "Kontrollü topic vocabulary için yeterli kanıt bulunamadı", "low"
    confidence = "high" if current_values or len(values) >= 2 else "medium"
    return values, "; ".join(matched[:12]) or "Mevcut canonical topic eşlemesi", confidence


def citation_mode(extension: str, provenance: bool) -> str:
    extension = extension.casefold()
    if extension == ".pdf" and provenance:
        return "pdf_page"
    if extension in {".ppt", ".pptx", ".pptm"}:
        return "slide"
    if extension in {".doc", ".docx", ".rtf", ".txt"}:
        return "document_section"
    if extension in {".xls", ".xlsx", ".csv"}:
        return "table_or_sheet"
    if extension in {".jpg", ".jpeg", ".png", ".tif", ".tiff"}:
        return "image"
    return "source_only"


def build_master(project_root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]:
    metadata_dir = project_root / "data/metadata"
    final_rows = read_csv(metadata_dir / "final_corpus_manifest.csv")
    current_rows = read_csv(metadata_dir / "markdown_metadata.csv")
    current_by_id = {row["document_id"]: row for row in current_rows}
    if len(final_rows) != 214 or len({row["document_id"] for row in final_rows}) != 214:
        raise MetadataError("GO engeli: final manifest tam ve benzersiz 214 canonical document_id içermiyor")
    output_rows = []
    queue = []
    year_conflicts = 0
    identity_index: dict[str, Path] | None = None
    for final in sorted(final_rows, key=lambda row: row["document_id"]):
        document_id = final["document_id"]
        current = current_by_id.get(document_id)
        if not current:
            raise MetadataError(f"Canonical metadata satırı eksik: {document_id}")
        expected_final_path = project_root / Path(unicodedata.normalize("NFC", final["final_output"].replace("\\", "/")))
        if not expected_final_path.is_file() and identity_index is None:
            identity_index = index_final_markdown_by_document_id(project_root)
        final_path = resolve_final_markdown(project_root, final, identity_index)
        text = final_path.read_text(encoding="utf-8-sig", errors="replace")
        path = final["source_relative_path"]
        filename = Path(unicodedata.normalize("NFC", path)).name
        extension = Path(filename).suffix.casefold()
        title = current.get("title", "") or first_heading(text) or Path(filename).stem

        language, language_conf = infer_language(text, current.get("language", ""))
        year, year_evidence, year_conf, year_conflict = infer_year(path, title, text, current.get("year", ""))
        year_conflicts += int(year_conflict)
        doc_type, doc_evidence, doc_conf = infer_document_type(path, title, text, current.get("document_type", ""), extension)
        authority, authority_evidence, authority_conf, organization = infer_authority(path, title, text, current.get("authority_level", ""), doc_type)
        topics, topics_evidence, topics_conf = infer_topics(path, title, text, current.get("topics", ""))
        provenance = as_bool(final.get("original_page_provenance_available", ""))
        mode = citation_mode(extension, provenance)

        review_reasons = []
        if authority_conf in {"medium", "low"} or authority == "unclassified":
            review_reasons.append(("authority_level", current.get("authority_level", ""), authority, authority_evidence, authority_conf))
        if year_conflict:
            review_reasons.append(("year", current.get("year", ""), year, year_evidence, year_conf))
        if doc_type == "unknown" or doc_conf == "low":
            review_reasons.append(("document_type", current.get("document_type", ""), doc_type, doc_evidence, doc_conf))
        if not topics or topics_conf == "low":
            review_reasons.append(("topics", current.get("topics", ""), "|".join(topics), topics_evidence, topics_conf))
        if language in {"mixed", "unknown"}:
            review_reasons.append(("language", current.get("language", ""), language, "Konservatif dil tespiti", language_conf))
        if authority in {"A", "B", "C"} and not organization:
            review_reasons.append(("organization", current.get("organization", ""), organization, "Authority kararı var; kurum doğrulaması eksik", "low"))

        requires_review = bool(review_reasons)
        output_rows.append({
            "document_id": document_id,
            "source_relative_path": path,
            "source_filename": filename,
            "source_extension": extension,
            "source_sha256": final["source_sha256"],
            "selected_variant": final["selected_variant"],
            "authority_level_current": current.get("authority_level", ""),
            "authority_level_suggested": authority,
            "authority_evidence": authority_evidence,
            "authority_confidence": authority_conf,
            "document_type_current": current.get("document_type", ""),
            "document_type_suggested": doc_type,
            "document_type_evidence": doc_evidence,
            "document_type_confidence": doc_conf,
            "language_current": current.get("language", ""),
            "language_suggested": language,
            "language_confidence": language_conf,
            "year_current": current.get("year", ""),
            "year_suggested": year,
            "year_evidence": year_evidence,
            "year_confidence": year_conf,
            "topics_current": current.get("topics", ""),
            "topics_suggested": "|".join(topics),
            "topics_evidence": topics_evidence,
            "topics_confidence": topics_conf,
            "organization_suggested": organization or current.get("organization", ""),
            "title_suggested": title,
            "citation_mode": mode,
            "citation_sidecar": final.get("citation_sidecar", ""),
            "original_page_provenance_available": str(provenance).lower(),
            "requires_human_review": str(requires_review).lower(),
            "review_status": "pending" if requires_review else "not_required",
        })
        for field, current_value, suggested, evidence, confidence in review_reasons:
            queue.append({
                "document_id": document_id, "source_relative_path": path, "field": field,
                "current_value": current_value, "suggested_value": suggested, "evidence": evidence,
                "confidence": confidence, "reviewer_value": "", "reviewer_note": "",
                "review_status": "pending", "reviewed_at": "",
            })
    queue.sort(key=lambda row: (row["document_id"], row["field"]))
    stats = {"year_conflicts": year_conflicts}
    return output_rows, queue, stats


def text_audit(project_root: Path, master: list[dict[str, str]]) -> tuple[str, dict[str, int]]:
    detectors = {
        "Türk İ YE benzeri OCR boşlukları": re.compile(r"\b(?:TÜRK\s+İ\s+YE|[A-ZÇĞİÖŞÜ]{3,}\s+İ\s+[A-ZÇĞİÖŞÜ]{1,5})\b"),
        "JEOLOJ İ K tipi parçalanmış kelimeler": re.compile(r"\b[A-ZÇĞİÖŞÜ]{4,}\s+İ\s+[A-ZÇĞİÖŞÜ]\b"),
        "Unicode replacement character": re.compile("\ufffd"),
        "Repeated whitespace": re.compile(r"(?:[ \t]{3,}|\n(?:[ \t]*\n){2,})"),
        "Dense glyph-code pattern": re.compile(r"(?:G\d{1,3}){10,}"),
        "Formula not decoded": re.compile(r"formula[-_ ]not[-_ ]decoded|equation[-_ ]not[-_ ]decoded", re.IGNORECASE),
        "Image placeholder": re.compile(r"!\[[^\]]*\]\([^)]*\)|<!--\s*(?:image|figure)[^>]*-->", re.IGNORECASE),
        "Line-break/hyphenation": re.compile(r"\b[\wÇĞİÖŞÜçğıöşü]{3,}-\s*\n\s*[\wÇĞİÖŞÜçğıöşü]{2,}\b"),
        "Broken encoding marker": re.compile(r"Ã.|Â.|Ä.|Å.|â(?:€™|€œ|€|€“|€)"),
    }
    counts = Counter()
    occurrences = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    suspicious_docs = set()
    short_docs = []
    repeated_header_docs = []
    for row in master:
        path = project_root / "data/corpus_final" / Path(unicodedata.normalize("NFC", row["source_relative_path"])).with_suffix(".md")
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        body = strip_front_matter(text)
        words = re.findall(r"\b\w+\b", body, flags=re.UNICODE)
        if len(words) < 100:
            short_docs.append((row["document_id"], len(words), row["source_relative_path"]))
        doc_suspicious = False
        for name, pattern in detectors.items():
            matches = list(pattern.finditer(body))
            if matches:
                counts[name] += 1
                occurrences[name] += len(matches)
                doc_suspicious = doc_suspicious or name in {
                    "Türk İ YE benzeri OCR boşlukları", "JEOLOJ İ K tipi parçalanmış kelimeler",
                    "Unicode replacement character", "Dense glyph-code pattern", "Broken encoding marker",
                }
                for match in matches[:2]:
                    if len(examples[name]) < 5:
                        sample = re.sub(r"\s+", " ", body[max(0, match.start()-45):match.end()+45]).strip()
                        examples[name].append(f"{row['document_id']}: {sample[:180]}")
        line_counts = Counter(
            re.sub(r"\s+", " ", line.strip()) for line in body.splitlines()
            if 4 <= len(line.strip()) <= 120 and not line.lstrip().startswith(("#", "|", "<!--", "---"))
        )
        repeated = [(line, count) for line, count in line_counts.items() if count >= 10]
        if repeated:
            repeated_header_docs.append((row["document_id"], sorted(repeated, key=lambda item: item[1], reverse=True)[:3]))
        if doc_suspicious:
            suspicious_docs.add(row["document_id"])
    counts["Çok tekrarlanan header/footer"] = len(repeated_header_docs)
    occurrences["Çok tekrarlanan header/footer"] = sum(sum(count for _, count in repeated) for _, repeated in repeated_header_docs)
    for document_id, repeated in repeated_header_docs[:5]:
        examples["Çok tekrarlanan header/footer"].append(f"{document_id}: " + "; ".join(f"{count}× {line[:100]}" for line, count in repeated))
    counts["Aşırı kısa belge (<100 kelime)"] = len(short_docs)
    occurrences["Aşırı kısa belge (<100 kelime)"] = len(short_docs)
    examples["Aşırı kısa belge (<100 kelime)"] = [f"{doc}: {words} kelime — {path}" for doc, words, path in short_docs[:5]]
    counts["OCR-confidence şüpheli içerik"] = len(suspicious_docs)
    occurrences["OCR-confidence şüpheli içerik"] = len(suspicious_docs)
    examples["OCR-confidence şüpheli içerik"] = sorted(suspicious_docs)[:5]

    lines = [
        "# TunnelBookAI Text Normalization Pre-Audit", "",
        "Bu rapor salt-okunur analizdir; `data/corpus_final/` üzerinde hiçbir normalization uygulanmadı.", "",
        "## Bulgular", "",
        "| Sorun | Etkilenen belge | Eşleşme |", "|---|---:|---:|",
    ]
    ordered = list(detectors) + ["Çok tekrarlanan header/footer", "Aşırı kısa belge (<100 kelime)", "OCR-confidence şüpheli içerik"]
    for name in ordered:
        lines.append(f"| {name} | {counts[name]} | {occurrences[name]} |")
    lines.extend(["", "## Örnekler", ""])
    for name in ordered:
        lines.append(f"### {name}")
        lines.append("")
        if examples[name]:
            lines.extend(f"- `{example}`" for example in examples[name])
        else:
            lines.append("- Eşleşme yok.")
        lines.append("")
    lines.extend([
        "## Sonraki normalization aşaması için öneriler", "",
        "- Yalnız yüksek kesinlikli Türkçe OCR harf-bölünmesi kuralları allowlist ve regresyon testleriyle uygulanmalı.",
        "- Unicode replacement ve broken-encoding örnekleri kaynağa göre insan kontrollü düzeltilmeli; toplu karakter değişimi yapılmamalı.",
        "- Header/footer kaldırma, belge içindeki aynı kısa satırın sayfa düzeyinde tekrarı doğrulandıktan sonra yapılmalı.",
        "- Hyphenation birleştirme sözlük ve satır bağlamıyla sınırlandırılmalı; gerçek bileşik/teknik terimler korunmalı.",
        "- Dense glyph ve formula-not-decoded belgeleri otomatik rewrite yerine baseline/sidecar karşılaştırmasına yönlendirilmeli.",
        "- Image placeholder bulunan belgeler görsel OCR/caption kapsamına ayrı alınmalı.",
        "- Aşırı kısa belgeler kaynak türü ve image/table ağırlığına göre insan incelemesine gönderilmeli.", "",
    ])
    return "\n".join(lines), dict(counts)


def metadata_audit(master: list[dict[str, str]], queue: list[dict[str, str]], text_stats: dict[str, int], test_summary: str) -> str:
    authority = Counter(row["authority_confidence"] for row in master)
    citation = Counter(row["citation_mode"] for row in master)
    duplicates = len(master) - len({row["document_id"] for row in master})
    missing_ids = sum(not row["document_id"] or not row["source_sha256"] for row in master)
    lines = [
        "# TunnelBookAI Metadata Enrichment Audit", "", "## Sonuç", "",
        f"- Karar: **{'GO' if len(master) == 214 and duplicates == 0 and missing_ids == 0 else 'NO-GO'}**",
        f"- Toplam belge: **{len(master)}**",
        f"- Language otomatik bulunan: **{sum(row['language_suggested'] != 'unknown' for row in master)}**",
        f"- Year otomatik bulunan: **{sum(bool(row['year_suggested']) for row in master)}**",
        f"- Document type otomatik bulunan: **{sum(row['document_type_suggested'] != 'unknown' for row in master)}**",
        f"- Authority high confidence: **{authority['high']}**",
        f"- Authority medium confidence: **{authority['medium']}**",
        f"- Authority low/unclassified: **{sum(row['authority_confidence'] == 'low' or row['authority_level_suggested'] == 'unclassified' for row in master)}**",
        f"- Topics bulunan: **{sum(bool(row['topics_suggested']) for row in master)}**",
        f"- Human review gereken belge: **{sum(row['requires_human_review'] == 'true' for row in master)}**",
        f"- Human review queue satırı: **{len(queue)}**", "",
        "## Citation mode dağılımı", "",
    ]
    lines.extend(f"- `{mode}`: **{citation[mode]}**" for mode in sorted(CITATION_MODES))
    lines.extend([
        "", "## Master integrity", "",
        f"- Metadata master duplicate document_id: **{duplicates}**",
        f"- Metadata master eksik zorunlu kimlik/SHA: **{missing_ids}**",
        f"- Canonical 214 document_id tam temsil: **{str(len(master) == 214 and duplicates == 0).lower()}**",
        "- Mevcut metadata `*_current` alanlarında korundu; suggestion alanları verified metadata olarak uygulanmadı.",
        "- Filesystem created/modified tarihleri publication year çıkarımında kullanılmadı.",
        "- Harici API/ücretli model çağrısı yapılmadı; LLM varsayılan olarak kapalıdır.", "",
        "## Text normalization pre-audit özeti", "",
    ])
    for key in sorted(text_stats):
        lines.append(f"- {key}: **{text_stats[key]} belge**")
    lines.extend(["", "## Test sonuçları", "", f"- {test_summary or 'Henüz çalıştırılmadı'}", ""])
    return "\n".join(lines)


def artifact_digest(project_root: Path) -> str:
    digest = hashlib.sha256()
    for relative in (
        "data/metadata/final_metadata_master.csv", "data/metadata/final_metadata_review_queue.csv",
        "reports/text_normalization_audit.md", "reports/metadata_enrichment_audit.md",
    ):
        path = project_root / relative
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run(project_root: Path, test_summary: str = "") -> dict[str, object]:
    master, queue, _ = build_master(project_root)
    text_report, text_stats = text_audit(project_root, master)
    report = metadata_audit(master, queue, text_stats, test_summary)
    changed = 0
    changed += atomic_write(project_root / "data/metadata/final_metadata_master.csv", csv_bytes(master, MASTER_FIELDS))
    changed += atomic_write(project_root / "data/metadata/final_metadata_review_queue.csv", csv_bytes(queue, QUEUE_FIELDS))
    changed += atomic_write(project_root / "reports/text_normalization_audit.md", text_report.encode("utf-8"))
    changed += atomic_write(project_root / "reports/metadata_enrichment_audit.md", report.encode("utf-8"))
    return {"go": len(master) == 214 and len({row['document_id'] for row in master}) == 214,
            "master_rows": len(master), "queue_rows": len(queue), "changed_artifacts": changed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic metadata suggestions and normalization pre-audit")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify-idempotent", action="store_true")
    parser.add_argument("--test-summary", default="")
    args = parser.parse_args()
    try:
        summary = run(args.project_root.resolve(), args.test_summary)
        if args.verify_idempotent:
            first = artifact_digest(args.project_root.resolve())
            second = run(args.project_root.resolve(), args.test_summary)
            if artifact_digest(args.project_root.resolve()) != first or second["changed_artifacts"]:
                raise MetadataError("Metadata enrichment hazırlığı idempotent değil")
            summary["idempotent"] = True
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["go"] else 2
    except MetadataError as exc:
        print(f"NO-GO: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
