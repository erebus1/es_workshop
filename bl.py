import elasticsearch as es
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search, Q

from settings import INDEX_NAME

client = es.Elasticsearch(host='elasticsearch')
index_client = IndicesClient(client)

def get_search(index_name=INDEX_NAME):
    return Search(using=client).index(*[index_name])

def index_tutors(tutors, **bulk_kwargs):
    """

    :param tutors: lit of dicts
    :return:
    """
    res = []
    for tutor in tutors:
        request = {
            '_index': INDEX_NAME,
            '_type': INDEX_NAME,
            '_id': tutor['id'],
            '_op_type': 'index',
            '_source': tutor,
        }
        res.append(request)
    bulk(client, res, **bulk_kwargs)




def find_tutors(subject=None, tags=None, tags_and=None, min_price=None, max_price=None,
                exp_price=None, score=None):
    """

    :return:
    """
    search = get_search()
    filters = []
    must = []
    if subject:
        filters.append(Q('term', subject=subject))
    if tags:
        must += [Q('bool', should=[Q('term', tag=tag) for tag in tags])]
    if tags_and:
        filters.append(Q('bool', filter=[Q('term', tag=tag) for tag in tags_and]))
    if min_price:
        filters.append(Q('range', price={'gte': min_price}))
    if max_price:
        filters.append(Q('range', price={'lte': max_price}))
    query = Q('bool', filter=filters, must=must)
    if exp_price:
        query = Q(
            'function_score',
            functions=[{"exp": {
                "price": {
                      "origin": exp_price,
                      "scale": 2,
                      "offset": 0,
                      "decay" : 0.5
                }
            }}],
            boost_mode='multiply',
            score_mode='multiply',
            query=query
        )
    if score:
        query = Q(
        'bool',
        should=[  # will summarise score from each query
            Q(
                'nested',
                path='score',
                query=Q(
                    'function_score',
                    functions=[dict(
                        field_value_factor={
                            "field": 'score.value',
                            "missing": 0
                        },
                    )],
                    boost_mode='replace',
                    query=Q('term', **{'score.key': score})
                )
            ),
            # to show ads without rating field, if rating indexing fail
            Q(boost=0)
        ]
    )
    search = search.query(query).extra(_source=False)
    res = search.execute()
    # assert False, res.hits.hits
    return [int(tutor.meta.id) for tutor in res.hits]
