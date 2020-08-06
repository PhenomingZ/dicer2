from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController

from datetime import datetime
from flasgger import swag_from

from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse
from App.utils.DateEncoder import Dicer2Encoder


class TaskResource(Dicer2Resource):
    """ Task相关资源接口 """

    @classmethod
    @swag_from("../docs/task_api/task_api_create.yaml")
    def post(cls, index, task):
        """
        新建一个Task
        :param index: Task所属的index
        :param task: Task的id
        :return: 创建成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().create_task(index_id=index, task_id=task, title=title, desc=desc)

        response_data = dict(index=index, task=task, title=title, desc=desc)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/task_api/task_api_delete.yaml")
    def delete(cls, index, task):
        """
        删除一个task
        :param index: Task所属的index
        :param task: Task的id
        :return: 删除成功响应
        """
        start_time = datetime.now()

        BaseController().delete_task(index_id=index, task_id=task)
        response_data = dict(index=index, task=task)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/task_api/task_api_total_update.yaml")
    def put(cls, index, task):
        """
        完整更新一个task
        :param index: Task所属的index
        :param task: Task的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().update_task(index_id=index, task_id=task, title=title, desc=desc)

        response_data = dict(index=index, task=task, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/task_api/task_api_partial_update.yaml")
    def patch(cls, index, task):
        """
        部分更新一个task
        :param index: Task所属的index
        :param task: Task的id
        :return: 更新成功响应
        """
        start_time = datetime.now()

        title = cls.get_parameter("title", required=False, location=["json", "form"])
        desc = cls.get_parameter("desc", location=["json", "form"])

        BaseController().update_task(index_id=index, task_id=task, title=title, desc=desc)

        response_data = dict(index=index, task=task, title=title, desc=desc)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/task_api/task_api_get.yaml")
    def get(cls, index, task):
        """
        获取一个task的信息
        :param index: Task所属的index
        :param task: Task的id
        :return: 获取成功响应
        """
        start_time = datetime.now()

        result = BaseController().get_task(index_id=index, task_id=task)

        docs_list = list()
        for doc in result.docs:
            doc_info = dict(doc=doc.id, title=doc.title, created_at=doc.created_at)
            docs_list.append(doc_info)

        response_data = dict(index=index, task=task, title=result.title, desc=result.desc,
                             created_at=result.created_at, updated_at=result.updated_at,
                             doc_count=result.doc_count, docs=docs_list)

        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
