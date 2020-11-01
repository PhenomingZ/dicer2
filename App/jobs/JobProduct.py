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
from App.models.BaseTaskMapping import BaseTask
from App.settings import get_config


class JobProduct(object):
    def __init__(self, job_type, job_name, queue, args, kwargs):
        """
        初始化Job对象
        :param job_type: Job的类别
        :param job_name: Job的名称
        :param queue: 当前Job要使用的消息队列对象
        :param args: 当前Job要执行的任务需要传入的参数，需以元组的形式传入
        """
        self.id = str(int(time.time() * 1000000))
        self.start_time = None
        self.job_type = job_type
        self.name = job_name
        self.queue = queue
        self.args = args
        self.kwargs = kwargs

        self.source_range = {}
        self.search_range = {}

    def target(self, *args, **kwargs):
        """
        需由子类重写，该Job待执行的任务
        :param args: 当前Job要执行的任务需要传入的参数，需以元组展开的形式传入
        :param kwargs: 当前Job要执行的任务需要传入的参数，需以键值对展开的形式传入
        :return: 返回值由子类定义
        """
        pass

    def wrapped_target(self, *args, **kwargs):
        """
        用于获取子进程中的异常的装饰方法，也是实际传入子进程的方法
        :param args: 当前Job要执行的任务需要传入的参数，需以元组展开的形式传入
        :param kwargs: 当前Job要执行的任务需要传入的参数，需以键值对展开的形式传入
        :return:
        """
        try:
            self.target(*args, **kwargs)
        except Exception as e:
            enable_error_traceback = get_config().ENABLE_ERROR_TRACEBACK
            error_msg = traceback.format_exc() if enable_error_traceback else str(e)

            JobFailingQueuePutter(self.id, self.name, self.queue, self.start_time).put({
                "progress": 0,
                "source_range": self.source_range,
                "search_range": self.search_range,
                "job_type": self.job_type,
                "config": self.kwargs,
                "error_msg": error_msg
            }, "Job Failed!")
            print(error_msg)

    def start(self):
        """
        创建子进程，开始一项Job
        :return:
        """
        self.start_time = datetime.now()
        JobStartedQueuePutter(self.id, self.name, self.queue, self.start_time).put({
            "progress": 0,
            "source_range": self.source_range,
            "search_range": self.search_range,
            "job_type": self.job_type,
            "config": self.kwargs,
        }, "Job Started!")
        get_job_pool().apply_async(self.wrapped_target, self.args, self.kwargs)


class JobSingleProduct(JobProduct):
    """ 单文档查重的JobProduct子类 """

    def target(self, index_id, task_id, document_id, search_range, document, **kwargs):
        """
        单独查重任务的执行函数
        :param index_id: 被查重文档所属index
        :param task_id: 被查重文档所属task
        :param document_id: 被查重文档的id
        :param search_range: 查重范围
        :param document: 被查重文档的BaseDocumentMapping对象
        :return:
        """
        source_range = {
            index_id: [task_id]
        }
        JobRunningQueuePutter(self.id, self.name, self.queue, self.start_time).put({
            "progress": 0,
            "document": document_id,
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.SINGLE_CHECK_JOB,
            "config": self.kwargs
        }, "Single job is running!")
        ret = job_single_handler(index_id, task_id, document_id, search_range, document.body, **kwargs)
        repetitive, result = ret[0], ret[1]
        JobSuccessQueuePutter(self.id, self.name, self.queue, self.start_time).put({
            "progress": 1,
            "document": document_id,
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.SINGLE_CHECK_JOB,
            "config": self.kwargs,
            "repetitive_rate": repetitive,
            "document_result": result
        }, "Single job finished successfully!")


class JobMultipleProduct(JobProduct):
    """ 联合文档查重的JobProduct子类 """

    total_doc_count = 0
    finished_count = 0

    def target(self, source_range, search_range, **kwargs):
        """
        联合文档查重的执行函数
        :param source_range: 被查重文档的范围，精确到task
        :param search_range: 查重范围
        :return:
        """
        for index_id, tasks in source_range.items():
            for task_id in tasks:
                task_instance: BaseTask = BaseController().get_task(index_id, task_id)
                self.total_doc_count += len(task_instance.docs)

        self.source_range = source_range
        self.search_range = search_range

        res = job_multiple_handler(self.progress_callback, source_range, search_range, **kwargs)

        JobSuccessQueuePutter(self.id, self.name, self.queue, self.start_time).put({
            "progress": 1,
            "source_range": source_range,
            "search_range": search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB,
            "config": self.kwargs,
            "result_summary": res[0],
            "cluster_list": res[1]
        }, "Multiple job finished successfully!")

    def progress_callback(self, res):
        """
        作为联合查重每个线程的回调函数，负责将任务进度记录发送给消息队列
        :param res: 单个任务线程的返回值
        :return:
        """
        self.finished_count += 1
        progress = self.finished_count / self.total_doc_count

        result = res.result()
        repetitive_rate = "%.4f" % result[0]
        document_detail = result[3]

        index, task, document = document_detail["index"], document_detail["task"], document_detail["document"]

        progress_str = "Progress: %.2f" % (progress * 100) + "%\t"
        detail_str = f"rep_rate: {repetitive_rate}\tindex: {index}\ttask: {task}\tdocument: {document}"

        JobRunningQueuePutter(self.id, self.name, self.queue, self.start_time).put({
            "progress": progress,
            "source_range": self.source_range,
            "search_range": self.search_range,
            "job_type": JobType.MULTIPLE_CHECK_JOB,
            "config": self.kwargs
        }, progress_str + detail_str)
