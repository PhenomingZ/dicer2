from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from App.controllers.BaseIndexController import BaseIndexController
from App.responses import NotFoundAbort


class BaseTaskController(BaseIndexController):
    @classmethod
    def clear_all_docs(cls, index_id, task_id):
        try:
            Search(index=index_id).query("match", task=task_id).delete()
        except NotFoundError:
            NotFoundAbort(f"Task '{index_id}/{task_id}' is not exist!")

    def create_task(self, index_id, task_id, **kwargs):
        index_instance = self.get_index(index_id)
        index_instance.add_task(task_id, **kwargs)
        self.base.save()

    def delete_task(self, index_id, task_id):
        index_instance = self.get_index(index_id)
        index_instance.del_task(task_id)
        self.clear_all_docs(index_id, task_id)
        self.base.save()

    def update_task(self, index_id, task_id, **kwargs):
        index_instance = self.get_index(index_id)
        index_instance.update_task(task_id, **kwargs)
        self.base.save()

    def get_task(self, index_id, task_id):
        index_instance = self.get_index(index_id)
        return index_instance.get_task(task_id)
