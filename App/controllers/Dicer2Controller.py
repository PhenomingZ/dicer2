from elasticsearch import NotFoundError

from App.models import Base
from App.responses import NotFoundAbort


class Dicer2Controller(object):
    def __init__(self):
        try:
            self.base = Base.get(id="dicer2")
        except NotFoundError:
            NotFoundAbort("Base document 'dicer2' in ElasticSearch is not found!")
