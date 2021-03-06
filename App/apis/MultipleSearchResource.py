from datetime import datetime
from flasgger import swag_from

from App.apis.SearchResource import SearchResource
from App.jobs.JobFactory import JobFactory
from App.jobs.JobTypeEnums import JobType
from App.responses import OKResponse


class MultipleSearchResource(SearchResource):
    """ 联合查重相关资源接口 """

    @classmethod
    @swag_from("../docs/search_api/search_api_multiple.yaml")
    def post(cls):
        """
        发送一个联合查重请求
        :return: 发送成功响应
        """
        start_time = datetime.now()

        job_name = cls.get_parameter("name", location=["json", "form"])

        source_range = cls.get_parameter("source_range", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        job = JobFactory.create_job(JobType.MULTIPLE_CHECK_JOB, job_name, source_range, search_range,
                                    **cls.get_custom_configs())
        job.start()

        response_data = dict(msg="Job Starting", job_id=job.id)
        return OKResponse(response_data, start_time)
