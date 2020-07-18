from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from App.settings import get_config
from App.utils.DocumentTools import DocumentTools
from App.utils.ImageSimilarity import p_hash_img_similarity
from App.utils.JaccardIndex import JaccardIndex

host = get_config().ELASTICSEARCH_HOST
connection = connections.create_connection(hosts=[host])


def job_single_handler(index_id, task_id, document_id, search_range, body):
    """
    单独查重任务处理函数
    :param index_id: 待查重文档的index
    :param task_id: 待查重文档的task
    :param document_id: 待查重文档的document
    :param search_range: 目标检索范围
    :param body: 待查重文档的全文
    :return: 重复比, 查重对应结果, 全部有效段落数, 待查重文档详细信息（用于回调函数）
    """

    minimal_line_length = get_config().MINIMAL_LINE_LENGTH
    jaccard_threshold_value = get_config().JACCARD_THRESHOLD_VALUE
    image_hamming_threshold_value = get_config().IMAGE_HAMMING_THRESHOLD_VALUE

    doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

    total_parts = len(body)
    total_val_parts = 0

    document_result = []

    for line_num, line_with_mark in enumerate(body):
        mark, line = line_with_mark[0], line_with_mark[1]

        if mark == 0 and len(line) <= minimal_line_length:
            continue

        total_val_parts += 1

        line_result = {
            "origin": line,
            "is_image": mark == 1,
            "part": line_num,
            "total": total_parts,
            "similar": []
        }

        for index in search_range.keys():
            tasks = search_range[index]

            if mark == 0:
                s = Search(using=connection, index=index).query("match", body=line).filter("terms", task=tasks)

                # TODO 在配置项中添加对ES结果的查询精度设置
                for hit in s[0:5]:
                    if hit.doc_id == doc_id or len(hit.body) <= minimal_line_length:
                        continue

                    jaccard_score = JaccardIndex.jaccard(line, hit.body)
                    if jaccard_score <= jaccard_threshold_value:
                        continue

                    line_result["similar"].append({
                        "score": hit.meta.score,
                        "jaccard": jaccard_score,
                        "index": hit.index,
                        "task": hit.task,
                        "document": hit.document,
                        "title": hit.title,
                        "body": hit.body,
                        "part": hit.part,
                        "total": hit.total
                    })
            elif mark == 1:
                s = Search(using=connection, index=index).query(
                    "match", is_image=True
                ).filter("terms", task=tasks).exclude('terms', doc_id=[doc_id])

                for hit in s.scan():
                    similarity = p_hash_img_similarity(hit.body, line)
                    if similarity >= image_hamming_threshold_value:
                        line_result["similar"].append({
                            "similarity": similarity,
                            "index": hit.index,
                            "task": hit.task,
                            "document": hit.document,
                            "title": hit.title,
                            "body": hit.body,
                            "part": hit.part,
                            "total": hit.total
                        })
        if line_result["similar"]:
            document_result.append(line_result)

    # 全文复制比
    if total_val_parts == 0:
        repetitive_rate = 0
    else:
        repetitive_rate = len(document_result) / total_val_parts

    document_detail = dict(index=index_id, task=task_id, document=document_id)

    return repetitive_rate, document_result, total_val_parts, document_detail
