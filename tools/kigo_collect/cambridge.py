"""Parse Cambridge Young Learners wordlists (words only, no examples)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_ROW = re.compile(r"^(.+?)\s*\(([^)]+)\)\s*$")


@dataclass
class WordRow:
    word: str
    pos: str
    level: str
    topic: str | None = None


def parse_wordlist_text(text: str, level: str) -> list[WordRow]:
    rows = []
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if m:
            rows.append(WordRow(m.group(1).strip(), m.group(2).strip(), level, None))
    return rows


def extract_pdf_text(pdf: Path) -> str:
    from pypdf import PdfReader

    return "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)
