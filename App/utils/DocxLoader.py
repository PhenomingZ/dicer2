import os
from functools import reduce
from os.path import basename

from PIL import Image
from docx import Document

import re
import pygrading as gg


class DocxLoader(object):
    """ Docx文件读取器 """

    def __init__(self, file):
        """
        初始化文件读取器
        :param file: docx文件的文件流
        """

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
        """
        :return: docx文档的全文
        """

        return self._text

    # 计算图片的局部哈希值--pHash
    @classmethod
    def p_hash(cls, img):
        """
        计算图片的pHash值
        :param img: 图片的文件流
        :return: 图片的pHash值
        """

        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
        hash_value = reduce(lambda x, y: x | (y[1] << y[0]),
                            enumerate(
                                map(lambda i: 0 if i < avg else 1, img.getdata())),
                            0)
        return hash_value

    def test_handler(self, text):
        """
        文本处理方法，将长句拆分为短句
        :param text: 未处理的长句子
        :return:
        """

        sep_text = re.split(r"[。？！；]", text)

        tmp = ""
        for sep in sep_text:

            line = sep.strip()

            tmp_line = ""
            for character in line:
                if character not in "œ∑®†¥øπåß∂ƒ©˙∆˚¬≈ç√µ≤≥¡™£¢∞§¶•ªº":
                    tmp_line += character

            line = tmp_line

            if line:

                tmp += line

                if len(tmp) < 50:
                    tmp += "，"
                    continue

                tmp += "。"

                # 添加一个元组，第一项是0代表纯文本，第二项是文本内容
                self._text.append((0, tmp))

                tmp = ""

        if len(tmp) > 0:
            self._text.append((0, tmp))

    def image_handler(self, images):
        """
        图片处理方法，将图片转换为pHash保存
        :param images: docx中获取的图片
        :return:
        """

        for image in images:
            for embed in image.xpath('.//a:blip/@r:embed'):
                part = self.document.part.related_parts[embed]

                with open(basename(part.partname), 'wb') as fp:
                    fp.write(part.blob)
                    fp.close()

                img = Image.open(basename(part.partname))

                ocr_result = gg.exec(
                    "python test/OCR/test_ocr.py", basename(part.partname))

                print(ocr_result.stdout)

                result_img = "result_" + basename(part.partname)

                img_ocr_text = ""

                if ocr_result.returncode:
                    base64 = gg.utils.img2base64(basename(part.partname))
                else:
                    base64 = gg.utils.img2base64(result_img)

                    text_path = "text_" + basename(part.partname)
                    img_ocr_text = gg.utils.readfile(text_path)

                    os.remove(result_img)
                    os.remove(text_path)

                os.remove(basename(part.partname))

                try:
                    image_hash = self.p_hash(img)
                except OSError:
                    continue

                # 添加一个元组，第一项是1代表图片，第二项是图片的hash值，第三项是图像的base64，第四项是识别出的文字
                self._text.append((1, image_hash, base64, img_ocr_text))
