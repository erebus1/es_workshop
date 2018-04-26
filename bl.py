import elasticsearch as es
from elasticsearch.client import IndicesClient
from elasticsearch_dsl import Search

from settings import INDEX_NAME

client = es.Elasticsearch(host='elasticsearch')
index_client = IndicesClient(client)

def get_search(index_name=INDEX_NAME):
    return Search(using=client).index(*[index_name])
