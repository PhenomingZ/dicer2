import time
import traceback

from datetime import datetime

from App.controllers import BaseController
from App.jobs import get_job_pool
from App.jobs.JobMultipleHandler import job_multiple_handler
from App.jobs.JobQueuePutter import JobSuccessQueuePutter, JobStartedQueuePutter, JobRunningQueuePutter, \
    JobFailingQueuePutter
from App.jobs.JobSingleHandler import job_single_handler
from App.jobs.JobTypeEnums import JobType
from App.models import BaseTask
from App.settings import get_config


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
            enable_error_traceback = get_config().ENABLE_ERROR_TRACEBACK
            error_msg = traceback.format_exc() if enable_error_traceback else str(e)

            JobFailingQueuePutter(self.id, self.queue, self.start_time).put({
                "progress": 0,
                "job_type": self.job_type,
                "error_msg": error_msg
            }, "Job Failed!")
            print(error_msg)

    def start(self):
        self.start_time = datetime.now()
        JobStartedQueuePutter(self.id, self.queue, self.start_time).put({
            "progress": 0,
            "job_type": self.job_type
        }, "Job Started!")
        get_job_pool().apply_async(self.wrapped_target, self.args)


class JobSingleProduct(JobProduct):
    def target(self, index_id, task_id, document_id, search_range, document):
        JobRunningQueuePutter(self.id, self.queue, self.start_time).put({
            "progress": 0,
            "index": index_id,
            "task": task_id,
            "document": document_id,
            "job_type": JobType.SINGLE_CHECK_JOB
        }, "Single job is running!")
        ret = job_single_handler(index_id, task_id, document_id, search_range, document.body)
        repetitive, result = ret[0], ret[1]
        JobSuccessQueuePutter(self.id, self.queue, self.start_time).put({
            "progress": 1,
            "index": index_id,
            "task": task_id,
            "document": document_id,
            "job_type": JobType.SINGLE_CHECK_JOB,
            "repetitive_rate": repetitive,
            "document_result": result
        }, "Single job finished successfully!")


class JobMultipleProduct(JobProduct):
    total_doc_count = 0
    finished_count = 0
    source_range = None
    search_range = None

    def target(self, source_range, search_range):
        for index_id, tasks in source_range.items():
            for task_id in tasks:
                task_instance: BaseTask = BaseController().get_task(index_id, task_id)
                self.total_doc_count += len(task_instance.docs)

        self.source_range = source_range
        self.search_range = search_range

        job_multiple_handler(self.progress_callback, source_range, search_range)
        JobSuccessQueuePutter(self.id, self.queue, self.start_time).put({
            "progress": 1,
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB
        }, "Multiple job finished successfully!")

    def progress_callback(self, res):
        self.finished_count += 1
        progress = self.finished_count / self.total_doc_count

        result = res.result()
        repetitive_rate = "%.4f" % result[0]
        document_detail = result[3]

        index, task, document = document_detail["index"], document_detail["task"], document_detail["document"]

        progress_str = "Progress: %.2f" % (progress * 100) + "%\t"
        detail_str = f"rep_rate: {repetitive_rate}\tindex: {index}\ttask: {task}\tdocument: {document}"

        JobRunningQueuePutter(self.id, self.queue, self.start_time).put({
            "progress": progress,
            "source_range": self.source_range,
            "search_range": self.search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB
        }, progress_str + detail_str)
