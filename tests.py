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


def test_find_tutors_by_list_of_tags_and_op():
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


    assert {3} == set(find_tutors(tags_and=['ielts', 'toefl']))



def test_find_tutors_by_range():
    index_tutors([
        {
            'id': 1,
            'price': 10
        },
        {
            'id': 2,
            'price': 16
        },
        {
            'id': 3,
            'price': 21
        },
    ], refresh=True)


    assert {2} == set(find_tutors(min_price=11, max_price=18))


def test_range_tutors_by_tags():
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
            'tag': ['toefl', 'ielts', 'daf']
        },
        {
            'id': 4,
            'tag': ['toefl', 'ielts', 'e', 't']
        },
        {
            'id': 5,
            'tag': ['other']
        }
    ], refresh=True)


    res = find_tutors(tags=['ielts', 'toefl', 'daf'])
    assert res[0] == 3
    assert res[1] == 4
    assert len(res) == 4
    assert set(res[2:]) == {1, 2}



def test_range_tutors_by_tags_and_price():
    index_tutors([
        {
            'id': 1,
            'price': 9,
            'tag': 'ielts'
        },
        {
            'id': 2,
            'price': 9,
            'tag': 'toefl'
        },
        {
            'id': 3,
            'price': 17,
            'tag': ['toefl', 'ielts', 'daf']
        },
        {
            'id': 4,
            'price': 11,
            'tag': ['toefl', 'ielts', 'e', 't']
        },
        {
            'id': 5,
            'price': 9,
            'tag': ['other']
        }
    ], refresh=True)


    res = find_tutors(tags=['ielts', 'toefl', 'daf'], exp_price=12)
    assert res[0] == 4
    assert res[1] == 3
    assert len(res) == 4
    assert set(res[2:]) == {1, 2}

def test_nested_docs():
    index_tutors([
        {
            'id': 1,
            'score': [
                {
                    'key': 'en',
                    'value': 1,
                },
                {
                    'key': 'ru',
                    'value': 2,
                },
            ]
        },{
            'id': 2,
            'score': [
                {
                    'key': 'en',
                    'value': 2,
                },
                {
                    'key': 'ru',
                    'value': 1,
                },
            ]
        },
    ], refresh=True)

    assert [2, 1] == find_tutors(score='en')
    assert [1, 2] == find_tutors(score='ru')
