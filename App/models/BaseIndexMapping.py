from datetime import datetime

from elasticsearch_dsl import InnerDoc, Keyword, Text, Integer, Nested, Date

from App.models.BaseTaskMapping import BaseTask
from App.responses import ForbiddenAbort


class BaseIndex(InnerDoc):
    id = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    task_count = Integer()
    tasks = Nested(BaseTask)
    created_at = Date()

    def isExist(self, task_id):
        for task_item in self.tasks:
            if task_item.id == task_id:
                return True
        return False

    def add_task(self, task_id, **kwargs):
        if self.isExist(task_id):
            ForbiddenAbort(f"Task '{task_id}' is already exist!")

        title = kwargs.get("title")

        new_task = BaseTask(id=task_id, title=title, doc_count=0, docs=[], created_at=datetime.now())
        self.tasks.append(new_task)

        self.task_count += 1

    def del_task(self, task_id):
        task_loc = self.get_task_loc(task_id)
        self.tasks.pop(task_loc)
        self.task_count -= 1

    def update_task(self, task_id, **kwargs):
        old_task = self.get_task(task_id)
        task_loc = self.get_task_loc(task_id)

        title = kwargs.get("title")

        if title:
            old_task.title = title

        self.tasks[task_loc] = old_task

    def get_task(self, task_id):
        for task_loc, task_item in enumerate(self.tasks):
            if task_item.id == task_id:
                return task_item
        ForbiddenAbort(f"Task '{task_id}' is not exist!")

    def get_task_loc(self, task_id):
        for task_loc, task_item in enumerate(self.tasks):
            if task_item.id == task_id:
                return task_loc
        ForbiddenAbort(f"Task '{task_id}' is not exist!")
