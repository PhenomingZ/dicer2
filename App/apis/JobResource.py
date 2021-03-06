from App.apis.Dicer2Resource import Dicer2Resource


class JobResource(Dicer2Resource):
    """ Job相关资源接口基类 """

    class JobResultHandler(object):
        """ 将获取到的任务结果规范为响应格式 """

        def __init__(self, job_result):
            self.id = job_result.get("id")
            self.name = job_result.get("name")
            self.took = job_result.get("took")
            self.stat = job_result.get("status")
            self.data = job_result.get("data")
            self.start_time = job_result.get("start_time")
            self.end_time = job_result.get("end_time")
            self.type = self.data.get("job_type")

        def get_response_data(self):
            response_data = dict(
                id=self.id,
                name=self.name,
                took=self.took,
                status=self.stat,
                start_time=self.start_time,
                end_time=self.end_time
            )
            response_data.update(self.data)

            return response_data
