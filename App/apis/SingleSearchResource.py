from datetime import datetime

from App.apis.SearchResource import SearchResource
from App.controllers import BaseController
from App.jobs import get_result_queue
from App.jobs.JobFactory import JobFactory, JobType
from App.responses import OKResponse


class SingleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        start_time = datetime.now()

        index_id = cls.get_parameter("index", required=True, location=["json", "form"])
        task_id = cls.get_parameter("task", required=True, location=["json", "form"])
        document_id = cls.get_parameter("document", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        document = BaseController().get_document(index_id, task_id, document_id)
        body = document.body

        # response_data = dict(index=index_id, task=task_id, document=document_id, title=document.title,
        #                      repetitive_rate=repetitive_rate, result=document_result)

        request_queue = get_result_queue()
        job_type = JobType.SINGLE_CHECK_JOB
        job = JobFactory.create_job(job_type, request_queue, index_id, task_id, document_id, search_range, body)
        job.start()

        response_data = dict(index=index_id, task=task_id, document=document_id, title=document.title)
        return OKResponse(response_data, start_time)
