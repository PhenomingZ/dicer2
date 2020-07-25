import multiprocessing

from App.jobs.JobResultHandler import result_handler

# 初始化进程池
from App.settings import get_config

job_processing_pool = None

# 初始化消息队列
result_queue = None


def init_job():
    """
    初始化Job模块
    :return:
    """

    global job_processing_pool
    job_processing_pool = multiprocessing.Pool(get_config().JOB_PROCESSING_NUM)

    global result_queue
    result_queue = multiprocessing.Manager().Queue()

    # 创建监听进程，用于监听是否有任务完成并返回结果
    job_processing_pool.apply_async(result_handler, (result_queue,))


def get_job_pool():
    """
    获取进程池对象
    :return: 进程池对象
    """
    return job_processing_pool


def get_result_queue():
    """
    获取消息队列对象
    :return: 消息队列对象
    """
    return result_queue
