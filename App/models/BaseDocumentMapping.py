from elasticsearch_dsl import InnerDoc, Keyword, Text, Date, Integer


class BaseDocument(InnerDoc):
    """ Document信息存入'.dicer2_base'基本数据库的字段结构和操作方法 """

    id = Keyword()
    version = Integer()
    title = Text(analyzer="ik_max_word", search_analyzer="ik_smart")
    created_at = Date()
    updated_at = Date()

    body = Text()
