import os
from datetime import datetime

from flask_restful import Resource

from App.responses import OKResponse, NotFoundAbort
from App.settings import get_config
from App.utils.DateEncoder import Dicer2Encoder


class JobResultResource(Resource):
    """ Job相关资源接口 """

    @classmethod
    def get(cls, job_id):
        """
        通过job_id获取对应job执行结果
        :param job_id: job的id，若为'_list'则显示全部job的列表
        :return: 获取成功响应
        """

        start_time = datetime.now()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")

        # TODO 给job加个名字属性 再给列表加上分页功能
        if job_id == "_list":
            job_file_list = os.listdir(store_folder_path)

            # 返回结果列表按照时间从近到远排序
            job_file_list.sort(key=lambda x: x.split(".")[0], reverse=True)

            job_list = list()

            count = 0
            for job in job_file_list:
                count += 1

                job_path = os.path.join(store_folder_path, job)
                job_result = Dicer2Encoder.load(job_path)
                job_detail = JobResultHandler(job_result)
                job_list.append({
                    "no": count,
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
    """ 将获取到的任务结果规范为响应格式 """

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
