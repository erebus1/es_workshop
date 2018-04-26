from bl import get_search, index_tutors, find_tutors


def test_basic():
    assert get_search().count() == 0

def test_get_all_tutors():
    index_tutors([
        {
            'id': 1
        },
        {
            'id': 2
        }
    ], refresh=True)
    assert {1, 2} == set(find_tutors())