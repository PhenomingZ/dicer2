from docx import Document

import re
import jieba.analyse


class DocxLoader(object):
    def __init__(self, file):

        # load docx
        self.document = Document(file)

        # load text in docx
        self._text = []
        self._tags = []

        for paragraph in self.document.paragraphs:
            if not paragraph.text:
                continue

            sep_text = re.split(r"[。？！；]", paragraph.text)

            tmp = ""
            for sep in sep_text:

                line = sep.strip()
                if line:

                    tmp += line

                    if len(tmp) < 50:
                        continue

                    tmp += "。"
                    self._text.append(tmp)

                    tmp_tags = []
                    for tag in jieba.analyse.textrank(tmp, withWeight=False, topK=10):
                        tmp_tags.append(tag)
                    self._tags.append(tmp_tags)

                    tmp = ""

            if len(tmp) > 0:
                self._text.append(tmp)
                tmp_tags = []
                for tag in jieba.analyse.textrank(tmp, withWeight=False, topK=10):
                    tmp_tags.append(tag)
                self._tags.append(tmp_tags)

    @property
    def text(self):
        return self._text

    @property
    def tags(self):
        return self._tags
