import os
import traceback

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

        # 当线程池中已经有多个任务在进行时，其中某一个线程报错导致整个查重任务停止后，
        # 后续的成功线程写入的进度信息会覆盖掉错误信息，所以在写入之前要先检查任务是否已经失败
        try:
            pre_result_data = Dicer2Encoder.load(store_job_path)
            status = pre_result_data.get("status")

            if status == "failing":
                continue

        except FileNotFoundError:
            pass

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
            enable_error_traceback = get_config().ENABLE_ERROR_TRACEBACK
            error_msg = traceback.format_exc() if enable_error_traceback else str(e)

            print(f"[FAILING] Error occurred when saving log for job '{job_result.id}'")
            print(error_msg)
