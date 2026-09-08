from __future__ import annotations

from collections import defaultdict

from utils import (
    canonical_sort_key, extension_priority, load_config, normalize_title, read_csv,
    setup_logging, write_csv,
)


EXACT_FIELDS = [
    "duplicate_group_id", "canonical_candidate", "document_id", "file_name",
    "relative_path", "extension", "size_bytes", "sha256",
]
LOGICAL_FIELDS = [
    "logical_group_id", "document_id", "file_name", "relative_path", "extension",
    "normalized_title", "match_method", "confidence", "preferred_source",
]


def find_exact_duplicates(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("sha256"):
            groups[row["sha256"]].append(row)
    output: list[dict[str, str]] = []
    duplicate_groups = [group for group in groups.values() if len(group) > 1]
    duplicate_groups.sort(key=lambda group: min(item["relative_path"].casefold() for item in group))
    for index, group in enumerate(duplicate_groups, 1):
        canonical_id = min(group, key=canonical_sort_key)["document_id"]
        for row in sorted(group, key=canonical_sort_key):
            output.append({
                "duplicate_group_id": f"EXACT{index:05d}",
                "canonical_candidate": row["document_id"] == canonical_id,
                **{key: row[key] for key in ("document_id", "file_name", "relative_path", "extension", "size_bytes", "sha256")},
            })
    return output


def find_logical_duplicates(rows: list[dict[str, str]], exact_rows: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    exact_noncanonical = {
        row["document_id"] for row in (exact_rows or [])
        if str(row["canonical_candidate"]).casefold() not in {"true", "1", "yes"}
    }
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["document_id"] in exact_noncanonical:
            continue
        normalized = normalize_title(row["file_name"])
        if normalized:
            groups[normalized].append(row)
    candidates: list[tuple[str, list[dict[str, str]]]] = []
    for title, group in groups.items():
        extensions = {row["extension"].lower() for row in group}
        if len(group) > 1 and len(extensions) > 1:
            candidates.append((title, group))
    candidates.sort(key=lambda item: item[0])
    output: list[dict[str, str]] = []
    for index, (title, group) in enumerate(candidates, 1):
        preferred = max(
            group,
            key=lambda row: (extension_priority(row["extension"]), -len(row["file_name"]), row["file_name"].casefold()),
        )
        for row in sorted(group, key=lambda item: (-extension_priority(item["extension"]), item["file_name"].casefold())):
            output.append({
                "logical_group_id": f"LOGICAL{index:05d}", "document_id": row["document_id"],
                "file_name": row["file_name"], "relative_path": row["relative_path"],
                "extension": row["extension"], "normalized_title": title,
                "match_method": "exact_normalized_title", "confidence": "high",
                "preferred_source": row["document_id"] == preferred["document_id"],
            })
    return output


def write_summary(exact_rows: list[dict], logical_rows: list[dict], path) -> None:
    exact_groups = {row["duplicate_group_id"] for row in exact_rows}
    logical_groups = {row["logical_group_id"] for row in logical_rows}
    preferred = sum(str(row["preferred_source"]).casefold() in {"true", "1", "yes"} for row in logical_rows)
    lines = [
        "# Duplicate Analizi Özeti", "",
        f"- Exact duplicate grup sayısı: **{len(exact_groups)}**",
        f"- Exact duplicate dosya sayısı: **{len(exact_rows)}**",
        f"- Exact duplicate nedeniyle canonical olmayan dosya sayısı: **{max(0, len(exact_rows) - len(exact_groups))}**",
        f"- Logical duplicate grup sayısı: **{len(logical_groups)}**",
        f"- Logical duplicate dosya/variant sayısı: **{len(logical_rows)}**",
        f"- Preferred variant sayısı: **{preferred}**", "",
        "Logical eşleşmeler yalnızca normalize edilmiş başlığın birebir aynı ve uzantıların farklı olduğu durumlarda oluşturuldu; fuzzy eşleştirme kullanılmadı.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    config = load_config()
    logger = setup_logging("02_duplicates", config)
    root = config["project_root"]
    inventory = read_csv(root / "data/inventory/inventory.csv")
    if not inventory:
        logger.error("Inventory is missing or empty; run 01_inventory.py first")
        return 2
    exact = find_exact_duplicates(inventory)
    logical = find_logical_duplicates(inventory, exact)
    write_csv(root / "data/duplicates/exact_duplicates.csv", exact, EXACT_FIELDS)
    write_csv(root / "data/duplicates/logical_duplicates.csv", logical, LOGICAL_FIELDS)
    write_summary(exact, logical, root / "reports/duplicate_summary.md")
    logger.info("Duplicate analysis completed: %d exact groups, %d logical groups", len({r['duplicate_group_id'] for r in exact}), len({r['logical_group_id'] for r in logical}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
