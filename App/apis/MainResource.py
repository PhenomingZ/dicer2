from flask_restful import Resource

dicer2_version = "v0.1.3"
elastic_search_version = "7.6.2"


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
