from datetime import datetime
from flasgger import swag_from

from App.apis.Dicer2Resource import Dicer2Resource
from App.models import Base
from App.responses import OKResponse
from App.utils.DateEncoder import Dicer2Encoder


class SummaryResource(Dicer2Resource):
    """ 文档存储概览资源相关接口 """

    @classmethod
    @swag_from("../docs/basic_api/basic_api_summary.yaml")
    def get(cls):
        """
        获取存储在数据库中的文档概览
        :return: 获取成功响应
        """
        start_time = datetime.now()

        dicer2_base = Base.get(id="dicer2")

        # 使用自定义的JSON编码器将日期类型转化为JSON可读类型，在用json,loads转化为Response可读的JSON类型
        index_list = [Dicer2Encoder.jsonify(i.to_dict()) for i in dicer2_base.index]

        response_data = dict(index_count=dicer2_base.index_count, indexs=index_list)
        return OKResponse(data=response_data, start_time=start_time)
