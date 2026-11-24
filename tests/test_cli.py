import csv

from kigo_collect.cli import main
from kigo_collect.entry import Entry, REQUIRED_FIELDS, write_entry


def entry(tmp_path, name, **over):
    m = {f: "x" for f in REQUIRED_FIELDS}
    m.update(tags_method=[], tags_topic=[], source_url=["http://a"],
             license_label="usable", reviewed=False, category="english/methods")
    m.update(over)
    d = tmp_path / "english" / "methods"
    d.mkdir(parents=True, exist_ok=True)
    write_entry(d / name, Entry(m, "body\n"))


def test_check_exit_code(tmp_path, capsys):
    entry(tmp_path, "ok.md")
    assert main(["--root", str(tmp_path), "check"]) == 0
    entry(tmp_path, "bad.md", license_label="green")
    assert main(["--root", str(tmp_path), "check"]) == 1
    assert "bad.md: bad license_label: green" in capsys.readouterr().out.replace("\\", "/")


def test_wordlist_merges_levels(tmp_path):
    txt = tmp_path / "w.txt"
    txt.write_text("apple (n)\nask (v)\n", encoding="utf-8")
    for _ in range(2):
        assert main(["--root", str(tmp_path), "wordlist", "--pdf", str(txt),
                     "--level", "starters"]) == 0
    main(["--root", str(tmp_path), "wordlist", "--pdf", str(txt), "--level", "movers"])
    path = tmp_path / "english" / "curriculum" / "vocabulary.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    assert len(rows) == 4
    assert {(r["word"], r["level"]) for r in rows} == {
        ("apple", "starters"), ("ask", "starters"), ("apple", "movers"), ("ask", "movers")}


def test_index_command_counts(tmp_path, capsys):
    entry(tmp_path, "a.md")
    entry(tmp_path, "b.md", id="y")
    assert main(["--root", str(tmp_path), "index"]) == 0
    assert "2" in capsys.readouterr().out
