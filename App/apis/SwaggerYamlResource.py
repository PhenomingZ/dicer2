from flask import send_from_directory
import os

from flask_restful import Resource

YAML_PATH = os.path.join(os.getcwd(), "App", "docs")


class SwaggerYamlResource(Resource):

    @classmethod
    def get(cls, filename):
        """
        获取yaml文档标注文件
        :param filename: 文件名
        :return:
        """
        return send_from_directory(YAML_PATH, filename)
