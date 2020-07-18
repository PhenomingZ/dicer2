from elasticsearch_dsl import Document, Text, Keyword, Integer, Boolean


class Article(Document):
    """ 待查文档存入ElasticSearch的字段结构 """

    index = Keyword()
    task = Keyword()
    document = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    doc_id = Keyword()
    part = Integer()
    total = Integer()
    vector = Keyword()
    is_image = Boolean()
    body = Text(analyzer="ik_max_word", search_analyzer="ik_smart")

    class Index:
        name = "default_course"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super(Article, self).save(**kwargs)
