from enum import Enum


class JobStatus(Enum):
    """ 任务执行状态枚举类 """

    DEFAULT = "default"
    STARTED = "started"
    SUCCESS = "success"
    WAITING = "waiting"
    RUNNING = "running"
    WARNING = "warning"
    FAILING = "failing"


class JobType(Enum):
    """ 任务类型枚举类 """

    SINGLE_CHECK_JOB = "single"
    MULTIPLE_CHECK_JOB = "multiple"
