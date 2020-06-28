from datetime import datetime

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from App.apis.Dicer2Resource import Dicer2Resource
from App.controllers import BaseController
from App.responses import OKResponse, NotFoundAbort
from App.settings import get_config
from App.utils.DocumentTools import DocumentTools
from App.utils.ImageSimilarity import p_hash_img_similarity
from App.utils.JaccardIndex import JaccardIndex


class SingleSearchResource(Dicer2Resource):

    @classmethod
    def get(cls):
        start_time = datetime.now()

        minimal_line_length = get_config().MINIMAL_LINE_LENGTH
        jaccard_threshold_value = get_config().JACCARD_THRESHOLD_VALUE
        image_hamming_threshold_value = get_config().IMAGE_HAMMING_THRESHOLD_VALUE

        index_id = cls.get_parameter("index", required=True, location=["json", "form"])
        task_id = cls.get_parameter("task", required=True, location=["json", "form"])
        document_id = cls.get_parameter("document", required=True, location=["json", "form"])
        search_range = cls.get_parameter("search_range", required=True, location=["json", "form"])

        doc_id = DocumentTools.get_doc_id(index_id, task_id, document_id)

        document = BaseController().get_document(index_id, task_id, document_id)
        body = document.body

        total_parts = len(body)
        total_valid_parts = 0

        document_result = []

        for line_num, line_with_mark in enumerate(body):
            mark, line = line_with_mark[0], line_with_mark[1]

            if mark == 0 and len(line) <= minimal_line_length:
                continue

            total_valid_parts += 1

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
                    try:
                        s = Search(index=index).query("match", body=line).filter("terms", task=tasks)
                        for hit in s:
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
                    except NotFoundError as e:
                        NotFoundAbort(e.info)
                elif mark == 1:
                    s = Search(index=index).query("match", is_image=True).filter("terms", task=tasks)
                    for hit in s.scan():
                        if hit.doc_id == doc_id:
                            continue

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
        if total_valid_parts == 0:
            repetitive_rate = 0
        else:
            repetitive_rate = len(document_result) / total_valid_parts

        response_data = dict(index=index_id, task=task_id, document=document_id, title=document.title,
                             repetitive_rate=repetitive_rate, result=document_result)
        return OKResponse(response_data, start_time)
