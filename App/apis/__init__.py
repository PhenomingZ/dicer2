from flask_restful import Api

from App.apis.DocumentsResource import DocumentsResource
from App.apis.IndexResource import IndexResource
from App.apis.MainResource import MainResource
from App.apis.SingleSearchResource import SingleSearchResource
from App.apis.TaskResource import TaskResource

api = Api()


def init_api(app):
    api.init_app(app)


# Main
api.add_resource(MainResource, "/", endpoint="main")

# CURD for index
api.add_resource(IndexResource, "/<string:index>/", endpoint="index")

# CURD for task
api.add_resource(TaskResource, "/<string:index>/<string:task>/", endpoint="task")

# CURD for document
api.add_resource(DocumentsResource, "/<string:index>/<string:task>/<string:document>/", endpoint="doc")

# Search for single document
api.add_resource(SingleSearchResource, "/single/_search/", endpoint="single_search")
