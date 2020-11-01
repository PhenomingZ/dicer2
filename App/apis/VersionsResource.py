from datetime import datetime
from flasgger import swag_from

from flask_restful import Resource

from App.controllers.BaseController import BaseController
from App.responses import OKResponse
from App.utils.DateEncoder import Dicer2Encoder


class VersionsResource(Resource):
    """ 文档版本资源相关接口 """

    @classmethod
    @swag_from("../docs/document_api/document_api_version.yaml")
    def get(cls, index, task, document):
        """
        获取一个文档的所有历史版本列表
        :param index: Document所属的index
        :param task: Document所属的task
        :param document: Document的id
        :return: 获取成功响应
        """
        start_time = datetime.now()

        versions = BaseController().list_versions(index, task, document)

        response_data = dict(index=index, task=task,
                             document=document, versions=versions)
        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
