from App.apis.SearchResource import SearchResource
from App.jobs import get_result_queue
from App.jobs.JobController import JobController


def test(result_queue, a):
    result_queue.put(a)


class MultipleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        result_queue = get_result_queue()

        JobController.add_job(test, (result_queue, 1))
        return {"mag": "success"}
