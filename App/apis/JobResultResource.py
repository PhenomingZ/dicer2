import os
from datetime import datetime

from flask_restful import Resource

from App.jobs.JobTypeEnums import JobStatus
from App.responses import OKResponse
from App.settings import get_config
from App.utils.DateEncoder import Dicer2Encoder


class JobResultResource(Resource):

    @classmethod
    def get(cls, job_id):
        start_time = datetime.now()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")
        store_job_path = os.path.join(store_folder_path, job_id + ".json")

        job_result = Dicer2Encoder.load(store_job_path)

        response_data = dict()

        if job_result["status"] == JobStatus.SUCCESS.value:
            print(111)

        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
