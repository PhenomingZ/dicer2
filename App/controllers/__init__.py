import multiprocessing
from App.controllers.BaseController import BaseController
from App.controllers.BaseDocumentController import BaseDocumentController
from App.controllers.BaseIndexController import BaseIndexController
from App.controllers.BaseTaskController import BaseTaskController
from App.controllers.Dicer2Controller import Dicer2Controller

# DICER2 任务进程池
# 每收到一个查重请求将会从进程池中取出一个进程
job_processing_pool = None


def init_job(app):
    global job_processing_pool

    job_processing_pool = multiprocessing.Pool(app.config['JOB_PROCESSING_NUM'])


def get_job_pool():
    return job_processing_pool
