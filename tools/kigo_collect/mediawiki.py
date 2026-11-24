"""vi.wikipedia / vi.wikisource client.

Reads the public article HTML (/wiki/<title>), which robots.txt allows.
The /w/api.php endpoint is disallowed for generic crawlers there, so it is not used.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

from .fetch import fetch

SITES = {"vi.wikipedia": "vi.wikipedia.org", "vi.wikisource": "vi.wikisource.org"}
_SKIP = {"script", "style", "sup", "table"}
_BLOCK = {"p", "h1", "h2", "h3", "h4", "li", "div", "br"}


@dataclass
class WikiPage:
    title: str
    url: str
    text: str
    categories: list[str]
    license_raw: str | None


class _Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.cats: list[str] = []
        self.title = ""
        self._skip = 0
        self._in_content = self._in_cats = self._in_h1 = False
        self._depth = 0
        self._stack: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id") == "mw-content-text":
            self._in_content = True
        if a.get("id") == "catlinks":
            self._in_content, self._in_cats = False, True
        if tag == "h1" and a.get("id") == "firstHeading":
            self._in_h1 = True
        if self._in_cats and tag == "a" and (a.get("title") or "").startswith("Thể loại:"):
            self.cats.append(a["title"])
        if self._in_content:
            if tag in _SKIP:
                self._skip += 1
            elif tag in _BLOCK and not self._skip:
                self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "h1":
            self._in_h1 = False
        if self._in_content and tag in _SKIP and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_h1:
            self.title += data
        elif self._in_content and not self._skip:
            self.parts.append(data)


def parse_html(html: str) -> tuple[str, str, list[str]]:
    ex = _Extract()
    ex.feed(html)
    text = re.sub(r"\n\s*\n+", "\n\n", "".join(ex.parts)).strip()
    return ex.title.strip(), text, ex.cats


def get_page(site: str, title: str, *, cache_dir: Path) -> WikiPage:
    host = SITES[site]
    url = f"https://{host}/wiki/{quote(title.replace(' ', '_'))}"
    res = fetch(url, cache_dir=cache_dir)
    real, text, cats = parse_html(res.path.read_text(encoding="utf-8"))
    if site == "vi.wikipedia":
        lic = "cc-by-sa"
    else:
        low = " ".join(cats).lower()
        lic = "public-domain" if ("phạm vi công cộng" in low or re.search(r"\bpd\b", low)) else None
    return WikiPage(real or title, url, text, cats, lic)
