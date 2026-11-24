import csv
import os

from kigo_collect.entry import Entry, REQUIRED_FIELDS, read_entry, write_entry
from kigo_collect.index import build_index, sync_review


def meta(id_, title, **over):
    m = {f: "" for f in REQUIRED_FIELDS}
    m.update(id=id_, title=title, category="vietnam/folktales", type="legend",
             tags_method=[], tags_topic=["tale"], source_url=["http://a"],
             license_label="usable", reviewed=False)
    m.update(over)
    return m


def make(tmp_path):
    d = tmp_path / "vietnam" / "folktales"
    d.mkdir(parents=True)
    paths = []
    for i, t in enumerate(["Tấm Cám", "Sơn Tinh"]):
        p = d / f"e{i}.md"
        write_entry(p, Entry(meta(f"id{i}", t), f"Nội dung {i}\n"))
        paths.append(p)
    return paths


def test_index_csv_has_bom_and_vietnamese(tmp_path):
    make(tmp_path)
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "skip.md").write_text("no front matter")
    assert build_index(tmp_path) == 2
    data = (tmp_path / "index.csv").read_bytes()
    assert data.startswith(b"\xef\xbb\xbf")
    assert "Tấm Cám" in data.decode("utf-8-sig")


def test_sync_updates_reviewed(tmp_path):
    p0, _ = make(tmp_path)
    build_index(tmp_path)
    body_before = read_entry(p0).body
    rows = list(csv.DictReader((tmp_path / "index.csv").open(encoding="utf-8-sig")))
    for r in rows:
        if r["id"] == "id0":
            r["reviewed"], r["license_label"] = "true", "excluded"
    with (tmp_path / "rev.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    report = sync_review(tmp_path, tmp_path / "rev.csv")
    assert report.errors == []
    e = read_entry(p0)
    assert e.meta["reviewed"] is True and e.meta["license_label"] == "excluded"
    assert e.body == body_before


def test_sync_rejects_bad_rows_without_touching_files(tmp_path):
    paths = make(tmp_path)
    mtimes = [os.stat(p).st_mtime_ns for p in paths]
    (tmp_path / "rev.csv").write_text(
        "id,reviewed,license_label\nnope,true,usable\nid0,true,green\n,,\n",
        encoding="utf-8")
    report = sync_review(tmp_path, tmp_path / "rev.csv")
    assert len(report.errors) == 3 and report.updated == 0
    assert [os.stat(p).st_mtime_ns for p in paths] == mtimes
