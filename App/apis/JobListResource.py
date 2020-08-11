import os
from datetime import datetime
from flasgger import swag_from

from App.apis.JobResource import JobResource
from App.responses import OKResponse, bad_request_abort
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

        limit = cls.get_parameter("limit", default_value=0, location=["args"], data_type="integer")
        page = cls.get_parameter("page", default_value=1, location=["args"], data_type="integer")

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")

        try:
            job_file_list = os.listdir(store_folder_path)
        except FileNotFoundError:
            job_file_list = list()
            os.mkdir(store_folder_path)

        # 返回结果列表按照时间从近到远排序
        job_file_list.sort(key=lambda x: x.split(".")[0], reverse=True)

        job_list = list()

        count = 0
        for job in job_file_list:
            count += 1

            job_path = os.path.join(store_folder_path, job)
            job_result = Dicer2Encoder.load(job_path)
            job_detail = cls.JobResultHandler(job_result)

            # 只有单独查重任务有document字段，联合查重中document字段为null
            job_list.append({
                "no": count,
                "id": job.split(".")[0],
                "name": job_detail.name,
                "took": job_detail.took,
                "type": job_detail.type,
                "status": job_detail.stat,
                "start_time": job_detail.start_time,
                "end_time": job_detail.end_time,
                "document": job_detail.data.get("document"),
                "source_range": job_detail.data.get("source_range"),
                "search_range": job_detail.data.get("search_range")
            })

        total_jobs = len(job_list)

        if limit <= 0:
            total_pages = 1
            limit = total_jobs
        else:
            total_pages = (total_jobs // limit) + (0 if total_jobs % limit == 0 else 1)

        if page > total_pages:
            bad_request_abort("The current number of pages exceeds the total pages")

        job_list = job_list[(page - 1) * limit: ((page - 1) + 1) * limit]

        response_data = dict(total_jobs=total_jobs, total_pages=total_pages, limit=limit, page=page, job_list=job_list)
        return OKResponse(data=Dicer2Encoder.jsonify(response_data), start_time=start_time)
