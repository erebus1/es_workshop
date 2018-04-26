import elasticsearch as es
from elasticsearch.client import IndicesClient
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

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




def find_tutors():
    """

    :return:
    """
    res = get_search().execute()
    return [tutor.id for tutor in res.hits]
