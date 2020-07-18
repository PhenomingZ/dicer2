from datetime import datetime

from App.jobs.JobError import JobError
from App.jobs.JobTypeEnums import JobStatus


class QueueMessage(object):
    """ 消息队列信息类 """

    def __init__(self, job_id, start_time, job_status, data=None):
        """
        初始化消息队列信息实例
        :param job_id: 任务的id
        :param start_time: 任务开始时间
        :param job_status: 任务的状态
        :param data: 消息携带的数据
        """
        self.id = job_id
        self.took = int((datetime.now() - start_time).total_seconds() * 1000)
        self.status = job_status
        self.data = data
        self.msg = "no message"

    def to_dict(self):
        """
        将类属性转化为字典对象
        :return: 类属性的字典对象
        """
        return self.__dict__


class JobQueuePutter(object):
    """ 消息队列通用添加器 """

    def __init__(self, job_id, queue, start_time):
        """
        初始化meta信息
        :param job_id: 任务id
        :param queue: 任务所用的消息队列对象
        :param start_time: 任务开始的时间
        """

        self.queue = queue

        if not self.queue:
            raise JobError("There is no available queue for this job")

        self.meta = QueueMessage(job_id, start_time, JobStatus.DEFAULT)

    def put(self, data, msg=None):
        """
        向消息队列中发送数据
        :param data: 消息队列中携带的数据
        :param msg: 发送的备注信息，会显示在控制台
        :return:
        """

        self.meta.data = data
        if msg:
            self.meta.msg = msg

        self.queue.put(self.meta)


class JobStartedQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.STARTED


class JobSuccessQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.SUCCESS


class JobWaitingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.WAITING


class JobRunningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.RUNNING


class JobWarningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.WARNING


class JobFailingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, queue, start_time):
        super().__init__(job_id, queue, start_time)
        self.meta.status = JobStatus.FAILING
