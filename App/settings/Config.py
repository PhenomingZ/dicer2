class Config(object):
    """ DICER2配置类 """

    # 更新配置表之后，需要更新`SettingResource.py`和`setting_api`中的yaml文件
    ELASTICSEARCH_HOST = "localhost"
    MINIMAL_LINE_LENGTH = 25
    JACCARD_THRESHOLD_VALUE = 0.45
    IMAGE_HAMMING_THRESHOLD_VALUE = 0.8
    DICER2_STORAGE_PATH = "./store"
    JOB_PROCESSING_NUM = 4
    ENABLE_CORS = False
    ENABLE_ERROR_TRACEBACK = False
    ENSURE_ASCII = True
    SEARCH_PRECISION = 5
