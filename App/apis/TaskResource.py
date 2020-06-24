from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController

from datetime import datetime

from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse


class TaskResource(Dicer2Resource):

    @classmethod
    def post(cls, index, task):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])

        BaseController().create_task(index_id=index, task_id=task, title=title)

        response_data = dict(index=index, task=task, title=title)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def delete(cls, index, task):
        start_time = datetime.now()

        BaseController().delete_task(index_id=index, task_id=task)
        response_data = dict(index=index, task=task)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    def put(cls, index, task):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=True, location=["json", "form"])

        BaseController().update_task(index_id=index, task_id=task, title=title)

        response_data = dict(index=index, task=task)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def patch(cls, index, task):
        start_time = datetime.now()

        title = cls.get_parameter("title", required=False, location=["json", "form"])

        BaseController().update_task(index_id=index, task_id=task, title=title)

        response_data = dict(index=index, task=task)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def get(cls, index, task):
        start_time = datetime.now()

        result = BaseController().get_task(index_id=index, task_id=task)

        docs_list = list()
        for doc in result.docs:
            docs_list.append(doc.id)

        response_data = dict(name=task, doc_count=result.doc_count, docs=docs_list)
        return OKResponse(data=response_data, start_time=start_time)