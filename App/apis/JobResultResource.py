import os
from datetime import datetime

from flask_restful import Resource

from App.responses import OKResponse, NotFoundAbort
from App.settings import get_config
from App.utils.DateEncoder import Dicer2Encoder


class JobResultResource(Resource):

    @classmethod
    def get(cls, job_id):
        start_time = datetime.now()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")

        # TODO 给job加个名字属性 再给列表加上分页功能
        if job_id == "_list":
            job_file_list = os.listdir(store_folder_path)
            job_list = list()

            for job in job_file_list:
                job_path = os.path.join(store_folder_path, job)
                job_result = Dicer2Encoder.load(job_path)
                job_detail = JobResultHandler(job_result)
                job_list.append({
                    "id": job.split(".")[0],
                    "took": job_detail.took,
                    "type": job_detail.type,
                    "status": job_detail.stat,
                })
            response_data = dict(job_count=len(job_list), job_list=job_list)
            return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)

        else:
            store_job_path = os.path.join(store_folder_path, job_id + ".json")

            try:
                job_result = Dicer2Encoder.load(store_job_path)
            except FileNotFoundError:
                return NotFoundAbort(f"Job '{job_id}' not found")

            response_data = JobResultHandler(job_result).get_response_data()

            return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)


class JobResultHandler(object):
    def __init__(self, job_result):
        self.took = job_result.get("took")
        self.stat = job_result.get("status")
        self.data = job_result.get("data")
        self.type = self.data.get("job_type")

    def get_response_data(self):
        response_data = dict(
            took=self.took,
            status=self.stat,
        )
        response_data.update(self.data)

        return response_data
