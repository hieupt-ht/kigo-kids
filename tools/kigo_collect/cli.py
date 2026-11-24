"""Command line: python -m kigo_collect [--root kigo-data] <command>."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .cambridge import WordRow, extract_pdf_text, parse_wordlist_text
from .fetch import FetchBlocked, FetchFailed
from .index import _entries, build_index, sync_review
from .entry import validate
from .licenses import classify_license

VOCAB_COLS = ["word", "pos", "level", "topic"]


def cmd_wordlist(args, root: Path) -> int:
    src = Path(args.pdf)
    text = src.read_text(encoding="utf-8") if src.suffix == ".txt" else extract_pdf_text(src)
    new = parse_wordlist_text(text, args.level)
    out = root / "english" / "curriculum" / "vocabulary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows: dict[tuple, dict] = {}
    if out.exists():
        for r in csv.DictReader(out.open(encoding="utf-8-sig", newline="")):
            rows[(r["word"], r["pos"], r["level"])] = r
    for w in new:
        rows.setdefault((w.word, w.pos, w.level),
                        {"word": w.word, "pos": w.pos, "level": w.level, "topic": w.topic or ""})
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=VOCAB_COLS)
        wr.writeheader()
        wr.writerows(rows.values())
    print(f"{len(new)} words read, {len(rows)} rows in {out}")
    return 0


def cmd_wiki(args, root: Path) -> int:
    from .mediawiki import get_page

    titles = [args.title] if args.title else [
        t.strip() for t in Path(args.titles_file).read_text(encoding="utf-8").splitlines() if t.strip()]
    code = 0
    for t in titles:
        try:
            page = get_page(args.site, t, cache_dir=root / "raw" / "wiki")
        except (FetchBlocked, FetchFailed) as exc:
            print(f"FAILED {t}: {exc}")
            code = 1
            continue
        label, _ = classify_license(page.license_raw)
        print(f"{page.title}\t{page.url}\t{label}")
    return code


def cmd_papers(args, root: Path) -> int:
    from .openalex import search_works

    try:
        papers = search_works(args.query, cache_dir=root / "raw" / "openalex")
    except (FetchBlocked, FetchFailed) as exc:
        print(f"FAILED: {exc}")
        return 1
    for p in papers:
        label, _ = classify_license(p.license_raw, ideas_only=True)
        print(f"{p.year}\t{label}\t{p.title}\t{p.url}")
    return 0


def cmd_check(args, root: Path) -> int:
    bad = 0
    for path, e in _entries(root):
        for msg in validate(e):
            print(f"{path.relative_to(root)}: {msg}")
            bad += 1
    print(f"{bad} problem(s)")
    return 1 if bad else 0


def cmd_index(args, root: Path) -> int:
    print(f"{build_index(root)} entries indexed")
    return 0


def cmd_sync(args, root: Path) -> int:
    rep = sync_review(root, Path(args.csv))
    print(f"{rep.updated} updated, {len(rep.errors)} error(s)")
    for e in rep.errors:
        print(e)
    return 1 if rep.errors else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="kigo_collect")
    ap.add_argument("--root", default="kigo-data")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("wordlist")
    p.add_argument("--pdf", required=True)
    p.add_argument("--level", required=True, choices=["starters", "movers", "flyers"])
    p.set_defaults(fn=cmd_wordlist)
    p = sub.add_parser("wiki")
    p.add_argument("--site", required=True, choices=["vi.wikipedia", "vi.wikisource"])
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--title")
    g.add_argument("--titles-file")
    p.set_defaults(fn=cmd_wiki)
    p = sub.add_parser("papers")
    p.add_argument("--query", required=True)
    p.set_defaults(fn=cmd_papers)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    p = sub.add_parser("sync-review")
    p.add_argument("--csv", required=True)
    p.set_defaults(fn=cmd_sync)
    args = ap.parse_args(argv)
    return args.fn(args, Path(args.root))
