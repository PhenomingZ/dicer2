from datetime import datetime

from App.jobs.JobError import JobError
from App.jobs.JobTypeEnums import JobStatus


class QueueMessage(object):
    def __init__(self, job_id, start_time, job_status, data=None):
        self.id = job_id
        self.took = int((datetime.now() - start_time).total_seconds() * 1000)
        self.status = job_status
        self.data = data
        self.msg = "no message"

    def to_dict(self):
        return self.__dict__


class JobQueuePutter(object):
    def __init__(self, job_id, queue, start_time):
        self.queue = queue

        if not self.queue:
            raise JobError("There is no available queue for this job")

        self.meta = QueueMessage(job_id, start_time, JobStatus.DEFAULT)

    def put(self, data, msg=None):
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
