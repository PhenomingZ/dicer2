from datetime import datetime

from flask_restful import Resource

from App.controllers import BaseController
from App.responses import OKResponse
from App.utils.DateEncoder import Dicer2Encoder


class VersionsResource(Resource):

    @classmethod
    def get(cls, index, task, document):
        start_time = datetime.now()

        versions = BaseController().list_versions(index, task, document)

        response_data = dict(index=index, task=task, document=document, versions=versions)
        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)