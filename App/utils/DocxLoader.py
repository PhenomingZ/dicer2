import os
from functools import reduce
from os.path import basename

from PIL import Image
from docx import Document

import re


class DocxLoader(object):
    def __init__(self, file):

        # load docx
        self.document = Document(file)

        # load text in docx
        self._text = []

        for paragraph in self.document.paragraphs:
            text = paragraph.text
            images = paragraph._element.xpath('.//pic:pic')

            if text:
                self.test_handler(text)

            if len(images) > 0:
                self.image_handler(images)

    @property
    def text(self):
        return self._text

    # 计算图片的局部哈希值--pHash
    @classmethod
    def p_hash(cls, img):
        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
        hash_value = reduce(lambda x, y: x | (y[1] << y[0]),
                            enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
                            0)
        return hash_value

    def test_handler(self, text):
        sep_text = re.split(r"[。？！；]", text)

        tmp = ""
        for sep in sep_text:

            line = sep.strip()
            if line:

                tmp += line

                if len(tmp) < 50:
                    continue

                tmp += "。"

                # 添加一个元组，第一项是0代表纯文本，第二项是文本内容
                self._text.append((0, tmp))

                tmp = ""

        if len(tmp) > 0:
            self._text.append((0, tmp))

    def image_handler(self, images):
        for image in images:
            for embed in image.xpath('.//a:blip/@r:embed'):
                part = self.document.part.related_parts[embed]

                with open(basename(part.partname), 'wb') as fp:
                    fp.write(part.blob)
                    fp.close()

                img = Image.open(basename(part.partname))

                os.remove(basename(part.partname))

                try:
                    image_hash = self.p_hash(img)
                except OSError:
                    continue

                # 添加一个元组，第一项是1代表图片，第二项是图片的hash值
                self._text.append((1, image_hash))
