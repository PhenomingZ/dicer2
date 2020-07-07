from App.apis.SearchResource import SearchResource
from App.controllers.JobController import JobController


class MultipleSearchResource(SearchResource):

    @classmethod
    def get(cls):
        JobController.add_job()
