from App.jobs.JobProduct import JobProduct


class JobMultipleProduct(JobProduct):

    def target(self, q, a, b):
        q.put(1)
        print(a, b)
