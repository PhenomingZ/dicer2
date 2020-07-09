from enum import Enum


class JobStatus(Enum):
    DEFAULT = "default"
    STARTED = "started"
    SUCCESS = "success"
    WAITING = "waiting"
    RUNNING = "running"
    WARNING = "warning"
    FAILING = "failing"


class JobType(Enum):
    SINGLE_CHECK_JOB = "single"
    MULTIPLE_CHECK_JOB = "multiple"
