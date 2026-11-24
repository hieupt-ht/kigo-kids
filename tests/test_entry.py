from kigo_collect.entry import (Entry, REQUIRED_FIELDS, read_entry, slugify,
                                unique_path, validate, write_entry)


def good_meta(**over):
    meta = {f: "x" for f in REQUIRED_FIELDS}
    meta.update(tags_method=[], tags_topic=[], source_url=["http://a"],
                license_label="usable", reviewed=False,
                category="english/methods", added_details=[])
    meta.update(over)
    return meta


def test_slugify_vietnamese():
    assert slugify("Sơn Tinh – Thủy Tinh") == "son-tinh-thuy-tinh"
    assert slugify("Đền Hùng?") == "den-hung"


def test_slug_collision_gets_suffix(tmp_path):
    (tmp_path / "tam-cam.md").write_text("x")
    assert unique_path(tmp_path, "tam-cam").name == "tam-cam-2.md"


def test_roundtrip(tmp_path):
    e = Entry(good_meta(title="Thánh Gióng"), "Ngày xưa đời Hùng Vương\n")
    p = tmp_path / "a.md"
    write_entry(p, e)
    r = read_entry(p)
    assert r.meta == e.meta and r.body.strip() == e.body.strip()


def test_missing_field_reported():
    m = good_meta()
    del m["license_label"]
    assert "missing field: license_label" in validate(Entry(m, ""))


def test_bad_label_reported():
    assert "bad license_label: green" in validate(Entry(good_meta(license_label="green"), ""))


def test_history_requires_source():
    e = Entry(good_meta(category="vietnam/history", type="history", source_url=[]), "")
    assert "history entry needs source_url" in validate(e)


def test_vietnam_requires_type():
    e = Entry(good_meta(category="vietnam/folktales", type="tale"), "")
    assert any("type" in x for x in validate(e))


def test_added_details_must_match_markers():
    e = Entry(good_meta(category="vietnam/folktales", type="legend"),
              'A [thêm]Gióng nói: "..."[/thêm] B')
    assert "unlisted [thêm] markers: 1" in validate(e)
    ok = Entry(good_meta(category="vietnam/folktales", type="legend",
                         added_details=['Gióng nói: "..."']),
               'A [thêm]Gióng nói: "..."[/thêm] B')
    assert validate(ok) == []
