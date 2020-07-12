from flask_restful import abort


def BaseAbort(status, msg, data):
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
