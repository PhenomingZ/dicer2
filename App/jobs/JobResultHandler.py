import os

from App.jobs.JobQueuePutter import QueueMessage, JobMessageType
from App.settings import get_config


def result_handler(result_queue):
    while True:
        job_result: QueueMessage = result_queue.get()

        store_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")
        os.makedirs(store_path, exist_ok=True)

        if job_result.type == JobMessageType.STARTED:
            print(f"Job '{job_result.id}' has started!")
            # TODO 在store路径下记录任务日志

        elif job_result.type == JobMessageType.SUCCESS:
            print(f"Job '{job_result.id}' has finished successfully!")
