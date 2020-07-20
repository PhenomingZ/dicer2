from App.apis.Dicer2Resource import Dicer2Resource

from flasgger import swag_from

dicer2_version = "v0.2.0"
elastic_search_version = "7.6.2"


# TODO 在这里要检查ES集群的健康状态并返回
class MainResource(Dicer2Resource):
    """ DICER2主页 """

    @staticmethod
    @swag_from("../docs/basic_api_main.yaml")
    def get():
        return {
            "name": "Dicer2",
            "version": {
                "dicer2_version": dicer2_version,
                "elastic_search_version": elastic_search_version
            },
            "msg": "Check your documents cooler!"
        }
