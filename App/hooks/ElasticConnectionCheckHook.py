from elasticsearch import NotFoundError
from elasticsearch_dsl import connections

from App.models import Base


def init_elastic_connection(app):
    """
    初始化ElasticSearch连接和基本信息数据库
    :param app: DICER2使用的app对象
    :return:
    """

    # Define a default Elasticsearch client
    connections.create_connection(hosts=[app.config['ELASTICSEARCH_HOST']])

    # Init Dicer2 base index
    try:
        Base.get(id="dicer2")
    except NotFoundError:
        Base.init()
        Base(meta={"id": "dicer2"}, index_count=0, index=[]).save()
