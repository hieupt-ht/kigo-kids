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
    note: str = ""


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


_TOK = r"(?:poss(?:\s+adj)?|adj|adv|conj|det|dis|excl|int|n|prep|pron|title|v)"
_POS_EXPR = rf"{_TOK}(?:\s*\+\s*{_TOK})*"
_TAIL = r"of\s+(?:place|time)(?:\s*\+\s*(?:place|time))?"
_POS_ONLY = re.compile(rf"^{_POS_EXPR}$")
_ENTRY = re.compile(rf"(?P<head>\S.*?)\s+(?P<pos>{_POS_EXPR})(?:\s+(?P<tail>{_TAIL}))?(?=\s|$)")
_NOPOS = re.compile(r"^(?P<word>[a-z][^\s(]*)\s+\((?P<note>[^)]+)\)$")
_LEVEL_HEADING = (("Starters A–Z wordlist", "starters"), ("Movers A–Z wordlist", "movers"),
                  ("Flyers A–Z wordlist", "flyers"))
_COMBINED = ("alphabetic vocabulary list", "grammatical vocabulary list", "thematic vocabulary list")


def _mask_parens(line: str) -> str:
    """Same-length copy of `line` with everything inside (...) blanked to `_`, so words in a note are never read as parts of speech."""
    out, depth = [], 0
    for ch in line:
        if ch == "(":
            depth += 1
        out.append("_" if depth else ch)
        if ch == ")" and depth:
            depth -= 1
    return "".join(out)


def _scan(line: str) -> list[tuple[str, str, str]]:
    """Every `head pos [of place]` entry on one line (two columns can be merged), or [] if the
    whole line is not made of entries."""
    masked, pos, found = _mask_parens(line), 0, []
    while pos < len(line):
        while pos < len(line) and line[pos].isspace():
            pos += 1
        if pos >= len(line):
            break
        m = _ENTRY.match(masked, pos)
        if not m:
            return []
        found.append((line[m.start("head"):m.end("head")], m.group("pos"),
                      line[m.start("tail"):m.end("tail")] if m.group("tail") else ""))
        pos = m.end()
    return found


def _needs_next(line: str, nxt: str | None) -> bool:
    """A wrapped entry: open parenthesis, or no part of speech and the next line carries it."""
    if nxt is None:
        return False
    if line.count("(") > line.count(")"):
        return True
    if _scan(line):
        return False
    return nxt.startswith("(") or bool(_POS_ONLY.match(nxt))


def _split_note(head: str, tail: str) -> tuple[str, str]:
    """`film (US movie) star` -> (`film star`, `US movie`); the parenthesised text is the note."""
    notes = []

    def take(m: re.Match) -> str:
        notes.append(m.group(1).strip())
        return " "

    word = re.sub(r"\s+", " ", re.sub(r"\((.*)\)", take, head)).strip()
    return word, " ".join(x for x in (*notes, tail) if x)


def parse_az_wordlists(text: str) -> list[WordRow]:
    """Rows from the 2025 Pre A1 Starters / A1 Movers / A2 Flyers A–Z wordlists
    (`word pos`, optional `(note)`, entries wrapped over two lines, columns sometimes merged)."""
    lines = [ln.strip() for ln in text.splitlines()]
    rows: list[WordRow] = []
    level: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if any(k in line for k in _COMBINED):
            level = None
            continue
        heading = next((lv for key, lv in _LEVEL_HEADING if key in line), None)
        if heading:
            level = heading
            continue
        if level is None or not line or re.fullmatch(r"[A-Z]", line):
            continue
        while _needs_next(line, lines[i] if i < len(lines) else None):
            line = f"{line} {lines[i]}".strip()
            i += 1
        entries = _scan(line)
        if entries:
            for head, pos, tail in entries:
                word, note = _split_note(head, tail)
                rows.append(WordRow(word, re.sub(r"\s+", " ", pos), level, None, note))
            continue
        m = _NOPOS.match(line)
        if m:
            rows.append(WordRow(m.group("word"), "", level, None, m.group("note").strip()))
    return rows


# (line prefix as printed, topic name or None to ignore, wrapped header lines to skip)
_THEMES = (
    ("Animals", "Animals", 0), ("The body", "The body and the face", 2), ("Clothes", "Clothes", 0),
    ("Colours", "Colours", 0), ("Family &", "Family and friends", 1), ("Food &", "Food and drink", 1),
    ("Health", "Health", 0), ("The home", "The home", 0), ("Materials", "Materials", 0),
    ("Names", None, 0), ("Numbers", None, 0), ("Places &", "Places and directions", 1),
    ("School", "School", 0), ("Sports &", "Sports and leisure", 1), ("Time", "Time", 0),
    ("The days of the", "Time", 1), ("The months of", "Time", 1), ("Toys", "Toys", 0),
    ("Transport", "Transport", 0), ("Weather", "Weather", 0), ("Work", "Work", 0),
    ("The world", "The world around us", 1),
)


def parse_thematic(text: str) -> dict[str, list[str]]:
    """lower-cased word -> topics it is listed under in the thematic vocabulary list.
    A header line can carry first words of two level columns (`Weather sun cloud`): both are kept."""
    lines = [ln.strip() for ln in text.splitlines()]
    try:
        start = lines.index("A2 Flyers thematic vocabulary list") + 1
    except ValueError:
        return {}
    topics: dict[str, list[str]] = {}
    topic, skip = None, 0

    def add(word: str) -> None:
        word = word.strip().lower()
        if topic and word and topic not in topics.setdefault(word, []):
            topics[word].append(topic)

    body, i = [], start
    while i < len(lines):  # join a wrapped `bat (as sports` / `equipment)`
        line = lines[i]
        i += 1
        while line.count("(") > line.count(")") and i < len(lines):
            line = f"{line} {lines[i]}"
            i += 1
        body.append(line)

    for line in body:
        if line.startswith("We believe that English"):
            break
        if not line or "thematic vocabulary list" in line or line.startswith("Pre A1 Starters A1 Movers"):
            continue
        header = next((t for t in _THEMES if line == t[0] or line.startswith(t[0] + " ")), None)
        if header:
            topic, skip = header[1], header[2]
            rest = line[len(header[0]):].strip()
            if rest and not skip and topic:
                add(rest)
                if " " in rest:
                    for w in rest.split():
                        add(w)
            continue
        if skip:
            skip -= 1
            continue
        add(line)
    return topics
