from pathlib import Path

from kigo_collect import openalex
from kigo_collect.fetch import FetchResult

FIX = Path(__file__).parent / "fixtures"


def test_openalex_abstract_rebuilt():
    assert openalex.rebuild_abstract({"Phonics": [0], "works": [1]}) == "Phonics works"


def test_search_works(monkeypatch, tmp_path):
    seen = {}

    def fake(url, *, cache_dir, params=None, **kw):
        seen["params"] = params
        return FetchResult(url, FIX / "openalex_works.json", False, "t")

    monkeypatch.setattr(openalex, "fetch", fake)
    papers = openalex.search_works("phonics", cache_dir=tmp_path)
    assert seen["params"]["filter"] == "is_oa:true"
    p = papers[0]
    assert (p.year, p.license_raw, p.abstract) == (2020, "cc-by", "Phonics works")
