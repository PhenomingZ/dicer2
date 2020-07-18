import hashlib


class DocumentTools(object):
    """ 关于Document的工具方法类 """

    @classmethod
    def get_doc_id(cls, index_id, task_id, document_id):
        """
        计算文档的id
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :return: 文档id
        """

        hl = hashlib.md5()
        src = index_id
        hl.update(src.encode("utf-8"))
        src = hl.hexdigest() + task_id
        hl.update(src.encode("utf-8"))
        src = hl.hexdigest() + document_id
        hl.update(src.encode("utf-8"))

        return hl.hexdigest()
