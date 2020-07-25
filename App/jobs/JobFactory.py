from App.jobs import get_result_queue
from App.jobs.JobProduct import JobSingleProduct, JobMultipleProduct
from App.jobs.JobTypeEnums import JobType
from App.responses import bad_request_abort


class JobFactory(object):
    """ 创建Job的工厂类 """

    @classmethod
    def create_job(cls, job_type, job_name=None, *args, **kwargs):
        """
        创建一个任务对象
        :param job_type: Job的类型
        :param job_name: Job的名称
        :param args: 执行Job所需的参数
        :return: 对应的Job产品对象
        """

        queue = get_result_queue()

        if job_type == JobType.SINGLE_CHECK_JOB:

            if not job_name:
                job_name = "New Single Document Check Job"

            return JobSingleProduct(job_type=job_type, job_name=job_name, queue=queue, args=args, kwargs=kwargs)
        elif job_type == JobType.MULTIPLE_CHECK_JOB:

            if not job_name:
                job_name = "New Multiple Documents Check Job"

            return JobMultipleProduct(job_type=job_type, job_name=job_name, queue=queue, args=args, kwargs=kwargs)
        else:
            bad_request_abort(f"Job type '{job_type}' is not supported!")
