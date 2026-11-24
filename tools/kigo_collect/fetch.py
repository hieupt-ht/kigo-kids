"""Polite fetcher: robots.txt check, raw cache, retries, generic User-Agent."""
from __future__ import annotations

import hashlib
import json
import time
import urllib.robotparser
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit

import requests

USER_AGENT = "kigo-collect/0.1 (research script)"


class FetchBlocked(Exception):
    """robots.txt disallows this URL."""


class FetchFailed(Exception):
    """All retries failed."""


@dataclass
class FetchResult:
    url: str
    path: Path
    from_cache: bool
    retrieved_at: str


def _key(url: str, params: dict | None) -> str:
    full = url + ("?" + urlencode(sorted(params.items())) if params else "")
    return hashlib.sha1(full.encode("utf-8")).hexdigest()


def _allowed(url: str, cache_dir: Path, session, delay: float) -> bool:
    parts = urlsplit(url)
    origin = f"{parts.scheme}://{parts.netloc}"
    rfile = cache_dir / f"robots-{hashlib.sha1(origin.encode()).hexdigest()}.txt"
    if rfile.exists():
        text = rfile.read_text(encoding="utf-8")
    else:
        try:
            r = session.get(origin + "/robots.txt", headers={"User-Agent": USER_AGENT}, timeout=30)
            text = r.text if r.status_code == 200 else ""
        except requests.RequestException:
            text = ""
        rfile.write_text(text, encoding="utf-8")
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    return rp.can_fetch(USER_AGENT, url)


def fetch(url: str, *, cache_dir: Path, params: dict | None = None, retries: int = 3,
          delay: float = 1.0, session: requests.Session | None = None) -> FetchResult:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    session = session or requests.Session()
    if not _allowed(url, cache_dir, session, delay):
        raise FetchBlocked(url)
    key = _key(url, params)
    body, meta = cache_dir / f"{key}.body", cache_dir / f"{key}.meta.json"
    if body.exists() and meta.exists():
        info = json.loads(meta.read_text(encoding="utf-8"))
        return FetchResult(url, body, True, info["retrieved_at"])
    last: Exception | None = None
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
            r.raise_for_status()
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            body.write_bytes(r.content)
            meta.write_text(json.dumps({"url": url, "retrieved_at": now}), encoding="utf-8")
            time.sleep(delay)
            return FetchResult(url, body, False, now)
        except requests.RequestException as exc:
            last = exc
            if attempt < retries - 1:
                time.sleep(delay)
    raise FetchFailed(f"{url}: {last}")
