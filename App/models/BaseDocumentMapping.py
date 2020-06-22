from elasticsearch_dsl import InnerDoc, Keyword, Text, Date


class BaseDocument(InnerDoc):
    id = Keyword()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    create_at = Date()

    body = []
