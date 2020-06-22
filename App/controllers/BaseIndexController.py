from elasticsearch_dsl import Index

from App.controllers.Dicer2Controller import Dicer2Controller
from App.models.ArticleMapping import Article


class BaseIndexController(Dicer2Controller):

    def create_index(self, index_id, **kwargs):
        self.base.add_index(index_id, **kwargs)
        self.base.save()
        Article.init(index=index_id)

    def delete_index(self, index_id):
        self.base.del_index(index_id)
        self.base.save()
        Index(index_id).delete()

    def update_index(self, index_id, **kwargs):
        self.base.update_index(index_id, **kwargs)
        self.base.save()

    def get_index(self, index_id):
        return self.base.get_index(index_id)
