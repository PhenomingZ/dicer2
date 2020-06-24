from elasticsearch.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError

from App.hooks.ElasticConnectionCheckHook import init_elastic_connection
from App.responses import ElasticSearchConnectionRefusedAbort


def init_hook(app):
    @app.before_first_request
    def before_first():
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
        if response.status_code == 500:
            ElasticSearchConnectionRefusedAbort("(Runtime Error) Elastic connection refused!")
        return response
