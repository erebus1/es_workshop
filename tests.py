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


def test_find_tutors_by_subject():
    index_tutors([
        {
            'id': 1,
            'subject': 'english'
        },
        {
            'id': 2,
            'subject': 'french'
        }
    ], refresh=True)

    assert {1} == set(find_tutors(subject='english'))
