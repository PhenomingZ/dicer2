import json
from datetime import datetime

from flask import Response


class Dicer2Response(Response):
    msg = "OK"
    charset = 'utf-8'
    default_status = 200
    default_mimetype = "application/json"

    def __init__(self, data, start_time, **kwargs):

        response = json.dumps({
            "meta": {
                "took": int((datetime.now() - start_time).total_seconds() * 1000),
                "msg": self.msg,
                "status": self.default_status
            },
            "data": data
        })

        super().__init__(response, **kwargs)


class OKResponse(Dicer2Response):
    msg = "OK"
    default_status = 200


class UpdatedResponse(Dicer2Response):
    msg = "UPDATED"
    default_status = 200


class DeletedResponse(Dicer2Response):
    msg = "DELETED"
    default_status = 200


class CreatedResponse(Dicer2Response):
    msg = "CREATED"
    default_status = 201


class BadRequestResponse(Dicer2Response):
    msg = "BAD REQUEST"
    default_status = 400


class ForbiddenResponse(Dicer2Response):
    msg = "FORBIDDEN"
    default_status = 403


class NotFoundResponse(Dicer2Response):
    msg = "NOT FOUND"
    default_status = 404
