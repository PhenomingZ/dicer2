from flask import Flask

from App.apis import init_api
from App.jobs import init_job
from App.ext import init_ext
from App.hooks import init_hook
from App.settings import init_config


def create_app(config):
    """
    创建新的app对象
    :param config: DICER2配置文件路径
    :return: 新建的app对象
    """

    app = Flask(__name__)

    app.config.from_pyfile(config)

    init_config(app)

    init_api(app)

    init_ext(app)

    init_hook(app)

    init_job(app)

    return app
