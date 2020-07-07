import multiprocessing
import time

# DICER2 任务进程池
# 每收到一个查重请求将会从进程池中取出一个进程
job_processing_pool = None

# 查重结果均放入消息队列
search_result_queue = None


# 创建一个用于接收结果的进程
def result_handler(result_queue):
    while True:
        search_result = result_queue.get()

        # 查重结果处理
        print(search_result)
        print("处理完毕")


def init_job(app):
    global job_processing_pool
    global search_result_queue

    job_processing_pool = multiprocessing.Pool(app.config['JOB_PROCESSING_NUM'])
    search_result_queue = multiprocessing.Manager().Queue()

    job_processing_pool.apply_async(result_handler, (search_result_queue,))


def get_job_pool():
    return job_processing_pool


def get_result_queue():
    return search_result_queue
