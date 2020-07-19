from App.apis.Dicer2Resource import Dicer2Resource

dicer2_version = "v0.2.0"
elastic_search_version = "7.6.2"


# TODO 在这里要检查ES集群的健康状态并返回
class MainResource(Dicer2Resource):
    """ DICER2主页 """

    @staticmethod
    def get():
        """
        The base information of dicer2
        ---
        tags:
          - Base API
        description:
          It shows dicer2 version and ElasticSearch cluster status
        responses:
          200:
            description: dicer2 basic information
            schema:
              properties:
                name:
                  type: string
                version:
                  type: object
                  properties:
                    dicer2_version:
                      type: string
                    elastic_search_version:
                      type: string
                msg:
                  type: string
         """

        return {
            "name": "Dicer2",
            "version": {
                "dicer2_version": dicer2_version,
                "elastic_search_version": elastic_search_version
            },
            "msg": "Check your documents cooler!"
        }
