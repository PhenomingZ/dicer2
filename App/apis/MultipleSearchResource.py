from datetime import datetime

from App.apis.SearchResource import SearchResource
from App.jobs.JobFactory import JobFactory
from App.jobs.JobTypeEnums import JobType
from App.responses import OKResponse


class MultipleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        start_time = datetime.now()

        job = JobFactory.create_job(JobType.MULTIPLE_CHECK_JOB, 1, 2)
        job.start()

        response_data = dict(msg="Job Starting", job_id=job.id)
        return OKResponse(response_data, start_time)
