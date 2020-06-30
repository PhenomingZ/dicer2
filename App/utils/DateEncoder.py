import json
import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

    @classmethod
    def jsonify(cls, data):
        return json.loads(json.dumps(data, cls=cls))

    @classmethod
    def save(cls, path, data):
        with open(path, "w") as fp:
            d = cls.jsonify(data)
            s = json.dumps(d)
            fp.write(s)
            fp.close()
