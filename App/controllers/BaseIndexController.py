import shutil

from elasticsearch_dsl import Index

from App.controllers.Dicer2Controller import Dicer2Controller
from App.models.ArticleMapping import Article


class BaseIndexController(Dicer2Controller):
    """ 基本Index数据控制器 """

    def create_index(self, index_id, **kwargs):
        """
        创建一个index
        :param index_id: 目标index
        :param kwargs: 创建index所需的其他参数
        :return:
        """
        self.base.add_index(index_id, **kwargs)
        self.base.save()
        Article.init(index=index_id)

    def delete_index(self, index_id):
        """
        删除一个index
        :param index_id: 目标index
        :return:
        """
        self.base.del_index(index_id)
        self.base.save()

        # 删除持久化文件
        storage_path = self.get_storage_path(index_id)
        shutil.rmtree(storage_path, ignore_errors=True)

        # ElasticSearch的Index类，表示直接删除对应的Index
        # 该Index下属的所有Task和Document均被删除
        Index(index_id).delete()

    def update_index(self, index_id, **kwargs):
        """
        更新一个index
        :param index_id: 目标index
        :param kwargs:
        :return:
        """
        self.base.update_index(index_id, **kwargs)
        self.base.save()

    def get_index(self, index_id):
        """
        获取一个index
        :param index_id: 目标index
        :return: 目标index的信息
        """
        return self.base.get_index(index_id)
