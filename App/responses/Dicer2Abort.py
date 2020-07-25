from flask_restful import abort


def base_abort(status, msg, data):
    """
    中止请求执行的异常处理方法
    :param status: 异常码
    :param msg: 异常信息
    :param data: 异常数据
    :return:
    """

    meta = {
        "took": 0,
        "msg": msg,
        "status": status
    }

    abort(status, meta=meta, data=data)


def bad_request_abort(data):
    base_abort(400, "BAD REQUEST", data)


def forbidden_abort(data):
    base_abort(403, "FORBIDDEN", data)


def not_found_abort(data):
    base_abort(404, "NOT FOUND", data)


def internal_server_error_abort(data):
    base_abort(500, "INTERNAL SERVER ERROR", data)


def elastic_search_connection_refused_abort(data):
    base_abort(500, "ElasticSearch Connection Refused", data)
