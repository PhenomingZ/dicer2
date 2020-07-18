from App.apis.Dicer2Resource import Dicer2Resource

dicer2_version = "v0.2.0"
elastic_search_version = "7.6.2"


# TODO 在这里要检查ES集群的健康状态并返回
class MainResource(Dicer2Resource):
    """ DICER2主页 """

    @staticmethod
    def get():
        """
        获取DICER2的基本信息
        :return: DICER2的基本信息
        """
        return {
            "name": "Dicer2",
            "version": {
                "dicer2_version": dicer2_version,
                "elastic_search_version": elastic_search_version
            },
            "msg": "Check your documents cooler!"
        }
