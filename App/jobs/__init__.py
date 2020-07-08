import multiprocessing

from App.jobs.JobResultHandler import result_handler

# 初始化进程池
job_processing_pool = None

# 初始化消息队列
result_queue = None


def init_job(app):
    global job_processing_pool
    job_processing_pool = multiprocessing.Pool(app.config['JOB_PROCESSING_NUM'] + 1)

    global result_queue
    result_queue = multiprocessing.Manager().Queue()

    # 创建监听进程，用于监听是否有任务完成并返回结果
    job_processing_pool.apply_async(result_handler, (result_queue,))


def get_job_pool():
    return job_processing_pool


def get_result_queue():
    return result_queue
