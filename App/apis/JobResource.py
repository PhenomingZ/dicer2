from flask_restful import Resource


# TODO 添加任务的相关配置项，可用于覆盖系统默认配置
class JobResource(Resource):
    """ Job相关资源接口基类 """

    class JobResultHandler(object):
        """ 将获取到的任务结果规范为响应格式 """

        def __init__(self, job_result):
            self.took = job_result.get("took")
            self.stat = job_result.get("status")
            self.data = job_result.get("data")
            self.type = self.data.get("job_type")

        def get_response_data(self):
            response_data = dict(
                took=self.took,
                status=self.stat,
            )
            response_data.update(self.data)

            return response_data
