from datetime import datetime

from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse


class IndexResource(Dicer2Resource):

    @classmethod
    def post(cls, index):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])

        BaseController().create_index(index_id=index, title=title)

        response_data = dict(index=index, title=title)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def delete(cls, index):
        start_time = datetime.now()

        BaseController().delete_index(index_id=index)

        response_data = dict(index=index)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    def put(cls, index):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])

        BaseController().update_index(index_id=index, title=title)

        response_data = dict(index=index, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def patch(cls, index):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=False, location=["json", "form"])

        BaseController().update_index(index_id=index, title=title)

        response_data = dict(index=index, title=title)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def get(cls, index):
        start_time = datetime.now()

        result = BaseController().get_index(index_id=index)

        tasks_list = list()
        for task in result.tasks:
            tasks_list.append(task.id)

        response_data = dict(task_count=result.task_count, tasks=tasks_list)
        return OKResponse(data=response_data, start_time=start_time)
