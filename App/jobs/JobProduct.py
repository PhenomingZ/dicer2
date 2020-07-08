from App.jobs import get_job_pool
from App.jobs.JobSingleHandler import job_single_handler


# TODO 加一个消息队列中传递信息的类
class JobProduct(object):
    def __init__(self, args):
        self.args = args

    def target(self, *args):
        pass

    def wrapped_target(self, *args):
        try:
            self.target(*args)
        except Exception as e:
            print(e)

    def start(self):
        get_job_pool().apply_async(self.wrapped_target, self.args)


class JobSingleProduct(JobProduct):
    def target(self, q, index_id, task_id, document_id, search_range, body):
        repetitive_rate, document_result = job_single_handler(index_id, task_id, document_id, search_range, body)
        print(repetitive_rate, document_result)


class JobMultipleProduct(JobProduct):
    def target(self, q, a, b):
        q.put(1)
        print(1 / 0)
        print(a, b)
