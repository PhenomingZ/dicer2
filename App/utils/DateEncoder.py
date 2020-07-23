import json
import datetime

from App.jobs.JobTypeEnums import JobStatus, JobType
from App.settings import get_config


class DateEncoder(json.JSONEncoder):
    """ DICER2的JSON解析基类 """

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
        """
        将Python中包含特殊类型的数据解析为普通Python数据类型
        :param data: 包含特殊类型的数据
        :return:
        """

        return json.loads(json.dumps(data, cls=cls))

    @classmethod
    def save(cls, path, data):
        """
        将Python数据以JSON格式保存在文件中
        :param path: 保存的目标路径
        :param data: 待保存的数据
        :return:
        """

        with open(path, "w") as fp:
            d = cls.jsonify(data)
            s = json.dumps(d, ensure_ascii=get_config().ENSURE_ASCII)
            fp.write(s)
            fp.close()

    @classmethod
    def load(cls, path):
        """
        从文件中读取JSON数据
        :param path: 文件路径
        :return: JSON格式数据
        """

        with open(path, "r") as fp:
            data = json.load(fp)
            fp.close()
            return data


class Dicer2Encoder(DateEncoder):
    """ DICER2的JSON解析类 """

    pass
