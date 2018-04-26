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

def test_find_tutors_by_complex_subject():
    index_tutors([
        {
            'id': 1,
            'subject': 'english lang'
        },
        {
            'id': 2,
            'subject': 'english new'
        }
    ], refresh=True)


    assert {1} == set(find_tutors(subject='english lang'))

def test_find_tutors_by_list_of_tags():
    index_tutors([
        {
            'id': 1,
            'tag': 'ielts'
        },
        {
            'id': 2,
            'tag': 'toefl'
        },
        {
            'id': 3,
            'tag': ['toefl', 'ielts']
        },
        {
            'id': 4,
            'tag': 'asd'
        }
    ], refresh=True)


    assert {1, 2, 3} == set(find_tutors(tags=['ielts', 'toefl']))
