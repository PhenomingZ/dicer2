from flask_restful import abort


def BaseAbort(status, msg, data):
    """
    中止请求执行的异常处理方法
    :param status: 异常码
    :param msg: 异常信息
    :param data: 异常数据
    :return:
    """

    meta = {
        "took": -1,
        "msg": msg,
        "status": status
    }

    abort(status, meta=meta, data=data)


def BadRequestAbort(data):
    BaseAbort(400, "BAD REQUEST", data)


def ForbiddenAbort(data):
    BaseAbort(403, "FORBIDDEN", data)


def NotFoundAbort(data):
    BaseAbort(404, "NOT FOUND", data)


def InternalServerErrorAbort(data):
    BaseAbort(500, "INTERNAL SERVER ERROR", data)


def ElasticSearchConnectionRefusedAbort(data):
    BaseAbort(500, "ElasticSearch Connection Refused", data)
