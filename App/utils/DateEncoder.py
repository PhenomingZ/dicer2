import json
import datetime

from App.jobs.JobTypeEnums import JobStatus, JobType


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, JobStatus):
            return obj.value
        elif isinstance(obj, JobType):
            return obj.value
        else:
            return json.JSONEncoder.default(self, obj)

    @classmethod
    def jsonify(cls, data):
        return json.loads(json.dumps(data, cls=cls))

    @classmethod
    def save(cls, path, data):
        with open(path, "w") as fp:
            d = cls.jsonify(data)
            # TODO 将是否以ASCII码保存设置在配置文件中
            s = json.dumps(d, ensure_ascii=False)
            fp.write(s)
            fp.close()

    @classmethod
    def load(cls, path):
        with open(path, "r") as fp:
            data = json.load(fp)
            fp.close()
            return data


class Dicer2Encoder(DateEncoder):
    pass
