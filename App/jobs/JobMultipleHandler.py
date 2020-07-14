import networkx as nx

from community import community_louvain
from elasticsearch_dsl.connections import connections

from App.controllers import BaseController
from App.jobs.JobSingleHandler import job_single_handler
from App.models import BaseTask, BaseDocument
from App.settings import get_config

from concurrent.futures import ThreadPoolExecutor

from App.utils.DocumentTools import DocumentTools

host = get_config().ELASTICSEARCH_HOST
connections.create_connection(hosts=[host])


def job_multiple_handler(progress_callback, source_range: dict, search_range: dict):
    pool = ThreadPoolExecutor(max_workers=4)

    # 查重结果的加权无向图（文档相关度取平均做权值）
    g = nx.Graph()

    # 本次被查重的文档对应的详细信息（source_range）
    source_map = dict()

    # 查重结果图中Key对应的详细信息（search_range）
    detail_map = dict()

    # 查重结果图中的Key对应的查重结果
    res_map = dict()

    for index_id, tasks in source_range.items():

        for task_id in tasks:
            task_instance: BaseTask = BaseController().get_task(index_id, task_id)

            for doc in task_instance.docs:
                document_id = doc.id
                document: BaseDocument = BaseController().get_document(index_id, task_id, document_id)

                res = pool.submit(job_single_handler, index_id, task_id, document_id, search_range, document.body)
                res.add_done_callback(progress_callback)

                # 不能在这里把result添加到列表，会非常耗时
                doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

                # 保证被查重的文档信息均被添加至图节点中
                g.add_node(doc_id)
                detail_map[doc_id] = {
                    "index": index_id,
                    "task": task_id,
                    "document": document_id
                }

                # 将source_range中的文档和search_range中的文档区分存放
                source_map[doc_id] = detail_map[doc_id]

                res_map[doc_id] = res

    # 等待线程池中所有任务完成
    pool.shutdown()

    for key in res_map.keys():
        index_id = detail_map.get(key).get("index")
        task_id = detail_map.get(key).get("task")
        document_id = detail_map.get(key).get("document")

        res = res_map.get(key).result()

        repetitive_rate = res[0]
        document_result = res[1]
        total_val_parts = res[2]

        similar_count = dict()

        for line in document_result:
            is_image = line.get("is_image")
            similar_list = line.get("similar")

            for similar in similar_list:
                similar_index_id = similar.get("index")
                similar_task_id = similar.get("task")
                similar_document_id = similar.get("document")

                similar_doc_id = DocumentTools.get_doc_id(similar_index_id, similar_task_id, similar_document_id)

                if similar_doc_id not in similar_count:
                    similar_count[similar_doc_id] = 0

                # 文档之间相似权重计算
                # 由于每一行文本或图片可能有多条数据与其相似，不同的相似数据相似程度不同
                # 所以采用图片相似度和文本的Jaccard系数来作为权重进行累加
                # 且由于每篇文档的长度也不同，最后要除文档的总有效分块数进行归一
                if is_image:
                    similar_count[similar_doc_id] += similar.get("similarity")
                else:
                    similar_count[similar_doc_id] += similar.get("jaccard")

                if similar_doc_id not in detail_map:
                    g.add_node(similar_doc_id)
                    detail_map[similar_doc_id] = {
                        "index": similar_index_id,
                        "task": similar_task_id,
                        "document": similar_document_id,
                    }

        for similar_key, similar_rank in similar_count.items():

            weight = similar_rank / total_val_parts
            if g.has_edge(key, similar_key):
                old_weight = g.get_edge_data(key, similar_key).get("weight")
                new_weight = (old_weight + weight) / 2
                g[key][similar_key]["weight"] = new_weight
            else:
                g.add_edge(key, similar_key, weight=weight)

    # edge_list = list()
    # for origin, destination, data in g.edges(data=True):
    #     origin_document_id = detail_map.get(origin).get("document")
    #     destination_document_id = detail_map.get(destination).get("document")
    #
    #     edge_list.append((origin_document_id, destination_document_id, data['weight']))
    #
    # edge_list.sort(key=lambda x: x[2], reverse=True)
    # for e in edge_list:
    #     print(e)

    # Louvain社群发现算法
    partition = community_louvain.best_partition(g)

    partition_cluster = dict()
    for doc_id, part in partition.items():
        if doc_id not in source_map:
            continue

        repetitive_rate = res_map.get(doc_id).result()[0]

        partition_cluster.setdefault(part, [])
        partition_cluster[part].append(("%.4f" % repetitive_rate, source_map.get(doc_id).get("document")))

    # for k, v in partition_cluster.items():
    #     v.sort(key=lambda x: x[0], reverse=True)
    #     print(f"类别{k}")
    #     print("==============")
    #     print(v)
