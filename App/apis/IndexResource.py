from datetime import datetime
from flasgger import swag_from

from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse
from App.utils.DateEncoder import Dicer2Encoder


# TODO 给index和task加上记录修改时间的功能
class IndexResource(Dicer2Resource):
    """ Index相关资源接口 """

    @classmethod
    @swag_from("../docs/index_api/index_api_create.yaml")
    def post(cls, index):
        """
        创建一个index
        :param index: index的id
        :return: 创建成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().create_index(index_id=index, title=title, desc=desc)

        response_data = dict(index=index, title=title, desc=desc)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/index_api/index_api_delete.yaml")
    def delete(cls, index):
        """
        删除一个index
        :param index: index的id
        :return: 删除成功响应
        """
        start_time = datetime.now()

        BaseController().delete_index(index_id=index)

        response_data = dict(index=index)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/index_api/index_api_total_update.yaml")
    def put(cls, index):
        """
        完全更新一个index
        :param index: index的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().update_index(index_id=index, title=title, desc=desc)

        response_data = dict(index=index, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/index_api/index_api_partial_update.yaml")
    def patch(cls, index):
        """
        部分更新一个index
        :param index: index的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=False, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().update_index(index_id=index, title=title, desc=desc)

        response_data = dict(index=index, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/index_api/index_api_get.yaml")
    def get(cls, index):
        """
        获取一个index的信息
        :param index: index的id
        :return: 获取成功响应
        """
        start_time = datetime.now()

        result = BaseController().get_index(index_id=index)

        tasks_list = list()
        for task in result.tasks:
            task_info = dict(task=task.id, title=task.title, desc=task.desc, created_at=task.created_at)
            tasks_list.append(task_info)

        response_data = dict(index=index, title=result.title, desc=result.desc, created_at=result.created_at,
                             task_count=result.task_count, tasks=tasks_list)

        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
