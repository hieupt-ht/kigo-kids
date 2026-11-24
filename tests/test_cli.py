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


def test_titles_file_accepts_core_marker_notes_and_comments(tmp_path):
    from kigo_collect.cli import read_titles
    f = tmp_path / "t.txt"
    f.write_text("# comment\n*Thánh Gióng\nSơn Tinh – Thủy Tinh | truyền thuyết\n\n*Hai Bà Trưng | 40\n",
                 encoding="utf-8")
    assert read_titles(f) == ["Thánh Gióng", "Sơn Tinh – Thủy Tinh", "Hai Bà Trưng"]


def test_wordlist_az2025_layout_writes_all_levels_with_notes(tmp_path):
    from pathlib import Path
    src = Path(__file__).parent / "fixtures" / "cambridge_az_2025.txt"
    for _ in range(2):  # second run must not duplicate rows
        assert main(["--root", str(tmp_path), "wordlist", "--pdf", str(src), "--layout", "az2025"]) == 0
    path = tmp_path / "english" / "curriculum" / "vocabulary.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    assert {r["level"] for r in rows} == {"starters", "movers", "flyers"}
    assert len(rows) == len({(r["word"], r["pos"], r["level"]) for r in rows})
    apt = next(r for r in rows if r["word"] == "apartment")
    assert (apt["pos"], apt["note"], apt["level"]) == ("n", "UK flat", "starters")


def test_wordlist_needs_level_unless_az2025(tmp_path, capsys):
    import pytest
    txt = tmp_path / "w.txt"
    txt.write_text("apple (n)\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["--root", str(tmp_path), "wordlist", "--pdf", str(txt)])


def test_wordlist_az2025_fills_topics_from_thematic_list(tmp_path):
    from pathlib import Path
    fx = Path(__file__).parent / "fixtures"
    src = tmp_path / "all.txt"
    src.write_text((fx / "cambridge_az_2025.txt").read_text(encoding="utf-8") + "\n"
                   + (fx / "cambridge_thematic_2025.txt").read_text(encoding="utf-8").replace(
                       "Animals animal\n", "Animals animal\nTime afternoon\n"), encoding="utf-8")
    assert main(["--root", str(tmp_path), "wordlist", "--pdf", str(src), "--layout", "az2025"]) == 0
    rows = list(csv.DictReader((tmp_path / "english" / "curriculum" / "vocabulary.csv").open(encoding="utf-8-sig")))
    topic = {(r["word"], r["note"]): r["topic"] for r in rows if r["level"] == "starters"}
    assert topic[("afternoon", "")] == "Time"
    assert topic[("answer", "")] == ""  # not in the thematic list
