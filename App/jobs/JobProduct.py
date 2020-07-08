import time

from datetime import datetime
from enum import Enum

from App.jobs import get_job_pool
from App.jobs.JobQueuePutter import JobSuccessQueuePutter, JobStartedQueuePutter
from App.jobs.JobSingleHandler import job_single_handler


class JobType(Enum):
    SINGLE_CHECK_JOB = "single"
    MULTIPLE_CHECK_JOB = "multiple"


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
            print(e)

    def start(self):
        self.start_time = datetime.now()
        JobStartedQueuePutter(self.id, self.queue, self.start_time).put({
            "job_type": JobType.SINGLE_CHECK_JOB
        })
        get_job_pool().apply_async(self.wrapped_target, self.args)


class JobSingleProduct(JobProduct):
    def target(self, index_id, task_id, document_id, search_range, document):
        result = job_single_handler(index_id, task_id, document_id, search_range, document.body)
        repetitive_rate, document_result = result
        JobSuccessQueuePutter(self.id, self.queue, self.start_time).put({
            "title": document.title,
            "job_type": JobType.SINGLE_CHECK_JOB,
            "repetitive_rate": repetitive_rate,
            "document_result": document_result
        })


class JobMultipleProduct(JobProduct):
    def target(self, q, a, b):
        q.put(1)
        print(1 / 0)
        print(a, b)
