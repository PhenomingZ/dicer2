class DocumentTools(object):
    @classmethod
    def get_doc_id(cls, index_id, task_id, document_id):
        return index_id + "-" + task_id + "-" + document_id
