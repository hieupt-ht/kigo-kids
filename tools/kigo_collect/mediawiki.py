"""Minimal MediaWiki client for vi.wikipedia / vi.wikisource."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .fetch import fetch

SITES = {"vi.wikipedia": "vi.wikipedia.org", "vi.wikisource": "vi.wikisource.org"}


@dataclass
class WikiPage:
    title: str
    url: str
    text: str
    categories: list[str]
    license_raw: str | None


def get_page(site: str, title: str, *, cache_dir: Path) -> WikiPage:
    host = SITES[site]
    params = {"action": "query", "prop": "extracts|categories", "titles": title,
              "explaintext": 1, "cllimit": "max", "redirects": 1, "format": "json"}
    res = fetch(f"https://{host}/w/api.php", cache_dir=cache_dir, params=params)
    data = json.loads(res.path.read_text(encoding="utf-8"))
    page = next(iter(data["query"]["pages"].values()))
    cats = [c["title"] for c in page.get("categories", [])]
    if site == "vi.wikipedia":
        lic = "cc-by-sa"
    else:
        low = " ".join(cats).lower()
        lic = "public-domain" if ("phạm vi công cộng" in low
                                  or re.search(r"pd", low)) else None
    real = page.get("title", title)
    return WikiPage(real, f"https://{host}/wiki/{real.replace(' ', '_')}",
                    page.get("extract", ""), cats, lic)
