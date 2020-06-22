from elasticsearch_dsl import Document, Text, Keyword, Integer


# 该类用于指定待查文档存入ElasticSearch包含的字段
class Article(Document):
    index = Keyword()
    task = Keyword()
    document = Keyword()
    doc_id = Keyword()
    part = Integer()
    total = Integer()
    vector = Keyword()
    tags = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    body = Text(analyzer="ik_max_word", search_analyzer="ik_smart")

    class Index:
        name = "default_course"
        settings = {
            "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super(Article, self).save(**kwargs)
