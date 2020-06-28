from elasticsearch_dsl import Document, Text, Keyword, Integer, Boolean


# 该类用于指定待查文档存入ElasticSearch包含的字段
class Article(Document):
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
