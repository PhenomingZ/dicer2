from datetime import datetime
from flasgger import swag_from

from App.apis.SearchResource import SearchResource
from App.controllers.BaseController import BaseController
from App.jobs.JobFactory import JobFactory
from App.jobs.JobTypeEnums import JobType
from App.responses import OKResponse


class SingleSearchResource(SearchResource):
    """ 单独查重相关资源接口 """

    @classmethod
    @swag_from("../docs/search_api/search_api_single.yaml")
    def post(cls):
        """
        发送一个单独查重请求
        :return: 发送成功响应
        """
        start_time = datetime.now()

        job_name = cls.get_parameter("name", location=["json", "form"])

        index_id = cls.get_parameter("index", required=True, location=["json", "form"])
        task_id = cls.get_parameter("task", required=True, location=["json", "form"])
        document_id = cls.get_parameter("document", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        document = BaseController().get_document(index_id, task_id, document_id)

        job = JobFactory.create_job(JobType.SINGLE_CHECK_JOB, job_name, index_id, task_id, document_id,
                                    search_range, document, **cls.get_custom_configs())
        job.start()

        response_data = dict(msg="Job Starting", job_id=job.id)
        return OKResponse(response_data, start_time)
