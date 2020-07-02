import os

from elasticsearch import NotFoundError

from App.models import Base
from App.responses import NotFoundAbort, BadRequestAbort
from App.settings import get_config


class Dicer2Controller(object):
    def __init__(self):
        try:
            self.base = Base.get(id="dicer2")
        except NotFoundError:
            NotFoundAbort("Base document 'dicer2' in ElasticSearch is not found!")

    @classmethod
    def get_storage_path(cls, index_id, task_id="", document_id=""):

        if not index_id:
            BadRequestAbort("Dicer2 can not parse a path without index_id!")

        return os.path.join(get_config().DICER2_STORAGE_PATH, index_id, task_id, document_id)
