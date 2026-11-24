"""Build index.csv from entries and sync the owner's review back."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from .entry import LABELS, REQUIRED_FIELDS, read_entry, write_entry

COLUMNS = list(REQUIRED_FIELDS) + ["type", "path"]


@dataclass
class SyncReport:
    updated: int = 0
    errors: list[str] = field(default_factory=list)


def _entries(root: Path):
    root = Path(root)
    for p in sorted(root.rglob("*.md")):
        if "raw" in p.relative_to(root).parts:
            continue
        try:
            yield p, read_entry(p)
        except ValueError:
            continue  # README, notes: not entries


def _cell(v) -> str:
    if isinstance(v, (list, tuple)):
        return "; ".join(str(x) for x in v)
    return "" if v is None else str(v)


def build_index(root: Path) -> int:
    root = Path(root)
    rows = []
    for p, e in _entries(root):
        row = {c: _cell(e.meta.get(c)) for c in COLUMNS}
        row["path"] = p.relative_to(root).as_posix()
        rows.append(row)
    with (root / "index.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def sync_review(root: Path, csv_path: Path) -> SyncReport:
    report = SyncReport()
    by_id = {str(e.meta.get("id")): (p, e) for p, e in _entries(root)}
    changes = []
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as f:
        for n, row in enumerate(csv.DictReader(f), start=2):
            rid = (row.get("id") or "").strip()
            label = (row.get("license_label") or "").strip()
            reviewed = (row.get("reviewed") or "").strip().lower()
            if not rid and not label and not reviewed:
                report.errors.append(f"row {n}: empty row")
            elif rid not in by_id:
                report.errors.append(f"row {n}: unknown id {rid!r}")
            elif label and label not in LABELS:
                report.errors.append(f"row {n}: bad license_label {label!r}")
            elif reviewed not in ("true", "false", ""):
                report.errors.append(f"row {n}: bad reviewed {reviewed!r}")
            else:
                changes.append((rid, label, reviewed))
    for rid, label, reviewed in changes:
        p, e = by_id[rid]
        new = dict(e.meta)
        if label:
            new["license_label"] = label
        if reviewed:
            new["reviewed"] = reviewed == "true"
        if new != e.meta:
            write_entry(p, type(e)(new, e.body))
            report.updated += 1
    return report
