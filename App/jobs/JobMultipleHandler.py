from elasticsearch_dsl.connections import connections

from App.controllers import BaseController
from App.jobs.JobSingleHandler import job_single_handler
from App.models import BaseTask, BaseDocument
from App.settings import get_config

from concurrent.futures import ThreadPoolExecutor

host = get_config().ELASTICSEARCH_HOST
connections.create_connection(hosts=[host])


def job_multiple_handler(source_range: dict, search_range: dict):
    pool = ThreadPoolExecutor(max_workers=4)

    res_list = list()

    for index_id, tasks in source_range.items():

        for task_id in tasks:
            task_instance: BaseTask = BaseController().get_task(index_id, task_id)

            for doc in task_instance.docs:
                document_id = doc.id
                document: BaseDocument = BaseController().get_document(index_id, task_id, document_id)

                res = pool.submit(job_single_handler, index_id, task_id, document_id, search_range, document.body)

                # 不能在这里把result添加到列表，会非常耗时
                res_list.append(res)

    pool.shutdown()

    for i in res_list:
        print(i.result())
