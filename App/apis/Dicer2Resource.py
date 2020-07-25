import json
from json import JSONDecodeError

from flask import request
from flask_restful import Resource

from App.responses import bad_request_abort


class Dicer2Resource(Resource):
    """ DICER2所有Resource的父类 """

    @classmethod
    def get_parameter(cls, key, default_value=None, required=False, location=None, data_type=None):
        """
        DICER2获取请求中的参数的类方法
        :param key: 请求的参数名
        :param default_value: 请求的参数的默认值
        :param required: 请求的参数是否必须
        :param location: 请求的参数位于请求体的位置
        :param data_type: 返回数据的类型，支持字符串转数字
        :return: 请求参数的值
        """

        if isinstance(location, str):
            location = [location]
        elif location and not isinstance(location, list):
            bad_request_abort("location in 'get_parameter' needs a string or list instance!")

        locations = {
            "args": None,
            "json": None,
            "form": None,
            "file": None,
            "headers": None,
            "cookies": None
        }

        try:
            locations["args"] = request.args
            locations["json"] = json.loads(request.data) if request.data else dict()
            locations["form"] = request.form.to_dict()
            locations["file"] = request.files
            locations["headers"] = request.headers
            locations["cookies"] = request.cookies
        except JSONDecodeError as e:
            bad_request_abort("JSONDecodeError: " + e.msg)

        search_range = location if location else locations.keys()

        for loc in search_range:
            if key in locations[loc]:

                value = locations[loc].get(key)

                try:
                    if data_type == "string":
                        return str(value)
                    elif data_type == "integer":
                        return int(value)
                    elif data_type == "float":
                        return float(value)
                    elif data_type == "boolean":
                        return bool(value)
                    else:
                        return value
                except ValueError:
                    bad_request_abort(f"Parameter '{key}' with value '{value}' can not convert to '{data_type}'")

        if required and not default_value:
            bad_request_abort(f"Key '{key}' is not found in the request body.")

        return default_value
