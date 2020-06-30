from elasticsearch_dsl import InnerDoc, Keyword, Text, Date, Integer


class BaseDocument(InnerDoc):
    id = Keyword()
    version = Integer()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    created_at = Date()
    updated_at = Date()

    body = []
