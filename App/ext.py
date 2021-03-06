import jieba
from flasgger import Swagger

from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from App.apis.MainResource import DICER2_VERSION

template = {
    "swagger": "2.0",
    "info": {
        "title": "DICER2 API",
        "description": "API for DICER2 documents checker!",
        "contact": {
            "responsibleDeveloper": "Charles Zhang",
            "email": "694556046@qq.ccom",
            "url": "https://gitee.com/phenoming",
        },
        "version": DICER2_VERSION
    },
    "host": "localhost:9605",
    "basePath": "/",
    "schemes": [
        "http"
    ]
}

# swagger 生成的文档可以访问`/apispec_1.json`获取JSON原始数据
# 再拷贝到Swagger Editor中即可导出文档
swagger = Swagger(template=template)

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    """
    初始化拓展模块
    :param app: DICER2使用的app对象
    :return:
    """

    jieba.initialize()

    # swagger会自动添加路由'/apidocs/'
    swagger.init_app(app)

    if app.config["ENABLE_CORS"]:
        CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
