from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse

from datetime import datetime
from flasgger import swag_from

from App.utils.DateEncoder import Dicer2Encoder


class DocumentsResource(Dicer2Resource):
    """ Document相关资源接口 """

    @classmethod
    @swag_from("../docs/document_api_create.yaml")
    def post(cls, index, task, document):
        """
        创建一个Document
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 创建成功响应
        """

        start_time = datetime.now()

        file = cls.get_parameter("file", required=True, location=["file"])
        title = cls.get_parameter("title", default_value=file.filename, location=["json", "form"])

        BaseController().create_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/document_api_delete.yaml")
    def delete(cls, index, task, document):
        """
        删除一个Document
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 删除成功响应
        """

        start_time = datetime.now()

        version = cls.get_parameter("version", required=False, location=["json", "form"])

        BaseController().delete_document(index, task, document, version)

        if not version:
            version = "_all"

        response_data = dict(index=index, task=task, document=document, version=version)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/document_api_total_update.yaml")
    def put(cls, index, task, document):
        """
        完全更新一个Document
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        file = cls.get_parameter("file", required=True, location=["file"])
        title = cls.get_parameter("title", required=True, location=["json", "form"])

        version = BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title, version=str(version))
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/document_api_partial_update.yaml")
    def patch(cls, index, task, document):
        """
        部分更新一个Document
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        file = cls.get_parameter("file", required=False, location=["file"])
        title = cls.get_parameter("title", required=False, location=["json", "form"])

        version = BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title, version=str(version))
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/document_api_get.yaml")
    def get(cls, index, task, document):
        """
        获取一个Document的信息
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 获取成功响应
        """
        start_time = datetime.now()

        version = cls.get_parameter("version", required=False, location=["json", "form"])

        result = BaseController().get_document(index, task, document, version)

        if not version:
            version = "latest"

        body = []

        # 筛选文档的查询结果，如果这一行是文本则显示，图片筛除
        for line in result.body:
            if line[0] == 1:
                body.append("[图片]")
            else:
                body.append(line[1])

        response_data = dict(index=index, task=task, document=document, version=version, title=result.title,
                             created_at=result.created_at, updated_at=result.updated_at, body=body)
        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
