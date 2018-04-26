import pytest

import settings
from bl import index_client


def ensure_es_index():
    if index_client.exists(index=settings.INDEX_NAME):
        index_client.delete(index=settings.INDEX_NAME)
    index_client.create(
        index=settings.INDEX_NAME,
        body={
            "settings": {
                "number_of_replicas": 0,
                "number_of_shards": 1,
            },
            "mappings": {
                settings.INDEX_NAME: {
                    "properties": {
                    }
                }
            }
        },
        wait_for_active_shards=1
    )


@pytest.fixture(scope='function', autouse=True)
def ensure_es_index_func_scope():
    return ensure_es_index()
