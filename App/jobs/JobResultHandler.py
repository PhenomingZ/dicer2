import os

from App.settings import get_config
from App.jobs.JobQueuePutter import QueueMessage
from App.jobs.JobTypeEnums import JobStatus
from App.utils.DateEncoder import Dicer2Encoder


def result_handler(result_queue):
    """
    消息队列中消息处理函数
    :param result_queue: 使用的消息队列对象
    :return:
    """

    while True:
        job_result: QueueMessage = result_queue.get()

        store_folder_path = os.path.join(get_config().DICER2_STORAGE_PATH, "_jobs")
        store_job_path = os.path.join(store_folder_path, job_result.id + ".json")
        os.makedirs(store_folder_path, exist_ok=True)

        msg = job_result.msg
        try:
            if job_result.status == JobStatus.STARTED:
                print(f"[STARTED] Job ID: '{job_result.id}' msg: {msg}")
            elif job_result.status == JobStatus.SUCCESS:
                print(f"[SUCCESS] Job ID: '{job_result.id}' msg: {msg}")
            elif job_result.status == JobStatus.WAITING:
                print(f"[WAITING] Job ID: '{job_result.id}' msg: {msg}")
            elif job_result.status == JobStatus.RUNNING:
                print(f"[RUNNING] Job ID: '{job_result.id}' msg: {msg}")
            elif job_result.status == JobStatus.WARNING:
                print(f"[WARNING] Job ID: '{job_result.id}' msg: {msg}")
            elif job_result.status == JobStatus.FAILING:
                print(f"[FAILING] Job ID: '{job_result.id}' msg: {msg}")

            Dicer2Encoder.save(store_job_path, job_result.to_dict())
        except Exception as e:
            print(f"[FAILING] Error occurred when saving log for job '{job_result.id}'")
            print(e)
