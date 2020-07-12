from flask_restful import Resource

dicer2_version = "v0.2.0"
elastic_search_version = "7.6.2"


# TODO 在这里要检查ES集群的健康状态并返回
class MainResource(Resource):

    @staticmethod
    def get():
        return {
            "name": "Dicer2",
            "version": {
                "dicer2_version": dicer2_version,
                "elastic_search_version": elastic_search_version
            },
            "msg": "Check your documents cooler!"
        }
