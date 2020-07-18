from elasticsearch.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError

from App.hooks.ElasticConnectionCheckHook import init_elastic_connection
from App.responses import ElasticSearchConnectionRefusedAbort, InternalServerErrorAbort


def init_hook(app):
    """
    初始化钩子函数
    :param app: DICER2使用的app对象
    :return:
    """

    @app.before_first_request
    def before_first():
        """
        第一次接收请求时尝试初始化对ElasticSearch的连接
        :return:
        """
        try:
            init_elastic_connection(app)
        except ConnectionRefusedError:
            ElasticSearchConnectionRefusedAbort("(Init Error) Elastic connection refused!")
        except NewConnectionError:
            ElasticSearchConnectionRefusedAbort("(Init Error) Failed to establish a new connection to ElasticSearch")
        except ConnectionError:
            ElasticSearchConnectionRefusedAbort("(Init Error) Failed to connect to ElasticSearch")

    @app.after_request
    def after_request(response):
        """
        请求返回时检查是否出现500内部错误
        :param response: 请求返回对象
        :return:
        """
        if response.status_code == 500:
            InternalServerErrorAbort("(Runtime Error) DICER2 has a internal server error!")
        return response
