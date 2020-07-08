from enum import Enum

from App.jobs.JobProduct import JobSingleProduct, JobMultipleProduct
from App.responses import BadRequestAbort


class JobType(Enum):
    SINGLE_CHECK_JOB = "single"
    MULTIPLE_CHECK_JOB = "multiple"


class JobFactory(object):

    @classmethod
    def create_job(cls, job_type, *args):
        if job_type == JobType.SINGLE_CHECK_JOB:
            return JobSingleProduct(args)
        elif job_type == JobType.MULTIPLE_CHECK_JOB:
            return JobMultipleProduct(args)
        else:
            BadRequestAbort(f"Job type '{job_type}' is not supported!")
