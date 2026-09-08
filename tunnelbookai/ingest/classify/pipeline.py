"""Final section classification (task §34, §36, §37, §40, §41).

    document
      -> structural chunks
      -> candidate section retrieval (loopback embeddings)
      -> chunk-level votes
      -> rule signals
      -> agreement / conflict logic
      -> local Qwen arbitration ONLY when unsettled (§39)
      -> FINAL classification

The taxonomy is `book/scope/normalized/book_scope.json` and nothing else (§35). A section id
that is not in it can never become the final answer (stop condition §90).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import arbiter as arbiter_module
from . import embeddings as embedding_module
from . import evidence as evidence_module
from .rules import DocumentEvidence, chunk_votes, score_sections
from .taxonomy import Taxonomy, load_taxonomy

CHUNK_CHARS = 1800


@dataclass
class ClassificationResult:
    final_primary_section: str | None = None
    final_secondary_sections: list[str] = field(default_factory=list)
    final_section_confidence: float | None = None
    classification_methods: list[str] = field(default_factory=list)
    section_evidence: list[dict[str, Any]] = field(default_factory=list)
    candidates: list[dict[str, Any]] = field(default_factory=list)
    embedding_status: str = embedding_module.UNAVAILABLE
    embedding_model: str | None = None
    arbiter_status: str = arbiter_module.NOT_RUN
    arbiter_reason: str | None = None
    arbiter_model: str | None = None
    decision_path: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    taxonomy_source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "final_primary_section": self.final_primary_section,
            "final_secondary_sections": self.final_secondary_sections,
            "final_section_confidence": self.final_section_confidence,
            "classification_methods": self.classification_methods,
            "section_evidence": self.section_evidence,
            "candidates": self.candidates,
            "embedding_status": self.embedding_status,
            "embedding_model": self.embedding_model,
            "arbiter_status": self.arbiter_status,
            "arbiter_reason": self.arbiter_reason,
            "arbiter_model": self.arbiter_model,
            "decision_path": self.decision_path,
            "warnings": self.warnings,
            "taxonomy_source": self.taxonomy_source,
        }


def structural_chunks(elements: list[dict[str, Any]], limit: int = 24) -> list[str]:
    """Coarse heading-bounded slices of the document, used for chunk votes only."""
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for element in elements:
        text = (element.get("text") or "").strip()
        if not text:
            continue
        if element.get("type") == "heading" and size > 400:
            chunks.append("\n".join(current))
            current, size = [], 0
        current.append(text)
        size += len(text)
        if size >= CHUNK_CHARS:
            chunks.append("\n".join(current))
            current, size = [], 0
    if current:
        chunks.append("\n".join(current))
    return chunks[:limit]


def build_evidence(
    *,
    metadata: dict[str, Any],
    elements: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    figures: list[dict[str, Any]],
    normalized_text: str,
) -> DocumentEvidence:
    headings = [e["text"] for e in elements if e.get("type") == "heading" and e.get("text")]
    paragraphs = [e["text"] for e in elements
                  if e.get("type") in {"paragraph", "list_item"} and e.get("text")]
    abstract = ""
    for text in paragraphs:
        if len(text) > 200:
            abstract = text
            break
    ocr_text = "\n".join(f.get("ocr_text") or "" for f in figures if f.get("ocr_text"))
    metadata_terms = [
        str(metadata.get("title") or ""), str(metadata.get("document_type") or ""),
        *[str(t) for t in (metadata.get("topics") or [])],
    ]
    return DocumentEvidence(
        title=str(metadata.get("title") or ""),
        abstract=abstract,
        headings=headings,
        body=normalized_text,
        table_captions=[t.get("caption") or "" for t in tables if t.get("caption")],
        figure_captions=[f.get("caption") or "" for f in figures if f.get("caption")],
        ocr_text=ocr_text,
        metadata_terms=[t for t in metadata_terms if t],
    )


def _fuse(rule_scores: list[dict[str, Any]], embedding_scores: list[dict[str, Any]],
          votes: dict[str, float], fusion: dict[str, Any]
          ) -> tuple[list[dict[str, Any]], bool]:
    rule_weight = float(fusion.get("rule_weight", 0.55))
    embedding_weight = float(fusion.get("embedding_weight", 0.45))
    bonus = float(fusion.get("agreement_bonus", 0.05))
    vote_weight = float(fusion.get("chunk_vote_weight", 0.20))

    rules = {str(r["id"]): float(r["score"]) for r in rule_scores}
    embeds = {str(e["id"]): float(e["score"]) for e in embedding_scores}
    fused: list[dict[str, Any]] = []
    for section_id in set(rules) | set(embeds) | set(votes):
        score = (rule_weight * rules.get(section_id, 0.0)
                 + embedding_weight * embeds.get(section_id, 0.0)
                 + vote_weight * votes.get(section_id, 0.0))
        if section_id in rules and section_id in embeds:
            score += bonus
        fused.append({
            "id": section_id,
            "score": round(min(0.99, score), 4),
            "rule_score": round(rules.get(section_id, 0.0), 4),
            "embedding_score": round(embeds.get(section_id, 0.0), 4),
            "chunk_vote": round(votes.get(section_id, 0.0), 4),
        })
    fused.sort(key=lambda row: row["score"], reverse=True)
    rule_top = rule_scores[0]["id"] if rule_scores else None
    embedding_top = embedding_scores[0]["id"] if embedding_scores else None
    disagreement = bool(rule_top and embedding_top and rule_top != embedding_top)
    return fused, disagreement


def classify(
    *,
    metadata: dict[str, Any],
    elements: list[dict[str, Any]],
    tables: list[dict[str, Any]],
    figures: list[dict[str, Any]],
    normalized_text: str,
    config: Any,
    taxonomy: Taxonomy | None = None,
    embedding_index: Any = None,
    embedding_status: str | None = None,
    embedding_model: str | None = None,
    allow_arbiter: bool = True,
) -> ClassificationResult:
    ccfg = config.classification or {}
    taxonomy = taxonomy or load_taxonomy(
        ccfg.get("taxonomy_source", "book/scope/normalized/book_scope.json"),
        ccfg.get("taxonomy_terms", "config/taxonomy.yaml"))
    result = ClassificationResult(taxonomy_source=taxonomy.source_path)

    doc_evidence = build_evidence(
        metadata=metadata, elements=elements, tables=tables, figures=figures,
        normalized_text=normalized_text)

    rule_scores = [s.as_dict() for s in score_sections(doc_evidence, taxonomy=taxonomy)]
    if rule_scores:
        result.classification_methods.append("heading_rules")
    result.decision_path.append(f"rules:{len(rule_scores)}")

    chunks = structural_chunks(elements)
    votes = chunk_votes(chunks, taxonomy=taxonomy)
    if votes:
        result.classification_methods.append("chunk_vote")
    result.decision_path.append(f"chunk_votes:{len(chunks)}")

    embedding_scores: list[dict[str, Any]] = []
    if embedding_index is None and embedding_status is None:
        embedding_index, embedding_status, embedding_model = embedding_module.build_index(
            config, taxonomy)
    result.embedding_status = embedding_status or embedding_module.UNAVAILABLE
    result.embedding_model = embedding_model
    if embedding_index is not None:
        ecfg = ccfg.get("embedding", {}) or {}
        embedding_scores = embedding_index.score(
            doc_evidence.embedding_text(),
            top_k=int(ecfg.get("top_k", 8)),
            min_similarity=float(ecfg.get("min_similarity", 0.30)))
        if embedding_scores:
            result.classification_methods.append("embedding")
    else:
        result.warnings.append(f"EMBEDDING_{result.embedding_status}")
    result.decision_path.append(f"embeddings:{len(embedding_scores)}")

    fusion = ccfg.get("fusion", {}) or {}
    fused, disagreement = _fuse(rule_scores, embedding_scores, votes, fusion)
    result.candidates = fused[:10]

    if not fused:
        result.warnings.append("NO_SECTION_CANDIDATES")
        result.decision_path.append("no_candidates")
        return result

    top = fused[0]
    gap = top["score"] - fused[1]["score"] if len(fused) > 1 else top["score"]
    auto_accept = float(fusion.get("auto_accept_score", 0.88))
    llm_review = float(fusion.get("llm_review_score", 0.52))
    margin = float(fusion.get("disagreement_margin", 0.10))

    needs_arbiter = (
        top["score"] < llm_review
        or (disagreement and gap < margin)
        or (gap < margin and top["score"] < auto_accept)
    )
    result.decision_path.append(
        f"top={top['id']}:{top['score']} gap={gap:.3f} disagreement={disagreement} "
        "")

    primary = top["id"]
    confidence = top["score"]

    if needs_arbiter and allow_arbiter:
        arbiter_result = arbiter_module.arbitrate(
            doc_evidence.embedding_text(6000), fused, taxonomy, config)
        result.arbiter_status = arbiter_result.status
        result.arbiter_reason = arbiter_result.reason
        result.arbiter_model = arbiter_result.model
        result.decision_path.append(f"arbiter:{arbiter_result.status}")
        if arbiter_result.status == arbiter_module.SUCCESS and arbiter_result.primary_section:
            primary = arbiter_result.primary_section
            if arbiter_result.confidence is not None:
                confidence = max(confidence, arbiter_result.confidence)
            result.classification_methods.append("local_llm_arbiter")
            for section_id in arbiter_result.secondary_sections:
                if section_id not in result.final_secondary_sections:
                    result.final_secondary_sections.append(section_id)
        else:
            result.warnings.append(f"ARBITER_{arbiter_result.status}")
    elif needs_arbiter:
        result.arbiter_status = arbiter_module.NOT_RUN
        result.warnings.append("ARBITER_SKIPPED_BY_FLAG")
        result.decision_path.append("arbiter:skipped")
    else:
        result.decision_path.append("arbiter:not_needed_strong_agreement")

    if primary not in taxonomy:
        result.warnings.append(f"INVALID_FINAL_SECTION:{primary}")
        result.decision_path.append("invalid_final_section")
        return result

    secondary_min = float((ccfg.get("secondary_sections", {}) or {}).get("min_score", 0.55))
    for candidate in fused[1:]:
        if candidate["id"] == primary or candidate["id"] in result.final_secondary_sections:
            continue
        if candidate["score"] >= secondary_min and candidate["id"] in taxonomy:
            result.final_secondary_sections.append(candidate["id"])

    result.final_primary_section = primary
    result.final_section_confidence = round(float(confidence), 4)
    result.section_evidence = evidence_module.collect(
        [primary, *result.final_secondary_sections], elements, tables, figures, taxonomy)
    return result


def write_classification(bundle: Path, result: ClassificationResult) -> Path:
    bundle.mkdir(parents=True, exist_ok=True)
    path = bundle / "classification.json"
    path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, default=str),
                    encoding="utf-8")
    return path
