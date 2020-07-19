from flask import send_from_directory
import os

from flask_restful import Resource

STATIC_PATH = os.path.join(os.getcwd(), "static")


class StaticFileResource(Resource):

    @classmethod
    def get(cls, filename):
        """
        获取静态文件
        :param filename: 文件名
        :return:
        """
        return send_from_directory(STATIC_PATH, filename)
