import time

from datetime import datetime

from App.jobs import get_job_pool
from App.jobs.JobMultipleHandler import job_multiple_handler
from App.jobs.JobQueuePutter import JobSuccessQueuePutter, JobStartedQueuePutter, JobRunningQueuePutter, \
    JobFailingQueuePutter
from App.jobs.JobSingleHandler import job_single_handler
from App.jobs.JobTypeEnums import JobType


class JobProduct(object):
    def __init__(self, job_type, queue, args):
        self.id = str(int(time.time() * 1000000))
        self.start_time = None
        self.job_type = job_type
        self.queue = queue
        self.args = args

    def target(self, *args):
        pass

    def wrapped_target(self, *args):
        try:
            self.target(*args)
        except Exception as e:
            JobFailingQueuePutter(self.id, self.queue, self.start_time).put({
                "job_type": self.job_type,
                "error_msg": str(e)
            })
            print(e)

    def start(self):
        self.start_time = datetime.now()
        JobStartedQueuePutter(self.id, self.queue, self.start_time).put({
            "job_type": self.job_type
        })
        get_job_pool().apply_async(self.wrapped_target, self.args)


class JobSingleProduct(JobProduct):
    def target(self, index_id, task_id, document_id, search_range, document):
        JobRunningQueuePutter(self.id, self.queue, self.start_time).put({
            "index": index_id,
            "task": task_id,
            "document": document_id,
            "job_type": JobType.SINGLE_CHECK_JOB
        })
        repetitive, result = job_single_handler(index_id, task_id, document_id, search_range, document.body)
        JobSuccessQueuePutter(self.id, self.queue, self.start_time).put({
            "index": index_id,
            "task": task_id,
            "document": document_id,
            "job_type": JobType.SINGLE_CHECK_JOB,
            "repetitive_rate": repetitive,
            "document_result": result
        })


class JobMultipleProduct(JobProduct):
    def target(self, source_range, search_range):
        JobRunningQueuePutter(self.id, self.queue, self.start_time).put({
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB
        })
        job_multiple_handler(source_range, search_range)
        JobSuccessQueuePutter(self.id, self.queue, self.start_time).put({
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB
        })
