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




def find_tutors(subject=None, tags=None, tags_and=None, min_price=None, max_price=None):
    """

    :return:
    """
    query = get_search()
    if subject:
        query = query.filter(Q('term', subject=subject))
    if tags:
        query = query.filter(Q('terms', tag=tags))
    if tags_and:
        query = query.filter(Q('bool', filter=[Q('term', tag=tag) for tag in tags_and]))
    if min_price:
        query = query.filter(Q('range', price={'gte': min_price}))
    if max_price:
        query = query.filter(Q('range', price={'lte': max_price}))
    res = query.execute()
    return [tutor.id for tutor in res.hits]
