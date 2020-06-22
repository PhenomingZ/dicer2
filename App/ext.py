import jieba
from flasgger import Swagger

swagger = Swagger()


def init_ext(app):
    jieba.initialize()

    swagger.init_app(app)
