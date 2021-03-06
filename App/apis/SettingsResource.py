import shutil
import re
from datetime import datetime

from flasgger import swag_from

from App.apis.Dicer2Resource import Dicer2Resource
from App.responses import UpdatedResponse, OKResponse

from App.settings import get_config


def refresh_config(key, value):
    """
    更新配置文件
    :param key: 配置项
    :param value: 配置项的值
    :return:
    """
    if not value:
        return

    config_path = "App/settings/dicer2_config.py"

    fp = open(config_path, 'r')
    body = fp.read()
    fp.close()

    s = re.sub(f"{key} = .*", f"{key} = {value}", body, 1)
    fp = open(config_path, 'w')
    fp.write(s)
    fp.close()

    print(f"Config '{key}' is updated to '{value}', the service needs to be restarted to take effect")


class SettingsResource(Dicer2Resource):

    @classmethod
    @swag_from("../docs/setting_api/setting_api_get.yaml")
    def get(cls):
        """
        获取全局配置信息
        :return:
        """
        start_time = datetime.now()

        config = get_config()

        config_dic = config.__dict__

        # 直接读取到的config是一个包含冗余信息的对象，需要去除
        pop_key = ["os"]
        for k, v in config.__dict__.items():
            if "__" in k:
                pop_key.append(k)

        for k in pop_key:
            config_dic.pop(k)

        return OKResponse(data=config_dic, start_time=start_time)

    @classmethod
    @swag_from("../docs/setting_api/setting_api_default.yaml")
    def put(cls):
        """
        恢复默认配置，部分需要重启服务生效
        :return:
        """
        start_time = datetime.now()

        shutil.copyfile("App/settings/dicer2_config_default.py", "App/settings/dicer2_config.py")

        response_data = dict(msg="Restore default settings success, the service needs to be restarted to take effect")
        return UpdatedResponse(data=response_data, start_time=start_time)

    @classmethod
    @swag_from("../docs/setting_api/setting_api_update.yaml")
    def patch(cls):
        """
        更改全局配置，会修改配置文件，部分需要重启服务生效
        :return:
        """
        start_time = datetime.now()

        # 需要重启后生效
        elasticsearch_host = cls.get_parameter("ELASTICSEARCH_HOST", location=["json", "form"])
        if elasticsearch_host:
            elasticsearch_host = f"\"{elasticsearch_host}\""
        refresh_config("ELASTICSEARCH_HOST", elasticsearch_host)

        minimal_line_length = cls.get_parameter("MINIMAL_LINE_LENGTH", location=["json", "form"])
        refresh_config("MINIMAL_LINE_LENGTH", minimal_line_length)

        jaccard_threshold_value = cls.get_parameter("JACCARD_THRESHOLD_VALUE", location=["json", "form"])
        refresh_config("JACCARD_THRESHOLD_VALUE", jaccard_threshold_value)

        image_hamming_threshold_value = cls.get_parameter("IMAGE_HAMMING_THRESHOLD_VALUE", location=["json", "form"])
        refresh_config("IMAGE_HAMMING_THRESHOLD_VALUE", image_hamming_threshold_value)

        dicer2_storage_path = cls.get_parameter("DICER2_STORAGE_PATH", location=["json", "form"])
        if dicer2_storage_path:
            dicer2_storage_path = f"\"{dicer2_storage_path}\""
        refresh_config("DICER2_STORAGE_PATH", dicer2_storage_path)

        # 需要重启后生效
        job_processing_num = cls.get_parameter("JOB_PROCESSING_NUM", location=["json", "form"])
        refresh_config("JOB_PROCESSING_NUM", job_processing_num)

        # 需要重启后生效
        enable_cors = cls.get_parameter("ENABLE_CORS", location=["json", "form"])
        if enable_cors == "true":
            enable_cors = "True"
        if enable_cors == "false":
            enable_cors = "False"
        refresh_config("ENABLE_CORS", enable_cors)

        enable_error_traceback = cls.get_parameter("ENABLE_ERROR_TRACEBACK", location=["json", "form"])
        if enable_error_traceback == "true":
            enable_error_traceback = "True"
        if enable_error_traceback == "false":
            enable_error_traceback = "False"
        refresh_config("ENABLE_ERROR_TRACEBACK", enable_error_traceback)

        ensure_ascii = cls.get_parameter("ENSURE_ASCII", location=["json", "form"])
        if ensure_ascii == "true":
            ensure_ascii = "True"
        if ensure_ascii == "false":
            ensure_ascii = "False"
        refresh_config("ENSURE_ASCII", ensure_ascii)

        search_precision = cls.get_parameter("SEARCH_PRECISION", location=["json", "form"])
        refresh_config("SEARCH_PRECISION", search_precision)

        response_data = dict(msg="Update settings success")
        return UpdatedResponse(data=response_data, start_time=start_time)
