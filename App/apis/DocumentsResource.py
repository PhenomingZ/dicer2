from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse

from datetime import datetime

from App.utils.DateEncoder import Dicer2Encoder


class DocumentsResource(Dicer2Resource):
    """ Document相关资源接口 """

    @classmethod
    def post(cls, index, task, document):
        """
        Create a new document
        ---
        tags:
          - Document API
        description:
          Upload a file and create a document into dicer2
        parameters:
          - in: path
            name: index
            type: string
            required: true
            description: index id
          - in: path
            name: task
            type: string
            required: true
            description: task id
          - in: path
            name: document
            type: string
            required: true
            description: document id
          - in: formData
            name: file
            type: file
            required: true
            description: file stream
          - in: formData
            name: title
            type: string
            required: false
            description: document title
        responses:
          201:
            description: Create successful response
            schema:
              id: CreatedResponse
              $ref: '/_swagger/created_response.yaml/'
         """

        start_time = datetime.now()

        file = cls.get_parameter("file", required=True, location=["file"])
        title = cls.get_parameter("title", default_value=file.filename, location=["json", "form"])

        BaseController().create_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
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

        response_data = dict(index=index, task=task, document=document)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
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

        BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
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

        BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(index=index, task=task, document=document, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
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
