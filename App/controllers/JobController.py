from App.controllers import get_job_pool
import time


def test():
    print("123")
    time.sleep(10)
    print("Job finish")


class JobController(object):

    @classmethod
    def add_job(cls):
        get_job_pool().apply_async(test)
