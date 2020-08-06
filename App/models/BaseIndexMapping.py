from datetime import datetime

from elasticsearch_dsl import InnerDoc, Keyword, Text, Integer, Nested, Date

from App.models.BaseTaskMapping import BaseTask
from App.responses import not_found_abort, forbidden_abort


class BaseIndex(InnerDoc):
    """ Index信息存入'.dicer2_base'的字段结构和操作方法 """

    id = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    desc = Text()
    task_count = Integer()
    tasks = Nested(BaseTask)
    created_at = Date()

    def isExist(self, task_id):
        """
        判断'.dicer2_base'当前index对象中某个task是否存在
        :param task_id: 目标task
        :return:
        """

        for task_item in self.tasks:
            if task_item.id == task_id:
                return True
        return False

    def add_task(self, task_id, **kwargs):
        """
        向'.dicer2_base'当前index对象中添加一个task
        :param task_id: 目标task
        :param kwargs: 添加task所需的其他字段
        :return:
        """

        if self.isExist(task_id):
            forbidden_abort(f"Task '{task_id}' is already exist!")

        if task_id[0] == "_":
            forbidden_abort(f"Task name can not start with '_'")

        title = kwargs.get("title")
        desc = kwargs.get("desc")

        new_task = BaseTask(id=task_id, title=title, desc=desc, doc_count=0, docs=[], created_at=datetime.now())
        self.tasks.append(new_task)

        self.task_count += 1

    def del_task(self, task_id):
        """
        从'.dicer2_base'当前index对象中删除一个task
        :param task_id: 目标task
        :return:
        """
        task_loc = self.get_task_loc(task_id)
        self.tasks.pop(task_loc)
        self.task_count -= 1

    def update_task(self, task_id, **kwargs):
        """
        从'.dicer2_base'当前index对象中更新一个task
        :param task_id: 目标task
        :param kwargs: 更新task所需的其他字段
        :return:
        """

        old_task = self.get_task(task_id)
        task_loc = self.get_task_loc(task_id)

        title = kwargs.get("title")
        desc = kwargs.get("desc")

        if title:
            old_task.title = title

        if desc:
            old_task.desc = desc

        self.tasks[task_loc] = old_task

    def get_task(self, task_id):
        """
        从'.dicer2_base'当前index对象中获取task对象
        :param task_id: 目标task
        :return: task信息
        """

        for task_loc, task_item in enumerate(self.tasks):
            if task_item.id == task_id:
                return task_item
        not_found_abort(f"Task '{task_id}' is not exist!")

    def get_task_loc(self, task_id):
        """
        从'.dicer2_base'当前index对象中获取一个task的索引位置
        :param task_id: 目标task
        :return: task索引位置
        """

        for task_loc, task_item in enumerate(self.tasks):
            if task_item.id == task_id:
                return task_loc
        not_found_abort(f"Task '{task_id}' is not exist!")
