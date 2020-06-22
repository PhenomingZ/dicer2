from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, CreatedResponse, DeletedResponse, UpdatedResponse

from datetime import datetime


class DocumentsResource(Dicer2Resource):

    @classmethod
    def post(cls, index, task, document):
        start_time = datetime.now()

        file = cls.get_parameter("file", required=True, location=["file"])
        title = cls.get_parameter("title", default_value=file.filename, location=["json", "form"])

        BaseController().create_document(index, task, document, file=file, title=title)

        response_data = dict(title=title, index=index, task=task)
        return CreatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def delete(cls, index, task, document):
        start_time = datetime.now()

        BaseController().delete_document(index, task, document)

        response_data = dict(index=index, task=task, document=document)
        return DeletedResponse(data=response_data, start_time=start_time)

    @classmethod
    def put(cls, index, task, document):
        start_time = datetime.now()

        file = cls.get_parameter("file", required=True, location=["file"])
        title = cls.get_parameter("title", required=True, location=["json", "form"])

        BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(title=title, index=index, task=task)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def patch(cls, index, task, document):
        start_time = datetime.now()

        file = cls.get_parameter("file", required=False, location=["file"])
        title = cls.get_parameter("title", required=False, location=["json", "form"])

        BaseController().update_document(index, task, document, file=file, title=title)

        response_data = dict(title=title, index=index, task=task)
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    def get(cls, index, task, document):
        start_time = datetime.now()

        result = BaseController().get_document(index, task, document)

        response_data = dict(title=result.title, index=index, task=task, body=result.body)
        return OKResponse(data=response_data, start_time=start_time)
