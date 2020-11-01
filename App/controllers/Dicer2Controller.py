import os

from elasticsearch import NotFoundError

from App.models.BaseMapping import Base
from App.responses import not_found_abort, bad_request_abort
from App.settings import get_config


class Dicer2Controller(object):
    """ 基本信息数据控制器 """

    def __init__(self):
        """
        初始化基本信息存储库"dicer2"
        """
        try:
            self.base = Base.get(id="dicer2")
        except NotFoundError:
            not_found_abort("Base document 'dicer2' in ElasticSearch is not found!")

    @classmethod
    def get_storage_path(cls, index_id, task_id="", document_id=""):
        """
        获取DICER2持久化存储的文件路径
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :return: 持久化存储的文件路径
        """

        if not index_id:
            bad_request_abort("Dicer2 can not parse a path without index_id!")

        return os.path.join(get_config().DICER2_STORAGE_PATH, index_id, task_id, document_id)
