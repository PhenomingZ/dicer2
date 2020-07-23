import os
from datetime import datetime
from flasgger import swag_from

from App.apis.JobResource import JobResource
from App.responses import OKResponse, NotFoundAbort
from App.settings import get_config
from App.utils.DateEncoder import Dicer2Encoder


class JobResultResource(JobResource):
    """ Job相关资源接口 """

    @classmethod
    @swag_from("../docs/job_api/job_api_result.yaml")
    def get(cls, job_id):
        """
        通过job_id获取对应job执行结果
        :param job_id: job的id，若为'_list'则显示全部job的列表
        :return: 获取成功响应
        """

        start_time = datetime.now()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")

        # TODO 给job加个名字属性 再给列表加上分页功能
        store_job_path = os.path.join(store_folder_path, job_id + ".json")

        try:
            job_result = Dicer2Encoder.load(store_job_path)
        except FileNotFoundError:
            return NotFoundAbort(f"Job '{job_id}' not found")

        response_data = cls.JobResultHandler(job_result).get_response_data()

        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
