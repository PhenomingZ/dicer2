from App.jobs import get_job_pool


class JobController(object):

    @classmethod
    def add_job(cls, func, args):
        get_job_pool().apply_async(func, args)
