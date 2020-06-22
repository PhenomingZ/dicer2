from elasticsearch import NotFoundError
from elasticsearch_dsl import connections

from App.models.ArticleMapping import Article
from App.models.BaseMapping import Base
from App.models.BaseIndexMapping import BaseIndex
from App.models.BaseTaskMapping import BaseTask
from App.models.BaseDocumentMapping import BaseDocument


def init_elastic(app):
    # Define a default Elasticsearch client
    connections.create_connection(hosts=[app.config['ELASTICSEARCH_HOST']])

    # Init Dicer2 base index
    try:
        Base.get(id="dicer2")
    except NotFoundError:
        Base.init()
        Base(meta={"id": "dicer2"}, index_count=0, index=[]).save()
