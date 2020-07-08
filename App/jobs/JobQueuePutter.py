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


class JobQueuePutter(object):
    def __init__(self, job_id, queue, start_time):
        self.queue = queue

        if not self.queue:
            raise JobError("There is no available queue for this job")

        self.meta = {
            "id": job_id,
            "took": int((datetime.now() - start_time).total_seconds() * 1000),
            "type": JobMessageType.DEFAULT,
            "data": None
        }

    def put(self, data):
        self.meta["data"] = data
        self.queue.put(self.meta)


class JobStartedQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.STARTED


class JobSuccessQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.SUCCESS


class JobWaitingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.WAITING


class JobRunningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.RUNNING


class JobWarningQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.WARNING


class JobFailingQueuePutter(JobQueuePutter):
    def __init__(self, job_id, start_time, queue=None):
        super().__init__(job_id, start_time, queue)
        self.meta["type"] = JobMessageType.FAILING
