from __future__ import annotations

import csv
import hashlib
import json
import logging
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


COPY_SUFFIX_RE = re.compile(
    r"(?:[\s._-]*(?:\(\s*\d+\s*\)|copy(?:\s*\d+)?|kopya(?:\s*\d+)?))+$",
    re.IGNORECASE,
)


def load_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load the deliberately small config schema without making PyYAML mandatory."""
    project_root = Path(__file__).resolve().parents[1]
    path = config_path or project_root / "config" / "config.yaml"
    data: dict[str, Any] = {"exclude_directories": [], "extensions": {}}
    section: str | None = None
    subsection: str | None = None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        text = line.strip()
        if indent == 0 and ":" in text:
            key, value = text.split(":", 1)
            section, subsection = key, None
            value = value.strip().strip("'\"")
            if value:
                data[key] = value
            elif key == "extensions":
                data[key] = {}
            else:
                data[key] = []
        elif indent == 2 and section == "extensions" and text.endswith(":"):
            subsection = text[:-1]
            data["extensions"][subsection] = []
        elif text.startswith("- "):
            value = text[2:].strip().strip("'\"")
            if section == "extensions" and subsection:
                data["extensions"][subsection].append(value.lower())
            elif section:
                data[section].append(value)
    configured_project_root = Path(data["project_root"]).expanduser()
    if not configured_project_root.is_absolute():
        configured_project_root = (project_root / configured_project_root).resolve()

    tunnel_root = os.environ.get("TUNNEL_ROOT")
    configured_source_root = Path(tunnel_root).expanduser() if tunnel_root else Path(data["source_root"]).expanduser()
    if not configured_source_root.is_absolute():
        configured_source_root = (project_root / configured_source_root).resolve()

    data["source_root"] = configured_source_root
    data["project_root"] = configured_project_root
    return data


def ensure_project_dirs(config: dict[str, Any]) -> None:
    root = config["project_root"]
    for rel in (
        "data/inventory", "data/duplicates", "data/markdown", "data/metadata",
        "data/markdown_full_docling", "data/converted_office", "data/failed", "data/temp",
        "data/inventory/snapshots", "logs", "reports", "tests", "tools",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)


def setup_logging(name: str, config: dict[str, Any]) -> logging.Logger:
    ensure_project_dirs(config)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(config["project_root"] / "logs" / f"{name}.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_title(value: str) -> str:
    stem = Path(value).stem
    stem = COPY_SUFFIX_RE.sub("", stem)
    stem = stem.replace("_", " ").replace("-", " ")
    stem = stem.translate(str.maketrans({"ı": "i", "İ": "i", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ç": "c", "Ç": "c", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u"}))
    stem = unicodedata.normalize("NFKD", stem.casefold())
    stem = "".join(ch for ch in stem if not unicodedata.combining(ch))
    stem = re.sub(r"[^a-z0-9]+", " ", stem)
    return re.sub(r"\s+", " ", stem).strip()


def canonical_sort_key(row: dict[str, str]) -> tuple[int, int, str]:
    name = Path(row["file_name"]).stem
    has_copy_marker = bool(COPY_SUFFIX_RE.search(name))
    clean = re.sub(r"[^\w]+", "", name, flags=re.UNICODE)
    return (int(has_copy_marker), len(clean), name.casefold())


EXTENSION_PRIORITY = {
    ".docx": 100, ".doc": 90, ".pdf": 80,
    ".pptx": 100, ".pptm": 95, ".ppt": 90,
    ".xlsx": 100, ".xls": 90,
    ".txt": 70, ".rtf": 60,
}


def extension_priority(extension: str) -> int:
    return EXTENSION_PRIORITY.get(extension.lower(), 0)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def iso_time(timestamp: float | None = None) -> str:
    return datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec="seconds") if timestamp else datetime.now().astimezone().isoformat(timespec="seconds")


def is_excluded(path: Path, source_root: Path, excluded_names: Iterable[str]) -> bool:
    try:
        relative = path.relative_to(source_root)
    except ValueError:
        return True
    excluded = {name.casefold() for name in excluded_names}
    return any(part.casefold() in excluded for part in relative.parts)


def mime_type_for(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def find_libreoffice() -> Path | None:
    project_root = Path(__file__).resolve().parents[1]
    candidates = [
        Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    ]
    if os.name == "nt":
        candidates.extend([
            project_root / "tools" / "LibreOfficePortable" / "App" / "libreoffice" / "program" / "soffice.com",
            project_root / "tools" / "LibreOffice" / "program" / "soffice.exe",
            Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
            Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        ])
    candidates.extend(Path(p) for p in filter(None, [shutil.which("soffice")]))
    return next((path for path in candidates if path.exists()), None)


def run_checked(command: list[str], timeout: int = 300, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False, encoding="utf-8", errors="replace", env=env)


def display_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
        amount /= 1024
    return f"{value} B"


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(json.dumps(item, ensure_ascii=False) for item in value) + "]"
    return json.dumps(str(value), ensure_ascii=False)


def strip_front_matter(text: str) -> str:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return text
    match = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n?", text, flags=re.DOTALL)
    return text[match.end():] if match else text


def native_path(path: Path) -> Path:
    """Return a Windows extended-length path while keeping manifests human-readable."""
    absolute = str(path.resolve())
    if os.name == "nt" and len(absolute) >= 240 and not absolute.startswith("\\\\?\\"):
        if absolute.startswith("\\\\"):
            return Path("\\\\?\\UNC\\" + absolute[2:])
        return Path("\\\\?\\" + absolute)
    return path
