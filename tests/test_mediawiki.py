from pathlib import Path

from kigo_collect import mediawiki
from kigo_collect.fetch import FetchResult
from kigo_collect.licenses import classify_license

FIX = Path(__file__).parent / "fixtures"


def patch(monkeypatch, name):
    seen = {}

    def fake(url, *, cache_dir, params=None, **kw):
        seen["url"], seen["params"] = url, params
        return FetchResult(url, FIX / name, False, "2026-11-24T00:00:00+00:00")

    monkeypatch.setattr(mediawiki, "fetch", fake)
    return seen


def test_wikipedia_license_reference(monkeypatch, tmp_path):
    seen = patch(monkeypatch, "wikipedia_page.json")
    page = mediawiki.get_page("vi.wikipedia", "Thánh Gióng", cache_dir=tmp_path)
    assert classify_license(page.license_raw)[0] == "reference"
    assert page.title == "Thánh Gióng" and "huyền thoại" in page.text
    assert seen["url"].startswith("https://vi.wikipedia.org/")
    assert seen["params"]["explaintext"] == 1


def test_wikisource_pd_category(monkeypatch, tmp_path):
    patch(monkeypatch, "wikisource_page.json")
    page = mediawiki.get_page("vi.wikisource", "Sơn Tinh Thủy Tinh", cache_dir=tmp_path)
    assert page.license_raw == "public-domain"
