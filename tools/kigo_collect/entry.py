"""Entry file format: YAML front matter + Markdown body, with validation."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import yaml

REQUIRED_FIELDS = (
    "id", "title", "category", "tags_method", "tags_topic", "age_range",
    "cefr_level", "license_label", "license_detail", "source_url",
    "retrieved_at", "reviewed",
)
LABELS = ("usable", "reference", "excluded")
_MARKER = re.compile(r"\[thêm\](.*?)\[/thêm\]", re.S)


@dataclass
class Entry:
    meta: dict
    body: str


def slugify(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "d")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def unique_path(dir: Path, slug: str) -> Path:
    path = Path(dir) / f"{slug}.md"
    n = 2
    while path.exists():
        path = Path(dir) / f"{slug}-{n}.md"
        n += 1
    return path


def write_entry(path: Path, entry: Entry) -> None:
    front = yaml.safe_dump(entry.meta, allow_unicode=True, sort_keys=False)
    Path(path).write_text(f"---\n{front}---\n\n{entry.body}", encoding="utf-8")


def read_entry(path: Path) -> Entry:
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n\r?\n?(.*)\Z", text, re.S)
    if not m:
        raise ValueError(f"no front matter in {path}")
    return Entry(yaml.safe_load(m.group(1)) or {}, m.group(2))


def validate(entry: Entry) -> list[str]:
    meta, errors = entry.meta, []
    for f in REQUIRED_FIELDS:
        if f not in meta:
            errors.append(f"missing field: {f}")
    label = meta.get("license_label")
    if label is not None and label not in LABELS:
        errors.append(f"bad license_label: {label}")
    category = str(meta.get("category", ""))
    if category.startswith("vietnam/"):
        if meta.get("type") not in ("legend", "history"):
            errors.append(f"bad type: {meta.get('type')} (legend|history)")
    if category == "vietnam/history" or meta.get("type") == "history":
        if not meta.get("source_url"):
            errors.append("history entry needs source_url")
    markers = len(_MARKER.findall(entry.body))
    listed = len(meta.get("added_details") or [])
    if markers != listed:
        errors.append(f"unlisted [thêm] markers: {abs(markers - listed)}")
    return errors
