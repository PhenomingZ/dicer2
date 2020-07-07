from App.apis.SearchResource import SearchResource
from App.jobs import get_result_queue
from App.jobs.JobMultipleProduct import JobMultipleProduct


class MultipleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        request_queue = get_result_queue()

        JobMultipleProduct((request_queue, 1, 2)).start()

        return {"mag": "success"}
