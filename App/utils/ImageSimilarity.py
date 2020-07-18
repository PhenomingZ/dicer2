def p_hash_img_similarity(p_hash_1, p_hash_2):
    """
    计算两个图片相似度函数局部敏感哈希算法
    :param p_hash_1: 图片1的pHash
    :param p_hash_2: 图片2的pHash
    :return:
    """

    # 计算汉明距离
    distance = bin(p_hash_1 ^ p_hash_2).count('1')
    similarity = 1 - distance / max(len(bin(p_hash_1)), len(bin(p_hash_2)))
    return similarity
