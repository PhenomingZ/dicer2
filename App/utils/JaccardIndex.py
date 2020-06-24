import jieba


class JaccardIndex(object):

    @classmethod
    def jaccard(cls, str1, str2):
        terms_reference = jieba.cut(str2)  # 默认精准模式
        terms_model = jieba.cut(str1)
        grams_reference = list(terms_reference)  # 去重；如果不需要就改为list
        grams_model = list(terms_model)
        temp = 0
        for i in grams_reference:
            if i in grams_model:
                temp = temp + 1
        union = len(grams_model) + len(grams_reference) - temp  # 并集
        jaccard_coefficient = float(temp / union)  # 交集
        return jaccard_coefficient
