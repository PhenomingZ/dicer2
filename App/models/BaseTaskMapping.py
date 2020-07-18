from datetime import datetime

from elasticsearch_dsl import InnerDoc, Keyword, Text, Integer, Nested, Date

from App.models.BaseDocumentMapping import BaseDocument
from App.responses import ForbiddenAbort


class BaseTask(InnerDoc):
    """ Task信息存入'.dicer2_base'的字段结构和操作方法 """

    id = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    doc_count = Integer()
    docs = Nested(BaseDocument)
    created_at = Date()

    def isExist(self, doc_id):
        """
        判断'.dicer2_base'中当前task对象中某个document是否存在
        :param doc_id: 目标document
        :return:
        """

        for doc_item in self.docs:
            if doc_item.id == doc_id:
                return True
        return False

    def add_doc(self, doc_id, **kwargs):
        """
        向'.dicer2_base'中当前task对象中添加document
        :param doc_id: 目标document
        :param kwargs: 添加document所需的其他字段
        :return:
        """

        if self.isExist(doc_id):
            ForbiddenAbort(f"Document '{doc_id}' is already exist!")

        if doc_id[0] == "_":
            ForbiddenAbort(f"Document name can not start with '_'")

        title = kwargs.get("title")

        new_document = BaseDocument(
            id=doc_id,
            version=1,
            title=title,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.docs.append(new_document)
        self.doc_count += 1

    def del_doc(self, doc_id):
        """
        从'.dicer2_base'当前task对象中删除document
        :param doc_id: 目标document
        :return:
        """

        doc_loc = self.get_doc_loc(doc_id)
        self.docs.pop(doc_loc)
        self.doc_count -= 1

    def update_doc(self, doc_id, **kwargs):
        """
        向'.dicer2_base'当前task对象中更新document
        :param doc_id: 目标document
        :param kwargs: 更新document所需的其他字段
        :return:
        """

        old_doc = self.get_doc(doc_id)
        doc_loc = self.get_doc_loc(doc_id)

        old_doc.version += 1
        old_doc.updated_at = datetime.now()

        title = kwargs.get("title")

        if title:
            old_doc.title = title

        self.docs[doc_loc] = old_doc

    def get_doc(self, doc_id):
        """
        从'.dicer2_base'当前task对象中获取document对象
        :param doc_id: 目标document
        :return:
        """

        for doc_loc, doc_item in enumerate(self.docs):
            if doc_item.id == doc_id:
                return doc_item
        ForbiddenAbort(f"Document '{doc_id}' is not exist!")

    def get_doc_loc(self, doc_id):
        """
        从'.dicer2_base'当前task对象中获取document对象的索引位置
        :param doc_id:
        :return:
        """

        for doc_loc, doc_item in enumerate(self.docs):
            if doc_item.id == doc_id:
                return doc_loc
        ForbiddenAbort(f"Document '{doc_id}' is not exist!")
