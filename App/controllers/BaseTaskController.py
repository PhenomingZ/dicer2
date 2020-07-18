import shutil

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from App.controllers.BaseIndexController import BaseIndexController
from App.responses import NotFoundAbort


class BaseTaskController(BaseIndexController):
    @classmethod
    def clear_all_docs(cls, index_id, task_id):
        """
        删除一个task下的全部document
        :param index_id: 目标index
        :param task_id: 目标task
        :return:
        """
        try:
            Search(index=index_id).query("match", task=task_id).delete()
        except NotFoundError:
            NotFoundAbort(f"Task '{index_id}/{task_id}' is not exist!")

    def create_task(self, index_id, task_id, **kwargs):
        """
        创建一个task
        :param index_id: 目标index
        :param task_id: 目标task
        :param kwargs: 创建task所需的其他参数
        :return:
        """
        index_instance = self.get_index(index_id)
        index_instance.add_task(task_id, **kwargs)
        self.base.save()

    def delete_task(self, index_id, task_id):
        """
        删除一个task
        :param index_id: 目标index
        :param task_id: 目标task
        :return:
        """
        index_instance = self.get_index(index_id)
        index_instance.del_task(task_id)

        # 删除持久化文件
        storage_path = self.get_storage_path(index_id, task_id)
        shutil.rmtree(storage_path, ignore_errors=True)

        self.clear_all_docs(index_id, task_id)
        self.base.save()

    def update_task(self, index_id, task_id, **kwargs):
        """
        更新一个task
        :param index_id: 目标index
        :param task_id: 目标task
        :param kwargs: 更新task所需的其他参数
        :return:
        """
        index_instance = self.get_index(index_id)
        index_instance.update_task(task_id, **kwargs)
        self.base.save()

    def get_task(self, index_id, task_id):
        """
        获取一个task的信息
        :param index_id: 目标index
        :param task_id: 目标task
        :return: 目标task的信息
        """
        index_instance = self.get_index(index_id)
        return index_instance.get_task(task_id)
