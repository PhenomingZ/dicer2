import hashlib


class DocumentTools(object):
    @classmethod
    def get_doc_id(cls, index_id, task_id, document_id):
        hl = hashlib.md5()
        src = index_id
        hl.update(src.encode("utf-8"))
        src = hl.hexdigest() + task_id
        hl.update(src.encode("utf-8"))
        src = hl.hexdigest() + document_id
        hl.update(src.encode("utf-8"))

        return hl.hexdigest()
