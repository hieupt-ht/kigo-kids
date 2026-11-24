import pytest
import requests

from kigo_collect.fetch import FetchBlocked, FetchFailed, fetch

UA = "kigo-collect/0.1 (research script)"


class Resp:
    def __init__(self, text="", status=200):
        self.text, self.status_code = text, status
        self.content = text.encode("utf-8")

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


class FakeSession:
    def __init__(self, robots="", body="hello", error=None):
        self.robots, self.body, self.error = robots, body, error
        self.gets, self.headers_seen = 0, []

    def get(self, url, params=None, headers=None, timeout=None):
        if url.endswith("/robots.txt"):
            return Resp(self.robots, 200 if self.robots else 404)
        self.gets += 1
        self.headers_seen.append(headers or {})
        if self.error:
            raise self.error
        return Resp(self.body)


URL = "https://example.org/page"


def test_fetch_uses_cache(tmp_path):
    s = FakeSession()
    a = fetch(URL, cache_dir=tmp_path, delay=0, session=s)
    b = fetch(URL, cache_dir=tmp_path, delay=0, session=s)
    assert not a.from_cache and b.from_cache and s.gets == 1
    assert b.path.read_text(encoding="utf-8") == "hello"
    assert (tmp_path / (b.path.stem + ".meta.json")).exists()


def test_fetch_retries_then_raises(tmp_path):
    s = FakeSession(error=requests.ConnectionError("down"))
    with pytest.raises(FetchFailed):
        fetch(URL, cache_dir=tmp_path, delay=0, session=s)
    assert s.gets == 3


def test_robots_disallow_blocks(tmp_path):
    s = FakeSession(robots="User-agent: *\nDisallow: /")
    with pytest.raises(FetchBlocked):
        fetch(URL, cache_dir=tmp_path, delay=0, session=s)
    assert s.gets == 0


def test_user_agent_generic(tmp_path):
    s = FakeSession()
    fetch(URL, cache_dir=tmp_path, delay=0, session=s)
    assert s.headers_seen[0]["User-Agent"] == UA
