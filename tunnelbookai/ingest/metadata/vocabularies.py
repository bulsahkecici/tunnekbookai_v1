"""Controlled metadata vocabularies and deterministic inference helpers.

This module is owned by the Unified Ingest Engine.  It deliberately contains no
legacy-corpus file access or artifact-writing behavior.
"""

from __future__ import annotations

import re
import unicodedata


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

TOPIC_ALIASES = {
    "tunnel_history": "history",
    "geotechnics": "geotechnical_investigation",
    "drill_and_blast": "blasting",
    "operation": "operations",
    "fiber_reinforcement": "fiber_reinforced_concrete",
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


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text).translate(str.maketrans({"İ": "i", "I": "ı"})).casefold()
    return re.sub(r"\s+", " ", text)


def strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    match = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n?", text, flags=re.DOTALL)
    return text[match.end():] if match else text


def first_heading(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+?)\s*$", line.strip())
        if match:
            return match.group(1).strip()
    return ""


def analysis_excerpt(text: str, max_words: int = 2500) -> str:
    return " ".join(strip_front_matter(text).split()[:max_words])


def infer_language(text: str, current: str) -> tuple[str, str]:
    current = (current or "").strip().casefold()
    if current in {"tr", "en", "de", "mixed"}:
        return current, "high"
    words = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşüÄÖÜäöüß]+", analysis_excerpt(text, 1800))
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
    explicit = sorted(set(re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", f"{path}\n{title}")))
    if len(explicit) == 1:
        return explicit[0], f"Dosya yolu/başlıkta açık yıl: {explicit[0]}", "high", False
    if len(explicit) > 1:
        return "", f"Dosya yolu/başlıkta çelişkili yıllar: {', '.join(explicit)}", "low", True
    pattern = re.compile(r"(?:yayın(?:lanma)?|publication|published|copyright|©|baskı|edition|tarih|date).{0,45}?((?:19|20)\d{2})", re.IGNORECASE)
    contextual = sorted(set(pattern.findall(analysis_excerpt(text, 2500))))
    if len(contextual) == 1:
        return contextual[0], f"Belge metninde publication/date bağlamında açık yıl: {contextual[0]}", "medium", False
    if len(contextual) > 1:
        return "", f"Belge metninde çelişkili publication/date yılları: {', '.join(contextual)}", "low", True
    return "", "Publication year için güvenilir açık kanıt bulunamadı; filesystem tarihi kullanılmadı", "low", False


def infer_document_type(path: str, title: str, text: str, current: str, extension: str) -> tuple[str, str, str]:
    current = (current or "").strip()
    if current in DOCUMENT_TYPES - {"unknown"}:
        return current, f"Mevcut canonical metadata document_type={current}", "high"
    strong_evidence = normalize(f"{path} {title} {first_heading(text)}")
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
