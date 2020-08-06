from datetime import datetime

from elasticsearch_dsl import Document, Integer, Nested

from App.models.BaseIndexMapping import BaseIndex
from App.responses import forbidden_abort, not_found_abort


class Base(Document):
    """ 基本信息数据库'.dicer2_base'的字段结构和操作方法 """

    index_count = Integer()
    index = Nested(BaseIndex)

    class Index:
        name = ".dicer2_base"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        """
        保存数据库改动
        :param kwargs: 保存时需要的其他字段
        :return:
        """

        return super(Base, self).save(**kwargs)

    def isExist(self, index_id):
        """
        判断在'.dicer2_base'中某个index是否存在
        :param index_id: 目标index
        :return:
        """

        for index_item in self.index:
            if index_item.id == index_id:
                return True
        return False

    def add_index(self, index_id, **kwargs):
        """
        向'.dicer2_base'中添加一个index
        :param index_id: 目标index
        :param kwargs: 添加index所需的其他字段
        :return:
        """

        if self.isExist(index_id):
            forbidden_abort(f"Index '{index_id}' is already exist!")

        if index_id[0] == "_":
            forbidden_abort(f"Index name can not start with '_'")

        title = kwargs.get("title")
        desc = kwargs.get("desc")

        new_index = BaseIndex(id=index_id, title=title, desc=desc, task_count=0, tasks=[], created_at=datetime.now())
        self.index.append(new_index)

        self.index_count += 1

    def del_index(self, index_id):
        """
        从'.dicer2_base'中删除一个index
        :param index_id: 目标index
        :return:
        """

        index_loc = self.get_index_loc(index_id)
        self.index.pop(index_loc)
        self.index_count -= 1

    def update_index(self, index_id, **kwargs):
        """
        向'.dicer2_base'中更新一个index
        :param index_id: 目标index
        :param kwargs: 更新index所需的其他字段
        :return:
        """

        old_index = self.get_index(index_id)
        index_loc = self.get_index_loc(index_id)

        title = kwargs.get("title")
        desc = kwargs.get("desc")

        if title:
            old_index.title = title

        if desc:
            old_index.desc = desc

        self.index[index_loc] = old_index

    def get_index(self, index_id):
        """
        从'.dicer2_base'中获取index对象
        :param index_id: 目标index
        :return: index的信息
        """

        for index_loc, index_item in enumerate(self.index):
            if index_item.id == index_id:
                return index_item
        not_found_abort(f"Index '{index_id}' is not exist!")

    def get_index_loc(self, index_id):
        """
        从'.dicer2_base'中获取一个index的索引位置
        :param index_id: 目标index
        :return: index的索引位置
        """

        for index_loc, index_item in enumerate(self.index):
            if index_item.id == index_id:
                return index_loc
        not_found_abort(f"Index '{index_id}' is not exist!")
