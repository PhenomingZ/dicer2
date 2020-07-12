import jieba
from flasgger import Swagger
from flask_cors import CORS

swagger = Swagger()


def init_ext(app):
    jieba.initialize()

    swagger.init_app(app)

    if app.config["ENABLE_CORS"]:
        CORS(app)
