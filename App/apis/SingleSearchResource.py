from datetime import datetime

from App.apis.SearchResource import SearchResource
from App.controllers import BaseController
from App.jobs.JobFactory import JobFactory
from App.jobs.JobTypeEnums import JobType
from App.responses import OKResponse


class SingleSearchResource(SearchResource):

    @classmethod
    def post(cls):
        start_time = datetime.now()

        index_id = cls.get_parameter("index", required=True, location=["json", "form"])
        task_id = cls.get_parameter("task", required=True, location=["json", "form"])
        document_id = cls.get_parameter("document", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        document = BaseController().get_document(index_id, task_id, document_id)

        job = JobFactory.create_job(JobType.SINGLE_CHECK_JOB, index_id, task_id, document_id, search_range, document)
        job.start()

        response_data = dict(msg="Job Starting", job_id=job.id)
        return OKResponse(response_data, start_time)
