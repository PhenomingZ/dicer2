from App.apis.SearchResource import SearchResource
from App.jobs import get_result_queue
from App.jobs.JobFactory import JobFactory, JobType


class MultipleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        request_queue = get_result_queue()

        job = JobFactory.create_job(JobType.MULTIPLE_CHECK_JOB, request_queue, 1, 2)
        job.start()

        return {"mag": "success"}
