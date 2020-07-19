from flask_restful import Api

from App.apis.MultipleSearchResource import MultipleSearchResource
from App.apis.StaticFileResource import StaticFileResource
from App.apis.SwaggerYamlResource import SwaggerYamlResource
from App.apis.VersionsResource import VersionsResource
from App.apis.DocumentsResource import DocumentsResource
from App.apis.IndexResource import IndexResource
from App.apis.MainResource import MainResource
from App.apis.SingleSearchResource import SingleSearchResource
from App.apis.SummaryResource import SummaryResource
from App.apis.TaskResource import TaskResource
from App.apis.JobResultResource import JobResultResource

api = Api()


def init_api(app):
    """
    初始化接口
    :param app: DICER2使用的app对象
    :return:
    """
    api.init_app(app)


# Main
api.add_resource(MainResource, "/", endpoint="main")

# Summary of dicer2
api.add_resource(SummaryResource, "/_summary/", endpoint="_summary")

# Static file visit
api.add_resource(StaticFileResource, "/_file/<string:filename>/", endpoint="_file")

# Swagger yaml file visit
api.add_resource(SwaggerYamlResource, "/_swagger/<string:filename>/", endpoint="_swagger")

# Versions view of document
api.add_resource(VersionsResource, "/_versions/<string:index>/<string:task>/<string:document>/", endpoint="_versions")

# CURD for index
api.add_resource(IndexResource, "/<string:index>/", endpoint="index")

# CURD for task
api.add_resource(TaskResource, "/<string:index>/<string:task>/", endpoint="task")

# CURD for document
api.add_resource(DocumentsResource, "/<string:index>/<string:task>/<string:document>/", endpoint="doc")

# Search for single document
api.add_resource(SingleSearchResource, "/_search/_single/", endpoint="single_search")

# Search for multiple documents
api.add_resource(MultipleSearchResource, "/_search/_multiple/", endpoint="multiple_search")

# GET job result
api.add_resource(JobResultResource, "/_job/<string:job_id>/", endpoint="_job")

# TODO 添加重新加载配置项的API
