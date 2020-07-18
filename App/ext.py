import jieba
from flasgger import Swagger
from flask_cors import CORS

swagger = Swagger()


def init_ext(app):
    """
    初始化拓展模块
    :param app: DICER2使用的app对象
    :return:
    """

    jieba.initialize()

    swagger.init_app(app)

    if app.config["ENABLE_CORS"]:
        CORS(app)
