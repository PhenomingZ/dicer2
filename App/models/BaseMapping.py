from datetime import datetime

from elasticsearch_dsl import Document, Integer, Nested

from App.models.BaseIndexMapping import BaseIndex
from App.responses import ForbiddenAbort


class Base(Document):
    index_count = Integer()
    index = Nested(BaseIndex)

    class Index:
        name = ".dicer2_base"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super(Base, self).save(**kwargs)

    def isExist(self, index_id):
        for index_item in self.index:
            if index_item.id == index_id:
                return True
        return False

    def add_index(self, index_id, **kwargs):
        if self.isExist(index_id):
            ForbiddenAbort(f"Index '{index_id}' is already exist!")

        if index_id[0] == "_":
            ForbiddenAbort(f"Index name can not start with '_'")

        title = kwargs.get("title")

        new_index = BaseIndex(id=index_id, title=title, task_count=0, tasks=[], created_at=datetime.now())
        self.index.append(new_index)

        self.index_count += 1

    def del_index(self, index_id):
        index_loc = self.get_index_loc(index_id)
        self.index.pop(index_loc)
        self.index_count -= 1

    def update_index(self, index_id, **kwargs):
        old_index = self.get_index(index_id)
        index_loc = self.get_index_loc(index_id)

        title = kwargs.get("title")

        if title:
            old_index.title = title

        self.index[index_loc] = old_index

    def get_index(self, index_id):
        for index_loc, index_item in enumerate(self.index):
            if index_item.id == index_id:
                return index_item
        ForbiddenAbort(f"Index '{index_id}' is not exist!")

    def get_index_loc(self, index_id):
        for index_loc, index_item in enumerate(self.index):
            if index_item.id == index_id:
                return index_loc
        ForbiddenAbort(f"Index '{index_id}' is not exist!")
