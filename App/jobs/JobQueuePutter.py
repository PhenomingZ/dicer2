from datetime import datetime
from enum import Enum

from App.jobs.JobError import JobError


class JobMessageType(Enum):
    DEFAULT = "default"
    STARTED = "started"
    SUCCESS = "success"
    WAITING = "waiting"
    RUNNING = "running"
    WARNING = "warning"
    FAILING = "failing"


class QueueMessage(object):
    def __init__(self, job_id, start_time, job_type, data=None):
        self.id = job_id
        self.took = int((datetime.now() - start_time).total_seconds() * 1000),
        self.type = job_type
        self.data = data


class JobQueuePutter(object):
    def __init__(self, job_id, queue, start_time):
        self.queue = queue

        if not self.queue:
            raise JobError("There is no available queue for this job")

        self.meta = QueueMessage(job_id, start_time, JobMessageType.DEFAULT)

    def put(self, data):
        self.meta.data = data
        self.queue.put(self.meta)


class JobStartedQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.STARTED


class JobSuccessQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.SUCCESS


class JobWaitingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.WAITING


class JobRunningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.RUNNING


class JobWarningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.WARNING


class JobFailingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta.type = JobMessageType.FAILING
