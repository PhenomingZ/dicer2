import os
import json
import shutil

from elasticsearch_dsl import Search

from App.controllers.BaseTaskController import BaseTaskController
from App.models import Article
from App.responses import NotFoundAbort
from App.utils.DateEncoder import Dicer2Encoder
from App.utils.DocumentTools import DocumentTools
from App.utils.DocxLoader import DocxLoader


def save_article(index_id, task_id, document_id, docx_loader, title):
    """
    将一篇文档保存到ElasticSearch中
    :param index_id: 目标index
    :param task_id: 目标task
    :param document_id: 目标document
    :param docx_loader: 文档内容读取器对象
    :param title: 文档标题
    :return:
    """
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
    """
    从ElasticSearch中删除一篇文档
    :param index_id: 目标index
    :param task_id: 目标task
    :param document_id: 目标document
    :return:
    """
    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

    if document_id == "_all":
        BaseTaskController.clear_all_docs(index_id, task_id)
    else:
        Search(index=index_id).query("match", doc_id=doc_id).delete()


def get_document_storage_path(index_id, task_id, document_id, version, makedir=False):
    """
    获取文档的某个版本的持久化存储路径
    :param index_id: 目标index
    :param task_id: 目标task
    :param document_id: 目标document
    :param version: 目标document的版本
    :param makedir: 是否创建目标路径
    :return: 目标document的持久化存储路径
    """
    storage_path = BaseDocumentController.get_storage_path(index_id, task_id, document_id)

    if makedir:
        os.makedirs(storage_path, exist_ok=True)

    file_path = os.path.join(storage_path, f"{str(version)}.dicer2doc")
    return file_path


def get_article_data(index_id, task_id, document_id, version):
    """
    获取文档的某个版本的持久化数据
    :param index_id: 目标index
    :param task_id: 目标task
    :param document_id: 目标document
    :param version: 目标document的版本
    :return: 文档的持久化数据
    """
    file_path = get_document_storage_path(index_id, task_id, document_id, version, makedir=False)

    try:
        fp = open(file_path, "r")
        return json.load(fp)
    except FileNotFoundError:
        NotFoundAbort(f"Version '{version}' of document '{index_id}'-'{task_id}'-'{document_id}' is not exist")


class BaseDocumentController(BaseTaskController):
    """ 基本Document数据控制器 """

    def get_task_instance(self, index_id, task_id):
        """
        获取一个BaseTaskMapping实例
        :param index_id: 目标index
        :param task_id: 目标task
        :return: BaseTaskMapping实例
        """
        index_instance = self.get_index(index_id)
        return index_instance.get_task(task_id)

    def list_versions(self, index_id, task_id, document_id):
        """
        获取某个文档的版本信息列表
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :return: 文档的版本信息列表
        """
        storage_path = self.get_storage_path(index_id, task_id, document_id)

        file_list = []
        try:
            file_list = os.listdir(storage_path)
        except FileNotFoundError:
            NotFoundAbort(f"Document '{index_id}'-'{task_id}'-'{document_id}' is not exist")

        version_list = []

        for file in file_list:
            fp = open(os.path.join(storage_path, file), "r")
            version = json.load(fp)
            meta_data = dict(
                version=version["version"],
                title=version["title"],
                updated_at=version["updated_at"]
            )
            version_list.append(meta_data)
            fp.close()

        version_list.sort(key=lambda v: v["version"])
        return version_list

    def persistence_version(self, index_id, task_id, document_id, docx_loader, version):
        """
        将文档的某个版本持久化为文件
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :param docx_loader: 文档内容读取器对象
        :param version: 文档的版本
        :return:
        """
        task_instance = self.get_task_instance(index_id, task_id)
        doc_data = task_instance.get_doc(document_id).to_dict()

        if docx_loader.text:
            doc_data.update(body=docx_loader.text)
        else:
            body = get_article_data(index_id, task_id, document_id, version - 1).get("body")
            if not body:
                body = list()
            doc_data.update(body=body)

        file_path = get_document_storage_path(index_id, task_id, document_id, version, makedir=True)
        Dicer2Encoder.save(file_path, doc_data)

    def create_document(self, index_id, task_id, document_id, file, **kwargs):
        """
        创建一个document
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :param file: 用于创建document的文件流
        :param kwargs: document的其他字段
        :return:
        """
        task_instance = self.get_task_instance(index_id, task_id)
        task_instance.add_doc(document_id, **kwargs)

        docx_loader = DocxLoader(file)
        self.persistence_version(index_id, task_id, document_id, docx_loader, 1)

        title = kwargs.get("title")
        save_article(index_id, task_id, document_id, docx_loader, title)

        self.base.save()

    def delete_document(self, index_id, task_id, document_id, version):
        """
        删除一个document
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :param version: document的版本
        :return:
        """

        if version:
            version_file_path = get_document_storage_path(index_id, task_id, document_id, version, makedir=False)
            try:
                os.remove(version_file_path)
            except FileNotFoundError:
                NotFoundAbort(f"Version '{version}' of document '{index_id}/{task_id}/{document_id}' is not exist")

            return

        task_instance = self.get_task_instance(index_id, task_id)
        task_instance.del_doc(document_id)

        storage_path = self.get_storage_path(index_id, task_id, document_id)
        shutil.rmtree(storage_path, ignore_errors=True)

        delete_article(index_id, task_id, document_id)

        self.base.save()

    def update_document(self, index_id, task_id, document_id, file, **kwargs):
        """
        更新一个document
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :param file: 用于更新document的文件流
        :param kwargs: 用于更新document的其他字段
        :return: 本次更新的版本号
        """
        task_instance = self.get_task_instance(index_id, task_id)

        docx_loader = DocxLoader(file)

        # 如果有title等字段的更新，则先更新到dicer2_base
        # 在这里会对当前文档的版本号加1
        task_instance.update_doc(document_id, **kwargs)

        # 之后再获取当前的title，用于在有file更新的情况下对ES文档进行更新
        article = task_instance.get_doc(document_id)
        title = article.title

        if file:
            delete_article(index_id, task_id, document_id)
            save_article(index_id, task_id, document_id, docx_loader, title)

        self.persistence_version(index_id, task_id, document_id, docx_loader, article.version)

        self.base.save()

        return article.version

    def get_document(self, index_id, task_id, document_id, version=None):
        """
        获取一个document
        :param index_id: 目标index
        :param task_id: 目标task
        :param document_id: 目标document
        :param version: 目标文档的版本
        :return: 文档的完整信息包括全文
        """

        task_instance = self.get_task_instance(index_id, task_id)
        article = task_instance.get_doc(document_id)

        if not version:
            version = article.version

        article.body = get_article_data(index_id, task_id, document_id, version).get("body")
        return article
