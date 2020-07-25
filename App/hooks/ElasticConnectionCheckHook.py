from elasticsearch import NotFoundError
from elasticsearch_dsl import connections

from App.models import Base
from App.settings import get_config


def init_elastic_connection():
    """
    初始化ElasticSearch连接和基本信息数据库
    :return:
    """

    # Define a default Elasticsearch client
    connections.create_connection(hosts=[get_config().ELASTICSEARCH_HOST])

    # Init Dicer2 base index
    try:
        Base.get(id="dicer2")
    except NotFoundError:
        Base.init()
        Base(meta={"id": "dicer2"}, index_count=0, index=[]).save()
