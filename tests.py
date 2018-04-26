from bl import get_search


def test_basic():
    assert get_search().count() == 0
