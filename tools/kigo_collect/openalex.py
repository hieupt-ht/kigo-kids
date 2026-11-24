"""OpenAlex client: open-access works with abstracts and license."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .fetch import fetch


@dataclass
class Paper:
    title: str
    year: int | None
    doi: str | None
    url: str | None
    license_raw: str | None
    abstract: str


def rebuild_abstract(inv: dict | None) -> str:
    if not inv:
        return ""
    slots = {pos: word for word, poss in inv.items() for pos in poss}
    return " ".join(slots[i] for i in sorted(slots))


def search_works(query: str, *, cache_dir: Path, per_page: int = 25) -> list[Paper]:
    params = {"search": query, "filter": "is_oa:true", "per-page": per_page}
    res = fetch("https://api.openalex.org/works", cache_dir=cache_dir, params=params)
    data = json.loads(res.path.read_text(encoding="utf-8"))
    out = []
    for w in data.get("results", []):
        loc = w.get("best_oa_location") or w.get("primary_location") or {}
        out.append(Paper(w.get("title") or "", w.get("publication_year"), w.get("doi"),
                         loc.get("landing_page_url") or w.get("doi"), loc.get("license"),
                         rebuild_abstract(w.get("abstract_inverted_index"))))
    return out
