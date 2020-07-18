from datetime import datetime

from App.apis.SearchResource import SearchResource
from App.jobs.JobFactory import JobFactory
from App.jobs.JobTypeEnums import JobType
from App.responses import OKResponse


class MultipleSearchResource(SearchResource):
    """ 联合查重相关资源接口 """

    @classmethod
    def post(cls):
        """
        发送一个联合查重请求
        :return: 发送成功响应
        """
        start_time = datetime.now()

        source_range = cls.get_parameter("source_range", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        job = JobFactory.create_job(JobType.MULTIPLE_CHECK_JOB, source_range, search_range)
        job.start()

        response_data = dict(msg="Job Starting", job_id=job.id)
        return OKResponse(response_data, start_time)
