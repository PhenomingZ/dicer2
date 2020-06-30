import os

from elasticsearch_dsl import Search

from App.controllers.BaseTaskController import BaseTaskController
from App.models import Article
from App.settings import get_config
from App.utils.DateEncoder import DateEncoder
from App.utils.DocumentTools import DocumentTools
from App.utils.DocxLoader import DocxLoader


def save_article(index_id, task_id, document_id, file, title):
    docx_loader = DocxLoader(file)
    line_list = docx_loader.text

    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)
    total_parts = len(line_list) - 1

    for count, line in enumerate(line_list):
        image_marker, body = line[0], line[1]

        is_image = False if image_marker == 0 else True

        article = Article(index=index_id, task=task_id, document=document_id, title=title, doc_id=doc_id,
                          vector="default", is_image=is_image, body=body, part=count, total=total_parts)
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
        image_marker = 1 if hit.is_image else 0

        body.append((image_marker, hit.body))

    return body


class BaseDocumentController(BaseTaskController):
    def get_task_instance(self, index_id, task_id):
        index_instance = self.get_index(index_id)
        return index_instance.get_task(task_id)

    # TODO 在删除index、task和document时，也需要删除对应的持久化文件
    # TODO 添加查询历史版本的API
    def save_old_version(self, index_id, task_id, document_id):
        old_document = self.get_document(index_id, task_id, document_id)

        store_path = get_config().DICER2_STORAGE_PATH
        doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

        try:
            os.mkdir(os.path.join(store_path, doc_id))
        except FileExistsError:
            pass

        path = os.path.join(store_path, doc_id, f"{str(old_document.version)}.dicer2doc")

        # elasticsearch_dsl提供的to_dict方法只能将es field字段转化为字典返回
        # 而body字段是一个普通属性，故需要单独添加
        doc_data = old_document.to_dict()
        doc_data.update(body=old_document.body)

        DateEncoder.save(path, doc_data)

    def create_document(self, index_id, task_id, document_id, file, **kwargs):
        task_instance = self.get_task_instance(index_id, task_id)
        task_instance.add_doc(document_id, **kwargs)

        title = kwargs.get("title")
        save_article(index_id, task_id, document_id, file, title)

        self.base.save()

    def delete_document(self, index_id, task_id, document_id):
        task_instance = self.get_task_instance(index_id, task_id)
        task_instance.del_doc(document_id)

        delete_article(index_id, task_id, document_id)

        self.base.save()

    def update_document(self, index_id, task_id, document_id, file, **kwargs):
        task_instance = self.get_task_instance(index_id, task_id)

        # 每次更新文档前先对旧版本进行持久化存储
        self.save_old_version(index_id, task_id, document_id)

        # 如果有title等字段的更新，则先更新到dicer2_base
        task_instance.update_doc(document_id, **kwargs)

        # 之后再获取当前的title，用于在有file更新的情况下对ES文档进行更新
        article = task_instance.get_doc(document_id)
        title = article.title

        if file:
            delete_article(index_id, task_id, document_id)
            save_article(index_id, task_id, document_id, file, title)

        self.base.save()

    def get_document(self, index_id, task_id, document_id):
        task_instance = self.get_task_instance(index_id, task_id)
        article = task_instance.get_doc(document_id)
        article.body = get_article(index_id, task_id, document_id)
        return article
