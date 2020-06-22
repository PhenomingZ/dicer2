from elasticsearch_dsl import Search

from App.controllers.BaseTaskController import BaseTaskController
from App.models import Article
from App.utils.DocumentTools import DocumentTools
from App.utils.DocxLoader import DocxLoader


def save_article(index_id, task_id, document_id, file):
    docx_loader = DocxLoader(file)
    line_list = docx_loader.text
    tags_list = docx_loader.tags

    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)
    total_parts = len(line_list) - 1

    for count, line in enumerate(line_list):
        article = Article(index=index_id, task=task_id, document=document_id, doc_id=doc_id,
                          vector="default", tags=tags_list[count], body=line, part=count, total=total_parts)
        article.save(index=index_id)


def delete_article(index_id, task_id, document_id):
    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

    if document_id == "_all":
        BaseTaskController.clear_all_docs(index_id, task_id)
    else:
        Search(index=index_id).query("match", doc_id=doc_id).delete()


def get_article(index_id, task_id, document_id):
    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

    doc_search = Search(index=index_id).query("match", doc_id=doc_id).sort("part")

    body = []
    for hit in doc_search.scan():
        body.append(hit.body)

    return body


class BaseDocumentController(BaseTaskController):
    def create_document(self, index_id, task_id, document_id, file, **kwargs):
        index_instance = self.get_index(index_id)
        task_instance = index_instance.get_task(task_id)
        task_instance.add_doc(document_id, **kwargs)

        save_article(index_id, task_id, document_id, file)

        self.base.save()

    def delete_document(self, index_id, task_id, document_id):
        index_instance = self.get_index(index_id)
        task_instance = index_instance.get_task(task_id)
        task_instance.del_doc(document_id)

        delete_article(index_id, task_id, document_id)

        self.base.save()

    def update_document(self, index_id, task_id, document_id, file, **kwargs):
        index_instance = self.get_index(index_id)
        task_instance = index_instance.get_task(task_id)
        task_instance.update_doc(document_id, **kwargs)

        if file:
            delete_article(index_id, task_id, document_id)
            save_article(index_id, task_id, document_id, file)

        self.base.save()

    def get_document(self, index_id, task_id, document_id):
        index_instance = self.get_index(index_id)
        task_instance = index_instance.get_task(task_id)
        article = task_instance.get_doc(document_id)
        article.body = get_article(index_id, task_id, document_id)
        return article
