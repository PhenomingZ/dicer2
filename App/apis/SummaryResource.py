from datetime import datetime

from App.apis.Dicer2Resource import Dicer2Resource
from App.models import Base
from App.responses import OKResponse
from App.utils.DateEncoder import Dicer2Encoder


class SummaryResource(Dicer2Resource):

    @classmethod
    def get(cls):
        start_time = datetime.now()

        dicer2_base = Base.get(id="dicer2")

        # 使用自定义的JSON编码器将日期类型转化为JSON可读类型，在用json,loads转化为Response可读的JSON类型
        index_list = [Dicer2Encoder.jsonify(i.to_dict()) for i in dicer2_base.index]

        response_data = dict(index_count=dicer2_base.index_count, index=index_list)
        return OKResponse(data=response_data, start_time=start_time)
