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
