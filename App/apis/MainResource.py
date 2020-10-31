from App.apis.Dicer2Resource import Dicer2Resource

from flasgger import swag_from

import requests

from App.settings import get_config

dicer2_version = "v0.2.2"

config = get_config()


class MainResource(Dicer2Resource):
    """ DICER2主页 """

    @staticmethod
    @swag_from("../docs/basic_api/basic_api_main.yaml")
    def get():

        try:
            response = requests.request("GET", f"http://{config.ELASTICSEARCH_HOST}:9200/")
            elastic_details = response.json()
            elastic_details.pop("tagline")
            elastic_connect = "Available"
        except Exception as e:
            elastic_connect = "NOT Available"
            elastic_details = dict()
            print(e)

        return {
            "name": "Dicer2",
            "version": dicer2_version,
            "elastic_connect": elastic_connect,
            "elastic_details": elastic_details,
            "tagline": "More then a document."
        }
