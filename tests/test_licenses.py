import pytest
from kigo_collect.licenses import classify_license


@pytest.mark.parametrize("raw", ["cc-by", "cc0", "public-domain", "OGL"])
def test_cc_by_usable(raw):
    assert classify_license(raw)[0] == "usable"


def test_cc_by_sa_reference():
    assert classify_license("cc-by-sa")[0] == "reference"


def test_nc_excluded():
    assert classify_license("cc-by-nc-sa")[0] == "excluded"


def test_unknown_excluded():
    assert classify_license(None)[0] == "excluded"


def test_nc_ideas_only_reference():
    assert classify_license("cc-by-nc", ideas_only=True)[0] == "reference"
