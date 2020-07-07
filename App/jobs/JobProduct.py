from App.jobs import get_job_pool


class JobProduct(object):
    def __init__(self, args):
        self.args = args

    def target(self, **kwargs):
        pass

    def start(self):
        get_job_pool().apply_async(self.target, self.args)
