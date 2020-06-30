from datetime import datetime

from elasticsearch_dsl import InnerDoc, Keyword, Text, Integer, Nested, Date

from App.models.BaseDocumentMapping import BaseDocument
from App.responses import ForbiddenAbort


class BaseTask(InnerDoc):
    id = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    doc_count = Integer()
    docs = Nested(BaseDocument)
    created_at = Date()

    def isExist(self, doc_id):
        for doc_item in self.docs:
            if doc_item.id == doc_id:
                return True
        return False

    def add_doc(self, doc_id, **kwargs):
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
        doc_loc = self.get_doc_loc(doc_id)
        self.docs.pop(doc_loc)
        self.doc_count -= 1

    def update_doc(self, doc_id, **kwargs):
        old_doc = self.get_doc(doc_id)
        doc_loc = self.get_doc_loc(doc_id)

        old_doc.version += 1
        old_doc.updated_at = datetime.now()

        title = kwargs.get("title")

        if title:
            old_doc.title = title

        self.docs[doc_loc] = old_doc

    def get_doc(self, doc_id):
        for doc_loc, doc_item in enumerate(self.docs):
            if doc_item.id == doc_id:
                return doc_item
        ForbiddenAbort(f"Document '{doc_id}' is not exist!")

    def get_doc_loc(self, doc_id):
        for doc_loc, doc_item in enumerate(self.docs):
            if doc_item.id == doc_id:
                return doc_loc
        ForbiddenAbort(f"Document '{doc_id}' is not exist!")
