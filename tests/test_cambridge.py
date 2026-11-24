from kigo_collect.cambridge import parse_wordlist_text


def test_parse_wordlist_basic():
    rows = parse_wordlist_text("apple (n)\nafter (prep)\nask (v)", "starters")
    assert len(rows) == 3
    r = rows[0]
    assert (r.word, r.pos, r.level, r.topic) == ("apple", "n", "starters", None)


def test_parse_wordlist_skips_headers_and_page_numbers():
    text = "Pre A1 Starters\n12\napple (n)\nWord list\n13\n"
    assert [r.word for r in parse_wordlist_text(text, "starters")] == ["apple"]


def test_parse_wordlist_multiword():
    rows = parse_wordlist_text("ice cream (n)", "movers")
    assert rows[0].word == "ice cream" and rows[0].level == "movers"


from pathlib import Path

from kigo_collect.cambridge import parse_az_wordlists

AZ = Path(__file__).parent / "fixtures" / "cambridge_az_2025.txt"


def rows_by_level():
    out: dict[str, list] = {}
    for r in parse_az_wordlists(AZ.read_text(encoding="utf-8")):
        out.setdefault(r.level, []).append(r)
    return out


def test_az_splits_levels_and_stops_at_combined_lists():
    by = rows_by_level()
    assert set(by) == {"starters", "movers", "flyers"}
    assert [r.word for r in by["flyers"]] == ["actor", "programme"]  # combined list not read


def test_az_pos_notes_and_multiword():
    by = {r.word: r for r in parse_az_wordlists(AZ.read_text(encoding="utf-8")) if r.level == "starters"}
    assert (by["answer"].pos, by["answer"].note) == ("n + v", "")
    assert (by["apartment"].pos, by["apartment"].note) == ("n", "UK flat")
    assert (by["fish"].pos, by["fish"].note) == ("n", "s + pl")
    assert (by["at"].pos, by["at"].note) == ("prep", "of place")
    assert by["foot/feet"].pos == "n" and by["Miss"].pos == "title"


def test_az_skips_headers_letters_names_and_key():
    words = [r.word for r in parse_az_wordlists(AZ.read_text(encoding="utf-8")) if r.level == "starters"]
    assert words == ["a", "afternoon", "Alex", "answer", "apartment", "at", "fish", "foot/feet", "Miss",
                     "her", "in", "kangaroo", "kick", "kind", "kitten", "film star", "have to",
                     "ugly", "under", "understand", "us"]


def test_az_joins_wrapped_entries():
    movers = {r.word: r for r in rows_by_level()["movers"]}
    assert movers["city/town centre"].note == "US center"
    assert movers["could"].pos == "v" and movers["could"].note == "as in past of can for ability"
    assert movers["floor"].pos == "n" and movers["take off"].pos == "v"
    assert movers["a.m."].pos == "" and movers["a.m."].note == "for time"


def test_az_splits_merged_columns_and_reads_multi_token_pos():
    by = {r.word: r for r in parse_az_wordlists(AZ.read_text(encoding="utf-8")) if r.level == "starters"}
    assert by["her"].pos == "poss adj + pron"
    assert (by["in"].pos, by["in"].note) == ("prep", "of place + time")
    assert (by["kind"].pos, by["us"].pos, by["understand"].pos) == ("n", "pron", "v")
    assert (by["film star"].pos, by["film star"].note) == ("n", "US movie")
    assert (by["have to"].pos, by["have to"].note) == ("v", "got")


from kigo_collect.cambridge import parse_thematic

THEMATIC = Path(__file__).parent / "fixtures" / "cambridge_thematic_2025.txt"


def test_thematic_maps_words_to_topics():
    t = parse_thematic(THEMATIC.read_text(encoding="utf-8"))
    assert t["animal"] == ["Animals"] and t["bear"] == ["Animals"]
    assert t["bat"] == ["Animals"]  # the sports sense is its own, wrapped, line
    assert t["bat (as sports equipment)"] == ["Sports and leisure"]
    assert t["face"] == ["The body and the face"] and t["arm"] == ["The body and the face"]
    assert t["drink"] == ["Food and drink"] and t["ball"] == ["Sports and leisure"]
    assert t["sun"] == ["Weather"] and t["cloud"] == ["Weather"] and t["rain"] == ["Weather"]


def test_thematic_ignores_header_wraps_names_numbers_and_footer():
    t = parse_thematic(THEMATIC.read_text(encoding="utf-8"))
    for w in ("and the", "leisure", "week:", "alex", "alice", "hundred", "we believe that english can unlock a world of opportunity"):
        assert w not in t
    assert t["monday"] == ["Time"]
    assert "work" not in t and "hard." not in t  # text before the thematic section is not read
