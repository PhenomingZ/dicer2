# 计算两个图片相似度函数局部敏感哈希算法
def p_hash_img_similarity(p_hash_1, p_hash_2):
    # 计算汉明距离
    distance = bin(p_hash_1 ^ p_hash_2).count('1')
    similarity = 1 - distance / max(len(bin(p_hash_1)), len(bin(p_hash_2)))
    return similarity
