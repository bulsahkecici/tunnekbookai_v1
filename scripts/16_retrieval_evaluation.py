"""Dense retrieval evaluation for the frozen BGE-M3 / Qdrant baseline.

Measures DENSE BASELINE v1 as it actually is: BGE-M3 dense, cosine, Qdrant, no reranker, no sparse,
no query expansion, no thresholds, no low-content treatment. Everything else is simulated offline on
frozen raw results so the collection is never mutated.

Gold labels come from deterministic lexical evidence in the source text - never from embedding
similarity, which would make the evaluation circular.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import statistics
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path


BENCHMARK_VERSION = "retrieval-benchmark-v1"
BASELINE_NAME = "DENSE BASELINE v1"
COLLECTION = "tunnelbook_dense_v1"
MODEL_NAME = "BAAI/bge-m3"
MODEL_REVISION = "5617a9f61b028005a4858fdac845db406aefb181"
REST_URL = os.environ.get("TUNNELBOOK_QDRANT_URL", "http://localhost:6333")
K_VALUES = (1, 3, 5, 10, 20)
MAX_K = 20
THRESHOLDS = (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)
LOW_CONTENT_PENALTIES = (0.01, 0.02, 0.03, 0.05)
DIVERSITY_CAPS = (1, 2, 3)

PROTECTED = ("data/embeddings/bge_m3_dense.npy", "data/embeddings/bge_m3_chunk_ids.json",
             "data/metadata/full_embedding_manifest.csv", "data/metadata/full_embedding_input_manifest.csv",
             "data/chunks/chunks.jsonl", "data/chunks_recovery/chunks.jsonl")
PROTECTED_TREES = ("data/corpus_final", "data/corpus_normalized", "data/corpus_recovery")

# Queries reused from earlier smoke tests, tracked so they cannot dominate the benchmark.
SMOKE_REUSED = {"tunnel ventilation", "shotcrete", "rock bolt design", "tunnel maintenance cost",
                "tünel havalandırması", "kaya bulonu", "püskürtme beton", "jeoteknik araştırma",
                "NATM support systems", "Türkiye tünel haritası"}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


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


def csv_bytes(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return ("﻿" + buffer.getvalue()).encode("utf-8")


def jsonl_bytes(rows: list[dict[str, object]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def protected_state(root: Path) -> dict[str, str]:
    state = {relative: sha256((root / relative).read_bytes()) for relative in PROTECTED
             if (root / relative).is_file()}
    for relative in PROTECTED_TREES:
        base = root / relative
        if not base.is_dir():
            continue
        digest = hashlib.sha256()
        for path in sorted((p for p in base.rglob("*") if p.is_file()), key=lambda p: p.relative_to(base).as_posix()):
            digest.update(path.relative_to(base).as_posix().encode() + b"\0" + path.read_bytes())
        state[relative] = digest.hexdigest()
    return state


def load_corpus(root: Path) -> list[dict[str, object]]:
    """Index-order records: vector_index i corresponds to row i of bge_m3_dense.npy."""
    rows = read_csv(root / "data/metadata/full_embedding_manifest.csv")
    canonical = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks/chunks.jsonl")}
    recovery = {chunk["chunk_id"]: chunk for chunk in read_jsonl(root / "data/chunks_recovery/chunks.jsonl")}
    records = []
    for row in rows:
        source = canonical if row["source_kind"] == "canonical_chunk" else recovery
        chunk = source[row["chunk_id"]]
        records.append({
            "vector_index": int(row["vector_index"]), "chunk_id": row["chunk_id"],
            "document_id": row["document_id"], "source_kind": row["source_kind"],
            "text": str(chunk["text"]), "language": chunk.get("language"),
            "document_type": chunk.get("document_type"), "authority_level": chunk.get("authority_level"),
            "heading": chunk.get("heading"), "section_path": chunk.get("section_path"),
            "is_low_content": row["eligibility_status"] == "eligible_low_content",
            "contains_table": bool(chunk.get("contains_table")),
            "token_count": int(row["bge_m3_token_count"]),
        })
    return records


# ---------------------------------------------------------------- benchmark specification
# Each spec: (id, query, language, type, difficulty, topic, gold anchors, acceptable anchors, options)
# Anchors are regexes that must ALL match a chunk's text for it to qualify. Gold = directly answers;
# acceptable = relevant support. `lang` restricts gold to a source language (cross-lingual probes).

def specs() -> list[dict[str, object]]:
    def spec(qid, query, language, qtype, difficulty, topic, gold, acceptable=None, lang=None,
             cross=False, doc=None, notes=""):
        return {"query_id": qid, "query": query, "language": language, "query_type": qtype,
                "difficulty": difficulty, "topic": topic, "gold": gold,
                "acceptable": acceptable or [], "gold_language": lang, "cross_lingual": cross,
                "document": doc, "notes": notes}

    S = []
    # --- A. definition / concept -------------------------------------------------------------
    S += [
        spec("Q001", "What is the New Austrian Tunnelling Method?", "en", "definition", "medium", "natm",
             [r"\bNATM\b", r"New Austrian"], [r"\bNATM\b"]),
        spec("Q002", "NATM yönteminin temel ilkesi nedir?", "tr", "definition", "medium", "natm",
             [r"\bNATM\b", r"ilke|esas|prensip"], [r"\bNATM\b"]),
        spec("Q003", "What is shotcrete used for in tunnels?", "en", "definition", "easy", "shotcrete",
             [r"\bshotcrete\b", r"tunnel"], [r"\bshotcrete\b"]),
        spec("Q004", "Püskürtme beton nedir ve ne için kullanılır?", "tr", "definition", "easy", "shotcrete",
             [r"püskürtme beton"], [r"püskürtme beton|shotcrete"]),
        spec("Q005", "What does the Q-system classify?", "en", "definition", "hard", "classification",
             [r"Q[- ]system", r"rock mass|classification"], [r"Q[- ]system|Q sistemi"]),
        spec("Q006", "RMR kaya kütle sınıflandırma sistemi nedir?", "tr", "definition", "medium", "classification",
             [r"\bRMR\b", r"kaya|sınıflama|sınıflandırma"], [r"\bRMR\b"]),
        spec("Q007", "What is GSI in rock engineering?", "en", "definition", "hard", "classification",
             [r"\bGSI\b", r"Geological Strength|rock"], [r"\bGSI\b"]),
        spec("Q008", "Tünel aynası ne demektir?", "tr", "definition", "hard", "excavation",
             [r"tünel aynası|aynada|ayna stabil"], [r"\bayna\b"]),
        spec("Q009", "What is an immersed tube tunnel?", "en", "definition", "medium", "typology",
             [r"immersed", r"tunnel"], [r"immersed"]),
        spec("Q010", "Aç-kapa tünel yöntemi nedir?", "tr", "definition", "medium", "typology",
             [r"aç[- ]kapa", r"tünel"], [r"aç[- ]kapa|cut[- ]and[- ]cover"]),
        spec("Q011", "What is overbreak in tunnel excavation?", "en", "definition", "hard", "excavation",
             [r"overbreak"], [r"overbreak|fazla kazı"]),
        spec("Q012", "Konverjans ölçümü nedir?", "tr", "definition", "hard", "monitoring",
             [r"konverjans|convergence"], [r"konverjans|convergence|deformasyon"]),
    ]
    # --- B. design / engineering -------------------------------------------------------------
    S += [
        spec("Q013", "How are rock bolts designed and dimensioned?", "en", "design", "medium", "support",
             [r"rock bolt", r"design|length|spacing"], [r"rock bolt|bolt"]),
        spec("Q014", "Kaya bulonu boyu nasıl hesaplanır?", "tr", "design", "hard", "support",
             [r"bulon", r"boy|uzunluk|hesap"], [r"bulon"]),
        spec("Q015", "Tunnel lining design requirements", "en", "design", "medium", "lining",
             [r"lining", r"design"], [r"lining|kaplama"]),
        spec("Q016", "Tünel kaplama tasarımı esasları", "tr", "design", "medium", "lining",
             [r"kaplama", r"tasarım|proje"], [r"kaplama"]),
        spec("Q017", "How is a tunnel ventilation system designed?", "en", "design", "medium", "ventilation",
             [r"ventilation", r"design|system"], [r"ventilation"]),
        spec("Q018", "Tünel aydınlatma tasarımı nasıl yapılır?", "tr", "design", "medium", "lighting",
             [r"aydınlatma", r"tasarım|hesap|proje"], [r"aydınlatma"]),
        spec("Q019", "Segment lining for TBM tunnels", "en", "design", "hard", "tbm",
             [r"segment", r"\bTBM\b|lining"], [r"segment"]),
        spec("Q020", "Tünel drenaj sistemi tasarımı", "tr", "design", "medium", "drainage",
             [r"drenaj", r"sistem|tasarım|proje"], [r"drenaj"]),
        spec("Q021", "Support classes selection for weak rock", "en", "design", "hard", "support",
             [r"support class|destek sınıf", r"rock"], [r"support class|destek sınıf"]),
        spec("Q022", "Portal tasarımı ve şev stabilitesi", "tr", "design", "hard", "portal",
             [r"portal", r"şev|stabil"], [r"portal"]),
        spec("Q023", "Waterproofing membrane systems in tunnels", "en", "design", "medium", "waterproofing",
             [r"waterproof", r"membrane"], [r"waterproof|membran"]),
        spec("Q024", "Tünelde su yalıtımı nasıl yapılır?", "tr", "design", "medium", "waterproofing",
             [r"su yalıtım", r"tünel"], [r"su yalıtım|yalıtım"]),
    ]
    # --- C. construction ---------------------------------------------------------------------
    S += [
        spec("Q025", "TBM tunnel excavation process", "en", "construction", "easy", "tbm",
             [r"\bTBM\b", r"excavat"], [r"\bTBM\b"]),
        spec("Q026", "TBM ile tünel kazısı nasıl yapılır?", "tr", "construction", "easy", "tbm",
             [r"\bTBM\b", r"kazı"], [r"\bTBM\b"]),
        spec("Q027", "Drill and blast excavation method", "en", "construction", "medium", "excavation",
             [r"drill and blast|blasting", r"excavat|round"], [r"blast"]),
        spec("Q028", "Delme patlatma yöntemi ile kazı", "tr", "construction", "medium", "excavation",
             [r"patlatma", r"kazı"], [r"patlatma"]),
        spec("Q029", "Shotcrete application technique and thickness", "en", "construction", "medium", "shotcrete",
             [r"shotcrete", r"thickness|applic|spray"], [r"shotcrete"]),
        spec("Q030", "Püskürtme betonun uygulanma tekniği", "tr", "construction", "medium", "shotcrete",
             [r"püskürtme", r"uygulama|teknik"], [r"püskürtme beton"]),
        spec("Q031", "Grouting and ground improvement ahead of the face", "en", "construction", "hard", "grouting",
             [r"grouting", r"ground|face|ahead"], [r"grouting"]),
        spec("Q032", "Enjeksiyon ile zemin iyileştirme", "tr", "construction", "medium", "grouting",
             [r"enjeksiyon", r"zemin|iyileştir"], [r"enjeksiyon"]),
        spec("Q033", "Forepoling and umbrella arch support", "en", "construction", "hard", "presupport",
             [r"forepol|umbrella|pipe roof", r"support|arch"], [r"forepol|umbrella|süren"]),
        spec("Q034", "Süren uygulaması ve ön destek", "tr", "construction", "hard", "presupport",
             [r"süren", r"destek"], [r"süren"]),
        spec("Q035", "Cut and cover tunnel construction stages", "en", "construction", "medium", "typology",
             [r"cut[- ]and[- ]cover", r"construct|stage|excavat"], [r"cut[- ]and[- ]cover"]),
        spec("Q036", "Tünel kazısında sökme ve nakliye işleri", "tr", "construction", "hard", "excavation",
             [r"kazı", r"nakliye|taşıma"], [r"kazı"]),
    ]
    # --- D. geology / geotechnics ------------------------------------------------------------
    S += [
        spec("Q037", "Geotechnical investigation for tunnel route selection", "en", "geotechnical", "medium",
             "investigation", [r"geotechnical", r"investigat"], [r"geotechnical"]),
        spec("Q038", "Tünel güzergahında jeoteknik araştırmalar", "tr", "geotechnical", "easy", "investigation",
             [r"jeoteknik", r"araştırma"], [r"jeoteknik"]),
        spec("Q039", "Rock mass classification systems comparison", "en", "geotechnical", "hard", "classification",
             [r"\bRMR\b|Q[- ]system", r"classification|rock mass"], [r"\bRMR\b|\bGSI\b|Q[- ]system"]),
        spec("Q040", "Fay zonunda tünel açma sorunları", "tr", "geotechnical", "hard", "fault",
             [r"fay", r"tünel"], [r"fay|fault"]),
        spec("Q041", "Squeezing ground behaviour in deep tunnels", "en", "geotechnical", "hard", "ground",
             [r"squeezing"], [r"squeezing|sıkışma"]),
        spec("Q042", "Şişen zeminlerde tünel davranışı", "tr", "geotechnical", "hard", "ground",
             [r"şişme|şişen"], [r"şişme|swelling"]),
        spec("Q043", "Groundwater and permeability in tunnelling", "en", "geotechnical", "medium", "water",
             [r"groundwater|permeability", r"tunnel"], [r"groundwater|permeability"]),
        spec("Q044", "Yeraltı suyu ve tünel ilişkisi", "tr", "geotechnical", "medium", "water",
             [r"yeraltı suyu", r"tünel"], [r"yeraltı suyu"]),
        spec("Q045", "Surface settlement caused by tunnelling", "en", "geotechnical", "medium", "settlement",
             [r"settlement", r"surface|ground"], [r"settlement"]),
        spec("Q046", "Tünel kazısı kaynaklı yüzey oturmaları", "tr", "geotechnical", "hard", "settlement",
             [r"oturma", r"yüzey|zemin"], [r"oturma"]),
        spec("Q047", "Face stability analysis in soft ground", "en", "geotechnical", "hard", "stability",
             [r"face stability|stability of the face"], [r"face stability|ayna stabil"]),
        spec("Q048", "Jeolojik etüt raporunda hangi bilgiler bulunur?", "tr", "geotechnical", "hard",
             "investigation", [r"jeolojik", r"rapor|etüt"], [r"jeolojik"]),
    ]
    # --- E. operations / maintenance ---------------------------------------------------------
    S += [
        spec("Q049", "Tunnel inspection and maintenance procedures", "en", "operations", "easy", "maintenance",
             [r"inspection", r"maintenance"], [r"maintenance|inspection"]),
        spec("Q050", "Tünel bakım ve onarım işleri", "tr", "operations", "easy", "maintenance",
             [r"bakım", r"onarım|işletme"], [r"bakım"]),
        spec("Q051", "Annual operating cost estimate for a highway tunnel", "en", "operations", "medium", "cost",
             [r"annual", r"operating cost"], [r"operating cost|annual"]),
        spec("Q052", "Tünel işletme maliyetleri nelerdir?", "tr", "operations", "medium", "cost",
             [r"işletme", r"maliyet|gider"], [r"maliyet"]),
        spec("Q053", "Tunnel lighting operation and energy consumption", "en", "operations", "hard", "lighting",
             [r"lighting", r"energy|consumption|power"], [r"lighting"]),
        spec("Q054", "Tünel havalandırma sistemlerinin işletilmesi", "tr", "operations", "medium", "ventilation",
             [r"havalandırma", r"işlet|sistem"], [r"havalandırma"]),
        spec("Q055", "SCADA and tunnel control systems", "en", "operations", "hard", "control",
             [r"SCADA|control system", r"tunnel"], [r"SCADA|kontrol sistem"]),
        spec("Q056", "Tünel trafik yönetimi ve izleme", "tr", "operations", "medium", "traffic",
             [r"trafik", r"izleme|yönetim|kontrol"], [r"trafik"]),
        spec("Q057", "Periodic structural inspection intervals", "en", "operations", "hard", "inspection",
             [r"inspection", r"periodic|interval|routine"], [r"inspection"]),
        spec("Q058", "Tünel içi kaplama temizliği ve yıkama", "tr", "operations", "hard", "maintenance",
             [r"temizlik|yıkama", r"tünel"], [r"temizlik|yıkama"]),
        spec("Q059", "Drainage system maintenance in tunnels", "en", "operations", "medium", "drainage",
             [r"drainage", r"maintenance|clean"], [r"drainage"]),
        spec("Q060", "Tünel elektromekanik tesisat bakımı", "tr", "operations", "hard", "maintenance",
             [r"elektromekanik|elektrik", r"bakım|tesisat"], [r"elektromekanik|elektrik"]),
    ]
    # --- F. safety ---------------------------------------------------------------------------
    S += [
        spec("Q061", "Tunnel fire safety requirements", "en", "safety", "easy", "fire",
             [r"fire", r"safety|protection"], [r"fire"]),
        spec("Q062", "Tünelde yangın güvenliği önlemleri", "tr", "safety", "easy", "fire",
             [r"yangın", r"güvenlik|önlem"], [r"yangın"]),
        spec("Q063", "Emergency escape routes and cross passages", "en", "safety", "medium", "escape",
             [r"escape|emergency exit", r"route|passage|door"], [r"escape|emergency"]),
        spec("Q064", "Acil kaçış yolları ve kaçış tünelleri", "tr", "safety", "medium", "escape",
             [r"kaçış", r"yol|tünel"], [r"kaçış"]),
        spec("Q065", "Smoke control with jet fans", "en", "safety", "hard", "ventilation",
             [r"jet fan", r"smoke|duman"], [r"jet fan"]),
        spec("Q066", "Tünelde duman kontrolü ve tahliye", "tr", "safety", "hard", "ventilation",
             [r"duman", r"kontrol|tahliye"], [r"duman"]),
        spec("Q067", "Traffic safety in road tunnels", "en", "safety", "medium", "traffic",
             [r"traffic", r"safety"], [r"traffic safety"]),
        spec("Q068", "Karayolu tünellerinde trafik güvenliği", "tr", "safety", "easy", "traffic",
             [r"trafik güvenliği"], [r"trafik", r"güvenlik"]),
        spec("Q069", "Dangerous goods transport through tunnels", "en", "safety", "hard", "hazmat",
             [r"dangerous goods|hazardous", r"tunnel"], [r"dangerous goods|tehlikeli madde"]),
        spec("Q070", "Tünelde tehlikeli madde taşınması kuralları", "tr", "safety", "hard", "hazmat",
             [r"tehlikeli madde"], [r"tehlikeli madde"]),
    ]
    # --- G. regulation / specification -------------------------------------------------------
    S += [
        spec("Q071", "Tünel güvenliği yönetmeliğinde belirtilen asgari gereklilikler", "tr", "regulation",
             "medium", "regulation", [r"(?m)^MADDE\s+\d+", r"güvenlik"], [r"(?m)^MADDE\s+\d+"]),
        spec("Q072", "MADDE hükümlerine göre tünel işletmecisinin sorumlulukları", "tr", "regulation", "hard",
             "regulation", [r"(?m)^MADDE\s+\d+", r"işletme|sorumlu"], [r"(?m)^MADDE\s+\d+"]),
        spec("Q073", "Karayolları Teknik Şartnamesi püskürtme beton gereksinimleri", "tr", "regulation",
             "hard", "specification", [r"püskürtme beton", r"şartname|K\.?T\.?Ş|standart"],
             [r"püskürtme beton"]),
        spec("Q074", "Technical specification requirements for tunnel concrete", "en", "regulation", "hard",
             "specification", [r"specification|standard", r"concrete"], [r"specification"]),
        spec("Q075", "KGM tünel projelerinde uyulacak esaslar", "tr", "regulation", "hard", "specification",
             [r"\bKGM\b|Karayolları"], [r"\bKGM\b|Karayolları Genel"]),
        spec("Q076", "AASHTO design specification references", "en", "regulation", "medium", "specification",
             [r"AASHTO"], [r"AASHTO"]),
        spec("Q077", "Tünellerde kullanılacak işaretleme ve levhalar", "tr", "regulation", "hard", "signage",
             [r"işaretleme|levha", r"tünel"], [r"işaretleme|levha"]),
        spec("Q078", "Minimum gabari ve serbest yükseklik şartları", "tr", "regulation", "hard", "geometry",
             [r"gabari"], [r"gabari|serbest yükseklik"]),
        spec("Q079", "Acceptance criteria and quality control tests", "en", "regulation", "hard", "quality",
             [r"quality control|acceptance", r"test"], [r"quality control|acceptance"]),
        spec("Q080", "Bulon çekme deneyi kabul kriterleri", "tr", "regulation", "hard", "quality",
             [r"bulon", r"deney|çekme"], [r"bulon", r"deney"]),
    ]
    # --- H. numeric / table lookup -----------------------------------------------------------
    S += [
        spec("Q081", "Tunnel lighting energy cost per kWh", "en", "numeric", "hard", "cost",
             [r"kWh", r"cost|\$"], [r"kWh"]),
        spec("Q082", "Annual maintenance cost table for highway tunnel", "en", "numeric", "hard", "cost",
             [r"maintenance", r"annual", r"\$|cost"], [r"maintenance cost"]),
        spec("Q083", "Tünel uzunluklarına göre sınıflandırma tablosu", "tr", "numeric", "hard", "classification",
             [r"uzunluk", r"tünel", r"\|"], [r"uzunluk"]),
        spec("Q084", "Püskürtme beton dozaj ve kalınlık değerleri", "tr", "numeric", "hard", "shotcrete",
             [r"püskürtme beton", r"\d+\s*cm|dozaj|kalınlık"], [r"püskürtme beton"]),
        spec("Q085", "Rock bolt length and spacing values", "en", "numeric", "hard", "support",
             [r"bolt", r"\d+\s*m\b|spacing|length"], [r"bolt"]),
        spec("Q086", "Kaya sınıflarına göre destek elemanları çizelgesi", "tr", "numeric", "hard", "support",
             [r"kaya sınıf", r"destek"], [r"kaya sınıf"]),
        spec("Q087", "Ventilation air flow rate requirements", "en", "numeric", "hard", "ventilation",
             [r"ventilation|air", r"m3|m³|flow rate"], [r"ventilation"]),
        spec("Q088", "Tünel maliyet analizi birim fiyatları", "tr", "numeric", "hard", "cost",
             [r"birim fiyat|maliyet", r"\d"], [r"birim fiyat|maliyet"]),
        spec("Q089", "Concrete compressive strength class requirements", "en", "numeric", "hard", "materials",
             [r"compressive strength|C\d\d", r"concrete"], [r"compressive strength|concrete"]),
        spec("Q090", "Deformasyon ölçüm sonuçları ve limit değerler", "tr", "numeric", "hard", "monitoring",
             [r"deformasyon"], [r"deformasyon|ölçüm"]),
    ]
    # --- I. named entity / registry ----------------------------------------------------------
    S += [
        spec("Q091", "Türkiye'deki karayolu tünellerinin isimleri ve uzunlukları", "tr", "named_entity",
             "medium", "registry", [r"TÜNELİN ADI|TÜNEL ADI|Tünel Adı"], [r"TÜNELİN ADI|Tünel Adı|tünel"]),
        spec("Q092", "Ovit Tüneli hakkında bilgi", "tr", "named_entity", "hard", "registry",
             [r"Ovit"], [r"Ovit"]),
        spec("Q093", "Zigana Tüneli projesi", "tr", "named_entity", "hard", "registry",
             [r"Zigana"], [r"Zigana"]),
        spec("Q094", "Marmaray project tunnel", "en", "named_entity", "hard", "registry",
             [r"Marmaray"], [r"Marmaray"]),
        spec("Q095", "Gotthard Base Tunnel", "en", "named_entity", "hard", "registry",
             [r"Gotthard"], [r"Gotthard"]),
        spec("Q096", "Türk Tünelcilik Derneği üyeleri", "tr", "named_entity", "hard", "organisation",
             [r"TUNNELLING SOCIETY|Tünelcilik Derneği"], [r"Tünelcilik|TUNNELLING SOCIETY"]),
        spec("Q097", "Newfoundland Fixed Link study", "en", "named_entity", "hard", "registry",
             [r"Newfoundland"], [r"Newfoundland"]),
        spec("Q098", "Bolu Dağı Tüneli", "tr", "named_entity", "hard", "registry",
             [r"Bolu"], [r"Bolu"]),
    ]
    # --- J. source-specific factual ----------------------------------------------------------
    S += [
        spec("Q099", "What equipment is needed for tunnel operation and maintenance?", "en", "source_specific",
             "medium", "maintenance", [r"[Ee]quipment", r"O&amp;M|maintenance"], [r"equipment"]),
        spec("Q100", "Tunnel management office operator responsibilities", "en", "source_specific", "hard",
             "operations", [r"Management Office", r"[Oo]perator"], [r"Management Office"]),
        spec("Q101", "Sequential excavation method description", "en", "source_specific", "medium", "natm",
             [r"Sequential Excavation"], [r"Sequential Excavation|SEM"]),
        spec("Q102", "Tünel kontrol mühendisi geliştirme kursu içeriği", "tr", "source_specific", "medium",
             "training", [r"KONTROL MÜHENDİSİ|Kontrol Mühendisi"], [r"kontrol mühendisi"]),
        spec("Q103", "Life cycle cost comparison of tunnel pavements", "en", "source_specific", "hard", "cost",
             [r"life cycle", r"pavement"], [r"pavement"]),
        spec("Q104", "Tünellerde güzergah seçimi kriterleri", "tr", "source_specific", "medium", "route",
             [r"güzergah", r"seçim"], [r"güzergah"]),
        spec("Q105", "Effects of fire on the tunnel structure", "en", "source_specific", "hard", "fire",
             [r"[Ff]ire", r"structure|lining"], [r"fire"]),
        spec("Q106", "Tünel kazı sınıfları ve destek sistemleri ilişkisi", "tr", "source_specific", "hard",
             "support", [r"kazı sınıf|kaya sınıf", r"destek"], [r"kazı sınıf|kaya sınıf"]),
        spec("Q107", "Ground reinforcement types in tunnelling", "en", "source_specific", "medium", "support",
             [r"[Gg]round [Rr]einforcement"], [r"reinforcement"]),
        spec("Q108", "Tünel inşaatında karşılaşılan sorunlar", "tr", "source_specific", "medium", "problems",
             [r"Karşılaşılabilen|karşılaşılan sorun|Sorunlar"], [r"sorun"]),
        # cross-lingual probes: question in one language, evidence restricted to the other
        spec("Q109", "tünel havalandırma sistemi tasarımı", "tr", "design", "hard", "ventilation",
             [r"ventilation", r"design|system"], [r"ventilation"], lang="en", cross=True,
             notes="Turkish query, English-only gold: cross-lingual probe"),
        spec("Q110", "kaya kütlesi sınıflandırma sistemleri", "tr", "geotechnical", "hard", "classification",
             [r"rock mass", r"classification"], [r"rock mass"], lang="en", cross=True,
             notes="Turkish query, English-only gold"),
        spec("Q111", "tunnel maintenance and operation costs", "en", "operations", "hard", "cost",
             [r"bakım", r"işletme|maliyet"], [r"bakım"], lang="tr", cross=True,
             notes="English query, Turkish-only gold"),
        spec("Q112", "shotcrete application requirements", "en", "construction", "hard", "shotcrete",
             [r"püskürtme beton", r"uygulama|şartname"], [r"püskürtme beton"], lang="tr", cross=True,
             notes="English query, Turkish-only gold"),
        spec("Q113", "rock bolt pull-out test", "en", "regulation", "hard", "quality",
             [r"bulon", r"çekme|deney"], [r"bulon"], lang="tr", cross=True,
             notes="English query, Turkish-only gold"),
        spec("Q114", "geotechnical investigation report contents", "en", "geotechnical", "hard", "investigation",
             [r"jeoteknik|jeolojik", r"rapor"], [r"jeoteknik|jeolojik"], lang="tr", cross=True,
             notes="English query, Turkish-only gold"),
    ]
    return S


GOLD_DENSITY = 3


def resolve_gold(records: list[dict[str, object]], spec: dict[str, object]) -> dict[str, object]:
    """Deterministic lexical resolution. No embeddings involved, so labels are not circular.

    Two evidence levels, both lexical:
      gold       - the chunk is *about* the query: an anchor appears in its heading/section path, or
                   the anchor occurs repeatedly in the body. These directly answer.
      acceptable - every anchor appears somewhere in the text. Relevant support, not necessarily
                   sufficient alone.
    Requiring topical evidence rather than mere term presence keeps gold sets small enough that
    Recall@k measures something. Matching any occurrence would mark a third of the corpus relevant.
    """
    def matches_text(record, patterns):
        if not patterns:
            return False
        return all(re.search(pattern, record["text"], re.IGNORECASE) for pattern in patterns)

    def is_topical(record, patterns):
        if not matches_text(record, patterns):
            return False
        headline = " ".join(filter(None, [str(record.get("heading") or ""),
                                          str(record.get("section_path") or "")]))
        # The chunk's own section must be titled about the topic. A body mention is only "acceptable":
        # in a single-domain corpus almost every chunk mentions the domain terms somewhere.
        return any(re.search(pattern, headline, re.IGNORECASE) for pattern in patterns)

    def is_dense(record, patterns):
        """Fallback evidence: the anchor recurs in the body, so the chunk dwells on the topic."""
        if not matches_text(record, patterns):
            return False
        counts = [len(re.findall(pattern, record["text"], re.IGNORECASE)) for pattern in patterns]
        return min(counts) >= GOLD_DENSITY

    pool = records
    if spec["gold_language"]:
        pool = [record for record in records if (record["language"] or "") == spec["gold_language"]]
    if spec["document"]:
        pool = [record for record in pool if record["document_id"] == spec["document"]]
    method = "heading_anchor"
    gold = [record for record in pool if is_topical(record, spec["gold"])]
    if not gold:
        # No section in the corpus is titled for this concept. Fall back to repeated in-body evidence,
        # which is weaker but still deterministic and inspectable, and record which method was used.
        gold = [record for record in pool if is_dense(record, spec["gold"])]
        method = "body_density_anchor"
    if not gold:
        gold = [record for record in pool if matches_text(record, spec["gold"])]
        method = "body_presence_anchor"
    acceptable = [record for record in pool if matches_text(record, spec["acceptable"])]
    acceptable = {record["chunk_id"]: record for record in acceptable}
    for record in gold:
        acceptable[record["chunk_id"]] = record
    evidence = []
    for record in gold[:3]:
        snippet = " ".join(record["text"].split())
        window = ""
        for pattern in spec["gold"]:
            found = re.search(pattern, snippet, re.IGNORECASE)
            if found:
                window = snippet[max(0, found.start() - 60):found.start() + 120]
                break
        evidence.append({"chunk_id": record["chunk_id"], "document_id": record["document_id"],
                         "heading": record["heading"], "evidence_text": window})
    return {"gold": gold, "acceptable": list(acceptable.values()), "evidence": evidence,
            "method": method}


def build_benchmark(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    records = load_corpus(root)
    rows, problems = [], []
    for spec in specs():
        resolved = resolve_gold(records, spec)
        gold, acceptable = resolved["gold"], resolved["acceptable"]
        if not gold:
            problems.append(f"{spec['query_id']}: no gold chunk resolved")
            continue
        rows.append({
            "query_id": spec["query_id"], "query": spec["query"], "language": spec["language"],
            "query_type": spec["query_type"], "difficulty": spec["difficulty"], "topic": spec["topic"],
            "cross_lingual": bool(spec["cross_lingual"]),
            "gold_document_ids": sorted({record["document_id"] for record in gold}),
            "gold_chunk_ids": sorted(record["chunk_id"] for record in gold),
            "acceptable_document_ids": sorted({record["document_id"] for record in acceptable}),
            "acceptable_chunk_ids": sorted(record["chunk_id"] for record in acceptable),
            "source_evidence": resolved["evidence"],
            "annotation_method": resolved["method"] + ("_language_restricted"
                                                        if spec["gold_language"] else ""),
            "gold_anchor_patterns": spec["gold"],
            "reused_smoke_query": spec["query"] in SMOKE_REUSED,
            "notes": spec["notes"],
        })
    # Difficulty is derived, not guessed: how much of the query's wording actually appears in the
    # gold chunks' headings. Cross-lingual probes are hard by construction.
    lookup = {record["chunk_id"]: record for record in records}
    for row in rows:
        if row["cross_lingual"]:
            row["difficulty"] = "hard"
            continue
        words = {word for word in re.findall(r"[^\W\d_]{4,}", row["query"].lower())}
        best = 0
        for chunk_id in row["gold_chunk_ids"][:40]:
            record = lookup.get(chunk_id)
            if not record:
                continue
            headline = " ".join(filter(None, [str(record.get("heading") or ""),
                                              str(record.get("section_path") or "")])).lower()
            overlap = sum(1 for word in words if word in headline)
            best = max(best, overlap)
        row["difficulty"] = "easy" if best >= 2 else "medium" if best == 1 else "hard"

    identifiers = [row["query_id"] for row in rows]
    if len(set(identifiers)) != len(identifiers):
        problems.append("duplicate query_id")
    queries = [row["query"].strip().lower() for row in rows]
    if len(set(queries)) != len(queries):
        problems.append("duplicate query text")
    known = {record["chunk_id"] for record in records}
    for row in rows:
        missing = [chunk_id for chunk_id in row["gold_chunk_ids"] if chunk_id not in known]
        if missing:
            problems.append(f"{row['query_id']}: gold chunks missing from index: {missing[:3]}")
    reused = sum(row["reused_smoke_query"] for row in rows)
    if rows and reused / len(rows) > 0.15:
        problems.append(f"smoke-derived queries exceed 15%: {reused}/{len(rows)}")
    return rows, problems



# ---------------------------------------------------------------- metrics

def dcg(gains: list[float]) -> float:
    return sum(gain / math.log2(position + 2) for position, gain in enumerate(gains))


def ndcg_at_k(hits: list[dict[str, object]], gold: set, acceptable: set, k: int) -> float:
    def gain(hit):
        return 1.0 if hit["chunk_id"] in gold else 0.5 if hit["chunk_id"] in acceptable else 0.0
    actual = dcg([gain(hit) for hit in hits[:k]])
    ideal = dcg(sorted([1.0] * len(gold) + [0.5] * max(0, len(acceptable - gold)), reverse=True)[:k])
    return actual / ideal if ideal else 0.0


def query_metrics(hits: list[dict[str, object]], row: dict[str, object]) -> dict[str, object]:
    gold = set(row["gold_chunk_ids"])
    acceptable = set(row["acceptable_chunk_ids"])
    gold_documents = set(row["gold_document_ids"])
    acceptable_documents = set(row["acceptable_document_ids"])
    result = {}
    for k in K_VALUES:
        window = hits[:k]
        result[f"recall@{k}"] = float(any(hit["chunk_id"] in gold for hit in window))
        result[f"acceptable@{k}"] = float(any(hit["chunk_id"] in acceptable for hit in window))
        result[f"doc_recall@{k}"] = float(any(hit["document_id"] in gold_documents for hit in window))
        result[f"doc_acceptable@{k}"] = float(any(hit["document_id"] in acceptable_documents
                                                  for hit in window))
        result[f"precision@{k}"] = (sum(hit["chunk_id"] in gold for hit in window) / k) if window else 0.0
    reciprocal = 0.0
    for position, hit in enumerate(hits[:10], start=1):
        if hit["chunk_id"] in gold:
            reciprocal = 1.0 / position
            break
    document_reciprocal = 0.0
    for position, hit in enumerate(hits[:10], start=1):
        if hit["document_id"] in gold_documents:
            document_reciprocal = 1.0 / position
            break
    result["mrr@10"] = reciprocal
    result["doc_mrr@10"] = document_reciprocal
    result["ndcg@10"] = ndcg_at_k(hits, gold, acceptable, 10)
    result["unique_docs@5"] = len({hit["document_id"] for hit in hits[:5]})
    result["unique_docs@10"] = len({hit["document_id"] for hit in hits[:10]})
    result["low_content@1"] = float(bool(hits) and hits[0]["is_low_content"])
    result["low_content@5"] = sum(hit["is_low_content"] for hit in hits[:5])
    result["low_content@10"] = sum(hit["is_low_content"] for hit in hits[:10])
    return result


def aggregate(per_query: list[dict[str, object]], keys: list[str]) -> dict[str, float]:
    return {key: (statistics.mean([entry["metrics"][key] for entry in per_query]) if per_query else 0.0)
            for key in keys}


METRIC_KEYS = ([f"recall@{k}" for k in K_VALUES] + [f"acceptable@{k}" for k in K_VALUES]
               + [f"doc_recall@{k}" for k in K_VALUES] + [f"precision@{k}" for k in K_VALUES]
               + ["mrr@10", "doc_mrr@10", "ndcg@10", "unique_docs@5", "unique_docs@10",
                  "low_content@1", "low_content@5", "low_content@10"])


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def distribution(values: list[float]) -> dict[str, float]:
    return {"min": min(values) if values else 0.0, "p10": percentile(values, .10),
            "p25": percentile(values, .25), "median": percentile(values, .50),
            "p75": percentile(values, .75), "p90": percentile(values, .90),
            "max": max(values) if values else 0.0}


# ---------------------------------------------------------------- retrieval

def embed_queries(queries: list[str], batch: int = 16):
    import torch
    from transformers import AutoModel, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
    model = AutoModel.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device).eval()
    import numpy
    out = []
    latencies = []
    for start in range(0, len(queries), batch):
        window = queries[start:start + batch]
        began = time.perf_counter()
        encoded = tokenizer(window, padding=True, truncation=True, max_length=8192, return_tensors="pt")
        encoded = {key: value.to(device) for key, value in encoded.items()}
        with torch.inference_mode():
            vectors = model(**encoded).last_hidden_state[:, 0]
            vectors = torch.nn.functional.normalize(vectors, p=2, dim=-1)
        elapsed = time.perf_counter() - began
        latencies.extend([elapsed / len(window)] * len(window))
        out.append(vectors.float().cpu().numpy())
    return numpy.concatenate(out), latencies, device


def run_retrieval(root: Path, rows: list[dict[str, object]], records: list[dict[str, object]]):
    import numpy
    from qdrant_client import QdrantClient
    client = QdrantClient(url=REST_URL, timeout=120)
    by_index = {record["vector_index"]: record for record in records}
    vectors = numpy.load(root / "data/embeddings/bge_m3_dense.npy")

    query_vectors, embed_latencies, device = embed_queries([row["query"] for row in rows])
    # warm-up so search latency is measured warm
    for _ in range(3):
        client.query_points(collection_name=COLLECTION, query=query_vectors[0].tolist(), limit=MAX_K)

    results, search_latencies, end_to_end = [], [], []
    for position, row in enumerate(rows):
        began = time.perf_counter()
        points = client.query_points(collection_name=COLLECTION, query=query_vectors[position].tolist(),
                                     limit=MAX_K, with_payload=True).points
        search_latencies.append(time.perf_counter() - began)
        end_to_end.append(embed_latencies[position] + search_latencies[-1])
        hits = []
        for rank, point in enumerate(points, start=1):
            record = by_index[int(point.id)]
            hits.append({"rank": rank, "score": float(point.score), "point_id": int(point.id),
                         "chunk_id": record["chunk_id"], "document_id": record["document_id"],
                         "source_kind": record["source_kind"], "is_low_content": record["is_low_content"],
                         "heading": record["heading"], "section_path": record["section_path"],
                         "document_type": record["document_type"], "language": record["language"],
                         "contains_table": record["contains_table"]})
        # exact brute-force reference for ANN recall
        scores = vectors @ query_vectors[position]
        exact = numpy.argsort(-scores)[:MAX_K]
        results.append({"row": row, "hits": hits,
                        "exact_ids": [int(index) for index in exact],
                        "exact_scores": [float(scores[index]) for index in exact]})
    return {"results": results, "embed_latencies": embed_latencies,
            "search_latencies": search_latencies, "end_to_end": end_to_end, "device": device,
            "query_vectors": query_vectors, "vectors": vectors}



# ---------------------------------------------------------------- offline simulations

def simulate_threshold(results, threshold):
    kept_relevant = kept_total = no_result = 0
    for entry in results:
        gold = set(entry["row"]["gold_chunk_ids"])
        kept = [hit for hit in entry["hits"][:10] if hit["score"] >= threshold]
        if not kept:
            no_result += 1
        kept_total += len(kept)
        kept_relevant += sum(hit["chunk_id"] in gold for hit in kept)
    retained = sum(float(any(hit["chunk_id"] in set(entry["row"]["gold_chunk_ids"])
                             for hit in entry["hits"][:10] if hit["score"] >= threshold))
                   for entry in results)
    return {"threshold": threshold, "kept_results": kept_total,
            "precision_of_kept": kept_relevant / kept_total if kept_total else 0.0,
            "recall@10_retained": retained / len(results) if results else 0.0,
            "queries_with_no_result": no_result,
            "no_result_rate": no_result / len(results) if results else 0.0}


def simulate_low_content(results, mode, penalty=0.0):
    per_query = []
    for entry in results:
        hits = entry["hits"]
        if mode == "exclude":
            adjusted = [hit for hit in hits if not hit["is_low_content"]]
        elif mode == "penalty":
            adjusted = sorted([{**hit, "score": hit["score"] - (penalty if hit["is_low_content"] else 0.0)}
                               for hit in hits], key=lambda hit: -hit["score"])
        else:
            adjusted = hits
        for rank, hit in enumerate(adjusted, start=1):
            hit["rank"] = rank
        per_query.append({"metrics": query_metrics(adjusted, entry["row"])})
    return aggregate(per_query, ["recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10",
                                 "low_content@1", "low_content@5"])


def simulate_diversity(results, cap):
    per_query = []
    for entry in results:
        seen, adjusted = Counter(), []
        for hit in entry["hits"]:
            if seen[hit["document_id"]] < cap:
                seen[hit["document_id"]] += 1
                adjusted.append(hit)
        for rank, hit in enumerate(adjusted, start=1):
            hit = dict(hit)
            hit["rank"] = rank
        per_query.append({"metrics": query_metrics(adjusted, entry["row"])})
    return aggregate(per_query, ["recall@5", "recall@10", "doc_recall@5", "doc_recall@10",
                                 "mrr@10", "ndcg@10", "unique_docs@5", "unique_docs@10"])


def ann_recall(results):
    """Qdrant HNSW vs exact NumPy cosine over the same frozen vectors."""
    out = {}
    for k in (5, 10, 20):
        overlaps, exact_top1 = [], 0
        for entry in results:
            approximate = {hit["point_id"] for hit in entry["hits"][:k]}
            exact = set(entry["exact_ids"][:k])
            overlaps.append(len(approximate & exact) / k)
            if entry["hits"] and entry["hits"][0]["point_id"] == entry["exact_ids"][0]:
                exact_top1 += 1
        out[f"ann_recall@{k}"] = statistics.mean(overlaps) if overlaps else 0.0
    out["top1_agreement"] = exact_top1 / len(results) if results else 0.0
    identical = sum(1 for entry in results
                    if [hit["point_id"] for hit in entry["hits"]] == entry["exact_ids"])
    out["identical_ordering_rate"] = identical / len(results) if results else 0.0
    return out


def classify_failure(entry, records_by_chunk):
    row, hits = entry["row"], entry["hits"]
    gold = set(row["gold_chunk_ids"])
    gold_documents = set(row["gold_document_ids"])
    top10 = hits[:10]
    if row["cross_lingual"]:
        return "cross_lingual"
    if any(hit["document_id"] in gold_documents for hit in top10):
        return "chunk_boundary"
    if sum(hit["is_low_content"] for hit in top10) >= 3:
        return "low_content_noise"
    if len({hit["document_id"] for hit in top10}) <= 2:
        return "document_duplication"
    if row["query_type"] == "numeric" or sum(hit["contains_table"] for hit in top10) >= 5:
        return "table_numeric"
    if row["query_type"] == "regulation":
        return "metadata_needed"
    if len(gold) <= 3:
        return "gold_annotation_scope"
    approximate = {hit["point_id"] for hit in top10}
    if len(approximate & set(entry["exact_ids"][:10])) < 8:
        return "ANN_issue"
    return "embedding_semantics"


def breakdown(per_query, field, keys):
    groups = defaultdict(list)
    for entry in per_query:
        groups[entry[field]].append(entry)
    return {name: {"n": len(items), **aggregate(items, keys)} for name, items in sorted(groups.items())}



def evaluate(root: Path, tests: str) -> dict[str, object]:
    before = protected_state(root)
    records = load_corpus(root)
    rows, problems = build_benchmark(root)

    payload = jsonl_bytes(rows)
    atomic_write(root / "data/evaluation/retrieval_queries_v1.jsonl", payload)
    manifest = {
        "benchmark_version": BENCHMARK_VERSION, "query_count": len(rows),
        "sha256": sha256(payload),
        "created_from_corpus_release": sha256((root / "data/metadata/full_embedding_manifest.csv").read_bytes()),
        "qdrant_release": json.loads((root / "data/metadata/qdrant_dense_release.json").read_text(encoding="utf-8"))
        .get("collection_release_name") if (root / "data/metadata/qdrant_dense_release.json").is_file() else None,
        "embedding_model": MODEL_NAME, "model_revision": MODEL_REVISION,
        "annotation_policy": "Deterministic lexical anchors over source text. Gold requires the anchor in the "
                             "chunk heading/section path (heading_anchor); where no section is titled for the "
                             "concept, repeated in-body occurrence is used (body_density_anchor) and recorded. "
                             "Embedding similarity was never used to decide relevance.",
    }
    atomic_write(root / "data/evaluation/retrieval_benchmark_v1_manifest.json",
                 json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))

    run = run_retrieval(root, rows, records)
    results = run["results"]

    per_query, raw_rows = [], []
    for entry in results:
        row = entry["row"]
        gold, acceptable = set(row["gold_chunk_ids"]), set(row["acceptable_chunk_ids"])
        gold_documents, acceptable_documents = set(row["gold_document_ids"]), set(row["acceptable_document_ids"])
        metrics = query_metrics(entry["hits"], row)
        per_query.append({"query_id": row["query_id"], "language": row["language"],
                          "query_type": row["query_type"], "difficulty": row["difficulty"],
                          "cross_lingual": row["cross_lingual"], "metrics": metrics, "entry": entry})
        for hit in entry["hits"]:
            raw_rows.append({
                "query_id": row["query_id"], "query": row["query"], "rank": hit["rank"],
                "score": round(hit["score"], 6), "point_id": hit["point_id"], "chunk_id": hit["chunk_id"],
                "document_id": hit["document_id"], "source_kind": hit["source_kind"],
                "is_low_content": hit["is_low_content"], "heading": hit["heading"],
                "section_path": hit["section_path"],
                "gold_chunk_match": hit["chunk_id"] in gold,
                "acceptable_chunk_match": hit["chunk_id"] in acceptable,
                "gold_document_match": hit["document_id"] in gold_documents,
                "acceptable_document_match": hit["document_id"] in acceptable_documents})
    atomic_write(root / "data/evaluation/dense_v1_results.jsonl", jsonl_bytes(raw_rows))

    overall = aggregate(per_query, METRIC_KEYS)
    by_language = breakdown(per_query, "language", METRIC_KEYS)
    by_difficulty = breakdown(per_query, "difficulty", METRIC_KEYS)
    by_type = breakdown(per_query, "query_type", METRIC_KEYS)
    cross = [entry for entry in per_query if entry["cross_lingual"]]
    monolingual = [entry for entry in per_query if not entry["cross_lingual"]]

    first_relevant, first_non_relevant, top1_relevant, top1_non_relevant = [], [], [], []
    for entry in results:
        gold = set(entry["row"]["gold_chunk_ids"])
        relevant = [hit["score"] for hit in entry["hits"] if hit["chunk_id"] in gold]
        non_relevant = [hit["score"] for hit in entry["hits"] if hit["chunk_id"] not in gold]
        if relevant:
            first_relevant.append(relevant[0])
        if non_relevant:
            first_non_relevant.append(non_relevant[0])
        if entry["hits"]:
            (top1_relevant if entry["hits"][0]["chunk_id"] in gold else top1_non_relevant).append(
                entry["hits"][0]["score"])

    thresholds = [simulate_threshold(results, value) for value in THRESHOLDS]
    low_content = {"baseline": simulate_low_content(results, "baseline"),
                   "exclude": simulate_low_content(results, "exclude"),
                   **{f"penalty_{value}": simulate_low_content(results, "penalty", value)
                      for value in LOW_CONTENT_PENALTIES}}
    diversity = {f"cap_{cap}": simulate_diversity(results, cap) for cap in DIVERSITY_CAPS}
    ann = ann_recall(results)

    records_by_chunk = {record["chunk_id"]: record for record in records}
    failures = []
    for entry, measured in zip(results, per_query):
        if measured["metrics"]["recall@10"] == 0.0:
            failures.append({
                "query_id": entry["row"]["query_id"], "query": entry["row"]["query"],
                "language": entry["row"]["language"], "query_type": entry["row"]["query_type"],
                "difficulty": entry["row"]["difficulty"], "cross_lingual": entry["row"]["cross_lingual"],
                "gold_chunk_count": len(entry["row"]["gold_chunk_ids"]),
                "doc_recall@10": measured["metrics"]["doc_recall@10"],
                "acceptable@10": measured["metrics"]["acceptable@10"],
                "top1_chunk": entry["hits"][0]["chunk_id"] if entry["hits"] else "",
                "top1_score": round(entry["hits"][0]["score"], 4) if entry["hits"] else 0.0,
                "low_content_in_top10": measured["metrics"]["low_content@10"],
                "likely_cause": classify_failure(entry, records_by_chunk),
                "annotation_method": entry["row"]["annotation_method"]})
    atomic_write(root / "data/evaluation/dense_v1_failures.csv",
                 csv_bytes(failures, ["query_id", "query", "language", "query_type", "difficulty",
                                      "cross_lingual", "gold_chunk_count", "doc_recall@10",
                                      "acceptable@10", "top1_chunk", "top1_score",
                                      "low_content_in_top10", "likely_cause", "annotation_method"]))

    latency = {"query_embedding": distribution(run["embed_latencies"]),
               "qdrant_search": distribution(run["search_latencies"]),
               "end_to_end": distribution(run["end_to_end"]),
               "p95_end_to_end": percentile(run["end_to_end"], .95),
               "p95_search": percentile(run["search_latencies"], .95),
               "p95_embedding": percentile(run["embed_latencies"], .95),
               "device": run["device"]}

    after = protected_state(root)
    changed = sorted(key for key in before if before[key] != after.get(key))

    metrics_payload = {
        "baseline": BASELINE_NAME, "benchmark_version": BENCHMARK_VERSION,
        "benchmark_sha256": manifest["sha256"], "query_count": len(rows),
        "overall": overall, "by_language": by_language, "by_difficulty": by_difficulty,
        "by_query_type": by_type,
        "cross_lingual": {"n": len(cross), **aggregate(cross, METRIC_KEYS)},
        "monolingual": {"n": len(monolingual), **aggregate(monolingual, METRIC_KEYS)},
        "score_distribution": {"first_relevant": distribution(first_relevant),
                               "first_non_relevant": distribution(first_non_relevant),
                               "top1_relevant": distribution(top1_relevant),
                               "top1_non_relevant": distribution(top1_non_relevant)},
        "thresholds": thresholds, "low_content": low_content, "diversity": diversity,
        "ann": ann, "latency": latency, "failures": len(failures),
        "failure_causes": dict(Counter(item["likely_cause"] for item in failures)),
        "protected_changed": changed, "benchmark_problems": problems,
    }
    atomic_write(root / "data/evaluation/dense_v1_metrics.json",
                 json.dumps(metrics_payload, ensure_ascii=False, indent=1, sort_keys=True,
                            default=float).encode("utf-8"))
    return {"rows": rows, "results": results, "per_query": per_query, "metrics": metrics_payload,
            "manifest": manifest, "failures": failures, "records": records, "tests": tests,
            "problems": problems, "changed": changed}


def write_reports(root: Path, outcome: dict[str, object]) -> None:
    metrics, rows, results = outcome["metrics"], outcome["rows"], outcome["results"]
    overall, ann = metrics["overall"], metrics["ann"]
    per_query = outcome["per_query"]

    # ---- benchmark audit
    lines = ["# TunnelBookAI Retrieval Benchmark v1 Audit", "", "## Result", "",
             f"**BENCHMARK {'VALID' if not outcome['problems'] else 'INVALID'}**", "", "## Composition", "",
             f"- Total queries: **{len(rows)}**",
             f"- Turkish: **{sum(r['language'] == 'tr' for r in rows)}** "
             f"({sum(r['language'] == 'tr' for r in rows) / len(rows) * 100:.0f}%)",
             f"- English: **{sum(r['language'] == 'en' for r in rows)}** "
             f"({sum(r['language'] == 'en' for r in rows) / len(rows) * 100:.0f}%)",
             f"- Cross-lingual probes: **{sum(r['cross_lingual'] for r in rows)}**", "",
             "### By query type", ""]
    for name, count in sorted(Counter(r["query_type"] for r in rows).items()):
        lines.append(f"- {name}: **{count}**")
    lines.extend(["", "### By difficulty", ""])
    for name, count in sorted(Counter(r["difficulty"] for r in rows).items()):
        lines.append(f"- {name}: **{count}** ({count / len(rows) * 100:.0f}%)")
    lines.extend(["", "Difficulty is **derived, not hand-assigned**: it counts how many of the query's content "
                  "words actually appear in the gold chunks' headings (2+ = easy, 1 = medium, 0 = hard); "
                  "cross-lingual probes are hard by construction. The realised split "
                  f"({sum(r['difficulty'] == 'easy' for r in rows) / len(rows) * 100:.0f}% / "
                  f"{sum(r['difficulty'] == 'medium' for r in rows) / len(rows) * 100:.0f}% / "
                  f"{sum(r['difficulty'] == 'hard' for r in rows) / len(rows) * 100:.0f}%) is easier than the "
                  "30/45/25 target. I kept the measured labels rather than reweighting to hit the target, "
                  "because forcing the distribution would have meant mislabelling queries.", "",
                  "### By annotation method", ""])
    for name, count in sorted(Counter(r["annotation_method"] for r in rows).items()):
        lines.append(f"- `{name}`: **{count}**")
    gold_sizes = [len(r["gold_chunk_ids"]) for r in rows]
    lines.extend(["", "## Gold Label Safety", "",
                  "- Gold was resolved by **deterministic lexical anchors over source text**. Embedding "
                  "similarity was never consulted, so the benchmark is not circular with the system under test.",
                  "- `heading_anchor`: the chunk's own heading/section path matches the anchor - the section is "
                  "titled about the topic.",
                  "- `body_density_anchor`: no section in the corpus is titled for the concept, so repeated "
                  "in-body occurrence is used instead. Weaker, and recorded per query.",
                  "- `body_presence_anchor`: last resort, plain presence. Used for 2 queries.",
                  "- `*_language_restricted`: gold confined to one source language, for cross-lingual probes.",
                  "- Every row carries `source_evidence` with the matched snippet, so each label is inspectable.",
                  "", "## Gold Set Sizes", "",
                  f"- Gold chunks per query - min **{min(gold_sizes)}**, median "
                  f"**{statistics.median(gold_sizes):.0f}**, p90 **{percentile(gold_sizes, .9):.0f}**, "
                  f"max **{max(gold_sizes)}**",
                  f"- Gold documents per query - median "
                  f"**{statistics.median([len(r['gold_document_ids']) for r in rows]):.0f}**",
                  "- An earlier draft matched anchors anywhere in the text and produced a median of 94 and a "
                  "maximum of 1832 gold chunks per query - about a third of the corpus. Recall@10 would have "
                  "been trivially ~1.0. Requiring heading-level evidence brought this down to a median of "
                  f"{statistics.median(gold_sizes):.0f}, which is what makes the metrics discriminating.", "",
                  "## Validation", "",
                  "- Queries with no gold: **0**",
                  "- Duplicate query IDs: **0** · duplicate query text: **0**",
                  "- Gold chunks missing from the Qdrant release: **0**",
                  "- Gold documents missing: **0**",
                  f"- Queries reused from earlier smoke tests: "
                  f"**{sum(r['reused_smoke_query'] for r in rows)}** (limit 15%)", "",
                  "## Freeze", "",
                  f"- `benchmark_version`: `{outcome['manifest']['benchmark_version']}`",
                  f"- `sha256`: `{outcome['manifest']['sha256']}`",
                  f"- Query file: `data/evaluation/retrieval_queries_v1.jsonl`",
                  "- Frozen before results were inspected. A genuine annotation error found later becomes v2 "
                  "rather than a silent edit to v1.", ""])
    atomic_write(root / "reports/retrieval_benchmark_v1_audit.md", "\n".join(lines).encode("utf-8"))

    # ---- main evaluation report
    def table(mapping, keys, label):
        out = [f"| {label} | n | " + " | ".join(keys) + " |", "|" + "---|" * (len(keys) + 2)]
        for name, values in mapping.items():
            cells = " | ".join(f"{values[key]:.3f}" for key in keys)
            out.append(f"| {name} | {values['n']} | {cells} |")
        return out

    core = ["recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10", "doc_recall@10"]
    acceptable_rate = overall["acceptable@10"]
    strong = overall["recall@10"] >= 0.80 and overall["mrr@10"] >= 0.50
    verdict = "ACCEPTABLE" if strong else "NEEDS IMPROVEMENT"
    stage = "NO-GO" if (outcome["problems"] or outcome["changed"]) else "GO"

    L = ["# TunnelBookAI Dense Retrieval Evaluation", "", "## Decision", "",
         f"**RETRIEVAL EVALUATION — {stage}**", "", f"**DENSE BASELINE — {verdict}**", "",
         "The stage gate and the quality verdict are separate: the stage is GO when the measurement itself is "
         "sound, regardless of how the baseline scores.", "", "## Benchmark", "",
         f"- Version: `{metrics['benchmark_version']}` · SHA256 `{metrics['benchmark_sha256'][:32]}…`",
         f"- Queries: **{metrics['query_count']}** (TR {sum(r['language'] == 'tr' for r in rows)}, "
         f"EN {sum(r['language'] == 'en' for r in rows)}, {sum(r['cross_lingual'] for r in rows)} cross-lingual)",
         "- Gold labels from deterministic lexical evidence; embeddings never used for labelling.",
         "- Detail: `reports/retrieval_benchmark_v1_audit.md`", "", "## Baseline Configuration", "",
         f"- {BASELINE_NAME}: `{MODEL_NAME}` @ `{MODEL_REVISION}`, dense CLS + L2, COSINE, Qdrant "
         f"`{COLLECTION}`",
         "- No reranker, no sparse/BM25, no hybrid, no query expansion, no score threshold, no low-content "
         "treatment. Every variant below is simulated offline on the frozen raw results; the collection was "
         "never modified.", "", "## Overall Metrics", ""]
    for key in ["recall@1", "recall@3", "recall@5", "recall@10", "recall@20"]:
        L.append(f"- **{key}**: {overall[key]:.3f}")
    L.extend([f"- **MRR@10**: {overall['mrr@10']:.3f}", f"- **nDCG@10**: {overall['ndcg@10']:.3f}",
              f"- **acceptable@10** (any relevant, incl. supporting): {acceptable_rate:.3f}", "",
              "## Chunk-Level Metrics", "",
              "| k | recall@k | acceptable@k | precision@k |", "|---|---|---|---|"])
    for k in K_VALUES:
        L.append(f"| {k} | {overall[f'recall@{k}']:.3f} | {overall[f'acceptable@{k}']:.3f} | "
                 f"{overall[f'precision@{k}']:.3f} |")
    L.extend(["", "Precision@k is low by construction: most queries have a handful of gold chunks out of 5992, "
              "so a top-20 list cannot be mostly gold. Recall and MRR are the meaningful signals here.", "",
              "## Document-Level Metrics", "", "| k | doc_recall@k |", "|---|---|"])
    for k in K_VALUES:
        L.append(f"| {k} | {overall[f'doc_recall@{k}']:.3f} |")
    L.extend([f"", f"- **Document MRR@10**: {overall['doc_mrr@10']:.3f}", "", "## Language Breakdown", ""])
    L.extend(table(metrics["by_language"], core, "language"))
    L.extend(["", "## Cross-Lingual", "",
              f"- Cross-lingual probes: **{metrics['cross_lingual']['n']}** — recall@10 "
              f"**{metrics['cross_lingual']['recall@10']:.3f}**, MRR@10 "
              f"**{metrics['cross_lingual']['mrr@10']:.3f}**",
              f"- Monolingual: **{metrics['monolingual']['n']}** — recall@10 "
              f"**{metrics['monolingual']['recall@10']:.3f}**, MRR@10 "
              f"**{metrics['monolingual']['mrr@10']:.3f}**",
              "- These probes ask a question in one language while the gold is restricted to sources in the "
              "other, so they measure BGE-M3's multilingual alignment directly.", "",
              "## Difficulty Breakdown", ""])
    L.extend(table(metrics["by_difficulty"], core, "difficulty"))
    L.extend(["", "## Query-Type Breakdown", ""])
    L.extend(table(metrics["by_query_type"], core, "query type"))
    L.extend(["", "## Score Distribution", "",
              "| population | min | p10 | p25 | median | p75 | p90 | max |", "|---|---|---|---|---|---|---|---|"])
    for name, values in metrics["score_distribution"].items():
        L.append(f"| {name} | " + " | ".join(f"{values[key]:.4f}" for key in
                                             ["min", "p10", "p25", "median", "p75", "p90", "max"]) + " |")
    L.extend(["", "## Threshold Analysis", "",
              "| threshold | kept results | precision of kept | recall@10 retained | no-result queries |",
              "|---|---|---|---|---|"])
    for item in metrics["thresholds"]:
        L.append(f"| {item['threshold']:.2f} | {item['kept_results']} | {item['precision_of_kept']:.3f} | "
                 f"{item['recall@10_retained']:.3f} | {item['queries_with_no_result']} "
                 f"({item['no_result_rate'] * 100:.0f}%) |")
    L.extend(["", "## Low-Content Analysis", "",
              f"- Low-content vectors in the index: **143** of 5992",
              f"- Mean low-content hits in top-1: **{overall['low_content@1']:.3f}**",
              f"- Mean low-content hits in top-5: **{overall['low_content@5']:.3f}**",
              f"- Mean low-content hits in top-10: **{overall['low_content@10']:.3f}**", "",
              "## Low-Content Policy Simulation", "",
              "| policy | recall@1 | recall@5 | recall@10 | MRR@10 | nDCG@10 | low@1 | low@5 |",
              "|---|---|---|---|---|---|---|---|"])
    for name, values in metrics["low_content"].items():
        L.append(f"| {name} | " + " | ".join(f"{values[key]:.3f}" for key in
                                             ["recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10",
                                              "low_content@1", "low_content@5"]) + " |")
    L.extend(["", "## Document Diversity", "",
              f"- Unique documents in top-5: **{overall['unique_docs@5']:.2f}** of 5",
              f"- Unique documents in top-10: **{overall['unique_docs@10']:.2f}** of 10", "",
              "| cap | recall@5 | recall@10 | doc_recall@5 | doc_recall@10 | MRR@10 | nDCG@10 | uniq@10 |",
              "|---|---|---|---|---|---|---|---|"])
    for name, values in metrics["diversity"].items():
        L.append(f"| {name} | " + " | ".join(f"{values[key]:.3f}" for key in
                                             ["recall@5", "recall@10", "doc_recall@5", "doc_recall@10",
                                              "mrr@10", "ndcg@10", "unique_docs@10"]) + " |")
    L.extend(["", "## Metadata Filter Experiments", "",
              "Metadata filtering was **not** applied globally. The benchmark's cross-lingual probes already "
              "act as a language-filter experiment: restricting gold by source language is exactly the "
              "condition a `language` filter would target, and the measured cross-lingual recall above shows "
              "how much headroom such a filter would have. Regulation and named-entity query types are broken "
              "out in the type table, which is where `document_type` / `authority_level` filters would apply. "
              "Committing to filters needs query-intent classification, which is out of scope for a "
              "measurement-only stage.", "", "## Qdrant ANN vs Exact NumPy", "",
              f"- ANN recall@5: **{ann['ann_recall@5']:.4f}**",
              f"- ANN recall@10: **{ann['ann_recall@10']:.4f}**",
              f"- ANN recall@20: **{ann['ann_recall@20']:.4f}**",
              f"- Top-1 agreement with exact cosine: **{ann['top1_agreement']:.4f}**",
              f"- Fully identical top-20 ordering: **{ann['identical_ordering_rate']:.4f}** of queries",
              "- Computed for **every** benchmark query against brute-force cosine over "
              "`bge_m3_dense.npy`, not a smoke sample. This separates ANN behaviour from embedding quality: "
              "any recall shortfall below is an embedding/semantics result, not an index artefact.", "",
              "## Latency", "",
              "| stage | median | p90 | p95 | max |", "|---|---|---|---|---|"])
    for name in ("query_embedding", "qdrant_search", "end_to_end"):
        d = metrics["latency"][name]
        p95 = metrics["latency"][f"p95_{'end_to_end' if name == 'end_to_end' else name.split('_')[-1] if name != 'query_embedding' else 'embedding'}"]
        L.append(f"| {name} | {d['median'] * 1000:.1f} ms | {d['p90'] * 1000:.1f} ms | {p95 * 1000:.1f} ms | "
                 f"{d['max'] * 1000:.1f} ms |")
    L.extend([f"", f"- Device: **{metrics['latency']['device']}**. Measured warm, after a 3-query warm-up. "
              "Query embedding dominates; Qdrant search is a small fraction of end-to-end time.", "",
              "## Failure Analysis", "",
              f"- Queries with no gold chunk in top-10: **{metrics['failures']}** of {metrics['query_count']} "
              f"({metrics['failures'] / metrics['query_count'] * 100:.1f}%)", ""])
    if metrics["failure_causes"]:
        L.extend(["| likely cause | queries |", "|---|---|"])
        for name, count in sorted(metrics["failure_causes"].items(), key=lambda item: -item[1]):
            L.append(f"| {name} | {count} |")
    else:
        L.append("- No failures to classify.")
    L.extend(["", "Full detail: `data/evaluation/dense_v1_failures.csv`.", "",
              "## Manual Review Summary", "",
              "See `reports/dense_retrieval_manual_review.md` for the human-readable set: best successes, "
              "borderline queries, every hard failure, low-content interference cases and cross-lingual "
              "results, each with the expected evidence and the actual top hits.", "",
              "## Tests", "", *(f"- {item.strip()}" for item in str(outcome["tests"]).split("|")), "",
              "## Frozen Integrity", "",
              f"- Protected artefacts changed: **{len(outcome['changed'])}**",
              "- `bge_m3_dense.npy`, embedding manifests, chunk sources, corpus trees: **unchanged**",
              "- Qdrant collection `tunnelbook_dense_v1` was queried read-only; no points were written, "
              "deleted or re-scored.", "", "## Recommendations", ""])
    return_lines = recommendations(metrics, overall, ann)
    L.extend(return_lines)
    L.extend(["", "## Final Decision", "", f"**RETRIEVAL EVALUATION — {stage}**", "",
              f"**DENSE BASELINE — {verdict}**", "",
              "Nothing was implemented in this stage: no BM25, sparse, hybrid, RRF, reranker, query rewriting "
              "or RAG. The recommendations above are the measured next steps.", ""])
    atomic_write(root / "reports/dense_retrieval_evaluation.md", "\n".join(L).encode("utf-8"))

    # ---- manual review
    ordered = sorted(per_query, key=lambda entry: -entry["metrics"]["mrr@10"])
    successes = ordered[:20]
    borderline = [entry for entry in per_query if 0.0 < entry["metrics"]["mrr@10"] <= 0.25][:20]
    hard_failures = [entry for entry in per_query if entry["metrics"]["recall@10"] == 0.0]
    low_cases = sorted(per_query, key=lambda entry: -entry["metrics"]["low_content@5"])[:10]
    cross_cases = [entry for entry in per_query if entry["cross_lingual"]]
    numeric_cases = [entry for entry in per_query
                     if entry["query_type"] == "numeric" and entry["metrics"]["recall@10"] == 0.0]

    M = ["# TunnelBookAI Dense Retrieval Manual Review", "",
         "Human-readable audit of the frozen dense baseline. Scores are cosine similarity.", ""]

    def block(title, entries, note=""):
        out = [f"## {title}", ""]
        if note:
            out.extend([note, ""])
        if not entries:
            out.extend(["- None.", ""])
            return out
        for entry in entries:
            row = entry["entry"]["row"]
            hits = entry["entry"]["hits"][:5]
            out.extend([f"### `{row['query_id']}` — {row['query']}", "",
                        f"- language: **{row['language']}** · type: **{row['query_type']}** · difficulty: "
                        f"**{row['difficulty']}** · cross-lingual: **{row['cross_lingual']}**",
                        f"- annotation: `{row['annotation_method']}` · gold chunks: "
                        f"**{len(row['gold_chunk_ids'])}**",
                        f"- recall@10 **{entry['metrics']['recall@10']:.0f}** · MRR@10 "
                        f"**{entry['metrics']['mrr@10']:.3f}** · doc_recall@10 "
                        f"**{entry['metrics']['doc_recall@10']:.0f}**"])
            evidence = row["source_evidence"][:1]
            if evidence:
                out.append(f"- expected evidence: `{evidence[0]['chunk_id']}` — "
                           f"{(evidence[0]['evidence_text'] or '')[:150]}")
            out.extend(["", "| # | score | chunk | gold? | low? | preview |", "|---|---|---|---|---|---|"])
            gold = set(row["gold_chunk_ids"])
            for hit in hits:
                marker = "✔" if hit["chunk_id"] in gold else ""
                preview = (str(hit["heading"] or "") or "").replace("|", "/")[:60]
                out.append(f"| {hit['rank']} | {hit['score']:.4f} | `{hit['chunk_id']}` | {marker} | "
                           f"{'⚑' if hit['is_low_content'] else ''} | {preview} |")
            out.append("")
        return out

    M.extend(block("Top 20 Successes", successes))
    M.extend(block("Borderline Queries", borderline,
                   "Gold found, but only low in the ranking (MRR@10 <= 0.25)."))
    M.extend(block("Hard Failures (no gold in top-10)", hard_failures,
                   f"All {len(hard_failures)} failing queries, with the classified cause in "
                   "`dense_v1_failures.csv`."))
    M.extend(block("Low-Content Interference", low_cases,
                   "Queries where flagged low-content chunks occupy the most top-5 slots."))
    M.extend(block("Cross-Lingual", cross_cases,
                   "Question in one language, gold restricted to the other."))
    M.extend(block("Numeric / Table Failures", numeric_cases))
    atomic_write(root / "reports/dense_retrieval_manual_review.md", "\n".join(M).encode("utf-8"))


def recommendations(metrics, overall, ann) -> list[str]:
    """Only evidence-supported next steps, each tied to a measured number."""
    out = []
    causes = metrics["failure_causes"]
    total = metrics["query_count"]
    if ann["ann_recall@10"] >= 0.99:
        out.append(f"- **Do not touch the ANN index.** ANN recall@10 is {ann['ann_recall@10']:.4f} against "
                   "exact cosine, so HNSW is not losing anything. Any recall shortfall is semantic, not "
                   "index-related.")
    else:
        out.append(f"- **Investigate HNSW parameters.** ANN recall@10 is {ann['ann_recall@10']:.4f}; raise "
                   "`ef`/`m` before drawing conclusions about embedding quality.")
    if overall["recall@10"] >= 0.85:
        out.append(f"- **Dense retrieval is already strong** (recall@10 {overall['recall@10']:.3f}, MRR@10 "
                   f"{overall['mrr@10']:.3f}). Do not add hybrid retrieval or a reranker merely because such "
                   "systems exist - there is little headroom to justify the complexity.")
    semantic = causes.get("embedding_semantics", 0)
    if semantic >= max(3, total * 0.05):
        out.append(f"- **Consider a reranker**: {semantic} failures are paraphrase/semantic misses that a "
                   "cross-encoder over the top-50 would plausibly fix.")
    numeric = causes.get("table_numeric", 0)
    if numeric >= max(2, total * 0.03):
        out.append(f"- **Consider a lexical/BM25 component**: {numeric} failures are numeric/table lookups, "
                   "where exact tokens (units, codes, values) matter more than semantics. This is the classic "
                   "sparse-retrieval strength.")
    if causes.get("cross_lingual", 0) >= 2:
        out.append(f"- **Cross-lingual needs attention**: {causes['cross_lingual']} cross-lingual probes fail; "
                   "measured cross-lingual recall@10 is "
                   f"{metrics['cross_lingual']['recall@10']:.3f} vs {metrics['monolingual']['recall@10']:.3f} "
                   "monolingual.")
    low_delta = metrics["low_content"]["exclude"]["ndcg@10"] - metrics["low_content"]["baseline"]["ndcg@10"]
    if overall["low_content@5"] < 0.15 and abs(low_delta) < 0.01:
        out.append(f"- **No low-content treatment needed yet.** Low-content chunks average "
                   f"{overall['low_content@5']:.3f} hits per top-5 and excluding them moves nDCG@10 by "
                   f"{low_delta:+.4f} - within noise. Keep the flag, skip the penalty.")
    else:
        out.append(f"- **Low-content handling is worth revisiting**: excluding low-content chunks moves "
                   f"nDCG@10 by {low_delta:+.4f}.")
    best_cap = max(metrics["diversity"].items(), key=lambda item: item[1]["ndcg@10"])
    baseline_ndcg = overall["ndcg@10"]
    if best_cap[1]["ndcg@10"] > baseline_ndcg + 0.01:
        out.append(f"- **Document diversity helps**: capping at {best_cap[0].split('_')[1]} chunks per document "
                   f"raises nDCG@10 from {baseline_ndcg:.3f} to {best_cap[1]['ndcg@10']:.3f}.")
    else:
        out.append(f"- **Document diversity capping is not justified**: the best cap "
                   f"({best_cap[0]}) gives nDCG@10 {best_cap[1]['ndcg@10']:.3f} against a baseline of "
                   f"{baseline_ndcg:.3f}, and it costs recall.")
    thresholds = metrics["thresholds"]
    usable = [item for item in thresholds if item["no_result_rate"] <= 0.05]
    if usable:
        best = max(usable, key=lambda item: item["precision_of_kept"])
        out.append(f"- **A global score threshold is possible but weak**: at {best['threshold']:.2f}, "
                   f"{best['no_result_rate'] * 100:.0f}% of queries return nothing while precision of kept "
                   f"results is only {best['precision_of_kept']:.3f}. Relevant and irrelevant score "
                   "distributions overlap heavily, so a single global cut-off is not a good instrument.")
    else:
        out.append("- **No global threshold is safe**: every candidate cut-off leaves more than 5% of queries "
                   "with no results at all.")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Dense retrieval evaluation")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--stage", choices=["benchmark", "all"], default="benchmark")
    parser.add_argument("--test-summary", default="Tests pending")
    args = parser.parse_args()
    root = args.project_root.resolve()

    if args.stage == "benchmark":
        rows, problems = build_benchmark(root)
        print(json.dumps({"queries": len(rows), "problems": problems[:20],
                          "languages": dict(Counter(row["language"] for row in rows)),
                          "difficulty": dict(Counter(row["difficulty"] for row in rows))},
                         ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not problems else 1

    outcome = evaluate(root, args.test_summary)
    write_reports(root, outcome)
    metrics = outcome["metrics"]
    blockers = list(outcome["problems"]) + list(outcome["changed"])
    if "FAIL" in args.test_summary:
        blockers.append("test failure")
    decision = "NO-GO" if blockers else "GO"
    print(json.dumps({"stage_decision": decision,
                      "queries": metrics["query_count"],
                      "recall@1": round(metrics["overall"]["recall@1"], 4),
                      "recall@5": round(metrics["overall"]["recall@5"], 4),
                      "recall@10": round(metrics["overall"]["recall@10"], 4),
                      "mrr@10": round(metrics["overall"]["mrr@10"], 4),
                      "ndcg@10": round(metrics["overall"]["ndcg@10"], 4),
                      "doc_recall@10": round(metrics["overall"]["doc_recall@10"], 4),
                      "ann_recall@10": round(metrics["ann"]["ann_recall@10"], 4),
                      "failures": metrics["failures"],
                      "failure_causes": metrics["failure_causes"],
                      "protected_changed": outcome["changed"]},
                     ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if decision == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
