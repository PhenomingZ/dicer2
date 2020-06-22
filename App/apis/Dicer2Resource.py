import json
from json import JSONDecodeError

from flask import request
from flask_restful import Resource

from App.responses import BadRequestAbort


class Dicer2Resource(Resource):

    @classmethod
    def get_parameter(cls, key, default_value=None, required=False, location=None):

        if isinstance(location, str):
            location = [location]
        elif location and not isinstance(location, list):
            BadRequestAbort("location in 'get_parameter' needs a string or list instance!")

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
            BadRequestAbort("JSONDecodeError: " + e.msg)

        search_range = location if location else locations.keys()

        for loc in search_range:
            if key in locations[loc]:
                return locations[loc].get(key)

        if required and not default_value:
            BadRequestAbort(f"Key '{key}' is not found in the request body.")

        return default_value
