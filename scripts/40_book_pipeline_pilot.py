"""Three-section pilot of the book-writing pipeline. Evidence preparation only - no prose.

Sections are chosen for different evidence patterns: concept-heavy, numeric/specification-heavy,
and multi-source comparative (where conflicting sources are plausible). Every research question is
executed through the frozen production grounded generator; nothing bypasses it.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "data/book"


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bp = _load("book_pipeline", "scripts/39_book_writing_pipeline.py")
production = bp.production

BOOK_ID = "BOOK-TUNNEL-001"

PROJECT = bp.BookProject(
    book_id=BOOK_ID,
    working_title="Karayolu Tünelleri: Tasarım, Yapım ve İşletme",
    language="tr", audience="inşaat mühendisleri ve tünel uygulayıcıları",
    technical_level="advanced_practitioner",
    purpose="Kurumsal tünel bilgi birikimini kanıta dayalı ve izlenebilir biçimde derlemek",
    chapter_ids=["CH-02"])

CHAPTER = bp.ChapterPlan(
    chapter_id="CH-02", chapter_number=2, title="Tünel Destekleme ve Kazı Yöntemleri",
    purpose="Destekleme sistemlerini, püskürtme beton gerekliliklerini ve kazı yöntemi seçimini "
            "kanıta dayalı olarak ortaya koymak",
    scope_in=["birincil/ikincil destekleme", "püskürtme beton", "TBM ve delme-patlatma"],
    scope_out=["maliyet analizi detayları", "sözleşme yönetimi"],
    prerequisites=["temel kaya mekaniği"],
    section_ids=["SEC-02-1", "SEC-02-2", "SEC-02-3"],
    target_audience="inşaat mühendisleri", technical_depth="advanced")

SECTIONS = [
    (bp.SectionPlan(
        section_id="SEC-02-1", chapter_id="CH-02", section_number="2.1",
        title="Tünel Destekleme Sistemleri: Kavramlar ve Elemanlar",
        objective="Birincil ve ikincil destekleme kavramlarını, elemanlarını ve işlevlerini "
                  "kanıta dayalı olarak tanımlamak",
        required_topics=["birincil destekleme", "ikincil destekleme", "püskürtme beton işlevi",
                         "kaya bulonu", "çelik iksa"],
        optional_topics=["süren boruları", "zemin çivisi"],
        excluded_topics=["maliyet"],
        expected_claim_types=["definition", "fact", "mechanism", "classification"]),
     [("Q-02-1-01", "Tünel destekleme sistemleri hangi ana gruplara ayrılır?", "tr",
       "classification", "P0", True, "classification", 1),
      ("Q-02-1-02", "Tünellerde birincil destekleme elemanları nelerdir?", "tr",
       "definition", "P0", True, "list", 1),
      ("Q-02-1-03", "Tünelde püskürtme betonun destekleme işlevleri nelerdir?", "tr",
       "mechanism", "P0", True, "mechanism", 1),
      ("Q-02-1-04", "Kaya bulonlarının tünel desteklemesindeki işlevi nedir?", "tr",
       "mechanism", "P1", True, "mechanism", 1),
      ("Q-02-1-05", "Çelik iksanın NATM destekleme sistemindeki rolü nedir?", "tr",
       "mechanism", "P1", False, "mechanism", 1),
      ("Q-02-1-06", "Tünellerde ikincil destekleme elemanları nelerdir?", "tr",
       "definition", "P1", False, "list", 1),
      ("Q-02-1-07", "What is the function of a waterproofing membrane in a tunnel lining?", "en",
       "cross_lingual", "P2", False, "mechanism", 1)]),

    (bp.SectionPlan(
        section_id="SEC-02-2", chapter_id="CH-02", section_number="2.2",
        title="Püskürtme Beton: Malzeme ve Uygulama Gereklilikleri",
        objective="Püskürtme betona ilişkin sayısal gereklilikleri ve şartname hükümlerini "
                  "kanıta dayalı olarak derlemek",
        required_topics=["çimento dozajı", "kaplama kalınlığı", "dayanım sınıfı"],
        optional_topics=["lif donatı", "kür"],
        excluded_topics=["birim fiyat"],
        expected_claim_types=["numeric", "requirement", "fact"]),
     [("Q-02-2-01", "Püskürtme beton için minimum çimento dozajı ne kadardır?", "tr",
       "numeric", "P0", True, "numeric", 1),
      ("Q-02-2-02", "What is the typical thickness of an initial shotcrete lining?", "en",
       "numeric", "P0", True, "numeric", 1),
      ("Q-02-2-03", "Püskürtme beton için hangi dayanım sınıfı öngörülmektedir?", "tr",
       "standard_or_specification", "P1", True, "numeric", 1),
      ("Q-02-2-04", "Püskürtme beton uygulamasında kaç kat uygulanır ve kalınlıkları nedir?", "tr",
       "numeric", "P1", False, "numeric", 1),
      ("Q-02-2-05", "What is flashcrete and what thickness is specified for it?", "en",
       "numeric", "P1", False, "numeric", 1),
      ("Q-02-2-06", "Püskürtme beton uygulamasında hasır çelik hangi tiplerde kullanılır?", "tr",
       "standard_or_specification", "P2", False, "list", 1)]),

    (bp.SectionPlan(
        section_id="SEC-02-3", chapter_id="CH-02", section_number="2.3",
        title="Kazı Yöntemi Seçimi: TBM ve Delme-Patlatma",
        objective="Kazı yöntemi seçim kriterlerini çok kaynaklı kanıtla ortaya koymak ve "
                  "kaynaklar arası farklılıkları görünür kılmak",
        required_topics=["seçim kriterleri", "TBM uygunluğu", "delme-patlatma uygunluğu"],
        optional_topics=["ilerleme hızı", "hibrit çözümler"],
        excluded_topics=["ihale süreçleri"],
        expected_claim_types=["comparison", "design_principle", "numeric"]),
     [("Q-02-3-01", "TBM ile delme-patlatma yöntemi hangi kriterlere göre karşılaştırılır?", "tr",
       "comparison", "P0", True, "comparison", 2),
      ("Q-02-3-02", "Hangi koşullarda TBM kullanımı uygun görülmektedir?", "tr",
       "design", "P0", True, "conditions", 1),
      ("Q-02-3-03", "What is the TBM competitiveness formula and what does it express?", "en",
       "formula", "P1", True, "formula", 1),
      ("Q-02-3-04", "Delme-patlatma yönteminin kazı aşamaları nelerdir?", "tr",
       "construction", "P1", False, "sequence", 1),
      ("Q-02-3-05", "How do costs compare between conventional and TBM tunnelling methods?", "en",
       "comparison", "P1", False, "comparison", 1),
      ("Q-02-3-06", "Kaya sınıfına göre izin verilen ilerleme boyu nedir?", "tr",
       "numeric", "P2", False, "numeric", 1)]),
]


def build_questions(section_id, rows):
    return [bp.ResearchQuestion(
        question_id=q[0], section_id=section_id, question=q[1], question_language=q[2],
        question_type=q[3], priority=q[4], required=q[5], expected_answer_type=q[6],
        minimum_sources=q[7]) for q in rows]


def main() -> int:
    (BOOK / "projects").mkdir(parents=True, exist_ok=True)
    (BOOK / "projects" / f"{BOOK_ID}.json").write_text(
        json.dumps(PROJECT.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    (BOOK / "chapter_plans" / f"{CHAPTER.chapter_id}.json").write_text(
        json.dumps(CHAPTER.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    runtime = production.ProductionGroundedGenerator()
    qdrant_before = production.qdrant_collection_state()
    summaries = []

    for section, rows in SECTIONS:
        questions = build_questions(section.section_id, rows)
        section.questions = [q.question_id for q in questions]
        (BOOK / "section_plans" / f"{section.section_id}.json").write_text(
            json.dumps(section.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        bp._write_jsonl(BOOK / "research_questions" / f"{section.section_id}.jsonl",
                        [q.as_dict() for q in questions])

        print(f"\n=== {section.section_id} {section.title} ({len(questions)} questions) ===",
              flush=True)
        research = bp.run_section_research(PROJECT, CHAPTER, section, questions, runtime=runtime)
        for row in research["results"]:
            print(f"  {row['question_id']} {row['priority']} {row['question_status']:<22}"
                  f"notes={len(row.get('note_ids', []))} {row['failure_reasons']}", flush=True)

        bp._write_jsonl(BOOK / "research_runs" / f"{section.section_id}.jsonl", research["results"])

        # Validate against the evidence text actually exposed by the packets used.
        bundle, validation = bp.build_section_bundle(PROJECT, CHAPTER, section, questions, research)

        bp._write_jsonl(BOOK / "evidence_notes" / f"{section.section_id}.jsonl",
                        [n.as_dict() for n in research["notes"]])
        bp._write_jsonl(BOOK / "claim_ledgers" / f"{section.section_id}.jsonl",
                        bundle.claim_ledger)
        (BOOK / "section_bundles" / f"{section.section_id}.json").write_text(
            json.dumps(bundle.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

        summaries.append({"section_id": section.section_id, "title": section.title,
                          "questions": len(questions), "notes": len(research["notes"]),
                          "valid_notes": validation["valid"], "invalid_notes": validation["invalid"],
                          "failure_histogram": validation["failure_histogram"],
                          "readiness": bundle.readiness,
                          "readiness_reasons": bundle.readiness_reasons,
                          "coverage": bundle.coverage_summary,
                          "bundle_sha": bundle.bundle_sha})
        print(f"  -> notes={len(research['notes'])} valid={validation['valid']} "
              f"invalid={validation['invalid']} readiness={bundle.readiness}", flush=True)

    qdrant_after = production.qdrant_collection_state()
    report = {"book_id": BOOK_ID, "sections": summaries,
              "qdrant_before": qdrant_before, "qdrant_after": qdrant_after,
              "qdrant_writes": qdrant_after[0] - qdrant_before[0],
              "pipeline": bp.pipeline_identity()}
    (BOOK / "manifests" / "pilot_summary_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nPILOT COMPLETE sections={len(summaries)} "
          f"qdrant {qdrant_before[0]}->{qdrant_after[0]} writes={report['qdrant_writes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
