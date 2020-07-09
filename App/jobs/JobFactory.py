from App.jobs import get_result_queue
from App.jobs.JobProduct import JobSingleProduct, JobMultipleProduct
from App.jobs.JobTypeEnums import JobType
from App.responses import BadRequestAbort


class JobFactory(object):

    @classmethod
    def create_job(cls, job_type, *args):
        queue = get_result_queue()

        if job_type == JobType.SINGLE_CHECK_JOB:
            return JobSingleProduct(job_type=job_type, queue=queue, args=args)
        elif job_type == JobType.MULTIPLE_CHECK_JOB:
            return JobMultipleProduct(job_type=job_type, queue=queue, args=args)
        else:
            BadRequestAbort(f"Job type '{job_type}' is not supported!")
