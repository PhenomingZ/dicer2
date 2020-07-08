from datetime import datetime
from enum import Enum

from App.jobs import get_result_queue
from App.jobs.JobError import JobError


class JobMessageType(Enum):
    DEFAULT = "default"
    SUCCESS = "success"
    WAITING = "waiting"
    RUNNING = "running"
    WARNING = "warning"
    FAILING = "failing"


class JobQueuePutter(object):
    def __init__(self, start_time, queue=None):
        if not queue:
            self.queue = get_result_queue()
        else:
            self.queue = queue

        if not queue:
            raise JobError("There is no available queue for this job")

        self.meta = {
            "took": int((datetime.now() - start_time).total_seconds() * 1000),
            "type": JobMessageType.DEFAULT,
            "data": None
        }

    def put(self, data):
        self.meta["data"] = data
        self.queue.put(self.meta)


class JobSuccessQueuePutter(JobQueuePutter):
    def __init__(self, start_time, queue=None):
        super().__init__(start_time, queue)
        self.meta["type"] = JobMessageType.SUCCESS


class JobWaitingQueuePutter(JobQueuePutter):
    def __init__(self, start_time, queue=None):
        super().__init__(start_time, queue)
        self.meta["type"] = JobMessageType.WAITING


class JobRunningQueuePutter(JobQueuePutter):
    def __init__(self, start_time, queue=None):
        super().__init__(start_time, queue)
        self.meta["type"] = JobMessageType.RUNNING


class JobWarningQueuePutter(JobQueuePutter):
    def __init__(self, start_time, queue=None):
        super().__init__(start_time, queue)
        self.meta["type"] = JobMessageType.WARNING


class JobFailingQueuePutter(JobQueuePutter):
    def __init__(self, start_time, queue=None):
        super().__init__(start_time, queue)
        self.meta["type"] = JobMessageType.FAILING
