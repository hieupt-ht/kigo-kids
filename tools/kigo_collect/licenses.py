"""Map a raw license string to a Kigo label (usable / reference / excluded)."""
from __future__ import annotations

import re


def classify_license(raw: str | None, *, ideas_only: bool = False) -> tuple[str, str]:
    if not raw or not raw.strip():
        return "excluded", "unknown license"
    s = re.sub(r"[\s_]+", "-", raw.strip().lower())
    if "-nc" in s or s.endswith("nc"):
        if ideas_only:
            return "reference", f"{raw}: non-commercial, ideas/conclusions only"
        return "excluded", f"{raw}: non-commercial"
    if "-sa" in s or "sharealike" in s:
        return "reference", f"{raw}: share-alike, rewrite in own words"
    if s in ("cc0", "public-domain", "pd", "ogl") or s.startswith(("cc-by", "ogl")):
        return "usable", raw
    return "excluded", f"{raw}: unrecognised license"
