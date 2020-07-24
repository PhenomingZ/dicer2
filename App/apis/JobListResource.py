import os
from datetime import datetime
from flasgger import swag_from

from App.apis.JobResource import JobResource
from App.responses import OKResponse
from App.settings import get_config
from App.utils.DateEncoder import Dicer2Encoder


class JobListResource(JobResource):
    """ Job列表相关资源接口 """

    @classmethod
    @swag_from("../docs/job_api/job_api_list.yaml")
    def get(cls):
        """
        获取全部job列表
        :return: 获取成功响应
        """

        start_time = datetime.now()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")

        job_file_list = os.listdir(store_folder_path)

        # 返回结果列表按照时间从近到远排序
        job_file_list.sort(key=lambda x: x.split(".")[0], reverse=True)

        job_list = list()

        count = 0
        for job in job_file_list:
            count += 1

            job_path = os.path.join(store_folder_path, job)
            job_result = Dicer2Encoder.load(job_path)
            job_detail = cls.JobResultHandler(job_result)
            job_list.append({
                "no": count,
                "id": job.split(".")[0],
                "name": job_detail.name,
                "took": job_detail.took,
                "type": job_detail.type,
                "status": job_detail.stat,
            })
        response_data = dict(job_count=len(job_list), job_list=job_list)
        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
