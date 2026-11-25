"""Print the readable text of a source page, for writing an entry (not part of the kigo_collect package).

    python tools/read_source.py wiki "Bà Mụ" [--site vi.wikipedia] [--offset 0] [--max 9000]
    python tools/read_source.py url "https://example.org/page" [--keyword "từ khóa"] [--offset 0] [--max 6000]

Both go through the polite cached fetcher (robots.txt, cache, generic User-Agent) and need network access
the first time a page is read. `wiki` needs the exact page title (vi.wikipedia or vi.wikisource).
Long pages: read in parts with --offset and --max.
"""
import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kigo_collect.fetch import fetch  # noqa: E402
from kigo_collect.mediawiki import get_page  # noqa: E402

CACHE = Path(__file__).resolve().parent.parent / "kigo-data" / "raw" / "wiki"
_END = re.compile(r"\n(Tham khảo|Chú thích|Liên kết ngoài|Xem thêm|Thư mục|Ghi chú|Nguồn)\s*\n")


def wiki_text(site: str, title: str) -> str:
    text = get_page(site, title, cache_dir=CACHE).text
    m = _END.search(text)
    if m:
        text = text[: m.start()]
    return re.sub(r"\[\s*(sửa|sửa mã nguồn|\d+)\s*\]", "", text)


def url_text(url: str) -> str:
    raw = Path(fetch(url, cache_dir=CACHE).path).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", raw))
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n", text)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="kind", required=True)
    w = sub.add_parser("wiki")
    w.add_argument("title")
    w.add_argument("--site", default="vi.wikipedia", choices=["vi.wikipedia", "vi.wikisource"])
    u = sub.add_parser("url")
    u.add_argument("url")
    u.add_argument("--keyword", help="start from the first occurrence of this text (skips menus)")
    for p in (w, u):
        p.add_argument("--offset", type=int, default=0)
        p.add_argument("--max", type=int, default=9000)
    a = ap.parse_args()
    if a.kind == "wiki":
        text = wiki_text(a.site, a.title)
    else:
        text = url_text(a.url)
        if a.keyword and a.keyword in text:
            text = text[max(0, text.index(a.keyword) - 300):]
    print(f"[{len(text)} ký tự; in từ {a.offset}]")
    print(text[a.offset: a.offset + a.max])


if __name__ == "__main__":
    main()
